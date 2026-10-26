# Method: the Shade and Sponge tool {#sec:method}

<!-- Draft 1, 26 Oct 2026. Sources: the code in shade_sponge/ (site.py, topo.py, heat.py, runoff.py, season.py,
layout.py, __main__.py, web_export.py), shade_sponge/README.md, notes/methodology.md §3–§7, §4b, §5,
databases/data_inventory_barcelona.md §A, §B, §G–§I, notes/method_heat_validation.md §1, notes/sidewalk_width.md,
notes/topic_decision.md §9.9, §10.5–10.6, exchange/README.md, web/README.md. Results are in Chapter 7, not here.
Every parameter is either sourced or marked ASSUMPTION, as in the code. Citation keys are provisional. -->

This chapter describes the method as implemented in the Python package `shade_sponge`. It covers six parts:

- what the tool decides, and under which rules;
- the data it reads;
- the tree model;
- the two objective models, heat and runoff, and the season;
- the optimiser and the scenarios;
- the two front-ends through which designers use it.

Its results for Porta follow in Chapter 7, and its validation in Chapter 6.

## Overview {#sec:method-overview}

**The decision.** For each plane-tree position, the tool chooses which species is planted there. In Porta that means 832 positions, or fewer if the planes of Avinguda Meridiana are kept.

**The rules.** Every choice must satisfy the city's rules (Chapter 3):

- the 15% species cap;
- the tree size class allowed by the sidewalk width;
- clearance from façades;
- the species palette.

**The objectives.** Each layout is scored on three:

1. **Summer shade:** effective shade on sunlit open ground in summer, a benefit.
2. **Winter shade:** the same quantity in winter, a cost, because it takes winter sun.
3. **Runoff:** event runoff of a two-year, one-hour storm, in total and at the district's flood hotspots.

The tool also reports canopy cover and the largest genus and family shares, as indicators, not objectives.

**Design principles.** The software follows two principles. There is one core, in Python, with two front-ends: Grasshopper for computational designers, and a web application for non-specialists. And every parameter in the code is either taken from a cited source or marked as an assumption, with the range used to test it where it has been tested. The assumptions are collected in Appendix A.

## Data {#sec:method-data}

All layers are reprojected to ETRS89 / UTM 31N (EPSG:25831) on a 1 m grid over Porta (83.7 ha).

| Input | Source | Use |
|---|---|---|
| Street-tree inventory: 140,404 trees; Porta 2,825 | Barcelona open data, `arbrat-viari` (CC BY 4.0) | Positions, species, planting date, trunk class |
| Airborne LiDAR, flown 26 Sept 2021 (leaf-on) | ICGC Territorial LiDAR, ≥ 8 points/m², classified (CC BY 4.0) | Terrain, building heights, tree height, crown and LAI proxy |
| Building footprints | OpenStreetMap (via OSMnx), and LiDAR building points | Roofs, obstacles for shade and flow |
| NDVI 2017, 0.9 m | Barcelona open data, `cobertura-vegetal-ndvi` (CC BY 4.0) | Pervious ground |
| Flood-hazard index, present | Barcelona Resilience Atlas (Barcelona Regional; licence not stated) | Flood hotspots |
| Design rainfall | PDISBA sewer master plan 2019, city empirical IDF | Design storm |
| Storm months | @esbri2026 [Fig. 4]: intense storms 2014–2022 | Season weighting of runoff |
| Leaf calendar per species | `phenology_palette.csv`: literature, species guides and Barcelona iNaturalist photos (Chapter 2) | Leaf-on fraction per month |
| Sidewalk widths | 1:1000 topographic base map, read as SVG vectors from its WMS in 250 m tiles (CC BY 4.0) | Size class per position |

: Table 5.1. Input data. Sources and licences are listed in full in Appendix B.

The LiDAR flight covering Porta is entirely from 26 September 2021, which falls in the leaf-on season. Crowns and LAI are therefore measured in full leaf, and the leaf calendar scales them for other months.

The site is built once and cached. A new site's geometry needs only two functions that return the same grids and tree table. The palette, the rules (cap, size classes, replacement mix), the design storm and the storm months are per-city data that a new site must replace (Chapter 8).

