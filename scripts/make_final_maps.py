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
x, y = tr.transform(C["p"]["lon"], C["p"]["lat"])
a.scatter(x, y, s=3, marker="x", color=INK, linewidths=0.4, zorder=4)
a.scatter([], [], s=25, marker="x", color=INK, linewidths=1, label="the 832 planes")
a.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=11)
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
PL = next(p for p in json.load(open("web/public/data/porta-barcelona/meta.json"))["palette"] if p["species"].startswith("Platanus"))
for kind in ("top", "elev", "vsplane"):
    fig, a = plt.subplots(figsize=(12.2, 4.9), facecolor=BG)
    cw, ch = 12.0, 23.0 if kind == "elev" else 15.0
    if kind == "vsplane":
        a.text(0, 9.5, f"dashed: median plane crown, {PL['crown_diam_m']:.1f} m (same trunk class)", fontsize=10, color=MUTED, va="bottom")                      # cell size in metres
    for i, p in enumerate(P):
        col, row = i % 10, i // 10
        x0, y0 = col * cw, -row * ch
        c, d = p["color"], p["crown_diam_m"]
        if kind in ("top", "vsplane"):
            a.add_patch(Circle((x0 + cw / 2, y0 + 6), d / 2, color=c, alpha=0.85, lw=0))
            if kind == "vsplane":
                a.add_patch(Circle((x0 + cw / 2, y0 + 6), PL["crown_diam_m"] / 2, fill=False, ec=INK, lw=0.8, ls=(0, (3, 2))))
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
    a.scatter(kx, ky, s=2, color=GREY, linewidths=0, label="street trees today")
    a.scatter(x, y, s=3, marker="x", color=INK, linewidths=0.4, label="the 832 planes")
    if kind == "class":
        for cl, lab, col in (("free", "free spot", TREE), ("conditional", "conditional spot", WARN)):
            q = sp[sp.spot_class == cl]
            a.scatter(q.x, q.y, s=40, color=col, edgecolor=BG, linewidths=0.6, zorder=5, label=f"{lab} ({len(q)})")
    else:
        q = sp[sp.spot_class == "conditional"]
        for key, lab, col in OBST:
            r = q[q.reasons.str.contains(key)]
            a.scatter(r.x, r.y, s=40, color=col, edgecolor=BG, linewidths=0.6, zorder=5, label=f"{lab} ({len(r)})")
    a.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, fontsize=10, markerscale=1.5)
    a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
    fig.savefig(OUT / f"porta_spots_{kind}.png", dpi=250, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
print("wrote porta_spots_class/obstacle")

# 5. Porta water: flow convergence (from the LiDAR terrain) + flood hotspots (Barcelona Resilience Atlas, index >= 40)
fig, a = plt.subplots(figsize=(8.9, 4.9), facecolor=BG)
bld.plot(ax=a, color="#E2DED5", linewidth=0, zorder=1)
for f, al in (("water.png", 0.9), ("hotspots.png", 0.85)):
    a.imshow(plt.imread(D + f), extent=ext, interpolation="nearest", alpha=al, zorder=2)
a.scatter(x, y, s=3, marker="x", color=INK, linewidths=0.4, zorder=4, label="the 832 planes")
a.scatter([], [], s=60, marker="s", color=RAIN, label="water flow paths (upstream area)")
a.scatter([], [], s=60, marker="s", color=HEAT, label="flood hotspots (hazard index ≥ 40)")
a.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, fontsize=10, markerscale=1.5)
a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
fig.savefig(OUT / "porta_water.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote porta_water")

