"""Allometric LAI for Porta street trees (Nowak 1996, Forest Science 42(4):504-507, Table 1, crown leaf-area equation),
compared with the LiDAR LAI proxy, then the runoff of the fixed tool layouts recomputed with it.
  ln Y = -4.3309 + 0.2942 H + 0.7312 D + 5.7217 S - 0.0148 C,  Y = leaf area (m²), H = crown height (m),
  D = average crown diameter (m), C = pi D (H + D) / 2; bias correction exp(MSE/2), MSE = 0.2317 (x1.123).
H = LiDAR height - crown base, D = LiDAR crown diameter. LAI_allo = Y / (pi D² / 4).
S = species shading factor from Nowak 1996 Table 2 (after McPherson 1984) where the species is listed; otherwise 0.83,
"the average shading coefficient for deciduous trees" per i-Tree UFORE Methods (citing Nowak 1996; the value is not printed
in Nowak 1996 itself). Celtis australis S = 0.92 lies above the paper's stated valid range 0.67-0.88.
H:D outside 0.5-2 (the valid range) is clamped as i-Tree does; ASSUMPTION for the detail: D is kept, H set to the bound,
leaf area scaled back by the volume ratio H/H_clamped (ellipsoid crown, volume proportional to H at fixed D).
LAI_allo is an UPPER BOUND for Porta: the equation estimates near-maximum leaf area of healthy, full-crown open-grown trees
and overestimates for pruned or declining trees (Nowak 1996, p.506). It was fitted on deciduous trees: evergreens flagged.
Runoff: S0 uses lai_allo per tree; S1a/S4 palette species get the equation applied to their palette crown (layout.palette,
city, TERCERA). Layouts are rebuilt as in scripts/runoff_s_sensitivity.py (fixed, s = 1.75, T = 2 and 10 yr, 60 min).
Usage: python scripts/allometric_lai.py -> databases/barcelona/porta_allometric_lai.csv, porta_allometric_lai_species.csv,
runoff_allometric_lai_porta.csv"""
import numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr
from shade_sponge.site import load_site, DB, ROOT
from shade_sponge import heat, runoff, layout, season

S_TABLE2 = {"platanus acerifolia": 0.86, "celtis australis": 0.92, "styphnolobium japonicum": 0.78,  # Sophora japonica
            "gleditsia triacanthos": 0.67}
S_DEFAULT = 0.83                                         # i-Tree UFORE Methods, deciduous average
ESCAPOS = {"platanus acerifolia": 2.51, "celtis australis": 3.5, "pyrus calleryana": 2.3}   # databases/florence/escapos_lai_vs_porta.csv
HABIT = pd.read_csv(ROOT / "databases/traits/phenology_palette.csv").set_index("species").leaf_habit


def key(sp):
    w = [t for t in str(sp).lower().replace("×", " ").split() if t != "x"]
    return " ".join(w[:2])


def lai_allo(h_crown, d, s):
    h_crown, d, s = (np.asarray(v, float) for v in (h_crown, d, s))
    hc = np.clip(h_crown, 0.5 * d, 2 * d)                # valid H:D range 0.5-2
    c = np.pi * d * (hc + d) / 2
    y = np.exp(-4.3309 + 0.2942 * hc + 0.7312 * d + 5.7217 * s - 0.0148 * c + 0.2317 / 2) * h_crown / hc
    return y / (np.pi * d ** 2 / 4)


def s_of(species):
    return np.array([S_TABLE2.get(key(sp), S_DEFAULT) for sp in species])


site = load_site("porta")
t = site.trees[site.trees.flag == "ok"].copy()
t["crown_h_m"] = t.height_m - t.crown_base_m
t["S"] = s_of(t.sp)
t["S_source"] = np.where([key(sp) in S_TABLE2 for sp in t.sp], "Nowak 1996 Table 2", "default 0.83 (UFORE Methods)")
t["lai_allo"] = lai_allo(t.crown_h_m, t.crown_diam_m, t.S)
t["hd_clamped"] = ~t.crown_h_m.between(0.5 * t.crown_diam_m, 2 * t.crown_diam_m)
t["outside_range"] = ~(t.crown_h_m.between(1, 12) & t.crown_diam_m.between(1, 14))
t["leaf_habit"] = t.sp.map(HABIT).fillna("unknown")
t["evergreen"] = t.leaf_habit.eq("evergreen")
t = t.rename(columns={"lai": "lai_lidar"})
cols = ["tree_id", "sp", "leaf_habit", "evergreen", "height_m", "crown_base_m", "crown_h_m", "crown_diam_m", "S", "S_source",
        "hd_clamped", "outside_range", "lai_lidar", "lai_allo"]
