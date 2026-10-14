"""Exploratory bracket (issue #2): can design-storm runoff tell street-tree species palettes apart?

Usage:  python scripts/explore_runoff_sensitivity.py      (plain pandas + numpy; reads repo CSVs only, no network, no rasters)
Writes: databases/barcelona/runoff_sensitivity_palettes.csv  (long table: palette x crown x s x LAI x P)
        databases/barcelona/runoff_sensitivity_spread.csv    (palette spread vs parameter spread per P)
Status: EXPLORATORY BRACKET, not a result. It does NOT replace scripts/runoff_model.py (1 m grid); it re-does the same
arithmetic on aggregates so that palettes, s, LAI, crown size and P can be swept in seconds.

Arithmetic (same buckets as runoff_model.py lines 87-104, methodology section 4b):
  tree i: crown disk area A_i = pi/4 D_i^2, storage S_i = s * LAI_i, interception I_i = min(P, S_i)   [mm of depth over the crown]
  canopy_storage_m3 = sum A_i * I_i / 1000
  runoff_reduction_m3 = sum A_i * (Q98(P) - Q98(P - I_i)) / 1000   (SCS-CN, CN 98)
  Q(P) = (P - 0.2S')^2 / (P + 0.8S') for P > 0.2S', S' = 25.4 (1000/CN - 10)
ASSUMPTIONS (everything not read from a repo CSV):
  - every crown sits on sealed open space, CN 98 (TR-55 impervious, ASSUMPTION as in runoff_model.py line 24); the grid instead masks
    roofs (CN 98, crown storage zeroed), puts some crowns on pervious CN 74, and takes max storage where crowns overlap;
  - background (non-street) canopy and the land-cover split (roofs 29% / sealed 52% / pervious 19%, methodology 4b) are NOT modelled
    here: only street-tree effects are compared (differences between palettes), baselines come from runoff_scenarios.csv;
  - 'LAI high' = LiDAR proxy x (median LAI of the 16 Freiburg TLS trees / median LAI proxy of the Porta crowns): ASSUMPTION that the
    proxy under-reads TLS by a constant ratio (methodology 4b 'known limits');
  - young crown 3.0 m (runoff_model.py line 32, ASSUMPTION) vs on-site median crown diameter of the 2,600 LiDAR crowns;
  - S1 uses expected values: the 809 plane positions split in the Porta proportions of the six candidates (porta_species.csv shares).
"""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
CAND = ["Celtis australis", "Melia azedarach", "Tipuana tipu", "Jacaranda mimosifolia", "Pyrus calleryana", "Brachychiton populneus",
        "Styphnolobium japonicum"]   # added 14 Oct (user); crown + LAI from only 5 LiDAR trees = estimate
S_LEVELS = {"low": 0.86, "mid": 1.75, "high": 2.2}      # mm per unit LAI: 0.86 Xiao & McPherson 2016 (matrix #3); 1.75 calibrated (Anys & Weiler 2024, #1); 2.2 upper sens.
YOUNG_M = 3.0                                            # ASSUMPTION (runoff_model.py)
CN = 98.0                                                # ASSUMPTION (runoff_model.py)


def q_scs(p, cn=CN):
    sp = 25.4 * (1000.0 / cn - 10.0)
    ia = 0.2 * sp
    p = np.asarray(p, float)
    return np.where(p > ia, (p - ia) ** 2 / np.where(p > ia, p - ia + sp, 1.0), 0.0)


# ---- inputs
t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
t = t[t.flag == "ok"].reset_index(drop=True)
pl = t.is_plane.values
sp = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species")
shares = pd.read_csv(DB / "porta_species.csv").set_index("cat_nom_cientific").share
w = (shares[CAND] / shares[CAND].sum()).values
cal = pd.read_csv(ROOT / "databases/traits/interception_calibration.csv")
idf = pd.read_csv(DB / "pdisba_idf_city.csv").set_index(["T_years", "duration_min"]).design_intensity_mmh
grid = pd.read_csv(DB / "runoff_scenarios.csv")
s0_file = pd.read_csv(ROOT / "exchange/to_gh/porta_tree_interception_S0.csv")
site_crown = float(t.crown_diam_m.median())
lai_factor = float(cal.LAI.median() / t.lai_proxy.median())
LAI_CASES = {"low": 1.0, "high": lai_factor}
marks = {f"T{T}-{d}min": float(idf[(T, d)] * d / 60) for d in (20, 60) for T in (1, 2, 5, 10)}
P_GRID = sorted(set(np.arange(1, 81, 1.0)) | set(marks.values()))
mark_of = {round(v, 6): k for k, v in marks.items()}


