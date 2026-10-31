"""Run the tool on a site: python -m shade_sponge [site] [--palette=barcelona] [--diversity=N] [--size=exact|at_most]
[--keep-meridiana] [--trunk=TERCERA] [--scenario=R|A|RA] [--area=FILE] [--priority=N] (default: porta; any barri by name or slug, e.g. "Sant Antoni", once scripts/bcn_lidar_barri.py has run; first run builds cache/site_<site>.npz). --diversity=N: optimised layouts keep at
least N effective species (exp of Shannon H) among the planted positions; off by default. --size: sidewalk-width sizing
rule of the 2011 guide (layout.size_fits); off by default. --keep-meridiana: the planes of Av. Meridiana are kept by the
city ("large avenue", guide p. 17) and leave the decision set. --trunk=CLASS: species traits at equal trunk size
(layout.palette). --scenario: R = replace the planes (default), A = add trees in the free spots (planes kept),
RA = both (notes/topic_decision.md §10.6; cap recomputed on the larger stock, layout.add_cap). --area=FILE: only the
planes and spots inside the project area the user draws (layout.in_area). --priority=N: only the N planes with the highest
replacement priority (health.py, a proxy). S1a (the city's 2026 mix within the exact sizing rule, layout.s1a_layout) and
S1b (the mix the city actually planted in place of planes 2018–2026, layout.s1b_mix) are always run, 10 seeds each.
--s1b-only: compute only S1b and replace its rows in an existing summary file (no optimisation, no Grasshopper export).
Outputs: databases/barcelona/tool_v0_summary<tag>.csv, exchange/to_gh/{positions,layouts}_tool_v0<tag>_<YYYYMMDD>.csv"""
import sys, json, datetime, pathlib, numpy as np, pandas as pd
from .site import load_site, rc, slug, DB, EX
from . import heat, runoff, layout, season, health

args = [a for a in sys.argv[1:] if not a.startswith("--")]
name = args[0] if args else "porta"
kind = "barcelona" if "--palette=barcelona" in sys.argv else "city"   # python -m shade_sponge porta --palette=barcelona
opt = dict(a[2:].split("=") for a in sys.argv[1:] if a.startswith("--") and "=" in a)
min_eff = float(opt["diversity"]) if "diversity" in opt else None
ptag = "" if kind == "city" else "_barcelona"
size_rule = opt.get("size")
keep_mer = "--keep-meridiana" in sys.argv
trunk = opt.get("trunk")
scen = opt.get("scenario", "R").upper()
area = opt.get("area")
top = int(opt["priority"]) if "priority" in opt else None
tag = ptag + (f"_div{opt['diversity']}" if min_eff else "") + (f"_size{size_rule}" if size_rule else "") + ("_keepmer" if keep_mer else "") + (f"_trunk{trunk}" if trunk else "")
tag += (f"_sc{scen}" if scen != "R" else "") + (f"_area{pathlib.Path(area).stem}" if area else "") + (f"_prio{top}" if top else "")
if name != "porta" and (scen != "R" or top):
    sys.exit("other barris: only --scenario=R without --priority for now (free spots and the priority proxy exist for "
             "Porta only; notes/citywide_plan.md §6.2 step 4). --size needs scripts/porta_sidewalk_width.py \"<barri>\" first")
tag = ("" if name == "porta" else "_" + slug(name)) + tag    # Porta keeps its file names
site = load_site(name)
o = json.load(open(EX / "site_origin.json"))
sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
p = runoff.design_storm(2, 60)                          # f2 storm: T = 2 yr, 1 h (methodology §6)
pal = layout.palette(site, kind, trunk)
pos = site.trees[site.trees.is_plane & ~(keep_mer & site.trees.street.str.contains("Meridiana"))].reset_index(drop=True)
if area:
    pos = pos[layout.in_area(pos, area)]
if top:                                                  # replace the most likely to go first (health.py, ASSUMPTION)
    pos = pos.merge(health.priority(site.trees)[["tree_id", "priority"]]).nlargest(top, "priority", keep="first")
spots = layout.planting_spots() if scen != "R" else None
if spots is not None and area:
    spots = spots[layout.in_area(spots, area)]
if scen == "A":
    if top:
        sys.exit("--priority selects planes; it does not apply to --scenario=A")
    pos = spots
elif scen == "RA":
    pos = pd.concat([pos.assign(size_class=layout.sidewalk_class(pos, site)), spots])
