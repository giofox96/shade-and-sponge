# Street trees, heat and pluvial runoff: mechanisms and traits {#sec:mechanisms}

<!-- Draft 1, 26 Oct 2026. Sources: notes/lit/literature_matrix.csv (row ids given in the key table at the end),
notes/topic_decision.md §6.1, notes/methodology.md §4b and §5, notes/decisions/leaf_state_inat.md,
notes/decisions/heat_objective.md, notes/decisions/hypothesis_tests.md §2, databases/data_inventory.md §1, §6.
Citation keys are provisional; align them with the Better BibTeX export. -->

The method in this thesis chooses tree species by the traits that change two outcomes: pedestrian heat stress and storm runoff. This chapter reviews what the literature says about how a street tree acts on each one, and which traits matter. It covers six topics:

- the flood type that trees can plausibly affect;
- rain interception by crowns;
- infiltration through tree pits;
- shade and pedestrian heat;
- evapotranspiration, and why it stays outside the model;
- leaf phenology.

The chapter ends with where the two objectives agree and where they pull apart, since that decides whether a trade-off exists at all.

## Which floods street trees can affect {#sec:mech-floodtype}

Urban floods differ in where the water comes from:

- **Fluvial** floods come from rivers and culverted streams.
- **Pluvial** floods come from intense rain on sealed surfaces, before the water reaches a watercourse.

Trees act on the second type. A crown can hold the first millimetres of a storm, and a pit can let some water into the soil. Neither changes the peak of a river or the response of soil that is already saturated.

The evidence from the cities first considered for this thesis shows why the distinction matters:

- **Bologna:** the urban flooding of 19 October 2024 came from small, partly culverted streams (Ravone, Savena, the Navile canal) overflowing after intense rain on saturated soils [press: @ilpost2024]. That mechanism is mixed, not purely pluvial, and it was one reason Bologna was dropped as a case.
- **Florence:** the city is exposed to pluvial and flash floods from its minor network and a combined sewer of about 800 km, much of it from the 19th century. Its hotspots lie in flat, highly sealed districts, the historic centre among them [@pacetti2022].
- **Barcelona:** recurrent intense-rain flooding in dense districts is mapped in the city's Resilience Atlas, and that map is what selected Porta (Chapter 1).

This thesis therefore addresses pluvial runoff from frequent, short, intense storms. Floods driven by rivers, and extreme events on saturated ground, are outside what a choice of street-tree species can change. They are stated as a boundary of the method (Chapter 1).

## Rain interception by tree crowns {#sec:mech-interception}

Interception is the rain that a crown holds on its leaves and bark and returns to the air by evaporation, so that it never reaches the ground as runoff. Field studies of urban trees agree on its order of magnitude and on what controls it.

**How much a crown holds.** A review puts the typical retention of foliated crowns at the first 2–4 mm of a storm [@kuehler2017]. Measured storage per unit of leaf and stem surface ranges widely:

- 0.87 mm for *Platanus × hispanica*;
- 0.51 mm for *Pyrus calleryana* 'Bradford';
- a mean of 0.86 mm across twenty species [@xiao2016, Table 4].

The rainfall-simulator study behind these values used young branch samples, so they may underestimate mature trees.

Two studies on a lime and a maple in Freiburg, and on a birch and a pine in Ljubljana, show the range in the field:

- **Freiburg:** across 76 events from April to September 2021 (leaf-on), eight trees per species intercepted on average 70.3% of rain for small-leaved lime and 54.8% for Norway maple [@anys2024]. The mean event was small, 6.7 mm.
- **Ljubljana:** over three and a half years, a birch intercepted 23.7% and a pine 46.9% of gross rain [@zabret2019water].

**What controls it.** Interception rises with leaf area index (LAI), the leaf area per unit of ground area:

- In Freiburg, relative interception correlated with LAI and with plant area index (adjusted R² > 0.45), and LAI fell at the more sealed sites [@anys2024].
- In Seoul, LAI and mean leaf area explained the differences between four species, while leaf angle and crown shape did not [@yang2019].

Interception also falls as storms grow:

- In Ljubljana the intercepted share fell for events larger than 6 mm with intensities above 1.8 mm/h, the category cut-offs of the authors' analysis [@zabret2019water].
- In San Juan, tree type mattered for low and moderate storms but not for heavy ones above 7.6 mm/h [@nytch2019].
- In Melbourne, two eucalypts that differed clearly in interception for a 2 mm event barely differed above 12 mm [@livesley2014].

**Leaf-off.** Deciduous trees lose much of their storage in winter:

- leaf-off cut the storage of a young *Platanus × acerifolia* by about 90% [@baptista2018];
- a leafless birch intercepted 32% of an event on average, against 51% in leaf [@zabret2018];
- a modelled 40-year crown held 85% of a five-minute, two-year storm in leaf and 16% leafless [@xiao2016].

