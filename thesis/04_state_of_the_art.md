# State of the art: computational tools for urban trees {#sec:sota}

<!-- Draft 1, 26 Oct 2026. Sources: notes/decisions/contribution_statement.md §1–§2, notes/lit/literature_matrix.csv
(row ids in the key table at the end), notes/method_heat_validation.md §1, §3, notes/methodology.md §4–§6,
notes/topic_decision.md §6.1 and §10.2 ("Gap"). Citation keys are provisional; align them with the Better BibTeX export. -->

Chapter 2 showed which tree traits act on heat and runoff. Chapter 3 showed that Barcelona's rules decide how many trees of each species, and of what size, but not what each choice does. This chapter reviews the computational tools that could fill that space, in three groups:

- the models that estimate runoff;
- the models that estimate pedestrian heat stress;
- the methods that recommend or optimise trees.

It ends with the gap this thesis addresses, stated as narrowly as the evidence allows.

## Runoff models for design {#sec:sota-runoff}

Four families of runoff models appear in the studies reviewed.

**Curve-number models.** The SCS curve number method turns rain on a surface into runoff through one parameter per land-cover and soil class. It is the most common choice where runoff is one objective among several:

- a Grasshopper workflow in Ostia that computed a composite curve number next to UTCI [@mannucci2025];
- a city-scale scenario study of Barcelona, Malmö and Utrecht, using InVEST's flood model for a 20 mm event [@cortinovis2022];
- a land-use optimisation of Xiamen, for a 50-year storm [@liang2021].

All three treat trees as land cover, or as part of a composite surface. None separates one tree from another.

**Sewer and catchment models.** SWMM routes runoff through drainage networks. In a 46 ha catchment in Sendai, SWMM coupled with a canopy energy-balance model showed that scaling LAI by 1.4 cut summer runoff by 10.7% and peak flow by 7.8% [@wu2024]. LAI and canopy storage came from satellite NDVI, by parcel, without species.

