# Shade & Sponge: Pecha Kucha pitch (RT final assignment)

Google Slides version (built through the connector): https://docs.google.com/presentation/d/1O8O2D067r3mQlhJclCj3zMWG--tIN833bFw879TQBUw/edit

Format: 15 slides x 20 s = 5:00. About 45 spoken words per slide (~135 wpm), ~680 words.
Brief points (RT L05, 01:31-01:36): topic and context · innovation · actors · exploitation · impacts (time frames, dimensions; reuse Assignment 2 Theory of Change) · TRL by end of thesis.
Lecture rules applied: one slide = one idea, little background, state of the art shown as its gap, clear thesis statement early, strong close.
Numbers come from the Theory of Change (RT A2) and the 10 Nov deck. Press figures are marked as press.

---

### 1. Hook (topic)
**On slide:** photo of a plane-tree street in Porta. "Which tree goes back?"
**Say:** "Barcelona is about to replace thousands of plane trees. Every one of them leaves a gap in the shade of a street, and in the way that street holds back rain. My research asks a simple question: which tree should go back, and where?"

### 2. Context: the decision is taken
**On slide:** 43,722 planes, 27% of street trees -> 12% (press, 2026) · no species above 15% (Tree Master Plan 2017-2037) · 30% canopy target
**Say:** "The city has decided. Planes are a quarter of its street trees, and the plan says no species above fifteen percent. So more than half will be replaced over the next decade, one tree at a time, when a tree dies or a street is rebuilt."

### 3. Context: heat and flooding overlap
**On slide:** city map of heat + pluvial hotspots; Porta highlighted. Porta canopy 20.1% vs 30% target.
**Say:** "And these streets face two hazards at once: summer heat and pluvial flooding. I work in Porta, in Nou Barris, where both are above the city average. Its canopy is twenty percent against a thirty percent target, and almost a third of it is plane trees."

### 4. The gap (thesis statement)
**On slide (large):** "The city fixes how many of each species. Nobody decides which species where, and nobody measures what it does to heat or runoff."
**Say:** "Here is the gap. The master plan fixes quotas, how many of each species. It does not say which species goes where. And no rule, no city tool, measures what a choice does to shade or runoff. Thousands of small decisions, unmeasured."

### 5. Why it matters
**On slide:** crown figure: same trunk, very different crowns (v6_04_crowns)
**Say:** "Why does it matter? At the same trunk size, the allowed species carry very different crowns. Some are close to a plane, others carry a quarter of the leaves. All of them follow the rules. The shade and rain interception left on the street can differ three to fourfold."

### 6. State of the art = its gap
**On slide:** three boxes: heat tools (no species) · runoff tools (no species, no heat) · species recommenders (SylvCiT 2026: runoff switched off). Empty box in the middle: "both services, per tree, inside city rules".
**Say:** "Research tools exist, but each covers one piece. Heat optimisers ignore runoff. Runoff models ignore species. The most advanced species recommender, SylvCiT, has its runoff module switched off. Nobody chooses species and positions for heat and runoff together, under a city's own rules."

### 7. Research question
**On slide:** "Can a trait-based layout method, inside Barcelona's tree rules, choose replacement species and new spots that keep more pedestrian cooling and storm-water interception than the city's own practice?"
**Say:** "So my question: can a trait-based method, working inside Barcelona's own rules, choose replacements and new spots that keep more cooling and hold back more rain than what the city actually plants? The baseline is not 'no trees'. It is the city's real replacement mix."

### 8. Innovation: the tool
**On slide:** flow: open data (inventory, LiDAR crowns, terrain, storm, weather) -> Shade & Sponge -> species + position per tree, scored on shade/UTCI and runoff. Web app screenshot.
**Say:** "The innovation is Shade and Sponge. It reads open data: the tree inventory, LiDAR crowns, terrain, a design storm and a hot day. For every tree to replace, it proposes a species and scores it on shade and runoff together. Every constraint is a real city rule."

