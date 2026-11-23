# Tutor feedback, 17 Nov 2026 (A. Chronis): sorted, with answers, questions and the plan to 24 Nov

*Written 18 Nov from Giovanni's dictated notes (four voice messages, no recording of the meeting). Plain-Italian explanations of the points Giovanni asked to understand: `/mnt/project-files/notes/spiegazioni_17nov_it.md` (project files, not in the repo). Previous round: `notes/tutor_feedback_10nov.md`.*

Status marks: ✅ already true in the repo · 🟡 partly · ⬜ to do · ❓ decision for Giovanni.

**The message in one line.** The work is there; the story is not. Next time bring *questions*, not a presentation. Before the 24 Nov Pecha Kucha: (1) a clear narrative (who uses the tool, for whom, what is fixed and why), (2) a methodology anyone can follow. Problem, research question and hypothesis drew no comment.

## 1. Feedback, sorted

### 1a. Narrative and users

| # | What Angelos said | What it means | Action |
|---|---|---|---|
| N1 | "Who are you? A landscape designer, an architect? What do you want to do?" Write it as a statement: "I'm a city planner, I need to add 200% more healthy trees" | One primary user, one goal sentence, in the first slide | ⬜ Narrative one-pager (§4) |
| N2 | Declare the constraints and why they are fixed ("why can't I move anything? because it is decided") | The tool works *inside* a street project that someone else has already designed; it does not redesign the street | ⬜ "Fixed / free" table (§4) |
| N3 | The questions he asked are the ones anyone will ask; the story must survive them | Rehearse answers to his questions in 20 s each | ⬜ Update `study/guide.md` §12 |
| N4 | Talk plainly: in 10–20 min non-specialists (hydrology, trees, design) are lost | Premises in everyday words; technical detail in backup | ⬜ Pecha Kucha script |
| N5 | Be very specific: talk more about Porta; consider specific areas of Porta as case studies | Show Porta with absolute numbers; pick 1–2 small project areas | ⬜ §1c P1–P3 |
| N6 | "Make the story clearer and justify everything" | Every choice traced to a source or declared as an assumption (already the repo rule) | ✅ assumption register (`slides/methodology_17nov.pptx`); ⬜ say it in the talk |

### 1b. Methodology

| # | What Angelos said | What is true today | Action |
|---|---|---|---|
| M1 | The screening was not clear (Giovanni could not explain it) | Screening = indicators computed once per street-tree position, city-wide (`notes/citywide_plan.md` §1–3, `shade_sponge/health.py`) | ⬜ Parameter table x1…xn (§2) + one sketch |
| M2 | Make the tree indicators / parameters explicit, as a table or vector x1, x2, x3, and say how each one acts on the method | Spread over `layout.py`, `health.py`, `porta_sidewalk_width.py` | ⬜ §2 is the draft |
| M3 | Four options per tree, not two: **leave as is, replace, move (transplant), add** | Code: keep / transplant / replace exists on branch `claude/keep-transplant-replace` (no PR; per-tree CSV, "clunky", Giovanni). Additions = free spots. They are **actions**, not scenarios: one project can use all four (Giovanni, 18 Nov) | ⬜ §3; tool work → thread "Sviluppare il tool" |
| M4 | Placement rules too strict: benches can be moved | Of Porta's 267 candidate spots, 115 are excluded; the first recorded cause is a bench for **1** spot, a bollard for 12, a sign support for 34, a crossing for 31, a lamp for 28 (`databases/barcelona/porta_planting_spots.csv`). So benches are not what blocks Porta; signs and bollards are the movable objects that matter | ❓ hard vs movable split (§3b) |
| M5 | Check the rules on the map (Giovanni saw ground-floor private enclosures where no tree can go) | Not in open data; a visual check per project area is feasible, city-wide is not | ⬜ visual check only in the case-study areas |
| M6 | Sketches of the city rules (crown radius, crown diameter, distances), like the drawings in the tool | 2011 guide rules are in `notes/tree_master_plan.md` §5 and `layout.py` (`SIZE_CLASS`, `fits`) | ⬜ 3–4 rule sketches (sidewalk → size class; spacing; distance to lamp/sign; crown vs façade) |
| M7 | Explain HiGHS; "it is not a polygon but a multidimensional polyhedron, a polytope" | Plain explanation exists in Italian (`slides/angelos_17nov_spiegazione_it.md` §3) | ✅ explanation; keep it in backup, one sentence in the talk |
| M8 | How "City rule" is built must be declared | **Inconsistency found:** the web app column "City rule" is **S1a** (press 2026 mix, `web/src/store.js`, `ComparePanel.vue`), while the thesis baseline since 6 Nov is **S1b** (what the city actually planted, 1,444 plane replacements 2018–2026; `notes/methodology.md` S1) | ❓ rename to "City practice" and use S1b everywhere (§5) |
| M9 | 7 or 30 species? | 30 = the city's 2011 catalogue minus the 4 "avoid" species; contains all 6 species the city really plants in place of planes. 7 = city press list + Styphnolobium. Palette 30 vs 7 = +5.0 pts summer shade | ❓ recommendation: 30 (§5) |
| M10 | Budget: start estimating one | Design note done in thread "Stimare il budget di sostituzione e trapianto alberi" (`/mnt/project-files/notes/budget_replacement_transplant.md`) | ⬜ that thread; here only "Step 0: € per back-test group" |

