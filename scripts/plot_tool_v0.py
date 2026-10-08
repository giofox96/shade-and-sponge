"""Figure for tool v0 (python -m shade_sponge first): (a) layouts on summer shade (benefit) vs winter shade (cost),
(b) Porta map of winter sun on open ground with the species of the balanced layout. Output: notes/figures/tool_v0.png"""
import glob, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from shade_sponge.site import load_site, ROOT, DB, EX
from shade_sponge.layout import CITY_PALETTE
from shade_sponge import heat

CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]   # categorical slots 1-6 (dataviz palette)
INK, MUTED = "#0b0b0b", "#52514e"
BAL, SUM = "S4_s0.50_w0.25_r0.25", "S4_s1.00_w0.00_r0.00"
s = load_site("porta")
res = pd.read_csv(DB / "tool_v0_summary.csv")
lay = pd.read_csv(sorted(glob.glob(str(EX / "to_gh/layouts_tool_v0_*.csv")))[-1])
fig, (a, b) = plt.subplots(1, 2, figsize=(13, 6.2), gridspec_kw=dict(width_ratios=[1, 1.15]))

g = {"S0_current": ("S0 current (mature planes)", INK, "s"), "S1": ("S1 random palette, 10 seeds", "#9a9893", "o"),
     "S4": ("S4 optimised, 15 weight sets", CAT[0], "D")}
for k, (lab, col, m) in g.items():
    d = res[res.scenario.str.startswith(k)]
    a.scatter(d.shade_summer_m2h / 1e3, d.shade_winter_m2h / 1e3, s=46, c=col, marker=m, label=lab, edgecolor="white",
              linewidth=1.5)
f = res.set_index("scenario")
p1, p2 = f.loc[SUM], f.loc[BAL]
a.annotate("", (p2.shade_summer_m2h / 1e3, p2.shade_winter_m2h / 1e3), (p1.shade_summer_m2h / 1e3, p1.shade_winter_m2h / 1e3),
           arrowprops=dict(arrowstyle="->", color=INK, lw=1))
a.annotate(f"summer-only → balanced:\n{100 * (p2.shade_winter_m2h / p1.shade_winter_m2h - 1):+.0f}% winter shade,\n"
           f"{100 * (p2.shade_summer_m2h / p1.shade_summer_m2h - 1):+.1f}% summer shade\n(Tipuana → Jacaranda)",
           (p2.shade_summer_m2h / 1e3, (p1.shade_winter_m2h + p2.shade_winter_m2h) / 2e3), xytext=(-150, 0),
           textcoords="offset points", fontsize=9, color=MUTED)
a.set_xlabel("Summer shade on sunlit open ground, 15 Jul 12–17 h (thousand m²·h)  →  better", color=MUTED)
a.set_ylabel("Winter shade on sunlit open ground, 15 Jan 10–15 h (thousand m²·h)  ↓  better", color=MUTED)
a.set_title("(a) Replacement layouts: summer shade vs winter sun", loc="left", color=INK)
r4 = res[res.scenario.str.startswith("S4")].runoff_hot_m3
a.text(0.02, 0.98, f"hotspot runoff varies little: {r4.min():.0f}–{r4.max():.0f} m³ (S4)", transform=a.transAxes,
       va="top", fontsize=9, color=MUTED)
a.legend(frameon=False, loc="lower right")
for sp in ("top", "right"):
    a.spines[sp].set_visible(False)
a.grid(alpha=0.25, linewidth=0.6)

ext = [0, s.domain.shape[1], 0, s.domain.shape[0]]
win = np.mean([heat.sunlit(s, *x) for x in heat.design_suns(s, "winter")], axis=0)
sunmap = LinearSegmentedColormap.from_list("sun", ["#8a8a86", "#ffffff"])      # building shade (grey) -> sun (white)
im = b.imshow(np.where(s.domain & ~s.roof, win, np.nan), cmap=sunmap, vmin=0, vmax=1, extent=ext)
b.imshow(np.where(s.roof & s.domain, 1, np.nan), cmap=ListedColormap(["#d9d3c4"]), extent=ext)
o = lay[lay.scenario == BAL]
x0, y1 = s.x0 - 430800, s.y1 - 4586800                    # local coords -> image coords (exchange/site_origin.json)
handles = []
for col, sp in zip(CAT, CITY_PALETTE):                     # colour fixed per species (palette order)
    d = o[o.species == sp]
    b.scatter(d.x - x0, s.domain.shape[0] - (y1 - d.y), s=10, c=col, edgecolor="white", linewidth=0.4)
    handles.append(Line2D([], [], marker="o", ls="", color=col, label=f"{sp} ({len(d)})"))
handles.append(Line2D([], [], marker="s", ls="", color="#d9d3c4", label="roofs"))
b.legend(handles=handles, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3)
b.set_title("(b) Winter sun on open ground, balanced layout (s .50, w .25, r .25)", loc="left", color=INK)
b.set_axis_off()
fig.colorbar(im, ax=b, shrink=0.6, label="share of 10–15 h in sun past the buildings, 15 Jan")
fig.tight_layout()
out = ROOT / "notes/figures/tool_v0.png"
fig.savefig(out, dpi=160)
print(out)