## The tree model {#sec:method-trees}

**Per-tree metrics from LiDAR.** Each inventory tree is used as a seed for a watershed segmentation of the canopy height model, with a maximum crown radius of 9 m. For each crown the tool records:

- height;
- crown diameter;
- crown base;
- a LAI proxy from the gap fraction, assuming an extinction coefficient k = 0.5.

Crown metrics were obtained for 2,600 of Porta's 2,825 inventory trees (92%). The 225 trees without crown metrics are left out of every evaluation, but they count in the species cap.

The LAI proxy is not calibrated and spans a narrow range: 1.9–2.9 across the medians of species with at least 30 trees. It is probably lower than LAI measured from the ground. Freiburg's 16 lime and maple trees, measured with an optical canopy analyser (LAI-2200C), ranged from 1.4 to 4.9, 13 of them at 2.5 or more [@anys2024]. The proxy is therefore used to rank species rather than as an absolute value (Chapter 6).

**Species traits.** A replacement tree at a position takes the median traits of its species. The default uses all of the species' LiDAR-measured trees in Porta. For the Barcelona palette, it uses Porta plus three city LiDAR tiles, and requires at least 20 measured trees (`ASSUMPTION`). The raw medians mix young and old trees, so they favour species that happen to be old in Porta. The thesis runs therefore compare species **at equal trunk size**:

- traits are the medians of each species' Porta trees in the inventory's third trunk class, 81–110 cm perimeter;
- a species with fewer than 20 trees there falls back to the second class, then to all classes (*Pyrus calleryana* has no third-class trees in Porta and uses the second);
- *Styphnolobium japonicum* has only five trees in Porta, so it takes the medians of a city-wide sample of 367 trees. That sample mixes all trunk classes, so this species is not at equal trunk size.

Equal trunk size is a fair comparison between species, not a forecast of how large a new tree will be (Chapter 8).

**Palettes.** Two palettes are available:

- **City palette:** seven species. Five are named as replacements in city or press sources: Celtis, Melia, *Pyrus calleryana*, Jacaranda and Tipuana. Two more complete it: *Brachychiton populneus*, common in Porta's recent plantings but named in no source, and *Styphnolobium japonicum*, named in the press. This is the palette used in the thesis results.
- **Barcelona shortlist:** 34 street-tree species with at least 500 trees in the city inventory, excluding the plane. The palms are a separate inventory and are not included. Invasive taxa were to be excluded, but none of them reached 500 trees.

## Topography and flood hotspots {#sec:method-topo}

**Routing.** Surface water is routed over the LiDAR terrain, with buildings as obstacles. The routing uses a Priority-Flood algorithm (Barnes et al., 2014; reference to add), which fills depressions implicitly and gives every cell one downstream neighbour. Two results follow:

- for each cell, the open area that drains through it;
- for each cell, the flow distance to the nearest flood hotspot.

**Hotspots.** A hotspot is a cell of the Resilience Atlas flood-hazard index at or above 40, the same threshold used to select Porta.

**What the routing omits.** It has no sewer and no inflow from outside the grid. It therefore shows where surface water would converge, not where it ends up.

**Capture distance.** Runoff counts toward a hotspot only if its flow path reaches one within 100 m (`ASSUMPTION`; a test at 50–200 m is planned). This stands in for the sewer inlets that would take the water on the way. Without a limit, almost all open ground would drain to some hotspot (about 97%, a figure noted in the code but not saved as an output), and position would no longer matter.

## The heat proxy {#sec:method-heat}

Ladybug UTCI is too slow to score every layout (Chapter 4), so the optimiser uses a fast proxy: **effective shade on sunlit open ground**, in m²·h, summed over the design hours.

**Sun.** Solar positions come from the NOAA solar-position equations. The design days are 15 July, 12–17 h CEST, for summer and 15 January, 10–15 h CET, for winter (both `ASSUMPTION`). The summer window still has to be aligned with the decided heat metric, which uses 12–17 h standard time (13–18 h CEST) on a hot design day.

**Building shade.** A cell counts only where a pedestrian at 1.1 m sees the sun past the buildings. This is computed by marching towards the sun over the building surface model.

