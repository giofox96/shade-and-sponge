# Miro map proposal (RM homework 1, "Mapping the field")

Source of the brief: `seminars/research_and_methodologies/RM_L01_notes.md` (chapters 11–12, pp. 35–38). Content below is taken from the repo notes (`topic_decision.md` §7, `methodology.md`, RM_L01 notes); nothing new is claimed. Check cluster with the advisor first (probably cluster 3).

## What is asked
1. One map per thesis cluster on the shared Miro board (link from Laura). Every student's research must be identifiable (own colour).
2. Unpack the cluster topic from my research's point of view with the prompts Open / Follow / Question (p. 35) and the map elements (p. 37).
3. Add 2 theoretical + 3 practical state-of-the-art projects. Each card: source link · what it lets me understand about my question · what it does · what it does NOT do.
4. Be ready to tell the story of the 5 examples through the map. The next class opens with a review. Date to be confirmed by Laura.

## Rules for the drawing
- Start from the context, not the tool. Pick one unit and follow it everywhere.
- No hierarchy, no single reading order (rhizome). Several entry points.
- A map is a claim: every frame choice is a decision. Show absences and what does not survive translation.
- Every visual choice means something (colour = layer, size = importance, distance = dependency). Keep one legend.
- Cite the date and provenance of every data source on the map.

## Board layout (one frame, centre outwards)

**Centre: the unit.** One plane-tree position being replaced on a Porta street.
Sticky: *Deciding which species replace Barcelona's plane trees, and where, so that streets stay cooler in summer and hold back more rain in storms.* (topic without the tool)

**Ring 1, OPEN (no software named)**
- Promise: what does this decision promise designers, and who made the promise?
- Before computation: how are replacements chosen today (like-for-like)? Gained / lost.
- Who benefits: pedestrians, residents, city.

**Ring 2, FOLLOW (the unit travels through)**
| Stop | Content |
|---|---|
| Representation | tree → LiDAR crown → height / crown / LAI proxy → 1 m grid cell. Lost: LAI is an uncalibrated proxy |
| Data | ICGC LiDAR (26 Sept 2021, leaf-on), tree inventory, PDISBA storms, trait sources. Missing: who labels, which climates are absent |
| Models | interception bucket + SCS-CN, sun × elliptical crown shadow, D8 flow routing. Assumptions marked ASSUMPTION |
| Infrastructure | Python core `shade_sponge/` → Grasshopper/Ladybug and web app. Lock-in: Ladybug, Infrared City |
| Users | computational designer, municipal climate planner, urban hydrologist. What the tool adds to their work |

**Ring 3, QUESTION**
- Validation: how would I know it worked, who decides, which benchmark (Anys and Weiler 2024 for interception; Florence as transfer test)?
- Failure: young tree, storm beyond T = 10 yr; who notices?
- Limits: what the tool cannot do (e.g. no fluvial flood, one district, no carbon yet).
- Who else belongs: parks department, maintenance, residents, the trees.
- Report v0 honestly: "no trade-off within the city palette" is a finding with limits, not a proof.

**Outer band, p. 37 map elements** (one sticky each, linked to the ring they belong to): users · impacts · applications · by-products · monitoring · disciplines · serving infrastructure (data in / data out) · drivers · verification · knowledge.

**State-of-the-art strip (bottom), 5 cards**
| Type | Candidate | Doesn't do (my gap) |
|---|---|---|
| Theory | Shaamala et al. 2025 | tree placement optimised for heat only; water is future work |
| Theory | Mannucci et al. 2025 | coupled heat and runoff, no species traits |
| Practice | SylvCiT (Nicol et al. 2026) | runoff module disabled; no heat; Montreal only |
| Practice | Davey Tree Benefits Engine API | to fill in after reading the paper |
| Practice | GreenInCities Barcelona tools (heatwave risk index) | to check: species choice / placement not covered? |
Draw an arrow from each card to the ring it informs. Verify every "doesn't do" against the paper in `papers/` before writing it on the board; add the source link on each card.

## Steps
1. Confirm the cluster with the advisor (1 message).
2. Build frame, centre, three rings (30 min).
3. Add p. 37 elements and colour everything in my colour (20 min).
4. Fill the 5 cards (about 1 h, reading needed).
5. Rehearse the 5-example story (2 min).
Keep a text copy in `notes/actors_map.md` (shared with the RT actor map).
