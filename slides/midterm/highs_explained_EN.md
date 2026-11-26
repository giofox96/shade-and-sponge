# What HiGHS does in Shade and Sponge, explained slowly

A stand-alone explanation of the solver that picks the species in the tool. It starts from everyday examples and ends with exactly what our code asks HiGHS to do. Read it in order: every section uses the previous one.

---

## 1. The one-sentence version

HiGHS receives a table of scores (how good each species would be at each position) and a list of rules (one species per position, only species that fit, no species above its cap), and it returns **the assignment of species to positions with the highest total score that breaks no rule**, together with the guarantee that no other assignment scores higher.

HiGHS does not know anything about trees, shade or rain. It only sees numbers and rules. Everything "tree-like" happens before it (the screening that fills the score table) and after it (the evaluation of the layout it returns).

---

## 2. A banal example: three friends and three pizzas

Three friends, Anna, Bruno and Carla, order three different pizzas: margherita, diavola and four cheeses. Each friend gives each pizza a mark from 0 to 10:

| | Margherita | Diavola | Four cheeses |
|---|---|---|---|
| Anna | 9 | 6 | 3 |
| Bruno | 8 | 7 | 3 |
| Carla | 7 | 4 | 2 |

Rule: everyone gets exactly one pizza, and each pizza goes to exactly one person. Goal: make the group as happy as possible, that is, maximise the sum of the marks.

**First idea, the "greedy" one:** everyone takes their favourite. Anna takes margherita (9), Bruno takes margherita (8)… but there is only one margherita. The greedy idea breaks the rule.

**Second idea, greedy but polite:** go in order and take the best pizza still available. Anna takes margherita (9), Bruno takes diavola (7), Carla gets four cheeses (2). Total **18**.

**Is 18 the best?** Try the others. There are only 3 × 2 × 1 = 6 ways to share three pizzas among three people:

| Anna | Bruno | Carla | Total |
|---|---|---|---|
| Margherita 9 | Diavola 7 | Four cheeses 2 | 18 |
| Margherita 9 | Four cheeses 3 | Diavola 4 | 16 |
| Diavola 6 | Margherita 8 | Four cheeses 2 | 16 |
| Diavola 6 | Four cheeses 3 | Margherita 7 | 16 |
| Four cheeses 3 | Margherita 8 | Diavola 4 | 15 |
| Four cheeses 3 | Diavola 7 | Margherita 7 | 17 |

Here the polite greedy wins: 18 is the best. But it was luck, as the next example shows. And with three people we could check all six options by hand. With many people that becomes impossible (section 4).

---

## 3. The example on slide 19: five positions, three species

The same idea with trees. Five positions on a street, three species A, B and C. Each cell is the score of that species at that position (made-up numbers, as on the slide). An × means the species does not fit there: the sidewalk is too narrow for its size.

| Position | Sidewalk | A | B | C |
|---|---|---|---|---|
| 1 | wide | 0.9 | 0.6 | 0.3 |
| 2 | wide | 0.8 | 0.7 | 0.3 |
| 3 | wide | 0.7 | 0.4 | 0.2 |
| 4 | medium | × | 0.6 | 0.5 |
| 5 | narrow | × | × | 0.4 |

Rules:
1. Each position gets **exactly one** species.
2. Only species that **fit** (no ×).
3. **Cap**: no species on more than 2 of the 5 positions (in Porta the cap is 15%; here 2 of 5 keeps the example small).

**Greedy, impolite** (best species everywhere): A, A, A, B, C = 0.9 + 0.8 + 0.7 + 0.6 + 0.4 = **3.4**. It looks great, but A appears three times: **it breaks the cap**. Not allowed.

**Greedy, polite** (go in order 1 → 5 and take the best species that still has room):
- position 1: A (0.9). A used once.
- position 2: A (0.8). A used twice: A is now full.
- position 3: A is full, so B (0.4).
- position 4: B (0.6). B is now full.
- position 5: C (0.4).
- Total: 0.9 + 0.8 + 0.4 + 0.6 + 0.4 = **3.1**.

**HiGHS's answer:** A at 1 and 3, B at 2 and 4, C at 5 = 0.9 + 0.7 + 0.7 + 0.6 + 0.4 = **3.3**.

