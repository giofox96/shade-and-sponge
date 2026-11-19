# Shade and Sponge: replacing street trees without making streets hotter or wetter

*MaCAD thesis, IAAC 2026 · Research & Technologies blog post · 19 Nov 2026*

![Plane trees in Porta, Nou Barris (Barcelona)](images/01_porta_plane_trees.jpg)

## Research topic and context

Barcelona replaces its street trees one at a time: when a tree dies, or when a street is rebuilt. Since 2018 the city's own inventory records almost 11,000 trees replaced with a different species, and almost half of them (46.8%) stand alone, one isolated tree at a time. Plane trees (*Platanus*) are the largest single case, about 13% of those replacements, and the city plans to bring them from 27% to 12% of the street-tree stock. The tree master plan also caps every species at 15%.

So the city has decided **how much** of each species it wants. It has not decided **which species goes where**. When a project has to replace trees, the only documented guidance for the new species is a qualitative table by district and sidewalk width, and most recent plantings do not follow it. What the city actually plants is a practice, not a written rule, and nothing checks whether a replacement keeps, loses or improves the street's shade and rain interception. A project can leave its street hotter or wetter, and nobody measures by how much.

The choice matters. At the same trunk size, the species the city plants carry crowns from almost a full plane crown down to a quarter of one.

![Crown area of the replacement species as a share of a plane crown, by trunk class](images/02_crowns_by_class.png)

**Research question.** When a project must replace street trees, can a trait-based method, inside the city's rules, choose the new species and positions so that pedestrian cooling and storm-water interception improve, or at least do not get worse, compared with today and with the city's own practice?

The first case is Barcelona's plane trees in Porta (Nou Barris), a neighbourhood that is both hot and prone to surface flooding.

## What is the innovation?

Data on heat and flooding, city rules and species tools all exist, but nothing links them tree by tree. Of 18 tools and workflows we reviewed that place or assess urban trees, seven cover both heat and runoff, one picks species, and none chooses the species for each position inside a city's replacement rules.

