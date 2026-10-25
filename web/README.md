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

## Palettes and designer mode (9 Oct)
- **Palette switch** (header): the city palette, 7 species: the city's 6 named replacements + Styphnolobium (`data/porta/`) or the Barcelona shortlist of 34 species (`data/porta-barcelona/`, from `python -m shade_sponge porta --palette=barcelona` and `python -m shade_sponge.web_export porta --palette=barcelona`). With 34 species, crowns are coloured by leaf habit (hue: ochre deciduous, green evergreen, olive semi-deciduous) and crown size (lightness); the species is in the tooltip and the inspector.
- **Add trees** (left panel, Design): click open ground to place a tree. The browser computes its summer shade, winter shade, interception and façade fit for every palette species at that point (`src/pointpot.js`, a port of the Python formulas on `grid.bin.gz`: sun bits per design hour, ground flags, façade distance), recommends the best species for the current priorities, and adds it to the estimates and to live re-optimisation. Roofs, ground outside the site and points under 1 m from a building are refused; under 4 m from another tree gives a warning (ASSUMPTION). At the 832 plane positions the port matches the Python potentials with a median difference of 0.01% of each position's largest value (95% within ~2%). No sidewalk data yet: the designer decides where planting is possible.
- **Download CSV** gives the added trees in Grasshopper local coordinates (`exchange/README.md`).

## Live optimisation (9 Oct)
Click anywhere inside the priority triangle (dots = precomputed exact layouts), change the max share per species, or untick species: the browser re-solves the same transportation LP as `shade_sponge/layout.py` with HiGHS (WebAssembly, `highs` npm package) on `potentials.json`, in ~0.1–0.3 s.
- **Check against Python:** for 4 weight sets the browser layout matches the saved Python layout at 827–832 of 832 positions, with the same species counts (one tree different in one set); the difference comes from the rounded potentials in the export.
- **Results are estimates (marked ≈):** summed single-tree potentials (no crown overlaps), calibrated by a straight line on the 16 saved palette layouts; the R² of each line is shown in the results panel. Exact scores need a run of the Python tool.

## Look (25 Oct): the deck's palette and fonts
Same "Earth" palette and fonts as the slides (`scripts/make_infographics.py`, `slides/palette_board.html` option C), as CSS tokens in `src/style.css`. Fonts: IBM Plex Sans for text, IBM Plex Mono for labels and numbers. Colours carry the deck's meaning: moss = trees and the decision (buttons, selection, optimised layouts), ochre = sun and shade, ink blue = water and runoff, rust = heat and warnings. The header is the dark green of the title slides.
- **Species colours (city palette):** seven earth tones in a fixed order (moss, ink blue, ochre, rose, olive, plum, rust; `shade_sponge/web_export.py`). Adjacent slots pass the colour-vision-deficiency check and every colour has ≥ 3:1 contrast on the page background. All 21 pairs together cannot pass with 7 hues, so species are also named in the legend, the tooltip and the inspector.
- **Overlays:** one-hue ramps, stone → ochre for sun, bone → ink blue for water convergence, bone → rust for hotspots. The committed PNGs and `meta.json` colours were remapped in place (exact colour-map lookup); the next `web_export` run writes the same colours.
