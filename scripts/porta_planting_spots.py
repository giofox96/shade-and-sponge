"""Free street-tree planting spots in Porta (additions scenarios A and R+A; notes/topic_decision.md §10.6).

Same sources and width method as scripts/porta_sidewalk_width.py (1:1000 topographic map, CC BY 4.0, cached SVG tiles):
walk every facade line, cast a ray away from the building, and take the first road line (kerb) as the sidewalk edge.
Rules (2011 street-tree guide pp. 22-23, notes/tree_master_plan.md §5): no tree below 2.5 m of sidewalk; size class by
width (<3.5 small, 3.5-6 medium, >6 large); spacing 7 / 9 / 13 m by class, here applied to every existing street tree too.
Spot = KERB_OFFSET m in from the kerb: the median kerb-to-tree distance of Porta's measured trees (0.69 m,
databases/barcelona/porta_sidewalk_width.csv, width_m - facade_dist_m).
ASSUMPTION / upper bound: driveways, crossings, bus stops, lamps, terraces and underground services are not in the data,
so the spots are a capacity ceiling, not a planting plan.
Output: databases/barcelona/porta_planting_spots.csv (EPSG:25831). Run from the repo root: python scripts/porta_planting_spots.py,
then python scripts/porta_spot_exclusions.py (adds the OSM street-furniture exclusions to the same file).
Other barri (whole-city "add only" run for the barris with no planes, user 28 Nov): python scripts/porta_planting_spots.py "<barri>"
-> databases/barcelona/<slug>_planting_spots.csv, from barris/<slug>/trees_lidar.csv and buildings.geojson
(scripts/bcn_lidar_barri.py). The OSM exclusions of scripts/porta_spot_exclusions.py are applied here from Overpass
(same rules and clearances). Porta's second pass from the city's street objects (lamps, signs, bollards;
scripts/porta_spot_exclusions_city.py) and the spot classes are Porta-only, so these spots are a looser upper bound
than Porta's (ASSUMPTION).
"""
import json, sys, numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree
from shapely.ops import unary_union
from porta_sidewalk_width import ROOT, RAY, MIN_KERB, TILE, lines, size_class

STEP, KERB_OFFSET, PROBE = 2.0, 0.7, 0.5
SPACING = {"small": 7.0, "medium": 9.0, "large": 13.0}

