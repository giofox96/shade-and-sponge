"""Figure for tool v0 (python -m shade_sponge first): (a) layouts on shade vs hotspot runoff, (b) Porta map of water
convergence, flood hotspots and the species suggested at w = 0.5. Output: notes/figures/tool_v0.png"""
import glob, pathlib, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from shade_sponge.site import load_site, ROOT, DB, EX
from shade_sponge.layout import CITY_PALETTE

CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]   # categorical slots 1-6 (dataviz palette)
INK, MUTED = "#0b0b0b", "#52514e"
s = load_site("porta")
res = pd.read_csv(DB / "tool_v0_summary.csv")
lay = pd.read_csv(sorted(glob.glob(str(EX / "to_gh/layouts_tool_v0_*.csv")))[-1])
fig, (a, b) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw=dict(width_ratios=[1, 1.15]))

g = {"S0_current": ("S0 current (mature planes)", INK, "s"), "S1": ("S1 random palette, 10 seeds", "#9a9893", "o"),
     "S4": ("S4 optimised, w = 0…1", CAT[0], "D")}
for k, (lab, col, m) in g.items():
    d = res[res.scenario.str.startswith(k)]
    a.scatter(d.shade_m2h / 1e3, d.runoff_hot_m3, s=46, c=col, marker=m, label=lab, edgecolor="white", linewidth=1.5)
a.set_xlabel("Effective shade on sunlit open ground, 12–17 h (thousand m²·h)  →  better", color=MUTED)
a.set_ylabel("Runoff reaching flood hotspots, T2-60 storm (m³)  ↓  better", color=MUTED)
a.set_title("(a) Replacement layouts: heat proxy vs hotspot runoff", loc="left", color=INK)
a.legend(frameon=False, loc="upper right")
r1, r4 = res[res.scenario.str.startswith("S1")].mean(numeric_only=True), res[res.scenario.str.startswith("S4")].mean(numeric_only=True)
a.annotate(f"every weight gives ~the same layout:\n{100 * (r4.shade_m2h / r1.shade_m2h - 1):+.0f}% shade, "
           f"{100 * (r4.runoff_hot_m3 / r1.runoff_hot_m3 - 1):+.1f}% hotspot runoff\nvs random palette",
           (r4.shade_m2h / 1e3, r4.runoff_hot_m3), xytext=(12, 30), textcoords="offset points", fontsize=9, color=MUTED)
for sp in ("top", "right"):
    a.spines[sp].set_visible(False)
a.grid(alpha=0.25, linewidth=0.6)

ext = [0, s.domain.shape[1], 0, s.domain.shape[0]]
acc = np.where(s.domain & ~s.roof, np.log10(np.maximum(s.acc, 1)), np.nan)
b.imshow(np.where(s.roof & s.domain, 1, np.nan), cmap="Greys", vmin=0, vmax=8, extent=ext)
im = b.imshow(acc, cmap="Blues", vmin=0, vmax=5, extent=ext)
b.imshow(np.where(s.hot & s.domain & ~s.roof, 1, np.nan), cmap="Reds", vmin=0, vmax=1.4, alpha=0.55, extent=ext)
o = lay[lay.scenario == "S4_w0.5"]
x0, y1 = s.x0 - 430800, s.y1 - 4586800                    # local coords -> image coords (exchange/site_origin.json)
handles = []
for col, sp in zip(CAT, CITY_PALETTE):                     # colour fixed per species (palette order)
    d = o[o.species == sp]
    b.scatter(d.x - x0, s.domain.shape[0] - (y1 - d.y), s=10, c=col, edgecolor="white", linewidth=0.4)
    handles.append(Line2D([], [], marker="o", ls="", color=col, label=f"{sp} ({len(d)})"))
handles.append(Line2D([], [], marker="s", ls="", color="#e88c80", label="flood-hazard index ≥ 40"))
b.legend(handles=handles, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3)
b.set_title("(b) Water convergence, hotspots, suggestion at w = 0.5", loc="left", color=INK)
b.set_axis_off()
fig.colorbar(im, ax=b, shrink=0.6, label="upstream open area, log10 m²")
fig.tight_layout()
out = ROOT / "notes/figures/tool_v0.png"
fig.savefig(out, dpi=160)
print(out)
