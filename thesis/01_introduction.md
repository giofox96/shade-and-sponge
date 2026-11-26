# Introduction {#sec:intro}

<!-- Draft 1, 26 Nov 2026. Sources: notes/topic_decision.md §10.1–10.6 (v7) and §11 (v8, 9 Nov); notes/tree_master_plan.md;
notes/site_selection.md §4–§5; notes/tutor_feedback_24nov.md §3d and D2; scripts/make_final_new.py (n_question, H1 wording
after commit c4018de, 26 Nov); thesis/results_numbers.md for any result quoted. Press figures are marked as press.
Citation keys are provisional (block at the end). -->

This thesis develops a computational method for choosing the species and positions of replacement street trees, so that a street keeps its shade and its rain interception when a project changes its trees. It is built and tested in Barcelona, in the neighbourhood of Porta, on the city's largest single replacement case: the plane tree.

This chapter sets out the context, the problem, why it matters, why Porta, the research question and the hypotheses. It ends with the user the method is built for and a map of the thesis.

## Context: a city that replaces its trees one at a time {#sec:intro-context}

Barcelona already decides a great deal about its street trees. Four decisions frame this thesis.

- **A species cap.** The tree master plan, *Arbres per viure*, sets a target that no tree species should exceed 15% of the trees in the urban fabric [@ajuntament2017arbres, §2.1]. The limit is older than the plan: the 2011 street-tree guide already set it [@ajuntament2011gestio, p. 21].
- **A cover target.** The same plan aims to raise tree cover by five points, to 30% of the city, by 2037 [@ajuntament2017arbres, §2.1].
- **A size rule.** The 2011 guide links each sidewalk's width to a tree size class, from "small" on narrow sidewalks to "large" on sidewalks wider than 6 m [@ajuntament2011gestio, pp. 22–23].
- **A plane reduction.** The plane tree, *Platanus × acerifolia*, is the only species above the cap. In May 2026 the city announced that more than half of its planes would be removed within ten years (press: @naciodigital2026; @beteve2026). The plan itself prints neither that figure nor a date.

The replacement does not happen in one campaign. Trees are replaced one at a time, when a tree dies or when a street project rebuilds the ground (Chapter 3). The city's quarterly tree inventory shows the scale of this. Between 2018 and mid-2026 it records 10,976 replacements in which a pit changed species: about 1,300 a year, a floor rather than a total, since a same-species replant is invisible in the data. Planes are the largest single taxon removed, at 1,444 cases (13%). Four species that the 2011 guide marks "avoid" (*Robinia pseudoacacia*, *Populus nigra*, *Ulmus pumila* and *Populus alba*) together account for 26% [@ajuntament2011gestio].

<!-- 10,976 / 1,444 / 13% / 26% / ~1,300 a year: notes/topic_decision.md §11.1 (scripts/inventory_history.py, Open Data BCN
quarterly inventory 2018Q1–2026Q2, CC BY 4.0). Same-species replant caveat from the same section. -->

So the question of which species goes back is asked thousands of times, street by street, by whoever designs or approves each project.

## The problem {#sec:intro-problem}

**In one sentence.** Barcelona replaces street trees one at a time, at least about 1,300 a year with a change of species, and the planes are the largest single case; the only documented rule for which species goes back is qualitative, and no rule checks whether a replacement keeps, loses or improves a street's shade and rain interception, so each project can make its street hotter or wetter than before without anyone measuring by how much.

The problem has five parts.

