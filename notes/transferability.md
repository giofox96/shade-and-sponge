# Transferability of the study and the tool

*Draft v1, 18 Oct 2026. For the 20 Oct talk (slide 10) and the discussion chapter. Sources: `databases/data_inventory_barcelona.md`, `databases/data_inventory.md`, `notes/topic_decision.md` §6.1, `notes/methodology.md` §4 and §8, `shade_sponge/README.md`, `databases/transfer_species_overlap.csv`.*

**Claim in one line:** the **code** is site-agnostic by construction, the **evidence is not**. Three of the six core modules carry no local constant; the transfer cost is almost entirely the cost of rebuilding the local data and re-deriving the local parameters. One dataset (a classified **leaf-on** point cloud) and one layer (a city **pluvial flood map**) are hard dependencies that no fallback replaces today.

Why this belongs in the talk: the method is calibrated in one 0.84 km² neighbourhood with 2,825 street trees (`notes/site_selection.md` §5). The tutor asks for a contribution to knowledge, so the thesis has to say where the method holds and what it costs to move it, rather than implying it is universal.

---

## 1. Four degrees of transfer
| | Case | New data needed | Cost | Status |
|---|---|---|---|---|
| **T0** | Another neighbourhood of Barcelona (**Sant Antoni**, flood-dominant contrast) | None: the same inventory, LiDAR, IDF and flood model cover the whole city. Only the site adapter (`build_<name>`) and the hotspot extract change | days | planned, methodology §8 |
| **T1** | Another Mediterranean city with mature open data (**Florence**, planned transfer case) | New adapter + 6 datasets; traits and phenology re-derived; the decision variable redefined (§5) | 2–3 weeks | planned 2–10 Dec, **data access unchecked** (`notes/agent_backlog.md`) |
| **T2** | A city with no species-level inventory or no open LiDAR (**Bologna** is the inventoried fallback) | As T1, plus the baseline itself is missing. The **design front-end still works** (§6): the designer supplies the positions | weeks–months | not planned |
| **T3** | Another climate (non-Csa) | Everything in T1, plus the interception constant, the leaf calendar, the storm season and the heat design days lose their anchors (§4) | out of scope | **not claimed** |

The thesis validates T0 and attempts T1. T2 and T3 belong to the discussion, as limits, not results.

## 2. What the method needs per site, and how well it travels
Status symbols as in the data inventories: ✅ verified · 🟡 found, to confirm · ❌ not found.

| # | Input | What it feeds | Barcelona (calibration) | Florence (T1) | Bologna (T2) | Travels? |
|---|---|---|---|---|---|---|
| 1 | Study-area boundary, buildings, DTM | Domain, shadows, flow routing | ✅ open data + ICGC LiDAR; OSM footprints used in runoff v1 (A3, A7) | ✅ DTM/DSM 1 m, 2019–21 (F3) | 🟡 city LiDAR coverage unconfirmed; TINITALY 10 m fallback (B3) | **Yes.** OSM buildings + a national DTM exist nearly everywhere; 10 m DEM degrades the routing |
| 2 | Street-tree inventory with **species and position** | Baseline S0, the positions to replace | ✅ 140,404 trees (A1) | ✅ 82,226 trees, no height, no planting date (F1) | ✅ 87,796 trees, with height class (B1) | **Yes where it exists.** It is the one thing the method cannot derive itself |
| 3 | **Classified leaf-on LiDAR point cloud** | Crown diameter, crown base, **LAI proxy** from gap fraction | ✅ ≥8 pts/m², classified, flown **26 Sept 2021 (leaf-on)**, CC BY 4.0 (A3, §G) | 🟡 only **1 m DTM/DSM rasters** are documented; point cloud and survey season not recorded (F3) | 🟡 coverage unconfirmed (B3) | **No.** A DSM gives height and crown width, not gap fraction. Leaf-off LiDAR makes the LAI proxy meaningless |
| 4 | Design rainfall (IDF) | Design storms T = 1, 2, 10 yr | ✅ PDISBA empirical IDF (B2, §I) | ✅ LSPP 2012, a and n gridded at 1 km (F5) | ❌ no regional IDF grid found: fit from Dext3r annual maxima (B5) | **Mostly.** Where no grid exists, add a gauge-fitting step |
| 5 | Pluvial flood map (hotspots or depth) | Where runoff matters; the hotspot objective | ✅ RESCCUE 1D/2D depth T10/T100 + hazard index (B1) | 🟡 PGRA P1–P3; a pluvial map is not confirmed, Pacetti et al. 2022 hotspots must be requested from the authors (F6, F7) | 🟡 PGRA + Oct 2024 event perimetration, but the event was **mixed, culvert-driven** (B6, B7) | **No.** See §3: the tool's own routing is not a substitute |
| 6 | Weather file (EPW) | UTCI inputs, design hours | ✅ TMYx El Prat + city station (C4) | 🟡 TMYx exists for Italian stations; licence to check | 🟡 same | **Yes.** TMYx coverage is global; the airport-vs-centre bias is a stated limit everywhere |
| 7 | Species traits (interception, cooling) | Trait table, gap-filling | 🟡 top-30 = 91% of street trees; a species-level runoff **or** heat value for **40%** of trees, both for 29% (*Platanus* alone 28.6%) | 🟡 top-30 = 80% of 82,226; **19%** of trees, both for **7%** | ❌ not computed | **Partly, and it gets worse.** §4 |
| 8 | Leaf-on calendar + storm season | `season.py`: LAI per month, storm weighting | ✅ photo-based January calendar (`notes/decisions/leaf_state_inat.md`); 78% of intense storm days in May–Oct (Esbrí et al. 2026) | ❌ to re-derive | ❌ to re-derive | **No.** Both are city-specific by definition |
| 9 | Policy constraint + replacement palette | `layout.py`: the feasible species set and the 15% cap | ✅ tree master plan: no species >15%, plane trees ~29% of street trees, named replacements (D1) | ❌ no equivalent programme found | ❌ no equivalent programme found | **No.** The decision problem itself is local (§5) |

