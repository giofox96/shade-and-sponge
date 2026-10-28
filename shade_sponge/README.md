# shade_sponge: tool core (v0, 8 Oct 2026)

Suggests **which species go at which street-tree position**, scoring each layout on a **heat proxy** (effective shade on sunlit open ground) and **event runoff** (total, and the part that reaches flood hotspots). One Python core serves both front-ends: Grasshopper (via `exchange/`, later Hops) and a web app (later).

## Run
```bash
python -m shade_sponge                                  # city palette (7 species)
python -m shade_sponge porta --palette=barcelona --diversity=10   # Barcelona shortlist, diversity floor on
```
Run from the project root with the conda env `shade-and-sponge` (`<env>/Library/bin` on PATH). The first run builds `cache/site_porta.npz` (~15 s); a full run takes ~4 min. Figure: `PYTHONPATH=. python scripts/plot_tool_v0.py`.

## Pipeline
| Module | What it does | Key inputs / assumptions |
|---|---|---|
| `site.py` | Site bundle on a 1 m grid: domain, roofs, CN, DTM, building heights, background canopy, flood hotspots, routing results | Surfaces identical to runoff v1. Hotspot = Resilience Atlas index ≥ 40. **`CAPTURE_M` = 100 m (ASSUMPTION)**: runoff counts toward a hotspot only if its flow path reaches it within 100 m (stand-in for sewer inlets) |
| `topo.py` | Priority-Flood routing on DTM + buildings → water convergence (upstream open area) and flow distance to hotspots | No sewer, no inflow from outside the grid |
| `heat.py` | Sun position (NOAA equations), building shadows at 1.1 m, elliptical shadows of ellipsoid crowns; opacity f·(1 − exp(−0.5·LAI)) + (1 − f)·OP_BARE with f = leaf fraction of the month. Summer shade = benefit, winter shade = cost | Design days **15 July 12–17 h CEST and 15 January 10–15 h CET (ASSUMPTION**; the summer window is still to be aligned with the heat metric decided on 19 Oct: mean UTCI over 12–17 h standard time = 13–18 h CEST on a hot design day, `notes/decisions/heat_objective.md` §1). **OP_BARE = 0.35 (ASSUMPTION**, test 0.25–0.54): leafless crowns cut ~35% of sunlight (McPherson 1984; up to ~54% for London plane, Heisler 1982/84; both cited in Thayer & Maeda 1985). Proxy, **to calibrate against Ladybug UTCI** |
| `runoff.py` | Runoff v1 as functions: storage bucket s·LAI + SCS-CN | Reproduces `runoff_scenarios.csv` exactly (S0, T2-60, full leaf: 17,649.6 m³) |
| `season.py` | Leaf-on calendar: LAI(m) = LAI(LiDAR, 26 Sept) × (R_OFF + (1 − R_OFF)·f(m)); runoff = expected value over the storm months | f(m): `databases/traits/phenology_palette.csv` (sources per species; class-default months marked ASSUMPTION). Storm months: `databases/barcelona/storm_months.csv` (Esbrí et al. 2026, Fig. 4). **R_OFF = 0.5 (ASSUMPTION**, test 0.3–0.7; anchors Herbst et al. 2008, Xiao et al. 2000). Heat uses July leaves |
| `layout.py` | Palette, 15% cap, façade-clearance fit, per-position potentials, weighted-sum LP (HiGHS) over 3 objectives (summer shade ↑, winter shade ↓, hotspot runoff ↓; 15 weight sets), random baseline, Pareto | Species traits = median of each species' Porta trees (LiDAR 2021; Styphnolobium from a city-wide sample, `site.CITY_LIDAR`); same s per LAI for all species. Clearance: crown radius ≤ distance to nearest building (ASSUMPTION: no margin). Optional sizing rule `--size=exact|at_most` (2011 guide: sidewalk width → tree size class, `databases/barcelona/porta_sidewalk_width.csv`; unmeasured positions unfiltered, ASSUMPTION) and `--keep-meridiana` (Meridiana planes kept by the city, out of the decision set) |

Tutorial (how it works, how to use it, a demo script): `study/tool_tutorial.md`.

To add a site, write `build_<site>()` and `trees_<site>()` in `site.py` (same keys and columns).