1. **The rule that exists is qualitative.** Parcs i Jardins' table for dead trees, from 2004 and 2005, assigns species by district and sidewalk width. In Nou Barris it gives *Prunus cerasifera* on sidewalks narrower than 3.5 m, Melia or Jacaranda on medium sidewalks, and keeps the plane on sidewalks wider than 6 m. Its stated criteria are tolerance, urban typology, tradition and the experience of the technicians [@parcsijardins2004seleccio; @parcsijardins2005pla].
2. **It is not visible in practice.** The 2011 guide no longer prints the table. In Porta, up to about 90% of the dated plantings on narrow and medium sidewalks are other species. This is an upper bound, because street rebuilds and exceptions follow other lists (Chapter 3).
3. **No rule quantifies the consequences.** No city document estimates what a species choice does to pedestrian heat stress or to storm runoff at a given position [@ajuntament2017arbres; @ajuntament2011gestio]. A 2013 Parcs i Jardins document on species diversification lists climate, space, environmental services, coexistence and durability as criteria. It mentions shade only as a "feeling of freshness", and runoff not at all.
4. **The consequences are large.** At equal trunk size, the species that the city plants in place of planes carry very different crowns. In Porta, Brachychiton carries about a quarter of a plane's crown area, Celtis a third to a half, Melia about three quarters, and Tipuana and Jacaranda close to a whole plane (Chapter 3).
5. **They fall where two hazards meet.** Porta is among the Barcelona neighbourhoods where both pluvial flooding and summer heat rank high, and it has 832 planes. Each choice fixes the street's canopy for decades.

<!-- Point 1: notes/tree_master_plan.md §5b. Point 2: same, "up to ~90%, an upper bound". Point 3: the 2013 document is
"Diversificació d'espècies", internal, read by machine translation (notes/tutor_feedback_24nov.md §2); check the Catalan
original before citing it formally: no citation key yet. Point 4: notes/topic_decision.md §9.9 (crown_by_trunk_class.csv):
Brachychiton 0.24–0.27, Celtis 0.32–0.52, Melia 0.71–0.81, Tipuana 0.91–1.07, Jacaranda 0.89–0.96. -->

The gap is therefore not a lack of rules. Barcelona's rules fix how many trees of each species may stand and how large each may be. They do not say which species should go where, and nobody measures what the choice costs in shade or in water.

## Why it matters {#sec:intro-why}

A question asked at the review of 20 October was simple: does Barcelona have enough trees? In Porta, the answer is no, and the shortfall sits where the planes are.

- **Porta's tree cover was 20.1%** of its 83.7 ha in 2021, measured from the leaf-on LiDAR flight of 26 September 2021 (canopy taller than 2 m). That is about ten points below the city's 2037 target of 30%.
- **Planes are its largest single canopy component.** Their crowns cover 5.75% of the neighbourhood, about 29% of its canopy.
- **The choice of species moves the cover.** At equal trunk size, replacing every plane with a Brachychiton-sized crown would cut Porta's cover by about four points. A Tipuana- or Jacaranda-sized crown would keep it roughly level.

<!-- notes/topic_decision.md §10.3 (scripts/porta_canopy_cover.py, ICGC LiDAR 26 Sept 2021). Caveat: CHM > 2 m includes tall
shrubs (ASSUMPTION). -->

So the choice of species is not a detail next to "plant more trees". In a neighbourhood that already lacks cover, the replacement of its largest canopy component decides whether it moves towards the city's target or away from it.

Heat and rain make the stakes concrete. Street trees cool pedestrians mainly by shading them, and the crown's size and density set how much sun they stop (Chapter 2). The same crowns hold back the first millimetres of a storm on their leaves, which matters most for the frequent, short and intense storms that cause pluvial flooding in dense districts (Chapter 2). A replacement that halves a street's crown area therefore removes both services at once, and it does so for decades.

## Why Porta {#sec:intro-porta}

Porta, in the district of Nou Barris, was chosen by a non-compensatory screening of Barcelona's neighbourhoods. A neighbourhood qualified only if three indicators were all above the city's 60th percentile:

- the share of its area with a high pluvial flood-hazard index;
- its summer daytime surface-temperature anomaly;
- its density of plane street trees.

A strong value on one hazard could not make up for the absence of the other. The eligible neighbourhoods were then ranked on these indicators plus social heat vulnerability. Porta came first at the 50th, 60th and 70th percentile thresholds.

<!-- notes/site_selection.md §2–§4 (scripts bcn_site_screening.py → bcn_heat_check.py → bcn_site_select.py). Sources of
the indicators: Barcelona Regional impact study via the Resilience Atlas; Landsat 8/9 C2 L2, Jun–Aug 2022–2025, own
processing; Ajuntament open data (vulnerability 2015, arbrat-viari). -->

