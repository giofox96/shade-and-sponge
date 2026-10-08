"""Figure of runoff-module results (databases/barcelona/runoff_scenarios.csv, runoff_sensitivity_storage.csv)."""
import pathlib, pandas as pd, matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
r = pd.read_csv(ROOT / "databases/barcelona/runoff_scenarios.csv")
s = pd.read_csv(ROOT / "databases/barcelona/runoff_sensitivity_storage.csv")
d = r[(r.T_years == 2) & (r.duration_min == 60) & r.scenario.str.startswith("R_")].copy()
d["species"] = d.scenario.str.split("_").str[1]
d["size"] = d.scenario.str.split("_").str[2]
p = d.pivot(index="species", columns="size", values="d_runoff_vs_S0_pct").sort_values("mature")
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
p[["mature", "young"]].plot.barh(ax=ax[0], color=["#2a7f62", "#a7d3a6"])
none = r[(r.scenario == "S_none_street") & (r.T_years == 2) & (r.duration_min == 60)].d_runoff_vs_S0_pct.iloc[0]
ax[0].axvline(none, color="grey", ls="--")
ax[0].text(none, -0.6, f" no street trees +{none:.2f}%", color="grey", fontsize=8)
ax[0].set_xlabel("Change in Porta runoff volume vs current trees (%)")
ax[0].set_ylabel("")
ax[0].set_title("Replacing all 807 plane trees: 2-yr, 1-h storm (31.9 mm)", fontsize=10)
for sv, g in s[s.duration_min == 60].groupby("s_mm_per_lai"):
    ax[1].plot(g.T_years, -g.street_tree_effect_open_space_pct, marker="o", label=f"s = {sv} mm/LAI")
ax[1].set_xscale("log")
ax[1].set_xticks([1, 2, 10], ["1", "2", "10"])
ax[1].set_xlabel("Design storm return period (yr), 1-h duration")
ax[1].set_ylabel("Runoff reduction by current street trees,\nopen space (%)")
ax[1].set_title("Tree benefit shrinks with storm size (H3)", fontsize=10)
ax[1].legend(fontsize=8)
fig.suptitle("Runoff module v1, Porta (Barcelona); storage calibrated on Anys & Weiler (2024) data", fontsize=11)
fig.savefig(ROOT / "notes/figures/runoff_results_v1.png", dpi=150, bbox_inches="tight")
