# Questions for the tutor, 20 Oct 2026 (one page)

Order: questions that change PS/RQ/H, then data access, then tools and logistics. "Fallback" = what I do if there is no answer. Answer column left blank.

| # | Question | Context (file §) | Fallback default | Affects | Answer |
|---|---|---|---|---|---|
| 1 | Is runoff volume alone acceptable, or must I add a peak proxy (rain intercepted in the peak 20-min block of the PDISBA hyetograph), or sewer surcharge? | PS v4 frames the hazard as >60 mm/h in the first 20 min; Selbig 2021 (matrix #10, full text read 9 Oct) reports no peak-flow effect from street trees; `slides/outline_20oct.md` Q&A "Why not peak flow?" | Volume only; PS wording adjusted so peak and surcharge are out of scope. Cost of the proxy (b): extra runoff-module output and one more objective column; small against methodology §10 (weeks 21 Oct - 3 Nov). Surcharge needs a sewer model: out of scope. | PS, RQ, H3, methodology §4 | |
| 2 | Can a hypothesis be a declared model boundary (H3: benefit fades as storms grow), or must each hypothesis be tested against observations? | `notes/decisions/hypothesis_tests.md` §9; `notes/todo_manual.md` | Declare H3 a method boundary; test the fade against the Freiburg data only if they prove open. | H3, slide 9 | |
| 3 | Which contribution should lead: A (method), B (knowledge) or C (validation)? | `notes/decisions/contribution_statement.md` | A, with the narrower gap wording (Dong 2026). | PS, RQ | |
| 4 | Infrared City: when can I have access, under which academic licence, and how do I cite it? | `notes/topic_decision.md` §6.4 (a)-(c); facts below | Ladybug Tier 1 (rule in the box below). | methodology §5, §10 (4-17 Nov) | |
| 5 | Infrared City, inputs and outputs: custom EPW plus urban offset? UTCI/MRT per point and hour? Maximum domain and grid? Per-species tree representation? | §6.4 (a)-(c) not repeated here; `notes/todo_manual.md` | Assume geometry only, so species traits enter by a shade x tau correction. | f1, methodology §5-6 | |
| 6 | RESCCUE pluvial depth maps: licence for thesis use, and does a T = 1 yr run exist? | `databases/data_inventory_barcelona.md` B1; `notes/resccue_data_request.md` (licence email sent 13 Oct) | Use the public T10/T100 tables; T = 1 yr from the PDISBA storm only. | validation, `site_selection.md` §6 | |
| 7 | Is the transfer test (Sant Antoni + Florence, planned 2-10 Dec) expected in the thesis, or can it move to the discussion? Florence data access is unchecked. | methodology §8, §10; `topic_decision.md` §5 | Sant Antoni in scope; Florence in the discussion only. | methodology §8, plan | |
| 8 | If no open Mediterranean throughfall data are found, is it acceptable that replacement-species parameters stay unvalidated (stated limitation), validating only the interception-model structure? | `notes/agent_backlog.md` tutor list | Yes, stated as a limitation, with sensitivity ranges. | H1, validation | |
| 9 | Is Grasshopper integration a hard requirement of the programme? | `CLAUDE.md` open questions | Keep Grasshopper for the heat module and the Python core. | methodology §9 | |
| 10 | Is the final delivery confirmed for 18 Dec 2026? | `CLAUDE.md` timeline | Plan to 18 Dec. | methodology §10 | |
| 11 | Slide format and language for the 5-minute talk? | `CLAUDE.md` open questions | Google Slides, English. | talk | |

## Infrared City: public facts (checked 16 Oct 2026)

| Fact | Source | Read level |
|---|---|---|
| A Python SDK exists on PyPI as `infrared-sdk`, version 1.0.0, summary "Python SDK for the Infrared City API"; project links: docs https://infrared.city/docs/sdk/, knowledge base https://infrared.city/knowledge-base/, examples https://github.com/Infrared-city/infrared-skills | https://pypi.org/pypi/infrared-sdk/json (PyPI metadata only; `infrared-city`, `infrared_city` and `infraredcity` return 404; `infrared` is an unrelated Ansible tool) | metadata only; docs not opened (infrared.city is blocked from the cloud) |
| Cloud-native, AI-driven simulation platform with plugins for Revit, Rhino, SketchUp and Grasshopper, plus API access for custom integrations | AEC Magazine directory listing, as quoted in a search summary (aidirectory.aecmag.com, `?p=324`) | search summary only; page not opened. A second listing (AEC+Tech) reportedly says "restricted beta, waitlist": unverified, relevant to question 4 |
| API limits, tree representation, validation and citation format: **not found** | - | open: questions 4-5 |

## Fallback rule for Infrared City

If access or per-species tree transmissivity is not available by **____** (date to fix with the tutor), Ladybug Tier 1 plus the tau correction becomes the in-loop heat engine.
