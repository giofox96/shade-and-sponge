# Shade and Sponge: replacing street trees without making streets hotter or wetter

*MaCAD thesis, IAAC 2026 · Research & Technologies blog post · draft 12 Nov*

<!-- IMAGE 1: title photo, Horts urbans de Porta (slides/fig/01_title_photo.webp) -->

## Research topic and context

Barcelona replaces its street trees one at a time: when a tree dies, or when a street is rebuilt. Since 2018 the city's own inventory records almost 11,000 trees replaced with a different species. Plane trees (*Platanus*) are the largest single case, about 13% of those replacements, and the city plans to bring them from 27% to 12% of the street-tree stock. The tree master plan also caps every species at 15%.

So the city has decided **how much** of each species it wants. It has not decided **which species goes where**. When a project has to replace trees, the only documented rule for the new species is a qualitative table by district and sidewalk width, and most recent plantings do not follow it. No rule checks whether a replacement keeps, loses or improves the street's shade and rain interception. A project can leave its street hotter or wetter, and nobody measures by how much.

The choice matters. At the same trunk size, the species the city plants carry crowns from almost a full plane crown down to a quarter of one.

<!-- IMAGE 2: crowns figure (slides/fig_v8/v8_crowns.png) + legend -->

**Research question.** When a project must replace street trees, can a trait-based method, inside the city's rules, choose the new species and positions so that pedestrian cooling and storm-water interception improve, or at least do not get worse, compared with the city's own practice?

The first, validated case is Barcelona's plane trees in Porta (Nou Barris), a neighbourhood that is both hot and prone to surface flooding.

## What is the innovation?

Data on heat and flooding, city rules and species tools all exist, but nothing links them tree by tree. Of 18 tools and workflows we reviewed that place or assess urban trees, seven cover both heat and runoff, one picks species, and none chooses the species for each position inside a city's replacement rules.

<!-- IMAGE 3: gap diagram (slides/fig_v8/v8_gap_boxes.png) -->

Shade and Sponge does three things differently:

- **Two services, one choice.** For every tree to replace, it proposes a species and a position, scored on summer shade (checked as UTCI, the pedestrian heat index) and on storm runoff together.
- **Rules inside, not after.** The city's 15% species cap, the sidewalk-width sizing rule and the city's species list are constraints of the optimiser, not a check done afterwards.
- **A real baseline, for any tree.** Results are compared with what the city actually plants where a tree was replaced (its inventory, 2018–2026), not with an invented scenario. The method works for any tree a project replaces, and a city needs only one data adapter.

It runs on open data: the tree inventory, LiDAR crowns, terrain, a design storm and a hot day. The layout is solved exactly, as a linear programme, so the same inputs always give the same answer.

<!-- IMAGE 4: method flowchart (slides/fig_v7/flow_00_overview.png) -->
<!-- IMAGE 5: web app screenshot (slides/rt_pechakucha/webapp_porta.jpg) -->

## Who are the actors?

- **Decide:** Parcs i Jardins, Ajuntament de Barcelona (tree master plan, 15% cap).
- **Use:** landscape architects, computational designers, urban planners working on a street project.
- **Data and testing:** ICGC (LiDAR), BCASA (drainage data), Ladybug Tools for the heat check, Infrared City (in contact), Comune di Firenze (LiDAR for a transfer test).
- **Benefit:** residents and pedestrians in streets that are both hot and flood-prone.

## What can be exploited, how, and for whom?

| What | How | For whom |
|---|---|---|
| The method: trait-based layout under city rules | Thesis, paper | Researchers, city technicians |
| Python core and web app | Open source, online | Designers, other cities |
| Per-tree crown and trait dataset | Open data (own data only) | City, researchers |
| Transfer guide | Florence and Mataró tests | Cities replacing a monoculture |

## What impact do we want to achieve?

**First evidence (simulated).** Across 28 Barcelona neighbourhoods, under one city-wide 15% cap, the tool keeps more summer shade than the city's announced replacement mix in 27 of them, by a median of 9 points. Against what the city actually plants, none of 33 neighbourhoods loses. Pedestrian heat (UTCI) stays within 0.2 °C of today's plane trees.

<!-- IMAGE 6: city map (slides/fig_v7/res_04_city_map.png, cropped, without the internal source line) -->

**Limits, said upfront.** Everything is simulated, not measured. The heat gain is small, and its sign depends on how porous the crowns are. Runoff is a check: the differences stay below what the model can resolve. And the benefits arrive only when the new trees mature.

**Over time:**

- **Short term (now):** an open, reproducible method with simulated gains across the city, checked in Ladybug and Honeybee.
- **Medium term (1–3 years):** pilot streets with Parcs i Jardins; transfer tests in Florence and Mataró.
- **Long term (2037):** canopy moving toward the city's 30% target, no species above 15%, and no street left hotter or wetter by a replacement.

## Which dimensions will it impact?

- **Environmental:** shade and rain interception kept or improved at each replacement.
- **Social:** thermal comfort for pedestrians and residents during decades of replacement.
- **Technological:** an open tool that links LiDAR, trait data and city rules.
- **Economic:** more benefit from the replacements the city already pays for.
- **Policy:** it turns a quota plan into a spatial one.

## Technology readiness

Today the method is at **TRL 3** (proof of concept on Porta). By the end of the thesis, in December, the aim is **TRL 4**: validated in simulation on real city data, city-wide and with a full heat check. A test with a real designer on a real street project would bring it to TRL 5, and a pilot street is the step after the thesis.

<!-- IMAGE 7: TRL bar (slide 14 of the pitch) -->

**Next step.** The city will replace trees anyway, street by street. The step from simulation to TRL 5 is to test this on one real street rebuild, with a designer or with Parcs i Jardins: least loss, inside the city's rules.

Web app: [giofox96.github.io/shade-and-sponge](https://giofox96.github.io/shade-and-sponge/)

## Sources

- Ajuntament de Barcelona, *Pla director de l'arbrat de Barcelona 2017–2037*.
- Ajuntament de Barcelona, *Gestió de l'arbrat viari de Barcelona* (2011).
- Parcs i Jardins, *Arbrat viari: selecció d'espècies* (rev. 2004).
- Open Data BCN, *Arbrat viari*, quarterly inventories 2018–2026 (CC BY 4.0).
- ICGC, LiDAR flight of 26 September 2021.
- Nació Digital, 4 May 2026; Betevé, 7 May 2026 (plane-tree reduction and replacement mix).
- Ladybug Tools (Ladybug, Honeybee).
- Mannucci et al. 2025; Nicol et al. 2026 (*PLoS One*); Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026 (prior tools).
