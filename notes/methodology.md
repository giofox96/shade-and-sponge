# Methodology (draft v1, 8 Oct 2026): Porta, Barcelona

**Method in one line:** a computational method that chooses **which species replace Porta's plane trees and where**, scoring every layout on **pedestrian heat stress (UTCI)** and **event runoff volume**, and returns the trade-off between the two (Pareto front).
Problem, research question and hypotheses: `notes/topic_decision.md` §7. Site: `notes/site_selection.md`.
Citations marked *(to add)* are standard references not yet in `papers/`/Zotero: add them before citing.

---

## 1. Scope
| | Choice | Reason |
|---|---|---|
| Area | Porta, 0.84 km² (runoff, whole area); **design sub-area** of 2–4 street segments for heat (e.g. Av. Meridiana edge + one interior street in the north-east heat hotspot; to fix in a block-scale overlay) | UTCI simulation cost; Meridiana = highest flood band + main plane corridor |
| Unit of decision | Each plane-tree position (replacement), optionally new positions on plantable sidewalk cells | Matches the municipal replacement process |
| Season / time | Heat: hottest summer week from the EPW, design hours 12–17 h. Runoff: design storms + observed autumn storms | Heat peaks in summer; intense rain mainly in autumn (Resilience Atlas) |

## 2. Data (details: `databases/data_inventory_barcelona.md`)
| Layer | Source | Use |
|---|---|---|
| Street trees (species, planting date, size class) | Ajuntament open data `arbrat-viari` | Baseline S0, positions to replace |
| LiDAR ≥8 pts/m² (2021–23) | ICGC, CC BY 4.0 | Tree height, crown diameter, crown base; building heights; DTM |
| Buildings, streets, sidewalks | ICGC / municipal cartography (OSM fallback) | Ladybug context, sealed surfaces, plantable cells |
| Flood-hazard index; depth maps (on request) | Barcelona Regional / RESCCUE | Where runoff matters; check against model |
| Design rainfall (IDF T = 1–10 yr) | PDISBA *Estudi de pluges* | Design storms |
| Weather file (EPW) | climate.onebuilding.org TMYx, Barcelona El Prat | Ladybug UTCI inputs |
| Species traits | `notes/lit/species_measurements.csv` + 3TF/BROT 2/GRooT + literature | Interception, LAI, leaf habit, wood anatomy |
| Constraints | Tree master plan (≤15% per species), invasive list (RD 630/2013), pests | Feasible species set |

## 3. Tree model (shared by both modules)
For each tree: position, species, **height H, crown diameter D, crown base Hb** (existing trees from LiDAR, new trees from species size classes at planting and at maturity), **LAI** (leaf-on / leaf-off months), **canopy storage capacity S**, **leaf habit**, **wood anatomy** (diffuse- vs ring-porous, as a transpiration class).
- **Gap-filling:** species without measurements get genus or leaf-habit class values with a range. This currently covers Celtis, Melia, Tipuana, Jacaranda and Brachychiton (`databases/barcelona/species_coverage.csv`). Every result is re-run at the low and high ends of the range (sensitivity), and the missing data are reported as a finding.
- Canopy transmissivity for radiation: τ = exp(−k·LAI) (Beer–Lambert, Monsi & Saeki 1953 *(to add)*), k = 0.5 as in Peng et al. (2026) and in our LiDAR LAI proxy.
- **Species storage (option for runoff v2):** Xiao & McPherson (2016) give surface storage per unit leaf + stem area for 20 street species. Examples: *Platanus × hispanica* 0.87 mm, *Pyrus calleryana* 'Bradford' 0.51 mm, *Celtis sinensis* 0.71 mm (a congener of *C. australis*); mean 0.86 mm. A species factor s_sp = s · (C_sp / 0.86) would replace the single s; species without a value keep s and get a range. (Baptista et al. 2018 is not used as a capacity: their 15-min, 2.54 mm/h event delivers only 0.64 mm.)

