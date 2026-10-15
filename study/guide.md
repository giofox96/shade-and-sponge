# Study guide: Shade and Sponge (state of 15 Oct 2026)

A condensed version of the thesis for **learning it**, not for writing it. Every fact here comes from the project notes; the source file is named in each chapter, so check there when a number changes. If a note is updated, update this guide and the cards (`flashcards.csv`, `quiz.csv`).

**How to read it:** read one chapter, close the file, answer its **Check yourself** questions out loud or on paper, *then* open the answers. Do not reread before you have tried to recall (see `README.md` for why).

---

## 0. The thesis in 30 seconds (learn this by heart first)

> Barcelona will replace many of its plane trees, because the tree master plan caps every species at 15% and planes are about 29% of street trees. In **Porta (Nou Barris)** the same streets suffer **summer heat stress** and **pluvial flooding**. My thesis is **a computational method that chooses which species replace the plane trees, and where**, scoring each layout on **pedestrian heat stress (UTCI)** and **event runoff volume**, and showing the **trade-off** between the two as a Pareto front.

**One sentence:** *species × position → heat + runoff → trade-off.*

**The logic chain (the tutor's order):** problem → why it matters → gap → research question → hypotheses → method (data, tools) → tool → first results → limits.

### What changed since 9 Oct (read this first if you studied the earlier version)
- **A seventh candidate species:** *Styphnolobium japonicum* (user decision, 14 Oct). Its crown and LAI now come from a LiDAR sample outside Porta (§1, §9).
- **The gap needs narrower wording** because of Dong et al. 2026: say "species **and positions**" and "**pedestrian UTCI**" (§6).
- **H3 is true by construction of the model:** with the v1 LAI proxy every crown is full at every design storm, so the falling % is arithmetic, not a test (§3, §7).
- **The runoff part of H1 may come out "not resolved by the model":** accepted as a valid outcome (user, provisional, 14 Oct) (§7, §9).
- **RESCCUE flood-depth maps are public**, and the routing was checked against them (§8, §10).
- **Several decisions wait for you** (heat metric, weather file, hypothesis wording, contribution statement): listed in §14.

---

## 1. The problem
Source: `notes/topic_decision.md` §7.

- Barcelona's **sealed surface grew from 45% to 72%** of the municipality (1956–2009; Barcelona Resilience Atlas, citing Barcelona Regional's climate-change impact study).
- About **3 storms a year exceed 60 mm/h in their first 20 minutes** and flood streets where the sewer lacks capacity (Barcelona Resilience Atlas). The sewer is sized for a **10-year** return period (`notes/city_screening.md`).
- Barcelona carries **one of Europe's highest urban-heat-island mortality burdens** (Iungman et al. 2023).
- The **tree master plan caps any species at 15%**; plane trees are **~29%** of street trees → many will be replaced.
- The city's named replacement species: ***Celtis*, *Melia*, *Pyrus calleryana*, *Jacaranda*, *Tipuana*, *Brachychiton*** (mnemonic: **"CeMeP-JaTiBra"**, or the sentence *"Celtic Melodies Play Jazz To Brazil"*).
- **Seventh candidate (user, 14 Oct):** ***Styphnolobium japonicum*** (formerly *Sophora japonica*), named in the press; only 5 trees in Porta. Extended mnemonic: *"Celtic Melodies Play Jazz To Brazil, Softly"*.
- **The data gap:** in the reviewed literature only *Pyrus calleryana* has a measured canopy-storage value (Xiao & McPherson 2016), and **none of the six city-named species has a measured cooling value**.
- **Why it matters:** replacement choices can trade away cooling or rain interception without anyone noticing.

**Primary user:** a computational designer working on the municipal street-tree replacement.

**Flood type matters.** The thesis is about **pluvial** flooding (rain on sealed surfaces, sewer overloaded), from **frequent, short storms**. Not fluvial (river) floods and not multi-day events: Bologna Oct 2024 and Emilia-Romagna May 2023 were saturated-soil, multi-day or culvert events, where trees have negligible influence. This is why Bologna was dropped (Florence fitted the pluvial framing; Barcelona was chosen later for data, access and the dual heat + runoff theme).

### Check yourself
1. What two hazards, and why do they meet in the same streets?
2. Why are plane trees being replaced, in one sentence with both numbers?
3. Name the six city-named replacement species, and the seventh candidate.
4. Why is Bologna a bad case for a tree-based flood thesis?

<details><summary>Answers</summary>

1. Summer heat stress (UHI) and pluvial flooding; both concentrate in dense, highly sealed districts.
2. The master plan caps any species at 15%, and planes are ~29% of street trees.
3. Celtis australis, Melia azedarach, Pyrus calleryana, Jacaranda mimosifolia, Tipuana tipu, Brachychiton populneus; seventh: Styphnolobium japonicum (added 14 Oct).
4. Its recent floods were multi-day / saturated-soil / culvert events; trees only matter for frequent, short pluvial storms.
</details>

