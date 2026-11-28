"""City-wide 15% cap: one layout LP over several barris at once (notes/citywide_plan.md §6.2 step 6, §6.8).
Each barri is set up as its reference run (python -m shade_sponge "<barri>" --size=exact --trunk=TERCERA, scenario R:
replace every plane): per-position potentials (summer shade, winter shade, hotspot runoff) and the sizing/facade fit.
The positions of all barris are stacked into one transportation LP (layout.assign), so species go where they work best
across barris; the cap is the city's (layout.city_cap), not one per barri. The same weight sweep as the tool
(layout.sweep, 15 combinations); every layout is then re-scored barri by barri with the full raster models.
Usage (PC, project env; needs the site caches and databases/barcelona/arbrat_viari.csv):
    python scripts/city_lp.py                         # Porta + Eixample + Sant Martí (the barris of run_barris.py)
    python scripts/city_lp.py "Gràcia" ...            # other districts or barri names, plus Porta
    python scripts/city_lp.py --local-ceiling         # also: in each barri no species above today's plane share
    python scripts/city_lp.py --all [--local-ceiling] # every barri of barris_summary.csv (the city-palette runs)
    python scripts/city_lp.py --all --totals          # city totals only, from the files already written (no LP)
--all: Sants and Vilapicina are not in barris_summary.csv (city palette infeasible there, PR #208), so they are left out.
--local-ceiling (user, 30 Oct): the city cap alone let one species reach 48.5% of a barri (notes/citywide_plan.md §6.8),
so a replacement may not create a larger single-species share than the planes it removes: per barri, species count
after replacement <= today's plane count (ASSUMPTION). Outputs then carry the suffix _local.
User decision (15 Nov): the local ceiling is relaxed only where needed: where a position fits only one palette species,
that species' local ceiling is raised to the number of such positions, so the ceiling cannot leave a position with no species.
Outputs: databases/barcelona/citylp/tool_v0_citylp_<slug>.csv (S0 + the 15 swept layouts, as tool_v0_summary_*),
         databases/barcelona/citylp_summary.csv (one row per barri, the joint layout with the most summer shade in total:
         local-cap tool, city-cap tool, city mix S1a),
         databases/barcelona/citylp_species.csv (species counts per barri and layout, and the city cap),
         databases/barcelona/citylp_city.csv (city totals over the barris run: today S0, city announced mix S1a, city
         practice S1b, the sum of the per-barri runs (each with its own local cap) and the joint city LP),
         databases/barcelona/citylp_add_only.csv (the barris with no planes: shade added in free spots, add_only())."""
import sys, pathlib, numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge import heat, runoff, layout  # noqa: E402
from shade_sponge.site import load_site, DB  # noqa: E402

TRUNK, SIZE = "TERCERA", "exact"                          # Porta's reference options (run_barris.py)
OUT = DB / "citylp"
TAG = "_sizeexact_trunkTERCERA"
ADD_ONLY = ["la Clota", "Ciutat Meridiana", "Torre Baró"]   # no planes: trees added in free spots only (user, 28 Nov)


def add_only():
    """The barris with no planes (user, 28 Nov): new trees in the free spots, planes none, same shade model and rules
    (python -m shade_sponge "<barri>" --scenario=A --size=exact --trunk=TERCERA after scripts/porta_planting_spots.py
    "<barri>"). Reported as shade ADDED, apart from the replacement totals. -> databases/barcelona/citylp_add_only.csv"""
    from shade_sponge.site import slug
    rows = []
    for name in ADD_ONLY:
        for pal in ("city", "barcelona"):                    # Barcelona palette where the city palette is infeasible
            f = DB / f"tool_v0_summary_{slug(name)}{'' if pal == 'city' else '_barcelona'}{TAG}_scA.csv"
            if f.exists():
                break
        else:
            print(f"no add-only run: {name}"); continue
        d = pd.read_csv(f)
        s0, opt = d.iloc[0], d[d.scenario.str.startswith("S4_")]
        best = opt.loc[opt.shade_summer_m2h.idxmax()]
        sp = d.columns[d.columns.get_loc("eff_species") + 1:].drop("pareto", errors="ignore")   # species count columns
        row = dict(barri=name, palette=pal, spots=int(best[sp].sum()), summer_m2h_today=round(s0.shade_summer_m2h))
        for k, r in (("method", best), ("s1a", d[d.scenario.str.startswith("S1a")].mean(numeric_only=True)),
                     ("s1b", d[d.scenario.str.startswith("S1b")].mean(numeric_only=True))):
            row[f"summer_added_m2h_{k}"] = round(r.shade_summer_m2h - s0.shade_summer_m2h)
            row[f"summer_added_pct_{k}"] = round(100 * (r.shade_summer_m2h / s0.shade_summer_m2h - 1), 1)
        rows.append(row)
    if rows:
        out = pd.DataFrame(rows)
        out.to_csv(DB / "citylp_add_only.csv", index=False)
        print(out.to_string(index=False))


