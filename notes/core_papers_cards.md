# Five core papers: one-page cards (27 Oct 2026)

For reading before the 10 Nov tutor session. Source of every number: `notes/lit/literature_matrix.csv` (ids in brackets), `notes/methodology.md` and `CLAUDE.md`. Built from those notes, **not re-checked against the PDFs** (cloud session has no `papers/`). Read the paper itself before quoting a figure.

**How the five fit together.** Nicol and Mannucci mark the gap; Shaamala and Peng are the optimisation precedents; Anys & Weiler and Mannucci give the validation. None does heat + runoff + species traits + optimisation together; that is the contribution.

| Role | Paper |
|---|---|
| Gap: species recommender, no hydrology | 1 Nicol |
| Precedent: species + placement, heat only | 2 Shaamala, 3 Peng |
| Precedent: heat + runoff, no traits, no optimiser | 4 Mannucci |
| Validation of interception | 5 Anys & Weiler |

---

## 1. Nicol et al. 2026: SylvCiT [#28, bucket B3]
*PLoS One 21(2): e0339173, doi:10.1371/journal.pone.0339173. Read level: summary in CLAUDE.md, not a full-text digest.*

**What it does.** Open-source (GPL-v3) recommender for Montreal urban forests. Content-based filtering over 10 functional groups (hierarchical clustering on 7 traits: seed size, specific leaf area, leaf nitrogen, wood density, shade, drought, flood tolerance). Candidates are pre-filtered with the 10-20-30 rule and exclude invasive or pest-affected species. Score = weighted sum of 5 indices (functional-group and species diversity and richness, carbon storage), x = n1/n0 − 1 on the effective number of species.

**Key result.** Diversity gains (mean +8.5% functional diversity in 10 parks). Not a hydrological or thermal outcome.

**What it does NOT say.** No heat-island mitigation and no runoff reduction: the runoff slider is disabled ("under development"). Montreal only; functional groups must be redefined for other regions; fixed DBH 15 cm for new trees.

**How I use it.** The gap: the most advanced trait-based recommender has no runoff and no heat module. Also precedent for the diversity logic (my Shannon / effective-number floor) and for a web front-end.

**Likely question.** "Why not just extend SylvCiT?" Answer to prepare: its traits are resilience traits, not eco-hydrological ones, and it recommends a species mix, not a position.

---

## 2. Shaamala et al. 2025 [#52, B5/B7]
*Cities, doi:10.1016/j.cities.2025.106356. Full text (8 Oct).*

**What it does.** Ant Colony Optimisation (Opossum, Grasshopper) of 42 trees × 4 species in a subtropical suburb (Bongaree, Queensland). Ladybug UTCI per configuration, 20–25 min each. ENVI-met check of optimal vs suboptimal layout. New Bio-Thermal Gain Index.

**Key result.** Mean UTCI 38.31 → 37.75 °C over 100 iterations. Optimal vs suboptimal: −22% of area above 39 °C, +18% below 36 °C, up to 3.5 °C cooler in the evening (bootstrap mean −2.42 °C [1.97, 2.88]).

**What it does NOT say.** One objective (UTCI), one day. Species chosen by morphology only (canopy spread, height, leaf habit); transpiration and LAI not used. The authors name multi-objective optimisation including water sensitivity as future work.

**How I use it.** (a) Precedent for optimising species and placement together. (b) Their own words confirm the multi-objective gap. (c) Cost evidence: 20–25 min per layout is why Porta's ~830 positions need a precomputed shade × τ proxy.

**Likely question.** "Their effect is 0.56 °C on the mean; why is yours worth it?" Prepare: the mean hides the hot area (−22% above 39 °C), and my test is against the city's own replacement, not a random layout.

---

## 3. Peng et al. 2026 [#53, B5/B7]
*Landscape Ecology, doi:10.1007/s10980-026-02324-z. Full text (8 Oct).*

**What it does.** Grasshopper + Ladybug, Outdoor Solar MRT revised with canopy transmittance τ = exp(−0.5·LAI). NSGA-II (Wallacei X, 20 × 10 = 200 evaluations). Objectives: UTCI heat stress at 14:00 in summer and winter, and |cost − budget|. 25 × 36 m campus site in Shanghai.

