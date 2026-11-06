# Study guide: Shade and Sponge (state of 3 Nov 2026)

A condensed version of the thesis for **learning it**, not for writing it. Every fact here comes from the project notes; the source file is named in each chapter, so check there when a number changes. If a note is updated, update this guide and the cards (`flashcards.csv`, `quiz.csv`).

**How to read it:** read one chapter, close the file, answer its **Check yourself** questions out loud or on paper, *then* open the answers. Do not reread before you have tried to recall (see `README.md` for why).

---

## 0. The thesis in 30 seconds (learn this by heart first)

> Barcelona has decided to remove more than half of its plane trees within ten years. Its tree master plan says **how much** of each species the city may have (no species above 15%), and its street-tree rules say **which tree size fits which sidewalk**. The only documented rule for **which species replaces a tree** is qualitative (a 2004/2005 table by district and sidewalk width), Porta's plantings mostly do not follow it, and no rule measures what each choice does to heat or runoff. In **Porta (Nou Barris)** the same streets suffer **summer heat stress** and **pluvial flooding**, and tree cover is already below the city's target. My thesis is **a computational method that takes the city's rules as constraints and chooses replacement species for plane trees and new planting spots that retain more cooling and rain interception than the city's own practice**, first in Porta, then over 28 barris in one city-wide optimisation.

**One sentence:** *the city fixes how much; the method decides which species where, within the rules, and keeps more shade than the city's own mix → heat no worse than today's planes in UTCI, runoff below what the model resolves.*

**The 10 Nov message in three sentences (learn these first):**
1. Barcelona will replace more than half of its planes, and the only rule for the new species is qualitative: nobody measures what changes for heat and runoff.
2. The method chooses species and positions inside the city's rules (15% cap, sidewalk rule) and compares them with the city's own practice (S1a press mix, S1b observed mix).
3. It keeps more summer shade than the city's rule in every barri tested on its own (27 of 28 in the joint city run); in UTCI it is "no worse than today's planes"; for runoff the difference is below what the model can resolve.

**The logic chain (the tutor's order):** problem → why it matters → gap → research question → hypotheses → method (data, tools) → tool → first results → limits.

### What changed from 21 Oct to 3 Nov (v7 — learn this first)
- **Gate 1 answered (24 Oct):** the city *does* have a replacement rule on paper, the Parcs i Jardins 2004/2005 table by district × sidewalk width (Nou Barris: *Prunus cerasifera* < 3.5 m, Melia or Jacaranda 3.5–6 m, keep the plane > 6 m). Its criteria are tolerance, typology, tradition, experience: **no heat, no runoff**. The 2011 guide no longer prints it, and in Porta up to ~90% of 2007–2026 plantings on narrow and medium sidewalks are other species (an upper bound). So the problem is "a qualitative rule, not visible in practice, that measures nothing" (§1).
- **"Are there enough trees?" answered:** no. Porta's tree cover is **20.1%** (LiDAR 2021) against the city's **30%** 2037 target (8.3 ha short), and planes are **~29%** of its canopy (§1).
- **RQ v7** (24 Oct): "reduce" became "**retain**", the method is compared with the city's rule (S1), additions of new trees are co-equal, and there are **four sub-questions** (§7).
- **Results v7** for Porta (replacement, additions, both), **33 barris** run one by one, and a **city-wide LP over 28 barris** with the 15% cap and a local ceiling (§9b).
- **A second baseline, S1b = the city's observed replacement mix** (1,444 plane replacements 2018–2026 from the quarterly inventory, 31 Oct). The tool beats both S1a and S1b. Decided 6 Nov: S1b is the reference baseline, S1a stays beside it, and the 2004/2005 table is renamed **S1-2004** (cited, not run) (§9b).
- **The first UTCI check is done (2–3 Nov):** Ladybug Tier 1 rebuilt in Python, Honeybee Tier 2, porous crowns. Claim for heat: **no worse than today's planes**, not "cooler" (§9c).
- **Policy chain checked (31 Oct):** Nature Plan = area targets only; Climate Plan 2024 p.33 = +5% tree cover, adapted species 30→40%, 7 ha SUDS, 9 ha shade. None sets species per position (§1).
- **Grasshopper is not required** by the programme (30 Oct); co-benefits (pollen, carbon, diversity) are a **backup slide only** before 10 Nov (3 Nov).

### What changed on 21 Oct (v6)
- **The tree master plan was read in full** (20 Oct) and the problem was **rebuilt on it** (`notes/topic_decision.md` §9, `notes/tree_master_plan.md`). The tutor's 20 Oct feedback (as you reported it): the problem was not defined well enough.
- **The answer to "hasn't the city already solved this?":** no. The city decided *how much* (15% cap; planes cut by 56% to 12% in ten years, press) and *which size fits which sidewalk* (2011 guide). It did **not** decide *which species at each position*, and nothing it publishes measures heat or runoff (§1).
- **S1 changed:** it is now **the city's own replacement**, i.e. the 2026 target mix assigned by the city's sizing rule, not "like-for-like" (§7, §8).
- **Palette correction:** only **Celtis, Melia, Pyrus calleryana, Styphnolobium, Tipuana** are named by the city as plane replacements. **Jacaranda and Brachychiton are not**; they stay in the palette, labelled "not named" (§1).
- **The cap is city-wide**, so the tool's Porta-local cap is an ASSUMPTION; **planes on large avenues are kept** by the city (Av. Meridiana holds 194 of Porta's 832); the **sidewalk width** becomes a constraint (§8).
- **Crown check:** at equal trunk size (2nd and 3rd trunk classes), Tipuana and Jacaranda keep 89–107% of a plane's crown area, Melia 71–81%, Celtis 32–52%, Pyrus 35%, Brachychiton 24–27% (§1).

### What changed on 19 Oct (your two decisions)
- **The heat metric is decided: mean UTCI over the 12–17 h window on a hot design day**, not UTCI at the peak summer hour. The peak-hour metric saturates (on the hottest day even full shade is ≥ 32 °C in 5 of 6 afternoon hours), so no layout could show a benefit. The RQ wording follows (§7).
- **H3 is withdrawn. The thesis has two hypotheses, H1 and H2.** The content of H3 stays as a **declared validity boundary** of the method, and you say openly that it *was* a hypothesis until the model showed it true by construction. Removing it is a result about the method, not a retreat (§7, §9, §11).
- Both are recorded in `notes/topic_decision.md` §8 (v5).

### What changed since 15 Oct (read this first if you studied the earlier version)
- **A whole new chapter, §10 Transferability**, and with it **slide 16** of the talk: the code travels, the evidence does not. It is the answer to the tutor's "contribution to knowledge", so treat it as core, not as an appendix.
- **The transfer city is decided: Mataró** (19 Oct), not a generic "Catalan city" and not Badalona. Reason: it is the only candidate with a **published design storm of its own** — borrowing Barcelona's IDF would make the transfer test circular (§10).
- **Florence stays the first-choice transfer case** but its point cloud is request-only, and the *Life Escapos* dataset that looked like a way round it **failed** (its LAI column is synthetic) (§10).
- **A negative result worth saying out loud:** **no Catalan city has a pluvial hazard map**. That is *why* Porta was the right place to calibrate (§10).
- **One comparison you must not quote raw:** Mataró's design storm looks 19–32% drier than Barcelona's, but most of that gap is **method, not climate** — an envelope against a central estimate (§10).
- **The talk was rebuilt on 19 Oct** to follow this guide's rhythm: **17 slides + 3 backups**, one idea each, with a written spoken script per slide (`slides/outline_20oct.md` v3; figure files are numbered by slide). The two RM-seminar figures (plane-tree map, cluster map) are **out of the tutor deck** and parked in `slides/seminar_rm/`.

### What changed since 9 Oct (older, keep for reference)
- **A seventh candidate species:** *Styphnolobium japonicum* (user decision, 14 Oct). Its crown and LAI now come from a LiDAR sample outside Porta (§1, §9).
- **The gap needs narrower wording** because of Dong et al. 2026: say "species **and positions**" and "**pedestrian UTCI**" (§6).
- **H3 was true by construction of the model:** with the v1 LAI proxy every crown is full at every design storm, so the falling % is arithmetic, not a test. This is what led to withdrawing it on 19 Oct (§3, §7).
- **The runoff part of H1 may come out "not resolved by the model":** accepted as a valid outcome (user, provisional, 14 Oct) (§7, §9).
- **RESCCUE flood-depth maps are public**, and the routing was checked against them (§8, §11).
- **Leaf calendar from photos (15 Oct):** Jacaranda is mostly in leaf in January. Re-run: the "no-regret swap" shrank from −9% to −2% winter shade and is not robust; the summer–winter trade-off holds (§5, §9).
- **Several decisions wait for you** (heat metric, weather file, hypothesis wording, contribution statement): listed in §15.

---

## 1. The problem
Sources: `notes/topic_decision.md` §10 (v7), §9 (v6) and §7; `notes/tree_master_plan.md` §5b, §8.

