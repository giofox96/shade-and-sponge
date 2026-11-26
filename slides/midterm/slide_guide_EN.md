# Shade and Sponge, midterm: the concepts behind each slide

A study companion for the midterm deck (24 slides, version of 24 Nov 2026), written so that you can explain any slide in your own words and answer follow-up questions. For each slide: **what it says**, **the concepts behind it**, and **questions you may get**. The spoken text is in `speech_midterm.md`; this file is the background.

Numbers come from the deck and the project notes. Where something is a modelling choice or an approximation, it is said so.

---

## Glossary (read this first)

- **Street tree / position / spot.** A *position* is a place where a street tree stands today. A *free spot* is a place on the sidewalk where a new tree could be planted. The method works on both.
- **Crown.** The leafy top of the tree. Its size (diameter, area) decides how much ground it shades and how much rain it catches.
- **LiDAR.** A laser scan from a plane that records millions of 3D points. From it we get each tree's height, crown size and how dense the crown is, and the shape of buildings and terrain. Here: the ICGC (Catalan mapping institute) flight of 2021, flown in late September with leaves on.
- **LAI (leaf area index).** Square metres of leaf per square metre of ground under the crown. A crown with LAI 2.3 has 2.3 m² of leaves stacked above every m² of ground. Higher LAI = denser crown = more shade and more rain held. We estimate it from the LiDAR: the more laser pulses pass through the crown to the ground, the more open (lower LAI) the crown is.
- **Summer shade (m²·h).** Our heat measure. It is shaded ground area multiplied by hours of shade on a hot July day in the afternoon (12–17 h): 10 m² shaded for 5 hours = 50 m²·h. It is a **proxy**: it says where the sun is blocked, not how hot a person feels.
- **Winter shade / winter sun.** The same measure on a January day (10–15 h). In winter, shade is a **cost**, because people want sun. That is why deciduous trees (bare in winter) score well.
- **UTCI.** Universal Thermal Climate Index, a "felt temperature" in °C that combines air temperature, radiation from the sun and hot surfaces, wind and humidity. It is the next heat step (Ladybug, Infrared City).
- **Runoff.** Rainwater that does not soak in or stay on the leaves and flows over the surface. Too much of it in one place gives a **pluvial flood** (flooding from rain, not from a river).
- **Interception.** Rain caught by leaves and branches, which then evaporates instead of reaching the ground.
- **Design storm.** A standard rainfall used for design, defined by duration and **return period** T: a "2-year storm" is so intense that, on average, it comes once every two years. Here: the PDISBA (Barcelona drainage plan) storm of T = 2 years, 60 minutes, 31.9 mm.
- **Flood hotspot.** A place where water collects in heavy rain, from the city's Barcelona Resilience Atlas.
- **City practice (S1b).** The species the city actually planted when it replaced trees, 2018–2026, read from its own inventory. This is the main baseline. **S1a** is the mix the city announced (press), shown next to it.
- **Effective number of species.** A diversity measure: exp(Shannon index). If 10 species are planted in equal numbers, it is 10; if one species dominates, it drops even if many species are present.
- **HiGHS.** An open-source solver for linear programming. "Exact" means it finds the best answer and can prove no better one exists.
- **Do-no-harm check.** A condition, not a goal: the method must not make runoff worse than the baseline, but it does not try to maximise runoff reduction.

---

## Main talk (slides 1–15, 20 s each)

### Slide 1. Title: "I am redesigning this street"
**What it says.** The talk opens with the project's name, Shade and Sponge, and what it is: an urban street-tree recommender. The thesis takes the point of view of a designer who is already redesigning a street. The layout is fixed; the open question is the trees: keep, move, replace or add, so that the street is cooler in summer and not worse for flooding, within the city's rules.

**Concepts.**
- The tool is not a city-scale planning tool. It enters **at project level**, where trees are actually decided.
- Two objectives, but not equal: **heat is the objective** (more summer shade), **runoff is a constraint** (no worse).
- "Within the city's rules" means the answer must be something the city could accept: allowed species, size limits, the 15% cap.

**Possible questions.** *Why the designer and not the city?* Because the city replaces trees one by one in projects (46.8% of replacements are isolated trees, per the 10 Nov analysis), so the decision happens in the project.