elif scen != "R":
    sys.exit(f"unknown --scenario={scen} (R, A or RA)")
pos = pos.reset_index(drop=True)
if pos.empty:
    sys.exit("no positions in the decision set (check --area / --priority)")
if spots is not None:
    pal["cap"] = layout.add_cap(pal.cap.values, len(site.trees), len(spots))
print(f"scenario {scen}: {len(pos)} positions, P = {p:.1f} mm; sun altitude " + ", ".join(
    f"{s} {min(np.degrees([a for a, _ in v])):.0f}–{max(np.degrees([a for a, _ in v])):.0f}°" for s, v in sun.items()))
print(pal.to_string(index=False))
sens = pd.DataFrame({**{f"r_off_{r}": season.storm_factor(pal.species, r) for r in (0.3, 0.5, 0.7)},
                     "no_gloria_jan": season.storm_factor(pal.species, storms=season.STORM.drop(1))}, index=pal.species)
sens.round(3).to_csv(DB / f"tool_v0_storm_leaf_factor{ptag}.csv")
print("season-weighted leaf factor in storms (sensitivity):\n", sens.round(3).to_string())
fit = layout.fits(site, pos, pal, size_rule)
fit_s1a = fit if size_rule == "exact" else layout.fits(site, pos, pal, "exact")
mix_b = layout.s1b_mix()
print(f"S1b: palette species cover {sum(mix_b.get(s, 0) for s in pal.species) / sum(mix_b.values()):.0%} of observed plane replacements")
s1b = {f"S1b_obs_{k}": layout.s1a_layout(pal, pal.cap.values, fit_s1a, np.random.default_rng(200 + k), mix_b) for k in range(10)}
if "--s1b-only" in sys.argv:
    f = DB / f"tool_v0_summary{tag}.csv"
    old = pd.read_csv(f)
    new = pd.DataFrame([dict(scenario=sc, **layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p),
                             eff_species=layout.eff_species(ch, len(pal)), **{s: int((ch == j).sum()) for j, s in enumerate(pal.species)})
                        for sc, ch in s1b.items()]).assign(pareto=False)
    out = pd.concat([old[~old.scenario.str.startswith("S1b")], new.round(1)], ignore_index=True)[old.columns]
    out.to_csv(f, index=False)
    print(f"S1b rows written to {f.name}")
    sys.exit(0)
print("positions where the species fits:", dict(zip(pal.species, fit.mean(0).round(2))))
pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
water = layout.water_potential(site, pos, pal, p)

layouts = {f"S1_random_{k}": layout.random_layout(pal.cap.values, fit, np.random.default_rng(k)) for k in range(10)}
if size_rule != "exact":
    print("note: S1a uses the exact sizing rule; the other layouts use", size_rule or "no sizing rule")
layouts.update({f"S1a_city_{k}": layout.s1a_layout(pal, pal.cap.values, fit_s1a, np.random.default_rng(100 + k)) for k in range(10)})
layouts.update(s1b)
objs = {"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)}
layouts.update({"S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w): ch for w, ch in layout.sweep(objs, pal.cap.values, fit, min_eff=min_eff).items()})
rows = [dict(scenario="S0_current", **layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p))]
for sc, ch in layouts.items():
    rows.append(dict(scenario=sc, **layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p),
                     eff_species=layout.eff_species(ch, len(pal)), **{s: int((ch == j).sum()) for j, s in enumerate(pal.species)}))
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
cur = pos.reindex(columns=["tree_id", "x", "y", "sp", "crown_diam_m", "height_m", "crown_base_m", "lai"])
cur = cur.assign(species=cur.sp.fillna("none")).loc[:, ["tree_id", "x", "y", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]]
lay = [cur.assign(scenario="S0_current")]
for sc in ["S1_random_0", "S1a_city_0"] + [k for k in layouts if k.startswith("S4")]:
    lay.append(layout.apply(site, pos, pal, layouts[sc]).tail(len(pos)).assign(scenario=sc))
lay = pd.concat(lay)
lay["ground_z"] = site.dtm[rc(site, lay.x.values, lay.y.values)].round(2)
lay["x"], lay["y"] = (lay.x - o["origin_x"]).round(2), (lay.y - o["origin_y"]).round(2)
lay[["scenario", "tree_id", "x", "y", "ground_z", "species", "crown_diam_m", "height_m", "crown_base_m", "lai"]].to_csv(
    EX / f"to_gh/layouts_tool_v0{tag}_{day}.csv", index=False)
