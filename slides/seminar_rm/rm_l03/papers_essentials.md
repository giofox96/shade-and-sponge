# The six papers in essentials (for 5 Nov)

Taken from the PDF abstracts and from my prior-art matrix (`notes/lit/prior_art_matrix.csv`) and literature matrix (`notes/lit/literature_matrix.csv`), both built from the full texts. I did not reopen the PDFs today. Each paper is described by what it does, where, and its one limit for you.

## 1. Nyelele & Kroll 2021 (Landscape and Urban Planning) – Bronx, New York
- **What:** decides where to add tree canopy in the Bronx, across 1,132 census block groups, with linear programming.
- **Services:** heat (heat-index reduction, i-Tree Cool), avoided runoff (in $ per year, i-Tree Hydro), air quality (PM2.5) and equity (Gini), in 14 scenarios.
- **Limit for you:** the unit is the block group and canopy square metres, not single trees. All species are lumped together; the authors name species choice only as a possible extension. No validation, just scenario comparison.
- **One line:** heat and runoff together, at city scale, without species.

## 2. Mannucci et al. 2025 (City and Environment Interactions) – Ostia, Rome
- **What:** a Grasshopper workflow on one square that assesses pedestrian heat (UTCI with Ladybug) and runoff (curve number, with Kangaroo particles for the water paths).
- **Limit for you:** it compares design scenarios, it does not optimise and does not choose species. The heat part is checked against ENVI-met at 4 points; runoff is not calibrated.
- **One line:** your same tools (Ladybug, Grasshopper) and both services, but only a scenario comparison.

## 3. Dong et al. 2026 (npj Urban Sustainability) – Philadelphia
- **What:** the only one of the 18 that chooses species with heat and runoff: it optimises the mix of 30 species with NSGA-III over 4 objectives.
- **Limit for you:** the unit is a 0.25 km² cell (species proportions, not tree positions). Heat is measured as building energy savings, not UTCI. Species effects come from i-Tree Eco, not from traits. The baseline is a random species mix, with no on-site validation. Abstract: about +20% stormwater and up to +80% microclimate vs that baseline.
- **One line:** the closest to you, but per cell, not per tree, and without city rules.

## 4. Shaamala et al. 2025 (Cities) – Queensland, Australia
- **What:** places 42 trees and chooses among 4 species (by crown spread, height, leaf habit) to minimise UTCI (Ladybug), with an ant-colony algorithm.
- **Limit for you:** heat only; the authors name water as future work. The check is ENVI-met, optimal vs suboptimal layout. Abstract: 22% less area above 39 °C, cooling up to 3.5 °C.
- **One line:** per tree and per species, but no water.

## 5. Peng et al. 2026 (Landscape Ecology) – Shanghai
- **What:** optimises tree positions with NSGA-II for summer and winter UTCI and cost. Trees are generic types, with transmittance from LAI.
- **Limit for you:** heat only, no real species. Validation is measured mean radiant temperature under one camphor tree (about 3 °C better in the shaded zones).
- **One line:** like you, summer shade as benefit and winter shade as cost, but no water and no real species.

## 6. Anys & Weiler 2024 (Hydrological Processes) – Freiburg, Germany
- **What:** field measurements of rain intercepted by real street trees: 8 trees per species, 76 events.
- **Results:** Tilia cordata intercepts 70.3% per event on average, Acer platanoides 54.8%. Interception rises with LAI/PAI (adjusted R² > 0.45) and falls as rain gets heavier and more intense. LAI is lower at the most sealed sites. Stemflow is under 1%.
- **Limit:** only two species and small events (mean 6.7 mm). The data are open on FreiDok.
- **For you:** it is your ground truth; your interception parameter (1.75 mm per unit LAI) is calibrated on it.

## The thread that ties them together
Species without heat and water (SylvCiT); heat and water without species (Nyelele & Kroll, Mannucci); species and both services but per cell (Dong); per tree but heat only (Shaamala, Peng); measured interception for two species (Anys & Weiler). Nobody works tree by tree, inside a city's replacement rules.
