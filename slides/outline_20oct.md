# 5-minute talk, 20 Oct 2026: slide outline and script (draft v1, 8 Oct)

**Format:** 9 slides, 16:9, Google Slides. Figures: `slides/fig/*.png` (insert as images) or `*.svg` (to edit). Regenerate them with `python scripts/make_infographics.py`.
**Script:** about 650 words, which is about 4 min 40 s at a calm 140 words per minute and leaves 20 s of slack. The times in brackets are the cumulative target.
**Sources:** every number is from `notes/topic_decision.md` §7, `notes/site_selection.md`, `notes/methodology.md` §4b, or the figures' own source lines. `*` on a figure = read from the abstract only. Get the full texts before the talk (see `notes/todo_manual.md`).

---

### 1. Title [0:10]
**On slide:** *Shade and Sponge*: a computational method to choose which species replace Barcelona's plane trees, for heat and runoff. Name · MaCAD, IAAC · 20 Oct 2026.
**Visual:** one photo of Av. Meridiana's plane trees (yours).
**Say:** "Barcelona will replace hundreds of plane trees in the coming years. My thesis is a computational method to decide which species replace them, and where, for heat and for rain."

### 2. Problem: two hazards, one street, one decision [0:45]
**On slide:**
- Sealed surface 45% → 72% (1956–2009)
- ~3 storms a year above 60 mm/h in the first 20 min (Resilience Atlas)
- Among Europe's highest heat-island mortality burdens (Iungman et al. 2023)
- Tree plan: no species above 15%; plane trees are ~29% of street trees

**Visual:** two icons (rain / sun) over one street section.
**Say:** "Two hazards hit the same streets. Barcelona's sealed surface grew from 45 to 72 percent between 1956 and 2009. About three storms a year exceed 60 millimetres per hour in their first twenty minutes, and they flood streets where the sewer is too small. In summer, the city carries one of Europe's highest heat-island mortality burdens. Meanwhile, the tree master plan caps every species at 15 percent. Plane trees are about 29 percent of street trees, so many will be replaced, and that choice affects both hazards."

### 3. Why Porta [1:20]
**On slide:** First of 73 neighbourhoods at every threshold · flood #13 · surface heat #11 (+1.36 °C) · heat vulnerability #12 · 832 plane trees · the six replacement species already grow there.
**Visual:** `notes/figures/porta_profile.png` (or `bcn_site_screening.png`).
**Say:** "To test this I needed a neighbourhood with both hazards and many plane trees. I screened all 73 neighbourhoods with open data. To qualify, a neighbourhood had to be above the city's 60th percentile for flood hazard, surface heat and plane density at the same time. Porta, in Nou Barris, comes first at every threshold I tested. It has 832 plane trees, and the six species the city proposes as replacements already grow there. Sant Antoni floods more, but its heat is average, so it becomes my contrast site."

### 4. Literature, runoff side [2:05]
**Visual:** `slides/fig/02_runoff_evidence.png`, with `01_lit_map.png` small in a corner (or as a backup slide).
**Say:** "The literature review covers 61 sources. On the runoff side, two findings matter. First, species differ. In field studies a crown intercepts roughly 10 to 70 percent of rainfall, and the main driver is leaf area. Second, the benefit fades as storms grow. A paired-catchment study measured a 3.5 to 4 percent cut in runoff volume from street trees, with no effect on peak flow. So trees are a tool for frequent storms, not for extreme events."

### 5. Literature: same tree, two jobs [2:40]
**Visual:** `slides/fig/03_heat_runoff_traits.png`
**Say:** "On the heat side, leaf area and crown size also drive shade and cooling, so the two goals share drivers. But they also pull apart. Leaf habit decides whether a crown is there for summer heat or for autumn storms. And transpiration, the stronger air-cooling effect, needs water. That is why one score is not enough: species choice needs a multi-objective search."

### 6. The gap [3:20]
**Visual:** `slides/fig/04_gap_matrix.png` (main) and `05_palette_data_gap.png` (click-in, or next to it).
**Say:** "Here is the gap. The closest precedents either assess heat and runoff for fixed scenarios without species traits, or optimise species and positions for heat only. One of them names a multi-objective version with water as future work. SylvCiT, the most advanced trait-based recommender, has its runoff module disabled. There is also a data gap. For the six replacement species we can measure crowns on site from LiDAR. But rain storage is measured for only one of them, and none has a measured cooling value."

### 7. Research question and hypotheses [3:55]
**On slide:**
**RQ:** In Porta, as plane trees are replaced, which species and positions jointly reduce pedestrian heat stress (UTCI, peak summer hour) and event runoff volume (1-, 2-, 10-yr design storms)? How large is the trade-off?
- **H1, synergy:** trait-based layouts beat like-for-like replacement on both goals.
- **H2, trade-off:** heat and runoff optima differ mainly in species, not positions.
- **H3, boundary:** the runoff benefit shrinks as storms grow.

