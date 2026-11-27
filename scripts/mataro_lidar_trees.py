"""Mataró transfer test: per-tree LiDAR crown, height, crown base and LAI proxy for the inventory trees around the six test
streets of scripts/mataro_transfer_test.py, plus a building-height raster. Replaces the Barcelona pool medians used there for
the existing trees (ASSUMPTION "crowns" in that script's docstring).

Method = scripts/bcn_lidar_barri.py, unchanged: ICGC Territorial LiDAR v3.1 (classified; CC BY 4.0), 0.5 m DTM (min of ground
points, gaps filled with nearest, 5-cell median), CHM from vegetation classes, canopy > 2 m opened once, watershed on the
smoothed CHM seeded at the inventory positions (1.5 m seeds), crown <= 9 m from its seed, then every crown cell to its nearest
seed (Voronoi split, ASSUMPTION user 23 Nov); height = CHM max within 1.5 m of the tree's point; crown base = 10th percentile of
vegetation heights > 1.5 m; LAI proxy = -ln(gap fraction) / 0.5; same flags.
What differs: the seeds are the Mataró inventory positions (T_C_ARBRAT, every "Arbre.png" row, street and park alike, so that
neighbouring crowns split correctly), and the extent is one box per test street = the transfer test's grid
(planes + R_DOM, + BUF), not a barri.

Run on the PC (ICGC is blocked from the cloud):
  python scripts/mataro_lidar_trees.py [path/to/mataro_t_c_arbrat.csv]
Inputs: the inventory CSV (restricted, databases/RESTRICTED_DATA.md); tiles downloaded to databases/mataro/raw/lidar/.
Outputs, all in databases/mataro/raw/ (gitignored: they carry the inventory's positions and species, no sublicensing):
  mataro_trees_lidar.csv          one row per inventory tree inside a street box (tree_id = the transfer test's "m<row>")
  lidar/<street_slug>_bldg_05m.tif  building height above ground (LiDAR class 6), read by the transfer test for Overture footprints
  lidar/tiles_dates.csv           flight dates of the tiles read (leaf-on check)
"""
import sys, datetime, pathlib, numpy as np, pandas as pd, laspy, rasterio, requests
from rasterio.transform import from_origin
from scipy import ndimage
from scipy.spatial import cKDTree
from shapely.geometry import MultiPoint
from skimage.segmentation import watershed

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import mataro_transfer_test as mt  # noqa: E402  (test streets, R_DOM, BUF, inventory loader)

RAW = ROOT / "databases/mataro/raw"
LID = RAW / "lidar"
URL = "https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/full10km{k}/lidar-territorial-v3r1-full1km{t}-2021-2023.laz"
RES, K = 0.5, 0.5                                     # as bcn_lidar_barri.py
GROUND, VEG, BLDG = (2, 8, 75), (3, 4, 5), (6,)
GPS0 = datetime.datetime(1980, 1, 6)


