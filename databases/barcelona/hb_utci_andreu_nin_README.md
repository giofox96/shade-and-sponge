# Honeybee Tier 2 UTCI, Pg Andreu Nin (run 2 Nov 2026 on the OMEN PC)

- Recipe: `utci_comfort_map` from lbt-recipes 0.26.23 (same recipe as the *HB UTCI Comfort Map* component), Ladybug Tools
  Python 3.10.10 at `C:\Program Files\ladybug_tools\python`, honeybee-radiance 1.66.197, ladybug-comfort 0.18.91.
- Command, per model: `python scripts/run_hb_utci.py exchange/to_gh/hb_andreu_nin_<model>.hbjson C:\hb_runs\<model>`
  (PATH + RAYPATH set to `C:\Program Files\ladybug_tools\radiance`). Inputs: EPW + DDY El Prat TMYx 2011-2025, north 0,
  run period `7/15 to 7/15 between 0 and 23 @1`, cpu-count 12, default radiance/solarcal/comfort parameters.
- Runtime: 2.6-2.8 min per model (16 logical cores).
- Output read: `results/temperature/andreu_nin.npy`, 1,974 sensors x 24 h; `hb_utci_andreu_nin.csv` = mean of columns
  11-16 (EPW 15 Jul 11:00-16:00, the Tier 1 hours), sensors in the order of `street_andreu-nin_testpoints_20261031.csv`.
- Means: S0 opaque 30.81, S0 porous 31.35, S4 opaque 30.87, S4 porous 31.19 C.
