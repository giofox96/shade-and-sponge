# Runoff metric sensitivity: can f2 tell palettes apart? (issue #2)

**Status: exploratory bracket, all recommendations pending user decision.** Methodology status is NOT DEFINED. Aggregate arithmetic only, no change to `scripts/runoff_model.py`, `methodology.md` or `topic_decision.md`.
Reproduce: `python scripts/explore_runoff_sensitivity.py` (repo CSVs only). Full table (7 depths x 16 palettes x 3 s x 2 LAI = 672 rows): `notes/decisions/runoff_sensitivity_table.csv`.

## 1. Method (what the script does)
- Per tree (2,600 LiDAR-ok trees, 809 planes; `porta_trees_lidar.csv`): crown disk area (π d²/4), interception I = min(P, s·LAI), intercepted m³ = area × I.
- Runoff saved = area × [Q(P) − Q(P − I)], SCS-CN (Q as in `runoff_model.py`), CN 98 on the sealed share of crowns and CN 74 on the rest.
- % of event runoff = saved / aggregate no-street-tree runoff of the whole site, background canopy ignored (0.84 km²; about 3% above the grid no-street-tree runoff in `runoff_scenarios.csv`, e.g. 9,879 vs 9,600 m³ at P = 19.6, so percentages are slightly low; 29% roofs and 52% sealed at CN 98, 19% pervious at CN 74; split from methodology §4b).
- Palettes: S0 (current); S1 (all 809 planes replaced by the six candidates in their Porta tree-count proportions, mature LiDAR median crown and LAI); best / worst (all planes at the candidate with highest / lowest crown area × LAI among the six, mature: Melia / Pyrus); single species mature and young (3 m crown). Non-plane trees keep their LiDAR crown and LAI.
- Evaporation: no separate Gash E/R term. s = 0.86 (surface storage only) vs 1.75 (effective, includes event evaporation) is the bracket, as the backlog rescope prescribes (no E/R value exists in the repo; Huang 2017 row 33 is abstract-only).

## 2. Assumptions
| Input | Value | Source |
|---|---|---|
| s low / mid / high | 0.86 / 1.75 / 2.2 mm per LAI | 0.86 = Xiao & McPherson 2016 mean (matrix row 3, full text); 1.75 = calibrated pooled median on Anys & Weiler 2024 (`calibrate_interception.py`, methodology §4b); 2.2 = sensitivity value in `runoff_sensitivity_storage.csv` |
| LAI | proxy as measured; ×1.5 | Proxy is uncalibrated (inventory §G). ×1.5 is an ASSUMPTION that lifts the median proxy 2.3 to about 3.5, inside the Freiburg TLS LAI 2.6–4.9 quoted in methodology §4b and the backlog rescope (the 16 calibration trees span LAI 1.39–4.89, `interception_calibration.csv`) |
| CN 98 / 74 | | ASSUMPTION, TR-55 (as `runoff_model.py`) |
| Sealed share of crowns | 0.52/(0.52+0.19) = 0.73 | ASSUMPTION; land cover unverified; crowns over roofs excluded |
| Young crown | 3 m | ASSUMPTION (as `runoff_model.py`) |
| Land-cover split | 29 / 52 / 19% | methodology §4b, grid model, unverified |
| Storm depths | 19.6 / 31.9 / 62.5 mm | PDISBA T1/T2/T10-60 (`runoff_scenarios.csv`); other P are generic, no return period attached |

## 3. Results (exploratory bracket)
**Check against the grid model.** At P = 31.9 mm, s = 1.75 the script reproduces the per-tree file (456.9 m³) but the grid gives a street-tree share of 405.3 m³ (817.51 − 412.22) because it handles overlap and roof masking. Absolute volumes here are an upper bound; compare palettes within this table only.

**Saturation.** Per-tree saturation depth s·LAI is 1.5 / 4.0 / 13.7 mm (min / median / max, s = 1.75). Every PDISBA storm used on main (≥ 19.6 mm) exceeds the maximum, so all canopies are saturated and intercepted volume is the same at every T. Palette differences show up in f2 only through the SCS-CN slope. Below ~14 mm (P = 5, 10) trees are partly unsaturated and the ranking can change (see below).

**Runoff saved (m³ and % of event runoff), proxy LAI.**

| Palette | P=19.6 (T1-60), s 0.86 / 1.75 / 2.2 | P=31.9 (T2-60) | P=62.5 (T10-60) |
|---|---|---|---|
| S0 | 157 / 316 / 395 (1.6 / 3.2 / 4.0%) | 175 / 353 / 442 (1.0 / 1.9 / 2.4%) | 196 / 398 / 500 (0.5 / 1.0 / 1.2%) |
| S1 | 118 / 238 / 297 (1.2 / 2.4 / 3.0%) | 132 / 266 / 333 (0.7 / 1.5 / 1.8%) | 148 / 300 / 377 (0.4 / 0.7 / 0.9%) |
| best | 146 / 293 / 367 | 162 / 328 / 411 | 182 / 370 / 464 |
| worst | 92 / 185 / 231 (0.9 / 1.9 / 2.3%) | 102 / 207 / 259 (0.6 / 1.1 / 1.4%) | 115 / 233 / 293 (0.3 / 0.6 / 0.7%) |

