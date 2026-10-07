# Site selection: why Porta (Nou Barris, Barcelona)

*Draft for the methodology chapter and the 20 Oct slides. 8 Oct 2026. Scripts: `scripts/bcn_site_screening.py` → `bcn_heat_check.py` → `bcn_site_select.py`.*

## 1. What the site must offer
The thesis tests one tree-planting method against **two hazards at once**: pedestrian heat stress and pluvial runoff. It also asks a live municipal question: which species should replace the plane trees that Barcelona's tree master plan reduces (no species above 15% of the total). The study area therefore had to show **both hazards physically present** and **a large plane-tree stock**.

## 2. Data (all open or public, 73 neighbourhoods)
| Criterion | Indicator | Source |
|---|---|---|
| Pluvial flood hazard | Share of area with flood-hazard index ≥ 40 (index 5–50 from sewer capacity, slope, contributing catchment; present scenario) | Barcelona Regional, *Impact study on climate change*, via the Barcelona Resilience Atlas |
| Physical heat | Median summer daytime land-surface-temperature anomaly vs city median | Landsat 8/9 Collection 2 L2, 31 clear scenes, Jun–Aug 2022–2025 (own processing) |
| Social heat vulnerability | Share of area in the top-20% class of global heat-wave vulnerability (2015) | Ajuntament de Barcelona open data, `factor-de-vulnerabilitat` |
| Plane-tree stock | Plane street trees per km² | Ajuntament open data, `arbrat-viari` (1 Oct 2026) |

## 3. Method: two steps, non-compensatory
1. **Eligibility:** flood share, surface-temperature anomaly and plane density must all be above the city's 60th percentile. A strong value on one hazard cannot make up for the absence of the other.
2. **Ranking** of the eligible neighbourhoods by the equal-weight mean of the four normalised criteria. Robustness check: 2,000 random weightings (Dirichlet), and the threshold varied at the 50th, 60th and 70th percentiles.

## 4. Result
| Threshold | Eligible neighbourhoods (score) |
|---|---|
| 50th pct | **Porta (0.65)**, Verdun (0.59), Provençals del Poblenou (0.52), … 12 in total |
| 60th pct | **Porta (0.65)**, Verdun (0.59), la Verneda i la Pau (0.44), … 7 in total |
| 70th pct | **Porta (0.65)**, el Camp de l'Arpa del Clot (0.37) |

**Porta is first at every threshold.** Across all 72 neighbourhoods with complete data, its ranks are: flood hazard #13, surface heat #11 (+1.36 °C), heat vulnerability #12 (91% of area in the top class), plane density #15 (994/km²). It is #2 overall on the four-criterion score and in the top 3 in 53% of random weightings.

**Why not Sant Antoni** (the highest compensatory score): it is #1 for flood hazard but #38 for surface heat (below the city median), so it fails the both-hazards condition. It is kept as a **flood-dominant contrast site** for the test phase, together with Florence.

## 5. Porta in numbers (open data)
- Area 0.84 km²; **2,825 street trees, 53 taxa; 832 plane trees (29%)**.
- Plane trees concentrate on **Av. Meridiana (194)**, Av. Río de Janeiro (111), Pg. Andreu Nin (80), Pg. Fabra i Puig (77), C. Doctor Pi i Molist (74), Pg. Valldaura (39).
- The next most common species are the replacements the city names: *Celtis australis* 296, *Melia azedarach* 167, *Pyrus calleryana* 147, *Jacaranda mimosifolia* 145, *Tipuana tipu* 139, *Brachychiton populneus* 103 (`databases/barcelona/porta_species.csv`). **The candidate palette already grows on site**, which helps field checks such as LAI and crown size from LiDAR.
- Spatial pattern (`notes/figures/porta_profile.png`): the highest flood-hazard band runs along the eastern edge (Av. Meridiana), which is also the main plane-tree corridor. Surface-heat hotspots are in the north-east and south-centre.

## 6. Limits to state openly
- The flood indicator is a hazard **index**, not water depth. RESCCUE depth maps (1-, 10-, 100-yr) exist but are behind the city login: request them via the tutor.
- Surface temperature ≠ pedestrian UTCI. It is a satellite reading at ~10:30 and includes treetops. UTCI will be computed in the method (Infrared City / Ladybug).
- The heat-vulnerability layer dates from 2015.
- The thresholds and equal weights are choices. The sensitivity tests above show that the selection does not depend on them.

Figures: `notes/figures/bcn_site_screening.png`, `notes/figures/bcn_lst_anomaly.png`, `notes/figures/porta_profile.png`.
