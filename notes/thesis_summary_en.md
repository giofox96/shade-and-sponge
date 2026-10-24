# Shade and Sponge: thesis summary (state of 24 Oct 2026)

MaCAD thesis (IAAC). Working title: *Shade and Sponge*. Written to share with colleagues. Source of record: `notes/topic_decision.md` §10 (v7).

## Short version

My thesis is about replacing plane trees in Barcelona. The city will cut its planes by more than half in ten years (press reports). It has rules on how much of each species is allowed and which tree size fits which sidewalk. The only documented rule on which species goes where is a qualitative table from 2004/2005, and in my study neighbourhood, Porta, most plantings do not follow it. Nobody quantifies what each choice does to heat or flooding. Porta already has too little tree cover (20% versus the city's 30% target), so each replacement matters. I am building a tool that picks the replacement species for each position within the city's rules, scores it on pedestrian thermal comfort (UTCI) and rainwater runoff, and compares it with what the city would do anyway. It is a Python engine with a Grasshopper plugin for designers and a web app for non-technical users.

## Abstract

Barcelona will remove more than half of its plane trees within ten years, according to the press. Its tree master plan caps any single species at 15% of the urban fabric, and its 2011 street-tree guide ties tree size to sidewalk width. The only documented rule for choosing the replacement species is qualitative: a 2004/2005 Parcs i Jardins table that assigns species by district and sidewalk width, based on tolerance, typology and tradition. In Porta (Nou Barris), up to about 90% of the plantings on narrow and medium sidewalks do not match it. This is an upper bound, since street rebuilds follow other lists. No rule quantifies what a species choice does to pedestrian heat stress or to storm runoff, and the stakes are high: at equal trunk size, the candidate species carry between a quarter and all of a plane's crown area. Porta already lacks cover (20.1% canopy against the city's 30% target for 2037), and planes make up about 29% of that canopy.

This thesis develops a computational method that works inside the city's replacement rules. For Porta's plane trees, it chooses the replacement species that retain the most pedestrian cooling and rain interception. It scores layouts on mean UTCI over 12-17 h on a hot design day and on runoff from a 2-year, 60-minute design storm, and compares them with the city's own rule-based replacement. The tool is a Python core with two front-ends: Grasshopper/Ladybug for designers, and a web app for non-technical users.

## Research question

Can a trait-based layout method, working inside Barcelona's replacement rules, choose replacement species for Porta's plane trees that retain more pedestrian cooling and stormwater interception than the city's own rule-based replacement?

- **SQ1 (heat):** how does mean UTCI over 12-17 h on a hot design day differ between the city's replacement and the method's layout?
- **SQ2 (runoff):** how does runoff from a 2-year, 60-minute storm differ, in total and at Porta's flood hotspots, and is the total difference larger than what the model can resolve?
- **SQ3 (trade-off):** do the heat-best and runoff-best layouts differ, and in which species?

## Hypotheses

- **H1:** the method beats the city's replacement on both heat and runoff, because crown size and LAI drive both shading and interception. For runoff, a difference smaller than the model can resolve is reported as "not resolved".
- **H2:** the heat-best and runoff-best layouts differ in species, so the trade-off front is not a single point.
- **Declared validity boundary (not a hypothesis):** the runoff benefit shrinks at sewer design level (10-year storm), and extreme events such as 6 Sept 2018 are outside what trees can affect.

## Contribution and validation

The contribution is a quantitative method for a decision the city currently makes qualitatively. It is validated in Porta, with Florence or Mataró as a transfer test. Validation uses interception calibrated on field data (Anys & Weiler 2024), a published Ladybug vs ENVI-met benchmark (Mannucci et al. 2025), and a check of the fast heat proxy against full Ladybug UTCI.

## Five core papers

1. Nicol et al. (2026). *SylvCiT: an AI-based support to urban forest resilience.* PLoS One 21(2): e0339173. doi:10.1371/journal.pone.0339173. The most advanced trait-based species recommender; its runoff module is disabled.
2. Shaamala et al. (2025). *Algorithmic urban greening for thermal resilience: AI-optimised tree placement and species selection.* Cities. doi:10.1016/j.cities.2025.106356. Optimises tree placement and species for UTCI only.
3. Peng et al. (2026). *A workflow for climate-adaptive tree planting design to optimize outdoor thermal environment through evolutionary algorithm.* Landscape Ecology. doi:10.1007/s10980-026-02324-z. NSGA-II with summer and winter UTCI; generic tree types, no runoff.
4. Mannucci et al. (2025). *A parametric integrated workflow to assess multi-domain heat- and flood-related performance of small outdoor urban spaces in a changing climate: a case study in the Mediterranean region.* City and Environment Interactions. doi:10.1016/j.cacint.2025.100215. Heat and runoff in one workflow, for fixed scenarios, nothing optimised.
5. Anys & Weiler (2024). *Rainfall interception by urban trees: event characteristics and tree morphological traits.* Hydrological Processes. doi:10.1002/hyp.15146. Empirical basis for the interception parameter.

## Status and caveats

- The "more than half of the planes (56%)" figure and the 2026 replacement mix come from press reports, not from a municipal document.
- The methodology is still a draft. The tool is a prototype.
- The exploratory runoff comparison (best layout vs the city's baseline) falls below the model's resolution threshold, so it currently reads "not resolved". No final results are claimed.
- Full-Porta UTCI with Ladybug is planned for 4-17 Nov. Next tutor session: 10 Nov 2026.
