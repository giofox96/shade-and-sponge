"""LiDAR extraction for Porta: terrain, canopy height, per-tree metrics and building heights.

Input: ICGC Territorial LiDAR v3.1 tiles (flown 26 Sept 2021, leaf-on), databases/barcelona/raw/lidar/lidar_<ID1K>.laz
       (download: https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/full10km4358/lidar-territorial-v3r1-full1km<ID1K>-2021-2023.laz)
Classes used: ground 2, 8, 75 | vegetation 3, 4, 5 | building 6 (class 12 = overlap strips, unlabelled: used only in gap fraction).
Outputs:
  databases/barcelona/raw/lidar/porta_{dtm,chm,bldg}_05m.tif
  exchange/to_gh/porta_trees_lidar.csv      per inventory tree: height, crown, crown base, gap fraction, LAI proxy
  exchange/to_gh/porta_buildings.geojson    OSM footprints (ODbL) with LiDAR height, local coordinates
  databases/barcelona/porta_species_lidar_summary.csv
  notes/figures/porta_lidar_qa.png
Run with the project env (see CLAUDE.md). Uses ~4 GB RAM.
"""
import json, pathlib, numpy as np, pandas as pd, geopandas as gpd, laspy, rasterio
import matplotlib.pyplot as plt, osmnx as ox
from rasterio.transform import from_origin
from rasterio.features import rasterize
from scipy import ndimage
from skimage.segmentation import watershed

ROOT = pathlib.Path(__file__).resolve().parents[1]
LID = ROOT / "databases/barcelona/raw/lidar"
TILES = ["430586", "430587", "431586", "431587"]
RES, BUF, K = 0.5, 30.0, 0.5            # cell size (m), buffer (m), Beer-Lambert extinction coefficient (assumed)
GROUND, VEG, BLDG = (2, 8, 75), (3, 4, 5), (6,)
origin = json.load(open(ROOT / "exchange/site_origin.json"))
OX, OY = origin["origin_x"], origin["origin_y"]

b = pd.read_csv(ROOT / "databases/barcelona/raw/BarcelonaCiutat_Barris.csv")
site = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
site = site[site.nom_barri == "Porta"]
x0, y0, x1, y1 = site.total_bounds + np.array([-BUF, -BUF, BUF, BUF])
W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
T = from_origin(x0, y1, RES, RES)

# ---- 1. crop point cloud (cached)
cache = LID / "porta_points.npz"
if not cache.exists():
    parts = []
    for t in TILES:
        with laspy.open(LID / f"lidar_{t}.laz") as f:
            for p in f.chunk_iterator(5_000_000):
                x, y = np.asarray(p.x), np.asarray(p.y)
                m = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
                if m.any():
                    parts.append(np.c_[x[m], y[m], np.asarray(p.z)[m], np.asarray(p.classification)[m],
                                       np.asarray(p.return_number)[m], np.asarray(p.number_of_returns)[m]])
    a = np.vstack(parts)
    np.savez_compressed(cache, x=a[:, 0], y=a[:, 1], z=a[:, 2].astype("float32"), c=a[:, 3].astype("uint8"),
                        rn=a[:, 4].astype("uint8"), nr=a[:, 5].astype("uint8"))
d = np.load(cache)
x, y, z, c, rn = d["x"], d["y"], d["z"], d["c"], d["rn"]
col = ((x - x0) / RES).astype(int).clip(0, W - 1)
row = ((y1 - y) / RES).astype(int).clip(0, H - 1)
idx = row * W + col
cls_share = pd.Series(c).value_counts(normalize=True).round(3)
print(f"{len(x):,} points in Porta+{BUF:.0f} m; class shares:", cls_share.head(10).to_dict())


def grid(mask, how):
    out = np.full(W * H, np.nan, "float32")
    i, v = idx[mask], z[mask]
    if how == "min":
        np.fmin.at(out, i, v)
    else:
        np.fmax.at(out, i, v)
    return out.reshape(H, W)


# ---- 2. DTM (min of ground points, gaps filled with nearest), CHM, building heights
g = grid(np.isin(c, GROUND), "min")
filled = ~np.isnan(g)
print(f"DTM: {filled.mean():.0%} of 0.5 m cells have ground points before filling")
nearest = ndimage.distance_transform_edt(~filled, return_distances=False, return_indices=True)
dtm = g[tuple(nearest)]
dtm = ndimage.median_filter(dtm, size=5)
chm = np.nan_to_num(grid(np.isin(c, VEG), "max") - dtm, nan=0).clip(0, 45)
bldg = grid(np.isin(c, BLDG), "max") - dtm
for name, arr in (("dtm", dtm), ("chm", chm), ("bldg", bldg)):
    with rasterio.open(LID / f"porta_{name}_05m.tif", "w", driver="GTiff", width=W, height=H, count=1,
                       dtype="float32", crs="EPSG:25831", transform=T, nodata=np.nan, compress="deflate") as dst:
        dst.write(arr.astype("float32"), 1)

# ---- 3. trees: seed watershed at inventory positions on the CHM
t = pd.read_csv(ROOT / "databases/barcelona/arbrat_viari.csv")
t = t[(t.tipus_element == "ARBRE VIARI") & (t.nom_barri.str.lower() == "porta")].reset_index(drop=True)
tc = ((t.x_etrs89 - x0) / RES).astype(int).values
tr = ((y1 - t.y_etrs89) / RES).astype(int).values
canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
markers = np.zeros((H, W), "int32")
markers[tr, tc] = np.arange(1, len(t) + 1)
markers = ndimage.grey_dilation(markers, size=(3, 3))                 # 1.5 m seed so a seed lands on canopy
crowns = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
# a crown may not extend more than 9 m from its seed (street trees; stops seeds flooding whole canopy patches)
rr, cc = np.indices((H, W))
lab = crowns.ravel()
far = np.zeros(W * H, bool)
has = lab > 0
far[has] = np.hypot(rr.ravel()[has] - tr[lab[has] - 1], cc.ravel()[has] - tc[lab[has] - 1]) * RES > 9.0
crowns.ravel()[far] = 0
crowns[~canopy] = 0

