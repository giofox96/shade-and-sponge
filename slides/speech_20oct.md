# What to say, 20 October 2026

Generated from `slides/outline_20oct.md` by `scripts/make_speech.py` — spoken text only. **1,542 words, 10:17** at 150 wpm for all 17 slides; **1,162 words, 7:45** if you drop the five marked *extra*. The time in brackets is where you should be when you finish that slide.

### 1. Title  ·  0:28

This is Porta, at the corner of Alcúdia and Maladeta, and those bare crowns are plane trees. Barcelona has to replace a large share of its street trees, because one species — the plane — is twenty-eight percent of the city stock, and twenty-nine percent in the neighbourhood I work in, while the tree plan caps every species at fifteen. My thesis is how to decide what goes back.

### 2. The thesis in one line  ·  0:54  ·  *extra, cut this first*

In one line: species times position, scored on heat and on runoff, and what I report is the trade-off between them. Three things it is not. It is not a flood model — the hotspots come from the city's map. It is not a city-wide plan. And it is not a ranking of species: the same tree is good or bad depending on where it stands.

### 3. The problem: two hazards, one street, one decision  ·  1:32

Two hazards arrive on the same streets. Barcelona's sealed surface went from forty-five to seventy-two percent between 1956 and 2009. About three storms a year exceed sixty millimetres an hour in their first twenty minutes, and the sewer is only sized for a ten-year storm — above that, the surface carries the water. In summer the city has one of the highest heat-island mortality burdens in Europe. And the decision is already taken: the plane trees are coming out. Nobody has to be convinced that something should be planted. The question is what, and where.

### 4. Why Porta  ·  2:14

I needed one neighbourhood where both hazards and the replacement problem are real at the same time. I screened all seventy-three with open data: to qualify, a neighbourhood had to be above the city's sixtieth percentile for flood hazard, for surface heat and for plane density, simultaneously. Porta comes first at every threshold I tried. On the equal-weight score across the whole city it is second, and it stays in the top three in just over half of two thousand random weightings. It has eight hundred and thirty-two plane trees. Sant Antoni floods more but its heat is average, so it becomes my contrast site.

### 5. What the review covers  ·  2:33  ·  *extra, cut this first*

The review is a hundred and thirty-five sources on topic, and a hundred and twenty-eight of them I have read in full rather than from the abstract. I will take two findings from the runoff side and two from the heat side, because those four decide the method.

### 6. Evidence: what a tree does for rain  ·  3:10

Two findings. First, species differ: a crown intercepts somewhere between four and seventy percent of rainfall across the field studies, and the main driver is leaf area — which is a measurable trait, not a preference. Second, the size of the prize is small and it has a boundary: a paired-catchment study measured four percent of runoff volume from street trees — three and a half in the calibrated re-analysis — and no effect at all on peak flow. So trees are a tool for frequent storms, not for extreme ones.

### 7. Evidence: what a tree does for heat, and what my model cannot see  ·  3:51  ·  *extra, cut this first*

On the heat side the honest version is two-sided. A crown works mostly through radiation — the sun-to-shade gap on a hot afternoon is between two and nearly five degrees of felt temperature, and that is a lower bound, and leaf area decides how much sun gets through. Transpiration cools the air more, but it needs water — and per leaf area it is lowest in Mediterranean climates, and separately about ten times lower for a tree in a paved pit than over grass. My engine ignores transpiration altogether. That is why the heat objective is a ranking of layouts, not a temperature forecast.

### 8. Same tree, two jobs  ·  4:22

Here is why one score is not enough. The two goals share their drivers — crown size and leaf area feed both shade and interception — so part of the benefit is free. But they pull apart on timing: leaf habit decides whether the crown is there for the August heat or for the October storm, and in winter the same crown becomes a cost, not a benefit. Shared drivers, different calendars. That is a multi-objective problem.

### 9. The gap  ·  4:56

The gap is narrow and I want to state it narrowly. The closest work either assesses heat and runoff for fixed planting scenarios, without species traits, or optimises species and positions for heat alone. The most advanced trait-based recommender, SylvCiT, has its runoff module written in the paper as disabled. Nobody chooses street-tree species *and* positions against pedestrian-level heat stress *and* event runoff together. That sentence is the gap, and every word in it is load-bearing; the contribution I would claim from it is the method.

### 10. The other gap: the data  ·  5:20  ·  *extra, cut this first*

There is a second gap, and it is in the data. For the city's own replacement species I can measure the crown on site from the laser scan. But canopy storage has been measured for one of them, and none has a measured cooling value. That gap is not a weakness of the thesis, it is one of its results.

### 11. The research question (v5)  ·  6:01

