# Mataró transfer test, first run (23 Nov 2026)

Script `scripts/mataro_transfer_test.py` → `databases/mataro/transfer_test.csv` (aggregates only), figure `notes/figures/mataro_transfer_test.png`.

## What was tested
A **forward what-if, not a back-test.** Mataró has one inventory snapshot (T_C_ARBRAT, received 12 Nov 2026), so there are no observed replacements to replay as in Barcelona (26 groups). Instead, on six streets (the streets with most plane trees in five barris), a project replaces **every plane** (640 positions in total). At the same positions, with every new tree at the same trunk size (TERCERA), we compare:
- **Method**: same core as the Barcelona back-test (30-species palette, 15% cap, façade clearance, weighted-sum LP with HiGHS, balanced weights 0.50 / 0.25 / 0.25).
- **City practice**: S1a (Barcelona's announced mix) and S1b (Barcelona's built mix, 2018–2026), 5 random draws each, as in Barcelona.
- **S1m, Mataró's own practice**: the species mix of Mataró's street trees in the smallest girth band (< 30 cm, about 3,400 trees), read as recent plantings (ASSUMPTION), 5 draws.
- Random palette, 5 draws.

## Result
| Street (barri, planes) | Method | S1a | S1b | S1m (Mataró) | Random |
|---|---|---|---|---|---|
| Jaume Isern (Eixample, 76) | 86% | 63% | 69% | 54% | 54% |
| Ronda Alfons X el Savi (Eixample, 124) | 80% | 59% | 60% | 50% | 48% |
| Francesc Layret (Pla d'en Boet, 137) | 87% | 72% | 68% | 55% | 51% |
| Foneria (Vista Alegre, 150) | 87% | 67% | 67% | 50% | 51% |
| València (Cerdanyola, 89) | 42% | 33% | 35% | 29% | 28% |
| Ronda Miguel de Cervantes (Palau-Escorxador, 64) | 76% | 46% | 55% | 43% | 43% |
| **Median** | **83%** | **61%** | **63%** | **50%** | **49%** |

Values = summer shade of the new trees (15 July, 12–17 h, proxy) as % of the shade of planes of the same trunk size.
- **Summer shade: the method wins on 6 of 6 streets** against every practice and the random palette (median +20 points vs S1b, +33 vs Mataró's recent plantings).
- **Runoff: never worse than any practice** (6/6). Against today's planes it is 0.3–1.2% higher (4–11 m³ per street), the same direction as every practice (practice +10–28 m³). So "no worse than practice" holds; "no worse than today" does not, as in Barcelona.
- **Winter shade (a cost):** lower than S1b on 6/6, lower than S1a on 3/6 and lower than S1m on 2/6.
- **València is the weak case:** a narrow street, where 57% of positions have no palette species that clears the façades, so the tool falls back to the smallest crown (42% vs 35% for S1b).

## Approximations (say these whenever the result is shown)
1. **No Mataró LiDAR** (ICGC is blocked from the cloud and the PC was off). Every tree takes the median crown of its species in Barcelona's LiDAR pool. The method is not limited by this, because its palette has the same crowns in both cities. Measured Mataró crowns (ICGC flight 20 Jul 2021, leaf-on) are the next step, on the OMEN.
2. **Buildings: Overture Maps** (release 2026-11-18.0, ODbL). Height = the `height` field, else floors × 3 m, else 9 m. The 9 m default covers 2–39% of the buildings, depending on the street. Ground is flat (no DTM).
3. **Runoff**: no Mataró pluvial hazard map exists, so runoff counts all open ground (no hotspots), with all open ground sealed. The storm is Barcelona's T2-60, used only to rank layouts.
4. **No sidewalk-width sizing rule** (Mataró widths are not measured). Only façade clearance applies, to the method and to the practice draws alike.
5. **The 15% cap is per barri.** It is the method's rule; Mataró has no such rule.
6. Mataró's practice (S1m) is inferred from girth, not from planting dates.

## Caveat on diversity
Where the cap does not bind, one species dominates: Firmiana simplex takes 133 of 137 positions on Francesc Layret and 144 of 150 on Foneria, giving 1.2–6.3 effective species. This is the same behaviour as in Barcelona. The diversity floor (`--diversity=N`) exists but was not used in this run. Rerun with it before showing species choices, not only shade.

Data: Ajuntament de Mataró tree inventory, *Llicència oberta d'ús d'informació – Catalunya* (no sublicensing, so the inventory is not in the repo). Overture Maps Foundation buildings (ODbL).