Rows 1, 2, 4 and 6 are the easy half: open data, fallbacks exist, and a missing piece only degrades precision. Rows 3, 5, 7, 8 and 9 are the transfer cost.

## 3. Three things that do not travel, in order of severity
1. **A classified, leaf-on point cloud (row 3).** The LAI proxy is `−ln(gap fraction)/k` computed from the classified points inside each segmented crown (`scripts/bcn_lidar_porta.py`), and LAI drives both objectives: canopy storage `S = s·LAI` for runoff and opacity `1 − exp(−0.5·LAI)` for shade. A 1 m DSM, which is what Tuscany publishes, yields height and crown width but no gap fraction, so on a DSM-only city the species differences collapse to crown size. **Fallback:** literature or database LAI per species, with the sensitivity range already used for the gap-filled species — i.e. the transfer city loses the one trait we measure ourselves.
2. **A city pluvial flood map (row 5).** Tested, not assumed: the tool's own routing (Priority-Flood on DTM + buildings, no sewer) **barely separates** RESCCUE wet from dry cells in Porta — ROC AUC 0.52 in all four scenarios, area-matched hit rate 25% vs 23% random at T10 present. Only the extreme tail is informative: of the top 0.5% of open ground by upstream area, 58% (T10 present) to 80% (T100 future) is wet, 1.7–2.6× the random rate (`scripts/compare_resccue_runoff.py`, methodology §4 validation iii). So hotspots must come from a municipal map; without one, the runoff objective reduces to total volume and the *placement* half of the method loses its target.
3. **Traits and phenology (rows 7, 8).** Transfer makes the trait gap **worse, not better**: measured-trait coverage falls from 40% of trees in Barcelona to 19% in Florence (7% with both a runoff and a heat value). The partial consolation, measured in `databases/transfer_species_overlap.csv`: **63.5% of Florence's top-30 trees (41,944 trees, 51% of the full inventory) are species that already grow in Porta with LiDAR crown, height and LAI medians**, and 74.0% match at genus level. So the trait table and the gap-filling classes carry over for about two thirds of the stock, but Porta's crown medians reflect Barcelona's planting age and pruning, so geometry must be re-measured from Florence's own survey. The species that match nothing in Porta are exactly the Mediterranean evergreens the coverage note flags: *Quercus ilex* 8.5% of the top-30, *Olea europaea* 6.2%, *Quercus robur* 1.7%, *Carpinus betulus* 1.2%. (Sanity check in the same file: Porta covers 97.9% of Barcelona's own city-wide top-30, which is why the site is a good calibration case and a weak test of generality.)

## 4. Parameters that must be re-derived, not copied
| Parameter | Value and anchor | Why it is local |
|---|---|---|
| `s` = 1.75 mm per unit LAI | Calibrated on Anys & Weiler (2024): 16 urban *Tilia*/*Acer*, Freiburg, 51 events Apr–Sep | **Already a transfer**: temperate climate, temperate species, long moderate events. Lower bound 0.86 mm (surface storage only, Xiao & McPherson 2016) is kept in every sensitivity run for that reason |
| Storm months | 78% of intense storm days in May–Oct (Esbrí et al. 2026, Barcelona) | Decides how much the leaf calendar matters. A city with winter-dominated storms would weight leafless months and could change the species ranking |
| Leaf calendar `phenology_palette.csv`, `R_OFF` = 0.5 | January photo evidence for Barcelona; `R_OFF` an assumption (test 0.3–0.7) | Phenology shifts with latitude and winter temperature; the whole winter-sun trade-off rests on it |
| Heat design days 15 Jul / 15 Jan, hours 12–17 / 10–15 | ASSUMPTION until the EPW hottest/coldest weeks | Latitude and climate; the sun model itself takes `(lat, lon)` and needs no change |
| `HAZARD_HIGH` = 40 | Resilience Atlas flood-hazard index, scale 5–50 | A threshold on **a Barcelona-specific index**. It has no meaning in another city's hazard product |
| `CAPTURE_M` = 100 m | ASSUMPTION, stand-in for sewer inlets (test 50–200 m) | Depends on the local drainage layout, which we do not have for any city |
| `OP_BARE` = 0.35, `k` = 0.5 | Literature (McPherson 1984; Heisler 1982/84; Beer–Lambert) | Not site-specific: these do travel |

## 5. The question travels less well than the method
The thesis asks **which species replace Porta's plane trees**. That question exists because Barcelona's tree master plan caps every species at 15% while plane trees are ~29% of the street stock (D1) — a live municipal decision with a given palette and a given set of positions. Neither Florence nor Bologna has an equivalent programme in the inventories. On transfer, the decision variable therefore has to be redefined: species at **renewal** positions (trees removed in the normal cycle), or species at **new** positions on plantable sidewalk cells, with a diversity constraint instead of a named palette. The optimiser does not change (positions × feasible species, two objectives, a share cap); what changes is who supplies the candidate positions and the cap. **This is worth saying explicitly in the talk**: it is a framing limit, not a code limit, and it is the kind of specificity the tutor asked for.

## 6. Two front-ends, two transfer profiles
`CLAUDE.md` already commits to one core and two front-ends, and they do not transfer equally:

- **Planning mode** (city-scale replacement, as in Porta) needs rows 1–9: inventory, point cloud, IDF, flood map, traits, phenology, policy. This is the demanding path and the one the thesis validates.
- **Design mode** (Grasshopper, the primary persona) needs far less: the designer supplies the site geometry and the candidate positions, so rows 2, 3 and 9 are replaced by the model on screen. What remains mandatory is an EPW, a DTM and species traits. **This is the honest answer to "is the tool transferable?"** — as a design tool, almost anywhere in the Csa belt; as a planning tool, only in cities with Barcelona-grade open data.

## 7. What can be claimed on 20 Oct, and what cannot
**Can:** the core is site-agnostic (a new site = `build_<name>()` + `trees_<name>()` with the same keys, `shade_sponge/README.md`); 3 of the 6 modules carry no local constant (`topo.py` routing, `heat.py` geometry and sun, `runoff.py` SCS-CN), while 3 do (`site.py` adapter and thresholds, `season.py` calendar and storm months, `layout.py` palette and cap); the data cost of a transfer is enumerated above; the Florence species overlap is measured.
**Cannot:** that the results transfer. No layout, Pareto front or species ranking from Porta has been tested anywhere else yet. Transfer is scheduled for 2–10 Dec and Florence data access is still unchecked, so the talk should present transferability as a **designed property of the tool plus a measured data bill**, not as a result.

## 8. Open checks
- [ ] Does Regione Toscana publish the **LiDAR point cloud** (not just the 1 m DTM/DSM), and in which season was it flown? Decides whether the LAI proxy survives the transfer (F3).
- [ ] Ask Pacetti et al. for the Pluvial Flood Index map and the historical pluvial event locations (already an open check in `notes/topic_decision.md` §5; it is now also the T1 hotspot layer).
- [ ] Tuscany HSG 1:10,000 download location (F2) — the only soil input the runoff module needs beyond CN assumptions.
- [ ] Re-derive the Florence storm season and leaf calendar, or state that the Barcelona values are used unchanged (and run them in sensitivity).
- [ ] Decide with the tutor whether T1 (Florence) stays a chapter or becomes a discussion section, given the 18 Dec deadline (open question in `notes/agent_backlog.md`).
- [ ] A climate-fit filter for candidate species at a new site is still on the tool's own "next" list (`shade_sponge/README.md`).
