"""Calibrate the canopy storage coefficient s (mm per unit LAI) of the runoff module on field data.

Data: Anys & Weiler (2024) throughfall/stemflow dataset, FreiDok plus 242951, CC BY-NC 4.0
      (16 urban Acer platanoides / Tilia cordata in Freiburg, Apr-Sep 2021, 10-min resolution; TREES.csv has measured LAI, PAI).
Period: 1 Apr - 30 Sep 2021 (leaf-on, as in the paper). Reference gauge NA = no tips = 0 mm.
Model (as in scripts/runoff_model.py): event interception I = min(P, S), S = s * LAI.
Steps: events = rain on the open gauge (THF_ref) separated by >= 6 h dry; I_obs = P - throughfall (stemflow < 1%, ignored);
       per tree fit S (least squares on events with P >= 1 mm); then s = S / LAI (and S / PAI) per tree.
Output: databases/traits/interception_calibration.csv, notes/figures/interception_calibration.png
"""
import pathlib, numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / "databases/traits/raw/anys_weiler_2024"
trees = pd.read_csv(D / "TREES.csv", sep=";", skiprows=[1])
trees = trees.set_index("Tee")
x = pd.read_csv(D / "DATA_TF_SF_10min.csv", parse_dates=["TIMESTAMP_TZ"], na_values="NA")
x = x[(x.TIMESTAMP_TZ >= "2021-04-01") & (x.TIMESTAMP_TZ < "2021-10-01")].copy()   # leaf-on season used in the paper
x["THF_ref"] = x.THF_ref.fillna(0)                                 # reference logs only tips: NA = no rain
rain = x.THF_ref.fillna(0)
wet = rain > 0
gap = (~wet).astype(int).groupby(wet.cumsum()).cumsum()           # consecutive dry steps
x["event"] = (wet & (gap.shift(fill_value=99) >= 36)).cumsum()     # new event after >= 6 h (36 x 10 min) dry
x = x[x.event > 0]
ids = [c for c in x.columns if c[:3] in {"GTS", "HHS", "IVM", "JCS", "SMS", "SWB", "TUF", "URS"}]
ev = x.groupby("event").agg(P=("THF_ref", "sum"), start=("TIMESTAMP_TZ", "min"), steps=("THF_ref", "size"))
rows = []
for tr in ids:
    g = x.groupby("event")[tr].agg(["sum", "count"])
    g = g.reindex(ev.index)
    full = g["count"] == ev.steps                                    # tree recorded for the whole event
    e = ev[full].assign(TF=g["sum"][full])
    e = e[(e.P >= 1.0) & (e.TF <= 1.5 * e.P)]                        # drop funnelling/clogging artefacts
    I = (e.P - e.TF).values
    P = e.P.values

    def sse(S):
        return ((np.minimum(P, S) - I) ** 2).sum()

    S = minimize_scalar(sse, bounds=(0, 20), method="bounded").x
    pred = np.minimum(P, S)
    rows.append(dict(tree=tr, species=trees.loc[tr, "Tree_species"], LAI=trees.loc[tr, "LAI"], PAI=trees.loc[tr, "PAI"],
                     n_events=len(e), P_total=P.sum().round(1), interception_pct=round(100 * I.sum() / P.sum(), 1),
                     S_fit_mm=round(S, 2), s_per_LAI=round(S / trees.loc[tr, "LAI"], 3), s_per_PAI=round(S / trees.loc[tr, "PAI"], 3),
                     rmse_mm=round(np.sqrt(((pred - I) ** 2).mean()), 2), bias_mm=round((pred - I).mean(), 2)))
r = pd.DataFrame(rows)
r.to_csv(ROOT / "databases/traits/interception_calibration.csv", index=False)
print(f"Apr-Sep 2021: {len(ev)} events, {int((ev.P >= 1).sum())} with P >= 1 mm; open-gauge total {ev.P.sum():.0f} mm")
print(r.to_string(index=False))
for sp, g in r.groupby("species"):
    print(f"{sp}: S {g.S_fit_mm.median():.2f} mm, s per LAI median {g.s_per_LAI.median():.3f} (IQR {g.s_per_LAI.quantile(.25):.3f}-{g.s_per_LAI.quantile(.75):.3f})")
print(f"pooled: s per LAI median {r.s_per_LAI.median():.3f}, s per PAI median {r.s_per_PAI.median():.3f}; "
      f"slope through origin S~LAI = {(r.S_fit_mm * r.LAI).sum() / (r.LAI ** 2).sum():.3f}")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
for sp, g in r.groupby("species"):
    ax[0].scatter(g.LAI, g.S_fit_mm, label=sp)
k = (r.S_fit_mm * r.LAI).sum() / (r.LAI ** 2).sum()
xx = np.linspace(0, r.LAI.max() * 1.1, 10)
ax[0].plot(xx, k * xx, "k--", label=f"S = {k:.2f} x LAI")
ax[0].set_xlabel("Measured LAI (TLS)")
ax[0].set_ylabel("Fitted canopy storage S (mm)")
ax[0].legend()
tr = r.iloc[0].tree
g = x.groupby("event")[tr].sum()
e = ev.assign(TF=g)
e = e[e.P >= 1]
ax[1].scatter(e.P, e.P - e.TF, s=10, label=f"observed ({tr})")
pp = np.linspace(0, e.P.max(), 50)
ax[1].plot(pp, np.minimum(pp, r.iloc[0].S_fit_mm), "r-", label="bucket model")
ax[1].set_xlabel("Event rainfall P (mm)")
ax[1].set_ylabel("Interception P - TF (mm)")
ax[1].legend()
fig.suptitle("Calibration of canopy storage on Anys & Weiler (2024) Freiburg data (CC BY-NC 4.0)")
fig.savefig(ROOT / "notes/figures/interception_calibration.png", dpi=130, bbox_inches="tight")
