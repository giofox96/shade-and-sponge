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
| `porta_street_trees.csv` | tree_id, x, y, species, size_category, planting_date, street, is_plane | 2,825 street trees (open data, 1 Oct 2026). Heights/crowns from LiDAR: next export |

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
