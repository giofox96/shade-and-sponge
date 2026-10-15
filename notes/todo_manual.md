# Manual to-do (things only you can do)

*8 Oct 2026, updated 15 Oct. Tick items off here, or tell me and I'll update the file. Where a file should go, it's named in each item.*

## Leaf state of Tipuana and Jacaranda, Nov–Mar (decides the size of the winter-sun result)
The user lives in Florence (15 Oct), so **no field photos in Porta**. Remote alternatives, which a Claude session can do:
- [x] Dated **iNaturalist** observations of *Tipuana tipu* and *Jacaranda mimosifolia*, Dec–Mar: **done 15 Oct** (`notes/decisions/leaf_state_inat.md`): 170 Barcelona photos scored. Tipuana is in leaf in January (base case holds); **Jacaranda is mostly in leaf in January too**, not bare as the tool assumes. Why: the no-regret winter gain is −9% if Tipuana stays leafed in January and only −2% if it is bare (`shade_sponge/README.md`, sensitivity).
- [ ] If iNaturalist is too thin: winter Google Street View captures of Porta's Tipuana and Jacaranda streets (check the capture date shown in Street View).
- [ ] **Decide:** adopt the photo-based leaf calendar proposed in `notes/decisions/leaf_state_inat.md`, then re-run the tool and its sensitivity **locally** (raw site data are not in cloud sessions) to see whether the Tipuana → Jacaranda no-regret swap survives.

## Before the 20 Oct meeting

### Decisions only you can take (memos ready; most give a recommended default)
- [ ] **Heat metric f1:** mean UTCI over 12–17 h on the DDY cooling day instead of one peak hour? Minimum difference = 0.8 °C (Ladybug vs ENVI-met MBE)? (`notes/decisions/heat_objective.md` §6)
- [ ] **Weather forcing:** El Prat TMYx 2011–2025 for the main run, with city station / city-terrain wind / +1.5 °C as sensitivities? (`notes/decisions/weather_forcing.md` §4)
- [ ] **H3:** declare it a boundary of the method (and reword slide 9, "as H3 predicts", and methodology §4b, "supporting H3"), or keep it testable on the Freiburg raw data? (`notes/decisions/hypothesis_tests.md` §9)
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
  - [ ] Ask the tutor: is a hypothesis that is true by construction of the model (H3) acceptable if declared as a method boundary?
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
