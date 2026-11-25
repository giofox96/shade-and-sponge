# Midterm feedback, 24 Nov 2026 (A. Chronis, D. Leon): sorted, with answers, decisions and the plan to 1 Dec

*Written 24 Nov from Giovanni's ten voice messages, sent straight after the 5-min Pecha Kucha. No recording of the session exists, and Giovanni asked not to split the points by speaker. Raw transcripts: `/mnt/project-files/midterm/feedback_24nov_raw.md`. Plain-Italian explanation: `/mnt/project-files/notes/spiegazioni_24nov_it.md` (+ `.docx`). Previous round: `notes/tutor_feedback_17nov.md`. Questions brought today: `/mnt/project-files/midterm/domande_angelos_24nov.md`.*

Status marks: ✅ already true · 🟡 partly · ⬜ to do · ❓ decision for Giovanni.

**The message in one line.** Next Tuesday (1 Dec) Angelos wants a **critical review of the results**: the results we already have, shown differently (more visuals, fewer boxes, placed on the map of Porta) and explained by Giovanni: why the method works, what it changes, what it brings to research. Around that: do not shrink the study to the data you happen to have; generalise the method (all of Barcelona, Mataró, Florence) and use mock data where real data cannot be shared; cost/feasibility and stakeholders on their own slides; readable numbers; a **guided** tool.

## 1. Feedback, sorted

### 1a. Generalise, do not shrink (answers today's questions 3 and 5)

| # | What was said | What it means | Action |
|---|---|---|---|
| G1 | Data availability must not lower the quality of the research. Do not cut the study to the small piece of Porta where we have utility plans | eWise plans cover only the Santapau / Emili Roca / Desfar rectangle and cannot be published. That is not a reason to reduce the area | ⬜ Keep Porta (and beyond) as the study area; the eWise demo stays a private check |
| G2 | Where data cannot be shared, make **mock (synthetic) data** for utilities and substrate, publish that, and say why | The tool treats utilities as an input layer. A synthetic layer shows the mechanism; the real one is run privately and reported only as counts | ⬜ Synthetic utility layer for the public app (§3a) |
| G3 | "Generalise is better": Giovanni asked about all of Barcelona, Mataró and Florence, and the answer was yes | Today's question 3 is answered: **Florence stays a full transfer test**, not a lighter check. "All of Barcelona" needs a scope decision (D1) | ⬜ Florence full test before 6 Dec · ❓ D1 |

### 1b. Results first

