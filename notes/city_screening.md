# City screening: European cities with BOTH urban pluvial flooding and urban heat (7 Oct 2026)

Goal: find a city where one district suffers both pluvial flooding and heat stress, so a single tree-planting method can address both. Evidence comes from `notes/lit/literature_matrix.csv` (row numbers #) and from web sources linked below.
Status marks: ✅ verified in the source; 🟡 from abstract, press or search summary (verify before citing); ❌ not found or weak.

## 1. Evidence per city

| City | Heat / UHI evidence | Pluvial flood evidence | Do both hazards overlap in space and season? | Open data for the method | Fit |
|---|---|---|---|---|---|
| **Florence** | 🟡 25-station network: ~3 °C between hottest and coolest station; tropical nights 42 vs 10 days; hottest in the centre with little green (Petralli/Morabito, UniFI). ✅ LST of heat-island zones +3.15 °C (Guha 2018 (abs)). 🟡 Asphalt square at 50 °C surface temperature (Guerri 2026 #48 (abs)). Not in the Iungman/Huang European samples | ✅ Whole city exposed to pluvial/flash floods; hotspots in flat, sealed districts incl. historic centre; ~800 km combined sewer (Pacetti 2022 #18). 🟡 May 2023: 35 mm in <1 h, underpasses flooded; Sept 2024 underpass and basement flooding (press) | **Yes, spatially**: the hottest stations and the pluvial hotspots are both in the dense, sealed centre. **Season**: documented storms in May and September (leaf-on) | ✅ 82k trees (species, circumference); ✅ LiDAR DTM+DSM 1 m; ✅ IDF grid 1 km; 🟡 soil group 1:10,000 | **High** |
| **Barcelona** | ✅ One of Iungman's two "high mortality impact" example cities; in the top-5 tables for UHI-attributable and tree-preventable deaths (#35) | 🟡 ~3 episodes/yr with >60 mm/h in the first 20 min; sewer sized for a 10-yr return period; known flood-prone areas: Poblenou, Paral·lel–Sant Antoni–Raval, Diagonal (Barcelona Resilience Atlas); calibrated 1D/2D BCASA drainage model (UPC studies) | Likely yes (dense Eixample/Raval are hot and flood-prone); season to verify | ✅ Street trees CC BY 4.0 (species, planting date, size category, irrigation type; updated 1 Oct 2026); ✅ ICGC LiDAR ≥8 pts/m² (2021–23, CC BY 4.0); 🟡 IDF/drainage model (owned by BCASA, access to check) | **High**, plus IAAC is in Barcelona (site visits, local network) |
| **Bologna** | ✅ Among the 3 worst European cities for annual net UHI mortality (3 extra deaths/100k/yr) and the highest economic impact, with Turin (Huang 2023 #36) | 🟡 Oct 2024 was mixed: saturated soils + culverted streams overflowing (Arpae; Dottori 2014 #20). Pluvial-only hotspots not documented | Weak on the flood side | ✅ 87.8k trees with height class; 🟡 contours 2 m; 🟡 Ksat 1:50k | Medium |
| **Milan** | 🟡 Record hottest day in 260 years (23 Aug 2023, Brera, press); used as an extreme-heat example by Huang 2023 #36 | 🟡 Sept 2023: >60 mm in 3 h; Oct 2023 and Sept 2024 storms, but flooding mostly from the **Seveso river overflowing** (fluvial) | Partly | 🟡 Open tree data incl. crown diameter (not checked in detail) | Medium |
| **Athens** | ✅ Heatwaves amplify the night-time UHI by ~3 °C (Founda, cited in Stavropoulos 2026 #54); heat mortality rises 20–35% at high temperatures (Paravantis 2017 (abs)) | 🟡 Flash floods (not checked) | Unknown | ❌ Not checked | Low–Medium (data risk) |
| **Lisbon** | 🟡 UTCI hotspots; street trees cut UTCI by 3.2–6.3 °C (Silva 2025 #47 (abs)) | 🟡 Dec 2022: >80 mm/24 h, 65.6 mm in 3 h; Baixa and Alcântara flooded; €250 M drainage tunnels (press) | **Season conflict**: winter floods = deciduous trees leafless | ❌ Not checked | Low–Medium |

## 2. Score (1–5)

| City | Heat | Pluvial | Overlap | Data | Feasibility for you | **Total /25** |
|---|---|---|---|---|---|---|
| Barcelona | 5 | 4 | 4 | 5 | 5 | **23** |
| Florence | 4 | 5 | 5 | 4 | 4 | **22** |
| Bologna | 5 | 2 | 2 | 4 | 4 | 17 |
| Milan | 4 | 3 | 3 | 3 | 4 | 17 |
| Athens | 5 | 3 | ? | 1 | 2 | ~13 |
| Lisbon | 3 | 4 | 2 | 1 | 2 | ~12 |

**Reading:** Florence and Barcelona are effectively tied. Florence is stronger on documented *pluvial* hotspots that coincide with the hottest districts, and has an existing local evidence base (Pacetti, Guerri, Petralli, Morabito). Barcelona is stronger on heat-health evidence, LiDAR and practical access (IAAC), but its flood hotspots come from drainage reports, not a peer-reviewed hotspot map yet. Bologna's heat case is excellent, but its floods do not fit a vegetation thesis.

## 3. What would decide between Florence and Barcelona
1. **Barcelona:** can the BCASA flood-prone areas map (or the RESCCUE 1D/2D results) be obtained as data, not only as a picture? If yes, Barcelona ≥ Florence.
2. **Florence:** can Pacetti's PFI map and the historical pluvial event locations be obtained from the authors (UniFI DICEA)?
3. Tutor preference: a site you can visit (Barcelona) vs the cities in your original draft (Florence).

## Sources (web)
- Florence UHI network (UniFI repository): https://flore.unifi.it/handle/2158/751525
- Florence storms (press): https://www.lanazione.it/firenze/cronaca/bomba-dacqua-su-firenze-sottopassi-ee1c51d0 ; https://www.meteogiornale.it/2023/05/cronaca-meteo/meteo-toscana-forti-temporali-grandine-firenze-sconquasso-per-un-nubifragio-con-grandine/
- Barcelona flood-prone areas and episodes: https://coneixement-eu.bcn.cat/widget/atles-resiliencia/en_index_inundabilitat.html ; https://coneixement-eu.bcn.cat/widget/atles-resiliencia/en_index_resccue_inun_urbana.html
- Barcelona street trees: https://opendata-ajuntament.barcelona.cat/data/en/dataset/arbrat-viari
- ICGC LiDAR: https://www.icgc.cat/en/Geoinformation-and-Maps/Data-and-products/Elevations/Territorial-elevations/Territorial-LiDAR
- Milan 2023 heat and Seveso floods (press): https://www.ilpost.it/2023/10/31/seveso-esondato/ ; https://www.meteo.it/notizie/a-milano-giornata-piu-calda-da-260-anni-il-23-agosto-da-record-26210158
- Lisbon floods: https://portugal.com/news/how-prepared-is-lisbon-for-a-monster-flood
- EEA 571-city vulnerability map: https://www.eea.europa.eu/en/analysis/maps-and-charts/vulnerability-of-571-european-cities
