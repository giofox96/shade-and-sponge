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
