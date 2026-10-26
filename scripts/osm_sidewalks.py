"""Can OpenStreetMap stand in for the 1:1000 map's sidewalk widths outside Porta? (notes/sidewalk_width.md, "OSM check")
Input: databases/barcelona/raw/osm/bcn.osm.pbf (BBBike extract "Barcelona", ODbL; downloaded if missing).
Reads the OSM sidewalk lines (footway=sidewalk), street tags, kerb/crossing/bus-stop nodes and the admin areas, then tests
two width proxies against the measured widths of Porta's trees (databases/barcelona/porta_sidewalk_width.csv, flag ok):
  A  tree -> nearest OSM building outline + 0.69 m (median kerb-to-tree offset, porta_planting_spots.py)
  B  2 x distance from the nearest OSM sidewalk line (<= 8 m from the tree) to the nearest building (line assumed centred)
Size classes as the 2011 guide (< 2.5 none, < 3.5 small, 3.5-6 medium, > 6 large).
Outputs: databases/barcelona/osm_sidewalk_check.csv (one row per proxy); raw/osm/{sidewalks,admin}.gpkg (cached layers).
Needs: pip install osmium. Run from the repo root: python scripts/osm_sidewalks.py"""
import json, pathlib, numpy as np, pandas as pd, geopandas as gpd, requests
import shapely.wkb as wkblib
from shapely.ops import nearest_points
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
OSM = ROOT / "databases/barcelona/raw/osm"
PBF = OSM / "bcn.osm.pbf"
URL = "https://download.bbbike.org/osm/bbbike/Barcelona/Barcelona.osm.pbf"
KERB_OFFSET, MAX_LINE = 0.69, 8.0       # m; MAX_LINE: ASSUMPTION, farther sidewalk lines belong to another street


def read_osm():
    import osmium
    fab = osmium.geom.WKBFactory()

    class H(osmium.SimpleHandler):
        def __init__(s):
            super().__init__()
            s.sw, s.adm, s.nodes = [], [], {"kerb": 0, "crossing": 0, "bus_stop": 0}

        def node(s, n):
            t = n.tags
            s.nodes["kerb"] += "kerb" in t or t.get("barrier") == "kerb"
            s.nodes["crossing"] += t.get("highway") == "crossing" or t.get("footway") == "crossing"
            s.nodes["bus_stop"] += t.get("highway") == "bus_stop"

        def way(s, w):
            if w.tags.get("footway") == "sidewalk":
                try:
                    s.sw.append(dict(geometry=wkblib.loads(fab.create_linestring(w), hex=True), width=w.tags.get("width")))
                except Exception:
                    pass

        def area(s, a):
            t = a.tags
            if t.get("boundary") == "administrative" and t.get("admin_level") in ("8", "9", "10"):
                try:
                    s.adm.append(dict(geometry=wkblib.loads(fab.create_multipolygon(a), hex=True), name=t.get("name"),
                                      level=t.get("admin_level")))
                except Exception:
                    pass
    h = H()
    h.apply_file(str(PBF), locations=True)
    gpd.GeoDataFrame(h.sw, crs=4326).to_crs(25831).to_file(OSM / "sidewalks.gpkg")
    gpd.GeoDataFrame(h.adm, crs=4326).to_crs(25831).to_file(OSM / "admin.gpkg")
    print("nodes:", h.nodes)


if not PBF.exists():
    PBF.write_bytes(requests.get(URL, timeout=600).content)
if not (OSM / "sidewalks.gpkg").exists():
    read_osm()
sw, adm = gpd.read_file(OSM / "sidewalks.gpkg"), gpd.read_file(OSM / "admin.gpkg")
city = adm[(adm.level == "8") & (adm.name == "Barcelona")].union_all()
c = sw[sw.intersects(city)]
print(f"OSM sidewalk lines in Barcelona: {len(c)} ways, {c.length.sum() / 1000:.0f} km; with a width tag: "
      f"{c[c.width.notna()].length.sum() / 1000:.0f} km")

o = json.load(open(ROOT / "exchange/site_origin.json"))
t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
t["x"], t["y"] = t.x + o["origin_x"], t.y + o["origin_y"]
w = pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv").merge(t[["tree_id", "x", "y"]], on="tree_id")
w = w[(w.flag == "ok") & w.width_m.notna()].reset_index(drop=True)
bld = gpd.read_file(ROOT / "exchange/to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
B = bld.set_geometry(bld.translate(o["origin_x"], o["origin_y"])).union_all().boundary   # OSM footprints (ODbL)
P = gpd.GeoSeries(gpd.points_from_xy(w.x, w.y), crs=25831)
s = sw[sw.intersects(P.union_all().buffer(50))].geometry.values
tree = STRtree(s)
cls = lambda v: np.select([v < 2.5, v < 3.5, v <= 6], ["none", "small", "medium"], "large")

a = P.distance(B).values + KERB_OFFSET
b = []
for p in P:
    g = s[tree.nearest(p)]
    b.append(2 * nearest_points(g, p)[0].distance(B) if g.distance(p) <= MAX_LINE else np.nan)
rows = []
for name, v in (("A_tree_to_building", a), ("B_sidewalk_line_x2", np.array(b))):
    m = ~np.isnan(v)
    e = v[m] - w.width_m.values[m]
    rows.append(dict(proxy=name, n=int(m.sum()), coverage=m.mean(), median_error_m=np.median(e), mae_m=np.abs(e).mean(),
                     within_1m=np.mean(np.abs(e) <= 1), class_agrees=np.mean(cls(v[m]) == w.size_class.values[m])))
rows.append(dict(proxy="baseline_all_large", n=len(w), coverage=1.0, class_agrees=(w.size_class == "large").mean()))
r = pd.DataFrame(rows)
r.round(3).to_csv(ROOT / "databases/barcelona/osm_sidewalk_check.csv", index=False)
print(r.round(2).to_string(index=False))
print(pd.crosstab(pd.Series(w.size_class.values, name="measured"), pd.Series(cls(a), name="proxy A")))
