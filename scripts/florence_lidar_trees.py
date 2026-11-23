"""Florence transfer check: per-tree LiDAR height, crown and LAI proxy for the Life Escapos census trees,
validated against the census height and crown width. Method copied from scripts/bcn_lidar_porta.py.

Data: Dati LiDAR 2023 forniti da [Comune di Firenze], derivati dal rilievo aereo effettuato sul territorio
comunale nel periodo maggio/giugno 2023.
  Raw cloud: databases/florence/raw/lidar_2023/*.las (EPSG:7791, ~20 pts/m2, RGB+NIR, NOT classified).
  Research use only, no redistribution: the cloud and every per-point / per-cell product stay in raw/ (gitignored).
  Census: Comune di Firenze, "Life Escapos - Alberature pubbliche", CC BY-NC 4.0 (databases/florence/raw/).

Changes from Porta, forced by the unclassified cloud (no ground or vegetation classes):
  - Ground: ASSUMPTION. 1 m grid of the lowest point, grey opening 21 m (removes trees and objects < 21 m wide),
    then a 5-cell median, as in Porta. The Comune's 2023 DTM was not used (not fetched).
  - Vegetation: points with NDVI = (nir-red)/(nir+red) > NDVI_MIN (ASSUMPTION, leaf-on May/June flight)
    replace classes 3-5. Without it the CHM would take building and vehicle heights.
  - Gap fraction: "ground" = points < 0.5 m above the DTM (ASSUMPTION) over all points in the crown
    (Porta: ground class over labelled points).
Unchanged: 0.5 m CHM, canopy > 2 m with one opening, 1.5 m seeds at census positions, watershed on the
smoothed CHM, 9 m crown limit, K = 0.5, flags. Outputs (per-tree values only):
  databases/florence/florence_tree_lidar.csv, databases/florence/florence_lidar_validation.csv,
  notes/figures/florence_lidar_validation.png
"""
import pathlib, numpy as np, pandas as pd, geopandas as gpd, laspy, matplotlib.pyplot as plt
from scipy import ndimage, stats
from skimage.segmentation import watershed

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/florence/raw"
RES, GRES, BUF, K = 0.5, 1.0, 30.0, 0.5
NDVI_MIN, GROUND_H, OPEN_M = 0.2, 0.5, 21    # ASSUMPTIONS, see docstring
MIN_SP = 20

t = gpd.read_file(RAW / "escapos_tree_census.shp")
assert t.crs.to_epsg() == 7791                      # same CRS as the cloud: no reprojection
x0, y0, x1, y1 = t.total_bounds + np.array([-BUF, -BUF, BUF, BUF])
W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
GW, GH = int(np.ceil((x1 - x0) / GRES)), int(np.ceil((y1 - y0) / GRES))
tx, ty = t.geometry.x.values, t.geometry.y.values
tc, tr = ((tx - x0) / RES).astype(int), ((y1 - ty) / RES).astype(int)

# keep points only within 12 m of a census tree (crown limit 9 m + margin); ground grid over the whole box
near = np.zeros((H, W), bool)
near[tr, tc] = True
near = ndimage.distance_transform_edt(~near) * RES <= 12

cache = RAW / "lidar_2023/escapos_points.npz"       # per-point cache: stays in raw/
gmin = np.full(GW * GH, np.inf, "float32")
if not cache.exists():
    parts = []
    for f in sorted((RAW / "lidar_2023").glob("*.las")):
        with laspy.open(f) as L:
            h = L.header
            if h.maxs[0] < x0 or h.mins[0] > x1 or h.maxs[1] < y0 or h.mins[1] > y1:
                continue
            for p in L.chunk_iterator(5_000_000):
                x, y, z = np.asarray(p.x), np.asarray(p.y), np.asarray(p.z, "float32")
                m = (x >= x0) & (x < x1) & (y >= y0) & (y < y1)
                x, y, z = x[m], y[m], z[m]
                gi = ((y1 - y) / GRES).astype(int) * GW + ((x - x0) / GRES).astype(int)
                np.minimum.at(gmin, gi, z)
                k = near[((y1 - y) / RES).astype(int), ((x - x0) / RES).astype(int)]
                red, nir = np.asarray(p.red, "float32")[m][k], np.asarray(p.nir, "float32")[m][k]
                parts.append(np.c_[x[k], y[k], z[k], (nir - red) / np.maximum(nir + red, 1)])
        print("read", f.name)
    a = np.vstack(parts)
    np.savez_compressed(cache, x=a[:, 0], y=a[:, 1], z=a[:, 2].astype("float32"),
                        ndvi=a[:, 3].astype("float32"), gmin=gmin)
d = np.load(cache)
x, y, z, ndvi, gmin = d["x"], d["y"], d["z"], d["ndvi"], d["gmin"]
print(f"{len(x):,} points within 12 m of census trees; NDVI > {NDVI_MIN}: {(ndvi > NDVI_MIN).mean():.0%}")

# ---- ground (ASSUMPTION: lowest-point grid + opening)
g = gmin.reshape(GH, GW).astype("float32")
g[np.isinf(g)] = np.nan
nn = ndimage.distance_transform_edt(np.isnan(g), return_distances=False, return_indices=True)
g = ndimage.median_filter(ndimage.grey_opening(g[tuple(nn)], size=OPEN_M), size=5)
gz = g[((y1 - y) / GRES).astype(int).clip(0, GH - 1), ((x - x0) / GRES).astype(int).clip(0, GW - 1)]
hag = z - gz
idx = ((y1 - y) / RES).astype(int).clip(0, H - 1) * W + ((x - x0) / RES).astype(int).clip(0, W - 1)
veg = (ndvi > NDVI_MIN) & (hag > 0)
chm = np.full(W * H, np.nan, "float32")
np.fmax.at(chm, idx[veg], hag[veg])
chm = np.nan_to_num(chm.reshape(H, W), nan=0).clip(0, 45)

