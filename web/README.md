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

## Data (`web/public/data/<site>/`, from `shade_sponge/web_export.py`)
`meta.json` (palette with leaf calendars and sources, scenarios with metrics, sensitivity, overlays) · `trees.json` (plane positions, kept trees, species per position for each saved layout) · `potentials.json` (per-position shade and interception potentials + façade fit, for live optimisation) · `buildings.geojson` · overlay PNGs (winter sun, summer sun, water convergence, flood hotspots). The map is flat: heights are metres above local ground.

## Status
Read-only (9 Oct): the triangle points are the 15 precomputed optimised layouts. Next: live re-optimisation in the browser (HiGHS WebAssembly) from `potentials.json`, with results labelled as estimates.