### Slide 2. Context: replacing trees one at a time
**What it says.** Barcelona replaced 10,976 street trees between 2018 and 2026. The tree master plan caps every species at 15%, but says nothing about which species should go where. Porta's canopy is 20.1% against a city target of 30%. And at the same trunk size, crowns of different species range from a full plane tree down to about a quarter of one. Everything is compared with the **plane**, because it is the tree most often replaced (13% of the observed replacements): results are given as a percentage of a plane's summer shade.

**Concepts.**
- **Pla director de l'arbrat 2017–2037** (the city's tree master plan) sets *how much* of each species (the 15% cap, for resistance to pests and diseases, climate resilience and biodiversity), not *which species in which street*.
- **Same trunk, different crowns.** Trunk size is how the city classifies trees. The chart shows that two trees with the same trunk can shade very different areas. So the species choice changes the shade a street gets, even with the same number of trees.
- The 15% cap is city-wide in the plan. In the tool it is applied to street trees only, a simplification declared on slide 22.

**Possible questions.** *Where do 10,976 replacements come from?* From the city's open tree inventory (Open Data BCN), comparing versions over time: a position whose species changed is a replacement.

### Slide 3. Porta in numbers
**What it says.** Why Porta: it is the first neighbourhood of Barcelona where heat, flood hazard and plane trees are all high (summer surface +1.4 °C vs the city, flood hazard in the city's top 20%, 832 planes = 29% of its street trees). Porta covers 84 ha with 2,825 street trees. Crowns cover 17 ha (20%). Reaching 30% would need about 8 ha more. Planting every free sidewalk spot adds only about 0.3 ha **of crown** (tree canopy, seen from above), against the 8 ha of crown that are missing.

**Concepts.**
- **Site selection was done with data**, ranking neighbourhoods on both hazards; Porta came first. Planes matter because the plan wants to reduce them, so many will be replaced.
- **The key argument of the slide:** new spots are few and small, so adding trees cannot close the gap. What is left to the designer is **which species** goes in each spot, because crown size depends on species.
- Squares, parks and courtyards could add more canopy, but they are outside the scope (future work).

**Possible questions.** *Is 1.4 °C air temperature?* No. It is the median summer daytime land-surface temperature anomaly against the city median (Landsat 8/9, 31 clear scenes, June–August 2022–2025), a screening indicator, not a felt temperature. *Why "first"?* Neighbourhoods were eligible only if flood share, surface heat and plane density were all above the city's 60th percentile; Porta ranks first among those at every threshold tested.

### Slide 4. State of the art and gap
**What it says.** Research covers each part of the problem, but separately; nobody joins them. Some models assess heat and runoff together without choosing species. Other tools choose species, but for one benefit or without positions. Of 18 tools reviewed, none chooses species tree by tree, on heat and runoff, inside a city's own rules.

**Concepts.**
- The review works like a **funnel**: 18 tools → 7 treat heat and runoff together → 1 also chooses species (Dong et al. 2026) → 0 do it per tree inside real city rules.
- **SylvCiT** (Nicol et al. 2026, Montreal) is the closest recommender: it chooses species for diversity and carbon, but its runoff module is "under development" and it has no heat module.
- The contribution is therefore **a method**, not a new physical model: it combines existing pieces (LiDAR crowns, shade, interception, flow routing, an exact optimiser) inside the city's constraints.

**Possible questions.** *Is the gap real or just narrow?* It is narrow on purpose: the tutor asked for a very specific thesis. The specific part is "per tree, inside the rules, against real practice".

### Slide 5. Refined question
**What it says.** In October the thesis started from trees against floods (Bologna). The feedback was that runoff depends more on the tree pit than on the species, so runoff became a do-no-harm check. The question now: when a street project in Barcelona must replace or add trees, to what extent can a trait-based method that chooses species and positions inside the city's rules give more summer cooling than the city's own practice, without losing rain interception?

**Concepts.**
- **Why runoff moved from goal to check:** a tree holds a few millimetres of rain; a heavy storm brings tens of millimetres. The soil and the pit decide more than the leaves. So the honest claim is "no worse", not "much better".
- **Trait-based:** species are compared by measurable properties (crown size, leaf density, leaf-on months), not by name or by look.
- **"To what extent"** makes the question measurable: the answer is a number (how much more shade), not yes or no.

### Slide 6. What is fixed, what is free
**What it says.** Fixed: the street layout, the 15% cap, the sidewalk width (which sets the tree size), traffic lights and driveways. Free: four actions per tree, keep, move, replace or add; never remove without replacing. The tool advises; the designer decides.

**Concepts.**
- **Keep:** the tree stays. **Move:** the tree is transplanted and its spot is freed. **Replace:** a new species in the same pit. **Add:** a new tree in a free spot.
- "Never remove without replacing" keeps the number of trees from falling.
- The designer chooses the action (often for reasons the data cannot see: health of the tree, works, neighbours). The optimiser only chooses the **species** for Replace and Add.

### Slide 7. Methodology
**What it says.** The full method in one diagram, from left to right: focus (heat stress, pluvial floods) → data (tree inventory, LiDAR 2021, hot day, terrain, flood hotspots, design storm, sidewalks and objects, city rules) → city screening (indicators per tree) → the designer decides an action per tree → HiGHS picks species for Replace and Add, scored on heat, runoff and canopy → evaluation against today and city practice → validation in Porta, then Sant Antoni, Mataró and Florence.

**Concepts.**
- **The dots next to the data** show which hazard each dataset serves: brown for heat (LiDAR, hot day), blue for floods (LiDAR, terrain, hotspots, storm).
- **City rules enter the optimiser as constraints** (the arrow from the City rules box): 30 allowed species, 15% cap, size by sidewalk.
- **Screening is done once for the whole city**; the project area is then cut out of it. That is why the tool is fast.
- **Two comparisons, at the end:** once the optimiser has chosen, the result is compared with two references: today's trees (does the street get better?) and city practice (does the method beat what the city would do?).
- **Terrain (DTM) at 0.5 m** is used for flow routing: on a digital terrain model each cell sends its water to the steepest lower neighbour (D8 method), which tells where rain from each point ends up.

### Slide 8. Screening (the indicator matrix)
**What it says.** The same indicators are computed once for every street-tree position and every free spot, one row each. Three groups of columns: A, the existing tree (species, trunk, crown, LAI, priority), which ranks candidates for replacement; B, the place (sidewalk width, allowed size, whether rain flows to a hotspot), which decides which species fit; C, a score for each of the 30 species at that position. The optimiser picks one species per row within the 15% cap. Values on the slide are illustrative.

**Concepts.**
- **Why a matrix:** once every position has a score for every species, the choice becomes a clean optimisation problem: one species per row, maximise the total, respect the cap.
- **Score of a species at a position:** a weighted combination of the summer shade it would give there, the winter sun it would block (a cost) and the rain it would hold. Weights are set by the designer (slide 16).
- **Priority** (group A) flags weak or problematic trees as candidates, but the designer decides.
- The same species scores differently at different positions, because buildings, street orientation and sidewalk width change its effect.

### Slide 9. City rules
**What it says.** The sidewalk width sets the tree size and spacing, and no species may exceed 15%.

**Concepts.**
- From the city's street-tree guide (Parcs i Jardins, *Gestió de l'arbrat viari*, 2011): sidewalk under 2.5 m, no tree; 2.5–3.5 m, small tree; 3.5–6 m, medium; over 6 m, large; spacing about 7, 9 and 13 m.
- **How the width is measured:** from the city's 1:1000 map, a line from the nearest façade through the tree to the kerb. It works for about 55% of Porta's trees; trees on medians or without a façade nearby are not filtered by size (declared assumption).
- The optimiser **never breaks** these rules: a species too big for a sidewalk is simply not allowed at that position.

