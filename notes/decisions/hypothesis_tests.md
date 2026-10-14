# Options memo: make H1-H3 falsifiable (issue #3, 8 Oct 2026)

Status: **options only, pending user decision.** Methodology status in CLAUDE.md is still NOT DEFINED; no tool code was written.
Scope follows `notes/agent_backlog_status.md` §#3 (it overrides the issue body). The 'Decisions' bullets in `notes/agent_backlog.md` lines 26-34 are cited here, not copied; each section updates them with evidence now on main.
Marks: 🟡 unverified; (abs) abstract only; (to add) no source in the repo yet. Matrix = `notes/lit/literature_matrix.csv` (row = id).
Current wording being tested: `notes/topic_decision.md` §7 (v4) and `slides/outline_20oct.md` slide 7.

## 0. Inputs and one correction

**Check of the H3 claim (done myself, `databases/barcelona/runoff_scenarios.csv`).** `interception_m3` is identical at all four storms for every scenario: S_none_street 412.22; S0_current 817.51; R_Celtis_mature 681.00; R_Jacaranda_mature 785.18; and so on (T1-60, T2-60, T10-60, T2-20 all equal within each scenario). Confirmed: every crown is saturated at every design storm (consistent with per-tree S 4.27-10.86 mm in `databases/traits/interception_calibration.csv` against P = 19.6-62.5 mm).
Refinement of the backlog wording ('avoided runoff nearly constant'): the *interception* is constant, but *avoided runoff* (S_none_street minus S0, my arithmetic from the CSV) is not: 303.7 / 333.2 / 365.2 m³ at T1 / T2 / T10 (60 min) and 308.2 m³ at T2-20. It rises about 20% from T1 to T10 through the SCS-CN slope, while the percentage falls (3.16 / 1.85 / 0.90 %) because total runoff grows (9,600 to 40,541 m³). So the "shrinking % benefit" is the ratio of a near-flat numerator to a growing denominator.

**Conflict to reconcile (user).** `notes/methodology.md` §4b ('The benefit shrinks with return period, supporting H3') and `slides/outline_20oct.md` slide 9 ('as H3 predicts') present the model output as evidence for H3. With I = min(P, S) and every tree saturated, that output is an arithmetic consequence of the model, not a test. Either reword both (see 3.3) or make H3 testable against field data (3.2).