**Crown shadows.** Each crown is an ellipsoid and casts an elliptical shadow:

- the shadow is longer when the sun is low;
- it is shifted away from the sun by the height of the crown centre above 1.1 m, divided by the tangent of the solar altitude.

**Crown opacity.** Each shadow has an opacity:

$$
O = f\,(1 - e^{-0.5\,\mathrm{LAI}}) + (1 - f)\,O_{\mathrm{bare}}
$$

- $f$ is the species' leaf fraction in the month, from its leaf calendar.
- The in-leaf term is one minus the Beer–Lambert transmittance, with k = 0.5 as in Peng et al. [-@peng2026].
- $O_{\mathrm{bare}}$ = 0.35 is the irradiance reduction of a leafless crown (`ASSUMPTION`, tested at 0.25 and 0.54). Measured leafless crowns cut about 35% (McPherson, 1984, as cited in Thayer & Maeda, 1985). A leafless London plane cuts up to about 54% at the shadow centre (Heisler, 1982, 1984, as cited in Thayer & Maeda, 1985).

Where shadows overlap, the cell takes the largest opacity.

**Sign.** Summer shade is a benefit and winter shade a cost. The proxy has to be calibrated against Ladybug UTCI on the same layouts before it can be read as heat stress (Chapter 6).

**The Ladybug check.** In Grasshopper, the final layouts are scored with Ladybug's outdoor MRT and UTCI on a 2 m sidewalk grid at 1.1 m. Crowns there are opaque by default (Chapter 4). The planned correction runs the sky relation twice for each test point, once with buildings only and once with buildings and crowns. It then sets the direct-sun exposure to

$$
f_{bc} + \tau\,(f_b - f_{bc}), \qquad \tau = e^{-0.5\,\mathrm{LAI}},
$$

which applies Peng et al.'s transmittance without changing Ladybug's code. Peng et al. give the correction as a reduction of direct radiation under the crown (their Eq. 7), but not how they wired it into Ladybug. This input-level construction is ours, from the structure of Ladybug's code.

## The runoff model {#sec:method-runoff}

**Storm.** The objective storm is the PDISBA design storm with a two-year return period and one-hour duration: 31.9 mm.

**Surfaces.** Each 1 m cell is one of three surfaces, each with an SCS curve number (CN):

| Surface | Share of Porta | How it is identified | CN |
|---|---|---|---|
| Roof | 29% | building footprint | 98 |
| Sealed open space | 52% | the rest | 98 |
| Pervious | 19% | NDVI ≥ 0.3 with canopy below 2 m, or an OSM green area | 74 (`ASSUMPTION`) |

: Table 5.2. Surface classes and curve numbers in the runoff model.

The CN of 74 for pervious ground is the TR-55 value for open space in good condition on hydrologic soil group C.

**Canopy storage.** Under each street-tree crown, the canopy holds

$$
S = s \cdot \mathrm{LAI}
$$

millimetres of rain before the rest falls through. Each crown is a disc: of the LiDAR crown diameter for a kept tree, and of the species' median diameter for a replacement. Two more rules apply:

- Crowns over roofs do not change roof runoff, which leaves through downpipes.
- All canopy outside today's street-tree discs is fixed background with a LAI of 2.3: 10.2 ha of park, square and private canopy, plus the parts of today's crowns that extend beyond their disc. Because that background stays in every layout, part of the planes' canopy is never removed, and the losses of a replacement are biased low.

The rain left on each cell, P − S, then goes through the SCS curve number, with an initial abstraction of 0.2 times the SCS retention, $S_{CN} = 25.4\,(1000/\mathrm{CN} - 10)$ mm.

**Calibration.** The storage parameter s was calibrated on the open field data of Anys and Weiler [-@anys2024]: 16 urban lime and maple trees, April–September 2021, 51 events of at least 1 mm. The result is s = 1.75 mm per unit LAI, the pooled median (lime 1.85, maple 1.60). This effective value includes evaporation during events. For Barcelona's short, intense storms it may be lower, so the surface-storage value of 0.86 mm [@xiao2016] is the lower bound in the sensitivity runs. The same s is used for every species, so species differ in runoff only through crown size, LAI and leaf calendar.

