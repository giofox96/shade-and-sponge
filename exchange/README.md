# Data exchange: Python (Claude) ↔ Grasshopper (you)

Claude cannot open Rhino. We exchange **plain CSV / GeoJSON files** in this folder, and git keeps the history.

```
exchange/
  site_origin.json      local origin of the Rhino model (EPSG:25831 minus origin = Rhino coords, metres)
  to_gh/                files Claude prepares for Grasshopper (trees, boundary, buildings, trait table, candidate positions)
  from_gh/              files you export from Grasshopper (UTCI/MRT results, chosen layouts)
grasshopper/            your .gh definitions (commit them; screenshots welcome as .png)
```

## Rules
1. **Coordinates:** Rhino units = metres; local XY = EPSG:25831 − origin (`site_origin.json`: 430800, 4586800). Z = height above ground. Large raw UTM numbers cause precision problems in Rhino, which is why we use a local origin.
2. **Long format, one row per point × scenario × hour:** `scenario, hour, point_id, x, y, z, <metric>`. Scenario names: `S0_current`, `S1_like_for_like`, `S2_heat_opt`, `S3_runoff_opt`, `S4_pareto_<k>`.
3. **File names:** `<what>_<scenario>_<YYYYMMDD>.csv`, e.g. `utci_S0_current_20261012.csv`.
4. Put the Ladybug/EPW settings you used in `from_gh/run_log.md` (EPW file, hours, wind, ground albedo, tree transmittance), so the results can be reproduced.

## Current files in `to_gh/`
| File | Columns | Notes |
|---|---|---|
| `porta_boundary.csv` | x, y | Closed polyline of Porta |
| `porta_street_trees.csv` | tree_id, x, y, species, size_category, planting_date, street, is_plane | 2,825 street trees (open data, 1 Oct 2026) |
| `porta_trees_lidar.csv` | tree_id, x, y, ground_z, species, is_plane, size_category, street, height_m, crown_area_m2, crown_diam_m, crown_base_m, gap_fraction, lai_proxy, n_points, flag | Same trees + LiDAR metrics (ICGC, flown **26 Sept 2021, leaf-on**). Use only `flag == ok` (2,600 of 2,825); others have no detectable crown. Crown in GH: ellipsoid/sphere centred at (x, y, ground_z + (crown_base_m + height_m)/2), horizontal diameter crown_diam_m, vertical extent height_m − crown_base_m. `lai_proxy` = −ln(gap)/0.5 is **uncalibrated** |
| `porta_tree_interception_S0.csv` | tree_id, species, crown_diam_m, lai, x, y, interception_L_T{1,2,10}_60min, interception_L_T2_20min | Litres intercepted per tree per design storm (runoff module v1, s = 1.75 mm/LAI). Use it to colour the crowns in GH |
| `positions_tool_v0_<date>.csv` | tree_id, x, y, water_convergence_m2, drains_to_hotspot, sun_share, shade_m2h_<genus>, water_m3_<genus> | Tool v0 (`shade_sponge/`), one row per plane position (832). water_convergence_m2 = upstream open area (max within 2 m); drains_to_hotspot = share of the ground around it whose runoff reaches a flood hotspot within 100 m; sun_share = share of 12–17 h in sun past the buildings; then the shade and interception potential of each palette species there. Colour points by any column |
| `layouts_tool_v0_<date>.csv` | scenario, tree_id, x, y, ground_z, species, crown_diam_m, height_m, crown_base_m, lai | Plane positions only, long format: `S0_current`, `S1_random_0`, `S4_w0.0` … `S4_w1.0`. Filter by scenario, then build crowns with the ellipsoid snippet below (skip the `flag` check) |
| `porta_buildings.geojson` | geometry (local coords), height_m, ground_z, lidar_cover | 745 OSM footprints (© OpenStreetMap contributors, ODbL) extruded by LiDAR median roof height above ground. Read with GH Python `json`, extrude by height_m |

## Grasshopper Python: read a CSV of points (Rhino 8 Python 3 or Rhino 7 IronPython)
Inputs: `path` (str). Outputs: `pts`, `species`, `is_plane`.
```python
import csv
import Rhino.Geometry as rg
pts, species, is_plane = [], [], []
with open(path) as f:
    for r in csv.DictReader(f):
        pts.append(rg.Point3d(float(r["x"]), float(r["y"]), 0.0))
        species.append(r["species"])
        is_plane.append(r["is_plane"] == "True")
```

## Grasshopper Python: write UTCI results
Inputs: `path` (str), `points` (list of Point3d, the test points), `values` (list of floats, e.g. UTCI from *LB UTCI Comfort*), `scenario` (str), `hour` (str, e.g. "07-15 15:00"), `metric` (str, e.g. "utci_C"), `run` (bool).
```python
import csv, os
if run:
    new = not os.path.exists(path)
    with open(path, "a") as f:            # appends, so several scenarios/hours can go in one file
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["scenario", "hour", "point_id", "x", "y", "z", metric])
        for i, (p, v) in enumerate(zip(points, values)):
            w.writerow([scenario, hour, i, round(p.X, 2), round(p.Y, 2), round(p.Z, 2), round(float(v), 3)])
```

## Grasshopper Python: buildings (extruded footprints) from `porta_buildings.geojson`
Inputs: `path`. Outputs: `breps`, `heights`. (z = ground_z, absolute elevation in m)
```python
import json
import Rhino.Geometry as rg
breps, heights = [], []
gj = json.load(open(path))
for f in gj["features"]:
    g, p = f["geometry"], f["properties"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        z0 = p["ground_z"]
        crv = rg.PolylineCurve([rg.Point3d(x, y, z0) for x, y in poly[0]])
        ext = rg.Extrusion.Create(crv, p["height_m"], True)
        if ext:
            breps.append(ext.ToBrep()); heights.append(p["height_m"])
```

## Grasshopper Python: tree crowns (ellipsoids) from `porta_trees_lidar.csv`
Inputs: `path`. Outputs: `crowns`, `species`, `lai`.
```python
import csv
import Rhino.Geometry as rg
crowns, species, lai = [], [], []
for r in csv.DictReader(open(path)):
    if r["flag"] != "ok" or not r["crown_base_m"]:
        continue
    h, hb, d, z0 = float(r["height_m"]), float(r["crown_base_m"]), float(r["crown_diam_m"]), float(r["ground_z"])
    c = rg.Point3d(float(r["x"]), float(r["y"]), z0 + (h + hb) / 2.0)
    s = rg.Sphere(rg.Point3d.Origin, 1.0).ToBrep()
    s.Transform(rg.Transform.Scale(rg.Plane.WorldXY, d / 2.0, d / 2.0, max(h - hb, 1.0) / 2.0))
    s.Transform(rg.Transform.Translation(rg.Vector3d(c)))
    crowns.append(s); species.append(r["species"]); lai.append(float(r["lai_proxy"] or 0))
```
