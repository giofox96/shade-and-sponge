"""Back-test deck: the city's plantings in real street works vs the method's choice at the same positions
(scripts/backtest_works.py -> databases/barcelona/backtest_works*.csv). Maps are rendered images (slides/fig_backtest/),
text, cards and charts are native PowerPoint objects (make_deck_editable.py helpers).
Output: slides/backtest_works.pptx. Run from scripts/: python make_backtest_deck.py [folder with the two CSVs]
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import shapely
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Circle, Patch  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.chart.data import CategoryChartData  # noqa: E402
from pptx.enum.chart import XL_CHART_TYPE  # noqa: E402
from pptx.util import Inches  # noqa: E402
from make_deck_editable import (text, box, head, source, picture, style_chart, quiet_axes, card, rgb, tint,  # noqa: E402
                                W, H, M, BG, ROOT, INK, MUTED, TREE, RAIN, WARN)

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "databases/barcelona"
FIG = ROOT / "slides/fig_backtest"
FIG.mkdir(exist_ok=True)
RUN = "_guide_capsmall"        # 2011 guide sizing on measured sidewalks, "small" species capped at the guide's limits
RUNS = (("", "Our façade test", "crown radius ≤ distance to the façade raster"),
        ("_guide", "2011 guide only", "sidewalk width → size class"),
        (RUN, "Guide + small sizes capped", "small species ≤ 4 m crown, ≤ 6 m height"))
r = pd.read_csv(DB / f"backtest_works{RUN}.csv")
p = pd.read_csv(DB / f"backtest_works{RUN}_positions.csv")
r = r.merge(pd.read_csv(DB / "backtest_works_sources.csv")[["group", "street", "works_status", "evidence", "url"]], how="left")
DOC = r.works_status.isin(["confirmed", "compatible"])
ORIGIN = json.load(open(ROOT / "exchange/site_origin.json"))
SPCOL = ["#3F663E", "#283F66", "#8C6A24", "#663825", "#6B8F5E", "#5B7DB1", "#C29A4A", "#9C5B43", "#7E6B8F", "#4F8A8B"]
for k in ("before", "city", "method_bal"):                 # summer shade per replaced position, m²·h per tree
    r[f"pt_{k}"] = (r[f"shade_summer_{k}"] - r.shade_summer_none) / r.n
r["gain"] = 100 * (r.pt_method_bal / r.pt_city - 1)     # method vs city, % (the % of the removed trees' shade explodes
                                                        # where the removed trees were small, so it is not the headline)
r["hot_vs_city"] = r.runoff_hot_method_bal - r.runoff_hot_city
r["tot_vs_city"] = r.runoff_method_bal - r.runoff_city
r["label"] = r.barri.str.replace("-", " ").str.title().str.replace(" I ", " i ").str.replace(" De ", " de ").str.replace(" L ", " l'") \
    .str.replace(" Del ", " del ").str.replace(" La ", " la ").str.replace(" Els ", " els ") + " " + r.quarter.str[2:4].radd("’")
SRC = ("Ajuntament de Barcelona, Open Data BCN: street-tree inventory, 35 quarterly releases 2018–2026 (CC BY 4.0); ICGC LiDAR "
       "2021–2022; Gestió de l'arbrat viari de Barcelona (2011); Pla director de l'arbrat 2017–2037.")


MIN_SP = 30                                              # plantings a species needs for its survival to be read
import backtest_survival  # noqa: E402
inv_norm = backtest_survival.ih_norm()


def short(sp):
    return " ".join(sp.split()[:3] if sp.split()[1:2] in (["×"], ["x"]) else sp.split()[:2])   # full genus + species


# ---------------------------------------------------------------- figures
def overview():
    g = gpd.read_file(ROOT / "web/public/data/barris.geojson").to_crs(25831)
    fig, ax = plt.subplots(figsize=(7, 6.2), dpi=200)
    g.plot(ax=ax, color="#E6E2D8", edgecolor="#FFFFFF", linewidth=0.6)
    s = ax.scatter(r.x, r.y, s=r.n * 9, c=np.clip(r.gain, -100, 100), cmap="BrBG", vmin=-100, vmax=100,
                   edgecolor=INK, linewidth=0.6, zorder=3)
    ax.set_axis_off()
    ax.set_aspect("equal")
    cb = fig.colorbar(s, ax=ax, shrink=0.55, pad=0.01)
    cb.set_label("Method vs city, summer shade (%)", color=INK, fontsize=9)
    cb.outline.set_visible(False)
    for n in (10, 20, 30):
        ax.scatter([], [], s=n * 9, color="none", edgecolor=INK, label=f"{n} trees")
    ax.legend(loc="lower right", frameon=False, fontsize=8, labelspacing=1.4, borderpad=1.2)
    fig.tight_layout()
    fig.savefig(FIG / "overview.png", facecolor=BG)
    plt.close(fig)


def context(slug, box_):
    x0, y0, x1, y1 = box_
    if slug == "porta":
        b = gpd.read_file(ROOT / "exchange/to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
        b = b.set_geometry(b.translate(ORIGIN["origin_x"], ORIGIN["origin_y"]))
        t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
        t["x"], t["y"] = t.x + ORIGIN["origin_x"], t.y + ORIGIN["origin_y"]
    else:
        b = gpd.read_file(ROOT / f"databases/barcelona/barris/{slug}/buildings.geojson").to_crs(25831)
        t = pd.read_csv(ROOT / f"databases/barcelona/barris/{slug}/trees_lidar.csv")
    return b.cx[x0:x1, y0:y1], t[t.x.between(x0, x1) & t.y.between(y0, y1)]


ROADS = DB / "backtest_map_roads.geojson"          # kerb lines, 1:1000 map (scripts/backtest_map_roads.py)
roads = gpd.read_file(ROADS) if ROADS.exists() else None


def street_labels(trees, xy, box_):
    """(name, x, y, angle, main) for streets with >= 4 inventory trees in the box; main = the street of the positions."""
    t = trees.dropna(subset=["street"])
    if t.empty:
        return []
    d = np.min(np.hypot(t.x.values[:, None] - xy[:, 0], t.y.values[:, None] - xy[:, 1]), 1)
    main = t[d < 3].street.mode()
    out = []
    for st, g in t.groupby("street"):
        if len(g) < 4:
            continue
        c = g[["x", "y"]].values - g[["x", "y"]].values.mean(0)
        v = np.linalg.svd(c, full_matrices=False)[2][0]
        a = np.degrees(np.arctan2(v[1], v[0]))
        a = a - 180 if a > 90 else a + 180 if a < -90 else a
        x0, y0, x1, y1 = box_
        mx = my = 0.2 * (x1 - x0)       # label at the street tree farthest from the positions, kept inside
        inner = g[g.x.between(x0 + mx, x1 - mx) & g.y.between(y0 + my, y1 - my)]
        inner = inner if len(inner) else g
        far = inner.iloc[np.argmax(np.min(np.hypot(inner.x.values[:, None] - xy[:, 0], inner.y.values[:, None] - xy[:, 1]), 1))]
        name = st.replace("C\\ ", "C. ").replace("Av\\ ", "Av. ").replace("Pg\\ ", "Pg. ").replace("Pl\\ ", "Pl. ") \
            .replace("G.V. Corts Catalanes", "Gran Via").replace("\\", ".").replace("Av ", "Av. ")
        out.append((name, far.x, far.y, a, len(main) and st == main.iloc[0]))
    return out


def area_map(row, fname):
    q = p[p.group == row.group]
    pad = 30
    x0, x1, y0, y1 = q.x.min() - pad, q.x.max() + pad, q.y.min() - pad, q.y.max() + pad
    side = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bb = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
    bld, trees = context(row.barri, bb)
    xy = q[["x", "y"]].values
    labels = street_labels(trees, xy, bb)
    kerb = roads[roads.group == row.group] if roads is not None else None
    road_fill = None                     # carriageway = gaps between kerb lines that touch no building (sidewalks do)
    if kerb is not None and len(kerb):
        cut = shapely.union_all(list(bld.geometry) + list(kerb.geometry.buffer(0.2)))
        faces = gpd.GeoSeries(shapely.get_parts(shapely.box(*bb).difference(cut)))
        near = shapely.union_all(list(bld.geometry.buffer(1.0)))
        planted = shapely.union_all(shapely.points(np.vstack([trees[["x", "y"]].values, xy])).tolist())  # trees stand off it
        road_fill = faces[(faces.area > 20) & ~faces.intersects(near) & ~faces.intersects(planted)]
    near = np.min(np.hypot(trees.x.values[:, None] - xy[:, 0], trees.y.values[:, None] - xy[:, 1]), 1) > 2 if len(trees) else []
    trees = trees[near] if len(trees) else trees
    allsp = pd.concat([q.sp_before, q.sp_city, q.sp_method_bal]).value_counts().index
    col = {s: SPCOL[i % len(SPCOL)] for i, s in enumerate(allsp)}
    panels = (("before", "Removed", row.pt_before), ("city", "City planted", row.pt_city),
              ("method_bal", "Method", row.pt_method_bal))
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.9), dpi=200)
    for ax, (k, ttl, pct) in zip(axes, panels):
        if road_fill is not None and len(road_fill):
            road_fill.plot(ax=ax, color="#E3DFD6", edgecolor="none", zorder=0)
        if kerb is not None and len(kerb):
            kerb.plot(ax=ax, color="#9A9488", linewidth=0.35, alpha=0.5, zorder=0)
        bld.plot(ax=ax, color="#D3CEC2", edgecolor="none")
        for x, y, d in zip(trees.x, trees.y, trees.crown_diam_m):
            ax.add_patch(Circle((x, y), max(d, 1) / 2, color="#B9B4A8", alpha=0.45, lw=0))
        for x, y, s, d in zip(q.x, q.y, q[f"sp_{k}"], q[f"crown_{k}"]):
            ax.add_patch(Circle((x, y), d / 2, facecolor=col[s], alpha=0.85, edgecolor="white", lw=0.6))
        for name, x, y, a, main in labels:
            ax.text(x, y, name, rotation=a, rotation_mode="anchor", ha="center", va="center", fontsize=7.5,
                    color=MUTED, zorder=5,
                    bbox=dict(facecolor=BG, edgecolor="none", alpha=0.75, pad=1.2))
        ax.set_xlim(bb[0], bb[2])
        ax.set_ylim(bb[1], bb[3])
        ax.set_aspect("equal")
        ax.set_axis_off()
        sub = f"  ·  {pct:,.0f} m²·h per tree"
        ax.set_title(ttl + sub, loc="left", fontsize=13, color=INK, fontweight="bold")
        cnt = q[f"sp_{k}"].value_counts()
        ax.legend(handles=[Patch(color=col[s], label=f"{short(s)} ({n})") for s, n in cnt.head(4).items()] +
                  ([Patch(color="#999999", label=f"other ({cnt.iloc[4:].sum()})")] if len(cnt) > 4 else []),
                  loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=2, frameon=False, fontsize=9.5)
    axes[0].plot([bb[0] + 5, bb[0] + 25], [bb[1] + 5] * 2, color=INK, lw=2)
    axes[0].text(bb[0] + 15, bb[1] + 7, "20 m", ha="center", fontsize=8, color=INK)
    fig.tight_layout()
    fig.savefig(FIG / fname, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# ---------------------------------------------------------------- slides
def s_title(s):
    box(s, 0, 0, W, H, "#283F2A", radius=0)
    text(s, M + 0.3, 2.4, W - 2 * M, 1.0, "Back-testing the method on real tree replacements", 40, "#F2F0EA", True)
    text(s, M + 0.3, 3.5, W - 2 * M, 1.0, f"{len(r)} groups of replacements in Barcelona, 2018–2026, {DOC.sum()} of them in documented street works: "
         "what the city planted, and what the method would have chosen at the same positions", 20, "#B3BAB9")


def s_test(s):
    head(s, "The test: same positions, same tree size, two choices",
         "Groups found in the city's own inventory: ten or more trees changed species in one quarter within 25 m")
    steps = [("1  Find the replacements", f"{len(r)} groups that look like plantings (new trees in the smallest trunk class), "
              f"in barris with LiDAR crowns; {DOC.sum()} match documented street works"),
             ("2  Freeze everything else", "Every other street tree stays as measured; only the replaced positions change"),
             ("3  Two answers per position", "City: the species it actually planted. Method: the optimiser, with the 15% cap "
              "and the 2011 guide's sidewalk-width sizing"),
             ("4  Score at equal size", "All species at the same trunk class, so young vs mature does not decide. "
              "Summer shade 12–17 h, storm runoff")]
    for k, (a, b) in enumerate(steps):
        y = 1.65 + k * 1.2
        box(s, M, y, 5.6, 1.05, tint(TREE, 0.08))
        text(s, M + 0.25, y + 0.12, 5.1, 0.4, a, 16, TREE, True)
        text(s, M + 0.25, y + 0.5, 5.1, 0.6, b, 13, INK)
    picture(s, FIG / "overview.png", 6.6, 1.45, 6.2, crop_top=0.0)
    source(s, SRC)


def s_works(s):
    head(s, "Which groups are real street works?", "Searched in the Ajuntament's works notices, district councils and the press")
    d = r[DOC].sort_values(["works_status", "quarter"], ascending=[False, True])
    xs, ws = [M, M + 3.3, M + 4.4, M + 5.9, M + 7.8], [3.2, 1.0, 1.4, 1.8, 4.4]
    for x, w, h in zip(xs, ws, ("Street", "Trees", "Works", "Summer shade, m²·h per tree", "")):
        text(s, x, 1.55, w, 0.3, h.upper(), 11, MUTED, True)
    for k, q in enumerate(d.itertuples()):
        y = 1.95 + k * 0.5
        if k % 2 == 0:
            box(s, M - 0.1, y - 0.06, 7.6, 0.48, tint(MUTED, 0.06), radius=0)
        c = TREE if q.works_status == "confirmed" else WARN
        text(s, xs[0], y, ws[0], 0.4, f"{q.street} ({q.quarter[:4]})", 14, INK, True)
        text(s, xs[1], y, ws[1], 0.4, str(q.n), 14, INK)
        text(s, xs[2], y, ws[2], 0.4, q.works_status, 13, c, True)
        text(s, xs[3], y, ws[3], 0.4, [[("city ", {"color": MUTED}), (f"{q.pt_city:.0f}", {"bold": True}),
                                        ("  method ", {"color": MUTED}), (f"{q.pt_method_bal:.0f}", {"bold": True})]], 14, INK)
    box(s, 8.75, 1.55, 4.05, 4.6, tint(RAIN, 0.08))
    text(s, 9.0, 1.7, 3.6, 4.4, [
        [("Confirmed: ", {"bold": True, "color": TREE}), ("the source names the street works and the tree change.", {})],
        [("Compatible: ", {"bold": True, "color": WARN}), ("works in the right street and period; the source does not mention trees.", {})],
        [(f"The other {(~DOC).sum()} groups: ", {"bold": True}), ("no works found. They fit the city's replacement campaigns, which "
                                                          "remove fragile or invasive species such as Ulmus pumila and Robinia.", {})],
        [("Where the works are documented, ", {"bold": True}), ("the method wins clearly on the wide streets; on Piquer, "
                                                              "a narrow street where only small trees fit, the gap is small either way.", {})]], 13, INK)
    source(s, "Betevé, 3 Mar 2022 (carrer de Piquer) and 21 Sep 2015 (replacement campaign); Ajuntament de Barcelona: works notice Av. "
              "Rio de Janeiro (Dec 2022), Obres news 8 Jan 2026 (Gran Via, Trambesòs), Sant Martí project sheet carrer de Bassols (2018); "
              "Consell de Barri de Porta, 12 Nov 2025.")


def s_summary(s):
    head(s, "Summer shade per new tree: city vs method",
         "m²·h of summer shade (12–17 h) per replaced position, at equal trunk size; one bar pair per group")
    d = r.sort_values("gain")
    cd = CategoryChartData()
    cd.categories = list(d.label)
    cd.add_series("City planted", list(d.pt_city.round(0)))
    cd.add_series("Method", list(d.pt_method_bal.round(0)))
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(M), Inches(1.45), Inches(8.3), Inches(5.55), cd).chart
    style_chart(ch, [WARN, TREE], labels=False, size=9)
    quiet_axes(ch, 0, gridlines=True)
    ch.plots[0].gap_width, ch.plots[0].overlap = 40, 0
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '#,##0', False
    wins = int((r.gain > 1).sum())
    card(s, 9.2, 1.55, 3.6, 1.6, f"{r.pt_city.median():,.0f} → {r.pt_method_bal.median():,.0f}",
         "m²·h per tree, median: city → method", TREE, 30, 13)
    card(s, 9.2, 3.3, 3.6, 1.6, f"{wins} of {len(r)}", "areas where the method gives more summer shade", TREE, 30, 13)
    tot = 100 * ((r.pt_method_bal * r.n).sum() / (r.pt_city * r.n).sum() - 1)
    card(s, 9.2, 5.05, 3.6, 1.6, f"{tot:+.0f}%", f"all {r.n.sum()} positions together, method vs city", TREE, 30, 13)
    source(s, SRC)


def s_rules(s):
    head(s, "Which rule decides the result?", "The same back-test under three readings of the planting rules; summer shade per tree")
    for k, (tag, ttl, how) in enumerate(RUNS):
        d = pd.read_csv(DB / f"backtest_works{tag}.csv")
        pc, pm = [(d[f"shade_summer_{c}"] - d.shade_summer_none) / d.n for c in ("city", "method_bal")]
        x, c = M + k * 4.15, TREE if tag == RUN else MUTED
        box(s, x, 1.55, 3.9, 3.6, tint(c, 0.10))
        text(s, x + 0.25, 1.7, 3.4, 0.4, ttl, 17, c, True)
        text(s, x + 0.25, 2.1, 3.4, 0.4, how, 12, MUTED)
        text(s, x + 0.25, 2.7, 3.4, 2.4, [
            [(f"{pm.median() / pc.median() - 1:+.0%}", {"bold": True, "size": 30, "color": c}), ("  median per tree", {})],
            [(f"{int((pm > pc * 1.01).sum())} of {len(d)}", {"bold": True, "size": 30, "color": c}), ("  areas won", {})],
            [(f"{(pm * d.n).sum() / (pc * d.n).sum() - 1:+.0%}", {"bold": True, "size": 30, "color": c}),
             ("  all positions", {})]], 13, INK)
    text(s, M, 5.45, W - 2 * M, 1.2, [
        [("Our first façade test was stricter than the city's rule: ", {"bold": True}),
         ("on narrow streets with balconies it left only the smallest species, so the method lost there.", {})],
        [("Small species are capped ", {"bold": True}), ("because the LiDAR sizes of a few Hibiscus include canopy above them. "
                                                         "The result shown in this deck is the right-hand one.", {})]], 13, INK)
    source(s, "Gestió de l'arbrat viari de Barcelona (2011): size classes and sidewalk widths. Open Data BCN street-tree inventory "
              "(CC BY 4.0); ICGC LiDAR 2021–2022.")


def s_runoff(s):
    head(s, "Runoff: the check is do-no-harm", "Storm T = 2 yr, 1 h; method minus city in each group")
    worse = r[r.hot_vs_city > 0.05]
    card(s, M, 1.6, 3.9, 2.0, f"{len(r) - len(worse)} of {len(r)}", "areas where the method sends no more water to a flood hotspot "
         "than the city's planting", RAIN, 34, 14)
    card(s, M + 4.15, 1.6, 3.9, 2.0, f"{r.tot_vs_city.median():+.1f} m³", "median change in total runoff of a group's area", RAIN, 34, 14)
    card(s, M + 8.3, 1.6, 3.7, 2.0, f"{r.hot_vs_city.max():+.1f} m³", "largest increase towards a hotspot", RAIN, 34, 14)
    text(s, M, 4.1, W - 2 * M, 2.0, [
        "Runoff differences come from crown size alone: every species stores the same water per unit of leaf area.",
        "They are small next to what the model resolves, so runoff stays a check, not an objective."], 16, INK)
    source(s, "PDISBA design storms (Ajuntament de Barcelona); Anys & Weiler 2024 (interception); USDA NRCS TR-55 (curve numbers).")


def s_map(key, row, ttl, sub):
    def build(s):
        head(s, ttl, sub)
        picture(s, FIG / f"map_{key}.png", M + 0.1, 1.5, W - 2 * M - 0.2, crop_top=0.0)
        ev = f"Works: {row.evidence}. " if row.works_status in ("confirmed", "compatible") else ""
        source(s, ev + "Buildings: Mapa base topogràfic 1:1000 (Ajuntament de Barcelona). Trees: Open Data BCN; crowns at equal "
                  "trunk size from ICGC LiDAR. Grey = trees kept.")
    return build


def s_species(s):
    head(s, "What differs is the species, not the number of trees", "All positions of the 27 groups, counted together")
    for k, (col, ttl, c) in enumerate((("sp_before", "Removed", MUTED), ("sp_city", "City planted", WARN),
                                       ("sp_method_bal", "Method", TREE))):
        x = M + k * 4.15
        box(s, x, 1.55, 3.9, 4.9, tint(c, 0.08))
        text(s, x + 0.25, 1.7, 3.4, 0.4, ttl, 17, c, True)
        v = p[col].value_counts()
        rows = [[(f"{n}  ", {"bold": True}), (sp, {"italic": True})] for sp, n in v.head(6).items()]
        if len(v) > 6:
            rows.append([(f"{v.iloc[6:].sum()}  ", {"bold": True}), (f"{len(v) - 6} other species", {})])
        text(s, x + 0.25, 2.25, 3.4, 4.0, rows, 14, INK)
    source(s, SRC)


def s_survival(s):
    head(s, "Do the city's new trees survive?",
         "Share of planted trees still standing with the same species in the 2026 Q3 inventory, by years since planting")
    a = pd.read_csv(DB / "backtest_survival_age.csv")
    sp = pd.read_csv(DB / "backtest_survival_species.csv").set_index("species")
    ages = [x for x in a.age.unique() if x != "all"]
    cd = CategoryChartData()
    cd.categories = [f"{x} yr" for x in ages]
    for k, lab in (("all replacements", "All city replacements"), ("back-test", "The 27 groups")):
        cd.add_series(lab, [float(a[(a.set == k) & (a.age == x)].alive.iloc[0]) for x in ages])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(M), Inches(1.55), Inches(7.6), Inches(5.0), cd).chart
    style_chart(ch, [MUTED, WARN], fmt='0%', size=11)
    quiet_axes(ch, 0, 1)
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0%', False
    tot = a[a.age == "all"].set_index("set")
    card(s, 8.6, 1.55, 4.2, 1.6, f"{tot.alive['back-test']:.0%}", f"of the {tot.n['back-test']} trees the city planted in the "
         "27 groups still stand", WARN, 30, 13)
    n_ok = sp.n >= MIN_SP                                   # age-standardised survival of the species each layout uses
    surv = {k: p[k].map(inv_norm).map(sp.alive_std.where(n_ok)) for k in ("sp_city", "sp_method_bal")}
    card(s, 8.6, 3.3, 4.2, 1.6, f"{surv['sp_city'].mean():.0%} vs {surv['sp_method_bal'].mean():.0%}",
         "expected survival of the species chosen: city vs method", TREE, 30, 13)
    text(s, 8.6, 5.1, 4.2, 1.5, f"Expected survival = the species' share still standing over all city replacements, at a "
         f"standard age mix. Species with fewer than {MIN_SP} plantings are left out "
         f"({surv['sp_method_bal'].isna().mean():.0%} of the method's positions).", 11, MUTED)
    source(s, "Ajuntament de Barcelona, Open Data BCN: street-tree inventory, quarterly releases 2018–2026 (CC BY 4.0). "
              "A missing tree may be a re-survey, not a death.")


def s_limits(s):
    head(s, "Limits of this back-test")
    text(s, M, 1.4, W - 2 * M, 5.2, [
        [("Equal size. ", {"bold": True}), ("Removed, planted and chosen trees are all scored at the same trunk class. "
                                            "It compares species, not the life cycle: a young tree gives less shade for years.", {})],
        [("Works not always proven. ", {"bold": True}), (f"{(~DOC).sum()} of {len(r)} groups have no documented street works: "
                                                         "they may be replacement campaigns. The inventory records what was planted either way.", {})],
        [("Only the replaced positions. ", {"bold": True}), ("Trees removed without a replacement, or added at new spots, "
                                                             "are not in the decision set.", {})],
        [("Different rules. ", {"bold": True}), ("The method obeys the 2011 sizing guide (not its 0.5 m balcony clearance); the city's planting is "
                                                 "scored as planted, even where it does not.", {})],
        [("Unknown reasons. ", {"bold": True}), ("The inventory says what changed, not why: pests, drought or a design choice "
                                                 "may have ruled species out.", {})],
        [("Missing crowns. ", {"bold": True}), ("Species with too few LiDAR-measured trees take the city's average crown; "
                                                "for the shrubby Tecoma stans (Poble-sec 2019) this overstates the city's shade. "
                                                "Small species are capped at the guide's adult size.", {})],
        [("Proxy. ", {"bold": True}), ("Heat is the shade proxy; full UTCI only on selected layouts (Ladybug, Infrared City).", {})]],
        17, INK)
    source(s, SRC)


SAY = {
    "works": "Are these real street works? For six groups I found the works in the city's notices or the press: Piquer is "
             "confirmed, with the tree change named; Rio de Janeiro, Gran Via and Bassols are compatible. For the other 21 I found no "
             "works: they are probably replacement campaigns. Either way the inventory records what the city actually planted.",
    "test": "To test the method against reality, I looked for groups of replacements in the city's own tree inventory: places where ten or "
            "more trees changed species in the same quarter. I kept the ones that look like real plantings, and where I have LiDAR "
            "crowns. For each one I froze every other tree, and gave the same positions two answers: what the city actually "
            "planted, and what the method would have chosen under the city's rules.",
    "summary": "This is the result: summer shade per new tree, at the same trunk size, the city's choice in grey and the "
               "method's in green. The method gives more shade in most areas. Where it loses, the sidewalks are narrow and "
               "only small species fit, so both choices give little shade and the gap is small. Where it wins, the gap is large, "
               "for example in Porta, where the city replaced poplars with ash.",
    "rules": "Does the result depend on how I read the rules? My first version used a façade test stricter than the city's "
             "own guide, and on narrow streets with balconies it left only the smallest species. With the guide's rule alone, "
             "and with small species held to the guide's adult size, the method still wins in most areas, by about the same "
             "margin overall.",
    "runoff": "On runoff the method has to do no harm. These are the differences towards the flood hotspots.",
    "species": "What differs is the species mix: here are the species removed, planted by the city, and chosen by the method.",
    "survival": "A real-world check no simulation gives: did the city's new trees survive? Nine in ten of the trees "
                "planted in these groups still stand, with the same species, in the latest inventory; across all city "
                "replacements it is eight in ten, falling to about seven in ten after five years. The species the method chooses "
                "do not survive worse than the city's: on the species with enough plantings to judge, they do slightly better.",
    "limits": "The main limit: all trees are compared at the same size, so this compares species, not the years a young tree "
              "needs to grow.",
}


def build():
    overview()
    home = r[(r.barri == "porta") & DOC].sort_values("n").iloc[-1]
    rest = r[(r.group != home.group) & DOC]               # examples only from groups with documented works
    best, worst = rest.sort_values("gain").iloc[-1], rest.sort_values(["gain", "n"], ascending=[True, False]).iloc[0]
    ex = [("home", home), ("best", best), ("worst", worst)]
    for k, row in ex:
        area_map(row, f"map_{k}.png")
        SAY[f"map_{k}"] = (f"{row.label}: {row.n} trees of {row.top_before} replaced in {row.quarter}. On the left what was removed, "
                           f"in the middle what the city planted, mostly {row.top_city}, on the right what the method would have "
                           f"chosen, mostly {row.top_method_bal}. Per tree: {row.pt_before:.0f}, {row.pt_city:.0f} and "
                           f"{row.pt_method_bal:.0f} square-metre-hours of summer shade.")

    def sub(row):
        return (f"{row.n} trees, {row.quarter}: {short(row.top_before)} → city {short(row.top_city)}, "
                f"method mostly {short(row.top_method_bal)}")
    slides = [(None, s_title), ("test", s_test), ("works", s_works), ("summary", s_summary), ("rules", s_rules)]
    slides += [(f"map_{k}", s_map(k, row, t + row.label, sub(row))) for (k, row), t in
               zip(ex, ("Works in ", "Works, method wins: ", "Works, city wins: "))]
    slides += [("runoff", s_runoff), ("species", s_species), ("survival", s_survival), ("limits", s_limits)]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for key, fn in slides:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        s.notes_slide.notes_text_frame.text = SAY.get(key, "")
    out = ROOT / "slides/backtest_works.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT), f"({len(slides)} slides)")


if __name__ == "__main__":
    build()