**What it adds up to.** At the scale of a street, the effect on runoff is small but measurable:

- **Removal experiment:** removing street trees from a catchment raised runoff by 4% of the measured total, summed over the two storm-depth ranges where the change was significant at the 90% level. Peak discharge did not change significantly across all events [@selbig2022].
- **Calibrated model:** a model calibrated on the same site gave avoided runoff of 2.3% of total runoff, against 3.5% from the field data expressed the same way; the two field figures differ in how they are computed. Matching the field data required raising the model's leaf and bark storage to 2.0 mm, well above the 0.07–0.6 mm reported by other studies [@coville2022].
- **Barcelona, city-wide:** 20,170 new street trees raised runoff retention only from 50.18% to 50.76% for a 20 mm event, in a study that treats trees as land cover [@cortinovis2022].

A narrative review found no study that tested the effect of urban forests on peak discharge [@kuehler2017].

The literature therefore supports a modest claim. Species with larger, denser crowns hold more of a frequent storm, and much less of a large one. This is why the runoff objective in this thesis is evaluated on a two-year, one-hour storm, and why the method reports whether a difference between layouts is larger than what the model can resolve (Chapter 6).

## Infiltration through tree pits {#sec:mech-pits}

Water that passes the crown can still infiltrate if it reaches open soil. Tree roots help:

- **Container experiments:** young trees raised infiltration through compacted soil by 63% on average, and by 153% in the more compacted soil [@bartens2008].
- **Root type:** the coarse-rooted black oak and the fine-rooted red maple did not differ.

The street evidence is weaker:

- **Pits:** in a Melbourne street, pits covering 0.3% of their catchment retained a median of 11% of its runoff [@grey2018]. In the authors' model, exfiltration into the soil removed at least 88% of the water the pits held, and the young trees' transpiration about 4%.
- **Trenches:** next to stormwater trenches, established trees transpired 0.7–6.2 mm per day per unit of canopy area, and their transpiration was equal to 17% of the annual runoff [@thom2020].
- **Species choice:** in a study of young potted trees for passively irrigated pits, species differed in water use, so pits could be planted to empty faster [@thom2022].

These studies concern pit design and soil more than species, and the Barcelona data give no pit size or soil per tree. Pit infiltration is therefore not a species trait in the method; Chapter 5 treats pits as part of the fixed surface.

## Shade and pedestrian heat {#sec:mech-shade}

A tree cools the space under it in two ways:

- it blocks radiation from the sun and from hot surfaces, which lowers the mean radiant temperature (MRT) felt by a pedestrian;
- it transpires, which cools the air.

In Melbourne streets during heat events, the radiative effect dominated pedestrian comfort. Trees cut the Universal Thermal Climate Index (UTCI) mainly through MRT, and on a 41.1 °C day unshaded stations exceeded 46 °C UTCI while shaded ones did not. Air temperature under the trees was on average only 0.2–0.6 °C lower, at most 1.5 °C, and the difference was not statistically significant [@coutts2016].

The heat objective in this thesis is therefore UTCI, which combines air temperature, humidity, wind and MRT.

**What controls shade cooling.** A meta-analysis of 26 field studies (13 of them on surface cooling) found canopy density, expressed as LAI, to be the strongest driver of surface cooling under trees: about 4 °C of surface cooling per unit of LAI [@rahman2020meta]. Two other results of that study bear on Porta:

- **Surface:** cooling was largest over asphalt, 6.2 °C more than over grass.
- **Climate:** surface cooling was among the largest in Mediterranean climates, together with tropical and steppe ones, while air cooling was lower there than in Oceanic and Continental climates. Only two of the 26 studies came from subtropical and tropical climates, so the authors flag a possible bias.

Single-tree studies add detail:

- **Bolzano:** under solitary trees, median maximum surface temperatures fell by about 18–20 °C from sun to shade, and LAI ranked among the top predictors of cooling [@speak2020].
- **Munich and Würzburg:** a denser *Tilia cordata* cooled asphalt about twice as much as *Robinia pseudoacacia* [@rahman2019; @rahman2020agric].
- **Four Central European cities:** low crown bases and dense, large canopies gave better shade [@helletsgruber2020].

Not every study finds the effect. Across 471 trees in Sydney, LAI, crown area and height had no systematic relation to the sun–shade surface difference. The surface material mattered more, from −17.5 °C over concrete pavers to −24.8 °C over bark mulch [@kaluarachchi2020].

**Seasons.** Shade is a benefit in summer and a cost in winter:

- **Lisbon:** in a modelling study, a *Tipuana tipu* lowered physiological equivalent temperature by up to 15.6 °C on a summer afternoon. Because it keeps its leaves in winter, it also lowered it by up to 2.7 °C at a winter noon, which the authors call overshading [@santosnouri2018].
- **Shanghai:** an optimisation found the best summer LAI at 4.6 and the best winter LAI at 0.6 [@peng2026].

