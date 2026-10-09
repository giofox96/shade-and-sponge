"""LiDAR crowns of candidate species outside Porta: same method as scripts/bcn_lidar_porta.py (0.5 m DTM/CHM,
watershed seeded at every inventory street tree, crowns <= 9 m from their seed, crown base = 10th percentile of
vegetation heights > 1.5 m, gap fraction -> LAI proxy), run on whole 1 km tiles read in chunks.
Inputs: databases/barcelona/lidar_tiles_species.csv (scripts/species_shortlist.py), raw/lidar/lidar_<ID1K>.laz (ICGC,
CC BY 4.0; download URL pattern in bcn_lidar_porta.py with the tile's ID10K folder), arbrat_viari.csv
Outputs: databases/barcelona/lidar_species_trees.csv (per tree), species_lidar_summary.csv (Porta + tiles, per species),
         lidar_tiles_dates.csv (flight dates per tile, from GPS time: leaf-on check)"""
import datetime, pathlib, numpy as np, pandas as pd, laspy
from scipy import ndimage
from skimage.segmentation import watershed
from species_shortlist import norm, EDGE

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, LID = ROOT / "databases/barcelona", ROOT / "databases/barcelona/raw/lidar"
RES, K = 0.5, 0.5                                     # as bcn_lidar_porta.py
GROUND, VEG, BLDG = (2, 8, 75), (3, 4, 5), (6,)
N = int(1000 / RES)
GPS0 = datetime.datetime(1980, 1, 6)

