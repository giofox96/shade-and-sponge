# Thesis outline (draft 1, 26 Oct 2026)

**Structure:** the tutor's three parts (CLAUDE.md, "Tutor's requirements"): **Purpose → Background → Contribution to knowledge.**
**Framing:** "a computational method for X", not "research on X".
**Citation style:** APA 7, author–date (no IAAC/UdL rule found, 26 Oct; confirm with the tutor).

**Paths:** a bare file name (e.g. `topic_decision.md`) is in `notes/` or `notes/decisions/`.
**Status key:** ✅ material is in the notes and ready to draft · 🟡 partial, or a decision is still open · ❌ result not produced yet.

**Length:** about 60–80 pages of body text (`ASSUMPTION`; no rule found). The percentages are each chapter's share.

**Working title:** *Shade and Sponge: a trait-based method for choosing plane-tree replacements that keep cooling and storm-water interception in Barcelona* (`ASSUMPTION`, to agree).

---

## Front matter
- Abstract (250 words), keywords. Write it **last**.
- Acknowledgements, list of figures and tables, abbreviations (UTCI, LAI, SCS-CN, CN, CHM, DTM, T2-60, S0/S1a/R/A/R+A).

---

# PART I · PURPOSE

## 1. Introduction (10%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 1.1 | **Context:** Barcelona will replace more than half of its plane trees within ten years. The master plan caps any species at 15% and sets a 30% cover target. Sidewalk width sets the tree size. Trees are replaced one at a time | `notes/topic_decision.md` §10.2 (context); `notes/tree_master_plan.md` §1, §4 | ✅ (press figures 🟡: mark them as press) |
| 1.2 | **Problem in one sentence**, then the five-point problem: the qualitative rule (2004/2005), invisible in practice, no quantities, large crown differences, both hazards overlap in Porta | `topic_decision.md` §10.1–10.2; `tree_master_plan.md` §5b | ✅ |
| 1.3 | **Why it matters:** canopy cover. Porta has 20.1% against the 30% target, and planes make up ≈29% of its canopy | `topic_decision.md` §10.3; `databases/barcelona/porta_canopy_cover.csv` | ✅ |
| 1.4 | **Why Porta:** both hazards above the city's 60th percentile; first at the 50th/60th/70th; 832 planes | `notes/site_selection.md`; `notes/city_screening.md` | ✅ |
| 1.5 | **Research question v7 + SQ1–SQ4** (SQ4 = additions) | `topic_decision.md` §10.5, §10.6 | ✅ |
| 1.6 | **Hypotheses H1, H2 + the declared validity boundary** (H3 withdrawn, and why) | `topic_decision.md` §8, §9.5, §10.5 rows 5 and 9; `notes/decisions/hypothesis_tests.md` | ✅ |
| 1.7 | Primary user (computational designer), the two front-ends, the scope (Porta first, then city-wide screening), thesis map | CLAUDE.md "Tool"; `notes/citywide_plan.md` §1 | ✅ |

---

# PART II · BACKGROUND

## 2. Street trees, heat and pluvial runoff: mechanisms and traits (15%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 2.1 | Pluvial vs fluvial flooding; why trees matter for frequent, short storms and not river peaks | CLAUDE.md "Known weaknesses"; `databases/data_inventory.md` §6 (Bologna dropped) | ✅ |
| 2.2 | **Rain interception:** storage capacity, LAI, event size, leaf-off. Anys & Weiler 2024; Xiao & McPherson 2016; Baptista 2018; Zabret & Šraj 2019; Selbig 2021 (4% of runoff) | `notes/lit/literature_matrix.csv` (bucket B1); `notes/decisions/interception_parameter_definition.md` | ✅ |
| 2.3 | **Tree pits and infiltration:** Bartens 2008; Grey 2018; Thom 2020/2022 | matrix; `todo_manual.md` (pit papers) | ✅ |
| 2.4 | **Shade and pedestrian heat:** UTCI, MRT, crown transmissivity τ = exp(−k·LAI); Rahman 2019; Speak 2020; Peng 2026; Santos Nouri 2018 (Tipuana) | matrix (bucket B3); `notes/decisions/heat_objective.md`; `notes/method_heat_validation.md` §2 | ✅ |
| 2.5 | **Evapotranspiration, and why it stays outside the model:** Ladybug is shade-only (Mannucci 2025); runoff is per event; Mediterranean and paved-pit trees transpire least (Rahman 2019); no wood-anatomy data yet | `notes/methodology.md` §5 "Known limits"; `hypothesis_tests.md` §2; `notes/method_traits.md` row D | ✅ |
| 2.6 | **Where the objectives agree and where they conflict:** crown × LAI drives both; leaf habit and winter sun set them apart | `topic_decision.md` rows 80–81; `shade_sponge/README.md` "Winter sun access" | ✅ |
| 2.7 | **Leaf phenology** of the palette species (iNaturalist evidence) | `notes/decisions/leaf_state_inat.md`; `databases/traits/phenology_palette.csv` | ✅ |