**Storm set in use** (`databases/barcelona/pdisba_idf_city.csv`, depth = design intensity × d): T1-60 19.6 mm, T2-60 31.9, T10-60 62.5, T2-20 21.2; T5-60 would be 48.86. No hyetograph, no month per storm (#11).

**Scale of effects available now (my arithmetic from the CSVs, T2-60, m³ of runoff vs S0):**

| Quantity | Value |
|---|---|
| Street-tree effect S_none_street - S0 | 333.2 m³ (1.85% of 17,982.79) |
| Same, s = 0.86 / 2.2 (`runoff_sensitivity_storage.csv`) | -0.91% / -2.33%, i.e. about 160 / 420 m³ (derived from rounded %) |
| Mature single-species replacement vs S0 | Jacaranda +29.6, Melia +39.4, Tipuana +48.2, Celtis and Brachychiton +106.2, Pyrus +122.1 |
| Young replacement vs S0 | +116.9 (Jacaranda) to +123.5 (Celtis) |
| Mature, T1 to T10 | Celtis +94.8 to +119.4 |

Existing R_* runs replace all 809 LiDAR-ok planes with one species. They break the 15% cap and are not S1 (backlog_status #9).

## 1. H1 (synergy: trait-based layouts beat like-for-like on both goals)

**Metric and unit.** f2 = event runoff volume, m³, whole Porta, at T2-60 (31.9 mm) as the headline; T1-60 and T10-60 reported. f1 = UTCI metrics of methodology §5: mean UTCI (°C) on sun-exposed sidewalk points at the design hour; share of points above 32 °C (Bröde 2012, (to add)). f1 weather and design hour are open (#7).
**Scenarios.** S4 (Pareto set) vs S1 (like-for-like in the city palette's proportions). S0 as reference. S1 has **not been run**.
**Comparison rule options.**
- (a) Knee point of S4 vs S1.
- (b) Best-f2 layout in S4 whose f1 is no worse than S1 (and the mirror).
- (c) Dominance of S1 by some S4 layout in at least a share p of trait-uncertainty runs (p fixed before the runs).
**Threshold rule options.**
- (i) Model error vs field data: event RMSE 0.9-3.2 mm, bias 0.08-1.19 mm (`interception_calibration.csv`; matrix row 1 is the data source). Converted to m³ by multiplying by the street-tree canopy (19.41 - 10.24 = 9.17 ha in `runoff_scenarios.csv`): bias 7-109 m³, RMSE 82-293 m³ (my arithmetic). RMSE is a per-event, per-tree scatter that partly averages out over about 2,600 trees; bias is the safer systematic term. 🟡 conversion is a rough scaling.
- (ii) The s spread: about 255 m³ between s = 0.86 and 2.2 in the street-tree effect (table above).
- (iii) 'Fixed before the runs' (the v2 rule in `topic_decision.md` §3 *Test*), from the larger of the model error and the gap-fill spread (backlog option b). Heat analogue: Mannucci 2025 Ladybug vs ENVI-met UTCI MBE 0.8-2.3 °C, CVRMSE 7-13% (matrix row 51, full text) or a UTCI stress-class crossing; Peng 2026 residual 2-4 °C MRT (row 53). Heat threshold lives in #7.
- Consequence of (i): mature palette differences of 30-50 m³ (Jacaranda, Melia, Tipuana) fall below even the lowest RMSE conversion; Celtis, Brachychiton and Pyrus (106-122 m³) sit at or above the upper bias conversion (109 m³, only Pyrus clearly) and below the RMSE range. A 'beats S1 on runoff' claim may therefore be inconclusive on runoff by its own threshold.

**Falsifiability check.**
- S1 lies inside the S4 search space, so S4 weakly dominates S1 by construction at point estimates. Rule (c) is the only comparison that can fail.
- v1 gives every species one s, so f2 differs between species only through crown area × LAI. Both f1 (τ = exp(-0.5·LAI), row 53) and f2 rise with crown area × LAI, so 'synergy' is partly built in. Exploratory check (porta_species_lidar_summary.csv medians, six palette species, my stand-in proxies: crown area × LAI for f2, crown area × (1 - τ) for f1): rank orders are identical except Jacaranda and Tipuana swap places (Melia > Jacaranda/Tipuana > Celtis > Brachychiton > Pyrus). Not f1 itself.
- A genuine failure mode: species with a high trait-based f2 but low or uncertain f1, or gap-filled values flipping the order.

**Supported / inconclusive / rejected rule for gap-filled species** (share p and sensitivity ranges fixed before the runs; p is (to fix), no source in matrix):
- Measured inputs: LiDAR crown and LAI proxy for all six palette species; storage measured only for *Pyrus calleryana* (row 3; Celtis via congener *C. sinensis*); cooling measured for none (PS v4). Everything else is gap-filled (methodology §3).
- **Supported**: S4 dominates S1 beyond the threshold on both objectives in at least p of the draws, *including* draws with gap-filled species at the low end of their class range.
- **Inconclusive**: dominance holds only at the favourable end of the ranges, or only on one objective, or the differences are below the threshold.
- **Rejected**: S1 is not dominated by any S4 layout in more than (1 - p) of draws, or S4 loses on one objective beyond the threshold.
- Report the share of the verdict that rests on gap-filled species (a stated result per methodology §11).

**Reformulations.**
- H1-R1: 'Layouts chosen with species traits, for the same number and size class of trees, reduce f2 by at least Δ m³ at T2-60 without raising the peak-hour UTCI metric above S1, in at least p of trait-uncertainty draws.'
- H1-R2 (weaker, honest about the data): 'The rank order of replacement layouts on f1 and f2 is the same under trait uncertainty' (synergy = rank agreement; falsified if ranks cross).
- H1-R3: 'Dominance of S1 by S4 holds on f2 only when the palette contains a species with a measured storage value'; frames the data gap as the result.

## 2. H2 (trade-off: heat and runoff optima differ mainly in species, not positions)

**Metric and unit.** Composition dissimilarity between S2 (heat-only optimum) and S3 (runoff-only optimum): e.g. Bray-Curtis or evergreen share difference over the six species at the 832 positions; plus a front-spread measure (see §4). No source in matrix for the dissimilarity index.
**Scenarios.** S2 vs S3 (and S4 front). None has been run.
**Comparison rule.** Fraction of positions where S2 and S3 choose different species vs different locations (see options).
**Threshold.** Fixed before the runs; no source in matrix.

**By-construction problems.**
1. Positions are fixed (832 existing plane pits; `topic_decision.md` §7, outline slide 8). 'Species, not positions' is then true by definition (backlog_status #3; `agent_backlog.md` line 28).
2. Leaf habit enters neither f1 (summer design hour) nor f2 (leaf-on LiDAR LAI, storms with no month). Transpiration is not in Tier 1 (methodology §5; Mannucci 2025, row 51, likely 2-3 °C UTCI underestimate). The stated mechanism in H2 therefore cannot act.
3. Possible front collapse: f1 and f2 both rise with crown area × LAI, so the two single-objective optima may pick the same species (the exploratory check in §1 shows near-identical ranks under proxies). If so, the front is one point, which falsifies the trade-off claim but through the model's own structure. Not yet testable with real f1. Run it as the first check once the f1 proxy exists (#15).

**Options.**
- (a) Restate H2 as a species-composition claim (S2 vs S3 differ in evergreen share or composition dissimilarity by more than a threshold). Recommended for positions.
- (b) Make positions decision variables on plantable sidewalk cells. Needs A6 sidewalk data (🟡 in the inventory) and raises the variable count; not recommended before the data are verified.
- (c) Drop the positions clause and keep 'the front is not a single point'.
- (d) Mechanism via a cold-season heat term (winter UTCI or sun access), with Peng 2026 (row 53: winter optimum LAI 0.6, summer 4.6; full text) as precedent. Only if Barcelona winter hours reach a cold-stress class (pending #7).
- (e) Mechanism via a wood-anatomy transpiration class (Bachofen 2025 row 43, full text: diffuse-porous 2-3× ring-porous; Rahman 2020 row 44 (abs); Park 2026 row 42, air temperature only; Rahman 2019 row 38 (abs): Mediterranean trees show lower transpiration cooling). Tier 1 cannot represent it (methodology §5), so this adds a correction term with its own uncertainty.
- Mechanism restricted to LAI, crown size and leaf-on timing, transpiration out of scope: the scope-down of (d)/(e); combine with the next item.
- **Month per storm** (links #4 phenology, #11 storm seasonality). Assigning each storm a month and a leaf state lets leaf habit enter f2: Xiao & McPherson 2016 (row 3): modelled crown storage falls from 85% to 16% of a 2-yr 5-min storm when leaf-off; Baptista 2018 (row 6): leaf-off cuts *Platanus* storage by 90%. Source for intense-storm timing: Resilience Atlas 'autumn' (methodology §1); monthly counts need PDISBA or BCASA/XEMA gauges (B3 🟡; #11). Leaf-out and leaf-fall months per species are not on main (#4).

**Reformulations.**
- H2-R1: 'S2 and S3 differ in species composition by more than a pre-fixed dissimilarity, and the Pareto front spans more than the pre-fixed threshold on each objective.'
- H2-R2: 'Within a fixed-position set, an evergreen replacement raises winter-storm interception and lowers summer UTCI benefit relative to a deciduous one' (needs month per storm and the leaf-off term).
- H2-R3: 'There is a measurable trade-off: the best f2 layout loses more than Δ on f1 vs the best f1 layout, and vice versa' (no species/position clause).

## 3. H3 (validity boundary: the runoff benefit shrinks as the return period grows, small at T = 10 yr)

**Metric and unit.** Street-tree effect on f2, % of runoff vs S_none_street (or vs S0), per T; also m³. Currently 3.16 / 1.85 / 0.90 % at T1 / T2 / T10 (60 min) and 2.89 % at T2-20 (`runoff_scenarios.csv`).
**Scenarios.** S_none_street, S0_current (exist); R_* for replacements.
**Comparison rule.** Monotone decrease of the % effect with T, and a magnitude cut-off for 'small'.

**3.1 Defining 'small'. Options (threshold fixed before the runs).**
- (i) Below the model's own error: effect < bias/RMSE conversion of 7-109 / 82-293 m³ (§1 (i)); at T10 the effect is 365 m³, so it would not be 'small' on this rule. 🟡
- (ii) Below the s-sensitivity band: at T10 the effect ranges 0.44-1.13% (`runoff_sensitivity_storage.csv`); no sourced criterion for 'small' here; fixed before the runs. Weak.
- (iii) Relative to the field benchmark: Selbig 2021 (row 10, abs) 4% of total runoff; Coville 2022 (row 11, abs) 64-66 L/m² canopy per season. 'Small' = under a fixed fraction of 4% (fraction (to fix)). Model at T2 gives 1.85%, so the order matches the benchmark only for frequent storms.
- Source for the T = 10 'small' cut-off: no source in matrix (PDISBA targets T ≤ 10 yr for flood risk, inventory B2 🟡).

**3.2 Test against Anys & Weiler (2024) field data (row 1; FreiDok, CC BY-NC 4.0, 16 trees, 2 species, Apr-Sep 2021, 51 events ≥ 1 mm).**
- The data already set s (pooled median 1.75), so a naive comparison is circular. Hold-out options: (a) leave-one-tree-out; (b) fit on *Tilia*, test on *Acer* (and the reverse), which also tests transfer across species; (c) fit on the first half of the season, test on the second.
- Prediction: interception fraction vs event depth. The bucket model predicts I/P = 1 for P ≤ S and S/P above; row 1 reports interception falls with rainfall depth and intensity (qualitative support). The test can fail if the observed fraction declines slower or faster than S/P, or if evaporation during long events lets I exceed S.
- Hard limit: the raw files are gitignored (`databases/traits/raw/anys_weiler_2024`), the matrix gives mean event depth 6.7 mm (row 1) but the maximum event depth is not in the repo. The design storms (19.6-62.5 mm) likely lie outside or at the edge of the observed range (🟡, to compute locally). The test would then support the saturation shape, not the T = 10 behaviour.
- Cost: about half a day once raw data are local; would live in `calibrate_interception.py` territory, which is tool code, so after the methodology is marked DEFINED. Not run here.

**3.3 State H3 as a declared model boundary.** I = min(P, S) with every tree saturated, so the effect shrinking with T is by construction. Honest wording: 'Within the model, the street-tree effect decreases from 3.2% (T1) to 0.9% (T10) of runoff, because interception is capped (S ≈ 4-11 mm per tree) while total runoff grows; this is a boundary of the method, supported in direction by Kuehler 2016 (row 9, abs) and Selbig 2021 (row 10, abs).' Plus: palette ranking is the same at every T (differences from the SCS-CN slope only: Celtis mature vs S0 +94.8 / +106.2 / +119.4 m³).

**Reformulations.**
- H3-R1 (declared boundary): as 3.3. Removes the 'significantly' and any evidence claim; slide 9 'as H3 predicts' becomes 'consistent with the stated boundary'.
- H3-R2 (testable): 'In field data, the fraction of rain intercepted by street trees falls with event depth in line with S/P for P above S, out-of-sample (hold-out tree or species)'; a field claim with a hold-out, not a model result.
- H3-R3 (magnitude): 'The street-tree effect at T = 10 is below X% of runoff, X fixed before the runs'; falsifiable, but X (sources above) needs a decision.

## 4. Trade-off metric options (RQ: 'how large is the trade-off?')

| Option | Definition | Source |
|---|---|---|
| % loss of one objective at the other's optimum | (f2 at S2 - f2 at S3) / f2 at S3, and mirror | no source in matrix |
| Hypervolume | volume dominated by the front relative to a reference point | no source in matrix (rows 24, 52, 53 use NSGA-II/ACO with fronts or single optima; whether they report hypervolume is 🟡 unchecked) |
| Knee-point distance | distance of the knee to the ideal point | no source in matrix |
| Rank correlation of species on f1 vs f2 | Spearman over species | no source in matrix |
**Recommended:** % loss at the other's optimum (reads directly in °C and m³, easy for the talk); report hypervolume as a secondary check only if a source is added.

## 5. Scenario conditions as used on main

| Condition | In use | Options |
|---|---|---|
| Storms | T1/T2/T10 at 60 min plus T2-20; T5 in the IDF (48.86 mm at 60 min); no hyetograph (#11) | keep; add hyetograph for a peak proxy if the tutor asks (outline Q&A 'Why not peak flow?', Selbig 2021, row 10 (abs)) |
| Horizon | young = 3 m crown (ASSUMPTION in `runoff_model.py`) vs LiDAR on-site median (mature); young loses 117-124 m³ vs S0 (about 35-37% of the street-tree effect lost; mature: Jacaranda 9%, Celtis/Brachychiton 32%, Pyrus 37%; my arithmetic from the CSV) | at planting / +10 yr / +20 yr / maturity (needs `size_category` meaning and growth sources, #13) |
| Leaf state | implicitly leaf-on (LiDAR 26 Sept 2021; calibration Apr-Sep) | leaf-on main + leaf-off sensitivity (row 3: leaf-off crown storage 16-26% vs 62-85%; row 6: -90% for *Platanus*); later month-weighted (#11) |

## 6. S0-S4 consequence table

| ID | Layout | Exists now | Supports | Result today (T2-60) | Note |
|---|---|---|---|---|---|
| none | No street trees | `S_none_street` | baseline for H3 | runoff 17,982.79 m³ | background canopy fixed (LAI 2.3, 10.24 ha) |
| S0 | Current trees | `S0_current` | reference for all | 17,649.57 m³ (-1.85% vs none) | |
| R_* | One species replaces all planes | 12 runs (6 species × mature/young) | sensitivity only | +29.6 to +122.1 m³ vs S0 (mature) | breaks 15% cap; not S1 |
| S1 | Planes replaced by the palette in proportions (note: existing R_* runs cover 809 LiDAR-ok planes, not the 832 pits) | **not run** | H1 baseline | n/a | needs palette and proportion decision (#9) |
| S2 | Heat-only optimum | not run | H2 | n/a | needs f1 proxy (#7, #15) |
| S3 | Runoff-only optimum | not run | H2 | n/a | f2 differences across species only via crown area × LAI in v1 |
| S4 | Pareto set | not run | H1, H2 | n/a | S1 in S4 space by construction |
| (opt.) | Young vs mature | R_*_young/mature | transition loss | about +117-124 m³ (young) | horizon open (#13) |

## 7. Recommended defaults

- H1: comparison (c) (only one that can fail), threshold (iii) = larger of model error and gap-fill spread, fixed before the runs, with the three-state rule above. Reformulation H1-R1; keep H1-R2 as fallback if runoff differences stay below the threshold.
- H2: (a) for positions; mechanism restricted to LAI, crown size and leaf-on timing plus **month per storm**; (d) only if winter heat stress is material. Reformulation H2-R1. Run the front-collapse check first.
- H3: declared boundary (3.3, H3-R1) now; upgrade to H3-R2 only if the Freiburg raw data reach local disk and the event-depth range covers at least the lowest storm (to compute locally). Fix 'small' by 3.1 (iii) or leave it as a reported number.
- Trade-off metric: % loss at the other's optimum. Horizon: leaf-on main, young vs mature as the optional scenario. Storm set unchanged.

## 8. Draft wording (changes PS/RQ/H: user decides)

Only the hypotheses are reworded; the problem statement and RQ stay as in §7 v4 apart from one clause.
- **RQ** (optional): keep §7 v4, replacing 'how large is the trade-off' by 'how large is the trade-off, measured as the % loss of one objective at the other's optimum'.
- **H1:** 'For the same number and size class of trees, trait-based layouts reduce event runoff at T2-60 by more than Δ m³ and do not raise the peak-hour UTCI metric, relative to the like-for-like palette, in at least p of the trait-uncertainty runs. Δ and p are fixed before the runs; gap-filled species are reported separately.'
- **H2:** 'At the fixed plane-tree positions, the heat-optimal and runoff-optimal layouts differ in species composition by more than a pre-fixed dissimilarity (driven by crown size, LAI and leaf-on timing), so the Pareto front is not a single point.'
- **H3:** 'Within the model, the runoff benefit of street trees falls from about 3% at T1 to about 1% at T10 of runoff because canopy storage saturates; this is stated as a boundary of the method, not as a test result. [Optional H3-R2: and in field data the intercepted fraction declines with event depth in line with S/P, out-of-sample.]'

**Files this would touch (not edited here):** `notes/topic_decision.md` §7 (Hypotheses, and §3 *Test* if the threshold rule is restored); `notes/methodology.md` §4b (line 47 'supporting H3'), §7 (tests line), §6 (objectives, if the metric is stated) and the S1 definition; `slides/outline_20oct.md` slide 7 (H1-H3 text and script) and slide 9 ('as H3 predicts'); `notes/agent_backlog.md` lines 26-34 (decisions list).

## 9. Questions

**User (one):** Do you want H3 stated as a declared model boundary (and slide 9 / methodology §4b reworded accordingly before 20 Oct), or kept as a testable claim against the Freiburg field data, accepting that the test needs the raw data locally and may only cover small events?

**Tutor (one, for 20 Oct):** Is a hypothesis that is true by construction of the model (H3) acceptable if it is declared as a method boundary, or must every hypothesis be tested against independent data?

## Remaining gaps
- No S1, S2, S3, S4 runs; no real f1 (no heat module, #7/#15); no species-specific s.
- Maximum event depth of the Freiburg data not known in the repo (🟡); hold-out test not run.
- Threshold values Δ, p and the 'small' cut-off are open; Bröde 2012 and hypervolume sources are (to add).
- Months, leaf-out dates and storm seasonality: #4, #11 (B3 gauge data pending).
