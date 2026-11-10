# Tutor feedback, 10 Nov 2026 (A. Chronis): what was said, what it means, plan for the week

*Written 10 Nov, evening, from Giovanni's notes (no recording). Overall: the tutor was happy with the progress. His request for this week: **solidify the assumptions, explain them better, and soften the ones that are too bold.** He also said that nobody will question an assumption that is declared as one.*

Status marks: ✅ already true in the repo · 🟡 partly, or source read only through a web fetch · ⬜ to do.

## 1. The feedback, point by point

| # | What the tutor said (Giovanni's notes) | What is true today | Answer / action |
|---|---|---|---|
| F1 | "Polish" the data shown in the tool. The brown lines are unclear: sometimes there is no building where they run | ✅ The brown lines are **façade lines of the city's 1:1000 topographic base map** (Ajuntament de Barcelona, CC BY 4.0), the other line is the kerb, dark in the light theme (`web/src/components/MapView.vue`, layer `sidewalks`). In Porta the 3D buildings are **OpenStreetMap footprints** (ten other barris use footprints traced from the LiDAR building class, `notes/citywide_plan.md`). Two sources, so a façade line can run where there is no building. The side panel already says "Brown = façade, dark = kerb" and lists both sources under "Data and sources", but not on the map itself | ⬜ Draw the sidewalk as one filled band between façade and kerb instead of two loose lines, and move the two sources into the map legend. Tool thread |
| F2 | Doubt on the sidewalk width (data missing in OSM, or the calculation itself?) | ✅ Both readings have an answer in `notes/sidewalk_width.md`. **The width does not come from OSM.** It is the façade-to-kerb distance on the 1:1000 map, measured by a ray through each tree. OSM was tested on 26 Oct and rejected as the reference: 0 of 85,819 street ways carry a sidewalk-width tag; the best OSM proxy gets the size class right for 76% of trees. Quality check: 18 of 20 random trees measured as intended, 2 corner cases overestimated; 8% of the measured planes lie within 0.3 m of a class threshold. **Limit to declare:** only 1,545 of Porta's 2,825 trees are façade-bounded and measured; medians, boulevards and plaza edges get no size filter (`ASSUMPTION`) | ⬜ One backup slide "How the sidewalk width is measured" (map window with the ray, the 20-tree check, the share measured). ⬜ The ±0.3 m check on the ICGC orthophoto is still open (needs the OMEN) |
| F3 | The substrate: sewers, electricity, gas. Underground networks may decide where a tree can go | 🟡 Not modelled. `notes/sidewalk_width.md` already lists "underground services" among what makes the free spots an upper bound. Sewer data = BCASA request BDM9240 (pending; must stay out of the public repo). The datos.gob.es catalogue lists a WMS "Map of energy and telecommunications of the city of Barcelona" published by the city's open-data service (the Open Data BCN page itself was not opened); the record names no layers and its format, licence and URL fields are blank, so **whether it shows underground lines is unknown** | See A3 below. ⬜ Open that WMS from the OMEN (GetCapabilities) and record what it holds |
| F4 | "Too bold": in a project area every tree is assumed to be felled. Trees can be kept or transplanted. The life cycle of the trees is missing. "Solidify this: why replace, fully justify" | 🟡 Less bold than it sounded: the Python core replaces only the **planes** inside the drawn area (`shade_sponge/__main__.py`, `is_plane`); in the web app "Replace all" is a button that is off by default, and when it is on the app warns that "replacing young or healthy trees looks like a gain that takes years to arrive" (`web/src/App.vue`). But within the area the choice is still all planes or all trees, never tree by tree. The city's own rule points the other way, see A1 | See A1 below. This is the main item of the week |
| F5 | Show the ground in 3D (DTM or LiDAR); the DTM did not appear in the methodology | ✅ The DTM **is** in the method: surface water is routed on it (`shade_sponge/topo.py`, Priority-Flood routing, buildings as obstacles) to find the ground that drains to flood hotspots. It is not visible in the web app or in the method diagram | ⬜ Method diagram: add the DTM box. ⬜ Web app: terrain from the DTM (MapLibre terrain) with buildings and crowns on top; fallback if it costs too much: a hillshade plus the flow-path overlay. Tool thread |
| F6 | Runoff: s·LAI with s = 1.75. "Position has no effect on s, or on runoff" | ✅ He is right about s, and half right about runoff, see A2 | See A2 below |
| F7 | What does HiGHS actually do? | ✅ Written in `shade_sponge/layout.py` (`assign`, `sweep`), never explained in plain words | See §3 below. ⬜ One slide |
| F8 | From other students' sessions: Mapillary, Google Places API | Not used | Mapillary: street-level photos under CC BY-SA with an API that is free with a token (🟡 only the CC BY-SA licence is confirmed; price and terms to re-check before use); possible use = a visual check of sidewalks, tree pits and leaf state without a site visit. Google Places is paid beyond a free quota: **left out** (Giovanni, 10 Nov) |

