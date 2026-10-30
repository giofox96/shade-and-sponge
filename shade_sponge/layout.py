"""Species palette, per-position potentials and layout optimisation (methodology §6, v0).
Decision: the species at each plane-tree position. Constraint: no species above 15% of the site's street trees.
v0 optimiser: weighted sum of the normalised potentials (summer shade, winter shade, hotspot runoff), solved exactly
as a transportation LP (HiGHS); sweeping the weights gives a trade-off front. Every layout is then re-scored with the full raster models (overlaps).
NSGA-II comes later, if the weighted-sum front leaves gaps."""
import itertools, numpy as np, pandas as pd
from scipy import ndimage, sparse
from scipy.optimize import linprog
from .site import DB, CITY_LIDAR, rc, species_lidar
from . import heat, runoff, season

CITY_PALETTE = ["Celtis australis", "Melia azedarach", "Pyrus calleryana", "Jacaranda mimosifolia", "Tipuana tipu",
                "Brachychiton populneus",   # the first five are named as replacements (city or press); Brachychiton is
                                            # common in Porta's plantings but named in no source (notes/topic_decision.md §9.6, §10.4)
                "Styphnolobium japonicum"]  # added by the user 14 Oct (press, inventory D1); crown + LAI from a city-wide LiDAR sample (site.CITY_LIDAR)
MAX_SHARE = 0.15                            # tree master plan: no species above 15% (notes/topic_decision.md §7)
MIN_LIDAR = 20                              # ASSUMPTION: species need >= 20 LiDAR-measured trees for median traits
# Size class per species, 2011 street-tree guide catalogue pp. 49-56 (notes/tree_master_plan.md §5); species not listed
# here get no size filter (ASSUMPTION). Sidewalk width -> position class: scripts/porta_sidewalk_width.py (guide pp. 22-23).
SIZE_CLASS = {"Platanus x acerifolia": "large", "Celtis australis": "large", "Tipuana tipu": "large",
              "Jacaranda mimosifolia": "large", "Melia azedarach": "medium", "Styphnolobium japonicum": "medium",
              "Brachychiton populneus": "medium", "Pyrus calleryana": "small"}
RANK = {"none": -1, "small": 0, "medium": 1, "large": 2}
# S1a, the city's own replacement (notes/topic_decision.md §9.6, §10.4; decided 24 Oct): the 2026 target mix (Betevé,
# 7 May 2026, press 🟡: Celtis ~12%, Melia 7.25%, Pyrus, Sophora and Tipuana ~5% each), used as relative weights of a
# random draw within the sizing rule. ASSUMPTION: the city-wide target shares are read as replacement proportions, and
# Celtis's 12% as per species (the source is ambiguous: "planes and Celtis ~12%"; notes/tree_master_plan.md §5).
S1A_MIX = {"Celtis australis": 12, "Melia azedarach": 7.25, "Pyrus calleryana": 5, "Styphnolobium japonicum": 5,
           "Tipuana tipu": 5}
# Equal trunk size (notes/topic_decision.md §9.9, §10.5 row 8): species traits = medians of the Porta trees in one trunk
# class of the inventory (categoria_arbrat; TERCERA = 81–110 cm perimeter, 2011 guide p. 18). ASSUMPTION: TERCERA is the
# reference; a species with fewer than MIN_CLASS trees there falls back to SEGONA, then to all classes.
MIN_CLASS = 20


def slug(species):
    """Column-safe species name: 'Tilia x euchlora' -> 'tilia_euchlora', 'Citrus × aurantium' -> 'citrus_aurantium'."""
    return "_".join(w for w in species.lower().replace("×", "x").split() if w != "x")