def city_totals(barris, sfx):
    """Sum over barris of shade (m²h), hotspot runoff (m³) and new trees per species, for each scenario. S1a, S1b = mean of
    their draws; per-barri tool = each barri's own best summer layout (as barris_summary.csv); city LP = the joint layout
    chosen below. Effective species = exp(Shannon) of the summed new trees."""
    acc, sp = {}, list(layout.CITY_PALETTE)
    best_lp = None
    for name, s in barris:
        f = DB / (f"tool_v0_summary{TAG}.csv" if s == "porta" else f"tool_v0_summary_{s}{TAG}.csv")
        if not f.exists():
            print(f"no per-barri run: {name}"); continue
        d = pd.read_csv(f)
        opt = d[d.scenario.str.startswith("S4_")]
        rows = {"S0_today": d.iloc[0], "S1a_city_announced_mix": d[d.scenario.str.startswith("S1a")].mean(numeric_only=True),
                "S1b_city_practice": d[d.scenario.str.startswith("S1b")].mean(numeric_only=True),
                "method_per_barri_sum": opt.loc[opt.shade_summer_m2h.idxmax()]}
        g = OUT / f"tool_v0_citylp{sfx}_{s}.csv"
        if g.exists():
            c = pd.read_csv(g).set_index("scenario")
            if best_lp is None:
                best_lp = pd.read_csv(DB / f"citylp{sfx}_summary.csv").layout.iloc[0]
            rows["method_city_lp"] = c.loc[best_lp]
        for k, r in rows.items():
            a = acc.setdefault(k, dict(barris=0, summer=0.0, winter=0.0, runoff_hot=0.0, **{x: 0.0 for x in sp}))
            a["barris"] += 1
            a["summer"] += r.shade_summer_m2h; a["winter"] += r.shade_winter_m2h; a["runoff_hot"] += r.runoff_hot_m3
            for x in sp:
                a[x] += float(r.get(x, 0) or 0) if k != "S0_today" else 0
    s0 = acc["S0_today"]
    if "method_city_lp" in acc and acc["method_city_lp"]["barris"] < s0["barris"]:   # old run over fewer barris: not comparable
        print(f"city LP files for {acc.pop('method_city_lp')['barris']} of {s0['barris']} barris only: city LP row left out")
    out = []
    for k, a in acc.items():
        n = np.array([a[x] for x in sp]); q = n[n > 0] / n.sum() if n.sum() else np.array([1.0])
        out.append(dict(scenario=k, barris=a["barris"], summer_m2h=round(a["summer"]), summer_pct_of_today=round(100 * a["summer"] / s0["summer"], 1),
                        winter_pct_of_today=round(100 * a["winter"] / s0["winter"], 1),
                        runoff_hot_change_pct=round(100 * (a["runoff_hot"] / s0["runoff_hot"] - 1), 2),
                        eff_species=round(float(np.exp(-(q * np.log(q)).sum())), 1) if n.sum() else None,
                        **{x: int(round(a[x])) for x in sp}))
    out = pd.DataFrame(out)
    out.to_csv(DB / f"citylp{sfx}_city.csv", index=False)
    print(out.drop(columns=sp).to_string(index=False))