t[cols].round(3).to_csv(DB / "porta_allometric_lai.csv", index=False)
assert t.lai_allo.gt(0).all() and np.isfinite(t.lai_allo).all()

sp = t.groupby("sp").agg(n=("tree_id", "size"), S=("S", "first"), evergreen=("evergreen", "first"),
                         lai_lidar_med=("lai_lidar", "median"), lai_allo_med=("lai_allo", "median"),
                         share_clamped=("hd_clamped", "mean"), share_outside=("outside_range", "mean"))
sp["lai_escapos"] = [ESCAPOS.get(key(s)) for s in sp.index]
sp = sp[sp.n >= 15].sort_values("n", ascending=False)
sp.round(2).to_csv(DB / "porta_allometric_lai_species.csv")
print(sp.round(2).to_string())
print(f"trees: {len(t)}; H:D clamped {t.hd_clamped.mean():.0%}; outside size range {t.outside_range.mean():.0%}")
print(f"across trees: Pearson r = {pearsonr(t.lai_lidar, t.lai_allo)[0]:.2f}, Spearman rho = {spearmanr(t.lai_lidar, t.lai_allo)[0]:.2f}")
print(f"across species (n>=15): Spearman rho of medians = {spearmanr(sp.lai_lidar_med, sp.lai_allo_med)[0]:.2f}")

# runoff with lai_allo, layouts fixed (built from the LiDAR palette exactly as the tool does)
sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
pal = layout.palette(site, "city", "TERCERA")
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
fit = layout.fits(site, pos, pal, "exact", cap=pal.cap.values)
pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
objs = {"summer": (pot["summer"], 1), "winter": (pot["winter"], -1),
        "runoff": (layout.water_potential(site, pos, pal, runoff.design_storm(2, 60)), 1)}
ch = {f"S1a_city_{k}": layout.s1a_layout(pal, pal.cap.values, fit, np.random.default_rng(100 + k)) for k in range(10)}
ch.update({"S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w): c for w, c in layout.sweep(objs, pal.cap.values, fit).items()})
pal_a = pal.assign(lai=lai_allo(pal.height_m - pal.crown_base_m, pal.crown_diam_m, s_of(pal.species)))
print(pal_a[["species", "lai"]].assign(lai_lidar=pal.lai).round(2).to_string(index=False))
lai_map = t.set_index("tree_id").lai_allo
rows = []
for lai_src, pl in (("lidar", pal), ("allo", pal_a)):
    def fix(tr):                                          # kept trees: per-tree allometric LAI
        return tr.assign(lai=tr.tree_id.map(lai_map).fillna(tr.lai)) if lai_src == "allo" else tr
    trees = {"S0_current": [fix(site.trees[site.trees.flag == "ok"])],
             "S1a_city_mean": [fix(layout.apply(site, pos, pl, c)) for k, c in ch.items() if k.startswith("S1a")]}
    trees.update({k: [fix(layout.apply(site, pos, pl, c))] for k, c in ch.items() if k.startswith("S4")})
    for T in (2, 10):
        p = runoff.design_storm(T, 60)
        for sc, ts in trees.items():
            for basis, f in (("leafon", runoff.event), ("seasonal", season.runoff_seasonal)):
                r = pd.DataFrame([f(site, x, p) for x in ts]).mean()
                rows.append(dict(lai=lai_src, storm=f"T{T}_60min", basis=basis, scenario=sc, **r.round(1)))
out = pd.DataFrame(rows)
out.to_csv(DB / "runoff_allometric_lai_porta.csv", index=False)
ref = pd.read_csv(DB / "tool_v0_summary_sizeexact_trunkTERCERA.csv").set_index("scenario").runoff_m3
chk = out.query("lai == 'lidar' and storm == 'T2_60min' and basis == 'seasonal' and scenario != 'S1a_city_mean'")
assert (chk.set_index("scenario").runoff_m3 - ref).dropna().abs().max() < 1.0, "LiDAR rows do not reproduce the tool summary"
