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
| `heat.py` | Sun position (NOAA equations), building shadows at 1.1 m, elliptical shadows of ellipsoid crowns; opacity f·(1 − exp(−0.5·LAI)) + (1 − f)·OP_BARE with f = leaf fraction of the month. Summer shade = benefit, winter shade = cost | Design days **15 July 12–17 h CEST and 15 January 10–15 h CET (ASSUMPTION** until the EPW hottest/coldest weeks). **OP_BARE = 0.35 (ASSUMPTION**, test 0.25–0.54): leafless crowns cut ~35% of sunlight (McPherson 1984; up to ~54% for London plane, Heisler 1982/84; both cited in Thayer & Maeda 1985). Proxy, **to calibrate against Ladybug UTCI** |
| `runoff.py` | Runoff v1 as functions: storage bucket s·LAI + SCS-CN | Reproduces `runoff_scenarios.csv` exactly (S0, T2-60, full leaf: 17,649.6 m³) |
| `season.py` | Leaf-on calendar: LAI(m) = LAI(LiDAR, 26 Sept) × (R_OFF + (1 − R_OFF)·f(m)); runoff = expected value over the storm months | f(m): `databases/traits/phenology_palette.csv` (sources per species; class-default months marked ASSUMPTION). Storm months: `databases/barcelona/storm_months.csv` (Esbrí et al. 2026, Fig. 4). **R_OFF = 0.5 (ASSUMPTION**, test 0.3–0.7; anchors Herbst et al. 2008, Xiao et al. 2000). Heat uses July leaves |
| `layout.py` | Palette, 15% cap, façade-clearance fit, per-position potentials, weighted-sum LP (HiGHS) over 3 objectives (summer shade ↑, winter shade ↓, hotspot runoff ↓; 15 weight sets), random baseline, Pareto | Species traits = median of each species' Porta trees (LiDAR 2021); same s per LAI for all species. Clearance: crown radius ≤ distance to nearest building (ASSUMPTION: no margin) |

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
**Current run (15 Oct):** seven species (Styphnolobium added 14 Oct) and the photo-based leaf calendar adopted 15 Oct (Jacaranda f = 0.8 on the 15 Jan design day instead of 0, Tipuana f = 0.5 in February; `notes/decisions/leaf_state_inat.md`). Crown shadows are ellipses (longer in low sun); runoff is season-weighted, with full-leaf values in the `*_leafon` columns (runoff and interception). Season-weighted interception is 1.3–2.3% lower than at full leaf.
| Layout | Summer shade (m²·h) | Winter shade (m²·h, cost) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 224,223 | 2,681.4 |
| S1 random palette (mean of 10) | 286,656 | 217,729 | 2,697.6 |
| S4 summer only (1, 0, 0) | 332,224 | 232,835 | 2,690.0 |
| **S4 balanced (0.50, 0.25, 0.25)** | **332,342** | **227,943** | 2,688.1 |
| S4 winter-heavy (0, 0.50, 0.50) | 272,596 | 187,782 | 2,690.2 |

S0's winter shade rose (217,003 → 224,223) while its summer shade did not change; the only S0 input that changed for 15 Jan is Jacaranda's leaf fraction (0 → 0.8), so Porta's existing Jacaranda are the likely cause (not isolated by a separate run).
- **A small free gain first:** summer-only → balanced cuts winter shade by only 2.1% at the same summer shade, still by swapping ~90 Tipuana (fully leafed in January) for Jacaranda (80% leafed). It is not robust: the swap vanishes in 3 of 8 sensitivity variants. The balanced layout beats the random palette on summer shade (+15.9%) but casts more winter shade than it (+4.7%).
- **Then a real trade-off:** beyond the balanced layout, more winter sun costs summer shade (winter-heavy: −17.6% winter shade for −18.0% summer shade). The winter-heavy layout drops Tipuana (0) and most Jacaranda (35) for the winter-bare Pyrus (276, its cap), Styphnolobium (223), Melia (185) and Celtis (98). The front is not a point, and the trade-off is robust (see sensitivity).
- **Placement follows the buildings, partly:** in the balanced layout the winter-bare Melia gets positions in sun 87% of winter hours, Jacaranda 62%, Tipuana 44%, evergreen Brachychiton 29% (positions file: `sun_share_winter`). But the winter-bare Styphnolobium (34%) and Pyrus (26%) also sit in streets that buildings already shade in winter, so leaf habit does not explain all placements.
- Total runoff follows interception, i.e. crown size (17,703 m³ balanced vs 17,743 m³ winter-heavy). Hotspot runoff varies by only 0.5% across weights (2,688–2,702 m³). In this run it mostly follows the runoff weight (lowest for runoff-only, highest for winter-only; Spearman −0.73 between runoff weight and hotspot runoff). In the 8 Oct run it did not (the winter-heavy layout was lowest), so the per-position water potential is still unverified (to check: crown overlap with kept trees, the box-filter approximation).

