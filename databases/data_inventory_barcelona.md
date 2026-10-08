# Data inventory: Barcelona (heat + pluvial runoff), 7 Oct 2026

Status: ✅ verified (dataset metadata or file opened); 🟡 found in an official page, report, paper or search summary (confirm before use); ❌ gap.
Licence of the Barcelona open data portal (opendata-ajuntament.barcelona.cat) datasets below: **CC BY 4.0** unless noted.

## A. Shared base layers

| # | Item | Status | Source | Format | Resolution / date | Usable for |
|---|---|---|---|---|---|---|
| A1 | **Street trees** | ✅ **140,404 trees** | `arbrat-viari`, updated 1 Oct 2026 | CSV/JSON | Point. Fields: species (scientific, Catalan, Spanish names), planting date, size category (`PRIMERA`/`SEGONA`/`TERCERA`/`EXEMPLAR`; exact meaning to confirm), irrigation type, address, neighbourhood, district. **No DBH, no height** | Baseline stock, species mix, candidate positions (existing tree pits) |
| A2 | Park and zone trees | ✅ | `arbrat-parcs`, `arbrat-zona`, `arbres-interes-local` | CSV/JSON | Updated 1 Oct 2026 | Complete canopy in squares and parks |
| A3 | **LiDAR → DTM, DSM, tree heights, crowns** | ✅ | ICGC 3rd LiDAR coverage of Catalonia, 2021–23, ≥8 pts/m² (65% of sheets >10), classified (ground, vegetation, buildings), 1×1 km sheets, **CC BY 4.0**: https://www.icgc.cat/en/Geoinformation-and-Maps/Data-and-products/Elevations/Territorial-elevations/Territorial-LiDAR | LAZ | 2021–23 | Terrain and flow paths, building and tree heights, crown size (completes A1), 3D model for Ladybug |
| A4 | Vegetation cover | ✅ | `cobertura-vegetal-ndvi` (NDVI 2017 GeoTIFF, 2019 archive) | TIF | City | Existing green, LAI proxy |
| A5 | Land cover / sealing | 🟡 | ICGC *Mapa de cobertes del sòl* WMS (2009, 2018, 2019–22, 2023; updated May 2025); CREAF MCSC; Copernicus Imperviousness 10 m | WMS / vector | | Impervious fraction → curve numbers |
| A6 | Streets, sidewalks | ✅ / 🟡 | `mapa-base-de-vialitat` (WMS, 2025); `ampliacio-voreres-bici-bcn` (sidewalk extensions, 2023) | WMS / ZIP | | Plantable cells and pedestrian routes |
| A7 | Buildings | 🟡 | ICGC Urban Digital Twin of Catalonia; municipal cartography; OSM via OSMnx as fallback | | | Geometry for UTCI shading |

## B. Runoff theme

