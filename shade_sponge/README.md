# shade_sponge: tool core (v0, 8 Oct 2026)

Suggests **which species go at which street-tree position**, scoring each layout on a **heat proxy** (effective shade on sunlit open ground) and **event runoff** (total, and the part that reaches flood hotspots). One Python core serves both front-ends: Grasshopper (via `exchange/`, later Hops) and a web app (later).

## Run
```bash
python -m shade_sponge
```
Run from the project root with the conda env `shade-and-sponge` (`<env>/Library/bin` on PATH). The first run builds `cache/site_porta.npz` (~15 s); a full run takes ~1 min. Figure: `PYTHONPATH=. python scripts/plot_tool_v0.py`.

## Pipeline
| Module | What it does | Key inputs / assumptions |
|---|---|---|
| `site.py` | Site bundle on a 1 m grid: domain, roofs, CN, DTM, building heights, background canopy, flood hotspots, routing results | Surfaces identical to runoff v1. Hotspot = Resilience Atlas index ≥ 40. **`CAPTURE_M` = 100 m (ASSUMPTION)**: runoff counts toward a hotspot only if its flow path reaches it within 100 m (stand-in for sewer inlets) |
| `topo.py` | Priority-Flood routing on DTM + buildings → water convergence (upstream open area) and flow distance to hotspots | No sewer, no inflow from outside the grid |
| `heat.py` | Sun position (NOAA equations), building shadows at 1.1 m, crown shadows with opacity 1 − exp(−0.5·LAI) | Design day **15 July (ASSUMPTION** until the EPW hottest week), 12–17 h CEST. Crown shadow = disk. Proxy, **to calibrate against Ladybug UTCI** |
| `runoff.py` | Runoff v1 as functions: storage bucket s·LAI + SCS-CN | Reproduces `runoff_scenarios.csv` exactly (S0, T2-60: 17,649.6 m³) |
| `layout.py` | Palette, 15% cap, façade-clearance fit, per-position potentials, weighted-sum LP (HiGHS), random baseline, Pareto | Species traits = median of each species' Porta trees (LiDAR 2021); same s per LAI for all species. Clearance: crown radius ≤ distance to nearest building (ASSUMPTION: no margin) |

To add a site, write `build_<site>()` and `trees_<site>()` in `site.py` (same keys and columns).

## Outputs
- `databases/barcelona/tool_v0_summary.csv`: one row per layout (S0, S1 random × 10, S4 weight sweep), with shade_m2h, runoff_m3, runoff_hot_m3, interception_m3, species counts and Pareto flag
- `exchange/to_gh/positions_tool_v0_<date>.csv`, `layouts_tool_v0_<date>.csv`: see `exchange/README.md`
- `notes/figures/tool_v0.png`

## First result (Porta, T2-60, 832 plane positions, city palette of 6)
- Optimised vs random palette: **+16% effective shade**, +5% interception, **−0.3% hotspot runoff** (−0.2% total). The runoff gain is small, as street trees remove only ~2% of Porta's runoff (runoff v1).
- **No trade-off:** every weight w = 0…1 gives almost the same layout (fill Tipuana, Melia and Jacaranda as far as the cap and space allow). Bigger, denser crowns win both objectives, so the front collapses to a point. This is the H2 risk flagged in `notes/agent_backlog.md`. A real trade-off needs traits that pull the two objectives apart: leaf habit vs storm season, species storage (Xiao & McPherson 2016), and growth speed (young vs mature).
- No replacement layout reaches S0 (mature planes): −7% shade even when optimised.

## Next (not done)
Leaf-on calendar per species and an autumn storm · species storage factor · young/mature horizon · `CAPTURE_M` and design-day sensitivity · calibrate the heat proxy on Ladybug Tier 1 (sub-area) · climate-fit filter for other sites · Grasshopper component (Hops) · web app.
