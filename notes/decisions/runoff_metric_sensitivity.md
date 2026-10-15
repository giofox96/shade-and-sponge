# Can design-storm runoff tell street-tree species palettes apart? An exploratory bracket (issue #2)

Status: **Exploratory bracket, not a result. Decision (user, 14 Oct, provisional): "not resolved by the model" is accepted as a valid outcome for the runoff part of H1, with Δmin as in §10; the rest stays pending.** Nothing here changes `topic_decision.md` (PS/RQ/H), `methodology.md` or `scripts/runoff_model.py`; CLAUDE.md still says the methodology is not DEFINED. (Issue #42, 15 Oct, changed only where `runoff_model.py` reads Styphnolobium's crown and LAI, via `shade_sponge/site.py`, and regenerated `runoff_scenarios.csv`.) Written 12 Oct 2026 from `scripts/explore_runoff_sensitivity.py` (run it to reproduce every number below; it reads repo CSVs only). Sources are matrix ids in `notes/lit/literature_matrix.csv` (all read in full text per the matrix): #1 Anys & Weiler 2024, #3 Xiao & McPherson 2016. §13 also cites #5 (Yang et al. 2019) and one web page (Diputació de Barcelona, Verd urbà, https://verd-urba.diba.cat/print/318, read 14 Oct 2026; recorded in `notes/lit/species_canopy_params.csv`). **TR-55 CN values were not re-verified here (🟡)**.

> **Update 14 Oct (issue #37): *Styphnolobium japonicum* added as a seventh candidate (user decision), all tables re-run.** Its crown (8.85 m) and LAI proxy (3.32) are medians of only 5 LiDAR trees on one street, so every Styphnolobium number is an estimate. With mature crowns it is the only candidate that beats today's planes (aggregate −75.6 m³, grid −21.5 m³ at T2-60) and it becomes the "best" palette. This changes two conclusions: the palette spread is now above the s and LAI spreads (§7), and best vs S1 rises from 78 to 185 m³ at the central parameters but at s 0.86 / LAI low it ties with Δmin (91.0 vs 90.6-91.6 m³ depending on how Δmin is rounded; §8, §10). The aggregate overstates Styphnolobium's gain 3.5× against the grid (§5), and S1 is still not run on the grid, so the H1 outcome is not settled. **Bracket of Styphnolobium inputs (§13): replacing the n = 5 medians by sourced values, alone or mixed with one LiDAR value, Styphnolobium ranks first or fourth and best vs S1 stays below Δmin in the worst s/LAI case (38-42 m³ with both values sourced, 62-66 m³ mixed). The runoff part of H1 is therefore not resolved for any input in the bracket; only the n = 5 medians reach the 91 m³ tie.** **Update 15 Oct (issue #42): a LiDAR sample of 607 Styphnolobium on 26 streets outside Porta gives crown 6.43 m / LAI 2.28, or 5.32 m / 2.12 without possibly merged crowns. The tool and every table below (§3-§11) now use 5.32 m / 2.12 (user decision). With these Styphnolobium ranks 5th of 8 palettes in the aggregate and 4th of 7 in the grid, adds runoff against today's planes (grid +92.5 m³, +0.52% at T2-60), Melia is the best palette again in the aggregate (Jacaranda in the grid, §5), best vs S1 is 78 m³ (worst case 38.5 m³), and H1 (runoff part) is not resolved. The 14 Oct figures quoted in this box are superseded.**

## 1. Question

Is the design-storm runoff volume (f2 in `methodology.md` §6) able to tell apart the replacement palettes for the 809 Porta plane positions, given how uncertain the interception inputs are? "Tell apart" is tested by comparing the spread between palettes with the spread caused by uncertain parameters (s, LAI, crown size) and with a minimum meaningful difference.

## 2. Method in one paragraph

Aggregate arithmetic, same buckets as the grid model (`runoff_model.py` lines 87-104): per tree, I = min(P, s·LAI) over the crown disk; canopy storage volume = Σ area × I; runoff reduction = Σ area × (Q98(P) − Q98(P − I)) with SCS-CN. Output: `databases/barcelona/runoff_sensitivity_palettes.csv` (16,368 rows) and `runoff_sensitivity_spread.csv`. P = 1-80 mm in 1 mm steps plus the eight PDISBA depths (design intensity × d, `pdisba_idf_city.csv`): T1/T2/T5/T10 at 20 min = 13.7 / 21.2 / 31.5 / 39.2 mm; at 60 min = 19.6 / 31.9 / 48.9 / 62.5 mm. The grid model's own storms are T1-60, T2-60, T10-60, T2-20.

## 3. Assumptions (each sourced or ASSUMPTION)

| Input | Value | Source / status |
|---|---|---|
| Trees | 2,600 LiDAR crowns with flag ok; 809 are planes (`is_plane`) | `exchange/to_gh/porta_trees_lidar.csv` |
| Crown disk | π/4 · D² of the LiDAR crown diameter | as `runoff_model.py` |
| s, low / mid / high | 0.86 / 1.75 / 2.2 mm per unit LAI | 0.86 = Xiao & McPherson 2016 mean surface storage (#3, methodology §3; defined per unit leaf+stem surface area, applied here per unit LAI: ASSUMPTION); 1.75 = pooled median calibrated on Anys & Weiler 2024 (#1; IQR about 1.45-1.92); **2.2 = upper sensitivity value taken from `runoff_model.py` line 154, no source** (ASSUMPTION) |
| Evaporation | 0.86 = "surface storage only"; 1.75 = "effective storage including event evaporation". No Gash E/R term is added on top of 1.75 | methodology §4b (backlog step 5); the `runoff_model.py` docstring line 8 says evaporation is "ignored", which contradicts §4b (flagged, not edited) |
| LAI low | LiDAR proxy as measured (street median 2.28; seven candidates 2.00-2.91; Styphnolobium 2.12 from the city-wide sample, n = 367) | `porta_species_lidar_summary.csv`; Styphnolobium from `styphnolobium_lidar_summary.csv` (no_merge_flag), applied by `shade_sponge/site.py` `species_lidar()` |
| LAI high | proxy × 1.56 (= Freiburg median 3.56 / Porta median 2.28) | **ASSUMPTION**: constant under-reading ratio; Freiburg trees are *Tilia*/*Acer* with TLS LAI (#1), not Porta species |
| Crown, mature | species median crown diameter (4.55 / 8.43 / 8.01 / 7.33 / 3.09 / 4.28 / 5.32 m for Celtis, Melia, Tipuana, Jacaranda, Pyrus, Brachychiton, Styphnolobium; the last from the city-wide sample, n = 367, 15 Oct) | as LAI low |
| Crown, young | 3.0 m (v1) or on-site median 5.92 m (all 2,600 crowns) | 3.0 m is an ASSUMPTION in `runoff_model.py` line 32; 5.92 m is the data median, used only as a spread bracket |
| CN | 98 for every crown, i.e. all crowns over sealed open space | ASSUMPTION (TR-55 impervious, 🟡 not re-verified). The grid instead has roofs 29% / sealed 52% / pervious 19% (methodology §4b), CN 74 on pervious, roof crowns zeroed, max storage on overlaps |
| Palettes | S0 = trees as measured. S1 = the 809 planes split by the Porta shares of the seven candidates (Celtis .105, Melia .059, Tipuana .049, Jacaranda .051, Pyrus .052, Brachychiton .036, Styphnolobium .002, renormalised), expected values. Best / worst = all 809 planes at the candidate with the highest / lowest crown area × LAI (mature: Melia / Pyrus; young 3 m: Jacaranda / Celtis). Single species mature / young as in v1 | `porta_species.csv`; best and worst are therefore identical to a single-species row by construction |
| Background canopy, land-cover split | not modelled; only differences between palettes are compared | design choice of this bracket |

## 4. Table summary (T2-60, P = 31.9 mm; extra runoff vs S0 in m³, + = more runoff than today's planes)

Mature crowns, from `runoff_sensitivity_palettes.csv` (storm = T2-60min). Rows: palette; columns: LAI case and s.

| Palette | LAI low, s 0.86 | LAI low, s 1.75 | LAI low, s 2.2 | LAI high, s 0.86 | LAI high, s 1.75 | LAI high, s 2.2 |
|---|---|---|---|---|---|---|
| single Melia (= best) | 16 | 32 | 40 | 25 | 50 | 62 |
| single Jacaranda | 18 | 37 | 46 | 28 | 57 | 72 |
| single Tipuana | 26 | 53 | 67 | 41 | 83 | 104 |
| S1 (mix) | 54 | 110 | 139 | 85 | 172 | 216 |
| single Styphnolobium (city-wide crown and LAI) | 70 | 141 | 177 | 109 | 220 | 276 |
| single Celtis | 79 | 161 | 203 | 124 | 252 | 316 |
| single Brachychiton | 80 | 162 | 204 | 124 | 252 | 317 |
| single Pyrus (= worst) | 91 | 185 | 232 | 142 | 288 | 361 |

Young crowns (3 m): all palettes fall in a narrow band, 178-187 m³ at LAI low, s 1.75 (S1 184.6, best Jacaranda 178, worst Celtis 187), i.e. species barely matter when every crown is 3 m. With the on-site median crown of 5.92 m the best / worst are 96 / 130 m³. Reference: today's street trees (S0) cut T2-60 runoff by 446 m³ in this aggregate (LAI low, s 1.75), 220-872 m³ across the s and LAI cases (220 at s 0.86 / LAI low, 872 at s 2.2 / LAI high). Other storms for every cell: the CSV (T1-60: S1 106, best 31, worst 178; T10-60: S1 112, best 33, worst 188, LAI low, s 1.75, mature).

As a share of the grid's S0 runoff (17,649.57 m³ at T2-60): S1 +0.62%, best +0.18%, worst +1.05% (central parameters). The grid's own range for single-species mature replacements is +0.17% (Jacaranda) to +0.69% (Pyrus); Styphnolobium +0.52% (`runoff_scenarios.csv`, regenerated 15 Oct). No candidate beats today's planes.

## 5. Gap to the grid model (important caveat)

- Interception volume: the per-tree file sums to **456.9 m³** (reproduced exactly by the script); the grid gives a street-tree share of 817.51 − 412.22 = **405.3 m³** (ratio 0.89), because it masks roofs, takes the maximum on overlapping crowns and holds the background fixed.
- Runoff reduction by today's trees (aggregate / grid): T1-60 429.5 / 303.7 (×1.41), T2-60 446.0 / 333.2 (×1.34), T10-60 453.9 / 365.2 (×1.24), T2-20 433.3 / 308.2 (×1.41).
- Palette deltas vs S0 at T2-60 (aggregate / grid): Celtis 161.5 / 106.2, Melia 32.0 / 39.4, Tipuana 53.1 / 48.2, Jacaranda 36.8 / 29.6, Pyrus 184.9 / 122.1, Brachychiton 162.1 / 106.2, Styphnolobium 141.3 / 92.5. The aggregate **overstates the large-to-small replacements by about 1.5×** and gets the small-crown ones within about ±25%. **The order of Melia and Jacaranda swaps** (aggregate: Melia best; grid: Jacaranda best); they differ by 5 m³ (aggregate) and 10 m³ (grid), a near-tie. Cause of the overstatement is probably the overlap and roof masking of large plane crowns in the grid (not tested). Styphnolobium (5.32 m crowns) is overstated 1.5×, like the other large-to-small replacements. (With the n = 5 Porta values of 14 Oct, −75.6 vs −21.5 m³, the overstatement was 3.5×.) Use the aggregate only for bracketing and ranking trends, not for absolute volumes.

## 6. Finding 1: saturation (verified from the data; backlog corrected where needed)

- **Confirmed:** `interception_m3` = 817.51 at T1-60, T2-60, T10-60 and T2-20 (`runoff_scenarios.csv`, S0), and the per-tree file is 456.9 m³ at all four storms. Largest per-tree S at s 1.75 with the LiDAR proxy = 1.75 × 7.82 = 13.7 mm < 19.6 mm (smallest modelled storm). Candidate saturation depths (s 1.75 × median LAI): Celtis 3.50, Pyrus 3.64, Tipuana 3.85, Brachychiton 3.90, Melia 3.95, Jacaranda 5.09, Styphnolobium 3.71 mm. Per-tree range 1.5-13.7 mm.
- **Correction 1:** the claim holds for the four modelled storms with the LiDAR proxy and s ≤ 2.2 (largest S 17.2 mm). It does not hold in the LAI-high case: with LAI × 1.56, 11 trees (s 1.75) or 20 trees (s 2.2) of 2,600 have S > 19.6 mm. These are a negligible share of crown area, so the conclusion stands. T1-20 (13.7 mm, in the PDISBA table but not in the grid storms) equals the largest per-tree S at s 1.75 (13.69 mm) to within 0.01 mm.
- **Correction 2:** "the palette ranking is identical at every T" is true for the top of the order only. In the grid (`runoff_scenarios.csv`) the mature replacements (Jacaranda, Melia, Tipuana, Styphnolobium, then Celtis/Brachychiton, then Pyrus) keep their order at all four storms, but Celtis and Brachychiton (a 0.01 m³ near-tie at T1-60) swap at T2-20, and Tipuana-young / Pyrus-mature swap between T1-60 and T2-60. The aggregate ranking of the seven candidates plus S1 at the centre parameters is constant for P ≥ 8 mm. In the grid, R_Styphnolobium_mature ranks fourth at all four storms (+0.89 / +0.52 / +0.26 / +0.81% at T1-60 / T2-60 / T10-60 / T2-20), after Jacaranda, Melia and Tipuana.
- **Confirmed numbers:** R_Celtis_mature vs S0 = +94.8 / +106.2 / +119.4 m³ at T1/T2/T10 (60 min). In the aggregate the absolute benefit of today's trees rises only from 429.5 to 453.9 m³ between T1-60 and T10-60, because dQ/dPeff goes from 0.95 to 0.99.
- **Meaning:** above about 7-10 mm, f2 differences between palettes are the canopy storage volume Σ area × s × LAI times a slope of 0.95-0.99. The aggregate runoff reduction is 98% of the storage volume at T2-60 (446.0 / 456.9). The storm return period adds no information on palettes; f2 at T2 is a restatement of crown area × s × LAI. H3 (benefit shrinks with T) holds in percentage terms only because the same volume is divided by a growing total (grid: −3.16% / −1.85% / −0.90% at T1/T2/T10, `tree_effect_vs_none_pct`). In m³ the benefit grows slightly. This follows from the model structure and is not independent evidence for H3 (methodology §4b and slide 9 of `slides/outline_20oct.md` present it as such: flagged).
- **Saturation is a model feature:** a bucket with no drying during the storm. The Freiburg calibration (#1) fits S per tree at 4.27-10.86 mm (median 6.04), not 0.6-1.8 mm; with LAI high and s 1.75, the median Porta tree has S = 1.75 × 1.56 × 2.28 = 6.2 mm, consistent with that. Because s was fitted against TLS LAI and then applied to the lower LiDAR proxy, "LAI low with s 1.75" is probably an underestimate, and **"LAI high with s 1.75" is the internally consistent pairing** (to be confirmed by the user; v1 uses LAI low).

## 7. Finding 2: spread between palettes vs spread from parameters (m³; from `runoff_sensitivity_spread.csv`)

Palette spread = max − min of the extra runoff over the 10 mature palettes (S1, best, worst, 7 singles) at s 1.75, LAI low. Parameter spread = range of the same quantity for one factor varied at a time (S1; maximum over the 10 palettes in brackets). The crown factor mixes an uncertainty with a design variable (mature vs young).

| P (mm) | palette | s 0.86-2.2 | LAI low-high | crown mature / 3 m / 5.9 m |
|---|---|---|---|---|
| 2 | 5.9 | 0.0 (0.0) | 0.0 (0.0) | 2.8 (6.0) |
| 5 | 67.2 | 11.3 (20.5) | 1.2 (1.4) | 31.6 (67.7) |
| 10 | 127.2 | 60.3 (103.7) | 31.9 (58.6) | 61.5 (126.9) |
| 13.7 (T1-20) | 139.5 | 73.2 (123.6) | 49.5 (84.6) | 67.6 (139.0) |
| 19.6 (T1-60) | 147.5 | 80.2 (134.7) | 57.6 (97.0) | 71.6 (147.0) |
| 31.9 (T2-60) | 152.9 | 84.2 (141.2) | 61.5 (103.1) | 74.3 (152.3) |
| 62.5 (T10-60) | 155.5 | 85.9 (144.0) | 63.0 (105.5) | 75.5 (155.0) |

- At design depths (≥ 13.7 mm) the palette spread (140-156 m³) is about 1.8-1.9 times the s spread for the S1 palette (73-86) but only about 1.1 times the worst-case s spread over palettes (124-144), and about equal to the worst-case crown spread (139-155). It stays larger than the LAI spread (about 1.5-1.6 times the maximum over palettes, 85-106). The palette spread is therefore **comparable to the s uncertainty**, as in the 12 Oct six-species run (140-156 m³). The 14 Oct result "above the uncertainty" (233-265 m³) rested on the n = 5 Styphnolobium values and no longer holds with the city-wide sample.
- Below saturation (P ≈ 2-6 mm) species effects exist (spread 6-89 m³), but the s spread is small there (S1 0-22 m³, maximum over palettes 0-41 m³): this is where palettes are most distinguishable relative to parameters, and where the rain is frequent.
- **Ranking:** at the eight PDISBA depths (all ≥ 13.7 mm) and at P ≥ 12 mm, the ranking of the seven singles plus S1 is the same for every s and LAI case (mature crowns; `n_distinct_rankings_s_lai_mature` = 1). At the centre parameters Melia ranks first at every P ≥ 2 mm; at P = 2-7 mm Tipuana is 2nd and Jacaranda 3rd, and from P = 8 mm they swap; S1 is 4th and Styphnolobium 5th throughout. Between P = 5 and 11 mm the ranking also depends on s and LAI. The ranking does change between mature and young crowns (young: ordered by LAI, Jacaranda best, Celtis worst, all within 9 m³ at T2-60).

## 8. Minimum meaningful difference (candidate, fixed before the optimiser runs)

Source: event RMSE of the interception calibration, 0.89 / 1.84 / 3.24 mm (min / median / max over the 16 trees, `interception_calibration.csv`; Anys & Weiler 2024, #1). Converted: 1 mm of interception error over all S0 street crowns (103,966 m² = 10.40 ha) = 104 m³ of interception = 102 m³ of runoff at T2-60 (slope 0.98). So the RMSE corresponds to **91 m³ (min), 187 m³ (median), 330 m³ (max) at T2-60**, i.e. 0.5%, 1.1%, 1.9% of S0 runoff (17,649.57 m³). This treats the error as systematic over all trees (an ASSUMPTION; independent errors would average down but the calibration cannot tell which). Against this:
- grid spread between mature single-species replacements at T2-60 = 92.5 m³ (Pyrus − Jacaranda; Styphnolobium, now fourth, does not widen it; 143.5 m³ with the 14 Oct n = 5 values); only Celtis, Brachychiton, Pyrus and Styphnolobium (92.5 m³) differ from S0 by more than 91 m³, none by more than 187 m³;
- best vs S1 (aggregate, mature, T2-60; best = Melia) = 110.3 − 32.0 = 78.3 m³, **below** the 91 m³ threshold. Across the s and LAI cases it is 38.5 / 78.3 / 98.4 m³ (LAI low; s 0.86 / 1.75 / 2.2) and 60.1 / 122.1 / 153.3 m³ (LAI high), so the worst case is well below Δmin (90.6 or 91.6 m³) and the choice between the two Δmin values no longer matters. With young 3 m crowns it is 6.5 m³. (14 Oct, with the n = 5 Styphnolobium values: 184.7 m³ central, 90.99 m³ worst case, a tie.) These are aggregate values; S1 has not been run on the grid.

## 9. Metric options

| Option | Distinguishes palettes? | Data needed | Cost |
|---|---|---|---|
| A. Design-storm runoff volume (current f2, T2-60) | Yes through crown area × s × LAI only; the storm adds nothing; effect about +0.2 to +1.0% of runoff, near the RMSE bracket | in repo | none |
| B. Canopy storage volume Σ area × s × LAI | Same ranking as A for P ≥ 7 mm (ratio 0.98); no CN, no storm | in repo | trivial, cheapest in an optimiser loop |
| C. Volume intercepted or runoff in frequent storms below saturation (P about 2-10 mm) | Yes, species and s matter and the ranking changes between 7 and 8 mm | needs the frequency of those storms: not in the repo (gauge data, B3; not verified 🟡) | needs rainfall record; weighting is a new choice |
| D. Seasonal interception (leaf-on, event series) | Likely best, includes phenology | gauge series (B3), leaf-on calendar `season.py` | largest; beyond 18 Dec unless the gauge data are already available |

## 10. Draft wording, all **pending user decision** (not edited into `topic_decision.md`)

Minimum meaningful difference Δmin, to be fixed before any optimiser run: **0.9 mm of interception over the street crown area (91 m³, 0.5% of T2-60 runoff)** as the lowest bar; 1.84 mm (187 m³, 1.1%) as the stricter bar.
- **H1 (runoff part), draft:** for the same number and size class of trees, the best trait-based layout reduces T2-60 runoff by more than Δmin relative to the like-for-like palette S1, at s = 0.86, 1.75 and 2.2 and for both LAI cases; if the difference is below Δmin at any of them the runoff part of H1 is reported as **not resolved by the model** (neither supported nor rejected). Current exploratory value (aggregate, 15 Oct, Styphnolobium from the city-wide sample): 78.3 m³ with mature crowns at the central parameters and 38.5 m³ at s 0.86 / LAI low, both below Δmin, so **not resolved**; 6.5 m³ with 3 m young crowns. With the 14 Oct n = 5 values it was 184.7 m³ (worst case 90.99 m³, a tie); the bracket of §13 (crown ≤ 8.85 m, LAI ≤ 3.32) gives 38-66 m³ in the worst case: not resolved in every case.
- **H3, draft:** the street-tree effect expressed as % of Porta runoff is smaller at T10 than at T1 by at least a factor 2 (grid: 0.90% vs 3.16%, factor 3.5), and the absolute benefit in m³ changes by less than Δmin between T1 and T10 (aggregate: +24 m³; grid: +61 m³; both below 91 m³). State that the % decline follows from storage saturation, so H3 tests the bucket model's consistency, not an independent finding.

**Flags on the tutor's order:** H1 and H3 are hypotheses. Making them falsifiable (this section) changes their wording, and a "not resolved" outcome would soften H1's claim of improving runoff; that needs your decision. The PS and RQ (which species and positions jointly reduce heat and runoff) are not changed by this memo. If runoff cannot tell palettes apart, the heat objective carries the species choice and runoff becomes a constraint or a check; that is a methodology option (§6), not a change to the RQ, but it should be raised at the 20 Oct tutor session.

## 11. Recommended default

Keep f2 as the T2-60 design-storm volume for reporting, but use canopy storage volume (option B) inside the optimiser, and add the below-saturation metric (option C) only if gauge data are obtained. Report palette differences against the Δmin bracket, with "not resolved" as a legitimate outcome. Re-run the table with LAI high / s 1.75 as the main pairing. Treat the aggregate as a bracket: it overstates the grid by 1.2-1.5× (Melia 0.8×). Run S1 and the best palette on the grid before reporting H1.

## 13. Styphnolobium input bracket (14 Oct)

Written 14 Oct, before the city-wide sample (§13 last bullets; the tool now uses 5.32 m / 2.12). Styphnolobium's Porta LiDAR medians (crown 8.85 m, LAI proxy 3.32) come from 5 trees on one street (C/ Pollença), with crowns from 1.95 to 9.93 m; `build_trait_table.py` leaves the LiDAR columns empty for a species with fewer than 10 LiDAR trees. The script therefore re-runs the T2-60 aggregate with a sourced bracket (`runoff_sensitivity_styphnolobium.csv`):
- crown 6 or 8 m: the sheet's crown class "Ampla (de 6 a 8 m de diàmetre)" (wide, 6 to 8 m; Diputació de Barcelona, Verd urbà, Acàcia del Japó sheet). It is a generic class used across the site's sheets, not a measured maximum, and the page does not say "mature". Plus the LiDAR 8.85 m;
- LAI 2.61: whole-canopy TLS LAI of one Seoul tree (Yang et al. 2019, #5), used as-is on the LiDAR-proxy scale (ASSUMPTION; converting with the 1.56 TLS/proxy factor of §3 would lower it further), plus the LiDAR 3.32. In the LAI-high cases the script multiplies 2.61 by 1.56 (about 4.07), above the measured TLS value; this inflates the best-case column for the 2.61 rows.

Mature crowns, over the six s × LAI cases (m³ of extra runoff vs S0; + = more runoff than today's planes):

| Crown (m) | LAI | Styphnolobium rank of 7 | Styphnolobium vs S0 | Best single | Best vs S1, worst case / central / best case |
|---|---|---|---|---|---|
| 6 | 2.61 | 4 | +51 to +204 | Melia | 38 / 78 / 153 |
| 6 | 3.32 | 4 | +38 to +151 | Melia | 38 / 78 / 153 |
| 8 | 2.61 | 1 | +12 to +49 | Styphnolobium | 42 / 85 / 165 |
| 8 | 3.32 | 1 | −46 to −12 | Styphnolobium | 66 / 133 / 260 |
| 8.85 (Porta LiDAR, n = 5) | 2.61 | 1 | −30 to −8 | Styphnolobium | 61 / 125 / 244 |
| 8.85 (Porta LiDAR, n = 5) | 3.32 | 1 | −147 to −37 | Styphnolobium | 91 / 185 / 360 |
| 6.43 (city LiDAR, all ok, n = 607) | 2.28 | 4 | +51 to +203 | Melia | 38 / 78 / 153 |
| 5.32 (city LiDAR, no merge flag, n = 367) | 2.12 | 4 | +70 to +276 | Melia | 39 / 78 / 153 |

Central = s 1.75, LAI low; worst case = s 0.86, LAI low; best case = s 2.2, LAI high.

- **"Best palette" is not robust.** A crown sweep shows that Styphnolobium overtakes Melia from a crown of 7.85 m (LAI 2.61) or 6.97 m (LAI 3.32), the same in all six s × LAI cases. At 6 m it ranks 4th and Melia leads, as in the six-species run.
- **"Beats today's planes" is not robust either.** In all six cases it does so only from a crown of 8.54 m (LAI 2.61) or 7.58 m (LAI 3.32). Within the bracket that means an 8 m crown with LAI 3.32, or the 8.85 m crown; at 6 m it adds runoff with either LAI, and at 8 m with LAI 2.61.
- **H1, runoff part.** Under the all-cases rule (§10), best vs S1 stays below Δmin (90.6-91.6 m³) in the worst s/LAI case for every bracket row except the n = 5 medians, which tie (91.0). Result: **not resolved for every input in the bracket**. Outside it, best vs S1 clears 91.6 m³ in all six cases from a crown of 8.87 m (LAI 3.32) or 10.01 m (LAI 2.61). The largest single LiDAR crown, 9.93 m, with LAI 3.32 gives a worst case of 126.8 m³ (not stored in the CSV). Yang's central-section LAI 5.11 with an 8 m crown gives 126.4 m³ (not stored in the CSV; both from the same tally functions, worst case s 0.86, LAI low). Larger inputs could therefore support H1. With Δmin = 90.6 m³ (unrounded), the n = 5 medians themselves pass by 0.4 m³.
- **Young 3 m crowns.** Styphnolobium ranks 1st with LAI 3.32 and 2nd (after Jacaranda) with 2.61; best vs S1 is 3-20 m³, not resolved.
- **City-wide LiDAR sample (15 Oct, issue #42).** `scripts/bcn_lidar_species_sample.py` (same method as Porta) on one 1 km ICGC tile (429586) gives 631 inventory Styphnolobium on 26 streets in 6 neighbourhoods (El Carmel, Horta, La Font d'en Fargues, La Teixonera, La Clota, La Vall d'Hebron), none in Porta; 607 are usable (`databases/barcelona/styphnolobium_lidar_summary.csv`). Medians: crown 6.43 m (IQR 3.08), LAI proxy 2.28 (IQR 0.90) for all 607; 40% have a crown flagged as possibly merged with a neighbour, and without them (n = 367, 25 streets) crown 5.32 m (IQR 2.58), LAI 2.12 (IQR 0.85). By size class the crown median is 3.61 m (PRIMERA, n = 66), 6.23 m (SEGONA, 386), 7.89 m (TERCERA, 148), 10.66 m (EXEMPLAR, 7). The 5 Porta trees (8.85 m, 3.32) sit in the upper part of this distribution. With either city pair Styphnolobium ranks 4th of 7 in all six s × LAI cases (Melia leads), adds runoff against today's planes, and best vs S1 in the worst case is 38-39 m³: **H1 (runoff part) not resolved**. Young 3 m crowns: rank 2 (6.43 m pair) or 5 (5.32 m pair), Jacaranda leads, best vs S1 3-13 m³. Limits: one tile, so 6 neighbourhoods in the north-east of the city, not a city-wide spread; aggregate model only.
- **What would settle it.** The city sample above answers the crown/LAI question for the aggregate; the tool now uses the no_merge_flag pair (user decision, 15 Oct; `shade_sponge/site.py` CITY_LIDAR), and §3-§11 are re-run with it. Still open: the grid run of S1 and the best palette.

## 12. Gaps and unverified items

- 🟡 CN 98 / 74 not re-checked against TR-55 here; s = 2.2 has no source; LAI-high factor is an assumption.
- S1 and best/worst were not run on the grid model (`runoff_model.py` may not be edited here), so aggregate-to-grid ratios are known only for single-species rows.
- Backlog statements corrected by this run: Freiburg TLS LAI is 1.39-4.89 (median 3.56; 2.55-4.89 without TUF_T1), not 2.6-4.9; the six original candidates' LAI medians are 2.00-2.91, not 1.9-2.9 (Styphnolobium 3.32 with the n = 5 Porta values; 2.12 with the city-wide sample); the "identical ranking at every T" statement is only true for the top order (§6).
- No rainfall frequency data in the repo (option C, D).

## One question for you

Do you accept "not resolved by the model" as a valid outcome for the runoff part of H1 with Δmin = 0.9 mm of interception (91 m³ at T2-60), or do you want to keep H1 as is and instead make runoff a constraint with heat as the species-deciding objective? (pending your decision)