# 6. context: three Barcelona numbers on maps (replacements 2018-2026; plane share vs the 15% cap; Porta canopy today)
rep = pd.read_csv("databases/barcelona/inventory_replacements.csv", usecols=["x", "y"])
gb = gpd.read_file("web/public/data/barris.geojson").to_crs(25831)
gb["share"] = 100 * gb.planes / gb.street_trees
porta_g = gb[gb.name == "Porta"]
for kind in ("replaced", "planes", "canopy"):
    fig, a = plt.subplots(figsize=(4, 4), facecolor=BG)
    if kind == "replaced":
        gb.plot(ax=a, color="#E2DED5", edgecolor=BG, linewidth=0.4)
        a.scatter(rep.x, rep.y, s=0.4, color=WARN, linewidths=0, alpha=0.7)
    elif kind == "planes":
        gb.plot(ax=a, column="share", cmap=ramp(TREE), edgecolor=BG, linewidth=0.4, vmin=0, vmax=50)
        gb[gb.share > 15].boundary.plot(ax=a, color=INK, linewidth=0.5)
    else:
        bld.plot(ax=a, color="#E2DED5", linewidth=0)                  # Porta itself fills the panel: canopy today
        cimg = np.zeros((gr["H"], gr["W"], 4))
        cimg[C["C"]] = to_rgba(TREE, 0.9)
        a.imshow(cimg, extent=ext, interpolation="nearest", zorder=2)
        a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3])
        loc = a.inset_axes([0.0, 0.72, 0.28, 0.28])                    # small locator: Porta in Barcelona
        gb.plot(ax=loc, color="#D6D1C6", edgecolor=BG, linewidth=0.2)
        porta_g.plot(ax=loc, color=TREE)
        loc.set_aspect("equal"); loc.set_axis_off()
    a.set_aspect("equal"); a.set_axis_off()
    fig.savefig(OUT / f"context_{kind}.png", dpi=250, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
print("wrote context maps; barris with planes > 15% of street trees:", int((gb.share > 15).sum()), "of", len(gb),
      "; city plane share", round(100 * gb.planes.sum() / gb.street_trees.sum(), 1))

# 7. Porta result: the 832 planes replaced, coloured by new species; city practice (one draw of S1b) vs method (balanced)
# NOTE: Porta maps 7-8 need the post-fix web export (claude/diversity-newcrowns @2742cd3 until merged)
TB = json.load(open("web/public/data/porta-barcelona/trees.json"))
PAL = json.load(open("web/public/data/porta-barcelona/meta.json"))["palette"]
px_, py_ = tr.transform(TB["positions"]["lon"], TB["positions"]["lat"])
LAY = (("S1b_obs_0", "City practice", RAIN), ("S4_s0.50_w0.25_r0.25", "Method", TREE))
names = {lid: pd.Series([PAL[i]["species"] for i in TB["layouts"][lid]]) for lid, _, _ in LAY}
tops = []
for lid, _, _ in LAY:
    tops += [sp for sp in names[lid].value_counts().index[:4] if sp not in tops]
CAT = dict(zip(tops, [TREE, RAIN, HEAT, WARN, SAGE, "#7B6A9B", "#C08A5B", "#5E8C8A"]))
fig, axs = plt.subplots(1, 2, figsize=(7.3, 4.9), facecolor=BG)
for a, (lid, t, tc) in zip(axs, LAY):
    bld.plot(ax=a, color="#E2DED5", linewidth=0)
    a.scatter(kx, ky, s=1.5, color=GREY, linewidths=0)
    a.scatter(px_, py_, s=7, c=[CAT.get(sp, "#CFC9BC") for sp in names[lid]], linewidths=0, zorder=4)
    a.set_title(t, fontsize=14, weight="bold", color=tc, loc="left")
    a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
for sp, c in list(CAT.items()) + [("other species", "#CFC9BC")]:
    axs[0].scatter([], [], s=40, color=c, label=sp)
fig.legend(loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.06), prop={"style": "italic", "size": 9})
fig.savefig(OUT / "porta_result_species.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote porta_result_species", {lid: names[lid].value_counts().head(4).to_dict() for lid, _, _ in LAY})

# 8. diversity: all Porta street trees by species, today (planes as they stand) vs after the method's replacement
kept_sp = pd.Series(TB["kept"]["species"])
kx2, ky2 = tr.transform(TB["kept"]["lon"], TB["kept"]["lat"])
STATES = (("Today", ["Platanus x hispanica"] * len(px_), INK), ("Method", list(names["S4_s0.50_w0.25_r0.25"]), TREE))
alls = pd.concat([pd.concat([kept_sp, pd.Series(v)]) for _, v, _ in STATES])
top8 = list(alls.value_counts().index[:7])
CAT2 = dict(zip(top8, [GREY, TREE, RAIN, HEAT, WARN, SAGE, "#7B6A9B"]))
fig, axs = plt.subplots(1, 2, figsize=(7.2, 4.9), facecolor=BG)
for a, (t, planes_sp, tc) in zip(axs, STATES):
    bld.plot(ax=a, color="#E2DED5", linewidth=0)
    a.scatter(kx2, ky2, s=4, c=[CAT2.get(sp, "#CFC9BC") for sp in kept_sp], linewidths=0)
    a.scatter(px_, py_, s=4, c=[CAT2.get(sp, "#CFC9BC") for sp in planes_sp], linewidths=0)
    a.set_title(t, fontsize=14, weight="bold", color=tc, loc="left")
    a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
for sp, c in list(CAT2.items()) + [("other species", "#CFC9BC")]:
    axs[0].scatter([], [], s=40, color=c, label=sp)
fig.legend(loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.06), prop={"style": "italic", "size": 9})
fig.savefig(OUT / "porta_diversity_species.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote porta_diversity_species", top8)