### 1c. Porta, area statistics, runoff

| # | What Angelos said | What is true today | Action |
|---|---|---|---|
| P1 | City-wide figures (e.g. canopy cover of Barcelona) say little; give statistics of the project area | Porta: 83.7 ha, canopy 20.1% (CHM > 2 m, LiDAR 2021) = about 16.8 ha (`notes/topic_decision.md` §10) | ⬜ Porta fact sheet |
| P2 | Absolute numbers as well as percentages ("we want 30% of Porta / of the small area") | 30% of 83.7 ha = 25.1 ha, so the gap is about 8.3 ha of crown. Planting all 152 free spots adds about 0.4 points (relative crown-disc measure), i.e. roughly 0.3 ha: sidewalk additions alone close about 4% of the gap. This is a strong, honest narrative point: street trees cannot reach 30% alone | ⬜ check the 0.3 ha with the canopy script before quoting |
| P3 | Same for runoff: absolute, and per area or per **street segment** | Today runoff is reported as % of the Porta total (T2-60 total about 18,200 m³, since Δmin 91 m³ = 0.5%; hotspot runoff about 2,702 m³). Percentages of a large total look like zero | ⬜ report litres per tree and m³ per street segment draining to a hotspot |
| P4 | s = 1.75 mm: he wanted to understand millimetres vs volume | 1 mm over 1 m² = 1 litre. Celtis, crown 6.3 m (31 m²), LAI ≈ 2.3: holds 1.75 × 2.3 ≈ 4 mm → about 125 L per storm, out of ≈ 1,000 L falling on its crown in the T2-60 storm (31.9 mm) | ⬜ one sketch "a crown is a bucket" |
| P5 | Were other s values tested? | **Yes.** s = 0.86 (Xiao & McPherson 2016), 0.83 (*Quercus ilex*, Hassan et al. 2017) and s per species (17 Nov): differences scale with s, signs and ranking hold, every difference < 1% (`notes/methodology.md` §4b) | ✅ |
| P6 | Hotspots: if runoff barely changes in total, how does it change at the hotspot? He reached it himself: a tree up the hill holds water that would have reached the flood spot | Position test (17 Nov, PRs #134–#135): same Celtis at all 2,825 positions; 74% of positions drain to no hotspot within 100 m; best 100 positions remove 12.5 m³ from hotspots vs 2.2 m³ at random (×5.6), but 12.5 m³ = 0.5% of hotspot runoff | ⬜ "hill" sketch; keep runoff as *do-no-harm* constraint |
| P7 | He liked the trade-off diagrams: the triangle and the chart in the tool (bottom right) — "swag"; it is clickable | `TradeoffChart.vue`: click a point to load that layout; `PriorityTriangle.vue` | ⬜ put both in the Pecha Kucha; demo the click |

## 2. Screening parameters as a vector (draft for M1–M2)

The screening describes **every street-tree position** before any design. Three groups: what is there (the existing tree), where it is (the position), what each candidate species would do there (the score). Only group C enters the optimiser's objective; A decides *which* trees are candidates for replacement, B decides *which species are allowed*.

| x | Parameter | Per | Source | Used for | Status |
|---|---|---|---|---|---|
| **A. The existing tree** |||||
| x1 | Species | tree | Open Data BCN inventory | 15% cap count; S1b baseline | sourced |
| x2 | Trunk class (PRIMERA…EXEMPLAR) | tree | inventory | age proxy; equal-size comparison (TERCERA) | sourced classes; "class = age" ASSUMPTION |
| x3 | Crown diameter, height, crown base | tree | ICGC LiDAR 2021 | shade and interception of today's tree (S0) | measured |
| x4 | LAI proxy (−ln gap / k) | tree | LiDAR gap fraction | crown opacity (heat), storage s·LAI (runoff) | proxy, ASSUMPTION k |
| x5 | Crown-vigour deficit (0–1) | tree | x3, x4 vs same species & class | replacement priority | ASSUMPTION; AUC 0.66 (planes 0.76) on removed trees 2021→2026 |
| x6 | Replacement priority = 0.5·x5 + 0.5·age | tree | x2, x5 | ranks trees for replace / keep | ASSUMPTION weights |
| **B. The position** |||||
| x7 | Sidewalk width (façade → kerb ray) | position | 1:1000 map | size class: < 2.5 m none, < 3.5 small, 3.5–6 medium, > 6 large | 2011 guide pp. 22–23 |
| x8 | Distance to façade | position | 1:1000 map / buildings | crown radius must fit | ASSUMPTION margin 0 m (tested +1/+2 m) |
| x9 | Distance to lamp, sign, traffic light, crossing, bollard, bench | spot | 1:1000 map, Open Data BCN | free spot yes/no | guide (lamp ×0.5, signs, lights); 1 m for small objects = ASSUMPTION |
| x10 | Drains to a flood hotspot (within 100 m) | position | DTM flow routing + Resilience Atlas | counts water only if it would reach a hotspot | ASSUMPTION 100 m (tested 50/200 m) |
| **C. The score of species j at position i** (the optimiser's table) |||||
| x11 | Summer shade, m²·h (12–17 h) | i × j | sun, buildings, crown, opacity | **benefit** (maximise) | proxy; UTCI on final layouts |
| x12 | Winter shade, m²·h (January) | i × j | same, leaf-off opacity | **cost** (minimise) | McPherson 1984, Heisler 1982 |
| x13 | Water held over hotspot-draining ground, m³ | i × j | s·LAI × crown area × x10 | **benefit** (do-no-harm check) | s = 1.75, Anys & Weiler 2024 |
| x14 | Fits (0/1) | i × j | x7, x8, species size class | hard constraint | 2011 guide catalogue |

Optimiser: maximise w1·x11 − w2·x12 + w3·x13 (normalised), subject to x14, one species per position, no species above 15%. Weights are swept (15 combinations), not chosen.

## 3. The four actions (M3, M4)

### 3a. Per tree and per spot

| Action | Applies to | What the tool does | Default | Why / source |
|---|---|---|---|---|
| **Keep** | existing tree | nothing; the tree stays as measured | ✅ default | city replaces mostly one by one (46.8% isolated; 10 Nov) |
| **Move (transplant)** | existing tree | the position is freed and replanted; where the tree lands is outside the tool | off | survival of large transplants is poor (budget thread: Struve 2000); spade limit ≈ DBH 32 cm |
| **Replace** | existing tree | cut + optimiser picks the species (S4) or the city practice draw (S1b) | off | city priority order: safety, dead, declining, uniformity, works last (`notes/tree_master_plan.md` §5) |
| **Add** | free spot | optimiser picks the species | off (on per spot) | 2011 guide + street objects |

The designer sets the action; the tool never decides to cut a healthy tree. The priority score (x6) only *suggests* candidates, because no open tree-health data exists.

### 3b. Placement rules: hard vs movable (proposal, ❓ Giovanni)

| Object | Spots it blocks first (Porta) | Proposal | Reason |
|---|---|---|---|
| Crossing, traffic light, bus stop, driveway | 31 + 5 + 1 + 1 + 2 + 1 | **hard** | safety, visibility, access |
| Lamp | 28 | **hard** (at half the guide's distance, decided 11 Nov) | wiring underground; moving it is a lighting project |
| Sign support | 34 | **movable** (flag, with a cost) | a pole can be shifted a few metres |
| Bollard, bench, fountain | 12 + 1 + 0 | **movable** | Angelos, 17 Nov |

If signs, bollards and benches become movable, Porta's free spots rise from 152 to at most about 199 (only the first cause per spot is recorded, so the true number is lower until re-run). The web app would show these as a third spot colour ("free if you move X").

## 4. Narrative (N1–N2): ✅ approved by Giovanni 18 Nov

**Who.** A designer (landscape architect or urban designer) working on a street project in Barcelona: a resurfacing, a single-level street, a utilities job. The street layout is already decided by the project.

**Goal sentence (Angelos's format).** *"I am redesigning this street. I have to assess the trees that stand there and their condition, and decide which to keep, which to move because the project needs it, which to replace, and where to add new ones, so that the street is cooler in summer, not darker in winter, and not worse for flooding — within the city's rules."*

**Not an option (Giovanni, 18 Nov):** removing a tree without replacing it.

**The method also questions the city's rules (Giovanni, 18 Nov).** City practice does not fully follow the city's own guidance (§9a: 21% of new plantings larger than the 2011 sidewalk rule allows; 51% of Porta's trees closer to a lamp than the guide). Probably for practical design reasons we cannot see in the data. The 2011 guide is technical guidance, not a law, so the point is not "the city breaks the rules" but: either the rules describe what is wanted and practice drifts from them, or practice shows that some rules need updating. The tool can measure **what each rule costs** in shade and runoff (switch it on/off and re-optimise), which turns this into evidence for updating the rules (see the policy-proposal idea, 16 Nov).

**For whom.** The city's tree service (Parcs i Jardins), which approves the planting, and the residents who use the street.

| Fixed (the tool does not change it) | Why | Free (the tool helps decide) |
|---|---|---|
| Street geometry, sidewalk width, kerbs | decided by the street project | action per tree: keep / move / replace |
| City rules: 15% species cap, 2011 sidewalk → size class, spacing, distance to lamps and signs | Pla director de l'arbrat; 2011 guide | species at each replaced position |
| Blocked street objects: traffic lights, driveways (§9d) | traffic layout, private access | additions on free spots, incl. conditional ones after a field check |
| Underground utilities (not in open data) | unknown → spots are an upper bound | moving signs, crossings, lamps, bollards, bus stops (conditional, §9d) |
| Tree health (not in open data) | designer's survey decides | the trade-off: pick a layout on the chart |

## 5. Decisions for Giovanni (recommendations)

| ❓ | Recommendation | Why |
|---|---|---|
| D1 7 or 30 species — ✅ **DECIDED 30 (Giovanni, 18 Nov)** | **30 as the method's palette; 7 only as one sensitivity row** ("a narrow list costs 5.0 pts of summer shade") | 30 comes from the city's own 2011 catalogue (minus its 4 "avoid" species) and contains all 6 species the city really plants for planes; 7 rests partly on press. All recent runs (back-test, city LP) are on 30 |
| D2 Name and content of "City rule" — ✅ **DECIDED "City practice" (Giovanni, 18 Nov); always say it is a practice, not a rule** | **Rename "City practice" = S1b** in tool, slides and thesis; S1a ("announced mix", press) as a footnote | It is not a written rule: it is what the city actually planted 2018–2026, placed within the 2011 sizing rule and the 15% cap. Saying "rule" invites "which rule?" |
| D3 Movable objects | **Signs, bollards, benches movable; the rest hard** (§3b) | Angelos's point; recompute spots |
| D4 Case-study areas in Porta | **Av. Rio de Janeiro** (real 2025 replacement of 22 poplars, back-test) + one designer area drawn in Porta | Real event inside the site; numbers already exist (167 / 74 / 240 m²·h per tree) |
| D5 Schedule table, save configuration (§6) | **After 24 Nov**, in the tool thread; for the talk, one mock-up image at most | Not needed for the story; it is a tool feature |

## 6. Giovanni's tool ideas (18 Nov) → thread "Sviluppare il tool", after 24 Nov

| Idea | Detail | Note |
|---|---|---|
| Tree schedule (like a Revit schedule) | Table of the project area's trees and free spots beside the 3D/2D map; click a tree → row highlighted; click a row → tree highlighted on the map | Replaces the per-tree CSV of branch `claude/keep-transplant-replace` |
| Column **Action** | Keep / Move / Replace (= cut + new) for trees; Add / Leave empty for spots | Same table for trees and spots |
| Column **Reason** | Pick list: dead, diseased, pests, dangerous, roots damage paving, works, other (free text) | The designer's knowledge that open data lacks; also the city's own priority order |
| Save a configuration | Save/load the whole set of actions + chosen layout (not just export CSV) | Keeps the designer in charge; the optimiser fills only what the designer leaves open |

## 7. Questions for Angelos (next meeting: questions, not slides)

1. **User.** Is "a designer working on a city street project" the right primary user, or is the city's tree service more credible as the one who runs the tool?
2. **Move.** Should transplanting carry a cost and a survival rate inside the optimiser, or stay a manual designer choice outside it?
3. **Placement.** Do you agree with the split: crossings, lights, lamps, driveways fixed; signs, bollards, benches movable at a cost?
4. **Budget.** Report € per layout beside heat and runoff, or make it a constraint the optimiser must respect?
5. **Runoff unit.** For a designer, which reads better: litres held per tree, m³ per street segment reaching a hotspot, or % of the area's runoff?
6. **Validation.** Can the back-test on 26 real replacement groups be the main validation, with Ladybug / Infrared City UTCI on selected layouts as the heat check?
7. **Target.** Should the tool accept a target as input ("reach X% canopy in this area") and report how far street trees can go, given that Porta's free spots close only about 4% of the gap to 30%?
8. **Scope.** Is the tree schedule with actions and reasons worth building before December, or is it future work?

## 8. Plan to Tuesday 24 Nov (Pecha Kucha, 5 min)

Order agreed with Giovanni: narrative first, then methodology, then slides.

| Day | Work | Who / thread | Done when |
|---|---|---|---|
| Wed 18 – Thu 19 | Decide D1–D3; correct the narrative (§4) | Giovanni (decisions), this thread | narrative fixed in one paragraph |
| Thu 19 | Porta fact sheet: area, canopy ha and %, trees, planes, free spots, runoff in m³ and per street segment; check the 0.3 ha figure | this thread (data only, no tool changes) | table with absolute numbers |
| Fri 20 | RT blog post due (separate thread "Prepare RT pitch and blog post"): reuse §4 | RT thread | posted |
| Fri 20 – Sat 21 | Sketches: city rules (4), "crown is a bucket", "tree on the hill", four actions | this thread, then Giovanni's taste | 6 images |
| Sat 21 – Sun 22 | Methodology one-page figure with the x1…x14 table; spots re-run with movable objects if D3 = yes | tool thread for the re-run | figure + new spot count |
| Sun 22 – Mon 23 | Pecha Kucha deck + script (story: problem in plain words → who → fixed/free → four actions → Porta case → trade-off chart → what it changes) | new deck thread or this one | deck + script |
| Tue 24 | Rehearse; bring §7 questions to the next tutor meeting | Giovanni | — |

Budget (M10) and tree-pit size continue in their own threads; nothing here duplicates them.

## 9. Follow-up, 18 Nov (Giovanni's answers)

### 9a. City practice vs the city's own rules

Giovanni: "we have the city's rules, but does the city respect them?" Measured on the 2011 guide's sidewalk → size-class rule (species class from the guide catalogue, `layout.SIZE_CLASS`; only positions on measured, façade-bounded sidewalks):

| Trees | Positions with a class | Species larger than the guide allows | Source |
|---|---|---|---|
| Porta, standing today (LiDAR 2021 inventory) | 750 | **171 (23%)**, mostly Catalpa 40, Citrus on sidewalks < 2.5 m 26, Celtis 20, Jacaranda 16 | `porta_sidewalk_width.csv` |
| Back-test groups: trees the city removed | 151 | **75 (50%)** | `backtest_works_guide_capsmall_positions.csv` |
| Back-test groups: what the city planted instead (2018–2026) | 171 | **36 (21%)**: Pyrus on sidewalks < 2.5 m 11, Casuarina on medium/small 19, Gleditsia on medium 4 | same |
| Lamp distance (guide pp. 22–23) | Porta, standing trees | **51%** closer than the guide | `notes/tutor_feedback_10nov.md` A3 |

Reading: the city's new plantings follow the sizing rule much better than the old trees (about 4 in 5 vs 1 in 2), but not always; on lamp distance practice is about half the guide's distance. So "City practice" = the species mix the city really planted (S1b), placed within the sizing rule and the 15% cap. That is *kinder* to the city than reality (we force its mix to fit the rule), which makes the comparison with the method conservative. The method follows the same rules; the only difference is **which species goes where**.

### 9b. Everything that removes a free spot in Porta

Candidate spots come from geometry first (sidewalk ≥ 2.5 m, 0.7 m from the kerb, spacing 7/9/13 m by size class): 267. Objects then remove 115 (first recorded cause only):

| Object | Spots removed | Distance | Source of the distance | Moving it (estimate, not sourced) | Proposal |
|---|---|---|---|---|---|
| Sign support | 34 | 3 m | 2011 guide | easy: unbolt and re-fix, traffic authority sign-off | conditional |
| Crossing | 31 | 3 m | ASSUMPTION (sight lines) | no: road layout | blocked |
| Lamp | 28 | half the guide (1.5–3.3 m) | guide × 0.5, ASSUMPTION 11 Nov | hard: cable in a trench, lighting design | conditional, flagged "costly" |
| Bollard | 12 | 1 m | ASSUMPTION | easy | conditional |
| Traffic light (city + OSM) | 5 + 1 | 3 m | 2011 guide | no: signal design, wiring | blocked |
| Driveway (OSM parking entrance) | 2 | 3 m | ASSUMPTION | no: property access | blocked |
| Bus stop | 1 | 8 m | ASSUMPTION | no | blocked |
| Bench | 1 | 1 m | ASSUMPTION | easy | conditional |
| Fountain | 0 | 1 m | ASSUMPTION | medium (water pipe) | conditional |
| **Not in open data** | ? | — | — | — | field check: underground utilities, driveways not in OSM, private ground-floor enclosures, bar terraces, bins, hydrants, manholes, bike/motorbike parking |

With this split: **152 free · 75 conditional (47 easy + 28 lamps) · 40 blocked.**

### 9c. Tool: one schedule, two tabs (proposal for "Sviluppare il tool", after 24 Nov)

Giovanni's idea: show all possible spots, each with what stands in the way, and let the designer decide after a field check. Recommended form:

- **Tab "Trees"** (existing trees in the area): id, species, size, priority score, Action (keep / move / replace), Reason (dead, diseased, pests, dangerous, roots damage paving, works, other + text), species chosen.
- **Tab "Spots"**: id, sidewalk width, size class, Status (free / conditional / blocked), What is in the way (e.g. "sign 2.1 m"), Action (add / leave empty), Field check (to do / ok / not possible).
- Same map selection for both tabs (click ↔ highlight). When a spot gets **Add**, it moves to the Trees tab as "new tree", so one list holds the final design.
- The optimiser uses free spots by default; a switch "include conditional spots" adds the 75, each flagged in the results.
- Save / load the whole configuration (actions, reasons, field checks, chosen layout).

### 9d. DECIDED (Giovanni, 18 Nov): spot classes

- **Blocked:** traffic lights (6) and driveways (2) only: changing them means changing traffic or private property.
- **Conditional:** sign supports (34), crossings (31: mid-block ones can move, and in a street rebuild they are repainted), lamps (28, flagged costly), bollards (12), bus stop (1).
- **Ignored:** benches (and fountains): no longer an obstacle.
- Result: **153 free · 106 conditional · 8 blocked** (267 candidates). To do in the tool thread: re-run spots with these classes; the optimiser keeps 153 free spots by default, conditional ones on a switch.
- **Done 23 Nov (tool thread, branch `claude/spot-classes`):** `scripts/porta_spot_classes.py` writes `spot_class` + `reasons` into `porta_planting_spots.csv`. Counting every object within clearance, not only the first rule, gives **153 free · 103 conditional · 11 blocked**: 3 crossing spots also sit within 3 m of a traffic light. `layout.planting_spots()` keeps the free ones (conditional=True adds the others). In the web app, conditional spots have an amber dot and "Fill spots" uses them only when "Include … conditional spots" is ticked. Web data and additions still need a rerun on the PC (`python -m shade_sponge.web_export`, `scripts/run_additions.py`).
- Crossing rules searched (18 Nov, web only, not fact-checked): **no Barcelona or Catalan rule found that sets a distance between a tree and a crossing**; the tool's 3 m stays an ASSUMPTION. National accessibility order TMA/851/2021 (as summarised in Basque Government sheet U3): the crossing must be visible day and night; at crossings without traffic lights no element that blocks the view may be placed; the sidewalk area of the kerb ramp must be free of obstacles. DGT, *12 Recomendaciones de movilidad urbana segura y sostenible* (a recommendation, not a law): remove car parking and street furniture at least 6 m before the crossing in the direction of traffic; about one crossing every 100 m. The Catalan Accessibility Code (Decree 209/2023) summary read has nothing specific. Reading: crossings stay **conditional** (they can be moved in a street rebuild), with the flag "check visibility: DGT recommends 6 m clear before an unsignalised crossing". Existing sensitivity: crossing clearance 2/3/5 m changes kept spots little (`notes/sidewalk_width.md`).

## 10. Porta fact sheet (P1–P3), absolute and %

All from files in `databases/barcelona/`; heat and runoff are today's trees (S0) in the T2-60 design storm (31.9 mm in 1 h, PDISBA).

| Item | Absolute | % | Source |
|---|---|---|---|
| Area | 83.7 ha | — | `porta_canopy_cover.csv` |
| Canopy (CHM > 2 m, LiDAR 26 Sept 2021) | 16.8 ha | 20.1% | same |
| of which street trees | 11.7 ha | 13.9% | same |
| of which other (courtyards, parks, private) | 5.2 ha | 6.2% | same |
| Gap to the Pla director's 30% | 8.3 ha | 9.9 pts | same (target 0.3) |
| Street-tree positions | 2,825, 60 species | — | `porta_sidewalk_width.csv` |
| Planes | 832 | 29% of positions | same |
| Free spots | 153 free · 106 conditional · 8 blocked | — | §9d |
| Canopy added by planting the 152 free spots (optimised) | ≈ 0.33 ha | +0.40 pts, ≈ 4% of the gap | `additions_summary.csv` (crown discs, relative measure; 7-species run of 11 Nov) |
| Rain on Porta in the storm | ≈ 26,700 m³ | 100% | 31.9 mm × 83.7 ha |
| Runoff, total | 17,660 m³ | ≈ 66% of the rain | `additions_summary.csv` S0 |
| Runoff reaching flood hotspots | 2,682 m³ | 15% of runoff | same |
| Held by today's street-tree crowns | 794 m³ | 1.85% less runoff (`notes/methodology.md` §4b) | same |
| Flooded area, RESCCUE T10 today | 13.7 ha wet, 3.6 ha ≥ 15 cm | 16% of Porta | `resccue_porta_summary.csv` |

To compute in the tool thread: runoff to hotspots **per street segment** and litres held **per tree** (P3); the same sheet for the case-study areas (Av. Rio de Janeiro; one drawn area); the additions row with the 30-species palette and the new spot classes.