### Slide 10. Where new trees go
**What it says.** Porta has 267 candidate spots: 153 free, 103 conditional, 11 blocked.

**Concepts.**
- **Free:** nothing in the way. **Conditional:** a sign, crossing, lamp, bollard or bus stop is in the way; a project can usually move it, but it needs a field check and costs money. **Blocked:** traffic lights and driveways, which a street project normally cannot move.
- This classification was decided with Giovanni (18 Nov) and recomputed on 23 Nov.
- Candidate spots respect the same spacing and size rules as slide 9.
- Underground services (pipes, cables) are **not** in these classes yet, so free spots are an upper bound (slide 22).

### Slide 11. A crown is a bucket
**What it says.** 1 mm of rain on 1 m² is 1 litre. In the 2-year, 1-hour storm (31.9 mm), about 1,000 litres fall on a typical Porta crown. About 125 litres stay on the leaves (1.75 mm × LAI ≈ 4 mm); about 875 litres reach the ground. The same tree holds the same water wherever it stands.

**Concepts.**
- **Why 1,000 litres:** a typical crown covers about 31 m²; 31 m² × 31.9 mm ≈ 1,000 L.
- **Canopy storage = s × LAI.** s = 1.75 mm per unit of LAI, calibrated on field data from Anys & Weiler (2024), 16 urban lime and maple trees. With LAI ≈ 2.3, storage ≈ 4 mm, so ≈ 125 L on a 31 m² crown.
- **"A bucket":** once the leaves are full, everything else falls through. In a heavy storm the bucket fills early, so most water still reaches the ground. This is why interception alone cannot solve floods.
- **The slide's key line:** the amount held depends on the tree, not on where it stands. Position matters only for where the held water *would have gone* (next slide).
- s is uncertain: a lower value (0.83–0.86 mm) is tested on slide 24.
- **Bridge to slide 12 (why the method matters for runoff):** since all species hold water but some hold much more (larger crown, denser leaves), the method puts the species that hold **the most water** in the positions whose rain is heading to a flood hotspot, so that less water piles up there. This happens whenever runoff has a weight in the score.

