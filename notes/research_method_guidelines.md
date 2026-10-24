# Research method guidelines: seminar checklist

A running checklist of the advice from the two research seminars, checked against the thesis. Add rows when new lectures are processed with `/transcribe-lecture`.

**Sources so far:** Applied Research Technologies (RT, Fiona Demeur) L01 *From Research to Innovation*, L02 *The Research Ecosystem* and L03 *The Entrepreneurial Ecosystem* (~21 Oct). Research and Methodologies (RM, Mathilde Marengo and Iacopo Neri) L02 *Mapping the field* (~22 Oct, review of the cluster maps); RM L01 is not in this checklist yet. Lecture notes, transcripts and slides are in `seminars/` (gitignored, local only). Citations give the lecture, then the slide or the timestamp in the recording.

**Status (last check 8 Oct, against `notes/topic_decision.md` §7, `notes/methodology.md` and `slides/outline_20oct.md`):** ✅ met · ⚠️ partly · ❌ missing · ⏳ not due yet

## Top gaps to close

1. **Problem and solution validation with people** (B4, E2). There is model validation, but no stakeholder in the loop.
2. **An actor and stakeholder map** (C1–C2). It also tells you whom to interview for gap 1.
3. **State the innovation type and target TRL** (A2–A3). Each needs one line on the 20 Oct contribution slide.

## Conclusions from the week of 19–24 Oct

**Tutor session, 20 Oct (not recorded; the points below come from the user, 24 Oct).**
1. **The problem was not explained well.** The plan had not been read properly before the session, so v6 (`notes/topic_decision.md` §9) now rebuilds the problem on it.
2. **First check whether Barcelona already has a structured plan, decided by a criterion, that sets which trees are replaced and where.** If it does, the problem is not "nobody decides where" but something narrower. This is the first gate of the problem, before anything else. What is known (`notes/tree_master_plan.md` §5): the mix, the mechanism and the sidewalk sizing rule are public. A per-street replacement list was announced in 2022 (press 🟡), but no copy has been found. Open leads: the older *Arbrat viari: selecció d'espècies* (Parcs i Jardins 2002/2004, BCNROC, not opened) and the email to Parcs i Jardins (`notes/email_parcs_i_jardins.md`, not sent). The RM lecturers raised the same risk (conclusion 2 below).
3. **Add a question to the problem: are there enough trees in Barcelona?** Not answered in the repo yet. Starting points: the plan's target 1, tree cover up to 30% of the urban surface (plan §2.1); its current value has not been extracted. Porta's own canopy cover can be measured from the 2021 LiDAR crowns already in the repo. An outside benchmark would be needed (e.g. the 3-30-300 rule; not in `papers/` yet, get it before citing).
4. **For the next session:**
   - a problem that is 100% clear;
   - the research question, scrutinised;
   - the methodology well defined, with **clear but short, concise flowcharts**;
   - what the **results** are and how the **validation** is carried out;
   - **the first results** already.

