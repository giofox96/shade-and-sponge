"""Run the tool on a site: python -m shade_sponge [site]   (default: porta; first run builds cache/site_<site>.npz)
Outputs: databases/barcelona/tool_v0_summary.csv, exchange/to_gh/{positions,layouts}_tool_v0_<YYYYMMDD>.csv"""
import sys, json, datetime, numpy as np, pandas as pd
from .site import load_site, rc, DB, EX
from . import heat, runoff, layout

name = sys.argv[1] if len(sys.argv) > 1 else "porta"
site = load_site(name)
o = json.load(open(EX / "site_origin.json"))
suns = heat.design_suns(site)
lits = [heat.sunlit(site, *s) for s in suns]
p = runoff.design_storm(2, 60)                          # f2 storm: T = 2 yr, 1 h (methodology §6)
pal = layout.palette(site)
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
print(f"{len(pos)} positions, P = {p:.1f} mm, sun altitude {np.degrees(suns[0][0]):.0f}–{np.degrees(suns[-1][0]):.0f}°")
print(pal.to_string(index=False))
shade, water = layout.potentials(site, pos, pal, suns, lits, p)
fit = layout.fits(site, pos, pal)
print("positions where the species fits:", dict(zip(pal.species, fit.mean(0).round(2))))

layouts = {f"S1_random_{k}": layout.random_layout(pal.cap.values, fit, np.random.default_rng(k)) for k in range(10)}
layouts.update({f"S4_w{w:.1f}": ch for w, ch in layout.sweep(shade, water, pal.cap.values, fit).items()})
rows = [dict(scenario="S0_current", **layout.evaluate(site, site.trees[site.trees.flag == "ok"], suns, lits, p))]
for sc, ch in layouts.items():
    rows.append(dict(scenario=sc, **layout.evaluate(site, layout.apply(site, pos, pal, ch), suns, lits, p),
                     **{s: int((ch == j).sum()) for j, s in enumerate(pal.species)}))
res = pd.DataFrame(rows)
rep = res.scenario != "S0_current"                       # front among replacement layouts (S0 keeps mature planes)
res["pareto"] = False
res.loc[rep, "pareto"] = layout.pareto(res[rep])
res.round(1).to_csv(DB / "tool_v0_summary.csv", index=False)
print(res.round(1).to_string(index=False))

# Grasshopper exchange (local coordinates, exchange/README.md)
day = datetime.date.today().strftime("%Y%m%d")
r, c = rc(site, pos.x.values, pos.y.values)
out = pd.DataFrame(dict(tree_id=pos.tree_id, x=(pos.x - o["origin_x"]).round(2), y=(pos.y - o["origin_y"]).round(2),
                        water_convergence_m2=layout.ndimage.maximum_filter(site.acc, size=5)[r, c].round(0),
                        drains_to_hotspot=layout._disk_mean(site.to_hot & ~site.roof, 6, site)[r, c].round(2),
                        sun_share=np.mean([l[r, c] for l in lits], axis=0).round(2)))
for j, s in enumerate(pal.species):
    g = s.split()[0].lower()
    out[f"shade_m2h_{g}"], out[f"water_m3_{g}"] = shade[:, j].round(1), water[:, j].round(3)
out.to_csv(EX / f"to_gh/positions_tool_v0_{day}.csv", index=False)
cur = pos.assign(species=pos.sp).loc[:, ["tree_id", "x", "y", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]]
lay = [cur.assign(scenario="S0_current")]
for sc in ["S1_random_0"] + [k for k in layouts if k.startswith("S4")]:
    lay.append(layout.apply(site, pos, pal, layouts[sc]).tail(len(pos)).assign(scenario=sc))
lay = pd.concat(lay)
lay["ground_z"] = site.dtm[rc(site, lay.x.values, lay.y.values)].round(2)
lay["x"], lay["y"] = (lay.x - o["origin_x"]).round(2), (lay.y - o["origin_y"]).round(2)
lay[["scenario", "tree_id", "x", "y", "ground_z", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]].to_csv(
    EX / f"to_gh/layouts_tool_v0_{day}.csv", index=False)
