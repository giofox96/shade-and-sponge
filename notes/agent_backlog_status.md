# Agent backlog: status check vs main (8 Oct 2026)

The user's commits 83040d3 (runoff module v1, calibrated canopy storage) and 81042ff (20 Oct talk, infographics, full-text reviews) overlap several issues. Each open issue was compared with `main` at 390e947: one assessor per two issues, then one adversarial verifier for every "done" or "partly done" verdict. #7 was checked by hand.
**For agents:** before starting issue #N, read its section below. Where the section and the issue body differ, the section wins. Values quoted here come from the repo files named; re-check them before reusing.

| Issue | Status |
|---|---|
| [#2](https://github.com/giofox96/shade-and-sponge/issues/2) Bracket whether design-storm runoff can tell species palettes apart | partly done on main |
| [#3](https://github.com/giofox96/shade-and-sponge/issues/3) Options memo: make H1-H3 falsifiable (metric, comparison, threshold) | still open |
| [#4](https://github.com/giofox96/shade-and-sponge/issues/4) Palette canopy parameters, phenology and evidence check (fix PS claim) | partly done on main |
| [#5](https://github.com/giofox96/shade-and-sponge/issues/5) Define canopy storage S, source interception values, verify method refs | partly done on main |
| [#6](https://github.com/giofox96/shade-and-sponge/issues/6) Screen close prior art and draft contribution statements | partly done on main |
| [#7](https://github.com/giofox96/shade-and-sponge/issues/7) Define heat objective f1 and weather forcing (EPW, wind, urban offset) | still open |
| [#8](https://github.com/giofox96/shade-and-sponge/issues/8) Heat tree representation, tau correction and validation rule from sources | partly done on main |
| [#9](https://github.com/giofox96/shade-and-sponge/issues/9) Replacement scope and S1 baseline: palette, cap headroom, diversity floor | still open |
| [#10](https://github.com/giofox96/shade-and-sponge/issues/10) 20 Oct pack: infographics plan, 5-min talk outline, tutor question sheet | partly done on main |
| [#11](https://github.com/giofox96/shade-and-sponge/issues/11) Extract PDISBA design storms and intense-storm seasonality | partly done on main |
| [#12](https://github.com/giofox96/shade-and-sponge/issues/12) Pick the shared design sub-area and the runoff spatial unit | still open |
| [#13](https://github.com/giofox96/shade-and-sponge/issues/13) Tree size: size_category meaning, sizes at planting/maturity, horizon | still open |
| [#14](https://github.com/giofox96/shade-and-sponge/issues/14) Verify runoff validation datasets and decide the tree-pit term | partly done on main |
| [#15](https://github.com/giofox96/shade-and-sponge/issues/15) Options memo: f1 proxy, optimiser choice and sensitivity plan | still open |

## #2: Bracket whether design-storm runoff can tell species palettes apart

**Status: partly done on main.**

### Already on main
Neither Done-when file exists on main (390e947): there is no notes/decisions/ folder and no scripts/explore_runoff_sensitivity.py. User commit 83040d3 covers part of the analysis, but none of the deliverables.
- Done-when (a), table, partly covered:
  - databases/barcelona/runoff_scenarios.csv (from scripts/runoff_model.py) gives interception_m3, runoff_m3, % vs S0 and % vs no street trees for S_none_street, S0_current and R_<species>_mature/young (the six city species each replacing all 809 LiDAR-ok planes). It covers 4 PDISBA storms (P = 19.6 / 31.9 / 62.5 / 21.2 mm), all at s = 1.75.
  - databases/barcelona/runoff_sensitivity_storage.csv adds s = 0.86 / 1.75 / 2.2, but only for S0 vs no street trees.
  - T2-60: S0 −1.85% vs no street trees; mature replacements +0.17% (Jacaranda) to +0.69% (Pyrus) vs S0; young about +0.66 to +0.70%; the s range moves the S0 effect from −0.91% to −2.33% (methodology §4b, line 47).
  - Missing from the table: S1, best, worst, an LAI bracket, and a P sweep below canopy saturation.
- Step 2 (S reading), settled in practice: v1 uses S = s·LAI with s = 1.75 mm per unit LAI, as depth over each crown disk (runoff_model.py lines 87-95; calibrate_interception.py).
  - The fitted per-tree S is 4.27–10.86 mm (interception_calibration.csv), far above 0.59–1.81 mm. So reading (a) cannot reproduce Freiburg. This is my inference from that CSV; main does not state it.
  - methodology §4 step 2 still carries the ambiguous wording.
- Step 5 (evaporation): implicit only. methodology §4b calls s = 1.75 an 'effective' value that includes event evaporation and uses 0.86 mm (Xiao & McPherson 2016) as the lower bound.
- Done-when (b), assumptions, partly covered: runoff_model.py lines 24-27 and 32 mark CN 98/74, background LAI 2.3 and the 3 m young crown as ASSUMPTION; methodology §4b lists the known limits.
- Done-when (c), recommended metric and draft H1/H3 with a minimum meaningful difference: not covered.
- Script item not met: runoff_model.py needs gitignored rasters and OSM calls (databases/barcelona/raw/BarcelonaCiutat_Barris.csv, porta_ndvi_2017.tif, lidar/porta_chm_05m.tif; osmnx at line 67). The issue asks for repo CSVs only.

### Revised scope (do this)
Revised task: an exploratory bracket on the v1 outputs. Do not touch scripts/runoff_model.py; CLAUDE.md line 24 still says NOT DEFINED.

1. Write scripts/explore_runoff_sensitivity.py (with a usage docstring).
   - It reads repo CSVs only: exchange/to_gh/porta_trees_lidar.csv (flag == ok; 809 plane positions), exchange/to_gh/porta_tree_interception_S0.csv, and from databases/barcelona/: porta_species_lidar_summary.csv, porta_species.csv, pdisba_idf_city.csv, runoff_scenarios.csv; plus databases/traits/interception_calibration.csv.
   - Use aggregate arithmetic: volume = Σ crown disk area × min(P, s·LAI).
   - Report the gap to the grid model. Example at T2-60: the per-tree file sums to 456.9 m³; the grid gives a street-tree share of 817.51 − 412.22 = 405.3 m³, because it handles overlap and roof masking and holds the background canopy fixed.
2. Add the palettes v1 lacks:
   - S1: planes replaced by the six species in their Porta proportions (porta_species.csv);
   - best and worst: all positions at the species with the highest or lowest crown area × LAI;
   - optional: the species factor s_sp = s·C_sp/0.86 (methodology §3; Xiao & McPherson 2016, matrix row 3).
3. Sweep P from about 1 to 80 mm and mark the PDISBA depths: T1/T2/T5/T10 at 20 and 60 min, as design intensity × d from pdisba_idf_city.csv. Show the saturation depth: 1.75 × median LAI is 3.5 mm (Celtis, 2.0) to 5.1 mm (Jacaranda, 2.91); per tree, LAI 0.86–7.82 gives 1.5–13.7 mm.
4. At each P, compare the spread between palettes with the spread from:
   - s: 0.86 / IQR about 1.45–1.92 / 2.2;
   - the LAI proxy: palette medians 1.9–2.9, against Freiburg TLS LAI 2.6–4.9;
   - crown size: young 3 m vs the on-site median.
   State whether the palette ranking changes.
5. Use 0.86 vs 1.75 as the bracket for 'surface storage only' vs 'effective storage incl. event evaporation'. Do not add a separate Gash E/R term on top of s = 1.75.
6. Write notes/decisions/runoff_metric_sensitivity.md with:
   - the table, and the assumptions, each sourced or labelled ASSUMPTION;
   - the finding that every tree is saturated at every design storm (largest per-tree S 13.7 mm < smallest storm 19.6 mm; interception_m3 = 817.51 at T1, T2, T10 and T2-20). Palette differences in f2 therefore change with T only through the SCS-CN slope (R_Celtis_mature vs S0: +94.8 / +106.2 / +119.4 m³ at T1/T2/T10), and the palette ranking is identical at every T;
   - metric options: design-storm volume; volume of frequent storms below saturation; canopy storage volume Σ area × s × LAI; seasonal interception (needs gauge data, B3);
   - draft H1/H3 wording with a minimum meaningful difference fixed before the runs (candidate: calibration event RMSE 0.9–3.2 mm, interception_calibration.csv), marked 'pending user decision'.

Done when:
- the memo has the table (P × {S0, S1, best, worst, single-species mature/young} × s low/mid/high × LAI low/high), the assumptions, and a recommended metric with draft H1/H3, all marked pending;
- the script reproduces the table from repo CSVs only.

### Parts of the issue body that now conflict with main
- Constraint 'aggregate arithmetic only, no module': main now has a per-tree 1 m grid runoff module (scripts/runoff_model.py, user commit 83040d3), while CLAUDE.md line 24 still says 'Methodology status: NOT DEFINED'.
- Step 1 (crown brackets per size_category; ASSUMPTION share of sealed ground) is superseded. Main uses LiDAR crowns and a land-cover split: roofs 29% / sealed open space 52% / pervious 19% (methodology §4b line 43).
- Step 2 reopens the S reading. Main implements S = s·LAI, s = 1.75 mm per LAI (calibrated), but methodology §4 step 2 still says 'S from species storage capacity × LAI'.
- The 'Why' line ('0.59–1.81 mm (Xiao 2015, #3, abs)') is outdated. Row 3 is now Xiao & McPherson 2016 in full text: Table 4 range 0.51 (Pyrus) to 1.81 mm, mean 0.86.
- Step 3 says to wait for design_storms.csv before mapping P to T. The PDISBA city IDF is already in databases/barcelona/pdisba_idf_city.csv (inventory §I).
- Step 5 (Gash E/R term) would double-count evaporation, since methodology §4b says the calibrated s already includes it. Main also contradicts itself: the runoff_model.py docstring (line 8) says wet-canopy evaporation is 'ignored'.
- Step 4's S1 (proportional mix) has not been run. v1 replaces all planes with one species at a time (R_<species>_*).
- The issue says H3 is true by construction, but methodology §4b ('supporting H3') and slides/outline_20oct.md slide 9 ('as H3 predicts') present the same model result as evidence.

## #3: Options memo: make H1-H3 falsifiable (metric, comparison, threshold)

**Status: still open.**

### Already on main
Nothing toward the Done-when exists on main. There is no notes/decisions/ folder and no hypothesis_tests.md. Neither 83040d3 nor 81042ff writes any part of the memo.
- The 'Decisions only you can take' bullets in notes/agent_backlog.md (lines 26-34) do not count as progress. They come from commit 9dec783, the same audit commit that produced this issue, and they restate the issue's own option lists. Counting them would be circular. They have no metric or unit, no supported / inconclusive / rejected rule, no reformulations, no S0-S4 table and no draft wording.
- methodology §5 'Metrics' and §6 f2 predate both commits; they are inputs the issue already cites.
- New inputs on main that the memo can now use, but which are not deliverables:
  - f2 values in m³ per scenario and storm: databases/barcelona/runoff_scenarios.csv;
  - a threshold candidate, the event RMSE of 0.9–3.2 mm: databases/traits/interception_calibration.csv;
  - the s spread: runoff_sensitivity_storage.csv;
  - the storm set: pdisba_idf_city.csv;
  - the young vs mature runs.

### Revised scope (do this)
Revised task: write notes/decisions/hypothesis_tests.md. Cite the agent_backlog.md 'Decisions' bullets rather than copying them, and update them with the evidence now on main.

1. H1 section:
   - metric and unit: f2 in m³ at T2-60 (runoff_scenarios.csv) and the f1 metrics in methodology §5;
   - scenarios: S1 vs S4. S1 has not been run (v1 has only single-species R_* runs);
   - comparison options: knee point; best runoff with UTCI no worse than S1; dominance in a pre-fixed share of trait-uncertainty runs;
   - threshold options: calibration RMSE 0.9–3.2 mm; the s spread from runoff_sensitivity_storage.csv; or 'fixed before the runs';
   - a supported / inconclusive / rejected rule for gap-filled species;
   - falsifiability check: S1 lies inside S4, and v1 gives every species the same s, so f2 differs between species only through crown area × LAI;
   - 2-3 reformulations.
2. H2 section, by-construction problems and options:
   - positions are fixed;
   - leaf habit enters neither f1 (summer only) nor f2 (leaf-on LiDAR LAI, storms without a month);
   - f1 (τ = exp(−0.5·LAI), Peng 2026 #53, full text) and f2 both rise with crown area × LAI, so the front may collapse;
   - give options (a)-(e) plus assigning a month to each storm; link #4 and #11.
3. H3 section:
   - every tree is saturated at every design storm (interception_m3 = 817.51 at T1, T2, T10 and T2-20), so avoided runoff is nearly constant in m³ and the % falls because total runoff grows;
   - define 'small' and give threshold options;
   - option to test against the Anys & Weiler field data (row 1), with a hold-out split, since the full dataset already calibrated s;
   - option to state H3 as a declared model boundary.
4. Trade-off metric options, each with a matrix row or 'no source in matrix'.
5. Scenario conditions as now used on main:
   - storms: T1/T2/T10 at 60 min plus T2-20 (T5 available; no hyetograph yet, #11);
   - horizon: young 3 m crown (ASSUMPTION) vs the on-site median (#13);
   - leaf state: implicitly leaf-on (LiDAR flown Sept 2021; calibration on Apr–Sep data).
6. S0-S4 consequence table, including the existing S_none_street and R_* runs.
7. Draft RQ/H1-H3 wording labelled 'changes PS/RQ/H: user decides'. List the files it would touch: topic_decision §7, methodology §4b/§7, outline_20oct slides 7 and 9.
8. One user question and one tutor question.

Done when: the original Done-when list is met, every value traces to a literature_matrix.csv row or a repo CSV (or is marked to add), and no other file changes. Run after #2 or reuse its result.

### Parts of the issue body that now conflict with main
- The H3 rationale is outdated. The issue blames 'pit infiltration that does not depend on T at the fixed d = 1 h', but v1 does not model tree pits at all (methodology §4b, Known limits). The by-construction effect comes from canopy saturation: interception is identical at every T in runoff_scenarios.csv.
- methodology §4b ('The benefit shrinks with return period, supporting H3') and slides/outline_20oct.md slide 9 ('as H3 predicts') treat H3 as supported by the model. The issue's premise is that this result is not evidence. The user should reconcile the two before the talk.
- Step 5's 'to check locally while PDISBA is unread' is outdated. The PDISBA city IDF has been read (pdisba_idf_city.csv; inventory §I), and main already uses T1/T2/T10-60 plus T2-20. Only the design hyetograph is still missing.
- The context tags are outdated: Peng 2026 (#53) and Shaamala 2025 (#52) are now full text, not '(abs)'.
- The planned inputs heat_objective.md, replacement_scenario.md and design_subarea.md do not exist.
- slides/outline_20oct.md slide 7 already fixes short H1-H3 wording for 20 Oct, so any reformulation changes the talk.

## #4: Palette canopy parameters, phenology and evidence check (fix PS claim)

**Status: partly done on main.**

### Already on main
None of the four Done-when items is met: species_canopy_params.csv, replacement_species_evidence.md and method_traits.md do not exist, and the required matrix rows are missing. Partial progress from 81042ff:
(1) PS claim partly corrected. notes/topic_decision.md §7 problem statement (line 121) now says 'only Pyrus calleryana has a measured canopy-storage value (Xiao & McPherson 2016), and none has a measured cooling value', with the Silva 2025 caveat. The interception half is fixed; the cooling half is not (see conflicts).
(2) k decided. notes/methodology.md §3 line 31 fixes k = 0.5 'as in Peng et al. (2026) and in our LiDAR LAI proxy'. Monsi & Saeki 1953 is still '(to add)', with no DOI.
(3) Evidence classification, as a figure only. scripts/make_infographics.py fig_palette (lines 245-286), output slides/fig/05_palette_data_gap.svg/png, rates the 7 palette species for LiDAR crown, rain storage measured and cooling measured. Footnotes cover the Celtis congener, the Pyrus/Silva caveat and Tipuana as second-hand. It does not mention Armson.
(4) species_measurements.csv rows new in 81042ff: Silva 2025 Pyrus UTCI 3.53–6.27 °C (full text, replacing the abs row) and Santos Nouri 2018 Tipuana PET 15.6 °C (secondary, via Silva). It also gained Xiao/Baptista storage rows, which belong to #5.
   - Correction to the earlier claim: the Armson 2013 Pyrus/Crataegus rows ('see paper', no matrix_row) predate these commits (the issue's Why cites them).
   - Correction: the Baptista '90% leaf-off' note is in literature_matrix row 6, not in species_measurements.
(5) LAI and phenology: databases/traits/porta_trait_table.csv has the LiDAR LAI proxy and BROT phenology (Celtis australis, Fraxinus angustifolia and Populus alba only). Both came from ca18c02, which the issue's update already covers, not from the new commits. methodology §4b compares the proxy only with Freiburg TLS LAI (Tilia/Acer 2.6–4.9).
Not present: no transmissivity or leaf-off LAI, no leaf-out/fall months, no wood porosity; no gap-filling rules or class sizes; no query log; no literature_matrix rows for Armson 2013, Abreu-Harbich 2012 or Santos Nouri 2018 (matrix ends at id 56).

### Revised scope (do this)
Revised task: build on porta_trait_table.csv, species_measurements.csv, fig 05 and the already-revised PS.
1. Create notes/lit/species_canopy_params.csv with columns species, parameter, value_or_range, unit, source, DOI, region, read_level.
   - Species: the 8 palette species (Platanus, Celtis australis, Melia, Pyrus calleryana, Jacaranda, Tipuana, Brachychiton, Styphnolobium), plus the 6 optional taxa at genus or class level.
   - Parameters: summer LAI range; leaf-off LAI; transmissivity leaf-on/off (or k with its basis); leaf habit (flag Jacaranda and Tipuana as uncertain); Mediterranean leaf-out and leaf-fall months; wood porosity (InsideWood).
   - Reference the LiDAR and BROT values in porta_trait_table.csv; do not copy them.
   - Write 'no value found' where nothing exists.
   - Compare the literature LAI with the LiDAR proxy for each species.
2. Write notes/lit/replacement_species_evidence.md:
   - evidence class per species, with matrix ids and read levels, and the query log;
   - a sourced replacement for the clause 'none has a measured cooling value' (see conflicts);
   - whether Santos Nouri et al. 2018 (10.3390/atmos9010012) is measured or simulated;
   - whether Styphnolobium belongs in the named palette (Yang 2019 #5; Ji 2025 for interception);
   - every file that repeats the claim: topic_decision §7; outline_20oct slide 6 script; make_infographics.py lines 279-280 and fig 05; data_inventory D2 and §E.2; methodology §3 gap list. Propose wording only; do not edit these files.
3. Write notes/method_traits.md:
   - the verified Monsi & Saeki citation and DOI;
   - note that methodology §3 already fixes k = 0.5 (Peng 2026 #53); treat species-specific k as a sensitivity question only;
   - 2-3 gap-filling rules with the number of measured species per class (flag classes with fewer than 2);
   - coverage % per parameter and per species;
   - the PDFs to fetch.
4. literature_matrix.csv: add rows from id 57 for Armson 2013 (10.48044/jauf.2013.021), Abreu-Harbich 2012, Santos Nouri 2018 and any new source. Back-fill matrix_row on the Armson species_measurements rows, add new measurement rows, and add paywalled papers to to_get_manually.md without duplicates.
Done when: the three files exist with this content; the cooling clause has a sourced replacement sentence and a list of files to change; the matrix, species_measurements and to_get_manually rows are added.

### Parts of the issue body that now conflict with main
1. The issue quotes the old PS ('no measured canopy-interception or cooling value'). Main's PS already credits Pyrus storage (Xiao & McPherson 2016) and Silva 2025, so step 8 now targets only the cooling clause.
   - That clause is contradicted by the repo itself. The Armson 2013 abstract (shortlist.csv line 115; candidates_heat.csv line 178) says Pyrus calleryana and Crataegus 'provided significantly more cooling' (measured surface temperature; mean −12 °C surface and −4 °C MRT across species, abs).
   - Abreu-Harbich 2012 (candidates_heat.csv line 49) reports field measurements 2007–2010 plus shade simulation, including a Tipuana tipu cluster (abs).
   - The claim has also spread to outline_20oct slide 6 and to fig 05 (make_infographics.py lines 279-280).
2. methodology §3 no longer says 'k from the literature'; it fixes k = 0.5. Asking 'fixed or species-specific' would reopen a decision already written on main.
3. The issue says Silva #47 is (abs). It is now full text (row 47), and Pyrus also has a storage value of 0.51 mm (Xiao & McPherson 2016, row 3).
4. Palette naming is inconsistent: inventory D1 names Sophora (Styphnolobium), the PS list omits it, and the issue includes it.
5. notes/todo_manual.md already asks the user for a TRY request (leaf phenology, vessel anatomy) and for Santos Nouri 2018. Phenology and porosity rows should point to that pending source instead of duplicating it.

## #5: Define canopy storage S, source interception values, verify method refs

**Status: partly done on main.**

### Already on main
None of the four Done-when items is met. Partial progress:
(1) The bucket definition of S is implemented and calibrated, but not written in the required file.
   - methodology §4b line 46 states S = s·LAI, s = 1.75 mm per unit LAI, calibrated on Anys & Weiler 2024 (scripts/calibrate_interception.py).
   - databases/traits/interception_calibration.csv also gives s_per_PAI, 1.06–2.85 per tree; databases/barcelona/runoff_params.json holds the parameters.
   - scripts/runoff_model.py (line 5; storage_raster, lines 87-95) applies I = min(P, s·LAI) as a depth over each crown disk, taking the max where crowns overlap and setting S to 0 over roofs.
   - Sensitivity runs for s = 0.86 / 1.75 / 2.2 are in runoff_sensitivity_storage.csv.
   - This settles the factor-of-LAI ambiguity for the implemented bucket.
(2) Storage values from full text (81042ff):
   - Xiao & McPherson 2016 (#3): Platanus × hispanica 0.87, Pyrus calleryana 0.51 and Celtis sinensis 0.71 mm per unit leaf + stem surface area;
   - Baptista 2018 (#6): Platanus Cmax/Cmin 0.49/0.29 mm per canopy projected area, flagged as rain-limited.
   - They appear in species_measurements.csv, in the porta_trait_table.csv lit_runoff column and in methodology §3. This closes the issue's 'Platanus value not yet extracted' gap.
(3) Method refs: the Gash refinement is named (methodology §4 step 2: Hassan 2017, Huang 2017), and TR-55 is mentioned in runoff_model.py (lines 9, 24-25), but neither has a DOI or URL.
Not present:
- notes/decisions/ and interception_parameter_definition.md;
- Gash or i-Tree parameter definitions;
- notes/lit/interception_params.csv; any E/R value;
- values for Melia, Jacaranda, Tipuana, Brachychiton, Citrus, Robinia, Catalpa, Grevillea, Casuarina, Populus;
- notes/lit/method_references.md; a source for the 45%→72% sealing figure;
- the measure_type column;
- a Ji 2025 matrix row (only candidates.csv line 49);
- the 'carries PS/H/validation' block in to_get_manually.md.

### Revised scope (do this)
Revised task: document what runoff v1 already does, then fill the gaps around it.
1. notes/decisions/interception_parameter_definition.md:
   - Write down the implemented definition: S [mm over crown projected area] = s [mm per unit one-sided LAI] × LAI; I = min(P, S); max where crowns overlap; 0 over roofs; s = 1.75 calibrated (Anys & Weiler 2024), an effective value that includes event evaporation. Cite runoff_model.py and calibrate_interception.py.
   - Reconcile the reference areas used on main:
     - Xiao & McPherson 0.86 mm is per unit leaf + stem surface, yet it is used as the lower bound of s per LAI (§4b) and as the divisor in s_sp = s·C_sp/0.86 (§3);
     - Baptista Cmax is per canopy projected area;
     - bridge them with the calibration s_per_PAI.
   - Add the parameter definitions and units for the revised Gash model (Gash 1979; Gash et al. 1995) and for i-Tree Hydro / UFORE leaf and bark storage.
   - Propose a rewording of methodology §4 step 2. Do not edit methodology.md.
2. notes/lit/interception_params.csv for the 13 Porta taxa:
   - seed it with the full-text values already in species_measurements.csv and with interception_calibration.csv (Tilia/Acer s per LAI and per PAI), stating reference_area for each;
   - search the 10 uncovered taxa and their genera;
   - find E/R values (Huang 2017 #33, Hassan 2017 #8, Llorens 2006);
   - extract the Yang 2019 #5 Styphnolobium value if an OA copy is reachable;
   - build genus and leaf-habit ranges (min / median / max / n), leaving cells blank where nothing exists.
3. notes/lit/method_references.md:
   - verify NEH-630 ch. 10, TR-55, Gash 1979, Gash et al. 1995 and Deb et al. 2002, and record how each was verified;
   - find the primary source for '45% to 72% (1956-2009)' or flag it for removal. The claim is in topic_decision §7 and on outline_20oct slide 2 (bullet and script).
4. Data rows:
   - add measure_type to all 32 rows of species_measurements.csv;
   - add Ji et al. 2025 (10.1016/j.ufug.2025.129068) to literature_matrix.csv as (abs), id 57 or the next free id, noting that it qualifies the §1 traits-vs-biomass row and the H1 mechanism;
   - open to_get_manually.md with a 'carries PS/H/validation' block (#4 Dowtin, #9 Kuehler, #10 Selbig, #34, #38, #39, Llorens 2006), naming the table or figure needed from each;
   - tick or remove the entries already read in full: Xiao 2015 (line 22), Baptista (9), Silva (33), Mannucci (37), Shaamala (38), Peng (47), Wu (71).
Done when: the definition md, interception_params.csv (13 taxa, direct or as a flagged genus/class) and method_references.md exist; measure_type is filled for every row; the Ji 2025 row is present; to_get_manually.md opens with the 'carries PS/H/validation' block.

### Parts of the issue body that now conflict with main
1. The issue calls 'S from species storage capacity × LAI' dimensionally undefined and asks for a new definition. Main has already implemented and calibrated S = s·LAI (methodology §4b; runoff_model.py; runoff_params.json), so the document must record and reconcile that choice, not re-decide it. The ambiguous §4 step 2 wording is still on main, and §3/§4b mix s per LAI with Xiao's per-leaf + stem-area values.
2. Step 2 asks to try open copies of Baptista (#6) and Xiao (#3). Both are now full text (rows 3 and 6, 'full text (8 Oct)'), so that step is moot. Only Yang 2019 #5 (Styphnolobium) is still unextracted.
3. topic_decision.md is internally stale: the §5 Xiao full-text check is unticked, and the §1 traits-vs-biomass row still cites 'Xiao et al. #3 (abs)'.
4. The unsourced 45%→72% sealing claim is now also on slide 2 of slides/outline_20oct.md, so a removal flag affects the 20 Oct talk.
5. to_get_manually.md still lists papers already read in full. The new block must not re-list them.

## #6: Screen close prior art and draft contribution statements

**Status: partly done on main.**

### Already on main
None of the three Done-when files exists: notes/lit/prior_art_matrix.csv, notes/decisions/ and contribution_statement.md are all missing. Partial progress from 81042ff:
(1) The novelty papers are read in full. literature_matrix.csv rows 51 (Mannucci 2025), 52 (Shaamala 2025) and 53 (Peng 2026) are 'full text (8 Oct)', with their limits recorded:
   - Mannucci: scenario testing only, no species traits, no optimisation;
   - Shaamala: UTCI only, and names multi-objective work with water sensitivity as future work;
   - Peng: generic tree types.
   This completes step 2 for those three papers.
(2) One of the 8 T2 papers is in the matrix: Wu 2024 (10.3390/su16125201), row 56, full text, 'does not fill our gap'.
(3) An informal verdict exists in three places:
   - notes/todo_manual.md line 17: 'The gap holds';
   - the reworded gap in topic_decision.md §7 v4 (line 121);
   - slides/outline_20oct.md slide 6.
(4) A small feature matrix exists only as a figure: make_infographics.py fig_gap() (lines 214-242) produces slides/fig/04_gap_matrix.
   - 6 precedents × 4 features, with no read_level column and not the issue's columns;
   - only rows 51, 52, 53 and 56 are among the 12 required papers;
   - its footer says 'Still to screen: Tan et al. 2026'.
(5) The Tan 2026 full text is a user task (todo_manual.md line 18).
Not done: the screen of Xing, Hao, Elkhateeb, Oneto, Eslami, Liang, Tan and Nyelele; the logged WebSearch round; contribution statements.

### Revised scope (do this)
Revised task: build on rows 51-53 and 56 and on fig 04; do not redo them.
1. Screen the papers not yet in the matrix.
   - From the abstracts stored in notes/lit/shortlist.csv: Xing 2026 (10.3390/su18042142), Hao 2023 (10.1016/j.ufug.2023.128017), Elkhateeb 2025 (10.3390/urbansci9120504), Oneto 2026 (10.1016/j.ufug.2026.129457), Eslami 2026 (10.71573/zhbx9v70).
   - With WebSearch, because no abstract is stored: Tan 2026 (10.1016/j.scs.2026.107726) and Liang 2021 (10.1016/j.scitotenv.2021.146415).
   - Nyelele 2021 (#25): only 237 characters of abstract are stored, so complete it with WebSearch.
2. Run one logged WebSearch round (2022-2026) for work that combines street-tree species selection or placement with both UTCI/MRT and runoff. Record the queries and the hit counts.
3. Write notes/lit/prior_art_matrix.csv with at least 12 rows: #25, #51, #52, #53, #56, the 7 new T2 papers and any new hits.
   - Columns: id, citation, doi, species_level_traits, heat_metric, runoff_metric, placement_optimised, species_optimised, multi_objective, mediterranean, validation_type, read_level.
   - Code the features as fig 04 does. Optionally add #28 and #18 so the CSV matches the figure.
4. Add the 7 new papers to literature_matrix.csv as ids 57-63; do not re-add Wu.
5. Write notes/decisions/contribution_statement.md with:
   - 2-3 cited contribution statements, each tied to a matrix row;
   - a verdict on the gap as now worded (topic_decision §7 v4, slide 6, fig 04): holds / narrower wording / does not hold;
   - the read level behind the verdict (full text for 4 papers, abstracts for the rest);
   - the search log;
   - the fetch list: reference the todo_manual Tan item, then add Nyelele and any abstract that could flip the verdict;
   - a flag if fig 04 or slide 6 needs a new row.
Done when: prior_art_matrix.csv has 12 or more rows, each with read_level; literature_matrix.csv has ids 57+ with no duplicates; contribution_statement.md has the statements, verdict, search log and fetch list.

### Parts of the issue body that now conflict with main
(a) The issue's Why says #51-53 are abstract-only. They are now full text, so step 2 is moot except for #25 Nyelele.
(b) Wu 2024 is one of the 8 'new' T2 papers but is already row 56. The next free id is 57.
(c) The issue asks for a verdict on the topic_decision §6.1 claim. The current wording is in §7 v4 (line 121), slide 6 and fig 04. The §6.1 table (line 82) still marks #51-53 '(abs)' and is stale; the memo should point that out, not edit it.
(d) 'Expect an abstract-level verdict' is outdated: the 4 closest precedents are now full text.
(e) todo_manual.md line 17 already says 'The gap holds' without Tan 2026 or the other T2 papers. The memo must confirm or qualify that statement.
(f) The Tan 2026 full text is already a user task (todo_manual line 18), and to_get_manually.md still lists Mannucci/Shaamala/Peng (lines 37, 38, 47) and Wu (line 71) as missing, although all four are now read in full.

## #7: Define heat objective f1 and weather forcing (EPW, wind, urban offset)

**Status: still open.**

### Already on main
Nothing toward the Done-when exists on main: no notes/decisions/heat_objective.md or weather_forcing.md, no scripts/heat_bounds.py or bcn_epw_summary.py, no heat_design_hours.csv or epw_summary.csv. methodology §5 still lists three candidate metrics, Bröde 2012 is still *(to add)*, and inventory C3/C4 are still 🟡.

### Revised scope (do this)
The original scope stands unchanged. New context on main that the memo should use: methodology §5 now has the Peng 2026 τ correction (k = 0.5), the Mannucci 2025 Ladybug vs ENVI-met errors (UTCI MBE 0.8–2.3 °C, CVRMSE 7–13%), and the proxy-cost figures (Shaamala 2025; Peng 2026). Use those errors as the candidate minimum-difference source instead of a new search. notes/todo_manual.md suggests the user run one Ladybug Tier 1 test, using the TMYx El Prat EPW, so check exchange/from_gh/ for an EPW or run log before marking the tables 'to compute locally'.

### Parts of the issue body that now conflict with main
None found. slides/outline_20oct.md already presents the heat metric for 20 Oct, so any change to f1 also changes the talk; flag it.

## #8: Heat tree representation, tau correction and validation rule from sources

**Status: partly done on main.**

### Already on main
notes/method_heat_validation.md does not exist on main. Some of its content is now in other files:
- Done-when 2 (τ formula and source): met in substance.
  - methodology §5 line 53: crowns are opaque in Tier 1, and shade MRT runs more than 6 °C below globe measurements. The fix is 'as in Peng et al. (2026): multiply direct radiation under the crown by τ = exp(−0.5·LAI) in the SolarCal step', which brought shade MRT within 2–4 °C.
  - methodology §3 line 31 fixes k = 0.5.
  - Source: literature_matrix.csv row 53 (DOI 10.1007/s10980-026-02324-z, full text): measured 46.5–48.6 °C, original LBT 42.1–44.0 °C, LAI-revised 45.2–46.5 °C.
  - Not stated anywhere: which ladybug input or code path carries τ.
- Done-when 4 (Bath study): met in substance by removal. Commit 81042ff removed 'Bath study (to add)' from methodology §5 Validation (line 58) and cites Mannucci 2025 instead: UTCI MBE 0.8–2.3 °C, CVRMSE 7–13%; MRT CVRMSE 22–38% (row 51, full text). The Bath study itself was never identified, and the swap is not recorded anywhere.
- Done-when 3 (validation table): partial. Rows 51 and 53 give DOI, method, how trees enter and the exact errors, but there is no consolidated table and no search beyond them. STMRT (Li 2022) is unread (to_get_manually.md line 48).
- Done-when 6 (acceptance rule and field decision): decision side only. todo_manual.md line 41 asks the user whether to drop the Porta MRT check; methodology §5 keeps 'optional MRT spot measurements'. There is no acceptance rule.
- Update-8-Oct note: implicit only. §3 uses the same k = 0.5 as the LiDAR LAI proxy; §4b and inventory §G call the proxy uncalibrated, probably low, and 'for ranking only'.
- Done-when 1 (GitHub source refs) and 5 (Barcelona observation datasets): not met.

### Revised scope (do this)
Revised task: write notes/method_heat_validation.md with six sections. Build on methodology §3/§5 and matrix rows 51 and 53; do not re-derive them.
1. Tier 1 crown treatment, with file and line refs in ladybug-tools on GitHub: LB Human to Sky Relation, LB Outdoor Solar MRT, ladybug-comfort OutdoorSolarCal / fraction_body_exposed.
   - State which input or code path applies Peng's τ to direct radiation under a crown, and whether sky view / diffuse radiation also needs it.
   - Give the honeybee-radiance shade transmittance modifier and a reference for the τ → Radiance transmittance mapping (Tier 2).
2. τ: record τ = exp(−0.5·LAI) (Peng 2026 #53) and its limit (constant k).
   - Answer the update note: can the per-species LiDAR LAI proxy (porta_species_lidar_summary.csv; palette 1.9–2.9) feed τ, and what calibration does it need? See the methodology §4b limits.
   - Check STMRT if reachable.
3. Validation table: rows 51 and 53 plus further field validations of Ladybug or tree MRT (Mediterranean preferred), with DOI, how trees and LAI enter, exact RMSE/bias, and read level.
4. Bath study: one line saying methodology §5 replaced it with Mannucci 2025 on 8 Oct. Run one DOI search, otherwise mark it 'not found'.
5. Open measured MRT, globe-temperature or UTCI data in Barcelona, with status and licence.
6. A Tier 1/Tier 2 agreement metric and acceptance rule grounded on the sourced errors (Mannucci MBE/CVRMSE; Peng 2–4 °C residual), plus a calibration check for the §6 shade × τ proxy. Frame the field measurement as a user decision, linked to todo_manual.md line 41.
7. New papers go into literature_matrix.csv from id 57; avoid duplicates in to_get_manually.md.
Done when: the file exists with these six sections, every number is sourced or marked 🟡/(abs), and methodology.md is untouched.

### Parts of the issue body that now conflict with main
- The Why says 'weight the shaded fraction by tau' has no formula or source. Main now has both (methodology §5 line 53, §3 line 31: τ = exp(−0.5·LAI), Peng 2026), so the 'no source found' branch of step 2 is moot.
- The issue cites 'Peng 2026 #53 (abs) … ~3 °C'. Row 53 is now full text: the original LBT is more than 6 °C low and the LAI-revised model is within 2–4 °C. Both the read level and the figure are out of date.
- 'The Bath study (to add) is unidentified' and step 3's 'recommend removing it': 81042ff already removed it from methodology §5 and replaced it with Mannucci 2025 (#51).
- Step 7's 'next free id' is now 57, because row 56 (Wu 2024) was added.

## #9: Replacement scope and S1 baseline: palette, cap headroom, diversity floor

**Status: still open.**

### Already on main
—

### Revised scope (do this)
Every Done-when item is still to do. None of these exist on main (390e947): databases/barcelona/palette_headroom.csv, porta_recent_plantings.csv, scripts/porta_recent_plantings.py, candidate_palette.csv, notes/decisions/. Inventory rows D1, D3 and D4 (databases/data_inventory_barcelona.md lines 42, 44, 45) are still 🟡 with no plan quotes; 83040d3 only added §I. Revised task, building on what now exists:
1. palette_headroom.csv (species, trees_porta, trees_city, headroom_a/b/c, source). Porta counts: databases/barcelona/porta_species.csv. City counts: species_coverage.csv (140,404 trees). Give the minimum number of plane replacements per cap scope. Document an answer main already applies without saying so: the 3 PLATANOR 'Vallis Clausa' trees are counted as planes, because is_plane = species.startswith('Platanus') (scripts/bcn_lidar_porta.py line 121). So 832 = 829 + 3 in exchange/to_gh/porta_street_trees.csv.
2. scripts/porta_recent_plantings.py → porta_recent_plantings.csv (species, trees, share, first_year, last_year), with cultivars stripped. The issue's counts still hold: 379 trees dated 2017 or later, led by Handroanthus 45, Grevillea 44, Fraxinus angustifolia 44, Casuarina 41, Celtis 33, Pyrus 28; 2,266 of 2,825 undated. Produce the city-wide version only if arbrat_viari.csv is local.
3. Shannon H and exp(H) for S0 and for the candidate S1 mixes; list the diversity-floor options.
4. Plan quotes from bcnroc, or mark 'to check locally'.
5. Invasive check (RD 630/2013) and pest check (EPPO/DARP), marked 🟡 if only search summaries are reachable.
6. candidate_palette.csv. At minimum: the six species now hard-coded in scripts/runoff_model.py CANDIDATES (line 30) and in figure 05; Sophora/Styphnolobium (D1 press list; already in databases/traits/porta_trait_table.csv); the leaders among recent plantings.
7. notes/decisions/replacement_scenario.md. Contents: headroom table, minimum replacements per scope, S1 options, Shannon values, floor options, replacement-location options with decision-variable counts, recommended default, one user question. Also flag:
   - that the runoff-v1 R_* scenarios are single-species sensitivity runs, not S1. They replace all planes with one species (methodology §4b; databases/barcelona/runoff_scenarios.csv);
   - that S1 drives H1 and the PS species list (topic_decision §7; slides 3, 6 and 8; slides/fig/05_palette_data_gap).
8. Update D1, D3 and D4.
Done when: unchanged from the issue.

### Parts of the issue body that now conflict with main
- More files now rely on the unsourced six-species list (Celtis, Melia, Pyrus calleryana, Jacaranda, Tipuana, Brachychiton) as 'the replacement species the city names':
  - scripts/runoff_model.py CANDIDATES (line 30) and methodology §3/§4b results;
  - scripts/make_infographics.py line 283 ('the six replacement species the city names') → slides/fig/05_palette_data_gap;
  - slides/outline_20oct.md slides 3 and 6;
  - topic_decision §7 PS.
  Inventory D1's press list (Celtis, Sophora, Melia, Tipuana) still differs. The palette conflict the issue describes is still open, and now has downstream dependents in the 20 Oct talk.
- The issue treats the replaced set as open (all 832 / cap minimum / sub-area only). Main already assumes all 832:
  - slides/outline_20oct.md slide 8 (line 52): 'An NSGA-II search chooses the species at each of the 832 plane positions, under the city's 15 percent rule and a diversity floor';
  - methodology §6 'Why proxies are needed' (line 65): 'Porta's 832 plane positions need a pre-computed shade × τ proxy'.
  The memo's recommended default must either confirm this or flag that the talk and methodology need changing.
- Methodology §4b reports scenarios that replace all planes with a single species. Under any of the issue's three cap scopes these layouts break the 15% rule, so they must not be read as S1. S1 is still undefined in methodology §7.

## #10: 20 Oct pack: infographics plan, 5-min talk outline, tutor question sheet

**Status: partly done on main.**

### Already on main
Commit 81042ff covers most of the figure and talk content, under other names. It covers none of the plan, CSV or tutor-sheet deliverables.
- Figures: 6 SVG+PNG in slides/fig/, built by scripts/make_infographics.py. Each footer lists source rows, and '*' marks abstract-only rows.
  - (a) evidence map = 01_lit_map (bucket × read level, from literature_matrix.csv);
  - (b) interception values = left panel of 02_runoff_evidence (species_measurements.csv, plus a Xiao & McPherson storage note);
  - (c) effect fades with storm size = right panel of 02 (cards for Liu 2026*, Esraz-Ul-Zannat 2024, Selbig 2021* and Xiao & McPherson 2016);
  - (d) gap matrix = 04_gap_matrix (rows 18, 28, 51-53, 56);
  - (e) palette trait coverage = 05_palette_data_gap (porta_trait_table.csv);
  - (f) shared vs conflicting traits = 03_heat_runoff_traits (rows 1, 3, 6, 9, 10, 13, 38-40, 42, 43, 45, 53, 56);
  - extra: 06_method_pipeline.
- Talk (Done-when 3), largely met in substance:
  - slides/outline_20oct.md has 9 slides with cumulative timings to [5:00], about 674 words of 'Say' text (about 4:49 at 140 wpm), plus backup slides and likely questions;
  - it differs from the brief: 9 slides instead of 6-8, a different order, a different file name, and no decision flags.
- Tutor-question content exists but not the sheet:
  - todo_manual.md 'Email the tutor': RESCCUE depth maps, Infrared City (a)-(c), the 18 Dec date, the Grasshopper requirement, the slide format;
  - agent_backlog.md lines 38-47: 10 tutor questions.

### Revised scope (do this)
Revised task: build on slides/fig, make_infographics.py and slides/outline_20oct.md; do not recreate them.
1. Write notes/lit/infographics_plan.md mapping (a)-(f) to the existing files: 01; 02 left; 02 right; 04; 05; 03; with 06 as an extra.
   - For each, give the source rows (from the figure footers), caveats, status (ready / provisional / pending) and CSV name.
   - Flag: 02 left puts event-mean %, annual % and share % on one axis, so split it by measure type or mark it provisional; 04 is pending the Tan 2026 screen; '55 papers' is hard-coded in the 01 subtitle (make_infographics.py line 124) and in the slide 4 script, while the matrix has 56 rows.
2. Export notes/lit/fig_a_evidence_map.csv and fig_e_porta_trait_coverage.csv (ready), plus fig_b_interception_by_measure.csv, fig_c_storm_size.csv and fig_f_shared_traits.csv with a provisional column.
   - Export them from make_infographics.py so the figures and CSVs share the same rows.
   - Include the storm-size card values and trait-panel claims that are now hard-coded strings in the script.
3. Add 'waits on decision' flags to slides/outline_20oct.md (not a new talk_20oct.md) without rewriting the script:
   - slide 7: the T set, the H1 comparison point, the H2 positions clause and mechanism;
   - slide 8: Infrared City vs Ladybug in the loop;
   - slide 9 and the Q&A: volume only vs a peak proxy, and the H3 'as predicts' wording.
   Keep the total at 5:00 or less, and ask the user whether a plan-to-18-Dec slide is wanted.
4. Write notes/tutor_questions_20oct.md: one page, at most 12 rows, columns #, question, context (file §), fallback default, affects, answer (blank).
   - Merge the todo_manual email list and the agent_backlog tutor list. Order: PS/RQ/H first, then data access, then tools and logistics.
   - (i) Volume vs a peak-block proxy. The fallback is the outline's 'Why not peak flow' answer; give the cost against methodology §10.
   - (ii) Infrared City: reference §6.4 / todo (a)-(c) without repeating them; add public facts from WebSearch (URL, access date, read level); check the SDK name on pypi.org; add the fallback rule with a blank date.
   - (iii) RESCCUE maps, transfer phase in or out of scope, the Grasshopper requirement, the 18 Dec date.
Done when: infographics_plan.md and the 5 fig_*.csv files exist; outline_20oct.md carries decision flags; tutor_questions_20oct.md has the table, the Infrared City facts with URLs and read levels, the blank-date fallback rule and a blank answer column.

### Parts of the issue body that now conflict with main
- The issue says there is 'no figure plan, no talk outline and no slides/ folder'. slides/ now exists, with outline_20oct.md and fig/01-06.
- The issue asks for slides/talk_20oct.md with 6-8 slides in the order problem, why, RQ, H, method, literature, plan to 18 Dec. The user's outline has 9 slides: title, problem, why Porta, literature runoff, literature heat, gap, RQ/H, method, first runoff result. It has no plan-to-18-Dec slide.
- Figure differences from the brief: (b) and (c) are merged into 02; (d) was built as final instead of 'pending' a prior_art_matrix; (e) uses porta_trait_table.csv, not porta_species × species_coverage; abstract-only rows are marked '*' instead of '(abs)'.
- 02 left breaks the 'no axis mixes measure types' rule, with only a caveat note.
- Tutor question (i): the outline already answers 'volume only' (Selbig 2021), but PS v4 still frames the hazard as more than 60 mm/h in 20 min with sewer capacity, and v1 also runs a T2-20 storm.
- Infrared City (a)-(c) are already repeated in todo_manual.md.
- The matrix has 56 rows, but fig 01 and slide 4 say '55 papers'.
- Step 1 ('run last, 16-17 Oct') is overtaken: the user drafted the talk on 8 Oct.

## #11: Extract PDISBA design storms and intense-storm seasonality

**Status: partly done on main.**

### Already on main
Commit 83040d3 extracted the PDISBA city IDF and now uses one storm set consistently. None of the issue's own files exist: design_storms.csv, design_hyetographs.csv, storm_seasonality.csv and design_storm_set.md are all missing.
- Done-when 1, partial: databases/barcelona/pdisba_idf_city.csv.
  - Covers d = 10/20/30/60/120 min × T = 1/2/5/10 yr, as max, min, mean, normal-95 and design intensity in mm/h, without climate change. Depth = intensity × d.
  - design_intensity equals min(max, normal95) in every row (checked).
  - Source: data_inventory_barcelona.md §I, 'Estudi de pluges' section 2.6, read in the browser. It cites the section, not page numbers.
  - Missing: climate-change variants, per-gauge Gumbel tables, hyetographs, the gauge nearest Porta.
- Storm set in use:
  - methodology §4b line 44: T1-60 = 19.6, T2-60 = 31.9, T10-60 = 62.5, T2-20 = 21.2 mm;
  - runoff_model.py line 29: STORMS = [(1,60), (2,60), (10,60), (2,20)], with P = design intensity × d (line 130);
  - results in runoff_scenarios.csv and runoff_sensitivity_storage.csv.
- T set now consistent at 1/2/10 in: the topic_decision §7 v4 RQ (line 123), methodology §4 line 36, §4b line 44, §6 line 62 (f2 at T = 2), and outline slide 7.
- Gauge data (step 4) is a user action: todo_manual.md line 40 (BCASA request, XEMA key). B3 is unchanged.
- Not done: seasonality, the Casas cross-check, the options memo, the B2 update.

### Revised scope (do this)
Revised task. Keep needs-user: the Doc2 hyetographs, climate-change variants and per-gauge tables still need a local or browser session, or Doc2 saved to a tracked folder.
1. Create databases/barcelona/design_storms.csv in the issue schema, seeded from pdisba_idf_city.csv: depth_mm = design intensity × d; peak_intensity_mm_h; climate_change = N; gauge = 'city empirical summary'; source = PDISBA Doc2 §2.6; page = the actual page.
   - Do not re-extract the city values.
   - Add climate-change design storms and per-gauge Gumbel rows, and name the gauge nearest Porta (Nou Barris).
2. Extract the PDISBA design hyetographs into design_hyetographs.csv (shape, duration, time step).
3. Cross-check the city IDF against the Casas UB thesis (generalised Fabra IDF).
4. Write storm_seasonality.csv (month, threshold, n_events, series, years, source), or a gap note listing every source tried (PDISBA, Casas, Barcelona Regional 2017 ch. III, XEMA without a key, Fabra series). Mirror the todo_manual XEMA and BCASA actions into B3.
5. Write notes/decisions/design_storm_set.md starting from the set in use: T = 1/2/10, d = 60 min plus T2-20, depth only, no climate uplift, leaf-on LiDAR LAI.
   - Compare it with a PDISBA design hyetograph, a climate-change uplift and a 20 min main duration.
   - Propose one set marked 'pending user decision'.
   - Note what would change: runoff_scenarios.csv, methodology §4b, the slide 7 RQ and the slide 9 numbers.
   - List open sub-hourly multi-year series for replaying observed storms.
6. Update B2: ✅ with page refs and a pointer to §I / pdisba_idf_city.csv, or keep 🟡 with the reason. Update B3 if it changes.
Done when: design_storms.csv (city rows plus climate-change and gauge rows where available), design_hyetographs.csv (if PDISBA gives them), storm_seasonality.csv or a gap note, design_storm_set.md (pending) and the updated B2/B3 rows all exist.

### Parts of the issue body that now conflict with main
- The issue says 'no depth has been extracted'. City IDF values are now in pdisba_idf_city.csv and methodology §4b; only the B2 row (inventory line 23) is stale ('🟡 in reports').
- The issue says 'the T sets disagree'. On main, 1/2/10 with f2 at T = 2 is consistent across the v4 RQ, methodology §4/§4b/§6, runoff_model.py and slide 7. 2/5/10 survives only in the superseded Florence v2/v3 text (topic_decision lines 15, 47, 98). The memo should confirm or challenge this set, not choose one from scratch.
- The issue says the 1 h duration has no Barcelona basis. 60 min is still the main duration, but v1 also runs T2-20 (21.2 mm).
- The issue says 'no hyetograph is chosen'. v1 needs none: it is depth-only (bucket plus SCS-CN on event totals, runoff_model.py lines 99-104, 130). A PDISBA hyetograph would change the published runoff_scenarios.csv and slide 9 numbers only if its total depth for the chosen duration differs from design intensity × d, or once a peak-block metric or an intensity-dependent (Gash) term is added. The earlier claim that v1 uses a 'uniform block' overstates this.
- Step 0 frames PDISBA access as allowlist, download or local run only. The user already read Doc2 §2.6 in a browser (inventory §I).
- Leaf state: v1 implicitly uses a leaf-on storm (LiDAR flown Sept 2021). The interim 'leaf-on main run plus leaf-off sensitivity run' (agent_backlog line 33) is not implemented.
- Step 4 wants the XEMA key added to B3. It is in todo_manual.md instead, and B3 is unchanged.

## #12: Pick the shared design sub-area and the runoff spatial unit

**Status: still open.**

### Already on main
—

### Revised scope (do this)
None of the three Done-when items exists on main. There is no scripts/porta_segments.py, no databases/barcelona/porta_segments.csv, no notes/figures/porta_subarea_candidates.png and no notes/decisions/ folder. Row A5 in databases/data_inventory_barcelona.md (line 14) is unchanged and still 🟡.

What the work can build on:
- notes/methodology.md §4b (lines 42-48) and scripts/runoff_model.py already compute runoff as total event volume on a 1 m grid over all of Porta. This is option A in practice. Line 48 states openly that there is no routing (volume only).
- Surfaces are already classed in runoff_model.py (lines 64-76): roofs from OSM footprints in exchange/to_gh/porta_buildings.geojson (29%), pervious ground from NDVI 2017 ≥0.3 with CHM <2 m, or OSM green (19%), and sealed ground for the rest (52%). Storage of crowns over roofs is set to 0 (line 93).
- LiDAR crowns (crown_diam_m) and street names are in exchange/to_gh/porta_trees_lidar.csv.

Revised task:
1. Write scripts/porta_segments.py with a usage docstring. Build runs of about 100 m per street from exchange/to_gh/porta_trees_lidar.csv using the street, is_plane, x and y columns. Output segment_id, street, n_planes, n_trees, length_m, bearing_deg and nn_spacing_m. Sample flood_share (index ≥40) and lst_anom_C locally from raw/flood_hazard_present.geojson and raw/lst_summer_anomaly.tif; in the cloud, mark both 'to compute locally'.
2. Make a hazard table at the 832 plane positions: the distribution, the share at index ≥40, and Av. Meridiana against the interior streets.
3. Compute the shares of crown area over roof, sealed and pervious ground, using the LiDAR crowns and the surface masks runoff_model.py already builds. The road vs sidewalk split needs A6 (mapa-base-de-vialitat) or A5. Record in A5 which layer opened, and note that runoff v1 classes surfaces from OSM, NDVI and CHM, not from A5.
4. Rank 2-3 candidate sub-areas of 2-4 contiguous runs, comparing the Meridiana edge with the north-east interior. Estimate the number of UTCI points on a 2 m grid, with the sidewalk width stated as an assumption.
5. Write up runoff options A, B and C. A is the current v1, and its results show that species differ only through crown size and LAI. B weights volume by the hazard index under each cell, which is a cheap change to v1. C follows flow paths on the local 0.5 m DTM; describe it only. For each option give the data needed, the cost against §10, what validation (iii) in §4 (line 40) becomes, and the consequence for H2.
6. Write up domain options (a), (b) and (c). Reconcile methodology §1 (heat on a sub-area only) with §6 (line 65: all 832 positions need a proxy) and with slide 8 (all 832 positions as decision variables). Give a recommended default marked 'pending user decision', plus one question.

Done when:
- the script, the CSV and the figure exist;
- notes/decisions/design_subarea.md has the hazard table, the crown-over-surface shares, the ranked candidates, runoff options A/B/C (with A noted as the current v1), the domain options, the default and one question;
- A5 is updated.

### Parts of the issue body that now conflict with main
- **Undefined runoff unit (the issue's "Why").** Main now defines the unit. Methodology §4b (lines 42-48) and scripts/runoff_model.py use a 1 m grid over all of Porta, with defined roof, sealed and pervious surfaces (CN 98/98/74) and total volume. That is option A in practice. Methodology §4 line 35 still says 'per street segment', so it contradicts §4b.
- **Step 3 is out of date.** It asks for a crown-radius bracket per size class, but LiDAR crowns now exist (already noted in the issue's Update 8 Oct). The crown-over-roof case is also already decided: storage over roofs is set to 0 in runoff_model.py line 93.
- **Option C's DTM exists.** It is already local (databases/barcelona/raw/lidar/porta_dtm_05m.tif).
- **The domain inconsistency the issue describes is still there, and has grown.** Methodology §1 (line 12) still keeps heat on a 2-4 segment sub-area. But §6 (line 65) says 'Porta's 832 plane positions need a pre-computed shade × τ proxy', which leans towards option (c). The 20 Oct talk script (slides/outline_20oct.md slide 8, line 52) tells the tutor that NSGA-II chooses species at all 832 positions. The runoff v1 scenarios in runoff_scenarios.csv also replace every plane in Porta. The memo must reconcile this before the talk.
- **Validation (iii) is unchanged.** It is still 'plausibility vs the flood-hazard index' (methodology line 40).

## #13: Tree size: size_category meaning, sizes at planting/maturity, horizon

**Status: still open.**

### Already on main
None of the three Done-when items still in scope after the issue's own Update 8 Oct note is met: A1, species_size_classes.csv and evaluation_horizon.md.
- The A3 and method_lidar_trees items were satisfied by main commit ca18c02 and dropped by that update. The two new commits do not change this. Note that the A3 table row itself (inventory line 12) still says '2021–23': the leaf-on facts are only in §G (line 72), the bcn_lidar_porta.py docstring and exchange/README.md line 24, and §G gives no Porta point density.
- A1 (inventory line 10) still reads 'exact meaning to confirm'.
- The new commit 83040d3 adds no sourced sizes. It adds an unsourced two-state framing (YOUNG_CROWN_M = 3.0, ASSUMPTION, runoff_model.py line 32, vs the on-site LiDAR median) and its results (runoff_scenarios.csv R_*_young/mature). These are inputs for the horizon memo, not deliverables.
- Existing inputs for the cross-tabs:
  - size_category and planting_date: exchange/to_gh/porta_street_trees.csv;
  - size_category with height_m and crown_diam_m: exchange/to_gh/porta_trees_lidar.csv;
  - species medians: porta_species_lidar_summary.csv;
  - BROT maximum height for Celtis australis (20 m) and Fraxinus angustifolia (25 m) only: porta_trait_table.csv.

### Revised scope (do this)
1. A1. Verify the size_category definition from the arbrat-viari metadata, BCNROC report 11703/88725 (trunk girth ≤40, 40-80, >80 cm; still 🟡) and the 2011 management report. Define EXEMPLAR. Mark it verified, or 'to check locally' with the URL. Optionally point the A3 row (line 12) and methodology §2 (line 20) to §G for the flight date.
2. Cross-tabs (no raw data needed):
   - size_category × planting year × species, from porta_street_trees.csv;
   - size_category against LiDAR height_m and crown_diam_m, from porta_trees_lidar.csv (flag == ok), with the §G segmentation caveat;
   - the city-wide table only if arbrat_viari.csv is local.
3. notes/lit/species_size_classes.csv: for the 8 palette species, height and crown diameter at planting and at maturity, with unit, source and read_level, or 'no value found'. Add a column with the on-site LiDAR median. Check, or replace, the v1 assumptions:
   - YOUNG_CROWN_M = 3.0 m;
   - 'mature' = the on-site median of all size classes pooled.
4. notes/decisions/evaluation_horizon.md:
   - the cross-tabs and the growth-source table;
   - the horizon options (at planting, +10 yr, +20 yr, maturity, trajectory), with consequences for H1's 'same number and size class' (topic_decision line 126), for comparability with S0 and for data needs;
   - a record that v1 already runs young vs on-site median, with its result: about +0.7%, about 37% of the benefit lost (methodology §4b line 47; slide 9);
   - a recommended default and one question.
Done when: A1 is updated, species_size_classes.csv exists, and evaluation_horizon.md exists with this content.

### Parts of the issue body that now conflict with main
- The issue's Goal and Why still ask when the LiDAR was flown, and cite A3 '2021-23'. §G answers it (26 Sept 2021, leaf-on), but the A3 row (line 12) and methodology §2 (line 20) still say '2021–23', so main is inconsistent with itself.
- Commit 83040d3 already fixed unsourced sizes for new trees:
  - young crown = 3.0 m (ASSUMPTION), keeping the species' on-site median LAI;
  - 'mature' = the on-site median crown, which pools all size classes. For example, Celtis australis rows in porta_trees_lidar.csv are 38 PRIMERA / 154 SEGONA / 82 TERCERA / 22 EXEMPLAR (all flags), so this is the current stock, not a mature size;
  - for Pyrus, young 3.0 m ≈ 'mature' 3.09 m.
  The '+0.7% / ≈37% of benefit lost' result in methodology §4b and slide 9 rests on these values, so the sourced sizes from this issue must check or replace them.
- methodology §3 line 29 still says new trees come 'from species size classes at planting and at maturity', with no source.
- methodology §7 line 75 still lists young vs mature as optional, although §4b has already run it for every candidate species.

## #14: Verify runoff validation datasets and decide the tree-pit term

**Status: partly done on main.**

### Already on main
No Done-when item is fully met. Step 1 is done in substance for one dataset, which gives partial coverage of Done-when items 1 and 2.
(a) The Anys & Weiler 2024 dataset is verified and downloaded.
   - data_inventory_barcelona.md §I line 85: FreiDok plus 242951, CC BY-NC 4.0, stored in databases/traits/raw/anys_weiler_2024/ (gitignored by 'databases/*/raw/').
   - The scripts/calibrate_interception.py docstring documents 16 urban Acer platanoides / Tilia cordata trees, Freiburg, Apr–Sep 2021, 10-min data: THF_ref open gauge plus per-tree throughfall and stemflow in DATA_TF_SF_10min.csv, and LAI/PAI per tree in TREES.csv.
   - The per-tree fit (n_events, RMSE 0.89–3.24 mm, bias) is in databases/traits/interception_calibration.csv; the summary is in methodology §4b.
(b) A partial list of unvalidated components exists in methodology §4b Known limits: the LiDAR LAI proxy, the same s for every species, no routing, no tree pits.
(c) A Selbig plausibility comparison is already used (methodology §4b: 1.85% 'same order as the measured 4%'), with no verified data release and no acceptance rule.
Not present:
- databases/validation_inventory.md;
- a 'Validation' row in the inventory (§I only says 'used for calibration');
- Selbig/Coville data-release checks; a Mediterranean throughfall search;
- notes/lit/tree_pit_infiltration.csv, notes/decisions/tree_pit_term.md, and a B4 update.

### Revised scope (do this)
Revised task (needs-user for paywalled papers and blocked domains):
1. Create databases/validation_inventory.md.
   - Row 1 is Anys & Weiler 2024, built from §I, calibrate_interception.py and interception_calibration.csv: verified Y; temperate climate; licence CC BY-NC 4.0 (non-commercial); serves calibration of s.
   - The full dataset already fitted s, so define a hold-out protocol (leave-one-tree-out, or split events by date) with event RMSE/bias and an acceptance rule fixed before any validation claim.
   - Add Selbig 2021 and Coville 2022 after searching USGS ScienceBase (Coville OA full text).
   - Add any Mediterranean or urban throughfall dataset (Zenodo/PANGAEA; Platanus, Celtis, Melia, Quercus ilex first), or write 'none found'.
   - Fill every column, and state the comparison mode per row: seasonal totals (6,376 L/tree; 64-66 L/m²) are not comparable with event volumes.
2. Unvalidated components: replacement-species s, the LiDAR LAI proxy, CN 74/98, background LAI 2.3, the young 3 m crown (runoff_model.py ASSUMPTION lines), the pit term.
3. Add a 'Validation' row to data_inventory_barcelona.md, or turn the §I line into one, plus rows for any other verified datasets.
4. Create notes/lit/tree_pit_infiltration.csv (value, unit, context, source, DOI, read_level) with absolute rates in mm/h. Zhang 2019 is MDPI OA; Bartens 2008 and Grey 2018 are paywalled.
5. Write notes/decisions/tree_pit_term.md: keep or drop, the low-high range and the run-on assumption, marked 'pending user decision'. Note that v1 has no pit term.
6. Update B4 with the Barcelona escocell specification and source, or '❌ not found'.
Done when: all five original Done-when items exist, and the Freiburg row states how calibration and validation are kept apart.

### Parts of the issue body that now conflict with main
1) The issue says the Freiburg data are unverified and that no FreiDok record was found. Main found it (FreiDok plus 242951, CC BY-NC 4.0), downloaded it, and stores it in databases/traits/raw/anys_weiler_2024/ rather than databases/validation/raw/.
2) The issue treats Freiburg as validation step (i) with 'no modelling'. Main used the whole dataset to calibrate s = 1.75 (calibrate_interception.py; methodology §4b), so it cannot serve as independent validation without a hold-out. methodology §4 'Validation (i)' (line 40) and §4b now disagree.
3) Main already reports the Selbig 4% comparison as plausibility (methodology §4b; outline slide 9), while Selbig is still abstract-only (matrix #10) and has no protocol.
4) methodology §4 step 3 (line 38) still lists the tree-pit term, but v1 omits it (§4b: 'tree pits are not yet modelled separately'). In practice main runs without it, while the issue asks for that decision to be made.
5) The licence is CC BY-NC 4.0, so the licence column must carry the non-commercial restriction. literature_matrix #1 still says only 'data open on FreiDok', with no record ID.

## #15: Options memo: f1 proxy, optimiser choice and sensitivity plan

**Status: still open.**

### Already on main
None of the Done-when items exists: there is no notes/decisions/ directory, so no optimisation_and_sensitivity.md. Inputs the memo can reuse: (a) run-time evidence for the f1 options and run budget in notes/methodology.md §6 'Why proxies are needed' (Shaamala 2025: Ladybug 20-25 min per layout for 42 trees; Peng 2026: 10-20 s per evaluation, 2-3 h for 200 evaluations; 832 positions need a proxy, surrogate or Infrared City). (b) Comparable-study rows now read in full: notes/lit/literature_matrix.csv #52 Shaamala (ACO/Opossum, 42 trees x 4 species), #53 Peng (NSGA-II in Wallacei, 20 x 10 = 200 evaluations, LAI transmittance), #56 Wu 2024, #51 Mannucci. #24 Liu (SWMM + NSGA-II, 520 variables) and #25 Nyelele are still abstract only. (c) A one-at-a-time sweep of one sensitivity parameter: databases/barcelona/runoff_sensitivity_storage.csv (s = 0.86/1.75/2.2 x 4 storms), with range sources in methodology §4b (0.86 = Xiao & McPherson 2016 lower bound) and in the runoff_model.py comment (calibration IQR 1.45-1.92). (d) Parameter values or ranges: databases/traits/porta_trait_table.csv and databases/barcelona/porta_species_lidar_summary.csv (lai_proxy_iqr); k = 0.5 fixed in methodology §3; ASSUMPTION parameters in scripts/runoff_model.py and databases/barcelona/runoff_params.json.

### Revised scope (do this)
Revised task: write notes/decisions/optimisation_and_sensitivity.md with:
1. A comparable-studies table (objectives, decision domain, algorithm, proxy validation) built from matrix #24, #25, #46, #51, #52, #53, #56, with (abs) marks for #24 and #25. Tan 2026 and Hao 2023 stay 'to get'.
2. f1 option table. Tier 1 in the loop is already costed in methodology §6 and is impractical for about 830 positions, so compare: precomputed shade x tau proxy, ML surrogate, Infrared City API, Tier 1 on a reduced sub-area. Give each a calibration sample size and an R2/RMSE-vs-Tier-1 acceptance metric, with the threshold left to the user. The metric and the domain stay placeholders until heat_objective.md and design_subarea.md exist.
3. Algorithm table: NSGA-II, epsilon-constraint integer programme, greedy. Validity conditions to state: (a) f2 in runoff_model.py is additive per position only where crowns do not overlap, because storage_raster takes the max on overlap and zeroes crowns over roofs; (b) the heat proxy must be additive; (c) the Shannon floor must be linearised. Note that with one s for all species, S3 reduces to ranking species by crown area x LiDAR LAI up to the 15% cap; runoff_scenarios.csv already gives that ranking. Use the decision-variable count from replacement_scenario.md, or note the 832 vs 809 discrepancy.
4. Sensitivity plan: a parameter list with range sources (s 0.86-2.2 done; LAI proxy IQR from the LiDAR summary; crown size at the horizon pending #13; CN 74/98; background LAI 2.3; young crown 3 m; pit infiltration pending #14; EPW +1/+2 °C), OAT vs Morris (method source or '(to add)'), run budget in model evaluations for each method, and robustness outputs (species-ranking stability, Pareto shift vs S1).
5. Recommended defaults and one user question.
Done when: the original Done-when list is met, and it reuses the existing s sweep and run-time evidence instead of re-deriving them.

### Parts of the issue body that now conflict with main
1) slides/outline_20oct.md slide 8 ('An NSGA-II search chooses the species at each of the 832 plane positions') and the method-pipeline infographic (scripts/make_infographics.py about line 316: 'NSGA-II', 'Decision: species at each of the 832 plane positions') present NSGA-II as the chosen method. This memo would re-decide it. Methodology status is still NOT DEFINED, so the memo is not blocked, but its recommendation must be reconciled with the talk draft. 2) The issue's 'Why' says f1 has no cost evidence. Main has since added it (methodology §6 'Why proxies are needed'), which in practice rules out 'Tier 1 directly' at Porta scale. 3) The issue frames the §3 sensitivity plan as naming no parameters. Main now has an executed OAT sweep for s with a defined range (runoff_sensitivity_storage.csv; §4b), so the s row should cite it rather than say 'pending'. 4) Parameter naming has changed: the issue lists 'S' and 'k', while main uses S = s x LAI with calibrated s = 1.75 mm/LAI, an optional species factor s_sp = s x (C_sp/0.86) (methodology §3), and k fixed at 0.5. Pit infiltration is not in the v1 model. 5) The decision-variable count is inconsistent: 832 planes in the inventory (notes/site_selection.md, topic_decision §7, slides), but only 809 have LiDAR crowns (flag == ok in exchange/to_gh/porta_trees_lidar.csv), and runoff_model.py replaces only those. porta_trait_table.csv lists 829 Platanus x acerifolia, and porta_species_lidar_summary.csv lists 807 + 2. 6) Context files named in the issue (heat_objective.md, design_subarea.md, replacement_scenario.md, interception_params.csv, species_canopy_params.csv) still do not exist on main, so placeholders are still needed.
