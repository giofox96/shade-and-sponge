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
- Canopy transmissivity for radiation: τ = exp(−k·LAI) (Beer–Lambert, Monsi & Saeki 1953 *(to add)*), k from the literature.

## 4. Runoff module (Python, later a Grasshopper component via Hops)
Event based, per street segment:
1. Rain depth P(T, d) from the PDISBA IDF curves, T = 1, 2, 10 yr, d = 1 h (plus observed storms if BCASA gauge data arrive).
2. **Canopy interception** over each crown's projection on sealed ground: storage-bucket I = min(P, S) with S from species storage capacity × LAI. An analytical Gash-type model (Hassan et al. 2017; Huang et al. 2017) is the refinement. Stemflow is ignored (<1% of rain; Anys & Weiler 2024).
3. **Tree-pit infiltration**: pit area × infiltration rate × event duration (literature range; Bartens et al. 2008, Zhang et al. 2019).
4. Remaining rain on sealed surfaces → SCS curve number (CN ≈ 98 sealed) → **event runoff volume (m³)**.
- **Validation:** (i) interception module vs the open Freiburg field data (Anys & Weiler 2024, FreiDok); (ii) per-tree and per-m²-canopy volumes vs paired-catchment benchmarks (Selbig et al. 2021: 6,376 L/tree; Coville et al. 2022: 64–66 L/m² canopy per leaf-on season); (iii) plausibility vs the flood-hazard index pattern.

## 5. Heat module (Ladybug Tools in Grasshopper now, Infrared City API later)
**Tier 1, fast, used for many layouts:** point-based UTCI at 1.1 m on a 2 m sidewalk grid.
`LB Import EPW` → hours → `LB Human to Sky Relation` (test points + context: buildings + tree crowns) → `LB Outdoor Solar MRT` → `LB UTCI Comfort` (air temperature, RH, wind from the EPW).
Limit: crowns act as opaque, so species differences enter only through crown size and shape. As an approximation, weight the shaded fraction by τ.
**Tier 2, detailed check of a few layouts:** `HB UTCI Comfort Map` (Honeybee: Radiance + EnergyPlus), with trees as HB Shades carrying a Radiance transmittance modifier and an energy transmittance schedule (leaf-on/off) from τ. Run locally or on Pollination.
**Later: Infrared City API** (UTCI/MRT in seconds) replaces Tier 1 inside the optimisation loop. Questions for the tutor are in `topic_decision.md` §6.4.
- **Metrics:** mean UTCI on sun-exposed sidewalks at the design hour; share of points in **strong heat stress (UTCI > 32 °C)** or above (stress classes: Bröde et al. 2012 *(to add)*); hours > 32 °C over the hot week (Tier 2).
- **Known limits:** the EPW is from the airport, not the city centre (test +1/+2 °C air-temperature offsets as sensitivity); UTCI uses wind at 10 m; transpiration cooling of air is not represented in Tier 1 (state it; Park 2026 shows it can exceed shading for air temperature).
- **Validation:** Ladybug vs ENVI-met agreement reported in the literature for 8–17 h (Bath study, *(to add)*); Tier 1 vs Tier 2 on the same layouts; optional MRT spot measurements in Porta (globe thermometer) on a hot day.

## 6. Optimisation
- **Decision variables:** species at each replaced plane position (from the feasible palette); optionally, new positions.
- **Objectives:** f₁ = heat (Tier 1 UTCI metric, or a calibrated shade × τ proxy pre-computed per position), f₂ = runoff volume at T = 2 yr (also reported for T = 1 and 10).
- **Constraints:** no species >15% within the study area (mirrors the city plan); diversity floor (Shannon); excluded species (invasive, pest hosts); crown clearance from façades.
- **Algorithm:** NSGA-II, in Python with `pymoo` (fast proxies) or in Grasshopper with Wallacei. The final Pareto layouts are re-checked with Tier 1/Tier 2 UTCI.

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
