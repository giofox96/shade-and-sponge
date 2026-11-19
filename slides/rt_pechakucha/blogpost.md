# Shade and Sponge

**When a project must cut street trees, what is the best way to replace them? First case: Barcelona's plane trees, in Porta.**

*Giovanni Carlo Volpe · MaCAD, IAAC · Research & Technologies · November 2026*

![Plane trees in Porta, Nou Barris (Barcelona)](images/01_porta_plane_trees.jpg)

## Research topic and context

Barcelona replaces its street trees one at a time, when a tree dies or when a street is rebuilt. Since 2018, 10,976 trees have been replaced with another species. Plane trees are the largest case: the city wants them to drop from 27% to 12% of the stock in ten years. Its tree master plan sets a maximum of 15% per species and a 30% tree cover target.

This is the context, not the problem: the city has already decided **how much** of each species it wants. What it has not decided is **which species goes where**.

**The problem.** When a project must replace street trees, the only rule for the new species is qualitative. Nobody measures whether the street ends up hotter or wetter. Thousands of small decisions, unmeasured.

And the choice matters. Under the same rules and at the same trunk size, the species the city plants carry crowns from almost a full plane crown down to a quarter of one.

![Crown area as a share of a plane's, same trunk size, Porta's own trees](images/02_crowns_by_class.png)

**Research question.** When a street project in Barcelona must replace or add trees, to what extent can a trait-based method that chooses species and positions inside the city's tree rules give more summer cooling than the city's own replacement practice, without losing rain interception?

Runoff depends more on the tree pit than on the species, so in this question runoff is a do-no-harm check, not something to maximise.

## What is the innovation?

The pieces already exist, but separately. Some models assess heat and runoff together, but do not choose species; other tools choose species, but look at one service only or ignore positions. Of 18 tools that place or assess urban trees, none chooses the species tree by tree inside a city's rules.

![State of the art and gap](images/03_gap.png)

Shade and Sponge closes that gap. The designer draws a project area. The street layout and the city's rules are fixed; what is free are four actions for each tree: **keep** it, **move** it, **replace** it, or **add** new trees in free spots, but never remove without replacing. The tool advises, the designer decides.

![What is fixed, what is free](images/04_four_actions.png)

It reads open data: the tree inventory, LiDAR crowns, terrain, flood hotspots, sidewalk width and street objects, a hot day and a design storm. For every tree to replace and every free spot it proposes one of 30 street-tree species and a position, scored on summer shade (checked as UTCI, the pedestrian heat index) and runoff together. An exact optimiser picks the best combination within the rules.

![Shade and Sponge: how it works](images/05_method.png)

Three things make it new:

- **Two services, one choice.** Species and position for every tree, scored on summer shade and runoff together.
- **Rules inside, not after.** The 15% species cap, the sidewalk width that sets the tree size, and the city's species list are part of the optimisation, not a check done afterwards.
- **A real baseline, any tree.** Results are compared with the **city's practice**: what the city actually planted where it replaced trees, from its own inventory, 2018–2026. It is a practice, not a written rule. The method works for any tree a project replaces, with one data adapter per city.

This is the web app. A designer picks an area, sets priorities between summer shade, winter sun and runoff, and compares today, the city's practice and the optimised layout, tree by tree, in 3D. It is online and open source.

![The web app on Porta](images/06_web_app.jpg)

## First evidence, and its limits

As a first test, we took 26 groups of trees that Barcelona really replaced, and let the method choose for the same positions, under the same rules. With the city's choice, each new tree gives a median of 59 m²·h of summer shade; with the method's, 139. The method gives more shade in 22 of the 26 groups, and in all 26 it sends no more water to a flood hotspot. It changes the species, not the number of trees, and diversity stays about the same. The baseline also shows that 1 in 5 of the city's new trees is larger than its sidewalk allows.

![First evidence: back-test](images/07_backtest.png)

**Limits, said upfront.** Everything is simulated, not measured. The back-test compares species at the same size, not the years a young tree needs to grow. The heat gain is small, and its sign depends on how porous the crowns are. Runoff is a check: the differences stay below what the model can resolve. And the benefits arrive only when the new trees mature.

## Who are the actors?

- **Decide:** Parcs i Jardins, Ajuntament de Barcelona (tree master plan, 15% cap).
- **Use:** landscape architects, computational designers, urban planners.
- **Data and testing:** ICGC (LiDAR), BCASA (drainage), Ladybug and Honeybee, Infrared City, Comune di Firenze (LiDAR, transfer test).
- **Benefit:** residents and pedestrians in streets that are both hot and flood-prone.

## What can be exploited, how, and for whom?

**The method**, a trait-based layout under city rules, through the thesis and a paper, for researchers and city technicians.

**The Python core and the web app**, open source and online, for designers and other cities.

**A per-tree crown and trait dataset**, as open data (our own data only), for the city and researchers.

**A transfer guide**, from the tests in Florence and Mataró, for cities replacing a monoculture.

## What impact do we want to achieve?

- **Short term (now):** an open, reproducible method, back-tested on the city's own replacements, with the heat checked in Ladybug and Infrared City.
- **Medium term (1–3 years):** pilot streets with Parcs i Jardins; transfer tests in Florence and Mataró.
- **Long term (2037):** canopy moving toward 30%, no species above 15%, no more runoff where streets flood, and a method for any city replacing a monoculture.

## Which dimensions will it impact?

Environmental, social, technological, economic and policy: from pedestrians' comfort to the city's plans. It turns a quota plan into a spatial one.

## Technology readiness

Today the method is at **TRL 3**. By December the aim is **TRL 4**: validated in simulation, on real city data. A test with a real designer would bring it to **TRL 5**; a pilot street is the step after the thesis.

![Impact dimensions and technology readiness](images/08_dimensions_trl.png)

**Next step.** The city will replace trees anyway, street by street. The step from simulation to TRL 5 is to test this on one real street rebuild, with a designer or with Parcs i Jardins. Least loss, inside the city's rules.

Web app: [giofox96.github.io/shade-and-sponge](https://giofox96.github.io/shade-and-sponge/)

## Sources

- Ajuntament de Barcelona, *Pla director de l'arbrat de Barcelona 2017–2037*.
- Parcs i Jardins, *Arbrat viari: selecció d'espècies* (rev. 2004); street-tree guide (2011).
- Open Data BCN, *Arbrat viari*, quarterly inventories 2018–2026 (CC BY 4.0).
- ICGC, LiDAR flight of 26 September 2021.
- Nació Digital, 4 May 2026; Betevé, 7 May 2026.
- Ladybug Tools (Ladybug, Honeybee).
- Mannucci et al. 2025; Wu et al. 2024; Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026; Nicol et al. 2026 (*PLoS One*).
