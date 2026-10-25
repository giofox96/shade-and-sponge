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

- **LiDAR:** about 100 tiles (§2) against the 4 used for Porta, so download and processing scale about 25×. This is a batch job on your machine (≈ 4 GB RAM per tile set, as `bcn_lidar_porta.py`).
- **Tool runtime:** one Porta run takes about 4 min (`shade_sponge/README.md`). The city is roughly 100× Porta's area, so a full set of runs is likely an overnight batch. The optimiser is not the bottleneck; the raster re-scoring is.
- **Sidewalk widths** (step 4) decide the schedule. Without option (a), the city layer will have "size class unknown" in most barris by December.
- **Runoff outside Porta is indicative:** the interception calibration and the Δmin were set on Porta (§5).

### 6.5 Open choice for the user

The **cap denominator**. The plan's 15% is over about 201,600 trees of the urban fabric, including squares (`notes/tree_master_plan.md`). The open street-tree inventory has 140,404. The city LP needs one of the two:
- street trees only: simpler, and already in the repo;
- street + zone trees (`arbrat-zona`): closer to the plan's wording.
