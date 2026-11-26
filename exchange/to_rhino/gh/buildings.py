"""Buildings (extruded footprints) from any kit buildings GeoJSON (Polygon or MultiPolygon, local metres).
Inputs: path (str). Outputs: breps, heights. Base at ground_z (absolute elevation, m), top at ground_z + height_m."""
import json
import Rhino.Geometry as rg

breps, heights = [], []
for f in json.load(open(path))["features"]:
    g, p = f["geometry"], f["properties"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        pts = [rg.Point3d(x, y, p["ground_z"]) for x, y in poly[0]]
        if len(pts) < 4: continue
        ext = rg.Extrusion.Create(rg.PolylineCurve(pts), p["height_m"], True)
        if ext:
            breps.append(ext.ToBrep()); heights.append(p["height_m"])
