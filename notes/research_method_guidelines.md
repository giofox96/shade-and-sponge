# Research method guidelines: seminar checklist

A running checklist of the advice from the two research seminars, checked against the thesis. Add rows when new lectures are processed with `/transcribe-lecture`.

**Sources so far:** Applied Research Technologies (RT, Fiona Demeur) L01 *From Research to Innovation* and L02 *The Research Ecosystem*. Research and Methodologies (RM) has no lectures processed yet. Lecture notes, transcripts and slides are in `seminars/` (gitignored, local only). Citations give the lecture, then the slide or the timestamp in the recording.

**Status (last check 8 Oct, against `notes/topic_decision.md` §7, `notes/methodology.md` and `slides/outline_20oct.md`):** ✅ met · ⚠️ partly · ❌ missing · ⏳ not due yet

## Top gaps to close

1. **Problem and solution validation with people** (B4, E2). There is model validation, but no stakeholder in the loop.
2. **An actor and stakeholder map** (C1–C2). It also tells you whom to interview for gap 1.
3. **State the innovation type and target TRL** (A2–A3). Each needs one line on the 20 Oct contribution slide.

## A. Framing the thesis

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| A1 | Applied research solves a real problem with measurable impact and produces actionable knowledge: a digital tool, a computational workflow or a design methodology that is tested and used | RT L01 slides 5–7, [00:22:22] | ✅ "a computational method that chooses which species replace Porta's plane trees and where" (methodology.md); `shade_sponge` v0 exists (PR #20) | Keep the framing |
| A2 | Say what is innovative compared with what exists, and which innovation type it is (Oslo Manual: product, process, social, marketing, organisational) | RT L01 slides 17–26, [00:45:25] | ⚠️ The gap is stated (SylvCiT's runoff module disabled; heat-only optimisers), but the innovation type is not named | Add "process innovation (a trait-based placement workflow), delivered as a tool" to the outline, slide 6 or 9 |
| A3 | Place the result on the Technology Readiness Level scale. IAAC theses usually reach TRL 3, sometimes 4; EU pilots expect 4–5 | RT L01 slide 29, [00:56:36]; RT L02 [01:42:30] | ❌ Not stated | Claim TRL 3 (experimental proof of concept on Porta). TRL 4 needs validation against measured data: say so as future work |
| A4 | Consider societal readiness: will the intended users adopt the tool? | RT L01 slides 30–31, [01:12:25] | ⏳ | Covered once E2 (user walkthrough) is done |
| A5 | Decide your intention for after the thesis (industry, start-up, policy, PhD, open source), since it shapes whom you involve | RT L02 slide 5, [00:07:14] | ❌ Not decided | One sentence in the thesis; also decides A6 |
| A6 | If the tool may go beyond IAAC, ask the programme about the IP policy early | RT L02 [01:54:21] | ❌ | Email David and Laura → `notes/todo_manual.md` |

## B. Problem definition

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| B1 | Fill the problem canvas: context (when, where), problem and trigger, affected group, emotional impact, current solution, its disadvantages | RT L01 slide 39, [01:28:36] | ⚠️ Context, problem, group and current-solution limits are in the problem statement (topic_decision §7). The Assignment 1 canvas is not in the repo, and emotional impact is absent | Add the canvas as `notes/problem_canvas.md`, or link the submitted file |
| B2 | Write the problem statement as a narrative: I AM / I TRY TO / BUT / THIS IS BECAUSE / IT GIVES ME THE FEELING | RT L01 slides 44–45, [01:38:20] | ❌ The current problem statement is evidence-led, with no persona narrative | Write it for the primary persona; it can open the talk |
| B3 | One primary persona, as specific as possible (e.g. landscape architect vs BIM architect) | RT L01 slides 40–42, [01:33:23] | ✅ v4: "a computational designer working on the municipal street-tree replacement" (topic_decision §7) | Use it consistently (CLAUDE.md still lists three personas) |
| B4 | Validate the problem: check with people in the field that it really is a problem for them | RT L01 slides 48–49, [01:44:49] | ❌ | 2–3 short interviews, e.g. a municipal tree manager and a landscape architect |
| B5 | Understand the problem from several perspectives, including ones you disagree with: literature, reports, policy | RT L01 slide 38, [01:26:27] | ✅ 55-paper literature review; tree master plan; Resilience Atlas | Keep the policy documents in the background chapter |

## C. Actors and stakeholders

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| C1 | Map the actors in eight categories: knowledge producers, knowledge users, enablers, funders, regulation and policy, industry and market, communities, non-humans. For each: role, contribution, needs, influence, stake, possible future role | RT L02 slides 9–14, [00:10:42]–[00:34:47] | ❌ | Half a page in `notes/actors_map.md`. Starting points from the repo: city open data, ICGC LiDAR, Resilience Atlas (producers); the primary persona (user); tutor / Infrared City, Ladybug (enablers); the tree master plan's 15% cap (regulation); trees, soil, water (non-humans) |
| C2 | Separate stakeholders (a stake in the outcome, present throughout) from actors, and engage key stakeholders from the start | RT L02 slide 15, [00:35:04]–[00:39:07] | ❌ | Mark 1–2 key stakeholders in the map; they are the interviewees for B4 and E2 |
| C3 | Know where data comes from, its licence, and local rules on collecting and processing it | RT L02 [00:26:31]–[00:27:52] | ✅ Licences recorded in `databases/data_inventory_barcelona.md` (e.g. ICGC CC BY 4.0, OSM ODbL) | Keep this up as data is added |

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

## F. State of the art and context

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| F1 | Know the state of the art (the highest current contribution), what works and what doesn't, and credit prior work | RT L01 [01:27:29] | ✅ Literature matrix and gap analysis | Add related EU projects: GreenInCities (heatwave risk index by LAND, UTCI for non-humans by IES, NDVI mapping) |
| F2 | Check tool databases such as digiNEB for existing Rhino/Grasshopper tools; you can also list your own tool there | RT L02 slide 53, [01:35:09] | ❌ | Search digiNEB for tree-placement and green-infrastructure tools |
| F3 | Use EU mission documents and Green Deal factsheets to show "why your problem is a problem" | RT L02 [00:52:35], [01:23:48] | ⚠️ Local evidence is strong (sealed surface, storms, heat mortality); the EU framing is unused | Optional: the Green Deal's "plant 3 billion trees by 2030" (slide 44) as the opening hook. Check whether Barcelona is a Mission City before saying so |

## G. Communication

| # | Rule | Source | Status | Next step |
|---|---|---|---|---|
| G1 | Pecha Kucha of about 5 minutes at the last RT session, summing up the seminar | RT L01 [00:18:18] | ⏳ | Reuse the 20 Oct talk (`slides/outline_20oct.md`) |
