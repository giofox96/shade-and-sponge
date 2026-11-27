"""Lines for the base map: GeoJSON LineStrings (porta_sidewalks.geojson, property 'kind') or a CSV polyline (porta_boundary.csv).
Inputs: path (str), kind (str, "" = all; e.g. "facade" or "kerb"). Outputs: curves, kinds. z = 0 (flat map)."""
import csv, json
import Rhino.Geometry as rg

curves, kinds = [], []
if path.lower().endswith(".csv"):
    pts = [rg.Point3d(float(r["x"]), float(r["y"]), 0) for r in csv.DictReader(open(path))]
    curves.append(rg.PolylineCurve(pts + [pts[0]])); kinds.append("boundary")
else:
    for f in json.load(open(path))["features"]:
        k = f["properties"].get("kind", "")
        if kind and k != kind: continue
        curves.append(rg.PolylineCurve([rg.Point3d(x, y, 0) for x, y in f["geometry"]["coordinates"]])); kinds.append(k)