ids = np.arange(1, len(t) + 1)
area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
hmax = ndimage.maximum(chm, crowns, ids)
hmax = np.where(area > 0, hmax, np.nan)
# per-crown point statistics: crown base (10th pct of vegetation heights > 1.5 m) and gap fraction
pid = crowns.ravel()[idx]
gz = dtm.ravel()[idx]
hag = z - gz
sel = pid > 0
P = pd.DataFrame({"id": pid[sel], "h": hag[sel], "veg": np.isin(c[sel], VEG), "gnd": np.isin(c[sel], GROUND),
                  "lab": c[sel] != 12})
vegp = P[P.veg & (P.h > 1.5)].groupby("id").h
base = vegp.quantile(0.10)
lab_pts = P[P.lab].groupby("id")
gap = (lab_pts.gnd.sum() / lab_pts.size()).reindex(ids)
npts = P.groupby("id").size().reindex(ids)
out = pd.DataFrame({
    "tree_id": t.codi, "x": (t.x_etrs89 - OX).round(2), "y": (t.y_etrs89 - OY).round(2),
    "ground_z": dtm[tr, tc].round(2), "species": t.cat_nom_cientific, "is_plane": t.cat_nom_cientific.str.startswith("Platanus"),
    "size_category": t.categoria_arbrat, "street": t.adreca.str.replace(r",.*", "", regex=True),
    "height_m": np.round(hmax, 2), "crown_area_m2": np.round(area, 1),
    "crown_diam_m": np.round(2 * np.sqrt(area / np.pi), 2),
    "crown_base_m": base.reindex(ids).round(2).values,
    "gap_fraction": gap.round(3).values,
    "lai_proxy": (-np.log(gap.clip(0.02, 1)) / K).round(2).values,
    "n_points": npts.fillna(0).astype(int).values})
out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                        ["no_crown_detected", "few_points", "low_tree"], "ok")
out.to_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv", index=False)
ok = out[out.flag == "ok"]
print(f"trees: {len(out)}, ok {len(ok)} ({len(ok) / len(out):.0%}); flags:", out.flag.value_counts().to_dict())
sp = out.assign(species=out.species.str.replace(r"\s*'.*", "", regex=True))[out.flag == "ok"].groupby("species").agg(
    n=("tree_id", "size"), height_med=("height_m", "median"), crown_diam_med=("crown_diam_m", "median"),
    crown_base_med=("crown_base_m", "median"), gap_med=("gap_fraction", "median"), lai_proxy_med=("lai_proxy", "median"),
    lai_proxy_iqr=("lai_proxy", lambda s: s.quantile(0.75) - s.quantile(0.25))).sort_values("n", ascending=False).round(2)
sp.to_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv")
print(sp.head(12).to_string())

# ---- 4. buildings: OSM footprints + LiDAR height (median of roof heights inside footprint)
bld = ox.features_from_polygon(site.to_crs(4326).buffer(0.0003).iloc[0], tags={"building": True})
bld = bld[bld.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(25831).reset_index()[["geometry"]]
lab_b = rasterize(((geom, i + 1) for i, geom in enumerate(bld.geometry)), out_shape=(H, W), transform=T, fill=0, dtype="int32")
bi = np.arange(1, len(bld) + 1)
bh = ndimage.median(np.nan_to_num(bldg, nan=0), lab_b, bi)
cover = ndimage.mean(~np.isnan(bldg), lab_b, bi)
bld["height_m"] = np.round(bh, 2)
bld["lidar_cover"] = np.round(cover, 2)
bld["ground_z"] = np.round(ndimage.median(dtm, lab_b, bi), 2)
bld = bld[(bld.height_m > 2.5) & (bld.lidar_cover > 0.3)]
loc = bld.copy()
loc["geometry"] = loc.translate(-OX, -OY)
loc.set_crs(None, allow_override=True).to_file(ROOT / "exchange/to_gh/porta_buildings.geojson", driver="GeoJSON")
print(f"buildings: {len(bld)} OSM footprints with LiDAR height; median {bld.height_m.median():.1f} m, p90 {bld.height_m.quantile(.9):.1f} m")

# ---- 5. QA figure
fig, ax = plt.subplots(1, 2, figsize=(16, 8))
im = ax[0].imshow(chm, cmap="Greens", vmin=0, vmax=25, extent=(x0, x0 + W * RES, y1 - H * RES, y1))
plt.colorbar(im, ax=ax[0], shrink=0.7, label="Canopy height (m)")
ax[0].scatter(t.x_etrs89, t.y_etrs89, s=1, c="red")
site.boundary.plot(ax=ax[0], color="black")
ax[0].set_title("Canopy height model (LiDAR 26 Sept 2021) + inventory trees (red)")
ax[0].set_axis_off()
top = sp.head(8).index
data = [ok[ok.species.str.replace(r"\s*'.*", "", regex=True) == s].height_m.dropna() for s in top]
ax[1].boxplot(data, orientation="horizontal", tick_labels=[f"{s} (n={len(d)})" for s, d in zip(top, data)])
ax[1].set_xlabel("LiDAR tree height (m)")
ax[1].set_title("Height by species, Porta (top 8)")
fig.savefig(ROOT / "notes/figures/porta_lidar_qa.png", dpi=130, bbox_inches="tight")