def palette_names(kind):
    """'city': the species the city names as plane replacements (+ Styphnolobium); 'barcelona': the shortlist of species
    common in Barcelona's streets (scripts/species_shortlist.py) with enough LiDAR-measured trees (scripts/bcn_lidar_species.py)."""
    if kind == "city":
        return CITY_PALETTE, "porta_species_lidar_summary.csv"
    sl = pd.read_csv(DB / "species_shortlist.csv")
    n = pd.read_csv(DB / "species_lidar_summary.csv").set_index("species").n
    return [s for s in sl[sl.status == "candidate"].species if n.get(s, 0) >= MIN_LIDAR], "species_lidar_summary.csv"


def palette(site, kind="city", trunk=None):
    """Species traits = median of the species' LiDAR-measured trees (Porta only for 'city'; Porta + three city tiles
    for 'barcelona'; site.CITY_LIDAR overrides in both) and how many more each may get under the cap.
    trunk (e.g. "TERCERA"): use the medians of the species' Porta trees in that trunk class instead (MIN_CLASS)."""
    names, summary = palette_names(kind)
    s = species_lidar(summary).loc[names]
    p = pd.DataFrame(dict(species=names, crown_diam_m=s.crown_diam_med.values, height_m=s.height_med.values,
                          crown_base_m=s.crown_base_med.values, lai=s.lai_proxy_med.values, n_lidar=s.n.values))
    p["trunk_class"] = "all"
    if trunk:
        ok = site.trees[site.trees.flag == "ok"]
        for i, sp in enumerate(names):
            if sp in CITY_LIDAR:                              # Porta sample too small: city-wide medians kept
                continue
            for cls in (trunk, "SEGONA"):
                g = ok[(ok.sp == sp) & (ok.size_category == cls)]
                if len(g) >= MIN_CLASS:
                    p.loc[i, ["crown_diam_m", "height_m", "crown_base_m", "lai", "n_lidar"]] = [
                        g.crown_diam_m.median(), g.height_m.median(), g.crown_base_m.median(), g.lai.median(), len(g)]
                    p.loc[i, "trunk_class"] = cls
                    break
    t = site.trees
    kept = t[~t.is_plane].sp.value_counts().reindex(names).fillna(0).values
    p["cap"] = (np.floor(MAX_SHARE * len(t)) - kept).clip(0).astype(int)
    p["storm_leaf_factor"] = season.storm_factor(names).round(3)    # season-weighted share of full-leaf LAI in storms
    return p


def size_fits(pos_class, species, rule="exact"):
    """Sizing rule of the 2011 guide: "exact" = one tree class per sidewalk class, as the guide reads literally;
    "at_most" = smaller classes also allowed on wider sidewalks (ASSUMPTION). Positions classed "check" (no facade-bounded
    sidewalk: medians, boulevards, plaza edges) and species without a class are not filtered (ASSUMPTION)."""
    p = np.array([RANK.get(c, np.nan) for c in pos_class])[:, None]
    q = np.array([RANK.get(SIZE_CLASS.get(s), np.nan) for s in species])[None, :]
    ok = (q == p) if rule == "exact" else (q <= p)
    return ok | np.isnan(p) | np.isnan(q)


def sidewalk_class(pos, site=None):
    """Size class of each position from databases/barcelona/porta_sidewalk_width.csv, or barris/<slug>/sidewalk_width.csv
    for another barri (scripts/porta_sidewalk_width.py); "check" if not measured or not measured yet."""
    if "size_class" in pos:                               # new planting spots carry their own class
        return pos.size_class.values
    f = DB / ("porta_sidewalk_width.csv" if site is None or site.name == "porta" else f"barris/{site.name}/sidewalk_width.csv")
    if not f.exists():
        return np.full(len(pos), "check", dtype=object)
    w = pd.read_csv(f).set_index("tree_id").size_class
    return w.reindex(pos.tree_id).fillna("check").values