| # | Item | Status | Source | Notes |
|---|---|---|---|---|
| B1 | **Flood-prone areas / flood model results** | ✅ **public atlas layer read (8 Oct)**: flood-hazard index 5–50 (sewer capacity + slope + contributing catchment), present (`ar_in_perill_inun`, 11,705 polygons) and 2040 scenarios (`_b1`, `_a2`), read anonymously from the atlas's public CARTO account (`urbisadmin`); licence not stated → cite Barcelona Regional, keep raw data out of git. It is an index, **not** flood depth. Depth maps (T = 1, 10, 100 yr) are still only in PDFs/viewer | Barcelona **Resilience Atlas** (urban-flooding maps from the calibrated 1D/2D BCASA model, RESCCUE project): https://coneixement-eu.bcn.cat/widget/atles-resiliencia/en_index_inundabilitat.html ; Barcelona Regional 2017 climate-impact study, Ch. III *Inundabilitat urbana*: https://lameva.barcelona.cat/barcelona-pel-clima/sites/default/files/cap03_inudabilitat_urbana-20180227.pdf ; RESCCUE summary: https://sitroom.bcn.cat/widget/atles-resiliencia/docs/ResumExecutiu_RESCCUE.pdf | Hazard maps exist for **1-, 10- and 100-year** events (pedestrian and vehicle stability). The sewer is sized for **T = 10 yr**; ~3 episodes/yr exceed 60 mm/h in the first 20 min; insufficient-capacity areas include **Poblenou, Paral·lel–Sant Antoni–Raval, and the Diagonal between Balmes and Via Laietana**. **Action: request the GIS layers from Barcelona Regional / BCASA / the Urban Resilience office** (IAAC contacts?) |
| B2 | **Design rainfall (IDF)** | 🟡 in reports | PDISBA (sewer master plan 2019) *Estudi de pluges* annex: empirical IDF for T = 1–10 yr and Gumbel IDF tables per gauge, plus design storms with and without climate change: https://bcnroc.ajuntament.barcelona.cat/jspui/bitstream/11703/119275/9/Doc2.-_ESTUDI_PLUGES_def_meta.pdf.txt ; UB thesis (Casas) with a generalised IDF equation from Fabra Observatory 1927–2001: https://diposit.ub.edu/dspace/handle/2445/35255 | PDISBA targets: reduce flood risk for T ≤ 10 yr, and by ≥50% for T ≤ 500 yr |
| B3 | Rain gauges | 🟡 | ~20 high-resolution tipping-bucket gauges since 1994 (CLABSA → BCASA), series 1994–2019 (request); Meteocat XEMA (free API key; licence wording to check): https://datos.gob.es/es/catalogo/a09002970-datos-meteorologicos-de-la-xema | Event replay, storm seasonality (leaf-on vs leaf-off) |
| B4 | Soil / infiltration | 🟡 weak | ICGC geological map 1:25,000 (Barcelona sheets not confirmed) and Barcelona subsoil geology viewer; soil map 1:25,000 unlikely to cover the city | In dense Barcelona the relevant "soil" is the **tree pit**. Assume CN 98 for sealed surfaces and tree-pit infiltration from the literature; state this as an assumption |

## C. Heat theme

