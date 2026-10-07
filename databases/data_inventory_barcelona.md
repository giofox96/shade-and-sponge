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
| B1 | **Flood-prone areas / flood model results** | 🟡 viewer + PDFs, **no open GIS layer found** | Barcelona **Resilience Atlas** (urban-flooding maps from the calibrated 1D/2D BCASA model, RESCCUE project): https://coneixement-eu.bcn.cat/widget/atles-resiliencia/en_index_inundabilitat.html ; Barcelona Regional 2017 climate-impact study, Ch. III *Inundabilitat urbana*: https://lameva.barcelona.cat/barcelona-pel-clima/sites/default/files/cap03_inudabilitat_urbana-20180227.pdf ; RESCCUE summary: https://sitroom.bcn.cat/widget/atles-resiliencia/docs/ResumExecutiu_RESCCUE.pdf | Hazard maps exist for **1-, 10- and 100-year** events (pedestrian and vehicle stability). The sewer is sized for **T = 10 yr**; ~3 episodes/yr exceed 60 mm/h in the first 20 min; insufficient-capacity areas include **Poblenou, Paral·lel–Sant Antoni–Raval, and the Diagonal between Balmes and Via Laietana**. **Action: request the GIS layers from Barcelona Regional / BCASA / the Urban Resilience office** (IAAC contacts?) |
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

## F. Site-selection logic (next step)
Overlay **B1 flood-prone areas** (Poblenou, Paral·lel–Sant Antoni–Raval, Diagonal Balmes–Via Laietana) with **C1 heat vulnerability** and **A1 plane-tree density** (where replacement is planned). The district where all three overlap becomes the case study.
