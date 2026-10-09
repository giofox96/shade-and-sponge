"""Species palette, per-position potentials and layout optimisation (methodology §6, v0).
Decision: the species at each plane-tree position. Constraint: no species above 15% of the site's street trees.
v0 optimiser: weighted sum of the normalised potentials (summer shade, winter shade, hotspot runoff), solved exactly
as a transportation LP (HiGHS); sweeping the weights gives a trade-off front. Every layout is then re-scored with the full raster models (overlaps).
NSGA-II comes later, if the weighted-sum front leaves gaps."""
import itertools, numpy as np, pandas as pd
from scipy import ndimage, sparse
from scipy.optimize import linprog
from .site import DB, rc
from . import heat, runoff, season

CITY_PALETTE = ["Celtis australis", "Melia azedarach", "Pyrus calleryana", "Jacaranda mimosifolia", "Tipuana tipu",
                "Brachychiton populneus"]   # named by the city as plane replacements (notes/topic_decision.md §7)
MAX_SHARE = 0.15                            # tree master plan: no species above 15% (notes/topic_decision.md §7)
MIN_LIDAR = 20                              # ASSUMPTION: species need >= 20 LiDAR-measured trees for median traits


def slug(species):
    """Column-safe species name: 'Tilia x euchlora' -> 'tilia_euchlora', 'Citrus × aurantium' -> 'citrus_aurantium'."""
    return "_".join(w for w in species.lower().replace("×", "x").split() if w != "x")


def palette_names(kind):
    """'city': the six species the city names as plane replacements; 'barcelona': the shortlist of species common in
    Barcelona's streets (scripts/species_shortlist.py) with enough LiDAR-measured trees (scripts/bcn_lidar_species.py)."""
    if kind == "city":
        return CITY_PALETTE, "porta_species_lidar_summary.csv"
    sl = pd.read_csv(DB / "species_shortlist.csv")
    n = pd.read_csv(DB / "species_lidar_summary.csv").set_index("species").n
    return [s for s in sl[sl.status == "candidate"].species if n.get(s, 0) >= MIN_LIDAR], "species_lidar_summary.csv"


def palette(site, kind="city"):
    """Species traits = median of the species' LiDAR-measured trees (Porta only for 'city'; Porta + three city tiles
    for 'barcelona') and how many more each may get under the cap."""
    names, summary = palette_names(kind)
    s = pd.read_csv(DB / summary).set_index("species").loc[names]
    p = pd.DataFrame(dict(species=names, crown_diam_m=s.crown_diam_med.values, height_m=s.height_med.values,
                          crown_base_m=s.crown_base_med.values, lai=s.lai_proxy_med.values, n_lidar=s.n.values))
    t = site.trees
    kept = t[~t.is_plane].sp.value_counts().reindex(names).fillna(0).values
    p["cap"] = (np.floor(MAX_SHARE * len(t)) - kept).clip(0).astype(int)
    p["storm_leaf_factor"] = season.storm_factor(names).round(3)    # season-weighted share of full-leaf LAI in storms
    return p


def fits(site, pos, pal):
    """Crown clearance from façades (methodology §6): crown radius <= distance from the position to the nearest building.
    ASSUMPTION: no extra margin; building = OSM footprint or LiDAR building points > 3 m above ground."""
    d = ndimage.distance_transform_edt(~(site.roof | (site.bldg_h > 3))) * site.res
    r, c = rc(site, pos.x.values, pos.y.values)
    f = d[r, c][:, None] >= pal.crown_diam_m.values[None, :] / 2
    f[~f.any(1), pal.crown_diam_m.values.argmin()] = True     # nothing fits: smallest crown
    return f


def _box_mean(mask, side, site):
    """Share of mask cells in a square of the given side (m) around each cell."""
    return ndimage.uniform_filter(mask.astype("float32"), size=max(1, int(round(side / site.res))))


def shade_potential(site, pos, pal, suns, lits, month):
    """shade[i, j]: m²·h of effective shade species j alone would cast on sunlit open ground from position i (no overlaps)."""
    open_ = site.domain & ~site.roof
    op = heat.opacity(pal.species, pal.lai.values, month)
    out = np.zeros((len(pos), len(pal)))
    for (alt, az), lit in zip(suns, lits):
        f = lit & open_
        dx, dy, area = heat.shadow_xy_area(pal.crown_diam_m.values, pal.height_m.values, pal.crown_base_m.values, alt, az)
        for j in range(len(pal)):
            r, c = rc(site, pos.x.values + dx[j], pos.y.values + dy[j])
            out[:, j] += _box_mean(f, np.sqrt(area[j]), site)[r, c] * area[j] * op[j]
    return out