**Superseded (old calendar, 8 Oct; six species, Jacaranda bare Jan–Mar):** summer-only → balanced −9% winter shade (~100 Tipuana → Jacaranda) at equal summer shade; balanced vs random +14% summer, −3% winter; winter-heavy vs balanced −11% winter for −16% summer shade; placement Jacaranda 80%, Tipuana 51%, Brachychiton 29% of winter hours in sun.

## Sensitivity of the winter-sun result (re-run 15 Oct, `scripts/sensitivity_tool_v0.py`)
Base run plus 7 one-change variants: leafless opacity 0.25 / 0.54; Tipuana bare in Jan–Feb ('briefly deciduous' in winter: Santa Barbara Beautiful, Tree of the Month; search snippet only); Jacaranda half-leafed Jan–Mar; Jacaranda bare Jan–Mar (the old calendar, from the Valencia BBCH study); winter design day 21 Dec / 15 Feb. Each re-optimises summer-only, balanced and winter-heavy layouts against 3 random palettes. Results: `databases/barcelona/tool_v0_sensitivity.csv` (summary), `_raw.csv`. The base variant reproduces the main run exactly.

| Claim | Range across variants | Verdict |
|---|---|---|
| Optimised (balanced) vs random palette, summer shade | +15.8 to +15.9% (main run vs 10 random: +15.9%) | **robust** |
| Balanced vs random palette, winter shade | −0.8 to +7.9% (−0.8% only with the old Jacaranda calendar) | no winter gain: about equal or worse |
| No-regret swap summer-only → balanced: winter shade at equal summer shade | −0.2 to −8.7% (base −2.1%; summer within ±0.1%) | sign holds, but **small** except with the old calendar |
| Trade-off beyond balanced: winter-heavy vs balanced | winter −12 to −19%, summer −17 to −20% | **robust** |
| Species of the balanced layout | Melia 256, Styphnolobium 67, Celtis 0 in every variant; Tipuana → Jacaranda swap (~90) in only 5 of 8 variants | swap **not robust** |
| Species of the winter-heavy layout | Pyrus 276 (cap) and Styphnolobium 213–245 in every variant, Tipuana 0–11; Melia 43–193, Jacaranda 28–188 | Pyrus + Styphnolobium robust |

- **The calendar, not the new species, shrank the swap:** with the old calendar in the same seven-species run (`jacaranda_bare_jan_mar`) the free gain is −8.7% (8 Oct: −8.9%); with the photo-based calendar it is −2.1%.
- The swap needs Jacaranda to carry fewer leaves than Tipuana on the design day. With the photo-based calendar that holds only in January (0.8 vs 1), so the swap vanishes when Tipuana is bare in Jan–Feb, on 21 Dec (both fully leafed) and on 15 Feb (Jacaranda 0.7 vs Tipuana 0.5). The small gain left in those variants (−0.2 to −0.9%) comes from other species.
- Leafless opacity still scales it (−3.0% at 0.25, −0.4% at 0.54).

**Superseded (old calendar, 8 Oct; 7 variants, six species):** free gain −2.2 to −11.6%; Jacaranda 278 and Tipuana 186 in the balanced layout of every variant; winter-heavy vs balanced winter −10 to −14%, summer −15 to −19%.