### Slide 12. The tree on the hill
**What it says.** A tree upstream of a flood hotspot keeps its ~125 litres from reaching the hotspot. But 74% of Porta's tree positions drain to no hotspot: following the slope of the terrain model, the rain that falls there flows away (to other streets, to drains, out of the neighbourhood) without ever passing through a flood hotspot, so the water those trees hold does not change any flooding. 100 trees placed by the method keep 5.6 times more water from hotspots than 100 trees at random. But that is only 0.5% of the hotspot water, so runoff is a do-no-harm check.

**Concepts.**
- **Flow routing** on the terrain model tells, for each position, whether its water ends in a hotspot. Only those positions can help the hotspot.
- **×5.6 vs 0.5%:** the method is much better than random at choosing *where*, but the total effect is tiny compared with the water a hotspot receives. Both facts are true; the second is why runoff cannot be the main objective.
- The model counts volumes only (no pipes, no ponding over time), which is another reason to claim "no worse" and not "solved".

### Slide 13. City practice, not a rule
**What it says.** The baseline is what the city really planted (2018–2026). One in five new city plantings is larger than its sidewalk allows. The same rules apply to both the city's practice and the method. Switching a rule off and re-optimising shows what each rule costs.

**Concepts.**
- **Why practice and not the written rule:** the written replacement table (2004/2005) is mostly not followed in Porta. Comparing with what actually happens is fairer and more useful.
- **S1b** is built from 1,444 plane replacements in the inventory: the observed species mix, placed by the sidewalk rule. **S1a** (the announced mix from the press) stays beside it as a second reference.
- **"1 in 5 too big"** (21% of new city plantings): the city itself does not always follow its size rule. The method does, so it is compared at a disadvantage, not an advantage.
- **Cost of a rule:** run the optimiser with and without, for example, the 15% cap; the difference in shade is what the rule costs. Useful for a city discussing its rules.

### Slide 14. First evidence: back-test and co-benefits
**What it says.** 26 groups where the city really replaced trees, same positions, city's choice vs method. Median summer shade per tree: 59 m²·h for the city, 139 for the method. The method gives more shade in 22 of 26 groups, and in 26 of 26 sends no more water to flood spots. Co-benefits in Porta (reported, not optimised, today = 100): carbon stored once grown 56 vs 42; pollen load below today in every replacement; lifting diversity from 6.2 to 9.4 effective species costs only 0.3 points of summer shade (city practice: 15.6).

**Concepts.**
- **Back-test:** replay the past. Take positions the city really replaced, keep them fixed, and ask what the method would have planted there. It is the fairest test, because positions and constraints are identical.
- **Why carbon is below 100:** today's trees are big mature planes; new trees, even once grown to today's sizes per species, store less. The method still stores more than city practice. Carbon uses the Jucker et al. (2017) allometry.
- **Pollen:** planes are highly allergenic (Cariñanos et al. 2014 index), so any replacement lowers it.
- **Diversity** was the weak point: without a floor the method concentrates on few high-shade species. A diversity floor (a minimum effective number of species) fixes most of it for almost no shade. The city still plants more variety (15.6).
- **If asked about the city-wide result:** with 30 species the method keeps a median 91.2% of a plane's summer shade, +6.7 points over the announced mix and +14.7 over practice, winning in 32 of 32 neighbourhoods.

