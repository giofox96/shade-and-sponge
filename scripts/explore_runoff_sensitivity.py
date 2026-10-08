"""Exploratory bracket: can event runoff (f2) tell tree palettes apart in Porta? Aggregate arithmetic on repo CSVs only.

Usage: python scripts/explore_runoff_sensitivity.py
Reads exchange/to_gh/porta_trees_lidar.csv, porta_tree_interception_S0.csv, databases/barcelona/{porta_species,
porta_species_lidar_summary,pdisba_idf_city,runoff_scenarios}.csv. Writes notes/decisions/runoff_sensitivity_table.csv, prints summaries.
Per tree: I = min(P, s*LAI); intercepted m3 = crown area * I; runoff saved = area * [Q(P) - Q(P-I)], CN 98 on the sealed share
of crowns, CN 74 on the rest. No grid, overlap or roof masking, so totals differ from scripts/runoff_model.py (reported below).
All results are an exploratory bracket (methodology status NOT DEFINED). Inputs without a source are ASSUMPTION.
"""
import itertools, pathlib, numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
DB = R / "databases/barcelona"
SITE_M2 = 0.84e6                                     # Porta area (CLAUDE.md)
ROOF, SEALED, PERV = 0.29, 0.52, 0.19                # land-cover split, methodology 4b (grid model, unverified)
CN_IMP, CN_PERV = 98, 74                             # ASSUMPTION (TR-55), as runoff_model.py
SEALED_CROWN = SEALED / (SEALED + PERV)              # ASSUMPTION: crowns sit on sealed open space or pervious, never roofs
YOUNG_D = 3.0                                        # ASSUMPTION, as runoff_model.py
S_RANGE = {"low": 0.86, "mid": 1.75, "high": 2.2}    # mm per LAI: Xiao & McPherson 2016 mean; calibrated pooled median; sensitivity high (runoff_sensitivity_storage.csv)
LAI_MULT = {"proxy": 1.0, "x1.5": 1.5}               # ASSUMPTION: x1.5 lifts median proxy 2.3 to 3.5, inside Freiburg TLS LAI 2.6-4.9 (matrix)
CAND = ["Celtis australis", "Melia azedarach", "Tipuana tipu", "Jacaranda mimosifolia", "Pyrus calleryana", "Brachychiton populneus"]
PS = [5, 10, 19.6, 31.9, 40, 62.5, 80]             # generic depths mm; 19.6, 31.9, 62.5 are PDISBA T1-60, T2-60, T10-60


def Q(p, cn):
    s = 25.4 * (1000 / cn - 10); ia = 0.2 * s
    return np.where(p > ia, (p - ia) ** 2 / (p - ia + s), 0.0)


t = pd.read_csv(R / "exchange/to_gh/porta_trees_lidar.csv"); t = t[t.flag == "ok"].reset_index(drop=True)
sp = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species")
share = pd.read_csv(DB / "porta_species.csv").set_index("cat_nom_cientific").trees[CAND]; share = share / share.sum()
area0, lai0, plane = np.pi * t.crown_diam_m.values ** 2 / 4, t.lai_proxy.values, t.is_plane.values


def effect(area, lai, p, s):
    """Return (intercepted m3, runoff saved m3) for arrays of crown area and LAI."""
    i = np.minimum(p, s * lai)
    saved = area * (SEALED_CROWN * (Q(p, CN_IMP) - Q(p - i, CN_IMP)) + (1 - SEALED_CROWN) * (Q(p, CN_PERV) - Q(p - i, CN_PERV)))
    return (area * i).sum() / 1000, saved.sum() / 1000


def swap(c, mult, d=None):
    """Arrays (area, lai) with every plane replaced by species c (mature crown unless d given)."""
    a, l = area0.copy(), lai0 * mult
    d = sp.loc[c, "crown_diam_med"] if d is None else d
    a[plane], l[plane] = np.pi * d ** 2 / 4, sp.loc[c, "lai_proxy_med"] * mult
    return a, l


