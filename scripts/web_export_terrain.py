"""Relief for the web app's "3D ground": python scripts/web_export_terrain.py [site]
Writes web/public/data/<site>*/terrain.png and a `terrain` entry in each meta.json. The PNG is the site DTM (ICGC LiDAR,
the grid the runoff routing uses) resampled to a lon/lat grid of about 2 m, as metres above the site's lowest point:
red × 25.6 + green × 0.1 (0.1 m steps). Needs the site's raw data (run where `python -m shade_sponge` runs)."""
import sys, json, glob, numpy as np
from PIL import Image
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling, transform_bounds
sys.path.insert(0, ".")
from shade_sponge.site import load_site, ROOT

STEP = 2.0   # m per pixel: ASSUMPTION (display only; a 1 m mesh is four times heavier and looks the same at street scale)
name = sys.argv[1] if len(sys.argv) > 1 else "porta"
site = load_site(name)
H, W = site.dtm.shape
w, s, e, n = transform_bounds(25831, 4326, site.x0, site.y1 - H * site.res, site.x0 + W * site.res, site.y1, densify_pts=21)
cols, rows = round(W * site.res / STEP), round(H * site.res / STEP)
out = np.full((rows, cols), np.nan, "float32")
reproject(site.dtm.astype("float32"), out, src_transform=site.transform, src_crs="EPSG:25831", src_nodata=np.nan,
          dst_transform=from_bounds(w, s, e, n, cols, rows), dst_crs="EPSG:4326", dst_nodata=np.nan,
          resampling=Resampling.bilinear)
lo = float(np.nanmin(out))
out = np.where(np.isnan(out), lo, out)   # slivers outside the UTM grid (it is slightly rotated against lon/lat): lowest point
d = np.round((out - lo) * 10).astype(int)
rgb = np.zeros((rows, cols, 3), "uint8")
rgb[..., 0], rgb[..., 1] = d // 256, d % 256
entry = dict(file="terrain.png", bounds=[round(v, 6) for v in (w, s, e, n)], min_m=round(lo, 1), max_m=round(float(out.max()), 1))
for folder in sorted(glob.glob(str(ROOT / f"web/public/data/{name}*/meta.json"))):
    Image.fromarray(rgb).save(folder.replace("meta.json", "terrain.png"), optimize=True)
    meta = json.load(open(folder, encoding="utf-8"))
    meta["terrain"] = entry
    json.dump(meta, open(folder, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(folder, entry)
