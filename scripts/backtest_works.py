"""Back-test on real street works: what the city planted vs what the method would have chosen, at the same positions.

Works areas = replacement groups of >= 10 trees changed in one quarter within 25 m (scripts/replacement_clusters.py,
notes/tutor_feedback_10nov.md A1), kept only if they look like a planting: >= 50% of the new trees are PRIMERA (the
smallest trunk class), and not the Tabebuia rosea -> Handroanthus heptaphyllus group (a likely re-identification, same note).
Each group is placed in the barri whose LiDAR tree table (scripts/bcn_lidar_barri.py) holds most of its members, by code
or within R_MATCH; groups in barris without LiDAR are skipped.

Per group, on that barri's site bundle (shade_sponge.site), the decision set is the group's positions; every other street
tree is kept as measured. Five layouts are scored:
  none = the positions empty · before = the species the city removed · city = the species it planted ·
  method_bal = the LP with balanced weights (0.50 summer, 0.25 winter, 0.25 hotspot runoff) · method_sum = summer only.
The method uses the Barcelona palette, the 15% cap (layout.palette, barri-local as in the citywide runs), façade clearance
and the exact sizing rule of the 2011 guide.
ASSUMPTION: every species at the crown it has at equal trunk size (TERCERA, layout.palette's rule; species outside the
palette from the city LiDAR pool: TERCERA, SEGONA, all classes with >= 20 trees, else all classes >= 5, else the genus,
else the pool's TERCERA median). So "before" is not the old trees as they were, and "city" is not the young trees as
planted: all three are compared at the same size (declared in notes/tutor_feedback_10nov.md A1, life cycle).
ASSUMPTION: scored on a local domain = 40 m around the positions (summer crown shadows at 12–17 h fall well inside it).
Limits: trees the works removed without replacement, or added at new spots, are not in the decision set; the city's
choice is not held to the sizing rule or façade clearance, the method's is.

Rule variant `--rule guide` (decided by the user, 16 Nov 2026): where the sidewalk class was measured, only the 2011 guide's
sizing rule decides; the crown-radius façade test (layout.fits, an ASSUMPTION stricter than the city's own practice, e.g.
C. Piquer) applies only to "check" positions. Where no species fits, the best-scoring species the sizing rule allows is
taken (the LP chooses among them), not the smallest crown. Species without a guide size class (Celtis sinensis) are not
allowed on measured sidewalks, since size_fits cannot filter them; only rows with nothing allowed keep layout.fits' fallback.
Every row reports fallback_share = positions where layout.fits had no choice (forced smallest crown).

Run (PC with the barri rasters, as python -m shade_sponge "<barri>"): python scripts/backtest_works.py [--list] [--rule guide]
Outputs: databases/barcelona/backtest_works[_guide].csv (one row per group), backtest_works[_guide]_positions.csv (one row
per position)
"""
import ast, copy, sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import DB, BARRIS, norm, rc, trees_porta, trees_barri  # noqa: E402

R_MATCH, R_DOM, MIN_N, MIN_PRIM = 2.0, 40.0, 10, 0.5
BAL, SUM = (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)


GUIDE = "--rule" in sys.argv and sys.argv[sys.argv.index("--rule") + 1] == "guide"
CAP_SMALL = "--cap-small" in sys.argv     # sensitivity: guide "small" species at most crown 4 m, height 6 m (2011 guide limits)


def fit_matrix(site, pos, pal, layout):
    """Allowed species per position (see the docstring) and the mask of positions where layout.fits fell back."""
    f = layout.fits(site, pos, pal, "exact", cap=pal.cap.values)
    dist = ndimage.distance_transform_edt(~(site.roof | (site.bldg_h > 3))) * site.res   # layout.fits' façade test,
    fac = dist[rc(site, pos.x.values, pos.y.values)][:, None] >= pal.crown_diam_m.values[None, :] / 2   # without fallback
    d = layout.size_fits(layout.sidewalk_class(pos, site), pal.species, "exact") & (pal.cap.values > 0)[None, :]
    fell = ~(fac & d).any(1) & (f.sum(1) == 1)
    if not GUIDE:
        return f, fell
    measured = layout.sidewalk_class(pos, site) != "check"
    classed = np.array([s in layout.SIZE_CLASS for s in pal.species])     # no guide class (Celtis sinensis): not on
    g = np.where(measured[:, None], d & classed[None, :], f)               # measured sidewalks (size_fits lets it pass)
    g[~g.any(1)] = f[~g.any(1)]
    return g, fell