Porta covers 0.84 km² and has 2,825 street trees of 53 taxa, of which 832 are planes (29%). They are concentrated along Avinguda Meridiana, which is also the band of highest flood hazard. The next most common species in Porta are the ones the city plants in place of planes: Celtis, Melia, *Pyrus calleryana*, Jacaranda, Tipuana and Brachychiton. The candidate species therefore already grow on site, and their crowns can be measured from the same LiDAR flight as the planes.

Sant Antoni, which ranks first for flood hazard but below the city median for surface heat, failed the both-hazards condition. Two other cities test whether the method travels: Mataró, a Catalan city on the same coast, and Florence (Chapter 6).

## Research question {#sec:intro-rq}

The research question starts from the project, not from the tree.

> **When a street project in Barcelona must replace trees, can a trait-based layout method, inside the city's tree rules, choose the new species and positions, and new planting spots, so that pedestrian cooling and storm-water interception improve, or at least do not get worse, compared with the city's own practice and with today?**

It has two references, in this order:

- **city practice:** the species the city has actually planted where it replaced planes between 2018 and 2026 (scenario S1b). The method must be no worse on any service.
- **today:** the street as it stands (S0). This is the target, which additions in new spots can help to reach.

"No worse" on runoff means within the smallest difference the model can resolve (Chapter 6).

Four sub-questions break the main question down:

- **SQ1 (heat):** how does pedestrian heat on a hot design day differ between city practice and the method's layout? The stated metric is the mean UTCI over 12–17 h. The method optimises a fast shade proxy, and checks it against UTCI.
- **SQ2 (runoff):** how does the runoff from a 2-year, 60-minute storm differ, in total and at Porta's flood hotspots, and is the difference larger than what the model can resolve?
- **SQ3 (trade-off):** do the heat-best and the runoff-best layouts differ, and in which species?
- **SQ4 (additions):** how much of the canopy gap to the 30% target can new street trees close within the planting rules, and where?

The plane is the first case, and the validated one. The logic covers any tree a project must replace, since the planes are only 13% of the city's replacements.

## Hypotheses and the validity boundary {#sec:intro-hypotheses}

- **H1 (do no harm, improve where possible):** for the trees a project must replace, the method's layout is no worse than city practice on heat or runoff, better on summer heat, and casts no more winter shade than today. Winter shade counts as a cost, because a crown that shades in January takes the winter sun from the street. Runoff is a check, not a target: in our runs the choice of species moves hotspot runoff by less than the model can resolve (Chapter 6), and tree pits matter at least as much as the crown (Chapter 2).
- **H2 (trade-off):** the heat-best and runoff-best layouts differ in species.

Two earlier formulations were dropped:

- a third hypothesis, that the runoff benefit shrinks as the storm grows, withdrawn on 19 October: in the interception model every crown is full at every design storm, so the claim is true by construction, an identity rather than a hypothesis;
- the wording "jointly reduce heat stress and runoff", replaced by "retain" and then by "improve, or at least do no harm". At equal trunk size the plane has one of the largest crowns in the palette, so almost every replacement loses some shade against today, and "reduce" would be misleading.

<!-- H1 wording: notes/topic_decision.md §11.4 (amended 26 Nov, Giovanni: "no more winter shade than today"; final-deck
commit c4018de; scripts/make_final_new.py n_question). H2: §11.4. H3 withdrawn: notes/topic_decision.md §8 point 2 (v5, 19 Oct). "Reduce" →
"retain": §10.5 row 2. Runoff as a check: §11.4 (RM_L04). -->

**Declared validity boundary.** Extreme storms on saturated ground, and floods driven by rivers, are outside what a choice of street-tree species can change. They are stated as a limit of the method, not tested. Its claims hold for frequent, short and intense storms, the ones that crowns can partly intercept.

## Who the method is for {#sec:intro-user}

The method has one primary user: **the designer of a city street project**. This can be a municipal technician or a firm the city commissions, and they work inside the city's rules. Parcs i Jardins de Barcelona, the municipal institute that manages the trees, sets those rules and approves the species. Other actors take part in the process:

