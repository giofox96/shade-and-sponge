"""LiDAR extraction for any barri: the inputs of shade_sponge.site.build_barri() (notes/citywide_plan.md §6.2 step 2).
Same method as scripts/bcn_lidar_porta.py (0.5 m DTM/CHM/building rasters, watershed crowns seeded at the inventory
street trees, crown <= 9 m from its seed, crown base = 10th percentile of vegetation heights > 1.5 m, gap fraction ->
LAI proxy), on the barri bounds + BUFFER_M instead of Porta + 30 m. Porta keeps its own script (regression baseline).

Usage (project env, on the PC: ICGC and Open Data BCN block the cloud):  python scripts/bcn_lidar_barri.py "Sant Antoni"
Inputs: databases/barcelona/lidar_tiles_barris.csv (scripts/lidar_tiles_barris.py), raw/lidar/lidar_<ID1K>.laz
        (downloaded here if missing, ICGC Territorial LiDAR v3.1, CC BY 4.0), arbrat_viari.csv, raw/BarcelonaCiutat_Barris.csv
Outputs: raw/lidar/<slug>_{dtm,chm,bldg}_05m.tif
         databases/barcelona/barris/<slug>/trees_lidar.csv     per inventory street tree, EPSG:25831
         databases/barcelona/barris/<slug>/buildings.geojson   OSM footprints (ODbL) with LiDAR height, EPSG:25831
         databases/barcelona/lidar_tiles_dates.csv             flight dates of the tiles read (leaf-on check), appended
Memory: the points of the whole extent are held at once (x, y, z, class); 8 tiles for Sant Antoni (0.8 km²)."""
import sys, datetime, pathlib, numpy as np, pandas as pd, laspy, rasterio, requests, osmnx as ox
from rasterio.transform import from_origin
from rasterio.features import rasterize
from scipy import ndimage
from skimage.segmentation import watershed

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import BUFFER_M, barri, slug  # noqa: E402

DB, LID = ROOT / "databases/barcelona", ROOT / "databases/barcelona/raw/lidar"
URL = "https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/full10km{k}/lidar-territorial-v3r1-full1km{t}-2021-2023.laz"
RES, K = 0.5, 0.5                                     # as bcn_lidar_porta.py
GROUND, VEG, BLDG = (2, 8, 75), (3, 4, 5), (6,)
GPS0 = datetime.datetime(1980, 1, 6)

site = barri(sys.argv[1])
name = site.nom_barri.iloc[0]
s = slug(name)
out_dir = DB / "barris" / s
out_dir.mkdir(parents=True, exist_ok=True)
x0, y0, x1, y1 = site.total_bounds + np.array([-BUFFER_M, -BUFFER_M, BUFFER_M, BUFFER_M])   # = build_barri() grid
W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
T = from_origin(x0, y1, RES, RES)