def corrections(d):
    """Members that are inventory corrections, not replacements: the new tree keeps the code AND has the same planting
    date as before, or a planting date more than a year before quarter_added. Case: group 6687 (El Clot), 12 trees
    planted 2024-03-13 as Styphnolobium, re-identified as Quercus and moved ~6 m in 2026Q2, same codes and date.
    Dates: databases/barcelona/backtest_planting_dates.csv (scripts/backtest_planting_dates.py)."""
    pdt = pd.read_csv(DB / "backtest_planting_dates.csv", dtype=str).set_index(["codi", "quarter"]).data_plantacio
    iso = pdt.where(~pdt.str.contains("/", na=False), pd.to_datetime(pdt, format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d"))
    date = lambda cs, qs: pd.to_datetime(pd.Series([iso.get((c, q)) for c, q in zip(cs, qs)], index=d.index))  # noqa: E731
    before, after = date(d.codi_out, d.quarter_removed), date(d.codi_in, d.quarter_added)  # releases mix d/m/Y and ISO
    start = d.quarter_added.map(lambda q: pd.Period(q, "Q").start_time)
    return (d.codi_out == d.codi_in) & ((after == before) | ((start - after).dt.days > 365))


def works_groups(filter_corrections=True):
    src = (ROOT / "scripts/replacement_clusters.py").read_text(encoding="utf-8")
    ns = {"np": np, "pd": pd}
    exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) or
                             (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "EPS")], []), "rc", "exec"), ns)
    d = pd.read_csv(DB / "inventory_replacements.csv")
    d["group"] = ns["groups"](d, ns["EPS"])
    keep = lambda m: len(m) >= MIN_N and (m.size_in == "PRIMERA").mean() >= MIN_PRIM  # noqa: E731
    d = d.groupby("group").filter(keep)
    if filter_corrections:                       # inventory-correction filter, then the group rules again
        drop = corrections(d)
        for g, n in d[drop].groupby("group").size().items():
            print(f"inventory correction: group {g}, {n} of {(d.group == g).sum()} members dropped")
        d = d[~drop].groupby("group").filter(keep)
    reid = d.species_out.str.startswith("Tabebuia") & d.species_in.str.startswith("Handroanthus")
    return d[~d.group.isin(d[reid].group)]


def place(d):
    """Barri slug per group: the LiDAR tree table that holds most members (by code, else within R_MATCH)."""
    tabs = {"porta": trees_porta()} | {p.name: trees_barri(p.name) for p in sorted(BARRIS.glob("*"))
                                       if (p / "trees_lidar.csv").exists()}
    kd = {k: cKDTree(t[["x", "y"]].values) for k, t in tabs.items()}
    out = {}
    for g, m in d.groupby("group"):
        hits = {k: (t.tree_id.isin(m.codi_out) | t.tree_id.isin(m.codi_in)).sum() +
                np.isfinite(kd[k].query(m[["x", "y"]].values, distance_upper_bound=R_MATCH)[0]).sum()
                for k, t in tabs.items()}
        k = max(hits, key=hits.get)
        out[g] = k if hits[k] >= len(m) else None          # both counts together: at least one per member
    return out


def traits_lookup(pal, pool):
    """Crown, height, base and LAI of any species (see ASSUMPTION in the docstring); returns (dict, source)."""
    p = pal.set_index("species")
    ref = pool[pool.size_category == "TERCERA"][["crown_diam_m", "height_m", "crown_base_m", "lai"]].median()
    cache = {}

    def get(sp):
        if sp in cache:
            return cache[sp]
        if sp in p.index:
            r, src = p.loc[sp], "palette"
        else:
            g, gen = pool[pool.sp == sp], pool[pool.sp.str.split().str[0] == sp.split()[0]]
            for sub, src, k in ((g[g.size_category == "TERCERA"], "TERCERA (city)", 20),
                                (g[g.size_category == "SEGONA"], "SEGONA (city)", 20),
                                (g, "all classes (city)", 20), (g, "all classes (city, n>=5)", 5),
                                (gen, "genus (city)", 20)):
                if len(sub) >= k:
                    r = sub[["crown_diam_m", "height_m", "crown_base_m", "lai"]].median()
                    break
            else:
                r, src = ref, "pool TERCERA median"
        cache[sp] = (dict(crown_diam_m=r.crown_diam_m, height_m=r.height_m, crown_base_m=r.crown_base_m, lai=r.lai), src)
        return cache[sp]
    return get


