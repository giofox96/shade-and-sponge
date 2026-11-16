"""Thinned LiDAR cloud for the web app's "LiDAR points" layer: python scripts/web_export_lidar.py
Reads the cropped Porta cloud cached by scripts/bcn_lidar_porta.py (ICGC Territorial LiDAR v3.1, flown 26 Sept 2021), keeps
one point per VOX-metre cube inside the site grid and writes web/public/data/porta*/lidar.bin.gz plus a `lidar` entry in
each meta.json. Run scripts/web_export_terrain.py first (heights share its zero). File layout, little-endian, n points:
int16 east[n], int16 north[n] (0.1 m from site.center, on the web map's sphere), uint16 z[n] (0.1 m above the site's lowest
point), uint16 height above ground[n] (0.1 m), uint8 class[n] (0 ground, 1 vegetation, 2 building, 3 other)."""
import sys, json, glob, gzip, numpy as np
from pyproj import Transformer
sys.path.insert(0, ".")
from shade_sponge.site import load_site, ROOT

VOX = 2.0     # m: ASSUMPTION (display only; about 1 M points, 4.7 MB; 1.5 m gave 1.77 M)
M_DEG = 40075016.686 / 360   # metres per degree on the Web Mercator sphere, as deck.gl places metre offsets
GROUND, VEG, BLDG = (2, 8, 75), (3, 4, 5), (6,)   # as scripts/bcn_lidar_porta.py
site = load_site("porta")
H, W = site.dtm.shape
d = np.load(ROOT / "databases/barcelona/raw/lidar/porta_points.npz")
x, y, z, c = d["x"], d["y"], d["z"], d["c"]
col, row = ((x - site.x0) / site.res).astype(int), ((site.y1 - y) / site.res).astype(int)
m = (col >= 0) & (col < W) & (row >= 0) & (row < H) & ~np.isin(c, (7, 18))   # inside the grid, no noise classes
x, y, z, c, col, row = x[m], y[m], z[m], c[m], col[m], row[m]
vox = np.c_[(x / VOX).astype(np.int64), (y / VOX).astype(np.int64), (z / VOX).astype(np.int64)]
_, keep = np.unique(vox, axis=0, return_index=True)
x, y, z, c, col, row = x[keep], y[keep], z[keep], c[keep], col[keep], row[keep]
metas = sorted(glob.glob(str(ROOT / "web/public/data/porta*/meta.json")))
meta0 = json.load(open(metas[0], encoding="utf-8"))
lon0, lat0 = meta0["site"]["center"]
lo = meta0["terrain"]["min_m"]
lon, lat = Transformer.from_crs(25831, 4326, always_xy=True).transform(x, y)
east = (lon - lon0) * M_DEG * np.cos(np.radians(lat0))
north = (lat - lat0) * M_DEG
hag = np.clip(z - site.dtm[row, col], 0, None)
cls = np.where(np.isin(c, GROUND), 0, np.where(np.isin(c, VEG), 1, np.where(np.isin(c, BLDG), 2, 3))).astype("uint8")
q = lambda a, t: np.round(np.asarray(a) * 10).astype(t).tobytes()
buf = q(east, "<i2") + q(north, "<i2") + q(np.clip(z - lo, 0, None), "<u2") + q(hag, "<u2") + cls.tobytes()
entry = dict(file="lidar.bin.gz", n=int(len(x)), voxel_m=VOX)
for f in metas:
    with gzip.open(f.replace("meta.json", "lidar.bin.gz"), "wb", compresslevel=9) as g:
        g.write(buf)
    meta = json.load(open(f, encoding="utf-8"))
    meta["lidar"] = entry
    json.dump(meta, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(entry, "class counts", np.bincount(cls).tolist(), "gz bytes", len(gzip.compress(buf, 9)))