**Outputs.** For each layout the model reports three quantities:

- **total runoff** over Porta;
- **hotspot runoff:** runoff generated on open ground whose flow path reaches a hotspot within the capture distance;
- **canopy interception.**

The optimiser works on hotspot runoff, while the hypothesis test uses total runoff (Chapter 6).

## The season {#sec:method-season}

LAI is measured in full leaf. For month $m$, each tree's LAI becomes

$$
\mathrm{LAI}(m) = \mathrm{LAI}_{\mathrm{LiDAR}} \cdot \bigl(R_{\mathrm{off}} + (1 - R_{\mathrm{off}})\,f(m)\bigr)
$$

where $f(m)$ is the species' leaf fraction. $R_{\mathrm{off}}$ = 0.5 is the storage of a leafless crown as a share of its full-leaf value (`ASSUMPTION`, tested at 0.3–0.7). Two studies are anchors for this value, though neither gives it directly:

- in a deciduous forest, leafless interception loss was 20% against 29% in leaf (Herbst et al., 2008);
- a deciduous pear intercepted 15% of winter rain, against 27% for an evergreen oak (Xiao et al., 2000, as cited in @kuehler2017).

The runoff objective is the expected runoff of the design storm, weighted by the share of intense storms in each month [@esbri2026]. The heat proxy uses the leaf fraction of the design month: July in summer, January in winter.

Species without a calendar keep full leaf (`ASSUMPTION`). These are some kept trees, and they are the same in every layout.

## Rules as constraints {#sec:method-rules}

**Species cap.** No species may exceed 15% of Porta's 2,825 street trees, counting the trees that are kept. The plan sets the cap city-wide (Chapter 3), so applying it within Porta is a local reading (`ASSUMPTION`). With additions, the cap is recomputed on the larger stock.

**Sizing rule.** Each position gets a sidewalk class from the façade-to-kerb distance. That distance was measured on the city's 1:1000 base map, read from its WMS because the full download kept failing.

- **Exact rule:** a species may go only where its size class from the 2011 guide matches the sidewalk class. This is the rule used in the thesis runs. A looser "at most" reading also allows smaller classes on wider sidewalks.
- **Unmeasured positions:** medians, boulevards and plaza edges have no façade-bounded sidewalk, so they are not filtered (`ASSUMPTION`).
- **Species without a class:** species that the 2011 guide does not classify, most of the Barcelona shortlist, are not size-filtered (`ASSUMPTION`).

**Façade clearance.** A species fits a position only if its crown radius does not exceed the distance to the nearest building (`ASSUMPTION`: no extra margin). A building is an OSM footprint or a LiDAR building point more than 3 m above ground.

**When nothing fits.** Where no species fits a position, including sidewalks under 2.5 m where the guide allows no tree, the smallest-crowned species is assigned. The position stays planted, which departs from the guide (`ASSUMPTION`).

**Optional rules.**

- **Diversity floor:** a minimum effective number of species, exp(Shannon H), among the replanted positions. It is linearised with a conservative piecewise-linear bound.
- **Kept avenue:** the planes of Avinguda Meridiana can be kept and removed from the decision set, since the city keeps planes on large avenues.

**Indicators, not constraints.** Two indicators are reported for every layout:

- **Genus and family check:** the largest genus and family shares, against Santamour's 20% and 30% (Chapter 3).
- **Canopy cover:** crown discs plus the fixed background. It is a relative measure, comparable between layouts only, and it reads 23.3% today against 20.1% from the LiDAR canopy model.

## The optimiser {#sec:method-optimiser}

The optimiser works in three steps.

**1. Potentials per position.** For each position and each palette species, the tool computes what that species alone would contribute there, with no overlaps:

- its effective shade in summer;
- its effective shade in winter;
- its season-weighted interception over ground that drains to a hotspot.

**2. Weighted sum.** The three potentials are normalised and combined with weights on a simplex grid in steps of 0.25. That gives 15 weight sets, from summer shade only to runoff only. For each set, the best assignment of one fitting species per position, with species counts under the cap, is a transportation problem. It is solved exactly as a linear program with HiGHS, through SciPy, and the solution is integral. The diversity floor adds a few integer variables.