def palettes(crown_mode):
    """name -> list of (weight, crown_diam_m, lai_proxy) for the plane positions (n = 809); other trees are always as measured."""
    cd = lambda c: sp.loc[c, "crown_diam_med"] if crown_mode == "mature" else (YOUNG_M if crown_mode == "young3" else site_crown)
    lai = lambda c: sp.loc[c, "lai_proxy_med"]
    out = {f"single:{c.split()[0]}": [(1.0, cd(c), lai(c))] for c in CAND}
    out["S1"] = [(wi, cd(c), lai(c)) for wi, c in zip(w, CAND)]
    key = {c: np.pi / 4 * cd(c) ** 2 * lai(c) for c in CAND}                 # crown area x LAI
    out["best"] = [(1.0, cd(max(key, key=key.get)), lai(max(key, key=key.get)))]
    out["worst"] = [(1.0, cd(min(key, key=key.get)), lai(min(key, key=key.get)))]
    return out


def tally(P, s, lai_mult, plane_set):
    """(canopy_storage_m3, runoff_reduction_m3) for non-plane trees as measured + plane positions given by plane_set (None = as measured)."""
    D, L = t.crown_diam_m.values, t.lai_proxy.values * lai_mult
    A, S = np.pi / 4 * D ** 2, s * L
    keep = np.ones(len(t), bool) if plane_set is None else ~pl
    A, S = A[keep], S[keep]
    parts = [(A, S)]
    if plane_set is not None:
        for wi, d, l in plane_set:
            parts.append((np.full(1, pl.sum() * wi * np.pi / 4 * d ** 2), np.full(1, s * l * lai_mult)))   # n*w trees of area a == one block of area n*w*a
    st = sum(float((a * np.minimum(P, x)).sum()) for a, x in parts) / 1000
    rr = sum(float((a * (q_scs(P) - q_scs(P - np.minimum(P, x)))).sum()) for a, x in parts) / 1000
    return st, rr


# ---- table
rows = []
for lc, lm in LAI_CASES.items():
    for sk, sv in S_LEVELS.items():
        for P in P_GRID:
            lab = mark_of.get(round(P, 6), "")
            st, rr = tally(P, sv, lm, None)
            rows.append(dict(palette="S0", crown_mode="existing", s_level=sk, s_mm_per_lai=sv, lai_case=lc, P_mm=round(P, 2),
                             storm=lab, canopy_storage_m3=st, runoff_reduction_m3=rr))
            for cm in ("mature", "young3", "young_site"):
                for name, ps in palettes(cm).items():
                    st, rr = tally(P, sv, lm, ps)
                    rows.append(dict(palette=name, crown_mode=cm, s_level=sk, s_mm_per_lai=sv, lai_case=lc, P_mm=round(P, 2),
                                     storm=lab, canopy_storage_m3=st, runoff_reduction_m3=rr))
df = pd.DataFrame(rows)
key = ["s_level", "lai_case", "P_mm"]
s0 = df[df.palette == "S0"][key + ["runoff_reduction_m3"]].rename(columns={"runoff_reduction_m3": "rr_S0"})
df = df.merge(s0, on=key)
df["d_runoff_vs_S0_m3"] = df.rr_S0 - df.runoff_reduction_m3                  # + = more runoff than S0
df = df.drop(columns="rr_S0")
g = grid[grid.scenario == "S0_current"].set_index(["T_years", "duration_min"]).runoff_m3
df["d_vs_S0_pct_of_grid_S0"] = [100 * d / g[(int(x.split("-")[0][1:]), int(x.split("-")[1][:-3]))] if x in
                                ("T1-60min", "T2-60min", "T10-60min", "T2-20min") else np.nan for d, x in zip(df.d_runoff_vs_S0_m3, df.storm)]
