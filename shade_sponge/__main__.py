"""Run the tool on a site: python -m shade_sponge [site]   (default: porta; first run builds cache/site_<site>.npz)
Outputs: databases/barcelona/tool_v0_summary.csv, exchange/to_gh/{positions,layouts}_tool_v0_<YYYYMMDD>.csv"""
import sys, json, datetime, numpy as np, pandas as pd
from .site import load_site, rc, DB, EX
from . import heat, runoff, layout, season

args = [a for a in sys.argv[1:] if not a.startswith("--")]
name = args[0] if args else "porta"
kind = "barcelona" if "--palette=barcelona" in sys.argv else "city"   # python -m shade_sponge porta --palette=barcelona
tag = "" if kind == "city" else "_barcelona"
site = load_site(name)
o = json.load(open(EX / "site_origin.json"))
sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
p = runoff.design_storm(2, 60)                          # f2 storm: T = 2 yr, 1 h (methodology §6)
pal = layout.palette(site, kind)
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
print(f"{len(pos)} positions, P = {p:.1f} mm; sun altitude " + ", ".join(
    f"{s} {min(np.degrees([a for a, _ in v])):.0f}–{max(np.degrees([a for a, _ in v])):.0f}°" for s, v in sun.items()))
print(pal.to_string(index=False))
sens = pd.DataFrame({**{f"r_off_{r}": season.storm_factor(pal.species, r) for r in (0.3, 0.5, 0.7)},
                     "no_gloria_jan": season.storm_factor(pal.species, storms=season.STORM.drop(1))}, index=pal.species)
sens.round(3).to_csv(DB / f"tool_v0_storm_leaf_factor{tag}.csv")
print("season-weighted leaf factor in storms (sensitivity):\n", sens.round(3).to_string())
pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
water = layout.water_potential(site, pos, pal, p)
fit = layout.fits(site, pos, pal)
print("positions where the species fits:", dict(zip(pal.species, fit.mean(0).round(2))))

layouts = {f"S1_random_{k}": layout.random_layout(pal.cap.values, fit, np.random.default_rng(k)) for k in range(10)}
objs = {"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)}
layouts.update({"S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w): ch for w, ch in layout.sweep(objs, pal.cap.values, fit).items()})
rows = [dict(scenario="S0_current", **layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p))]
for sc, ch in layouts.items():
    rows.append(dict(scenario=sc, **layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p),
                     **{s: int((ch == j).sum()) for j, s in enumerate(pal.species)}))
res = pd.DataFrame(rows)
rep = res.scenario != "S0_current"                       # front among replacement layouts (S0 keeps mature planes)
res["pareto"] = False
res.loc[rep, "pareto"] = layout.pareto(res[rep])
res.round(1).to_csv(DB / f"tool_v0_summary{tag}.csv", index=False)
print(res.round(1).to_string(index=False))

# Grasshopper exchange (local coordinates, exchange/README.md)
day = datetime.date.today().strftime("%Y%m%d")
r, c = rc(site, pos.x.values, pos.y.values)
out = pd.DataFrame(dict(tree_id=pos.tree_id, x=(pos.x - o["origin_x"]).round(2), y=(pos.y - o["origin_y"]).round(2),
                        water_convergence_m2=layout.ndimage.maximum_filter(site.acc, size=5)[r, c].round(0),
                        drains_to_hotspot=layout._box_mean(site.to_hot & ~site.roof, 6, site)[r, c].round(2),
                        sun_share_summer=np.mean([l[r, c] for l in lit["summer"]], axis=0).round(2),
                        sun_share_winter=np.mean([l[r, c] for l in lit["winter"]], axis=0).round(2)))
for j, s in enumerate(pal.species):
    g = layout.slug(s)
    out[f"shade_summer_m2h_{g}"], out[f"shade_winter_m2h_{g}"] = pot["summer"][:, j].round(1), pot["winter"][:, j].round(1)
    out[f"water_m3_{g}"] = water[:, j].round(3)
out.to_csv(EX / f"to_gh/positions_tool_v0{tag}_{day}.csv", index=False)
cur = pos.assign(species=pos.sp).loc[:, ["tree_id", "x", "y", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]]
lay = [cur.assign(scenario="S0_current")]
for sc in ["S1_random_0"] + [k for k in layouts if k.startswith("S4")]:
    lay.append(layout.apply(site, pos, pal, layouts[sc]).tail(len(pos)).assign(scenario=sc))
lay = pd.concat(lay)
lay["ground_z"] = site.dtm[rc(site, lay.x.values, lay.y.values)].round(2)
lay["x"], lay["y"] = (lay.x - o["origin_x"]).round(2), (lay.y - o["origin_y"]).round(2)
lay[["scenario", "tree_id", "x", "y", "ground_z", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]].to_csv(
    EX / f"to_gh/layouts_tool_v0{tag}_{day}.csv", index=False)
