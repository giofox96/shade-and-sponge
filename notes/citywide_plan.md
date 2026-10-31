# From Porta to the whole city: feasibility and plan (24 Oct 2026)

User, 24 Oct:
- start from Porta but aim at the whole of Barcelona;
- run the scenarios as discussed, with additions **co-equal** in the RQ;
- add a tree-health map, so that replacement targets the trees likely to go first;
- let the tool pick a **project area** and replace only the trees inside it.

## 1. Verdict: feasible, if "city-wide" means coverage, not one city-wide optimisation

Optimising all ~43,700 planes at once is not needed, and it would not be realistic. The city replaces trees one at a time, as they die or when a street is rebuilt (§9.7.3 of `notes/topic_decision.md`). The model that fits that reality has two layers:

| Layer | What it is | Scale |
|---|---|---|
| **City screening** | Precomputed indicators for every street-tree position: crown and LAI (LiDAR), heat potential (effective shade), water convergence and distance to flood hotspots, sidewalk size class, health/priority proxy | Whole city, computed once, in batches by district |
| **Project tool** | The user draws a project area anywhere in the city. The tool takes the trees inside it (replacement) and the free spots (additions), and optimises them within the city's rules | One area at a time, seconds to minutes |

**City scale also improves the method.** At city scale the 15% cap becomes the plan's real rule, city-wide headroom, instead of the Porta-local reading that is now an `ASSUMPTION`. And the project area answers "the method must work for any subset of positions".

## 2. Data, input by input

| Input | City-wide? | Note / risk |
|---|---|---|
| Street-tree inventory (species, position, trunk class, planting date) | ✅ Open Data BCN, CC BY 4.0, 140,404 street trees | Already in the repo |
| LiDAR (ICGC, CHM, crowns, buildings) | ✅ open, but **mixed flights**: Porta's tile mixes 2021-09-26 and 2022-06-01; tiles 427583 and 428583 are 2022-06-01 only (`databases/barcelona/lidar_tiles_dates.csv`) | Both dates are leaf-on for the palette (phenology table), so usable. The flight date is recorded per tile. About 100 tiles of 1 km² for the city: hours of batch processing, not days |
| Sidewalk width | ⚠️ the hardest input | For Porta it was read in pieces from the 1:1000 WMS. City-wide that is slow. Look for an open sidewalk-polygon or street-section dataset first. Fallback: compute width only inside the chosen project area, on demand |
| DTM + flow routing | ✅ LiDAR DTM | City-wide 1 m routing is 10⁸ cells: tile by catchment, or use 2 m |
| Flood hotspots | ✅ Resilience Atlas (city-wide) and RESCCUE T10/T100 depths (city-wide) | Licence still open (`notes/todo_manual.md`) |
| Surfaces / CN | ✅ the same sources as Porta, city-wide | Runoff v1 was built for Porta; generalise its site bundle |
| Heat proxy | ✅ sun vectors × buildings × crowns | Ladybug UTCI only on project areas (Tier 1) |
| **Tree health** | ❌ **no official open dataset** | See §3 |

## 3. Tree health: a proxy, clearly labelled

No condition field is published (Open Data BCN inventory). iArbol (Starlab) estimates risk from satellite indices, but it is a third-party service and not open. Three proxies we can build ourselves, combined into a **replacement-priority score** (`ASSUMPTION`, to be checked against the Parcs i Jardins reply):
1. **Crown vigour from LiDAR:** crown area and gap fraction compared with same-species trees in the same trunk class. A small or open crown for its size suggests decline or heavy pruning.
2. **Spectral change (Sentinel-2 or the city NDVI 2017):** summer NDVI decline per crown, 2017 → recent.
3. **Age and size:** trunk class and planting date. The oldest planes are the first candidates. This mirrors the 2004 rule's priority order: dead, then declining, then street works (`notes/tree_master_plan.md` §5b).

How the score is used: it ranks which trees are replaced first. The optimiser then chooses species for the top-ranked set, or for a project area. **Validation:** the trees removed between two inventory snapshots (Open Data BCN publishes quarterly versions) should have had higher scores. That is a cheap, honest test.

## 4. Plan (8 weeks to 18 Dec)

| When | Step | Done when |
|---|---|---|
| to 10 Nov | **Porta first results:** S1a built, crowns at equal trunk size, replacement vs additions vs both on the proxy; project-area selection in Porta (polygon → subset); health proxy v0 (LiDAR vigour + trunk class) | Radar + bars for the 4 scenarios; one map of priority scores |
| 10–17 Nov | **City data check:** the LiDAR tile list and dates for the whole city, a sidewalk-width source, the inventory snapshots for the health validation | A go/no-go table per input |
| 17 Nov – 1 Dec | **City screening layer:** batch per district; per-position indicators to `web/public/data/barcelona/` | City map of indicators online; Porta values identical to the Porta run (regression check) |
| 1–8 Dec | **Project tool anywhere:** draw an area → replacement + additions → optimise with city-wide cap headroom | Demo on Porta plus one area in another district (Sant Antoni, the flood-dominant contrast site) |
| 8–18 Dec | Validation write-up, booklet, final deck | — |

