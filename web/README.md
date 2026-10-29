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

## Layout (28 Oct cleanup)
- **Header:** the site, and two labelled switches: **Palette** (city 7 / Barcelona 34) and **New trees at** (≈ 10 years / established).
- **Left panel**, in working order:
  1. **Scenario:** today, city rule, optimised, project area, random, plus the priority triangle.
  2. **Project area:** draw, replace all, fill spots.
  3. **Add trees.**

  Collapsed groups: **Rules and species** (cap, diversity floor, excluded species), **Map display** (sidewalks, overlay, month) and **Data and sources**. Each closed group shows its current setting in its title. Longer explanations are under *How it works*.
- **Map | Compare side by side:** tabs over the main view.
- **Right panel:** canopy cover, results (with the scenario's description), trade-off (collapsible) and the selected tree.
- **Map defaults:** no overlay, so the sidewalks and free spots read clearly. The sun and water layers are under Map display.
- **Narrow screens:** the map comes first, then the controls, then the results.
- **Side panels:** drag the inner edge of either panel to resize it (200–520 px; arrow keys on the focused edge). The ‹ / › button on the edge hides or shows it. Widths and open state are remembered in the browser.
- **Project-area outline** (29 Oct): the outline and the corners being drawn are drawn over buildings and crowns (no depth test), so they stay visible behind tall blocks. **Buildings slider** in Map display: building opacity, 0–100% (below 100% the buildings stop hiding the crowns behind them).
- **Cursor:** the map shows a crosshair while drawing a project area or adding trees, and the hand otherwise.
- **Look:** the slide deck's "Earth" palette and fonts (`scripts/make_infographics.py`):
  - **colours:** ink, moss = trees, ink blue = rain / accent, rust = heat / worse, ochre = warnings, title-slide green = header;
  - **fonts:** IBM Plex Sans and Plex Mono, from Google Fonts.

  All colours are CSS tokens in `src/style.css`. The map and the chart, which cannot read CSS, take theirs from `themeColors` in `store.js`.
- **Dark mode:** **Auto | Light | Dark** in the header. Auto follows the system, and the choice is remembered. The basemap switches between OpenFreeMap Positron (light) and CARTO Dark Matter (dark), and buildings, sidewalks, tree outlines and the chart follow the theme.

## Species cards (29 Oct)
The **Species** tab (next to Map and Compare) shows one botanical card per species of the palette on screen:
- a **photo** from Wikimedia Commons, free licences only (CC0, public domain, CC BY, CC BY-SA), with author and licence on the photo. `scripts/fetch_species_photos.py` (run on the PC: Wikimedia is not reachable from the cloud) writes `public/species/<slug>.jpg` and `photos.json`; `FILE` in the script replaces a lead image that is not the whole tree (`--candidates` lists options);
- a **profile drawing** to one scale on every card (height, crown width, clear trunk, a 1.7 m person);
- **icons** for height, crown width, clear trunk (crown base), trunk diameter (from the trunk class: perimeter / π, 2011 guide p. 18), LAI (LiDAR proxy, five pips relative to the palette's largest), sidewalk size class, the 15% cap, and the leaf calendar;
- how many positions of the layout on screen get the species (sortable).

All values come from `meta.json → palette`: no new parameters.

**Summary (29 Oct):** above the cards, the street trees of the layout on screen (`src/speciesview.js`): today's trees with their own LiDAR crown, height and LAI, new and added trees with the palette medians. Drawing a project area switches the tab to the area (a toggle goes back to the whole neighbourhood); a "replace all" area counts the replaced trees with their new species.
- **Tiles:** trees, species, effective species (exp Shannon H), the largest species' share (red above the plan's 15% in the neighbourhood view), share evergreen, mean height, crown width and LAI, crown disc area.
- **Species mix:** ranked bars (top 10 + other) with the 15% cap as a dashed line; a donut would not read with 50 species.
- **Donuts:** leaf habit (palette text, or the leaf calendar for today's other species), crown width (< 4.5 / 4.5–7 / > 7 m, the Barcelona palette classes), today's vs new vs added trees.
- Trees without a matched LiDAR crown (`flag != ok`, 202 of 2,825 in Porta) are not counted.

## Canopy cover counter (28 Oct)
The top of the right panel shows the **canopy cover** of the layout on screen against the plan's **30% target**:
- **Today:** the measured 20.1% (LiDAR CHM > 2 m).
- **Precomputed layouts:** today plus the change of the disc model (exact, overlaps included).
- **Live layouts, project areas and added trees:** today plus their crown discs summed without overlaps (marked ≈, runs high). Each added tree updates the counter.
- **Gap:** the points and hectares left to the target.
- **For scale** (city palette, established): what planting all 232 free street spots would add (after the OSM exclusions; re-run 28 Oct).

The data are in `meta.json → cover`, from `databases/barcelona/porta_canopy_cover.csv` and `additions_summary.csv`.

## Project area (28 Oct)
Trees are not replaced all at once. A plane is replaced when it dies, when it is unsafe, or when a street project rebuilds the ground. **Project area** (left panel) lets the designer draw that place:
1. **Draw area:** click the corners on the map (clicks on trees count too, and double-click zoom is off while drawing), then **Finish**, a right click (without dragging), Enter or Space. Escape cancels. **Edit area** (toggle) moves the corners: drag a corner, click a midpoint to add one, right-click a corner to remove it; **Done** or Enter applies (the "replace all" choice and the priorities are kept), Escape cancels.
2. **What is replaced:** only the plane positions inside the polygon. Today's trees stay everywhere else.
3. **Optimisation:** the same LP as the live optimiser, restricted to those positions, with the current weights, cap, excluded species and diversity floor. Clicking the triangle or a dot re-optimises the area.
4. **The comparison** inside the area:
   - **today:** the measured planes;
   - **city rule:** the expected value of the 2026 mix within the sizing rule. Capped species are scaled down to their room, as in the exact S1a draws;
   - **optimised.**

   The results panel ("vs city rule") and the Compare view use the area.
5. **Back to the whole district:** the **Whole site** button.
6. **Replace all trees in the area** (checkbox): the other street trees inside become decision positions too, as in a street rebuild that removes the whole stretch.
   - They are scored in the browser at their position with the sizing rule of their sidewalk (`porta_sidewalk_width.csv`).
   - Today's version uses their LiDAR crown, LAI and leaf calendar.
   - The cap gains the room their species free up.
   - New trees are scored at the selected stage, so replacing young trees looks like a gain that takes years to arrive. The panel says so.
7. **Fill the free spots:** every free planting spot inside the area (`porta_planting_spots.csv`, an upper bound) becomes an added tree with its sidewalk's size class. The optimiser then chooses its species together with the area.

**Sidewalks on the map** (Map layer → *Sidewalk edges and free planting spots*, on by default):
- façade lines (brown) and kerb lines (dark) from the 1:1000 base map, so the sidewalk is the band between them;
- the 232 free spots as green dots (267 minus those near crossings, signals, parking entrances and bus stops; `scripts/porta_spot_exclusions.py`) (light to dark = small / medium / large). In *Add trees* mode, a click on a spot plants there.

Built by `web_export.py` from the cached WMS tiles (`sidewalks.geojson`).

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
- **Palette switch** (header): the city palette, 7 species: the city's 6 named replacements + Styphnolobium (`data/porta/`) or the Barcelona shortlist of 34 species (`data/porta-barcelona/`, from `python -m shade_sponge porta --palette=barcelona` and `python -m shade_sponge.web_export porta --palette=barcelona`). With 34 species, crowns are coloured by leaf habit (hue: ochre deciduous, green evergreen, olive semi-deciduous) and crown size (lightness); the species is in the tooltip and the inspector.
- **Add trees** (left panel, Design): click open ground to place a tree. The browser computes its summer shade, winter shade, interception and façade fit for every palette species at that point (`src/pointpot.js`, a port of the Python formulas on `grid.bin.gz`: sun bits per design hour, ground flags, façade distance), recommends the best species for the current priorities, and adds it to the estimates and to live re-optimisation. Roofs, ground outside the site and points under 1 m from a building are refused; under 4 m from another tree gives a warning (ASSUMPTION). While the mode is on, the map shades the same rules on the 1 m grid (`addableMask()` in `store.js`): green = accepted, amber = accepted with a warning (under 2 m from a building or 4 m from a tree). With a project area, trees can be added only inside it. A refused click, or one accepted with a warning, shows the reason next to the cursor. Added trees keep a ring drawn on top and a trunk line, so they stay visible inside other crowns or behind buildings. At the 832 plane positions the port matches the Python potentials with a median difference of 0.01% of each position's largest value (95% within ~2%). No sidewalk data yet: the designer decides where planting is possible.
- **Download CSV** gives the added trees in Grasshopper local coordinates (`exchange/README.md`).

## Live optimisation (9 Oct)
Click anywhere inside the priority triangle (dots = precomputed exact layouts), change the max share per species, or untick species: the browser re-solves the same transportation LP as `shade_sponge/layout.py` with HiGHS (WebAssembly, `highs` npm package) on `potentials.json`, in ~0.1–0.3 s.
- **Check against Python:** for 4 weight sets the browser layout matches the saved Python layout at 827–832 of 832 positions, with the same species counts (one tree different in one set); the difference comes from the rounded potentials in the export.
- **Results are estimates (marked ≈):** summed single-tree potentials (no crown overlaps), calibrated by a straight line on the 16 saved palette layouts; the R² of each line is shown in the results panel. Exact scores need a run of the Python tool.

## Species colours, overlays and the neighbourhood picker (25–28 Oct)
The UI look is described under "Layout" above. On top of it:
- **Species colours (city palette):** seven earth tones in a fixed order: moss, ink blue, ochre, rose, olive, plum, rust (`shade_sponge/web_export.py`).
  - In light mode, adjacent slots pass the colour-vision-deficiency check, and every colour has ≥ 3:1 contrast.
  - In dark mode they also pass the colour-vision check, but ink blue, rose and plum fall to 2.5–2.7:1 on the dark map.
  - All 21 pairs together cannot pass with 7 hues. So species are also named in the legend, the tooltip and the inspector.
- **Barcelona palette:** colour = leaf habit (ochre deciduous, green evergreen, olive semi-deciduous); darker = larger crown.
- **Overlays:** one-hue ramps:
  - sun: stone → ochre;
  - water convergence: bone → ink blue;
  - hotspots: bone → rust.

  The committed PNGs and `meta.json` colours were remapped in place, by an exact colour-map lookup, for all three datasets. The next `web_export` run writes the same colours.
- **Neighbourhood picker** (left panel, `src/components/BarriPicker.vue`): a mini-map of the 73 barris plus a dropdown grouped by district.
  - Only barris with exported data open on the map (Porta for now); the others show their plane count and "not computed yet".
  - The outlines come from `scripts/make_barris_web.py` → `public/data/barris.geojson`. Since 28 Oct they are the official Open Data BCN boundaries (CC BY 4.0); without that file the script falls back to OSM.
