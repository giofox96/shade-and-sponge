# Next tutor session: slide outline and spoken script (v6 draft, 21 Oct)

**Why a new deck.** At the 20 Oct session the tutor said the problem was not defined well enough. v6 (`notes/topic_decision.md` §9) rebuilds the problem on Barcelona's tree master plan. The 20 Oct deck (`slides/outline_20oct.md`) is left untouched as the record of that session.

**Figures.**
- **New for v6:** in `slides/fig_v6/` (SVG + PNG). Regenerate them with `python make_slides_v6.py`, run from `scripts/`.
- **Unchanged slides:** they reuse `slides/fig/NN_*.png` from the 20 Oct deck.
- **Two figures to revise before use:**
  - **Slide 3** of 20 Oct still says "like-for-like".
  - **Slide 12** still describes H1 against a like-for-like replacement.

  The outline below says "text on slide" where the old figure should not be shown.

**Length.** 12 slides plus 2 backups, ~1,000 spoken words, about 6:40 at 150 words a minute. The core version, dropping slides 5 and 11, is about 5:30.

**Sources.** Every number is from `notes/topic_decision.md` §9, `notes/tree_master_plan.md`, `notes/sidewalk_width.md`, `databases/barcelona/crown_by_trunk_class.csv`, or the 20 Oct sources it reuses.

**Results caveat.** The optimisation results (slide 11) are still the 20 Oct runs. Their baseline is a random palette, not v6's S1, and the sizing rule was off. Re-run with `python -m shade_sponge porta --size=exact` before quoting them as v6 results.

---

## 1. Title [0:20]
**Figure:** `slides/fig/01_title.png` (unchanged).

**Say (45 words):**
"This is Porta, and those bare crowns are plane trees. Barcelona has decided to remove more than half of them in ten years. My thesis is about one decision the city has not taken: which species goes back, where, and what that does to heat and to storm water."

---

## 2. The decision is already taken [0:55]
**Figure:** none (text on slide).
**On slide:**
- Planes: **43,722 trees, 27.45% of the city stock → 12%** within ten years (press, May 2026)
- Tree master plan 2017–2037: **no species above 15%** of the urban fabric
- Replaced **one tree at a time**, when a tree dies or a street is rebuilt

**Say (85 words):**
"The starting point is not a proposal, it is a decision. Barcelona's plane is more than a quarter of the city's trees, and the master plan says no species may exceed fifteen percent. The city has announced it will cut the planes by more than half, to twelve percent, within ten years. Nobody plants them all at once. Each one is replaced when it dies or when its street is rebuilt. That makes thousands of small decisions over the next decade."

---

## 3. What the city decided, and what it left open [1:45]
**Figure:** `slides/fig_v6/v6_03_decided.png`

**Say (120 words):**
"So I read the plan and the city's 2011 street-tree guide. On the left is what the city has decided: how much of each species, how and when to replace, which species may be used, and which tree size fits which sidewalk. On the right is what it has not decided. First, which species goes at each position. The city says it chooses from criteria such as orientation, space, soil and desired shade, but that list is not public, and nothing puts a number on the choice. Second, what each choice does to heat and to runoff. Third, where heat and flooding overlap, because the plan is city-wide. My thesis is the right-hand column. It takes the left-hand column as hard constraints."

---

## 4. Why the choice matters: the crowns differ [2:35]
**Figure:** `slides/fig_v6/v6_04_crowns.png`

**Say (115 words):**
"Why does it matter which species? Because the replacements are very different trees. Here is crown area as a share of a plane's crown, at the same trunk size, for the trees standing in Porta today, from the 2021 laser scan. Tipuana and Jacaranda carry about the same crown as a plane. Melia carries three quarters. Celtis, Pyrus and Brachychiton carry between a quarter and a half. Every one of these choices follows the city's rules, and yet the shade and rain interception left on the street can differ by a factor of three to four. This also sets two of the plan's own targets against each other: diversity on one side, canopy cover on the other."

---

## 5. Why Porta [3:15]
**Figure:** `slides/fig/04_why_porta.png` (unchanged).

**Say (95 words):**
"The losses would matter most where heat and flooding overlap. I screened all seventy-three neighbourhoods with open data. To qualify, a neighbourhood had to be above the city's sixtieth percentile for flood hazard, for surface heat and for plane density at the same time. Porta comes first at every threshold I tried. It has eight hundred and thirty-two plane trees. And every replacement species the city names already grows there, so I can measure them rather than assume them."

---

## 6. Same tree, two jobs [3:45]
**Figure:** `slides/fig/08_heat_runoff_traits.png` (unchanged).

**Say (70 words):**
"The literature gives the mechanism. The same crown traits drive both services: crown size and leaf area set how much shade a tree casts and how much rain it holds back. But some traits pull apart. An evergreen crown intercepts winter rain and also blocks winter sun. So I expect gains on both goals together, and a real trade-off at the margin."

---

## 7. The gap [4:15]
**Figure:** `slides/fig/09_gap_matrix.png` (unchanged).