## 3. How Barcelona chooses its street trees (10%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 3.1 | Master plan 2017–2037: the 15% cap and its stated reasons; the 30% cover target | `tree_master_plan.md` §1–§3 | ✅ |
| 3.2 | The 2011 street-tree guide: sidewalk width → size class and spacing | `tree_master_plan.md` §5; `notes/sidewalk_width.md` | ✅ |
| 3.3 | **Gate 1:** the 2004/2005 district × sidewalk table, and Porta's plantings checked against it (up to ~90% off the table, an upper bound) | `tree_master_plan.md` §5b | ✅ (🟡 if Parcs i Jardins replies) |
| 3.4 | The 2026 replacement mix (press) → baseline **S1a**; S1b is cited but not run | `topic_decision.md` §10.4 | ✅ |
| 3.5 | **Diversity rules of thumb:** Santamour 1990 (10-20-30), Kendal et al. 2014; why caps on species alone are weak | `topic_decision.md` §10.2 "Gap"; matrix #139, #140 | ✅ |

## 4. State of the art: computational tools for urban trees (15%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 4.1 | **Runoff models** for design: SCS-CN, Rational, SWMM, i-Tree Hydro; the choice for a 1 m grid | `methodology.md` §4; matrix (bucket B2) | ✅ |
| 4.2 | **Heat models:** Ladybug (Tier 1), ENVI-met (Tier 2), Infrared City; validation evidence | `method_heat_validation.md` §1, §3, §6; `notes/decisions/weather_forcing.md` | ✅ (weather forcing 🟡: undecided) |
| 4.3 | **Optimisers and recommenders:** SylvCiT (runoff disabled), Shaamala 2025 and Peng 2026 (heat only), Schrodi 2023, Tan & Liu 2026 (closest precedent: no runoff), Wu 2024 and Mannucci 2025 (scenarios, no species) | `notes/decisions/contribution_statement.md` §1; matrix | ✅ |
| 4.4 | **Precedents in practice** (5+, from the RM map) | `notes/miro_map_proposal.md`; `notes/research_method_guidelines.md` §H | 🟡 (the RM map is due 27 Oct) |
| 4.5 | **The gap**, in three layers: practice, research, diversity literature | `topic_decision.md` §10.2 "Gap"; `contribution_statement.md` | ✅ |

---

# PART III · CONTRIBUTION

## 5. Method: the Shade and Sponge tool (20%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 5.1 | Overview flowchart; the design principles: one Python core with two front-ends, and every parameter either sourced or marked `ASSUMPTION` | `slides/outline_10nov.md` §10–11; `slides/fig_v7/` flowcharts; `shade_sponge/README.md` | ✅ |
| 5.2 | **Data:** inventory, LiDAR 2021, DTM, buildings, Resilience Atlas, RESCCUE, PDISBA IDF; licences | `databases/data_inventory_barcelona.md` | ✅ |
| 5.3 | **Tree model:** per-tree height, crown and LAI from LiDAR; traits at equal trunk size | `scripts/bcn_lidar_porta.py`; `databases/data_inventory_barcelona.md` §G–H; `topic_decision.md` §9.9 | ✅ |
| 5.4 | **Topography:** Priority-Flood/D8 routing, water convergence, capture distance to hotspots | `shade_sponge/README.md` (site.py, topo.py) | ✅ |
| 5.5 | **Heat proxy:** sun positions, building and crown shadows, opacity from LAI × leaf fraction; summer benefit, winter cost | README (heat.py); `methodology.md` §5 | ✅ |
| 5.6 | **Runoff module:** storage s·LAI + SCS-CN; s = 1.75 mm/LAI calibrated; season-weighted storms | `methodology.md` §4b; `scripts/calibrate_interception.py`; README (season.py) | ✅ |
| 5.7 | **Rules as constraints:** the 15% cap, the sizing rule, façade clearance, the palette (city 7 / Barcelona 34), the genus and family check | README (layout.py); `topic_decision.md` §10.6 | ✅ |
| 5.8 | **Optimiser:** weighted-sum LP sweep (HiGHS), Pareto front; NSGA-II if needed | README; `methodology.md` §6 | ✅ (NSGA-II ❌) |
| 5.9 | **Scenarios:** S0, R (S1a vs optimised), A (free spots), R+A; project area | `topic_decision.md` §10.6; `scripts/porta_planting_spots.py` | ✅ |
| 5.10 | **Front-ends:** Grasshopper exchange (and Ladybug UTCI); web app with live re-optimisation | `exchange/README.md`; `web/README.md`; `study/tool_tutorial.md` | ✅ |