### Slide 15. Next
**What it says.** Three next steps. (1) Felt temperature (UTCI) with Ladybug and Infrared City, to check that more shade means a cooler street. (2) The transfer tests: Mataró already gives 83% vs 63% summer shade (6 of 6 streets) and is now rerun with real ICGC LiDAR crowns; Florence follows (transfer test planned 29 Nov – 3 Dec). (3) The utility plans, to see which spots are really free (today free spots are an upper bound). The talk ends with a plain "Thank you".

**Concepts.**
- **From shade to UTCI:** shade is a proxy. Ladybug Tools (in Grasshopper) and Infrared City compute felt temperature, which also counts hot surfaces and wind. This checks whether more shade really means a more comfortable street.
- **Transfer:** Mataró tests a different city with its own data and practice; Florence (municipal LiDAR 2023) is the next transfer case.
- The photo is Porta.

---

## Backup slides (only if asked)

### Slide 16. In the tool: priorities and trade-offs
**What it says.** The designer clicks a point on a triangle whose corners are summer shade, winter sun and runoff; the optimiser re-solves in the browser. Every layout appears as a dot on a chart of summer shade against winter shade, next to today's trees, city practice and a random palette.

**Concepts.**
- **The triangle sets the weights** of the score (slide 8). A corner means "only this objective"; the centre means balanced.
- **Trade-off:** more summer shade usually means more winter shade too (more crown, more shade all year). Deciduous species with dense summer crowns break this partly. The chart lets the designer see what they gain and what they pay.
- On the chart, the optimised layouts sit to the right of city practice and of today's trees (more summer shade), and several of them also below today (less winter shade).
- **Pareto idea:** a layout is "efficient" if you cannot gain on one axis without losing on the other.

### Slide 17. Method (simple version)
Four steps: screen every tree and free spot; the designer sets an action per tree with a reason; an exact optimiser picks the species for every replaced or added position; compare with today and with city practice. Use it if the full diagram (slide 7) is too dense for a question.

### Slide 18. Screening (simple version)
Three questions for every position: what stands there (species, trunk class, crown size, leaf density, a weak-crown hint), where it is (sidewalk width → size; lamps, signs, crossings; does rain flow to a flood spot?), and what each of the 30 species would do there (summer shade +, winter shade −, rain held +). The simple face of slide 8.

### Slide 19. HiGHS: the solver that picks every species
**What it says.** A five-position, three-species example. Rules: one species per position; only species that fit the sidewalk; no species above its cap (here 2 of 5). Every layout that obeys the rules is a point in a shape; the best is a corner; HiGHS finds the highest corner and proves none is higher. Total 3.3. Greedy (best per position, A, A, A, B, C) breaks the cap; trial-and-error methods (genetic, ant colony) obey the rules but never know if they found the best. Porta: 832 positions × 30 species in about 0.2 s; the answer is always whole trees.

**Concepts.**
- **Linear programming:** maximise a sum of scores under linear constraints. The feasible layouts form a polytope; the optimum is always at a vertex (corner). Simplex-type methods walk from corner to corner uphill.
- **Why exact matters:** it gives a defensible answer ("the best under these rules"), reproducible every time, and lets you measure the cost of a rule exactly.
- **Whole trees:** this assignment problem has a structure (a transportation problem) whose corners are whole numbers, so no tree is split into fractions.
- Decided on 9 Nov: no genetic algorithms or ML surrogate in the thesis; HiGHS only.

