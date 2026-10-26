"""Drop free planting spots that sit too close to street furniture mapped in OSM (notes/sidewalk_width.md, "Spot exclusions").
Input: databases/barcelona/porta_planting_spots.csv (scripts/porta_planting_spots.py) and the OSM cut raw/osm/porta.osm
(scripts/osmnx_street_width.py), read with OSMnx. Writes the column `excluded_by` back into porta_planting_spots.csv
(empty = kept); layout.planting_spots() drops excluded spots. Clearances, measured to the OSM point or line:
  traffic signals          3 m  2011 street-tree guide (> 3 m from traffic lights and signs; notes/tree_master_plan.md §5)
  crossings (line, point)  3 m  ASSUMPTION: the guide's sign clearance, as crossings carry signs and need sight lines
  parking entrance         3 m  ASSUMPTION: guide's > 1 m from driveways + half a ~4 m driveway (OSM has the point only)
  bus stop / platform      8 m  ASSUMPTION: keeps ~16 m of kerb free for the shelter and the bus doors; no source yet
Not in OSM here (so the spots stay an upper bound): lamps (4 mapped in the cut), signs, driveways without a parking
entrance, underground services, balconies. Run from the repo root: python scripts/porta_spot_exclusions.py"""
import pathlib, pandas as pd, geopandas as gpd, osmnx as ox

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPOTS, XML = ROOT / "databases/barcelona/porta_planting_spots.csv", ROOT / "databases/barcelona/raw/osm/porta.osm"
RULES = [("traffic_signals", {"highway": "traffic_signals"}, 3.0),
         ("crossing", {"highway": "crossing"}, 3.0),
         ("crossing", {"footway": "crossing"}, 3.0),
         ("parking_entrance", {"amenity": "parking_entrance"}, 3.0),
         ("bus_stop", {"highway": "bus_stop"}, 8.0),
         ("bus_stop", {"public_transport": "platform"}, 8.0)]

s = pd.read_csv(SPOTS).drop(columns="excluded_by", errors="ignore")
pts = gpd.GeoSeries(gpd.points_from_xy(s.x, s.y), crs=25831)
s["excluded_by"] = ""
for name, tags, d in RULES:
    f = ox.features_from_xml(XML, tags=tags).to_crs(25831).geometry
    hit = pts.apply(lambda p: f.distance(p).min() < d).values & (s.excluded_by == "")   # first rule that applies
    s.loc[hit, "excluded_by"] = name
s.to_csv(SPOTS, index=False)
kept = s[s.excluded_by == ""]
print(f"{len(s)} spots -> {len(kept)} kept; excluded by:", s[s.excluded_by != ""].excluded_by.value_counts().to_dict())
print("kept by size class:", kept.size_class.value_counts().to_dict(), "| before:", s.size_class.value_counts().to_dict())
