# Transfer-city candidates: which other cities could the method move to?

*Draft v2, 18 Oct 2026 — §0, §3 and §5 rewritten after the data search of the same day (`databases/data_inventory.md` §6). Original v1 text kept where the evidence did not move it.*

*Drafted 18 Oct 2026. Follows `notes/transferability.md` (what a transfer costs) and `notes/city_screening.md` (the 7 Oct screening that chose the study city). Status marks as in the inventories: ✅ verified in the source · 🟡 from a search summary, press or metadata, verify before citing · ❌ looked for, not found.*

**Answer in one line:** the binding input is not the tree inventory, it is a **classified, high-density, leaf-on LiDAR point cloud**, and Catalonia's ICGC coverage is the best of every programme checked. That makes **a second Catalan city the only transfer that is certainly affordable before 18 Dec**, with **Valencia or Madrid** as the real cross-country test (Spain's 3rd PNOA coverage now reaches 5 pts/m²), and **non-European cities viable on data but not on framing**.

---

## 0. The checks came back (18 Oct)
Every item below was **downloaded and opened**, not read off a landing page; the two decisive Florence findings were then adversarially re-checked and both were **confirmed**. Full evidence: `databases/data_inventory.md` §6.

- **Florence's pluvial blocker is gone.** The PGRA has no pluvial layer over Florence — its own "Alluvioni pluviali (A12)" and "A15" past-flood layers hold **zero polygons inside the Florence bbox** — but **Pacetti et al. (2022) published their Pluvial Flood Index as supplementary material**, downloaded, no login, a KML ground overlay covering the whole comune. Caveats: a **relative 1–42 colour rank**, not depth or return period, and **CC BY-NC-ND 4.0**, so the right to publish a derived raster is unresolved.
- **Florence's point-cloud blocker is confirmed**, and the re-check made it firmer. The only public cloud is the 2008 Arno lot: **unclassified, ~1.7–2.4 pts/m²**, flown across a leaf-off-to-leaf-on window, and it **misses the built-up city** (centro storico, Novoli, Rifredi, Campo di Marte, Gavinana all fall on "nuvola di punti non disponibile" sheets). But the city **does** publish an open **leaf-on CHM**: DSM and DTM from a **27 Jun 2023** flight, whole municipality, CC BY 4.0.
- **Three more Florence inputs are verified in hand**: the hydrologic soil group (field `gi` of the DB Pedologico, 324 polygons inside the comune), the **LSPP 1 km a/n grid** (read: a = 47.532, n = 0.25641 at the centre → h(1 h, T20) = 47.5 mm), and the tree inventory (82,324 features, daily refresh, still no height).
- **A new dataset changes the shape of the problem**: *Life Escapos — Alberature pubbliche* (Feb 2026), **1,459 trees with measured `lai`, `dbh_cm`, `h_m`, `crn_w_m`, `can_h_m`, `canopy_area_m2`**, in Firenze Nova — inside Pacetti's own D5 Rifredi–Novoli pilot district. See §7.
- **Bologna is out, now on its own documents.** An agent was told to **refute** the disqualification and failed. The LIFE+ **BLUE AP** strategy states that *"grazie alla struttura della rete di drenaggio di Bologna … le aree soggette a rischio idraulico sono poche e di estensione limitata"*, and **all seven named critical nodes are watercourses**; "allagamenti" appears once in 2,292 lines, with no map. Its PGRA "RSP" layer is a **reclamation-channel** product (every Bologna polygon names a *scolo*) and it has **no IDF product at all**. Only its LiDAR improved — see §3.

## 1. The screening rule
From `notes/transferability.md` §2–3, in order of severity:

| # | Criterion | Why it ranks here |
|---|---|---|
| 1 | **Classified, leaf-on, high-density point cloud** | The LAI proxy is a gap fraction of points inside the crown. A DSM raster cannot give it, and a leaf-off flight makes it meaningless. This is the input that eliminates most cities |
| 2 | **Public pluvial flood map** (depth or hotspot index) | Our routing is not a substitute (ROC AUC 0.52 vs RESCCUE). Without it the *placement* half of the method loses its target |
| 3 | **Open inventory with species and position** | The one input the method cannot derive |
| 4 | **Both hazards in the same streets** | The thesis premise |
| 5 | Design rainfall (IDF) | Usually solvable; a gauge-fitting step at worst |
| 6 | A policy driver (species cap, replacement programme) | Makes the decision variable real, as Barcelona's 15% cap does |
| 7 | Csa climate | Keeps the interception constant, the leaf calendar and the storm season inside their anchors (§4 of the transferability note) |

