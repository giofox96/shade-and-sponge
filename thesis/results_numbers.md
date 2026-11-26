# Results numbers for the thesis (one source of truth)

*Built 26 Nov 2026 from the CSVs on `main` after the needle-tree fix (PR #184, merged 26 Nov). Every number below was recomputed from the file named in its row. Chapters 6–9 and the abstract quote only from this sheet. When a run changes, update this sheet first, then the chapters.*

Conventions:
- **Porta** means 832 plane positions replaced. The palette is Barcelona's (30 species), the sizing rule is exact, and the trunk class is TERCERA where the city has enough trees of the species, else SEGONA (9 of 30 species: Pyrus, Prunus, Magnolia, Tilia × euchlora, Fraxinus, Hibiscus, Ginkgo, Acer campestre, Acer monspessulanum; `meta.json` trunk_class).
- **Method** means the balanced layout `S4_s0.50_w0.25_r0.25` (weights: summer 0.50, winter 0.25, runoff 0.25), unless stated otherwise.
- Summer and winter shade are given as a % of today's (S0). The window is 12–17 h on the design days.
- **S1a** is the announced mix and **S1b** is city practice. Each is the mean of 10 seeds.
- **Runoff hot** is the runoff at the flood hotspots in the T2-60 design storm, in m³.

## 1. Porta, plane replacement (R)
Source: `databases/barcelona/tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv`.

| Scenario | Summer % | Winter % | Runoff hot m³ | Total runoff m³ | Interception m³ | Effective species | Max genus % |
|---|---|---|---|---|---|---|---|
| S0 today | 100 | 100 | 2,702.8 | 17,649.2 | 801.5 | (planes) | 30.6 (Platanus) |
| S1a announced mix | 100.2 | 112.0 | 2,703.3 | 17,653.8 | — | 9.3 | 17.6 |
| S1b city practice | 99.0 | 109.4 | 2,704.7 | 17,661.0 | — | 15.9 | 17.5 |
| S1 random | 91.4 | 110.0 | 2,709.6 | 17,683.3 | — | 28.6 | 15.1 |
| **Method (balanced)** | **106.7** | **99.2** | **2,698.8** | **17,641.1** | **824.3** | 5.7 | 15.6 |
| Summer only (s=1) | 106.9 | 107.8 | 2,698.9 | 17,638.4 | 827.7 | 5.8 | 15.4 |
| Runoff only (r=1) | 106.5 | 110.3 | 2,698.1 | 17,640.5 | 825.1 | 6.9 | 14.7 |
| Winter only (w=1) | 74.9 | 82.3 | 2,720.0 | 17,723.4 | 702.7 | 5.7 | 15.3 |

- **Method vs city practice:** +7.7 pts of summer shade (106.7 vs 99.0). Winter shade is 99.2% vs 109.4%, so the method gives more winter sun. Total runoff is 17,641.1 vs 17,661.0 m³ (−19.9 m³), below Δmin = 91 m³ (a total-runoff threshold, `notes/decisions/runoff_metric_sensitivity.md`), so we call it **equal**. Hotspot runoff 2,698.8 vs 2,704.7 m³ (−5.9 m³) is reported but not tested against Δmin (different scale; topic_decision §10.5 row 5).
- **The balanced layout's species mix:** Firmiana simplex 423 (50.8%), Gleditsia 176, Tipuana 48, Prunus cerasifera 31, Celtis sinensis 29, plus 18 other species. **City practice** (top 6): Celtis australis 127, Melia 112, Gleditsia 84, Grevillea 64, Koelreuteria 58, Jacaranda 45.
- **City palette (7 species)** from `tool_v0_summary_sizeexact_trunkTERCERA.csv`: method 99.3%, S1a 91.2%, S1b 93.8%.
- **Before and after the needle fix** (PR #184 body):
  - 7 species: method 98.3 → 99.3.
  - 30 species: method 103.4 → 106.7, S1a ≈96.8 → ≈100.2, S1b ≈95.5 → ≈98.9.
  - Porta needle trees: 136 → 27. Total crown area is unchanged.

## 2. S1c, the city's own per-tree plan (513 of Porta's planes)
Source: `tool_v0_summary_barcelona_*_replporta_plan_planes.csv`, plus the PR #184 body. The plan itself is gitignored raw data. Credit: Parcs i Jardins de Barcelona, Institut Municipal.

| Scenario | Summer % | Winter % | Runoff hot m³ | Effective species |
|---|---|---|---|---|
| S0 | 100 | 100 | 2,702.8 | — |
| S1c city plan | 98.2 | 104.4 | 2,699.8 | 9.7 |
| Method, no diversity floor | 101.4 | 97.7 | 2,699.5 | 5.7 |
| **Method, floor 9.7 (same diversity as the plan)** | **101.4** | **98.1** | **2,699.6** | 9.7 |
| Method, floor 14.3 | 100.9 | 98.2 | 2,699.7 | 14.3 |

- At the same diversity as the plan, the method gives **+3.2 pts** of summer shade, 98% vs 104% winter shade, and equal runoff.

## 3. Diversity floor (Porta)
Source: `databases/barcelona/diversity_series.csv` (balanced layout). Diversity is measured as the effective number of species, exp(Shannon) (Nicol et al. 2026).

| Floor | Effective species | Summer % | Winter % | Top species share % | Summer lost vs no floor (pts) | Carbon % of S0 | Pollen load % of S0 (lower bound) |
|---|---|---|---|---|---|---|---|
| none | 5.7 | 106.7 | 99.2 | 50.8 | 0 | 69.4 | 5.4 |
| 7.5 | 7.5 | 106.6 | 99.4 | 43.0 | 0.16 | 69.0 | 6.1 |
| **9.4 (≈ S1a, announced mix: 9.3 over 10 draws)** | 9.4 | **106.3** | 99.9 | **35.6** | **0.42** | 68.2 | 6.7 |
| 10 (Santamour) | 10.0 | 106.2 | 100.0 | 33.9 | 0.48 | 67.7 | 6.8 |
| **15.6 (≈ S1b, city practice: 15.65 in seed 0, 15.9 over 10 draws)** | 15.6 | **105.1** | 101.0 | 17.8 | 1.59 | 64.1 | 8.0 |
| 20 | 20.0 | 103.5 | 101.2 | 12.6 | 3.18 | 60.8 | 8.4 |

- Matching the announced mix's diversity costs **0.4 pts** of summer shade. Matching city practice's diversity costs **1.6 pts**, and the method still beats practice: 105.1 vs 99.0.
- Without a floor, the method is **less diverse** than practice (5.7 vs 15.9 effective species). With a floor, the top species share falls from 50.8% to 35.6% (floor 9.4) or 17.8% (floor 15.6).
- **Correction to the brief of 26 Nov:** it said "top species 44 → 33%", which the current file does not give.

## 4. Co-benefits (Porta; indicators, not objectives)
Source: `cobenefits_porta*.csv`, `diversity_series.csv`. Carbon comes from Jucker et al. 2017 allometry.

| Scenario | Carbon stock % of S0 | Pollen load % of S0 (lower bound only; see §11 for the range) | Effective species (S1a/S1b: one draw, seed 0) |
|---|---|---|---|
| S1a | 52.3 | 6.6 | 9.16 |
| S1b city practice | 52.1 | 8.5 | 15.65 |
| Method (balanced) | 69.4 | 5.4 | 5.7 |
| Method, floor 9.4 | 68.2 | 6.7 | 9.4 |

- **Correction to the brief of 26 Nov:** it said "carbon 58 vs 42", which is the pre-fix value. The current figure is **69 vs 52** (% of today's stock). Every replacement starts with less carbon than today's mature planes, because new trees are taken at the same trunk size.

## 5. Back-test: 26 groups the city really replaced (2018–2026)
Source: `databases/barcelona/backtest_works_guide.csv`. This is the deck's run (`scripts/make_final_new.py`). It uses the 2011 guide sizing on measured sidewalks, with the same positions and the same trunk size. Shade per tree = (shade − shade with no tree) / n.

| Variant | Groups won (gain > 1%) | Median shade per tree, city → method (m²·h) | Ratio | All 366 positions | Runoff hot worse than city |
|---|---|---|---|---|---|
| **Guide sizing (headline)** | **23 of 26** | **76 → 130** | **1.7×** | **+45%** | **0 of 26** |
| Guide sizing, small species capped | 20 of 26 | 76 → 129 | 1.7× | +44% | 0 of 26 |
| Façade test only | 15 of 26 | 76 → 110 | 1.5× | +36% | 2 of 26 |

- The earlier "22/26, 59 → 139" (PR #137) used the capped variant before the needle fix. **Replace it everywhere.**

## 6. Barcelona: 32 barris (30-species palette)
Source: `tool_v0_summary_<barri>_barcelona_sizeexact_trunkTERCERA.csv`, `barris_summary_barcelona.csv`.

**Status: the 30-species barri runs date from 16 Nov, before the needle fix (only the 7-species barri runs were redone on 24 Nov). Mark every number in this section "pre-fix, to rerun".**

| Median of 32 barris | Value |
|---|---|
| Method summer % (layout with the most summer shade) | 91.1 |
| Method summer % (balanced) | 90.9 |
| Gain over S1a (pts) | +6.7 |
| Gain over S1b (pts) | +8.2 |
| Palette 30 minus palette 7 (pts) | 5.0 (range −2.2 to 14.8) |
| Barris where the method beats S1a / S1b | 32 / 32 |
| Runoff hot change, method vs S0 | +0.55% (S1b +0.76%); method ≤ S1b in 32 of 32 |

- **Correction:** the earlier "+14.7 vs S1b" (thesis ch. 7, 23 Nov) does not reproduce from these files. The same S1b runs give +8.2. Use +8.2.
- **City LP** (Porta + 27 barris, one city-wide 15% cap): `citylp_summary.csv`. Porta city LP 100.3% (7-species palette, pre-fix).

## 7. Mataró transfer test (forward what-if, 23 Nov)
Source: `notes/mataro_transfer_test.md`. Six streets with the most plane trees. Crowns are approximated by Barcelona species medians; the run with real ICGC LiDAR crowns is still to do.

| Median | Method | S1a | S1b | S1m (Mataró's own recent plantings) | Random |
|---|---|---|---|---|---|
| Summer % of the planes' shade | 83 | 61 | 63 | 50 | 49 |

- The method wins on 6 of 6 streets. Runoff is never worse than any practice (6/6), but it is 0.3–1.2% above today's planes, as every practice is. Winter shade is below S1b on 6/6.

## 8. New planting spots (A)
Source: `notes/tutor_feedback_17nov.md` §9d, `porta_planting_spots.csv`.
- 267 candidates: 153 free · 103 conditional · 11 blocked.
- The additions table (`additions_summary.csv`, 153 spots) is still the 7-species palette and pre-fix: R+A optimised 369,785 m²·h vs R+A S1a ≈338,000. Use it only as "to rerun".

## 9. Validation and sensitivity
- **Heat proxy vs Ladybug UTCI** (mesh rerun): r = −0.73 across points in S0, and −0.82 on the S4 − S0 change (opaque crowns; −0.76 with LAI opacity). The slope is ≈ −0.5 °C UTCI per hour of full shade (`notes/methodology.md` l.74).
- **Interception** s = 1.75 mm per unit LAI, calibrated on Anys & Weiler 2024 (`scripts/calibrate_interception.py`).
- **Δmin** = 91 m³, the smallest difference in Porta's **total** runoff the model resolves (not a hotspot threshold) (`notes/decisions/runoff_metric_sensitivity.md`).
- **Flow routing vs RESCCUE flood maps:** ROC AUC 0.52; only the tail is informative (`study/guide.md`).

## 10. Cost and scale (deck, `scripts/make_final_new.py`)
- Replacement: up to 500 € per tree (DIBA subsidy cap). Moving a tree with a tree spade: 502 / 1,451 / 2,867 € (CYPE, 90 / 200 / 300 cm root balls). Widening a pit from 1 to 1.5 m²: ≈100 € (CYPE).
- 10 M€ ≈ up to 20,000 replacements (500 € is a subsidy cap, so an upper bound) ≈ 15 years of the city's replacements with a change of species (~1,300 a year). The method gives 1.7× the summer shade per new tree at the same cost (back-test median).
- City replacements 2018–2026: 10,976 observed, 13% of them planes (`notes/topic_decision.md` §11).

## 11. Added by ch.6–7 (26 Nov 2026)
Each row recomputed or read from the named source.

- **Average effectively shaded open ground, Porta (summer).** The heat proxy sums 6 hourly sun positions (12:00 to 17:00 CEST, `hours_utc=range(10, 16)` in `shade_sponge/heat.py`), each counted as 1 h. Average shaded area = m²·h ÷ 6 (the brief said ÷ 5 h, but the code samples 6 hours). Source `tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv`:
  - S0 360,119 → 60,020 m²
  - S1a 360,796 → 60,133 m²
  - S1b 356,384 → 59,397 m²
  - random 329,291 → 54,882 m²
  - method (balanced) 384,278 → 64,046 m²
  - Method − S1b = +4,649 m². Method − S0 = +4,027 m².
  - Winter, the same ÷ 6: S0 31,187, S1b 34,128, method 30,950 m².
- **Back-test per tree as average area** (`backtest_works_guide.csv`, ÷ 6): city 12.6 m², method 21.6 m² per tree (medians).
  - Total over 366 positions: method − city = +2,603 m² average shaded area.
  - Groups lost (gain < 1%):
    - el Poble-sec, group 1107, 10 trees: city Tecoma stans, method Hibiscus syriacus, −60%.
    - el Camp de l'Arpa del Clot, group 3050, 20 trees: Cercis vs Catalpa, −8.7%.
    - el Parc i la Llacuna, group 3707, 11 trees: Gleditsia vs Melia, −3.5%.
  - Largest win: Sant Andreu, group 1114, 13 trees: Fraxinus ornus vs Celtis australis, +554%.
  - Hotspot runoff, method − city: mean −0.05 m³ per group, max 0.0 (never worse).
  - Winter shade: method lower than city in 14 of 26 groups.
- **Back-test selection** (`scripts/backtest_works.py` docstring):
  - ≥ 10 trees changed species in one quarter within 25 m;
  - ≥ 50% of the new trees in the smallest trunk class (PRIMERA);
  - in a barri with LiDAR;
  - a 40 m local scoring domain (ASSUMPTION);
  - all species at equal trunk size class (TERCERA, else SEGONA for 9 of 30 species).
- **Palette traits at equal trunk size class (TERCERA, else SEGONA)**, crown diameter m / LAI proxy / size class (`web/public/data/porta-barcelona/meta.json`, palette):
  - Firmiana simplex 7.55 / 3.22 / medium, cap headroom 423 = floor(0.15 × 2,825 Porta trees), none present today (Porta-local cap, `layout.py`; used in full by the balanced layout);
  - Gleditsia 8.87 / 2.58 / large;
  - Celtis australis 8.20 / 3.59 / large, cap headroom 127 = 423 − 296 Celtis already in Porta;
  - Melia 8.14 / 2.98 / medium;
  - Koelreuteria 6.77 / 2.49 / medium;
  - Grevillea 8.21 / 2.98 / large, evergreen;
  - Platanus (today) 8.69 / 2.81.
- **Heat proxy vs Ladybug, absolute UTCI** (`notes/methodology.md` §5b, 2–3 Nov). These are the 7-species pre-fix layouts: TO UPDATE.
  - All of Porta's plane streets, 21,352 points: S4 − S0 = −0.04 °C with opaque crowns, −0.11 °C with porous crowns (TMYx 2011–2025: −0.03 / −0.10 °C).
  - Python chain vs Grasshopper: bias −0.01 °C, r = 0.999.
  - Honeybee Tier 2 on Pg Andreu Nin: +0.06 opaque / −0.15 °C porous.
- **Routing vs RESCCUE** (`study/guide.md` l.373): AUC 0.52 overall. The top 0.5% of open ground by upstream area is wet in 58–80% of cases (1.7–2.6× random).
- **Interception calibration** (`notes/methodology.md` §4b):
  - 16 urban Tilia cordata / Acer platanoides, Apr–Sep 2021, 51 events ≥ 1 mm;
  - s = 1.75 mm per unit LAI (lime 1.85, maple 1.60);
  - event RMSE 0.9–3.2 mm.
  - Sensitivity at s = 0.86 and 0.83: the layout ranking holds, and every difference is < 1%.
- **Δmin derivation** (`notes/decisions/runoff_metric_sensitivity.md` l.85): 1 mm of interception error over 10.40 ha of S0 crowns = 104 m³ of interception = 102 m³ of runoff at T2-60. The minimum event RMSE 0.89 mm → 91 m³.
- **City LP with local ceiling** (`citylp_local_summary.csv`, 7-species palette, rerun 25 Nov after the fix), Porta + 27 barris, medians:
  - city LP 89.8% summer shade vs S1a 80.4% and the per-barri tool 86.3%;
  - the city LP beats S1a in 28 of 28;
  - city LP − per-barri local cap +1.5 pts;
  - Porta 100.3%.
- **Pollen is a range, not a value** (`cobenefits_porta*.csv`, pollen_load_pct_S0 = lower bound with unscored species at 0; pollen_max_pct_S0 = upper bound at the index maximum; pollen_coverage_pct = share of new trees with a score). Of today's pollen load:
  - S1a 6.6–62.2% (52.0% scored);
  - S1b 8.5–45.2% (63.2%);
  - method 5.4–106.5% (35.4%);
  - method with floor 9.4: 6.7–93.0% (43.5%).
  - Section 4 above gives only the lower bound. Do not quote it alone.
- **S1b on the 513 S1c positions** (`..._replporta_plan_planes.csv`): 353,978 m²·h = 98.3% of S0, the same as S1c's 98.2%.
- **Medium-class palette species by LAI proxy** (meta.json): Firmiana 3.22 is the highest of 12; its crown, 7.55 m, ranks 5th of 12 (Melia 8.14, Quercus ilex 8.06, Styphnolobium 7.84, Cercis 7.64 are wider; fact-check 26 Nov).