def palette(name, mult):
    """List of (area, lai, weight) for a palette; non-plane trees keep their LiDAR values."""
    if name == "S0":
        return [(area0, lai0 * mult, 1.0)]
    if name == "S1":                                   # six species in Porta proportions (expectation)
        return [(*swap(c, mult), share[c]) for c in CAND]
    if name in ("best", "worst"):                      # highest / lowest crown area x LAI among the six, mature
        f = {c: np.pi * sp.loc[c, "crown_diam_med"] ** 2 / 4 * sp.loc[c, "lai_proxy_med"] for c in CAND}
        return [(*swap((max if name == "best" else min)(f, key=f.get), mult), 1.0)]
    _, c, age = name.split("_")                        # R_<genus>_mature|young
    c = next(x for x in CAND if x.startswith(c))
    return [(*swap(c, mult, None if age == "mature" else YOUNG_D), 1.0)]


def run(name, p, s, mult):
    return sum(w * np.array(effect(a, l, p, s)) for a, l, w in palette(name, mult))


def event_runoff_none(p):                              # whole-site runoff with no street trees, aggregate (background canopy ignored)
    return SITE_M2 / 1000 * ((ROOF + SEALED) * Q(p, CN_IMP) + PERV * Q(p, CN_PERV))


names = ["S0", "S1", "best", "worst"] + [f"R_{c.split()[0]}_{a}" for c in CAND for a in ("mature", "young")]
rows = []
for p, nm, (sk, s), (lk, m) in itertools.product(PS, names, S_RANGE.items(), LAI_MULT.items()):
    i, sv = run(nm, p, s, m)
    rows.append(dict(P_mm=p, palette=nm, s=sk, lai=lk, intercepted_m3=round(i, 1), runoff_saved_m3=round(sv, 1),
                     saved_pct_of_event_runoff=round(100 * sv / event_runoff_none(p), 3)))
tab = pd.DataFrame(rows); tab.to_csv(R / "notes/decisions/runoff_sensitivity_table.csv", index=False)
pd.set_option("display.width", 200)

print("== Crowns:", len(t), "ok trees,", plane.sum(), "planes, total crown area", round(area0.sum()), "m2")
print("== Gap to grid model at T2-60 (P=31.9, s=1.75): per-tree file", round(pd.read_csv(R / "exchange/to_gh/porta_tree_interception_S0.csv").interception_L_T2_60min.sum() / 1000, 1),
      "m3; this script", round(run("S0", 31.9, 1.75, 1.0)[0], 1), "m3; grid street share",
      round(817.51 - 412.22, 1), "m3 (runoff_scenarios.csv)")
print("== Saturation depth s*LAI (mm), per tree: min/median/max at s=1.75:", *np.round(np.percentile(1.75 * lai0, [0, 50, 100]), 1))
print("\n== runoff saved (m3), mid s, proxy LAI")
mid = tab[(tab.s == "mid") & (tab.lai == "proxy")].pivot(index="palette", columns="P_mm", values="runoff_saved_m3").loc[names]
print(mid.to_string())
print("\n== palette spread vs S0 (m3) at mid s, proxy LAI: best-S0, worst-S0, S1-S0 | parameter spread of S0: s low..high; LAI proxy..x1.5; (both) per P")
for p in PS:
    g = lambda nm, s="mid", l="proxy": tab[(tab.P_mm == p) & (tab.palette == nm) & (tab.s == s) & (tab.lai == l)].runoff_saved_m3.iloc[0]
    print(f"P={p:5}: best {g('best')-g('S0'):+7.1f} worst {g('worst')-g('S0'):+7.1f} S1 {g('S1')-g('S0'):+7.1f} | "
          f"s {g('S0','low')-g('S0','high'):+7.1f} (low-high) LAI {g('S0','mid','proxy')-g('S0','mid','x1.5'):+7.1f} (proxy-x1.5) "
          f"S0 range {g('S0','low','proxy'):.1f}..{g('S0','high','x1.5'):.1f}")
print("\n== ranking of the six mature single-species palettes by runoff saved, mid s, proxy LAI (same at every P?)")
rk = {p: tuple(tab[(tab.P_mm == p) & tab.palette.str.endswith("mature") & (tab.s == "mid") & (tab.lai == "proxy")].sort_values("runoff_saved_m3", ascending=False).palette) for p in PS}
for p, r in rk.items(): print(p, r)
print("ranking identical across P:", len(set(rk.values())) == 1)
print("\n== denominator: aggregate no-street-tree event runoff (m3):", {p: round(float(event_runoff_none(p))) for p in PS})