| # | What was said | What is true today | Action |
|---|---|---|---|
| R1 | For next time, methodology matters, but **results** matter most: show them properly | Results exist (Porta, 26-group back-test, Mataró what-if, diversity floor, co-benefits). Needle-tree recompute ends tonight on OMEN; S1c (city's per-tree plan) runs after it | ⬜ One results set after the recompute; results frozen 6 Dec |
| R2 | Explain **why** the method works | Today we show *that* it wins (e.g. 22/26 groups), not *where the gain comes from* | ⬜ Gain decomposition (§3b) |

### 1c. Feasibility and cost

| # | What was said | What is true today | Action |
|---|---|---|---|
| C1 | Feasibility and cost are more interesting than having every substrate dataset. Collect economic data, but if it is missing, results still come first | Spot classes (153 free / 103 conditional / 11 blocked) are already a feasibility layer. Cost design note exists (`/mnt/project-files/notes/budget_replacement_transplant.md`): DIBA subsidy cap 500 €/tree for a full street-tree replacement, CYPE tree-spade transplant 502 / 1,451 / 2,867 € direct cost (90 / 200 / 300 cm balls), pit widening ~100 €/tree (PR #146). Cost was **not shown** today | ⬜ Cost per layout (§3c) + one cost slide |
| C2 | The pit size was explained, but late in the session; it went into the background | Pit size enters the budget only (memory 23 Nov) | ✅ nothing new |

### 1d. Users, decision maker, stakeholders

| # | What was said | What is true today | Action |
|---|---|---|---|
| S1 | "Who is the decision maker?" It was not clear from the talk | Narrative of 18 Nov (`tutor_feedback_17nov.md` §4): user = designer of a street project; approval by Parcs i Jardins | ⬜ Stakeholder slide (§3d) |
| S2 | Is the app for landscape designers or for the city's urban planners? Giovanni answered: more for the city planner, because the tool is tied to the city's rules | **Conflicts with the 18 Nov narrative** (designer first) | ❓ D2 |
| S3 | Who are the stakeholders, who decides, who is the botanist, the agronomist? | Partly known (§3d). Who designs Barcelona street projects (in-house vs commissioned firms) is **not verified** | ⬜ Short desk research on how a public street project works in Barcelona (§3d) |

### 1e. The tool's UI/UX

| # | What was said | Action |
|---|---|---|
| U1 | The UI looks dated, overloaded, full of text and inputs everywhere: "more a piece of software than a web app". "Let me walk in the UI" | ⬜ Guided version (§3e) |
| U2 | Make the process **guided**: start from one page, choose and draw the project area, then step after step along a flow chart to the result | ⬜ Flow chart first, then build |
| U3 | Risk: losing depth (today many settings). Giovanni: keep **all functions**, only guide them | Keep "advanced" behind each step |
| U4 | Authentication was asked; the answer was "not needed" | ✅ No login: autosave in the browser + download/open a project file (§3e) |
| U5 | (Giovanni) A final **video demo** is likely; a guided flow makes a better demo | ⬜ Demo script follows the guided steps |

### 1f. Presentation

| # | What was said | Action |
|---|---|---|
| P1 | Numbers too long, hard to read: **m²·h of shade** in particular | ⬜ New units (§3f) |
| P2 | Too many infographics, hard to follow. **Place them in the space** of the city, the project areas, Porta | ⬜ Results on the Porta map, one map per message |
| P3 | Sketches again, and not only for the rules: the **data must be localised** | ⬜ ComfyUI/perspective sketches of real Porta streets with the result drawn in (slot 3–6 Dec) |
| P4 | Cost and stakeholders asked, not shown | ⬜ One slide each next time |

### 1g. Critical review of the results and contribution (the task for 1 Dec)

| # | What was said | What it means | Action |
|---|---|---|---|
| W1 | For next Tuesday: **critical review of the results**. Same results, represented differently, explained well by Giovanni. "Next week: results, methodology" | Not a new run: a reading of what we have. What holds, what does not, where the method loses, how sure we are | ⬜ Critical review (§3g) = the main deliverable for 1 Dec |
| W2 | More visuals, fewer "cloud boxes" | Text boxes and flow boxes → maps, before/after images, one chart per message | ⬜ Applies to every slide from now on |
| W3 | "**What will I change** with this project?" Example: "imagine you get €10 M for this: you say I will lower the heat by X and the runoff by Y" | A scaled-up impact statement: what happens if the city used the method for the replacements it plans anyway, in physical units and € | ⬜ Impact statement (§3h) |
| W4 | "**What do you bring?**" (to research) | Contribution in one or two sentences, against the prior-art funnel (18 → 7 → 1 → 0) | ⬜ Contribution slide (§3h) |

### 1h. Giovanni's own points after the session (not tutor feedback)

| # | Point | Action |
|---|---|---|
| O1 | Maps of a project area: the back-test groups shown with Street View before/after (`backtest_works_streetview.pptx`, private). Maybe bring those changed areas back into the talk | ⬜ Use 1–2 back-test groups as the localised case (fits P2–P3); Street View stays private, use the map + aerial |
| O2 | Sub-questions and hypothesis disappeared when the new slides were made; they were an early request from Angelos | ⬜ Put back RQ + SQ1–SQ4 + H1/H2 (`notes/topic_decision.md` §10–§11) on one slide, and answer each SQ in the critical review |
| O3 | One slide with **all scenarios** (S0, S1a, S1b, S1c, S1-2004 cited, method) | ⬜ Scenario slide: name, what it is, source, run or cited (glossary in `study/guide.md` §13) |
| O4 | Final slide: **limits, constraints and assumptions** (existed as a backup, not shown) | ⬜ Rebuild from the assumption register (`slides/methodology_17nov.pptx`) |
| O5 | A **report** generated by the tool: scripted (no LLM), charts + statistics + plain discursive text, comparison: what improves, what gets worse | ⬜ "Report" step at the end of the guided flow (§3e), printable page/PDF |

## 2. Answers already given in the thread (24 Nov)

- **Authentication: no.** The app is static (GitHub Pages); a login needs a server and a database only to save a project. Instead: (1) autosave in the browser (`localStorage`), (2) "Download project / Open project" as a small JSON file (trees, actions, settings), (3) optional share link with the state in the URL. Argument for the thesis: the project data stay with whoever made them.
- **Private and public app: yes.** Same code, different data folder. Public = GitHub Pages with synthetic utilities/substrate. Private = runs only locally on the OMEN with the real data from a gitignored folder, never deployed. The only way that fits the eWise terms (AGBAR exclusive use, Nedgia confidential). Needs a build guard so the private data can never be published by mistake.
- **Parcs i Jardins 2013 document** (`Diversificació d'espècies`, internal, machine translation; check the Catalan original before citing):
  - p.6: target that **by 2062** no street-tree species exceeds 15%, **also in each of the 10 districts**. Coloma Rull wrote today "always city-wide". The two sources differ → one-line question to her, and D4.
  - §6: trees are replaced "as the trees die or when remodeling works are done": the thesis's starting case.
  - p.7 criteria: climate, space (adult crown and height vs façade and sidewalk), environmental services, coexistence (allergies, fragility), durability. Shade only as a "feeling of freshness", runoff absent: no criterion quantifies heat or water (supports the gap).
  - Names the technicians of the Directorate of Green Spaces and Biodiversity and the NTJ 14B gardening standard (first lead for §3d).

## 3. Work items

### 3a. Synthetic utilities and substrate (G1–G2)
- Generate a public mock layer for Porta from **published rules**, not from the eWise plans: e.g. sewer on the carriageway axis, house connections crossing the sidewalk (BCASA sewer guide 2015, `notes/data_requests.md` §6), plus random service lines at a declared density (ASSUMPTION). Label every map and file "synthetic".
- Run the spot classes with it; report real-data results only as counts per class, with the IBC credit.
- Owner: tool thread. Done when the public app shows the synthetic layer and the private build reads the real one.

### 3b. Why the method works: gain decomposition (R2)
Proposal (cheap, same LP): on the back-test groups and Porta, run
1. city practice (S1b),
2. **the same species as the practice, assigned optimally to the positions** (only *where* changes),
3. the method with the city's 7 species (palette effect),
4. the full method (30 species).

2−1 = gain from placement, 3−2 = gain from species choice, 4−3 = gain from a wider palette. One stacked bar = "why it works". Owner: tool thread (OMEN if it needs the LiDAR data). Must finish before 6 Dec.

### 3c. Cost per layout (C1)
- Step 0 (from the 18 Nov note): € per layout = replacements × unit cost + transplants × spade cost + conditional spots × cost of moving the object + pit widening.
- Report **€ per tree** and **€ per unit of shade gained** beside heat and runoff, never as an objective. Missing unit costs (moving a sign, a lamp, a bollard) are a gap: find a source or declare an ASSUMPTION range.
- Owner: tool thread for the numbers, this thread for the slide.

### 3d. Stakeholders and decision maker (S1–S3)
What we already know, with sources:
- **The city approves and pays** for street projects. Example inside Porta: Santapau executive project approved definitively by the Comissió de Govern on 9 Oct 2025, EUR 1,101,205.00 incl. VAT; Desfar initial approval 16 Sep 2025, EUR 557,352.07 (BOPB notices, `notes/sylvcit_followups.md` §1). The district runs the works news.
- **Parcs i Jardins de Barcelona, Institut Municipal** manages the trees: decides the species per pit (the per-tree plan sent 24 Nov), sets the 15% cap and the diversification criteria (Department of Green Strategy and Biodiversity, head Coloma Rull; 2013 document names technicians of the Directorate of Green Spaces and Biodiversity).
- **Utility companies** (water, sewer, electricity, gas, telecom) give the affected-services plans via ACEFAT/eWise.
- **Residents** comment during the public display of the project (30 working days, e.g. from 30 Sep 2025 for this project).

Still to verify (desk research, then one slide):
- Who **designs** a street project: municipal technicians or firms commissioned by the city (and which municipal company manages the works)? Not yet verified, do not state it.
- Whether agronomists / botanists sit inside Parcs i Jardins' technical staff and where they enter the process (the 2013 document only says "technicians").

Output: one slide "who pays · who designs · who decides the species · who maintains · who uses" and a sentence on where the tool enters (D2).

### 3e. Guided UI, version 0.2.0 (U1–U5)
- **Freeze today's app as v0.1.0** (`web/package.json` already says 0.1.0): git tag + GitHub release; keep it online at a stable path as "expert mode".
- **v0.2.0 = guided flow on the same code**, not a second app, so no function is lost. Draft steps:
  1. Choose the city / district and **draw the project area**
  2. See today's trees and spots (screening: condition, free / conditional / blocked)
  3. Set the trees you must act on (keep / move / replace) or let the tool propose
  4. Choose the priority (summer shade · winter sun · runoff) on the triangle
  5. Run → layout on the map + tree schedule
  6. Compare with city practice (and S1c), with **cost**
  7. **Report**: one scripted page (no LLM), printable to PDF: the area, the numbers, plain sentences ("summer shade +X% vs city practice; runoff unchanged; winter sun −Y%; cost €Z"), what improves and what gets worse (O5)
  8. Save / download the project, export (CSV, DXF)
  "Advanced" panel in each step = today's settings.
- Flow chart first (one image for Giovanni to approve), then build. Owner: tool thread. Not a result → can run after 6 Dec, but must be ready for the demo video (~10 Dec).

### 3f. Readable numbers (P1)
m²·h is correct but unreadable. Proposals, to pick one:
- **% of today's summer shade** (already used: method 103% vs practice 96%) as the headline;
- **average shaded sidewalk area over the afternoon (m²)** = m²·h ÷ hours of the window: a physical area anyone can picture;
- per street: "X more m² of shade on this sidewalk at 15:00", drawn on the map.

### 3g. Critical review of the results (W1, O2): the deliverable for 1 Dec
A short document + 6–8 visuals, built on the numbers after tonight's needle recompute and S1c. Structure, one page per sub-question:
1. **SQ by SQ** (RQ, SQ1–SQ4, H1/H2 from `notes/topic_decision.md` §10–§11): the answer, the evidence (Porta, 26-group back-test, Mataró, Florence when ready), a verdict (supported / partly / not).
2. **Where the method loses or does not matter**: narrow sidewalks (Piquer, the city wins), runoff differences below what the model resolves (do-no-harm only), diversity lower than practice without the floor, winter sun as a cost.
3. **How sure we are**: proxy vs Ladybug (r = −0.73 across points), sensitivities already run (interception s, capture distance, façade margin, palette 30 vs 7), needle-tree fix (+8.8% → +5.9% vs the city's palette), approximations (Mataró crowns, synthetic utilities).
4. **Why it works**: the gain decomposition (§3b).
5. **What it changes**: the impact statement (§3h).
Every number on a map of Porta or of a back-test group, not in a box (W2, P2).

### 3h. What it changes and what it brings (W3, W4)
- **Impact statement** (the "€10 M" question), built only from our numbers: the city already plans to change 513 of Porta's planes (S1c) and replaced 10,976 street trees in 2018–2026 (13% planes). If those replacements followed the method instead of practice: + X m² of afternoon shade on sidewalks, runoff not worse, at € Y (from §3c). Scale per barri and city-wide only as far as D1 allows. Heat in UTCI only where Ladybug/Infrared ran; otherwise say "shade", not "°C".
- **Contribution** (what do you bring): no published tool picks species *and* positions per tree, for heat and runoff together, inside a real city's planting rules (prior-art funnel 18 → 7 → 1 → 0, `notes/lit/prior_art_matrix.csv`), and the back-test against what the city really planted. Plus: the tool measures what each city rule costs (policy angle, 16 Nov).

## 4. Decisions for Giovanni (recommendations)

| ❓ | Recommendation | Why |
|---|---|---|
| D1 What "all of Barcelona" means | **Run the same pipeline on every barri overnight on the OMEN if it fits in one night**; otherwise Porta full + city-wide back-test (already 26 groups) + Mataró + Florence | The tutor said yes to generalising. The back-test is already city-wide; a full city run is the strongest "generalise" proof if runtime allows |
| D2 Primary user: designer or city planner | **Keep one primary user: the designer of a city street project**, working for the city and inside its rules; Parcs i Jardins = the one who approves. Revisit after §3d | The 18 Nov narrative, the four actions and the tree schedule are all designer tools. "Tied to the city's rules" holds for any designer of a public project. Changing user now costs slides and thesis text |
| D3 Guided UI before or after the freeze | **Flow chart this week, build after the results run (from ~2 Dec), ready by ~10 Dec for the video** | Does not change results; competes with Florence and the gain decomposition only for OMEN time, which it does not need |
| D4 15% cap: city / district / street-only | **Keep street-only as the declared simplification for now; ask Coloma one line on "district or city"** | Two city sources disagree (2013 document vs 24 Nov email); a rerun only if the answer changes the base |
| D5 Headline unit | **% of today's summer shade + average m² of shaded sidewalk**; m²·h only in the methods | §3f |
| D6 What to bring on 1 Dec | **The critical review (§3g) as a short PDF + 6–8 visuals, then the questions in §5**. No full deck | Angelos asked for the review; he wants to discuss, not watch a presentation |
| D7 Tool report (O5) | **Yes, as step 7 of the guided flow, after 6 Dec**; the same script can produce the per-area pages of the critical review earlier | Report and review share content; building it once saves work |

## 5. Questions for Angelos, Tue 1 Dec 16:00 (DRAFT: finalise on Mon 30 Nov, after the critical review)

1. **Generalise.** "Generalise" = the same method run on every Barcelona barri, plus Mataró and Florence? Or is Porta in full + city-wide back-test + two transfer cities enough?
2. **Why it works.** Is a decomposition of the gain (placement vs species vs palette) the explanation you expect? *(bring the draft bar)*
3. **Cost.** Which reads better for a city: € per tree, or € per m² of shade gained? Report only, or a budget cap in the optimiser?
4. **Decision maker.** Draft stakeholder slide: is the designer of a city street project, approved by Parcs i Jardins, the right user?
5. **Guided tool.** Do these eight steps match what you meant by guided? *(bring the flow chart)*
6. **Mock data.** Synthetic utilities in the public tool + counts from the real plans in the thesis: enough for the utilities constraint?

Carried over from today, not answered: diversity floor for the headline (Q1), S1c vs practice as the main comparison (Q2), runoff as do-no-harm and the name "Shade and Sponge" (Q6). Ask them only if time remains, or decide them ourselves with a recommendation.

## 6. Plan to Tuesday 1 Dec

| Day | Work | Who / thread | Done when |
|---|---|---|---|
| Tue 24 night | Needle-tree recompute ends on OMEN; then S1c run | OMEN RC thread + tool thread | new numbers listed |
| Wed 25 | Decide D1–D7 (Giovanni, from the explanation file) | Giovanni | answers in this note |
| Wed 25 | Line to Coloma: 15% cap per district or city-wide? (D4) | Giovanni / institutions thread | sent |
| Wed 25 – Thu 26 | Stakeholder desk research (§3d) | this thread (sources only) | slide draft with sources |
| Wed 25 – Fri 27 | Gain decomposition (§3b) + cost per layout (§3c) on Porta and back-test | tool thread (OMEN if needed) | stacked bar + € table |
| Thu 26 – Fri 27 | Guided-flow chart (§3e) + v0.1.0 tag/release | tool thread | image approved by Giovanni |
| Thu 26 – Sun 29 | Synthetic utility layer (§3a); public/private build split | tool thread | public app shows "synthetic" |
| 26–29 (as planned) | Mataró real LiDAR crowns + diversity floor | Mataró thread / OMEN | rerun done |
| 29 Nov – 3 Dec (as planned) | Florence **full** transfer test (G3) | OMEN | result table |
| Fri 27 – Mon 30 | **Critical review** (§3g): SQ-by-SQ verdicts, where it loses, how sure, why it works, what it changes (§3h) | this thread + thesis thread (it becomes ch. 6–7 text) | PDF/.docx + 6–8 map-based visuals |
| Sun 29 – Mon 30 | Slides that go with it: RQ + SQ + H, scenarios, cost, stakeholders, limits/constraints/assumptions (O2–O4, P4) | this thread / deck | 5 slides + §5 questions |
| **Tue 1 Dec 16:00** | Angelos: critical review, then questions §5 | Giovanni | answers noted |

After 1 Dec: guided UI build with the report step (to ~10 Dec), demo video script, localised sketches in the 3–6 Dec ComfyUI slot, **results frozen 6 Dec** (unchanged).

## 7. Giovanni's decisions, 25 Nov

- **D1:** all Barcelona barris (73), and they should be browsable in the web app. After the Mon 30 token reset (tool thread + OMEN).
- **D2:** "urban planner" meant the city's designer or a landscape designer: Giovanni answered "both". Keep the designer of a public street project; one stakeholder slide strengthens the narrative.
- **D3:** Giovanni drafts the guided-app plan himself (today or in the next days); before 1 Dec if possible.
- **D4:** thank Coloma Rull warmly and send her every open question now (draft in the thread, 25 Nov).
- **D5:** Angelos's point was about **decimals and long digit strings**, hard to read at a glance. Rule for every number in slides and app: 2–3 significant figures, no decimals unless they matter (103%, not 103.4%; 130 m²·h, not 129.7). The % of today + m² of shaded sidewalk proposal stands.
- **D6:** the critical review is **slides**, not a document.
- **D7:** yes, a scripted report in the tool.

Budget constraint (25 Nov): about 9% of the weekly tokens left until Sun 29. Until then only the critical-review slides; everything else after the reset.
