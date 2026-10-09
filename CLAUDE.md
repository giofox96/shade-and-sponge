# CLAUDE.md: MaCAD Thesis (IAAC), Working Title: "Micro Bio Space"

## Language and working rules
- ALL output must be in English (code comments, docs, notes, slides, speech, thesis text).
- YAGNI: write only the minimum code needed, keep scripts light, avoid speculative abstractions, keep token use low.
- Follow the TUTOR'S ORDER OF WORK (see below): problem -> why -> research question -> hypothesis -> methodology (data, tools) -> tool. **Exception decided by the user (8 Oct):** tool prototyping starts now, in parallel with the methodology; the methodology stays a draft and the tool must follow it when it changes.
- Never invent citations, trait values, statistics, or datasets. If something is not in `papers/` or verified from a source, say so.
- Cite sources for every factual claim in literature notes (author, year, and the file name in `papers/`).
- Ask at most one clarifying question at a time.

## Folder structure (Windows)
Root: `C:\Users\giofo\Desktop\ARCHIVIO\MASTERS\MACAD\2_MACAD\THESIS_MACAD\`
Project (launch Claude Code here): `...\THESIS_MACAD\1_THESIS_PROJECT\`
- `CLAUDE.md`: this file
- `papers/`: PDFs of papers (managed in Zotero; Better BibTeX for export)
- `databases/`: datasets and data-source inventories
- Create only when needed (YAGNI): `notes/` (literature notes), `slides/`, `scripts/`
- Literature workflow: `/lit-review` skill (`.claude/skills/lit-review/SKILL.md`) runs `scripts/search_papers.py` → `fetch_pdfs.py` → `digest_pdfs.py`. Outputs live in `notes/lit/` (`shortlist.csv`, `literature_matrix.csv`, `to_get_manually.md`). Synthesis is in `notes/topic_decision.md`
- Seminars (8 Oct): `seminars/research_and_technologies/` (RT) and `seminars/research_and_methodologies/` (RM), gitignored. Files are named `RM_L03.mp4` → `RM_L03.txt` (transcript) → `RM_L03_notes.md` (chapters), with slides as `RM_L03_slides.pdf` and homework as `RM_HW01_brief/draft/final`. The `/transcribe-lecture` skill runs Whisper on the GPU (conda env `whisper`) and writes the chapter notes.
- **Decided by the user (7 Oct):** city = **Barcelona only** for now (the user has worked on Barcelona projects; strong open data). Scope = **both themes, heat (UTCI) + pluvial runoff, before 20 Oct**: trait-based street-tree selection and placement in one Barcelona district that is both a heat and a pluvial-flood hotspot. Basis: `notes/topic_decision.md` §6, `notes/city_screening.md`. Species coverage: `scripts/species_coverage.py` -> `databases/barcelona/species_coverage.csv`
- Git: private repo https://github.com/giofox96/shade-and-sponge (branch `main`). `.gitignore` excludes secrets, `papers/` and derived full text, and large raw downloads. CI: `.github/workflows/ci.yml` runs ruff (errors only) + `tests/` (data-free core tests) on every push that touches Python or `requirements.txt`
- **Commit policy (user, 8 Oct): every session commits and pushes on its own, without asking,** when a unit of work is done (a script runs, a note or section is complete, a figure is regenerated) and before it ends with changed files. Work on a `claude/*` branch, never `main` (on `main`, first create `claude/<topic>`). Stage only the files this session changed (`git add <paths>`, never `-A` or `.`: parallel sessions share the working tree). If `shade_sponge/` changed, run `python -m pytest -q -p no:cacheprovider tests` first. Run `fact-checker` first when the diff adds factual claims, numbers or citations. Then `git push -u origin <branch>`; if CI fails, fix it in the next commit. PRs and merges into `main` stay with the user (`/agent-task` still opens its own PR)
- Zotero: read-only MCP server `mcp-zotero` configured in `.mcp.json`. The key and user ID come from Windows user environment variables `ZOTERO_API_KEY` / `ZOTERO_USER_ID`. Never write them into files. Works locally only (it starts via Windows `cmd`)

## Agent workflow (set up 7 Oct; guide: `notes/agent_workflow.md`)
- **Methodology status: PROTOTYPING (user, 8 Oct).** The methodology is a draft (`notes/methodology.md`), but tool code is allowed on `claude/*` branches: core package `shade_sponge/` (see "Tool"). Every parameter in tool code is either sourced (cite it) or marked `ASSUMPTION`. Change this line to `DEFINED` once the methodology is final.
- Task board = GitHub Issues. `agent-ready` = an agent can do it alone; `needs-user` = waits for the user; `in-progress` = claimed. One issue → one `claude/*` branch → one PR. Agents never push to `main`; the user reviews and merges.
- Runner: `/agent-task` skill. Subagents in `.claude/agents/`: `lit-scout`, `data-scout`, `method-critic`, `fact-checker` (run it before committing any diff with new claims, numbers or citations; see Commit policy).
- Cloud sessions have no `papers/`, no Zotero and no Rhino; Python deps come from `.claude/hooks/session-start.sh` (`requirements.txt`).

## Tool (prototyping since 8 Oct)
- **Idea:** suggest tree species and positions for a site from its topography, climate and existing trees, to improve ecosystem services. Built site-agnostic (a data adapter per site), but **validated only for heat (UTCI) + runoff in Porta**; Florence = transfer test. More services (carbon, biodiversity) = later modules.
- **One core, two front-ends:** Python package `shade_sponge/` → (1) Grasshopper (primary user: computational designer; file exchange via `exchange/`, later Hops) with Ladybug for full UTCI; (2) web app for non-technical users (Streamlit or similar, last 2–3 weeks), using the fast heat proxy.
- **Core modules:** site bundle (grid, surfaces, DTM, buildings, trees) · topography (D8 flow routing → water convergence, positions upstream of flood hotspots) · heat proxy (sun exposure × elliptical crown shadow, opacity from LAI and leaf-on month; summer shade = benefit, winter shade = cost) · leaf-on calendar + storm months (`season.py`) · runoff (v1 model) · species palette + constraints · layout optimiser (weighted-sum sweep first, NSGA-II later). Run: `python -m shade_sponge` (details in `shade_sponge/README.md`).
- **Web app (9 Oct, `web/`):** Vue 3 + Vite, MapLibre + deck.gl (3D crowns, buildings, overlays), ECharts; static, data from `python -m shade_sponge.web_export` → `web/public/data/<site>/`. Read-only first (precomputed layouts), then live in-browser optimisation (HiGHS WebAssembly), a palette switch (city 6 / Barcelona shortlist 34) and a designer "Add trees" mode. Online: https://giofox96.github.io/shade-and-sponge/. Details: `web/README.md`.

## Who and what
- User: MaCAD student (Master in Advanced Computation for Architecture & Design, IAAC) developing the thesis.
- The thesis is judged mainly on the computational workflow or design tool and its validation. Frame it as "a computational method for X", not "research on X". The user really wants to develop a tool, but only after the methodology is defined.
- Tentative stack: Python (GeoPandas, scikit-learn, scipy), Grasshopper for design integration, SVG for Google Slides, booklet chapters in Markdown/LaTeX.
- Literature in Zotero; abstracts can be exported to CSV for AI screening and trait/metric extraction.

## Timeline (today is 7 Oct 2026)
- **Final delivery:** third week of December 2026, probably **18 Dec 2026** (not yet confirmed).
- **Tutor sessions:** 7 in total. First one done (6 Oct). **Next: 20 Oct 2026.**
- ~13 days to the next session, ~10 weeks to final delivery.

## Tutor's requirements (from first meeting)
Thesis structure the tutor wants: **1) Purpose, 2) Background (really know the field), 3) Contribution to knowledge.** The thesis must be **super specific**: narrow the topic. Describe a problem, understand it, explain WHY we want to solve it, and only then HOW.

**Deliverables for the 20 Oct meeting:**
1. The problem, defined as well as possible
2. The research question, defined very well
3. The hypothesis
4. Then methodology: define data and tools
5. A **literature review with infographics**
6. A **5-minute speech based on slides**

The user also wants to start the **data search as early as possible** (data availability will drive which option is feasible).

## Current draft (user's earlier wording; to be sharpened, not final)
**Problem statement:** Extreme rainfall in Bologna and Florence highlights the limits of traditional drainage. While urban greening is increasingly used for climate adaptation, current landscape workflows rely on generic, aesthetic planting rather than data-driven frameworks that quantify eco-hydrological traits (such as canopy interception and root permeability) needed to mitigate pluvial flooding.

**Research question:** Can a multi-criteria computational framework, scoring plant species based on eco-hydrological functional traits and localized climate data, enable landscape designers to optimize vegetation placement and measurably reduce surface runoff in flood-vulnerable urban zones?

**Hypothesis:** Yes. Integrating an eco-hydrological trait scoring system into design workflows significantly reduces surface runoff compared to standard planting approaches. This occurs because stormwater retention depends on specific plant traits (e.g., high canopy interception capacity, deep root architecture) rather than sheer biomass. Algorithmically matching these functional traits with localized spatial vulnerabilities maximizes soil infiltration and attenuates peak discharge during extreme precipitation.

### Known weaknesses to fix (flagged in discussion; tutor wants specificity)
- **Too many claims in one sentence.** Separate: (a) which problem, (b) which gap in practice or knowledge, (c) which contribution.
- **Flood type must match the evidence.** Verify whether the recent Bologna/Emilia-Romagna and Florence/Tuscany events were pluvial, fluvial, or mixed. Vegetation is relevant to pluvial runoff and frequent rainfall, much less to river-flood peaks or extreme events on saturated soil. The problem statement must name the flood type it addresses.
- **"Significantly reduces ... compared to standard planting"** is not testable as written. Needs: a defined baseline, a metric (runoff volume, peak flow, infiltration), a scale (site, street, small catchment), a design storm (return period from local rainfall data), and a threshold or comparison method. "Extreme precipitation" should be replaced by a specific design storm.
- **Claim about traits vs biomass** ("not sheer biomass") must be backed by literature, or reframed as something the thesis tests.
- **Scope:** "Bologna and/or Florence" is still broad. Narrow to one city, one scale, and one site or small catchment once data is checked.
- "Landscape designers" as the user is vague; pick one primary user (see personas).

## Open decisions
- **Site/scale (decided 8 Oct): Porta (Nou Barris, Barcelona), 0.84 km².** Both hazards above the city 60th percentile; first among eligible neighbourhoods at the 50/60/70th percentiles. Justification: `notes/site_selection.md` (scripts `bcn_site_screening.py` → `bcn_heat_check.py` → `bcn_site_select.py`). Sant Antoni = flood-dominant contrast site; **Florence (then possibly Bologna) = later transfer/test case**. Current PS/RQ/H: `notes/topic_decision.md` §7 (v4)
- **Methodology draft (not yet defined, user 7 Oct):** `notes/methodology.md` (runoff module, Ladybug Tier 1/Tier 2 heat module, NSGA-II, scenarios S0–S4, plan to 18 Dec).
- **Python ↔ Grasshopper exchange:** `exchange/README.md` (local origin 430800, 4586800 in EPSG:25831; `to_gh/` from Claude, `from_gh/` from the user; GH Python read/write snippets). The user runs Ladybug; Claude never opens Rhino.
- **Heat engine:** Infrared City (tutor is a co-founder; access to confirm), fallback/cross-check Ladybug Tools. Open questions in `notes/topic_decision.md` §6.4.
- **LiDAR + traits (8 Oct):** `scripts/bcn_lidar_porta.py` (ICGC LiDAR flown 26 Sept 2021, leaf-on → per-tree height/crown/LAI proxy, buildings) and `scripts/build_trait_table.py` (`databases/traits/porta_trait_table.csv`). Details in `databases/data_inventory_barcelona.md` §G–H.
- **Runoff module v1 (8 Oct):** `scripts/runoff_model.py` (1 m grid, PDISBA storms, bucket interception s·LAI + SCS-CN; scenarios S0, no street trees, planes→candidate species mature/young) with s = 1.75 mm/LAI calibrated in `scripts/calibrate_interception.py` on Anys & Weiler (2024). Results `databases/barcelona/runoff_scenarios.csv`, figure `notes/figures/runoff_results_v1.png`, methodology §4b.
- **20 Oct talk (draft 8 Oct):** `slides/outline_20oct.md` (9 slides, ~660-word script); infographics `slides/fig/` (SVG + PNG) from `scripts/make_infographics.py`. User-side tasks: `notes/todo_manual.md`.
- **Python env:** conda env `shade-and-sponge` (geopandas, matplotlib, requests) at `~/miniconda3/envs/shade-and-sponge`; put `<env>/Library/bin` on PATH when running GIS scripts.
- **Focus:** A→B narrowed, dual objective (UTCI + runoff), decided 7 Oct. Option C's heat element is now in scope; diversity stays a constraint only.

| Option | Core idea | Strength | Risk |
|---|---|---|---|
| A. Trait-based species recommender for stormwater | Extend SylvCiT logic with eco-hydrological traits and a new functional clustering | Clear gap, strong ML component | Sparse trait data for root architecture and interception |
| B. Site-level planting optimisation in Grasshopper | Given terrain, soil, sealed surfaces, place and select vegetation to minimise runoff | Very MaCAD-fitting, visual | Needs a credible runoff model coupled to geometry |
| C. Diversity vs. hydrology trade-off tool | Multi-objective: functional diversity + runoff + heat | Original | Larger scope, harder to validate |
| D. Green-grey infrastructure screening | City-scale GIS to find where interventions help most | Useful for planners | Less design-oriented |

Working idea: A feeding into B (trait-based selection, then spatial application at a real site). Not final.

**Scoring criteria (1 to 5 each):** data availability (Italy) | validation (measurable result, even simulated) | computational depth | scope vs. the 18 Dec deadline | personal interest and portfolio value.

## SylvCiT (main reference framework)
Nicol et al., PLoS One 21(2): e0339173, 2026. File: `papers/SylvCiT_-_An_AI-based_support_to_urban_forest_resi.pdf`
- Content-based filtering recommender; open source (GPL-v3); Montreal only; stack Django, React, Solr, MapBox, Docker.
- 10 functional groups (1A, 1B, 2A, 2B, 2C, 3A, 3B, 4A, 4B, 5) from hierarchical clustering on 7 traits: seed size, specific leaf area, leaf nitrogen, wood density, shade tolerance, drought tolerance, flood tolerance. Data from 3TF (integrates TRY).
- Candidate species are pre-filtered with the 10-20-30 rule; invasive and pest-affected species excluded.
- Score = sum of w_i * x_i over 5 indices: functional group diversity and richness (weights fixed at 10), species diversity and richness, carbon storage (user weights 1 to 10). x_i = n1/n0 - 1 using effective number of species (exponential of Shannon).
- Carbon via Lambert et al. Canadian allometry, Li et al. root biomass, x0.8 open-grown factor, x0.5 carbon fraction; new trees assume fixed DBH 15 cm.
- **Stated limitations:** no heat-island mitigation and no stormwater runoff reduction yet (runoff slider disabled, "under development"); Montreal only; functional groups must be redefined for other regions; no local genetic adaptation; fixed DBH for new trees.
- Results are diversity-index gains (mean +8.5% functional diversity in 10 parks), NOT hydrological outcomes.

**Implications:** (1) our work would extend a module the authors flag as missing, a defensible gap; (2) SylvCiT's 7 traits are resilience/diversity traits, not eco-hydrological, so a new trait set and clustering are needed; (3) hydrological validation requires coupling a runoff model (SCS-CN, Rational, SWMM, i-Tree Hydro-like); (4) allometry would need Mediterranean replacements if carbon stays in the score.

## Personas (Assignment 1 canvas)
- Computational designer: wants data-driven eco-hydrological trait calculation inside CAD/Grasshopper workflows.
- Municipal climate planner: needs quantifiable runoff reduction to justify green budgets vs. grey infrastructure.
- Urban hydrologist: needs reliable interception volumes to integrate green infrastructure into emergency/civil protection plans.

## Knowledge-gathering plan (five buckets)
1. Eco-hydrological traits: interception, infiltration, evapotranspiration, with quantitative evidence (make-or-break bucket).
2. Runoff modelling methods feasible in Python or Grasshopper (SCS-CN, Rational, SWMM, i-Tree Hydro).
3. Recommender and multi-criteria methods (MCDA, multi-objective optimisation, functional diversity indices).
4. Case context: recent floods in Emilia-Romagna and Tuscany (flood type!), pluvial flood maps, municipal open data.
5. Computational design precedents: sponge-city projects, green infrastructure tools, Grasshopper hydrology/vegetation plugins.

## Data feasibility checklist (do early; fill per city: Bologna, Florence)
For each item record: available? source/URL, format, licence, resolution, date, coverage, usable for?
- Tree inventory (species, DBH/height, location)
- Soil and permeability / hydrological soil group
- DTM / DSM (resolution)
- Land cover, impervious surfaces, building footprints (OSM via OSMnx as fallback)
- Rainfall: IDF curves, historical events, regional rain gauge data
- Flood hazard and pluvial flood maps, past event extents
- Plant trait databases: TRY, 3TF, BROT 2 (Mediterranean); gaps for root architecture and interception
- Local plant constraints: pests and pathogens (red palm weevil, Xylella), native/invasive lists
Store findings as a table in `databases/data_inventory.md` (or CSV).
**Barcelona (current city):** `databases/data_inventory_barcelona.md` (heat + runoff items, constraints, gaps, site-selection logic).

## Papers already collected (in `papers/`)
SylvCiT; Davey Tree Benefits Engine API usage; systematic review of cooling effects; urban ecohydrological model (vegetation, urban climate and hydrology); computational modeling for climate; coupling hydrological and microclimate models (evapotranspiration); landscape design of urban green space under climate change (review); Design with Water; standardized reporting need; role of urban forests in mitigating UHI; OSMnx new methods; BROT 2 trait database (Tavsanoglu and Pausas 2018); urban forests and nutrient removal from stormwater; urban forest and ecosystem services (water, heat, pollution); urban forests and climate change (Brasanac-Bosanac et al.); role and value of urban forests; Urban Forests CCRC.

## Immediate plan to the 20 Oct meeting
1. Literature review: screen the papers and extract, per paper: problem, method, traits/metrics, quantified results, limits. Focus first on bucket 1 and 2.
2. Data feasibility scan for Bologna and Florence (checklist above).
3. Sharpen problem -> why -> research question -> hypothesis (fix the weaknesses listed above).
4. Build literature-review infographics (SVG, Google Slides compatible) and a 5-minute slide-based speech.
5. Draft methodology outline (data + tools) only after steps 1 to 3.

## Open questions for the user
- Is Grasshopper integration a hard requirement of the programme?
- Slide format and language constraints for the 5-minute talk (Google Slides assumed)?
