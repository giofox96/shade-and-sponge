# Contribution statement candidates and prior-art verdict (issue #6)

Status: **PENDING USER DECISION.** Nothing here is adopted. Drafted 11 Oct 2026 from `notes/lit/prior_art_matrix.csv` (18 rows) and `notes/lit/literature_matrix.csv`.
Read level is marked per claim: full text = matrix `read_level` full text; **(abs)** = abstract or search summary only; 🟡 = not verified.
Matrix ids 82-87 were assigned on this branch. Other open PRs may use 82+ (PR #28 adds 82, PR #25 adds 62-68-style ids), so **renumber at rebase** and update the ids quoted below.

## 1. Verdict on the gap

**Wording tested** (`topic_decision.md` line 82 (§6.1 'Is it already done?'), `slides/outline_20oct.md` slides 6 (lines 37-39), `slides/fig/04_gap_matrix`): existing workflows either assess heat and runoff for fixed scenarios without species traits (Mannucci 2025; Wu 2024), or optimise trees for heat only (Shaamala 2025; Peng 2026); SylvCiT has its runoff module disabled.

**Verdict: holds, with narrower wording.** The sentence is true for everything read in full, but a new close neighbour makes the unqualified form ("nobody optimises species for heat and runoff") unsafe.

- **Holds (full text):** Mannucci #51, Shaamala #52, Peng #53, Wu #56, Hao #62, Elkhateeb #63, Oneto #64, Tan & Liu #80 (the eight papers this issue targeted), plus Nicol #28, Pacetti #18, Cortinovis #69. None optimises species and positions against pedestrian UTCI/MRT and runoff together. The nearest heat optimiser, Tan & Liu 2026 (#80), has no runoff; Mannucci (#51) has both but no species and no optimisation.
- **Needs narrower wording (new): Dong et al. 2026, npj Urban Sustain. 6:47, doi 10.1038/s42949-026-00361-w (#85, full text from the open PDF).** It optimises species mixes for stormwater and microclimate (plus air quality and carbon) with NSGA-III. The differences from our proposal are real but specific. Heat is "building energy saving (a proxy for microclimate regulation)", not UTCI/MRT. Runoff is i-Tree Eco avoided runoff. The decision variable is species proportions per 0.25 km2 cell, with no tree positions. Study area: Philadelphia. So the safe claim is: *"no method yet chooses street-tree species and positions against pedestrian-level UTCI and event runoff together"*. Do not say "species for heat and runoff" without the qualifiers "pedestrian UTCI" and "positions".
- **Read at abstract level only (could still flip, see fetch list):** Nyelele 2021 #25 (multi-objective planting locations incl. runoff and heat reduction; linear programming, Bronx; no species (abs + search summary)); Xing 2026 #82 (PET + runoff + CO2 by GI scenarios (abs)); Eslami 2026 #83 (runoff only (abs)); Liang 2021 #84 (**title only; unverified 🟡**).

**`todo_manual.md` "The gap holds" (lines 26 and 28) is confirmed in substance and should be qualified:** it was written before Dong 2026, and Nyelele, Liang, Xing and Eslami are still abstract-level or title-only. Line 29 (Tan & Liu: "closest precedent, but no runoff: the gap holds") is confirmed (full text).

**Gap in the text, not edited:** the §6.1 table in `topic_decision.md` (line 82, "Is it already done?") already cites #51-53, #62-64, #69 and #80 as read, but Dong 2026 is missing.

**Figures and slides:**
- `fig_gap()` / fig 04: **add a "Dong et al. 2026" row** (suggested coding, matching the existing 0 / .5 / 1 scheme: heat .5 (energy proxy, not UTCI), runoff 1, species traits .5 (i-Tree values, not traits), optimises species and positions .5 (species, not positions)). Add Dong to the footer list of rows read in full. Optional: row for Nyelele 2021 once its abstract-level reading is confirmed.
- Slide 6 script: add one clause, for example "One recent study optimises species mixes for stormwater and an energy-based heat proxy per district grid cell, not for pedestrian heat stress at tree positions." Slide 6 should not say "no one optimises species for heat and runoff".

## 2. Candidate contribution statements (pending user decision)

**A. Method contribution.** A reproducible computational workflow that selects replacement street-tree species *and* positions in a Mediterranean district against two objectives, pedestrian UTCI and event runoff, using species-resolved crowns and leaf area (from LiDAR and a trait table) and a seasonal (leaf-on) interception term.
- Basis: the closest optimisers are heat-only (Shaamala #52, Peng #53, Tan & Liu #80, Hao #62), the heat + runoff workflow does not optimise (Mannucci #51), and the species-level heat + runoff optimiser works at district-cell scale with an energy proxy (Dong #85).
- Reusable pieces that are already published: LAI-based canopy transmittance for Ladybug (Peng #53); NSGA-II with a surrogate for speed (Tan & Liu #80); interception with time-varying LAI (Eslami #83, abs).

**B. Knowledge contribution.** A quantified comparison, for the named replacement palette in Porta, of cooling against rain interception: do the species and layouts that minimise UTCI also minimise runoff, and how large is the trade-off compared with like-for-like replacement and single-objective layouts?
- Hooks in the literature: LAI scaling moves summer runoff and surface temperature together (Wu #56: LAI x1.4 gives runoff -10.7% and mean LST -2.5 C; LAI x0.8 gives runoff +6% and LST +1.5 C). A seasonal LAI trade-off exists for comfort (Peng #53). Dong #85 reports, for optimised vs random species composition, a gain of about 18-20% for stormwater (0.71 vs 0.60 million m3/yr in matrix row #85) against +77.1% for its energy proxy, in i-Tree Eco terms; this may suggest the trade-off may be asymmetric, but it is a different metric and a different city.
- No species in the Porta palette except *Pyrus calleryana* has a measured storage value, and cooling values are modelled (e.g. Silva 2025 #47, generic ENVI-met tree geometry), not measured (`topic_decision.md` §7 v4, citing Xiao & McPherson 2016 and Silva 2025 #47); the result therefore depends on stated assumptions and carries a sensitivity analysis.

**C. (Optional) Validation contribution.** A transparent two-tier check of a fast shade x transmittance heat proxy against Ladybug UTCI, with the Ladybug-vs-ENVI-met error known from Mannucci #51 (UTCI MBE 0.8-2.3 C; MRT MBE 2.4-5.9 C; Ladybug treats trees as shade only and underestimates vegetation cooling by roughly 2-3 C) and the surrogate-vs-simulation accuracy of Tan & Liu #80 (RMSE 0.09 C site-mean UTCI) as reference points. Several optimisers have no field validation (Elkhateeb #63, Tan & Liu #80, authors' own limits); stating validation limits plainly is a defensible differentiator, not a claim of field accuracy.

## 3. Search log (11 Oct 2026, WebSearch mode standard, no date filter available)

Relevant hit = a tree study addressing heat *and* runoff. Search summaries are weak evidence for absence.

| # | Query (exact) | Relevant hits | Notes |
|---|---|---|---|
| 1 | street tree species selection and placement optimisation UTCI and stormwater runoff multi-objective | 2 | Dong 2026 (#85); Langenheim & White 2022 (#86, qualitative) |
| 2 | tree planting layout optimization mean radiant temperature and rainfall interception runoff NSGA-II urban trees | 0 | heat-only: Schrodi 2023 (#87, abs); a 2026 Swin-Unet + genetic-algorithm Tmrt preprint, heat only (🟡 snippet only, not added) |
| 3 | Grasshopper Ladybug SWMM street trees species pluvial flooding and thermal comfort parametric workflow 2024 2025 | 0 new | Morganti, Mannucci & Fiocchi 2024 (pluvial Grasshopper workflow; abstract shows no species or thermal) 🟡 not added; Milosevic 2017 pre-2022 |
| 4 | trait-based tree species selection urban cooling and stormwater interception trade-off Mediterranean street trees | 0 | Canberra shading-tree trade-off is cooling only (surface vs thermal), no stormwater |
| 5 | street tree species ranking pedestrian thermal comfort UTCI and rainfall interception runoff reduction combined assessment 2023 2024 2025 urban trees both heat and stormwater | 0 | Lisbon UTCI paper = Silva 2025 (#47); interception papers separate |
| 6 | ENVI-met and SWMM coupled tree species heat mitigation stormwater green infrastructure street trees scenario 2024 | 0 | no ENVI-met + SWMM species study found |
| s1 | Nyelele 2021 "multi-objective decision support framework ..." | n/a | gave Bronx, linear programming, cover/runoff/PM2.5/heat/cost/equity (abs) |
| s2, s3 | Liang 2021 title (exact); same topic keywords | n/a | paper not found: no abstract |

Result: 2 real new hits relevant to heat + runoff (Dong 2026 full text, Langenheim 2022 partial text), 1 heat-only placement optimiser (Schrodi 2023, abs). Verified by fetching: Dong (repository page and open PDF), Langenheim (PMC), Schrodi (arXiv abstract page).

## 4. Fetch list for the user

1. **Liang 2021** (doi 10.1016/j.scitotenv.2021.146415): title only, no abstract found anywhere. Carries the novelty claim until read: if it is tree-level heat + runoff optimisation, the verdict changes.
2. **Nyelele 2021** (doi 10.1016/j.landurbplan.2021.104172, #25): abstract-level only. Carries the novelty claim: check whether species are an optimisation variable and which heat metric it uses.
3. **Dong 2026** (doi 10.1038/s42949-026-00361-w): open PDF at https://edoc.hu-berlin.de/18452/37591. Save it to `papers/`; I read it in full, but the Supplementary tables of species values are not seen.
4. **Xing 2026** (doi 10.3390/su18042142, open MDPI PDF, blocked in the cloud) and **Eslami 2026** (doi 10.71573/zhbx9v70): abstract-level; unlikely to flip the verdict (GI scenarios; runoff only).
5. Tan & Liu 2026 is full text (#80) and already ticked in `todo_manual.md` (line 29).
6. `to_get_manually.md` was updated for items 1-4 and has 3 new entries (Dong, Langenheim, Schrodi). Its older Mannucci, Shaamala, Peng and Wu lines (already read in full) were not touched.

## 5. Caveats

- Coding in `prior_art_matrix.csv` comes from matrix rows, stored abstracts and search summaries, not from fresh full-text reads, except for Dong (#85) and Langenheim (#86, first ~100k of 147k characters).
- Rows #28, #18, #69 (and the fig 04 codings) were added so the CSV covers the figure's precedents; Pacetti and Cortinovis are coded from their matrix rows.
- Nyelele's matrix row #25 was not edited; the prior-art row adds search-summary detail (Bronx, linear programming).
- Fact-check could not re-open the Dong PDF (login/403), so Dong's NSGA-III, species count and 0.71 vs 0.60 figures rest on matrix row #85; the repository abstract confirms only Philadelphia, 0.25 km2 cells, ~20% stormwater and up to 80% microclimate.