## 2. What the national programmes decide (the new finding)
Criterion 1 is set nationally, not by the city. This is what the check turned up:

| Programme | Density | Classified | Season | Verdict for the LAI proxy |
|---|---|---|---|---|
| **ICGC Territorial LiDAR v3, Catalonia** | **≥8 pts/m²** ✅ (1st and 2nd coverages were 0.5) | ✅ | Flights **24 Apr 2021 – 20 Nov 2023**, 159 missions ✅; per-tile dates in the ICGC tool. Porta's tiles: **26 Sept 2021, leaf-on** ✅ | **Best found.** Covers all of Catalonia |
| **PNOA-LiDAR 3rd coverage, Spain** | **5 pts/m²** nationwide 🟡 (2nd coverage was 0.5–2) | ✅ NPC02 | 2022–2025; Valencia flown **Aug 2023 – Jun 2024** 🟡; Madrid and Andalucía finished 2024 🟡 | **Usable.** Per-tile season must be checked (the window spans summer and winter) |
| **IGN LiDAR HD, France** | 10 pts/m² ✅ | ✅ (3 vegetation height classes) | **"Mostly autumn and winter"** per IGN dataset pages 🟡; one documented acquisition flown 2–3 March 2022, and leaf-off is described as an *advantage* for ground capture 🟡 | **Fails criterion 1** as a rule. Only a leaf-on tile would do, and the programme is built the other way |
| AHN, Netherlands | high | ✅ | leaf-off by design ❌ not re-verified here | Same problem as France |
| Italy (regional) | patchy | varies | varies | Tuscany: **1 m DTM/DSM rasters documented, point cloud not** (F3) |
| Germany (state-level) | varies | varies | not checked | Not checked |

Criterion 2 is also largely national:
- **Switzerland:** a **nationwide surface-runoff hazard map** (FOEN + insurers), depth classes <0.1 / 0.1–0.25 / ≥0.25 m plus flow paths, >100-yr scenario, publicly viewable ✅; an update adds depth, velocity and direction for 30-, 100-, 300-year and extreme events 🟡.
- **Netherlands:** national water-depth maps for 70 mm/1 h, 90 mm/1 h and 155 mm/2 h at **0.5 m**, as open data in the Klimaateffectatlas, announced for July 2026 🟡 (publication not confirmed).
- **New York City:** **NYC Stormwater Flood Maps** (DEP), citywide, four scenarios from Limited (1.77 in/h) to Extreme (3.66 in/h) with sea-level variants ✅; licence unspecified 🟡.
- **Germany:** no national pluvial map, but **KOSTRA-DWD-2020** gives the whole country a free design-rainfall raster (5 km, EPSG:3035, ASCII/vector) ✅ — criterion 5 solved nationally.
- **Spain / Italy / France:** official flood mapping is fluvial (ARPSI, PGRA, TRI). Catalonia's ACA reports having **incorporated 44 municipalities with pluvial risk** alongside its 15 fluvial ARPSIs 🟡 — the list itself was not reachable in search and is the single most useful open check in this note.

## 3. Shortlist
Scores are judgements on the evidence above, 1–5, same convention as `notes/city_screening.md`. "Point cloud" is criterion 1, "Pluvial map" criterion 2.

