# RM cluster 3: speech, backup answers, paper cheat sheet (29 Oct 2026)

Map: "Cluster 03 - Data-driven decision making" (Elena's layout, final version agreed by the three of us). Speech focuses on Giovanni's line. About 2.5 minutes at a calm pace.

---

## 1. The speech

> Our cluster is about data-driven decisions in public space. The three theses are very different on the surface: Elena works on how neurodivergent people perceive a place, David on native plants and water for walking comfort in Colombia, and I work on street trees in Barcelona. So we did not look for a shared topic. We looked for a shared **structure**, and the map follows it: six stations, grouped in three questions. Who is in the model, what the place does to them, and how the decision is made and checked. Each line is one of us travelling through the same stations.
>
> My line follows **one plane tree in a street in Porta**, a neighbourhood in Barcelona.
>
> **Station one, the coarse rule.** Barcelona is replacing many of its plane trees. When it chooses the new species, the only documented rule is a qualitative table from 2004/2005 that picks species by district and sidewalk width. It says nothing about heat or about rainwater. Every street of the same type gets the same answer, the way a demographic label gives every person the same answer in Elena's work.
>
> **Station two, instead.** I score each tree position on its own: its own crown size and leaf area, measured from LiDAR, not a species average.
>
> **Station three, the proxy.** I predict before anything is planted. For heat I use a fast shade and leaf-area proxy, checked against Ladybug UTCI, the same comfort index David uses. For water I model runoff from a two-year design storm. This is simulated, not measured, and I say so.
>
> **Station four, the ground truth.** My interception model is calibrated on rain actually measured under urban trees, from Anys and Weiler in Freiburg. For heat I have no measurements in Porta, so I rely on a published error between Ladybug and ENVI-met. That is the weakest point, and the question under the station, one season of field data, is exactly my case.
>
> **Station five, the baseline.** The tool is only useful if it beats what the city would do anyway. So my baseline is the city's own rule-following replacement, plus today's trees.
>
> **Station six, the tool.** A Grasshopper plug-in for designers, and a web app for people who are not technical.
>
> At the bottom are our core papers. They connect to the three questions, and you can see that the literature does not overlap much: the shared ground is in the method, not the topic.
>
> The open question we keep for discussion is station five: **what if the simple rule wins?** For us that would be a result, not a failure.

---

## 2. If they ask "what did YOU do on this map?"

- **My line and my six slots:** I wrote what happens to one plane tree at each station, so my thesis can be compared station by station with Elena's and David's.
- **The shared structure:** before the map, I checked whether our literatures overlap. I put my literature and Elena's core papers into an embedding map (each paper's title and abstract as a vector, then UMAP). They sit in separate clusters, with no paper in between. That is why we built the map on a shared **method** (rule → individual → proxy → ground truth → baseline → tool) instead of a shared topic.
- **The common-points notes:** I wrote down the shared claim we started from: cities decide with averages, and each of us predicts for the single case and tests it against the rule.
- **Tags on my papers:** I tagged my five core papers by station group, and Yang is split between David and me.
- **The shared lines:** with David, the same UTCI index and greening inside existing constraints.

## 3. If they ask harder questions

- **"Why is UTCI an individual measure? It is for a standard person."** True. UTCI is computed for a reference person, so on the people side my thesis is closer to the average Elena criticises. My "individual" is the tree position, not the person.
- **"Where is your ground truth for heat?"** I have none in Porta. Heat is checked against a published Ladybug vs ENVI-met error (Mannucci et al. 2025: UTCI mean bias 0.8 to 2.3 °C). A difference smaller than that is not counted.
- **"What if the simple rule wins?"** Then the tool shows that the city's table is good enough for that street, and says so. That still answers the question.
- **"Who decides?"** The planner sets the weight between heat and runoff. The tool gives options, not one answer.

---

## 4. Paper cheat sheet (one line each)

### Mine (Giovanni)
- **Anys & Weiler 2024** (Hydrological Processes): measured rain interception under urban lime and maple trees in Freiburg; interception follows leaf area. My calibration: 1.75 mm of storage per unit of leaf area.
- **Peng et al. 2026** (Landscape Ecology): Grasshopper + Ladybug + NSGA-II to place trees for summer and winter UTCI on a small campus in Shanghai; adds a leaf-area correction to Ladybug's shade, checked against measurements under one tree. Generic tree types, no runoff.
- **Shaamala et al. 2025** (Cities): ant-colony optimisation of species and positions of 42 trees, UTCI in Ladybug, Queensland. Heat only; authors name multi-objective with water as future work.
- **Nicol et al. 2026, SylvCiT** (PLoS One): an open-source species recommender for Montreal based on functional traits and diversity. Its runoff module is disabled; no heat. My gap.
- **Mannucci et al. 2025** (City and Environment Interactions): heat (UTCI) and runoff in one Grasshopper workflow on a square in Ostia; no species traits, no optimiser. Source of the Ladybug vs ENVI-met error.

### David's
- **Buddika et al. 2022** (conference, CFD): where trees stand and the shape of their crown change how much wind ventilates a building; cuboid crowns close upstream cut ventilation most.
- **Mallya 2022** (Master's thesis, UTS Sydney): permaculture ideas to bring fine-grained green space close to homes in master-planned housing estates. (Only the abstract read.)
- **Yang, Lin & Li 2018** (Advances in Meteorology): ENVI-met calibrated with field measurements in a Singapore housing estate; shade trees over grass cool best; high-albedo paving and water bodies did not help in hot humid climate. Shared with me: shade trees and a field-checked model.
- **Arosemena Díaz & Mora 2026** (Geology, Ecology, and Landscapes): ENVI-met in three suburbs of Panama City; more lawn and taller street canyons lowered the heat index; tree cooling dropped in the hottest hours.
- **de Souza, Lee & Cook 2023** (IJERPH): low-cost greening of a hospital campus in Darwin with staff volunteers and Indigenous healers, to give patients and staff cool outdoor space.

### Elena's
- **Kenna 2022** (Area): calls for urban research on neurodiversity, because lived city experience of neurodivergent people is little studied.
- **Wang et al. 2025**: language models used in place of human participants misportray and flatten identity groups.
- **Park et al. 2026**: agents built from two-hour interviews predict 1,052 people's own answers; the individual, not the group.
- **Mushkani 2025**: a small benchmark of 100 Montreal street images; vision-language models agree with people more on visible things than on subjective impressions.
- **Mauro et al. 2022**: a place recommender for autistic people that combines preferences with sensory aversions; tested on 148 adults, 20 autistic.

Sources: `notes/core_papers_cards.md`, `notes/rm_cluster3_common_points.md`, `notes/lit/paper_map_extra.csv`, the five papers David shared (first pages only) and his ClimateLoop abstract (27 Oct).
