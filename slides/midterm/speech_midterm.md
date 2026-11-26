# Shade and Sponge: midterm speech (Tue 24 Nov 2026, Pecha Kucha, 5 min)

Spoken version of `script.md`, for the public deck `shade_and_sponge_midterm_pechakucha.pptx` (24 slides, latest version 24 Nov, with Giovanni's corrections of 24 Nov afternoon: full methodology on slide 7, screening matrix on slide 8, why Porta on slide 3, co-benefits on slide 14, Mataró on slide 15). 15 slides × 20 s; slides 16–24, plus the utilities slide in the private copy (25), are backups for questions only.

How to read it (v3, 24 Nov: Giovanni's corrections applied to slides 1–4, 7, 10–13 and 15):
- Each slide is one or two flowing sentences; breathe at the commas, pause at the full stops.
- About 45 words per slide; the slides show the details, so the text says only what they need.
- **Bold** = the word to stress.

---

### 1. Title
Hi, my project is called **Shade and Sponge**, an **urban street-tree recommender**. Imagine a Barcelona street whose layout is already decided: what is left are the **trees**, which to keep, move, replace or add, so that the street is **cooler** in summer and **no worse** when it rains.

### 2. Context
Since 2018, Barcelona has replaced almost **eleven thousand** street trees, capping every species at **fifteen percent** but never saying **which species goes where**. I compare everything with the **plane**, the tree most often replaced: with the **same trunk**, one species matches its crown, while another makes only a **quarter** of it.

### 3. Porta in numbers
I chose **Porta** because heat, flood hazard and planes are all high there, with **832 planes** and a surface **1.4 degrees** hotter in summer. **Eight hectares** of crown are missing to the city's thirty percent target, while every free spot would add only a **third of a hectare**: what matters is the **species** in each spot.

### 4. State of the art and gap
Research covers each part of this problem, but **separately**: some models measure heat and runoff without choosing species, while other tools choose species for a single benefit. Of the **eighteen** tools I reviewed, **none** chooses the species tree by tree, for heat and runoff, inside a city's **own rules**.

### 5. Refined question
In October I started from **floods**, but runoff depends more on the **tree pit** than on the species, so I now ask how much more **summer cooling** a method can give than the **city's own practice**, while runoff becomes a **do-no-harm** check.

### 6. What is fixed, what is free
The project fixes the **street**, while the city fixes the fifteen percent cap and the sidewalk width, which sets the tree size. What stays **free** are four actions per tree, **keep, move, replace or add**, and the tool **advises**, while the designer **decides**.

### 7. Methodology
**Heat** and **floods** decide the data, from LiDAR to storms and sidewalks. Every tree is **screened**, the designer sets an **action** for each one, and an **exact optimiser** picks the species within the city's rules. Finally, I compare the result with **today's trees** and with the **city's practice**.

### 8. Screening
The screening fills **one row** for every tree and free spot, saying **what** stands there, from species to leaf density, and **where**, from the sidewalk to whether rain flows to a flood spot; each row then scores all **thirty species**, and the optimiser picks **one per row**.

### 9. City rules
The rules come from the city's **street-tree guide**, which allows no tree on sidewalks under **two and a half metres** and, above that, lets the width decide between **small, medium or large** trees. With the cap, these are rules the optimiser **never breaks**.

### 10. Where new trees go
Of Porta's **two hundred sixty-seven** possible spots, **one hundred fifty-three** are free and **one hundred three** conditional, because a sign, a crossing, a lamp or a bollard is in the way, which a project can move. Only **eleven** are blocked, by **traffic lights** and **driveways**.

### 11. A crown is a bucket
One millimetre of rain on one square metre is **one litre**: in a two-year storm about **a thousand litres** fall on a typical crown here, and the leaves hold about **one hundred twenty-five**. So, where rain heads to a **flood hotspot**, the method puts the species that hold **the most water**.

### 12. The tree on the hill
But on this terrain, rain on **three positions in four** never reaches a hotspot, so there the litres held change nothing; only a tree **uphill** of one keeps water out of it. Placed by the method, trees keep **5.6 times** more than at random, yet only **half a percent** of the hotspot water, so runoff stays a **check**.

### 13. City practice, not a rule
My baseline is what the city **really planted**: a **practice**, not a rule, since **one new tree in five** is too big for its sidewalk. Since the method always follows the rules, I can **switch one rule off** and re-optimise, to measure what that rule **costs** in shade.

### 14. First evidence: back-test and co-benefits
On **twenty-six** groups the city replaced, the method gives **one hundred thirty-nine** square-metre hours of shade per tree against **fifty-nine**, winning **twenty-two**. In Porta it also stores more **carbon** than city practice and brings **less pollen** than today, while more **diversity** costs only **0.3 points** of shade.

### 15. Next
Three steps come next: **felt temperature**, with **Ladybug** and **Infrared City**, to check that more shade means a cooler street; the transfer tests, where **Mataró** already gives **eighty-three** against **sixty-three** percent of summer shade, now with **real LiDAR crowns**, and then **Florence**; and the **utility plans**, to see which spots are really free. **Thank you.**

---

## Backup slides (only if asked; not timed, about 30–40 s each)

### 16. In the tool: priorities and trade-offs
In the tool, the designer sets the priorities by clicking a point on this **triangle**, whose corners are the three objectives, **summer shade**, **winter sun** and **runoff**, and the optimiser re-solves straight away in the browser. Every layout then becomes a dot on the chart, which compares summer shade with winter shade: the city's practice and a random palette sit to the left of today's trees, while the **optimised layouts** sit to the right, so that the designer can see what each choice gains and what it costs before deciding.

### 17. Method (the simple version)
If the full diagram is too much, this is the same method in four steps: it **screens** every tree and free spot once; the designer chooses an **action** for each tree, giving a reason; an **exact optimiser** picks the species for every replaced or added position; and I compare the result with **today** and with the **city's practice**.

### 18. Screening (the simple version)
If the matrix is too dense, the same screening fits in three questions, asked for every position: **what** stands there, meaning its species, crown and leaf density; **where** it stands, meaning the sidewalk width, the objects nearby and whether rain flows to a flood spot; and what each of the **thirty species** would do there, in summer shade, winter shade and rain held.

### 19. HiGHS: the solver that picks every species
To show how the optimiser chooses, I use a small example with **five positions and three species**. On the left is the score of each species at each position; then come the **rules**, which say that each position gets one species, that only species fitting the sidewalk are allowed, and that no species goes above its **cap**, here two out of five. Every layout that obeys these rules is a point in this shape, and since the best one is always a corner, **HiGHS finds the highest corner and proves that no other is higher**, which here gives a score of **3.3**. If you simply took the best species everywhere, you would get A three times and **break the cap**, while a genetic algorithm would respect the rules without ever knowing whether it found the best. In Porta, with eight hundred thirty-two positions and thirty species, the solve takes about **0.2 seconds**.

### 20. Why Mataró
Mataró is the city where I test whether the method still works with **other data** and **another practice**. I chose it because it has a **full tree inventory**, with species and position for every tree, and because it was covered by the **same ICGC LiDAR** as Porta, a leaf-on summer flight in the same coordinate system. It is also the only finalist city with its **own design storm**, from its drainage plan, and it is one of the **forty-four** Catalan municipalities that ACA lists for **pluvial flood risk**. Since it lies only **twenty-five kilometres** from Porta, on the same Mediterranean coast and with plane trees too, the climate stays the same, while the planting choices are different.

### 21. Mataró: six plane streets
In this first run, I took the **six streets** with the most plane trees and imagined that a project replaces **every plane**. At the same positions and with the same trunk size, the method keeps a median **eighty-three percent** of the planes' summer shade, against **sixty-three** for the city's practice, and it wins on **all six** streets, while runoff is **never worse** than any practice. The run is still **approximate**, because crowns are Barcelona medians per species until I process Mataró's LiDAR, the ground is flat and there is no hotspot map. The weak case is **València**, a narrow street where few species fit, so the gain shrinks to **forty-two** against **thirty-five**.

### 22. Declared assumptions
These are the assumptions I declare, together with the reason why they are acceptable at this stage. New trees take the **crown their species has in Barcelona today**, the median from the LiDAR, so growth is not modelled, while a ten-year view is available in the tool. Heat is measured as **summer shade**, a proxy, until felt temperature comes in with Ladybug and Infrared City. Every species uses **one interception rate**, because species-specific rates do not change the ranking. Free spots are an **upper bound**, since there is no open data on underground services, while replacements reuse the existing pit. The fifteen percent cap counts **street trees only**, which I will revisit before the final results, and a **moved tree** leaves the site, because where it lands is outside the tool.

### 23. Case study: Av. Rio de Janeiro, Porta
This is a real replacement in Porta, from start to end. Between 2022 and 2024, **twenty-two poplars** were removed along Avinguda Rio de Janeiro, and in 2025 the city replanted all the positions together with **narrow-leaved ash**. If the method had chosen instead, it would have planted **honey locust** and **Chinese parasol trees**, which give about **two hundred forty** square-metre hours of summer shade per tree, against **seventy-four** for the city's choice and **one hundred sixty-seven** for the poplars that were there. Each of those trees would also hold about **two hundred twenty litres** of rain in a two-year storm, against **fifty-four** for the city, while sending the same water to flood spots. The cost is **winter shade**: about **eighty-five** square-metre hours per tree, far more than the city's ashes give, although slightly less than the poplars had.

### 24. Cost and robustness
This slide answers two questions, what the actions cost and whether the ranking survives a different interception rate. A **replacement** costs up to about **five hundred euros** per tree, following the provincial grant ceiling, while **moving** a tree with a tree spade costs between about **five hundred and almost three thousand euros**, depending on the root ball, and **widening a pit** costs about **one hundred euros**. Since the method and the city's practice replace the **same trees**, the method changes the species, not the number of works. As for robustness, giving **eleven of the thirty species** their own interception rate leaves Porta's summer shade at the same level, and using a **lower rate** for short storms halves the differences between layouts without changing their sign, so the **ranking holds**: the method stays ahead on summer shade and is never worse on runoff.

### 25. Underground utilities (private copy only; do not show unless asked)
Below the sidewalk there are pipes and cables which can make a **tree pit impossible** even where the surface looks free. I requested the utility plans for Porta **through the official channel**, and I now have almost all networks, while the water network is still pending. Since the plans are **confidential**, I will neither show nor publish them, and I will use them only to turn spots into **blocked or conditional**, the same classes you saw on slide ten; at the moment, the spot classes do **not** yet include utilities, so that is the next check.

## Numbers to have ready for questions

| If asked about… | Say |
|---|---|
| Results across the city | With the 30 species, the method keeps a median **91.2%** of a plane's summer shade; **+6.7 points** over the city's announced mix and **+14.7** over what the city really plants; it wins **32 of 32** neighbourhoods. |
| Why Porta | First Barcelona neighbourhood where heat, flood hazard and planes are all high: summer surface **1.4 °C** above the city mean, flood hazard in the **top 20%**, **832** planes (**29%** of street trees). |
| Back-test | **22 of 26** groups; median **59 → 139** m²·h of summer shade per new tree; no more water to flood spots in **26 of 26**. |
| Mataró | Six streets, every plane replaced: **83%** for the method vs **63%** for Barcelona's practice, **6 of 6** streets. Crowns are still approximate (Barcelona medians); real LiDAR crowns are the next step. |
| Spots | **153** free · **103** conditional · **11** blocked, of **267**. |
| Diversity | Without a floor the method uses **6.2** effective species; a diversity floor lifts it to **9.4** for only **−0.3 points** of summer shade. City practice reaches **15.6**, so the gap is narrower but still there. |
| Carbon and pollen | Carbon stored once grown: **56** for the method vs **42** for city practice (today = 100). Pollen: **below today** in every replacement, because today's planes are highly allergenic. Both are reported, not optimised. |
| Why "practice" and not "rule" | The baseline is what the city really planted (2018–2026), not its written rule; one in five of those trees is too big for its sidewalk. |
| Why runoff is only a check | On the terrain model, rain on three tree positions in four (**74%**) never flows to a flood hotspot; 100 trees placed by the method keep **5.6×** more water from hotspots than at random, but that is only **0.5%** of the hotspot water, below what the model can resolve. |

Total spoken text (slides 1–15): about 731 words, about 49 per slide: at 145 words a minute that is about 5 minutes, so keep a brisk pace.
