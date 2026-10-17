# Options memo: f1 proxy, optimiser choice and sensitivity plan (issue #15)

Status: **options for the user; nothing adopted.** Methodology status is PROTOTYPING; `methodology.md`, `topic_decision.md`, `slides/outline_20oct.md` and `scripts/make_infographics.py` are not edited. No optimiser code was written. Marks: 🟡 = not verified; (abs) = abstract only. Order check (problem, why, RQ, H, methodology): none of the options below changes the PS/RQ/H. Option "ML surrogate" and "Infrared City" change only the tool inside the methodology (§6).

Placeholders: `heat_objective.md` exists on main (issue #7) but is itself "pending user decision", so the f1 metric (afternoon-window mean UTCI, hours 12-17, DDY cooling day) is a placeholder here. `design_subarea.md` and `replacement_scenario.md` (which defines S1) do not exist on main; S1 below means "like-for-like palette replacement" as written in `methodology.md` §7.

## 1. Question
How should f1 (heat) be computed for about 830 candidate positions inside an optimiser, which optimiser should search the species-per-position layouts, and how should parameter uncertainty be propagated, given the 18 Dec plan?

## 2. Comparable studies (matrix ids; read level from `notes/lit/literature_matrix.csv`)
Read-level note: the issue text says #24 and #25 are abstract-only and Tan 2026 / Hao 2023 are "to get". The matrix now lists all four as full text (#24, #25 on 8 and 12 Oct; #80 and #62 on 9 Oct), and `to_get_manually.md` ticks them. I use the matrix and flag the mismatch; if the user prefers the issue's wording, mark #24, #25 (abs) and Tan/Hao "to get".

| # | Study | Objectives | Decision domain | Algorithm | Proxy / validation |
|---|---|---|---|---|---|
| 24 | Liu et al. 2026 | Runoff reduction, pollutant removal, cost | 520 continuous areas (green roofs, bioretention, permeable pavement), 571 subcatchments; no trees | pymoo NSGA-II, pop 200 x 120 gen, 50 processes; K-means + entropy TOPSIS | SWMM calibration NSE 0.88, validation 0.86 / 0.72 |
| 25 | Nyelele & Kroll 2021 | PM2.5, avoided runoff, heat-index reduction, canopy, equity (14 scenarios) | m2 of new canopy on pervious / impervious land in 1,132 block groups (2,264 variables); species not a variable | Linear programme (lpSolve); constraint method for a Pareto front | Linear benefit per m2 from i-Tree; no outcome validation |
| 46 | Lachapelle et al. 2023 | Tmrt | Sidewalk tree spacing, idealised streets | No optimiser (parametric TUF-Pedestrian runs) | Not reported in the matrix row |
| 51 | Mannucci et al. 2025 | UTCI, runoff (scenario testing) | Scenarios, no species traits | None | Ladybug vs ENVI-met UTCI MBE 0.8-2.3 C, CVRMSE 7-13% (4 points) |
| 52 | Shaamala et al. 2025 | Mean UTCI (single objective) | 42 trees x 4 species | Ant colony (Opossum) | Ladybug in the loop, 20-25 min per layout; ENVI-met check of optimal vs suboptimal |
| 53 | Peng et al. 2026 | UTCI (summer, winter), cost | Generic tree types on a 25 x 36 m site | NSGA-II (Wallacei), 20 x 10 = 200 evaluations | Ladybug with tau = exp(-0.5 LAI); MRT within 2-4 C of measurement; 10-20 s per evaluation |
| 56 | Wu et al. 2024 | Runoff, peak runoff, land surface temperature | 7 greening patterns on 143 parcels | None (scenario scaling of LAI) | Canopy energy balance + SWMM; NDVI-derived LAI, no field validation stated in the row |
| 80 | Tan & Liu 2026 (not in the issue list; closest precedent) | Site-mean UTCI, CO2, diversity | 30 trees, 4 species, 108 locations | Random Forest surrogate (1,500 radiation + CFD runs) + NSGA-II 60 x 50 | Surrogate RMSE 0.09 C, Kendall tau 0.84; Pareto solutions re-simulated |
| 62 | Hao et al. 2023 | Park-mean UTCI | 55 trees on 17 x 17 zones | Genetic algorithm | Air T r 0.98, RMSE 0.98 C; ~730 layouts, 7 h per run; gain 0.1-0.3 C |

Gap visible in the table (supports the contribution, no change to the RQ): none of the tree rows jointly optimises runoff and UTCI with species as the variable at street-network scale; the runoff optimisers (#24, #25) do not use tree species.

## 3. f1 options
Common acceptance test (threshold left to the user): on N held-out layouts, f1_proxy vs f1_Tier1 gives R2, RMSE (C) and Kendall tau of the layout ranking. Candidate reference points, not decisions: RMSE below the minimum meaningful f1 difference (0.8 C, the Ladybug-vs-ENVI-met MBE low end, `heat_objective.md` §4), and a tau floor (Tan & Liu report 0.84). Domain and metric stay placeholders until `design_subarea.md` and the f1 decision exist.

| Option | What it is | Calibration sample (against Tier 1) | Cost evidence | Main risk |
|---|---|---|---|---|
| A. Precomputed shade x tau proxy | Per position x species, effective shade (m2 h on sunlit open ground, crown shadow x (1 - exp(-k LAI))), summed per layout. Already in `shade_sponge/heat.py` / `layout.py` `shade_potential` (v0) | Small: N = 30-50 random layouts on the sub-area (ASSUMPTION, no source) | Tier 1 at 20-25 min per layout (42 trees; Shaamala) gives roughly 10-21 h for 30-50 layouts; at 10-20 s per evaluation (Peng, small site) under 1 h; sub-area dependent, not measured here | Additivity: overlapping shadows take the max (`heat.py`), so the proxy is not exactly additive; trees as shade only |
| B. ML surrogate (e.g. Random Forest) | Learn layout -> f1 from Tier 1 runs | Large: Tan & Liu used 1,500 runs (1,250 train / 250 validation); Oneto et al. 2026 SVR R2 = 0.63 on 314,928 runs, lower on held-out (cited via methodology §6, matrix #64, 🟡 not re-read) | 1,500 runs = 500-625 h at Shaamala cost, 4-8 h at Peng cost | Sampling cost dominates and is the budget risk; weak generalisation reported |
| C. Infrared City API | Vendor AI surrogate returns UTCI/MRT in seconds | Small, to quantify bias: N = 30-50 layouts vs Tier 1 | Vendor-described only (`topic_decision.md` §6.4); access (tutor is a co-founder) unconfirmed 🟡 | Access, licence, black-box error unknown until tested |
| D. Tier 1 on a reduced sub-area | Ladybug in the loop on one block / street | None (it is the reference) | Costed in `methodology.md` §6: impractical for about 830 positions | Sub-area may not represent Porta; fits only as Pareto re-check or as the calibration reference for A-C |

Reading: D is the reference that A-C are checked against, not a rival for the whole site. A is already implemented and free; B and C are the fallbacks if A fails the acceptance test.

## 4. Optimiser options
| Option | Needs | Strength | Weakness | Cost vs 18 Dec plan |
|---|---|---|---|---|
| NSGA-II (pymoo) | No additivity; can call the full raster model (overlaps) | Handles non-additive f1/f2, any constraint | Stochastic, thousands of evaluations (precedents: 200 in Peng; 3,000 in Tan & Liu; 24,000 in Liu); no optimality certificate; 832-variable categorical encoding | Moderate; needs per-evaluation time measured (not in repo) |
| Epsilon-constraint integer programme | (a), (b), (c) below | Exact; finds non-supported Pareto points that the v0 weighted-sum sweep misses; minutes | Wrong if validity conditions fail | Low; v0 already solves a transportation LP with HiGHS (`layout.py` `assign`) |
| Greedy / ranking | (a), (b) | Trivial, transparent | No guarantee once the Shannon floor binds | Lowest |

Validity conditions for the two non-evolutionary options:
- (a) f2 additive per position only where crowns do not overlap. `runoff_model.py` `storage_raster` rasterises ascending so the largest storage wins on overlap (max, not sum) and sets storage over roofs to zero; `layout.py` documents "no overlaps" in `shade_potential`/`water_potential` and re-scores layouts with the raster model.
- (b) The heat proxy must be additive; `heat.py` also takes the max on overlapping shadows, so the same caveat holds.
- (c) The Shannon floor is concave, so it is not linear; it must be replaced by linear proxies (minimum count per species, minimum number of species, or the existing 15% cap) before an integer programme can use it. v0 has no diversity term (checked: no match in `shade_sponge/*.py`).
- Cap only (no floor, additive objectives): the problem is a transportation LP, integral at a vertex (v0 `assign`); this is the case where an exact method beats NSGA-II.

S3 (runoff-only) check. With one s for all species, S = s x LAI, so the per-position value is monotone in crown area x LAI, and S3 reduces to filling species in that order up to the 15% cap. Crown area x LAI from `porta_species_lidar_summary.csv` (my arithmetic: pi/4 x d^2 x LAI): Styphnolobium 204 (n = 5 sample), Melia 126, Jacaranda 123, Tipuana 111, Celtis 33, Brachychiton 32, Pyrus 16. The raster result (`runoff_scenarios.csv`, T2-60, all planes replaced by mature crowns, uncapped) orders them Jacaranda (785 m3 intercepted), Melia (771), Tipuana (759), Styphnolobium (700), Brachychiton (681), Celtis (681), Pyrus (660). The ranking matches except Styphnolobium (top by the product, fourth in the raster). Consistent with overlap/roof clipping breaking additivity, or the n = 5 crown being unrepresentative; not tested here. Practical consequence: the ranking is a cheap first check, and the gap is the reason to re-score with the raster model.

Young crowns (3 m ASSUMPTION): all young replacements give +0.66-0.70% runoff vs S0 at T2-60, so species do not differ at planting; species ranking exists only at the mature horizon (pending #13).

Decision-variable count: 832 plane positions in the inventory (verified in `exchange/to_gh/porta_trees_lidar.csv`), of which 809 have `flag == ok` and are the ones `runoff_model.py` replaces; 23 have no LiDAR crown. `porta_trait_table.csv` lists 829 Platanus x acerifolia and the LiDAR summary 807 + 2 PLATANOR. `replacement_scenario.md` (the stated authority) is absent: the user should fix one number (809 suggested, since only these have crowns).

Reconciliation with the 20 Oct talk: `slides/outline_20oct.md` slide 8 and `scripts/make_infographics.py` (~l. 330) say "NSGA-II ... species at each of the 832 plane positions". `methodology.md` §6 also names NSGA-II, but v0 already uses an LP and reports the front collapsing in the city palette until winter sun is a cost. If the user adopts an exact method, three places need rewording (slide 8, the infographic, §6) and 832 becomes 809; none is edited here. Safe wording either way: "a Pareto search chooses the species at each plane position".

## 5. Sensitivity plan
Parameters (baseline from `runoff_params.json` and `runoff_model.py`):

| Parameter | Baseline | Range and source | Status |
|---|---|---|---|
| s (mm per LAI) | 1.75 | 0.86 (Xiao & McPherson 2016) - 2.2; calibration IQR 1.45-1.92 | Done: `runoff_sensitivity_storage.csv`; street-tree effect at T2-60 is -0.91 / -1.85 / -2.33% for s = 0.86 / 1.75 / 2.2 |
| LAI proxy | species median | +/- IQR per species (e.g. Platanus 2.31, IQR 0.86; Celtis 2.0, IQR 1.3) from `porta_species_lidar_summary.csv` | To run |
| Crown size at horizon | species median (mature) / 3.0 m (young) | Pending #13 | Blocked |
| Young crown | 3.0 m (ASSUMPTION) | Range to be set with #13 | Blocked |
| CN pervious / sealed | 74 / 98 | 74: TR-55 open space, HSG C (soil group unknown); 98: TR-55 impervious; range to add | To run |
| Background LAI | 2.3 | Median LiDAR proxy of street trees; range to add (IQR-based) | To run |
| Pit infiltration | not in v1 | Pending #14 | Out of v1 |
| EPW air temperature offset | 0 | +1 / +2 C (`methodology.md` §5) | To run (f1 only) |
| k (extinction) | 0.5 fixed | Peng 2026; fixed, not varied (state as an assumption) | Fixed |

Method choice. OAT (one at a time) varies each parameter low/high around the baseline: with p parameters, 1 + 2p runs; cannot see interactions (here likely: s x LAI, crown x LAI). Morris elementary effects (Morris 1991, Technometrics 33(2):161-174; bibliographic details confirmed by a web search, DOI not confirmed 🟡): r trajectories, r(p + 1) runs, gives mean and spread of effects, so it flags non-linearity and interactions; r = 10 is a common choice but I have no verified source for it, so treat r as a user-set number. Sobol indices: (to add), more costly.

Run budget (model evaluations; p = 9 parameters in the table excluding pit infiltration and k; "evaluation" = one scenario set scored with the raster models; per-evaluation time is not recorded in the repo, so wall-clock is not stated):
- OAT on fixed layouts: 1 + 2 x 9 = 19 evaluations per layout; for S0, S1 and, say, the 3 chosen Pareto layouts: 19 x 5 = 95.
- OAT with re-optimisation: 19 optimiser runs. With an LP this is cheap; with NSGA-II it is 19 x (pop x generations), e.g. 19 x 3,000 = 57,000 (Tan & Liu size).
- Morris on fixed layouts: r(p + 1) = 10 x 10 = 100 per layout (r = 10 assumed); x5 layouts = 500.
- Morris with re-optimisation: 100 optimiser runs: only viable with the LP route.
Heat parameters (EPW offset) affect f1 only and runoff parameters (s, CN, background LAI) f2 only, so the two sets can be run separately; LAI and crown size affect both.

Robustness outputs: (1) species-ranking stability: Kendall tau (or rank change) of the species order for f2 and f1 across parameter draws; expected from the table above that a common s rescales all species and leaves the order unchanged, while LAI IQR (Celtis 1.3 vs Pyrus 0.84) and crown size can reorder; hypothesis, not tested. (2) Pareto shift vs S1: change in the S4 front relative to S1 (like-for-like, `methodology.md` §7; the defining memo `replacement_scenario.md` is not on main, so S1 is a placeholder) under each parameter set, judged against the minimum meaningful difference (f1) and a runoff threshold the user must set; v1 shows species effects of only 0.17-0.69% of runoff, small against the s-driven range of the tree effect itself (0.4-4.0%, `methodology.md` §4b).

## 6. Recommended default (pending user decision)
- f1: use option A in the optimiser; calibrate it against option D on one sub-area with N = 30-50 layouts (ASSUMPTION); report R2, RMSE and Kendall tau; move to B or C only if A fails the threshold the user sets.
- Optimiser: epsilon-constraint integer programme as the main method with the raster model re-scoring every Pareto layout (overlaps), and NSGA-II as the cross-check on the same problem if time allows; fixes (c) by linear diversity proxies.
- Sensitivity: OAT on fixed layouts first (about 95 evaluations); Morris with r = 10 only on the parameters OAT flags, and with the LP for re-optimisation.

## 7. Question for the user
Do you accept an exact epsilon-constraint programme (with NSGA-II as cross-check) as the main optimiser in place of NSGA-II alone, which would require rewording slide 8, the method infographic and `methodology.md` §6 and fixing the decision-variable count at 809?
