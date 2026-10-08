# Agent backlog (first batch, 8 Oct 2026)

Made by a methodology audit: 4 lens agents (runoff, heat, traits + optimisation, 20 Oct framing), one adversarial verifier per lens, then a synthesis step. Every item targets **defining the methodology**: no design-tool code (CLAUDE.md gate).
Each issue below becomes one GitHub issue (title = heading, labels as listed, body = the text under it). Run one with `/agent-task <n>`.

| # | Title | Labels | Agent |
|---|---|---|---|
| 1 | Bracket whether design-storm runoff can tell species palettes apart | agent-ready, analysis, priority-1 | method-critic |
| 2 | Options memo: make H1-H3 falsifiable (metric, comparison, threshold) | agent-ready, analysis, priority-1 | method-critic |
| 3 | Palette canopy parameters, phenology and evidence check (fix PS claim) | agent-ready, lit, priority-1 | lit-scout |
| 4 | Define canopy storage S, source interception values, verify method refs | agent-ready, lit, priority-1 | lit-scout |
| 5 | Screen close prior art and draft contribution statements | agent-ready, lit, priority-1 | lit-scout |
| 6 | Define heat objective f1 and weather forcing (EPW, wind, urban offset) | agent-ready, analysis, priority-1 | method-critic |
| 7 | Heat tree representation, tau correction and validation rule from sources | agent-ready, lit, priority-1 | lit-scout |
| 8 | Replacement scope and S1 baseline: palette, cap headroom, diversity floor | agent-ready, data, analysis, priority-1 | data-scout |
| 9 | 20 Oct pack: infographics plan, 5-min talk outline, tutor question sheet | agent-ready, analysis, tutor-question, priority-1 | method-critic |
| 10 | Extract PDISBA design storms and intense-storm seasonality | needs-user, data, priority-1 | data-scout |
| 11 | Pick the shared design sub-area and the runoff spatial unit | needs-user, analysis, priority-1 | method-critic |
| 12 | Tree size: size_category meaning, LiDAR season, sizes, evaluation horizon | needs-user, data, priority-1 | data-scout |
| 13 | Verify runoff validation datasets and decide the tree-pit term | needs-user, data, priority-1 | data-scout |
| 14 | Options memo: f1 proxy, optimiser choice and sensitivity plan | agent-ready, analysis, priority-2 | method-critic |

## Decisions only you can take
(The memos from issues 1, 2, 10–13 give you the evidence for these.)