### 9. Innovation: rules inside, not after
**On slide:** palette of 30 species (res_07_palette30) · 15% cap · sidewalk width -> tree size · city mix as baseline
**Say:** "Three things make it new. The city's rules are inside the optimiser, not checked afterwards: the fifteen percent cap, sidewalk width, a palette of thirty allowed species. It compares against the city's real practice. And it is site-agnostic: one data adapter per city."

### 10. First evidence
**On slide:** res_04_city_map: 28 neighbourhoods under the city-wide 15% cap, tool beats the city mix in 27, median +9.2 pts summer shade · UTCI check in Ladybug: pedestrian heat unchanged vs today's planes (within 0.2 C)
**Say:** "First evidence. I ran it on twenty-eight neighbourhoods under the city-wide cap. In twenty-seven it keeps more summer shade than the city's own mix, by a median of nine points. A Ladybug check shows pedestrian heat stays as with today's planes. Gains: runoff, diversity, winter sun."

### 11. Actors
**On slide:** actor map. Decide: Parcs i Jardins / Ajuntament. Use: landscape architects, computational designers. Data and test: BCASA (drainage), ICGC (LiDAR), Infrared City (heat engine, in discussion), Comune di Firenze (LiDAR for the transfer). Benefit: residents and pedestrians.
**Say:** "Who is involved? The city's parks department decides. Designers use the tool. Data comes from the Catalan mapping institute, the city and its water-cycle company. I test the heat side with Ladybug and am in contact with Infrared City. Florence's municipality has offered LiDAR for a transfer test."

### 12. Exploitation: what, how, for whom
**On slide:** table: open method (thesis, paper) -> researchers · Python core + web app, open source -> designers, other cities · per-tree trait and crown dataset -> city, researchers · transfer guide -> cities replacing monocultures
**Say:** "What can be exploited? The method, through the thesis and a paper. The code and a public web app, open source, for designers and cities. A per-tree dataset of crowns and traits. And a transfer guide for any city that has to replace a monoculture."

### 13. Impact over time
**On slide:** short term (now): reproducible method, simulated gains across 28 neighbourhoods · medium term: pilot streets with Parcs i Jardins, transfer to Florence and Mataró · long term: canopy toward 30% by 2037, no species above 15%, less runoff in flood hotspots
**Say:** "Impact over time. Short term: an open, reproducible method with simulated gains across the city. Medium term: pilot streets with the parks department, and a transfer test in Florence and Mataro. Long term: canopy moving toward thirty percent, no species above fifteen, less runoff where streets flood."

### 14. Impact dimensions + TRL
**On slide:** dimensions: environmental · social (comfort kept during replacement) · technological (open tool) · economic (avoided drainage and heat costs) · policy (makes the master plan spatial). TRL bar: today 3-4 -> end of thesis 4 (validated in simulation on real city data) -> 5 needs a real user test -> 6+ = pilot street.
**Say:** "It touches five dimensions, from comfort to policy: it turns a quota plan into a spatial one. By December I expect TRL four: validated in simulation, on real city data. A test with a real designer would bring it to five. A pilot street is the step after the thesis."

### 15. Close
**On slide:** "Replace trees with the least loss, inside the city's rules." + web app link + QR.
**Say:** "The city will replace these trees anyway. My point is to do it with the least loss of shade and the most rain held back, inside its own rules. The gains are small per tree, but multiplied by thousands of trees. Thank you."

---
Words: see count below. Fact notes: slide 10 uses the figure's own numbers (res_04_city_map: 28 barris, city LP with 15% cap, +9.2 median vs city mix, 27/28, PR #82). The 33-barri comparison vs the real replacement mix (+7.2, PR #80) is an alternative if a figure for it is made. "Three to fourfold" and "within 0.2 C" come from the 10 Nov deck and the Theory of Change.