def fits(site, pos, pal, size_rule=None):
    """Crown clearance from façades (methodology §6): crown radius <= distance from the position to the nearest building.
    ASSUMPTION: no extra margin; building = OSM footprint or LiDAR building points > 3 m above ground.
    size_rule ("exact" / "at_most"): also apply the sidewalk-width sizing rule (size_fits); None = off."""
    d = ndimage.distance_transform_edt(~(site.roof | (site.bldg_h > 3))) * site.res
    r, c = rc(site, pos.x.values, pos.y.values)
    f = d[r, c][:, None] >= pal.crown_diam_m.values[None, :] / 2
    if size_rule:
        f &= size_fits(sidewalk_class(pos, site), pal.species, size_rule)
    f[~f.any(1), pal.crown_diam_m.values.argmin()] = True     # nothing fits (incl. sidewalks < 2.5 m): smallest crown
    return f


def planting_spots():
    """Free street-tree spots (additions, scenarios A and R+A; scripts/porta_planting_spots.py), with their size class,
    minus those too close to crossings, signals, parking entrances or bus stops (scripts/porta_spot_exclusions.py)."""
    s = pd.read_csv(DB / "porta_planting_spots.csv").rename(columns={"spot_id": "tree_id"})
    return s[s.get("excluded_by", pd.Series("", index=s.index)).fillna("") == ""].drop(columns="excluded_by", errors="ignore")


def add_cap(cap, n_total, n_add):
    """Cap per species when n_add trees are added: the 15% share is recomputed on the larger stock (Porta-local, ASSUMPTION)."""
    return cap + int(np.floor(MAX_SHARE * (n_total + n_add)) - np.floor(MAX_SHARE * n_total))


def city_cap(n_species, n_total, planes_here, planes_city):
    """City-wide 15% cap (tree master plan; street trees only, notes/citywide_plan.md §6.5) for a joint layout of some
    barris: headroom = floor(15% of the city's street trees) − the species' trees today, then the pro-rata part of it
    for the planes replaced here (ASSUMPTION: so that the barris run first do not use up the headroom of the others)."""
    head = (np.floor(MAX_SHARE * n_total) - np.asarray(n_species)).clip(0)
    return np.floor(head * planes_here / planes_city).astype(int)


def in_area(pos, path):
    """Positions inside the project area the user draws (notes/topic_decision.md §10.6): any polygon file GeoPandas
    reads (GeoJSON, shapefile, GeoPackage), in its own CRS; EPSG:25831 if it has none (GeoJSON without one is WGS84).
    Trees outside stay as they are today."""
    import geopandas as gpd
    a = gpd.read_file(path)
    a = a.set_crs(25831) if a.crs is None else a.to_crs(25831)
    return gpd.GeoSeries(gpd.points_from_xy(pos.x, pos.y), crs=25831).within(a.union_all()).values


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


def _entropy_chords(n_pos):
    """Chords of g(n) = −(n/N)·ln(n/N) on breakpoints dense near 0. g is concave, so its piecewise-linear interpolation
    (the min of the chord lines) lies below it: a floor on the sum of chords is a conservative floor on Shannon H."""
    n = np.unique(np.r_[0, np.round(np.geomspace(1, n_pos, 40))])
    p = n / n_pos
    g = -p * np.log(np.where(p > 0, p, 1))
    b = np.diff(g) / np.diff(n)
    return g[:-1] - b * n[:-1], b                     # line k: a_k + b_k·n