---

## 2. The site: why Porta
Source: `notes/site_selection.md`.

- **Porta, Nou Barris, 0.84 km²**; 2,825 street trees, 53 taxa; **832 plane trees (29%)**, concentrated on **Av. Meridiana (194)**.
- **Method, non-compensatory, two steps:** (1) *eligibility*: flood share, surface-temperature anomaly and plane density all above the city's **60th percentile**; (2) *ranking* by the equal-weight mean of four normalised criteria (flood, surface heat, heat vulnerability, plane density).
- **Robustness:** thresholds at the 50th, 60th, 70th percentile → **Porta is first at every threshold**. Under 2,000 random weightings (Dirichlet) it is in the top 3 in 53% of cases (#2 overall on the four-criterion score).
- Porta's ranks: flood **#13**, surface heat **#11 (+1.36 °C)**, heat vulnerability **#12** (91% of area in the top class), plane density #15.
- **Sant Antoni** = #1 for flood, but #38 for surface heat → fails "both hazards" → **flood-dominant contrast site**. **Florence** = transfer test.
- The replacement palette **already grows in Porta** → LiDAR can measure real crowns of each species. Exception: *Styphnolobium* has only 5 trees in Porta, so its crown and LAI come from a **LiDAR sample outside Porta** (§9).

**Why "non-compensatory"?** A very high flood score must not make up for no heat. Both hazards must be present.

### Check yourself
1. What does "non-compensatory" mean here, and why use it?
2. How did you test the robustness of the choice?
3. Why is Sant Antoni not the main site, and what is it for?

<details><summary>Answers</summary>

1. Every criterion must pass a threshold (60th percentile) before ranking; a strong value on one hazard cannot offset the absence of the other.
2. Thresholds at the 50/60/70th percentile: Porta is first at every one. 2,000 random weightings: top 3 in 53% of them (#2 on the four-criterion score).
3. It is #1 for flood but below the city median for heat (#38); it is the flood-dominant contrast site in the test phase.
</details>

---

## 3. Runoff science
Sources: `notes/topic_decision.md` §1, `notes/methodology.md` §4–4b.

**The chain:** rain → **canopy interception** (crowns hold water, which evaporates) → rest falls on sealed ground → **SCS curve number** → **event runoff volume**.

- **Storage bucket:** interception I = min(P, S), with **S = s · LAI**. Calibrated **s = 1.75 mm per unit LAI** on open field data from Freiburg (Anys & Weiler 2024: 16 urban lime and maple trees, 51 storms). Lower bound in sensitivity: **0.86 mm** (surface storage only, Xiao & McPherson 2016).
- **Plausibility:** leafy crowns hold the **first 2–4 mm** of a storm (Kuehler et al. 2017); 1.75 × 2.3 ≈ 4.0 mm.
- **SCS-CN:** curve number **98** for sealed surfaces and roofs; **74** for pervious (assumption, TR-55 open space, soil group C).
- **Storms (PDISBA IDF, 60 min):** **T1 = 19.6 mm, T2 = 31.9 mm, T10 = 62.5 mm**.
- **The effect fades as storms grow:** the crown fills up early, so its share of a big storm is small (per-event interception falls from 87% to 1% as rain depth grows, Song et al. 2020).
- **Why volume, not peak flow:** a paired-catchment field study found a **~4% runoff-volume cut from 31 street trees and no peak-flow effect** (Selbig et al. 2021); 3.5% in the calibrated re-analysis (Coville et al. 2022).
- **Species do differ:** storage capacity varies **threefold among 20 species** (Xiao & McPherson 2016); *Tilia cordata* 70% vs *Acer platanoides* 55% event interception (Anys & Weiler 2024). **LAI is the main driver.**
- **Roots:** not in the score. Only two lab studies (Bartens 2008; Zhang 2019); roots raise infiltration, but species differences are unclear.
- **Stemflow:** ignored (< 1% of rain).
- **Caution: the model's crowns are always full.** At every design storm (19.6–62.5 mm) every crown is saturated, so interception is the **same volume** at T1, T2 and T10. The avoided runoff even rises a little in m³ (304 → 365 m³ from T1 to T10), but total runoff grows much faster (9,600 → 40,541 m³), so the **percentage** falls (3.16% → 0.90%). The shrinking % is arithmetic of the bucket model, **not an independent test** (`notes/decisions/hypothesis_tests.md`).
- **LAI bias may differ by species:** field LAI in Sydney (Kaluarachchi 2020) is higher than our LiDAR proxy for *Platanus* (2.8 vs 2.31) and *Pyrus* (2.6 vs 2.08), but lower for *Jacaranda* (2.0 vs 2.91). Different city and method: a check of direction, not a correction.

### Check yourself
1. Write the interception equation and explain each symbol.
2. Where does s = 1.75 come from, and what is its lower bound?
3. Why is the metric runoff *volume* and not *peak flow*?
4. Why does the tree benefit shrink with the return period?
5. Why are roots left out of the scoring?
6. In the model, why is the falling % benefit not a real test of H3?

<details><summary>Answers</summary>

1. I = min(P, S), S = s · LAI. P = rain depth of the event, S = canopy storage (mm), s = storage per unit leaf area index, LAI = leaf area index.
2. Calibrated on Anys & Weiler (2024) Freiburg field data (16 trees, 51 storms). Lower bound 0.86 mm = surface storage only (Xiao & McPherson 2016).
3. Field evidence (Selbig et al. 2021): street trees cut volume ~4% but did not change peak flow.
4. Canopy storage is filled in the first few mm; the rest of a large storm passes through, so the intercepted share falls.
5. Only two lab studies, young trees in tanks; species differences unclear (Bartens: oak vs maple not significant).
6. With the v1 LAI proxy, every crown is full at every design storm, so interception is constant; the % falls only because total runoff grows. It follows from the model's own equation.
</details>

---

## 4. Heat science
Sources: `notes/methodology.md` §3, §5; `notes/topic_decision.md` §6.1.

- **UTCI** (Universal Thermal Climate Index) = "felt" temperature for a pedestrian, from air temperature, humidity, wind and **mean radiant temperature (MRT)**. Shade lowers MRT the most.
- **Strong heat stress = UTCI > 32 °C** (stress classes from Bröde et al. 2012, still to add to Zotero).
- **Canopy transmissivity (Beer–Lambert):** **τ = exp(−k · LAI), k = 0.5**. More leaf area → less sun through the crown.
- **Ladybug Tier 1** (fast, many layouts): point UTCI at 1.1 m on a 2 m sidewalk grid. Limit: crowns are opaque, so shade MRT is underestimated; fix by multiplying direct radiation under crowns by τ (Peng et al. 2026). Ladybug ignores evapotranspiration, so it likely underestimates vegetation cooling by ~2–3 °C UTCI (Mannucci et al. 2025).
- **Tier 2** (few layouts): Honeybee UTCI comfort map with leaf-on/off transmittance.
- **Infrared City API** (tutor co-founded it): AI surrogate for UTCI in seconds; access still to confirm. Ladybug stays as fallback and cross-check.
- **Transpiration** is the stronger *air*-cooling term (Park 2026: 1.15 °C vs shade 0.43 °C), but needs soil water.
- **Heatwave risk:** *Platanus* lost roughly 30–50% of its plant area index after a > 41 °C heatwave (Sanusi & Livesley 2020) → low-LAI plane variant in sensitivity.
- **Night:** dense clusters trap heat at night (Zölch et al. 2019); the design hour misses this → stated limit.
- **Transpiration matters less in Porta:** per leaf area it is lowest in Mediterranean climates and ~10× lower for trees in paved pits than over grass, while shade cools asphalt the most (Rahman et al. 2019 meta-analysis). So Ladybug's missing transpiration is a smaller error here.

**Choosing the heat metric (`notes/decisions/heat_objective.md`, pending your decision):**
- On the **hottest** El Prat day, even full shade is ≥ 32 °C in 5 of 6 afternoon hours, so "share of points > 32 °C" **saturates** and cannot show a benefit.
- The **sun–shade gap is 2.3–4.7 °C UTCI** (full shade; a lower bound for a tree), and the **Ladybug model error is 1–2 °C**: trust **rankings** of layouts more than absolute values.
- Recommended default: **mean UTCI over 12–17 h on the design (DDY) cooling day**, plus the hottest real day as a check. This would change the RQ wording from "peak summer hour" to "12–17 h window on a hot design day".
- **Weather (`notes/decisions/weather_forcing.md`, pending):** main run El Prat TMYx 2011–2025; sensitivities with the Barcelona city station file, city-terrain wind, and an urban offset of **0 to +1.5 °C**.

### Check yourself
1. What is UTCI and which input do trees change most?
2. Write the transmissivity formula and its k.
3. Two reasons why Ladybug Tier 1 underestimates tree cooling.
4. Why use a heat *proxy* inside the optimiser?
5. Why is "share of points above 32 °C" a weak metric on the hottest day?

<details><summary>Answers</summary>

1. A pedestrian "felt temperature" index; trees change mean radiant temperature (shade) most.
2. τ = exp(−0.5 · LAI).
3. Crowns treated as opaque solids without the τ correction (shade MRT wrong), and no evapotranspiration.
4. Ladybug costs minutes per layout (20–25 min for 42 trees, Shaamala 2025); 832 positions × many layouts is impossible, so a shade × τ proxy, a surrogate or Infrared City runs in the loop.
5. Even full shade stays ≥ 32 °C in 5 of 6 afternoon hours, so sun and shade count alike: the metric saturates.
</details>

---

## 5. Same tree, two jobs: synergy and trade-off
Source: `notes/topic_decision.md` §6.1.

| | Heat | Runoff |
|---|---|---|
| **Shared drivers** | LAI and crown size → more shade | LAI and crown size → more interception |
| **Conflict 1: leaf habit** | Evergreen blocks *winter* sun (a cost) | Evergreen intercepts in autumn–winter storms (a benefit) |
| **Conflict 2: water** | Transpiration cools, needs soil water | — |

**Key finding of tool v0:** with the city palette there was **no trade-off at first** (the Pareto front collapsed to a point: bigger, denser crowns win both). Adding the leaf calendar did not help: **78% of intense storm days fall in May–Oct**, when all palette species are in leaf (Esbrí et al. 2026). The first **real trade-off appeared with winter sun access** (winter shade counted as a cost).

**Mnemonic:** *"Big crowns win both; leaves in winter split them."*

### Check yourself
1. Which traits help both objectives? Which create the conflict?
2. Why did the leaf-on calendar not create a trade-off?
3. What finally created one?

<details><summary>Answers</summary>

1. LAI and crown size help both. Leaf habit (evergreen vs deciduous) and transpiration/water demand create the conflict.
2. 78% of intense storm days are in May–Oct, when every palette species is in full leaf.
3. Counting winter shade on sunlit open ground as a cost (winter sun access).
</details>

---

## 6. The gap and the closest precedents
Sources: `notes/topic_decision.md` §6.1, §7; `slides/outline_20oct.md`; `notes/decisions/contribution_statement.md`.

| Work | What it does | What it lacks |
|---|---|---|
| **SylvCiT** (Nicol et al. 2026) | Trait-based tree recommender, Montreal | Runoff module **disabled**; no heat; diversity traits, not eco-hydrological |
| **Mannucci et al. 2025** | Grasshopper + Ladybug + Kangaroo: UTCI **and** runoff | Fixed scenarios, **no species traits, no optimisation** |
| **Shaamala et al. 2025**, **Peng et al. 2026** | Optimise species/placement | **Heat only**; Shaamala names water as future work |
| **Tan & Liu 2026** (closest) | NSGA-II + Random Forest surrogate in Grasshopper, species + positions of 30 trees, UTCI + CO2 + diversity | **No runoff**; 4 Chicago species, US allometry, one summer hour |
| **Cortinovis et al. 2022** | Heat + runoff for Barcelona | City-wide; trees as land cover |
| **Dong et al. 2026** (new close neighbour) | NSGA-III over species **mixes** for stormwater + microclimate (+ air quality, carbon), Philadelphia | Heat = **building-energy proxy**, not UTCI; runoff = i-Tree Eco; **no tree positions** (species shares per 0.25 km² cell) |

**The gap in one line (safe wording):** *no method yet chooses street-tree species **and positions** against **pedestrian-level UTCI** and **event runoff** together.* Never say just "species for heat and runoff": Dong 2026 does that, at cell scale with an energy proxy.

**Contribution (three candidates, pending your decision):** **A. Method:** a reproducible workflow that selects replacement species and positions against UTCI and runoff, with LiDAR crowns, a trait table and a leaf-on interception term. **B. Knowledge:** a quantified cooling-vs-interception comparison for the city's palette in Porta (how large is the trade-off?). **C. (optional) Validation:** a transparent two-tier check of the fast heat proxy against Ladybug, with known error bars. Plus: most replacement species lack measured traits, and the data gap itself is a result.

### Check yourself
1. Name the closest precedent and three things this thesis adds to it.
2. What is SylvCiT and what is missing in it?
3. State the gap in one sentence, in the safe wording.
4. What does Dong et al. 2026 do, and why does it force narrower wording?

<details><summary>Answers</summary>

1. Tan & Liu 2026. Adds: runoff, the city's own replacement palette, the seasons (leaf calendar, winter sun).
2. Trait-based AI recommender for urban forests (Montreal); runoff module disabled, no heat, diversity traits only.
3. No method yet chooses street-tree species and positions against pedestrian-level UTCI and event runoff together.
4. NSGA-III over species mixes for stormwater and microclimate in Philadelphia, but heat is a building-energy proxy, runoff is i-Tree Eco, and there are no tree positions. So the claim must name "positions" and "pedestrian UTCI".
</details>

---

## 7. Research question and hypotheses (learn word-perfect)
Source: `notes/topic_decision.md` §7.

**RQ:** *In Porta, as plane trees are replaced under the city's tree plan, which replacement species and positions jointly reduce (a) pedestrian heat stress (UTCI at the peak summer hour along sun-exposed routes) and (b) event runoff volume from sealed street surfaces (1-, 2- and 10-year design storms from the PDISBA rainfall curves)? How large is the trade-off between the two, compared with the current trees, a like-for-like replacement with the city's named palette, and single-objective layouts?*

- **H1, synergy:** same number and size class of trees → trait-based layouts beat like-for-like on **both** goals (crown size and LAI drive both).
- **H2, trade-off:** heat-optimal and runoff-optimal layouts differ mainly in **species**, not positions (leaf habit, transpiration) → the Pareto front is not a single point.
- **H3, validity boundary:** the runoff benefit **shrinks as the return period grows**; small at T = 10 yr; extreme events (6 Sept 2018, ≈300-yr 20-min intensity) are outside what trees can affect.

**Mnemonic: S-T-B** = **S**ynergy, **T**rade-off, **B**oundary.

**Status of the hypotheses (memos, pending your decision; the wording above is still the official v4):**
- **H1, runoff part:** a minimum meaningful difference **Δmin = 91 m³** (0.9 mm over the street crowns, 0.5% of T2-60 runoff) is proposed, fixed before the runs. If the best layout beats S1 by less than Δmin, the runoff part is reported as **"not resolved by the model"**: accepted as a valid outcome (user, provisional, 14 Oct). Today's exploratory value is **78 m³** (worst case 38.5 m³) → not resolved. Then heat carries the species choice and runoff becomes a check.
- **H2:** proposed as a species-composition claim (S2 vs S3 differ by more than a pre-fixed dissimilarity) at the fixed plane positions.
- **H3:** proposed as a **declared boundary of the method**, not a test result (it is true by construction, §3). Question for the tutor: is that acceptable?
- **Trade-off metric (proposed):** % loss of one objective at the other's optimum.

### Check yourself
1. Say the RQ in under 40 words.
2. Name H1–H3 and the scenario comparison that tests each.
3. What is Δmin, and what happens if the best layout beats S1 by less than it?

<details><summary>Answers</summary>

1. In Porta, which replacement species and positions jointly reduce UTCI and runoff volume (1-, 2-, 10-yr storms), and how large is the trade-off versus current trees, like-for-like and single-objective layouts?
2. H1 synergy: S4 vs S1 on both objectives. H2 trade-off: species composition of S2 vs S3. H3 boundary: runoff benefit vs return period T.
3. The minimum meaningful runoff difference, 91 m³ (0.5% of T2-60 runoff). Below it, the runoff part of H1 is "not resolved by the model" (neither supported nor rejected).
</details>

---

## 8. Method and tool
Sources: `notes/methodology.md`, `shade_sponge/README.md`.

**Pipeline (5 steps):** LiDAR trees → trait table → runoff module + heat module → optimiser → Pareto front → test on Sant Antoni and Florence.

- **Data:** street trees (Ajuntament `arbrat-viari`), **ICGC LiDAR** (flown 26 Sept 2021, leaf-on; ≥ 8 pts/m², CC BY 4.0), PDISBA IDF, Resilience Atlas flood-hazard index, **RESCCUE flood-depth maps T10/T100** (public CARTO tables, found 13 Oct; licence email sent), EPW (Barcelona El Prat), trait databases (3TF, BROT 2, literature).
- **Tree model:** position, species, height H, crown diameter D, crown base Hb, LAI (leaf-on/off), storage S, leaf habit, wood anatomy. Missing species → genus or leaf-habit class values with a range + sensitivity.
- **Scenarios:** **S0** current trees · **S1** like-for-like palette · **S2** heat-only optimum · **S3** runoff-only optimum · **S4** multi-objective Pareto set.
- **Optimiser:** NSGA-II (pymoo or Wallacei). Constraints: **≤ 15% per species**, Shannon diversity floor, no invasive or pest-host species, crown clearance from façades. **v0** uses a weighted-sum LP instead (HiGHS).
- **Tool package `shade_sponge/`:** `site.py` (1 m grid), `topo.py` (Priority-Flood routing on the DTM → water convergence, distance to flood hotspots), `heat.py` (sun position, elliptical crown shadows, opacity from LAI and leaf month), `season.py` (leaf calendar, storm months), `runoff.py` (bucket + SCS-CN), `layout.py` (palette, cap, LP, Pareto).
- **One core, two front-ends:** Grasshopper (primary, computational designer) and a later web app (non-technical users).
- **Palette in the tool:** the six city species + *Styphnolobium*. Species crowns and LAI come from one function, `species_lidar()` in `site.py`: Porta LiDAR medians, with a hard-coded override for *Styphnolobium* (sample outside Porta).
- **Every parameter is cited or marked ASSUMPTION** (e.g. `CAPTURE_M` = 100 m, `OP_BARE` = 0.35, `R_OFF` = 0.5).
- **Routing vs RESCCUE (checked 15 Oct):** upstream area barely separates RESCCUE wet from dry cells overall (**ROC AUC 0.52**), but the top 0.5% of open ground by upstream area is wet in **58–80%** of cases (1.7–2.6× random). So the routing finds the **main convergence points** but is **not a flood map**: hotspots stay tied to the atlas index (or RESCCUE depth).
- **Proposed tool changes (methodology §12, not adopted):** weight shade by ground surface (asphalt cools ~2× grass); check SVF/street orientation of chosen positions; tag k = 0.5 as ASSUMPTION; keep R_OFF = 0.5 with new birch anchors; add birch/pine storage anchors (1.00–1.08 mm per LAI) to the s sensitivity range.

**Mnemonic for scenarios: "Now, Swap, Hot, Wet, Both"** = S0 now · S1 swap like-for-like · S2 hot (heat only) · S3 wet (runoff only) · S4 both.

### Check yourself
1. List S0–S4.
2. Name the optimiser and its four constraints.
3. What does `topo.py` add that runoff v1 did not have?
4. What is the rule for every parameter in tool code?
5. What did the comparison with RESCCUE show about the routing?

<details><summary>Answers</summary>

1. S0 current, S1 like-for-like palette, S2 heat-only, S3 runoff-only, S4 multi-objective Pareto set.
2. NSGA-II; ≤ 15% per species, Shannon diversity floor, no invasive/pest hosts, façade clearance.
3. Flow routing on the DTM, so runoff that reaches flood hotspots can be targeted (positions upstream of hotspots).
4. Either sourced (cited) or marked ASSUMPTION.
5. It finds the main convergence points (top 0.5% of upstream area mostly wet) but is not a flood map (AUC 0.52); hotspots stay tied to the atlas index.
</details>

---

## 9. First results
Sources: `notes/methodology.md` §4b, §6; `shade_sponge/README.md`.

**Runoff v1 (T2, 60 min):**
- Current street trees cut Porta's runoff by **1.85%** (open space only: **2.9%**). Range over s and T: **0.4–4.0%**.
- Same order as the field benchmark (**3.5–4%**, Selbig 2021 / Coville 2022). Barcelona city-wide also small (Cortinovis 2022: 20,170 new trees, retention 50.18% → 50.76% for a 20 mm event).
- **Any young replacement: ≈ +0.7% runoff ≈ 37% of the current street-tree benefit lost** during the transition ("more than a third").
- Benefit shrinks with return period (as a %), but in the model this is arithmetic, not a test of H3 (§3).

**Styphnolobium (15 Oct):** a LiDAR sample from one 1 km tile outside Porta gives crown **5.32 m / LAI 2.12** from **367 trees on 25 streets** without possibly merged crowns (the tool uses these; all 607 trees give 6.43 m / 2.28). With them it ranks **5th of 8 palettes** (aggregate) and **4th of 7** (grid), and replacing the planes with it **adds runoff** (+92.5 m³, +0.52% at T2-60). Best palette: Melia (aggregate) or Jacaranda (grid). Best vs S1: **78 m³ < Δmin 91 m³** → runoff part of H1 not resolved. (The earlier 14 Oct result, where Styphnolobium came first, used only 5 Porta trees and is superseded.)

**Tool v0 (shade proxy + runoff):**
- Optimised (balanced) vs random palette: **+14% summer shade** (robust across 7 sensitivity variants).
- **No-regret swap:** summer-only → balanced cuts winter shade by **9%** at equal summer shade by swapping ~100 **Tipuana → Jacaranda** (Jacaranda is bare Jan–Mar).
- Beyond balanced: a **real trade-off** (more winter sun costs summer shade).
- **Placement follows the buildings:** winter-bare Jacaranda goes where the street is sunny in winter; winter-leafed species go where buildings already shade it.
- **Open problem:** hotspot runoff does not follow the runoff weight (to investigate).
- **No replacement layout reached S0** (mature planes): replacement always loses shade at first.
- Tool v0 numbers above are from the 8 Oct run with the six city species; they have not been re-run with *Styphnolobium*.

### Check yourself
1. How much do Porta's street trees cut runoff, and is it plausible?
2. What happens during the transition to young trees?
3. What is the "no-regret swap"?
4. Why did Styphnolobium drop from first to fifth?

<details><summary>Answers</summary>

1. 1.85% at T2-60 (2.9% on open space); same order as the 3.5–4% measured in the field.
2. Young replacements lose ≈ 37% (more than a third) of the current street-tree runoff benefit.
3. Swapping ~100 Tipuana for Jacaranda: same summer shade, 9% less winter shade.
4. The first result used the medians of only 5 Porta trees (crown 8.85 m, LAI 3.32); the sample outside Porta (367 trees without merged crowns) gives a smaller crown (5.32 m) and LAI (2.12).
</details>

---

## 10. Limits (say them before the tutor does)
- Flood indicator is a hazard **index**, not water depth. RESCCUE depth maps (T10, T100) are now public; licence for thesis use asked on 13 Oct. Our routing is not a flood map (AUC 0.52).
- Surface temperature (Landsat) ≠ pedestrian UTCI.
- LiDAR LAI proxy (~2.3) probably **too low** → storage underestimated.
- Same s for every species; species differ only via crown and LAI.
- **Volume only**: no sewer, no routing to outlets, no ponding.
- EPW from the airport, not the city (test +1/+2 °C).
- Design hour misses night effects.
- **H3 is true by construction** in the bucket model; declare it as a boundary.
- Runoff differences between palettes may stay below Δmin: the runoff part of H1 may be "not resolved".
- Most palette species lack measured traits → ranges + sensitivity; **the gap is a finding**.
- Seminar gaps: no stakeholder validation yet; innovation type and TRL not yet stated (claim **TRL 3**, process innovation) (`notes/research_method_guidelines.md`).

---

## 11. Likely tutor questions (practise answering in 20 seconds each)
Sources: `slides/outline_20oct.md`; the Porta and Barcelona answers from `notes/site_selection.md` and `notes/city_screening.md`.

| Question | Short answer |
|---|---|
| Why not peak flow? | Trees barely change peak flow in the field (Selbig 2021); volume is what they change. |
| Hasn't Tan & Liu 2026 done this? | Heat, CO2, diversity only; no runoff, 4 Chicago species, one summer hour. I add runoff, the city's own palette and the seasons. |
| Is a 2% effect worth a thesis? | The thesis is the method and the trade-off, not a big runoff number. H3 states the limit; heat may dominate. |
| Where do species values come from? | LiDAR crowns and LAI on site, database traits, genus/leaf-habit proxies with sensitivity ranges. |
| Why Porta and not Sant Antoni? | Porta passes both hazards at every threshold; Sant Antoni's heat is below the city median. |
| Why Barcelona and not Florence? | Heat-health evidence, LiDAR, open data and site access; Florence becomes the transfer test. |
| What if the scope is too narrow? | Widen the tree into a system: add the tree pit as one design variable; carbon reported, not optimised. |
| Hasn't Dong et al. 2026 done this? | They optimise species mixes per 0.25 km² cell with an energy proxy for heat and i-Tree runoff. I choose species and positions per tree, against pedestrian UTCI and event runoff. |
| Isn't H3 true by definition of your model? | Yes, in the model every crown is full, so I declare H3 as a boundary of the method. In field data the intercepted fraction also falls as rain depth grows (Anys & Weiler 2024). |
| What if runoff can't tell the palettes apart? | Then the runoff part of H1 is "not resolved" (below Δmin = 91 m³, fixed before the runs); heat carries the species choice, runoff is a check. That is still a result. |
| How good is your flood routing? | It finds the main convergence points but is not a flood map (AUC 0.52 vs RESCCUE depth); hotspots come from the atlas index. |

---

## 12. Glossary
| Term | Meaning |
|---|---|
| **Pluvial flood** | Flooding from rain on the surface when drainage is overwhelmed (vs **fluvial** = river) |
| **Return period T** | Average interval between storms of that size; T = 10 yr ≈ 10% chance per year |
| **IDF curve** | Intensity–Duration–Frequency: rain intensity for a given duration and return period |
| **PDISBA** | Barcelona's drainage master plan; source of the design storms |
| **SCS-CN** | Curve-number method: runoff from rain depth and a surface number (98 = sealed) |
| **Interception** | Rain held on leaves and bark that evaporates without reaching the ground |
| **Canopy storage S** | Water depth (mm) a crown can hold; here S = s · LAI |
| **LAI** | Leaf area index: one-sided leaf area per unit ground area under the crown |
| **Stemflow** | Rain that runs down the trunk (< 1% here, ignored) |
| **UTCI** | Universal Thermal Climate Index, "felt" temperature for a pedestrian (°C) |
| **MRT** | Mean radiant temperature: radiation load on the body; shade lowers it |
| **τ (tau)** | Canopy transmissivity, exp(−0.5·LAI) |
| **UHI** | Urban heat island |
| **LST** | Land surface temperature (satellite) |
| **EPW** | EnergyPlus weather file used by Ladybug |
| **Ladybug / Honeybee** | Grasshopper plugins for climate analysis / building and comfort simulation |
| **Pareto front** | Set of layouts where no objective can improve without another getting worse |
| **NSGA-II** | A genetic algorithm for multi-objective optimisation |
| **Weighted-sum LP** | Single-objective linear program with weights on each goal (tool v0) |
| **Surrogate / proxy** | Fast stand-in for a slow simulation |
| **Priority-Flood / D8** | DTM flow-routing methods: where water goes downhill |
| **LiDAR, DTM, DSM** | Laser scan; terrain model; surface model (incl. trees, buildings) |
| **Leaf habit** | Evergreen vs deciduous |
| **Non-compensatory** | Every criterion must pass; one cannot offset another |
| **TRL** | Technology Readiness Level (thesis: TRL 3, proof of concept) |
| **RESCCUE** | EU project whose Barcelona flood model gives water-depth maps (T10, T100) |
| **Δmin** | Minimum meaningful difference, fixed before the runs (runoff: 91 m³) |
| **DDY** | Design-day file: a synthetic hot (or cold) design day for a station |
| **ROC AUC** | How well a score separates two classes; 0.5 = no better than chance |

---

## 13. Key numbers cheat sheet
| Number | What |
|---|---|
| 45% → 72% | Barcelona sealed surface, 1956–2009 |
| ~3 / yr, 60 mm/h | Storms above 60 mm/h in the first 20 min |
| 15% | Max share per species (tree master plan) |
| ~29% | Plane trees among street trees (city and Porta) |
| 0.84 km² | Porta area |
| 832 | Plane trees in Porta (194 on Av. Meridiana) |
| 2,825 / 53 | Street trees / taxa in Porta |
| #13, #11, #12 | Porta's ranks: flood, surface heat, heat vulnerability |
| +1.36 °C | Porta summer surface-temperature anomaly |
| 60th pct | Eligibility threshold (robust at 50th and 70th) |
| 2,000 | Random weightings in the robustness test |
| 1.75 mm/LAI | Calibrated canopy storage per unit LAI |
| 0.86 mm | Lower-bound storage (Xiao & McPherson 2016) |
| 2–4 mm | What a leafy crown holds at the start of a storm |
| 98 / 74 | Curve numbers: sealed / pervious |
| 19.6 / 31.9 / 62.5 mm | T1 / T2 / T10, 60-min design storms |
| 1.85% (2.9%) | Runoff cut by current street trees, T2 (open space) |
| 3.5–4% | Field benchmark (Coville 2022 / Selbig 2021) |
| ≈ 37% | Benefit lost with young replacements |
| k = 0.5 | Beer–Lambert extinction coefficient |
| 32 °C | UTCI threshold for strong heat stress |
| 78% | Intense storm days in May–Oct |
| +14% | Summer shade, optimised vs random palette |
| −9% | Winter shade, no-regret swap Tipuana → Jacaranda |
| 7 | Candidate species (6 city-named + *Styphnolobium*) |
| 367 / 5.32 m / 2.12 | *Styphnolobium* LiDAR sample outside Porta (no merged crowns): trees / crown / LAI |
| 91 m³ | Δmin, runoff part of H1 (0.5% of T2-60 runoff) |
| 78 m³ | Best palette vs S1 today (below Δmin → not resolved) |
| 3.16% → 0.90% | Street-tree effect, T1 → T10 (arithmetic of the model) |
| 2.3–4.7 °C | Sun–shade UTCI gap on hot afternoons (lower bound) |
| 0.52 | ROC AUC of routing vs RESCCUE wet cells |
| 18 Dec 2026 | Probable final delivery |
| 20 Oct 2026 | Next tutor session |

---

## 14. Decisions waiting for you (as of 15 Oct)
Know these exist and what the recommended default is; the tutor may ask. Only the "not resolved" rule for H1's runoff part is provisionally accepted (14 Oct); the rest is open.
| Decision | Recommended default | Source |
|---|---|---|
| Heat metric f1 | Mean UTCI, 12–17 h, DDY cooling day (+ hottest real day as check) | `notes/decisions/heat_objective.md` |
| Weather forcing | El Prat TMYx 2011–2025, file wind, no offset; sensitivities: city station, city-terrain wind, +1.5 °C | `notes/decisions/weather_forcing.md` |
| Hypothesis wording | H1 with Δmin and "not resolved"; H2 as species composition; H3 as a declared boundary | `notes/decisions/hypothesis_tests.md`, `runoff_metric_sensitivity.md` |
| Contribution statement | No default given: choose among A (method), B (knowledge), C (validation, optional) | `notes/decisions/contribution_statement.md` |
| Tool changes | Methodology §12 items 1–5 | `notes/methodology.md` §12 |