def setup(name):
    site = load_site(name)
    sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
    lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
    pal = layout.palette(site, "city", TRUNK)
    pos = site.trees[site.trees.is_plane].reset_index(drop=True)
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    return site, sun, lit, pal, pos, pot


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or ["Eixample", "Sant Martí"]
    idx = pd.read_csv(DB / "lidar_tiles_barris.csv").drop_duplicates("barri")
    if "--all" in sys.argv:
        args = [b for b in pd.read_csv(DB / "barris_summary.csv").barri.unique() if b != "Porta"]
    dist = [a for a in args if a not in set(idx.barri)]  # a name that is also a barri ("Sant Andreu") means the barri only
    sel = idx[idx.district.isin(dist) | idx.barri.isin(args)]
    barris = [("Porta", "porta")] + list(zip(sel.barri, sel.slug))
    p = runoff.design_storm(2, 60)
    loc = "--local-ceiling" in sys.argv
    relax = loc                                       # user decision (15 Nov): the single-fit exception is part of the local ceiling
    sfx = "_local" if loc else ""
    if "--totals" in sys.argv:
        city_totals(barris, sfx)
        add_only()
        sys.exit()

    # 1. potentials and fit per barri (palette species are the same everywhere; their traits are each barri's medians)
    parts = []
    for name, s in barris:
        print(f"setup {name}", flush=True)
        site, sun, lit, pal, pos, pot = setup(name if s != "porta" else "porta")
        kept = site.trees[~site.trees.is_plane].sp.value_counts().reindex(pal.species).fillna(0).values
        parts.append(dict(name=name, slug=s, pal=pal, pos=pos, local=(len(pos) - kept).clip(0), summer=pot["summer"], winter=pot["winter"],
                          water=layout.water_potential(site, pos, pal, p), fit=layout.fits(site, pos, pal, SIZE)))
    species = list(parts[0]["pal"].species)
    if relax:                                         # positions that fit one species only: never blocked by the ceiling
        for q in parts:
            only = q["fit"][q["fit"].sum(1) == 1].sum(0).astype(int)
            raised = only > q["local"]
            if raised.any():
                print(f"RELAXED {q['name']}:", {species[j]: f"{q['local'][j]} -> {only[j]} ({only[j]} single-fit positions)"
                                                 for j in np.flatnonzero(raised)})
            q["local"] = np.maximum(q["local"], only)

    # 2. the city cap (street-tree inventory, notes/citywide_plan.md §6.5)
    t = pd.read_csv(DB / "arbrat_viari.csv", usecols=["cat_nom_cientific", "tipus_element"])
    t = t[t.tipus_element == "ARBRE VIARI"]
    n_sp = t.cat_nom_cientific.value_counts().reindex(species).fillna(0).values
    planes_city = int(t.cat_nom_cientific.str.startswith("Platanus").sum())
    P = sum(len(q["pos"]) for q in parts)
    cap = layout.city_cap(n_sp, len(t), P, planes_city)
    print(f"{len(t)} street trees, {planes_city} planes; {P} planes in {len(parts)} barris; city cap here:",
          dict(zip(species, cap)))

    # 3. one sweep over the stacked positions
    stack = lambda k: np.vstack([q[k] for q in parts])
    objs = {"summer": (stack("summer"), 1), "winter": (stack("winter"), -1), "runoff": (stack("water"), 1)}
    local = (np.repeat(np.arange(len(parts)), [len(q["pos"]) for q in parts]), np.vstack([q["local"] for q in parts])) if loc else None
    if loc:                                           # name the barris where the local ceiling leaves no feasible layout
        for q in parts:
            try:
                layout.assign(np.zeros(q["fit"].shape), cap, q["fit"], local=(np.zeros(len(q["pos"]), int), q["local"][None]))
            except RuntimeError:
                print(f"INFEASIBLE {q['name']}: {len(q['pos'])} positions, no fit {int((~q['fit'].any(1)).sum())},",
                      "local cap", dict(zip(species, q["local"])), "fit per species", dict(zip(species, q["fit"].sum(0))))
    lay = layout.sweep(objs, cap, stack("fit"), local=local)
    cut = np.cumsum([0] + [len(q["pos"]) for q in parts])

    # 4. re-score each barri with the full models
    OUT.mkdir(exist_ok=True)
    allres, counts = {}, []
    for k, q in enumerate(parts):
        print(f"evaluate {q['name']}", flush=True)
        site = load_site(q["name"] if q["slug"] != "porta" else "porta")
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        res = [dict(scenario="S0_current", **layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p))]
        for w, ch in lay.items():
            c = ch[cut[k]:cut[k + 1]]
            sc = "S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w)
            n = {sp: int((c == j).sum()) for j, sp in enumerate(species)}
            res.append(dict(scenario=sc, **layout.evaluate(site, layout.apply(site, q["pos"], q["pal"], c), sun, lit, p),
                            eff_species=layout.eff_species(c, len(species)), **n))
            counts.append(dict(barri=q["name"], scenario=sc, **n))
        allres[q["name"]] = res = pd.DataFrame(res).set_index("scenario")
        res.round(1).to_csv(OUT / f"tool_v0_citylp{sfx}_{q['slug']}.csv")
    # one joint layout for every barri (the per-barri best would mix weights and break the city cap): most summer shade in total
    best = pd.concat([r.shade_summer_m2h.iloc[1:] for r in allres.values()], axis=1).sum(1).idxmax()
    rows = []
    for q in parts:
        r = allres[q["name"]]
        s0, b = r.loc["S0_current"], r.loc[best]
        rows.append(dict(barri=q["name"], planes=len(q["pos"]), layout=best,
                         **{f"{v}_pct_citylp": round(100 * b[f"shade_{v}_m2h"] / s0[f"shade_{v}_m2h"], 1) for v in ("summer", "winter")},
                         runoff_hot_change_pct_citylp=round(100 * (b.runoff_hot_m3 / s0.runoff_hot_m3 - 1), 1),
                         max_genus_pct_citylp=round(b.max_genus_pct, 1), max_genus_citylp=b.max_genus))
    out = pd.DataFrame(rows)
    ref = pd.read_csv(DB / "barris_summary.csv").drop_duplicates("barri")[["barri", "summer_pct_s1a", "summer_pct_s1b", "summer_pct_tool"]]
    out = out.merge(ref, on="barri", how="left")
    out["citylp_minus_local_pts"] = (out.summer_pct_citylp - out.summer_pct_tool).round(1)
    out.to_csv(DB / f"citylp{sfx}_summary.csv", index=False)
    c = pd.DataFrame(counts)
    tot = c.groupby("scenario")[species].sum().reset_index().assign(barri="ALL")
    pd.concat([c, tot, pd.DataFrame([dict(barri="CITY_CAP", scenario="", **dict(zip(species, cap)))])]).to_csv(
        DB / f"citylp{sfx}_species.csv", index=False)
    print(out.to_string(index=False))
    city_totals(barris, sfx)
    add_only()