Why is 3.3 better than the polite greedy's 3.1? Look at position 2 versus position 3:
- At position 2, A gives 0.8 and B gives 0.7: B **loses only 0.1** compared with A.
- At position 3, A gives 0.7 and B gives 0.4: B **loses 0.3** compared with A.

Since A can only go in two places, it should go where its **advantage** over the alternative is largest, not simply where its score is highest. Greedy looks at one position at a time and cannot see this. HiGHS looks at everything together. This is the whole point of an optimiser: **a limited resource (the cap) should be spent where it makes the most difference.**

In real projects these differences add up over hundreds of positions and 30 species, which is why the method beats choices made one tree at a time.

---

## 4. Why not just try every combination?

With 5 positions and 3 species there are 3⁵ = 243 combinations: a computer checks them instantly.

In Porta there are about 832 positions and 30 species. The number of combinations is 30⁸³². That is a number with **about 1,229 digits**. For comparison, the number of atoms in the observable universe has about 80 digits. Even a computer checking a billion billion combinations per second would never finish, not in the age of the universe, not in a billion ages of the universe.

So "try everything" is impossible. Two other families of methods exist:

- **Trial and error (heuristics)**: genetic algorithms, ant colony, simulated annealing. They try many good-looking combinations, keep the best ones, mix them, try again. They often find good answers, but **they never know whether the answer is the best one**, and two runs can give two different answers.
- **Exact optimisation**: methods that exploit the structure of the problem to reach the best answer **without** trying everything, and **prove** that it is the best. HiGHS belongs here.

Our problem has a structure that makes exact optimisation easy: everything is a sum of scores, and every rule is a "count must be equal to / at most" rule. This is called a **linear** problem.

---

## 5. What "linear programming" means, with a picture

Forget trees for a moment. A tiny problem with only two numbers to choose:
- x = how many trees of species A we plant,
- y = how many trees of species B.

Rules:
- at most 4 positions in total: x + y ≤ 4,
- cap on A: x ≤ 2,
- cap on B: y ≤ 3,
- no negative trees: x ≥ 0, y ≥ 0.

Goal: maximise 3x + 2y (each A is worth 3 points, each B 2).

Draw it on squared paper, x horizontal and y vertical. Each rule is a straight line, and the allowed side of it is a half-plane. Together they cut out a shape, a **polygon**, whose corners are:

| Corner | x | y | Score 3x + 2y |
|---|---|---|---|
| (0, 0) | 0 | 0 | 0 |
| (2, 0) | 2 | 0 | 6 |
| (2, 2) | 2 | 2 | **10** |
| (1, 3) | 1 | 3 | 9 |
| (0, 3) | 0 | 3 | 6 |

Every point inside the polygon is a legal choice. Now imagine the goal as a ruler laid across the paper: all points on the line 3x + 2y = 6 have score 6, on 3x + 2y = 9 they have score 9, and so on. These lines are all parallel. Slide the ruler in the direction where the score grows. The **last** point of the polygon it touches before leaving it is the best one, and that point is always **a corner** (here (2, 2), score 10).

This is the key fact of linear programming: **when the goal and the rules are all straight lines, the best answer is always at a corner of the shape of legal choices.** It is never hidden in the middle.

Slide 19 shows exactly this picture: a grey shape (all layouts that obey the rules), a "start" corner, arrows going from corner to corner, and the "best" corner at the top.

In Porta there are not 2 numbers but 832 × 30 ≈ 25,000. The "shape" lives in 25,000 dimensions and cannot be drawn, but the rule is the same: the best answer is at a corner.

---

## 6. How HiGHS walks to the best corner (the simplex idea)

Knowing that the answer is at a corner helps, but a 25,000-dimensional shape has an astronomical number of corners. HiGHS does not visit them all. Its main method, the **simplex method** (in its "dual revised" form, the version HiGHS is known for), works like a hiker in fog who wants to reach the top of a mountain:

1. Start from any corner (for example, a dull but legal layout).
2. Look at the edges leaving this corner. Is there one along which the score goes up?
3. If yes, walk along it to the next corner.
4. Repeat.
5. When no edge goes up, stop: you are at the top.

In a mountain range you could get stuck on a small hill. **In a linear problem you cannot**: the shape is convex (it has no dents), so a corner with no upward edge is the highest point of all. That is why the answer is exact, not just good.

