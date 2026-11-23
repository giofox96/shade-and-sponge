# Shade and Sponge: midterm speech (Tue 24 Nov 2026, Pecha Kucha, 5 min)

Spoken version of `script.md`, for the public deck `shade_and_sponge_midterm_pechakucha.pptx` (18 slides, PR #154: slides 9 and 10 back to the original figures). 15 slides × 20 s; slides 16–18 and the private slide 19 are backups for questions only.

How to read it:
- Short sentences, one idea each. A pause at every full stop.
- About 43 words per slide. If you fall behind, skip the words in [square brackets].
- **Bold** = the word to stress.

---

### 1. Title
Imagine you are **redesigning a street** in Barcelona. The layout is fixed. Your job is the **trees**. Which do you keep, move or replace? Where do you add new ones? The goal: a **cooler** street in summer, and **no worse** when it rains.

### 2. Context
Barcelona is my case. Since 2018, the city has replaced almost **eleven thousand** street trees. No species can go above **fifteen percent**. But nothing says **which species goes where**. And with the **same trunk**, one crown can be **four times** bigger than another.

### 3. Porta in numbers
My site is **Porta**. Eighty-four hectares, almost three thousand street trees. Crowns cover **twenty** percent; the city wants **thirty**. So **eight hectares** are missing. Planting every free spot adds only a **third** of a hectare. So what matters is the **species** in each spot.

### 4. State of the art and gap
The pieces exist, but **apart**. Some models measure heat and runoff, but do not choose species. Some tools choose species, but for one benefit, [or without a position]. I reviewed **eighteen** tools. **None** chooses the species tree by tree, for heat and runoff, inside a city's **own rules**.

### 5. Refined question
In October I started from **floods**. But runoff depends more on the **tree pit** than on the species. So now I ask: how much more **summer cooling** can a method give than the **city's own practice**, without losing rain interception? Runoff becomes a **do-no-harm** check.

### 6. What is fixed, what is free
What is **fixed**? The street, the fifteen percent cap, the sidewalk width that sets the tree size, [traffic lights and driveways]. What is **free**? Four actions per tree: **keep, move, replace, add**. Never remove without replacing. The tool **advises**; the designer **decides**.

### 7. Method
Four steps. **One**: screen every tree and every free spot. **Two**: the designer picks an action for each tree, with a reason. **Three**: an **exact optimiser** picks the species for each new position. **Four**: compare with **today** and with the **city's practice**.

### 8. Screening
The screening asks three questions everywhere. **What** stands there? Species, crown size, leaf density. **Where** is it? Sidewalk width, objects nearby, [and whether rain flows to a flood spot]. And what would each of **thirty species** do there? Summer shade, winter shade, rain held.

### 9. City rules
The rules come from the city's **street-tree guide**. If the sidewalk is under **two and a half metres**, no tree. Above that, the width sets **small, medium or large** trees, [every seven, nine or thirteen metres]. Plus the fifteen percent cap. The optimiser **never breaks** them.

### 10. Where new trees go
Porta has **two hundred sixty-seven** possible spots. **One hundred fifty-three** are free. **One hundred three** are conditional: a sign, a crossing, a lamp or a bollard is in the way, and a project can move it [after a field check]. Only **eleven** are blocked.

### 11. A crown is a bucket
Now rain, in **litres**. One millimetre on one square metre is **one litre**. In a two-year storm, about **a thousand litres** fall on a typical crown here. The leaves hold about **one hundred twenty-five**. Plant it anywhere: the same tree holds the **same water**.

### 12. The tree on the hill
But **position** decides where that water was going. A tree **uphill** of a flood spot keeps its litres away from it. With the method, trees keep **five times** more water from flood spots than at random. But it is still **under one percent**. So runoff stays a **check**.

### 13. City practice, not a rule
My baseline is the **city's practice**: what it really planted when it replaced trees. It is a **practice**, not a rule. And it does not always follow the rules: **one new tree in five** is too big for its sidewalk. So the method can also show what each rule **costs**.

### 14. First evidence: back-test
First test: **twenty-six** real replacements by the city, same positions. Per new tree, the city's choice gives a median of **fifty-nine** square-metre hours of summer shade. The method gives **one hundred thirty-nine**. It wins **twenty-two of twenty-six**, and never sends more water to flood spots.

### 15. Next
Next. A first test in **Mataró** shows the same pattern: **eighty-three** against **sixty-three** percent of a plane's summer shade. My weak point is **diversity**: fewer species than the city uses. Tests to fix it are **running**. The **right tree**, in the **right place**, within the city's rules. **Thank you.**

---

## Backup slides (only if asked)

- **16. Full method:** "This is the whole method on one page: data in, screening, the designer's choice, the optimiser, and the comparison."
- **17. Screening matrix:** "One row per position, one column per indicator. It is computed once, and the optimiser only reads it."
- **18. How HiGHS picks:** "On five positions: each species gets a score per position, and the solver picks the best mix that respects the cap and the sidewalk size."
- **19. Underground utilities (private copy only):** "Pipes and cables under the sidewalk can block a tree pit. I have the utility plans through the official request channel and will use them only to flag spots as blocked or conditional; the plans are confidential, so I don't show them."

## Numbers to have ready for questions

| If asked about… | Say |
|---|---|
| Results across the city | With the 30 species, the method keeps a median **91.2%** of a plane's summer shade; **+6.7 points** over the city's announced mix and **+14.7** over what the city really plants; it wins **32 of 32** neighbourhoods. |
| Back-test | **22 of 26** groups; median **59 → 139** m²·h of summer shade per new tree; no more water to flood spots in **26 of 26**. |
| Mataró | Six streets, every plane replaced: **83%** for the method vs **63%** for Barcelona's practice, **6 of 6** streets. Crowns are still approximate (Barcelona medians); real LiDAR crowns are the next step. |
| Spots | **153** free · **103** conditional · **11** blocked, of **267**. |
| Diversity (the declared weak point) | Effective number of species **5.7** for the method vs **9.4** for the city's practice. Runs with a diversity floor at 9.4 and 7.5 are under way. |
| Why "practice" and not "rule" | The baseline is what the city really planted (2018–2026), not its written rule; one in five of those trees is too big for its sidewalk. |
| Why runoff is only a check | Differences are under one percent of the water reaching flood spots, below what the model can resolve. |

Total spoken text (slides 1–15, brackets included): about 650 words, about 43 per slide.
