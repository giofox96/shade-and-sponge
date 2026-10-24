"""Scenarios R, A and R+A in Porta (notes/topic_decision.md §10.6), each as the city's rule (S1a, 5 seeds) vs the
optimised layout (weights 0.5 summer / 0.25 winter / 0.25 hotspot runoff), with the exact sizing rule and traits at equal
trunk size (TERCERA), as in `python -m shade_sponge porta --size=exact --trunk=TERCERA`.
R = the 832 plane positions; A = the free spots (scripts/porta_planting_spots.py), planes kept; R+A = both.
The 15% cap is recomputed on the larger stock when trees are added (still Porta-local, ASSUMPTION).
Output: databases/barcelona/additions_summary.csv. Run from the repo root: python scripts/run_additions.py
"""
import sys, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from shade_sponge.site import load_site, DB
from shade_sponge import heat, runoff, layout

W = np.array([0.5, 0.25, 0.25])                            # summer, winter, hotspot runoff (as S4_s0.50_w0.25_r0.25)
site = load_site("porta")
sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
p = runoff.design_storm(2, 60)
pal = layout.palette(site, "city", "TERCERA")
planes = site.trees[site.trees.is_plane].reset_index(drop=True)
spots = pd.read_csv(DB / "porta_planting_spots.csv").rename(columns={"spot_id": "tree_id"})
sets = {"R": planes, "A": spots, "RA": pd.concat([planes.assign(size_class=layout.sidewalk_class(planes)), spots],
                                                 ignore_index=True)}
N = len(site.trees)
rows = [dict(scenario="S0_current", n_new=0, **layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p))]
for name, pos in sets.items():
    n_add = len(spots) if name != "R" else 0
    cap = pal.cap.values + int(np.floor(layout.MAX_SHARE * (N + n_add)) - np.floor(layout.MAX_SHARE * N))
    fit = layout.fits(site, pos, pal, "exact")
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    norm = [sg * m / m.max() for m, sg in ((pot["summer"], 1), (pot["winter"], -1),
                                           (layout.water_potential(site, pos, pal, p), 1))]
    lays = {f"{name}_S1a_{k}": layout.s1a_layout(pal, cap, fit, np.random.default_rng(100 + k)) for k in range(5)}
    lays[f"{name}_Opt"] = layout.assign(sum(w * m for w, m in zip(W, norm)) + 1e-3 * sum(norm), cap, fit)
    for sc, ch in lays.items():
        assert fit[np.arange(len(ch)), ch].all(), sc
        rows.append(dict(scenario=sc, n_new=len(pos), **layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p),
                         **{s: int((ch == j).sum()) for j, s in enumerate(pal.species)}))
    print(name, len(pos), "positions done")
res = pd.DataFrame(rows)
res.round(2).to_csv(DB / "additions_summary.csv", index=False)
g = res.assign(group=res.scenario.str.replace(r"_\d+$", "", regex=True)).groupby("group", sort=False)
print(g[["shade_summer_m2h", "shade_winter_m2h", "runoff_m3", "runoff_hot_m3", "canopy_pct"]].mean().round(1).to_string())
