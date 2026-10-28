"""ICGC 1 km LiDAR tiles each barri needs: the tiles touching the barri polygon buffered by BUFFER_M (shade_sponge/site.py),
the part of build_barri()'s grid that can shade or drain into the barri (notes/citywide_plan.md §6.2 step 1). Input: web/public/data/barris.geojson (73 official outlines,
Open Data BCN, scripts/make_barris_web.py). Output: databases/barcelona/lidar_tiles_barris.csv, one row per barri × tile,
with the flight dates already read for that tile (lidar_tiles_dates.csv; empty = not read yet).
Tile id = x km (3 digits) + (y km − 4000) (3 digits) of its lower-left corner, as scripts/bcn_lidar_species.py."""
import pathlib, sys, pandas as pd, geopandas as gpd
from shapely.geometry import box
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import BUFFER_M, slug

b = gpd.read_file(ROOT / "web/public/data/barris.geojson").to_crs(25831)
dates = pd.read_csv(ROOT / "databases/barcelona/lidar_tiles_dates.csv", dtype={"tile": str}).set_index("tile")
rows = []
for r in b.itertuples():
    g = r.geometry.buffer(BUFFER_M)
    x0, y0, x1, y1 = g.bounds
    for i in range(int(x0 // 1000), int(x1 // 1000) + 1):
        for j in range(int(y0 // 1000), int(y1 // 1000) + 1):
            if not g.intersects(box(i * 1000, j * 1000, i * 1000 + 1000, j * 1000 + 1000)):
                continue
            t = f"{i:03d}{j - 4000:03d}"
            rows.append(dict(barri=r.name, slug=slug(r.name), district=r.district, planes=r.planes, tile=t,
                             first=dates.first.get(t, ""), last=dates["last"].get(t, "")))
out = pd.DataFrame(rows)
out.to_csv(ROOT / "databases/barcelona/lidar_tiles_barris.csv", index=False)
n = out.groupby("barri").tile.size()
print(f"{len(b)} barris, {out.tile.nunique()} distinct tiles; tiles per barri: median {n.median():.0f}, max {n.max()} ({n.idxmax()})")
print("tiles with a flight date already read:", out[out["first"] != ""].tile.nunique())
