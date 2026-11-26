# Abstract {.unnumbered}

<!-- Draft 1, 26 Nov 2026. ≤ 500 words (IAAC); ≤ 5 keywords. Numbers from thesis/results_numbers.md (needle-fix state).
Rewrite once the TO UPDATE items in ch. 7–8 are final (UTCI on one street, barris rerun, Florence). -->

Cities replace street trees one at a time, when a tree dies or a street is rebuilt. Barcelona does so about 1,300 times a year with a change of species, and its largest single case is the plane tree, which the city plans to reduce under a 15% cap per species. The city's rules fix how many trees of each species may stand and how large each may be. They do not say which species should go where, and no rule measures what a choice does to a street's shade or to its storm runoff.

This thesis develops a computational method for it. When a street project must replace trees, can a trait-based layout method, inside the city's tree rules, choose species and positions so that pedestrian cooling and storm-water interception improve, or at least do not get worse, compared with the city's own practice and with today? The hypothesis is that the method's layout is no worse than city practice on heat or runoff, better on summer heat, and casts no more winter shade than today.

The method reads each tree's crown and leaf density from a leaf-on LiDAR flight, at equal trunk size per species. It scores summer shade as a benefit and winter shade as a cost with a fast sun-and-shadow proxy, checked against Ladybug UTCI. It models runoff with a calibrated interception term in an SCS-CN model, on a 1 m grid with flow routing to flood hotspots. An exact linear programme chooses one species per position, inside the city's 15% cap, the sidewalk size rule and a façade clearance. The baseline is city practice: the species the city actually planted where it replaced planes between 2018 and 2026.

In Porta, a Barcelona neighbourhood where heat and flooding overlap, replacing the 832 planes keeps 106.7% of today's summer shade with the method, against 99.0% with city practice. Winter shade stays at today's level, and total runoff is equal within model resolution. For 513 planes in the city's own per-tree plan, the method gives 101.4% against 98.2% at the same diversity. In a back-test on 26 groups of trees the city really replaced, the method gives more summer shade in 23, 1.7 times the shade per new tree at the median, and never more hotspot runoff. Matching city practice's species diversity costs 1.6 points of summer shade. In Mataró, a first transfer test, it keeps 83% of the planes' shade against 63% for Barcelona's practice, on six of six streets.

The hypothesis is supported on the shade proxy. Heat and runoff do not trade off, because both follow crown area and density; the real trade-off is between summer shade and winter sun. Runoff remains a do-no-harm check. The contribution is a method that chooses species tree by tree, for pedestrian shade and runoff together, inside a real city's rules, and tests its choices against what the city actually planted. It also measures what each rule costs.

**Keywords:** street-tree replacement; urban heat; pluvial runoff; layout optimisation; LiDAR
