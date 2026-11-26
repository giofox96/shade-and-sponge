# Conclusion: contribution to knowledge {#sec:conclusion}

<!-- Draft 1, 26 Nov 2026. Sources: notes/decisions/contribution_statement.md §1–§2; notes/lit/prior_art_matrix.csv (18 rows);
slides/outline_10nov.md §7 (funnel 18 → 7 → 1 → 0, as spoken: "Of eighteen tools that place or assess urban trees, seven
cover both services, one picks species, and none works tree by tree inside a city's rules"); notes/tutor_feedback_24nov.md
§3h, §3e; thesis/results_numbers.md. Funnel re-checked 26 Nov against the CSV: both heat and runoff = #25, 51, 56, 69, 82, 84, 85 (7; #86 is
qualitative); species optimised among them = #85 only (1). Validation types: column validation_type. -->

This thesis set out to build a computational method for choosing replacement street trees, species and positions, so that a street keeps its shade and its rain interception when a project changes its trees. This chapter states what the thesis adds, what it does not, and what should come next.

## What the thesis answers {#sec:concl-answer}

When a street project in Barcelona must replace trees, a trait-based layout method working inside the city's tree rules can choose species that keep more summer shade than the city's practice. On the shade proxy, it does so without more runoff and without more winter shade than today.

- In Porta, replacing the 832 planes, the method keeps 106.7% of today's summer shade, against 99.0% for city practice. Winter shade stays at today's level (99.2%), and total runoff is equal within what the model resolves.
- For the 513 planes in the city's own per-tree plan, the method gives 101.4% against the plan's 98.2%, at the same diversity.
- Against what the city really planted in 26 groups between 2018 and 2026, the method gives more summer shade in 23, 1.7 times the shade per tree at the median, and never more runoff.
- In Mataró, a first transfer, it keeps 83% of the planes' shade against 63% for Barcelona's practice and 50% for Mataró's own, on six of six streets.

H1, "do no harm, improve where possible", is supported on the shade proxy. H2, that heat and runoff call for different species, is not supported as stated: both objectives follow the same trait, the crown's area and density, and the real trade-off the method finds is between summer shade and winter sun. Runoff stays a check. The choice of species moves it by less than the model can resolve, so the method can promise "no worse", never "better".

## Contribution {#sec:concl-contribution}

**What is new.** The review of Chapter 4 coded 18 tools and studies that place or assess urban trees for heat, runoff or both. Seven cover both services. One of those chooses species, and it does so as species proportions per grid cell, against an energy-based heat proxy [@dong2026]. None chooses species tree by tree, against pedestrian heat and event runoff together, inside a city's planting rules. The contribution of this thesis fills that place:

> **A computational method that chooses street-tree species and positions, tree by tree, against pedestrian-level shade and event runoff together, inside a real city's planting rules, and tests its choices against what the city actually planted.**

The contribution has four parts:

1. **The method.** Species-resolved crowns and leaf density from a leaf-on LiDAR flight, a seasonal heat proxy that counts summer shade as a benefit and winter shade as a cost, and a calibrated interception term in an SCS-CN runoff model. All of it is solved as an exact linear programme, with the city's rules as constraints: the 15% cap, the sidewalk size class and the façade clearance.
2. **The test against reality.** A back-test on 26 groups of trees the city replaced, with the same positions and trunk sizes, using the city's own quarterly inventory. None of the 18 reviewed studies validates against the trees a city actually planted: they compare with simulations, field measurements or a random baseline. This one compares with the city's actual choices.
3. **The resolution limit.** The method reports when a difference is smaller than what its models can resolve (91 m³ of runoff in Porta), and calls it equal instead of ranking layouts on noise.
4. **The cost of a rule.** Running the method with and without a constraint measures what that constraint costs in shade. In Porta, matching city practice's diversity costs 1.6 points of summer shade. That is a number a city can use when it sets a cap or a palette.

**What it builds on.** The reusable pieces are published, and the method combines them rather than replacing them:

- the LAI-based crown transmittance for Ladybug [@peng2026];
- per-tree interception from LiDAR crowns [@eslami2025];
- fast proxies or surrogates for heat [@tanliu2026; @schrodi2023];
- the known error of Ladybug against ENVI-met [@mannucci2025];
- the effective number of species as a diversity measure [@nicol2026].

**What it does not claim.**

- It does not claim a temperature. Until the UTCI check is done, its heat result is shade.
- It does not claim a runoff reduction. Its runoff result is "no worse".
- It does not claim to replace the technician's judgement of a site. It advises; Parcs i Jardins decides.
- It does not claim to be valid in another climate (Chapter 8).

## Future work {#sec:concl-future}

The near-term work finishes what this thesis has started. These results are marked **TO UPDATE** in Chapters 7 and 8:

- the Ladybug UTCI check on one street, so that SQ1 is answered in its own metric;
- the rerun of the 32 barris with the corrected crowns;
- the Mataró rerun with its own LiDAR crowns, and the full Florence transfer test;
- the gain decomposition, to show how much of the gain comes from placement, from species choice and from a wider palette;
- the rerun of the additions with the 30-species palette.

Beyond the thesis, five extensions follow from its limits:

- **Growth over time.** New trees enter at today's crown for their trunk size. A growth model per species would show which choices keep their advantage over decades, and when a small young tree costs more shade than its adult form suggests.
- **More objectives, as modules.** Carbon and biodiversity are reported today as co-benefits, not optimised. They could enter the optimiser as further objectives. With more than two or three objectives, a genetic algorithm such as NSGA-II would replace the weighted-sum sweep.
- **Every tree a project replaces.** The plane is the validated case, but it is only 13% of the city's replacements. The same logic applies to any species the city removes, with the city's practice for that species as the baseline.
- **A tree-health proxy.** There is no open data on which trees will need replacing. A proxy from LiDAR vigour, vegetation-index change and age, validated against the trees removed between inventory releases, would let the method plan ahead of failures.
- **City-wide use.** A screening layer that runs the method on every barri would show where the choice of species matters most, and the guided web tool would let a street designer use it on a project area without knowing the method's internals.

A last point concerns the city's own rules. Barcelona's 15% cap is a rule of thumb, like the caps in the diversity literature [@santamour1990; @kendal2014]. This thesis does not argue for a different number. It shows that a city can now see what its rules cost in shade, street by street, and decide with that number in front of it.

<!--
PROVISIONAL CITATION KEYS → references (keys as in thesis/02–05)
dong2026        #85  Dong et al. 2026, npj Urban Sustain. 6:47 (ch. 4 block)
peng2026        #53  Peng et al. 2026, Landsc. Ecol. (ch. 4 block)
eslami2025      #83  Eslami et al. 2025, UDM 2025 (ch. 4 block)
tanliu2026      #80  Tan & Liu 2026, Sustain. Cities Soc. 149:107726 (ch. 4 block)
schrodi2023     #87  Schrodi et al. 2023, arXiv:2310.05691 (ch. 4 block)
mannucci2025    #51  Mannucci et al. 2025 (ch. 4 block)
nicol2026       #28  Nicol et al. 2026, SylvCiT (ch. 4 block)
santamour1990   Santamour 1990 (ch. 3 block, #139)
kendal2014      Kendal, Dobbs & Lohr 2014 (ch. 3 block, #140)
-->