inv = pd.read_csv(DB / "arbrat_viari.csv", usecols=["codi", "x_etrs89", "y_etrs89", "cat_nom_cientific", "tipus_element"])
inv = inv[(inv.tipus_element == "ARBRE VIARI") & inv.cat_nom_cientific.notna()]
rows, dates = [], []
for tile in pd.read_csv(DB / "lidar_tiles_species.csv").tile.astype(str):
    x0, y0 = int(tile[:3]) * 1000, (4000 + int(tile[3:])) * 1000
    y1 = y0 + 1000
    lo, hi = np.full(N * N, np.nan, "float32"), np.full(N * N, np.nan, "float32")
    gmin, gmax = np.inf, -np.inf

    def chunks():
        with laspy.open(LID / f"lidar_{tile}.laz") as f:
            adjusted = bool(f.header.global_encoding.gps_time_type)
            for p in f.chunk_iterator(5_000_000):
                x, y = np.asarray(p.x), np.asarray(p.y)
                m = (x >= x0) & (x < x0 + 1000) & (y >= y0) & (y < y1)
                yield p, m, adjusted, ((y1 - y[m]) / RES).astype(int).clip(0, N - 1) * N + ((x[m] - x0) / RES).astype(int).clip(0, N - 1)

    # pass 1: ground minimum, vegetation maximum, flight dates
    for p, m, adjusted, idx in chunks():
        z, c = np.asarray(p.z)[m], np.asarray(p.classification)[m]
        g, v = np.isin(c, GROUND), np.isin(c, VEG)
        np.fmin.at(lo, idx[g], z[g])
        np.fmax.at(hi, idx[v], z[v])
        t = np.asarray(p.gps_time)[m]
        if t.size:
            gmin, gmax = min(gmin, t.min()), max(gmax, t.max())
    off = 1e9 if adjusted else 0                         # LAS 1.4 adjusted standard GPS time
    d0, d1 = (GPS0 + datetime.timedelta(seconds=float(v + off)) for v in (gmin, gmax))
    dates.append(dict(tile=tile, first=d0.date(), last=d1.date()))
    lo = lo.reshape(N, N)
    dtm = ndimage.median_filter(lo[tuple(ndimage.distance_transform_edt(np.isnan(lo), return_distances=False,
                                                                           return_indices=True))], size=5)
    chm = np.nan_to_num(hi.reshape(N, N) - dtm, nan=0).clip(0, 45)

    # crowns seeded at every street tree in the tile
    t = inv[(inv.x_etrs89 >= x0) & (inv.x_etrs89 < x0 + 1000) & (inv.y_etrs89 >= y0) & (inv.y_etrs89 < y1)].reset_index(drop=True)
    tc = ((t.x_etrs89 - x0) / RES).astype(int).clip(0, N - 1).values
    tr = ((y1 - t.y_etrs89) / RES).astype(int).clip(0, N - 1).values
    canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
    markers = np.zeros((N, N), "int32")
    markers[tr, tc] = np.arange(1, len(t) + 1)
    markers = ndimage.grey_dilation(markers, size=(3, 3))
    crowns = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
    rr, cc = np.indices((N, N))
    lab = crowns.ravel()
    has = lab > 0
    far = np.zeros(N * N, bool)
    far[has] = np.hypot(rr.ravel()[has] - tr[lab[has] - 1], cc.ravel()[has] - tc[lab[has] - 1]) * RES > 9.0
    crowns.ravel()[far] = 0
    crowns[~canopy] = 0
    ids = np.arange(1, len(t) + 1)
    area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
    hmax = np.where(area > 0, ndimage.maximum(chm, crowns, ids), np.nan)

    # pass 2: per-crown point statistics
    parts = []
    for p, m, _, idx in chunks():
        pid = crowns.ravel()[idx]
        s = pid > 0
        if s.any():
            c = np.asarray(p.classification)[m][s]
            parts.append(pd.DataFrame({"id": pid[s], "h": np.asarray(p.z)[m][s] - dtm.ravel()[idx[s]],
                                       "veg": np.isin(c, VEG), "gnd": np.isin(c, GROUND), "lab": c != 12}))
    P = pd.concat(parts)
    base = P[P.veg & (P.h > 1.5)].groupby("id").h.quantile(0.10).reindex(ids)
    L = P[P.lab].groupby("id")
    gap = (L.gnd.sum() / L.size()).reindex(ids)
    npts = P.groupby("id").size().reindex(ids).fillna(0).astype(int)
    ex, ey = t.x_etrs89 - x0, t.y_etrs89 - y0
    out = pd.DataFrame({"tree_id": t.codi, "species": t.cat_nom_cientific.map(norm), "tile": tile,
                        "height_m": np.round(hmax, 2), "crown_area_m2": np.round(area, 1),
                        "crown_diam_m": np.round(2 * np.sqrt(area / np.pi), 2), "crown_base_m": base.round(2).values,
                        "gap_fraction": gap.round(3).values, "lai_proxy": (-np.log(gap.clip(0.02, 1)) / K).round(2).values,
                        "n_points": npts.values,
                        "inner": ((ex > EDGE) & (ex < 1000 - EDGE) & (ey > EDGE) & (ey < 1000 - EDGE)).values})
    out["flag"] = np.select([~out.inner, out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                            ["tile_edge", "no_crown_detected", "few_points", "low_tree"], "ok")
    rows.append(out)
    print(tile, f"{d0:%Y-%m-%d}–{d1:%Y-%m-%d}", len(out), "trees,", (out.flag == "ok").mean().round(2), "ok", flush=True)

trees = pd.concat(rows, ignore_index=True)
trees.to_csv(DB / "lidar_species_trees.csv", index=False)
pd.DataFrame(dates).to_csv(DB / "lidar_tiles_dates.csv", index=False)

# per-species summary: Porta trees (bcn_lidar_porta.py) + tile trees not already measured in Porta
porta = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv").assign(species=lambda d: d.species.map(norm), src="porta")
tiles = trees[~trees.tree_id.isin(porta.tree_id)].assign(src="tiles")
allt = pd.concat([porta, tiles], ignore_index=True)
ok = allt[allt.flag == "ok"]
g = ok.groupby("species")
summary = pd.DataFrame({
    "n": g.size(), "n_porta": g.src.apply(lambda s: (s == "porta").sum()), "n_tiles": g.src.apply(lambda s: (s == "tiles").sum()),
    "height_med": g.height_m.median(), "crown_diam_med": g.crown_diam_m.median(), "crown_base_med": g.crown_base_m.median(),
    "gap_med": g.gap_fraction.median(), "lai_proxy_med": g.lai_proxy.median(),
    "lai_proxy_iqr": g.lai_proxy.quantile(0.75) - g.lai_proxy.quantile(0.25)}).round(2).sort_values("n", ascending=False)
summary.to_csv(DB / "species_lidar_summary.csv")
sl = pd.read_csv(DB / "species_shortlist.csv").set_index("species")
print(summary.reindex(sl.index[sl.status == "candidate"]).to_string())