# ---- 1. tiles (download if missing) and points in the extent
tiles = pd.read_csv(DB / "lidar_tiles_barris.csv", dtype={"tile": str}).query("slug == @s").tile.tolist()
LID.mkdir(parents=True, exist_ok=True)
for t in tiles:
    f = LID / f"lidar_{t}.laz"
    if not f.exists():
        print("downloading", f.name)
        with requests.get(URL.format(k=t[:2] + t[3:5], t=t), stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(f.with_suffix(".part"), "wb") as o:
                for chunk in r.iter_content(1 << 22):
                    o.write(chunk)
        f.with_suffix(".part").rename(f)
parts, dates = [], []
for t in tiles:
    gmin, gmax = np.inf, -np.inf
    with laspy.open(LID / f"lidar_{t}.laz") as f:
        adjusted = bool(f.header.global_encoding.gps_time_type)
        for p in f.chunk_iterator(5_000_000):
            x, y = np.asarray(p.x), np.asarray(p.y)
            m = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
            if m.any():
                parts.append((x[m], y[m], np.asarray(p.z)[m].astype("float32"), np.asarray(p.classification)[m]))
                g = np.asarray(p.gps_time)[m]
                gmin, gmax = min(gmin, g.min()), max(gmax, g.max())
    if np.isfinite(gmin):
        off = 1e9 if adjusted else 0                     # LAS 1.4 adjusted standard GPS time
        dates.append(dict(tile=t, first=(GPS0 + datetime.timedelta(seconds=float(gmin + off))).date(),
                          last=(GPS0 + datetime.timedelta(seconds=float(gmax + off))).date()))
x, y, z, c = (np.concatenate(a) for a in zip(*parts))
del parts
d = pd.DataFrame(dates)
d["leaf_off_check"] = pd.to_datetime(d["first"]).dt.month.isin([12, 1, 2, 3]) | pd.to_datetime(d["last"]).dt.month.isin([12, 1, 2, 3])
print(f"{len(x):,} points in {name} + {BUFFER_M:.0f} m from {len(tiles)} tiles; flight dates:\n{d.to_string(index=False)}")
if d.leaf_off_check.any():
    print("WARNING: some tiles were flown Dec–Mar (crowns of deciduous trees may be leafless): check before using the crowns")
old = pd.read_csv(DB / "lidar_tiles_dates.csv", dtype={"tile": str})
pd.concat([old, d.drop(columns="leaf_off_check").astype({"first": str, "last": str})]).drop_duplicates("tile", keep="last") \
    .to_csv(DB / "lidar_tiles_dates.csv", index=False)

col = ((x - x0) / RES).astype(int).clip(0, W - 1)
row = ((y1 - y) / RES).astype(int).clip(0, H - 1)
idx = row * W + col
del col, row


def grid(mask, how):
    out = np.full(W * H, np.nan, "float32")
    (np.fmin if how == "min" else np.fmax).at(out, idx[mask], z[mask])
    return out.reshape(H, W)


# ---- 2. DTM (min of ground points, gaps filled with nearest), CHM, building heights
g = grid(np.isin(c, GROUND), "min")
dtm = ndimage.median_filter(g[tuple(ndimage.distance_transform_edt(np.isnan(g), return_distances=False,
                                                                    return_indices=True))], size=5)
chm = np.nan_to_num(grid(np.isin(c, VEG), "max") - dtm, nan=0).clip(0, 45)
bldg = grid(np.isin(c, BLDG), "max") - dtm
for k, arr in (("dtm", dtm), ("chm", chm), ("bldg", bldg)):
    with rasterio.open(LID / f"{s}_{k}_05m.tif", "w", driver="GTiff", width=W, height=H, count=1, dtype="float32",
                       crs="EPSG:25831", transform=T, nodata=np.nan, compress="deflate") as dst:
        dst.write(arr.astype("float32"), 1)

# ---- 3. trees: seed watershed at inventory positions on the CHM
t = pd.read_csv(DB / "arbrat_viari.csv")
t = t[(t.tipus_element == "ARBRE VIARI") & (t.nom_barri.fillna("").map(slug) == s)].reset_index(drop=True)
tc = ((t.x_etrs89 - x0) / RES).astype(int).values
tr = ((y1 - t.y_etrs89) / RES).astype(int).values
canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
markers = np.zeros((H, W), "int32")
markers[tr, tc] = np.arange(1, len(t) + 1)
markers = ndimage.grey_dilation(markers, size=(3, 3))                 # 1.5 m seed so a seed lands on canopy
crowns = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
rr, cc = np.indices((H, W))
lab = crowns.ravel()
far = np.zeros(W * H, bool)
has = lab > 0
far[has] = np.hypot(rr.ravel()[has] - tr[lab[has] - 1], cc.ravel()[has] - tc[lab[has] - 1]) * RES > 9.0
crowns.ravel()[far] = 0
crowns[~canopy] = 0
ids = np.arange(1, len(t) + 1)
area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
hmax = np.where(area > 0, ndimage.maximum(chm, crowns, ids), np.nan)
pid = crowns.ravel()[idx]
sel = pid > 0
P = pd.DataFrame({"id": pid[sel], "h": (z - dtm.ravel()[idx])[sel], "veg": np.isin(c[sel], VEG),
                  "gnd": np.isin(c[sel], GROUND), "lab": c[sel] != 12})
base = P[P.veg & (P.h > 1.5)].groupby("id").h.quantile(0.10)
lab_pts = P[P.lab].groupby("id")
gap = (lab_pts.gnd.sum() / lab_pts.size()).reindex(ids)
npts = P.groupby("id").size().reindex(ids)
out = pd.DataFrame({
    "tree_id": t.codi, "x": t.x_etrs89.round(2), "y": t.y_etrs89.round(2), "ground_z": dtm[tr, tc].round(2),
    "species": t.cat_nom_cientific, "is_plane": t.cat_nom_cientific.str.startswith("Platanus"),
    "size_category": t.categoria_arbrat, "street": t.adreca.str.replace(r",.*", "", regex=True),
    "height_m": np.round(hmax, 2), "crown_area_m2": np.round(area, 1), "crown_diam_m": np.round(2 * np.sqrt(area / np.pi), 2),
    "crown_base_m": base.reindex(ids).round(2).values, "gap_fraction": gap.round(3).values,
    "lai_proxy": (-np.log(gap.clip(0.02, 1)) / K).round(2).values, "n_points": npts.fillna(0).astype(int).values})
out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                        ["no_crown_detected", "few_points", "low_tree"], "ok")
out.to_csv(out_dir / "trees_lidar.csv", index=False)
print(f"trees: {len(out)} ({out.is_plane.sum()} planes), ok {(out.flag == 'ok').mean():.0%}; flags:", out.flag.value_counts().to_dict())

# ---- 4. buildings: OSM footprints + LiDAR height (median of roof heights inside footprint)
bld = ox.features_from_polygon(site.buffer(BUFFER_M).to_crs(4326).iloc[0], tags={"building": True})
bld = bld[bld.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(25831).reset_index()[["geometry"]]
lab_b = rasterize(((geom, i + 1) for i, geom in enumerate(bld.geometry)), out_shape=(H, W), transform=T, fill=0, dtype="int32")
bi = np.arange(1, len(bld) + 1)
bld["height_m"] = np.round(ndimage.median(np.nan_to_num(bldg, nan=0), lab_b, bi), 2)
bld["lidar_cover"] = np.round(ndimage.mean(~np.isnan(bldg), lab_b, bi), 2)
bld["ground_z"] = np.round(ndimage.median(dtm, lab_b, bi), 2)
bld = bld[(bld.height_m > 2.5) & (bld.lidar_cover > 0.3)]
bld.to_file(out_dir / "buildings.geojson", driver="GeoJSON")
print(f"buildings: {len(bld)} OSM footprints with LiDAR height; median {bld.height_m.median():.1f} m")