def main():
    d = works_groups()
    where = place(d)
    if "--list" in sys.argv:
        s = d.groupby("group").agg(n=("x", "size"), quarter=("quarter_added", "first"),
                                   out=("species_out", lambda s: s.mode()[0]), inn=("species_in", lambda s: s.mode()[0]))
        print(s.assign(barri=s.index.map(where)).sort_values(["barri", "quarter"]).to_string())
        return
    from rasterio.features import rasterize
    from shapely.geometry import MultiPoint
    from shade_sponge.site import load_site, city_trees
    from shade_sponge import heat, runoff, layout, season

    p_mm = runoff.design_storm(2, 60)
    pool = city_trees()
    rows, prow = [], []
    groups = sorted((k, g) for g, k in where.items() if k)
    print(f"{len(where)} planting groups, {len(groups)} in barris with LiDAR")
    for slug in dict.fromkeys(k for k, _ in groups):
        site = load_site(slug)
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        T = site.trees
        kd = cKDTree(T[["x", "y"]].values)
        for _, g in (x for x in groups if x[0] == slug):
            m = d[d.group == g].reset_index(drop=True)
            xy = m[["x", "y"]].values
            near = sorted({i for hit in kd.query_ball_point(xy, R_MATCH) for i in hit})
            gone = np.isin(np.arange(len(T)), near) | T.tree_id.isin(m.codi_out).values | T.tree_id.isin(m.codi_in).values
            # position id: the member's own code if the site has it (sidewalk class lookup), else a new one
            tid = np.where(m.codi_out.isin(T.tree_id), m.codi_out, np.where(m.codi_in.isin(T.tree_id), m.codi_in, "w" + m.index.astype(str)))
            pos = pd.DataFrame(dict(tree_id=tid, x=m.x, y=m.y))
            loc = copy.copy(site)
            area = MultiPoint(xy).buffer(R_DOM)
            loc.domain = rasterize([(area, 1)], out_shape=site.domain.shape, transform=site.transform, fill=0).astype(bool)
            pal = layout.palette(site, "barcelona", "TERCERA", gone)
            if CAP_SMALL:                # same capped sizes for the city's and the method's trees (traits_lookup reads pal)
                sm = pal.species.map(lambda s: layout.SIZE_CLASS.get(s.replace("×", "x"), layout.SIZE_CLASS.get(s))) == "small"
                pal.loc[sm, "crown_diam_m"] = pal.loc[sm, "crown_diam_m"].clip(upper=4.0)
                pal.loc[sm, "height_m"] = pal.loc[sm, "height_m"].clip(upper=6.0)
                pal.loc[sm, "crown_base_m"] = np.minimum(pal.loc[sm, "crown_base_m"], pal.loc[sm, "height_m"] - 1.0)
            fit, fell = fit_matrix(site, pos, pal, layout)
            pot = {s: layout.shade_potential(loc, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
            water = layout.water_potential(loc, pos, pal, p_mm)
            sw = layout.sweep({"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)},
                              pal.cap.values, fit)
            get = traits_lookup(pal, pool)
            kept = T[~gone & (T.flag == "ok")]
            lay = {"none": [], "before": m.species_out.map(norm).tolist(), "city": m.species_in.map(norm).tolist(),
                   "method_bal": pal.species.values[sw[BAL]].tolist(), "method_sum": pal.species.values[sw[SUM]].tolist()}
            r = dict(group=g, barri=slug, quarter=m.quarter_added.iloc[0], n=len(m),
                     top_before=pd.Series(lay["before"]).mode()[0], top_city=pd.Series(lay["city"]).mode()[0],
                     top_method_bal=pd.Series(lay["method_bal"]).mode()[0], x=xy[:, 0].mean(), y=xy[:, 1].mean(),
                     size_class_measured=float((layout.sidewalk_class(pos, site) != "check").mean()),
                     fallback_share=float(fell.mean()),
                     city_species_in_palette=float(np.isin(lay["city"], pal.species).mean()),
                     traits_src="; ".join(sorted({f"{s}: {get(s)[1]}" for s in set(lay["before"] + lay["city"]) if get(s)[1] != "palette"})))
            for k, sp in lay.items():
                new = pd.DataFrame([dict(tree_id=t, x=x, y=y, species=s, sp=s, **get(s)[0])
                                    for t, x, y, s in zip(pos.tree_id, pos.x, pos.y, sp)]) if sp else pd.DataFrame()
                trees = pd.concat([kept, new], ignore_index=True)
                for s in sun:
                    r[f"shade_{s}_{k}"] = heat.shade_m2h(loc, trees, sun[s], lit[s], heat.SEASONS[s]["month"])
                ro = season.runoff_seasonal(loc, trees, p_mm)
                r[f"runoff_{k}"], r[f"runoff_hot_{k}"] = ro["runoff_m3"], ro["runoff_hot_m3"]
            for k in ("city", "method_bal", "method_sum"):       # shade of the new trees as % of the removed ones'
                r[f"summer_pct_{k}"] = 100 * (r[f"shade_summer_{k}"] - r["shade_summer_none"]) / \
                    (r["shade_summer_before"] - r["shade_summer_none"])
            rows.append(r)
            for i in range(len(m)):
                prow.append(dict(group=g, barri=slug, x=xy[i, 0], y=xy[i, 1], size_class=layout.sidewalk_class(pos, site)[i],
                                 **{f"sp_{k}": lay[k][i] for k in lay if k != "none"},
                                 **{f"crown_{k}": get(lay[k][i])[0]["crown_diam_m"] for k in lay if k != "none"}))
            print(f"{slug} {r['quarter']} n={r['n']}: {r['top_before']} -> city {r['top_city']} "
                  f"{r['summer_pct_city']:.0f}% | method {r['top_method_bal']} {r['summer_pct_method_bal']:.0f}% of the removed trees' summer shade")
    tag = ("_guide" if GUIDE else "") + ("_capsmall" if CAP_SMALL else "")
    pd.DataFrame(rows).round(3).to_csv(DB / f"backtest_works{tag}.csv", index=False)
    pd.DataFrame(prow).round(2).to_csv(DB / f"backtest_works{tag}_positions.csv", index=False)


if __name__ == "__main__":
    main()