![From 18 tools to none that chooses species tree by tree inside a city's rules](images/03_gap.png)

Shade and Sponge does four things differently:

- **Four actions per tree.** The designer draws a project area. For each existing tree the tool works with four actions: **leave** it (the default), **move** it (transplant), **replace** it, or **add** new trees in the free planting spots the city's street-tree guide allows.
- **Two services, one choice.** For every tree to replace and every free spot it proposes a species, scored on summer shade (checked as UTCI, the pedestrian heat index) and on storm runoff together. Runoff is a do-no-harm check: no layout may send more water to a flood hotspot.
- **Rules inside, not after.** The city's 15% species cap, the sidewalk-width sizing rule, the distance between trees and the city's list of 30 street-tree species are constraints of the optimiser, not a check done afterwards. Street objects (signs, lamps, bus stops) and underground networks turn spots into excluded or conditional ones.
- **A real baseline.** Results are compared with what the city actually plants where a tree was replaced (its inventory, 2018–2026), not with an invented scenario.

It runs on open data: the tree inventory, LiDAR crowns, terrain, a design storm and a hot day. The layout is solved exactly, as a linear programme, so the same inputs always give the same answer.

![Methodology](images/04_methodology.png)

![Why replace? The city's order, what it actually did, and what the tool does](images/05_four_actions_per_tree.png)

The tool has two front-ends: a web app for anyone, and a 3D map for designers.

![Web app: today, the city's practice and the optimised layout, tree by tree](images/06_web_app.jpg)

![3D map of a project area](images/06b_tool_3d_map.png)

## Who are the actors?

- **Decide:** Parcs i Jardins, Ajuntament de Barcelona (tree master plan, 15% cap).
- **Use:** landscape architects, computational designers, urban planners working on a street project.
- **Data and testing:** ICGC (LiDAR), the city's water-cycle company (drainage data), utility companies (underground networks for the demo street), Ladybug Tools for the heat check, Infrared City, Comune di Firenze (LiDAR for a transfer test).
- **Benefit:** residents and pedestrians in streets that are both hot and flood-prone.

## What can be exploited, how, and for whom?

**The method** (a trait-based layout under city rules) goes into the thesis and a paper, for researchers and city technicians.

**The Python core and the web app** are open source and online, for designers and for other cities.

**The per-tree crown and trait dataset** will be shared as open data (our own derived data only), for the city and for researchers.

**A transfer guide**, built on the tests in Florence and Mataró, is for any city that has to replace a monoculture.

**A quantified proposal for the city**: what each planting rule costs in shade and runoff, and how much better a choice within today's rules does than current practice. It will be one chapter of the thesis, shared with Parcs i Jardins, for city policy makers.

## What impact do we want to achieve?

**First evidence (simulated).** In Porta, replacing the planes and filling the 152 free spots brings the street trees to about 102% of today's summer shade, against about 90% for the city's practice. In every sensitivity test so far, the method stays about eight points of summer shade ahead of the city's practice and is no worse on hotspot runoff. Pedestrian heat (UTCI) stays within 0.2 °C of today's plane trees.

**Back-test on real replacements.** We took 26 places where Barcelona actually replaced ten or more street trees together (366 positions) and let the method choose for the same positions, under the same rules. At equal trunk size, the method's choice gives more summer shade per tree in 22 of the 26 places: the median goes from 59 to 139 m²·h per tree, +55% over all positions together. Where it loses, sidewalks are narrow, only small species fit, and the gap is small.

![Back-test: summer shade per new tree, city vs method](images/07_backtest_shade.png)

In all 26 places the method sends no more water to a flood hotspot than the city's planting.

![Back-test: runoff, do-no-harm in 26 of 26](images/08_backtest_runoff.png)

The method changes the species, not the number of trees: 18 species against the city's 19, so diversity stays about the same. And it does not pick species that die more: from all the city's replacements, the expected survival of the species each side chooses is 84% for the city and 85% for the method.

![Back-test: do the new trees survive?](images/09_backtest_survival.png)

**Limits, said upfront.** Everything is simulated, not measured. The back-test compares species at the same size, not the years a young tree needs to grow. The heat gain is small, and its sign depends on how porous the crowns are. Runoff is a check: the differences stay below what the model can resolve. And the benefits arrive only when the new trees mature.

**Over time:**

- **Short term (now):** an open, reproducible method with simulated gains, back-tested on the city's own replacements and checked in Ladybug and Honeybee.
- **Medium term (1–3 years):** pilot streets with Parcs i Jardins; transfer tests in Florence and Mataró.
- **Long term (2037):** canopy moving toward the city's 30% target, no species above 15%, and no street left hotter or wetter by a replacement.

## Which dimensions will it impact?

- **Environmental:** shade and rain interception kept or improved at each replacement.
- **Social:** thermal comfort for pedestrians and residents during decades of replacement.
- **Technological:** an open tool that links LiDAR, trait data and city rules.
- **Economic:** more benefit from the replacements the city already pays for.
- **Policy:** it turns a quota plan into a spatial one.

## Technology readiness

Today the method is at **TRL 3** (proof of concept on Porta). By the end of the thesis, in December, the aim is **TRL 4**: validated in simulation on real city data, against the city's own past replacements, with a full heat check and transfer tests in Mataró and Florence. A test with a real designer on a real street project would bring it to TRL 5, and a pilot street is the step after the thesis.

![Technology readiness: TRL 3 today, TRL 4 by December](images/10_trl.png)

**Next step.** The city will replace trees anyway, street by street. The step from simulation to TRL 5 is to test this on one real street rebuild, with a designer or with Parcs i Jardins: least loss, inside the city's rules.

Web app: [giofox96.github.io/shade-and-sponge](https://giofox96.github.io/shade-and-sponge/)

## Sources

- Ajuntament de Barcelona, *Pla director de l'arbrat de Barcelona 2017–2037*.
- Ajuntament de Barcelona, *Gestió de l'arbrat viari de Barcelona* (2011).
- Parcs i Jardins, *Arbrat viari: selecció d'espècies* (rev. 2004).
- Ajuntament de Barcelona, *Pla de gestió de l'arbrat viari de Barcelona* (2005).
- Open Data BCN, *Arbrat viari*, quarterly inventories 2018–2026 (CC BY 4.0).
- ICGC, LiDAR flight of 26 September 2021.
- Nació Digital, 4 May 2026; Betevé, 7 May 2026 (plane-tree reduction and replacement mix).
- Ladybug Tools (Ladybug, Honeybee).
- Mannucci et al. 2025; Nicol et al. 2026 (*PLoS One*); Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026 (prior tools).
