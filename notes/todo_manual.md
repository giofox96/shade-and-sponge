# Manual to-do (things only you can do)

*8 Oct 2026, updated 24 Oct. Tick items off here, or tell me and I'll update the file. Where a file should go, it's named in each item.*

## Fast track to the 10 Nov tutor session (only you can do these; in order)
1. [ ] **Watch for the Parcs i Jardins reply** (sent 24 Oct). Forward it to me as soon as it arrives: a current per-street list would replace S1.
2. [ ] **Download 3 papers into `papers/`** (open access or IAAC access):
   - Nieuwenhuijsen et al. 2022, *Environ. Res.* 215:114387 (3-30-300 in Barcelona; open PDF: https://ddd.uab.cat/pub/artpub/2022/284178/284178.pdf);
   - Santamour 1990 (10-20-30 rule);
   - Kendal, Dobbs & Lohr 2014 (diversity benchmarks, 108 cities).
3. [ ] **Ladybug Tier 1 on one Porta street, S0 vs one replacement** (≈1 evening). This is the first real UTCI number for the deck: mean UTCI 12–17 h, hot design day. I prepare the files in `exchange/to_gh/` and you run it in Grasshopper. Tell me which day you can do it.
4. [ ] **RM cluster map by hand on Miro, by Tue 27 Oct** (below).
5. [ ] **Ask the tutor by email (one line):** is Infrared City access possible before 10 Nov? If yes, it replaces item 3.
6. [ ] **Decide the baseline** when I send the research-question memo: S1a (2026 press mix) or S1b (2004 documented table) as the headline.
7. [ ] Pick a day before 10 Nov for a 20-min **dry run of the deck** with me (problem → RQ → flowcharts → first results → validation).

## For the next tutor session, 10 Nov (requests from the 20 Oct session)
Full list: `notes/research_method_guidelines.md`, "Conclusions from the week of 19–24 Oct".
- [x] **Gate 1: does Barcelona already decide which species replaces which tree, and where, by a criterion?** Partly settled 24 Oct: a 2004/2005 rule exists on paper, but Porta's plantings mostly do not follow it (`notes/tree_master_plan.md` §5b). Still waiting on the Parcs i Jardins reply.
- [x] **Are there enough trees?** Porta has 20.1% canopy cover against the city's 30% target (`notes/topic_decision.md` §10.3).
- [x] Problem 100% clear (v7, `notes/topic_decision.md` §10).
- [ ] Research question scrutinised → methodology flowcharts (short) → results + validation → first results. Claude is working on these.

## Due this week (from RM L02 and RT L03, 21–22 Oct)
- [ ] **RM cluster map, redrawn by hand on Miro by Tue ~27 Oct** (reviewed in class Thu ~29 Oct). No AI-generated canvas. Follow one unit (one Porta plane due for replacement), include the topic without the tool, list only papers you have read, 5+ precedents (2 theoretical, 3 practice). Checklist: `notes/research_method_guidelines.md` §H.
- [ ] Read the links Mathilde leaves on Miro (Treepedia, Barcelona tree maps, the nursery's species database) and note the nursery's name.
- [ ] Ask Fiona Demeur whether PEMB / Consorci del Besòs (GreenInCities) hold street-tree or flood data for Nou Barris.

## Leaf state of Tipuana and Jacaranda, Nov–Mar (decides the size of the winter-sun result)
The user lives in Florence (15 Oct), so **no field photos in Porta**. Remote alternatives, which a Claude session can do:
- [x] Dated **iNaturalist** observations of *Tipuana tipu* and *Jacaranda mimosifolia*, Dec–Mar: **done 15 Oct** (`notes/decisions/leaf_state_inat.md`): 170 Barcelona photos scored. Tipuana is in leaf in January (base case holds); **Jacaranda is mostly in leaf in January too**, not bare as the tool assumed.
- [ ] If iNaturalist is too thin: winter Google Street View captures of Porta's Tipuana and Jacaranda streets (check the capture date shown in Street View).
- [x] Photo-based leaf calendar **adopted (15 Oct)** and written into `databases/traits/phenology_palette.csv`.
- [x] **Tool and sensitivity re-run locally (15 Oct):** the Tipuana → Jacaranda no-regret swap shrinks from −9% to −2% winter shade and vanishes in 3 of 8 variants; the summer–winter trade-off beyond the balanced layout is robust (`shade_sponge/README.md`). Street View check no longer needed for the tool.

## Open: data licence on the public web app
- [ ] **Flood-hazard index licence.** The public app (https://giofox96.github.io/shade-and-sponge/) shows the hotspot layer derived from the Barcelona Resilience Atlas flood-hazard index (index ≥ 40). The source states no licence. Kept online for now (your decision, 9 Oct) with credit to Barcelona Regional. Later: ask Barcelona Regional / the Urban Resilience office for the terms, or remove the overlay (`shade_sponge/web_export.py`, layer `hotspots`).

## Before the 20 Oct meeting

### Decisions only you can take (memos ready; most give a recommended default)
- [x] **Heat metric f1: DECIDED 19 Oct — mean UTCI over 12–17 h on a hot design day**, hottest real day as a check (`notes/topic_decision.md` §8). Still open inside it: the minimum meaningful difference (0.8 °C, Ladybug vs ENVI-met MBE).
- [ ] **Weather forcing:** El Prat TMYx 2011–2025 for the main run, with city station / city-terrain wind / +1.5 °C as sensitivities? (`notes/decisions/weather_forcing.md` §4)
- [x] **H3: DECIDED 19 Oct — withdrawn as a hypothesis**, kept as a declared validity boundary of the method; the talk says it was a hypothesis until the model showed it true by construction (`notes/topic_decision.md` §8). Anything still reading "supporting H3" or "as H3 predicts" is wrong.
- [ ] **H1/H2 wording:** Δmin = 91 m³ and the "not resolved" rule for H1's runoff part (provisionally accepted 14 Oct; still to write into `topic_decision.md` §7); H2 as a species-composition claim (`notes/decisions/hypothesis_tests.md` §8, `runoff_metric_sensitivity.md` §10).
- [ ] **Contribution statement:** pick A (method), B (knowledge) and/or C (validation); use the narrower gap wording because of Dong 2026 (`notes/decisions/contribution_statement.md`).
- [ ] **Methodology §12 proposed changes** (surface-weighted shade, SVF check, k as ASSUMPTION, R_OFF anchors, storage anchors for s): adopt or drop (`notes/methodology.md` §12).

### Requests that take time: send them first
- [x] **TRY data request sent** (user, by 15 Oct); waiting for the reply. Request covers the 21 species in `databases/traits/porta_trait_table.csv`. Ask for leaf phenology type, leaf area, wood vessel anatomy (ring- or diffuse-porous) and leaf wettability / water storage. Save the reply in `databases/TRY_DATABASE/` (git ignores it). Approval can take weeks, so nothing waits on it.
- [ ] **Email the tutor** (one email, or bring it to the meeting):
  - [x] RESCCUE **flood depth maps**: found on 13 Oct as public tables (T10, T100, present/future) in the atlas's CARTO account, no login needed (`databases/data_inventory_barcelona.md` B1). Still worth asking: licence for thesis use, and whether a T = 1 yr run exists.
  - [x] **Sent 13 Oct: RESCCUE licence email** to br@bcnregional.com; waiting for the reply; reminder by ~23 Oct if none (text and steps: `notes/resccue_data_request.md`).
  - [ ] **Infrared City access**, plus three questions: (a) how are trees represented: geometry only, or porosity/LAI per species? (b) API limits for thousands of runs; (c) published validation against ENVI-met or Ladybug.
  - [ ] Confirm the **final delivery date** (18 Dec?), and whether **Grasshopper integration** is required by the programme.
  - [ ] Slide format for the 5-min talk (Google Slides assumed).
  - [ ] Ask the tutor (now on slide 12): we removed H3 because it is true by construction of the model and declared it a boundary instead — is that the right call?
- [ ] **RESCCUE licence reminder ~23 Oct** if Barcelona Regional has not replied (`notes/resccue_data_request.md`).

### Papers (download in the browser via IAAC access; save to `papers/` and tell me, I'll digest them)
These carry the gap and evidence slides. **First, the backup slide on tree pits** (`slides/outline_20oct.md` B1):
- [x] Grey et al. 2018, tree pits to mitigate runoff in dense urban areas: read in full on 9 Oct.
- [x] Thom et al. 2020, tree transpiration and the efficiency of stormwater control measures: read in full on 9 Oct.
- [x] Thom et al. 2022 (online 2021), choosing species with high transpiration for passively irrigated pits: read in full on 9 Oct. Backup slide B1 is now backed by all four pit papers.
- [x] Bartens et al. 2008, tree roots and infiltration through compacted subsoil: read in full on 8 Oct (also Rahmi et al. 2025). Roots do raise infiltration, but oak vs maple did not differ.

Then the gap and evidence papers:
- [x] Mannucci 2025, Shaamala 2025, Peng 2026, Wu 2024, Xiao & McPherson 2016, Baptista 2018, Silva 2025: read in full on 8 Oct. The gap holds. Wu 2024 does heat + runoff, but with surface temperature, by scenario, without species and without optimisation.
- [x] 16 more papers read in full on 8 Oct: Yang, Llorens & Domingo, Zabret & Sraj, Coville, Kuehler, Huang, Zhang, Marrazzo & Raimondi, Song, Liu, Berland, Bruner, Yadav, Wang, Quagliolo, Cremonini. Three PDFs in `papers/` were exact duplicates (deleted 12 Oct): `Increase and Spatial Variation in Soil Infiltration.pdf`, `Variation in leaf area density drives the rainfall storage capacity of individual urban.pdf` (= Baptista 2018), `Surface Water Storage Capacity of Twenty Tree Species in davis california.pdf` (= Xiao 2016).
- [x] 15 more papers read in full on 9 Oct (Hao 2023, Elkhateeb 2025, Oneto 2026, Zölch 2019, Sanusi & Livesley 2020, Huang 2022, Rochette Cordeiro 2026, Cortinovis 2022, Livesley 2016, Rombeek 2025, Axelsson 2020, Morabito 2016, Esposito 2024, Campanale 2025, Petralli 2006). The gap holds: the new optimisers are heat-only. `to_get_manually.md` now lists what is still missing, the ones that matter first at the top. Livesley 2016 is in `papers/` twice (same paper, two different downloads), also listed there.
- [x] **Tan & Liu 2026**: read in full on 9 Oct. Closest precedent (species + positions for UTCI, CO2, diversity), but no runoff: the gap holds.
- [x] Selbig et al. 2021 (issue 2022): read in full on 9 Oct. 4% of runoff and no peak-flow change confirmed.
- [x] **Santos Nouri et al. 2018**: read in full on 9 Oct. Tipuana: PET up to −15.6 °C on a hot day, but it keeps its leaves in winter (as cited), so PET is up to −2.7 °C lower at noon in December.
- (The full list of papers is in `notes/lit/to_get_manually.md`; the T1 ones matter first.)

### i-Tree
- [ ] Your export `databases/traits/raw/i-Tree-Eco_dat.csv` has only ID, code and names (no traits). If i-Tree shows trait columns for a species (leaf type, mature height, growth form, shading), export the species list with those columns. If it doesn't, tell me and we drop i-Tree as a trait source.

### Optional but strong for the talk
- [ ] **One Ladybug test run (Tier 1, S0)** on a small piece of Porta (e.g. one block of Av. Meridiana). Setup and file names are in `exchange/README.md`:
  - EPW: Barcelona El Prat TMYx (LB Download Weather from climate.onebuilding.org);
  - buildings: `exchange/to_gh/porta_buildings.geojson`;
  - crowns: `exchange/to_gh/porta_trees_lidar.csv`.
  
  Put the results in `exchange/from_gh/` and the settings in `exchange/from_gh/run_log.md`. A first UTCI map would show the heat side is working, not only planned.

### Talk
- [ ] Read and sign off PS/RQ/H v4 (`notes/topic_decision.md` §7) and the slide outline (`slides/outline_20oct.md`).
- [ ] Put the figures into Google Slides (PNG versions in `slides/fig/`; SVG if you want to edit them).
- [ ] Rehearse against a 5-min timer, twice.

## After 20 Oct
- [ ] Rain-gauge data: request the BCASA high-resolution gauge series (1994–2019), and/or create a free Meteocat XEMA API key yourself. Both are optional, for replaying real storms.
- [x] ~~Field check of crown temperature / MRT in Porta~~: dropped (user lives in Florence, 15 Oct). Heat validation relies on Ladybug vs ENVI-met and the papers in `notes/method_heat_validation.md`.

## Papers still to get (details in `notes/lit/to_get_manually.md`)
- [ ] Heat validation, T1: Lopez-Cabeza et al. 2025 (open access, Huelva repository) and Lindberg & Grimmond 2011.
- [ ] Published version of Kuehler et al. 2017 (only the accepted manuscript is read). Llorens & Domingo 2007 is read; only its value extraction is open.
- [ ] Speak 2020 supplementary per-tree table (not in `papers/`).
- [ ] Zotero by hand ("Add Item by Identifier"): Eslami, Sciuto (Zenodo DOI) and Schrodi (arXiv DOI), which have no Crossref record (`notes/handoff_papers.md`).

## Housekeeping
- [ ] The Zotero MCP server timed out in this session. Restart Claude Code; if it fails again, check that `npx` works in a new terminal. Adding papers through `scripts/zotero_add.py` doesn't depend on it.
- [ ] Optional: delete `databases/barcelona/raw/2017_NDVI.tif` (1.6 GB). The Porta crop the model uses is already saved.

## Catalan transfer city: four portals blocked from the cloud container (18 Oct)
The screening in `notes/catalan_transfer_city.md` settled everything except one criterion, and it needs a browser on Windows — about 30 minutes, no emails, no requests. **Does the city publish a street-tree inventory with species?** In priority order:

**Corrected 18 Oct after the fact-check: only two are actually blocked, and the recommendation changed.**

- [ ] **Mataró — the three URLs that settle the transfer city (19 Oct, see `notes/catalan_transfer_city.md` §3b).**
  All three are on `apex.mataro.org`, which is genuinely proxy-blocked from the container — **blocked, not absent**.
  Mataró's inventory is known to exist: its own map viewer reads it from these endpoints without a key.
  1. `https://apex.mataro.org/ords/sig/geodades/T_C_ARBRAT?limit=50000` — **the decisive one.** Does it return one
     JSON object per tree with `ESPECIE` and a `WKT` point? And are `ALCADA` / `DIAMETRE` / `PERIMETRE` populated
     for species other than *Melia*? (If height or DBH is populated, it also rescues the LiDAR-proxy validation
     that the Escapos check failed to provide.) Save the JSON.
  2. `https://apex.mataro.org/dadesobertes` — **the licence**, and whether a packaged CSV/GeoJSON of the tree layer
     is published. Equal priority to #1: the data is unusable without reuse terms, and `mataro.cat/ca/legal` is
     restrictive by default.
  3. `https://apex.mataro.org/ords/rest/dobertes/elements` — the dataset-list API; shows what else Mataró publishes.
  If all three fail, request the Safetree extract from the municipality. **Contact caveat:** the phone, hours and
  both mailboxes below are taken from the *plànols* / GeoMat page footer and belong to the **Servei en Sistemes
  d'Informació i Telecomunicacions** (Tecnocampus Mataró Maresme), **not** the Àrea d'Ecologia Urbana as an earlier
  draft said — `bustia@ajmataro.cat` is the generic *Bústia d'avisos* and `planoldelaciutat@ajmataro.cat` the
  map-products request box: `+34 93 758 21 91`, Mon–Fri 08:00–15:00. The addresses are real; the attribution was
  wrong. Confirm the right unit on mataro.cat before writing.
- [x] ~~Mataró portal check~~ — superseded by the three URLs above; the species composition is already in the repo
  (`databases/mataro/mataro_street_tree_species_2016.csv`, 17,204 street trees, 117 species) and 79,748 tree
  positions are downloadable without any portal, from the municipal GeoPackage (EPSG:25831, same CRS as Porta).
- [ ] **Sabadell**: `https://dadesobertes.sabadell.cat/ca/dataset?q=arbrat` (genuinely blocked)
- [x] ~~Badalona~~ — **reachable, and the answer is a near-negative**: its GeoServer lists 161 WMS layers with no tree/green layer and it has no AOC CKAN organisation. Worth one look behind `https://geoportal.badalona.cat/badalona42/visor/geoportal` only if you want to be sure
- [x] ~~Reus~~ — reachable; `https://geoportal.reus.cat/inici/` answers 200, no inventory surfaced

For whichever city answers yes, record: record count, the species field, distinct species, any height/DBH/crown field, licence, last update, download URL.

Two smaller local checks from the same note:
- [ ] Open `https://sig.gencat.cat/ows/AIGUA/wms` (layer `AIGUA_PLUVIAL_ARPSI`) to get the 44-municipality polygon layer **and its licence**, which is still unknown.
- [ ] For the chosen city, download the published 1×1 km `datacloud` LAZ over the study district and histogram per-point GPS date and classification over the full extent, to confirm the clip-service result.

- [ ] **Title-slide photo (20 Oct):** `slides/fig/01_title_photo.webp` (Porta allotments, Carrer d'Alcúdia × Carrer de la Maladeta) came from a web image, so **author and licence are unverified**. Confirm the credit before the booklet, or replace the file with your own photo of the same corner and re-run `scripts/make_infographics.py`.