NAME = sys.argv[1] if len(sys.argv) > 1 else "Porta"
sys.path.insert(0, str(ROOT))
from shade_sponge.site import slug  # noqa: E402
SLUG = slug(NAME)
b = pd.read_csv(ROOT / "databases/barcelona/raw/BarcelonaCiutat_Barris.csv")
if SLUG == "porta":
    o = json.load(open(ROOT / "exchange/site_origin.json"))
    t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
    TX, TY = (t.x + o["origin_x"]).values, (t.y + o["origin_y"]).values
    bld = gpd.read_file(ROOT / "exchange/to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
    blds = unary_union(bld.translate(o["origin_x"], o["origin_y"]).geometry.values)
else:
    d = ROOT / f"databases/barcelona/barris/{SLUG}"
    t = pd.read_csv(d / "trees_lidar.csv")
    TX, TY = t.x.values, t.y.values
    blds = unary_union(gpd.read_file(d / "buildings.geojson").to_crs(25831).geometry.values)
porta = gpd.GeoSeries.from_wkt(b.loc[b.nom_barri.map(slug) == SLUG, "geometria_etrs89"]).iloc[0]   # the site polygon

xs = np.arange(np.floor((TX.min() - RAY) / TILE) * TILE, TX.max() + RAY, TILE)
ys = np.arange(np.floor((TY.min() - RAY) / TILE) * TILE, TY.max() + RAY, TILE)
fac, road = lines("facade", xs, ys), lines("road", xs, ys)
road = [g for g in road if g.length >= MIN_KERB]
tf, tr = STRtree(fac), STRtree(road)

cand = []
for i, f in enumerate(fac):
    if not f.intersects(porta.buffer(RAY)):
        continue
    for s in np.arange(STEP / 2, f.length, STEP):
        a, c = f.interpolate(max(0, s - 0.5)), f.interpolate(min(f.length, s + 0.5))
        q = f.interpolate(s)
        dx, dy = c.x - a.x, c.y - a.y
        n = np.hypot(dx, dy)
        if n < 1e-6:
            continue
        for u in (np.array([-dy, dx]) / n, np.array([dy, -dx]) / n):
            if blds.contains(Point(q.x + u[0] * PROBE, q.y + u[1] * PROBE)):
                continue                                   # this side is inside a building
            ray = LineString([(q.x, q.y), (q.x + u[0] * RAY, q.y + u[1] * RAY)])
            d = sorted(Point(q.x, q.y).distance(h) for h in (ray.intersection(road[j]) for j in tr.query(ray)) if not h.is_empty)
            d = [x for x in d if x > 0.05]
            if not d:
                continue
            w = d[0]
            fd = [Point(q.x, q.y).distance(h) for h in (ray.intersection(fac[j]) for j in tf.query(ray) if j != i) if not h.is_empty]
            if any(0.05 < x < w for x in fd):                  # another facade before the kerb: courtyard, recess
                continue
            p = Point(q.x + u[0] * (w - KERB_OFFSET), q.y + u[1] * (w - KERB_OFFSET))
            if w >= 2.5 and porta.contains(p):
                cand.append((i, s, p.x, p.y, w))

c = pd.DataFrame(cand, columns=["line", "s", "x", "y", "width_m"]).drop_duplicates(["x", "y"])
# Street sidewalks only: the map's road lines also trace paths inside blocks. Keep spots within STREET_M of an OSM street
# centreline (ODbL). ASSUMPTION: 15 m covers half a carriageway plus the pit offset on Porta's streets.
import osmnx as ox
STREET_M = 15.0
STREETS = ["primary", "secondary", "tertiary", "residential", "unclassified", "living_street", "pedestrian"]
e = ox.features_from_polygon(gpd.GeoSeries([porta.buffer(50)], crs=25831).to_crs(4326).iloc[0], tags={"highway": STREETS})
e = e[e.geom_type.isin(["LineString", "MultiLineString"])].to_crs(25831)
streets = unary_union(e.geometry.values)
c = c[[streets.distance(Point(x, y)) <= STREET_M for x, y in zip(c.x, c.y)]]
c["size_class"] = size_class(c.width_m.values)
c["spacing_m"] = c.size_class.map(SPACING)
taken_x, taken_y, keep = list(TX), list(TY), []
for r in c.sort_values(["line", "s"]).itertuples():          # greedy along each facade, existing trees first
    if np.min(np.hypot(np.array(taken_x) - r.x, np.array(taken_y) - r.y)) >= r.spacing_m:
        keep.append(r.Index)
        taken_x.append(r.x)
        taken_y.append(r.y)
out = c.loc[keep, ["x", "y", "width_m", "size_class"]].reset_index(drop=True)
out.insert(0, "spot_id", [f"ADD{k:04d}" for k in range(len(out))])
assert out.width_m.min() >= 2.5 and porta.contains(gpd.points_from_xy(out.x, out.y)).all()
if SLUG != "porta":                                       # OSM exclusions, same rules as scripts/porta_spot_exclusions.py
    from porta_spot_exclusions import RULES
    from osmnx._errors import InsufficientResponseError
    area = gpd.GeoSeries([porta.buffer(50)], crs=25831).to_crs(4326).iloc[0]
    pts = gpd.GeoSeries(gpd.points_from_xy(out.x, out.y), crs=25831)
    out["excluded_by"] = ""
    for name, tags, dist in RULES:
        try:
            f = ox.features_from_polygon(area, tags=tags).to_crs(25831).geometry
        except InsufficientResponseError:          # none of these objects in the barri
            continue
        hit = pts.apply(lambda q: f.distance(q).min() < dist).values & (out.excluded_by == "")
        out.loc[hit, "excluded_by"] = name
    print("excluded by:", out[out.excluded_by != ""].excluded_by.value_counts().to_dict())
out.round({"x": 2, "y": 2, "width_m": 2}).to_csv(ROOT / f"databases/barcelona/{SLUG}_planting_spots.csv", index=False)
print(f"{len(c)} candidate points on sidewalks >= 2.5 m; {len(out)} spots after spacing:", out.size_class.value_counts().to_dict())
