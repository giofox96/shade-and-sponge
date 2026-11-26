"""Thesis figures drawn from the result CSVs (post needle fix), in the project palette.
Writes thesis/fig/ch7_porta_tradeoff.png and thesis/fig/ch7_diversity_series.png. Run from the repo root."""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

DB, OUT = Path("databases/barcelona"), Path("thesis/fig")
GREEN, BLUE, TERRA, INK, GREY, CREAM = "#3F663E", "#283F66", "#8A3E22", "#2A2622", "#A8A293", "#F2F0EA"
plt.rcParams.update({"font.family": "IBM Plex Sans", "font.size": 9, "axes.edgecolor": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "figure.facecolor": "white"})

d = pd.read_csv(DB / "tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv")
s0 = d[d.scenario == "S0_current"].iloc[0]
d["summer"] = 100 * d.shade_summer_m2h / s0.shade_summer_m2h
d["winter"] = 100 * d.shade_winter_m2h / s0.shade_winter_m2h
fig, ax = plt.subplots(figsize=(5.2, 4.0), dpi=300)
for pre, lab, c, m in (("S1_random", "Random palette", GREY, "o"), ("S1a", "Announced mix (S1a)", BLUE, "o"),
                       ("S1b", "City practice (S1b)", TERRA, "o"), ("S4", "Method, weight sweep", GREEN, "D")):
    x = d[d.scenario.str.startswith(pre)]
    ax.scatter(x.summer, x.winter, s=22, c=c, marker=m, label=lab, alpha=0.85, edgecolors="none")
b = d[d.scenario == "S4_s0.50_w0.25_r0.25"].iloc[0]
ax.scatter(b.summer, b.winter, s=90, facecolors="none", edgecolors=INK, marker="D", label="Method, balanced")
ax.scatter(100, 100, s=40, c=INK, marker="s", label="Today (S0)")
ax.axvline(100, c=INK, lw=0.6, ls="--"), ax.axhline(100, c=INK, lw=0.6, ls="--")
ax.set_xlabel("Summer shade, % of today (more is better)"), ax.set_ylabel("Winter shade, % of today (less is better)")
ax.legend(frameon=False, fontsize=7.5, loc="lower right"), ax.grid(alpha=0.3)
fig.tight_layout(), fig.savefig(OUT / "ch7_porta_tradeoff.png"), plt.close(fig)

v = pd.read_csv(DB / "diversity_series.csv")
fig, ax = plt.subplots(figsize=(5.2, 3.9), dpi=300)
for lay, lab, c in (("balanced", "Method, balanced weights", GREEN), ("summer_only", "Method, summer only", BLUE)):
    x = v[v.layout == lay]
    ax.plot(x.eff_species, x.summer_pct_S0, marker="o", ms=4, c=c, label=lab)
for pre, lab, c in (("S1a", "Announced mix (S1a)", BLUE), ("S1b", "City practice (S1b)", TERRA)):
    x = d[d.scenario.str.startswith(pre)]
    ax.scatter(x.eff_species.mean(), x.summer.mean(), s=40, c=c, marker="s", label=lab + ", mean of 10 draws")
ax.axhline(100, c=INK, lw=0.6, ls="--")
ax.text(20.3, 100.15, "today", fontsize=7.5, color=INK, ha="right")
ax.set_xlabel("Effective number of species, exp(Shannon), replaced positions"), ax.set_ylabel("Summer shade, % of today")
ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2), ax.grid(alpha=0.3)
fig.tight_layout(), fig.savefig(OUT / "ch7_diversity_series.png"), plt.close(fig)
