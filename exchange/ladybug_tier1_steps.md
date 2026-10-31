# Ladybug Tier 1 test, step by step (Pg Andreu Nin, S0 vs tool layout)

What it gives: mean UTCI 12–17 h on 15 July at 1,974 points along Pg Andreu Nin. Run 1 uses today's planes (S0); run 2 uses the tool's layout on the same 80 positions (S4). Everything else stays the same. Method: `notes/methodology.md` §1 (Tier 1). Window: `notes/decisions/heat_objective.md`.
Time: about 1 h the first time, then a few minutes per run.

## 0. Before you start
- `git pull` in the project folder. The files are in `exchange/to_gh/`, named `street_andreu-nin_*_20261031.*`.
- Rhino 8 (or 7) with Ladybug Tools 1.x installed.
- The EPW: TMYx El Prat 2011–2025, the same file as `scripts/heat_bounds.py`. If you don't have it locally, drag *LB Download Weather* onto the canvas and give it the climate.onebuilding.org URL of that file.
- Create the folder `exchange/from_gh/` if it doesn't exist: the writer in step 4 doesn't create it.
- Units: metres. All files are in local coordinates (see the top of `exchange/README.md`), and z is absolute elevation, so nothing needs moving.

## 1. Geometry (three GH Python components)
Create a GhPython component for each snippet below. Set `path` to the full file path (a Panel works), and use item access for every input.

**1a. Buildings:** the "buildings" snippet in `exchange/README.md`, on `street_andreu-nin_buildings_20261031.geojson`. Output `breps`.

**1b. Context trees:** the "tree crowns" snippet in `exchange/README.md`, on `street_andreu-nin_context_trees_20261031.csv`. Output `crowns`.

**1c. Street trees:** this variant. The S0 and S4 files have no `flag` column and use `lai`. Start with path = `street_andreu-nin_trees_S0_current_20261031.csv`.
```python
import csv
import Rhino.Geometry as rg
crowns, species = [], []
for r in csv.DictReader(open(path)):
    h, hb, d, z0 = float(r["height_m"]), float(r["crown_base_m"]), float(r["crown_diam_m"]), float(r["ground_z"])
    c = rg.Point3d(float(r["x"]), float(r["y"]), z0 + (h + hb) / 2.0)
    s = rg.Sphere(rg.Point3d.Origin, 1.0).ToBrep()
    s.Transform(rg.Transform.Scale(rg.Plane.WorldXY, d / 2.0, d / 2.0, max(h - hb, 1.0) / 2.0))
    s.Transform(rg.Transform.Translation(rg.Vector3d(c)))
    crowns.append(s); species.append(r["species"])
```

**1d. Test points:** on `street_andreu-nin_testpoints_20261031.csv`. Output `pts`.
```python
import csv
import Rhino.Geometry as rg
pts = [rg.Point3d(float(r["x"]), float(r["y"]), float(r["z"])) for r in csv.DictReader(open(path))]
```
Check: 30 buildings, 87 context crowns, 80 street crowns and 1,974 points, all overlapping in the Rhino view.

**1e. Context:** *Merge* the three outputs `breps` + context `crowns` + street `crowns` into one list. This is the shade context.

## 2. Weather, 15 July, 12–17 h local time
1. *LB Import EPW*, with `_epw_file` set to the El Prat TMYx file.
2. *LB Analysis Period*: start month 7, day 15, hour **11**; end month 7, day 15, hour **16**. The EPW is in standard time, so EPW hours 11–16 = 12–17 h summer time, the decided window.
3. One *LB Apply Analysis Period* for each of the six outputs: dry_bulb_temperature, relative_humidity, wind_speed, direct_normal_rad, diffuse_horizontal_rad, horizontal_infrared_rad. Plug in the period from step 2.

## 3. MRT and UTCI
1. *LB Human to Sky Relation*:
   - `_location` from *LB Import EPW*;
   - `_position` = the test points `pts`;
   - `_context` = the merged context from 1e;
   - `_cpu_count_` empty (uses all cores);
   - `_run` = True.

   Outputs: `fract_body_exp`, `sky_exposure`. This is the slow step.
2. *LB Outdoor Solar MRT*:
   - `_location`;
   - `_surface_temp` = filtered dry bulb;
   - `_dir_norm_rad`, `_diff_horiz_rad` and `_horiz_infrared` = the filtered radiation streams;
   - `_fract_body_exp_` and `_sky_exposure_` from step 1;
   - `_ground_ref_` = 0.25;
   - `_run` = True.

   Output `mrt`.
3. *LB UTCI Comfort*:
   - `_air_temp` = filtered dry bulb;
   - `_mrt_` = `mrt`;
   - `_rel_humid` = filtered relative humidity;
   - `_wind_vel_` = filtered wind speed (10 m wind as is, as in the bounding run).

   Output `utci`: one data collection per point, with 6 hours.

Check: values should sit roughly in the 30–40 °C range. Sunlit points should be clearly hotter than points under crowns.

## 4. Save, then repeat with the tool layout
GhPython writer. Inputs:
- `path` (item);
- `points` = `pts` (list access);
- `utci` (list access);
- `scenario` (item);
- `run` (Boolean Toggle).
```python
import csv, os
if run:
    new = not os.path.exists(path)
    with open(path, "a") as f:
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["scenario", "hour", "point_id", "x", "y", "z", "utci_C"])
        for i, (p, dc) in enumerate(zip(points, utci)):
            for dt, v in zip(dc.datetimes, dc.values):
                w.writerow([scenario, str(dt), i, round(p.X, 2), round(p.Y, 2), round(p.Z, 2), round(float(v), 3)])
```
1. Set path = `exchange/from_gh/utci_S0_current_<date>.csv` and scenario = `S0_current`. Toggle `run` once, then set it back to False.
2. In 1c, change the path to `street_andreu-nin_trees_S4_s1.00_w0.00_r0.00_20261031.csv`. Ladybug recomputes.
3. Set path = `exchange/from_gh/utci_S4_s1.00_w0.00_r0.00_<date>.csv` and scenario = `S4_s1.00_w0.00_r0.00`, then toggle `run` once.
4. In `exchange/from_gh/run_log.md`, write: EPW file name, period, ground reflectance 0.25, wind as is, crowns opaque, Ladybug version, run time. Then commit and push, or tell me and I do it from the PC.

I then compute mean UTCI 12–17 h per scenario and the S4 − S0 difference per point. The difference counts only if it exceeds the Ladybug-vs-ENVI-met error, 0.8–2.3 °C (`heat_objective.md`).

## Known limits of this first run (state them, don't fix them now)
- **Opaque crowns.** Species differ here only by crown size and shape, not by leaf density. The τ = exp(−0.5·LAI) correction (Peng et al. 2026) is the next step (`methodology.md` §1).
- **No transpiration cooling.** Ladybug likely underestimates the cooling by about 2–3 °C UTCI (Mannucci et al. 2025).
- **Airport weather.** The EPW is from El Prat, not from Porta.
- **The date.** 15 July is an ASSUMPTION shared with the tool's shade proxy.

If a component's inputs or outputs look different from what is written here (Ladybug versions change), send me a screenshot of the canvas.