# ---- crowns: identical to Porta
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

ids = np.arange(1, len(t) + 1)
area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
hmax = np.where(area > 0, ndimage.maximum(chm, crowns, ids), np.nan)
pid = crowns.ravel()[idx]
sel = pid > 0
P = pd.DataFrame({"id": pid[sel], "h": hag[sel], "veg": veg[sel], "gnd": hag[sel] < GROUND_H})
base = P[P.veg & (P.h > 1.5)].groupby("id").h.quantile(0.10)
gap = P.groupby("id").gnd.mean().reindex(ids)
npts = P.groupby("id").size().reindex(ids)
out = pd.DataFrame({
    "tree_id": t.id, "cens_id": t.cens_id, "species": t.species, "x": tx.round(2), "y": ty.round(2),
    "census_h_m": t.h_m.round(2), "census_crown_w_m": t.crn_w_m.round(2),
    "height_m": np.round(hmax, 2), "crown_area_m2": np.round(area, 1),
    "crown_diam_m": np.round(2 * np.sqrt(area / np.pi), 2),
    "crown_base_m": base.reindex(ids).round(2).values, "gap_fraction": gap.round(3).values,
    "lai_proxy": (-np.log(gap.clip(0.02, 1)) / K).round(2).values, "n_points": npts.fillna(0).astype(int).values})
out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                        ["no_crown_detected", "few_points", "low_tree"], "ok")
# census fields (CC BY-NC, kept out of the repo) are dropped; join back on cens_id
out.drop(columns=["x", "y", "census_h_m", "census_crown_w_m"]).to_csv(ROOT / "databases/florence/florence_tree_lidar.csv", index=False)
ok = out[out.flag == "ok"]
print(f"trees {len(out)}, ok {len(ok)}; flags:", out.flag.value_counts().to_dict())


# ---- validation against the census
def metrics(a, b):
    e = a - b
    return {"n": len(a), "bias": e.mean(), "mae": e.abs().mean(), "rmse": np.sqrt((e ** 2).mean()),
            "pearson": stats.pearsonr(a, b)[0], "spearman": stats.spearmanr(a, b)[0]}


rows = []
for var, lid, cen in (("height", "height_m", "census_h_m"), ("crown_width", "crown_diam_m", "census_crown_w_m")):
    rows.append({"variable": var, "species": "ALL", **metrics(ok[lid], ok[cen])})
    for sp, s in ok.groupby("species"):
        if len(s) >= MIN_SP:
            rows.append({"variable": var, "species": sp, **metrics(s[lid], s[cen])})
v = pd.DataFrame(rows).round(3)
v.to_csv(ROOT / "databases/florence/florence_lidar_validation.csv", index=False)
print(v.to_string(index=False))

# ---- LAI proxy per species next to Porta (no reference: Escapos `lai` is synthetic)
porta = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv").set_index("species")
fl = ok.groupby("species").lai_proxy.agg(n="size", med="median", q25=lambda s: s.quantile(.25), q75=lambda s: s.quantile(.75))
key = lambda s: s.lower().replace(" x ", " ").replace("×", "").split("'")[0].strip()
pk = {key(s): s for s in porta.index}
lai = fl[fl.n >= MIN_SP].assign(porta_species=lambda d: [pk.get(key(s)) for s in d.index]).dropna()
lai = lai.join(porta[["n", "lai_proxy_med", "lai_proxy_iqr"]].rename(columns=lambda c: "porta_" + c), on="porta_species")
print("LAI proxy, shared species (>= 20 Florence trees):\n", lai.round(2).to_string())
lai.round(2).to_csv(ROOT / "databases/florence/florence_lai_vs_porta.csv")

fig, ax = plt.subplots(1, 2, figsize=(11, 5))
for a, (lid, cen, lbl) in zip(ax, (("height_m", "census_h_m", "Height (m)"), ("crown_diam_m", "census_crown_w_m", "Crown width (m)"))):
    a.scatter(ok[cen], ok[lid], s=6, alpha=.4)
    m = max(ok[cen].max(), ok[lid].max())
    a.plot([0, m], [0, m], "k--", lw=1)
    r = v[(v.species == "ALL") & (v.variable == ("height" if lid == "height_m" else "crown_width"))].iloc[0]
    a.set(xlabel=f"Census {lbl}", ylabel=f"LiDAR {lbl}",
          title=f"n={int(r.n)}  bias {r.bias:+.2f}  RMSE {r.rmse:.2f}  r {r.pearson:.2f}")
fig.suptitle("Firenze Nova: LiDAR 2023 vs Life Escapos census", fontsize=10)
fig.text(0.01, 0.0, "Dati LiDAR 2023 forniti da [Comune di Firenze], derivati dal rilievo aereo effettuato sul "
         "territorio comunale nel periodo maggio/giugno 2023.", fontsize=7)
fig.savefig(ROOT / "notes/figures/florence_lidar_validation.png", dpi=130, bbox_inches="tight")