| # | Item | Status | Source | Notes |
|---|---|---|---|---|
| C1 | **Heat-vulnerability maps** | ✅ | `impacte-de-la-calor` (2018, population exposed by age group), `factor-de-vulnerabilitat` (2015/2017 heat-wave vulnerability factors), `presencia-absencia-vegetacio` (2015/2017, no-vegetation areas crossed with high temperatures), `poblacio-vulnerable` | GPKG | **Heat-hotspot side of the site selection** |
| C2 | Climate shelters | ✅ | `xarxa-refugis-climatics` (2025) | CSV/JSON | Context; possible route endpoints for UTCI paths |
| C3 | Urban air temperature, 100 m hourly | 🟡 | UrbClim (VITO/Copernicus), 2008–2017. Iungman et al. 2023 used UrbClim for its 93 cities, Barcelona included. The CDS entry is marked deprecated (May 2024), so check the new location | NetCDF | Heat-island context, validation of the warm-district choice |
| C4 | **Weather file for Ladybug (EPW)** | 🟡 | climate.onebuilding.org TMYx for Spain (e.g. Barcelona El Prat, 2009–2023 or 2011–2025); the zip also has RAIN and DDY files | EPW | Airport (coastal, rural) ≠ city centre: note it as a limitation, or adjust with UrbClim. A forum reports missing wind direction in some Barcelona EPWs: check the wind rose |
| C5 | Long temperature record | ✅ | `temperatures-hist-bcn` (monthly mean since 1780) | CSV | Warming trend for the problem statement |
| C6 | Heat health burden | ✅ | Iungman et al. 2023 (#35): Barcelona is a high-UHI-mortality example city; 🟡 press: ~300 heat-related deaths in Barcelona in one year (ASPB report via Catalan News) | | Problem statement |

## D. Species and constraints

| # | Item | Status | Source | Notes |
|---|---|---|---|---|
| D1 | **Tree master plan 2017–2037** ("Arbres per viure") | 🟡 | BCNROC: https://bcnroc.ajuntament.barcelona.cat/jspui/bitstream/11703/101548/4/Pla_arbrat_2017.pdf.txt | **No species above 15% of the total**; 40% climate-adapted species target. Press: plane trees (~28–30% of street trees) to be reduced to 15% (2027) or 12% (2037) (sources conflict); replacement species named include *Celtis*, *Sophora*, *Melia*, *Tipuana*. **This makes "which replacement species, and where" a live municipal question for the thesis** |
| D2 | Species coverage of measured traits | ✅ | `databases/barcelona/species_coverage.csv` | Top-30 species = 91% of street trees; species-level runoff or heat value for 40% of trees, both for 29% (mostly *Platanus*). **The named replacements (Celtis, Melia, Tipuana, Jacaranda, Brachychiton) have no values** |
| D3 | Pests | 🟡 | *Ceratocystis platani* (canker stain of plane): recorded in Catalonia (Calonge, 2010); current status not confirmed. *Xylella fastidiosa*: Catalonia declared free (2017); present in the Balearics and Alicante. Check DARP plant-health service / EPPO | Strengthens the case for reducing *Platanus* |
| D4 | Invasive species | 🟡 | Spanish catalogue (RD 630/2013, amended): *Ailanthus altissima* listed ✅; status of *Robinia*, *Ligustrum lucidum*, *Melia azedarach* not confirmed | Filter for candidate species |

## E. Gaps that matter
1. **Flood GIS layers (B1):** maps exist but aren't published as data. This is the critical request for site selection.
2. **Replacement-species traits (D2):** no interception or cooling measurements for Celtis, Melia, Tipuana, Jacaranda, Brachychiton. Fill by leaf habit / genus class and run a sensitivity analysis, or treat as the knowledge gap the thesis exposes.
3. **Urban weather (C4):** the EPW is from the airport.
4. Tree size (A1): derive from LiDAR (A3).

## F. Site selection: first pass done 8 Oct (`scripts/bcn_site_screening.py`)
Overlay **B1 flood-prone areas** (Poblenou, Paral·lel–Sant Antoni–Raval, Diagonal Balmes–Via Laietana) with **C1 heat vulnerability** and **A1 plane-tree density** (where replacement is planned). The district where all three overlap becomes the case study.

**Result (equal weights; `databases/barcelona/site_screening_barris.csv`, map `notes/figures/bcn_site_screening.png`):**
1. **Sant Antoni (Eixample)**, score 0.74: 48% of area in flood-hazard index ≥40, 51% in the top heat-vulnerability class, 989 plane street trees (1,230/km²)
2. Porta (Nou Barris) 0.60 · 3. Sant Martí de Provençals 0.53 · 4. Sants–Badal 0.52 · 5. les Corts 0.52

Caveats: (1) the heat layer is a 2015 *vulnerability* index (exposure + social sensitivity), not temperature. Next, check physical heat (LST, UrbClim or Infrared City UTCI). (2) The flood layer is a hazard index, not depth. (3) The equal weights are arbitrary, so check that the top neighbourhood is stable under ±weights. The Raval scores low on this flood index (4% high-hazard area), despite being named in the atlas text.
**Run:** `~/miniconda3/envs/shade-and-sponge/python.exe scripts/bcn_site_screening.py`, with `<env>/Library/bin` on PATH (GDAL DLLs).

### F2. Physical heat check and weight sensitivity (8 Oct, `scripts/bcn_heat_check.py`)
- Summer daytime **LST anomaly** (Landsat 8/9 C2 L2, Microsoft Planetary Computer, 31 clear scenes, Jun–Aug 2022–2025, per-scene anomaly vs city median, then median): `databases/barcelona/raw/lst_summer_anomaly.tif`, map `notes/figures/bcn_lst_anomaly.png`.
- Ranks for **Sant Antoni** out of 73 barris: flood hazard **#1**, plane density #6, heat vulnerability #19, **LST #39** (+0.28 °C; city median of barri means +0.30, 90th percentile +1.69). It is still #1 on the combined score with LST (0.81) and first in 54–60% of 1,000 random weightings (top-3 in 75–81%). **But it is a flood-led choice: its heat is average.** Plausible but untested: the dense plane canopy keeps its surfaces cool, which would make plane removal a heat risk.
- Barris above the **60th percentile on flood, LST and plane density at once**: la Verneda i la Pau, **Porta** (also 91% in the top heat-vulnerability class; LST +1.36 °C), Vilapicina i la Torre Llobeta, el Camp de l'Arpa del Clot, Verdun, Navas. Above the median on all three: also **Provençals del Poblenou** (flood 27%, LST +0.47, 1,347 planes/km²) and el Congrés i els Indians.
- LST limits: satellite surface temperature at ~10:30, under the canopy top, not pedestrian UTCI. Treat it as a screening signal only.

### F3. Decision (user, 8 Oct): **Porta**. Justification in `notes/site_selection.md`.

### G. LiDAR extraction for Porta (8 Oct, `scripts/bcn_lidar_porta.py`)
- Tiles 430586, 430587, 431586, 431587 (Territorial LiDAR v3.1, LAS 1.4, EPSG:25831), **flown 26 Sept 2021 (leaf-on)** from GPS time. Direct download pattern: `https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/full10km<ID10K>/lidar-territorial-v3r1-full1km<ID1K>-2021-2023.laz`; tile grid `https://datacloud.icgc.cat/datacloud/lidar-territorial/json/lidar-territorial-tall.json`.
- 29.2 M points in Porta + 30 m; class 12 (overlap strips, 35% of points) is unlabelled and used only for the gap fraction. Ground points cover 58% of 0.5 m cells before filling.
- Outputs: DTM/CHM/building-height rasters (0.5 m, `raw/lidar/`), **2,600 of 2,825 trees with crown metrics** (92%), 745 buildings (median 16.8 m, p90 23.2 m), species summary `databases/barcelona/porta_species_lidar_summary.csv`, QA figure `notes/figures/porta_lidar_qa.png`.
- Median height / crown diameter: *Platanus* 14.3 / 8.4 m (n=807), *Celtis australis* 9.5 / 4.6 m, *Melia* 9.8 / 8.4 m, *Jacaranda* 9.2 / 7.3 m, *Tipuana* 10.0 / 8.0 m, *Pyrus calleryana* 6.6 / 3.1 m, *Brachychiton* 8.3 / 4.3 m.
- Limits: the crowns are watershed-segmented from inventory seeds (9 m max radius), so overlapping crowns are split approximately. The LAI proxy (gap fraction, k = 0.5) is uncalibrated and has a narrow range (1.9–2.9). Use it for ranking only, after checking against literature LAI.

### H. Trait table (`scripts/build_trait_table.py` → `databases/traits/porta_trait_table.csv`)
Top-20 Porta species + *Styphnolobium japonicum*; species-level values only, each with its source: LiDAR (this study), **BROT 2.0** (CC0, Figshare collection 3843841; leaf phenology, SLA, LDMC, P50, root depth, wood density), **3TF** (SLA, LDMC, WD, Nmass), **SylvCiT BDD** (drought/shade/flood tolerance), literature measurements. A `gaps` column lists what is missing per species.
**Leaf-on calendar of the palette (8 Oct):** `databases/traits/phenology_palette.csv` (leaf fraction per month, source per species; months without a source = winter-deciduous class default or a species-specific assumption (Jacaranda Jan–Mar, Tipuana Mar–Apr), all marked in the file). Storm-month shares: `databases/barcelona/storm_months.csv` (Esbrí, Rigo & Llasat 2026, Atmosphere 17(1):41, Fig. 4: 45 intense days 2014–2022, Sep 29%, Oct 22%).
**Still to obtain (user actions):** i-Tree species list export (i-Tree Eco desktop → View → Species List: leaf persistence, leaf area/biomass relations, shading coefficients); TRY data request (try-db.org) for leaf phenology type, leaf area, wood vessel anatomy and leaf wettability of the palette.

### I. Runoff inputs added (8 Oct)
- **PDISBA city IDF** (sewer master plan 2019, *Estudi de pluges*, section 2.6 "Taula resum de les IDF empíriques de la ciutat de Barcelona"; read in the browser because the repository rate-limits scripts): `databases/barcelona/pdisba_idf_city.csv` (durations 10/20/30/60/120 min × T = 1/2/5/10 yr; max, min, mean, normal-95 and design intensity in mm/h). The full table (5–200 min) is in the source.
- **NDVI 2017** (open data `cobertura-vegetal-ndvi`, 0.9 m, CC BY 4.0): the full city raster is 1.6 GB in `raw/` (it can be deleted; `raw/porta_ndvi_2017.tif` is the 1 m crop).
- **Anys & Weiler (2024) dataset** (FreiDok plus 242951, CC BY-NC 4.0): `databases/traits/raw/anys_weiler_2024/`, used for calibration.