def water_potential(site, pos, pal, p_mm, runoff_target="hotspot"):
    """water[i, j]: m³ intercepted (season-weighted) over open ground, counting only ground that drains to high
    flood-hazard cells if runoff_target == "hotspot"."""
    tgt = site.domain & ~site.roof & (site.to_hot if runoff_target == "hotspot" else True)
    area = np.pi * (pal.crown_diam_m.values / 2) ** 2
    r, c = rc(site, pos.x.values, pos.y.values)
    out = np.zeros((len(pos), len(pal)))
    for j, d in enumerate(pal.crown_diam_m.values):
        stor = sum(w * min(p_mm, runoff.P_["s_mm_per_lai"] * pal.lai.values[j] * season.factor([pal.species[j]], m)[0])
                   for m, w in season.STORM.items()) / season.STORM.sum()
        out[:, j] = _box_mean(tgt, d, site)[r, c] * area[j] * stor / 1000
    return out


def assign(score, cap, fit):
    """Max total score, one fitting species per position, species counts <= cap (transportation LP, integral at a vertex)."""
    P, S = score.shape
    A_eq = sparse.kron(sparse.eye(P), np.ones((1, S)))
    A_ub = sparse.kron(np.ones((1, P)), sparse.eye(S))
    res = linprog(-score.ravel(), A_ub=A_ub, b_ub=cap, A_eq=A_eq, b_eq=np.ones(P),
                  bounds=np.c_[np.zeros(P * S), fit.ravel()], method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    return res.x.reshape(P, S).argmax(1)


def sweep(objs, cap, fit, step=0.25):
    """objs: {name: (potential matrix, +1 to maximise / −1 to minimise)}. Every weight combination on a simplex grid
    (step 0.25 -> 15 combinations for 3 objectives); potentials normalised by their maximum. A 1e-3 share of the
    unweighted sum breaks ties (e.g. positions that do not drain to a hotspot)."""
    n = int(round(1 / step))
    norm = [sign * m / m.max() for m, sign in objs.values()]
    out = {}
    for c in itertools.product(range(n + 1), repeat=len(objs)):
        if sum(c) == n:
            w = np.array(c) / n
            out[tuple(w)] = assign(sum(wk * m for wk, m in zip(w, norm)) + 1e-3 * sum(norm), cap, fit)
    return out


def random_layout(cap, fit, rng):
    """Baseline: each position gets a random fitting palette species that still has room under its cap."""
    left, out = cap.copy(), []
    for f in fit:
        j = rng.choice(np.flatnonzero((left > 0) & f))
        left[j] -= 1
        out.append(j)
    return np.array(out)


def apply(site, pos, pal, choice):
    """Full street-tree set: kept trees (LiDAR crowns) + the chosen species at the plane positions."""
    t = site.trees
    kept = t[~t.is_plane & (t.flag == "ok")]
    new = pos[["tree_id", "x", "y"]].copy()
    for k in ("species", "crown_diam_m", "height_m", "crown_base_m", "lai"):
        new[k] = pal[k].values[choice]
    new["sp"] = new.species
    return pd.concat([kept, new], ignore_index=True)


def evaluate(site, trees, sun, lit, p_mm):
    """Heat proxy per season (summer shade = benefit, winter shade = cost); runoff season-weighted, plus the full-leaf
    (LiDAR, September) value for reference."""
    leafon = {f"{k}_leafon": v for k, v in runoff.event(site, trees, p_mm).items()}
    shade = {f"shade_{s}_m2h": heat.shade_m2h(site, trees, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    return dict(**shade, **season.runoff_seasonal(site, trees, p_mm), **leafon)


def pareto(df, maximise=("shade_summer_m2h",), minimise=("shade_winter_m2h", "runoff_hot_m3")):
    """Rows not dominated by any other row."""
    v = np.c_[df[list(maximise)].values, -df[list(minimise)].values]
    return np.array([not np.any(np.all(v >= v[i], 1) & np.any(v > v[i], 1)) for i in range(len(v))])
