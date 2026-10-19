# 20 Oct 2026 tutor session: slide outline and spoken script (draft v3, 19 Oct)

**What changed in v3 (19 Oct, evening).** The deck is rebuilt to follow the rhythm of `study/guide.md`: **one idea per slide**, the number first and its caveat in the same breath, and the limits said before the tutor asks. It goes from 10 slides to **17 + 3 backups**. Six new figures were written for it (`02_one_sentence`, `03_problem`, `07_heat_evidence`, `11_research_question`, `12_hypotheses`, `17_limits_asks`); the others are the existing ones, renamed. The two RM-seminar figures stay parked in `slides/seminar_rm/`.

**Figure files = slide numbers.** `slides/fig/NN_*.png` is the figure for slide NN. Slides **4, 14, 15** have no file there on purpose: they use a plot from `notes/figures/`. Slide 1 is a full-bleed photo slide, built from `slides/fig/01_title_photo.webp`. Backups are `B1_*`, `B2_*`. Regenerate everything with `python scripts/make_infographics.py` (run it from `scripts/`).

**Length.** Brackets in the headings are the cumulative target at **150 words a minute** (most people present at 140–160).
- **Full deck, 17 slides:** 1,542 spoken words ≈ 10:17 (11:01 slow, 9:38 brisk).
- **Core, 12 slides** (drop 2, 5, 7, 10, 15): 1,162 words ≈ 7:45 (7:16 brisk). **Aim for this one** — you said overrunning is fine, and it still covers all six things the tutor asked for.
- **Short, 9 slides** (1, 3, 4, 6, 9, 11, 12, 13, 14, then one spoken line of slide 17's three asks): 875 words ≈ 5:50 (5:28 brisk). To get strictly under 5:00, drop slide 9 (the gap, 86 words) or trim slide 4 — but then say the gap in one line inside slide 11.
- Order in which to cut if you are stopped: 5 → 10 → 15 → 7 → 2 → 16 → 8.
- Longest single slides, if you need to trim: 16 (123 w), 12 (131 w), 7 (104 w), 15 (102 w), 4 (105 w).

**Sources.** Every number is from `notes/topic_decision.md` §7, `notes/site_selection.md`, `notes/methodology.md` §4b and §6, `notes/transferability.md`, `notes/catalan_transfer_city.md` §1–§5b, or the figure's own source line. The study version of all of this, with the "check yourself" questions, is `study/guide.md` §0–§15.

---

## 1. Title — CORE [0:28]
**Figure:** `slides/fig/01_title.png` — full-bleed photo of the Porta allotments at Carrer d'Alcúdia × Carrer de la Maladeta, with the title over a scrim. The bare crowns in the foreground are plane trees, which is the whole thesis in one picture.
**On slide (in the figure):** *Shade and Sponge* — a computational method for choosing which species replace Barcelona's plane trees, and where, scored on summer heat and on storm runoff. MaCAD, IAAC · Tutor session, 20 October 2026.
**Two things to do yourself:** add **your name** to the title block (type it in Slides, or ask for it in the figure), and **confirm the photo credit** — the file came from a web image, so the author and licence are unverified (`notes/todo_manual.md`). If it is not yours to use, swap in your own photo of the same corner: `slides/fig/01_title_photo.webp`, then re-run `make_infographics.py`.

**Say (69 words):**
"This is Porta, at the corner of Alcúdia and Maladeta, and those bare crowns are plane trees. Barcelona has to replace a large share of its street trees, because one species — the plane — is twenty-eight percent of the city stock, and twenty-nine percent in the neighbourhood I work in, while the tree plan caps every species at fifteen. My thesis is how to decide what goes back."

---

## 2. The thesis in one line — EXTRA [0:54]
**Figure:** `slides/fig/02_one_sentence.png`
**On slide:** species × position → heat + runoff → trade-off. Plus the three "what it is not" lines.

**Say (66 words):**
"In one line: species times position, scored on heat and on runoff, and what I report is the trade-off between them. Three things it is not. It is not a flood model — the hotspots come from the city's map. It is not a city-wide plan. And it is not a ranking of species: the same tree is good or bad depending on where it stands."

---

## 3. The problem: two hazards, one street, one decision — CORE [1:32]
**Figure:** `slides/fig/03_problem.png`
**On slide:** the three columns of the figure (rain / heat / the decision already taken).

**Say (95 words):**
"Two hazards arrive on the same streets. Barcelona's sealed surface went from forty-five to seventy-two percent between 1956 and 2009. About three storms a year exceed sixty millimetres an hour in their first twenty minutes, and the sewer is only sized for a ten-year storm — above that, the surface carries the water. In summer the city has one of the highest heat-island mortality burdens in Europe. And the decision is already taken: the plane trees are coming out. Nobody has to be convinced that something should be planted. The question is what, and where."

---

## 4. Why Porta — CORE [2:14]
**Figure:** `notes/figures/porta_profile.png` (fallback: `notes/figures/bcn_site_screening.png`).
**On slide:** Porta, Nou Barris · 0.84 km² · 73 screened, **first of the eligible set at every threshold** (#2 overall on the equal-weight score; top 3 in 53% of 2,000 random weightings) · ranks among the 72 with complete data: flood #13 · surface heat #11 (+1.36 °C) · heat vulnerability #12 · **832 plane trees** · 2,825 street trees, 53 taxa · the six named replacement species, plus *Styphnolobium*, already grow there.

**Say (105 words):**
"I needed one neighbourhood where both hazards and the replacement problem are real at the same time. I screened all seventy-three with open data: to qualify, a neighbourhood had to be above the city's sixtieth percentile for flood hazard, for surface heat and for plane density, simultaneously. Porta comes first at every threshold I tried. On the equal-weight score across the whole city it is second, and it stays in the top three in just over half of two thousand random weightings. It has eight hundred and thirty-two plane trees. Sant Antoni floods more but its heat is average, so it becomes my contrast site."

---

## 5. What the review covers — EXTRA [2:33]
**Figure:** `slides/fig/05_lit_map.png`
**On slide:** 135 on-topic sources, 128 read in full; what they cover (runoff · heat · traits · optimisation · precedents).

**Say (48 words):**
"The review is a hundred and thirty-five sources on topic, and a hundred and twenty-eight of them I have read in full rather than from the abstract. I will take two findings from the runoff side and two from the heat side, because those four decide the method."

---

## 6. Evidence: what a tree does for rain — CORE [3:10]
**Figure:** `slides/fig/06_runoff_evidence.png`
**On slide:** interception 4–70% of rainfall across the field studies, leaf area the main driver · paired-catchment study: **4%** of runoff volume measured (Selbig 2021), 3.5% in the calibrated re-analysis (Coville 2022), **no effect on peak flow** · the benefit falls as the storm grows.

**Say (91 words):**
"Two findings. First, species differ: a crown intercepts somewhere between four and seventy percent of rainfall across the field studies, and the main driver is leaf area — which is a measurable trait, not a preference. Second, the size of the prize is small and it has a boundary: a paired-catchment study measured four percent of runoff volume from street trees — three and a half in the calibrated re-analysis — and no effect at all on peak flow. So trees are a tool for frequent storms, not for extreme ones."

---

## 7. Evidence: what a tree does for heat, and what my model cannot see — EXTRA [3:51]
**Figure:** `slides/fig/07_heat_evidence.png`
**On slide:** the two columns of the figure.

**Say (104 words):**
"On the heat side the honest version is two-sided. A crown works mostly through radiation — the sun-to-shade gap on a hot afternoon is between two and nearly five degrees of felt temperature, and that is a lower bound, and leaf area decides how much sun gets through. Transpiration cools the air more, but it needs water — and per leaf area it is lowest in Mediterranean climates, and separately about ten times lower for a tree in a paved pit than over grass. My engine ignores transpiration altogether. That is why the heat objective is a ranking of layouts, not a temperature forecast."

---

## 8. Same tree, two jobs — CORE [4:22]
**Figure:** `slides/fig/08_heat_runoff_traits.png`
**On slide:** shared drivers (crown size, LAI) · what pulls apart (leaf habit: summer shade vs autumn storms; transpiration needs water; winter sun is a cost).

**Say (77 words):**
"Here is why one score is not enough. The two goals share their drivers — crown size and leaf area feed both shade and interception — so part of the benefit is free. But they pull apart on timing: leaf habit decides whether the crown is there for the August heat or for the October storm, and in winter the same crown becomes a cost, not a benefit. Shared drivers, different calendars. That is a multi-objective problem."

---

## 9. The gap — CORE [4:56]
**Figure:** `slides/fig/09_gap_matrix.png`
**On slide:** precedents either assess heat **and** runoff for fixed scenarios without species traits, or optimise species and positions for **heat only**; SylvCiT's runoff module is disabled; Dong et al. 2026 work per 0.25 km² cell with an energy proxy, not per tree with pedestrian UTCI.

**Say (86 words):**
"The gap is narrow and I want to state it narrowly. The closest work either assesses heat and runoff for fixed planting scenarios, without species traits, or optimises species and positions for heat alone. The most advanced trait-based recommender, SylvCiT, has its runoff module written in the paper as disabled. Nobody chooses street-tree species *and* positions against pedestrian-level heat stress *and* event runoff together. That sentence is the gap, and every word in it is load-bearing; the contribution I would claim from it is the method."

---

## 10. The other gap: the data — EXTRA [5:20]
**Figure:** `slides/fig/10_palette_data_gap.png`
**On slide:** for the 7 candidate species: LiDAR crown ✅ for all · rain storage measured for one · no measured cooling value.

**Say (60 words):**
"There is a second gap, and it is in the data. For the city's own replacement species I can measure the crown on site from the laser scan. But canopy storage has been measured for one of them, and none has a measured cooling value. That gap is not a weakness of the thesis, it is one of its results."

---

## 11. The research question (v5) — CORE [6:01]
**Figure:** `slides/fig/11_research_question.png`
**On slide (the figure carries it):**
> **RQ (v5, 19 Oct).** In Porta, as plane trees are replaced under the city's tree plan, which replacement species and positions jointly reduce (a) pedestrian heat stress (**mean UTCI over 12–17 h on a hot design day**, along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year PDISBA design storms)? **How large is the trade-off between the two, compared with the current trees, a like-for-like replacement with the city's named palette, and single-objective layouts?**

*Changed on 19 Oct (your decision): the heat metric is the 12–17 h mean, not the peak summer hour — at the peak the metric saturates, since even full shade is above 32 °C in 5 of 6 afternoon hours (`notes/topic_decision.md` §8).*

**Say (102 words):**
"So, the question. In Porta, as the plane trees are replaced, which species and which positions jointly reduce pedestrian heat stress and event runoff volume for one-, two- and ten-year design storms — and how large is the trade-off, measured against three baselines: the trees that are there today, a like-for-like replacement, and each single-objective optimum. One thing I changed yesterday: I measure heat as an average over the afternoon, twelve to five, not at the single peak hour — at the peak even full shade is above the stress threshold, so the metric saturated and no layout could show a benefit."

---

## 12. Two hypotheses, and the one I took out — CORE [6:54]
**Figure:** `slides/fig/12_hypotheses.png`
**On slide (the figure carries it):**
- **H1 · synergy** — at the same number and size class of trees, trait-based layouts beat like-for-like replacement on **both** goals.
- **H2 · trade-off** — heat-optimal and runoff-optimal layouts differ mainly in **species**, not in positions.
- **H3 · withdrawn, 19 Oct** — *the runoff benefit shrinks as the return period grows*. It was a hypothesis until the model showed it is an identity (I = min(P, S), every crown full at every storm), so it is now a **declared validity boundary**, not a test.
- Minimum meaningful difference **Δmin = 91 m³**, fixed before the runs — today's exploratory best is **78 m³**, i.e. below it.
- **Question for you:** we removed H3 and declared it a boundary instead — is that the right call?

**Say (131 words):**
"Two hypotheses, and one I removed. One, synergy: at the same number and size of trees, a trait-based layout beats a like-for-like replacement on both goals. Two, trade-off: the heat optimum and the runoff optimum differ mainly in species, not in positions. I fixed a minimum meaningful difference before running anything — ninety-one cubic metres — and on today's exploratory numbers the best layout does not clear it, which I would report as not resolved. The third one I took out yesterday. It said the runoff benefit shrinks as storms grow, and the model cannot fail it: with a full crown at every storm that is arithmetic, not a test. So it is now a declared boundary of the method. My question to you is whether that is the right call."

---

## 13. The method — CORE [7:32]
**Figure:** `slides/fig/13_method_pipeline.png`
**On slide:** 5 steps: LiDAR trees → trait table → runoff module (Python) + heat module (Ladybug in Grasshopper) → NSGA-II over the 832 positions, under ≤ 15% per species and a diversity floor → Pareto front, scenarios S0–S4, then Sant Antoni and the transfer city.

**Say (95 words):**
"The method has five steps. From the 2021 laser scan — flown in September, with the leaves on, which matters — I get every tree's height, crown and a leaf-area proxy. A Python module scores runoff for a design storm; a Ladybug module in Grasshopper scores felt temperature on a design afternoon. A genetic search then chooses the species at each of the eight hundred and thirty-two plane positions, under the city's fifteen-percent rule and a diversity floor. The output is a Pareto front, and then the same machine is pointed at a second site."

---

## 14. First result: the runoff module runs — CORE [8:12]
**Figure:** `notes/figures/runoff_results_v1.png`
**On slide:** today's street trees: **−1.85%** runoff at T = 2 (−2.9% on open ground, i.e. everything but roofs) · field benchmark 3.5–4% · young replacements lose **≈ 37%** of that benefit · effect falls 3.16% → 0.90% from T = 1 to T = 10 · calibrated on 16 trees, 51 storms (Freiburg), s = 1.75 mm per unit LAI.

**Say (101 words):**
"The runoff module already runs. I calibrated canopy storage on open field data — sixteen trees, fifty-one storms. Porta's street trees as they stand today cut runoff in a two-year storm by one point eight five percent, or about three percent counting open ground only, everything but the roofs. That is the same order as the three and a half to four percent measured in the field, which is the check I wanted. Replace the mature planes with young trees and more than a third of that benefit disappears during the transition. That number is for the city, not for me."

---

## 15. First result: shade, and a real trade-off — EXTRA [8:53]
**Figure:** `notes/figures/tool_v0.png`
**On slide:** optimised vs random palette: **+16% summer shade**, robust across 8 sensitivity variants — but **no winter gain** (−0.8 to +7.9%: about equal or worse) · beyond the balanced layout a genuine trade-off: **−17.6% winter shade for −18.0% summer shade** in the base run (ratio ~0.6–1.0 across the variants) · **even with mature replacement crowns**, no layout reaches today's planes (balanced: −7.5% summer shade).

**Say (102 words):**
"The first version of the optimiser also runs, on the shade side. Against a random palette, an optimised one gives sixteen percent more summer shade, and that holds across eight sensitivity variants — but it buys no winter sun at all: about equal, or slightly worse. Push it further and the trade-off becomes real: you buy winter sun with summer shade, one for one in the base run and two-thirds to one across the variants. And this is with mature replacement crowns — even then, no layout reaches the planes that are standing today. That is the honest shape of the problem."

---

## 16. Transferability: the code travels, the evidence does not — CORE [9:42]
**Figure:** `slides/fig/16_transferability.png`
**On slide:**
- Site-agnostic **kernels** (routing, crown-shadow geometry, SCS-CN) carry no local constant; a new site is one data adapter. `heat.py` and `runoff.py` still hold Barcelona design days, the calibrated *s* and the IDF path.
- The transfer bill is **data**: inventory · leaf-on point cloud · IDF · flood map · traits · phenology · policy.
- **Florence** (first choice): ~82,000 trees, a 1 km IDF grid, a published pluvial index — but only 1 m rasters, so the point cloud is request-only. Measured traits for **19%** of trees against **40%** here.
- **Mataró** (Catalan fallback, 19 Oct): the same leaf-on classified ICGC product, same climate zone, same CRS — and, of the two finalists, the only city with a **design storm of its own**.
- **No Catalan city publishes a city-wide pluvial map.** Barcelona's RESCCUE model is the only one found — which is why Porta was the right place to calibrate.

**Say (123 words):**
"Last piece: how far this travels. The code is site-agnostic by construction — the routing, the shadow geometry and the runoff kernel carry no local constant. What does not travel is the evidence, and in particular one input: a laser scan taken with the leaves on, dense enough to see inside a crown. Florence has the trees and the rainfall but only rasters, so I have to ask for the cloud. My fallback is Mataró, which has the scan and, unlike Badalona, its own design storm — borrowing Barcelona's would have made the test circular. And the thing I did not expect: no Catalan city publishes a city-wide pluvial map. Barcelona's is the only one I found. That is why I calibrated here."

---

## 17. What I cannot do yet, and what would unblock me — CORE [10:17]
**Figure:** `slides/fig/17_limits_asks.png`
**On slide:** the limits column, the three asks, and the plan to 18 December.

**Say (87 words):**
"I would rather say the limits myself. It is volume, not peak flow. It is a hazard index, not water depth — my own routing is not a flood map and I tested that. The leaf-area proxy is probably low. And the third hypothesis is true by construction of my model, so I declare it as a boundary rather than claim it as a result. Three things would unblock me: the licence to use the city's flood-depth maps, access to Infrared City, and the Florence point cloud."

---

# Backup slides (only if asked)

## B1. If the scope looks too narrow: from the crown to the tree as a system
**Figure:** `slides/fig/B1_tree_system.png`
**On slide:** core today = species × position → UTCI + runoff · the one extension worth making is the **tree pit** (open area, soil volume, surface) · soil as 2–3 literature options with sensitivity · carbon reported, not optimised.

**Say (~85 words):** "If the scope needs to be wider, I would not add parallel themes. I would widen the tree into a system. The pit is the one design variable I'd add, because it links the two goals: it takes runoff from the pavement and stores it as water for transpiration, which cools the air more than shade does. Soil would enter as two or three literature options with sensitivity, since there is no survey under the streets. Carbon would be reported, not optimised."

**Status of the evidence:** the water link rests on Park et al. 2026 (transpiration 1.15 °C vs shade 0.43 °C), Pace et al. 2025 (dry soils → more runoff reduction; wet soils → more cooling) and Mannucci et al. 2025 (irrigation trade-off). Bartens et al. 2008, read in full: roots raise infiltration through compacted subsoil (+63% overall, +153% in the more compacted soil; Ksat ×27 in structural soil), with no significant difference between oak and maple. Grey et al. 2018 (Melbourne clay: 0.72 m² pits draining ~200 m² kept a median 11% of runoff; ~90% retention needs pits of 2.5–8% of their catchment; exfiltration, not the young tree, removes ≥ 88% of the water). Thom et al. 2020 (established evergreen street trees transpired the equivalent of 17% of annual runoff from the ~200 m² catchment draining to each 6 m² trench, though the trenches did not raise transpiration — probably because the trees were not water-limited). Thom et al. 2022 (13 species in pots: crop factor 0.33–1.56, *Pyrus calleryana* among the high transpirers). So the pit link is plausible for large established crowns, but untested in the field for Barcelona's deciduous palette and autumn storms. Pit dimensions are not in the open inventory, which carries irrigation type (`tipus_reg`) and water type (`tipus_aigua`) only.

## B2. If the tutor presses on transferability: the 22-city Catalan screening
**Figure:** `slides/fig/B2_catalonia_lidar.png`
**On slide:** 22 Catalan municipalities screened on criterion 1. **18 are leaf-on and classified**; 3 are unclassified (Girona and Vic leaf-on, Figueres only partly, flown in April); 1 is leaf-off (Manresa, November). 18 + 3 + 1 = 22. Badalona, Santa Coloma and Sant Cugat were flown on Porta's exact mission day, 26 September 2021 — **a convenience, not a validity condition**; the city chosen is **Mataró** (leaf-on July 2021, classified), on design rainfall and tree data instead.

**Say (~60 words):** "I screened twenty-two Catalan cities on the one input that decides a transfer. ICGC publishes only the flight year, so I read the date from the per-point GPS time in the cloud itself, and checked it against Porta, where it reproduces the date I already had. Eighteen are leaf-on and classified. Three are flown but unclassified, and one is flown in November."

**If asked why not Badalona:** it shares Porta's mission day and has the better rain-gauge record, but **no open tree inventory was found** and it has **no design rainfall of its own** — the only published route is to drive its model with *Barcelona's* IDF curves, which is what the one peer-reviewed study of it does. That makes the transfer test partly circular: you would be transferring to a city whose design storm is, by assumption, the one you started from. A missing species field is a degraded input you can declare; a borrowed design storm invalidates the comparison.

**What is still open on Mataró:** the joined per-tree table (species on positions) is wired into the city's own map viewer but nobody has had a response; three browser URLs in `notes/todo_manual.md` settle it. Without it, species have to be assigned probabilistically from the published composition, which turns a *species-level* transfer test into a **composition-weighted** one. There is also no numeric DBH or height, so the crown/LAI proxy cannot be validated there, and the **licence is unknown for every Mataró asset**.

## B3. If the tutor presses on the design storm: method vs climate
**Figure:** none (text).
**On slide:** raw, Mataró looks **19–32% drier** than Porta, and *duration-dependently* so (0.81 at 10 min → 0.68 at 30 → 0.71 at 60). That pattern cannot be climate. The two numbers are different *kinds* of quantity: Porta's PDISBA value is an across-gauge **envelope** (+24% over the gauge mean) from pluviograph records; Mataró's is a **central** Gumbel estimate from daily maxima with the sub-daily shape supplied analytically. Rebuilt the same way, **66% of the gap goes at 10 min and 77–80% at 20–60 min**, leaving a flat 0.93 at T = 10 and 1.00 at T = 2.

**Say (~55 words):** "A naive city-to-city comparison would have reported a thirty percent climate difference. Most of it is not climate, it is how the two design storms were built — an envelope against a central estimate. Harmonised, what is left is under ten percent. That is the kind of thing a transfer test has to control before it can claim anything."

**The honest caveats:** the flat 0.93 is **not** a finding — it is an identity. Both cities sit in the same I1/Id = 11 region, so the duration factor cancels; any two such cities would give a flat line. The evidence is the *raw* ratio reversing direction with duration, which climate cannot do. The harmonised legs still use different frequency laws (Gumbel for Mataró, SQRT-ET max for Barcelona), and the Témez route carries **no sub-hourly observation from either transfer city** — for Porta the sub-hourly curve is empirical, for Mataró it is an assumption. Also: PDCLAM's "T = 1" column is the Gumbel T = 1.001 limit, so **T = 1 yr is published for no candidate transfer city**. Detail: `notes/catalan_transfer_city.md` §5b.

**On the LiDAR screening, if pressed:** each date is one 150 × 150 m clip at the city centre, not a municipality-wide check — Rubí and Granollers split two missions inside a single clip, and a mission boundary runs through Porta's own tile. Data: `databases/catalonia_lidar_dates.csv`.

## Other backup material
- Site-selection robustness: 2,000 random weightings, thresholds at the 50th/60th/70th percentile (`notes/site_selection.md` §3–4).
- Calibration: `notes/figures/interception_calibration.png` (s = 1.75 mm per unit LAI; 16 trees, 51 storms).
- Sensitivity of the tree effect, s = 0.86–2.2 mm per unit LAI: 0.4–4.0% of total runoff (`databases/barcelona/runoff_sensitivity_storage.csv`).
- Routing vs RESCCUE: `notes/figures/resccue_vs_routing.png` (AUC 0.52; top 0.5% of open ground by upstream area wet in 58–80% of cases).
- Transferability in full: `notes/transferability.md`. Study version of the whole talk: `study/guide.md`.

---

## Likely tutor questions, with short answers
- **Why not peak flow?** Field evidence shows trees barely change peak flow (Selbig et al. 2021). Volume is what they can change.
- **Hasn't Tan & Liu 2026 done this?** They optimise species and positions of 30 trees for heat (UTCI), CO₂ and diversity in a Chicago block, with a similar Grasshopper + NSGA-II approach and a Random Forest surrogate. No runoff, four common Chicago street trees at 5 years old (US allometry), one summer hour. This thesis adds runoff, the city's own replacement palette and the seasons.
- **Hasn't Dong et al. 2026 done this?** They optimise species mixes per 0.25 km² cell, with an energy proxy for heat and i-Tree for runoff, and no tree positions. Hence "species **and** positions", "**pedestrian** UTCI".
- **Is a 2% effect worth a thesis?** The thesis is the method and the trade-off, not a big runoff number. The declared boundary states the limit openly, and the heat side may dominate.
- **Isn't H3 true by definition of your model?** It is, which is why it is no longer a hypothesis: I withdrew it on 19 Oct and kept the content as a declared validity boundary. In field data the intercepted fraction does fall as rain depth grows (Anys & Weiler 2024), so the statement is true — it is just not something my model can test.
- **What if runoff cannot separate the palettes?** Then the runoff part of H1 is "not resolved" (below Δmin = 91 m³, fixed before the runs); heat carries the species choice and runoff is a check. That is still a result.
- **How good is your flood routing?** It finds the main convergence points but is not a flood map (ROC AUC 0.52 against RESCCUE depth); hotspots come from the city's map.
- **Why Porta and not Sant Antoni?** Porta passes both hazards at every threshold; Sant Antoni's heat is below the city median.
- **Why Barcelona and not Florence?** Heat-health evidence, LiDAR, open data and site access — and, as it turns out, the only city-wide pluvial depth model in Catalonia. Florence becomes the transfer test.
- **Where do species values come from, if most are not measured?** LiDAR crowns and LAI on site, database traits, and genus or leaf-habit proxies with sensitivity ranges. TRY and i-Tree requests are pending.
- **Does this only work in Barcelona?** The code does not: a new site is one adapter (`build_<name>()` + `trees_<name>()`). The evidence does: traits, leaf calendar, storm season, flood map and the 15% cap are all local. Detail: `notes/transferability.md`.