On the pizza example, a step of the walk would be: "swap the pizzas of Bruno and Carla: does the total go up?" The simplex is a very clever, very fast way of choosing which swaps to try, so that it reaches the top in few steps instead of trying everything.

HiGHS also has a second method, the **interior point method**, which instead of walking along the edges cuts through the inside of the shape towards the best corner. For a problem like ours it does not matter which one runs: the answer is the same corner. HiGHS chooses automatically.

---

## 7. How HiGHS proves the answer is the best

"Exact" has a precise meaning. When HiGHS stops, it has not only a layout but also a **certificate**: a second set of numbers, one for each rule, called **dual values** or **shadow prices**.

An intuitive way to see it. Each rule gets a "price" that says how much the total score would go up if that rule were relaxed by one unit. In the slide 19 example:
- the cap on A is binding (A is used twice, the maximum). If the cap on A were 3 instead of 2, we could put A at position 2 instead of B and gain 0.8 − 0.7 = 0.1. So the cap on A "costs" 0.1 at this point.
- The cap on C is not binding (C is used once out of 2). Allowing one more C would gain nothing. Its price is 0.

With these prices one can check, rule by rule, that no change to the layout can increase the total. It is like a receipt that anyone can recheck without redoing the whole calculation.

This connects to an idea in the thesis: **"what each rule costs"** (slide 13). In the thesis we measure it directly, by re-running the optimiser with and without a rule (for example, with and without the 15% cap) and comparing the totals. The shadow prices are the same idea for a one-unit change.

---

## 8. Why the answer is always whole trees

A worry: in the drawing of section 5, the polygon also contains points like (1.5, 2.3). Could HiGHS answer "half a Celtis and half a Tipuana at position 47"? That would make no sense for trees.

In our code, the number HiGHS chooses for each position and species, call it x(i, j), may in principle be anywhere between 0 and 1. But our problem has a special structure, called a **transportation problem**: positions on one side, species on the other, "each position receives exactly one" and "each species is sent at most cap times". Mathematicians proved long ago that for this structure **every corner of the shape is made of whole numbers** (0 or 1). Since the best answer is at a corner, it is automatically whole trees, with no extra work. The comment in our code says it: "transportation LP, integral at a vertex".

The same holds when we add the caps per neighbourhood (for city-wide runs): the groups nest inside the species totals, so the structure stays a network flow and the corners stay whole.

There is one case where this is no longer free: the **diversity floor** (section 11).

---

## 9. What exactly our code gives to HiGHS

The function is `assign` in `shade_sponge/layout.py`, which calls HiGHS through SciPy (`scipy.optimize.linprog(method="highs")`). In the web app the same problem is solved in the browser with HiGHS compiled to WebAssembly.

**The unknowns.** For every position i and every species j, a number x(i, j) between 0 and 1: 1 means "species j goes in position i".

**The goal.** Maximise the sum of score(i, j) × x(i, j) over all positions and species.

**The rules.**
1. *One species per position*: for each position i, the sum of x(i, j) over all species equals 1.
2. *Only species that fit*: if species j does not fit at position i (too big for the sidewalk, or it would hit the façade), x(i, j) is forced to 0 by its upper bound.
3. *Cap per species*: for each species j, the sum of x(i, j) over all positions is at most cap(j). In Porta, cap(j) comes from the 15% rule.
4. *(City-wide runs only)* caps per neighbourhood as well.

**Where the scores come from.** For each position and species the screening computes three "potentials":
- summer shade (m²·h of shade on sunlit open ground on the July design day), to maximise;
- winter shade (the same on the January day), to minimise because winter sun is wanted;
- rain held over ground that drains to a flood hotspot (m³ on the design storm), to maximise.

Each potential is divided by its largest value, so all three run from 0 to 1 and can be added. Then:

score = w₁ × summer shade − w₂ × winter shade + w₃ × rain held, plus a tiny tie-breaker,

where w₁, w₂ and w₃ are the weights the designer sets with the triangle in the tool (slide 16), and they add up to 1. The tie-breaker (one thousandth of the unweighted sum) only decides between options that would otherwise score exactly the same, for example at positions that drain to no hotspot.

**The answer.** For each position, the species with x = 1.

---

## 10. The sweep: many weights, many answers

