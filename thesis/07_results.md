# Results {#sec:results}

<!-- DRAFT (23 Nov 2026): headline numbers only, to be expanded into 7.1–7.5 (outline.md).
Sources: notes/barris_buildings_1000.md (30-species rerun, PR #125); scripts/make_backtest_deck.py (PR #137);
notes/mataro_transfer_test.md (PR #150); notes/tutor_feedback_17nov.md §9d (spot classes, branch claude/spot-classes). -->

All comparisons are against city practice (S1b), the announced mix (S1a) and today (S0), with the 30-species method palette (Chapter 5).

## Plane replacement across Barcelona

Across the 32 screened barris, the method keeps a median of 91.2% of today's summer shade. That is 6.7 points more than the announced mix and 14.7 points more than city practice, and the method is ahead of city practice in all 32 barris. In Porta it reaches 103.4% of today.

A narrow 7-species palette costs a median of 5.0 points of summer shade against the 30-species palette (range −2.2 to 14.8 points across the 32 barris).

## Back-test on real replacements

On 26 groups of plane trees that the city actually replaced, the method gives more summer shade than what was planted in 22 groups. The median rises from 59 to 139 m²·h of summer shade per tree, at equal trunk size.

## Transfer test: Mataró

On Mataró's six streets with the most plane trees, the method keeps a median of 83% of today's summer shade, against 63% for city practice, and wins on all six streets. Runoff is never worse than any practice. Crowns are approximated with Barcelona medians; the run with real LiDAR crowns is still to come.

## New planting spots in Porta

Of the 267 candidate spots, 153 are free, 103 are conditional and 11 are blocked (Chapter 5).

## Still to update

- **Diversity (TO UPDATE):** the current results lower species diversity against city practice. Runs with a diversity floor are in progress; numbers go here when they finish.
- **The 144 tall, narrow LiDAR trees (TO UPDATE):** the crown fix is running; all numbers above will be re-checked after it.
