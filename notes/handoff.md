# Handoff (24 Oct 2026)

Branch: `claude/tesi-conclusioni-revisioni-0639f0` (pushed, no PR yet). Diff vs `main`: 66 files.

## Done on this branch (24 Oct)
- **Problem v7 + gate 1:** the 2004/2005 district × sidewalk replacement table; Porta's plantings mostly do not match it (up to ~90%, an upper bound). Porta canopy 20.1% vs the city's 30% target, planes ≈29% of it (`notes/topic_decision.md` §10).
- **RQ v7** with three sub-questions and the subset that can be answered by 10 Nov. **Baseline decided:** S1a (2026 mix), S1b cited only.
- **Where the 15% comes from:** Santamour 1990, Kendal 2014, Nieuwenhuijsen 2022 added. Kendal/Santamour are now in the gap (notes + slide 7); genus and family shares are reported as an indicator. Fact-checked (Kendal quotes on p. 415, Santamour pages).
- **Tool:** S1a within the sizing rule, traits at equal trunk size, canopy cover; free planting spots and scenarios R / A / R+A; first Porta results (`tests/test_core.py` extended).
- **Methodology flowcharts** (IoB grammar, Earth palette): overview plus five modules (`slides/fig_v7/flow_*`).
- **10 Nov deck:** `slides/outline_10nov.md`, figures in `slides/fig_v7/`, `slides/shade_and_sponge_10nov.pptx` with speaker notes.

## Open
- **Heat on the slides is still the effective-shade proxy, not UTCI.** The first UTCI number comes from the Ladybug Tier 1 run on one Porta street (S0 vs one replacement). Claude prepares `exchange/to_gh/`; the user runs Grasshopper.
- User items in `notes/todo_manual.md`, "Fast track to the 10 Nov tutor session": Parcs i Jardins reply (would replace S1), 3 papers to download, RM cluster map on Miro by Tue 27 Oct, Infrared City email to the tutor, deck dry run.
- Decisions still pending (same file): weather forcing, H1/H2 wording, contribution statement, methodology §12.
- PR and merge of this branch into `main`: the user does this.

## Prompt for the next session
Paste the block below into a new chat launched in `1_THESIS_PROJECT`.

```
Continue from notes/handoff.md. First `git fetch` and check out branch claude/tesi-conclusioni-revisioni-0639f0 (or, if the user has merged it, start a new claude/* branch from main).

Goal: get the 10 Nov tutor deck (slides/outline_10nov.md, slides/shade_and_sponge_10nov.pptx) from the heat proxy to a first real UTCI number.

Steps:
1. Prepare the Ladybug Tier 1 run for one Porta street, S0 vs one replacement (mean UTCI 12–17 h, hot design day): files in exchange/to_gh/ following exchange/README.md, plus a short run sheet for the user. Use the weather forcing in notes/decisions/weather_forcing.md §4 unless the user decides otherwise.
2. When the user puts results in exchange/from_gh/, read them, add the UTCI number to slide 12 (outline, figure and pptx) and replace the "proxy, not yet UTCI" caveat.
3. Check notes/todo_manual.md "Fast track" for replies (Parcs i Jardins, Infrared City) and apply them (a per-street list replaces S1; Infrared City replaces step 1).
4. Run the tests if shade_sponge/ changed, run the fact-checker on new numbers, then commit and push (CLAUDE.md commit policy).
```
