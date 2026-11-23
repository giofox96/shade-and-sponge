# Shade and Sponge: midterm speech (Tue 24 Nov 2026, Pecha Kucha, 5 min)

Spoken version of `script.md`, for the public deck `shade_and_sponge_midterm_pechakucha.pptx` (18 slides, final version on main after PR #165: co-benefits on slide 14). 15 slides × 20 s; slides 16–18 and the private slide 19 are backups for questions only.

How to read it (v2, 23 Nov evening: rewritten as connected speech, with subordinate clauses, as Giovanni asked):
- Each slide is one or two flowing sentences; breathe at the commas, pause at the full stops.
- About 45 words per slide. If you fall behind, skip the words in [square brackets].
- **Bold** = the word to stress.

---

### 1. Title
Imagine that you are **redesigning a street** in Barcelona, whose layout is already decided. What is left to you are the **trees**: which to keep, move or replace, and where to add new ones, so that the street is **cooler** in summer and **no worse** when it rains.

### 2. Context
Barcelona, which is my case, has replaced almost **eleven thousand** street trees since 2018. It caps every species at **fifteen percent**, but it never says **which species goes where**, even though, with the **same trunk**, one crown can be **four times** larger than another.

### 3. Porta in numbers
My site is **Porta**, a neighbourhood of eighty-four hectares, where crowns cover **twenty** percent while the city aims for **thirty**. Since planting every free spot would add only a **third** of a hectare out of the **eight** that are missing, what really matters is the **species** in each spot.

### 4. State of the art and gap
The pieces already exist, but **apart**: some models measure heat and runoff without choosing species, while other tools choose species for a single benefit[, or without a position]. Of the **eighteen** tools I reviewed, **none** chooses the species tree by tree, for heat and runoff, inside a city's **own rules**.

### 5. Refined question
In October I started from **floods**, but the feedback showed that runoff depends more on the **tree pit** than on the species. So I now ask how much more **summer cooling** a method can give than the **city's own practice**, without losing rain interception, which becomes a **do-no-harm** check.

### 6. What is fixed, what is free
The project fixes the **street**, while the city fixes the fifteen percent cap and the sidewalk width, which sets the tree size[, together with traffic lights and driveways]. What stays **free** are four actions per tree, **keep, move, replace or add**, and the tool **advises**, while the designer **decides**.

### 7. Method
The method has four steps: it **screens** every tree and free spot; the designer chooses an action for each tree, giving a reason; an **exact optimiser** picks the species for each new position; and I compare the result with **today** and with the **city's practice**.

### 8. Screening
For every position, the screening asks three questions: **what** stands there, meaning its species, crown and leaf density; **where** it stands, meaning the sidewalk, the objects nearby[ and whether rain flows to a flood spot]; and what each of **thirty species** would do there, in shade and in rain held.

### 9. City rules
The rules come from the city's **street-tree guide**, which allows no tree on sidewalks under **two and a half metres** and, above that, lets the width decide between **small, medium or large** trees[, planted every seven, nine or thirteen metres]. Together with the cap, these are rules the optimiser **never breaks**.

### 10. Where new trees go
Of the **two hundred sixty-seven** possible spots in Porta, **one hundred fifty-three** are free, while **one hundred three** are conditional, because a sign, a crossing, a lamp or a bollard is in the way, which a project can usually move[ after a field check]. Only **eleven** are truly blocked.

### 11. A crown is a bucket
To talk about rain, it helps to think in **litres**, since one millimetre on one square metre is **one litre**. In a two-year storm, about **a thousand litres** fall on a typical crown here, of which the leaves hold about **one hundred twenty-five**, wherever the tree is planted.

### 12. The tree on the hill
What position changes is **where that water was going**, since a tree **uphill** of a flood spot keeps its litres away from it. Placed by the method, trees keep **five times** more of it than at random, but still **under one percent**, so runoff stays a **check**.

### 13. City practice, not a rule
My baseline is what the city **really planted** when it replaced trees, which is a **practice**, not a rule, and which does not always follow the rules either, since **one new tree in five** is too big for its sidewalk. This also lets the method show what each rule **costs**.

### 14. First evidence: back-test and co-benefits
In a first test on **twenty-six** groups the city replaced, the method gives **one hundred thirty-nine** square-metre hours of shade per tree against **fifty-nine**, winning **twenty-two**. In Porta it also stores more **carbon** than city practice and brings **less pollen** than today, while more **diversity** costs only **0.3 points** of shade.

### 15. Next
Next come felt temperature, with **Ladybug** and **Infrared City**, and the same method in Florence and **Mataró**, where a first run already gives **eighty-three** against **sixty-three** percent of a plane's shade[, while the tool lets the designer set each tree's action]. The **right tree**, in the **right place**, within the city's rules. **Thank you.**

