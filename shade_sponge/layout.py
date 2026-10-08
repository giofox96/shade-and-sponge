"""Species palette, per-position potentials and layout optimisation (methodology §6, v0).
Decision: the species at each plane-tree position. Constraint: no species above 15% of the site's street trees.
v0 optimiser: weighted sum of the two normalised potentials, solved exactly as a transportation LP (HiGHS);
sweeping the weight gives a trade-off front. Every layout is then re-scored with the full raster models (overlaps).
NSGA-II comes later, if the weighted-sum front leaves gaps."""
import numpy as np, pandas as pd
from scipy import ndimage, sparse
from scipy.optimize import linprog
from .site import DB, rc
from . import heat, runoff

CITY_PALETTE = ["Celtis australis", "Melia azedarach", "Pyrus calleryana", "Jacaranda mimosifolia", "Tipuana tipu",
                "Brachychiton populneus"]   # named by the city as plane replacements (notes/topic_decision.md §7)
MAX_SHARE = 0.15                            # tree master plan: no species above 15% (notes/topic_decision.md §7)


def palette(site, names=CITY_PALETTE):
    """Species traits = median of the species' trees in Porta (LiDAR 2021) and how many more each may get (cap)."""
    s = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species").loc[names]
    p = pd.DataFrame(dict(species=names, crown_diam_m=s.crown_diam_med.values, height_m=s.height_med.values,
                          crown_base_m=s.crown_base_med.values, lai=s.lai_proxy_med.values, n_lidar=s.n.values))
    t = site.trees
    kept = t[~t.is_plane].sp.value_counts().reindex(names).fillna(0).values
    p["cap"] = (np.floor(MAX_SHARE * len(t)) - kept).clip(0).astype(int)
    return p


def fits(site, pos, pal):
    """Crown clearance from façades (methodology §6): crown radius <= distance from the position to the nearest building.
    ASSUMPTION: no extra margin; building = OSM footprint or LiDAR building points > 3 m above ground."""
    d = ndimage.distance_transform_edt(~(site.roof | (site.bldg_h > 3))) * site.res
    r, c = rc(site, pos.x.values, pos.y.values)
    f = d[r, c][:, None] >= pal.crown_diam_m.values[None, :] / 2
    f[~f.any(1), pal.crown_diam_m.values.argmin()] = True     # nothing fits: smallest crown
    return f


def _disk_mean(mask, diam, site):
    """Share of mask cells in a square of side = crown diameter around each cell (box filter)."""
    return ndimage.uniform_filter(mask.astype("float32"), size=max(1, int(round(diam / site.res))))


def potentials(site, pos, pal, suns, lits, p_mm, runoff_target="hotspot"):
    """Benefit of species j alone at position i, ignoring overlaps:
    shade[i, j] (m²·h of effective shade on sunlit open ground) and water[i, j] (m³ intercepted over open ground,
    counting only ground that drains to high flood-hazard cells if runoff_target == "hotspot")."""
    open_ = site.domain & ~site.roof
    tgt = open_ & site.to_hot if runoff_target == "hotspot" else open_
    area = np.pi * (pal.crown_diam_m.values / 2) ** 2
    shade, water = np.zeros((len(pos), len(pal))), np.zeros((len(pos), len(pal)))
    zc = (pal.height_m.values + pal.crown_base_m.values) / 2
    for (alt, az), lit in zip(suns, lits):
        for j, d in enumerate(pal.crown_diam_m.values):
            r, c = rc(site, *heat.shadow_xy(pos.x.values, pos.y.values, zc[j], alt, az))
            shade[:, j] += _disk_mean(lit & open_, d, site)[r, c] * area[j] * (1 - np.exp(-heat.K * pal.lai.values[j]))
    r, c = rc(site, pos.x.values, pos.y.values)
    for j, d in enumerate(pal.crown_diam_m.values):
        stor = min(p_mm, runoff.P_["s_mm_per_lai"] * pal.lai.values[j])
        water[:, j] = _disk_mean(tgt, d, site)[r, c] * area[j] * stor / 1000
    return shade, water


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


def sweep(shade, water, cap, fit, weights=np.linspace(0, 1, 11)):
    """Weight w on heat, 1 − w on runoff (each potential normalised by its maximum). A 1e-3 share of the other
    objective breaks ties (e.g. positions that do not drain to a hotspot when w = 0)."""
    hn, wn = shade / shade.max(), water / water.max()
    return {round(float(w), 2): assign(w * hn + (1 - w) * wn + 1e-3 * (hn + wn), cap, fit) for w in weights}


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
    return pd.concat([kept, new], ignore_index=True)


def evaluate(site, trees, suns, lits, p_mm):
    return dict(shade_m2h=heat.shade_m2h(site, trees, suns, lits), **runoff.event(site, trees, p_mm))


def pareto(df, maximise="shade_m2h", minimise="runoff_hot_m3"):
    """Rows not dominated by any other row."""
    a, b = df[maximise].values, df[minimise].values
    return np.array([not np.any((a >= a[i]) & (b <= b[i]) & ((a > a[i]) | (b < b[i]))) for i in range(len(df))])