- the city approves and pays for street projects. Inside Porta, for example, the executive project for carrer de Santapau was approved by the Comissió de Govern on 9 October 2025, for EUR 1,101,205.00 including VAT;
- the utility companies supply the plans of the services under the sidewalk;
- residents can comment while a project is on public display.

<!-- notes/tutor_feedback_24nov.md §3d and decision D2 (designer first; Parcs i Jardins approves). Santapau approval:
notes/sylvcit_followups.md §1 (BOPB notice https://bop.diba.cat/anuncio/ver-pdf/3833557). NOT VERIFIED (§3d): whether
street projects are designed in-house or by commissioned firms as a rule; do not state a share. -->

The method reaches the designer through two front-ends on one Python core:

- a Grasshopper exchange, for computational designers who already work in Rhino;
- a web application that runs in the browser, re-optimises live, and lets a designer draw a project area. Only the trees inside that area are decided, and every result is compared with city practice and with today for that area.

The method advises; people decide. It does not replace the botanist's or the technician's judgement of a site. It shows, for each choice the rules allow, what that choice keeps or loses in shade and in rain interception.

## Thesis map {#sec:intro-map}

The thesis follows the IAAC structure in four parts.

**Introduction (Chapters 1–4).**

- **Chapter 2** reviews how street trees affect pedestrian heat and pluvial runoff: rain interception, tree pits, shade and UTCI, transpiration, and leaf phenology.
- **Chapter 3** sets out how Barcelona chooses its street trees: the 15% cap, the size rule, the 2004/2005 table and the 2026 mix. It places the cap in the diversity literature [@santamour1990; @kendal2014].
- **Chapter 4** reviews computational tools for urban trees and narrows the gap: no method yet chooses street-tree species and positions against pedestrian heat stress and event runoff together [@mannucci2025; @nicol2026; @dong2026].

**Development and research materials (Chapters 5–6).**

- **Chapter 5** describes the method: the data, the tree model from LiDAR, the heat proxy, the runoff model, the rules as constraints, the optimiser and the scenarios.
- **Chapter 6** validates it: the interception calibration, the heat proxy against Ladybug, what the runoff model can resolve, a back-test against 26 groups of trees the city really replaced, and a transfer test in Mataró.

**Results (Chapter 7):** Porta, the city's own per-tree plan, the diversity floor, the co-benefits, new planting spots and the city-wide screening.

**Discussion and conclusions (Chapters 8–9).** Chapter 8 answers the sub-questions and hypotheses and states the limits. Chapter 9 states the contribution and the future work.

<!--
PROVISIONAL CITATION KEYS → references (keys as in thesis/02–05; align with the Better BibTeX export)
ajuntament2017arbres       Ajuntament de Barcelona 2017, Arbres per viure: Pla director de l'arbrat 2017–2037 (ch. 3 block)
ajuntament2011gestio       Ajuntament de Barcelona 2011, Gestió de l'arbrat viari de Barcelona (ch. 3 block)
parcsijardins2004seleccio  Parcs i Jardins 2004, Arbrat viari: selecció d'espècies (ch. 3 block)
parcsijardins2005pla       Parcs i Jardins 2005, Pla de gestió de l'arbrat viari (ch. 3 block)
naciodigital2026           Nació Digital, 4 May 2026 (press; ch. 3 block)
beteve2026                 Betevé, May 2026 (press; date to confirm; ch. 3 block)
santamour1990              Santamour 1990 (ch. 3 block, matrix #139)
kendal2014                 Kendal, Dobbs & Lohr 2014 (ch. 3 block, matrix #140)
mannucci2025               #51  Mannucci et al. 2025 (ch. 4 block)
nicol2026                  #28  Nicol et al. 2026, SylvCiT (ch. 4 block)
dong2026                   #85  Dong et al. 2026 (ch. 4 block)
Not cited with a key: Parcs i Jardins 2013 "Diversificació d'espècies" (internal; machine translation read; check the
Catalan original before adding a reference).
-->
