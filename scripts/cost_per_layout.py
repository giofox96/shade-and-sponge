"""Cost per layout: direct cost and summer shade of the method vs city practice (S1b), Porta and the whole city.
Unit costs from notes/costs_stakeholders.md §1 (direct costs, no VAT, no watering): replace a street tree ~190 € (small)
to ~1,070 € (large stump); widen a pit 1 -> 1.5 m² ~100 € (make_final_new.py cost slide, CYPE items). Every layout replaces
the same planes with one tree each, so the direct cost is the same for the method and for city practice; pit size follows
the sidewalk class, not the species (scripts/porta_sidewalk_width.py), so widening does not change between layouts either.
The difference is the shade the same money buys. Shade: m²·h on 15 July 12–17 h; / 6 = mean shaded m² over the afternoon.
Inputs: databases/barcelona/tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv (Porta, Barcelona palette),
        citylp_city.csv + citylp_summary.csv (python scripts/city_lp.py --all, 67 barris, city palette).
Output: databases/barcelona/cost_per_layout.csv. Run from the repo root: python scripts/cost_per_layout.py"""
import pathlib, pandas as pd

DB = pathlib.Path(__file__).resolve().parents[1] / "databases/barcelona"
REPLACE = (190, 1070)          # € per replaced tree, low / high (costs_stakeholders.md §1)
WIDEN = 100                    # € per pit widened 1 -> 1.5 m² (optional add-on, every position, ASSUMPTION)
BUDGET = 10e6

s = pd.read_csv(DB / "tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv").set_index("scenario")
porta_n = int(s.loc["S4_s0.50_w0.25_r0.25", [c for c in s.columns if c[0].isupper() and " " in c]].sum())
c = pd.read_csv(DB / "citylp_city.csv").set_index("scenario")
city_n = int(pd.read_csv(DB / "citylp_summary.csv").planes.sum())
cases = [("Porta", porta_n, s.loc["S0_current"].shade_summer_m2h, s[s.index.str.startswith("S1b")].shade_summer_m2h.mean(),
          s.loc["S4_s0.50_w0.25_r0.25"].shade_summer_m2h, "S4 balanced"),
         ("Whole city (67 barris)", city_n, c.loc["S0_today"].summer_m2h, c.loc["S1b_city_practice"].summer_m2h,
          c.loc["method_city_lp"].summer_m2h, "city LP")]
rows = []
for name, n, s0, prac, meth, label in cases:
    gain = meth - prac                                          # m²·h the method adds over city practice, same spend
    rows.append(dict(case=name, method=label, trees_replaced=n,
                     cost_low_eur=n * REPLACE[0], cost_high_eur=n * REPLACE[1], cost_high_with_pits_eur=n * (REPLACE[1] + WIDEN),
                     summer_pct_practice=round(100 * prac / s0, 1), summer_pct_method=round(100 * meth / s0, 1),
                     gain_over_practice_m2h=round(gain), gain_over_practice_m2=round(gain / 6),
                     gain_m2_per_tree=round(gain / 6 / n, 2), extra_cost_eur=0))
df = pd.DataFrame(rows)
df.to_csv(DB / "cost_per_layout.csv", index=False)
print(df.T.to_string())
r = df.iloc[-1]
k = BUDGET / (REPLACE[1] + WIDEN)
print(f"\n10 M€ at the high unit cost ({REPLACE[1] + WIDEN} €/tree) replaces ~{k:,.0f} trees; with the city-wide gain per tree "
      f"({r.gain_m2_per_tree} m²) the method shades ~{k * r.gain_m2_per_tree:,.0f} m² more than city practice on summer afternoons, at no extra cost.")