## 6. Validation (10%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 6.1 | Validation strategy (flowchart): what is validated against what | `slides/outline_10nov.md` §14; `topic_decision.md` §10.5 "What can be answered" | ✅ |
| 6.2 | Interception calibrated on Freiburg field data (Anys & Weiler 2024) | `methodology.md` §4b | ✅ |
| 6.3 | **Heat:** proxy vs Ladybug Tier 1 on the same layouts; Ladybug vs ENVI-met benchmark (Mannucci 2025) | `method_heat_validation.md` §6 | ❌ Ladybug run pending (to-do item 3) |
| 6.4 | Routing vs the RESCCUE flood maps (ROC AUC 0.52; tail informative) | `study/guide.md` (routing vs RESCCUE); `scripts/` RESCCUE check | ✅ |
| 6.5 | **What the model can resolve:** Δmin = 91 m³ | `notes/decisions/runoff_metric_sensitivity.md` §8, §10 | ✅ |
| 6.6 | Sensitivity of the winter-sun result (8 variants) | `shade_sponge/README.md` "Sensitivity" | ✅ (re-run 26 Oct) |
| 6.7 | **Transfer test:** Mataró or Florence; what travels and what does not | `notes/transferability.md`; `notes/catalan_transfer_city.md` | 🟡 (Mataró URLs unchecked) |

## 7. Results: Porta (15%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 7.1 | **R:** optimised vs S1a on heat proxy, winter sun, runoff (total vs Δmin, hotspots), canopy cover, diversity | `shade_sponge/README.md` "S1a and equal trunk size"; `databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv`; `slides/fig_v7/res_01–02` | ✅ |
| 7.2 | **A and R+A:** free planting spots; the gap to 30% (SQ4) | `databases/barcelona/additions_summary.csv`; `slides/fig_v7/res_03_scenarios` | ✅ |
| 7.3 | **SQ3 trade-off:** the summer–winter front is robust; heat–runoff is still open | README "Winter sun access"; `topic_decision.md` §10.5 row 9 | ✅ (heat–runoff 🟡) |
| 7.4 | **SQ1 in UTCI**, on one street and then Porta | Ladybug runs in `exchange/from_gh/` | ❌ |
| 7.5 | City-wide screening layer | `notes/citywide_plan.md` §4 | ❌ |

## 8. Discussion (8%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 8.1 | Answers to SQ1–SQ4; H1 and H2 accepted, rejected or "not resolved" | ch. 7 | 🟡 |
| 8.2 | **Limits:** transpiration; airport weather file; CHM shrubs; the press-sourced 2026 mix; flat positions; licences (hotspot layer, Mataró) | `methodology.md` §5, §11; `todo_manual.md` (licences); `topic_decision.md` §10.3 caveats | ✅ |
| 8.3 | Transferability: four degrees of transfer | `transferability.md` §1–§5 | ✅ |
| 8.4 | Implications for the city: performance data per species and position; the genus/family check | `topic_decision.md` §10.2 "Our inference" | ✅ |

## 9. Conclusion: contribution to knowledge (5%)
| § | Content | Source notes | Status |
|---|---|---|---|
| 9.1 | Contribution statement | `topic_decision.md` §9.3 | ✅ |
| 9.2 | Future work: NSGA-II, carbon and biodiversity modules, the tree-health proxy, city-wide use | CLAUDE.md "Tool"; `citywide_plan.md` §3 | ✅ |

---

## Back matter
- **References** (APA 7, generated from Zotero).
- **Appendix A:** parameter table, each one sourced or marked `ASSUMPTION` (from the README tables and `notes/methodology.md`).
- **Appendix B:** data sources and licences (`databases/data_inventory_barcelona.md`).
- **Appendix C:** tool user guide (`study/tool_tutorial.md`, shortened).
- **Appendix D:** code and data availability (the repository, the web app URL).

## Before drafting (open items that change the text)
1. **Ladybug Tier 1 UTCI** on one street (6.3, 7.4): the only ❌ in Purpose to Validation.
2. **Weather forcing** decision (4.2).
3. **Methodology §12** proposed changes: adopt or drop (ch. 5).
4. **Zotero:** add Kendal 2014, Santamour 1990 and Nieuwenhuijsen 2022 (in `papers/`, not in the `THESIS_MACAD` collection, checked 26 Oct).
5. Confirm the citation style, length and format with the tutor.

## Suggested drafting order
Chapter 3 → 2 → 4 → 5 → 1 → 6 → 7 → 8 → 9 → abstract.
The chapters whose material is ✅ come first. The Introduction is written once the background holds. Results and Discussion wait for UTCI.
