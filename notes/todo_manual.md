# Manual to-do (things only you can do)

*8 Oct 2026. Tick items off here, or tell me and I'll update the file. Where a file should go, it's named in each item.*

## Field check, Nov–Mar (decides the size of the winter-sun result)
- [ ] **Leaf state of Tipuana and Jacaranda in Porta**, every 2–3 weeks from mid-Nov: photograph 5 trees of each from the same spot (one standard frame, sky behind the crown), and note the date and an estimate of leaf cover (0 / ¼ / ½ / ¾ / full). Nou Barris also has 11 Tipuana trees of local interest in Plaça del Virrei Amat (name in the city tree catalogue; possibly renamed Plaça Salvat-Papasseit in 2026, unconfirmed). Save to `databases/barcelona/field_phenology/` as `<species>_<YYYYMMDD>_<n>.jpg` + one `log.csv`. Why: the no-regret winter gain is −9% if Tipuana stays leafed in January and only −2% if it is bare (`shade_sponge/README.md`, sensitivity). The same photos can also give the leafless crown opacity (sky gap fraction).

## Open: data licence on the public web app
- [ ] **Flood-hazard index licence.** The public app (https://giofox96.github.io/shade-and-sponge/) shows the hotspot layer derived from the Barcelona Resilience Atlas flood-hazard index (index ≥ 40). The source states no licence. Kept online for now (your decision, 9 Oct) with credit to Barcelona Regional. Later: ask Barcelona Regional / the Urban Resilience office for the terms, or remove the overlay (`shade_sponge/web_export.py`, layer `hotspots`).

## Before the 20 Oct meeting

### Requests that take time: send them first
- [ ] **TRY data request** (try-db.org): the 21 species in `databases/traits/porta_trait_table.csv`. Ask for leaf phenology type, leaf area, wood vessel anatomy (ring- or diffuse-porous) and leaf wettability / water storage. Save the reply in `databases/TRY_DATABASE/` (git ignores it). Approval can take weeks, so nothing waits on it.
- [ ] **Email the tutor** (one email, or bring it to the meeting):
  - [ ] RESCCUE / Barcelona Regional **flood depth maps** (T = 1, 10, 100 yr) as GIS layers. The viewer needs a city login, which I can't and shouldn't use.
  - [ ] **Infrared City access**, plus three questions: (a) how are trees represented: geometry only, or porosity/LAI per species? (b) API limits for thousands of runs; (c) published validation against ENVI-met or Ladybug.
  - [ ] Confirm the **final delivery date** (18 Dec?), and whether **Grasshopper integration** is required by the programme.
  - [ ] Slide format for the 5-min talk (Google Slides assumed).

### Papers (download in the browser via IAAC access; save to `papers/` and tell me, I'll digest them)
These carry the gap and evidence slides. **First, the backup slide on tree pits** (`slides/outline_20oct.md` B1):
- [ ] Grey et al. 2018, tree pits to mitigate runoff in dense urban areas. https://doi.org/10.1016/j.jhydrol.2018.08.038
- [ ] Thom et al. 2020, tree transpiration and the efficiency of stormwater control measures. https://doi.org/10.1016/j.watres.2020.115597
- [ ] Thom et al. 2021, choosing species with high transpiration for passively irrigated pits. https://doi.org/10.1016/j.scitotenv.2021.151466
- [x] Bartens et al. 2008, tree roots and infiltration through compacted subsoil: read in full on 8 Oct (also Rahmi et al. 2025). Roots do raise infiltration, but oak vs maple did not differ.

Then the gap and evidence papers:
- [x] Mannucci 2025, Shaamala 2025, Peng 2026, Wu 2024, Xiao & McPherson 2016, Baptista 2018, Silva 2025: read in full on 8 Oct. The gap holds. Wu 2024 does heat + runoff, but with surface temperature, by scenario, without species and without optimisation.
- [x] 16 more papers read in full on 8 Oct: Yang, Llorens & Domingo, Zabret & Sraj, Coville, Kuehler, Huang, Zhang, Marrazzo & Raimondi, Song, Liu, Berland, Bruner, Yadav, Wang, Quagliolo, Cremonini. Three PDFs in `papers/` are exact duplicates and can be deleted: `Increase and Spatial Variation in Soil Infiltration.pdf`, `Variation in leaf area density drives the rainfall storage capacity of individual urban.pdf` (= Baptista 2018), `Surface Water Storage Capacity of Twenty Tree Species in davis california.pdf` (= Xiao 2016).
- [x] 15 more papers read in full on 9 Oct (Hao 2023, Elkhateeb 2025, Oneto 2026, Zölch 2019, Sanusi & Livesley 2020, Huang 2022, Rochette Cordeiro 2026, Cortinovis 2022, Livesley 2016, Rombeek 2025, Axelsson 2020, Morabito 2016, Esposito 2024, Campanale 2025, Petralli 2006). The gap holds: the new optimisers are heat-only. `to_get_manually.md` now lists what is still missing, the 12 that matter first at the top. Livesley 2016 is in `papers/` twice (same paper, two different downloads), also listed there.
- [ ] **Tan et al. 2026**, multi-objective tree configuration: the last one that could overlap our gap. https://doi.org/10.1016/j.scs.2026.107726
- [ ] Selbig et al. 2021: the field benchmark (slide 4 and slide 9; abstract 4%, Coville et al. 2022 report 3.5% from the same data). https://doi.org/10.1016/j.scitotenv.2021.151296
- [ ] **Santos Nouri et al. 2018**, *Tipuana tipu* and thermal comfort in Lisbon canyons (PET −15.6 °C, cited in Silva 2025). Open access on MDPI. It would give a second candidate species a cooling value. https://doi.org/10.3390/atmos9010012
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
- [ ] Field check of crown temperature / MRT in Porta: probably not possible before December (no hot days). Decide whether to drop it.

## Housekeeping
- [ ] The Zotero MCP server timed out in this session. Restart Claude Code; if it fails again, check that `npx` works in a new terminal. Adding papers through `scripts/zotero_add.py` doesn't depend on it.
- [ ] Optional: delete `databases/barcelona/raw/2017_NDVI.tif` (1.6 GB). The Porta crop the model uses is already saved.