**The problem in one sentence (v7, slide 5):** *When Barcelona replaces a plane tree, the only documented rule for the new species is qualitative (district, sidewalk width, tradition; 2004/2005). Current practice is unpublished, and no rule quantifies heat or runoff. So thousands of replacements over the next decade will change how much shade and rain interception each street keeps, and nobody measures by how much.*

**Context ≠ problem ≠ gap (keep them apart):**
- **Context** (decided, not your problem): planes cut by more than half; 15% cap; size class by sidewalk width; replacement one tree at a time.
- **Problem:** (1) the rule exists and is qualitative; (2) it is not visible in practice (up to ~90% of Porta's 2007–2026 plantings on narrow/medium sidewalks are other species, an upper bound); (3) no rule quantifies the consequences; (4) the consequences are large (crowns differ three- to fourfold at equal trunk size); (5) they fall where both hazards overlap.
- **Gap:** practice has rules but no quantities; research assesses heat + runoff without species (Mannucci 2025; Wu 2024) or optimises heat only (Shaamala 2025; Peng 2026); SylvCiT has runoff switched off; the diversity literature calls caps rules of thumb (Santamour 1990; Kendal 2014).

**Gate 1, the 2004/2005 table (Parcs i Jardins), Nou Barris:** *Prunus cerasifera* below 3.5 m · Melia or Jacaranda 3.5–6 m · **keep the plane** above 6 m. Criteria: tolerance, urban typology, tradition, technicians' experience. This is why Jacaranda now counts as named (for medium sidewalks), while Brachychiton is still not named anywhere. **Baseline:** decided 24 Oct as S1a (the 2026 press mix); **from 6 Nov the reference is S1b, the city's observed replacement mix**, with S1a beside it. The table is called **S1-2004** and is cited in the problem chapter, not run.

**Are there enough trees? (tutor, 20 Oct)** No. City target **30%** tree cover by 2037 (plan 2017, target 1). **Porta 20.1%** of 83.7 ha (CHM > 2 m, LiDAR 2021), ~10 points and **8.3 ha** short. Plane crowns = 5.75% of the area, **~29% of the canopy**. At equal trunk size, all-Brachychiton crowns would bring Porta to **~16%**; Tipuana or Jacaranda keep it roughly level. Outside benchmark: only 8.7% of 3,145 Barcelona residents met 3-30-300's 30% criterion (Nieuwenhuijsen et al. 2022).

**The policy chain (31 Oct; `notes/tree_master_plan.md` §8):**
| Document | What it sets | What it does not |
|---|---|---|
| Tree master plan 2017–2037 | 15% per species; 30% tree cover; 40% adapted species | species per position; heat or runoff per tree |
| Nature Plan 2021–2030 | area targets only | no street-tree or canopy target; "which species for shade, where" is a study still to do (project 83, p.114) |
| Climate Plan 2024 | p.33: tree cover +5% by 2037, adapted species 30→40%, 7 ha SUDS, 9 ha shade; p.43 "aligned tree pits" | targets in hectares and shares, never per tree |

**Your line:** *every level sets areas or shares; none says what a species does at a position. That is the gap the method fills.*

**What the city has decided, and what it has not (learn the two lists):**
- **Decided:** reduce the planes (no species above **15%** of the urban fabric by 2037, master plan target 3; planes cut by **56%**, from **43,722 (27.45%)** to **12%**, within ten years, press May 2026); **how** (gradually, as trees die and when streets are rebuilt); **which species may be used** (the city's catalogue and a 2026 target mix, press); **which size fits which sidewalk** (2011 street-tree guide).
- **Not decided:** **which species at each position** (the city says it set the possible replacements in advance from criteria; the list is not public); **what each choice does to heat and runoff** (no document quantifies it); **priority where heat and flooding overlap**.
- **Why the cap exists:** pest and disease risk of a monoculture, climate resilience, biodiversity (plan §1.4.4, §2.1; 2011 guide). **The plan derives no number**, but 15% sits at the loose end of the 10–15% species benchmarks in the literature (Kendal et al. 2014); Santamour's classic rule (1990) says 10% per species, 20% per genus, 30% per family. Barcelona caps species only. Kendal et al. warn that targets set well below the existing share (planes: ~27% vs 15%) risk abandoning well-adapted species and changing ecosystem services (p. 415); supplying the missing performance data is our inference and our contribution.
- **Why it matters:** the plan's targets can pull against each other at one position. Moving away from planes serves the 15% target (though Celtis is already close to it), but a small-crowned replacement works against the **canopy target (tree cover up to 30% of the urban surface)**. At equal trunk size in Porta (2nd and 3rd trunk classes), Pyrus carries 35% of a plane's crown area and Celtis 32–52%, while Tipuana and Jacaranda carry 89–107%.

- Barcelona's **sealed surface grew from 45% to 72%** of the municipality (1956–2009; Barcelona Resilience Atlas, citing Barcelona Regional's climate-change impact study).
- About **3 storms a year exceed 60 mm/h in their first 20 minutes** and flood streets where the sewer lacks capacity (Barcelona Resilience Atlas). The sewer is sized for a **10-year** return period (`notes/city_screening.md`).
- Barcelona carries **one of Europe's highest urban-heat-island mortality burdens** (Iungman et al. 2023).
- The **tree master plan caps any species at 15%** (city-wide); plane trees are **27.45%** of the city's trees (43,722; press 2026) → more than half will be replaced.
- The tool's **seven-species palette**: ***Celtis*, *Melia*, *Pyrus calleryana*, *Jacaranda*, *Tipuana*, *Brachychiton*, *Styphnolobium*** (mnemonic: *"Celtic Melodies Play Jazz To Brazil, Softly"*).
- **Only five are named by the city as plane replacements:** Celtis, Melia, Styphnolobium, Tipuana (city, 2022) and Pyrus calleryana (2026 target mix: planes and Celtis ~12%, each or together is unclear, Melia 7.25%, Pyrus, Sophora, Tipuana ~5% each; press). **Jacaranda and Brachychiton are not named** in any source found: they stay as catalogue species already common in Porta, labelled "not named" (v6 correction).
- **The data gap:** in the reviewed literature only *Pyrus calleryana* has a measured canopy-storage value (Xiao & McPherson 2016); for cooling, only Pyrus (surface temperature, Manchester, abstract) and Tipuana (tropical field and modelled values) have anything. *Styphnolobium* has measured event interception (Yang 2019), not a storage value (`notes/lit/replacement_species_evidence.md`).
- **Why it matters:** replacement choices can trade away cooling or rain interception without anyone noticing.

**Primary user (v6):** the **computational designer of a street-rebuild project**: street works are when the city replaces planes, so this is the person making the choice.

**Flood type matters.** The thesis is about **pluvial** flooding (rain on sealed surfaces, sewer overloaded), from **frequent, short storms**. Not fluvial (river) floods and not multi-day events: Bologna Oct 2024 and Emilia-Romagna May 2023 were saturated-soil, multi-day or culvert events, where trees have negligible influence. This is why Bologna was dropped (Florence fitted the pluvial framing; Barcelona was chosen later for data, access and the dual heat + runoff theme).

### Check yourself
1. What two hazards, and why do they meet in the same streets?
2. Why are plane trees being replaced, in one sentence with both numbers?
3. Name the five species the city names as plane replacements, and the two palette species it does not name.
4. Why is Bologna a bad case for a tree-based flood thesis?
5. What has the city already decided, and what has it not? (Two lists.)
6. Give the three reasons for the 15% cap. Where does the number 15 come from?
7. Does the city already decide which tree replaces which? (Gate 1, in 20 seconds.)
8. Are there enough trees in Porta? Give both numbers.
9. Name the three policy documents and what each sets.

<details><summary>Answers</summary>

1. Summer heat stress (UHI) and pluvial flooding; both concentrate in dense, highly sealed districts.
2. The master plan caps any species at 15%, and planes are 27.45% of the city's trees (press 2026); the city will cut them by 56% to 12% in ten years.
3. Named: Celtis australis, Melia azedarach, Styphnolobium japonicum, Tipuana tipu, Pyrus calleryana. Not named: Jacaranda mimosifolia, Brachychiton populneus.
4. Its recent floods were multi-day / saturated-soil / culvert events; trees only matter for frequent, short pluvial storms.
5. Decided: how much (15% cap, 12% planes), how and when (at death, at street works), which species may be used, which size fits which sidewalk. Not decided: which species at each position, the heat and runoff effect of each choice, priority where the hazards overlap.
6. Pest/disease risk of a monoculture, climate resilience, biodiversity. The plan derives no number; the literature's species benchmarks are mostly 10–15% (Kendal et al. 2014), Santamour's is 10%, and 15% is also the regional convention.
7. On paper: the 2004/2005 table by district × sidewalk width (Nou Barris: Prunus < 3.5 m, Melia or Jacaranda 3.5–6 m, plane kept > 6 m), qualitative criteria, no heat or runoff; the 2011 guide no longer prints it, and Porta's plantings mostly do not match it (up to ~90% other species, an upper bound).
8. No: 20.1% cover (LiDAR 2021) against the 30% target for 2037, 8.3 ha short; planes are ~29% of the canopy.
9. Master plan (15% cap, 30% cover, adapted species), Nature Plan (area targets only; project 83 lists "which species for shade, where" as a study to do), Climate Plan 2024 (+5% cover, adapted 30→40%, 7 ha SUDS, 9 ha shade). None sets species per position.
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

**The heat metric (`notes/decisions/heat_objective.md`, DECIDED by you on 19 Oct):**
- On the **hottest** El Prat day, even full shade is ≥ 32 °C in 5 of 6 afternoon hours, so "share of points > 32 °C" **saturates** and cannot show a benefit.
- The **sun–shade gap is 2.3–4.7 °C UTCI** (full shade; a lower bound for a tree), and the **Ladybug model error is 1–2 °C**: trust **rankings** of layouts more than absolute values.
- **Decided: mean UTCI over 12–17 h on the design (DDY) cooling day**, plus the hottest real day as a check. This changes the RQ wording from "peak summer hour" to "12–17 h window on a hot design day".
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

**Key finding of tool v0:** with the city palette there was **no trade-off at first** (the Pareto front collapsed to a point: bigger, denser crowns win both). Adding the leaf calendar did not help: **78% of intense storm days fall in May–Oct**, when all palette species are in leaf (Esbrí et al. 2026). The first **real trade-off appeared with winter sun access** (winter shade counted as a cost). It survived the 15 Oct re-run with the photo-based leaf calendar: beyond the balanced layout, **−20% winter shade costs −18% summer shade** (base run, 20 Oct), and the trade-off holds in all 8 sensitivity variants (winter −14 to −23%, summer −17 to −20%).

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
Source: `notes/topic_decision.md` §10.5–10.6 (v7, 24 Oct), §9.5, §8.

**RQ (v7, 24 Oct, slide 8):** *Can a trait-based layout method, inside Barcelona's tree rules, choose replacement species for plane trees and new planting spots that retain and add more pedestrian cooling and storm-water interception than the city's own practice?*

- **SQ1 heat:** mean UTCI 12–17 h (CEST) on a hot design day, city rule vs method.
- **SQ2 runoff:** 2-year, 60-min storm, in total and at flood hotspots; is the total difference larger than what the model resolves (**Δmin**)?
- **SQ3 trade-off:** do the heat-best and runoff-best layouts differ, and in which species?
- **SQ4 additions:** how much of the canopy gap to the 30% target can new street trees close within the planting rules, and where?

**The three changes from v6 (say them when asked "you scrutinised it how?"):**
1. **"Reduce" became "retain".** At equal trunk size the plane has one of the largest crowns, so a replacement almost always loses shade against today. The fair test is the method against the city's own rule (S1), with today (S0) as the reference.
2. **Additions are co-equal:** replace, add, or both (R, A, R+A).
3. **Every sub-question has a metric and a threshold;** "not resolved" is an allowed answer for runoff.

Older v6 wording (superseded): "which replacement species … and at which plane positions, jointly reduce (a) … UTCI … and (b) event runoff volume …".

- **H1, synergy:** trait-based layouts beat **the city's rule (S1)** on heat **and** runoff (crown size and LAI drive both).
- **H2, trade-off:** heat-best and runoff-best layouts differ in **species**. Mechanism restated in v7 as crown size and leaf-on calendar (transpiration is not in Tier 1).
- **~~H3, validity boundary~~ — WITHDRAWN 19 Oct:** *the runoff benefit shrinks as the return period grows; small at T = 10 yr; extreme events (6 Sept 2018, ≈300-yr 20-min intensity) are outside what trees can affect.* Still true, still said — but as a **declared boundary of the method**, not a hypothesis, because the bucket model cannot fail it.

**Mnemonic: S-T** = **S**ynergy, **T**rade-off — plus **one withdrawn boundary**. If you are asked for three, name two and say why the third went.

**Status of the hypotheses (v5, `notes/topic_decision.md` §8):**
- **H1, runoff part:** a minimum meaningful difference **Δmin = 91 m³** (0.9 mm over the street crowns, 0.5% of T2-60 runoff) is proposed, fixed before the runs. If the best layout beats S1 by less than Δmin, the runoff part is reported as **"not resolved by the model"**: accepted as a valid outcome (user, provisional, 14 Oct). The v7 result (24 Oct, method vs S1a, total T2-60) is **33.9 m³** → not resolved (earlier exploratory value: 78 m³, worst case 38.5 m³). Then heat carries the species choice and runoff becomes a check.
- **H2:** proposed as a species-composition claim (S2 vs S3 differ by more than a pre-fixed dissimilarity) at the fixed plane positions.
- **H3: withdrawn (user, 19 Oct)** and kept as a **declared boundary of the method**, since it is true by construction (§3). Question for the tutor, on slide 12: is that the right call?
- **Trade-off metric (proposed):** % loss of one objective at the other's optimum.

### Check yourself
1. Say the RQ in under 40 words.
2. Name the two hypotheses and the scenario comparison that tests each — and say what happened to the third.
3. What is Δmin, and what happens if the best layout beats S1 by less than it?

<details><summary>Answers</summary>

1. Can a trait-based layout method, inside Barcelona's tree rules, choose replacement species for planes and new planting spots that retain and add more cooling and storm-water interception than the city's own practice?
2. H1 synergy: S4 vs S1 on both objectives. H2 trade-off: species composition of S2 vs S3. H3 was withdrawn on 19 Oct (true by construction) and is now a declared boundary; the old comparison was runoff benefit vs return period T.
3. The minimum meaningful runoff difference, 91 m³ (0.5% of T2-60 runoff). Below it, the runoff part of H1 is "not resolved by the model" (neither supported nor rejected).
</details>

---

## 8. Method and tool
Sources: `notes/methodology.md`, `shade_sponge/README.md`.

**What is new since 21 Oct (slides 10–11):**
- **Two branches inside a project area the designer draws:** replace the planes (ranked by priority) and add trees in free spots. Scenarios: **S0** today · **R** replacement only (S1 city rule vs optimised) · **A** additions only · **R+A** both. Compared on a radar of normalised indicators (summer shade, winter sun, total and hotspot runoff, canopy cover, diversity), always next to bars in real units with the Δmin marks.
- **Free spots (Porta): 232** on sidewalks wide enough under the city's rules, away from crossings and bus stops. An upper bound: driveways and services are not in the data.
- **City's rules as hard inputs:** 15% cap (city-wide, counted on **street trees only**, a simplification decided 26 Oct), sidewalk size class, the city's mix as baseline.
- **Equal trunk size:** species are scored at equal trunk class, not at their raw Porta medians.
- **Optimiser in practice:** a weighted-sum LP (HiGHS) sweep; NSGA-II is still the plan for later. The **city LP** solves 28 barris at once under one city-wide cap, plus an optional **local ceiling** (no species in a barri above today's plane count).
- **Any barri:** `site.build_barri` builds a site from the city LiDAR tiles; 33 barris computed (`notes/citywide_plan.md` §6).
- **Palettes scale to N species:** city palette of 7 and a Barcelona shortlist of 34 (30 after excluding the 2011 guide's red "avoid" species, 3 Nov, branch not yet merged). Answer to "only three species?".
- **Front-ends:** Grasshopper is **not required** by the programme (30 Oct); the web app covers non-programmers.

**Pipeline (5 steps):** LiDAR trees → trait table → runoff module + heat module → optimiser → Pareto front → test on Sant Antoni and Florence.

- **Data:** street trees (Ajuntament `arbrat-viari`), **ICGC LiDAR** (flown 26 Sept 2021, leaf-on; ≥ 8 pts/m², CC BY 4.0), PDISBA IDF, Resilience Atlas flood-hazard index, **RESCCUE flood-depth maps T10/T100** (public CARTO tables, found 13 Oct; licence email sent), EPW (Barcelona El Prat), trait databases (3TF, BROT 2, literature).
- **Tree model:** position, species, height H, crown diameter D, crown base Hb, LAI (leaf-on/off), storage S, leaf habit, wood anatomy. Missing species → genus or leaf-habit class values with a range + sensitivity.
- **Scenarios:** **S0** current trees · **S1** the city's own replacement (2026 target mix assigned at random within the sizing rule; v6) · **S2** heat-only optimum · **S3** runoff-only optimum · **S4** multi-objective Pareto set.
- **Optimiser:** NSGA-II (pymoo or Wallacei). Constraints: **≤ 15% per species** (applied in Porta: an ASSUMPTION, since the plan's cap is city-wide), **size class set by sidewalk width** (v6; one class per sidewalk type in the guide, a "≤" reading would be an ASSUMPTION; widths still to extract), Shannon diversity floor, no invasive or pest-host species, crown clearance from façades. **v0** uses a weighted-sum LP instead (HiGHS).
- **Tool package `shade_sponge/`:** `site.py` (1 m grid), `topo.py` (Priority-Flood routing on the DTM → water convergence, distance to flood hotspots), `heat.py` (sun position, elliptical crown shadows, opacity from LAI and leaf month), `season.py` (leaf calendar, storm months), `runoff.py` (bucket + SCS-CN), `layout.py` (palette, cap, LP, Pareto).
- **One core, two front-ends:** Grasshopper (primary, computational designer) and a later web app (non-technical users).
- **Palette in the tool:** seven species, five named by the city + Jacaranda and Brachychiton (not named). Species crowns and LAI come from one function, `species_lidar()` in `site.py`: Porta LiDAR medians, with a hard-coded override for *Styphnolobium* (sample outside Porta).
- **Every parameter is cited or marked ASSUMPTION** (e.g. `CAPTURE_M` = 100 m, `OP_BARE` = 0.35, `R_OFF` = 0.5).
- **Routing vs RESCCUE (checked 15 Oct):** upstream area barely separates RESCCUE wet from dry cells overall (**ROC AUC 0.52**), but the top 0.5% of open ground by upstream area is wet in **58–80%** of cases (1.7–2.6× random). So the routing finds the **main convergence points** but is **not a flood map**: hotspots stay tied to the atlas index (or RESCCUE depth).
- **Proposed tool changes (methodology §12, not adopted):** weight shade by ground surface (asphalt cools ~2× grass); check SVF/street orientation of chosen positions; tag k = 0.5 as ASSUMPTION; keep R_OFF = 0.5 with new birch anchors; add birch/pine storage anchors (1.00–1.08 mm per LAI) to the s sensitivity range.

**Mnemonic for scenarios: "Now, Swap, Hot, Wet, Both"** = S0 now · S1 the city's swap · S2 hot (heat only) · S3 wet (runoff only) · S4 both.

### Check yourself
1. List S0–S4.
2. Name the optimiser and its four constraints.
3. What does `topo.py` add that runoff v1 did not have?
4. What is the rule for every parameter in tool code?
5. What did the comparison with RESCCUE show about the routing?

<details><summary>Answers</summary>

1. S0 current, S1 the city's own replacement, S2 heat-only, S3 runoff-only, S4 multi-objective Pareto set.
2. NSGA-II; ≤ 15% per species, size class by sidewalk width, Shannon diversity floor, no invasive/pest hosts, façade clearance.
3. Flow routing on the DTM, so runoff that reaches flood hotspots can be targeted (positions upstream of hotspots).
4. Either sourced (cited) or marked ASSUMPTION.
5. It finds the main convergence points (top 0.5% of upstream area mostly wet) but is not a flood map (AUC 0.52); hotspots stay tied to the atlas index.
</details>

---

## 9. First results
Sources: `notes/methodology.md` §4b, §6; `shade_sponge/README.md`.

*The results in this chapter are the v0/v1 runs of 8–20 Oct (shade proxy, random-palette S1). The 10 Nov results are in §9b and §9c.*

**Runoff v1 (T2, 60 min):**
- Current street trees cut Porta's runoff by **1.85%** (open space only: **2.9%**). Range over s and T: **0.4–4.0%**.
- Same order as the field benchmark (**3.5–4%**, Selbig 2021 / Coville 2022). Barcelona city-wide also small (Cortinovis 2022: 20,170 new trees, retention 50.18% → 50.76% for a 20 mm event).
- **Any young replacement: ≈ +0.7% runoff ≈ 37% of the current street-tree benefit lost** during the transition ("more than a third").
- Benefit shrinks with return period (as a %), but in the model this is arithmetic — which is exactly why H3 was withdrawn on 19 Oct and is now a declared boundary (§3, §7).

**Styphnolobium (15 Oct):** a LiDAR sample from one 1 km tile outside Porta gives crown **5.32 m / LAI 2.12** from **367 trees on 25 streets** without possibly merged crowns (the tool uses these; all 607 trees give 6.43 m / 2.28). With them it ranks **5th of 8 palettes** (aggregate) and **4th of 7** (grid), and replacing the planes with it **adds runoff** (+92.5 m³, +0.52% at T2-60). Best palette: Melia (aggregate) or Jacaranda (grid). Best vs S1: **78 m³ < Δmin 91 m³** → runoff part of H1 not resolved. (The earlier 14 Oct result, where Styphnolobium came first, used only 5 Porta trees and is superseded.)

**Tool v0 (shade proxy + runoff; re-run 15 Oct with the seven species and the photo-based leaf calendar; trade-off figures from the 20 Oct run):**
- Optimised (balanced) vs random palette: **+16% summer shade** (robust across 8 sensitivity variants), but about **5% more winter shade** than random.
- **No-regret swap:** summer-only → balanced still swaps ~90 **Tipuana → Jacaranda**, but now cuts winter shade by only **2%** at equal summer shade, because 170 iNaturalist photos from Barcelona show Jacaranda mostly in leaf in January (79%). The swap vanishes in 3 of 8 variants. *Superseded (old calendar, Jacaranda bare Jan–Mar): −9%.*
- Beyond balanced: a **real trade-off**, robust: winter-heavy gives **−20% winter shade for −18% summer shade**, with the winter-bare Pyrus and Styphnolobium instead of Tipuana.
- **Placement follows the buildings, partly:** the winter-bare Melia gets the sunniest winter positions (87% of winter hours in sun), evergreen Brachychiton far less (29%); but the winter-bare Styphnolobium (34%) and Pyrus (26%) also sit in winter-shaded streets.
- **Hotspot runoff** varies only 0.5% across weights; on 15 Oct it mostly follows the runoff weight (on 8 Oct it did not), so still to check.
- **No replacement layout reached S0** (mature planes): replacement always loses shade at first (balanced: −7.5% summer shade).

### Check yourself
1. How much do Porta's street trees cut runoff, and is it plausible?
2. What happens during the transition to young trees?
3. What is the "no-regret swap"?
4. Why did Styphnolobium drop from first to fifth?
5. Did the summer–winter trade-off survive the photo-based leaf calendar?

<details><summary>Answers</summary>

1. 1.85% at T2-60 (2.9% on open space); same order as the 3.5–4% measured in the field.
2. Young replacements lose ≈ 37% (more than a third) of the current street-tree runoff benefit.
3. Swapping ~90 Tipuana for Jacaranda: same summer shade, only 2% less winter shade (15 Oct re-run; 9% with the old calendar), and not robust.
4. The first result used the medians of only 5 Porta trees (crown 8.85 m, LAI 3.32); the sample outside Porta (367 trees without merged crowns) gives a smaller crown (5.32 m) and LAI (2.12).
5. Yes: beyond the balanced layout, winter-heavy gives −20% winter shade for −18% summer shade (base run); the trade-off holds in all 8 variants (winter −14 to −23%, summer −17 to −20%). Only the "free" swap at the start of the front shrank.
</details>

---

## 9b. Results v7: Porta, additions, the city (slides 12–15)
Sources: `slides/outline_10nov.md` slides 12–15; `notes/citywide_plan.md` §6.6–6.9; `notes/topic_decision.md` §10.5; observed S1b: `notes/data_sources_pemb_30oct.md` §6.

**Porta, replacement of all 832 planes (slide 12).** Heat here is effective shade (proxy), each axis normalised to today = 100.
- **Summer shade: city rule (S1a) 87%, method 98%** of today. Price: about **6% more winter shade**, a real trade-off.
- **Runoff: −33.9 m³** total at T2-60 vs S1a, **below Δmin = 91 m³ → "not resolved"**. An honest result, not a failure.

**Porta, additions (slide 13).** 232 free spots. Keeping the planes and adding trees gives the most shade, but the planes are going. **City rule + the same new trees: 92%** of today. **Method + additions: 103.5%**. Only the combination of the two levers, chosen with numbers, ends above today.

**City-wide, 28 barris, one LP (slides 14–15).** Barris with ≥ 500 planes: **31,580 planes**, one optimisation under the 15% city cap plus the local ceiling.
- Against the city's mix: **median +9.2 points** of today's summer shade (−1.4 to +25.4); **27 of 28 gain**. The one loss: **Sant Gervasi – la Bonanova, 90.8% vs 92.2%**, because with one city cap the capped species go where they add most (el Poble-sec +21.8, Diagonal Mar +17.4 against the local cap).
- **Celtis (1,318) and Tipuana (11,348) end at the cap.** Three barris end above today: Porta 103.3%, el Poble-sec 105.3%, Sant Andreu 105.7%. Winter shade median 114%.
- **Local ceiling** (your addition): stops a barri from ending more concentrated than today (without it one barri got almost half Tipuana). **It is infeasible where few planes are replaced** (Baró de Viver, 15 planes; la Trinitat Vella, 167): small barris need a different rule. Open, and one of the three questions for the tutor ("may a barri lose while the city gains?").
- LiDAR season differs: most new barris are from the **June 2022** flight, Porta from **26 Sept 2021**. Declared, not corrected.

**First transfer, Sant Antoni (28 Oct):** the flood-dominant contrast site, 989 planes; the tool keeps more shade than the city rule there too (79.2% vs 72.1% in the city LP). Within-city transfer is the validation case; Florence and Mataró become "future work: other cities".

**S1a vs S1b, "from press to real data" (31 Oct).**
- **S1a** = the 2026 target mix (press), drawn within the sizing rule. **S1b** = the same draw weighted by what the city **actually planted** where planes were replaced: **1,444 cases, 2018–2026**, from 35 quarterly inventory files (Celtis 296, Melia 219, Gleditsia 105, Koelreuteria 89, Styphnolobium 86, Grevillea 70, Pyrus 65, Jacaranda 54). The city keeps the pit code when it replants, so a replacement is a species change on the same code.
- Tool margin in summer shade, 33 barris run one by one: **vs S1a median +5.7 points (0.8–11.7), vs S1b median +7.2 (0.9–18.1); no barri ≤ 0.** The observed mix is usually a little worse than the press mix (median −1.5 points).
- **Porta: S1a 87.4, S1b 90.3, tool 99.1** → margin 11.7 → 8.8.
- **Decided 6 Nov:** S1b (observed) is the reference baseline, S1a (press) stays beside it, and the 2004/2005 table is renamed **S1-2004**: cited to show a rule exists, not run. The city LP numbers (+9.2 median) are still against S1a.

### Check yourself
1. Porta replacement: summer shade for the city rule and for the method? What does it cost?
2. Why is the runoff answer "not resolved", and why is that acceptable?
3. With additions, which path ends above today?
4. City LP: how many barris and planes, what median gain, who loses and why?
5. What is the local ceiling, and where does it break?
6. What is S1b, and how large is the tool's margin against S1a and S1b?

<details><summary>Answers</summary>

1. 87% (S1a) vs 98% of today's summer shade; about 6% more winter shade.
2. The total difference (33.9 m³) is below Δmin = 91 m³, fixed before the runs; "not resolved" was declared an allowed outcome, so heat carries the species choice.
3. Trait-based replacement plus the 232 additions: 103.5% (city rule + additions: 92%).
4. 28 barris, 31,580 planes; median +9.2 points vs the city mix; 27/28 gain; la Bonanova loses (90.8 vs 92.2) because the city-wide cap sends Celtis and Tipuana where they add most.
5. No species in a barri above today's plane count; infeasible where few planes are replaced (Baró de Viver, la Trinitat Vella).
6. The city's observed plane-replacement mix 2018–2026 (1,444 cases). Margin median +5.7 points vs S1a and +7.2 vs S1b; Porta 11.7 → 8.8.
</details>

---

## 9c. Heat validation: the first UTCI check (slide 16)
Sources: `notes/methodology.md` §5b; `notes/method_heat_validation.md`; `/mnt/project-files/figures_10nov/ladybug_tier1_steps.md`.

**What was run (2–3 Nov):** today's planes (S0) against the tool's species (S4) on **Pg Andreu Nin** (1,974 sidewalk points) and on all Porta plane streets, mean UTCI 12–17 h CEST (EPW hours 11–16), 15 July.
- **Tier 1 = Ladybug** (Human to Sky, Outdoor Solar MRT, UTCI), **rebuilt in Python** (`scripts/porous_utci.py`): matches Grasshopper to **bias −0.01/−0.02 °C, r 0.998–0.999**, so long runs go in Python.
- **Tier 2 = Honeybee** with Radiance (UTCI comfort map), crowns as ellipsoid meshes, porous via a Radiance glass modifier.
- **Porous crowns:** τ = exp(−0.5·LAI) lets light through by leaf area. Opaque crowns would hide the LAI difference between species.
- **Weather:** El Prat **TMYx 2011–2025** (the project reference; the full-record 1973–2023 TMYx is 2.5–3 °C cooler on 15 July).
- **Bug found and fixed:** the Grasshopper loader left crowns round (non-uniform scale on a sphere Brep); mesh ellipsoids fixed it.

**Results (S4 − S0, mean UTCI):**
| | Porous crowns | Opaque crowns |
|---|---|---|
| Pg Andreu Nin, Honeybee (Tier 2) | **−0.15 °C** | +0.06 °C |
| Pg Andreu Nin, Python Tier 1 | **−0.19 °C** | +0.10 °C |
| All Porta plane streets (832 positions, 21,352 points), Tier 1 | **−0.10 °C** | −0.03 °C |

All with TMYx 2011–2025. The differences do not change with the weather file. Note: 15 July in this TMYx is an ordinary July day, not yet the hot design day.

- **Proxy vs Ladybug: r = −0.73 across points, −0.82 on the S4 − S0 change** (opaque crowns, Andreu Nin). The proxy ranks points as Ladybug does, so it is fit for choosing positions (more shade → lower UTCI, hence the negative r).
- Honeybee is 0.6–0.9 °C warmer than Tier 1 in absolute terms; cause not checked. Trust **differences and rankings**, not absolute values.

**The claim (learn it):** *for heat the method is no worse than today's planes, within model uncertainty; the two layouts differ by about a tenth of a degree and the sign depends on crown porosity. The gains are runoff, diversity and winter sun.* Precedent for small effects: a genetic algorithm moved site-mean UTCI by only **0.1–0.3 °C** (Hao et al. 2023).

**Next (to 1 Dec):** UTCI of the final layouts with **Infrared City** (~160 runs on sample streets, then calibrate the shade proxy; a surrogate only as plan B). Open question for the tutor (a co-founder): does Infrared model porous crowns?

### Check yourself
1. What are Tier 1 and Tier 2, and how well does the Python chain match Grasshopper?
2. Why porous crowns, and with which formula?
3. Give S4 − S0 for Andreu Nin (both tiers) and for all of Porta.
4. What does r = −0.82 mean, and why is it negative?
5. State the heat claim in one sentence.

<details><summary>Answers</summary>

1. Tier 1: Ladybug sky view + solar MRT + UTCI, rebuilt in Python (bias −0.01/−0.02 °C, r 0.998–0.999 vs Grasshopper). Tier 2: Honeybee with Radiance.
2. Opaque crowns hide the LAI difference between species; τ = exp(−0.5·LAI).
3. Porous: −0.15 °C (Honeybee), −0.19 °C (Python Tier 1); all Porta −0.10 °C. Opaque: +0.06 / +0.10 °C on Andreu Nin, −0.03 °C over Porta.
4. The proxy's change in shade from S0 to S4 tracks Ladybug's change in UTCI; more shade means lower UTCI, so the correlation is negative.
5. No worse than today's planes within model uncertainty; the gains are runoff, diversity and winter sun.
</details>

---

## 10. Transferability: the code travels, the evidence does not
Sources: `notes/transferability.md`, `notes/catalan_transfer_city.md` §1–§5b, `notes/city_transfer_candidates.md`, `databases/transfer_species_overlap.csv`. This is **slide 16** of the 20 Oct talk (`slides/outline_20oct.md` v3).

**The one line:** the **code** is site-agnostic by construction, the **evidence is not**.
- Constant-free kernels: flow routing (`topo.route`), sun position and crown-shadow geometry (`heat.sun`), SCS-CN (`runoff.scs`). As a *file*, only `topo.py` carries no local constant.
- Local by construction: `heat.py` (Barcelona design days and hours), `runoff.py` (the calibrated `runoff_params.json` and the PDISBA IDF table, loaded at import), `site.py`, `season.py`, `layout.py`.
- So a new site is **one data adapter** (`build_<name>()` + `trees_<name>()`) plus the real cost: rebuilding the local data and re-deriving the local parameters.

**Four degrees of transfer:**
| | Case | New data | Cost | Status |
|---|---|---|---|---|
| **T0** | Another Barcelona neighbourhood (**Sant Antoni**, flood-dominant contrast) | none: same inventory, LiDAR, IDF, flood model | days\* | planned |
| **T1** | Another Mediterranean city with open data (**Florence**) | new adapter + 6 datasets; traits and phenology re-derived; the decision variable redefined | 2–3 weeks\* | planned 2–10 Dec, **access unchecked** |
| **T2** | No point cloud, or no species inventory at all (**Bologna**: it *has* an inventory, ~87,000 trees, and a 2023 leaf-on classified survey covers the municipality — but **no LAS is served**) | as T1; where the inventory is missing the baseline goes with it, but the **design front-end still works** (the designer supplies the positions) | weeks–months\* | not planned |
| **T3** | Another climate (non-Csa) | as T1, plus *s*, the leaf calendar, the storm season and the heat design days all lose their anchors | out of scope | **not claimed** |

\* Order-of-magnitude estimates, **not measured** — and in tension with the plan, which gives 2–10 Dec (9 days) to Sant Antoni **and** Florence together. The thesis validates T0 and attempts T1.

**The three inputs that do not travel — mnemonic CLOUD · MAP · TRAITS:**
1. **A classified leaf-on point cloud.** LAI = −ln(gap fraction)/k from the classified points inside each segmented crown, and LAI drives *both* objectives (storage S = s·LAI, opacity 1 − e^(−0.5·LAI)). A 1 m DSM gives height and crown width but no gap fraction, so on a DSM-only city the species differences collapse to crown size. Fallback: database LAI per species — i.e. the transfer city loses the one trait we measure ourselves.
2. **A city pluvial flood map.** Tested, not assumed: our own routing barely separates RESCCUE wet from dry cells (**ROC AUC 0.52**); only the tail is informative (the top 0.5% of open ground by upstream area is wet in **58–80%** of cases, 1.7–2.6× random). Without a municipal map the runoff objective collapses to total volume and the **placement** half of the method loses its target.
3. **Traits and phenology.** Transfer makes the trait gap **worse**: a species-level runoff *or* heat value exists for **40%** of trees in Barcelona, **19%** in Florence (**7%** with both).

**Florence (T1, first choice):** ~82,000 public trees, a 1 km IDF grid (LSPP 2012) and a **published** pluvial index (Pacetti's PFI, downloaded) — but each comes with a catch: the LSPP grid's **shortest fitted duration is 1 h**, so the 10–60 min design storms are an extrapolation (ASSUMPTION), and the PFI is a **relative 1–42 rank**, with no depth and no return period, under CC BY-**NC-ND** 4.0 (the ND clause is an open question for derived products). Terrain is only **1 m DTM/DSM rasters**; the point cloud is request-only. The *Life Escapos* dataset looked like the way round it and **failed the test (18 Oct)**: its `lai` column is not measured but a deterministic function of species and DBH (51 of 68 species flat, the other 17 an exact DBH power law, log–log R² = 1.0000), so it cannot calibrate or validate our proxy. Licence CC BY-**NC** 4.0. The point-cloud request to the Comune di Firenze is **drafted and not yet sent** (`notes/firenze_lidar_request.md`), so T1 still rests on an unanswered request.

**Mataró (Catalan fallback, chosen 19 Oct):** the same ICGC product as Porta — **leaf-on and classified**, flown 20 July 2021 (*not* Porta's 26 Sept mission; same programme, another flight day, and the date was read from one 150 × 150 m clip, so download the LAZ over the study district before relying on it). Same climate zone (Csa) and the same CRS (**EPSG:25831**), so the interception constant, leaf calendar and storm season stay **inside their anchors** — but they still have to be re-derived, not copied. Of the **two finalists checked**, it is the only one with a design storm of its own: a 5–120 min IDF table in its 2003 sewer master plan (PDCLAM). **That is availability, not independent measurement** — its sub-hourly values are themselves a Témez extrapolation below the 1 h anchor, pre-computed by CLABSA rather than measured.
Its tree data is **split in two** — **17,204 street trees** by composition (2016 street-tree master plan; "117 species" counts table entries including cultivars, **108 distinct binomials**), and **79,748 positions** in the municipal GeoPackage with **no species, no DBH, no height** (every row flagged `nivell = 'nec'`, outside the survey commission). Unless the joined per-tree table proves public, species must be assigned **probabilistically from the composition**, which turns a *species-level* transfer test into a **composition-weighted** one — a real loss of independence, to label `ASSUMPTION`. And with no numeric DBH or height, the crown/LAI proxy **cannot be validated in Mataró at all**.
Porta's measured species cover **52.2% of Mataró's top-30 species** (counting only species with ≥5 Porta trees) — about **46% of its street stock** — and 92.9% at genus, against Florence's **43.5% of its top-30** (≈ a third of its inventory) and 74.0% at genus. **Never quote that margin bare:** Mataró and Porta are street-tree inventories while Florence's counts park trees too; the shares are the **2016** vintage, and *Platanus* at 21.4% is of *identified* street trees (a 2024 source gives 16.4% — but over ~25,300 trees of all kinds, a different universe). **Licence UNKNOWN for every Mataró asset.**

**Why not Badalona:** it shares Porta's exact LiDAR mission day (26 Sept 2021) — a convenience, not a validity condition — and has the better rain-gauge record, but **no open tree inventory was found** and it has **no design rainfall of its own** — the only published route is to drive it with *Barcelona's* IDF curves, which makes the transfer test partly circular. A missing species field is a degraded input you can declare; a borrowed design storm invalidates the comparison.

**The negative finding that lands hardest: no Catalan city publishes a pluvial hazard map of its own.** The ACA lists 44 pluvial municipalities, but the ARPSI polygon *is* the municipal boundary. The one exception is tiny and not a city: the Vila-seca i Salou pluvial ARPSI (8.54 km²) does have modelled depth maps, which still stand although the ARPSI is proposed for deletion. Barcelona's RESCCUE depth model is the only **city-wide** pluvial depth model found in Catalonia — which is why Porta was the right place to calibrate.

**Method vs climate (only if the tutor presses on the design storm):** raw, Mataró looks **19–32% drier** than Porta, and *duration-dependently* so (ratio 0.81 at 10 min → 0.68 at 30 → 0.71 at 60). Climate cannot do that. The two numbers are different *kinds* of quantity: Porta's PDISBA value is an across-gauge **envelope** (+24% over the gauge mean), Mataró's a **central** Gumbel estimate with the sub-daily shape supplied analytically. Rebuilt the same way, **66% of the gap disappears at 10 min and 77–80% at 20–60 min** (do not pair "two thirds" with the 30% figure: at 10 min the gap is 19%, not 30%), leaving a flat **0.93 at T = 10** and **1.00 at T = 2**. The flat line is **not** a finding — it is an identity (both cities sit in the I1/Id = 11 region, so the duration factor cancels at both ends). The evidence is the **raw ratio reversing direction with duration**. Two residuals to state plainly rather than bury: the harmonised daily legs still use **different frequency laws** (Gumbel for Mataró, SQRT-ET max for Barcelona), and harmonised, the sub-hourly comparison carries no information beyond the daily one — for the transfer city the sub-hourly curve is an **assumption**, for Porta it is empirical.

**The question travels less well than the method.** "Which species replace Porta's plane trees" exists because of a Barcelona rule (15% cap, planes ~29%, a named palette). No equivalent programme is recorded for Florence or Bologna, and neither was searched for one, so treat *those* as **unchecked, not absent**. Catalonia **was** searched (criterion 6), and Mataró has **no cap of its own**: outside Barcelona only L'Hospitalet has a formally approved 15% maximum, and Sabadell's is a conference-deck proposal, not policy. So in Mataró the candidate set would have to come from the city's own 2016 tree plan, which classifies species as *apte* / *restriccions* / *evitar* — a suitability list, not a cap. On transfer the decision variable has to be redefined: species at **renewal** positions, or species at **new** plantable sidewalk cells, with a diversity constraint instead of a named palette. The optimiser itself does not change. Say this out loud: it is a **framing** limit, not a code limit, and it is the specificity the tutor asked for.

**Two module constraints to remember:** **T = 1 yr is published for no candidate transfer city** (Barcelona's PDISBA has one, which is exactly the problem; PDCLAM's "T = 1" column is the Gumbel T = 1.001 limit — do not use it), and Mataró's central estimate must be **harmonised** against PDISBA's envelope before any comparison.

**Parameters that must be re-derived, not copied:** *s* = 1.75 mm/LAI (**already a transfer**: Freiburg, Cfb, *Tilia*/*Acer*, 51 events) · storm months (78% of intense storm days May–Oct) · leaf calendar and `R_OFF` = 0.5 · heat design days 15 Jul / 15 Jan · `HAZARD_HIGH` = 40 (**a threshold on a Barcelona-specific index**, meaningless elsewhere) · `CAPTURE_M` = 100 m. `OP_BARE` = 0.35 and k = 0.5 travel, but they travel as **assumptions**.

### Check yourself
1. What exactly is site-agnostic, and what is not?
2. Name the three inputs that do not travel, worst first.
3. Why is Mataró the fallback and not Badalona?
4. What is the strongest negative result of the Catalan screening, and why does it help the thesis?
5. Mataró's design storm looks 30% drier than Barcelona's. What do you answer?
6. What has to be redefined in a city with no replacement programme?
7. Why can't Florence's Escapos LAI column replace the point cloud?

<details><summary>Answers</summary>

1. The physics and geometry kernels (routing, sun and crown shadows, SCS-CN) carry no local constant; as a file, only `topo.py` is constant-free. `heat.py` holds Barcelona design days, `runoff.py` loads the calibrated storage and the PDISBA IDF at import, and `site.py`/`season.py`/`layout.py` are local by design. A new site = one adapter plus rebuilding the local data.
2. (1) a classified leaf-on point cloud, because the LAI proxy and therefore both objectives depend on gap fraction; (2) a city pluvial flood map, because our routing is not one (AUC 0.52); (3) traits and phenology, which get worse on transfer (40% → 19% of trees with a measured value).
3. Of the two finalists checked, only Mataró has a published design storm of its own; it has the same leaf-on classified ICGC product (another 2021 mission day), the same climate zone and CRS, and about **46%** of its street stock is in species already measured in Porta. For Badalona **no open tree inventory was found**, and it has no design rainfall of its own, so it would have to borrow Barcelona's IDF — a circular transfer test.
4. No Catalan city publishes a **city-wide** pluvial hazard or depth map (the ACA's pluvial polygon is the municipal boundary; the one exception, Vila-seca i Salou, is an 8.54 km² ARPSI). It makes Porta the right calibration site, because Barcelona's RESCCUE model is the only city-wide pluvial depth model found in Catalonia.
5. That most of it is method, not climate: an across-gauge envelope against a central Gumbel estimate. Harmonised, 66% of the gap goes at 10 min and 77–80% at 20–60 min, and the rest is 0.93 at T = 10 and 1.00 at T = 2 — and that flat line is an identity, not a finding. The real evidence is the raw ratio reversing direction with duration, which climate cannot do.
6. The decision variable: species at renewal positions or at new plantable cells, with a diversity constraint instead of the city's named palette and 15% cap. The optimiser does not change; the framing does.
7. Because its `lai` values are synthetic — a deterministic function of species and DBH (log–log R² = 1.0000) — so they carry no independent measurement to calibrate or validate against.
</details>

---

## 11. Limits (say them before the tutor does)
- Flood indicator is a hazard **index**, not water depth. RESCCUE depth maps (T10, T100) are now public; licence for thesis use asked on 13 Oct. Our routing is not a flood map (AUC 0.52).
- Surface temperature (Landsat) ≠ pedestrian UTCI.
- LiDAR LAI proxy (~2.3) probably **too low** → storage underestimated.
- Same s for every species; species differ only via crown and LAI.
- **Volume only**: no sewer, no routing to outlets, no ponding.
- EPW from the airport, not the city (test +1/+2 °C).
- Design hour misses night effects.
- **H3 was true by construction** in the bucket model, so it is **withdrawn as a hypothesis** (19 Oct) and stated as a declared boundary instead.
- Runoff differences between palettes may stay below Δmin: the runoff part of H1 may be "not resolved".
- Most palette species lack measured traits → ranges + sensitivity; **the gap is a finding**.
- Seminar gaps: no stakeholder validation yet; innovation type and TRL not yet stated (claim **TRL 3**, process innovation) (`notes/research_method_guidelines.md`).
- **Calibrated in one 0.84 km² neighbourhood.** Transfer is costed input by input (§10), but the transfer costs are order-of-magnitude estimates, not measured, and the point cloud alone eliminates most cities. A city pluvial map exists in some countries (Switzerland, the Netherlands, New York City), but in Catalonia only Barcelona has one.
- **Heat in UTCI is within ±0.2 °C** of today's planes and its sign depends on crown porosity (§9c): the heat claim is "no worse", not "cooler". Honeybee and Tier 1 differ by 0.6–0.9 °C in absolute terms (cause unchecked).
- **The baseline mix is from the press (S1a)**; the observed mix (S1b) is a reconstruction from inventory snapshots with re-coding filters (ASSUMPTION), and same-species replanting is invisible.
- **The 15% cap is counted on street trees only** (26 Oct simplification); the plan's base is ~201,600 trees incl. squares.
- **The local ceiling is infeasible in barris with few planes** (Baró de Viver, la Trinitat Vella), and with one city cap a barri can lose (la Bonanova).
- **LiDAR seasons differ across barris** (June 2022 vs Porta's 26 Sept 2021).
- **The 232 free spots are an upper bound** (no driveways or services in the data); city-wide sidewalk widths still come partly from OSM (size class right for about 3 trees in 4).

---

## 12. Likely tutor questions (practise answering in 20 seconds each)
Sources: `slides/outline_20oct.md`; the Porta and Barcelona answers from `notes/site_selection.md` and `notes/city_screening.md`.

| Question | Short answer |
|---|---|
| **Does the city already decide which tree goes where?** (20 Oct ask) | Only on paper: the 2004/2005 table by district × sidewalk, qualitative, no heat or runoff; the 2011 guide no longer prints it and Porta's plantings mostly do not match it (up to ~90% other species). |
| **Are there enough trees?** (20 Oct ask) | No: Porta 20.1% against the 30% target, 8.3 ha short; planes are ~29% of the canopy, so the species choice decides the direction. |
| **How do you validate?** (20 Oct ask) | Each module against something it was not fitted to: interception on Freiburg field data; heat proxy against Ladybug and Honeybee (r −0.73 / −0.82); routing against RESCCUE (AUC 0.52, stated); Sant Antoni as within-city transfer; next, Infrared City on the final layouts. |
| **So heat does not improve?** | About a tenth of a degree, sign set by crown porosity: "no worse than the planes". The gains are runoff, diversity and winter sun. Hao 2023 also finds only 0.1–0.3 °C. |
| **Why the press mix as baseline?** | It was the current policy; now there is also the observed mix (1,444 real replacements 2018–2026). The method beats both: median +5.7 and +7.2 points. |
| **May a barri lose while the city gains?** | With one city cap, yes (la Bonanova −1.4 vs the city mix). A per-barri floor is one more constraint set; ask the tutor which he prefers. |
| **Why a local ceiling, and does it always work?** | Without it one barri got almost half Tipuana. It breaks where few planes are replaced (Baró de Viver, la Trinitat Vella): small barris need a different rule. |
| **Only a few species?** | The method scales to N species: 7 in the city palette, a 34-species Barcelona shortlist (30 after the guide's "avoid" list). |
| Hasn't the city already solved this? | No. The plan fixes how much of each species (15%) and the 2011 guide which size fits which sidewalk; the only species rule (2004/2005 table) is qualitative and not followed in Porta, and nothing measures heat or runoff. The method works inside their rules. |
| Why 15%? | Pest and disease risk, climate resilience, biodiversity. The plan derives no number; benchmarks in the literature are mostly 10–15% per species (Kendal 2014), Santamour's is 10-20-30. Kendal warns that targets far below the existing share can cost well-adapted species and change ecosystem services; I supply the performance data. |
| Why not peak flow? | Trees barely change peak flow in the field (Selbig 2021); volume is what they change. |
| Hasn't Tan & Liu 2026 done this? | Heat, CO2, diversity only; no runoff, 4 Chicago species, one summer hour. I add runoff, the city's own palette and the seasons. |
| Is a 2% effect worth a thesis? | The thesis is the method and the trade-off, not a big runoff number. The declared boundary states the limit; the shade gain over the city's rule (+9.2 points median city-wide) carries the species choice. |
| Where do species values come from? | LiDAR crowns and LAI on site, database traits, genus/leaf-habit proxies with sensitivity ranges. |
| Why Porta and not Sant Antoni? | Porta passes both hazards at every threshold; Sant Antoni's heat is below the city median. |
| Why Barcelona and not Florence? | Heat-health evidence, LiDAR, open data and site access; Florence becomes the transfer test. |
| What if the scope is too narrow? | Widen the tree into a system: add the tree pit as one design variable; carbon reported, not optimised. |
| Hasn't Dong et al. 2026 done this? | They optimise species mixes per 0.25 km² cell with an energy proxy for heat and i-Tree runoff. I choose species and positions per tree, against pedestrian UTCI and event runoff. |
| Isn't H3 true by definition of your model? | It is — which is why I withdrew it on 19 Oct and kept it as a boundary of the method. In field data the intercepted fraction also falls as rain depth grows (Anys & Weiler 2024). |
| What if runoff can't tell the palettes apart? | Then the runoff part of H1 is "not resolved" (below Δmin = 91 m³, fixed before the runs); heat carries the species choice, runoff is a check. That is still a result. |
| How good is your flood routing? | It finds the main convergence points but is not a flood map (AUC 0.52 vs RESCCUE depth); hotspots come from the atlas index. |
| Does this only work in Barcelona? | The code does not: a new site is one adapter, and the routing, shade-geometry and SCS-CN kernels carry no local constant. The evidence does: traits, leaf calendar, storm season, flood map and the 15% cap are all local (§10). |
| Why Mataró and not Badalona? | Badalona has no open tree inventory and no design rainfall of its own; it would have to borrow Barcelona's IDF, which makes the transfer test circular. Mataró has its own 5–120 min design storm, the same leaf-on classified LiDAR, calendar and CRS. |
| Isn't Mataró just 30% drier, so the comparison is unfair? | Most of that gap is method, not climate: an across-gauge envelope against a central Gumbel estimate. Harmonised, 66–80% of it disappears. The flat residual is an identity, not a finding. |
| What stops you transferring to any city? | Two hard dependencies: a classified **leaf-on** point cloud (the LAI proxy) and a city **pluvial flood map** — our own routing is not one (AUC 0.52). |
| Why did you calibrate in Barcelona? | It has the only city-wide pluvial depth model found in Catalonia (RESCCUE); no Catalan city publishes a pluvial hazard map. |
| Does the research question travel too? | Less well than the method. The question exists because of a Barcelona rule; elsewhere the decision variable becomes species at renewal or at new plantable positions, with a diversity constraint instead of a named palette. |

---

## 13. Glossary
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
| **ICGC** | Catalonia's cartographic and geological institute; publisher of the LiDAR point cloud (CC BY 4.0) |
| **PDCLAM** | Mataró's 2003 sewer master plan; source of its own 5–120 min design storm |
| **ACA / ARPSI** | Catalan Water Agency / its flood-risk areas. The *pluvial* ARPSI polygon is the municipal boundary, so it is not a hazard map |
| **PFI** | Pluvial Flood Index: Florence's published pluvial hotspot index (Pacetti et al.) |
| **Envelope vs central estimate** | Two ways to build a design storm: the upper bound across gauges (Barcelona's PDISBA) vs the best single estimate (Mataró's Gumbel fit). Never compare one with the other |
| **Témez / I1/Id** | Spanish method for turning a daily rainfall depth into a sub-daily intensity; I1/Id = 11 over this whole region, so the duration factor cancels between the two cities |
| **Leaf-on / leaf-off LiDAR** | Whether the flight was made with the canopy in leaf. Leaf-off makes the LAI proxy meaningless |
| **Gap fraction** | Share of laser pulses that pass through a crown; the LAI proxy is −ln(gap)/k |
| **T0–T3** | The four degrees of transfer: same city · another open-data city · a city missing the point cloud or the inventory · another climate (not claimed) |

---

## 14. Key numbers cheat sheet
| Number | What |
|---|---|
| **v7 results (10 Nov)** | |
| 2004/2005 | Parcs i Jardins replacement table (district × sidewalk); ~10% of Porta's 2007–2026 plantings match it |
| 20.1% / 30% / 8.3 ha | Porta tree cover (LiDAR 2021) / city 2037 target / Porta's shortfall |
| ~16% | Porta cover if every plane got a Brachychiton-size crown |
| 87% / 98% | Porta summer shade vs today: city rule (S1a) / method (replacement only) |
| +6% | Extra winter shade of the method (the trade-off) |
| 33.9 m³ | Runoff difference method vs S1a, T2-60 (< Δmin → not resolved) |
| 232 | Free planting spots in Porta (upper bound) |
| 92% / 103.5% | City rule + additions / method + additions |
| 28 / 31,580 | Barris (≥ 500 planes) / planes in the city LP |
| +9.2 pts / 27 of 28 | City LP median summer-shade gain vs city mix / barris that gain |
| 90.8 vs 92.2% | Sant Gervasi – la Bonanova, the one loss |
| 1,318 / 11,348 | Celtis / Tipuana at the city cap in the LP |
| 1,444 | Observed plane replacements 2018–2026 (S1b input; Celtis 296, Melia 219) |
| +5.7 / +7.2 pts | Tool margin, median of 33 barris: vs S1a / vs S1b |
| 11.7 → 8.8 pts | Porta margin: vs S1a → vs S1b |
| −0.15 / −0.19 °C | S4 − S0 mean UTCI, porous crowns, Andreu Nin: Honeybee / Python Tier 1 |
| −0.10 °C | Same, all Porta plane streets |
| +0.06 / +0.10 °C | Same, opaque crowns, Andreu Nin |
| r −0.73 / −0.82 | Proxy vs Ladybug: across points / on the S4 − S0 change |
| −0.01 / −0.02 °C | Bias of the Python Tier 1 chain vs Grasshopper (Porta / Andreu Nin) |
| TMYx 2011–2025 | Reference weather file (El Prat) |
| 0.1–0.3 °C | UTCI effect of tree-position optimisation in Hao et al. 2023 |
| p.33 | Climate Plan 2024: +5% cover, adapted 30→40%, 7 ha SUDS, 9 ha shade |
| **Earlier results (v0/v1)** | |
| 45% → 72% | Barcelona sealed surface, 1956–2009 |
| ~3 / yr, 60 mm/h | Storms above 60 mm/h in the first 20 min |
| 15% | Max share per species (tree master plan), city-wide over the urban fabric (~201,600 trees, 2017) |
| 27.45% / 43,722 | Plane trees in Barcelona (press, May 2026); ~29% among Porta's street trees |
| −56% → 12% | Plane cut within ten years (press, May 2026) |
| 30% / 40% | Master-plan 2037 targets: tree cover of the urban surface / climate-adapted species (both restated in the Climate Plan 2024, p.33: "+5%" cover, adapted species 30% → 40%) |
| < 3.5 / 3.5–6 / > 6 m | Sidewalk width → small / medium / large tree (2011 guide; < 2.5 m no tree) |
| 7 / 9 / 13 m | Tree spacing for small / medium / large |
| 194 of 832 | Porta's planes on Av. Meridiana (the city keeps planes on large avenues; whether Meridiana counts is open) |
| 35% / 32–52% / 89–107% | Crown area vs a plane, 2nd–3rd trunk classes: Pyrus / Celtis / Tipuana + Jacaranda |
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
| +16% | Summer shade, optimised vs random palette (15 Oct re-run; was +14%) |
| −2% | Winter shade, no-regret swap Tipuana → Jacaranda (15 Oct re-run; −9% with the old calendar) |
| −20% / −18% | Winter-heavy vs balanced: winter / summer shade (the trade-off) |
| 7 | Candidate species (5 named as plane replacements + Jacaranda, Brachychiton, not named as such) |
| 367 / 5.32 m / 2.12 | *Styphnolobium* LiDAR sample outside Porta (no merged crowns): trees / crown / LAI |
| 91 m³ | Δmin, runoff part of H1 (0.5% of T2-60 runoff) |
| 78 m³ | Best palette vs S1 today (below Δmin → not resolved) |
| 3.16% → 0.90% | Street-tree effect, T1 → T10 (arithmetic of the model) |
| 2.3–4.7 °C | Sun–shade UTCI gap on hot afternoons (lower bound) |
| 0.52 | ROC AUC of routing vs RESCCUE wet cells |
| **Transfer (§10)** | |
| 40% → 19% | Trees with a measured species-level trait: Barcelona → Florence (7% with both) |
| 52.2% / 92.9% | Mataró **top-30 species** covered by Porta's measured species (≥5 trees) / at genus level. As a share of the whole street stock: **46%** |
| 43.5% / 74.0% | Same for Florence (top-30; ≈ a third of its whole inventory) — **not** like-for-like, its inventory includes park trees |
| 17,204 / 117 | Mataró street trees / species rows (= **108** distinct binomials), composition only (2016) |
| 79,748 | Mataró tree positions in the GeoPackage: no species, no DBH, no height |
| ~82,000 | Florence public trees (inventory) |
| 22 / 18 | Catalan cities screened on LiDAR date / leaf-on **and** classified (2 leaf-on unclassified, 1 partly leaf-on, 1 leaf-off) |
| 44 | ACA pluvial municipalities — but the polygon is the municipal boundary, so **no city-wide** pluvial map (one 8.54 km² exception) |
| 19–32% | Raw Mataró-vs-Barcelona design-storm gap (do not quote it raw) |
| 66–80% | Share of that gap that is method, not climate (66% at 10 min, 77–80% at 20–60 min) |
| 0.93 / 1.00 | Harmonised ratio at T = 10 / T = 2 (an identity, not a finding) |
| 26 Sept 2021 | Porta's LiDAR mission day (shared by Badalona, Santa Coloma, Sant Cugat) |
| EPSG:25831 | CRS shared by Porta and Mataró |
| 2–3 weeks | Estimated cost of the Florence transfer (order of magnitude, not measured) |
| 18 Dec 2026 | Probable final delivery |
| 10 Nov 2026, 16:00 | Next tutor session (A. Chronis); then 17 Nov, 24 Nov, 1 Dec |

---

## 15. Decisions: what is settled and what is open (as of 3 Nov)
Know these exist and what the recommended default is; the tutor may ask.

**Settled since 21 Oct:** baseline = **S1a** (24 Oct); additions co-equal in the RQ and a project area the designer draws (24 Oct); heat clock **12–17 h CEST** (25 Oct); 15% cap counted on **street trees only** (26 Oct); city LP with the **local ceiling** (30 Oct); Grasshopper **not required** (30 Oct); H3 withdrawal accepted by the tutor (no objection, 30 Oct); weather reference **El Prat TMYx 2011–2025** (3 Nov); co-benefits only as a backup slide before 10 Nov (3 Nov); red "avoid" species out of the Barcelona palette (3 Nov).

| Open decision | Recommended default | Source |
|---|---|---|
| City LP against S1b | Rerun `scripts/city_lp.py` against the observed mix after 10 Nov (S1b is the reference since 6 Nov; the table is S1-2004) | `notes/methodology.md` §7 (branch), `notes/topic_decision.md` §10.4 |
| May a barri lose while the city gains? | Ask the tutor; a per-barri floor (no barri below the city mix) is one more constraint set | `notes/citywide_plan.md` §6.9 |
| Local ceiling in small barris | Different rule for barris with few planes (open) | `notes/citywide_plan.md` §6.9 |
| Is Sant Antoni enough as a transfer test? | Yes for within-city; Florence/Mataró as future work. Ask the tutor | `notes/citywide_plan.md` §4 |
| Infrared City | ~160 runs on final layouts, then calibrate the proxy; surrogate only as plan B. Awaiting reply (porous crowns?) | `notes/email_infrared_city_reply.md` |
| Parcs i Jardins | Follow up (RGF7342); ask for the current per-street list and the "adapted" species list | `notes/todo_manual.md` |
| Contribution statement | Choose among A (method), B (knowledge), C (validation) | `notes/decisions/contribution_statement.md` |
| Weather sensitivities | City station, city-terrain wind, +1.5 °C | `notes/decisions/weather_forcing.md` |
| Mataró access / licence | Licence UNKNOWN; three browser URLs settle the per-tree table | `notes/catalan_transfer_city.md` §3b |
