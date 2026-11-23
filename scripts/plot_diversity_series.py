"""Shade lost vs effective species: the diversity-floor series (Barcelona palette, size exact, TERCERA trunk).

Inputs:  databases/barcelona/tool_v0_summary_barcelona<_divN>_sizeexact_trunkTERCERA.csv (python -m shade_sponge ... --diversity=N)
         databases/barcelona/cobenefits_porta<_divN>.csv (scripts/cobenefits.py)
Outputs: databases/barcelona/diversity_series.csv, notes/figures/diversity_series.png
Run from the repo root: python scripts/plot_diversity_series.py
"""
import pathlib, pandas as pd, matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
BAL, SUMMER = "S4_s0.50_w0.25_r0.25", "S4_s1.00_w0.00_r0.00"   # balanced weights; summer-shade only
rows, refs = [], {}
for tag, floor in [("", None), ("_div7.5", 7.5), ("_div9.4", 9.4), ("_div10", 10), ("_div15.6", 15.6), ("_div20", 20)]:
    f = DB / f"tool_v0_summary_barcelona{tag}_sizeexact_trunkTERCERA.csv"
    if not f.exists():
        print("missing (infeasible or not run):", f.name)
        continue
    s = pd.read_csv(f).set_index("scenario")
    s0 = s.loc["S0_current"]
    cb = pd.read_csv(DB / f"cobenefits_porta{tag}.csv", index_col=0)
    for sc in (BAL, SUMMER):
        r = s.loc[sc]
        rows.append(dict(floor=floor, layout="balanced" if sc == BAL else "summer_only", eff_species=round(r.eff_species, 2),
                         summer_pct_S0=round(100 * r.shade_summer_m2h / s0.shade_summer_m2h, 2),
                         winter_pct_S0=round(100 * r.shade_winter_m2h / s0.shade_winter_m2h, 2),
                         runoff_pct_S0=round(100 * r.runoff_m3 / s0.runoff_m3, 3),
                         max_species_pct=round(cb.loc[sc, "max_species_pct"], 1),
                         pollen_load_pct_S0=round(cb.loc[sc, "pollen_load_pct_S0"], 1),
                         carbon_t_pct_S0=round(cb.loc[sc, "carbon_t_pct_S0"], 1)))
    for k in ("S1a_city_0", "S1b_obs_0"):
        refs[k] = (s.loc[k].eff_species, 100 * s.loc[k].shade_summer_m2h / s0.shade_summer_m2h)
t = pd.DataFrame(rows)
for lay, g in t.groupby("layout"):
    t.loc[g.index, "summer_lost_pts_vs_nofloor"] = (g.summer_pct_S0.iloc[0] - g.summer_pct_S0).round(2)   # first row = no floor
t.to_csv(DB / "diversity_series.csv", index=False)
print(t.to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 4.2))
for lay, g in t.groupby("layout"):
    g = g.sort_values("eff_species")
    ax.plot(g.eff_species, g.summer_pct_S0, "o-", label=f"method, {lay.replace('_', ' ')} weights")
    for _, r in g.iterrows():
        ax.annotate("no floor" if pd.isna(r.floor) else f"{r.floor:g}", (r.eff_species, r.summer_pct_S0),
                    textcoords="offset points", xytext=(4, 4), fontsize=8)
for k, (x, y) in refs.items():
    ax.plot(x, y, "s", color="grey")
    ax.annotate({"S1a_city_0": "city rule (S1a)", "S1b_obs_0": "observed practice (S1b)"}[k], (x, y),
                textcoords="offset points", xytext=(4, -10), fontsize=8, color="grey")
ax.axhline(100, color="k", lw=0.6, ls=":")
ax.set_xlabel("Effective number of species, exp(Shannon H), replaced positions")
ax.set_ylabel("Summer shade, % of today (S0)")
ax.set_title("Porta, plane replacement: summer shade vs species diversity (floor on exp H)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(ROOT / "notes/figures/diversity_series.png", dpi=200)
