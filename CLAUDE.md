# CLAUDE.md: MaCAD Thesis (IAAC), Working Title: "Micro Bio Space"

## Language and working rules
- ALL output must be in English (code comments, docs, notes, slides, speech, thesis text).
- YAGNI: write only the minimum code needed, keep scripts light, avoid speculative abstractions, keep token use low.
- Follow the TUTOR'S ORDER OF WORK (see below): problem -> why -> research question -> hypothesis -> methodology (data, tools) -> tool. Do NOT jump ahead to building the tool until the user says the methodology is defined.
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
- **Decided by the user (7 Oct):** city = **Barcelona only** for now (the user has worked on Barcelona projects; strong open data). Scope = **both themes, heat (UTCI) + pluvial runoff, before 20 Oct**: trait-based street-tree selection and placement in one Barcelona district that is both a heat and a pluvial-flood hotspot. Basis: `notes/topic_decision.md` §6, `notes/city_screening.md`. Species coverage: `scripts/species_coverage.py` -> `databases/barcelona/species_coverage.csv`
- Git: private repo https://github.com/giofox96/shade-and-sponge (branch `main`). `.gitignore` excludes secrets, `papers/` and derived full text, and large raw downloads. Commit and push only when the user asks
- Zotero: read-only MCP server `mcp-zotero` configured in `.mcp.json`. The key and user ID come from Windows user environment variables `ZOTERO_API_KEY` / `ZOTERO_USER_ID`. Never write them into files

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
- **Methodology draft:** `notes/methodology.md` (runoff module, Ladybug Tier 1/Tier 2 heat module, NSGA-II, scenarios S0–S4, plan to 18 Dec).
- **Python ↔ Grasshopper exchange:** `exchange/README.md` (local origin 430800, 4586800 in EPSG:25831; `to_gh/` from Claude, `from_gh/` from the user; GH Python read/write snippets). The user runs Ladybug; Claude never opens Rhino.
- **Heat engine:** Infrared City (tutor is a co-founder; access to confirm), fallback/cross-check Ladybug Tools. Open questions in `notes/topic_decision.md` §6.4.
- **LiDAR + traits (8 Oct):** `scripts/bcn_lidar_porta.py` (ICGC LiDAR flown 26 Sept 2021, leaf-on → per-tree height/crown/LAI proxy, buildings) and `scripts/build_trait_table.py` (`databases/traits/porta_trait_table.csv`). Details in `databases/data_inventory_barcelona.md` §G–H.
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
