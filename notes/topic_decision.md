# Topic decision: problem, research question, hypothesis (v2, 7 Oct 2026)

> **Update v3 (same day):** a dual heat + runoff version was added in §6 after a second literature round (21 heat papers, rows #35–#55) and a city screening (`notes/city_screening.md`). §1–§5 below are the runoff-only v2, kept as the fallback.

Inputs (v2, 7 Oct): 34 papers in `notes/lit/literature_matrix.csv` (13 read as full-text digests, 21 from abstracts only, marked there; on 8 Oct the matrix has 61 rows, 47 read in full), plus `databases/data_inventory.md`.
Citations below give author, year and the matrix row (#). Claims from abstracts only are marked (abs). Rows #4 and #10, which carry the argument, are now read in full (#3 on 8 Oct, #10 on 9 Oct, #4 on 12 Oct; #18 digested from full text).

---

## 1. What the literature says about the five known weaknesses

| Weakness in v1 | Evidence | Consequence for v2 |
|---|---|---|
| **Flood type** | Florence: whole city exposed to pluvial and flash floods from the minor network and a ~800 km combined 19th-century sewer; hotspots in flat, highly sealed areas incl. historic centre, validated against historical pluvial events (Pacetti et al. 2022, #18). Emilia-Romagna May 2023: no hourly extremes, multi-day accumulation, return period >500 yr (Scoccimarro et al. 2025, #21); mainly stratiform rain at 2–5 mm/h on saturated soils (Cremonini et al. 2024, #61). Bologna Oct 2024: 160–180 mm/24 h on saturated soils, culverted streams overflowed (Arpae report; see data inventory). Ravone culvert insufficient for intense events (Dottori et al. 2014, #20) | **Florence fits a pluvial framing; Bologna's recent events do not.** v2 names *urban pluvial flooding from frequent short storms* and explicitly excludes multi-day/fluvial events |
| **Testability** ("significantly reduces", "extreme precipitation") | Tree effect is largest for short, low-intensity storms and falls with depth and intensity (leafy crowns hold the first 2–4 mm, Kuehler et al. 2017 #9; Anys & Weiler 2024 #1; per-event interception falls from 87% to 1% as rain depth grows, Song et al. 2020 #12). Catchment experiment: 4% runoff-volume reduction from 31 street trees, **no peak-flow effect** (Selbig et al. 2021 #10); 3.5% of total runoff in the calibrated re-analysis (Coville et al. 2022 #11). NbS effect decays with return period (Costa et al. 2021 #23; Esraz-Ul-Zannat et al. 2024 #32; Liu et al. 2026 #24); the 10-yr storm, the most frequent one modelled, carries 74% of the expected annual flood damage in Aveiro (Quagliolo et al. 2023 #60) | Metric = **event runoff volume** from sealed surfaces (not peak discharge). Storms = **local design storms of 2, 5, 10-yr return period, ≥1 h** (Tuscany LSPP grid; ≥1 h avoids the 15-min aggregation bias, Lompi et al. 2022 #19). Baseline and comparison defined (§4) |
| **Traits vs biomass** | Interception differs strongly between species: storage capacity varies threefold among 20 species (Xiao & McPherson 2016 #3); *Tilia cordata* 70% vs *Acer platanoides* 55% event interception (Anys & Weiler 2024 #1); *Quercus ilex* 46–51% vs *Q. pyrenaica* 10–16% of annual rain, one isolated tree each (Hassan et al. 2017 #8); birch 23% vs pine 47% (Zabret & Sraj 2019 #7); *Ginkgo* 58% vs *Zelkova* 21%, one tree each (Yang et al. 2019 #5). LAI / leaf area density is the main driver (LAI: Anys & Weiler #1; central-crown LAI and small leaves, not leaf area density: Yang et al. 2019 #5; leaf area density: Baptista et al. 2018 #6); full trait list in Dowtin et al. 2023 #4 (systematic review, 99 articles: LAI, canopy density, crown projection area, leaf angle, hydrophobicity, bark storage; trait directions only, no pooled effect size per trait; Table 3 compiles per-species interception from earlier studies) | Supported for *interception*: species traits (storage capacity, LAI, leaf area density) matter, not just size. **Not** supported for roots: only two lab studies (#16, #17). Bartens et al. 2008 (#16, read in full) show that tree roots raise infiltration through compacted subsoil, but black oak (coarse roots) and red maple (fine roots) did not differ significantly. Zhang et al. 2019 (#17, read in full) found +118% (tap-rooted *Sophora*) vs +19% (fibrous *Malus*), but for three-year-old saplings in lab tanks, measured one year after planting. v2 drops "deep root architecture" as a claim and keeps roots out of the scoring |
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
- [x] Get full text: Dowtin 2023 (#4), read on 12 Oct together with Hassan 2017 (#8), de Mello 2024 (#34), Rahman 2019 (#38) and Kaluarachchi 2020 (#45). Earlier: Xiao & McPherson 2016 (#3) and Llorens & Domingo 2007 (#57, Mediterranean partitioning review) on 8 Oct; Selbig 2021 (#10) on 9 Oct. See `notes/lit/to_get_manually.md`.
- [x] Count species coverage: done for Florence and Barcelona, see `databases/*/species_coverage.csv` and §6.1.
- [ ] Get full text of Llorens 2006 (Mediterranean rainfall partitioning): the most likely source for Quercus ilex / Pinus / evergreen interception values.
- [ ] Confirm access to Tuscany HSG 1:10,000 and Pacetti's PFI map (ask authors?).
- [ ] Ask tutor: is runoff volume only (no peak) acceptable as the metric?

---

## 6. v3 option: one method for BOTH heat stress and pluvial runoff

### 6.1 Is a dual theme justified by the evidence?
| Question | Evidence | Verdict |
|---|---|---|
| Do cities suffer both, in the same places? | Florence: pluvial hotspots in the flat, sealed centre (Pacetti 2022 #18); the dense centre is also the warmest part of the city (Petralli et al. 2006 #76), and air temperature differs by almost 3 °C between the hottest and coolest of 25 stations (Petralli 2012 #49); in the centre, street air is ~1.5 C warmer than in gardens on average and up to ~2 C on calm evenings in May (Petralli et al. 2006 #76). Barcelona: high UHI mortality (Iungman 2023 #35) and recurrent intense-rain flooding in dense districts (Barcelona Resilience Atlas). Mediterranean review confirms the dual exposure (Stavropoulos 2026 #54) | **Yes** (see `notes/city_screening.md`) |
| Do the same tree traits drive both? | Interception rises with LAI / leaf area density (Anys & Weiler 2024 #1; Yang 2019 #5). Shade cooling rises with canopy density, LAI and crown width (Rahman 2019 #38: about 4 °C of surface cooling per unit LAI; shade cooling is largest over asphalt and among the largest in Mediterranean (and tropical/steppe) climates, with few such studies, transpiration is smallest in Mediterranean climates and about 10× lower for trees in paved pits than over grass; Speak 2020 #39: under solitary trees in Bolzano, ceptometer LAI ranks among the top predictors of surface cooling and wide crowns help, while Kaluarachchi 2020 #45 found no LAI effect; Helletsgruber 2020 #40). The flip side: heat that thins crowns cuts both at once (Platanus lost roughly 30–50% of its plant area index after a > 41 °C heatwave, Sanusi & Livesley 2020 #66) | **Partly shared**: LAI and crown size help both |
| Where do they conflict? | (a) Leaf habit: evergreen crowns intercept in autumn–winter storms but block winter sun; seasonal LAI trade-off for comfort (Peng 2026 #53). (b) Water: transpiration is the larger air-cooling term (Park 2026 #42) and needs soil water (Pace 2025 #13); diffuse-porous species such as Platanus transpire 2–3× ring-porous ones (Bachofen 2025 #43). (c) Surface material can matter more than species for surface temperature: across 471 Sydney trees, LAI and crown area did not change the sun–shade surface difference, whose mean ranged from −17.5 °C (concrete pavers) to −24.8 °C (bark mulch) (Kaluarachchi 2020 #45) | **Real trade-offs**, so a multi-objective method is needed rather than one score |
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

**Problem statement.** Between 1956 and 2009, Barcelona's sealed surface grew from 45% to 72% of the municipality (Barcelona Resilience Atlas, citing Barcelona Regional's climate-change impact study). About three storms a year exceed 60 mm/h in their first 20 minutes and flood streets where the sewer lacks capacity (Barcelona Resilience Atlas). The city also carries one of Europe's highest urban-heat-island mortality burdens (Iungman et al. 2023). Its street trees are about to change: the tree master plan caps any species at 15%, so a large share of the plane trees, today ~29% of street trees, will be replaced (municipal plan; press). In **Porta** (Nou Barris) both hazards overlap. 15% of its area is in the high flood-hazard classes (#13 of 72 neighbourhoods), its summer surfaces run 1.36 °C above the city median (#11), and 91% of its area is in the top heat-vulnerability class. It has 832 plane trees. The replacement species the city names (*Celtis*, *Melia*, *Pyrus calleryana*, *Jacaranda*, *Tipuana*, *Brachychiton*) already grow there, and so does *Styphnolobium japonicum* (5 trees), named in the press (inventory D1) and added to the palette (user, 14 Oct). Yet in the literature we reviewed, only *Pyrus calleryana* has a measured canopy-storage value (Xiao & McPherson 2016), and **none has a measured cooling value**. The one species-level UTCI result models *Pyrus* as a default ENVI-met tree sized to the municipal maximum, so it reflects tree size rather than species (Silva et al. 2025). Replacement choices can therefore trade away cooling or rain interception without anyone noticing. Existing workflows either assess heat and runoff for fixed scenarios without species traits (Mannucci et al. 2025; Wu et al. 2024, the latter with surface rather than pedestrian temperature), or they optimise trees for heat only (Shaamala et al. 2025; Peng et al. 2026). Shaamala et al. name multi-objective optimisation that includes water sensitivity as future work. The most advanced trait-based recommender, SylvCiT, has its runoff module disabled (Nicol et al. 2026).

**Research question.** In Porta, as plane trees are replaced under the city's tree plan, which replacement species and positions jointly reduce (a) pedestrian heat stress (UTCI at the peak summer hour along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year design storms from the PDISBA rainfall curves)? How large is the trade-off between the two, compared with the current trees, a like-for-like replacement with the city's named palette, and single-objective layouts?

**Hypotheses.**
- **H1 (synergy):** for the same number and size class of trees, trait-based layouts improve both UTCI and runoff volume over the like-for-like palette, because crown size and LAI drive both shading and interception.
- **H2 (trade-off):** the heat-optimal and runoff-optimal layouts differ mainly in **species**, not positions: leaf habit (evergreen vs deciduous, given autumn storms vs summer heat) and transpiration capacity. The Pareto front is therefore not a single point.
- **H3 (validity boundary):** the runoff benefit shrinks as the storm return period grows, and is small at the sewer design level (T = 10 yr). Extreme events like 6 Sept 2018 (≈300-yr 20-min intensity) are outside what trees can affect.

**Test phase (later):** Sant Antoni (flood-dominant contrast site) and Florence (transfer case) run through the same method.

## 8. v5 (19 Oct, user decisions): the heat metric, and H3 withdrawn
Two decisions taken by the user on 19 Oct. **Everything else in §7 stands**; these two points supersede it.

**1. Heat metric — decided.** The objective is the **mean UTCI over the 12–17 h window on a hot design day**, not UTCI at the peak summer hour. Reason: at the peak hour the metric saturates — on the hottest El Prat day even full shade is ≥ 32 °C in 5 of 6 afternoon hours, so a layout cannot show a benefit (`notes/decisions/heat_objective.md` §5). The hottest real day stays as a check. The RQ clause becomes:

> …which replacement species and positions jointly reduce (a) pedestrian heat stress (**mean UTCI over 12–17 h on a hot design day**, along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year design storms from the PDISBA rainfall curves)? How large is the trade-off between the two, compared with the current trees, a like-for-like replacement with the city's named palette, and single-objective layouts?

**2. H3 withdrawn — decided.** The thesis now has **two hypotheses, H1 and H2**. H3 ("the runoff benefit shrinks as the return period grows") is **not a hypothesis**: in the bucket model every crown is full at every design storm, so the falling percentage is an arithmetic consequence of `I = min(P, S)`, not a test (`notes/decisions/runoff_metric_sensitivity.md`; `notes/decisions/hypothesis_tests.md` §3.3). It is kept, explicitly, as a **declared validity boundary of the method**: the runoff benefit is small at the sewer design level (T = 10 yr) and extreme events such as 6 Sept 2018 (≈300-yr 20-min intensity) are outside what trees can affect.

**How to present it:** say that H3 *was* among the hypotheses and was removed once the model showed it to be true by construction. Withdrawing it is a result about the method, not a retreat: it is the difference between a claim and an identity. Anything that still reads "supporting H3" or "as H3 predicts" is wrong and must say "consistent with the declared boundary" instead.

## 9. v6 (21 Oct): the problem, rebuilt on the tree master plan

**Why v6.** At the 20 Oct session the tutor said (user-reported) the problem was not defined well enough: the thesis must exist *because of* a problem. Until 20 Oct the tree master plan was known only through the press; its text was read that day (`notes/tree_master_plan.md`). v6 rebuilds the problem on what the plan decides and what it leaves open.
- **§8 stands:** the heat metric, and H3 withdrawn and kept as a declared boundary.
- **The literature gap in §7 stands.**
- **Superseded below:** §7's problem statement, research question, hypotheses, palette wording and S1.

### 9.1 What the city has decided, and what it has not

| Question | Decided? | Source |
|---|---|---|
| Whether to reduce the planes, and by how much | ✅ No species above 15% of the urban fabric by 2037. Planes cut by 56%, to 12%, within ten years | plan §2.1, target 3; press, May 2026 🟡 |
| How and when | ✅ Gradually, as trees die and when streets are rebuilt | press 2022, 2026 🟡 |
| Which species may be used | ✅ The city's species catalogue, plus a target mix for the replacements | 2011 guide pp. 49–56; press 2026 🟡 |
| Which tree size fits which street | ✅ Sidewalk width sets the size class and the spacing | 2011 guide pp. 22–23 |
| **Which species at each position** | ❌ The city says it set the possible replacements in advance from criteria (street orientation, aerial space, soil, desired shade). The list is not public, and nothing quantifies the choice | press 2022 🟡 |
| **What each choice does to heat and runoff** | ❌ No document quantifies it per species or per position | plan; 2011 guide |
| **Priority where heat and flooding overlap** | ❌ The plan is city-wide and does not link replacement to flood or heat-vulnerability maps | plan |

### 9.2 Problem statement (v6)

**Problem.** Barcelona has decided to remove more than half of its plane trees within ten years (56% of 43,722; press, May 2026). Its tree master plan caps any species at 15% of the urban fabric, and its street-tree rules set which tree size fits which sidewalk (Ajuntament de Barcelona 2017, 2011). These rules fix *how much* of each species the city should have. They do not fix *which species goes where*. Trees are replaced one at a time, when a tree dies or a street is rebuilt, and the species comes from qualitative criteria the city has not published. No published instrument estimates what each choice does to pedestrian heat stress or to storm runoff.

**Why it matters.**
- **The palette species differ widely in crown size.** In Porta, in the 2nd and 3rd trunk classes (41–110 cm perimeter), the share of a plane's crown area that each palette species carries is (§9.9):
  - Tipuana and Jacaranda: 89–107%
  - Melia: 71–81%
  - Celtis: 32–52%
  - Pyrus: 35%
  - Brachychiton: 24–27%
- **There is little evidence behind them.** Most of these species have no measured cooling or interception value (`notes/lit/replacement_species_evidence.md`).
- **The plan's own targets can pull against each other at a single position.** Moving away from planes serves the diversity target (no species above 15%; Celtis is already close to it). A small-crowned replacement works against the canopy target (tree cover up to 30% of the urban surface; plan §2.1, target 1).
- **The losses would go unmeasured where it matters most.** In Porta (Nou Barris), pluvial flooding and summer heat overlap on the same streets (§7; `notes/site_selection.md`), and the neighbourhood has 832 planes. There, thousands of rule-compliant decisions over the next decade can erode shade and rain interception without anyone measuring it.
- **Each choice lasts for decades.** Every replacement starts as a young tree, so each decision fixes the canopy for a long time.

**Gap.**
- **In practice,** the city has rules and qualitative criteria but no quantities.
- **In research,** existing workflows either assess heat and runoff for fixed scenarios without species traits (Mannucci et al. 2025; Wu et al. 2024), or optimise trees for heat only (Shaamala et al. 2025; Peng et al. 2026). The most advanced trait-based recommender has its runoff module disabled (SylvCiT; Nicol et al. 2026). Details in §7.

### 9.3 Contribution

**A computational method that takes the plan's rules as hard constraints** (the species cap, tree size class by sidewalk width, the city's species catalogue) **and gives, position by position, the compliant replacement that keeps the most cooling and rain interception.** It also measures the heat–runoff trade-off that the plan creates but does not quantify. Its main result is the difference between the city's own rule-following replacement and an optimised replacement under the same rules.

### 9.4 Research question (v6)

> In Porta, as plane trees are replaced under Barcelona's tree master plan, which replacement species, chosen within the plan's rules (no species above 15%, tree size class set by sidewalk width, the city's species catalogue), and at which plane positions, jointly reduce (a) pedestrian heat stress (**mean UTCI over 12–17 h on a hot design day**, along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year PDISBA design storms)? How large is the trade-off between the two, and how far do rule-compliant optimised choices differ from the current trees and from the city's own replacement?

### 9.5 Hypotheses (v6)

- **H1 (synergy):** at the same positions, and with the size class each sidewalk takes, trait-based choices improve both heat and runoff over the city's own replacement (S1). The reason is that crown size and LAI drive both shading and interception. The runoff part keeps the Δmin rule: a difference below Δmin is reported as "not resolved by the model" (`notes/decisions/hypothesis_tests.md`).
- **H2 (trade-off):** unchanged. The heat-optimal and runoff-optimal choices differ mainly in species (leaf habit, transpiration), so the Pareto front is not a single point.
- **Declared validity boundary:** unchanged (§8).

### 9.6 S1 is now the city's own replacement

S1 = **what the city would do anyway**, built in three steps:
1. Take the 2026 target mix: Celtis, Melia, *Pyrus calleryana*, *Styphnolobium*, Tipuana (press 🟡).
2. Assign it to positions with the 2011 sizing rule: a species goes only where the sidewalk takes its size class (one class per sidewalk type, as the guide states it).
3. Assign at random, in proportion to the mix, with no heat or runoff information, and repeat over several seeds.

If the city's internal replacement list is obtained (§9.8), it replaces this proxy.

**Palette correction.**
- **Named for plane replacement:** Celtis, Melia, *Styphnolobium* and Tipuana (city, 2022; press 🟡), plus *Pyrus calleryana* in the 2026 mix (press 🟡).
- **Not named in any source found: Jacaranda and Brachychiton.** They stay in the tool's palette as catalogue species already common in Porta, labelled "not named".
- §7's phrase "the replacement species the city names" was unsourced for these two and is withdrawn.

### 9.7 Four changes of scope

1. **The cap is city-wide.** The plan never applies it per neighbourhood, so the tool's Porta-local 15% cap is an `ASSUMPTION`: a local reading of the city's rule. The alternatives:
   - a city-wide headroom on the urban-fabric denominator (~201,600 trees in 2017);
   - Porta's proportional share of the 12% plane target.

   Girona sets limits per neighbourhood (10-20-30), which gives a precedent (`notes/catalan_transfer_city.md` §5).
2. **Not every plane is a decision variable.** The city keeps planes on large avenues and in emblematic places (2011 guide p. 17). Av. Meridiana holds 194 of Porta's 832 planes. The guide does not define which streets count as large avenues, so whether Av. Meridiana counts is open: either the thesis sets a rule or the question goes to Parcs i Jardins (§9.8).
3. **Replacement happens one opportunity at a time.** Trees are replaced when they die or when a street is rebuilt, so the method must work for any subset of positions, not only for all of them at once. This also makes the primary user concrete: **the computational designer of a street-rebuild project**, who is the person making the replacement choice.
4. **The sizing rule becomes a constraint.** The guide gives one size class per sidewalk type; allowing smaller classes on wider sidewalks would be an `ASSUMPTION`. The constraint needs the sidewalk width at each position, which is not yet in the repo (plan: `notes/sidewalk_width.md`).

### 9.8 Two risks, and how they are settled

- **The city may already have a per-street replacement list.** In 2022 the city said it had determined which species can replace dying trees (press 🟡). If that list exists and uses shade, the contribution narrows to the quantities (heat, runoff, the trade-off), and S1 becomes that list. To settle it: the email to Parcs i Jardins (`notes/email_parcs_i_jardins.md`).
- **The sizing rule may leave only one or two species per position.** Under the literal reading the palette splits into three groups (2011 catalogue): large Celtis, Tipuana, Jacaranda; medium Melia, *Styphnolobium*, Brachychiton; small *Pyrus* only. A narrow sidewalk would then take only *Pyrus*. If so, the optimisation shrinks, and the main result becomes the cost of the forced downsizing. Check this as soon as sidewalk widths exist.

### 9.9 Crown evidence (Porta, LiDAR 2021, equal trunk size)

- **Source:** `scripts/crown_by_trunk_class.py` → `databases/barcelona/crown_by_trunk_class.csv`.
- **Measure:** crown area as a share of the plane's, in the same trunk class.
- **Trunk class:** the inventory's `categoria_arbrat`, by perimeter at 1 m: 41–80 cm (2nd class) and 81–110 cm (3rd class) (2011 guide p. 18).

| Species | 2nd class (n) | 3rd class (n) | Raw median, all classes |
|---|---|---|---|
| Platanus × acerifolia | 1.00 (326) | 1.00 (341) | 1.00 (807) |
| Tipuana tipu | 1.07 (62) | 0.91 (58) | 0.92 |
| Jacaranda mimosifolia | 0.89 (73) | 0.96 (55) | 0.77 |
| Melia azedarach | 0.71 (33) | 0.81 (70) | 1.02 |
| Celtis australis | 0.32 (149) | 0.52 (79) | 0.30 |
| Pyrus calleryana | 0.35 (48) | — (none) | 0.14 |
| Brachychiton populneus | 0.24 (55) | 0.27 (25) | 0.26 |

**Raw medians mislead.**
- **They make Melia look as big as a plane.** 30% of the Melias in the table are in the largest trunk class (> 110 cm), against 16% of the planes.
- **They overstate the loss for Pyrus.** 63% of the Pyrus trees in the table are in the smallest class.
- **The largest class is left out of the ranges.** In it, Melia carries 0.91, Celtis 0.67 and Brachychiton 0.37 of a plane's crown area; Tipuana (n = 9) and Jacaranda (n = 4) are too few (CSV).

**What the table does not show.**
- **Mature potential.** Equal trunk size is not equal age, and street trees are pruned. The table compares the trees as they stand in Porta.
- **Exact crowns.** Crowns are watershed segments from the 2021 LiDAR, capped at a 9 m radius (`scripts/bcn_lidar_porta.py`).
