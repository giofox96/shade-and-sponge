"""Map of Porta's 832 plane positions by sidewalk size class (2011 guide), over the 1:1000 facade and road lines.

Input: databases/barcelona/porta_sidewalk_width.csv, exchange/to_gh/porta_trees_lidar.csv, cached WMS tiles (optional)
Output: notes/figures/porta_sidewalk_classes.png (used by slides/fig_v6/v6_09_sidewalk.svg)
"""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import porta_sidewalk_width as sw

COL = {"large": "#3B7F4A", "medium": "#2F6DB5", "small": "#D9622B", "none": "#B91C1C", "check": "#9CA3AF"}
LAB = {"large": "large (> 6 m)", "medium": "medium (3.5–6 m)", "small": "small (< 3.5 m, Pyrus only)",
       "none": "no tree (< 2.5 m)", "check": "median, boulevard, plaza\n(no size filter)"}

o = json.load(open(sw.ROOT / "exchange/site_origin.json"))
t = pd.read_csv(sw.ROOT / "exchange/to_gh/porta_trees_lidar.csv")[["tree_id", "x", "y"]]
w = pd.read_csv(sw.ROOT / "databases/barcelona/porta_sidewalk_width.csv").merge(t, on="tree_id")
p = w[w.is_plane].copy()
p["X"], p["Y"] = p.x + o["origin_x"], p.y + o["origin_y"]

fig, ax = plt.subplots(figsize=(12, 7))
if sw.SVG.exists() and any(sw.SVG.iterdir()):
    xs = np.arange(np.floor((w.x.min() + o["origin_x"] - sw.RAY) / sw.TILE) * sw.TILE, w.x.max() + o["origin_x"] + sw.RAY, sw.TILE)
    ys = np.arange(np.floor((w.y.min() + o["origin_y"] - sw.RAY) / sw.TILE) * sw.TILE, w.y.max() + o["origin_y"] + sw.RAY, sw.TILE)
    for layer, c in (("road", "#D1D5DB"), ("facade", "#9CA3AF")):
        for g in sw.lines(layer, xs, ys):
            ax.plot(*g.xy, color=c, lw=0.4)
for k in COL:
    s = p[p.size_class == k]
    ax.scatter(s.X, s.Y, s=9, color=COL[k], label=f"{LAB[k]}: {len(s)}", zorder=3)
ax.set_xlim(p.X.min() - 40, p.X.max() + 40); ax.set_ylim(p.Y.min() - 40, p.Y.max() + 40)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=10, frameon=False, markerscale=2, title="Porta plane positions, sidewalk class", title_fontsize=11)
fig.tight_layout()
fig.savefig(sw.ROOT / "notes/figures/porta_sidewalk_classes.png", dpi=200, bbox_inches="tight")
print(p.size_class.value_counts().to_dict())