## 4. Runoff module (Python, later a Grasshopper component via Hops)
Event based, per street segment:
1. Rain depth P(T, d) from the PDISBA IDF curves, T = 1, 2, 10 yr, d = 1 h (plus observed storms if BCASA gauge data arrive; fallback: Netatmo personal weather stations, 5-min public data, r = 0.94 with official daily gauges for one event, 24 station pairs, Valencia, Rombeek et al. 2025; check station density in Nou Barris and the data terms first).
2. **Canopy interception** over each crown's projection on sealed ground: storage-bucket I = min(P, S) with S from species storage capacity × LAI. An analytical Gash-type model (Hassan et al. 2017; Huang et al. 2017) is the refinement; Huang et al. validated it on two conifers only, and found the evaporation-to-rain ratio the most sensitive input. Stemflow is ignored (<1% of rain; Anys & Weiler 2024).
3. **Tree-pit infiltration**: pit area × infiltration rate × event duration (literature range; Bartens et al. 2008, Zhang et al. 2019). Absolute values from Bartens et al. (read in full): approximate container saturated conductivity of compacted clay loam (1.59 g/cm3) 1.3e-3 cm/s (~47 mm/h) without a tree, 3.0–3.9e-3 cm/s (~108–140 mm/h) with young oak or maple; 1.31e-3 vs 4.83e-5 cm/s (~47 vs ~1.7 mm/h) with vs without green ash (structural soil over compacted subsoil). These are lab values for the most restrictive layer, so use them only to bracket a sensitivity range. Zhang et al. (2019, read in full), three-year-old saplings in loam tanks, one year after planting: 0.28 m/d (~12 mm/h) without a tree, 0.33 m/d (+19%, fibrous *Malus baccata*), 0.61 m/d (~25 mm/h, +118%, tap-rooted *Sophora japonica* = *Styphnolobium*). Roots help; whether the effect depends on species is unclear (Bartens: oak vs maple not significant; Zhang: tap vs fibrous differ, young trees in tanks), so the term stays species-independent. Why the pit matters: once sealed surfaces drain onto the tree's soil, the canopy benefit fades and infiltration controls runoff; with run-on from 3× the soil area, raising infiltration from 0.036 to 3.6 mm/h cuts the November runoff probability from 89% to <1% (Marrazzo & Raimondi 2025, analytical model, *Platanus*, Lecco rain). Pit sizing (read in full): in Melbourne clay, 0.72 m² kerb pits draining ~200 m² kept a median 11% of runoff; ~90% retention needs a pit of 2.5–8% of its impervious catchment, and exfiltration (≥ 88%), not the young tree (~4%), removes the water (Grey et al. 2018). Established evergreen street trees transpired the equivalent of 17% of the annual runoff from the ~200 m² impervious catchment draining to each 6 m² trench, but the trench did not raise their transpiration (Thom et al. 2020; Apr–Sep modelled from ETo). If the pit is added, its variables are pit area relative to catchment and native-soil exfiltration; species enter through the crop factor (0.33–1.56 among 13 potted species, *Pyrus calleryana* in the high class; Thom et al. 2022), which matters little while trees are young (crop factor < 5% effect in Grey et al. 2018).
4. Remaining rain on sealed surfaces → SCS curve number (CN ≈ 98 sealed) → **event runoff volume (m³)**.
- **Validation:** (i) interception module vs the open Freiburg field data (Anys & Weiler 2024, FreiDok); (ii) per-tree and per-m²-canopy volumes vs paired-catchment benchmarks (Selbig et al. 2021: 6,376 L/tree; Coville et al. 2022: field 66 L/m² canopy per leaf-on season, calibrated i-Tree Hydro 6,120 L/tree and 63.5 L/m²; uncalibrated defaults gave about twice the total runoff); (iii) plausibility vs the flood-hazard index pattern.

### 4b. Runoff module v1: implemented 8 Oct (`scripts/runoff_model.py`, calibration `scripts/calibrate_interception.py`)
- **Grid:** 1 m over Porta (83.7 ha): roofs 29% (OSM footprints, CN 98), sealed open space 52% (CN 98), pervious 19% (NDVI 2017 ≥ 0.3 and LiDAR canopy < 2 m, or OSM park/garden/grass; CN 74 = TR-55 open space HSG C, *assumption*).
- **Storms:** PDISBA city-level empirical IDF, design intensity (`databases/barcelona/pdisba_idf_city.csv`): T1-60 min 19.6 mm, T2-60 31.9 mm, T10-60 62.5 mm, T2-20 min 21.2 mm.
- **Trees:** 2,600 LiDAR street-tree crowns (disk of LiDAR crown diameter; LAI = LiDAR proxy). Non-street canopy (parks, squares, private; 10.2 ha) is fixed background (LAI 2.3).
- **Calibration** of effective canopy storage S = s·LAI on Anys & Weiler (2024) open field data (16 urban *Tilia cordata* / *Acer platanoides*, Apr–Sep 2021, 51 events ≥ 1 mm): **s = 1.75 mm per unit LAI** (pooled median; lime 1.85, maple 1.60), per-tree interception 38–78% of rain, event RMSE 0.9–3.2 mm. The effective value includes evaporation during events; for Barcelona's short intense storms it may be lower, so 0.86 mm (surface storage only, Xiao & McPherson 2016) is the lower bound in the sensitivity runs. Plausibility of s: leafy crowns hold the first 2–4 mm of a storm (Kuehler et al. 2017), and S = 1.75 × 2.3 ≈ 4.0 mm; Coville et al. (2022) set i-Tree Hydro's leaf storage depth to 2.0 mm (typical 0.07–0.6, mean 0.25 mm) from in-situ estimates to match the field data, while noting that the value may be site-specific. Lower-bound evidence: Leyton storage 3.5 mm at LAI 2.6 (birch) and 2.9 mm at LAI 4.3 (pine), i.e. ~1.35 and ~0.67 mm per unit LAI (Zabret & Sraj 2019; surface storage only, without evaporation during events). Default leaf storage of 0.2 mm (Wang et al. 2008 via Huang et al. 2017; Dickinson 1984 via Marrazzo & Raimondi 2025) may underestimate interception.
- **Results (T2-60):** current street trees reduce Porta runoff by **1.85%** (open space only: 2.9%); the range across s = 0.86–2.2 and T = 1–10 yr is 0.4–4.0% (open space 0.7–6.3%). Plausibility: the same order as the measured 3.5–4% (Selbig et al. 2021; Coville et al. 2022). City-wide, Cortinovis et al. (2022) also found a small effect for Barcelona: 20,170 new street trees raised runoff retention from 50.18% to 50.76% for a 20 mm event (curve number, trees as land cover). Replacing all plane trees by mature Jacaranda/Melia/Tipuana: +0.17/+0.22/+0.27% runoff; by Celtis/Brachychiton: +0.60%; by Pyrus: +0.69%; **any young replacement: ≈ +0.7% (≈ 37% of the current street-tree benefit lost during the transition)**. The benefit shrinks with return period, supporting H3. Figure: `notes/figures/runoff_results_v1.png`.
- **Known limits:** the LiDAR LAI proxy (median ~2.3) is probably lower than TLS-measured LAI (Freiburg 2.6–4.9), so storage is likely underestimated; the same s is used for every species (species differ only through crown size and LAI); no routing, sewer or ponding (volume only); tree pits are not yet modelled separately.