## Barcelona shortlist palette (9 Oct): `python -m shade_sponge porta --palette=barcelona`
- **Shortlist** (`scripts/species_shortlist.py` → `databases/barcelona/species_shortlist.csv`): street-tree species with ≥ 500 trees in Barcelona's inventory (140,404 street trees of 211 species, Open Data BCN; palms are inventoried separately, 4,772, and left out as a design choice), taken as established in the city's climate (ASSUMPTION). Excluded: Platanus (being replaced). None of the tree taxa of the Spanish invasive catalogue that apply in Catalonia (Ailanthus altissima, Acacia dealbata, A. melanoxylon, Myoporum laetum; MITECO table, 21 Oct 2025) reaches 500 street trees; they would be excluded. Flagged but kept (invasive behaviour reported, not legally listed): Robinia pseudoacacia and Ulmus pumila (riparian invasion in Spain: Cabra-Rivas, Castro-Díez & Saldaña 2015, Ecosistemas 24(1):18–28), Ligustrum lucidum (global review: Fernandez et al. 2020, Bot. Rev. 86:93–118). Result: **34 species**.
- **Crowns:** LiDAR on 3 ICGC tiles (one is Porta's own tile) chosen to cover ≥ 40 inventory trees per species away from tile edges (`scripts/bcn_lidar_species.py`, same method as Porta; flights 26 Sept 2021 and 1 June 2022, both leaf-on: `lidar_tiles_dates.csv`) → `species_lidar_summary.csv` (33–735 trees per species; Porta + tiles). The 6 city species also get these city-wide medians in this run (e.g. Celtis crown 6.3 m vs 4.6 m in Porta).
- **Leaf habit:** sourced for all 34 (BROT 2, Zaragoza species guide, UConn, NC State, UF/IFAS, ACT; `databases/traits/phenology_palette.csv`); months: class defaults for the new deciduous species, leaf-on all year for evergreens (both ASSUMPTION; Grevillea's spring leaf drop is ignored).

| Layout (Barcelona palette) | Summer shade (m²·h) | Winter shade (m²·h) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 188,656 | 2,682.5 |
| S1 random palette (mean of 10) | 280,593 | 180,023 | 2,698.9 |
| S4 summer only | 365,457 | 247,263 | 2,682.5 |
| **S4 balanced** | **362,485** | **201,145** | 2,682.4 |
| S4 winter-heavy | 272,615 | 148,113 | 2,683.7 |

- **Optimised replacements now match or exceed the mature planes on summer shade** (+0.9% balanced, +1.7% summer-only), which the city palette could not (−8%). Balanced vs city-palette balanced: +9% summer shade, +16% winter shade (more evergreen crown).
- **The trade-off is wider:** winter shade spans 136,000–248,000 m²·h across the 15 weight sets (city palette: 150,000–194,000). Summer-only → balanced: −19% winter shade for −0.8% summer shade (P. halepensis and some P. pinea → Ulmus pumila). Caveat: Ulmus pumila, the main species of the balanced layout, is coded winter-deciduous, but is reported semi-evergreen in warm climates (treelib.ca), which would shrink this gain.
- **Low diversity:** a few species dominate (balanced: Ulmus pumila 349 + Pinus pinea 346 = 84% of 832 positions; summer-only: Pinus pinea 422, at its cap, + P. halepensis 183; winter-heavy: the small-crowned Hibiscus syriacus 404, at its cap). The model scores only shade and interception: it ignores maintenance, roots and paving, allergenicity, the invasive flag on Ulmus pumila, and functional diversity. Two levers: the max share per species (web app slider) and the optional diversity floor (next section).

## Diversity floor (optional, added 12 Oct)
`--diversity=N` (web app: "Diversity floor" toggle) keeps at least N **effective species**, exp(Shannon H), among the replanted positions; off by default. The effective number of species is the diversity measure SylvCiT uses (Nicol et al. 2026). Shannon H is concave in the species counts, so the floor is linear: each species' term −p·ln p is replaced by the piecewise-linear interpolation through about 36 breakpoints (40 log-spaced counts, rounded; which lies below the curve, so the floor is conservative) and only the species counts are integer (`layout._entropy_chords`, `layout.assign`). The value of N is a designer choice, not a sourced threshold. Every replacement-layout row of the summary now has `eff_species`. Summary and exchange outputs carry a `_div<N>` suffix.

Barcelona shortlist, N = 10 (`databases/barcelona/tool_v0_summary_barcelona_div10.csv` vs `tool_v0_summary_barcelona.csv`):
| Layout | Effective species | Summer shade | Winter shade | Hotspot runoff | Interception |
|---|---|---|---|---|---|
| S4 summer only (1, 0, 0) | 4.95 → 10.0 | −1.9% | −3.1% | +0.1% | −1.5% |
| **S4 balanced (0.50, 0.25, 0.25)** | **4.16 → 10.0** | **−1.9%** | **−2.0%** | **+0.0%** | **−1.2%** |
| S4 (0, 0.50, 0.50) | 6.71 → 10.0 | −1.6% | +0.2% | +0.0% | −0.8% |
| S4 runoff only (0, 0, 1) | 4.50 → 10.0 | −2.0% | −1.1% | +0.0% | −1.3% |

- In the balanced layout, Ulmus pumila + Pinus pinea drop from 84% (349 + 346 of 832) to 52% of the positions (209 + 223); Melia azedarach (102) and Pinus halepensis (63) come next.
- Diversity is cheap here: the balanced layout with the floor still gives +27% summer shade over the random palette mean (+29% without it). The floor does not touch S0 or the random layouts.
- Browser check (same LP in `web/src/optimize.js`, HiGHS WASM): floors 6, 10 and 15 are met (6.01, 10.02, 15.02) in 1–5 s; with the city palette (6 species) a floor of 6 is infeasible and the app says so.

## Next (not done)
check whether hotspot runoff follows the runoff weight (it did not on 8 Oct; it mostly does on 15 Oct) · species storage factor · young/mature horizon · `CAPTURE_M` and design-day sensitivity · calibrate the heat proxy on Ladybug Tier 1 (sub-area) · climate-fit filter for other sites · Grasshopper component (Hops) · web app.
