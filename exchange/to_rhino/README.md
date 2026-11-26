# Rhino kit for the final deck (26 Nov 2026)

Inputs for the three visuals marked RHINO in `scripts/make_final_new.py`: the Porta results map, the back-test areas, and
streets before / after. Regenerate with `python scripts/make_rhino_kit.py` (repo root; needs pyproj, scipy).
Step-by-step guide (Italian): `guida_rhino_passo_passo.md`. GH Python snippets: `gh/` (crowns, buildings, lines).

- Coordinates: local metres. Porta = EPSG:25831 minus (430800, 4586800), as `exchange/site_origin.json`. Back-test = one
  origin per group (`origin_x`, `origin_y` in `backtest/backtest_groups.csv`). Z = absolute ground elevation (m).
- Numbers: main after PR #184 (needle fix). Method = Barcelona palette, balanced weights `S4_s0.50_w0.25_r0.25`;
  city practice = `S1b_obs_0` (one of 10 draws).
- Per-tree and per-street shade values are each tree's standalone potential (no crown overlap): for colouring and ranking
  only. Slide totals come from the full model (`databases/barcelona/tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv`).
- Back-test heights and crown bases follow `scripts/backtest_works.py`'s lookup rule (`height_source`); crown diameters are
  the back-test's own.