**i-Tree Hydro and i-Tree Eco.** These tools estimate the runoff avoided by tree cover. At a Wisconsin site, i-Tree Hydro with default parameters predicted nearly twice the total runoff of the calibrated model, and about a third (34%) of its avoided runoff. Matching the field data needed extensive calibration, including a leaf and bark storage of 2.0 mm [@coville2022]. i-Tree Eco values per species also drive the most recent species optimiser ([below](#sec:sota-optimisers)).

**Per-tree interception models.** A per-tree Rutter–Gash model makes storage a function of LAI and bark area, with throughfall validated at R² 0.83 [@eslami2025]. Applied to a pilot area in Copenhagen, it gave a 15.2% runoff reduction for one leaf-on summer event, with local contributions of 2–43% depending on tree characteristics. The authors flag species-specific storage and the LAI parameterisation as open problems. The source is an extended conference abstract.

**What this means for the method.** For a street-tree choice in Porta, the model has to:

- resolve single trees and their crowns;
- run fast enough to score hundreds of layouts;
- use parameters that can be calibrated on open data.

Curve-number and catchment models do not resolve single trees. No field data to calibrate i-Tree for a Barcelona street were found, and its defaults are meant for catchments of 25–250 km² [@coville2022]. The method therefore combines a per-tree storage term, calibrated on open field data, with the curve number for the surface below (Chapter 5).

## Heat models for pedestrian comfort {#sec:sota-heat}

Pedestrian heat stress is usually expressed as UTCI or physiological equivalent temperature (PET). Both depend strongly on mean radiant temperature (MRT), and so on how a model treats tree crowns.

**Ladybug Tools.** Ladybug runs inside Grasshopper, the environment of the primary user of this thesis. In its fast outdoor-comfort path (Human-to-Sky relation and Outdoor Solar MRT), tree crowns are context geometry that blocks rays and nothing else: there is no transmittance and no LAI. Honeybee's UTCI comfort map can take a transmittance modifier for plants, at a much higher computing cost. In the fast path, two consequences follow:

- **Shade MRT is too low.** Under one camphor tree in Shanghai (LAI 3.2), measured MRT was 46.5–48.6 °C. Standard Ladybug gave 42.1–44.0 °C, with the largest gaps, over 6 °C, between 13:00 and 15:00. Multiplying direct radiation under the crown by a transmittance τ = exp(−0.5·LAI) brought it to 45.2–46.5 °C, within 2–4 °C of the measurement [@peng2026].
- **Transpiration is missing.** Against ENVI-met in a square in Ostia, Ladybug's UTCI had a mean bias of 0.8–2.3 °C and a CVRMSE of 7–13%. Its MRT was worse, with a CVRMSE of 22–38% and the largest errors under direct sun. The authors estimate that treating trees as shade only underestimates vegetation cooling by about 2–3 °C UTCI [@mannucci2025].

**ENVI-met.** ENVI-met simulates air flow, radiation and vegetation together, including transpiration. It is among the most used tools and a common reference for Ladybug, as in the Ostia comparison [@mannucci2025]. In a Lisbon validation against climate walks, its UTCI RMSE was about 2 °C [@silva2025].

**SOLWEIG.** SOLWEIG models MRT with a canopy transmissivity. In three squares of Gràcia, Barcelona, it was compared against globe-derived MRT [@colaninno2025]:

- **Sunlit points:** simulated MRT was 6.6–8.7 °C above the measurement on one day.
- **Shade under plane rows:** the result moved by about 2.5 °C when the canopy transmissivity rose from 3% to 10%.

**CFD coupling.** In Chicago, a workflow coupled Honeybee radiation, with species-specific canopy transmittance, to OpenFOAM, with trees as porous media that emit heat and vapour [@tanliu2026].

**Cost.** Accuracy has a price in time:

- Ladybug UTCI for one configuration of 42 trees took 20–25 minutes [@shaamala2025].
- On a 25 × 36 m site, one evaluation took 10–20 seconds at first, with the time rising during the run, so a run of 200 evaluations took 2–3 hours [@peng2026].
- Optimisers over larger areas therefore replace the simulation with a surrogate. A random-forest surrogate trained on 1,500 simulations predicted site-mean UTCI with an RMSE of 0.09 °C [@tanliu2026]. U-Net surrogates trained on SOLWEIG predicted point-wise MRT with an L1 error of 1.93 K, up to 400,000 times faster for decade-long aggregates [@schrodi2023].

**No study found reports the error of Ladybug Tools, standard or τ-corrected, against measured MRT under Mediterranean street trees.** The closest evidence is the SOLWEIG study in Barcelona [@colaninno2025] and the single camphor tree in Shanghai [@peng2026].

The method therefore uses a fast shade proxy inside the optimiser. Ladybug UTCI, with the τ correction, checks the final layouts, and the known Ladybug–ENVI-met error is the reference for how much of a difference can be trusted (Chapters 5 and 6). A commercial fast UTCI service, Infrared City, is a candidate replacement for the Ladybug step. Access is not yet confirmed.

## Recommenders and optimisers {#sec:sota-optimisers}

Table 4.1 sets the closest studies against five properties that a tool for Porta's replacements needs:

- **Pedestrian heat:** heat measured as UTCI, PET or MRT at street level.
- **Runoff:** event runoff from rain on the site.
- **Species from traits:** species chosen from measured or modelled traits.
- **Tree positions:** individual tree positions as decision variables.
- **Optimises:** searches the design space rather than testing a few scenarios.

| Study | Pedestrian heat | Runoff | Species from traits | Tree positions | Optimises |
|---|---|---|---|---|---|
| SylvCiT [@nicol2026] | no | module disabled | yes (diversity traits) | no (species and functional groups for a selected area) | recommender |
| @mannucci2025 | UTCI | curve number | no | fixed scenarios | no |
| @wu2024 | surface temperature | SWMM | no (LAI scaling) | no | no |
| @cortinovis2022 | heat index | curve number | no | no | no |
| @liang2021 | surface temperature | curve number | no (land cover) | no | yes |
| @nyelele2021 | heat index | i-Tree Hydro | no (all species pooled) | no (canopy area per block group) | yes (LP) |
| @dong2026 | building energy (proxy) | i-Tree Eco | i-Tree Eco values | no (species shares per cell) | yes (NSGA-III) |
| @shaamala2025 | UTCI | no | by morphology | yes | yes (ant colony) |
| @peng2026 | UTCI | no | generic tree types | spacing pattern only | yes (NSGA-II) |
| @hao2023 | UTCI | no | no (identical trees) | yes | yes (GA) |
| @elkhateeb2025 | shade, MRT | no | no (crown size only) | yes (hypothetical sites) | yes (Galapagos) |
| @oneto2026 | shading | no | matched afterwards | layout type (rows) | ranking + ML |
| @schrodi2023 | MRT | no | no (uniform trees) | yes | yes (local search) |
| @tanliu2026 | UTCI | no | species-specific crowns (US allometry) | yes (30 trees) | yes (NSGA-II) |
| @langenheim2022 | winter sun (qualitative) | flood maps (qualitative) | four tree types | rule-based per position | no |

: Table 4.1. Studies closest to the task, by the properties a Porta replacement tool needs. All were read in full; Eslami et al. (2025), cited in the text, is an extended abstract.

Three groups emerge.

**Heat optimisers that ignore runoff.** Most optimisers place trees for heat alone:

- **Ant colony:** the Bongaree study cut mean UTCI from 38.31 to 37.75 °C over 100 iterations. Its authors name multi-objective optimisation with water sensitivity as future work [@shaamala2025].
- **Generic tree types:** the Shanghai study found the best summer and winter LAI, but for tree types, not species [@peng2026].
- **Identical trees:** the Hong Kong study and the Freiburg U-Net study place trees that are all the same [@hao2023; @schrodi2023]. In Hong Kong, the best arrangement of 55 trees was 0.1 °C cooler than the status quo in site-mean UTCI, and the worst 0.2 °C warmer [@hao2023].
- **Crown size only:** the Cairo study optimises positions and canopy radii, on hypothetical sites [@elkhateeb2025].

The closest is the Chicago study. It optimises the species and positions of a fixed set of 30 trees for UTCI, CO₂ uptake and diversity, with NSGA-II, species-specific crowns from US allometry and a surrogate. Its best layout lowered site-mean UTCI by 1.36 °C against no trees [@tanliu2026]. It has no runoff objective and no field validation.

**Heat-and-runoff studies that do not choose trees.** Several studies assess both hazards, but none chooses trees:

- **Fixed scenarios, no species:** the Ostia workflow computes UTCI and runoff for a few scenarios [@mannucci2025], and so does the Sendai study, by parcel [@wu2024].
- **Trees as land cover:** the Barcelona study treats trees as land cover, and found street trees changed runoff retention by less than a percentage point [@cortinovis2022].
- **Land-cover areas, no trees:** the Xiamen study optimises land-cover areas per 1 km cell [@liang2021].
- **Canopy area, all species pooled:** the Bronx study optimises new canopy area per census block group [@nyelele2021].

**One species optimiser for stormwater and microclimate.** The nearest neighbour is a Philadelphia study [@dong2026]. It optimises the species mix of new trees per 0.25 km² cell for stormwater, microclimate, air quality and carbon, with NSGA-III and i-Tree Eco values for the 30 most common local species. At 15% more canopy, the optimised mix reduced runoff by 0.71 against 0.60 million m³ per year for a random mix, and raised the energy-saving value by 77.1% [@dong2026].

The study classed *Platanus × acerifolia* and *Pyrus calleryana* as Pareto-dominated there: on i-Tree Eco values, at least one other species was better on every objective. Its microclimate objective is building energy saving, not pedestrian comfort. Its decision variable is species shares per cell, with no tree positions or crown geometry.

**A recommender built for diversity.** SylvCiT recommends functional groups and species for a user-selected area, such as a park, from seven functional traits, to raise functional diversity in Montreal [@nicol2026]. It places no trees. Its runoff module is disabled, marked as under development, and it has no heat objective. Its traits concern resilience and diversity, not interception or shade.

## Precedents in practice {#sec:sota-practice}

<!-- TO WRITE after the RM cluster map (due 27 Oct): five or more precedents, two theoretical and three from practice,
only from sources read (notes/research_method_guidelines.md §H; notes/miro_map_proposal.md). Not drafted here, to avoid
naming precedents that have not been read. -->

*To be completed from the research-methods mapping exercise (two theoretical and three practice precedents).*

## The gap {#sec:sota-gap}

The review supports a gap, but only in a narrow form. "Nobody optimises tree species for heat and runoff" is not safe: Dong et al. [-@dong2026] optimise species mixes for stormwater and an energy-based microclimate proxy. The claim that holds for every study read is narrower:

> **No method yet chooses street-tree species and positions against pedestrian-level heat stress (UTCI) and event runoff together.**

Chapter 3 adds a layer from practice. Barcelona fixes how many trees of each species may stand and how large each tree may be, but no rule quantifies what a choice does to heat or runoff. None of the tools above works inside such rules:

- the species cap;
- the size class set by sidewalk width;
- a named replacement palette.

The gap therefore has three parts, and the method addresses all three:

1. **Research:** joint pedestrian UTCI and event runoff, at the level of species and positions.
2. **Practice:** inside the city's own replacement rules, compared against the city's own replacement (S1a).
3. **Evidence:** a known resolution limit. The method reports when a difference is smaller than what its models can resolve, rather than ranking layouts on noise (Chapter 6).

The reusable pieces are already published, and the method builds on them rather than replacing them:

- the LAI-based crown transmittance for Ladybug [@peng2026];
- per-tree interception from LiDAR crowns [@eslami2025];
- surrogates or proxies for speed [@tanliu2026; @schrodi2023];
- the known error of Ladybug against ENVI-met [@mannucci2025].

What is new is putting them together for one decision: which replacement species goes at which plane position in Porta.

<!--
PROVISIONAL CITATION KEYS → literature_matrix.csv row (read level in brackets)
mannucci2025    #51  Mannucci et al. 2025, City Environ. Interact. [full text]
cortinovis2022  #69  Cortinovis et al. 2022, Urban For. Urban Green. 67:127450 [full text]
liang2021       #84  Liang, Zhang, Zeng & Shen 2021, Sci. Total Environ. 779:146415 [full text]
wu2024          #56  Wu et al. 2024, Sustainability 16:5201 [full text]
coville2022     #11  Coville et al. 2022, Urban For. Urban Green. [full text]
eslami2025      #83  Eslami et al. 2025, 13th Urban Drainage Modelling Conf., Innsbruck (extended abstract; search record dates it 2026) [full text, page images]
peng2026        #53  Peng et al. 2026, Landsc. Ecol. [full text]
silva2025       #47  Silva et al. 2025 (Lisbon, ENVI-met vs climate walks) [full text]
colaninno2025   #129 Colaninno et al. 2025, Sustain. Cities Soc. (SOLWEIG, Gràcia) [full text]
tanliu2026      #80  Tan & Liu 2026, Sustain. Cities Soc. 149:107726 [full text]
shaamala2025    #52  Shaamala et al. 2025, Cities [full text]
schrodi2023     #87  Schrodi et al. 2023, arXiv:2310.05691 (preprint) [full text]
nicol2026       #28  Nicol et al. 2026, PLoS One 21(2):e0339173 (SylvCiT) [full text]
nyelele2021     #25  Nyelele & Kroll 2021, Landsc. Urban Plan. 214:104172 [full text]
dong2026        #85  Dong, Ye, Su, Haase & Lausch 2026, npj Urban Sustain. 6:47 [full text + supplement]
hao2023         #62  Hao, Zhao & Huang 2023, Urban For. Urban Green. 86:128017 [full text]
elkhateeb2025   #63  Elkhateeb & Anwar 2025, Urban Sci. 9:504 [full text]
oneto2026       #64  Oneto, Mosca, Villa & Perini 2026, Urban For. Urban Green. 120:129457 [full text]
langenheim2022  #86  Langenheim & White 2022, Int. J. Environ. Res. Public Health 19:8220 [full text]
Infrared City: no citation (tool; access to confirm with the tutor).
-->
