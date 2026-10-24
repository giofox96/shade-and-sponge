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