**3. Re-scoring.** Every resulting layout is re-scored with the full raster models, overlaps included. The Pareto front is taken over all replacement layouts, the baselines included.

A weighted sum can miss parts of a front that is not convex. NSGA-II is the fallback if the swept front leaves gaps (Chapter 7 reports whether it does).

## Scenarios {#sec:method-scenarios}

| Scenario | What it is |
|---|---|
| **S0** | Today: the measured trees, planes included (807 planes have crown metrics, against 832 positions replanted in the other scenarios) |
| **S1a** | The city's rule: the 2026 mix (Celtis 12, Melia 7.25, *Pyrus*, *Styphnolobium* and Tipuana 5 each) as relative weights of a random draw within the exact sizing rule and the cap. The most constrained positions are drawn first. 10 seeds |
| **S1 random** | Any fitting palette species at random under the cap. 10 seeds; a check of what optimisation adds over chance |
| **S4** | The optimised layouts of the weight sweep |

: Table 5.3. Scenarios for the plane positions.

S1a reads the 2026 figures as one weight per species (`ASSUMPTION`; Chapter 3).

The scenarios are combined with three planting options:

- **R:** replacement at the plane positions only;
- **A:** additions in free planting spots, with the planes kept;
- **R+A:** both.

For A and R+A, the city's rule is run with 5 seeds and the optimised layout with one weight set (summer 0.5, winter 0.25, runoff 0.25), not the full sweep. The free spots come from the same base map. Pits are placed 0.7 m in from the kerb, on sidewalks of at least 2.5 m, within 15 m of a street centreline (`ASSUMPTION`), and spaced 7, 9 or 13 m by size class. This gives 267 spots in Porta. They are an upper bound, because driveways, crossings, bus stops, lamps and underground services are not in the data.

**Project area.** A designer will be able to draw a project area so that only the positions inside it are decided. This is planned, not yet implemented.

## Front-ends {#sec:method-frontends}

**Grasshopper.** The tool exchanges CSV files with Grasshopper in local coordinates, with an origin at 430,800 / 4,586,800 m in EPSG:25831. Each layout gives the position, species and crown of every decided position; the kept trees come in a separate file. Together they are ready to build crowns and run Ladybug. The designer can export their own positions or species to a return folder; scoring them in Python is planned, as is a Hops component.

**Web application.** A static web application shows the layouts on a 3D map, built with Vue, MapLibre and deck.gl. It has three functions:

- **Live re-optimisation:** the designer moves a point in a triangle of priorities, and the browser re-solves the same transportation problem with HiGHS compiled to WebAssembly, in about 0.1–0.3 s. The web data currently come from the default run, without the sizing rule and with traits from all trunk sizes, not from the configuration used in the thesis results.
- **Add trees:** a designer can place new trees by hand. The browser scores every palette species at that point with a port of the Python formulas.
- **Exact check:** browser results are estimates from summed potentials, calibrated on the saved layouts. Exact scores need a Python run. How closely the browser matches Python is reported in Chapter 6.

<!--
PROVISIONAL CITATION KEYS
anys2024      #1   Anys & Weiler 2024 (calibration data, FreiDok, CC BY-NC 4.0)
xiao2016      #3   Xiao & McPherson 2016
peng2026      #53  Peng et al. 2026
barnes2014    Barnes, Lehman & Mulla 2014, Priority-Flood (to add; not in matrix or papers/). Plain text for now.
esbri2026     #142 Esbrí et al. (year unresolved 2025/2026)
Secondary: McPherson 1984 and Heisler 1982/1984 as cited in Thayer & Maeda 1985 (only Thayer & Maeda goes in the reference list; not in matrix/papers — add and check). Herbst et al. 2008: not in matrix/papers — add and read before citing. Xiao et al. 2000: as cited in Kuehler 2017 (the code says "evergreen oak", the matrix "cork oak"; check).
TR-55 (USDA NRCS 1986) for CN 74: add a reference.
Data sources (Open Data BCN, ICGC, OSM, Resilience Atlas, PDISBA): reference list entries to add (Appendix B).
-->
