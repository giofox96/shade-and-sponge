# Shade and sponge: web app

Browse the street-tree layouts of the tool (`shade_sponge/`) on a 3D map: priorities triangle, results against the current trees and a random palette, trade-off chart, and a per-tree inspector that shows what each palette species would deliver at that position.

**Stack:** Vue 3 + Vite · MapLibre GL (OpenFreeMap basemap, no key) · deck.gl (buildings, tree crowns as ellipsoids, raster overlays) · ECharts. Static site: no server.

## Run
```bash
python -m shade_sponge             # tool run (layouts + metrics), from the repo root
python -m shade_sponge.web_export  # writes web/public/data/porta/
cd web && npm install && npm run dev
```
`npm run build` writes a static site to `web/dist/` (relative paths, so it can be hosted anywhere).

**Online:** https://giofox96.github.io/shade-and-sponge/ — `.github/workflows/pages.yml` rebuilds and publishes `web/dist` to the `gh-pages` branch whenever `web/` changes on `main` or `claude/web-ui`. Data credits are in the app's left panel (Data and sources).

## Data (`web/public/data/<site>/`, from `shade_sponge/web_export.py`)
`meta.json` (palette with leaf calendars and sources, scenarios with metrics, sensitivity, overlays) · `trees.json` (plane positions, kept trees, species per position for each saved layout) · `potentials.json` (per-position shade and interception potentials + façade fit, for live optimisation) · `buildings.geojson` · overlay PNGs (winter sun, summer sun, water convergence, flood hotspots). The map is flat: heights are metres above local ground.

## Live optimisation (9 Oct)
Click anywhere inside the priority triangle (dots = precomputed exact layouts), change the max share per species, or untick species: the browser re-solves the same transportation LP as `shade_sponge/layout.py` with HiGHS (WebAssembly, `highs` npm package) on `potentials.json`, in ~0.1–0.3 s.
- **Check against Python:** for 4 weight sets the browser layout matches the saved Python layout at 827–832 of 832 positions, with the same species counts (one tree different in one set); the difference comes from the rounded potentials in the export.
- **Results are estimates (marked ≈):** summed single-tree potentials (no crown overlaps), calibrated by a straight line on the 16 saved palette layouts; the R² of each line is shown in the results panel. Exact scores need a run of the Python tool.