**Validation stays on Porta.** The full chain is validated there: interception calibration, Ladybug Tier 1 vs proxy, the health-score test. A second district in the same city (Sant Antoni) becomes the within-city transfer test. It is cheaper than Florence and uses identical data. Florence/Mataró become "future work: other cities".

## 5. Risks

- **Sidewalk width city-wide** is the critical input. If no dataset exists, compute it per project area only. The screening layer then shows "size class unknown" outside measured areas.
- **Time:** the city layer is engineering, not new method. If it slips, the thesis still stands on Porta plus the project tool, with the city layer as a working prototype.
- **Runoff city-wide:** the runoff model was calibrated and checked on Porta only. Outside Porta it is labelled indicative.

## 6. How to cover all 73 barris (proposal, 25 Oct)

User, 25 Oct: start working out how to bring every Barcelona neighbourhood into the tool. This section is a proposal, not a decision.

### 6.1 Three units, one per job

| Unit | Used for | Why |
|---|---|---|
| **1 km LiDAR tile** (ICGC) | crowns, DTM, CHM, building heights | The data comes in tiles. `scripts/bcn_lidar_species.py` already processes whole tiles and every inventory tree in them |
| **Barri + 150 m buffer** | the site bundle (grid, surfaces, routing, sun) and the tool run | Same code as Porta, one barri at a time. The buffer makes the in-barri objectives exact (§6.2 step 3) |
| **City** | the 15% cap, species traits, the screening map | The cap is a city-wide rule (`notes/tree_master_plan.md`); the Porta-local cap is only an `ASSUMPTION` |

### 6.2 Pipeline, step by step (what changes in the code)

1. **Tile index.** From the barri boundaries (`BarcelonaCiutat_Barris.csv`), list the 1 km tiles that touch each barri plus 150 m. Record each tile's flight date from the GPS time, as `bcn_lidar_species.py` already does (`lidar_tiles_dates.csv`). Flag any tile flown leaf-off.
2. **LiDAR per tile, once.** Generalise `bcn_lidar_species.py`: 0.5 m DTM/CHM/building rasters and per-tree crowns for every street tree in the tile. Read a 30 m margin from the neighbouring tiles, as `bcn_lidar_porta.py` does (`BUF = 30`), so crowns on tile edges are complete. Output: one crown table for the whole city, keyed by inventory `codi`.
3. **Site bundle per barri.** Turn `site.build_porta()` / `trees_porta()` into `build_barri(name)` / `trees_barri(name)` (cache `cache/site_<slug>.npz`). The grid covers the barri plus 150 m, and the domain stays the barri polygon. The 150 m covers two things:
   - Winter building shadows: at the lowest winter design sun (15°), a 40 m building casts a 149 m shadow.
   - The 100 m flow path of `CAPTURE_M`: a cell's route to a hotspot stays inside the grid.

   So summer shade, winter shade and hotspot runoff inside the barri do not depend on where the barri is cut. Upstream water convergence (`acc`) does depend on the cut, but it is a display layer, not an objective. Inputs are city-wide already: Resilience Atlas hazard, NDVI 2017, OSM buildings and green areas.
4. **Sidewalk widths and free spots**: the critical input. Three options, in order:
   - (a) On your machine, retry the 652 MB 1:1000 GeoPackage once (`notes/sidewalk_width.md`). Then `porta_sidewalk_width.py` and `porta_planting_spots.py` run offline for the whole city.
   - (b) WMS tiles barri by barri, as for Porta. This is slow but proven.
   - (c) Compute widths only inside a project area. Elsewhere the screening map shows "size class unknown".
5. **Tool run per barri.** Run R, A and R+A with `--size=exact --trunk=TERCERA` (25 Oct options). The species traits come from the city-wide crown table at equal trunk size (more trees per species × trunk class than Porta alone).
6. **City-wide cap: one LP for the whole city** (recommended). The per-position potentials (shade × 2, water) are already computed per barri. Stack them and solve one transportation LP with the real city-wide cap: about 39,700 plane positions × 7 species ≈ 280,000 variables. That is still a sparse LP of the same form as Porta's (832 × 7); solving it at this size has not been tested. Then re-score each barri with the full raster model, as now. This removes the order problem: barri-by-barri optimisation would let the first barri use up the headroom.
7. **Aggregate.** `databases/barcelona/city/summary_<barri>.csv` plus one city table: per barri, S0 / S1a / Opt on the five indicators, canopy cover and taxon shares. For the web app, a per-district screening layer (`web/public/data/barcelona/`).

**Regression check:** the Porta bundle rebuilt by `build_barri("Porta")` must reproduce `tool_v0_summary_sizeexact_trunkTERCERA.csv`. The only differences allowed come from the 150 m buffer: Porta's current grid is the bare bounding box.

