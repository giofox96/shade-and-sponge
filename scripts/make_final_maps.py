"""Final deck maps in the deck palette (26 Nov 2026):
  slides/final/fig/barri_screening.png  - the site-selection rule on Barcelona's 73 barris (flood, surface heat, planes, eligible)
  slides/final/fig/porta_canopy.png     - Porta canopy today by owner (street / park / square / no inventory) + the 832 planes
Inputs: databases/barcelona/site_selection.csv, web/public/data/barris.geojson, web/public/data/porta/*.
Run from the repo root: python scripts/make_final_maps.py
"""
import json
import runpy
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from pyproj import Transformer

INK, MUTED, GRID, BG = "#2A2622", "#665E4F", "#DCD8CE", "#F2F0EA"
HEAT, RAIN, TREE, WARN, GREY = "#663825", "#283F66", "#3F663E", "#8C6A24", "#A8A293"
SAGE = "#9DB596"   # canopy with no inventory point (also in the deck pie)
FONTS = Path("/mnt/project-files/thesis_layout/Document Fonts")
for f in FONTS.glob("IBMPlexSans-*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({"font.family": "IBM Plex Sans", "font.size": 11, "text.color": INK})
OUT = Path("slides/final/fig")
OUT.mkdir(parents=True, exist_ok=True)


def ramp(c):
    return LinearSegmentedColormap.from_list(c, ["#ECE8DF", c])


# 1. barri screening: the rule (flood, surface heat, planes all above the 60th percentile) and its result
s = pd.read_csv("databases/barcelona/site_selection.csv")
g = gpd.read_file("web/public/data/barris.geojson").rename(columns={"name": "barri"}).merge(s, on="barri", how="left").to_crs(25831)
fig, ax = plt.subplots(1, 4, figsize=(16, 5.2), facecolor=BG)
panels = [("flood_high_share", "Flood hazard", "share of area at high hazard", RAIN, 100, "%"),
          ("lst_anom_C", "Summer surface heat", "°C above the city median", HEAT, 1, " °C"),
          ("plane_per_km2", "Plane trees", "street planes per km²", TREE, 1, "")]
for a, (c, t, sub, col, k, u) in zip(ax, panels):
    v = g[c] * k
    th = s[c].quantile(0.6) * k
    g.assign(v=v).plot(column="v", ax=a, cmap=ramp(col), edgecolor=BG, linewidth=0.4,
                       missing_kwds={"color": GRID}, vmin=max(v.min(), 0) if c != "lst_anom_C" else v.min())
    g[v > th].boundary.plot(ax=a, color=INK, linewidth=0.7)
    a.set_title(t, fontsize=16, weight="bold", color=col, loc="left")
    a.text(0, -0.02, f"{sub}\noutlined: top 40% (> {th:.0f}{u})", transform=a.transAxes, fontsize=11, color=MUTED, va="top")
el = g[g.eligible_q60.fillna(False).astype(bool)]
g.plot(ax=ax[3], color=GRID, edgecolor=BG, linewidth=0.4)
el.plot(ax=ax[3], color="#9FB39E", edgecolor=BG, linewidth=0.4)
porta = g[g.barri == "Porta"]
porta.plot(ax=ax[3], color=TREE, edgecolor=INK, linewidth=0.8)
p = porta.geometry.iloc[0].representative_point()
ax[3].annotate("Porta", (p.x, p.y), xytext=(p.x + 2500, p.y + 1200), fontsize=14, weight="bold", color=TREE,
               arrowprops={"arrowstyle": "-", "color": TREE})
ax[3].set_title("All three high", fontsize=16, weight="bold", color=TREE, loc="left")
ax[3].text(0, -0.02, f"{len(el)} of 72 barris qualify\nPorta ranks first", transform=ax[3].transAxes, fontsize=11, color=MUTED, va="top")
for a in ax:
    a.set_axis_off()
fig.savefig(OUT / "barri_screening.png", dpi=250, bbox_inches="tight", facecolor=BG)
plt.close(fig)

# 2. Porta canopy by owner + the planes
C = runpy.run_path("scripts/canopy_split_porta.py")
D = "web/public/data/porta/"
m, gr = C["m"], C["m"]["grid"]
ext = [gr["x0"], gr["x0"] + gr["W"], gr["y1"] - gr["H"], gr["y1"]]
img = np.zeros((gr["H"], gr["W"], 4))
for X, col in zip(C["parts"].values(), (TREE, RAIN, WARN, SAGE)):
    img[X] = to_rgba(col, 0.9)
tr = Transformer.from_crs(4326, 25831, always_xy=True)
fig, a = plt.subplots(figsize=(7.6, 4.9), facecolor=BG)
bld = gpd.read_file(D + "buildings.geojson").to_crs(25831)
bld.plot(ax=a, color="#E2DED5", linewidth=0)
a.imshow(img, extent=ext, interpolation="nearest", zorder=2)
g[g.barri == "Porta"].boundary.plot(ax=a, color=INK, linewidth=1.0, linestyle="--", zorder=3)
x, y = tr.transform(C["p"]["lon"], C["p"]["lat"])
a.scatter(x, y, s=2.5, color=INK, linewidths=0, zorder=4)
a.scatter([], [], s=20, color=INK, label="the 832 planes")
a.legend(loc="lower right", frameon=False, fontsize=11)
a.set_xlim(ext[0], ext[1])
a.set_ylim(ext[2], ext[3])
a.set_aspect("equal")
a.set_axis_off()
x0 = ext[0] + 40
a.plot([x0, x0 + 200], [ext[2] + 40] * 2, color=INK, lw=2)
a.text(x0 + 100, ext[2] + 55, "200 m", ha="center", fontsize=10)
fig.savefig(OUT / "porta_canopy.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote", OUT / "barri_screening.png", OUT / "porta_canopy.png")

# 3. the 30 species of the Barcelona palette, one scale: (a) crowns from above, (b) elevations with a 1.7 m person
from matplotlib.patches import Circle, Ellipse, Rectangle

P = [p for p in json.load(open("web/public/data/porta-barcelona/meta.json"))["palette"] if p.get("in_palette", True)]
P.sort(key=lambda p: -p["crown_diam_m"])
name = lambda p: p["species"].replace(" x ", " × ").replace(" ", "\n", 1)          # genus on one line, epithet below
for kind in ("top", "elev"):
    fig, a = plt.subplots(figsize=(12.2, 4.9), facecolor=BG)
    cw, ch = 12.0, 19.0 if kind == "elev" else 15.0                      # cell size in metres
    for i, p in enumerate(P):
        col, row = i % 10, i // 10
        x0, y0 = col * cw, -row * ch
        c, d = p["color"], p["crown_diam_m"]
        if kind == "top":
            a.add_patch(Circle((x0 + cw / 2, y0 + 6), d / 2, color=c, alpha=0.85, lw=0))
            a.text(x0 + cw / 2, y0 + 0.4, name(p), ha="center", va="top", fontsize=8, style="italic", linespacing=1.0)
        else:
            gy, h, cb = y0 + 1.5, p["height_m"], p["crown_base_m"]
            cx = x0 + cw / 2 - 1
            a.add_patch(Rectangle((cx - 0.2, gy), 0.4, cb, color=MUTED, lw=0))
            a.add_patch(Ellipse((cx, gy + (h + cb) / 2), d, h - cb, color=c, alpha=0.85, lw=0))
            a.plot([x0 + 0.5, x0 + cw - 0.5], [gy, gy], color=MUTED, lw=0.6)
            px = cx + max(d / 2, 2) + 1.0                                # 1.7 m person
            a.add_patch(Circle((px, gy + 1.55), 0.15, color=INK, lw=0))
            a.plot([px, px], [gy + 0.6, gy + 1.4], color=INK, lw=0.8)
            a.plot([px - 0.2, px, px + 0.2], [gy, gy + 0.6, gy], color=INK, lw=0.8)
            a.text(x0 + cw / 2, gy - 0.4, name(p), ha="center", va="top", fontsize=8, style="italic", linespacing=1.0)
    a.set_aspect("equal")
    a.autoscale_view()
    a.set_axis_off()
    fig.savefig(OUT / f"species30_{kind}.png", dpi=250, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
print("wrote species30_top/elev")

# 4. Porta spots: (a) by class, (b) conditional spots by what is in the way (street furniture from Open Data BCN / OSM)
T = json.load(open(D + "trees.json"))
sp = pd.DataFrame(T["spots"])
sp["x"], sp["y"] = tr.transform(sp.lon.values, sp.lat.values)
kx, ky = tr.transform(T["kept"]["lon"], T["kept"]["lat"])
OBST = [("sign_support", "traffic sign", RAIN), ("lamp", "street lamp", WARN), ("crossing", "pedestrian crossing", HEAT),
        ("bollard", "bollard", MUTED)]
for kind in ("class", "obstacle"):
    fig, a = plt.subplots(figsize=(8.9, 4.9), facecolor=BG)
    bld.plot(ax=a, color="#E2DED5", linewidth=0)
    g[g.barri == "Porta"].boundary.plot(ax=a, color=INK, linewidth=1.0, linestyle="--")
    a.scatter(kx, ky, s=2, color=GREY, linewidths=0, label="street trees today")
    a.scatter(x, y, s=2, color=INK, linewidths=0, label="the 832 planes")
    if kind == "class":
        for cl, lab, col in (("free", "free spot", TREE), ("conditional", "conditional spot", WARN)):
            q = sp[sp.spot_class == cl]
            a.scatter(q.x, q.y, s=40, color=col, edgecolor=BG, linewidths=0.6, zorder=5, label=f"{lab} ({len(q)})")
    else:
        q = sp[sp.spot_class == "conditional"]
        for key, lab, col in OBST:
            r = q[q.reasons.str.contains(key)]
            a.scatter(r.x, r.y, s=40, color=col, edgecolor=BG, linewidths=0.6, zorder=5, label=f"{lab} ({len(r)})")
    a.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=11, markerscale=1.2)
    a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
    fig.savefig(OUT / f"porta_spots_{kind}.png", dpi=250, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
print("wrote porta_spots_class/obstacle")

# 5. Porta water: flow convergence (from the LiDAR terrain) + flood hotspots (Barcelona Resilience Atlas, index >= 40)
fig, a = plt.subplots(figsize=(8.9, 4.9), facecolor=BG)
bld.plot(ax=a, color="#E2DED5", linewidth=0, zorder=1)
for f, al in (("water.png", 0.9), ("hotspots.png", 0.85)):
    a.imshow(plt.imread(D + f), extent=ext, interpolation="nearest", alpha=al, zorder=2)
g[g.barri == "Porta"].boundary.plot(ax=a, color=INK, linewidth=1.0, linestyle="--", zorder=3)
a.scatter(x, y, s=2, color=INK, linewidths=0, zorder=4, label="the 832 planes")
a.scatter([], [], s=60, marker="s", color=RAIN, label="water flow paths (upstream area)")
a.scatter([], [], s=60, marker="s", color=HEAT, label="flood hotspots (hazard index ≥ 40)")
a.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=11)
a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
fig.savefig(OUT / "porta_water.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote porta_water")