**Say (75 words):**
"The gap is the same in practice and in research. The city has rules and qualitative criteria, but no quantities. Studies assess heat and runoff for fixed scenarios without species traits, or optimise trees for heat only. The most advanced trait-based recommender, SylvCiT, has its runoff module switched off. Nobody gives, position by position, the rule-compliant species that keeps the most cooling and the most rain interception."

---

## 8. The research question (v6) [5:00]
**Figure:** `slides/fig_v6/v6_08_research_question.png`

**Say (105 words):**
"So the question. In Porta, as the planes are replaced under the master plan, which species, chosen within the plan's rules, and at which positions, jointly reduce pedestrian heat stress and event runoff? I measure heat stress as mean felt temperature over the afternoon of a hot day, and runoff for one-, two- and ten-year design storms. And how large is the trade-off between the two? The comparison is new. It is not against a random palette but against the city's own replacement: its announced species mix, placed by its own sizing rule. That is what happens anyway if this method does not exist."

---

## 9. The sizing rule leaves room [5:45]
**Figure:** `slides/fig_v6/v6_09_sizing_rule.png`

**Say (110 words):**
"One risk could have killed the optimisation. The 2011 guide sets the tree size by sidewalk width. If most sidewalks were narrow, only one species would fit and there would be nothing to choose. So I measured the sidewalk at every plane, from façade to kerb, on the city's 1:1000 map, and checked twenty trees by eye. Four hundred positions have a proper sidewalk, and only fifteen of them are forced to Pyrus or to no tree. The rest keep three species each. The other four hundred and thirty-two are medians, boulevards and plaza edges. There the rule does not apply as written, and I state that as an assumption."

---

## 10. Hypotheses and method [6:25]
**Figure:** `slides/fig/13_method_pipeline.png` (unchanged pipeline). The hypotheses are text on slide; do **not** show the old `12_hypotheses.png`.
**On slide:**
- **H1, synergy:** at the same positions, with the size class each sidewalk takes, trait-based choices beat the city's own replacement (S1) on **both** heat and runoff. Runoff differences below Δmin = 91 m³ are reported as "not resolved".
- **H2, trade-off:** the heat optimum and the runoff optimum differ mainly in species, so the front is not a point.
- **Declared boundary:** the runoff benefit shrinks as storms grow. This is true by construction of the model, so it is not tested.
- **Constraints:** ≤ 15% per species · size class by sidewalk width · the city's catalogue · diversity floor.

**Say (95 words):**
"Two hypotheses. One, synergy: under the same rules, trait-based choices beat the city's own replacement on both goals, because crown size and leaf area drive both. Two, trade-off: the heat optimum and the runoff optimum differ in species. The method is unchanged from last time. A laser scan gives each tree's crown. A runoff module and a heat module score each layout. An optimiser picks a species per position, now under the plan's rules as hard constraints. Because trees are replaced one street at a time, it also works on any subset of positions."

---

## 11. Where the tool stands [7:00]
**Figure:** `slides/fig/15_shade_result.png` (20 Oct run). Say clearly that it predates v6.

**Say (75 words):**
"The tool already runs end to end. In the version before v6, an optimised layout gave sixteen percent more summer shade than a random one, and that held across eight sensitivity variants. But those runs were against a random palette and without the sizing rule. The next run uses the city's replacement as the baseline and the sidewalk constraint. That comparison is the result the thesis is built on."

---

## 12. Open questions, and what I asked the city [7:35]
**Figure:** none (text on slide).
**On slide:**
- **Email to Parcs i Jardins (21 Oct).** Five questions:
  - Is there an internal replacement list?
  - Which streets keep their planes (is Av. Meridiana one of them)?
  - Is the 15% applied per neighbourhood?
  - Is there an official source for the 2026 target mix?
  - Is there an official sidewalk width, and how are trees on medians sized?
- **If the city has a list:** it becomes S1, and the contribution narrows to the quantities.
- **Assumptions to defend:**
  - the Porta-local 15% cap;
  - no size filter on medians;
  - Av. Meridiana included by default.

**Say (80 words):**
"Three things are still open, and I have asked the city about each. If there is an internal replacement list, it becomes my baseline, and my contribution narrows to the numbers. That is fine. I also asked which avenues keep their planes, because Meridiana alone holds a hundred and ninety-four of Porta's. Until they answer, I state my assumptions. My question to you: is the city's own replacement the right baseline for the main result?"

---

# Backup

## B1. How the sidewalk was measured
**Figure:** `notes/figures/sidewalk_width_qa_20.png` (20 random trees).
- For each tree, a ray runs from the nearest façade, through the tree, to the first kerb line.
- 18 of 20 are correct. The other 2 are corner trees, measured diagonally, and both stay "large".
- LiDAR at 0.5 m cannot check ±0.3 m. Roofs overhang the façades by a median 0.6 m, and kerbs are smoothed out of the ground model.
- 32 of the 400 measured planes lie within 0.3 m of a class threshold.

## B2. The crown comparison, raw vs equal trunk size
- **Raw medians mislead.** Melia looks as big as a plane because 30% of the Melias in the table are in the largest trunk class, against 16% of the planes.
- **They overstate the Pyrus loss.** 63% of the Pyrus trees are in the smallest class.
- **Source:** `notes/topic_decision.md` §9.9.