## 5. Heat module (Ladybug Tools in Grasshopper now, Infrared City API later)
**Tier 1, fast, used for many layouts:** point-based UTCI at 1.1 m on a 2 m sidewalk grid.
`LB Import EPW` → hours → `LB Human to Sky Relation` (test points + context: buildings + tree crowns) → `LB Outdoor Solar MRT` → `LB UTCI Comfort` (air temperature, RH, wind from the EPW).
Limit: crowns act as opaque, so species differences enter only through crown size and shape, and shade MRT is underestimated (>6 °C below globe measurements under one tree). Fix, as in Peng et al. (2026): multiply direct radiation under the crown by τ = exp(−0.5·LAI) in the SolarCal step. This brought shade MRT within 2–4 °C of measurement. Ladybug also treats trees as shade only (no evapotranspiration), so it likely underestimates vegetation cooling by ~2–3 °C UTCI (Mannucci et al. 2025).
**Tier 2, detailed check of a few layouts:** `HB UTCI Comfort Map` (Honeybee: Radiance + EnergyPlus), with trees as HB Shades carrying a Radiance transmittance modifier and an energy transmittance schedule (leaf-on/off) from τ. Run locally or on Pollination.
**Later: Infrared City API** (UTCI/MRT in seconds) replaces Tier 1 inside the optimisation loop. Questions for the tutor are in `topic_decision.md` §6.4.
- **Metrics:** mean UTCI on sun-exposed sidewalks at the design hour; share of points in **strong heat stress (UTCI > 32 °C)** or above (stress classes: Bröde et al. 2012 *(to add)*); hours > 32 °C over the hot week (Tier 2).
- **Known limits:** the EPW is from the airport, not the city centre (test +1/+2 °C air-temperature offsets as sensitivity); UTCI uses wind at 10 m; transpiration cooling of air is not represented in Tier 1 (state it; Park 2026 shows it can exceed shading for air temperature). A fixed summer LAI overstates plane trees in heatwaves above ~40 °C (rare in Barcelona so far): Platanus lost roughly 30–50% of its plant area index after four days at 41.7–43.9 °C in Melbourne (Sanusi & Livesley 2020), so the plane baseline gets a low-LAI variant in the sensitivity runs. The design hour (day) misses night effects: dense tree clusters trap heat at night (Zölch et al. 2019); report it as a limit.
- **Validation:** Ladybug vs ENVI-met in a Mediterranean square: UTCI MBE 0.8–2.3 °C, CVRMSE 7–13%; MRT worse under direct sun (CVRMSE 22–38%) (Mannucci et al. 2025). Tier 1 vs Tier 2 on the same layouts; optional MRT spot measurements in Porta (globe thermometer) on a hot day.

