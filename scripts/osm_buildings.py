"""City-wide OSM building footprints and green areas from the local BBBike extract, so the barri runs need no Overpass
(busy for days).
Input: databases/barcelona/raw/osm/bcn.osm.pbf (scripts/osm_sidewalks.py; BBBike extract "Barcelona", ODbL; downloaded if missing).
Output: databases/barcelona/raw/osm/buildings.gpkg (EPSG:25831), read by scripts/bcn_lidar_barri.py before trying Overpass;
        raw/osm/green.gpkg (leisure=park/garden, landuse=grass, the tags of shade_sponge.site), read by build_barri().
Needs: pip install osmium. Run from the repo root: python scripts/osm_buildings.py"""
import pathlib, geopandas as gpd, osmium, requests
import shapely.wkb as wkblib

OSM = pathlib.Path(__file__).resolve().parents[1] / "databases/barcelona/raw/osm"
PBF = OSM / "bcn.osm.pbf"
URL = "https://download.bbbike.org/osm/bbbike/Barcelona/Barcelona.osm.pbf"
fab = osmium.geom.WKBFactory()


class H(osmium.SimpleHandler):
    def __init__(s):
        super().__init__()
        s.geoms, s.green = [], []

    def area(s, a):
        t = a.tags
        out = s.geoms if t.get("building", "no") != "no" else \
            s.green if t.get("leisure") in ("park", "garden") or t.get("landuse") == "grass" else None
        if out is not None:
            try:
                out.append(wkblib.loads(fab.create_multipolygon(a), hex=True))
            except Exception:
                pass


if not PBF.exists():
    OSM.mkdir(parents=True, exist_ok=True)
    PBF.write_bytes(requests.get(URL, timeout=600).content)
h = H()
h.apply_file(str(PBF), locations=True)
g = gpd.GeoDataFrame(geometry=h.geoms, crs=4326).to_crs(25831)
g.to_file(OSM / "buildings.gpkg")
gpd.GeoDataFrame(geometry=h.green, crs=4326).to_crs(25831).to_file(OSM / "green.gpkg")
print(f"{len(g)} building footprints and {len(h.green)} green areas from {PBF.name} (modified {PBF.stat().st_mtime:.0f}) -> {OSM / 'buildings.gpkg'}")