df.round(3).to_csv(DB / "runoff_sensitivity_palettes.csv", index=False)

# ---- checks against the grid model and the per-tree file
print(f"S0 per-tree file sum (T2-60): {s0_file.interception_L_T2_60min.sum() / 1000:.1f} m3; this script s=1.75, LAI low, P=31.92: "
      f"{tally(marks['T2-60min'], 1.75, 1.0, None)[0]:.1f} m3")
gi = grid[grid.scenario == "S0_current"].set_index(["T_years", "duration_min"]).interception_m3
gn = grid[grid.scenario == "S_none_street"].set_index(["T_years", "duration_min"])
print(f"grid: street-tree share of interception at T2-60 = {gi[(2, 60)]:.2f} - {gn.interception_m3[(2, 60)]:.2f} = "
      f"{gi[(2, 60)] - gn.interception_m3[(2, 60)]:.1f} m3")
print("\nrunoff reduction by S0 street trees vs grid (m3), s=1.75, LAI low")
for T, d in ((1, 60), (2, 60), (10, 60), (2, 20)):
    P = idf[(T, d)] * d / 60
    gr = gn.runoff_m3[(T, d)] - g[(T, d)]
    print(f"  T{T}-{d}: P={P:.1f} mm  script {tally(P, 1.75, 1.0, None)[1]:.1f}  grid {gr:.1f}  ratio {tally(P, 1.75, 1.0, None)[1] / gr:.2f}")
print("\nscript d_runoff vs S0 (m3) for mature single-species/S1 vs grid R_<sp>_mature, s=1.75, LAI low")
gp = grid.set_index(["scenario", "T_years", "duration_min"]).runoff_m3
for T, d in ((1, 60), (2, 60), (10, 60)):
    m = df[(df.s_level == "mid") & (df.lai_case == "low") & (df.storm == f"T{T}-{d}min") & (df.crown_mode == "mature")].set_index("palette")
    print(f"  T{T}-{d}: " + "  ".join(f"{c.split()[0]} {m.loc['single:' + c.split()[0], 'd_runoff_vs_S0_m3']:.1f}/{gp[(f'R_{c.split()[0]}_mature', T, d)] - gp[('S0_current', T, d)]:.1f}"
                                      for c in CAND) + f"  S1 {m.loc['S1', 'd_runoff_vs_S0_m3']:.1f}   (script/grid)")

# ---- saturation depths
cs = sp.loc[CAND, "lai_proxy_med"]
print(f"\nsaturation depth s*LAI_med (mm), s=1.75: " + ", ".join(f"{c.split()[0]} {1.75 * v:.2f}" for c, v in cs.items()))
print(f"per-tree S range at s=1.75, LAI low: {1.75 * t.lai_proxy.min():.2f}-{1.75 * t.lai_proxy.max():.2f} mm; s=2.2: {2.2 * t.lai_proxy.max():.2f}; "
      f"LAI high (x{lai_factor:.2f}), s=2.2: {2.2 * lai_factor * t.lai_proxy.max():.2f}; trees with S > 19.6 mm: "
      f"{int((1.75 * lai_factor * t.lai_proxy > 19.6).sum())} (s=1.75, LAI high), {int((2.2 * lai_factor * t.lai_proxy > 19.6).sum())} (s=2.2, LAI high)")
print(f"Freiburg TLS LAI: min {cal.LAI.min()}, median {cal.LAI.median()}, max {cal.LAI.max()}; S_fit median {cal.S_fit_mm.median()} (range {cal.S_fit_mm.min()}-{cal.S_fit_mm.max()}); "
      f"Porta proxy median {t.lai_proxy.median()}; LAI factor {lai_factor:.3f}; on-site median crown {site_crown} m")