This seasonal conflict is the main source of a trade-off in this thesis (see the last section of this chapter).

**Limits of the benefit.**

- **Heatwaves:** extreme heat can thin crowns. After a heatwave above 41 °C in Melbourne, *Platanus* street trees lost about 30–50% of their plant area index, and the canopy's MRT benefit largely disappeared within eleven days [@sanusi2020].
- **Night:** dense tree clusters can trap heat at night. In a Munich square, tree layouts lowered afternoon PET but a grass-only layout was best at 4:00 [@zolch2019].

## Evapotranspiration, and why it stays outside the model {#sec:mech-et}

Transpiration matters for both objectives:

- **Air cooling:** in Seoul, modelled daytime cooling from transpiration was 1.15 °C against 0.43 °C from shade, for a crown radius of 1 m [@park2026].
- **Species differences:** diffuse-porous species, such as *Platanus*, transpire two to three times as much as ring-porous ones (Bush et al., 2008, as cited in @bachofen2025).
- **Soil water:** between storms, transpiration empties the soil and frees storage for the next event [@thom2020].

The method in this thesis does not represent it, for five reasons:

1. **The heat engine cannot see it.** Ladybug Tools, the Tier 1 heat model, treats trees as shade only. It probably underestimates vegetation cooling by about 2–3 °C UTCI [@mannucci2025].
2. **The runoff model is per event.** Transpiration acts between storms, not within a one-hour storm.
3. **The effect is smallest in this setting.** In the meta-analysis above, transpiration per leaf area was lowest in Mediterranean climates (0.55 against 6.96 g m⁻² min⁻¹ in Oceanic ones). It was also about ten times lower for trees in cut-out pits in pavement than for trees over grass [@rahman2020meta]. Porta's street trees stand in paved pits over asphalt.
4. **The data are missing.** The planned proxy, wood porosity, has no measured or classified value for the palette species yet.
5. **The trade-off it was meant to explain cannot act.** An earlier hypothesis of this thesis attributed the heat–runoff trade-off to leaf habit and transpiration capacity. As modelled, that mechanism cannot change either objective, so the hypothesis was restated in terms of crown size and the leaf-on calendar (Chapter 1).

Transpiration is therefore a declared limit, not a variable. Its omission likely makes the method conservative on air cooling. It may also understate the advantage of high-transpiring species such as the plane, which the replacement removes.

## Leaf phenology of the palette species {#sec:mech-phenology}

Because shade is a winter cost and leaf-off cuts interception, the months in which each species carries its leaves enter both objectives. Published calendars for the palette species are scarce, and some do not fit Barcelona.

A phenology study of *Jacaranda mimosifolia* in Bétera, Valencia (2022–2023), recorded leaf fall complete by mid-December and the first new leaves in early April [@gandiaventura2025]. Read as a calendar, that means bare crowns from January to March, which is how this thesis first modelled it. Photographs from Barcelona tell a different story. We scored the first photo of every Barcelona iNaturalist observation of *Tipuana tipu* and *Jacaranda mimosifolia* from December to March: 96 and 74 observations, mostly from 2023–2025.

- **Tipuana:** in leaf in all determinable December and January photos (n = 27 and 20), partly bare in February, and bare in 42% of March photos.
- **Jacaranda:** in leaf in 79% of January photos (n = 14) and 67% in February (n = 24), with no bare crown before March.

The method's leaf calendar follows these photos. The older Valencia-based calendar is kept as a sensitivity variant (Chapter 6).

The photos are an opportunistic sample, not a survey:

- one rater scored them;
- several years are pooled;
- the samples are small, 14–27 determinable photos per month;
- parks are included as well as streets.

## Where the two objectives agree, and where they conflict {#sec:mech-agree}

The evidence above points to a shared driver. LAI and crown size raise both interception [@anys2024; @yang2019] and shade cooling [@rahman2020meta; @speak2020]. A species with a large, dense crown in summer should therefore score well on both, and a heatwave that thins crowns cuts both at once [@sanusi2020].

They conflict in three places:

1. **Leaf habit.** An evergreen crown keeps intercepting through autumn and winter storms, but it also blocks winter sun [@santosnouri2018; @peng2026]. In the Barcelona metropolitan area, about 35 of 45 high-intensity storm episodes in 2014–2022 fell in May–October, when every palette species is in leaf [@esbri2026; values read from its Fig. 4], so the runoff advantage of evergreens is small, while the winter shade cost remains (Chapter 7).
2. **Water.** Transpiration cools the air and needs soil water [@park2026; @pace2025]. It is outside the model (see the section on evapotranspiration).
3. **Surface.** The surface under a tree can matter as much as the species for the cooling it gives [@kaluarachchi2020; @rahman2020meta].