**Status 28 Oct:** steps 1–3 are coded (`scripts/lidar_tiles_barris.py`, `scripts/bcn_lidar_barri.py`, `site.build_barri`; `shade_sponge/README.md`, "Any barri"). Step 1 gives **158 distinct tiles** for the 73 barris (86 for the 27 barris with ≥ 500 planes), not ~100: the 150 m margin adds tiles. Not yet run on real data; the first run is Sant Antoni (8 tiles).

### 6.3 Order of work

From `databases/barcelona/site_screening_barris.csv` (inventory as screened on 8 Oct: 137,717 street trees and 39,656 planes in 72 barris; the press figure of 43,722 planes has a different date and scope):
- **The 27 barris with at least 500 planes hold 78% of them** (31,084). Run these first; in the rest the plane question is small and A (additions) matters more.
- **Two districts, Sant Martí (11,927) and Eixample (8,442), hold 51% of the planes.** A first batch by district covers half the problem.
- Suggested sequence:
  1. Porta (regression).
  2. Sant Antoni: the flood-dominant contrast site and the highest screening score (0.741, 989 planes).
  3. The rest of Eixample and Sant Martí.
  4. The other ≥ 500-plane barris.
  5. Everything else.
- 3 barris have no planes, and la Marina de Port has no tree data in the screening. They only get A.

### 6.4 Costs and risks (estimates, not measured)

- **LiDAR:** 158 tiles (step 1, 28 Oct; first estimate ~100, §2) against the 4 used for Porta, so download and processing scale about 25×. This is a batch job on your machine (≈ 4 GB RAM per tile set, as `bcn_lidar_porta.py`).
- **Tool runtime:** one Porta run takes about 4 min (`shade_sponge/README.md`). The city is roughly 100× Porta's area, so a full set of runs is likely an overnight batch. The optimiser is not the bottleneck; the raster re-scoring is.
- **Sidewalk widths** (step 4) decide the schedule. Without option (a), the city layer will have "size class unknown" in most barris by December.
- **Runoff outside Porta is indicative:** the interception calibration and the Δmin were set on Porta (§5).

### 6.5 Cap denominator: DECIDED (user, 26 Oct): street trees only

The tool works on street trees and sidewalks, so the city-wide cap counts the open street-tree inventory. Zone trees (`arbrat-zona`) stay out. The thesis states that the plan's 15% is over a wider base (~201,600 trees incl. squares), so the street-only reading is a local interpretation (`ASSUMPTION`).

**This is a simplification for developing the tool, not a claim about the plan** (user, 26 Oct). It keeps the cap on the same tree set the tool optimises (street trees on sidewalks). Before the final results, either switch to street + zone trees or report how much the cap changes with the wider base. It is listed in `notes/methodology.md` §1 (simplifications).

The options were:

The **cap denominator**. The plan's 15% is over about 201,600 trees of the urban fabric, including squares (`notes/tree_master_plan.md`). The open street-tree inventory has 140,404. The city LP needed one of the two:
- street trees only: simpler, and already in the repo;
- street + zone trees (`arbrat-zona`): closer to the plan's wording.

### 6.6 First transfer: Sant Antoni (28 Oct)

Steps 1–3 and 5 ran end to end on the user's PC (`python scripts/bcn_lidar_barri.py "Sant Antoni"`, then `python -m shade_sponge "Sant Antoni" [--trunk=TERCERA]`). Porta's regression run gave an identical summary, so the refactor of the site bundle changed nothing there.

**Inputs.** 8 ICGC tiles, all flown on 2022-06-01 (leaf-on), 66.7 M points in the barri + 150 m. 2,475 street trees: 989 planes and 950 *Celtis australis*; 90% have a usable LiDAR crown. 2,415 OSM building footprints with LiDAR height (median 21.4 m). The Overpass servers were overloaded and answered after several retries; the script now falls back to LiDAR footprints if they do not answer.

**Results, scenario R (replace the 989 planes), `--trunk=TERCERA`** (`databases/barcelona/tool_v0_summary_sant-antoni_trunkTERCERA.csv`; Porta from `tool_v0_summary_sizeexact_trunkTERCERA.csv`). Shares of today (S0); S1 and S1a = means of 10 seeds; "tool" = the optimised layout with the most summer shade.

