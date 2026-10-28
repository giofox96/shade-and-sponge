# Shade and sponge: web app

Browse the street-tree layouts of the tool (`shade_sponge/`) on a 3D map: priorities triangle, results against the current trees and a random palette, trade-off chart, and a per-tree inspector that shows what each palette species would deliver at that position.

**Stack:** Vue 3 + Vite · MapLibre GL (OpenFreeMap basemap, no key) · deck.gl (buildings, tree crowns as ellipsoids, raster overlays) · ECharts. Static site: no server.

## Run
```bash
python -m shade_sponge porta --size=exact --trunk=TERCERA             # tool run in the thesis configuration (from the repo root)
python -m shade_sponge.web_export porta --size=exact --trunk=TERCERA  # writes web/public/data/porta/
cd web && npm install && npm run dev
```
The published data use the **thesis configuration** (since 26 Oct): the exact sidewalk sizing rule and species traits at equal trunk size (TERCERA), with the city rule (S1a, the 2026 mix) as the comparison column. Without the two options you get the default run (no sizing rule, traits from all trunk sizes). For the Barcelona shortlist add `--palette=barcelona` to both commands. The header switch **≈ 10 years | Established** loads `data/porta-segona/` (`--trunk=SEGONA`, the second trunk class, a median of 9.7 years after planting) or `data/porta/` (`--trunk=TERCERA`); city palette only.
`npm run build` writes a static site to `web/dist/` (relative paths, so it can be hosted anywhere).

**Online:** https://giofox96.github.io/shade-and-sponge/ — `.github/workflows/pages.yml` rebuilds and publishes `web/dist` to the `gh-pages` branch whenever `web/` changes on `main` or `claude/web-ui`. Data credits are in the app's left panel (Data and sources).

## Data (`web/public/data/<site>/`, from `shade_sponge/web_export.py`)
`meta.json` (palette with leaf calendars and sources, scenarios with metrics, sensitivity, overlays) · `trees.json` (plane positions, kept trees, species per position for each saved layout) · `potentials.json` (per-position shade and interception potentials + façade fit, for live optimisation) · `buildings.geojson` · overlay PNGs (winter sun, summer sun, water convergence, flood hotspots). The map is flat: heights are metres above local ground.

## Project area (28 Oct)
Trees are not replaced all at once. A plane is replaced when it dies, when it is unsafe, or when a street project rebuilds the ground. **Project area** (left panel) lets the designer draw that place:
1. **Draw area:** click the corners on the map (clicks on trees count too, and double-click zoom is off while drawing), then **Finish**.
2. **What is replaced:** only the plane positions inside the polygon. Today's trees stay everywhere else.
3. **Optimisation:** the same LP as the live optimiser, restricted to those positions, with the current weights, cap, excluded species and diversity floor. Clicking the triangle or a dot re-optimises the area.
4. **The comparison** inside the area:
   - **today:** the measured planes;
   - **city rule:** the expected value of the 2026 mix within the sizing rule. Capped species are scaled down to their room, as in the exact S1a draws;
   - **optimised.**

   The results panel ("vs city rule") and the Compare view use the area.
5. **Back to the whole district:** the **Whole site** button.

**How the estimate works:** today's exact metrics + calibration slope × Σ (potential of the new species − potential of today's plane) over the area.
- **Today's planes** are scored in the browser, from their measured crown and the plane's median LAI (`ASSUMPTION`). Their potentials are rescaled per metric, so that the calibration line, fed with all 832 planes, returns today's exact value.
- **Checked on 28 Oct:** an area covering 752 of the 832 positions gives 352,534 / 207,760 m²·h and 17,691 m³. The exact full replacement gives 353,075 / 209,485 m²·h and 17,688 m³.
- **Not estimated:** canopy cover. Added trees are counted on top, as elsewhere.

## Compare side by side (28 Oct)
The **Compare side by side** button (left panel, Layout) replaces the 3D map with three columns: **today | city rule | optimised**. The optimised column is the selected or live layout, otherwise the balanced one.
- **Mini-map:** each column draws every crown to scale. Plane positions are coloured by species, today's planes are dark, kept trees are light grey.
- **Metrics:** summer and winter shade, hotspot and total runoff, and canopy cover, each against today. Canopy cover is shown in percentage points.
- **Species mix** of the replanted positions.
- **City-rule column:** the metrics are the mean of its 10 draws; the map and mix show draw #0.
- **Stage:** the "≈ 10 years | Established" switch applies to all three columns.
- **Layout:** the three columns sit side by side from about 1,300 px of window width and stack on narrower screens.
- **Canopy cover** is a new exported metric (`canopy_pct`). Live layouts show no canopy value.

## Palettes and designer mode (9 Oct)
- **Palette switch** (header): the city palette, 7 species: the city's 6 named replacements + Styphnolobium (`data/porta/`) or the Barcelona shortlist of 34 species (`data/porta-barcelona/`, from `python -m shade_sponge porta --palette=barcelona` and `python -m shade_sponge.web_export porta --palette=barcelona`). With 34 species, crowns are coloured by leaf habit (hue) and crown size (lightness); the species is in the tooltip and the inspector.
- **Add trees** (left panel, Design): click open ground to place a tree. The browser computes its summer shade, winter shade, interception and façade fit for every palette species at that point (`src/pointpot.js`, a port of the Python formulas on `grid.bin.gz`: sun bits per design hour, ground flags, façade distance), recommends the best species for the current priorities, and adds it to the estimates and to live re-optimisation. Roofs, ground outside the site and points under 1 m from a building are refused; under 4 m from another tree gives a warning (ASSUMPTION). At the 832 plane positions the port matches the Python potentials with a median difference of 0.01% of each position's largest value (95% within ~2%). No sidewalk data yet: the designer decides where planting is possible.
- **Download CSV** gives the added trees in Grasshopper local coordinates (`exchange/README.md`).

## Live optimisation (9 Oct)
Click anywhere inside the priority triangle (dots = precomputed exact layouts), change the max share per species, or untick species: the browser re-solves the same transportation LP as `shade_sponge/layout.py` with HiGHS (WebAssembly, `highs` npm package) on `potentials.json`, in ~0.1–0.3 s.
- **Check against Python:** for 4 weight sets the browser layout matches the saved Python layout at 827–832 of 832 positions, with the same species counts (one tree different in one set); the difference comes from the rounded potentials in the export.
- **Results are estimates (marked ≈):** summed single-tree potentials (no crown overlaps), calibrated by a straight line on the 16 saved palette layouts; the R² of each line is shown in the results panel. Exact scores need a run of the Python tool.