Loose words in the notes ("what exactly building", "save the trees", "keep/cut", "set assumptions", "tighten up") fit F1 and F4: say exactly what the tool builds on, and make keep / cut an explicit choice.

## 2. Assumption register (v1)

Each row: what is assumed, why it is bold, how it is softened. "Declare" means it goes on the assumptions slide and in thesis ch. 5.

### A1. "Every tree in a project area is replaced" → the removed set becomes an input

- **Today:** the area the user draws decides which trees are replaced: all its planes, or all its street trees. Reading it as "a street project fells everything" is the bold part.
- **Evidence against the bold reading (🟡 read through a web fetch on 10 Nov; re-read the PDF on the OMEN before citing):** Parcs i Jardins, *Protecció d'elements vegetals, durant la realització d'obres* (Barcelona, January 2017, 2 pp., https://ajuntament.barcelona.cat/espaisverds/sites/default/files/2024-08/Proteccio-verd-obres.pdf). The note is about **protecting** vegetation during works: it refers to art. 73-3 of the Ordenances Generals del Medi Ambient Urbà, asks to avoid trenches within 1 m of a tree pit, to dig by hand within 1 m of the trunk, to fence trees, gives transplanting seasons "en cas que calgui realitzar trasplantaments o noves plantacions", and requires a deposit that guarantees the replacement of affected vegetation, valued with the Norma Granada. It states no keep → transplant → fell order and no criteria for when a tree may be felled.
- **The city's own criterion for replacing (already in the repo):** the priority order for replacing a plane or elm is (1) road-safety problems, (2) dead, (3) aesthetically unrecoverable or declining, (4) to unify a stretch where another species already dominates, (5) taking advantage of street works (`notes/tree_master_plan.md` §5, S §2.4.2; PG §3.4.2). Street works come **last**: a project is an occasion to replace a tree that already qualifies, not a reason to fell a healthy one. This is the sourced answer to "why replace".
- **Evidence that replacement happens anyway:** 10,976 observed species changes in the city inventory, 2018Q1–2026Q2, a floor (`notes/topic_decision.md` §11.1); the city's stated mechanism (press, 🟡) is gradual, planes go as they die and during street works (`notes/tree_master_plan.md`, N1, N5). The inventory does not say **why** each tree went.
- **Softened version (proposal):**
  1. **The tool does not decide which trees go.** The designer marks each tree in the area as *keep*, *transplant* or *replace*; the default is *keep*, and the tool can pre-mark the trees that meet the city's criteria above. The tool answers "given the trees that must go, what goes back, and where can trees be added". "Replace all" stays as one button, the worst case.
  2. A transplanted tree leaves its position (the position is replanted or freed); where it lands is outside the tool. `ASSUMPTION`, declared.
  3. **Why replace, justified with data (Giovanni's idea, 10 Nov):** find the street-works signature in the inventory, i.e. many trees of one street changing in the same quarter, and report for a handful of real projects how many trees were kept, how many changed species and how many disappeared. This turns "projects replace trees" from an assumption into a measured share. ⬜ Script on `databases/barcelona/inventory_replacements.csv`.
- **Life cycle (declare, do not solve):** layouts are compared with each species at the crown size it has in Porta today (median of its LiDAR-measured trees, `layout.py`), not at planting size. A felled mature tree is therefore compared with a mature replacement, which favours replacing. Softening: report the planting-year value next to the mature one (the runoff module has a young-tree scenario, `scripts/runoff_model.py`, and the web app a "≈ 10 years" check), and say that keeping a healthy tree always wins in the first years. Growth curves per species = future work.

### A2. Runoff: what position changes and what it does not

- **Not position-dependent (the tutor is right):** canopy storage is I = min(P, s·LAI) with one s = 1.75 mm per unit LAI for every species (calibrated on Anys & Weiler 2024, two species; for Barcelona's short intense storms it may be lower, `notes/methodology.md` §4b). A given tree intercepts the same depth wherever it stands.
- **Position-dependent, by construction of the model:** (1) what lies under the crown: a crown over a roof changes nothing, a crown over open ground does (`runoff.storage`); (2) whether that ground drains to a flood hotspot within 100 m along the flow path on the DTM (`site.CAPTURE_M`, `ASSUMPTION`, a stand-in for sewer inlets). The optimiser counts only that part (`layout.water_potential`).
- **How much it matters:** little. Every runoff difference between layouts is below 1%, under s = 1.75, 0.86 and 0.83 and under the allometric LAI (`notes/methodology.md` §4b). The thesis already calls runoff "not resolved" and uses it as a do-no-harm check (v8, H1).
- **Softened wording for the talk:** "Position does not change how much a tree intercepts. It changes whether the intercepted water would have reached a flood hotspot. In our results this effect is smaller than what the model resolves, so runoff is a check, not an objective."
- **LAI from LiDAR in one sentence:** the share of laser pulses that pass through a crown without hitting it (gap fraction) gives LAI = −ln(gap) / 0.5 (Beer–Lambert; Alonzo et al. 2015; Morsdorf et al. 2006). It is an effective LAI on the flight day, 26 Sept 2021.

### A3. Underground services

- **Assumed today:** nothing underground constrains planting.
- **Softening:** (1) for **replacement** the pit already exists, so the conflict with services was settled when the pit was built: the assumption only touches **added spots**; (2) added spots are already reported as an upper bound (232 in Porta, 209–243 under other clearances); say so next to every additions result; (3) if a network layer turns up (the open WMS, or BCASA sewers kept local), use it as one more exclusion buffer, as done for crossings and bus stops (`scripts/porta_spot_exclusions.py`). No clearance value is sourced yet: the 2017 note gives distances for trenches near trees, not for trees near pipes.

### A4. The other assumptions, at a glance

| Assumption | Value | Basis | Tested? | Softening |
|---|---|---|---|---|
| 15% species cap read locally | per study area | Plan: city-wide cap (`notes/tree_master_plan.md`) | City LP run exists (`notes/citywide_plan.md`) | Show both; say the local reading is stricter |
| Cap counts street trees only | — | User decision 26 Oct | No | Revisit before final results |
| Unmeasured positions get no size filter | 1,280 of 2,825 trees | No façade to measure from | Results can be split with / without | Report both |
| Crown clearance = crown radius ≤ distance to building, no margin | — | None | No | One variant with a margin |
| Hotspot capture distance | 100 m | None (stand-in for inlets) | Not found in the notes read tonight | Sensitivity 50 / 100 / 200 m, or drop when BCASA inlets arrive |
| Curve numbers | 98 sealed, 74 pervious | TR-55, HSG C assumed | Not found | Declare |
| Leafless crown opacity | 0.35 | McPherson 1984; Heisler 1982/84 | Range 0.25–0.54 stated | Keep range on the slide |
| Leafless canopy storage ratio | 0.5 | Herbst et al. 2008; Xiao et al. 2000 | Range 0.3–0.7 stated | Same |
| Design days | 15 Jul 12–17 h, 15 Jan 10–15 h | Window decided 25 Oct; days assumed | 21 Dec and 15 Feb variants run | Hot design day from the EPW (roadmap, 16–22 Nov) |
| Extinction coefficient K | 0.5 | Peng et al. 2026 | No; not tagged in `heat.py` | Tag and declare (`notes/methodology.md` §12.3) |
| Replacement-priority proxy | equal weights | None | Not validated | Keep out of the headline results |
| Spot clearances (crossings 3 m, bus stops 8 m) | — | 2011 guide for signals; rest assumed | Yes: 209–243 spots | Done |

⬜ Next pass: complete the "Tested?" column from `shade_sponge/README.md` and the decision notes, then turn the table into one slide and one thesis table (ch. 5).

## 3. What the optimiser (HiGHS) does, in plain words

1. **Before any optimisation**, the tool computes a score table: for each position and each palette species, how much summer shade that species would cast there on open ground, how much winter shade (a cost), and how much rain it would intercept over ground that drains to a hotspot.
2. **The decision:** one species for each position.
3. **The rules:** exactly one species per position; a species only where it fits (sidewalk size class, crown clear of the façade; where nothing fits the smallest crown goes in, and unmeasured positions have no size filter); no species above its cap (15%); optionally a minimum diversity.
4. **The goal:** the highest total score, where the score is a weighted sum of the three tables. The weights are the designer's priorities. The tool repeats the run for 15 weight combinations, re-scores each layout with the raster heat proxy and the runoff model (which do count crown overlaps), and keeps the layouts that no other layout beats on every objective (the Pareto set).
5. **HiGHS** is an open-source solver for this kind of problem (linear programming). Unlike a genetic algorithm it does not search by trial and error: for a given set of weights it returns **the** best layout, with a proof that no better one exists. (With the optional diversity floor the problem becomes mixed-integer and the diversity constraint is a conservative approximation; HiGHS solves that too.) The same solver runs inside the web page (compiled to WebAssembly), which is why the app can re-optimise live.
6. **What it is not:** it does not simulate heat or water. Its answer is only as good as the score table, which ignores overlaps between neighbouring crowns. That is why every layout is re-scored with the raster models inside the tool, and the final ones are checked outside it for UTCI (Ladybug / Infrared).

One-line version: *"It is an assignment problem, like seating guests at tables with rules. HiGHS finds the provably best seating for each set of priorities."*

## 4. Plan for the week (11–17 Nov)

This replaces the "Every tree" row of `notes/roadmap_nov_dec.md` for this week: the generalisation to any tree and the keep / transplant / replace input are the same code change.

| When | Work | Who | Check |
|---|---|---|---|
| Wed 11 | Giovanni reads this note (20 min) and corrects what the tutor meant. Re-read the 2017 protection note on the PDF | Giovanni + Claude (OMEN) | A1 quotes confirmed or corrected |
| Wed 11–Thu 12 | Street-works signature in the inventory: projects, trees kept / changed / gone (A1.3) | Claude, cloud | Table of ≥ 5 real projects with counts |
| Thu 12–Fri 13 | Tool: per-tree keep / transplant / replace, default keep; any species, not only planes | Tool thread | Tests pass; Porta plane results unchanged with "replace all" |
| Fri 13 | Tool polish: sidewalk band + legend sources (F1); DTM in the method diagram (F5) | Tool thread | Screenshot before / after |
| Sat 14–Mon 16 | Terrain in the web app (F5), time-boxed to one session; else hillshade | Tool thread | App loads Porta with relief |
| Mon 16 | Register v2 (full "Tested?" column), missing sensitivities (capture distance, clearance margin) | Claude, cloud | Each row: sourced, tested or declared |
| Tue 17 | Three slides for the next session: assumptions, how the optimiser works, why replace. Utilities WMS check | Claude + Giovanni | Deck section ready |

The heat week (UTCI of the final layouts) moves by a few days only if the terrain work overruns; it is time-boxed for that reason.