### Slide 20. Why Mataró
**What it says.** Mataró tests whether the method works with other data and another practice. It has a full tree inventory (species and position for every tree, received Nov 2026), the same ICGC LiDAR as Porta (leaf-on summer flight, same coordinate system), its own design storm (PDCLAM, the only finalist city with one), pluvial flood risk (one of ACA's 44 Catalan municipalities), and the same climate with different planting choices. It is 25 km from Porta.

**Concepts.**
- **Why not Badalona:** no design storm of its own, so it would have to borrow Barcelona's, making the test circular.
- **Transfer test:** the method is re-run with the same rules and palette on another city's data; if it still beats practice, it is not tuned only to Porta.
- Mataró's inventory has no licence to share, so it stays out of the public repository.

### Slide 21. Mataró: six plane streets
**What it says.** On the six streets with most planes, a project replaces every plane. Median summer shade of the new trees, as % of planes of the same size: 83% method vs 63% city practice; the method wins on 6 of 6 streets; runoff never worse than any practice. First run, approximate: crowns are Barcelona medians per species (Mataró LiDAR next), buildings from Overture Maps, flat ground, no hotspot map. València (narrow) is the weak case: 42% vs 35%.

**Concepts.**
- **% of planes of the same size:** each new tree's shade divided by the shade of a plane with the same trunk, so 100% = as good as a plane.
- **It is a forward what-if, not a back-test:** Mataró has one inventory snapshot, so there are no past replacements to replay.
- **"City practice" here is Barcelona's** (S1b), applied in Mataró. Against Mataró's own recent plantings the method wins by more (about +33 points).
- **València:** on a narrow street few species fit between the façades, so every option is small and the gap shrinks.

### Slide 22. Declared assumptions
**What it says.** What the method takes as given and why it is acceptable now:
1. New trees at the size of today's trees: each species takes the median crown it has in Barcelona today (LiDAR). Growth and life cycle are not modelled; a ≈10-year view is in the tool.
2. Heat = summer shade, not felt temperature; UTCI is next.
3. One interception rate for every species (1.75 mm per unit of LAI); species-specific rates do not change the ranking.
4. Free spots are an upper bound: no open data on underground services; replacements reuse the existing pit; conditional spots need a field check.
5. 15% cap on street trees only; the plan counts squares too; to revisit before the final results.
6. A moved tree leaves the site: its position is freed or replanted; where it lands is outside the tool.

**Concepts.**
- **Declaring assumptions** is what makes a computational method trustworthy: the reader knows where the result could move.
- Each assumption is either tested (interception on slide 24) or has a planned step (UTCI, utilities, cap).
- **Median crown in Barcelona:** using the city-wide median per species avoids comparing a young new tree with an old one, which would be unfair to the new species.

### Slide 23. Case study: Av. Rio de Janeiro, Porta
**What it says.** 22 poplars removed in 2022–24 and replanted together in 2025. Before: 16 *Populus nigra* + 6 *Populus alba*, 167 m²·h of summer shade per tree. City planted: 22 *Fraxinus angustifolia* (narrow-leaved ash), 74 m²·h. Method: 14 *Gleditsia triacanthos* (honey locust) + 8 *Firmiana simplex* (Chinese parasol tree), 240 m²·h. Per tree, removed · city · method: rain held in a 2-year storm 123 · 54 · 219 litres; winter shade 92 · 29 · 85 m²·h; runoff to flood spots: the same.

**Concepts.**
- **A real project from start to end**, shown as the designer would see it.
- The method gives more summer shade and holds more rain than the city's choice, and even more than the poplars that were there.
- **The cost is winter shade:** 85 vs 29 for the city's ash, though still below the poplars' 92. This is the trade-off of slide 16 in a real street.
- Two species instead of one: also a small gain in diversity on that street.

### Slide 24. Cost and robustness
**What it says.** Costs: replace up to 500 € per tree (fell, remove stump, plant a 16–18 cm tree; provincial grant ceiling incl. VAT); move 502–2,867 € per tree (tree spade, root ball 90–300 cm; direct cost); widen a pit from 1 to 1.5 m² about 100 € (direct cost). Method and city practice replace the same trees, so the method changes the species, not the number of works. Robustness: with 11 of 30 species given their own interception rate, Porta's summer shade is 103.4% of today in both runs, and runoff to flood spots is −0.2% vs −0.3% of city practice; with a lower rate for short storms (0.86 or 0.83 mm instead of 1.75), differences between layouts halve but keep their sign, all under 1%. The ranking holds.

**Concepts.**
- **Costs come from** the Diputació de Barcelona catalogue 2024–2027 (replacement ceiling) and the CYPE price generator (moving, pit).
- **"Same works":** the extra cost of the method over city practice is close to zero, because only the species changes. Moving is the expensive action, so the designer should use it sparingly.
- **Sensitivity analysis:** change an uncertain input and check whether the conclusion changes. Here the size of the runoff difference changes, but its sign and the ranking do not.
- **103.4% of today:** the optimised Porta layout gives slightly more summer shade than today's trees.

### Slide 25 (private copy only). Underground utilities
**What it says.** Pipes and cables under the sidewalk can make a tree pit impossible where the surface looks free. The utility plans were requested through the official channel; almost all networks have arrived, the water network is pending.

**Concepts.** The plans are confidential: never show or publish them. They will only turn some free spots into blocked or conditional. Until then, free spots are an upper bound (slide 22).
