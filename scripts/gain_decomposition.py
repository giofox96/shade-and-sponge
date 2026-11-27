"""Why the method wins: split its summer-shade gain over city practice into placement, species choice and palette width
(notes/tutor_feedback_24nov.md §3b, R2). Four layouts on the same positions, all scored with the same models:
  1 practice   = what the city does: S1b (the mix it planted in place of planes 2018–2026, 10 seeds) in Porta; the species it
                 really planted in each back-test group (scripts/backtest_works.py)
  2 placed     = the SAME species, in the same numbers, assigned to the positions by the LP (only *where* changes)
  3 method_7   = the LP with the city's 7 replacement species (layout.CITY_PALETTE)
  4 method_30  = the LP with the Barcelona palette (the tool's default)
Gains: placement = 2 − 1, species choice = 3 − 2, wider palette = 4 − 3; they add up to 4 − 1.
In a back-test group planted with one species (18 of 26) placement cannot be measured (nothing to swap): it is left empty (NaN),
not 0, and the bars draw it as 0.
Every LP uses the balanced weights (0.50 summer, 0.25 winter, 0.25 hotspot runoff), normalised as layout.sweep does.
Constraints: 2 keeps the practice's species counts as exact caps and the same fit rules as 4 (façade clearance + 2011 sizing
rule; backtest_works.fit_matrix in the back-test), except that a position may always keep the species practice gave it, so
the counts stay feasible (the city's own choice is not held to the rules). 3 and 4 have the 15% cap and the fit rules.
So "species choice" (3 − 2) also contains the effect of holding the city's species to the rules; read it with that.
Traits at equal trunk size (TERCERA), as in the Porta runs and the back-test (same ASSUMPTIONs as there).

Run on the PC (needs the LiDAR rasters and the barri bundles), from the project root:
  python scripts/gain_decomposition.py [--rule guide] [--skip-porta] [--skip-backtest]
Outputs: databases/barcelona/gain_decomposition_porta.csv (one row per S1b seed + mean),
         databases/barcelona/gain_decomposition_backtest[_guide].csv (one row per works group),
         notes/figures/gain_decomposition[_guide].png (stacked bars)."""
import copy, importlib.util, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import DB, load_site, norm  # noqa: E402
from shade_sponge import heat, runoff, layout, season  # noqa: E402

BAL = np.array([0.5, 0.25, 0.25])
VARIANTS = ["practice", "placed", "method_7", "method_30"]
GAINS = [("placement", "placed", "practice"), ("species choice", "method_7", "placed"), ("wider palette", "method_30", "method_7")]
TAG = "_guide" if "--rule" in sys.argv and sys.argv[sys.argv.index("--rule") + 1] == "guide" else ""


def balanced(site, pos, pal, sun, lit, p_mm, cap, fit):
    """The LP at the balanced weights (layout.sweep's normalisation and tie-break, one weight only)."""
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    water = layout.water_potential(site, pos, pal, p_mm)
    norm_ = [sg * m / m.max() if m.max() > 0 else np.zeros_like(m, float)
             for m, sg in ((pot["summer"], 1), (pot["winter"], -1), (water, 1))]
    return layout.assign(sum(w * m for w, m in zip(BAL, norm_)) + 1e-3 * sum(norm_), np.asarray(cap), fit)


def placed(site, pos, sp, get, sun, lit, p_mm, fitter):
    """Variant 2: the practice species sp (list, one per position) re-assigned by the LP, counts fixed."""
    names = list(dict.fromkeys(sp))
    pal = pd.DataFrame([dict(species=s, **get(s)) for s in names])
    own = np.array([names.index(s) for s in sp])
    pal["cap"] = np.bincount(own, minlength=len(names))
    fit = fitter(pal)
    fit[np.arange(len(sp)), own] = True                    # keeping practice's own choice is always allowed
    ch = balanced(site, pos, pal, sun, lit, p_mm, pal.cap.values, fit)
    return pal.species.values[ch].tolist()


def trees_with(kept, pos, sp, get):
    new = pd.DataFrame([dict(tree_id=t, x=x, y=y, species=s, sp=s, **get(s)) for t, x, y, s in zip(pos.tree_id, pos.x, pos.y, sp)])
    return pd.concat([kept, new], ignore_index=True)