def assign(score, cap, fit, min_eff=None):
    """Max total score, one fitting species per position, species counts <= cap (transportation LP, integral at a vertex).
    min_eff: optional diversity floor (methodology §6) on the planted positions as an effective number of species,
    exp(Shannon H) as in SylvCiT (Nicol et al. 2026). Linear in the counts via _entropy_chords; only the S counts are
    integer, the x-part stays a transportation problem."""
    P, S = score.shape
    A_eq = sparse.kron(sparse.eye(P), np.ones((1, S)))
    A_ub = sparse.kron(np.ones((1, P)), sparse.eye(S))
    if min_eff is None:
        res = linprog(-score.ravel(), A_ub=A_ub, b_ub=cap, A_eq=A_eq, b_eq=np.ones(P),
                      bounds=np.c_[np.zeros(P * S), fit.ravel()], method="highs")
    else:                                             # variables: x (P·S), n (S counts), h (S entropy terms)
        a, b = _entropy_chords(P)
        K, I, Z = len(a), sparse.eye(S), sparse.csr_matrix
        A_eq = sparse.vstack([sparse.hstack([A_eq, Z((P, 2 * S))]), sparse.hstack([A_ub, -I, Z((S, S))])])
        A_ub = sparse.vstack([sparse.hstack([Z((K * S, P * S)), -sparse.kron(b[:, None], I), sparse.kron(np.ones((K, 1)), I)]),
                              sparse.hstack([Z((1, P * S + S)), -np.ones((1, S))])])
        res = linprog(np.r_[-score.ravel(), np.zeros(2 * S)], A_ub=A_ub, b_ub=np.r_[np.repeat(a, S), -np.log(min_eff)],
                      A_eq=A_eq, b_eq=np.r_[np.ones(P), np.zeros(S)], method="highs",
                      bounds=np.r_[np.c_[np.zeros(P * S), fit.ravel()], np.c_[np.zeros(S), cap], np.c_[np.zeros(S), np.full(S, np.inf)]],
                      integrality=np.r_[np.zeros(P * S), np.ones(S), np.zeros(S)])
    if not res.success:
        raise RuntimeError(res.message if min_eff is None else f"diversity floor {min_eff} not reachable: {res.message}")
    return res.x[:P * S].reshape(P, S).argmax(1)


def eff_species(choice, n_species):
    """Effective number of species exp(Shannon H) of a layout (palette indices)."""
    p = np.bincount(choice, minlength=n_species) / len(choice)
    p = p[p > 0]
    return float(np.exp(-(p * np.log(p)).sum()))


def sweep(objs, cap, fit, step=0.25, min_eff=None):
    """objs: {name: (potential matrix, +1 to maximise / −1 to minimise)}. Every weight combination on a simplex grid
    (step 0.25 -> 15 combinations for 3 objectives); potentials normalised by their maximum. A 1e-3 share of the
    unweighted sum breaks ties (e.g. positions that do not drain to a hotspot)."""
    n = int(round(1 / step))
    norm = [sign * m / m.max() for m, sign in objs.values()]
    out = {}
    for c in itertools.product(range(n + 1), repeat=len(objs)):
        if sum(c) == n:
            w = np.array(c) / n
            out[tuple(w)] = assign(sum(wk * m for wk, m in zip(w, norm)) + 1e-3 * sum(norm), cap, fit, min_eff)
    return out


def random_layout(cap, fit, rng):
    """Baseline: each position gets a random fitting palette species that still has room under its cap."""
    left, out = cap.copy(), np.empty(len(fit), int)
    for i in np.argsort(fit.sum(1), kind="stable"):     # most constrained positions first, so the cap rarely blocks a fit
        ok = np.flatnonzero((left > 0) & fit[i])
        j = rng.choice(ok if len(ok) else np.flatnonzero(left > 0))   # last resort: any species with room (raises if none)
        left[j] -= 1
        out[i] = j
    return out


def s1a_layout(pal, cap, fit, rng):
    """S1a: each position draws a fitting S1A_MIX species with probability proportional to its weight, under the cap.
    Positions are drawn most constrained first. Where no mix species fits or has room: any fitting palette species with
    room, else (last resort) any species with room."""
    w = pal.species.map(S1A_MIX).fillna(0).values
    left, out = cap.copy(), np.empty(len(fit), int)
    for i in np.argsort((fit * (w > 0)).sum(1), kind="stable"):   # positions with fewest fitting mix species first
        ok = (left > 0) & fit[i]
        p = w * ok
        alt = np.flatnonzero(ok) if ok.any() else np.flatnonzero(left > 0)  # as random_layout
        j = rng.choice(len(w), p=p / p.sum()) if p.sum() > 0 else rng.choice(alt)
        left[j] -= 1
        out[i] = j
    return out


