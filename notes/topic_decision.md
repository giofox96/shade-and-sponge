# Topic decision: problem, research question, hypothesis (v2, 7 Oct 2026)

> **Update v3 (same day):** a dual heat + runoff version was added in §6 after a second literature round (21 heat papers, rows #35–#55) and a city screening (`notes/city_screening.md`). §1–§5 below are the runoff-only v2, kept as the fallback.

Inputs (v2, 7 Oct): 34 papers in `notes/lit/literature_matrix.csv` (13 read as full-text digests, 21 from abstracts only, marked there; on 8 Oct the matrix has 61 rows, 47 read in full), plus `databases/data_inventory.md`.
Citations below give author, year and the matrix row (#). Claims from abstracts only are marked (abs). **Still to do before 20 Oct:** read the full text of rows #4 and #10 (#3 read on 8 Oct; #18 digested from full text). These carry the argument.

---

## 1. What the literature says about the five known weaknesses

| Weakness in v1 | Evidence | Consequence for v2 |
|---|---|---|
| **Flood type** | Florence: whole city exposed to pluvial and flash floods from the minor network and a ~800 km combined 19th-century sewer; hotspots in flat, highly sealed areas incl. historic centre, validated against historical pluvial events (Pacetti et al. 2022, #18). Emilia-Romagna May 2023: no hourly extremes, multi-day accumulation, return period >500 yr (Scoccimarro et al. 2025, #21); mainly stratiform rain at 2–5 mm/h on saturated soils (Cremonini et al. 2024, #61). Bologna Oct 2024: 160–180 mm/24 h on saturated soils, culverted streams overflowed (Arpae report; see data inventory). Ravone culvert insufficient for intense events (Dottori et al. 2014, #20) | **Florence fits a pluvial framing; Bologna's recent events do not.** v2 names *urban pluvial flooding from frequent short storms* and explicitly excludes multi-day/fluvial events |
| **Testability** ("significantly reduces", "extreme precipitation") | Tree effect is largest for short, low-intensity storms and falls with depth and intensity (leafy crowns hold the first 2–4 mm, Kuehler et al. 2017 #9; Anys & Weiler 2024 #1; per-event interception falls from 87% to 1% as rain depth grows, Song et al. 2020 #12). Catchment experiment: 4% runoff-volume reduction from 31 street trees, **no peak-flow effect** (Selbig et al. 2021 #10); 3.5% of total runoff in the calibrated re-analysis (Coville et al. 2022 #11). NbS effect decays with return period (Costa et al. 2021 #23; Esraz-Ul-Zannat et al. 2024 #32; Liu et al. 2026 #24); the 10-yr storm, the most frequent one modelled, carries 74% of the expected annual flood damage in Aveiro (Quagliolo et al. 2023 #60) | Metric = **event runoff volume** from sealed surfaces (not peak discharge). Storms = **local design storms of 2, 5, 10-yr return period, ≥1 h** (Tuscany LSPP grid; ≥1 h avoids the 15-min aggregation bias, Lompi et al. 2022 #19). Baseline and comparison defined (§4) |
| **Traits vs biomass** | Interception differs strongly between species: storage capacity varies threefold among 20 species (Xiao & McPherson 2016 #3); *Tilia cordata* 70% vs *Acer platanoides* 55% event interception (Anys & Weiler 2024 #1); *Quercus ilex* 46–51% vs *Q. pyrenaica* 10–16% (Hassan et al. 2017 #8 (abs)); birch 23% vs pine 47% (Zabret & Sraj 2019 #7); *Ginkgo* 58% vs *Zelkova* 21%, one tree each (Yang et al. 2019 #5). LAI / leaf area density is the main driver (LAI: Anys & Weiler #1; central-crown LAI and small leaves, not leaf area density: Yang et al. 2019 #5; leaf area density: Baptista et al. 2018 #6); full trait list in Dowtin et al. 2023 #4 (abs) | Supported for *interception*: species traits (storage capacity, LAI, leaf area density) matter, not just size. **Not** supported for roots: only two lab studies (#16, #17). Bartens et al. 2008 (#16, read in full) show that tree roots raise infiltration through compacted subsoil, but black oak (coarse roots) and red maple (fine roots) did not differ significantly. Zhang et al. 2019 (#17, read in full) found +118% (tap-rooted *Sophora*) vs +19% (fibrous *Malus*), but for three-year-old saplings in lab tanks, measured one year after planting. v2 drops "deep root architecture" as a claim and keeps roots out of the scoring |
| **Scope** | Florence offers hotspot maps (Pacetti #18), 1 m LiDAR, regional IDF grid, HSG 1:10,000 (used by Pacetti), 82k-tree inventory. NBS space in a hotspot district is only 0.1–7.1% of its area (Pacetti #18) | **One city (Florence), one scale (small catchment / district hotspot, ~0.5–2 km²), one intervention (street and square trees over sealed surfaces)** |
| **User** | Tree-selection DSSs rarely include climate resilience (Yadav et al. 2024 #27); bioretention guidelines select plants by native status far more than by traits (Rahmi et al. 2025 #26: 47 guidelines, 3 of 30 North American ones name any trait; rain gardens, not street trees); SylvCiT's runoff module is disabled (Nicol et al. 2026 #28) | Primary user = **computational designer / landscape architect in the early design phase**. The municipal planner is the secondary reader of the outputs |

## 2. Candidate topics scored (1–5, CLAUDE.md criteria)

| Option | Data (Italy) | Validation | Comp. depth | Scope vs 18 Dec | Interest / portfolio | **Total** |
|---|---|---|---|---|---|---|
| A. Trait-based species recommender only | 3 (interception data for ~10–20 species, roots ≈ none) | 2 (no hydrological outcome without a site) | 4 | 4 | 3 | 16 |
| B. Site planting optimisation in Grasshopper (generic vegetation) | 4 | 3 | 4 | 3 | 5 | 19 |
| **A→B narrowed: trait-parameterised street-tree selection and placement for a Florence pluvial hotspot** | **4** | **4** (interception module vs open field data #1; per-tree output vs #10/#11 benchmarks; hotspot vs #18) | **4** | **4** | **5** | **21** |
| C. Diversity–hydrology–heat trade-off | 3 | 2 | 5 | 2 | 4 | 16 |
| D. City-scale GI screening | 4 | 3 | 2 | 4 | 2 | 15 (and Pacetti #18 already did it for Florence) |
| E. Early abstract (UHI + runoff + biodiversity + ML surrogates + i-Tree agent, web + CAD) | 3 | 1 | 5 | 1 | 5 | 15 |

**Recommendation: the narrowed A→B topic.** It keeps what was interesting in the early abstract: Grasshopper, trees as attribute-rich components, runoff computed by SCS-CN. It drops what made the abstract unfinishable: three objectives, ML surrogates, a web app and an agent. The SCS-CN and interception calculation is instant, so the runoff part needs no surrogate. Heat (UTCI) stays an optional second objective only if time allows; Pace et al. 2025 (#13) gives the trade-off logic.

**City: Florence.** This reverses the provisional "Bologna" reading in `databases/data_inventory.md`. Bologna's validation data (Oct 2024 flood extents) describes a mixed, culvert-driven event that trees cannot meaningfully affect. Fallback if Florence data access fails: Bologna Ravone catchment (Dottori et al. 2014 #20), framed as a flash-flood headwater.

---

## 3. v2 statements

### Problem statement
Florence is repeatedly hit by **urban pluvial floods**: short, intense storms exceed the infiltration capacity of sealed surfaces and the capacity of a ~800 km, largely 19th-century combined sewer. Hotspots lie in flat, highly sealed districts, including the historic centre (Pacetti et al. 2022). In these districts, less than ~7% of the area is available for bioretention-type solutions (Pacetti et al. 2022). Trees are therefore one of the few retrofits possible, because their canopy spreads over pavements without taking ground space.

Trees do not all intercept the same amount of rain. Interception differs several-fold between species and is driven by measurable traits such as canopy storage capacity and leaf area index (Xiao & McPherson 2016; Anys & Weiler 2024; Dowtin et al. 2023). Yet street-tree choices and existing selection tools do not use these traits. Stormwater bioretention guidelines favour native origin over traits: 50% suggest and 17% require native species, while 3 of 30 North American guidelines name any plant trait (Rahmi et al. 2025; the review covers rain-garden planting, not street trees). Tree-selection decision support rarely addresses climate adaptation (Yadav et al. 2024). The most advanced trait-based recommender, SylvCiT, has its runoff module still disabled (Nicol et al. 2026). Designers therefore cannot tell, at the design stage, how much runoff a given choice of species and positions will avoid in a flood-prone block.

> Scope note (for the slide): the thesis addresses frequent, short-duration pluvial storms. It does **not** address river floods or multi-day events like Emilia-Romagna 2023 (return period >500 yr; Scoccimarro et al. 2025), where vegetation has negligible influence (Kuehler et al. 2016; Selbig et al. 2021).

### Research question
In a pluvial-flood hotspot catchment of Florence, how much event runoff volume from sealed surfaces can be avoided by street trees **selected and placed using species-specific interception traits** (canopy storage capacity, leaf area index) and the catchment's drainage geometry? The comparison is against (a) the existing tree stock and (b) a conventional planting palette with the same number of trees, under 2-, 5- and 10-year design storms of 1 h duration derived from the Tuscany rainfall-frequency (LSPP) grid.

### Hypothesis
**H1:** For the same number of new trees, trait-based selection and placement avoids more event runoff volume than the conventional palette. The reason: canopy interception scales with species-specific storage capacity and LAI, and placement over the sealed surfaces that drain to the hotspot maximises the intercepting area that matters.
**H2 (validity boundary):** the advantage, in % of event runoff, decreases as the design-storm return period increases, because canopy storage saturates early in the event (Kuehler et al. 2017; Anys & Weiler 2024).
*Test:* paired comparison of runoff volume per scenario and storm. The minimum difference counted as meaningful is set **before** the runs, after the baseline is computed (proposal: larger than the model's error against the field interception data in validation step 1). No threshold is invented here.

---

## 4. Methodology outline (data + tools)
1. **Site:** select one hotspot sub-catchment from Pacetti et al. 2022 (PFI > 80) or near the historical pluvial flood locations Pacetti et al. used for validation. Delineate it from the 1 m LiDAR DTM.
2. **Surfaces:** Copernicus imperviousness 10 m + municipal buildings/streets; HSG 1:10,000 (Tuscany Region) → SCS curve numbers.
3. **Trees:** Florence inventory (82,226 trees: species, circumference); height and crown from LiDAR DSM−DTM; LAI from allometry or LiDAR.
4. **Trait table:** species storage capacity, LAI and interception from the literature (#1, #3, #5, #6, #7, #8). Coverage of the top-20 Florence species is to be measured; gaps are filled by genus or leaf-type class and flagged.
5. **Runoff engine (Python, then Grasshopper component):** canopy interception (storage-bucket or Gash-type, #8/#33) over each tree's crown projection on sealed surfaces → SCS-CN on the remainder → event runoff volume.
6. **Selection + placement:** score candidate species (interception traits + local constraints: pests, invasiveness, drought tolerance from BROT 2) and place them on plantable pavement cells with a simple optimiser (greedy or NSGA-II, as in Liu et al. 2026).
7. **Validation:** (i) interception module vs open Freiburg field data (Anys & Weiler 2024, FreiDok); (ii) per-tree and per-m² canopy results vs Selbig et al. 2021 / Coville et al. 2022 (field 6,376 L/tree, 66 L/m² canopy per leaf-on season; calibrated i-Tree Hydro 6,120 L/tree, 63.5 L/m²); (iii) hotspot consistency vs Pacetti PFI.

## 5. Open checks (before 20 Oct)
- [ ] Get full text: Dowtin 2023 (#4). Done: Xiao & McPherson 2016 (#3) and Llorens & Domingo 2007 (#57, Mediterranean partitioning review) on 8 Oct; Selbig 2021 (#10) on 9 Oct. See `notes/lit/to_get_manually.md`.
- [x] Count species coverage: done for Florence and Barcelona, see `databases/*/species_coverage.csv` and §6.1.
- [ ] Get full text of Llorens 2006 (Mediterranean rainfall partitioning): the most likely source for Quercus ilex / Pinus / evergreen interception values.
- [ ] Confirm access to Tuscany HSG 1:10,000 and Pacetti's PFI map (ask authors?).
- [ ] Ask tutor: is runoff volume only (no peak) acceptable as the metric?

---

## 6. v3 option: one method for BOTH heat stress and pluvial runoff

### 6.1 Is a dual theme justified by the evidence?
| Question | Evidence | Verdict |
|---|---|---|
| Do cities suffer both, in the same places? | Florence: pluvial hotspots in the flat, sealed centre (Pacetti 2022 #18); the hottest stations are also in the centre, with less green (Petralli, #49, search summary); in the centre, street air is ~1.5 C warmer than in gardens on average and up to ~2 C on calm evenings in May (Petralli et al. 2006 #76). Barcelona: high UHI mortality (Iungman 2023 #35) and recurrent intense-rain flooding in dense districts (Barcelona Resilience Atlas). Mediterranean review confirms the dual exposure (Stavropoulos 2026 #54) | **Yes** (see `notes/city_screening.md`) |
| Do the same tree traits drive both? | Interception rises with LAI / leaf area density (Anys & Weiler 2024 #1; Yang 2019 #5). Shade cooling rises with canopy density, LAI and crown width (Rahman 2019 #38 (abs); Speak 2020 #39 (abs); Helletsgruber 2020 #40). The flip side: heat that thins crowns cuts both at once (Platanus lost roughly 30–50% of its plant area index after a > 41 °C heatwave, Sanusi & Livesley 2020 #66) | **Partly shared**: LAI and crown size help both |
| Where do they conflict? | (a) Leaf habit: evergreen crowns intercept in autumn–winter storms but block winter sun; seasonal LAI trade-off for comfort (Peng 2026 #53). (b) Water: transpiration is the larger air-cooling term (Park 2026 #42) and needs soil water (Pace 2025 #13); diffuse-porous species such as Platanus transpire 2–3× ring-porous ones (Bachofen 2025 #43). (c) Surface material can matter more than species for surface temperature (Kaluarachchi 2020 #45 (abs)) | **Real trade-offs**, so a multi-objective method is needed rather than one score |
| Is it already done? | Mannucci 2025 #51: Grasshopper + Ladybug + Kangaroo assess UTCI **and** runoff, but by scenario testing, with no species traits and no optimisation. Shaamala 2025 #52 and Peng 2026 #53 optimise species/placement for **heat only**; so do Hao 2023 #62 (genetic algorithm, identical trees), Elkhateeb 2025 #63 (Galapagos, shade only, hypothetical sites) and Oneto 2026 #64 (machine learning on Ladybug shading runs, species matched afterwards by size). Cortinovis 2022 #69 assesses heat and runoff for Barcelona, but city-wide, with trees as land cover. Closest: Tan & Liu 2026 #80 optimise species (crowns from US allometry) and positions of a fixed 30 trees for UTCI, CO2 uptake and diversity with a surrogate and NSGA-II in Grasshopper, but with no runoff. SylvCiT has neither (#28) | **Gap**: no method selects species *and* positions using measured traits for both objectives |
| Is there trait data? | Florence top-30 species (80% of 82,226 trees): a species-level runoff or heat value exists for 19% of trees, both for 7%. Barcelona top-30 (91% of 140,404 street trees): 40% and 29% (Platanus alone 28.6%). **Celtis australis is #2 in both cities with no value at all**; Mediterranean evergreens (Cupressus, Quercus ilex for heat, Olea, Pinus pinea) are weakly covered (`databases/*/species_coverage.csv`) | **Usable with explicit gap-filling** (genus/leaf-habit classes + sensitivity analysis). The gap itself is a finding |

### 6.2 Option scores (CLAUDE.md criteria, 1–5)
| Option | Data | Validation | Comp. depth | Scope vs 18 Dec | Interest | Total |
|---|---|---|---|---|---|---|
| Runoff only (v2, §3) | 4 | 4 | 4 | 4 | 5 | 21 |
| **Dual heat + runoff, one district** | 3 | 4 | 5 | 3 | 5 | **20** |
| Heat only (UTCI) | 4 | 4 | 4 | 4 | 4 | 20 |

Taken alone, the dual option is not "better". It is **more original** (it fills the Mannucci → Shaamala gap) but **heavier**: UTCI needs a radiation simulation for every layout. It is feasible only if (1) the site is one street/square cluster of a few hectares, (2) UTCI is evaluated at one or two design hours with Ladybug Tools, and (3) the optimiser runs on a fast proxy: shade-hours × crown LAI, or an ML surrogate trained on Ladybug runs. This is where the surrogate idea from the early abstract becomes justified, but only for the heat term.

### 6.3 v3 statements (dual; city = Florence or Barcelona, to decide)

**Problem statement.** Dense Mediterranean districts face two climate hazards in the same streets: summer heat stress, amplified by the urban heat island, and pluvial flooding from short, intense storms on sealed surfaces. In Florence both concentrate in the flat, highly sealed centre (Pacetti et al. 2022; Petralli et al.). Street trees are one of the few interventions that act on both: they shade and transpire, and they intercept rain over pavements. Their effect, though, depends on species traits. LAI and crown size help both objectives, while leaf habit and water demand create trade-offs (Rahman et al. 2019; Anys & Weiler 2024; Bachofen et al. 2025). Current design workflows either evaluate heat and runoff for fixed scenarios without species traits (Mannucci et al. 2025) or optimise trees for heat only (Shaamala et al. 2025; Peng et al. 2026). Designers therefore cannot see how species choice and placement trade pedestrian comfort against runoff reduction.

**Research question.** In a district that is both a heat and a pluvial-flood hotspot, can a trait-based method that selects and places street trees find layouts that reduce pedestrian heat stress (UTCI at the peak summer hour) and event runoff volume (2-, 5-, 10-yr, 1-h design storms) at the same time? How large is the trade-off between the two objectives, compared with the existing trees, a conventional planting palette, and single-objective layouts?

**Hypotheses.**
- **H1 (synergy):** with the same number of trees, trait-based layouts improve both UTCI and runoff volume over the conventional palette, because LAI and crown size drive both shading and interception.
- **H2 (trade-off):** heat-optimal and runoff-optimal layouts differ mainly in **species**, not positions: in leaf habit (evergreen vs deciduous) and transpiration capacity. The Pareto front between the two objectives is therefore not a single point.
- **H3 (validity boundary):** the runoff benefit shrinks as the storm return period grows (as in v2 H2). The UTCI benefit is largest in sun-exposed pedestrian routes (Lachapelle et al. 2023).

### 6.4 Decision (user, 7 Oct): **Barcelona**, **dual theme before 20 Oct**
Next: Barcelona data feasibility for both themes (done: `databases/data_inventory_barcelona.md`), then choose one district where a heat hotspot and a flood-prone area overlap (first pass: **Sant Antoni**).

**Validation / transfer (user, 8 Oct):** develop and calibrate on Barcelona; then **test the tool on Florence** (and possibly Bologna) as a transfer case. The Florence data and literature already collected (Pacetti 2022 hotspots, 82k-tree inventory, LiDAR 1 m, IDF grid) become the test set. This answers "does the method generalise?" without new data collection.

**Heat engine option (user, 8 Oct): Infrared City** (the tutor is a co-founder; free access hoped). Vendor-described: AI surrogate models trained on CFD/simulation data return UTCI, MRT, wind and solar radiation in seconds, via Grasshopper/Rhino plugins, a REST API and a Python SDK. This would remove the UTCI computation bottleneck in the optimisation loop (§6.2). **Questions for the tutor:** (a) how trees are represented (geometry only, or canopy porosity/LAI per species)? Species heat traits must enter through it; (b) API limits for thousands of optimisation evaluations; (c) published validation vs ENVI-met/Ladybug. Ladybug Tools stays the fallback and a cross-check.

_Original options considered:_
- City: **Florence vs Barcelona**. They score 22 vs 23 in `notes/city_screening.md`; the deciding checks are listed there.
- Scope: **dual** (more original, heavier) vs **runoff-only** (safer). A middle path is to build runoff-only first and add the UTCI objective after the 20 Oct feedback.

---

## 7. v4 (8 Oct): Barcelona, Porta (Nou Barris), heat + pluvial runoff
Site justification: `notes/site_selection.md`. Primary user: a **computational designer working on the municipal street-tree replacement**, who needs species and placement options with quantified heat and runoff effects.

**Problem statement.** Between 1956 and 2009, Barcelona's sealed surface grew from 45% to 72% of the municipality. About three storms a year exceed 60 mm/h in their first 20 minutes and flood streets where the sewer lacks capacity (Barcelona Resilience Atlas). The city also carries one of Europe's highest urban-heat-island mortality burdens (Iungman et al. 2023). Its street trees are about to change: the tree master plan caps any species at 15%, so a large share of the plane trees, today ~29% of street trees, will be replaced (municipal plan; press). In **Porta** (Nou Barris) both hazards overlap. 15% of its area is in the high flood-hazard classes (#13 of 72 neighbourhoods), its summer surfaces run 1.36 °C above the city median (#11), and 91% of its area is in the top heat-vulnerability class. It has 832 plane trees. The replacement species the city names (*Celtis*, *Melia*, *Pyrus calleryana*, *Jacaranda*, *Tipuana*, *Brachychiton*) already grow there. Yet in the literature we reviewed, only *Pyrus calleryana* has a measured canopy-storage value (Xiao & McPherson 2016), and **none has a measured cooling value**. The one species-level UTCI result models *Pyrus* as a default ENVI-met tree sized to the municipal maximum, so it reflects tree size rather than species (Silva et al. 2025). Replacement choices can therefore trade away cooling or rain interception without anyone noticing. Existing workflows either assess heat and runoff for fixed scenarios without species traits (Mannucci et al. 2025; Wu et al. 2024, the latter with surface rather than pedestrian temperature), or they optimise trees for heat only (Shaamala et al. 2025; Peng et al. 2026). Shaamala et al. name multi-objective optimisation that includes water sensitivity as future work. The most advanced trait-based recommender, SylvCiT, has its runoff module disabled (Nicol et al. 2026).

**Research question.** In Porta, as plane trees are replaced under the city's tree plan, which replacement species and positions jointly reduce (a) pedestrian heat stress (UTCI at the peak summer hour along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year design storms from the PDISBA rainfall curves)? How large is the trade-off between the two, compared with the current trees, a like-for-like replacement with the city's named palette, and single-objective layouts?

**Hypotheses.**
- **H1 (synergy):** for the same number and size class of trees, trait-based layouts improve both UTCI and runoff volume over the like-for-like palette, because crown size and LAI drive both shading and interception.
- **H2 (trade-off):** the heat-optimal and runoff-optimal layouts differ mainly in **species**, not positions: leaf habit (evergreen vs deciduous, given autumn storms vs summer heat) and transpiration capacity. The Pareto front is therefore not a single point.
- **H3 (validity boundary):** the runoff benefit shrinks as the storm return period grows, and is small at the sewer design level (T = 10 yr). Extreme events like 6 Sept 2018 (≈300-yr 20-min intensity) are outside what trees can affect.

**Test phase (later):** Sant Antoni (flood-dominant contrast site) and Florence (transfer case) run through the same method.