def score(site, trees, sun, lit, p_mm):
    r = {f"shade_{s}": heat.shade_m2h(site, trees, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    ro = season.runoff_seasonal(site, trees, p_mm)
    return dict(**r, runoff_hot=ro["runoff_hot_m3"], runoff=ro["runoff_m3"])


def gains(r):
    for k, a, b in GAINS:
        r[f"gain_{k.replace(' ', '_')}"] = r[f"shade_summer_{a}"] - r[f"shade_summer_{b}"]
    r["gain_total"] = r["shade_summer_method_30"] - r["shade_summer_practice"]
    return r


def porta():
    site = load_site("porta")
    sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
    lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
    p_mm = runoff.design_storm(2, 60)
    gone = layout.removed(site.trees)
    pos = site.trees[gone].reset_index(drop=True)
    kept = site.trees[~site.trees.tree_id.isin(pos.tree_id) & (site.trees.flag == "ok")]
    palB, palC = (layout.palette(site, k, "TERCERA", gone) for k in ("barcelona", "city"))
    fitB, fitC = (layout.fits(site, pos, p, "exact", cap=p.cap.values) for p in (palB, palC))
    traits = palB.set_index("species")[["crown_diam_m", "height_m", "crown_base_m", "lai"]]
    get = lambda s: traits.loc[s].to_dict()  # noqa: E731  (S1b only draws palette species)
    fitter = lambda pal: layout.fits(site, pos, pal, "exact")  # noqa: E731
    m7 = palC.species.values[balanced(site, pos, palC, sun, lit, p_mm, palC.cap.values, fitC)].tolist()
    m30 = palB.species.values[balanced(site, pos, palB, sun, lit, p_mm, palB.cap.values, fitB)].tolist()
    getC = palC.set_index("species")[["crown_diam_m", "height_m", "crown_base_m", "lai"]]
    fixed = {k: score(site, trees_with(kept, pos, sp, (lambda s, t=t: t.loc[s].to_dict())), sun, lit, p_mm)
             for k, sp, t in (("method_7", m7, getC), ("method_30", m30, traits))}
    mix_b, rows = layout.s1b_mix(), []
    for k in range(10):                                    # the same seeds as python -m shade_sponge (S1b_obs_k)
        ch = layout.s1a_layout(palB, palB.cap.values, fitB, np.random.default_rng(200 + k), mix_b)
        prac = palB.species.values[ch].tolist()
        lay = {"practice": prac, "placed": placed(site, pos, prac, get, sun, lit, p_mm, fitter)}
        r = dict(seed=k, n=len(pos))
        for v, sp in lay.items():
            r.update({f"{m}_{v}": x for m, x in score(site, trees_with(kept, pos, sp, get), sun, lit, p_mm).items()})
        for v, s in fixed.items():
            r.update({f"{m}_{v}": x for m, x in s.items()})
        rows.append(gains(r))
        print(f"Porta seed {k}: " + ", ".join(f"{g} {r['gain_' + g.replace(' ', '_')]:+,.0f}" for g, _, _ in GAINS) + " m²·h")
    df = pd.DataFrame(rows)
    df = pd.concat([df, df.mean(numeric_only=True).to_frame().T.assign(seed="mean")], ignore_index=True)
    df.round(2).to_csv(DB / "gain_decomposition_porta.csv", index=False)
    return df.iloc[-1]


def backtest():
    spec = importlib.util.spec_from_file_location("backtest_works", ROOT / "scripts/backtest_works.py")
    bw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bw)                            # reads --rule guide from sys.argv itself
    from rasterio.features import rasterize
    from scipy.spatial import cKDTree
    from shapely.geometry import MultiPoint
    from shade_sponge.site import city_trees
    d = bw.works_groups()
    where = bw.place(d)
    groups = sorted((k, g) for g, k in where.items() if k)
    p_mm, pool, rows = runoff.design_storm(2, 60), city_trees(), []
    for slug in dict.fromkeys(k for k, _ in groups):
        site = load_site(slug)
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        T = site.trees
        kd = cKDTree(T[["x", "y"]].values)
        for _, g in (x for x in groups if x[0] == slug):  # set-up as in backtest_works.main
            m = d[d.group == g].reset_index(drop=True)
            xy = m[["x", "y"]].values
            near = sorted({i for hit in kd.query_ball_point(xy, bw.R_MATCH) for i in hit})
            gone = np.isin(np.arange(len(T)), near) | T.tree_id.isin(m.codi_out).values | T.tree_id.isin(m.codi_in).values
            tid = np.where(m.codi_out.isin(T.tree_id), m.codi_out, np.where(m.codi_in.isin(T.tree_id), m.codi_in, "w" + m.index.astype(str)))
            pos = pd.DataFrame(dict(tree_id=tid, x=m.x, y=m.y))
            loc = copy.copy(site)
            loc.domain = rasterize([(MultiPoint(xy).buffer(bw.R_DOM), 1)], out_shape=site.domain.shape, transform=site.transform,
                                   fill=0).astype(bool)
            palB, palC = (layout.palette(site, k, "TERCERA", gone) for k in ("barcelona", "city"))
            get0 = bw.traits_lookup(palB, pool)
            get = lambda s: get0(s)[0]  # noqa: E731
            fitter = lambda pal: bw.fit_matrix(site, pos, pal, layout)[0]  # noqa: E731
            city = m.species_in.map(norm).tolist()
            lay = {"practice": city, "placed": placed(loc, pos, city, get, sun, lit, p_mm, fitter),
                   "method_7": palC.species.values[balanced(loc, pos, palC, sun, lit, p_mm, palC.cap.values, fitter(palC))].tolist(),
                   "method_30": palB.species.values[balanced(loc, pos, palB, sun, lit, p_mm, palB.cap.values, fitter(palB))].tolist()}
            kept = T[~gone & (T.flag == "ok")]
            getC = palC.set_index("species")[["crown_diam_m", "height_m", "crown_base_m", "lai"]]
            r = dict(group=g, barri=slug, quarter=m.quarter_added.iloc[0], n=len(m), n_species_practice=len(set(city)))
            for v, sp in lay.items():
                gt = (lambda s: getC.loc[s].to_dict()) if v == "method_7" else get
                r.update({f"{k}_{v}": x for k, x in score(loc, trees_with(kept, pos, sp, gt), sun, lit, p_mm).items()})
                r[f"top_{v}"] = pd.Series(sp).mode()[0]
            rows.append(gains(r))
            if r["n_species_practice"] == 1:                 # one species: nothing to swap, placement is not measured here
                r["gain_placement"] = np.nan
            print(f"{slug} {r['quarter']} n={r['n']}: " + ", ".join(f"{k} {r['gain_' + k.replace(' ', '_')]:+,.0f}" for k, _, _ in GAINS))
    df = pd.DataFrame(rows)
    df.round(2).to_csv(DB / f"gain_decomposition_backtest{TAG}.csv", index=False)
    return df


def figure(p, bt):
    """Left: Porta (mean of 10 seeds) and the back-test pooled over all groups, as % of practice's summer shade.
    Right: the same split per back-test group (% of that group's practice), sorted by total gain."""
    import matplotlib.pyplot as plt
    cols = {"placement": "#9DB4DE", "species choice": "#D9B866", "wider palette": "#7A9A6B"}
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw=dict(width_ratios=[1, 3]))

    def bars(ax, labels, parts, total):
        x = np.arange(len(labels))
        for sign in (1, -1):                               # positives stack up from 0, negatives down from 0
            base = np.zeros(len(labels))
            for k in cols:
                v = np.where(np.sign(parts[k]) == sign, parts[k], 0)
                ax.bar(x, v, bottom=base, color=cols[k], label=k if sign == 1 else None, width=0.7)
                base += v
        ax.scatter(x, total, color="black", s=12, zorder=3, label="total")
        ax.axhline(0, color="grey", lw=0.6)
        ax.set_xticks(x, labels, rotation=0 if len(labels) < 4 else 90, fontsize=8)
        ax.set_ylabel("summer shade gain, % of practice")

    pooled = {k: [] for k in cols}
    sources = ([p] if p is not None else []) + ([bt.sum(numeric_only=True)] if bt is not None else [])
    labels = (["Porta"] if p is not None else []) + (["back-test\n(all groups)"] if bt is not None else [])
    for s in sources:
        for k in cols:
            pooled[k].append(100 * s[f"gain_{k.replace(' ', '_')}"] / s["shade_summer_practice"])
    bars(a, labels, {k: np.array(v) for k, v in pooled.items()}, np.sum([pooled[k] for k in cols], 0))
    a.legend(fontsize=8, frameon=False)
    if bt is not None:
        q = bt.assign(tot=bt.gain_total / bt.shade_summer_practice).sort_values("tot")
        parts = {k: np.nan_to_num((100 * q[f"gain_{k.replace(' ', '_')}"] / q.shade_summer_practice).values) for k in cols}
        bars(b, [f"{s[:12]} {qq}" for s, qq in zip(q.barri, q.quarter)], parts, 100 * q.tot.values)
        b.set_title("per back-test group", fontsize=9)
    a.set_title("why the method wins: summer shade vs city practice", fontsize=9)
    fig.tight_layout()
    out = ROOT / f"notes/figures/gain_decomposition{TAG}.png"
    fig.savefig(out, dpi=200)
    print("figure:", out)


if __name__ == "__main__":
    p = None if "--skip-porta" in sys.argv else porta()
    bt = None if "--skip-backtest" in sys.argv else backtest()
    figure(p, bt)