---

## Backup slides (only if asked; not timed, about 30–40 s each)

### 16. Methodology (full method on one page)
This slide shows the whole method from left to right. It starts from two hazards, **heat stress** and **pluvial floods**, and from open data only: the tree inventory, the **2021 LiDAR**, which gives crowns and buildings, the terrain, the flood hotspots, the sidewalks with their objects, a hot day and the design storms. From these I compute **indicators for every tree**, once for the whole city. In the project area, the **designer then decides an action** for each tree, and for every replacement or addition **HiGHS** picks the species, scoring heat, runoff and canopy inside the **city's rules**, that is the thirty species, the fifteen percent cap and the sidewalk size. I evaluate the result against **today** and against the **city's practice**, and I validate it in **Porta** before moving to Sant Antoni, Mataró and Florence.

### 17. City screening (the indicator matrix)
What the screening produces is a table with **one row for every position**, whether it holds a tree or is a free spot, and with three groups of columns. The first group describes the **existing tree**, its species, trunk, crown, leaf density and a priority, and it ranks which trees are candidates for replacement. The second describes the **place**, meaning the sidewalk width, the tree size it allows and whether the rain there flows to a **flood hotspot**, and it decides which species fit. The third gives a **score to each of the thirty species**, which weighs summer shade, winter sun and water held, and this is the matrix the optimiser solves, choosing one species per row within the fifteen percent cap. The values shown are **illustrative**.

### 18. HiGHS: the solver that picks every species
To show how the optimiser chooses, I use a small example with **five positions and three species**. On the left is the score of each species at each position; then come the **rules**, which say that each position gets one species, that only species fitting the sidewalk are allowed, and that no species goes above its **cap**, here two out of five. Every layout that obeys these rules is a point in this shape, and since the best one is always a corner, **HiGHS finds the highest corner and proves that no other is higher**, which here gives a score of **3.3**. If you simply took the best species everywhere, you would get A three times and **break the cap**, while a genetic algorithm would respect the rules without ever knowing whether it found the best. In Porta, with eight hundred thirty-two positions and thirty species, the solve takes about **0.2 seconds**.

### 19. Underground utilities (private copy only; do not show unless asked)
Below the sidewalk there are pipes and cables which can make a **tree pit impossible** even where the surface looks free. I requested the utility plans for Porta **through the official channel**, and I now have almost all networks, while the water network is still pending. Since the plans are **confidential**, I will neither show nor publish them, and I will use them only to turn spots into **blocked or conditional**, the same classes you saw on slide ten; at the moment, the spot classes do **not** yet include utilities, so that is the next check.

## Numbers to have ready for questions

| If asked about… | Say |
|---|---|
| Results across the city | With the 30 species, the method keeps a median **91.2%** of a plane's summer shade; **+6.7 points** over the city's announced mix and **+14.7** over what the city really plants; it wins **32 of 32** neighbourhoods. |
| Back-test | **22 of 26** groups; median **59 → 139** m²·h of summer shade per new tree; no more water to flood spots in **26 of 26**. |
| Mataró | Six streets, every plane replaced: **83%** for the method vs **63%** for Barcelona's practice, **6 of 6** streets. Crowns are still approximate (Barcelona medians); real LiDAR crowns are the next step. |
| Spots | **153** free · **103** conditional · **11** blocked, of **267**. |
| Diversity | Without a floor the method uses **6.2** effective species; a diversity floor lifts it to **9.4** for only **−0.3 points** of summer shade. City practice reaches **15.6**, so the gap is narrower but still there. |
| Carbon and pollen | Carbon stored once grown: **56** for the method vs **42** for city practice (today = 100). Pollen: **below today** in every replacement, because today's planes are highly allergenic. Both are reported, not optimised. |
| Why "practice" and not "rule" | The baseline is what the city really planted (2018–2026), not its written rule; one in five of those trees is too big for its sidewalk. |
| Why runoff is only a check | Differences are under one percent of the water reaching flood spots, below what the model can resolve. |

Total spoken text (slides 1–15, brackets included): about 710 words without the brackets, about 47 per slide: at 140 words a minute that is just over 5 minutes, so skip the brackets if a slide runs short.