# ---- spread between palettes vs spread from parameters (Delta = runoff(palette) - runoff(S0), same parameters)
mat = df[df.palette != "S0"]
cen = dict(s_level="mid", lai_case="low", crown_mode="mature")
names8 = [n for n in mat.palette.unique()]
spread = []
for P in P_GRID:
    sub = mat[mat.P_mm == round(P, 2)]
    c = sub[(sub.s_level == "mid") & (sub.lai_case == "low") & (sub.crown_mode == "mature")].set_index("palette").d_runoff_vs_S0_m3
    row = dict(P_mm=round(P, 2), storm=mark_of.get(round(P, 6), ""), palette_spread_m3=c.max() - c.min())
    for fac, cols in (("s", ["s_level"]), ("lai", ["lai_case"]), ("crown", ["crown_mode"])):
        rng = {}
        for n in names8:
            x = sub[(sub.palette == n)]
            for k, v in cen.items():
                if k not in cols:
                    x = x[x[k] == v]
            rng[n] = x.d_runoff_vs_S0_m3.max() - x.d_runoff_vs_S0_m3.min()
        row[f"param_spread_{fac}_S1_m3"] = rng["S1"]
        row[f"param_spread_{fac}_max_m3"] = max(rng.values())
    # ranking of the six single species + S1 (tie-aware, 0.01 m3) under each s x LAI combination (mature crowns)
    ranks = set()
    for (sl, lc, cm), grp in sub[~sub.palette.isin(["best", "worst"]) & (sub.crown_mode == "mature")].groupby(["s_level", "lai_case", "crown_mode"]):
        ranks.add((sl, lc, cm, tuple(grp.set_index("palette").d_runoff_vs_S0_m3.round(2).rank(method="min").sort_index().astype(int))))
    row["n_distinct_rankings_s_lai_mature"] = len({r[3] for r in ranks})
    spread.append(row)
sp_df = pd.DataFrame(spread)
sp_df.round(3).to_csv(DB / "runoff_sensitivity_spread.csv", index=False)
pd.set_option("display.width", 250)
show = sp_df[(sp_df.storm != "") | sp_df.P_mm.isin([2, 5, 10, 15, 25, 40, 80])]
print("\nSpread (m3; Delta vs S0). palette spread at s=1.75, LAI low, mature crowns; parameter spreads one-at-a-time around that centre")
print(show.round(1).to_string(index=False))

# ranking across P at the centre
cr = mat[(mat.s_level == "mid") & (mat.lai_case == "low") & (mat.crown_mode == "mature") & ~mat.palette.isin(["best", "worst"])]
by = {P: tuple(g_.set_index("palette").d_runoff_vs_S0_m3.round(2).rank(method="min").sort_index().astype(int)) for P, g_ in cr.groupby("P_mm")}
chg = sorted({v for v in by.values()})
names7 = sorted(cr.palette.unique())
print("ranks (1 = least extra runoff) by P at centre params, order:", names7)
for P in (1, 2, 3, 4, 5, 6, 8, 10):
    print(f"  P={P}: {by[float(P)]}")
print(f"\nranking (7 palettes, centre params): {len(chg)} distinct over P; P where ranking differs from P=31.92:",
      [P for P, v in by.items() if v != by[round(marks['T2-60min'], 2)]][:12])
d_ = cr[cr.P_mm == round(marks['T2-60min'], 2)].set_index("palette").d_runoff_vs_S0_m3.sort_values()
print("order at T2-60 (best to worst, m3 vs S0):", ", ".join(f"{k} {v:.1f}" for k, v in d_.items()))

# ---- minimum meaningful difference candidate: calibration RMSE (mm of interception per event) as a volume, assuming a systematic error
area = (np.pi / 4 * t.crown_diam_m ** 2).sum()
print(f"\nS0 street crown area {area:.0f} m2 (= {area / 1e4:.2f} ha)")
for T, d in ((1, 60), (2, 60), (10, 60), (2, 20)):
    P = idf[(T, d)] * d / 60
    slope = float(q_scs(P) - q_scs(P - 1.0))
    print(f"  T{T}-{d} P={P:.1f}: 1 mm interception error over all street crowns = {area / 1000:.1f} m3 of interception = {area / 1000 * slope:.1f} m3 of runoff "
          f"(dQ/dPeff {slope:.2f}); RMSE {cal.rmse_mm.min()} / {cal.rmse_mm.median()} / {cal.rmse_mm.max()} mm -> "
          + " / ".join(f"{area / 1000 * slope * r:.0f}" for r in (cal.rmse_mm.min(), cal.rmse_mm.median(), cal.rmse_mm.max())) + " m3 runoff")
print("P marks (mm):", {k: round(v, 1) for k, v in marks.items()})