# 9. city practice vs the 2011 sizing rule: new trees in the 26 back-test groups, share planted larger than the sidewalk allows
#    ("none" = sidewalk too narrow for any tree, so any tree is above the rule; same count as notes/tutor_feedback_17nov.md 9a: 36 of 171)
import sys
sys.path.insert(0, ".")
from shade_sponge.layout import SIZE_CLASS, RANK
bt = pd.read_csv("databases/barcelona/backtest_works_guide_capsmall_positions.csv")
bt["cls"] = bt.sp_city.map(SIZE_CLASS)
bt["ok"] = bt.size_class.isin(list(RANK)) & bt.cls.isin(["small", "medium", "large"])
bt["over"] = bt.ok & (bt.cls.map(RANK) > bt.size_class.map(RANK))
grp = bt.groupby("group").agg(x=("x", "mean"), y=("y", "mean"), n=("ok", "sum"), over=("over", "sum"))
fig, a = plt.subplots(figsize=(8.4, 4.9), facecolor=BG)
gb.plot(ax=a, color="#E2DED5", edgecolor=BG, linewidth=0.4)
q = grp[grp.n > 0]
sc = a.scatter(q.x, q.y, s=12 * q.n + 20, c=q.over / q.n, cmap=LinearSegmentedColormap.from_list("ok", [TREE, "#D9CFB8", HEAT]),
               vmin=0, vmax=1, edgecolor=INK, linewidths=0.5, zorder=3)
for lab, c in (("all within the rule", TREE), ("all larger than the sidewalk allows", HEAT)):
    a.scatter([], [], s=80, color=c, edgecolor=INK, linewidths=0.5, label=lab)
a.legend(loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2, frameon=False, fontsize=10)
a.set_aspect("equal"); a.set_axis_off()
fig.savefig(OUT / "city_practice_rule.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote city_practice_rule", int(bt.ok.sum()), int(bt.over.sum()), len(q), "groups")

# 10. S1c: the city's own per-tree plan for 513 Porta planes vs the method on the same positions, by species.
#     Inputs are internal documents kept OUT of the repo (Parcs i Jardins xlsx; the method's per-tree layout from the
#     div9.7 plan run on OMEN, columns tree_id, species). Only the rendered image goes in the deck.
import re
PJ = Path("/mnt/project-files/parcs_jardins")
xl = pd.read_excel(PJ / "Arbrat_Barri_Porta_planned_species.xlsx")
pid = pd.Series(TB["positions"]["tree_id"])
xl = xl[xl.CODI_ELEM.isin(pid) & xl.NOM_SUBST.notna() & (xl.NOM_SUBST != xl.NOM_ESPECIE) & ~xl.NOM_SUBST.str.startswith("Eliminar")]
nm = lambda s: re.sub(r"\s*'[^']*'|\s+\S*®", "", s).strip().replace("Platanus × acerifolia", "Platanus (new clone)")
xy = pd.DataFrame({"x": px_, "y": py_}, index=pid)
PANELS = [("City plan", xl.set_index("CODI_ELEM").NOM_SUBST.map(nm), RAIN)]
mf = PJ / "porta_plan_method_div9.7.csv"
if mf.exists():
    PANELS.append(("Method", pd.read_csv(mf).set_index("tree_id").species.map(nm), TREE))
tops = []
for _, sp, _ in PANELS:
    tops += [k for k in sp.value_counts().index[:5] if k not in tops]
CAT3 = dict(zip(tops, [TREE, RAIN, HEAT, WARN, SAGE, "#7B6A9B", "#C08A5B", "#5E8C8A", "#B5677A", "#6B7F3A"]))
fig, axs = plt.subplots(1, len(PANELS), figsize=(3.65 * len(PANELS), 4.9), facecolor=BG, squeeze=False)
for a, (t, sp, tc) in zip(axs[0], PANELS):
    bld.plot(ax=a, color="#E2DED5", linewidth=0)
    a.scatter(kx, ky, s=1.5, color=GREY, linewidths=0)
    a.scatter(px_, py_, s=1.5, color=GREY, linewidths=0)
    q = xy.loc[sp.index]
    a.scatter(q.x, q.y, s=7, c=[CAT3.get(v, "#CFC9BC") for v in sp], linewidths=0, zorder=4)
    a.set_title(t, fontsize=14, weight="bold", color=tc, loc="left")
    a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3]); a.set_aspect("equal"); a.set_axis_off()
for k, c in list(CAT3.items()) + [("other species", "#CFC9BC")]:
    axs[0][0].scatter([], [], s=40, color=c, label=k)
fig.legend(loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.06), prop={"style": "italic", "size": 9})
fig.savefig(OUT / "porta_cityplan_species.png", dpi=250, bbox_inches="tight", facecolor=BG)
print("wrote porta_cityplan_species", len(xl), "trees;", [p[0] for p in PANELS])
