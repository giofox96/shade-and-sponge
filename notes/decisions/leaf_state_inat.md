# Winter leaf state of Tipuana and Jacaranda in Barcelona, from iNaturalist photos (15 Oct 2026)

Status: **adopted (user, 15 Oct)**: the calendar below is now in `databases/traits/phenology_palette.csv`; the old Jacaranda calendar (bare Jan–Mar) is kept as the sensitivity variant `jacaranda_bare_jan_mar`. **Tool outputs not re-run yet** (needs the raw site data, local only). Replaces the field photos in Porta (the user lives in Florence; `notes/todo_manual.md`).
Scripts and data: `scripts/inat_leaf_state.py` → `databases/barcelona/inat_leaf_state.csv` (annotation counts); photo scores in `databases/barcelona/inat_leaf_photos.csv` (one row per observation, with its iNaturalist URL).

## Method
1. **Annotations** (iNaturalist "Leaves" term: green / no live leaves / coloured / breaking buds), Barcelona, Spain, Portugal, Italy, all months. Too sparse to use: in Dec–Mar, 13 annotated Tipuana and 9 annotated Jacaranda observations across all four places (`inat_leaf_state.csv`).
2. **Photo scoring (own visual check):** first photo of every Barcelona-city observation (place 30022) in Dec, Jan, Feb and Mar, any year: 96 Tipuana and 74 Jacaranda observations (2014–2026, most 2023–2025; 168 of 170 are "casual", i.e. marked cultivated). Each scored once by me (single rater): **Lc** crown in leaf (crown view), **Lx** leaves present (close-up), **P** partial (thin, yellow or dry crown), **B** bare (branches with at most a few leaves or pods), **U** cannot tell (trunk, seed, ground).

## Result (share of the determinable photos, U excluded)
| Species | Month | n | In leaf (Lc + Lx) | Partial | Bare |
|---|---|---|---|---|---|
| Tipuana | Dec | 27 | 100% | 0% | 0% |
| Tipuana | Jan | 20 | 100% | 0% | 0% |
| Tipuana | Feb | 19 | 37% | 63% | 0% |
| Tipuana | Mar | 19 | 26% | 32% | 42% |
| Jacaranda | Dec | 16 | 100% | 0% | 0% |
| Jacaranda | Jan | 14 | 79% | 21% | 0% |
| Jacaranda | Feb | 24 | 67% | 33% | 0% |
| Jacaranda | Mar | 16 | 50% | 12% | 38% |

Many January–February Jacaranda crowns are yellow (senescing) but still carry their leaves.

## Comparison with the tool's leaf calendar (`databases/traits/phenology_palette.csv`, leaf fraction f by month)
- **Tipuana** (tool: Jan 1, Feb 1, Mar 0.5, Apr 0.5): **consistent for January**, so the base case of the winter-sun run (Tipuana leafed on 15 Jan) holds. Leaf drop starts in February, a month earlier than the tool assumes, and many trees are bare in March.
- **Jacaranda** (tool: Dec 0.5, **Jan–Mar 0**, from BBCH observations in Bétera, Valencia; Gandía-Ventura et al. 2025): **contradicted for Barcelona.** No bare Jacaranda appears in the photos before March; on 15 Jan most crowns are in leaf.

## Consequence for the tool v0 result
The "no-regret swap" (summer-only → balanced layout, ~100 Tipuana → Jacaranda, −9% winter shade at equal summer shade; `shade_sponge/README.md`) relies on Jacaranda being bare on the 15 Jan design day. The sensitivity runs tested Jacaranda half-leafed in Jan–Mar (the swap still appeared), but not Jacaranda fully leafed. If both species are leafed on 15 Jan, the winter advantage of Jacaranda shrinks to the difference in crown size and LAI, and the swap may weaken or vanish. **This needs a re-run of the tool**, which needs the raw site data (not in cloud sessions; run locally).

## Change (adopted 15 Oct)
- Jacaranda f: Dec 1, Jan 0.8, Feb 0.7, Mar 0.5 (rounded from the table above; was Dec 0.5, Jan–Mar 0), marked as an estimate from photos.
- Tipuana f: Feb 0.5 (was 1); Mar 0.5 and Jan 1 unchanged.
- Re-run `python -m shade_sponge` and `scripts/sensitivity_tool_v0.py` locally; update the no-regret claim in `shade_sponge/README.md`, `notes/methodology.md` §6 and the study guide.

## Limits
- Opportunistic photos, not a survey: people may photograph green or flowering trees more often; several years pooled; one rater; close-ups (Lx) show leaves on a branch, not crown cover.
- Some observations repeat the same tree (two identical Tipuana photos in March; one Jacaranda photographed in Feb and again in Mar).
- City-wide photos, not Porta; parks are included as well as streets.
- Small samples per month (14–27 determinable photos).