## Outputs
- `databases/barcelona/tool_v0_summary.csv`: one row per layout (S0, S1 random × 10, S4 weight sets `S4_s<summer>_w<winter>_r<runoff>`), with shade_summer_m2h, shade_winter_m2h, runoff_m3, runoff_hot_m3, interception_m3, species counts and Pareto flag
- `exchange/to_gh/positions_tool_v0_<date>.csv`, `layouts_tool_v0_<date>.csv`: see `exchange/README.md`
- `notes/figures/tool_v0.png`

## Earlier runs (8 Oct, superseded; kept for the record)
**Run 1: two objectives, disk shadows, full leaf.** Numbers from that run, not reproducible from the current CSVs.
- Optimised vs random palette: +16% effective shade, +5% interception, −0.3% hotspot runoff (−0.2% total). The runoff gain is small, as street trees remove only ~2% of Porta's runoff (runoff v1).
- **No trade-off:** every weight gave almost the same layout (fill Tipuana, Melia and Jacaranda as far as the cap and space allow). Bigger, denser crowns win both objectives, so the front collapsed to a point (the H2 risk flagged in `notes/agent_backlog.md`).
- No replacement layout reached S0 (mature planes): −7% shade even when optimised.

**Run 2: leaf-on calendar added (two objectives, disk shadows).** It does not create the trade-off.
- 78% of intense storm days fall in May–Oct (Esbrí et al. 2026: 35 of 45 days), when every palette species is in full leaf. The season-weighted leaf factor in storms is 0.93 for the deciduous species (incl. Styphnolobium), 0.98 Jacaranda, 0.99 Tipuana and 1.00 Brachychiton (across R_OFF 0.3–0.7 and without Storm Gloria: deciduous 0.90–0.96, Jacaranda 0.98–0.99, Tipuana 0.99; `databases/barcelona/tool_v0_storm_leaf_factor.csv`). This part is still current (Jacaranda was 0.95 with the old leaf calendar).
- In that intermediate run (not saved), runoff-weighted layouts took a few more evergreen Brachychiton, the other species did not change, and both objectives moved < 0.1% across weights.
- So with the city palette, crown size and LAI decide both objectives; a trade-off needs a criterion where evergreen or big crowns cost something: **winter sun access**.

## Winter sun access (added 8 Oct): the first real trade-off
**Current run (20 Oct):** seven species (Styphnolobium added 14 Oct) and the photo-based leaf calendar adopted 15 Oct (Jacaranda f = 0.8 on the 15 Jan design day instead of 0, Tipuana f = 0.5 in February; `notes/decisions/leaf_state_inat.md`), now also with leaf calendars for Porta's kept trees of the shortlist species (about 92% of its LiDAR-measured non-plane trees; the other kept species, e.g. Morus alba, stay in full leaf, ASSUMPTION); in the 15 Oct run they were all in full leaf. Crown shadows are ellipses (longer in low sun); runoff is season-weighted, with full-leaf values in the `*_leafon` columns (runoff and interception). Season-weighted interception is 1.9–2.8% lower than at full leaf.
| Layout | Summer shade (m²·h) | Winter shade (m²·h, cost) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 196,218 | 2,682.3 |
| S1 random palette (mean of 10) | 286,479 | 190,015 | 2,698.7 |
| S4 summer only (1, 0, 0) | 332,224 | 205,396 | 2,690.8 |
| **S4 balanced (0.50, 0.25, 0.25)** | **332,342** | **200,750** | 2,688.9 |
| S4 winter-heavy (0, 0.50, 0.50) | 272,596 | 159,790 | 2,691.1 |