## 6. Optimisation
- **Decision variables:** species at each replaced plane position (from the feasible palette); optionally, new positions.
- **Objectives:** f₁ = heat (Tier 1 UTCI metric, or a calibrated shade × τ proxy pre-computed per position), f₂ = runoff volume at T = 2 yr (also reported for T = 1 and 10).
- **Constraints:** no species >15% within the study area (mirrors the city plan); diversity floor (Shannon); excluded species (invasive, pest hosts); crown clearance from façades.
- **Algorithm:** NSGA-II, in Python with `pymoo` (fast proxies) or in Grasshopper with Wallacei. The final Pareto layouts are re-checked with Tier 1/Tier 2 UTCI.
- **Implemented v0 (8 Oct, `shade_sponge/`):** weighted-sum transportation LP instead of NSGA-II, with the shade × τ heat proxy, a topography-aware runoff target (runoff reaching flood hotspots, via DTM flow routing) and façade clearance. First result: no trade-off within the city palette (the front collapses). Adding the leaf-on calendar and season-weighted storms (Esbrí et al. 2026) does not change this: 78% of intense storm days fall in May–Oct, when all palette species are in full leaf. **Winter sun access** (winter shade on sunlit open ground as a cost, 15 Jan 10–15 h; leafless crowns cut ~35% of sunlight) creates the first real trade-off: the balanced layout cuts winter shade by 9% at equal summer shade (Tipuana → Jacaranda), and beyond it winter sun costs summer shade. Sensitivity (7 variants): the +14 to +15% summer gain vs a random palette and the summer–winter trade-off are robust; the size of the no-regret winter gain (−2 to −12%) depends on Tipuana's winter leaf state and on leafless crown opacity, both observable in the field. Field support for the winter term: in Coimbra (Csa), clear-winter midday air under leafless deciduous crowns was occasionally 0.3–0.7 °C warmer than under evergreens (Rochette Cordeiro et al. 2026). Details and limits in `shade_sponge/README.md`.
- **Why proxies are needed:** Ladybug in the loop costs 20–25 min per layout for 42 trees (Shaamala et al. 2025). On a 25 × 36 m site it costs 10–20 s rising to 2–3 h for 200 evaluations (Peng et al. 2026). Porta's 832 plane positions need a pre-computed shade × τ proxy, a surrogate, or the Infrared City API. Precedent for the Python stack: PySWMM + pymoo NSGA-II, population 200 × 120 generations on 50 parallel processes for 520 green-infrastructure area variables (Liu et al. 2026, no trees). Tree-placement precedents: a genetic algorithm needed 7 h per run for ~730 layouts and moved site-mean UTCI by only 0.1–0.3 °C (Hao et al. 2023); an SVR trained on 314,928 Ladybug shading runs predicted the best tree configuration per canyon with R² = 0.63, lower on held-out data (Oneto et al. 2026). Expect small per-layout differences and test them against the proxy error.

## 7. Scenarios compared
| ID | Layout |
|---|---|
| S0 | Current trees (planes kept) |
| S1 | Like-for-like: planes replaced with the city's named palette in its proportions |
| S2 | Heat-only optimum |
| S3 | Runoff-only optimum |
| S4 | Multi-objective Pareto set (trait-based) |
| (opt.) | Young vs mature crowns: transition loss after replacement |

Tests H1 (S4 vs S1 on both objectives), H2 (species composition of S2 vs S3) and H3 (runoff benefit vs T).

## 8. Test / transfer phase
Same pipeline on **Sant Antoni** (flood-dominant contrast) and **Florence** (transfer: Pacetti 2022 hotspots, 82k-tree inventory, LiDAR 1 m, regional IDF grid). Questions: do the trade-off pattern and the species ranking hold?

## 9. Tools
Python (geopandas, rasterio, pymoo; LiDAR via laspy/PDAL) · Rhino 8 + Grasshopper + **Ladybug Tools / Honeybee** · Infrared City API (later) · Hops (connects Python modules to Grasshopper) · Git/GitHub · Zotero. Exchange conventions: `exchange/README.md`.

## 10. Plan to 18 Dec (≈10 weeks)
| Weeks | Work |
|---|---|
| to 20 Oct | PS/RQ/H, literature infographics, this methodology, 5-min talk |
| 21 Oct – 3 Nov | LiDAR trees and buildings for Porta; trait table + gap-filling; runoff module + validation |
| 4 – 17 Nov | Ladybug Tier 1 for S0/S1; heat proxy calibration; Infrared City API if available |
| 18 Nov – 1 Dec | Optimisation S2–S4; Tier 2 checks |
| 2 – 10 Dec | Test on Sant Antoni and Florence; sensitivity |
| 11 – 18 Dec | Booklet, figures, final presentation |

## 11. Main risks → mitigation
- Missing species traits → gap-filling with ranges + sensitivity; the gap itself is a stated result.
- Flood depth maps unavailable → keep the hazard index for the site, and validate the runoff module on field benchmarks instead.
- UTCI cost → Tier 1 proxy + Infrared City; Tier 2 only for final layouts.
- Scope creep → one sub-area for heat, one storm set, one optimiser.