The designer does not always know the right weights. So the tool also runs a **sweep**: it solves the problem for every combination of weights on a grid with step 0.25. For three objectives that is 15 combinations, from "only summer shade" (1, 0, 0) through "balanced" to "only rain" (0, 0, 1). Each one is a separate HiGHS solve, each one exact for its weights.

These 15 layouts are the dots on the trade-off chart of slide 16. Since each solve takes a fraction of a second, the whole sweep is fast, and in the web app a click anywhere on the triangle is solved live.

---

## 11. The diversity floor: when HiGHS has to work harder

Without any diversity rule, the optimiser tends to fill each species up to its cap, starting from the best ones. The result can have few species. The thesis measures diversity as the **effective number of species**, exp(Shannon H). The diversity floor says: "the planted layout must have at least N effective species" (for example 9.4).

Two problems:

1. **Shannon's formula is not a straight line.** It contains a logarithm, a curve. Linear programming only accepts straight lines. Solution in our code: the curve is replaced by many short straight segments that stay just **below** it (a "piecewise linear" approximation). Since they stay below, if the layout passes the floor with the segments, it passes the real floor too: the approximation is conservative (`_entropy_chords` in the code).

2. **The counts must be whole numbers.** The diversity rule is written on the number of trees of each species, n(j). With the curve in play, the corners of the shape are no longer guaranteed to be whole numbers. So the counts n(j) are declared **integer**. The problem becomes a **mixed-integer** problem (MILP): some unknowns must be whole, others not.

HiGHS solves integer problems with **branch and bound**. The idea, with a banal example: suppose the best answer of the relaxed problem says "plant 4.6 Celtis". HiGHS splits the problem in two branches, one with "Celtis ≤ 4" and one with "Celtis ≥ 5", and solves each as an ordinary linear problem. If a branch gives a whole answer, that is a candidate. If a branch's best possible score is already worse than a candidate found earlier, the whole branch is thrown away without exploring it (that is the "bound"). It continues until no branch can beat the best candidate. The answer is still exact, just slower. In our code only the 30 species counts are integer; the 25,000 x-values stay a transportation problem, so it stays fast.

The result on slide 14: the floor lifts diversity from 6.2 to 9.4 effective species at a cost of only 0.3 points of summer shade.

---

## 12. What HiGHS does NOT do (the limits to say out loud)

- **It does not compute shade or rain.** It trusts the score table completely. If a score is wrong, the "best" layout is the best for wrong numbers. This is why the screening and its assumptions (slide 22) matter.
- **It treats every position as independent.** The shade a tree casts is computed as if it were alone (`no overlaps` in the code). In reality, two neighbouring crowns can shade the same patch of ground, so the total shade is a little lower than the sum. This keeps the problem linear and exact; the evaluation after the solve counts the real, overlapping shade.
- **It does not choose the actions.** Keep, move, replace or add is decided by the designer. HiGHS only fills the positions marked Replace or Add.
- **It does not decide the weights.** "Best" always means "best for these weights". That is why the tool shows the sweep and the trade-off chart instead of a single answer.
- **It does not model time.** Trees are at the size each species has today in Barcelona (median from LiDAR), not growing.

---

## 13. Why HiGHS and not something else

- **Exact and reproducible**: the same input always gives the same answer, with a proof. A reviewer can rerun it and get the same layout.
- **Fast**: Porta, 832 positions × 30 species, in about 0.2 seconds.
- **Open source** (MIT licence), developed at the University of Edinburgh, included in SciPy, and available as WebAssembly for the browser. No licence fees, nothing to install for a user of the web app.
- **Decided on 9 Nov**: no genetic algorithms, no ant colony and no machine-learning surrogate in the thesis. The problem is linear, so a heuristic would only add uncertainty about whether the answer is the best.
- **Reference**: Huangfu, Q. and Hall, J. A. J. (2018) "Parallelizing the dual revised simplex method", *Mathematical Programming Computation*, 10, pp. 119–142. The name HiGHS has no official expansion (highs.dev).

---

## 14. Explaining it in 30 seconds (if Angelos asks)

"For every position and every species, the screening gives a score: how much summer shade, winter sun and rain held that species would give there. HiGHS then picks one species per position so that the total score is the highest possible, without breaking the city's rules: only species that fit the sidewalk, and none above 15%. It does not try every combination, which would be impossible; it uses linear programming, which guarantees that the answer is the best one and proves it. Porta takes a fifth of a second."