For the method, this means the heat–runoff trade-off may be weak: if crown size and LAI drive both objectives, the best layouts for each may be nearly the same. The trade-off this thesis can expect is between summer shade and winter sun, through leaf habit. Chapter 7 tests both. A collapsed heat–runoff front is an allowed result, not a failure of the method.

The traits the method needs follow from this chapter: crown size, LAI, leaf habit and a monthly leaf calendar. They are measurable per tree from LiDAR and per species from photos. Root traits, transpiration and pit soil are not used. Chapter 5 shows how each trait enters the two models.

<!--
PROVISIONAL CITATION KEYS → literature_matrix.csv row (all read in full unless noted)
pacetti2022        #18  Pacetti et al. 2022, J. Hydrol. Reg. Stud.
kuehler2017        #9   Kuehler, Hathaway & Tirpak 2017, Ecohydrology 10:e1813 (accepted manuscript read)
xiao2016           #3   Xiao & McPherson 2016, J. Environ. Qual. 45:188
anys2024           #1   Anys & Weiler 2024, Hydrol. Processes
zabret2019water    #111 Zabret & Šraj 2019, Water 11:2659
zabret2018         #116 Zabret, Rakovec & Šraj 2018, J. Hydrol. 558:29–41
yang2019           #5   Yang et al. 2019, Landsc. Ecol. Eng.
nytch2019          #110 Nytch et al. 2019, Urban Ecosyst. 22:103–115
livesley2014       #115 Livesley, Baudinette & Glover 2014, Urban For. Urban Green. 13:192–197
baptista2018       #6   Baptista et al. 2018, Hydrol. Processes (accepted manuscript)
selbig2022         #10  Selbig et al. 2022 (online 2021), Sci. Total Environ. 806:151296
coville2022        #11  Coville et al. 2022, Urban For. Urban Green.
cortinovis2022     #69  Cortinovis et al. 2022 (Barcelona)
bartens2008        #16  Bartens et al. 2008, J. Environ. Qual.
grey2018           #77  Grey et al. 2018, J. Hydrol. 565:400–410
thom2020           #78  Thom et al. 2020, Water Res. 173:115597
thom2022           #79  Thom et al. 2022 (online 2021), Sci. Total Environ. 812:151466
coutts2016         #100 Coutts et al. 2016 (online 2015), Theor. Appl. Climatol. 124:55–68
rahman2020meta     #38  Rahman et al. 2020 (online Dec 2019), Build. Environ. 170:106606  [the notes call this "Rahman 2019"]
rahman2019         #102 Rahman, Moser, Rötzer & Pauleit 2019, Urban Ecosyst. 22:683–697
rahman2020agric    #44  Rahman et al. 2020, Agric. For. Meteorol. 287:107947
speak2020          #39  Speak et al. 2020, Landsc. Urban Plan. 197:103748
helletsgruber2020  #40  Helletsgruber et al. 2020, Forests (digest)
kaluarachchi2020   #45  Kaluarachchi, Tjoelker & Pfautsch 2020, Forests 11:1141
santosnouri2018    #81  Santos Nouri et al. 2018, Atmosphere 9:12
peng2026           #53  Peng et al. 2026, Landsc. Ecol.
sanusi2020         #66  Sanusi & Livesley 2020, Urban For. Urban Green. 54:126746
zolch2019          #65  Zölch et al. 2019, Build. Environ. 149:640–654
park2026           #42  Park et al. 2026, Sci. Rep. (digest)
bachofen2025       #43  Bachofen et al. 2025, Urban For. Urban Green. (digest)
mannucci2025       #51  Mannucci et al. 2025, City Environ. Interact.
pace2025           #13  Pace et al. 2025, Sci. Rep. (digest)
ilpost2024         Il Post, 21 Oct 2024 (press; databases/data_inventory.md B7) https://www.ilpost.it/2024/10/21/quarta-alluvione-emilia-romagna/
esbri2026          Esbrí et al. — Characterization of high-intensity storms in the Metropolitan Area of Barcelona (2014–2022), Atmosphere 17(1):41. YEAR UNRESOLVED: repo CSV says 2026, UB repository 2025; confirm (MDPI 403 on 26 Oct). Values read from Fig. 4 (databases/barcelona/storm_months.csv). Matrix row added 26 Oct.
gandiaventura2025  Gandía-Ventura et al. 2025, Biology 14(11):1569 (Bétera 2022–23, BBCH; https://pmc.ncbi.nlm.nih.gov/articles/PMC12650108/). Matrix row added 26 Oct.
bush2008           not read: cited as "as cited in Bachofen et al. (2025)".

the iNaturalist photo scoring is our own analysis (scripts/inat_leaf_state.py, databases/barcelona/inat_leaf_photos.csv).
-->
