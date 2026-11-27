# Discussion {#sec:discussion}

<!-- Draft 1, 26 Nov 2026. Every number comes from thesis/results_numbers.md (needle-fix state, PR #184), whose rows name
their CSV. Other sources: notes/topic_decision.md §10.5, §11; notes/tutor_feedback_24nov.md §1g, §3b, §3d, §3g, §3h;
notes/transferability.md §1–§6; notes/methodology.md l.74; scripts/make_final_new.py (n_limits, n_impact);
notes/mataro_transfer_test.md. Items marked TO UPDATE wait for runs that are not final. -->

This chapter reads the results of Chapters 6 and 7 against the question of Chapter 1. It first answers each sub-question and hypothesis with a verdict. It then says where the method loses or does not matter, how sure we can be, and what its limits are. It ends with how far the method travels and what it could change for the city.

All numbers are for the balanced layout (summer 0.50, winter 0.25, runoff 0.25), with Barcelona's 30-species palette, unless stated otherwise. Shade is given as a share of today's shade.

## Answers to the sub-questions {#sec:disc-answers}

@tbl:verdicts summarises the answers. The paragraphs after it give the evidence for each.

| Question | Verdict | Main evidence |
|---|---|---|
| SQ1 heat (proxy) | Supported | Porta: 106.7% of today's summer shade, against 99.0% for city practice; back-test: 23 of 26 groups |
| SQ1 heat (UTCI) | Not yet answered | Proxy ranks points as Ladybug does (r = −0.73); UTCI on one street is TO UPDATE |
| SQ2 runoff | Equal (do no harm holds) | Total runoff 17,641.1 vs 17,661.0 m³ (−19.9 m³), below the 91 m³ the model resolves; hotspot runoff 2,698.8 vs 2,704.7 m³ (not tested against Δmin); never worse at the hotspots in the back-test (0 of 26) |
| SQ3 trade-off | Heat–runoff: no trade-off; summer–winter: yes | Summer-only and runoff-only layouts within 0.4 pts and 0.8 m³ of each other; winter-only layout at 74.9% summer shade |
| SQ4 additions | Partly; TO UPDATE | 267 candidate spots, 153 free; the additions run is pre-fix |
| H1 | Supported on the proxy | No worse than practice on runoff, better in summer, winter shade 99.2% of today |
| H2 | Not supported as stated | The top genus changes, but the heat and runoff results barely do |

: Verdicts on the sub-questions and hypotheses (Porta unless stated). {#tbl:verdicts}

**SQ1, heat.** On the shade proxy the answer is clear.

- **Porta:** replacing the 832 planes, the method keeps 106.7% of today's summer shade, against 99.0% for city practice and 100.2% for the announced mix. That is +7.7 points over practice. A random choice of fitting species keeps 91.4%, so the gain comes from the choice, not from the palette alone.
- **The city's own plan:** for the 513 planes Parcs i Jardins plans to change, the method at the same diversity as the plan gives 101.4%, against the plan's 98.2%.
- **Back-test:** in 23 of the 26 groups the city really replaced, the method's species, at the same positions and trunk size, give more summer shade per tree. The median rises from 76 to 130 m²·h per tree, 1.7 times.

The question was asked in UTCI, and UTCI is not yet computed for the method's layouts at Porta scale. What we have is a check of the proxy against Ladybug: the proxy ranks points as Ladybug does (r = −0.73 across points today, r = −0.82 on the change between layouts), with a slope of about −0.5 °C of UTCI per hour of full shade. That supports the ranking, not a temperature. **TO UPDATE:** the Ladybug UTCI run on one street (today, city practice, method). Until then, the thesis reports shade, not degrees.

**SQ2, runoff.** The method does no harm, and it does no measurable good.

- In Porta, hotspot runoff in the 2-year, 60-minute storm is 2,698.8 m³ for the method, 2,704.7 m³ for city practice and 2,702.8 m³ today. The differences are a few cubic metres.
- The smallest difference the model can resolve is 91 m³. It comes from the error of the interception calibration, spread over all of Porta's street crowns (Chapter 6). Every total-runoff difference between layouts in Porta is far below it (method against practice, −19.9 m³), so the honest verdict is "equal". Hotspot runoff is reported but not tested against Δmin, which was derived for total runoff.
- In the back-test, the method's hotspot runoff is never higher than the city's choice (0 of 26 groups). In Mataró it is never worse than any practice (6 of 6 streets), although every replacement, the method's included, runs 0.3–1.2% above today's planes.

This is why runoff is a check in H1 and not a target. At the scale of a design storm, the choice of species among trees of the same trunk size moves interception by a small share of the rain. Pits, grouping and sealed surfaces matter more (Chapter 2).

**SQ3, trade-off.** The answer splits in two.

- **Heat against runoff: no real trade-off.** The summer-only layout gives 106.9% summer shade and 2,698.9 m³ hotspot runoff. The runoff-only layout gives 106.5% and 2,698.1 m³. Both objectives follow the same trait, crown area times leaf density, so the layout that is best for one is nearly best for the other. The front between them collapses.
- **Summer against winter: a real trade-off.** The winter-only layout, which keeps the most winter sun, falls to 74.9% of today's summer shade. The summer-only layout casts 107.8% of today's winter shade. Crown size drives most of this, and leaf habit adds to it: the winter-only layout chooses small crowns, many of them evergreen (*Citrus*), and still casts the least winter shade. The balanced layout sits between the two, at 106.7% summer and 99.2% winter shade.

**SQ4, additions.** Of 267 candidate spots on Porta's sidewalks, 153 are free, 103 are conditional on moving an object (a sign, a crossing, a lamp, a bollard, a bus stop) and 11 are blocked by traffic lights or driveways. Additions in the free spots raise shade and lower runoff in every run so far. The additions run, however, still uses the 7-species palette and the crowns from before the needle fix. **TO UPDATE:** the rerun with the 30-species palette, and the share of the gap to 30% cover that the spots close.

**H1, do no harm.** On the proxy, H1 holds in Porta on each of its parts:

- no worse than city practice on runoff (equal within what the model resolves);
- better in summer (+7.7 points);
- no more winter shade than today (99.2% of today; city practice casts 109.4%).

It also holds against the city's per-tree plan (+3.2 points in summer, 98% against 104% winter shade, equal runoff), in 23 of 26 back-test groups, and in 6 of 6 Mataró streets. The verdict is "supported on the shade proxy". It becomes "supported" only once the UTCI check agrees.

**H2, heat-best and runoff-best layouts differ in species.** Only weakly. Among the new trees, both corner layouts are led by *Firmiana simplex* (419 in the summer-only layout, 305 in the runoff-only layout), followed by *Tipuana* and *Gleditsia* in different proportions. The difference does not matter for either objective, as SQ3 shows. H2 assumed that species would trade cooling against interception, through leaf habit or transpiration. In the method as built, both objectives follow crown area and leaf density, transpiration is not modelled, and the species that cast the largest crowns win on both. H2 is therefore not supported as stated. The trade-off the method does find is between summer and winter, and that is where a designer's choice of weights matters.

<!-- New trees per corner layout = species columns minus S0 counts, tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv:
S4_s1.00_w0.00_r0.00 Firmiana 419, Tipuana 156, Gleditsia 82; S4_s0.00_w0.00_r1.00 Firmiana 305, Tipuana 174, Gleditsia 161. -->

**Why the method works.** The result so far shows *that* the method gains, not *where* the gain comes from. A decomposition is planned on the back-test groups and on Porta. It compares:

1. city practice;
2. the same species, placed optimally (only the positions change);
3. the method with the city's 7 species;
4. the full method with 30 species.

The differences between these steps separate the gain from placement, from species choice and from a wider palette. **TO UPDATE** when the runs finish. One part is already known: in Porta, the 7-species palette gives 99.3% against 106.7% for the 30-species palette. Across the 32 screened barris, the narrow list costs a median of 5.0 points (pre-fix runs).

## Where the method loses, or does not matter {#sec:disc-loses}

A method that wins everywhere should be distrusted. This one does not.

- **It loses in some places.** In 3 of the 26 back-test groups, the city's choice gave more summer shade per tree than the method's. With a stricter reading of the sizing rule, which caps small species at the guide's limits, the method wins 20 of 26. With only the façade test and no sizing rule, it wins 15 of 26. So the margin depends on how the city's rules are read, and the headline reading (23 of 26) is the 2011 guide's own.
- **Runoff does not move.** Every total-runoff difference in Porta is below what the model resolves. The method can claim "no worse", never "better".
- **Diversity falls without a floor.** Left free, the balanced layout puts 423 of the 832 positions, 50.8%, on one species, *Firmiana simplex*. Its effective number of species is 5.7, against 15.9 for city practice. The 15% cap is respected: read within Porta, it allows 423 trees per species (15% of 2,825), and for a species new to Porta that is half of the 832 new trees. But a neighbourhood with half its new trees of one species repeats the plane's problem on a smaller scale. A diversity floor fixes this cheaply (Chapter 7):
  - matching the announced mix's diversity (9.4 effective species) costs 0.4 points of summer shade, and the top species falls to 35.6%;
  - matching city practice's diversity (15.6) costs 1.6 points, and the method still beats practice, at 105.1% against 99.0%.
  The thesis therefore recommends running the method with a floor at least equal to city practice's diversity. It treats the result without a floor as a bound, not as a proposal.
- **Winter is a cost.** Any layout that maximises summer shade also casts more winter shade, unless winter is weighted. The balanced layout keeps winter shade at today's level, which is H1's condition. A designer who drops the winter weight gets more summer shade and darker winters.
- **Carbon drops with any replacement.** At equal trunk size, every replacement starts with less stored carbon than today's mature planes. The method keeps 69% of today's stock against 52% for city practice, but neither comes close to today. Pollen is not resolved: at its lower bound the load falls to 5–9% of today's with any replacement, but at the upper bound it ranges from 45% to 107% of today's (106.5% for the method), because only 35% of the method's new trees have a pollen score.

## How sure we are {#sec:disc-confidence}

Four kinds of uncertainty bear on the results.

**The heat proxy is a ranking, not a temperature.** It agrees with Ladybug on which points are hotter (r = −0.73) and on which layout change cools more (r = −0.82). Ladybug itself treats trees as shade only and underestimates vegetation cooling against ENVI-met [@mannucci2025]. Both errors push in the same direction: they understate what trees do. Whether they could reverse a ranking between species has not been tested.

**The crowns came from LiDAR, and one error was found and fixed.** In November the segmentation was found to produce tall, narrow "needle" crowns where neighbouring trees shared canopy cells. The fix gave contested cells to the nearest tree and took each tree's height near its own trunk. It cut Porta's needle trees from 136 to 27, with the total crown area unchanged. The Porta replacement runs, S1c, the diversity series, the co-benefits, the back-test and the city LP were redone; the 30-species barri runs, the additions and the UTCI runs are still pre-fix. The method's lead held in every repeated comparison:

- 30 species: method 103.4% → 106.7%; city practice about 95.5% → 99.0%;
- 7 species: method 98.3% → 99.3%.

The episode shows that the results depend on crown geometry, and that the comparison between layouts is more robust than any single number.

**Some results still rest on approximations.**

- **The 32 barris:** the 30-species runs date from before the needle fix. Their medians (91.1% summer shade, +6.7 points over the announced mix, +8.2 over city practice, ahead of both in 32 of 32 barris) are **TO UPDATE**.
- **Mataró:** each tree takes the median crown of its species in Barcelona's LiDAR, not its own. The run with Mataró's own 2021 LiDAR is **TO UPDATE**.
- **Florence:** the full transfer test is **TO UPDATE**.
- **Underground services:** the free spots are an upper bound. Real utility plans exist for one project area only and cannot be published. The public tool will use a synthetic layer, and the thesis reports the real-plan check only as counts.

**The parameters are sourced or declared.** Every parameter in the code is either cited or marked `ASSUMPTION` (Appendix A). The interception rate is calibrated on Freiburg field data [@anys2024]. The sensitivity to the interception rate is reported in Chapter 6, and the palette comparison (30 against 7 species) in Chapter 7.

## Limits {#sec:disc-limits}

The method takes the following as given. Each limit is a place where a result could change if the assumption were dropped.

- **New trees at today's size.** Each species enters at its median crown in Barcelona's LiDAR, at equal trunk size. Growth over the decades after planting is not modelled, nor are mortality and pruning. The comparison is fair between species; it is not a forecast.
- **Heat as shade on a hot day.** The optimiser scores shade with a fast proxy, checked against Ladybug; the Infrared City check is still to come. It is not a full microclimate simulation of each layout. Transpiration is not modelled: Ladybug is shade-only [@mannucci2025], and a meta-analysis found transpiration cooling lowest in Mediterranean climates and, separately, for trees in paved pits [@rahman2020meta].
- **One weather file.** The design days come from an airport weather file, which differs from a dense street canyon.
- **One interception rate.** 1.75 mm per unit of leaf area is calibrated on two temperate species [@anys2024]. Species-specific rates would not change the ranking, since the ranking follows leaf area.
- **Runoff barely moves.** All differences between layouts are below what the model resolves, so runoff stays a do-no-harm check.
- **Canopy from a height model.** The canopy height model counts everything above 2 m, tall shrubs included.
- **Free spots are an upper bound.** There are no open data on underground services, and conditional spots need a field check.
- **The cap counts street trees only.** The city's plan also counts trees in squares, about 201,600 trees in all [@ajuntament2017arbres]. A Parcs i Jardins document of 2013 also asks for 15% per district, while the institute wrote in November 2026 that the cap is city-wide. The thesis counts street trees only, and the Porta and barri runs read the cap within the neighbourhood (15% of its street trees, Chapter 5); the city LP applies one city-wide cap. Both readings are declared simplifications.
- **Baselines partly from the press.** The announced mix (S1a) comes from press reports. City practice (S1b) comes from the city's own inventory, and that is why it is the reference.
- **Licences.** The flood hazard layer, the Mataró inventory and the utility plans carry restrictions. Only aggregates are published.

<!-- Limits list: scripts/make_final_new.py n_limits + thesis/outline.md §8.2 (transpiration; airport weather file; CHM shrubs;
press-sourced 2026 mix; licences). 2013 document vs Coloma Rull's 24 Nov email: notes/tutor_feedback_24nov.md §2 and D4.
~201,600: thesis/03_barcelona_rules.md (ajuntament2017arbres pp. 18–19). rahman2020meta: as cited in thesis/02 §2.5. -->

## How far the method travels {#sec:disc-transfer}

The code is site-agnostic. The evidence is not. Moving the method means rebuilding local data and re-deriving local parameters, and four degrees of transfer differ in cost (@tbl:transfer).

| Degree | Case | What it needs | Status in this thesis |
|---|---|---|---|
| T0 | Another Barcelona neighbourhood | Nothing new: the same inventory, LiDAR, rainfall curves and flood model cover the city | Done: 32 barris (pre-fix, TO UPDATE), back-test across the city |
| T1 | Another Mediterranean city with mature open data | A new site adapter; traits, leaf calendar and rainfall curves re-derived; the decision redefined | Mataró done (approximate crowns); Florence TO UPDATE |
| T2 | A city with no leaf-on point cloud, or no species inventory | As T1; the design front-end still works if the designer supplies the positions | Not attempted |
| T3 | Another climate | Interception rate, leaf calendar, storm season and design days all lose their anchors | Not claimed |

: Four degrees of transfer. {#tbl:transfer}

Three inputs do not travel easily:

- **A classified, leaf-on point cloud.** Leaf density drives both objectives, and a surface model alone gives crown width but not density.
- **A pluvial flood map.** The tool's own flow routing finds the main convergence points but is not a flood map (Chapter 6).
- **Traits and phenology.** These must be re-derived for each city.

The question also travels less well than the method. Barcelona's 15% cap and its plane reduction make "which species replaces this plane" a live decision. Elsewhere the decision has to be restated, for example as the species for trees removed in the normal renewal cycle, with a diversity constraint in place of a named palette. The optimiser does not change; who supplies the positions and the cap does.

Mataró shows the method surviving a first transfer. On six streets, it keeps 83% of the planes' shade against 63% for Barcelona's practice and 50% for Mataró's own recent plantings. It wins on all six streets, with runoff never worse than any practice.

<!-- notes/transferability.md §1 (T0–T3), §3 (three things that do not travel), §5 (the question travels less well), §6.
Mataró: thesis/results_numbers.md §7. -->

## What the method could change {#sec:disc-impact}

**Who decides, and where the tool enters.** In Barcelona the city approves and pays for street projects, and Parcs i Jardins manages the trees, sets the diversification criteria and decides the species for each pit. The utility companies supply the plans of the services under the sidewalk, and residents can comment during the public display of a project. The tool enters at the point where a designer proposes species for a project area and Parcs i Jardins reviews them. It gives both of them the same numbers: what each allowed choice keeps or loses in shade, winter sun and runoff, against city practice and against today. Whether Barcelona's street projects are mostly designed in-house or by commissioned firms has not been verified, and the thesis makes no claim about it.

**Same works, same cost.** The method replaces the same trees as city practice, at the same positions, so the works and their cost are the same. The cost of the choice is zero. Only the species change. Where the method also moves a tree or widens a pit, the costs are known:

- up to 500 € for a full replacement (the Diputació de Barcelona's subsidy cap);
- 502 to 2,867 € to move a tree with a tree spade, for root balls of 90 to 300 cm;
- about 100 € to widen a pit from 1 to 1.5 m².

**The 10 M€ question.** The tutor asked what the method would change with a budget of ten million euros. A rough scale-up of the back-test gives an order of magnitude, not a forecast:

- at up to 500 € per replacement (a subsidy cap, not a unit cost), 10 M€ pays for up to about 20,000 replacements;
- at the observed rate of about 1,300 species-changing replacements a year, that is about 15 years of the city's replacements;
- chosen with the method instead of city practice, each new tree would give 1.7 times the summer shade (back-test median), for the same money, with runoff no worse.

Two caveats stay attached to this statement. It is shade, not degrees, until the UTCI check is done. And it holds at equal trunk size, so it describes the trees the city plants, not the trees they will become.

**What the city would gain beyond shade.** The method makes visible something the current rules do not: the cost of each rule. Running it with and without a constraint shows what that constraint costs in shade. Matching city practice's diversity costs 1.6 points in Porta, and a 7-species palette costs a median of 5.0 points across the 32 barris (pre-fix). These are policy numbers. They let the city decide, for example, whether a wider palette is worth its management cost, with the trade-off in front of it.

<!-- Who decides: notes/tutor_feedback_24nov.md §3d (verified items only; the in-house vs commissioned question is listed
there as NOT verified). Cost: thesis/results_numbers.md §10 (DIBA Catàleg 2024–2027; CYPE Generador de precios). 10 M€:
§10 and scripts/make_final_new.py n_impact. Policy angle: notes/tutor_feedback_24nov.md §3h. -->

<!--
PROVISIONAL CITATION KEYS → references (keys as in thesis/02–05)
mannucci2025          #51  Mannucci et al. 2025, City Environ. Interact. (ch. 2/4 blocks)
anys2024              #1   Anys & Weiler 2024, Hydrol. Processes (ch. 2/5 blocks)
rahman2020meta        #38  Rahman et al. 2020, Build. Environ. 170:106606 (ch. 2 block; the notes call it "Rahman 2019")
ajuntament2017arbres  Ajuntament de Barcelona 2017, Arbres per viure (ch. 3 block)
Data and grey sources without keys yet (Appendix B): Diputació de Barcelona, Catàleg de serveis 2024–2027 (500 €/tree);
CYPE Generador de precios (tree spade, pit widening); Parcs i Jardins per-tree plan for Porta (2026, private, credit only).
-->