| | Sant Antoni | Porta |
|---|---|---|
| Summer shade, tool | 79.7% | 99.1% |
| Summer shade, S1a (city's mix) | 66.8% | 87.4% |
| Summer shade, S1 (random) | 66.2% | 89.4% |
| Runoff to hotspots, tool / S1a | +2.5% / +3.1% | +0.1% / +0.4% |
| Canopy cover, S0 → tool | 25.1% → 21.8% | 23.3% → 22.3% |

Reading:
- The tool's margin over the city's mix is about the same in both barris (+12.9 and +11.7 points of today's summer shade), but Sant Antoni loses about a fifth of its summer shade even with the best layout: planes are 40% of its street trees (29% in Porta) and its mature planes are large.
- Winter shade is a third of Porta's in absolute terms (65,400 vs 196,200 m²·h at S0): Eixample's tall blocks already shade the streets in winter, so the winter-sun objective matters less there.
- **The Porta-local 15% cap breaks here:** *Celtis* is already 38% of Sant Antoni's street trees, so its cap is 0 in every layout. A barri-by-barri cap penalises barris that are already unbalanced; this is the case for the city-wide LP of step 6.

**With sidewalk widths (same evening).** The 652 MB GeoPackage download was reset again at 24%, so the widths come from the WMS, as for Porta (`python scripts/porta_sidewalk_width.py "Sant Antoni"` → `barris/sant-antoni/sidewalk_width.csv`). 1,747 of 2,475 trees are measured (`ok`, median width 5.0 m against Porta's 6.7 m); 630 are flagged `median`, 54 `no_facade`, 44 `no_kerb`. Of the 989 planes, 322 are large, 293 medium, 2 small and 372 unmeasured (`check`, no size filter). With `--size=exact --trunk=TERCERA` (`tool_v0_summary_sant-antoni_sizeexact_trunkTERCERA.csv`), now the same options as Porta's run:

| | Sant Antoni | Porta |
|---|---|---|
| Summer shade, tool | 79.0% | 99.1% |
| Summer shade, S1a (city's mix) | 72.1% | 87.4% |
| Summer shade, S1 (random) | 71.0% | 89.4% |
| Runoff to hotspots, tool / S1a | +2.5% / +2.8% | +0.1% / +0.4% |

The sizing rule narrows the tool's margin over the city's mix to 6.9 points (11.7 in Porta). S1a rises from 66.8% to 72.1% because the rule keeps the small *Pyrus* off the wide sidewalks. So in Sant Antoni the sidewalk rule decides most of the outcome, and species choice adds less than in Porta.

**Still not fully comparable, in two ways:** (1) with `--trunk=TERCERA`, only *Celtis* (TERCERA) and *Melia* (SEGONA, 23 trees) have enough local trees; the other five species keep Porta's medians over all trunk classes; (2) the runoff calibration and Δmin are Porta's (§6.4).

### 6.7 Batch: Eixample + Sant Martí (28–29 Oct)

`python scripts/run_barris.py` on the user's PC, all 16 barris of the two districts (37 tiles, all flown in 2022, leaf-on), same options as Porta's reference run (`--size=exact --trunk=TERCERA`, scenario R: replace every plane). Table: `databases/barcelona/barris_summary.csv`; log: `databases/barcelona/barris/run_log.csv`. Shares of today (S0); random and city mix = means of 10 seeds; tool = the optimised layout with the most summer shade.

The first night, four barris got zero inventory trees: their names carry an apostrophe and the inventory spells them differently, so the slug match failed silently. `bcn_lidar_barri.py` now matches names without separators and stops if no tree matches; the four were rerun on 29 Oct.

| Barri | Canopy S0 | Largest genus | Summer: random / city mix / tool | Tool margin (pts) | Winter: city mix / tool | Hot runoff: city mix / tool | Buildings |
|---|---|---|---|---|---|---|---|
| Porta | 23.3% | Platanus 31.1% | 89.4 / 87.4 / 99.1% | +11.7 | 100.3 / 120.6% | +0.4 / +0.1% | Porta set |
| Sant Antoni | 25.1% | Platanus 41.5% | 71.0 / 72.1 / 79.0% | +6.9 | 97.8 / 113.7% | +2.8 / +2.5% | OSM |
| el Fort Pienc | 28.1% | Platanus 43.1% | 67.5 / 68.2 / 78.0% | +9.8 | 88.8 / 100.3% | +0.8 / +0.6% | OSM |
| l'Antiga Esquerra de l'Eixample | 21.9% | Platanus 42.9% | 61.8 / 61.8 / 69.7% | +7.9 | 91.0 / 105.7% | +3.6 / +3.0% | OSM |
| la Dreta de l'Eixample | 24.8% | Platanus 46.4% | 60.4 / 59.9 / 70.9% | +11.0 | 89.0 / 106.2% | +4.1 / +3.2% | OSM |
| la Nova Esquerra de l'Eixample | 22.8% | Celtis 37.5% | 72.7 / 75.1 / 83.5% | +8.4 | 98.7 / 115.4% | +3.6 / +2.3% | OSM |
| la Sagrada Família | 26.3% | Celtis 36.8% | 68.8 / 74.7 / 77.8% | +3.1 | 97.2 / 99.6% | +3.3 / +3.2% | LiDAR |
| Diagonal Mar i el Front Marítim del Poblenou | 22.6% | Platanus 36.2% | 71.5 / 74.1 / 79.8% | +5.7 | 88.9 / 97.9% | +0.5 / +0.4% | LiDAR |
| Provençals del Poblenou | 31.9% | Platanus 53.7% | 58.0 / 65.2 / 68.8% | +3.6 | 80.2 / 81.2% | +1.1 / +0.9% | LiDAR |
| Sant Martí de Provençals | 33.8% | Platanus 46.7% | 70.2 / 71.6 / 78.4% | +6.8 | 100.7 / 118.4% | +1.7 / +1.5% | LiDAR |
| el Besòs i el Maresme | 25.5% | Platanus 40.0% | 71.1 / 77.3 / 82.6% | +5.3 | 103.0 / 110.1% | +1.3 / +1.3% | LiDAR |
| el Camp de l'Arpa del Clot | 20.2% | Celtis 42.6% | 77.2 / 79.0 / 81.2% | +2.2 | 95.7 / 96.5% | +0.8 / +0.8% | LiDAR |
| el Clot | 24.0% | Platanus 35.9% | 67.1 / 70.6 / 76.5% | +5.9 | 95.6 / 101.5% | +1.3 / +1.2% | OSM (rerun) |
| el Parc i la Llacuna del Poblenou | 21.3% | Platanus 48.2% | 62.3 / 72.2 / 78.4% | +6.2 | 89.0 / 92.7% | +1.3 / +1.2% | LiDAR |
| el Poblenou | 23.8% | Platanus 53.0% | 60.2 / 65.2 / 75.3% | +10.1 | 96.6 / 115.9% | +1.5 / +1.3% | LiDAR |
| la Verneda i la Pau | 29.9% | Platanus 44.5% | 72.8 / 72.0 / 82.2% | +10.2 | 101.9 / 126.0% | +0.8 / +0.7% | LiDAR |
| la Vila Olímpica del Poblenou | 28.1% | Platanus 48.1% | 70.5 / 72.3 / 77.8% | +5.5 | 92.9 / 96.8% | +1.4 / +1.2% | LiDAR |

Reading (the 16 new barris, Porta excluded):
- **The tool beats the city's mix in all 16**, by 2.2 to 11.0 points of today's summer shade (median 6.5). The margin does not follow the share of the largest genus (r = 0.19), so the local 15% cap is not what drives it.
- **No barri gets back to today's summer shade:** tool 68.8–83.5% (median 78.2), city mix 59.9–79.0% (median 72.0). Porta (99.1%) is the exception, not the rule: its sidewalks are wider (median 6.7 m against 4.9–5.1 m in the six Eixample barris).
- Runoff to the hotspots rises a little in every barri, because the canopy that replaces the planes is smaller: +0.4 to +3.2% with the tool, +0.5 to +4.1% with the city's mix. The tool is never worse than the city's mix on runoff.
- The tool buys its summer shade partly with winter shade (median 103.6% of today against 95.6% for the city's mix; up to 126% in la Verneda). This is the known cost of the weighted-sum sweep picking its summer-best layout.

Caveats:
- **Buildings come from two sources.** Overpass was overloaded on most of the night, so 11 barris first used footprints traced from the LiDAR building class (`source = "lidar"`, city blocks merge into one polygon) and five used OSM; el Clot was then rerun with OSM (below), so ten keep LiDAR footprints. Shadows do not depend on this: the heat proxy always casts them from the LiDAR building-height raster (`bldg_h`). The footprints only set the roof mask (runoff CN), which cells count as pedestrian ground, and which canopy is background. The median tool margin is 5.7 points with LiDAR footprints and 8.4 with OSM, but the groups are confounded with the district (five of the six OSM barris are in Eixample), so this is not evidence that the source matters. **Test (29 Oct): el Clot rerun with OSM footprints** (1,350 from the local BBBike extract, `scripts/osm_buildings.py`, against 646 LiDAR polygons): tool 76.7% → 76.5%, city mix 70.6% → 70.6%, margin 6.1 → 5.9 points, canopy S0 24.6% → 24.0%, hot runoff unchanged. The source moves the results by 0.2 points at most, so the other ten barris keep their LiDAR footprints. Overpass did not answer from the PC all day; buildings and green areas now come from the local extract (`raw/osm/{buildings,green}.gpkg`).
- Sidewalk widths: 14–54% of the trees per barri are unmeasured (`check`, no size filter), highest in el Besòs i el Maresme (54%) and Diagonal Mar (50%).
- As in §6.6: trunk sizes fall back to Porta's medians for species with few local trees; the runoff calibration is Porta's; the cap is still per barri.

### 6.8 City-wide cap: one LP for 17 barris (30 Oct)

`python scripts/city_lp.py` on the user's PC: Porta + the 16 Eixample and Sant Martí barris, 21,201 planes, stacked in one LP (`layout.assign`) with the same 15-point weight sweep as the tool. The cap is the city's (`layout.city_cap`): floor(15% × 140,404 street trees) minus each species' trees today, and of that headroom only the share of the city's 40,137 planes replaced here (21,201 / 40,137, `ASSUMPTION`: otherwise the first barris computed would use up the headroom of the rest). Cap here: Celtis 885, Styphnolobium 6,809, Tipuana 7,618, Melia 7,816, Brachychiton 8,350, Jacaranda 9,415, Pyrus 11,123. Outputs: `databases/barcelona/citylp/`, `citylp_summary.csv`, `citylp_species.csv`.

**Read one joint layout, not the best per barri.** `citylp_summary.csv` picks, in each barri, the swept layout with the most summer shade. Different barris then come from different weights, and their species counts added together are not one layout under the cap. The numbers below are all from the single summer-only layout (`S4_s1.00_w0.00_r0.00`). Its species totals are Celtis 885 (at the cap in every weight), Melia 3,252, Pyrus 1,641, Jacaranda 3,119, Tipuana 6,714, Brachychiton 986 and Styphnolobium 4,604. The top three summer-weighted layouts differ by less than 0.2% in total summer shade.

| Barri | Summer: city mix / local cap / city cap | City cap − local cap (pts) | Winter, city cap | Hot runoff, city cap | Largest species, city cap (S0: largest genus) |
|---|---|---|---|---|---|
| Porta | 87.4 / 99.1 / 103.3% | +4.2 | 124.2% | 0.0% | Jacaranda 29.6% (Platanus 31.1%) |
| Sant Antoni | 72.1 / 79.0 / 81.1% | +2.1 | 115.1% | +2.5% | Celtis 42.3% (Platanus 41.5%) |
| el Fort Pienc | 68.2 / 78.0 / 82.4% | +4.4 | 110.6% | +0.6% | Jacaranda 34.9% (Platanus 43.1%) |
| l'Antiga Esquerra de l'Eixample | 61.8 / 69.7 / 70.1% | +0.4 | 106.0% | +3.0% | Celtis 31.5% (Platanus 42.9%) |
| la Dreta de l'Eixample | 59.9 / 70.9 / 78.0% | +7.1 | 94.5% | +2.1% | Celtis 40.3% (Platanus 46.4%) |
| la Nova Esquerra de l'Eixample | 75.1 / 83.5 / 84.3% | +0.8 | 117.3% | +2.2% | Celtis 36.1% (Celtis 37.5%) |
| la Sagrada Família | 74.7 / 77.8 / 79.9% | +2.1 | 94.9% | +3.2% | Celtis 35.2% (Celtis 36.8%) |
| Diagonal Mar i el Front Marítim del Poblenou | 74.1 / 79.8 / 102.0% | +22.2 | 145.5% | +0.1% | Tipuana 48.5% (Platanus 36.2%) |
| Provençals del Poblenou | 65.2 / 68.8 / 69.7% | +0.9 | 85.4% | +1.1% | Melia 23.9% (Platanus 53.7%) |
| Sant Martí de Provençals | 71.6 / 78.4 / 83.7% | +5.3 | 128.1% | +1.2% | Tipuana 27.6% (Platanus 46.7%) |
| el Besòs i el Maresme | 77.3 / 82.6 / 86.8% | +4.2 | 134.8% | +1.0% | Tipuana 32.3% (Platanus 40.0%) |
| el Camp de l'Arpa del Clot | 79.0 / 81.2 / 81.2% | 0.0 | 96.5% | +0.8% | Celtis 40.8% (Celtis 42.6%) |
| el Clot | 70.6 / 76.5 / 78.9% | +2.4 | 115.0% | +1.0% | Tipuana 26.3% (Platanus 35.9%) |
| el Parc i la Llacuna del Poblenou | 72.2 / 78.4 / 78.7% | +0.3 | 95.2% | +1.1% | Melia 22.0% (Platanus 48.2%) |
| el Poblenou | 65.2 / 75.3 / 77.9% | +2.6 | 120.5% | +1.2% | Tipuana 21.5% (Platanus 53.0%) |
| la Verneda i la Pau | 72.0 / 82.2 / 83.1% | +0.9 | 126.7% | +0.7% | Jacaranda 27.6% (Platanus 44.5%) |
| la Vila Olímpica del Poblenou | 72.3 / 77.8 / 80.4% | +2.6 | 115.8% | +1.2% | Tipuana 41.5% (Platanus 48.1%) |

Reading:
- **The city cap never does worse than the local one** (0.0 to +22.2 points, median +2.4). Its margin over the city's mix grows to +2.2 to +27.9 points (median +9.2). Two barris, Porta and Diagonal Mar, now get back to more than today's summer shade.
- The gain comes from moving species to where they work best. 712 of the 885 Celtis the cap allows go to la Dreta de l'Eixample. Diagonal Mar gets 612 Tipuana, which its local cap had set to 0 because the barri already has many.
- **The city cap alone allows local monocultures.** In Diagonal Mar, Tipuana becomes 48.5% of the barri's street trees, against a plane share of 36.2% today. The cap's reasons are pest risk and resilience (`notes/tree_master_plan.md`), and these act locally too. So a city cap without any local ceiling can recreate the problem it is meant to solve. In 15 of the 17 barris, the largest species stays below today's largest genus share; the exceptions are Diagonal Mar and Sant Antoni (42.3% against 41.5%).
- Winter shade rises with summer shade (median 115%): the summer-only layout ignores the winter cost.

**With a local ceiling (`--local-ceiling`, second run, 30 Oct).** The ceiling is that in each barri, no species ends with more trees than the barri has planes today (`ASSUMPTION`). The idea is that a replacement should never create a larger single-species share than the one it removes. The summary now always reads one joint layout, the one with the most summer shade in total; here that is `S4_s1.00_w0.00_r0.00` again. Outputs: `citylp/*_local_*`, `citylp_local_summary.csv`, `citylp_local_species.csv`.
- The ceiling moves 219 Tipuana to Melia (214) and Jacaranda (5), and Celtis stays at its cap (885). Eight barris change.
- **Diagonal Mar:** Tipuana falls from 48.5% to 37.2% and summer shade from 102.0% to 97.2%. The 37.2% sits above the barri's 36.2% plane share because the shares are over trees with a usable LiDAR crown, while the ceiling counts every tree.
- **Sant Antoni:** summer shade falls from 81.1% to 80.1% (Celtis 40.3%).
- **la Dreta de l'Eixample:** summer shade rises from 78.0% to 78.4%.
- Overall the city cap with the local ceiling beats the local cap by 0.0 to +17.4 points (median +2.4), and beats the city's mix by +2.2 to +23.1 (median +9.2). Porta stays at 103.3%.
- **The ceiling costs little and removes the monoculture problem. It is the rule (DECIDED, user, 30 Oct):** the city's 15% fixes how much of each species, and the barri ceiling stops any barri from ending more concentrated than today.


### 6.9 Batch 2 and the city LP over 28 barris (30–31 Oct)

**Batch 2.** `run_barris.py` on the user's PC (30 Oct, 19:46–23:38) added the 11 barris with ≥500 planes outside Eixample and Sant Martí. "Sant Andreu" is both a barri and a district, and the script matches districts too, so it also ran five Sant Andreu barris below 500 planes (Navas 324, el Congrés i els Indians 184, la Sagrera 417, la Trinitat Vella 167, Baró de Viver 15). `barris_summary.csv` now has 33 rows. The tool beats the city's mix (S1a) in all 33.
- Four barris (la Maternitat i Sant Ramon, Sant Gervasi - la Bonanova, Baró de Viver, la Trinitat Vella) first failed in the LP: **no position drains to a flood hotspot**, so the runoff potential is all zero and its normalisation gave 0/0. Fixed in `layout.sweep` (an all-zero potential stays zero, test `test_sweep_zero_objective`); there the runoff weight has no effect.
- LiDAR: of the 90 tiles, 59 are from the 2022-06-01 flight, 20 from 2021-09-26 (Porta's) and 11 mixed. Both are leaf-on, but **the crown/LAI proxy mixes a June and a late-September canopy** across barris. Declared as a limitation; not corrected.

**The local ceiling can be infeasible.** With all 33 barris the city LP with `--local-ceiling` had no solution. A per-barri check (now printed by `city_lp.py`) named Baró de Viver and la Trinitat Vella. In Baró de Viver (15 planes) the existing trees already exceed 15 for five of the seven species, so only Pyrus (15) and Styphnolobium (5) have room, and each fits only 10 of the 15 positions. In la Trinitat Vella the total room is ample, but some positions fit only species with little room there (Melia 19, Pyrus 16). **Finding: the ceiling (no species above today's plane count) breaks down where few planes are replaced.** Both barris are outside the ≥500-plane criterion, so the LP was run on the planned 28; a barri with few planes would need a different ceiling (open).
- `city_lp.py`: a name that is both a barri and a district now selects the barri only.

**City LP with the local ceiling, 28 barris (31 Oct).** 31,580 planes. Cap here: Celtis 1,318, Styphnolobium 10,142, Tipuana 11,348, Melia 11,642, Brachychiton 12,438, Jacaranda 14,024, Pyrus 16,569. The joint layout is again `S4_s1.00_w0.00_r0.00`. Totals: **Celtis 1,318 and Tipuana 11,348 at the cap**; Melia 5,851, Styphnolobium 5,300, Jacaranda 3,966, Pyrus 2,591, Brachychiton 1,206.

| Barri | Planes | Summer: city mix / local cap / city LP | City LP − local cap (pts) | Winter, city LP | Largest species, city LP |
|---|---|---|---|---|---|
| Porta | 832 | 87.4 / 99.1 / 103.3% | +4.2 | 124.2% | Jacaranda 29.6% |
| Sant Pere, Santa Caterina i la Ribera | 830 | 77.6 / 87.5 / 99.7% | +12.2 | 148.5% | Tipuana 49.2% |
| Sant Antoni | 989 | 72.1 / 79.0 / 79.2% | +0.2 | 115.4% | Celtis 38.6% |
| el Fort Pienc | 980 | 68.2 / 78.0 / 82.4% | +4.4 | 110.6% | Jacaranda 34.9% |
| l'Antiga Esquerra de l'Eixample | 1,444 | 61.8 / 69.7 / 70.1% | +0.4 | 106.0% | Celtis 31.5% |
| la Dreta de l'Eixample | 2,696 | 59.9 / 70.9 / 71.2% | +0.3 | 108.5% | Celtis 27.6% |
| la Nova Esquerra de l'Eixample | 1,186 | 75.1 / 83.5 / 84.3% | +0.8 | 117.3% | Celtis 36.1% |
| la Sagrada Família | 1,147 | 74.7 / 77.8 / 79.9% | +2.1 | 94.9% | Celtis 35.2% |
| Horta | 552 | 91.1 / 98.2 / 98.6% | +0.4 | 128.4% | Tipuana 22.1% |
| Pedralbes | 980 | 86.1 / 89.5 / 91.6% | +2.1 | 112.5% | Tipuana 25.6% |
| la Maternitat i Sant Ramon | 729 | 89.2 / 94.0 / 99.6% | +5.6 | 127.7% | Tipuana 26.5% |
| les Corts | 1,633 | 77.3 / 79.4 / 87.3% | +7.9 | 102.1% | Tipuana 22.5% |
| Sant Andreu | 681 | 96.3 / 106.3 / 105.7% | -0.6 | 121.3% | Citrus 16.8% |
| el Bon Pastor | 666 | 78.6 / 84.0 / 84.7% | +0.7 | 100.4% | Celtis 32.5% |
| Diagonal Mar i el Front Marítim del Poblenou | 728 | 74.1 / 79.8 / 97.2% | +17.4 | 129.2% | Tipuana 37.2% |
| Provençals del Poblenou | 1,463 | 65.2 / 68.8 / 69.7% | +0.9 | 85.4% | Melia 23.9% |
| Sant Martí de Provençals | 1,258 | 71.6 / 78.4 / 83.7% | +5.3 | 128.1% | Tipuana 27.6% |
| el Besòs i el Maresme | 1,583 | 77.3 / 82.6 / 86.6% | +4.0 | 134.8% | Tipuana 32.3% |
| el Camp de l'Arpa del Clot | 496 | 79.0 / 81.2 / 81.2% | +0.0 | 95.9% | Celtis 40.8% |
| el Clot | 657 | 70.6 / 76.5 / 78.6% | +2.1 | 104.5% | Tipuana 20.9% |
| el Parc i la Llacuna del Poblenou | 1,120 | 72.2 / 78.4 / 78.7% | +0.3 | 95.2% | Melia 22.0% |
| el Poblenou | 1,861 | 65.2 / 75.3 / 77.9% | +2.6 | 120.5% | Tipuana 21.5% |
| la Verneda i la Pau | 1,692 | 72.0 / 82.2 / 83.1% | +0.9 | 126.7% | Jacaranda 27.6% |
| la Vila Olímpica del Poblenou | 1,069 | 72.3 / 77.8 / 80.4% | +2.6 | 115.8% | Tipuana 41.2% |
| el Poble-sec | 2,289 | 79.9 / 83.5 / 105.3% | +21.8 | 95.4% | Celtis 38.4% |
| Sant Gervasi - Galvany | 722 | 83.8 / 90.7 / 90.0% | -0.7 | 103.4% | Styphnolobium 19.1% |
| Sant Gervasi - la Bonanova | 550 | 92.2 / 95.0 / 90.8% | -4.2 | 109.9% | Tipuana 17.1% |
| les Tres Torres | 747 | 75.5 / 80.2 / 88.5% | +8.3 | 116.6% | Tipuana 31.0% |

Reading:
- **Against the city's mix:** −1.4 to +25.4 points (median +9.3). The only loss is Sant Gervasi - la Bonanova (90.8% against 92.2%).
- **Against the local cap:** −4.2 to +21.8 (median +2.1). With 28 barris the joint LP is no longer never-worse: three barris lose (la Bonanova −4.2, Galvany −0.7, Sant Andreu −0.6) because the capped Celtis and Tipuana go where they add most, el Poble-sec (+21.8) and Diagonal Mar (+17.4) first. The total gains; a barri can lose. If a per-barri floor is wanted (no barri below its local cap or below the city mix), it is one more constraint set; not added.
- Three barris end above today's summer shade (Porta 103.3%, el Poble-sec 105.3%, Sant Andreu 105.7%). Winter shade median 114%.
- Sant Pere, Santa Caterina i la Ribera reaches 49.2% Tipuana. The ceiling allows it because planes are 51.5% of the barri today, so it is not more concentrated than now, but it is a high share for one species.
- The 17-barri numbers in §6.8 change slightly (e.g. Sant Antoni 80.1 → 79.2%) because the cap is pro-rata to the planes in the run.