# Family of every genus in Porta's inventory (standard taxonomy, APG IV; "X" = ×Chitalpa). For the 10-20-30 check of
# Santamour 1990 (#139): genus and family shares are reported, not constrained (Barcelona caps species only).
FAMILY = {"Platanus": "Platanaceae", "Celtis": "Cannabaceae", "Melia": "Meliaceae", "Pyrus": "Rosaceae",
          "Jacaranda": "Bignoniaceae", "Tipuana": "Fabaceae", "Brachychiton": "Malvaceae", "Populus": "Salicaceae",
          "Citrus": "Rutaceae", "Robinia": "Fabaceae", "Catalpa": "Bignoniaceae", "Grevillea": "Proteaceae",
          "Casuarina": "Casuarinaceae", "Gleditsia": "Fabaceae", "Fraxinus": "Oleaceae", "Handroanthus": "Bignoniaceae",
          "Tilia": "Malvaceae", "Ligustrum": "Oleaceae", "Morus": "Moraceae", "Prunus": "Rosaceae", "Acer": "Sapindaceae",
          "X": "Bignoniaceae", "Hibiscus": "Malvaceae", "Eugenia": "Myrtaceae", "Koelreuteria": "Sapindaceae",
          "Hesperocyparis": "Cupressaceae", "Eucalyptus": "Myrtaceae", "Cercis": "Fabaceae", "Ulmus": "Ulmaceae",
          "Styphnolobium": "Fabaceae", "Crataegus": "Rosaceae", "Cupressus": "Cupressaceae", "Photinia": "Rosaceae",
          "Pinus": "Pinaceae", "Phoenix": "Arecaceae", "Liquidambar": "Altingiaceae", "Magnolia": "Magnoliaceae",
          "Eriobotrya": "Rosaceae"}


def taxon_shares(trees):
    """Largest genus and family share (%) of a tree set; genera missing from FAMILY count as their own family."""
    g = trees.species.str.split().str[0]
    f = g.map(FAMILY).fillna(g)
    gs, fs = g.value_counts(normalize=True), f.value_counts(normalize=True)
    return dict(max_genus_pct=100 * gs.iloc[0], max_genus=gs.index[0], max_family_pct=100 * fs.iloc[0], max_family=fs.index[0])


def canopy_cover(site, trees):
    """Share of the site under canopy: street-tree crown discs (no overlap double-counting) + fixed park/private canopy."""
    from rasterio.features import rasterize
    from shapely.geometry import Point
    street = rasterize(((Point(x, y).buffer(d / 2), 1) for x, y, d in zip(trees.x, trees.y, trees.crown_diam_m)),
                       out_shape=site.domain.shape, transform=site.transform, fill=0).astype(bool)
    return float(((street | site.background) & site.domain).sum() / site.domain.sum())


def apply(site, pos, pal, choice):
    """Full street-tree set: kept trees (LiDAR crowns) + the chosen species at the plane positions."""
    t = site.trees
    kept = t[~t.tree_id.isin(pos.tree_id) & (t.flag == "ok")]       # non-planes, plus planes kept out of the decision
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
    return dict(**shade, **season.runoff_seasonal(site, trees, p_mm), **leafon, canopy_pct=100 * canopy_cover(site, trees), **taxon_shares(trees))


def pareto(df, maximise=("shade_summer_m2h",), minimise=("shade_winter_m2h", "runoff_hot_m3")):
    """Rows not dominated by any other row."""
    v = np.c_[df[list(maximise)].values, -df[list(minimise)].values]
    return np.array([not np.any(np.all(v >= v[i], 1) & np.any(v > v[i], 1)) for i in range(len(v))])
