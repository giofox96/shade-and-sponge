# shade_sponge: tool core (v0, 8 Oct 2026)

Suggests **which species go at which street-tree position**, scoring each layout on a **heat proxy** (effective shade on sunlit open ground) and **event runoff** (total, and the part that reaches flood hotspots). One Python core serves both front-ends: Grasshopper (via `exchange/`, later Hops) and a web app (later).

## Run
```bash
python -m shade_sponge
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
- 78% of intense storm days fall in May–Oct (Esbrí et al. 2026: 35 of 45 days), when every palette species is in full leaf. The season-weighted leaf factor in storms is 0.93 for the deciduous species, 0.95 Jacaranda, 0.99 Tipuana and 1.00 Brachychiton (across R_OFF 0.3–0.7 and without Storm Gloria: deciduous 0.90–0.96, Jacaranda 0.92–0.98, Tipuana 0.99; `databases/barcelona/tool_v0_storm_leaf_factor.csv`). This part is still current.
- In that intermediate run (not saved), runoff-weighted layouts took a few more evergreen Brachychiton, the other species did not change, and both objectives moved < 0.1% across weights.
- So with the city palette, crown size and LAI decide both objectives; a trade-off needs a criterion where evergreen or big crowns cost something: **winter sun access**.

## Winter sun access (added 8 Oct): the first real trade-off
**Current run (city palette).** Crown shadows are ellipses (longer in low sun); runoff is season-weighted, with full-leaf values in the `*_leafon` columns (runoff and interception). Season-weighted interception is 2.1–3.0% lower than at full leaf. Since 9 Oct the leaf calendar also covers 28 more species (Barcelona shortlist, below), including many of Porta's kept non-plane trees, which were assumed in full leaf before: winter shade dropped by ~28,000 m²·h in every layout, season-weighted interception by ~4 m³ and hotspot runoff rose by ~1 m³; summer shade and all layouts are unchanged.
| Layout | Summer shade (m²·h) | Winter shade (m²·h, cost) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 188,656 | 2,682.5 |
| S1 random palette (mean of 10) | 290,226 | 179,822 | 2,698.2 |
| S4 summer only (1, 0, 0) | 331,421 | 194,221 | 2,691.6 |
| **S4 balanced (0.50, 0.25, 0.25)** | **331,572** | **174,104** | 2,691.5 |
| S4 winter-heavy (0, 0.50, 0.50) | 278,891 | 151,406 | 2,689.9 |

- **A free gain first:** summer-only → balanced cuts winter shade by 10% at the same summer shade, by swapping ~100 Tipuana (leafed in January) for Jacaranda (bare Jan–Mar). The balanced layout beats the random palette on summer shade (+14%); its winter advantage (−3%) is not robust (see sensitivity).
- **Then a real trade-off:** beyond the balanced layout, more winter sun costs summer shade (winter-heavy: −13% winter shade for −16% summer shade, with Pyrus at its cap and no Tipuana). The front is no longer a point.
- **Placement follows the buildings:** in the balanced layout the winter-bare Jacaranda gets positions in sun 80% of winter hours, Tipuana 51%, evergreen Brachychiton 29% (positions file: `sun_share_winter`). Winter-leafed species go where buildings already shade the street in winter.
- Total runoff follows interception, i.e. crown size (17,712 m³ balanced vs 17,736 m³ winter-heavy). Hotspot runoff varies < 0.4% across weights (2,690–2,700 m³) and does **not** follow the runoff weight: the winter-heavy layout has the lowest hotspot runoff with the least interception, and the runoff-only weight set is not the lowest. So the per-position water potential predicts the re-scored hotspot runoff poorly (to check: crown overlap with kept trees, the box-filter approximation).

## Sensitivity of the winter-sun result (re-run 9 Oct with the extended leaf calendar, `scripts/sensitivity_tool_v0.py`)
Base run plus 6 one-change variants: leafless opacity 0.25 / 0.54; Tipuana bare in Jan–Feb ('briefly deciduous' in winter: Santa Barbara Beautiful, Tree of the Month; search snippet only); Jacaranda half-leafed Jan–Mar (tests partial leaf retention; the Valencia study reports end of leaf fall by mid-Dec); winter design day 21 Dec / 15 Feb. Each re-optimises summer-only, balanced and winter-heavy layouts against 3 random palettes. Results: `databases/barcelona/tool_v0_sensitivity.csv` (summary), `_raw.csv`. The base variant reproduces the main run.

| Claim | Range across variants | Verdict |
|---|---|---|
| Optimised (balanced) vs random palette, summer shade | +14.5 to +14.6% (main run vs 10 random: +14.2%) | **robust** |
| Balanced vs random palette, winter shade | −8.4 to +3.2% | not robust: about equal |
| No-regret swap summer-only → balanced: winter shade at equal summer shade | −2.6 to −14.5% (always ≤ 0, summer ±0.0%) | **robust in sign**, size depends on data |
| Trade-off beyond balanced: winter-heavy vs balanced | winter −11.6 to −16.6%, summer −15.0 to −18.9% | **robust** |
| Species of the balanced layout | Jacaranda 278 and Tipuana 186 in every variant (Celtis 52–67, Pyrus 23–29, Brachychiton 16–37) | **robust** |
| Species of the winter-heavy layout | e.g. Brachychiton 66–191, Melia 3–224 | not robust |

- The swap Tipuana → Jacaranda appears in every variant, even with Tipuana bare in winter: both give almost the same summer shade (Jacaranda's denser canopy offsets its smaller crown), so any weight on winter or runoff tips the choice to Jacaranda (smaller winter shadow, LAI 2.91 vs 2.20).
- Its size depends on two data gaps: Tipuana's winter leaf state (−10.4% if leafed in January, −2.6% if bare) and the leafless opacity (−14.5% at 0.25, −5.0% at 0.54). **Both can be observed:** Tipuana and Jacaranda leaf state in Porta's streets in Dec–Mar (photos per date), or dated iNaturalist observations from Mediterranean cities.

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
- **Low diversity:** a few species dominate (balanced: Ulmus pumila 349 + Pinus pinea 346 = 84% of 832 positions; summer-only: Pinus pinea 422, at its cap, + P. halepensis 183; winter-heavy: the small-crowned Hibiscus syriacus 404, at its cap). The model scores only shade and interception: it ignores maintenance, roots and paving, allergenicity, the invasive flag on Ulmus pumila, and functional diversity. The methodology's diversity constraint (Shannon floor, §6) is not implemented yet; meanwhile the max share per species (web app slider) is the lever.

## Next (not done)
diversity constraint (Shannon floor) · why hotspot runoff does not follow the runoff weight · species storage factor · young/mature horizon · `CAPTURE_M` and design-day sensitivity · calibrate the heat proxy on Ladybug Tier 1 (sub-area) · climate-fit filter for other sites · Grasshopper component (Hops) · web app.