- H1 threshold: (a) minimum meaningful difference = runoff-module error against the Anys & Weiler 2024 field data (#1); (b) the larger of the model error and the gap-fill sensitivity spread; (c) for heat, crossing a UTCI stress-class limit (Bröde 2012, to verify). Recommended: (b), fixed before the runs. This restores the v2 §3 rule; the heat analogue waits for the heat-validation memo.
- H1 comparison point: S1 lies inside the S4 search space, so S4 dominates S1 by construction for point estimates. Options: (a) knee point vs S1; (b) best-runoff layout with UTCI no worse than S1; (c) dominance in a share of trait-uncertainty runs fixed in advance. Recommended: (c), because it is the only one that can fail. Add a supported / inconclusive / rejected rule for gap-filled species.
- H2 positions: with fixed plane pits, 'species, not positions' is true by construction. Options: (a) restate H2 as a species-composition claim (evergreen share or composition dissimilarity, S2 vs S3); (b) make positions decision variables on plantable cells (needs sidewalk data, A6 🟡); (c) drop the positions clause. Recommended: (a), since (b) needs data that is not yet verified.
- H2 mechanism: leaf habit and transpiration cannot change f1 or f2 as specified. Options: (a) add a cold-season heat term (winter UTCI or sun access; Peng 2026 #53, abs); (b) a transpiration correction by wood-anatomy class (#38, #42, #43, #44); (c) restrict H2 to LAI, crown size and leaf-on timing, with transpiration out of scope; (d) with any of these, assign each design storm a month so leaf habit enters f2. Recommended: (c) + (d), since Tier 1 does not model transpiration (methodology §5). Use (a) only if Barcelona winter hours reach a cold-stress class (pending heat_bounds.py).
- H3: (a) restate it as a declared model boundary (it is true by construction for I = min(P, S)); (b) test the modelled benefit vs event depth against the Anys & Weiler 2024 field data; (c) keep it as a model result, with 'small' defined by a threshold fixed before the runs. Recommended: (b) if the Freiburg data prove open, otherwise (a).
- Trade-off metric for the RQ: % loss of one objective at the other's optimum, hypervolume, or knee-point distance. No default yet: there is no source in the matrix. Decide after the prior-art memo.
- Evaluation horizon for S0 vs S1-S4: at planting, +10 yr, +20 yr, maturity, or the full trajectory. No default until the size_category meaning and species growth sources are verified (tree-size issue).
- Leaf state of the design storm: leaf-on, leaf-off, transitional (an Oct-Nov LAI fraction), or season-weighted by storm month. Recommended interim: a leaf-on main run plus a leaf-off sensitivity run. Switch to season-weighted once PDISBA or gauge data give a monthly distribution.
- Storm duration and T set: 20 min, 1 h (carried over from Tuscany, Lompi #19), or the PDISBA design hyetograph; T = 1/2/10 vs 2/5/10. Recommended: the PDISBA design hyetograph, with one T set used consistently in the RQ, §4 and §6, pending extraction (1 h has no Barcelona justification).

## New questions for the tutor (20 Oct)

- If runoff volume alone is not acceptable, is a simple peak proxy enough (the rain depth intercepted within the peak 20-min block of the PDISBA design hyetograph), or must sewer surcharge be modelled? The PS frames the hazard as >60 mm/h in the first 20 min, and Selbig 2021 (#10, abs) reports that peak discharge was generally not affected by street trees.
- Infrared City access: when can I get access, under which academic licence, and how should the tool be cited in the thesis?
- Infrared City inputs and outputs: can it take a custom EPW (plus an urban temperature offset), and does it return UTCI/MRT per grid point and per hour? What are the maximum domain size and the grid resolution?
- Heat-engine fallback: if Infrared City access or per-species crown transmissivity is not available by a date we fix now, is Ladybug Tier 1 plus a tau correction an acceptable in-loop heat engine?
- Can you help request the RESCCUE pluvial flood-depth maps that sit behind the city login (site_selection.md §6)?
- Is the transfer test (Sant Antoni + Florence, planned for 2-10 Dec) expected in the thesis, or can it move to a discussion section, given the 18 Dec deadline and the unconfirmed Florence data access?
- Can a hypothesis be stated as a declared model boundary (H3: the tree benefit fades as the storm return period grows), or must every hypothesis be testable against observations?
- If no open Mediterranean throughfall dataset is found, is it acceptable that the replacement-species parameters stay unvalidated, stated as a limitation, with validation limited to the interception-model structure?
- Is Grasshopper integration a hard requirement of the programme, and what slide format and language are expected for the 5-minute talk?
- Is the final delivery confirmed for 18 Dec 2026?

---

## Issue 1: Bracket whether design-storm runoff can tell species palettes apart

Labels: `agent-ready`, `analysis`, `priority-1`

Agent role: method-critic

### Goal
Test, using aggregate arithmetic only, whether the event-runoff objective f2 can tell species palettes in Porta apart. Then draft a runoff metric and H1/H3 wording that can be tested.

### Why (blocks methodology)
- `notes/methodology.md` §4 step 2 uses a bucket I = min(P, S). The definition 'S from storage capacity x LAI' (§3/§4) is ambiguous, and its two readings differ by a factor of LAI.
- The only storage range in the repo is 0.59-1.81 mm (Xiao 2015, `literature_matrix.csv` #3, abs). Freiburg (#1) reports 55-70% interception on a 6.7 mm mean event. That is above what this bucket allows, so the evaporation term may be central rather than a refinement.
- §6 optimises f2 = event volume at T = 2 yr. If palette differences come to only a few % of event runoff and are smaller than parameter uncertainty, f2 is flat and H1 (`notes/topic_decision.md` §7) cannot be tested. H3 is true by construction for any fixed-storage bucket.
- v4 §7 dropped the v2 §3 rule that fixes the minimum meaningful difference before the runs.

### Context files
- `exchange/to_gh/porta_street_trees.csv` (2,825 trees, size_category; the class meaning is unconfirmed, inventory A1)
- `databases/barcelona/porta_species.csv`
- `notes/lit/literature_matrix.csv` rows #1, #3, #33
- `notes/methodology.md` §3, §4, §6; `notes/topic_decision.md` §3 (v2 'Test' line), §7
- `databases/data_inventory_barcelona.md` A1, A5, B1, B2

### Steps
1. Give each size_category (PRIMERA/SEGONA/TERCERA/EXEMPLAR) a low and a high crown diameter, each cited or labelled ASSUMPTION. Bracket the share of crown over sealed ground (ASSUMPTION; land cover A5 is unverified).
2. Bracket S two ways: (a) 0.59-1.81 mm per unit crown ground area; (b) per unit leaf area x an LAI bracket (cited or ASSUMPTION). State which reading the Freiburg magnitudes (#1) favour.
3. Sweep rain depth P over a generic range (e.g. 5-80 mm) with no return period attached. Do not invent PDISBA depths. Mapping P to T waits for `databases/barcelona/design_storms.csv` (issue 'Extract PDISBA design storms and intense-storm seasonality').
4. Palettes: S0 (current trees); S1 (planes replaced by Celtis/Melia/Pyrus calleryana/Jacaranda/Tipuana/Brachychiton in their Porta proportions); best case (all trees at high S); worst case (all at low S). Compute intercepted m3 and % of event runoff with SCS-CN, CN 98, on a bracketed sealed area of Porta (0.84 km2).
5. Add a Gash-type evaporation term (E/R x P during saturation) as a sensitivity. Cite the E/R range or label it ASSUMPTION. The repo has no E/R value; Huang 2017 #33 (abs) says only that E/R is the most sensitive parameter.
6. At each P, compare the spread between palettes with the spread from parameter uncertainty.
7. Write an options memo on the runoff metric: keep design-storm volume; add frequent-storm or leaf-on-season volume; or use intercepted depth per tree. Draft H1/H3 wording that restores a minimum meaningful difference fixed before the runs, and flag any change this implies for the RQ.

### Done when
- `notes/decisions/runoff_metric_sensitivity.md` contains: (a) a table of P x palette (S0, S1, best, worst) x S reading (a/b) x S low/high, giving intercepted m3 and % of event runoff, with and without the evaporation term; (b) every assumption with its source or the ASSUMPTION label; (c) a recommended runoff metric and draft H1/H3 wording, each marked 'pending user decision'.
- `scripts/explore_runoff_sensitivity.py` (short, with a usage docstring, reading only repo CSVs) reproduces the table.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs). Label every unsourced input ASSUMPTION, and mark all results 'exploratory bracket'.
- Aggregate arithmetic only: no per-tree geometry, no per-segment routing, no reusable module functions (CLAUDE.md: Methodology status NOT DEFINED).
- No network access needed. Do not edit topic_decision.md or methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 2: Options memo: make H1-H3 falsifiable (metric, comparison, threshold)

Labels: `agent-ready`, `analysis`, `priority-1`

Agent role: method-critic

### Goal
Write one options memo that turns H1-H3 (`notes/topic_decision.md` §7) into falsifiable tests. For each hypothesis, give the metric, the comparison rule and the threshold rule, and flag every place where the current method makes a hypothesis true or false by construction.

### Why (blocks methodology)
- §7 H1-H3 and `notes/methodology.md` §7 give no unit, comparison rule or threshold. The v2 rule (topic_decision §3: the minimum meaningful difference is set before the runs and is larger than the model error against field interception data) is missing from v4.
- H1: S1 (methodology §7) is a feasible point of the S4 search space (§6 decision variables), so a converged Pareto set weakly dominates S1 by construction. Which Pareto point is compared with S1 is undefined. S1 relies on gap-filled values (§3), so H1 also needs a supported / inconclusive / rejected rule.
- H2: positions are fixed plane pits (§6; new positions are only optional), so 'species, not positions' holds by construction. Leaf habit cannot change f1, because heat is scored only in the hottest summer week (§1/§5). Transpiration enters neither objective (§5 'Known limits'; §4 is event-based), and the design storms have no season (§4 step 1). If runoff is evaluated leaf-on, both objectives rise with LAI and crown size, and the front may collapse to a single point.
- H3: with I = min(P, S) and pit infiltration that does not depend on T at the fixed d = 1 h, the % benefit falls with P by construction. 'Small at T = 10 yr' has no threshold.
- The RQ asks 'how large is the trade-off' but gives no metric for it.

### Context files
- `notes/topic_decision.md` §3, §7; `notes/methodology.md` §1, §3-§7
- `notes/lit/literature_matrix.csv` (#1, #13, #24, #38, #42, #43, #44, #52, #53)
- `databases/data_inventory_barcelona.md` A1, A6, B2, B3
- If merged by then (otherwise use placeholders): `notes/decisions/runoff_metric_sensitivity.md`, `heat_objective.md`, `replacement_scenario.md`, `design_subarea.md`

### Steps
1. H1: give the metric and unit (from methodology §5 'Metrics' and §6 f2) and the scenarios compared. Give comparison-rule options: knee point; best runoff at UTCI no worse than S1; dominance in a share of trait-uncertainty runs fixed in advance. Give threshold-rule options, each sourced from a matrix row or stated as 'fixed before the runs'. Candidates are the module error against Anys & Weiler 2024 (#1) and the gap-fill sensitivity spread. Add a supported / inconclusive / rejected rule for gap-filled values.
2. H2: show the by-construction problem, then give the options: (a) a species-composition claim with a metric (evergreen share, or a composition-dissimilarity index with its source marked 'to add') comparing S2 and S3; (b) positions as decision variables on plantable cells (needs A6, 🟡); (c) restrict H2 to LAI, crown size and leaf-on timing, with transpiration out of scope; (d) add a cold-season heat term such as winter UTCI or sidewalk sun access (Peng 2026 #53, abs); (e) a transpiration correction by wood-anatomy class, using only #38, #42, #43 and #44. Separately, state that leaf habit enters f2 only if design storms are assigned to a month, and link the PDISBA issue and the palette-phenology issue. Check whether the front collapses when runoff is leaf-on.
3. H3: define 'small' (for example, the benefit as % of event runoff at each T) and give 2-3 threshold options. Add an option to test the modelled % against event depth using the Anys & Weiler field data instead of model output, and an option to restate H3 as a declared model boundary.
4. Give trade-off metric options (% loss of one objective at the other's optimum; hypervolume; knee-point distance), each with a matrix row or 'no source in matrix'.
5. Scenario conditions, options only, each linked to the issue that owns its evidence: time horizon (at planting / +10 / +20 yr / maturity); leaf state per design storm (leaf-on / leaf-off / season-weighted); storm duration and T set (20 min / 1 h / PDISBA hyetograph; mark 'to check locally' while PDISBA is unread).
6. Build an S0-S4 consequence table: which test needs which scenario, and whether S2 and S3 are still needed.
7. Give a recommended default for each item. Draft RQ/H1-H3 rewordings that make no new factual claims, labelled 'changes PS/RQ/H: user decides'. End with one question for the user and one question for the tutor.

### Done when
`notes/decisions/hypothesis_tests.md` contains:
- one section each for H1, H2 and H3, with the metric and unit, the scenarios, the comparison rule, the threshold rule (sourced or 'fixed before the runs'), a falsifiability check and 2-3 reformulations;
- the trade-off metric options and the scenario-condition options;
- the S0-S4 consequence table;
- the draft wording, marked as the user's decision;
- one user question and one tutor question.
Every value traces to a literature_matrix.csv row or is marked (to add). No other file is changed.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Memo only: no design-tool code (CLAUDE.md: Methodology status NOT DEFINED). Do not edit topic_decision.md or methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 3: Palette canopy parameters, phenology and evidence check (fix PS claim)

Labels: `agent-ready`, `lit`, `priority-1`

Agent role: lit-scout

### Goal
Build one sourced, long-format table of canopy parameters for the replacement palette: LAI, transmissivity/k, leaf habit, leaf-out and leaf-fall months, and wood porosity. Classify the measured heat and runoff evidence for each species, and propose a corrected problem-statement sentence.

### Why (blocks methodology)
- `notes/methodology.md` §3 uses tau = exp(-k LAI) with 'k from the literature' (Monsi & Saeki 1953 marked '(to add)'), per-species LAI by leaf-on/leaf-off months, and wood anatomy as a transpiration class. It also gap-fills 'with a range' but has no rule for building classes or for classes with fewer than 2 measured species. LAI is shared with the runoff module (§4).
- `notes/lit/species_measurements.csv` has no LAI, transmissivity or leaf-out/leaf-fall dates. `databases/barcelona/species_coverage.csv` has no heat value for Celtis, Melia, Tipuana, Jacaranda or Brachychiton.
- The PS (`notes/topic_decision.md` §7) says none of the named replacements has a measured interception or cooling value. The repo contradicts this:
  - Pyrus calleryana has two rows: Armson 2013 (full-text digest, value not extracted, no matrix row) and Silva 2025 #47 (abs).
  - Abreu-Harbich 2012 is a field study of a Tipuana tipu cluster (`candidates_heat.csv`).
  - Ji 2025 measured interception for Sophora japonica (`candidates.csv`).
  - Inventory D2 and methodology §3 already leave Pyrus out of the no-value list.
- H2 and the leaf state of the design storm need phenology months, and the repo has no source for them.

### Context files
- `notes/lit/species_measurements.csv`, `literature_matrix.csv` (#39 Speak 2020, #40, #43, #47, #52, #53), `shortlist.csv`, `candidates*.csv`, `to_get_manually.md` (Rochette Cordeiro 2026, Sanusi 2020, Li 2022 STMRT)
- `databases/barcelona/porta_species.csv`, `species_coverage.csv`
- `notes/methodology.md` §3, §5; `notes/topic_decision.md` §7; `databases/data_inventory_barcelona.md` D1, D2

### Steps
1. Species: Platanus x acerifolia, Celtis australis, Melia azedarach, Pyrus calleryana, Jacaranda mimosifolia, Tipuana tipu, Brachychiton populneus, Styphnolobium japonicum. If time allows, add the other taxa with ≥2% share in porta_species.csv (Citrus x aurantium, Robinia pseudoacacia, Catalpa bignonioides, Grevillea robusta, Casuarina cunninghamiana, Populus nigra) at genus or leaf-habit-class level.
2. Parameters: summer LAI (range); leaf-off LAI; crown shortwave transmissivity leaf-on and leaf-off (or k with its leaf-angle basis); leaf habit (evergreen / deciduous / semi-deciduous; flag Jacaranda and Tipuana as uncertain); leaf-out and leaf-fall months under Mediterranean conditions; wood porosity (InsideWood). Storage capacity S and E/R belong to the issue 'Define canopy storage S...'. Mature size belongs to the tree-size issue.
3. Search the repo first: grep the title and abstract fields of candidates*.csv and shortlist.csv for each name and synonym. Then use WebSearch with synonyms (chinaberry; tipu tree / Tipuana speciosa; kurrajong; Sophora japonica / pagoda tree; European nettle tree) crossed with: interception, throughfall, LAI, transmissivity, ENVI-met LAD, shade cooling, surface temperature, MRT, UTCI/PET, phenology. Include studies from the species' other ranges (South America, Australia, Iran/Turkey, China). Log every query and every 'nothing found'.
4. Find a citable source for k, with DOI (for example the English translation of Monsi & Saeki; verify it), and state whether k is fixed or species-specific.
5. Classify each species' evidence as: measured runoff / measured heat / simulated only / LAI or structure only / nothing found.
6. Draft 2-3 gap-filling rules (leaf-habit class min-max; nearest measured species by leaf size and habit; regression from 3TF traits). Give the number of measured species per class and flag classes with fewer than 2.
7. Add literature_matrix.csv rows for Armson 2013 (doi 10.48044/jauf.2013.021), Abreu-Harbich 2012 and every new source, using the next free id (renumber at rebase if a parallel PR took the same id). Add species_measurements.csv rows, writing 'value not reported in abstract' where that applies. Add paywalled full texts to to_get_manually.md without duplicates.
8. Propose an exact rewording of the PS sentence in topic_decision.md §7, and list whether D2 and methodology §3 need the same change. Do not edit those files.

### Done when
- `notes/lit/species_canopy_params.csv` (species, parameter, value_or_range, unit, source author-year, DOI, region, read_level) has one row per species x parameter, holding either a value or 'no value found'.
- `notes/lit/replacement_species_evidence.md` gives the evidence class for each species with matrix ids and read levels, the query log, the proposed PS sentence, and the files that need the same correction.
- `notes/method_traits.md` gives the k source and DOI, whether k is species-specific, the gap-filling options with their class sizes, coverage % per parameter and per species, and the PDFs the user must fetch.
- The new rows are in literature_matrix.csv, species_measurements.csv and to_get_manually.md.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- OpenAlex, doi.org and publisher hosts are blocked in the cloud, but WebSearch works. Give a value seen only in a search summary the read_level 'search summary' and mark it 🟡. Copy values exactly, give ranges where sources disagree, and leave a cell blank rather than guess.
- Do not edit topic_decision.md, methodology.md or data_inventory_barcelona.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 4: Define canopy storage S, source interception values, verify method refs

Labels: `agent-ready`, `lit`, `priority-1`

Agent role: lit-scout

### Goal
Define the canopy storage S without ambiguity, source storage capacity and E/R values for Porta's main taxa, and tag every interception value by measure type. Also verify the standard-method references and the unsourced claims in the problem statement.

### Why (blocks methodology)
- `notes/methodology.md` §4 step 2, 'S from species storage capacity x LAI', is dimensionally undefined: it could mean storage per unit leaf area x LAI, or storage per unit crown ground area, and the two differ by a factor of LAI. The gap-filling classes (§3) have no numbers. The Gash refinement needs E/R and free-throughfall parameters, and none has a source.
- In `notes/lit/species_measurements.csv`, Platanus (Baptista 2018, #6) and Styphnolobium (Yang 2019, #5) read 'value not yet extracted'. Interception values mix event %, annual % and storage. The full-text checks in topic_decision.md §5 are unticked (#3 Xiao, #4 Dowtin, #10 Selbig, Llorens 2006). The traits-vs-biomass row of §1 rests on the abstract-only rows #3 and #5-#8.
- Ji et al. 2025 (`candidates.csv`) reports interception 'largely independent of canopy structure', which bears on H1's mechanism. It is not in the matrix.
- SCS-CN, Gash and NSGA-II have no citation. The PS figure 'sealed surface 45% to 72% (1956-2009)' (topic_decision.md §7) has no source in the repo.

### Context files
- `notes/methodology.md` §3, §4, §6; `notes/topic_decision.md` §1, §5, §7
- `notes/lit/literature_matrix.csv` (#1, #3-#11, #24, #33, #34, #38, #39), `species_measurements.csv`, `candidates.csv`, `to_get_manually.md`
- `databases/barcelona/porta_species.csv`

### Steps
1. From open documentation, state the exact parameter definitions and units used by: the simple bucket; the revised Gash model (Gash 1979; Gash et al. 1995); and the i-Tree Hydro / UFORE-Hydro leaf and bark storage. Draft a one-paragraph definition of S (unit, reference area, and how LAI enters).
2. Find values for canopy storage capacity (mm), specific leaf storage (mm per unit LAI) and E/R. Cover the 13 taxa with ≥2% share in porta_species.csv (Platanus x acerifolia, Celtis australis, Melia azedarach, Pyrus calleryana, Jacaranda mimosifolia, Tipuana tipu, Brachychiton populneus, Citrus x aurantium, Robinia pseudoacacia, Catalpa bignonioides, Grevillea robusta, Casuarina cunninghamiana, Populus nigra), then their genera. Prefer Mediterranean and urban measurements. Try open copies before calling a source paywalled: Huang 2017 (#33, OA bronze), Yang 2019 (#5, OA hybrid), Baptista 2018 (#6, White Rose eprints), Hassan 2017 (#8, OA hybrid), Dowtin 2023 (#4, OA hybrid), Coville 2022 (#11), #24, plus Europe PMC and author repositories. Where a full text is reached, extract the exact values and upgrade read_level.
3. Build genus and leaf-habit class ranges (min, median, max, n sources). Leave a taxon blank rather than guess.
4. Add a measure_type column to species_measurements.csv with this vocabulary: event_interception_pct, annual_interception_pct, storage_capacity_mm, transpiration, surface_temp, MRT, UTCI_simulated, other. Fill it for every row.
5. Add Ji et al. 2025 (10.1016/j.ufug.2025.129068) to literature_matrix.csv from its candidates.csv abstract, marked (abs), with a note on which claims it qualifies (the topic_decision §1 traits-vs-biomass row and the H1 mechanism).
6. Verify the DOI or official reference for: USDA NRCS NEH-630 ch. 10 and TR-55 (SCS-CN); Gash 1979; Gash et al. 1995; Deb et al. 2002 (NSGA-II). Record how each was verified. Find the primary source for the 45% to 72% sealing figure, or flag the sentence for removal.
7. Move the sources you cannot reach (#3, #9, #10, #34, #38, #39, Llorens 2006, plus any OA copy you could not fetch) into a top block of to_get_manually.md headed 'carries PS/H/validation'. Name the exact table or figure needed, and avoid duplicates.

### Done when
- `notes/decisions/interception_parameter_definition.md` holds the S definition paragraph and the bucket, Gash and i-Tree parameter definitions, with sources.
- `notes/lit/interception_params.csv` (taxon_or_class, parameter, value_or_range, unit, reference_area, definition, source, DOI, read_level, region) covers all 13 taxa directly or through a flagged genus or class, and leaves cells empty where no source exists.
- `notes/lit/method_references.md` lists every standard-method reference with a verified DOI/URL or 'not found' and how it was verified, plus the sealing-claim source or a removal flag.
- species_measurements.csv has measure_type for every row, literature_matrix.csv has the Ji 2025 row, and to_get_manually.md opens with the 'carries PS/H/validation' block.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- In the cloud, OpenAlex, doi.org, mdpi.com, sciencedirect.com and eprints.whiterose.ac.uk were blocked on 7-8 Oct; WebSearch works. Values seen only in search summaries are 🟡 'search summary'. Agents cannot read papers/ or Zotero.
- Ownership in other issues: Bröde 2012 goes to the heat-objective issue, Monsi & Saeki to the canopy-parameter issue, the 'Bath study' to the heat-validation issue. LAI values come from species_canopy_params.csv. New matrix ids: renumber at rebase if they clash.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 5: Screen close prior art and draft contribution statements

Labels: `agent-ready`, `lit`, `priority-1`

Agent role: lit-scout

### Goal
Screen the closest prior art and draft 2-3 cited contribution statements, with a verdict on whether the novelty claim holds.

### Why (blocks methodology)
- CLAUDE.md ('Tutor's requirements') asks for Purpose / Background / Contribution to knowledge, but no contribution statement exists in notes/.
- The novelty claim in `notes/topic_decision.md` §6.1 ('Is it already done?') rests on Mannucci 2025 #51, Shaamala 2025 #52 and Peng 2026 #53, all abstract-only in `literature_matrix.csv`. Nyelele 2021 #25 is also abstract-only.
- The close prior art listed in `notes/lit/to_get_manually.md` T2 has not been screened.

### Context files
- `notes/lit/shortlist.csv` (abstract column), `candidates*.csv`, `literature_matrix.csv`, `to_get_manually.md` (T2)
- `notes/topic_decision.md` §6.1, §7

### Steps
1. Screen from the stored abstracts: #25 Nyelele, #51 Mannucci, #52 Shaamala, #53 Peng, plus Tan 2026 (10.1016/j.scs.2026.107726), Wu 2024 (10.3390/su16125201), Xing 2026 (10.3390/su18042142), Liang 2021 (10.1016/j.scitotenv.2021.146415), Hao 2023 (10.1016/j.ufug.2023.128017), Elkhateeb 2025 (10.3390/urbansci9120504), Oneto 2026 (10.1016/j.ufug.2026.129457) and Eslami 2026 (10.71573/zhbx9v70). Use WebSearch where the stored abstract is missing or truncated (Tan, Liang, Nyelele).
2. Try OA full texts for #51, #52, #53 and #25 only if the host is reachable. Otherwise keep read_level 'abstract' and mark them in to_get_manually.md as 'carries the novelty claim'.
3. Run one WebSearch round for 2022-2026 work that combines street-tree species selection or placement with both UTCI/MRT and stormwater runoff. Log the query strings and the number of relevant hits.
4. Build a feature matrix with the columns: id, citation, doi, species_level_traits (Y/N), heat_metric, runoff_metric, placement_optimised, species_optimised, multi_objective, mediterranean, validation_type, read_level.
5. Append the new papers to literature_matrix.csv with the next free ids. Renumber at rebase if a parallel PR took the same ids.
6. Draft 2-3 contribution statements (one method contribution plus one knowledge contribution), each claim tied to a matrix row. Give a verdict on the §6.1 gap claim: holds / holds only with narrower wording / does not hold. State the read level the verdict rests on, and list the papers whose full text could change it.

### Done when
- `notes/lit/prior_art_matrix.csv` has at least 12 rows (#25, #51, #52, #53 and the 8 T2 papers), each with read_level, plus any new hits from the logged search.
- literature_matrix.csv has rows for the newly screened papers, with unique ids after rebase.
- `notes/decisions/contribution_statement.md` has 2-3 cited candidate statements, the verdict on the §6.1 gap, the search log, and the list of full texts the user should fetch.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Full texts cannot be fetched in the cloud: sciencedirect.com, mdpi.com, OpenAlex, Crossref and doi.org were blocked on 8 Oct. Expect an abstract-level verdict.
- Do not edit topic_decision.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 6: Define heat objective f1 and weather forcing (EPW, wind, urban offset)

Labels: `agent-ready`, `analysis`, `priority-1`

Agent role: method-critic

### Goal
Propose one definition of f1: metric, design day and hours, domain rule, and minimum meaningful difference. Also define the weather forcing that every UTCI number depends on: EPW period, pedestrian-height wind rule and urban offset range. Back both with a bounding script for sun and shade UTCI.

### Why (blocks methodology)
- f1 conflicts across files:
  - `notes/methodology.md` §1: hottest summer week, 12-17 h.
  - §5: three metrics (mean UTCI on sun-exposed sidewalks at 'the design hour'; share of points >32 °C; hours >32 °C over the hot week).
  - §6: Tier 1 UTCI, or a calibrated shade x tau proxy.
  - `notes/topic_decision.md` §7 RQ: 'peak summer hour along sun-exposed routes'.
- Also undefined: the time convention (EPW standard time vs CEST), the sun-exposed domain rule and the minimum difference. Bröde et al. 2012 is '(to add)', and no one has checked whether the 32 °C class limit saturates at midday.
- Inventory C4:
  - The TMYx El Prat period (2009-2023 or 2011-2025) is not chosen, and the file has never been opened.
  - A forum report of missing wind direction is unchecked.
  - §5 has unsourced +1/+2 °C offsets and no pedestrian-height wind rule.
  - El Prat is coastal, while Porta is inland.
- Inventory C3: the UrbClim data location is unconfirmed (the CDS entry is deprecated).

### Context files
- `notes/methodology.md` §1, §5, §6, §10; `notes/topic_decision.md` §3, §7
- `databases/data_inventory_barcelona.md` C3, C4
- `notes/lit/literature_matrix.csv` #35 (Iungman 2023), #37 (Lauwaet 2024, abs)

### Steps
0. Optional user unlock (the agent proceeds without it): climate.onebuilding.org is blocked in the cloud (tested 7 Oct), and databases/*/raw/ is gitignored. The user can allow that host, or commit the TMYx El Prat EPW/DDY to `databases/barcelona/weather/` if the licence allows. If no EPW is there, test the scripts only on raw.githubusercontent.com/ladybug-tools/ladybug/master/tests/assets/epw/chicago.epw, report no numbers from that file, and mark the Barcelona tables 'to compute locally'.
1. Run `pip install ladybug-comfort`, then write `scripts/heat_bounds.py` (bounding only: no geometry, trees or grid) and `scripts/bcn_epw_summary.py`. Candidate days are the hottest TMYx day, a day in the hottest TMYx week and the DDY cooling design day, at 12-17 h, plus one winter design hour. For each, compute:
   - MRT for full shade and full sun with ladybug_comfort.collection.solarcal.OutdoorSolarCal (fraction_body_exposed 0 and 1; record sky_exposure and floor_reflectance);
   - UTCI with ladybug_comfort.utci.universal_thermal_climate_index;
   - wind at 10 m and at pedestrian height with ladybug.windprofile.WindProfile.
   State the time convention.
2. If an EPW is available, summarise it: source period, completeness, wind-direction completeness, wind-speed statistics, summer Ta/RH and the DDY cooling design-day values.
3. Wind rule: document, with sources, the options of using EPW 10 m as is or the WindProfile power law (terrain 'city' vs met 'country'). Check in the ladybug source on GitHub how LB UTCI Comfort uses the EPW wind.
4. Urban offset: bound the range from #35 (the Barcelona value, if given) and #37 (abs), and locate the current UrbClim/Lauwaet 100 m data via WebSearch. Compare with an urban station only if a keyless source is reachable. If a key is needed (Meteocat XEMA, AEMET), draft the request in `notes/data_requests.md` and stop. Do not assume station codes.
5. Verify Bröde et al. 2012 (Int J Biometeorol 56:481-494; confirm the candidate DOI 10.1007/s00484-011-0454-1) and the UTCI stress-class limits. Flag the hours at which sun and shade fall in the same class, or both exceed 32 °C.
6. Write the memo:
   - f1 options: mean UTCI over fixed points; share of points above a class limit; UTCI degree-hours above a limit.
   - A scenario-independent domain rule, e.g. points sunlit with buildings only and no trees, inside the design sub-area.
   - A minimum-difference rule tied to a sourced model error, taken from the heat-validation issue (invent no number).
   - A recommended default and one question for the user.
   Flag it if f1 needs more than one hour, because the §7 RQ says 'peak summer hour'.
7. Update C3 and C4 in data_inventory_barcelona.md: ✅ or ❌ with URL, licence and date, or 'to check locally'.

### Done when
- `notes/decisions/heat_objective.md` has the design-time table with the EPW file name (or 'to compute locally'), the f1 options, the class threshold with the verified Bröde 2012 DOI, the domain rule, the minimum-difference rule, a recommended default and one user question.
- `notes/decisions/weather_forcing.md` has the EPW period options with completeness statistics (or 'to compute locally'), the wind-height options with sources, the urban-offset range with sources, and a recommended default.
- `databases/barcelona/heat_design_hours.csv` (epw_file, day, hour, time_convention, Ta, RH, wind_10m, wind_ped, MRT_shade, MRT_sun, UTCI_shade, UTCI_sun) and `databases/barcelona/epw_summary.csv` exist, or both are marked 'to compute locally' in the memo.
- Both scripts have usage docstrings, and C3/C4 are updated.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- This is a bounding check, not the heat module (CLAUDE.md: Methodology status NOT DEFINED). Do not edit methodology.md or topic_decision.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 7: Heat tree representation, tau correction and validation rule from sources

Labels: `agent-ready`, `lit`, `priority-1`

Agent role: lit-scout

### Goal
Establish, from the ladybug source code and the literature: how Tier 1 treats crowns; whether a sourced tau correction exists; and which Tier 1/Tier 2 agreement and calibration rule the heat validation can use.

### Why (blocks methodology)
`notes/methodology.md` §5 has four gaps:
- Tier 1 treats crowns as opaque, and 'weight the shaded fraction by tau' has no formula or source.
- The mapping from tau to a Radiance transmittance in Tier 2 has no reference.
- The Tier 1 vs Tier 2 comparison has no acceptance criterion, and the §6 'calibrated shade x tau proxy' has no calibration protocol.
- The 'Bath study (to add)' is unidentified, and the optional globe-thermometer measurement has no protocol.

Peng 2026 #53 (abs) reports that field validation shifted shaded MRT by ~3 °C, which is the size of error at stake. The heat-objective memo needs a sourced model error for its minimum-difference rule.

### Context files
- `notes/methodology.md` §5, §6
- `notes/lit/literature_matrix.csv` #46 (Lachapelle 2023, full-text digest), #51, #52, #53
- `notes/lit/to_get_manually.md` (Li et al. 2022 STMRT, DOI 10.1016/j.buildenv.2022.109846)

### Steps
1. Read the ladybug-tools source on GitHub (raw.githubusercontent.com is reachable). Confirm, with file and line references: how 'LB Human to Sky Relation' and 'LB Outdoor Solar MRT' treat context geometry; which input could carry a partial transmissivity (e.g. fraction_body_exposed in OutdoorSolarCal); and how honeybee-radiance sets a shade transmittance modifier.
2. Propose a tau-correction formula only if a source supports it; check STMRT and #46 first. Otherwise write 'no source found'.
3. Identify the 'Bath study' (Ladybug/Honeybee vs ENVI-met MRT/UTCI) with its DOI. If it cannot be found, record 'not found' and recommend removing the claim from §5.
4. From #51, #52, #53 and any further study that validates Ladybug or tree-radiation MRT against field data (Mediterranean preferred), record how trees and LAI enter the model and the reported RMSE/bias, copied exactly with read level.
5. Search for open measured MRT, globe-temperature or UTCI data in Barcelona (university campaigns, superblock studies). Record availability and licence.
6. Propose a Tier 1/Tier 2 agreement metric and an acceptance rule based on the reported errors, plus a calibration check for the proxy. Invent no numbers. List the field measurement (equipment, day, points) as a decision for the user.
7. Append new papers to literature_matrix.csv (next free id; renumber at rebase if needed), and add paywalled ones to to_get_manually.md without duplicates.

### Done when
`notes/method_heat_validation.md` has six sections:
1. Tier 1 crown treatment, with GitHub source references.
2. The candidate tau-correction formula and its source, or 'no source found'.
3. A table of validation sources with DOI, method, exact error values and read level.
4. The Bath study, resolved or marked for removal.
5. Barcelona observation datasets, with status and licence.
6. The proposed Tier 1/Tier 2 acceptance rule and the open field-measurement decision for the user.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Publisher hosts and doi.org are blocked in the cloud, so values seen only in WebSearch summaries are 'search summary' 🟡.
- Bröde 2012 belongs to the heat-objective issue and Monsi & Saeki to the canopy-parameter issue; do not duplicate them. Do not edit methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 8: Replacement scope and S1 baseline: palette, cap headroom, diversity floor

Labels: `agent-ready`, `data`, `analysis`, `priority-1`

Agent role: data-scout

### Goal
Define, with sources or explicit alternatives:
- the candidate palette;
- how many of Porta's 832 planes are replaced;
- what S1 (the like-for-like baseline) is;
- the diversity floor.

### Why (blocks methodology)
- **Palette.** `notes/methodology.md` §6 sets the decision variables as species 'from the feasible palette', but no palette list exists, and the named lists conflict:
  - topic_decision.md §7: Celtis, Melia, Pyrus calleryana, Jacaranda, Tipuana, Brachychiton.
  - Inventory D1 (press): Celtis, Sophora, Melia, Tipuana.
  - `notes/site_selection.md` §5 calls Porta's common species 'the replacements the city names', without a source.
- **S1.** S1 ('the city's named palette in its proportions', §7) has no source. The 379 Porta trees dated 2017 or later are led by Handroanthus heptaphyllus, Grevillea robusta, Fraxinus angustifolia and Casuarina cunninghamiana, then Celtis and Pyrus. 2,266 of the 2,825 trees are undated.
- **Replacement count.**
  - §6 applies the 15% cap locally, while the plan caps the city total (D1).
  - A Porta-local 15% cap allows at most 423 trees per species. At least 409 of the 832 planes must then go, and Celtis has 127 trees of headroom.
  - City-wide, Celtis is already 13.8% (19,384 of 140,404).
  - The plane target conflicts: 15% by 2027 vs 12% by 2037.
  - The replaced set (all 832; the cap minimum; the sub-area only) sets the number of decision variables.
- **Other constraints.**
  - The diversity floor (§6) has no value.
  - The façade-clearance constraint (§6) has no rule.
  - The invasive filters (D4: Melia, Robinia, Ligustrum lucidum) and pest filters (D3: Ceratocystis platani, Xylella fastidiosa) are unconfirmed.

### Context files
- `exchange/to_gh/porta_street_trees.csv`; `databases/barcelona/porta_species.csv`, `species_coverage.csv`
- `notes/methodology.md` §6, §7; `notes/topic_decision.md` §7; `notes/site_selection.md` §5
- `databases/data_inventory_barcelona.md` D1, D3, D4; `literature_matrix.csv` #28 (SylvCiT)

### Steps
1. (Repo only.) Compute the headroom per candidate species under three cap scopes: (a) Porta-local 15%, (b) city-wide 15%, (c) city-wide 12%. Give the minimum number of planes to replace under each scope, and state whether the 3 PLATANOR 'Vallis Clausa' trees count as Platanus.
2. (Repo only.) Compute the species composition of Porta trees planted in 2017 or later, overall and per year, with cultivars stripped to species. Report the undated share as a bias caveat. Write `scripts/porta_recent_plantings.py`, which produces `databases/barcelona/porta_recent_plantings.csv` (species, trees, share, first_year, last_year). Produce the city-wide version only if arbrat_viari.csv is present locally; otherwise mark it 'to check locally'.
3. (Repo only.) Compute Shannon H and exp(H) for S0 and for these candidate S1 mixes: the recent-planting mix; equal shares of the named palette; the current Porta proportions of the palette species. List diversity-floor options: the S0 value; the 10-20-30 rule as used in SylvCiT (Nicol et al. 2026, #28); plan targets, if any.
4. Read the Pla director de l'arbrat 2017-2037 (BCNROC URL in D1). Quote, with page or section:
   - the species lists;
   - the 15% rule and its scope;
   - the plane targets and dates;
   - the climate-adapted list behind the 40% target;
   - any rule linking species size to sidewalk width, street width or façade distance ('not in plan' if absent).
   Search official Ajuntament / Parcs i Jardins pages for a plane-replacement list; anything found only in press is 🟡. bcnroc was blocked in the cloud on 8 Oct: if it still is, mark this step 'to check locally' and keep all three cap scopes as alternatives.
5. Check every candidate against the Spanish invasive catalogue (RD 630/2013 as amended) and any Catalan list. Check pests against EPPO and the Catalan plant-health service. If boe.es or gd.eppo.int are blocked, record the WebSearch findings as 🟡.
6. Write `databases/barcelona/candidate_palette.csv` with the columns: species; in_plan_list (Y/N, page); named_for_plane_replacement (source); invasive_status (source); pest_flags (source); trees_porta; trees_city.
7. Write the memo: S1 options crossed with replacement-count options, with sources; the decision-variable count per option; the diversity-floor options; a recommended default; and one user question. Flag that the S1 choice changes H1 and the species list in the PS.
8. Update D1, D3 and D4 in data_inventory_barcelona.md: ✅ or ❌ with quotes, or the exact remaining gap.

### Done when
- `databases/barcelona/palette_headroom.csv` exists (species, trees_porta, trees_city, headroom_a, headroom_b, headroom_c, source).
- `porta_recent_plantings.csv` and its script exist.
- `candidate_palette.csv` exists, and every non-empty cell has a source.
- `notes/decisions/replacement_scenario.md` has: the headroom table; the minimum replacements per scope; the S1 options; the Shannon values; the floor options; the replacement-location options with decision-variable counts; a recommended default; and one user question.
- D1, D3 and D4 are updated.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Full completion needs these hosts allowlisted, or steps 4-5 run locally: bcnroc.ajuntament.barcelona.cat, www.boe.es, gd.eppo.int, opendata-ajuntament.barcelona.cat. Steps 1-3 and 7 work now.
- Leaf habit stays in species_canopy_params.csv. Write no optimiser code. Do not edit methodology.md or topic_decision.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 9: 20 Oct pack: infographics plan, 5-min talk outline, tutor question sheet

Labels: `agent-ready`, `analysis`, `tutor-question`, `priority-1`

Agent role: method-critic (use the dataviz skill for the figures)

### Goal
Prepare the 20 Oct deliverables that consolidate the other issues: the figure plan and figure data for the literature review, a 5-minute slide storyline, and a one-page tutor question sheet.

### Why (blocks methodology)
- CLAUDE.md deliverables 5-6 for 20 Oct are a literature review with infographics and a 5-minute slide talk (`notes/methodology.md` §10 'to 20 Oct'). There is no figure plan, no talk outline and no slides/ folder.
- `species_measurements.csv` mixes event %, annual % and storage values, so a direct comparison would be invalid.
- The questions only the tutor can settle are scattered:
  - `notes/topic_decision.md` §5 (runoff volume only) and §6.4 (Infrared City (a)-(c));
  - `notes/site_selection.md` §6 (RESCCUE depth maps, 'request via the tutor');
  - CLAUDE.md (Grasshopper requirement, slide format, the unconfirmed 18 Dec date);
  - methodology §8/§10 (Sant Antoni + Florence transfer in 2-10 Dec, while Florence data access is unchecked, topic_decision §5).
- The PS frames the hazard as a peak or surcharge mechanism (>60 mm/h in the first 20 min; sewer capacity), but f2 is event volume, and Selbig 2021 (#10, abs) reports that peak discharge was generally not affected by street trees.
- Infrared City is the in-loop engine 'later' (§5/§6, and §10 4-17 Nov 'if available'), with no fallback date.

### Context files
- CLAUDE.md; `notes/topic_decision.md` §1, §5, §6.1, §6.4, §7; `notes/methodology.md`; `notes/site_selection.md` §6
- `notes/lit/literature_matrix.csv`, `species_measurements.csv`; `databases/barcelona/porta_species.csv`, `species_coverage.csv`
- Any merged `notes/decisions/*.md`, `notes/lit/prior_art_matrix.csv` and `species_canopy_params.csv`

### Steps
1. Run this last (target 16-17 Oct), after the other priority-1 PRs merge. Use placeholders and 'pending' flags for anything not yet merged.
2. Plan 5-6 figures. Each figure lists its source rows and follows an honesty rule: abstract-only rows are shown as (abs), and no axis mixes measure types.
   - (a) Evidence map: matrix rows by bucket x read level.
   - (b) Interception values grouped by measure_type (#1, #2, #3, #7, #8).
   - (c) 'Effect fades with storm size', for H3 (#1, #9, #10, #12, #23, #24, #32).
   - (d) Gap matrix of tools x features (#24, #25, #28, #46, #51, #52, #53, plus prior_art_matrix.csv).
   - (e) Trait coverage of the Porta palette (porta_species.csv x species_coverage.csv).
   - (f) Shared vs conflicting traits for heat and runoff (§6.1 rows #1, #5, #13, #38, #39, #40, #42, #43, #45, #53).
   Write one CSV per figure from verified rows only. Build (a) and (e) now. Build (b), (c) and (f) with a 'provisional' column. Mark (d) 'pending' until prior_art_matrix.csv exists. Use the dataviz skill for any draft figure, and keep exports SVG-compatible with Google Slides.
3. Talk: 6-8 slides with timings totalling 4:30-5:00, in this order: problem, why, RQ, H1-H3, method diagram (data, tree model, two modules, optimiser, S0-S4), literature figures, plan to 18 Dec. Flag the slides that wait on user decisions.
4. Tutor sheet: one table with the columns #, question, context (file §), fallback default, affects (methodology § / H) and answer (blank). Put the questions that change PS/RQ/H first, then data access, then tools and logistics; at most 12 questions, on one page. Include:
   - (i) Runoff volume vs a simple peak proxy. Cite the evidence from #10, #9, #24 (abs) and #32 with read levels. Option (a): volume only, with peak and sewer surcharge out of scope and the PS wording adjusted. Option (b): volume plus the rain depth intercepted within the peak 20-min block of the PDISBA hyetograph. Give the cost of each against §10.
   - (ii) Infrared City, building on §6.4 (a)-(c) without repeating them: access and timing; per-species porosity/LAI/transmissivity; custom EPW and urban offset; batch API and evaluations per day; outputs per point and hour; citability. Add public facts from WebSearch (URL, access date, read level), and confirm the Python SDK's package name at pypi.org/pypi/<name>/json. Add a fallback rule with a blank date: 'if access or per-tree transmissivity is not available by ___, Ladybug Tier 1 plus the tau correction becomes the in-loop engine'.
   - (iii) RESCCUE depth maps; the transfer phase in or out of scope; the Grasshopper requirement; the 18 Dec date; and the tutor questions from merged decision memos.

### Done when
- `notes/lit/infographics_plan.md` lists figures (a)-(f) with source rows, caveats, status (ready / provisional / pending) and CSV name.
- `notes/lit/fig_a_evidence_map.csv` and `fig_e_porta_trait_coverage.csv` exist, and the provisional `fig_b_interception_by_measure.csv`, `fig_c_storm_size.csv` and `fig_f_shared_traits.csv` exist with a provisional column.
- `slides/talk_20oct.md` has a slide-by-slide outline with timings totalling 4:30-5:00 and flags on the slides that wait on decisions.
- `notes/tutor_questions_20oct.md` has the one-page table, the Infrared City facts with URLs and read levels, the fallback rule with a blank date, and a blank answer column.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- infrared.city is blocked for curl in the cloud, so use WebSearch (pypi.org is reachable). Do not edit topic_decision.md or methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 10: Extract PDISBA design storms and intense-storm seasonality

Labels: `needs-user`, `data`, `priority-1`

Agent role: data-scout

### Goal
Extract Barcelona design storms (IDF, hyetographs, climate-change variants) and the monthly frequency of intense storms from primary sources. Propose one T / duration / hyetograph set to use consistently.

### Why (blocks methodology)
- `notes/methodology.md` §4 step 1 uses P(T, d) with T = 1, 2, 10 yr and d = 1 h, but no depth has been extracted (B2 is '🟡 in reports').
- The 1 h duration comes from Tuscany (topic_decision §1, Lompi #19). B1 instead describes Barcelona storms above 60 mm/h in the first 20 min.
- The T sets disagree: v2 uses 2/5/10, the v4 RQ and §4 use 1/2/10, and §6 optimises T = 2 only.
- No hyetograph is chosen, although §4 step 3 needs an event duration and a Gash term needs intensity. The PDISBA climate-change storms are not considered.
- 'Intense rain mainly in autumn' (§1) rests on a Resilience Atlas statement, and no month-by-month frequency exists. H2 and the leaf state of the design storm depend on it. The gauge series are 'on request' or behind an API key (B3).

### Context files
- `databases/data_inventory_barcelona.md` B1, B2, B3
- `notes/methodology.md` §1, §4, §6; `notes/topic_decision.md` §1, §7

### Steps
0. User action: bcnroc.ajuntament.barcelona.cat and diposit.ub.edu are blocked in the cloud (tested 7-8 Oct). Do one of the following, then relabel the issue agent-ready:
   - allowlist them, plus datos.gob.es and the Generalitat open-data portal;
   - download PDISBA Doc2 'Estudi de pluges', the Casas UB thesis and Barcelona Regional 2017 ch. III into a tracked folder (e.g. `databases/barcelona/docs/`, if the licences allow; databases/*/raw/ is gitignored);
   - run the issue in a local session.
1. From PDISBA Doc2, extract with page numbers: the empirical IDF for T = 1-10; the Gumbel tables per gauge; the design hyetographs (shape, duration, time step); and the climate-change variants. Name the gauge closest to Porta (Nou Barris).
2. Cross-check against the generalised Fabra Observatory IDF in the Casas UB thesis (B2).
3. Tabulate depth and peak intensity for d = 10, 20, 30 and 60 min and T = 1, 2, 5 and 10, with and without climate change. Copy values exactly, and leave unknown cells empty.
4. Seasonality:
   - Extract any per-month count of intense events (threshold, period, page) from PDISBA, Casas and Barcelona Regional 2017.
   - Check whether Meteocat XEMA sub-hourly precipitation can be downloaded without a key (the datos.gob.es entry in B3), and look for Fabra Observatory series. If a key is needed, add it to B3 as a user action; do not request one.
   - Do NOT use a TMYx RAIN file: a typical meteorological year is not a sample of extremes.
5. Write an options note on duration (20 min, 1 h, PDISBA design storm), T set and climate uplift. Propose ONE set to use consistently in the §7 RQ, §4 and §6, marked 'pending user decision'. List open multi-year hourly or sub-hourly series for observed-storm replay.
6. Upgrade B2 to ✅ with page references, or keep it 🟡 with the reason.

### Done when
- `databases/barcelona/design_storms.csv` exists (T, duration_min, depth_mm, peak_intensity_mm_h, climate_change Y/N, hyetograph_id, gauge, source, page).
- `design_hyetographs.csv` exists if PDISBA gives hyetographs.
- `databases/barcelona/storm_seasonality.csv` exists (month, threshold, n_events, series, years, source), or a documented gap lists every source tried.
- `notes/decisions/design_storm_set.md` proposes one set, marked 'pending user decision'.
- B2 (and B3, if changed) is updated.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs). Never invent IDF depths.
- The final T/duration set is the user's decision. Do not edit methodology.md or topic_decision.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 11: Pick the shared design sub-area and the runoff spatial unit

Labels: `needs-user`, `analysis`, `priority-1`

Agent role: method-critic

### Goal
Find 2-3 candidate design sub-areas where flood hazard, summer LST and plane stock overlap. Set out how the runoff objective counts tree position (the spatial unit), so that both objectives score the same trees.

### Why (blocks methodology)
- **Two domains.** `notes/methodology.md` §1 computes runoff over all of Porta (0.84 km2), but heat only on a 'design sub-area of 2-4 street segments ... to fix in a block-scale overlay'. §6 makes every replaced plane position a decision variable. Outside the sub-area there is no heat signal, so the S2-S4 and H1/H2 comparisons are inconsistent.
- **Undefined runoff unit.** §4 says 'per street segment' but defines neither the segment nor its contributing surfaces nor the sealed layer (A5 is 🟡, B4 is weak).
- **Position-blind runoff.** With uniform rain and CN 98, total volume barely depends on position. The RQ's 'which species and positions' and H2's 'species, not positions' are therefore partly settled by construction.
- **Validation (iii) has nothing to test.** It is 'plausibility vs the flood-hazard index', but the index encodes sewer capacity, slope and contributing catchment (B1), and the module has no routing.
- **Undefined terms.** 'Sun-exposed routes' (§7 RQ) and 'sun-exposed sidewalks' (§5) are not defined.

### Context files
- `exchange/to_gh/porta_street_trees.csv`, `porta_boundary.csv`, `exchange/site_origin.json` (local origin; EPSG:25831)
- `scripts/bcn_site_screening.py`, `bcn_heat_check.py`, `bcn_site_select.py` (and the raw inputs they read)
- `notes/site_selection.md` §5; `notes/methodology.md` §1, §4, §5, §6, §10
- `databases/data_inventory_barcelona.md` A5, A6, B1, B4

### Steps
0. User action: `databases/barcelona/raw/` (flood_hazard_present.geojson, lst_summer_anomaly.tif) is gitignored and absent in the cloud. urbisadmin.carto.com, planetarycomputer.microsoft.com, opendata-ajuntament.barcelona.cat and www.icgc.cat are blocked. Either run this issue in a local session where the raw files exist, or allowlist those hosts. In the cloud, an agent may do steps 1, 4 (without the LST and flood columns), 5 and 6, leaving the overlay columns as 'to compute locally'.
1. Segment runs: group trees by street, and split long streets into runs of about 100 m using the tree coordinates (no street layer). For each run give n_planes, n_trees, length_m, bearing_deg and the median nearest-neighbour spacing of planes (to show where crowns likely merge).
2. Sample the present flood-hazard index and the summer LST anomaly at each run: flood_share (index ≥40) and mean lst_anom_C. Report the index value at the 832 plane positions: the distribution, the share in the ≥40 band, and the contrast between Av. Meridiana and interior streets.
3. Sealed surfaces: try the ICGC land cover (A5) or the municipal mapa-base-de-vialitat. Using a crown-radius bracket per size class (cited or labelled ASSUMPTION), report the shares of crown area over road, sidewalk, roof and permeable ground. Record in A5 which layer opened (✅), or why not (❌ or 'to check locally').
4. Rank 2-3 candidate sub-areas of 2-4 contiguous runs, comparing the Meridiana edge with the north-east interior. For each, give planes, length, flood share, LST anomaly, orientation, and an estimate of UTCI test points on a 2 m grid (state the sidewalk width assumed).
5. Runoff spatial-unit options:
   - A: total volume (position-blind, stated openly).
   - B: volume weighted by the hazard index at the receiving area.
   - C: volume reaching the high-hazard band along DTM flow paths (data need: ICGC LiDAR DTM; describe it, do not compute D8).
   For each option, give the data needed, the cost against §10, what validation (iii) becomes, and the consequence for H2.
6. Domain framing options:
   - (a) both objectives on the sub-area only;
   - (b) runoff on all of Porta, with only sub-area trees as decision variables;
   - (c) a heat proxy at every position.
   Give the consequences for H1-H3, S0-S4 and the joint Pareto front, then a recommended default and one user question.

### Done when
- `scripts/porta_segments.py` (with a usage docstring) produces `databases/barcelona/porta_segments.csv` (segment_id, street, n_planes, n_trees, length_m, bearing_deg, nn_spacing_m, flood_share, lst_anom_C) and `notes/figures/porta_subarea_candidates.png` (plane positions on the hazard index, with the candidates).
- `notes/decisions/design_subarea.md` has: the hazard table at plane positions; the crown-over-surface shares; 2-3 ranked candidates; runoff options A/B/C; the domain options; a recommended default marked 'pending user decision'; and one question.
- A5 is updated.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Overlay and counts only: no runoff or UTCI computation, no routing, no D8 (CLAUDE.md: Methodology status NOT DEFINED). Do not edit methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 12: Tree size: size_category meaning, LiDAR season, sizes, evaluation horizon

Labels: `needs-user`, `data`, `priority-1`

Agent role: data-scout

### Goal
Pin down:
- what size_category means;
- when the ICGC LiDAR over Porta was flown;
- the sourced planting and mature sizes of the palette species;
- the options for the evaluation horizon and for crown extraction.

### Why (blocks methodology)
- **Size class in H1.** H1 (topic_decision §7) assumes 'the same number and size class of trees'. methodology §3 sizes new trees 'from species size classes at planting and at maturity' with no source, and young vs mature crowns is only an optional scenario (§7).
- **size_category meaning (A1).** It is unconfirmed. In Porta the category tracks planting date, not species: median planting year PRIMERA 2023 (n = 398), SEGONA 2013 (n = 140), TERCERA 2011 (n = 17). 80% of Porta trees are undated. A search summary (8 Oct, unverified) points to a BCNROC Diagonal report (11703/88725) that defines the classes by trunk girth (≤40, 40-80, >80 cm). EXEMPLAR is undefined.
- **LiDAR season (A3).** A3 gives only '2021-23'. A leaf-off flight would under-represent deciduous crowns (Platanus, Celtis, Melia, Pyrus), and shade results depend strongly on crown size and crown base (Helletsgruber 2020 #40).
- **No extraction protocol.** There is no protocol for H, D and Hb (§2-§3), and §10 schedules this work for 21 Oct-3 Nov.
- **Horizon.** The horizon at which S0 (mature planes) and S1-S4 (new trees) are compared dominates both objectives.

### Context files
- `exchange/to_gh/porta_street_trees.csv`, `porta_boundary.csv`, `exchange/site_origin.json`
- `databases/data_inventory_barcelona.md` A1, A3; `notes/methodology.md` §2, §3, §7, §10; `notes/site_selection.md` §5; `literature_matrix.csv` #40

### Steps
0. User action: www.icgc.cat, opendata-ajuntament.barcelona.cat, bcnroc.ajuntament.barcelona.cat and www.fs.usda.gov are blocked in the cloud (8 Oct). Allowlist them, or run steps 1, 2 and 4 locally. In the cloud, an agent can do step 3, the WebSearch parts of steps 1, 2 and 4 (marked 🟡) and the memo in step 5 now.
1. size_category: verify the definition from the arbrat-viari metadata or data dictionary, from the primary text of the BCNROC Diagonal report and, if reachable, from 'Gestió de l'arbrat viari de Barcelona' (2011). Find what EXEMPLAR means.
2. LiDAR: identify the ICGC 1x1 km sheets covering Porta, and record flight dates, point density and class codes from the metadata. State whether the flights were leaf-on or leaf-off for the deciduous palette species, and propose a correction or caveat. If a sheet can be downloaded, read only its header and class counts with laspy; otherwise write out the exact check for the user to run.
3. Cross-tabulate size_category x planting year x species for the palette species from porta_street_trees.csv. Do the city-wide table only if arbrat_viari.csv is available locally; otherwise mark it 'to check locally'. Report dated counts per species.
4. Sizes: for Platanus x acerifolia, Celtis australis, Melia azedarach, Pyrus calleryana, Jacaranda mimosifolia, Tipuana tipu, Brachychiton populneus and Styphnolobium japonicum, find height and crown diameter at planting (nursery or municipal standard) and at maturity, plus growth curves. Candidate sources: the USDA Urban Tree Database (McPherson et al. 2016; verify its coverage) and Mediterranean urban allometry studies. Record value plus source, or 'gap'.
5. Horizon options (at planting, +10 yr, +20 yr, maturity, trajectory): for each, give the consequence for the H1 wording, for comparability with S0 and for data needs. Recommend a default and end with one user question.
6. Crown-extraction options (lower priority, do last): seeded matching with inventory points; CHM watershed; allometric crowns from LiDAR height. Add a literature accuracy table at similar point densities (row trees, crown base, LiDAR-derived LAI) and validation options (a small field sample by the user; agreement with size_category). Build no production pipeline and do not download LAZ for every sheet.

### Done when
- A1 states the definition with its source, marked verified or 'to check locally' with the URL.
- A3 lists the Porta sheet IDs, flight dates, point density and the season caveat, or 'to check locally'.
- `notes/lit/species_size_classes.csv` exists (species, height and crown diameter at planting and at maturity, unit, source URL/DOI, read_level, or 'no value found').
- `notes/decisions/evaluation_horizon.md` has the Porta cross-tab, the growth-source table, the horizon options, a recommended default and one question.
- `notes/method_lidar_trees.md` has the protocol options, the accuracy table and the steps the user must run locally.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- No per-tree crown extraction: that is the tree-module phase after the methodology gate (CLAUDE.md: Methodology status NOT DEFINED). Do not edit methodology.md or topic_decision.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 13: Verify runoff validation datasets and decide the tree-pit term

Labels: `needs-user`, `data`, `priority-1`

Agent role: data-scout

### Goal
Verify which open datasets can validate the runoff module, and define each comparison. Decide whether the tree-pit infiltration term stays (as a species-independent range) or goes.

### Why (blocks methodology)
- `notes/methodology.md` §4 validation has three steps:
  - (i) The Freiburg data are 'open on FreiDok' (matrix #1), but the record, licence, variables and time step are unverified, and a web search during review found no FreiDok record.
  - (ii) Selbig 2021 (#10) and Coville 2022 (#11) are read from abstracts only. Their benchmarks (6,376 L per tree per season; 64-66 L/m2 of canopy over the leaf-on season) are seasonal totals for deciduous ash/maple in Wisconsin, while the module is event-based. No dataset covers a palette species or a Mediterranean climate.
  - (iii) depends on the spatial-unit issue.
- §4 step 3 computes pit area x infiltration rate x event duration from Bartens 2008 (#16) and Zhang 2019 (#17). Both are abstract-only, and both report relative increases in lab or tank studies (+153%; +118% vs +19%), not absolute rates for urban pits.
- Root-driven values also contradict v2 §1, which keeps roots out of the scoring.
- Barcelona pit (escocell) dimensions and surface finishes are unknown (B4), and pavement run-on is undefined.

### Context files
- `notes/methodology.md` §4; `notes/topic_decision.md` §1
- `literature_matrix.csv` #1, #10, #11, #16, #17
- `databases/data_inventory_barcelona.md` B4; `notes/lit/to_get_manually.md`

### Steps
0. User action: freidok.uni-freiburg.de, www.sciencebase.gov, zenodo.org, pangaea.de, bcnroc.ajuntament.barcelona.cat and www.mdpi.com were blocked in the cloud (7-8 Oct). Allowlist them, or run this issue locally. Selbig 2021, Bartens 2008 and Grey et al. 2018 are paywalled; supply them via Zotero or university access if needed.
1. Anys & Weiler 2024 (DOI 10.1002/hyp.15146): find the FreiDok record or the data-availability statement. Record the URL, licence, variables (gross rain, throughfall, stemflow, LAI/PAI per tree), time step, species and period. If the data are downloadable, save them to `databases/validation/raw/` (gitignored) and report only the real column names and row counts; no modelling.
2. Search USGS ScienceBase and data-release DOIs for Selbig 2021 and Coville 2022 (rain, runoff, tree inventory, time step). Try Coville's OA full text (#11, OA hybrid) for the methods.
3. Search Zenodo, PANGAEA and the literature for open throughfall or interception datasets of Mediterranean or urban trees, with Platanus, Celtis, Melia and Quercus ilex first.
4. For each dataset, state which validation it supports (model structure, seasonal magnitude, species parameters) and the comparison protocol: event replay vs seasonal total, the metric (bias, RMSE), and an acceptance rule fixed before the runs. List the unvalidated components as stated limitations.
5. Tree pits:
   - Find the Barcelona escocell specifications (Ajuntament technical specifications, NTJ standards, bcnroc), with page.
   - Compile measured absolute infiltration rates (mm/h) for street-tree pits and compacted urban soils. Zhang 2019 is in an MDPI open-access journal; the fetch was blocked, but the paper is not paywalled.
   - Note any evidence beyond the two lab studies for species dependence.
   - Write the keep/drop decision with a low/high range and the run-on assumption for the user to confirm.

### Done when
- `databases/validation_inventory.md` has one row per dataset (name, DOI/URL, licence, variables, time step, species, climate, verified Y/N, validation step served, protocol), followed by a list of unvalidated components.
- Verified datasets get a 'Validation' row in data_inventory_barcelona.md.
- `notes/lit/tree_pit_infiltration.csv` exists (value, unit, context, source, DOI, read_level).
- `notes/decisions/tree_pit_term.md` gives keep or drop, the range and the run-on assumption, marked 'pending user decision'.
- B4 records the Barcelona pit specification and its source, or '❌ not found'.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- No modelling. Agents cannot obtain data that is only available from authors on request. Do not edit methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---

## Issue 14: Options memo: f1 proxy, optimiser choice and sensitivity plan

Labels: `agent-ready`, `analysis`, `priority-2`

Agent role: method-critic

### Goal
Set out the options for how f1 is computed inside the optimisation loop (Tier 1 directly or a calibrated proxy), which optimiser fits the problem structure, and a sensitivity plan with named parameters, method and run budget.

### Why (blocks methodology)
- `notes/methodology.md` §6 leaves f1 open ('Tier 1 UTCI metric, or a calibrated shade x tau proxy pre-computed per position'), with no calibration design and no acceptance criterion.
- NSGA-II (§6) was chosen without checking the problem structure. With fixed positions, a per-tree runoff term and a cap constraint, the runoff side may be close to separable: S3 could reduce to filling positions with the highest-storage species up to the cap.
- An exact epsilon-constraint integer programme is valid only under three conditions:
  - an additive heat proxy;
  - non-overlapping crowns (rows such as the 194 planes on Av. Meridiana may interlock);
  - a linearised diversity constraint (a Shannon floor is nonlinear).
- The §3 sensitivity plan ('re-run at the low and high ends of the range') names no parameters (S, LAI, k, crown size at the horizon, pit infiltration, CN, the +1/+2 °C EPW offsets in §5), no method and no robustness output.

### Context files
- `notes/methodology.md` §3-§7
- `notes/lit/literature_matrix.csv` (#24 Liu, #25 Nyelele, #46 Lachapelle, #52 Shaamala, #53 Peng); `notes/lit/to_get_manually.md` (Tan 2026, Hao 2023)
- If merged (otherwise use placeholders): `notes/decisions/heat_objective.md`, `design_subarea.md`, `replacement_scenario.md`, `notes/lit/interception_params.csv`, `species_canopy_params.csv`

### Steps
1. Tabulate how comparable studies set the objectives, decision domain, algorithm and proxy validation. Mark (abs) where only the abstract was read.
2. Write option tables:
   - f1 computation: Tier 1 directly, or a proxy with a stated calibration sample size and an acceptance metric (R2 or RMSE vs Tier 1), with the threshold left to the user. The metric definition itself comes from heat_objective.md, and the heat domain from design_subarea.md; do not redo them.
   - Algorithm: NSGA-II, an epsilon-constraint integer programme, or greedy, each with the conditions under which it is valid (additivity, crown overlap, linearised diversity). Use the decision-variable counts from replacement_scenario.md.
3. Draft the sensitivity plan:
   - a parameter list with a range-source column (the trait tables when they exist, else 'pending');
   - one-at-a-time vs Morris screening, with a method source cited or marked (to add);
   - a run-budget estimate in model evaluations for each method;
   - the robustness outputs (species-ranking stability; Pareto shift relative to S1).
4. Recommend defaults and end with one user question.

### Done when
`notes/decisions/optimisation_and_sensitivity.md` contains:
- option tables for f1 computation, algorithm and sensitivity method, each backed by a matrix row or marked 'no evidence found';
- the validity conditions for an exact formulation;
- a run-budget estimate;
- recommended defaults and one user question.

### Constraints
- Never invent citations or numbers; mark unverified items 🟡 and abstract-only values (abs).
- Memo only: write no optimiser code (CLAUDE.md: Methodology status NOT DEFINED). Do not edit methodology.md.
- Run the fact-checker subagent on the diff before committing.

Open a PR from your claude/* branch and summarise findings + remaining gaps in the PR body.

---