**What the kept-tree calendars changed (15 → 20 Oct):** every layout and every summer value is identical; winter shade fell by 27,090–28,005 m²·h in every layout (kept deciduous trees of those species are now bare in January), season-weighted interception by ~4 m³ and hotspot runoff rose by ~0.9 m³. The percentages below move slightly.
- **A small free gain first:** summer-only → balanced cuts winter shade by only 2.3% at the same summer shade, still by swapping ~90 Tipuana (fully leafed in January) for Jacaranda (80% leafed). It is not robust (see sensitivity). The balanced layout beats the random palette on summer shade (+16.0%) but casts more winter shade than it (+5.6%).
- **Then a real trade-off:** beyond the balanced layout, more winter sun costs summer shade (winter-heavy: −20.4% winter shade for −18.0% summer shade). The winter-heavy layout drops Tipuana (0) and most Jacaranda (35) for the winter-bare Pyrus (276, its cap), Styphnolobium (223), Melia (185) and Celtis (98). The front is not a point.
- **Placement follows the buildings, partly:** in the balanced layout the winter-bare Melia gets positions in sun 87% of winter hours, Jacaranda 62%, Tipuana 44%, evergreen Brachychiton 29% (positions file: `sun_share_winter`). But Melia already holds the sunniest streets in the summer-only layout (winter weight 0: 82% of winter hours, 98% of summer hours), so that is mostly summer sun. The winter-driven evidence is the winter-heavy layout: the winter-bare Pyrus gets positions in sun 78% of winter hours and Celtis 68%, the evergreen Brachychiton 31%. The winter-bare Styphnolobium (34% balanced, 36% winter-heavy) also sits in winter-shaded streets, so leaf habit does not explain all placements.
- Total runoff follows interception, i.e. crown size (17,706 m³ balanced vs 17,747 m³ winter-heavy). Hotspot runoff varies by only 0.5% across weights (2,688–2,703 m³). It mostly follows the runoff weight (Spearman −0.73 between runoff weight and hotspot runoff; lowest for runoff-only). In the 8 Oct run it did not (the winter-heavy layout was lowest), so the per-position water potential is still unverified (to check: crown overlap with kept trees, the box-filter approximation).

**Superseded (15 Oct; kept trees without leaf calendars):** S0 winter 224,223, balanced 227,943, winter-heavy 187,782 m²·h; free gain −2.1%; balanced vs random winter +4.7%; winter-heavy vs balanced −17.6% winter for −18.0% summer.

**Superseded (old calendar, 8 Oct; six species, Jacaranda bare Jan–Mar):** summer-only → balanced −9% winter shade (~100 Tipuana → Jacaranda) at equal summer shade; balanced vs random +14% summer, −3% winter; winter-heavy vs balanced −11% winter for −16% summer shade; placement Jacaranda 80%, Tipuana 51%, Brachychiton 29% of winter hours in sun.

## Sensitivity of the winter-sun result (re-run 20 Oct; random palettes re-drawn 26 Oct after the 24 Oct change to `random_layout`, which moved only the vs-random columns; `scripts/sensitivity_tool_v0.py`)
Base run plus 7 one-change variants: leafless opacity 0.25 / 0.54; Tipuana bare in Jan–Feb ('briefly deciduous' in winter: Santa Barbara Beautiful, Tree of the Month; search snippet only); Jacaranda half-leafed Jan–Mar; Jacaranda bare Jan–Mar (the old calendar, from the Valencia BBCH study); winter design day 21 Dec / 15 Feb. Each re-optimises summer-only, balanced and winter-heavy layouts against 3 random palettes. Results: `databases/barcelona/tool_v0_sensitivity.csv` (summary), `_raw.csv`. The base variant reproduces the main run exactly. Every variant's layouts and summer values are identical to the 15 Oct run; only winter shade moved, through the kept trees' leaf calendars.

| Claim | Range across variants | Verdict |
|---|---|---|
| Optimised (balanced) vs random palette, summer shade | +15.8 to +15.9% (main run vs 10 random: +16.0%) | **robust** |
| Balanced vs random palette, winter shade | −0.4 to +8.9% (−0.4% only with the old Jacaranda calendar) | no winter gain: about equal or worse |
| No-regret swap summer-only → balanced: winter shade at equal summer shade | −0.2 to −10.1% (base −2.3%; summer within ±0.1%) | sign holds, but **small** except with the old calendar |
| Trade-off beyond balanced: winter-heavy vs balanced | winter −14 to −23%, summer −17 to −20% | **robust** |
| Species of the balanced layout | Melia 256, Styphnolobium 67, Celtis 0 in every variant; Tipuana → Jacaranda swap (~90) in only 5 of 8 variants | swap **not robust** |
| Species of the winter-heavy layout | Pyrus 276 (cap) and Styphnolobium 213–245 in every variant, Tipuana 0–11; Melia 43–193, Jacaranda 28–188 | Pyrus + Styphnolobium robust |