def tiles_for(x0, y0, x1, y1):
    """Tile id = x km (3 digits) + (y km - 4000) (3 digits) of the lower-left corner, as scripts/lidar_tiles_barris.py."""
    return [f"{i:03d}{j - 4000:03d}" for i in range(int(x0 // 1000), int(x1 // 1000) + 1)
            for j in range(int(y0 // 1000), int(y1 // 1000) + 1)]


def fetch(t):
    f = LID / f"lidar_{t}.laz"
    if not f.exists():
        print("downloading", f.name, flush=True)
        with requests.get(URL.format(k=t[:2] + t[3:5], t=t), stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(f.with_suffix(".part"), "wb") as o:
                for chunk in r.iter_content(1 << 22):
                    o.write(chunk)
        f.with_suffix(".part").rename(f)
    return f


def one_box(name, x0, y0, x1, y1, t, dates):
    """bcn_lidar_barri.py steps 1-3 on one box; t = inventory trees inside it (columns tree_id, x, y, especie, ...)."""
    W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
    T = from_origin(x0, y1, RES, RES)
    parts = []
    for tile in tiles_for(x0, y0, x1, y1):
        gmin, gmax = np.inf, -np.inf
        with laspy.open(fetch(tile)) as f:
            adjusted = bool(f.header.global_encoding.gps_time_type)
            for p in f.chunk_iterator(5_000_000):
                x, y = np.asarray(p.x), np.asarray(p.y)
                m = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
                if m.any():
                    cell = ((y1 - y[m]) / RES).astype("int32").clip(0, H - 1) * W + ((x[m] - x0) / RES).astype("int32").clip(0, W - 1)
                    parts.append((cell, np.asarray(p.z)[m].astype("float32"), np.asarray(p.classification)[m]))
                    g = np.asarray(p.gps_time)[m]
                    gmin, gmax = min(gmin, g.min()), max(gmax, g.max())
        if np.isfinite(gmin):
            off = 1e9 if adjusted else 0
            dates[tile] = ((GPS0 + datetime.timedelta(seconds=float(gmin + off))).date(),
                           (GPS0 + datetime.timedelta(seconds=float(gmax + off))).date())
    idx, z, c = (np.concatenate(a) for a in zip(*parts))
    del parts

    def grid(mask, how):
        out = np.full(W * H, np.nan, "float32")
        (np.fmin if how == "min" else np.fmax).at(out, idx[mask], z[mask])
        return out.reshape(H, W)

    g = grid(np.isin(c, GROUND), "min")
    dtm = ndimage.median_filter(g[tuple(ndimage.distance_transform_edt(np.isnan(g), return_distances=False,
                                                                        return_indices=True))], size=5)
    chm = np.nan_to_num(grid(np.isin(c, VEG), "max") - dtm, nan=0).clip(0, 45)
    bldg = grid(np.isin(c, BLDG), "max") - dtm
    with rasterio.open(LID / f"{name}_bldg_05m.tif", "w", driver="GTiff", width=W, height=H, count=1, dtype="float32",
                       crs="EPSG:25831", transform=T, nodata=np.nan, compress="deflate") as dst:
        dst.write(bldg.astype("float32"), 1)

    t = t.reset_index(drop=True)
    tc = ((t.x - x0) / RES).astype(int).clip(0, W - 1).values
    tr = ((y1 - t.y) / RES).astype(int).clip(0, H - 1).values
    canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
    markers = np.zeros((H, W), "int32")
    markers[tr, tc] = np.arange(1, len(t) + 1)
    markers = ndimage.grey_dilation(markers, size=(3, 3))
    crowns = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
    rr, cc = np.indices((H, W))
    lab = crowns.ravel()
    far = np.zeros(W * H, bool)
    has = lab > 0
    far[has] = np.hypot(rr.ravel()[has] - tr[lab[has] - 1], cc.ravel()[has] - tc[lab[has] - 1]) * RES > 9.0
    crowns.ravel()[far] = 0
    crowns[~canopy] = 0
    lab = crowns.ravel()
    has = np.flatnonzero(lab > 0)
    _, near = cKDTree(np.c_[tr, tc]).query(np.c_[rr.ravel()[has], cc.ravel()[has]])
    crowns.ravel()[has] = near + 1
    ids = np.arange(1, len(t) + 1)
    area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
    disk = np.hypot(*np.mgrid[-3:4, -3:4]) * RES <= 1.5
    hmax = np.where(area > 0, ndimage.maximum_filter(chm, footprint=disk)[tr, tc], np.nan)
    pid = crowns.ravel()[idx]
    sel = pid > 0
    P = pd.DataFrame({"id": pid[sel], "h": (z - dtm.ravel()[idx])[sel], "veg": np.isin(c[sel], VEG),
                      "gnd": np.isin(c[sel], GROUND), "lab": c[sel] != 12})
    base = P[P.veg & (P.h > 1.5)].groupby("id").h.quantile(0.10)
    lab_pts = P[P.lab].groupby("id")
    gap = (lab_pts.gnd.sum() / lab_pts.size()).reindex(ids)
    npts = P.groupby("id").size().reindex(ids)
    out = pd.DataFrame({
        "tree_id": t.tree_id, "box": name, "x": t.x.round(2), "y": t.y.round(2), "ground_z": dtm[tr, tc].round(2),
        "species": t.especie, "height_m": np.round(hmax, 2), "crown_area_m2": np.round(area, 1),
        "crown_diam_m": np.round(2 * np.sqrt(area / np.pi), 2), "crown_base_m": base.reindex(ids).round(2).values,
        "gap_fraction": gap.round(3).values, "lai_proxy": (-np.log(gap.clip(0.02, 1)) / K).round(2).values,
        "n_points": npts.fillna(0).astype(int).values})
    out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                            ["no_crown_detected", "few_points", "low_tree"], "ok")
    print(f"{name}: {len(z):,} points, {len(out)} trees, ok {(out.flag == 'ok').mean():.0%}", flush=True)
    return out


def main():
    LID.mkdir(parents=True, exist_ok=True)
    d = mt.load_trees()
    dates, rows = {}, []
    for street, barri in mt.STREETS:
        m = d[(d.ubicacio == street) & (d.barri == barri) & d.is_plane & d.street]
        x0, y0, x1, y1 = np.array(MultiPoint(m[["x", "y"]].values).buffer(mt.R_DOM).bounds) + [-mt.BUF, -mt.BUF, mt.BUF, mt.BUF]
        inside = d[d.x.between(x0, x1) & d.y.between(y0, y1)]       # = make_site()'s grid_trees
        rows.append(one_box(mt.street_slug(street), x0, y0, x1, y1, inside, dates))
    out = pd.concat(rows, ignore_index=True).drop_duplicates("tree_id")   # a tree in two boxes: first box kept
    out.to_csv(RAW / "mataro_trees_lidar.csv", index=False)
    dd = pd.DataFrame([dict(tile=k, first=a, last=b) for k, (a, b) in dates.items()])
    dd.to_csv(LID / "tiles_dates.csv", index=False)
    leaf_off = pd.to_datetime(dd["first"]).dt.month.isin([12, 1, 2, 3]) | pd.to_datetime(dd["last"]).dt.month.isin([12, 1, 2, 3])
    print("flight dates:\n" + dd.to_string(index=False))
    if leaf_off.any():
        print("WARNING: some tiles were flown Dec-Mar (deciduous crowns may be leafless): check before using the crowns")
    print(f"trees: {len(out)}, ok {(out.flag == 'ok').mean():.0%}; flags:", out.flag.value_counts().to_dict())


if __name__ == "__main__":
    main()