**What the two seminars change for the thesis**
1. **Present the palette as a method that scales to N species, not as "three species"** (RM L02 [01:26:14], H5). The lecturers heard "three species". The tool already runs a 7-species city palette and a 34-species Barcelona shortlist (`shade_sponge/README.md`), but no talk has shown this. Their point applies anyway: Barcelona's problem is a monoculture, so a method tested on few species has to show that it carries over to more.
2. **A precedent may already answer "which species where"** (RM L02 [01:26:14], H6). Barcelona's own tree maps, and a nursery's functional species database, may already assign species to streets. This is the same risk as `notes/topic_decision.md` §9.8 (a per-street replacement list), now flagged from outside. Check it before 29 Oct: if it exists, it becomes S1 and part of "the topic without the tool".
3. **Validation = case study + replicability + a test with people, each decided in advance** (RT L03 slide 56, E5–E6). Porta is the case study and the Florence/Mataró transfer is the replicability evidence (`notes/transferability.md`). The test with people (E2) is still missing. Before the walkthrough, write down what it has to show and how the result will be presented.
4. **Map the field before your own solution** (RM L02 [00:20:04], H2–H4). Cover what exists, how the task is done today without computation (the master plan, the 2011 guide, the city's qualitative criteria), and only then where this tool sits. Follow **one unit**: one Porta plane tree due for replacement.
5. **Context ≠ problem; current solutions = state of the art, digital tools included** (RT L03 slide 3, B6, F4). v6 keeps the context (master plan, plane removal) apart from the problem (no quantities per position). SylvCiT, Treepedia and i-Tree belong under "current solutions".
6. **Whom a tool leaves out** (RM L02 [00:44:36], H8). The lecturers' question, who a Grasshopper tool blocks out, is the argument for the web front-end.
7. **Stakeholders by level of engagement; involve whoever holds the data** (RT L03 slides 50–51, C4–C5). Parcs i Jardins is the key data holder (email draft ready). GreenInCities includes PEMB and Consorci del Besòs, so ask the RT lecturer whether they hold relevant data.

**Deadline:** RM cluster map, redrawn by hand on Miro, due **Tue ~27 Oct** (`notes/todo_manual.md`).

## A. Framing the thesis

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| A1 | Applied research solves a real problem with measurable impact and produces actionable knowledge: a digital tool, a computational workflow or a design methodology that is tested and used | RT L01 slides 5–7, [00:22:22] | ✅ "a computational method that chooses which species replace Porta's plane trees and where" (methodology.md); `shade_sponge` v0 exists (PR #20) | Keep the framing |
| A2 | Say what is innovative compared with what exists, and which innovation type it is (Oslo Manual: product, process, social, marketing, organisational) | RT L01 slides 17–26, [00:45:25] | ⚠️ The gap is stated (SylvCiT's runoff module disabled; heat-only optimisers), but the innovation type is not named | Add "process innovation (a trait-based placement workflow), delivered as a tool" to the outline, slide 6 or 9 |
| A3 | Place the result on the Technology Readiness Level scale. IAAC theses usually reach TRL 3, sometimes 4; EU pilots expect 4–5 | RT L01 slide 29, [00:56:36]; RT L02 [01:42:30] | ❌ Not stated | Claim TRL 3 (experimental proof of concept on Porta). TRL 4 needs validation against measured data: say so as future work |
| A4 | Consider societal readiness: will the intended users adopt the tool? | RT L01 slides 30–31, [01:12:25] | ⏳ | Covered once E2 (user walkthrough) is done |
| A5 | Decide your intention for after the thesis (industry, start-up, policy, PhD, open source), since it shapes whom you involve | RT L02 slide 5, [00:07:14] | ❌ Not decided | One sentence in the thesis; also decides A6 |
| A7 | Answer four questions: what is novel; what application beyond the thesis; how you will validate the research or tool; what opportunities could follow. The thesis does not have to be entrepreneurial | RT L03 slides 1, 62, [00:01:24], [01:32:31] | ⚠️ Novelty and validation are in `notes/topic_decision.md` §9.3 and the methodology; application and opportunities are not written | One paragraph each; they also feed A5 and the contribution chapter. Paths after the thesis: consultancy, municipalities, industry R&D, PhD (RT L03 slides 24–25) |
| A6 | If the tool may go beyond IAAC, ask the programme about the IP policy early | RT L02 [01:54:21] | ❌ | Email David and Laura → `notes/todo_manual.md` |

## B. Problem definition

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| B1 | Fill the problem canvas: context (when, where), problem and trigger, affected group, emotional impact, current solution, its disadvantages | RT L01 slide 39, [01:28:36] | ⚠️ Context, problem, group and current-solution limits are in the problem statement (topic_decision §7). The Assignment 1 canvas is not in the repo, and emotional impact is absent | Add the canvas as `notes/problem_canvas.md`, or link the submitted file |
| B2 | Write the problem statement as a narrative: I AM / I TRY TO / BUT / THIS IS BECAUSE / IT GIVES ME THE FEELING | RT L01 slides 44–45, [01:38:20] | ❌ The current problem statement is evidence-led, with no persona narrative | Write it for the primary persona; it can open the talk |
| B3 | One primary persona, as specific as possible (e.g. landscape architect vs BIM architect) | RT L01 slides 40–42, [01:33:23] | ✅ v4: "a computational designer working on the municipal street-tree replacement" (topic_decision §7) | Use it consistently (CLAUDE.md still lists three personas) |
| B4 | Validate the problem: check with people in the field that it really is a problem for them | RT L01 slides 48–49, [01:44:49] | ❌ | 2–3 short interviews, e.g. a municipal tree manager and a landscape architect |
| B5 | Understand the problem from several perspectives, including ones you disagree with: literature, reports, policy | RT L01 slide 38, [01:26:27] | ✅ 55-paper literature review; tree master plan; Resilience Atlas | Keep the policy documents in the background chapter |
| B6 | Keep context and problem apart: context is the background that leads to the problem; the problem is more specific | RT L03 slide 3, [00:04:42] | ✅ v6 separates them: the master plan and the plane removal are context; the missing quantities per position are the problem (`notes/topic_decision.md` §9.2) | Keep the split on the slides |

## C. Actors and stakeholders

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| C1 | Map the actors in eight categories: knowledge producers, knowledge users, enablers, funders, regulation and policy, industry and market, communities, non-humans. For each: role, contribution, needs, influence, stake, possible future role | RT L02 slides 9–14, [00:10:42]–[00:34:47] | ❌ | Half a page in `notes/actors_map.md`. Starting points from the repo: city open data, ICGC LiDAR, Resilience Atlas (producers); the primary persona (user); tutor / Infrared City, Ladybug (enablers); the tree master plan's 15% cap (regulation); trees, soil, water (non-humans) |
| C2 | Separate stakeholders (a stake in the outcome, present throughout) from actors, and engage key stakeholders from the start | RT L02 slide 15, [00:35:04]–[00:39:07] | ❌ | Mark 1–2 key stakeholders in the map; they are the interviewees for B4 and E2 |
| C3 | Know where data comes from, its licence, and local rules on collecting and processing it | RT L02 [00:26:31]–[00:27:52] | ✅ Licences recorded in `databases/data_inventory_barcelona.md` (e.g. ICGC CC BY 4.0, OSM ODbL) | Keep this up as data is added |
| C4 | Rank stakeholders by level of engagement: empowered, collaborative, involved, consulted, informed | RT L03 slide 51, [01:14:48] | ❌ | Add a level column to `notes/actors_map.md` (C1) |
| C5 | If you need data, find who holds it and involve them | RT L03 [01:14:48] | ⚠️ Parcs i Jardins email drafted (`notes/email_parcs_i_jardins.md`); RESCCUE request sent 13 Oct | Send the Parcs i Jardins email; ask the RT lecturer about PEMB / Consorci del Besòs (GreenInCities partners, slide 50) |

## D. Evidence and methodology

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| D1 | Back the solution with evidence: experiments, simulations, user testing, environmental data, case studies, expert interviews, literature | RT L01 slide 8, [00:23:51] | ⚠️ Simulations, environmental data, a case study and literature are covered; user testing and expert interviews are missing | Covered by B4 and E2 |
| D2 | Be feasible: the skills, knowledge and time to build it in a short thesis | RT L01 slide 9, [00:25:07] | ⚠️ Risks and mitigations are listed (methodology §11); the heat module and multi-objective search are still ahead | Re-check scope after the 20 Oct feedback |
| D3 | Define the methodology and its phases up front ("one of the most fundamental aspects") | RT L02 [01:03:56] | ⚠️ Draft v1 (methodology.md); status PROTOTYPING | Freeze it after 20 Oct |
| D4 | Measure impact by re-running the same baseline measurements after the intervention (GreenInCities co-monitoring) | RT L02 slide 32, [01:05:12] | ✅ S0 baseline vs scenarios, scored on the same metrics (methodology §7) | Say explicitly that this is the impact-evaluation logic |

## E. Solution and validation

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| E1 | Generate several solution ideas, then pick by originality × feasibility (How–Now–Wow) | RT L01 slides 46–47, [01:42:16] | ✅ The equivalent was done: options A–D scored on fixed criteria (topic_decision §2, §6.2) | — |
| E2 | Validate the solution with users: give them the tool and ask whether it solves the problem (interviews, focus groups, surveys) | RT L01 slide 49, [01:46:07] | ❌ Only model validation (Freiburg interception data, paired-catchment benchmarks, Ladybug vs ENVI-met) | One walkthrough with the primary persona near the end; add it to the plan (methodology §10) |
| E3 | Test with people who didn't build the tool: they will get different results | RT L01 [01:05:29] | ⏳ | Same session as E2 |
| E4 | Design for the least technical user (e.g. a municipal officer), inclusivity (NEB values) | RT L02 [01:30:11], slide 49 | ⚠️ A web app for non-technical users is planned for the last weeks (CLAUDE.md "Tool", PR #20) | Keep it in scope only if time allows (D2) |
| E5 | Validation in a thesis: a case study, showing it is replicable in other contexts ("important!"), tests or experiments with the quantitative/qualitative data chosen beforehand, a first client or pilot | RT L03 slide 56, [01:23:13] | ⚠️ Case study (Porta) and replicability (Florence/Mataró transfer, `notes/transferability.md`) are planned; the test with people is E2 | Present the transfer test as the replicability evidence |
| E6 | Before testing, decide what you need to learn and how you will present that data | RT L03 [01:40:32] | ❌ | Write the walkthrough protocol (questions, measures, figure) before running E2 |

## F. State of the art and context

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| F1 | Know the state of the art (the highest current contribution), what works and what doesn't, and credit prior work | RT L01 [01:27:29] | ✅ Literature matrix and gap analysis | Add related EU projects: GreenInCities (heatwave risk index by LAND, UTCI for non-humans by IES, NDVI mapping) |
| F2 | Check tool databases such as digiNEB for existing Rhino/Grasshopper tools; you can also list your own tool there | RT L02 slide 53, [01:35:09] | ❌ | Search digiNEB for tree-placement and green-infrastructure tools |
| F3 | Use EU mission documents and Green Deal factsheets to show "why your problem is a problem" | RT L02 [00:52:35], [01:23:48] | ⚠️ Local evidence is strong (sealed surface, storms, heat mortality); the EU framing is unused | Optional: the Green Deal's "plant 3 billion trees by 2030" (slide 44) as the opening hook. Check whether Barcelona is a Mission City before saying so |
| F4 | "Current solutions" are your state of the art: which digital tools exist, and what works and what doesn't in them | RT L03 slide 3, [00:04:42] | ⚠️ Research tools are covered (SylvCiT, heat-only optimisers); practice tools are not (i-Tree, Treepedia, the city's own maps) | Add a short critique of each to the background chapter |

## H. Mapping the field (RM)

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| H1 | Make the map yourself; AI may help search, but must not do the thinking or the exercise. A simple, unfinished map you made beats a complete generated one; mark unknowns with "?" | RM L02 [00:37:52], [01:51:00] | ⏳ Due ~27 Oct | Redraw by hand on Miro (`notes/miro_map_proposal.md` is input only, not the map) |
| H2 | Peel the onion: what exists, what has been done, the limits of current uses, and only then where yours sits. Include "the topic without the tool" | RM L02 [00:20:04], [00:24:14], slide 88 | ⚠️ The literature gap exists; today's non-computational practice (master plan, 2011 guide, qualitative criteria) is not on the map | Put it at the root of the map |
| H3 | Follow one unit through everything behind it | RM L02 [00:24:14], slide 88 | ❌ | One Porta plane due for replacement: data → constraint → choice → heat/runoff → who decides |
| H4 | Explain, don't just describe; show hierarchy (primary/secondary/tertiary) and cross-links, not a linear schema | RM L02 [00:18:39], [01:04:16], slide 48 | ⏳ | Link it to cluster 3's shared frame: urban vulnerability → data → options for non-expert decision makers |
| H5 | Few species is limiting; present the case study as a methodological test for more species, so it is replicable | RM L02 [01:26:14] | ⚠️ The tool runs 7 species and a 34-species shortlist, but the talks did not show it; the lecturers heard "three species" | State the palette size; show the shortlist run as the scaling test |
| H6 | Precedents: Treepedia (MIT Senseable City Lab); Barcelona's own tree maps, which may already say which species go where; a Barcelona nursery's functional species database (name unclear); Smelly Maps (cluster example) | RM L02 [01:25:03]–[01:28:16] | ❌ None in the literature matrix | Check each; read the links Mathilde leaves on Miro; a city species-to-street map would affect §9.8 and S1 |
| H7 | List only papers you have read (or say which parts); add practice-based projects: 5+ precedents (2 theoretical, 3 practice), each annotated with source / what it does / what it does not | RM L02 [01:51:00], slide 91 | ⚠️ Strong on theory, weak on practice | Practice: Treepedia, i-Tree, SylvCiT (open-source tool), the city's tree maps |
| H8 | Ask who a tool's infrastructure leaves out, e.g. who a Grasshopper tool blocks out | RM L02 [00:44:36] | ✅ The web front-end for non-technical users answers this | Say it explicitly in the methodology |

## G. Communication

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| G1 | Pecha Kucha of about 5 minutes at the last RT session, summing up the seminar | RT L01 [00:18:18] | ⏳ | Reuse the 20 Oct talk (`slides/outline_20oct.md`) |
