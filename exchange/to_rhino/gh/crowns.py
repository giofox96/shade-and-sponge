"""GH Python 3 (Rhino 8) or IronPython (Rhino 7). Crowns (ellipsoids) + trunks from any kit crowns CSV.
Inputs:  path (str), scenario (str, "" = all), street (str, "" = all), group (str, "" = all), value (str, column to output, e.g. street_gain_pct)
Outputs: crowns (Breps), trunks (Lines), colors (Colors, from the 'color' column), values (floats), species (str)
"""
import csv
import System.Drawing as sd
import Rhino.Geometry as rg

crowns, trunks, colors, values, species = [], [], [], [], []
with open(path) as f:
    for r in csv.DictReader(f):
        if scenario and r.get("scenario") != scenario: continue
        if street and r.get("street") != street: continue
        if group and r.get("group") != str(group): continue
        h, hb, d, z0 = float(r["height_m"]), float(r["crown_base_m"]), float(r["crown_diam_m"]), float(r["ground_z"])
        x, y = float(r["x"]), float(r["y"])
        depth = max(h - hb, 1.0)
        zc = z0 + h - depth / 2.0
        s = rg.Sphere(rg.Point3d.Origin, 1.0).ToBrep()
        s.Transform(rg.Transform.Scale(rg.Plane.WorldXY, d / 2.0, d / 2.0, depth / 2.0))
        s.Transform(rg.Transform.Translation(rg.Vector3d(x, y, zc)))
        crowns.append(s)
        trunks.append(rg.Line(rg.Point3d(x, y, z0), rg.Point3d(x, y, zc - depth / 2.0 + 0.3)))
        colors.append(sd.ColorTranslator.FromHtml(r.get("color") or "#9a9a9a"))
        v = r.get(value) if value else None
        values.append(float(v) if v not in (None, "") else 0.0)
        species.append(r.get("species", ""))
