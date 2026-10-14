# Miro map proposal (RM homework 1, "Mapping the field")

Source of the brief: `seminars/research_and_methodologies/RM_L01_notes.md` (chapters 11–12, pp. 35–38). Template = slide p. 37 "Before you draw: open up your topic": a centre box (CLUSTER TOPIC) and 10 boxes in a loop. Content below comes from the repo notes (`topic_decision.md` §7, `methodology.md`); nothing new is claimed. Confirm the cluster with the advisor first (probably cluster 3).

## What is asked
1. One map per cluster on the shared Miro board (link from Laura). Each student's research must be identifiable (own colour).
2. Unpack the cluster topic from my point of view with Open / Follow / Question (p. 35) on the p. 37 template.
3. State of the art: 2 theoretical + 3 practical projects. Each card: source link · what it lets me understand about my question · what it does · what it does NOT do.
4. Be ready to tell the story of the 5 examples through the map. The next class opens with a review of the maps (date to be confirmed by Laura).

## Collaboration protocol (cluster colleagues share one map)
- Agree on **one** centre text for the cluster topic, then everyone works from their own point of view around it.
- One colour per person, used for every sticky and arrow. Initials on each sticky as a backup for colour-blind readers.
- Every box holds several stickies, one or more per person. A shared item = one sticky with a multi-colour border, not a merged consensus.
- Each person draws their "unit path" (Follow) as an arrow in their colour through the boxes. Where arrows overlap = shared ground; where they diverge = the interesting part.
- State-of-the-art cards go in one lane per person under the loop, so the 5 cards per person stay countable.
- Use Miro comments for questions to colleagues. Do the first pass alone, then 30 min together to link overlapping stickies.
- Agree who checks the legend and who prepares the first 2 minutes of the story, since the class opens with a review.

## Fill-in for the p. 37 template (my colour; one sticky per bullet)

**Centre, CLUSTER TOPIC:** cluster topic text (agreed with colleagues) + my sticky: *deciding which species replace Barcelona's plane trees, and where, so that streets stay cooler in summer and hold back more rain in storms* (Open: topic without the tool).
My unit to follow everywhere: one plane-tree position being replaced on a Porta street.

| Box | My content |
|---|---|
| Users | computational designer; municipal climate planner; urban hydrologist. What extra work the tool adds for them |
| Impacts | less summer heat stress (UTCI), less pluvial runoff in storms; cost: winter shade; trade-off size between the two |
| Applications | species and placement choice for tree replacement in Porta; transfer test in Florence |
| By-products | per-tree trait table, scenario results (S0–S4), layout options for designers. Gap to note: who stores and reuses them |
| Monitoring | how success would be tracked after planting. Currently a gap: write it as an open question |
| Disciplines | landscape design, urban hydrology, urban climatology, computational design, plant ecology |
| Serving infrastructure | Python core `shade_sponge/` → Grasshopper/Ladybug and web app. Lock-in: Ladybug, Infrared City |
| ↑ Data (in) | ICGC LiDAR (26 Sept 2021, leaf-on), tree inventory, PDISBA storms, trait sources, DTM, buildings. Add date and provenance on each |
| ↓ Data (out) | runoff and shade maps, ranked layouts, exchange files for Grasshopper |
| Drivers | heat and storm hazards in Porta (both above the city 60th percentile); verify the policy driver before writing it |
| Verification | interception calibration vs Anys and Weiler 2024; UTCI cross-check with Ladybug; Florence transfer test; who decides, against which benchmark |
| Knowledge | what it adds: joint species + placement for heat and runoff. What does not survive translation: LAI from LiDAR is an uncalibrated proxy |

Add three loose stickies from the Question prompts: failure cases (young tree; storm beyond T = 10 yr; who notices), limits (no fluvial flood, one district, no carbon yet), and who else belongs on the map (parks department, maintenance, residents). Report v0 honestly: "no trade-off within the city palette" is a finding with limits.

## State-of-the-art strip (5 cards, my lane)
| Type | Candidate | Doesn't do (my gap) |
|---|---|---|
| Theory | Shaamala et al. 2025 | placement + species optimised for heat (UTCI) only, species by morphology; authors name water sensitivity as a missing objective |
| Theory | Mannucci et al. 2025 | heat + runoff in Grasshopper, but scenario testing only: no species traits, no optimisation |
| Practice | SylvCiT (Nicol et al. 2026) | no heat-island or runoff service yet (authors' words); diversity and carbon only; Montreal |
| Practice | Davey Tree Benefits Engine API | per-tree i-Tree benefits (incl. avoided runoff) for a given species and DBH; no placement or species choice; paid; US averages outside supported areas |
| Practice | GreenInCities (EU 2024–27; Barcelona pilot in Besòs) | participatory greening with NDVI, heatwave risk index, non-human UTCI, co-monitoring; species or placement choice and runoff not described in the sources read |
Checked against the full texts (14 Oct); GreenInCities from RT L02 notes + greenincities.eu/tools. Add the source link on each card. Arrow from each card to the box it informs.

## Steps
1. Confirm the cluster with the advisor and message colleagues the protocol above.
2. Copy the p. 37 template into the cluster frame; pick colours (10 min).
3. Fill the loop alone (about 45 min), then draw my unit path.
4. Fill the 5 cards (about 1 h, reading needed).
5. 30 min with colleagues to link overlaps; rehearse the 5-example story (2 min).
Keep a text copy in `notes/actors_map.md` (shared with the RT actor map).