- **The calendar, not the new species, shrank the swap:** with the old calendar in the same seven-species run (`jacaranda_bare_jan_mar`) the free gain is −10.1% (15 Oct: −8.7%; 8 Oct: −8.9%); with the photo-based calendar it is −2.3%.
- The swap needs Jacaranda to carry fewer leaves than Tipuana on the design day. With the photo-based calendar that holds only in January (0.8 vs 1), so the swap vanishes when Tipuana is bare in Jan–Feb, on 21 Dec (both fully leafed) and on 15 Feb (Jacaranda 0.7 vs Tipuana 0.5). The small gain left in those variants (−0.2 to −0.9%) comes from other species.
- Leafless opacity still scales it (−3.6% at 0.25, −0.4% at 0.54).

**Superseded (15 Oct; kept trees without leaf calendars):** free gain −0.2 to −8.7% (base −2.1%); balanced vs random winter −0.8 to +7.9%; winter-heavy vs balanced winter −12 to −19%, summer −17 to −20%.

**Superseded (old calendar, 8 Oct; 7 variants, six species):** free gain −2.2 to −11.6%; Jacaranda 278 and Tipuana 186 in the balanced layout of every variant; winter-heavy vs balanced winter −10 to −14%, summer −15 to −19%.

## Barcelona shortlist palette (9 Oct; re-run 20 Oct): `python -m shade_sponge porta --palette=barcelona`
- **Shortlist** (`scripts/species_shortlist.py` → `databases/barcelona/species_shortlist.csv`): street-tree species with ≥ 500 trees in Barcelona's inventory (140,404 street trees of 211 species, Open Data BCN; palms are inventoried separately, 4,772, and left out as a design choice), taken as established in the city's climate (ASSUMPTION). Excluded: Platanus (being replaced). None of the tree taxa of the Spanish invasive catalogue that apply in Catalonia (Ailanthus altissima, Acacia dealbata, A. melanoxylon, Myoporum laetum; MITECO table, 21 Oct 2025) reaches 500 street trees; they would be excluded. Flagged but kept (invasive behaviour reported, not legally listed): Robinia pseudoacacia and Ulmus pumila (riparian invasion in Spain: Cabra-Rivas, Castro-Díez & Saldaña 2015, Ecosistemas 24(1):18–28), Ligustrum lucidum (global review: Fernandez et al. 2020, Bot. Rev. 86:93–118). Result: **34 species**.
- **Crowns:** LiDAR on 3 ICGC tiles (one is Porta's own tile) chosen to cover ≥ 40 inventory trees per species away from tile edges (`scripts/bcn_lidar_species.py`, same method as Porta; flights 26 Sept 2021 and 1 June 2022, both leaf-on: `lidar_tiles_dates.csv`) → `species_lidar_summary.csv` (33–735 trees per species; Porta + tiles). The city species also get these city-wide medians in this run (e.g. Celtis crown 6.3 m vs 4.6 m in Porta), except Styphnolobium, which uses the same city-wide sample as the city palette in both runs (`site.CITY_LIDAR`, user decision 15 Oct: crown 5.3 m, LAI 2.12, instead of this table's 6.8 m and 3.21).
- **Leaf habit:** sourced for all 34 (BROT 2, Zaragoza species guide, UConn, NC State, UF/IFAS, ACT; `databases/traits/phenology_palette.csv`); months: class defaults for the new deciduous species, leaf-on all year for evergreens (both ASSUMPTION; Grevillea's spring leaf drop is ignored).

| Layout (Barcelona palette) | Summer shade (m²·h) | Winter shade (m²·h) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 196,218 | 2,682.3 |
| S1 random palette (mean of 10) | 278,536 | 188,713 | 2,699.6 |
| S4 summer only | 365,428 | 254,876 | 2,682.4 |
| **S4 balanced** | **362,500** | **208,828** | 2,682.4 |
| S4 winter-heavy | 272,457 | 155,655 | 2,683.7 |

Re-run 20 Oct with the photo-based leaf calendar and Styphnolobium's city-wide values; layouts shift only slightly from 9 Oct (2–43 of 832 positions change species; balanced 19; the dominant counts below are unchanged; 9 Oct: balanced 362,485 / 201,145 m²·h). The random layouts also differ, because Styphnolobium's smaller crown now fits more positions. With its city-wide values Styphnolobium drops out of the summer-only, balanced and winter-heavy layouts (9 Oct: 9, 14 and 18 trees; now 0; at most 9 in any weight set), and keeps only 4–5 trees in them with the diversity floor (9 Oct: 17–26).

- **Optimised replacements now match or exceed the mature planes on summer shade** (+0.9% balanced, +1.7% summer-only), which the city palette could not (−7.5%). Balanced vs city-palette balanced: +9.1% summer shade, +4.0% winter shade (more evergreen crown; 9 Oct: +16%, before Jacaranda was leafed in January in the city palette).
- **The trade-off is wider:** winter shade spans 143,000–255,000 m²·h across the 15 weight sets (city palette: 153,000–206,000). Summer-only → balanced: −18.1% winter shade for −0.8% summer shade (P. halepensis and some P. pinea → Ulmus pumila). Caveat: Ulmus pumila, the main species of the balanced layout, is coded winter-deciduous, but is reported semi-evergreen in warm climates (treelib.ca), which would shrink this gain.
- **Low diversity:** a few species dominate (balanced: Ulmus pumila 349 + Pinus pinea 346 = 84% of 832 positions; summer-only: Pinus pinea 422, at its cap, + P. halepensis 183; winter-heavy: the small-crowned Hibiscus syriacus 404, at its cap). The model scores only shade and interception: it ignores maintenance, roots and paving, allergenicity, the invasive flag on Ulmus pumila, and functional diversity. Two levers: the max share per species (web app slider) and the optional diversity floor (next section).

## Diversity floor (optional, added 12 Oct)
`--diversity=N` (web app: "Diversity floor" toggle) keeps at least N **effective species**, exp(Shannon H), among the replanted positions; off by default. The effective number of species is the diversity measure SylvCiT uses (Nicol et al. 2026). Shannon H is concave in the species counts, so the floor is linear: each species' term −p·ln p is replaced by the piecewise-linear interpolation through about 36 breakpoints (40 log-spaced counts, rounded; which lies below the curve, so the floor is conservative) and only the species counts are integer (`layout._entropy_chords`, `layout.assign`). The value of N is a designer choice, not a sourced threshold. Every replacement-layout row of the summary now has `eff_species`. Summary and exchange outputs carry a `_div<N>` suffix.

Barcelona shortlist, N = 10 (`databases/barcelona/tool_v0_summary_barcelona_div10.csv` vs `tool_v0_summary_barcelona.csv`):
| Layout | Effective species | Summer shade | Winter shade | Hotspot runoff | Interception |
|---|---|---|---|---|---|
| S4 summer only (1, 0, 0) | 4.9 → 10.0 | −2.0% | −3.0% | +0.1% | −1.6% |
| **S4 balanced (0.50, 0.25, 0.25)** | **4.1 → 10.0** | **−2.0%** | **−1.7%** | **+0.0%** | **−1.3%** |
| S4 (0, 0.50, 0.50) | 6.6 → 10.0 | −1.8% | +0.2% | +0.0% | −0.9% |
| S4 runoff only (0, 0, 1) | 4.4 → 10.0 | −2.2% | −1.0% | +0.0% | −1.4% |

Re-run 20 Oct (photo-based leaf calendar, Styphnolobium city-wide values); effective species as rounded in the summary CSVs.

- In the balanced layout, Ulmus pumila + Pinus pinea drop from 84% (349 + 346 of 832) to 52% of the positions (209 + 220); Melia azedarach (105) and Pinus halepensis (63) come next.
- Diversity is cheap here: the balanced layout with the floor still gives +27.5% summer shade over the random palette mean (+30.1% without it). The floor does not touch S0 or the random layouts.
- Browser check (same LP in `web/src/optimize.js`, HiGHS WASM): floors 6, 10 and 15 are met (6.01, 10.02, 15.02) in 1–5 s; with the six-species city palette of 12 Oct a floor of 6 was infeasible and the app said so. With the seven-species city palette (20 Oct) a floor of 6 is feasible: from the balanced weights the browser reaches 6.0 effective species in 0.7 s, at ≈ 317,800 m²·h summer shade (≈ −4% vs the balanced layout without the floor; a live estimate, not a Python run).

## S1a and equal trunk size (24 Oct): first results for the 10 Nov deck
Run: `python -m shade_sponge porta --size=exact --trunk=TERCERA` → `databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv`; figures `scripts/make_results_v7.py` → `slides/fig_v7/res_01_radar`, `res_02_bars`.

**Setup:**
- **S1a** = the city's rule: the 2026 mix (Betevé 2026, press) used as relative weights (Celtis 12, Melia 7.25, Pyrus / Styphnolobium / Tipuana 5 each, `ASSUMPTION`), drawn at random within the exact sidewalk sizing rule and the 15% cap; 10 seeds. The most constrained positions are drawn first, so every tree fits in all 10 seeds, and only mix species are used.
- **Equal trunk size:** species traits are the medians of Porta's trees in trunk class TERCERA (81–110 cm perimeter); *Pyrus* falls back to SEGONA (it has no TERCERA trees in Porta); *Styphnolobium* keeps the city-wide sample.
- **Optimised layouts:** the weighted-sum sweep under the same sizing rule.
- **New indicator:** canopy cover, measured as crown discs plus the fixed park/private canopy over the site. It reads 23.3% for S0, against 20.1% from the LiDAR CHM. The discs are not the cause: they cover 11.1%, below the 12.3% of segmented crowns. The excess is in the fixed background, which is built by removing only the S0 discs, so plane canopy outside each disc stays in every layout. This also makes the cover lost by replacement look smaller (a conservative bias). Compare it between layouts, not with the 30% target.

**Results** (all 832 plane positions, T2-60 storm, heat = effective-shade proxy; Opt = weights 0.5 summer / 0.25 winter / 0.25 hotspot runoff):

| | S0 today | S1a (mean of 10) | Opt |
|---|---|---|---|
| Summer shade, thousand m²·h | 359.3 | 314.0 (−12.6% vs S0) | 353.1 (−1.7%) |
| Winter shade, thousand m²·h (a cost) | 196.2 | 196.9 | 209.5 |
| Total runoff, m³ | 17,668.2 | 17,722.3 | 17,688.4 (−33.9 vs S1a; below Δmin = 91) |
| Hotspot runoff, m³ | 2,682.3 | 2,694.0 | 2,681.0 |
| Canopy cover (disc model), % | 23.3 | 21.5 | 22.2 |

**Reading:**
- Against the city's rule, the optimised layout keeps **+39 thousand m²·h of summer shade (+12.4%)**: it keeps 98% of today's summer shade, where S1a keeps 87%.
- It pays for it with **+13 thousand m²·h of winter shade (+6.4%)**: the summer–winter trade-off again.
- Runoff differences stay under Δmin, so the runoff half of H1 is **not resolved** by the model.
- Opt mix: Jacaranda 278, Melia 256 (both at the cap), Tipuana 125, Styphnolobium 69, Pyrus 54, Celtis 43, Brachychiton 7. S1a mix (mean of 10): Tipuana 216, Styphnolobium 187, Pyrus 153, Melia 150, Celtis 127 (cap).

**Caveats:**
- These are not UTCI results yet; the effective-shade proxy is the heat measure.
- The replacement trees are scored at TERCERA size, not as young trees.
- The 15% cap is applied within Porta (`ASSUMPTION`).
- S0 is not at equal trunk size: it has today's measured planes, 2,600 trees, while each layout puts trees at all 832 plane positions, 25 more than S0's planes with good LiDAR crowns.
- Additions (A, R+A): see the next section.

## Growth stage: about 10 years vs established (28 Oct)
Run: `python -m shade_sponge porta --size=exact --trunk=SEGONA` → `databases/barcelona/tool_v0_summary_sizeexact_trunkSEGONA.csv`; web: `porta-segona` (header switch "≈ 10 years | Established").

**Stage definition:**
- **About 10 years:** the second trunk class (SEGONA, 41–80 cm perimeter). Among the dated palette-species trees in the city inventory, the median time from planting to the LiDAR flight (26 Sept 2021) is 9.7 years (n = 4,213). Planting dates go back only about 14 years, so older trees are missing from this estimate.
- **Established:** the third class (TERCERA, 81–110 cm), the thesis comparison above. Its dated trees have a median of 11.1 years, but that is censored by the same date limit, so no age is claimed for it.
- **Planting (first class, PRIMERA):** not offered. Too few palette trees have crowns in Porta (Brachychiton 1, Tipuana 7, Jacaranda 9, Melia 10), and their LiDAR heights are implausible (Melia 12.2 m), probably small crowns segmented under larger ones.

**Results** (all 832 positions, T2-60, balanced weights; S0 = today's measured trees in both rows):

| Stage | S1a summer shade, % of today | Opt summer shade, % of today | Opt vs S1a, summer / winter shade | Total runoff vs today, S1a / Opt (m³) | Canopy (disc model), S1a / Opt |
|---|---|---|---|---|---|
| About 10 years | 75.5 | 81.8 | +8.4% / +7.6% | +84.4 / +64.1 | 20.5 / 21.0% |
| Established | 87.4 | 98.3 | +12.4% / +6.4% | +54.1 / +20.2 | 21.5 / 22.2% |

**Reading:**
- **The transition costs a quarter of today's summer shade under the city's rule, and about a fifth with optimised species.** Both stages compare against today's mature planes.
- **The optimised advantage is smaller at 10 years** (+8.4% vs +12.4%), because young crowns differ less between species.
- **Every runoff difference still stays within Δmin** (91 m³), even against today. The stage barely moves the runoff answer.
- **The 10-year optimised mix shifts to the species that grow wide fast:** Jacaranda 278 and Tipuana 284 (both at the cap), Styphnolobium 130, Melia 88, Brachychiton 38, Celtis 9, Pyrus 5.

**Caveats:**
- *Styphnolobium* keeps its city-wide all-class medians at both stages, so it is not staged, and it is favoured at 10 years. Treat its 130 trees with caution.
- A trunk class is not an age class, and growth depends on site.
- The dated trees are those planted since about 2007.

## Additions: R, A and R+A (24 Oct)
**Spots:** `scripts/porta_planting_spots.py` → `databases/barcelona/porta_planting_spots.csv`, built in four steps:
1. Walk every façade line of the 1:1000 map (same tiles and ray method as the sidewalk widths) and take the first road line beyond it as the kerb.
2. Place the pit 0.7 m in from the kerb: the median kerb-to-tree distance of the measured trees is 0.69 m.
3. Keep sidewalks ≥ 2.5 m, and only spots within 15 m of an OSM street centreline (`ASSUMPTION`; it drops paths inside blocks).
4. Keep 7 / 9 / 13 m between trees by size class, existing trees included (2011 guide).

The result is **267 spots: 142 small, 53 medium, 72 large.** This is an **upper bound**: driveways, crossings, bus stops, lamps and underground services are not in the data.

**Run:** `scripts/run_additions.py` → `databases/barcelona/additions_summary.csv`. S1a has 5 seeds; Opt uses the balanced weights; both use the exact sizing rule and TERCERA traits. The cap is recomputed on the larger stock.

| | Summer shade, % of today | Winter shade, % of today | Total runoff, m³ vs today | Canopy (disc model), points vs today |
|---|---|---|---|---|
| R, city rule | 87.3 | 100.5 | +54.4 | −1.8 |
| R, optimised | 98.3 | 106.8 | +20.2 | −1.1 |
| A, city rule | 104.5 | 104.1 | −16.9 | +0.6 |
| A, optimised | 106.2 | 106.7 | −24.6 | +0.7 |
| R+A, city rule | 92.6 | 106.5 | +35.9 | −1.2 |
| R+A, optimised | **104.2** | 111.9 | −4.2 | −0.4 |

**Reading:**
- **Of the scenarios that replace the planes, only R+A optimised ends above today's summer shade (104.2%).** The city's rule with the same additions stays below (92.6%). Adding trees while keeping the planes (A) ends higher still (104.5% city rule, 106.2% optimised), but A is not the city's policy: the planes are being replaced.
- **Additions alone add little through species choice** (+1.7 points over the city's rule). 174 of the 267 spots are fixed to *Pyrus* in every layout: 142 narrow sidewalks, plus 32 wider ones where no larger crown clears the façade. So species choice acts on only 93 spots.
- **Every runoff difference stays within ±Δmin (91 m³).**
- **Canopy stays below today in R and R+A, but the gap is smaller with optimised species.** The disc model is conservative here (see the S1a section).

**Caveats:**
- Heat is the shade proxy, and the trees are scored at TERCERA size.
- The spots are a ceiling, not a plan. Not modelled: driveways (> 1 m), traffic lights and signs (> 3 m), lamps (3 / 4.5 / 6.5 m), balcony clearance (0.5 m), crossings, bus stops and services.
- A new spot is spaced by its own class only, so a small spot can sit 7–13 m from an existing large tree. This slightly overstates the count.
- R scores 832 positions; S0 has 809 planes with good LiDAR crowns.

### Canopy cover against the 30% target (28 Oct)
**The gap:** Porta's measured cover is 20.1% (LiDAR CHM > 2 m, 2021; `databases/barcelona/porta_canopy_cover.csv`), against the plan's 30%. That is **9.9 points, about 8.3 ha of crowns**.

**What street trees can close** (from the additions run above, disc model):
- **All 267 free spots, optimised species:** **+0.70 pts**, reaching about **20.8%**, so about 7% of the gap. With the city's mix: +0.59 pts.
- **Crown per new tree:** each optimised new tree adds on average about 22 m² of crown (0.70% × 83.7 ha / 267).
- **Trees needed:** closing the gap would take about **3,800 street trees** of that size. That is 14 times the street spots found, which are themselves an upper bound.

**Reading:**
- **Additions are the lever on cover, replacement is not.** Every replacement layout lowers cover, and every additions layout raises it.
- **Street trees alone cannot reach the 30%.** The rest has to come from squares, courtyards, parks and de-sealed ground (scale estimate; the 30% is a city-wide target, not a per-neighbourhood one).

**In the web app:** a "Canopy cover" counter shows the layout on screen against the target. It starts from the measured 20.1% and adds the change of the disc model, and it rises with every added tree. For live layouts, project areas and added trees the change is a no-overlap sum, so it runs high.

## Genus and family check (24 Oct)
Every layout now reports its largest genus and family share: `layout.taxon_shares`, with families from standard taxonomy. These are compared with Santamour's (1990) 20% per genus and 30% per family (values from `databases/barcelona/additions_summary.csv`; city rule = mean of its 5 seeds), and reported, not constrained, because Barcelona caps species only. The denominator is the evaluated tree set (good LiDAR crowns plus the new trees), so shares run slightly above the cap's 2,825-tree denominator.

| | Largest genus | Largest family |
|---|---|---|
| Today (S0) | Platanus 31.1% | Platanaceae 31.1% |
| R, city rule | Celtis 17.3% | Fabaceae 25.3% (Tipuana + Styphnolobium + Robinia + …) |
| R, optimised | Jacaranda 16.0% | Bignoniaceae 19.9% |
| A (planes kept) | Platanus 28.2% | Platanaceae 28.2% |
| R+A, city rule / optimised | Celtis 17.1% / Jacaranda 15.9% | Fabaceae 24.9% / Bignoniaceae 19.5% |

**Reading:**
- Today's stock fails both the genus and the family rule (31.1%). Additions-only fails the genus rule (28.2%).
- Every replacement layout passes both the genus and the family limit.
- The optimised layouts with balanced weights are the more even ones at family level: their largest family is about 20%, against about 25% under the city rule. Other weight sets reach Fabaceae 23–24%.
- Santamour notes that the legume genera may share few pests across their subfamilies (p. 63), so the 25% Fabaceae of the city rule is a cautious reading.

## Next (not done)
align the summer design window with the heat metric decided on 19 Oct (mean UTCI over 12–17 h on a hot design day, `notes/topic_decision.md` §8; that window is EPW standard time, i.e. 13–18 h CEST, `notes/decisions/heat_objective.md` §1; the proxy uses 15 Jul 12–17 h CEST) together with the Ladybug calibration · check whether hotspot runoff follows the runoff weight (it did not on 8 Oct; it mostly does on 15 and 20 Oct) · species storage factor · young/mature horizon · `CAPTURE_M` and design-day sensitivity · calibrate the heat proxy on Ladybug Tier 1 (sub-area) · climate-fit filter for other sites · Grasshopper component (Hops) · web app.