So, the question. In Porta, as the plane trees are replaced, which species and which positions jointly reduce pedestrian heat stress and event runoff volume for one-, two- and ten-year design storms — and how large is the trade-off, measured against three baselines: the trees that are there today, a like-for-like replacement, and each single-objective optimum. One thing I changed yesterday: I measure heat as an average over the afternoon, twelve to five, not at the single peak hour — at the peak even full shade is above the stress threshold, so the metric saturated and no layout could show a benefit.

### 12. Two hypotheses, and the one I took out  ·  6:54

Two hypotheses, and one I removed. One, synergy: at the same number and size of trees, a trait-based layout beats a like-for-like replacement on both goals. Two, trade-off: the heat optimum and the runoff optimum differ mainly in species, not in positions. I fixed a minimum meaningful difference before running anything — ninety-one cubic metres — and on today's exploratory numbers the best layout does not clear it, which I would report as not resolved. The third one I took out yesterday. It said the runoff benefit shrinks as storms grow, and the model cannot fail it: with a full crown at every storm that is arithmetic, not a test. So it is now a declared boundary of the method. My question to you is whether that is the right call.

### 13. The method  ·  7:32

The method has five steps. From the 2021 laser scan — flown in September, with the leaves on, which matters — I get every tree's height, crown and a leaf-area proxy. A Python module scores runoff for a design storm; a Ladybug module in Grasshopper scores felt temperature on a design afternoon. A genetic search then chooses the species at each of the eight hundred and thirty-two plane positions, under the city's fifteen-percent rule and a diversity floor. The output is a Pareto front, and then the same machine is pointed at a second site.

### 14. First result: the runoff module runs  ·  8:12

The runoff module already runs. I calibrated canopy storage on open field data — sixteen trees, fifty-one storms. Porta's street trees as they stand today cut runoff in a two-year storm by one point eight five percent, or about three percent counting open ground only, everything but the roofs. That is the same order as the three and a half to four percent measured in the field, which is the check I wanted. Replace the mature planes with young trees and more than a third of that benefit disappears during the transition. That number is for the city, not for me.

### 15. First result: shade, and a real trade-off  ·  8:53  ·  *extra, cut this first*

The first version of the optimiser also runs, on the shade side. Against a random palette, an optimised one gives sixteen percent more summer shade, and that holds across eight sensitivity variants — but it buys no winter sun at all: about equal, or slightly worse. Push it further and the trade-off becomes real: you buy winter sun with summer shade, one for one in the base run and two-thirds to one across the variants. And this is with mature replacement crowns — even then, no layout reaches the planes that are standing today. That is the honest shape of the problem.

### 16. Transferability: the code travels, the evidence does not  ·  9:42

Last piece: how far this travels. The code is site-agnostic by construction — the routing, the shadow geometry and the runoff kernel carry no local constant. What does not travel is the evidence, and in particular one input: a laser scan taken with the leaves on, dense enough to see inside a crown. Florence has the trees and the rainfall but only rasters, so I have to ask for the cloud. My fallback is Mataró, which has the scan and, unlike Badalona, its own design storm — borrowing Barcelona's would have made the test circular. And the thing I did not expect: no Catalan city publishes a city-wide pluvial map. Barcelona's is the only one I found. That is why I calibrated here.

### 17. What I cannot do yet, and what would unblock me  ·  10:17

I would rather say the limits myself. It is volume, not peak flow. It is a hazard index, not water depth — my own routing is not a flood map and I tested that. The leaf-area proxy is probably low. And the third hypothesis is true by construction of my model, so I declare it as a boundary rather than claim it as a result. Three things would unblock me: the licence to use the city's flood-depth maps, access to Infrared City, and the Florence point cloud.

---

## Only if the tutor asks

### B1. If the scope looks too narrow: from the crown to the tree as a system

If the scope needs to be wider, I would not add parallel themes. I would widen the tree into a system. The pit is the one design variable I'd add, because it links the two goals: it takes runoff from the pavement and stores it as water for transpiration, which cools the air more than shade does. Soil would enter as two or three literature options with sensitivity, since there is no survey under the streets. Carbon would be reported, not optimised.

### B2. If the tutor presses on transferability: the 22-city Catalan screening

I screened twenty-two Catalan cities on the one input that decides a transfer. ICGC publishes only the flight year, so I read the date from the per-point GPS time in the cloud itself, and checked it against Porta, where it reproduces the date I already had. Eighteen are leaf-on and classified. Three are flown but unclassified, and one is flown in November.

### B3. If the tutor presses on the design storm: method vs climate

A naive city-to-city comparison would have reported a thirty percent climate difference. Most of it is not climate, it is how the two design storms were built — an envelope against a central estimate. Harmonised, what is left is under ten percent. That is the kind of thing a transfer test has to control before it can claim anything.

### One-line answers

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
