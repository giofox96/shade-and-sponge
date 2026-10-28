"""Sidewalk width without a tree, from OSMnx (street centrelines + lanes) and OSM buildings: the estimate new planting
spots would need outside Porta (notes/sidewalk_width.md, "OSMnx check").
Input: databases/barcelona/raw/osm/bcn.osm.pbf (scripts/osm_sidewalks.py). A Porta + margin cut is written to raw/osm/porta.osm
(OSM XML), because OSMnx reads XML offline (Overpass is unreachable from cloud sessions; on a PC graph_from_polygon works too).
Method, per measured Porta tree (porta_sidewalk_width.csv, flag ok): nearest drivable street edge -> ray from the centreline
through the tree to the first building outline (distance D) -> width = D - lanes x LANE_W / 2 - PARKING.
ASSUMPTIONS: LANE_W 3.0 m; lanes untagged = 1 one-way / 2 two-way; PARKING variants 0 / 1.1 / 2.2 m (parking is tagged on ~1% of
edges, so its presence is unknown: 1.1 m = half a 2.2 m parking lane, a midpoint, not a measurement).
Output: databases/barcelona/osmnx_street_width_check.csv. Run from the repo root: python scripts/osmnx_street_width.py"""
import json, pathlib, numpy as np, pandas as pd, osmium, osmnx as ox
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
OSM = ROOT / "databases/barcelona/raw/osm"
PBF, XML = OSM / "bcn.osm.pbf", OSM / "porta.osm"
BOX = (2.168, 41.426, 2.190, 41.444)                     # Porta + margin, lon/lat
LANE_W, RAY = 3.0, 40.0
DRIVE = "primary|secondary|tertiary|residential|living_street|unclassified|trunk"

if not XML.exists():                                     # ways touching the box + every node they reference
    inside = lambda l: l.valid() and BOX[0] <= l.lon <= BOX[2] and BOX[1] <= l.lat <= BOX[3]
    keep = {o.id for o in osmium.FileProcessor(str(PBF)).with_locations() if o.is_way() and any(inside(n.location) for n in o.nodes)}
    with osmium.BackReferenceWriter(str(XML), ref_src=str(PBF), overwrite=True) as w:
        for o in osmium.FileProcessor(str(PBF)).with_locations():
            if (o.is_way() and o.id in keep) or (o.is_node() and inside(o.location) and len(o.tags)):
                w.add(o)

ox.settings.useful_tags_way = list(set(ox.settings.useful_tags_way + ["sidewalk", "sidewalk:both", "parking:both", "width", "lanes", "oneway"]))
E = ox.graph_to_gdfs(ox.project_graph(ox.graph_from_xml(XML, retain_all=True), to_crs=25831), nodes=False)
E = E[E.highway.astype(str).str.contains(DRIVE)]
bld = ox.features_from_xml(XML, tags={"building": True}).to_crs(25831)
B = bld[bld.geom_type.isin(["Polygon", "MultiPolygon"])].union_all().boundary
counts = {k: len(ox.features_from_xml(XML, tags={k.split("=")[0]: k.split("=")[1]}))
          for k in ("highway=crossing", "highway=bus_stop", "footway=sidewalk", "natural=tree")}
print(f"drive edges {len(E)}: lanes tagged {E.lanes.notna().mean():.0%}, width {E.width.notna().mean():.0%}, "
      f"parking {E['parking:both'].notna().mean():.0%}; features in the cut: {counts}")

o = json.load(open(ROOT / "exchange/site_origin.json"))
t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
t["x"], t["y"] = t.x + o["origin_x"], t.y + o["origin_y"]
w = pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv").merge(t[["tree_id", "x", "y"]], on="tree_id")
w = w[(w.flag == "ok") & w.width_m.notna()].reset_index(drop=True)
lines = E.geometry.values
tree = STRtree(lines)


def lanes(e):
    try:
        n = float(str(e.lanes).split(";")[0])
        if n == n:                                       # "nan" parses as a float
            return n
    except ValueError:
        pass
    return 1.0 if str(e.oneway) == "True" else 2.0


D, L = [], []
for r in w.itertuples():
    P = Point(r.x, r.y)
    i = tree.nearest(P)
    Q = nearest_points(lines[i], P)[0]
    d = P.distance(Q)
    hit = LineString([Q.coords[0], (Q.x + RAY * (P.x - Q.x) / d, Q.y + RAY * (P.y - Q.y) / d)]).intersection(B) if d > 0.5 else None
    ok = hit is not None and not hit.is_empty and Q.distance(hit) > d
    D.append(Q.distance(hit) if ok else np.nan)
    L.append(lanes(E.iloc[i]))
D, L = np.array(D), np.array(L)
m = ~np.isnan(D)
cls = lambda v: np.select([v < 2.5, v < 3.5, v <= 6], ["none", "small", "medium"], "large")
ref, rc = w.width_m.values[m], w.size_class.values[m]
rows = []
for park in (0.0, 1.1, 2.2):
    v = (D - L * LANE_W / 2 - park)[m]
    rows.append(dict(proxy=f"C_centreline_lanes_parking{park}", n=int(m.sum()), coverage=m.mean(), median_error_m=np.median(v - ref),
                     within_1m=np.mean(np.abs(v - ref) <= 1), class_agrees=np.mean(cls(v) == rc)))
rows.append(dict(proxy="baseline_all_large", n=int(m.sum()), coverage=m.mean(), class_agrees=np.mean(rc == "large")))
r = pd.DataFrame(rows)
r.round(3).to_csv(ROOT / "databases/barcelona/osmnx_street_width_check.csv", index=False)
print(r.round(2).to_string(index=False))
