"""GhPython component 'LOAD': everything the Ladybug test needs for Pg Andreu Nin, in one component.
Inputs (all Item Access):
  folder   text, the full path of exchange/to_gh, e.g. C:\\ladybug_andreu_nin\\exchange\\to_gh
  scenario text, S0 (today's planes) or S4 (tool layout)
  step     integer, keep every n-th test point (1 = all 1,974; 10 = about 200, for a quick test)
Outputs:
  context  buildings + context crowns + street crowns (the shade context for Ladybug)
  pts      test points, 1.1 m above ground
  info     counts, to check the load"""
import csv, json, os
import Rhino.Geometry as rg

TAG = "20261031"
TREES = {"S0": "street_andreu-nin_trees_S0_current_%s.csv" % TAG,
         "S4": "street_andreu-nin_trees_S4_s1.00_w0.00_r0.00_%s.csv" % TAG}


def rows(name):
    with open(os.path.join(folder, name)) as f:
        return list(csv.DictReader(f))


def crown(r):
    """Ellipsoid crown: centre between crown base and top, horizontal diameter crown_diam_m."""
    h, hb, d, z0 = float(r["height_m"]), float(r["crown_base_m"]), float(r["crown_diam_m"]), float(r["ground_z"])
    s = rg.Sphere(rg.Point3d.Origin, 1.0).ToBrep()
    s.Transform(rg.Transform.Scale(rg.Plane.WorldXY, d / 2.0, d / 2.0, max(h - hb, 1.0) / 2.0))
    s.Transform(rg.Transform.Translation(rg.Vector3d(float(r["x"]), float(r["y"]), z0 + (h + hb) / 2.0)))
    return s


buildings = []
gj = json.load(open(os.path.join(folder, "street_andreu-nin_buildings_%s.geojson" % TAG)))
for f in gj["features"]:
    g, p = f["geometry"], f["properties"]
    for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
        crv = rg.PolylineCurve([rg.Point3d(x, y, p["ground_z"]) for x, y in poly[0]])
        b = rg.Surface.CreateExtrusion(crv, rg.Vector3d(0, 0, p["height_m"])).ToBrep().CapPlanarHoles(0.01)
        if b:
            buildings.append(b)

ctx_crowns = [crown(r) for r in rows("street_andreu-nin_context_trees_%s.csv" % TAG)]
street_crowns = [crown(r) for r in rows(TREES[str(scenario).strip().upper()])]
context = buildings + ctx_crowns + street_crowns
pts = [rg.Point3d(float(r["x"]), float(r["y"]), float(r["z"]))
       for r in rows("street_andreu-nin_testpoints_%s.csv" % TAG)][::int(step or 1)]
info = "scenario %s: %d buildings, %d context crowns, %d street crowns, %d test points" % (
    scenario, len(buildings), len(ctx_crowns), len(street_crowns), len(pts))