LAI ×1.5 raises S0 at T2-60 from 353 to 525 m³ (mid s). The table file has all palettes, both LAI readings and the intercepted m³.

**Palette spread vs parameter spread (mid s, proxy LAI, S0 as reference).**
- Palette effect: S1 − S0 = −78 / −87 / −98 m³ at T1/T2/T10-60 (about 0.8% / 0.5% / 0.2% of aggregate event runoff at T1 / T2 / T10-60); best − S0 = −22 to −29 m³; worst − S0 = −131 to −165 m³. S1 and worst lose volume mainly because the planes are the largest crowns, so any replacement with smaller crowns reduces interception; best (Melia, 8.4 m crown, matching the plane's 8.35 m) is about equal to S0.
- Parameter spread of S0 alone at T2-60: s low-to-high 267 m³; LAI proxy-to-×1.5 172 m³; both together 175 to 656 m³. This is 2–3 times the S1 − S0 difference and larger than the gap between S0 and worst.
- So the **level** of f2 (how many m³ or % trees save) is not identified by the current parameters: s and LAI dominate. The **ranking** of the six mature single-species palettes at P = 31.9 mm is identical for all six s × LAI combinations (Melia > Jacaranda > Tipuana > Celtis > Brachychiton > Pyrus). The ranking is identical at every P ≥ 10 mm; at P = 5 mm Tipuana and Jacaranda swap. Ranking mostly follows crown area, not species traits: Melia, Tipuana, Jacaranda have 7.3–8.4 m crowns, Celtis, Brachychiton, Pyrus 3.1–4.6 m.
- Young trees (3 m) are within about ±5 m³ of one another at T2-60 (205–212 m³), so at planting f2 cannot tell species apart; the difference comes from mature crown size, i.e. from the horizon chosen (issue #13).

**Answer to the question.** f2 can order palettes (robustly to s and LAI) but only by crown area, S1 − S0 differences are 0.2–0.8% of event runoff (larger for worst), and absolute levels sit inside the s/LAI uncertainty. It cannot rank species by eco-hydrological traits beyond crown area and the uncalibrated LAI proxy. Cited alone it gives H1 no species signal.

## 4. Metric options (pending user decision)
1. **Design-storm volume (current f2).** Keeps the RQ wording. Weakness: saturated canopies, differences of 0.2–0.8%, T-independent interception (H3 is then a property of SCS-CN, not evidence).
2. **Canopy storage volume Σ area × s × LAI** (m³ held per event, independent of P once saturated). Directly tied to the calibrated trait; avoids dependence on CN and land-cover split; cannot claim a runoff-volume reduction on its own.
3. **Frequent-storm volume** (P below ~14 mm, where trees are unsaturated and species differ most: at P = 10 mm, worst − S0 is −110 m³ and best − S0 −17 m³, as % of a much smaller event runoff). Needs a rainfall-depth distribution from gauge data (inventory B3); not in the repo.
4. **Intercepted depth per tree.** Simple and calibrated but ignores the spatial/CN part that the optimiser uses.

**Suggested default (pending):** keep the T2-60 volume as the headline f2 for continuity, and add option 2 as a companion so the species signal is visible; add option 3 only if gauge data are obtained.

## 5. Draft H1 / H3 wording (pending user decision)
Minimum meaningful difference (MMD), fixed before the runs: candidate = the event-level RMSE of the interception calibration, 0.9–3.2 mm (`interception_calibration.csv`), applied as a depth over canopy area. For a street-tree crown area of 10.4 ha (103,966 m², script output) that is roughly 95–330 m³ of canopy-area interception; the S1 − S0 difference above (78–98 m³) falls at or below the low end of that range. A palette comparison is called meaningful only if it exceeds the MMD under the lowest and highest s.
- **H1 (draft):** at the T2-60 design storm and for the same planting positions, the optimised palette holds at least the MMD more event interception than S1 under s = 0.86 and s = 2.2 mm per LAI. (Caution: with the current model the gain is bounded by crown-area growth, so this is falsifiable but may fail.)
- **H3 (draft):** drop "as predicted by saturation" as supporting evidence. State instead: the palette ranking by f2 is unchanged across T1, T2, T10 and over s and LAI brackets. This is true by construction when all canopies are saturated, so it should be reported as a model property, not as a test of the hypothesis. A real test needs option 3 (unsaturated range) or event data.
- **RQ flag:** "measurably reduce runoff" needs the wording "relative to S1, on the stated metric, above the MMD". Changing slide 7 of `slides/outline_20oct.md` and methodology §4b ("supporting H3") is for the user to decide.

## 6. Gaps
- Tree-pit infiltration, stemflow, overlap and roof masking are absent (aggregate only).
- LAI proxy is uncalibrated; leaf-off season is not covered.
- Sealed share of crowns and the land-cover split are unverified.
- No E/R literature value; evaporation is only bracketed through s.
- Design hyetograph and gauge-based depth distribution still missing.