**Key result.** Under one camphor tree (LAI 3.2): measured MRT 46.5–48.6 °C; original Ladybug 42.1–44.0 °C (more than 6 °C low); LAI-revised 45.2–46.5 °C (2–4 °C low). Summer optimum LAI 4.6, 8 m crown, 12 m height, 10 m spacing: UTCI 30.4–30.8 °C, MRT up to −3.5 °C. Winter optimum LAI 0.6; deciduous conical 12 m trees were robust in both seasons.

**What it does NOT say.** Generic tree types, no real species. Constant k. No transpiration. No runoff. Runtime 10–20 s per evaluation, up to 2–3 h per run on a small site.

**How I use it.** The τ correction goes into my Tier 1 heat module (k = 0.5; `methodology.md` §5). The summer/winter trade-off motivates my winter-sun cost (summer shade is a benefit, winter shade a cost). Same stack I run in Grasshopper.

**Likely question.** "Is k = 0.5 valid for plane trees?" Honest answer: it is their value, fitted on one camphor tree (LAI 3.2); I use it as a sourced starting point, and a sensitivity test on k for planes is still to do (not yet done, as far as these notes show).

---

## 4. Mannucci et al. 2025 [#51, B5/B8]
*City and Environment Interactions, doi:10.1016/j.cacint.2025.100215. Full text (8 Oct).*

**What it does.** One Grasshopper workflow for heat and flood on a small Mediterranean square (Piazza Anco Marzio, Ostia). Ladybug/Honeybee UTCI + MOCI on a 2 m grid for the hottest day; runoff by a Kangaroo particle simulation (qualitative) plus SCS curve number (composite CN). Ladybug checked against ENVI-met at 4 points.

**Key result.** Ladybug vs ENVI-met: UTCI MBE 0.8–2.3 °C, CVRMSE 7–13%; MRT MBE 2.4–5.9 °C, CVRMSE 22–38% (worst under direct sun, up to +8.65 °C UTCI at 7–8 h). Peak UTCI 29–41 °C. SCS-CN runoff depth about 95.5 mm for the design event. Ladybug treats trees as shade only and likely underestimates vegetation cooling by about 2–3 °C.

**What it does NOT say.** Scenario testing only: no species traits, no optimisation. Particle runoff not calibrated. No CFD wind.

**How I use it.** (a) The closest precedent for heat + runoff in Grasshopper: it shows my idea is not empty, and where it differs (traits, optimisation, a rule-based baseline). (b) The only published error band for Ladybug vs ENVI-met I have: an f1 difference counts only if it exceeds the 0.8 °C low end (`notes/decisions/heat_objective.md`). Note this is a published benchmark, not my own run.

**Likely question.** "So they already did heat + runoff?" Answer: for fixed scenarios on one square, with no species and no optimiser.

---

## 5. Anys & Weiler 2024 [#1, B1]
*Hydrological Processes, doi:10.1002/hyp.15146. Full-text digest.*

**What it does.** Field measurement of throughfall and stemflow on urban trees in Freiburg: 8 trees per species, 76 events, with LAI, PAI, leaf area density, crown metrics and surface sealing.

**Key result.** Mean event interception *Tilia cordata* 70.3% vs *Acer platanoides* 54.8%. Interception correlates with LAI/PAI (adjusted R² > 0.45); falls with rainfall depth and intensity; lower LAI at most sealed sites; stemflow < 1%.

**What it does NOT say.** Only two species; small mean event (6.7 mm); Freiburg, not Mediterranean short intense storms. Data are open (FreiDok).

**How I use it.** Calibration: on the open data (16 trees, Apr–Sep 2021, 51 events ≥ 1 mm) the pooled effective storage is **s = 1.75 mm per unit LAI** (lime 1.85, maple 1.60), per-tree interception 38–78%, event RMSE 0.9–3.2 mm (`methodology.md` §4b). Also the evidence that species and LAI drive interception.

**Caveats I must state.** The same s is used for every species. The LiDAR LAI proxy (median about 2.3) is probably below their ground LAI (1.4–4.9 per tree, 13 of 16 at ≥ 2.5), so storage is probably underestimated. Neither of their species is a Porta plane tree.

**Likely question.** "Why is a German lime/maple calibration valid for Barcelona?" Answer: it is a direction-of-effect and magnitude check, with s varied over a range in sensitivity runs; it is not a Barcelona validation.