**Say:** "So my question is this. In Porta, as plane trees are replaced, which species and positions jointly reduce pedestrian heat stress, measured as UTCI at the peak summer hour, and runoff volume for 1-, 2- and 10-year design storms? And how large is the trade-off? I test three hypotheses. First, trait-based layouts beat a like-for-like replacement on both goals. Second, the heat and runoff optima differ mainly in species, not positions. Third, the runoff benefit shrinks as storms grow."

### 8. Method [4:30]
**Visual:** `slides/fig/06_method_pipeline.png`
**Say:** "The method has five steps. From 2021 LiDAR I extract every tree's height, crown and a leaf-area proxy. A Python runoff module and a Ladybug heat module in Grasshopper score each layout. An NSGA-II search chooses the species at each of the 832 plane positions, under the city's 15 percent rule and a diversity floor. The output is a Pareto front between heat and runoff, which I will then test on Sant Antoni and on Florence."

### 9. First result and next steps [5:00]
**Visual:** `notes/figures/runoff_results_v1.png`
**On slide:** Street trees today: −1.9% runoff in a 2-yr storm (−2.9% on streets and squares); field benchmark 4% · young replacements lose >⅓ of the benefit · benefit shrinks with storm size (H3).
**Say:** "The runoff module already runs. I calibrated canopy storage on open field data from Freiburg. Today's street trees cut runoff in a 2-year storm by 1.9 percent, or 2.9 percent on streets and squares. That is the same order as the 3.5 to 4 percent measured in the field. Replacing the planes with young trees loses more than a third of that benefit, and the benefit shrinks for bigger storms, as H3 predicts. The heat module is next. Two things would help me: the city's flood depth maps, and access to Infrared City."

---

## Backup slides (only if asked)

### B1. If the tutor finds the scope too narrow: from the crown to the tree as a system
**Visual:** `slides/fig/07_tree_system_backup.png`
**On slide:**
- Core today: species × position → UTCI + runoff.
- **Extension (one added design variable): the tree pit:** open area, soil volume, surface.
- Soil: 2–3 pit-soil options from the literature, with sensitivity. There is no stratigraphy data under the streets.
- Carbon: reported, not optimised (carbon lost when mature planes are replaced).

**Say (~85 words, only if asked):** "If the scope needs to be wider, I would not add parallel themes. I would widen the tree into a system. The pit is the one design variable I'd add, because it links the two goals: it takes runoff from the pavement and stores it as water for transpiration, which cools the air more than shade does. Soil would enter as two or three literature options with sensitivity, since there is no survey under the streets. Carbon would be reported, not optimised."

**Status of the evidence:** the water link rests on Park et al. 2026 (transpiration 1.15 °C vs shade 0.43 °C), Pace et al. 2025 (soil moisture: dry soils, more runoff reduction; wet soils, more cooling) and Mannucci et al. 2025 (irrigation trade-off). Bartens et al. 2008 is now read in full: roots raise infiltration through compacted subsoil (+63% overall and +153% in the more compacted soil; Ksat ×27 in structural soil over compacted subsoil), with no significant difference between oak and maple. Grey et al. 2018 and Thom et al. 2020, 2021 are not read yet: read them before using this slide. Pit dimensions are not in the open inventory, which has irrigation type (`tipus_reg`) and water type (`tipus_aigua`) only.

### Other backup material
- `slides/fig/01_lit_map.png`: what the 61 sources cover, and how many I read in full.
- Site-selection robustness: 2,000 random weightings, thresholds at the 50th/60th/70th percentile (`notes/site_selection.md` §3–4).
- Calibration: `notes/figures/interception_calibration.png` (s = 1.75 mm per unit LAI; 16 trees, 51 storms).
- Sensitivity of the tree effect, s = 0.86–2.2 mm per unit LAI: 0.4–4.0% of total runoff (`databases/barcelona/runoff_sensitivity_storage.csv`).
- Limits: the LiDAR LAI proxy is probably low; the same storage coefficient for every species; volume only, with no routing yet.

## Likely tutor questions, with short answers
- **Why not peak flow?** Field evidence shows that trees barely change peak flow (Selbig et al. 2021). Volume is what they can change.
- **Is a 2% effect worth a thesis?** The thesis is the method and the trade-off, not a big runoff number. H3 states the limit openly, and the heat side may dominate.
- **Where do species values come from, if most are not measured?** LiDAR crowns and LAI on site, database traits, and genus or leaf-habit proxies with sensitivity ranges. TRY and i-Tree requests are pending.