| Candidate | Point cloud | Pluvial map | Inventory | Dual hazard | Csa | Policy driver | Feasible by 18 Dec | Verdict |
|---|---|---|---|---|---|---|---|---|
| **A second Catalan city** (Girona, Terrassa, Sabadell, Mataró, Badalona, Tarragona, Reus…) | **5** (ICGC ≥8 pts/m², same as Porta) | 3 (ACA's 44 pluvial-risk municipalities 🟡; needs the list) | 4 (Girona publishes trees with scientific name, yearly CSV since 2014 ✅; the others unchecked) | 3–4 (to establish per city) | 5 | 3 (no 15% cap found outside Barcelona; the city's own tree plan would have to serve) | **5** | **Recommended.** The only transfer certain to fit the calendar |
| **Valencia** | 4 (PNOA 5 pts/m², NPC02 published; season per tile 🟡) | 2 (no open pluvial map found; municipal drainage plan not open) | 4 (open inventory ✅; press figures on species inconsistent 🟡) | 5 | 5 | 3 | 3 | **Best cross-country test** if the pluvial map can be sourced |
| **Madrid** | 4 (PNOA, published 🟡) | 2 | 4 🟡 | 4 (heat extreme; pluvial weaker) | 5 | 3 | 3 | Second choice to Valencia |
| **Florence** (incumbent) | **2** (verified: open cloud is 2008, unclassified, ~2 pts/m², misses the city; open leaf-on **CHM** yes, cloud request-only) | **4** (Pacetti PFI downloaded; rank-only, CC BY-NC-ND) | 5 (82,324 trees ✅, daily) | **5** (best documented of all) | 5 | 2 | 4 (data already inventoried) | **Keep as fallback**; resolve its two checks first |
| **Lisbon** | 2 (not checked) | 3 (PGDL 2016–2030 has a flood-vulnerability map 🟡; ~6% of the municipality classed highly vulnerable 🟡) | 4 (94,286 street trees in Mar 2021, **67,854 with species**, 26,432 without ✅) | 3 (**season conflict**: the documented floods are winter, when the deciduous palette is bare — flagged already in `city_screening.md`) | 5 | 2 | 2 | Weak: the season conflict undercuts the premise |
| **Swiss city** (Geneva, Lugano) | 3 (not checked) | **5** (nationwide surface-runoff map) | 2 (not checked) | 3 | 1–2 (Cfb/Cfa) | 2 | 2 | Great hazard data, wrong climate |
| **German city** (Berlin, Hamburg, Köln) | 2 (not checked) | 3 (city Starkregen maps, not checked) | **5** (Berlin: species, genus, **crown diameter**, trunk circumference, height; ~406,544 street trees 🟡; licence varies) | 3 | 1 | 2 | 2 | Best inventories in Europe, wrong climate, unchecked LiDAR |
| **Vienna** | 2 (1 m DSM/DTM used by third parties; season unknown 🟡) | 2 (not checked) | **5** (≈480,000 trees: species, planting year, trunk **and crown** diameter, height, CC BY 4.0 🟡) | 3 | 1 | 2 | 2 | Same as above |
| **Bologna** | **3** (leaf-on Jun 2023 city survey; metadata names "LAS classificati", CC BY 4.0 / public access — but **not served**, request-only) | **1** (verified: PGRA "RSP" = reclamation channels; BLUE AP maps no pluvial areas) | 5 (87,285 trees, species + height class) | **1** (flood type, confirmed against the city's own BLUE AP) | 3 | 2 | 4 | **Drop — on hazard, not on data** |

## 4. The non-European check (asked for explicitly)
**Yes, it can work — and on two criteria it works better than Europe.** It fails on framing, not on data.

| City | What it has | What breaks |
|---|---|---|
| **New York City** | The **best pluvial map of any city checked**: citywide DEP Stormwater Flood Maps, four rainfall scenarios ✅. 2015 Street Tree Census with species and diameter, open (counts differ by source: 584,036 live + 8,036 dead on GBIF vs 666,134 on NYC Open Data 🟡). Classified city LiDAR ✅, but the 2017 topographic flight was **May 2017, ~50% leaf-off** 🟡 | Climate is Cfa, not Csa: the interception constant, the leaf calendar and the storm season all lose their anchors (T3 in the transferability note, which the thesis does **not** claim). Licence on the flood maps unspecified |
| **Melbourne** | Open "trees with species and dimensions" ✅. And a striking parallel: one study of eight cities' open inventories reports **Platanus × acerifolia at 34% of the city-centre stock** 🟡 — the same over-reliance on plane trees that drives this thesis | Cfb climate. No overland-flow map found in the search (likely held by Melbourne Water). 16,000 km away: no site visit, no municipal contact |
| **Adelaide / Perth** | **Genuinely Mediterranean (Csa/Csb)**, so the climate anchors hold. Adelaide street trees are open under CC BY with **species, common name, height and age** ✅; Perth publishes 17,075 trees CC BY 4.0 ✅ | Both datasets cover only the central council area, not the metropolitan region. Pluvial mapping and LiDAR not checked. Same distance problem |

**The argument that deserves a sentence in the thesis:** three of the seven palette species — *Jacaranda mimosifolia*, *Tipuana tipu*, *Melia azedarach* — and *Brachychiton populneus*, which is **native to Australia**, are standard street trees in Australian cities, and the Australian literature already underpins this methodology (Grey et al. 2018, Thom et al. 2020/2022 in Melbourne; Sanusi & Livesley 2020; Kaluarachchi et al. 2020 in Sydney). So the **trait transfer to an Australian Csa city could be better than to Florence**, where the dominant species (*Quercus ilex*, *Olea*, *Cupressus*) have no values at all. 🟡 — the palette-overlap claim is not yet measured; `scripts/species_coverage.py` and `scripts/transfer_species_overlap.py` would settle it in an hour against Adelaide's open CSV.

**Why it should still not be the December transfer:** no site access, no municipal contact, a different policy world, and a tutor and programme anchored in European practice. It belongs in the discussion chapter as evidence that the method is not Europe-specific, not in the 2–10 Dec work package.

## 5. Recommendation — revised after the data search

**The call: keep Florence as the transfer city, and add one Catalan city as the insurance policy. Do not pick Valencia or a non-European city this December.**

Why Florence survived its own bad news: of the four inputs, **three are verified open and in hand** (trees, 1 km IDF grid, soil groups) and the fourth — the pluvial target — turned out to be **published**, not request-only. What is missing is one input, the point cloud, for which Florence has two routes the other candidates do not: an **open leaf-on CHM already published**, and **1,459 trees with measured LAI** sitting inside the very district Pacetti nominates as the pluvial pilot. No other candidate has a measured-LAI dataset at all.

Why not Bologna, despite its better cloud: its leaf-on classified LAS is the more openly licensed of the two Italian options, but it fails criteria 2 and 4 — **the thesis premise**. A transfer city with no pluvial hazard to target and no design rainfall is not a cheaper Florence; it is a different thesis.

Why add a Catalan city anyway: Florence's remaining input depends on a **municipal reply inside a nine-day window** (2–10 Dec). A second Catalan city needs no reply at all — it inherits Barcelona's ≥8 pts/m² leaf-on ICGC cloud, which is the best of every programme screened. It is academically the weaker test (same climate, same data pipeline), so it is the **fallback, not the headline**.

Then, unchanged from v1:
1. **Do one transfer, not two.** `notes/methodology.md` §10 allots 2–10 Dec (9 days) to Sant Antoni *and* Florence. That is already optimistic; adding a third city is scope the calendar cannot absorb.
2. **Make it a second Catalan city.** It inherits the ≥8 pts/m² ICGC point cloud, the regional rainfall context and the species palette, so what changes is exactly what a transfer test should change: a different tree stock, a different street geometry, a different hazard pattern and a different municipality. Be explicit about the limit: this tests **site** transfer, not **climate** transfer.
3. **Resolve Florence's two checks this week anyway.** If the Tuscany point cloud exists and Pacetti's map arrives, Florence returns as the stronger test (different country, documented dual hazard) and the Catalan city becomes the cheap backup.
4. **Name Valencia as the stated next step** in the thesis: Csa, PNOA 5 pts/m² published, open inventory, real dual hazard — blocked only on a pluvial map.
5. **Drop Bologna** on flood type, quoting its own BLUE AP; that is now a documented argument, not an inference.

## 7. The check that would change everything (do this before any email)
The LAI proxy is the only reason a classified point cloud is criterion #1. Florence now offers a way to test whether it has to be:

**Fit `lai ~ species + crown width + height` on the 1,459 Life Escapos trees**, then read crown width and height for the same trees off the **open, leaf-on 2023 CHM** (DSM−DTM, CC BY 4.0) and check the error against the measured LAI.

- If the fit is adequate, **the point cloud leaves the critical path** — for Florence *and* for every future transfer city — and the screening rule in §1 collapses from "a classified leaf-on point cloud" to "an open leaf-on CHM plus an inventory", which most European cities have.
- It needs **no permission, no email and no waiting**; both inputs are already open.
- It is also a methodological result in its own right: it would let the thesis state how much of the Porta LAI proxy is really species-and-geometry, which is the question the LiDAR-proxy limitation in `notes/methodology.md` §4b already raises.

If the fit fails, Florence needs the Comune's 27 Jun 2023 cloud, and the request must ask about **points/m², returns per pulse and whether vegetation returns are retained** *before* licence — a leaf-on classified cloud thinned to ground + first pulse cannot produce a gap fraction.

## 6. Open checks, cheapest first
- [ ] **ACA's list of the 44 municipalities with pluvial risk** (the press note cites it; the list is in the ACA planning-cycle annexes on aca.gencat.cat). Cross it with Catalan cities that publish a tree inventory → this alone produces the shortlist for recommendation 2.
- [ ] Girona, Terrassa, Sabadell, Mataró, Badalona, Tarragona: does each publish an **open tree inventory with species**? (Girona ✅ confirmed; the rest unchecked.)
- [ ] ICGC per-tile **flight dates** for the candidate city: leaf-on or not? (The ICGC tool and the SHP of tile dates give it, as for Porta.)
- [ ] Florence: does Regione Toscana publish the **point cloud**, and in which season? Ask Pacetti et al. for the PFI map.
- [ ] Valencia: is any **pluvial** flood or drainage-model output public, or obtainable from the Ajuntament or the Confederación Hidrográfica del Júcar?
- [ ] Cheap and interesting: run `scripts/transfer_species_overlap.py` against **Adelaide's** open street-tree CSV to measure the palette overlap claimed in §4.

## Sources (web, checked 18 Oct 2026)
- ICGC Territorial LiDAR v3.1 2021–2023 (metadata, ≥8 pts/m², flight window): https://catalegs.ide.cat/geonetwork/srv/api/records/lidar-territorial-v3r1-2021-2023?language=eng and https://www.icgc.cat/en/Geoinformation-and-Maps/Data-and-products/Elevations/Territorial-elevations/Territorial-LiDAR ; 159 missions: https://govern.cat/salapremsa/notes-premsa/652442/
- PNOA-LiDAR 3rd coverage (5 pts/m², status by region): https://pnoa.ign.es/pnoa-lidar/tercera-cobertura , https://pnoa.ign.es/pnoa-lidar/especificaciones-tecnicas , https://blog.idee.es/archivo/-/blogs/nuevos-productos-lidar-de-la-3-cobertura-del-pnoa
- IGN LiDAR HD (classification, season): https://geoservices.ign.fr/lidarhd , https://www.data.gouv.fr/datasets/lidar-hd-ign-2022 , https://www.ign.fr/institut/programme-lidar-hd-vers-une-nouvelle-cartographie-3d-du-territoire
- Swiss surface-runoff hazard map: https://www.bafu.admin.ch/bafu/en/home/topics/natural-hazards/hazard-situation-and-land-use/naturgefahren-karten/surface-runoff-risk-map.html ; update: https://www.ebp.global/ch-en/projects/mapping-surface-runoff-hazards-switzerland-and-liechtenstein
- Netherlands national water-depth maps: https://omgevingsweb.nl/nieuws/nieuwe-landelijke-kaarten-tonen-waterdiepte-bij-hevige-buien/
- KOSTRA-DWD-2020 open data: https://dwd.de/DE/leistungen/kostra_dwd_rasterwerte/download/kostra_dwd_2020_anwenderhilfe_pdf.pdf
- ACA, 44 pluvial-risk municipalities: https://govern.cat/gov/notes-premsa/763628/
- Girona open tree data: https://www.girona.cat/opendata/dataset/arbrat
- Valencia open tree data: https://valencia.opendatasoft.com/explore/dataset/arbratge-arbolado/
- Lisbon trees (94,286 / 67,854 with species, Mar 2021): https://www.isa.ulisboa.pt/ceabn/uploads/docs/projectos/lxtree/Adenda_LxTree_Relatorio_Final_Marco2022.pdf ; drainage plan: https://planodrenagem.lisboa.pt/sobre-o-plano
- Berlin tree cadastre: https://fbinter.stadt-berlin.de/fb_daten/beschreibung/baumbestand.html ; Vienna: https://www.wien.gv.at/umweltgut/public/grafik.aspx?ThemePage=11
- NYC Stormwater Flood Maps: https://data.cityofnewyork.us/Environment/NYC-Stormwater-Flood-Maps/9i7c-xyvv ; 2015 Street Tree Census: https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh ; 2017 NYC topobathy LiDAR (May 2017, ~50% leaf-off): https://www.fisheries.noaa.gov/inport/item/64728
- Melbourne trees: https://data.melbourne.vic.gov.au/explore/dataset/trees-with-species-and-dimensions-urban-forest/ ; eight-city inventory study (plane 34% of the centre): https://www.sciencedirect.com/science/article/pii/S1618866721001242
- Adelaide street trees: https://data.sa.gov.au/data/dataset/street-trees ; Perth: https://catalogue.data.wa.gov.au/dataset/perth-trees-in-the-city
