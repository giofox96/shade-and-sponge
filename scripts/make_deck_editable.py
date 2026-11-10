"""Editable 10 Nov deck: the same 26 slides as make_slides_v7.py, but text, cards, tables and charts are native
PowerPoint objects (python-pptx): flowcharts are boxes + connectors, the city map is one freeform per barri, every chart is
a native chart. Only the title photo and the B5 sidewalk map (a raster map) are pictures. Speaker notes = the "Say" scripts of slides/outline_10nov.md.
Numbers come from the same CSVs as make_slides_v7.py, make_results_v7.py and make_citywide_v7.py.
Output: slides/shade_and_sponge_10nov_editable.pptx. Run from scripts/: python make_deck_editable.py
"""
import io
import re
import numpy as np
import pandas as pd
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
import make_results_v7 as rv
import make_citywide_v7 as cw
from make_infographics import ROOT, INK, MUTED, GRID, BG, HEAT, RAIN, TREE, WARN

DB = ROOT / "databases/barcelona"
FONT = "Calibri"
W, H, M = 13.333, 7.5, 0.55                     # slide size and side margin, inches
WHITE = "#FFFFFF"


def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


def tint(h, op):
    """Colour h at opacity op over the slide background (no alpha in the file, so it prints the same everywhere)."""
    a, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)], [int(BG[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(op * x + (1 - op) * y):02X}" for x, y in zip(a, b))


def text(s, x, y, w, h, runs, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, name=None):
    """runs: a string, or a list of paragraphs, each a string or a list of (text, {size, color, bold, italic})."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap, tf.vertical_anchor = True, anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate([runs] if isinstance(runs, str) else runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if i:
            p.space_before = Pt(size * 0.5)
        for txt, o in ([(para, {})] if isinstance(para, str) else para):
            r = p.add_run()
            r.text = txt
            f = r.font
            f.name, f.size = FONT, Pt(o.get("size", size))
            f.bold, f.italic = o.get("bold", bold), o.get("italic", False)
            f.color.rgb = rgb(o.get("color", color))
    return tb


def box(s, x, y, w, h, fill, line=None, radius=0.08, name=None):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    if radius:
        shp.adjustments[0] = radius
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb, shp.line.width = rgb(line), Pt(1.5)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    if name:
        shp.name = name
    return shp


def card(s, x, y, w, h, big, small, color, big_size=36, small_size=15):
    box(s, x, y, w, h, tint(color, 0.10))
    text(s, x + 0.3, y + 0.25, w - 0.6, 0.8, big, big_size, color, True)
    text(s, x + 0.3, y + 0.3 + big_size / 72 * 1.25, w - 0.6, h - 0.5 - big_size / 72, small, small_size, INK)


def head(s, title, sub=None):
    text(s, M, 0.38, W - 2 * M, 0.6, title, 30, INK, True, name="Title")
    if sub:
        text(s, M, 0.98, W - 2 * M, 0.4, sub, 17, MUTED, name="Subtitle")


def source(s, txt):
    text(s, M, H - 0.48, W - 2 * M, 0.4, "Sources: " + txt, 9, MUTED, name="Sources")


def picture(s, path, x, y, w, crop_top=0.155, crop_bottom=0.0, crop_left=0.0, crop_right=0.0):
    p = s.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(w))
    p.crop_top, p.crop_bottom, p.crop_left, p.crop_right = crop_top, crop_bottom, crop_left, crop_right
    iw, ih = Image.open(path).size
    p.height = int(p.width * ih * (1 - crop_top - crop_bottom) / (iw * (1 - crop_left - crop_right)))
    return p


def style_chart(ch, colors, legend=True, labels=True, fmt='0.0', size=12):
    ch.font.name, ch.font.size, ch.font.color.rgb = FONT, Pt(size), rgb(INK)
    ch.has_legend = legend
    if legend:
        ch.legend.position, ch.legend.include_in_layout = XL_LEGEND_POSITION.BOTTOM, False
        ch.legend.font.size = Pt(size)
    for ser, c in zip(ch.plots[0].series, colors):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(c)
        if hasattr(ser, "invert_if_negative"):
            ser.invert_if_negative = False   # PowerPoint otherwise draws negative bars white (invisible)
    if labels:
        pl = ch.plots[0]
        pl.has_data_labels = True
        pl.data_labels.number_format, pl.data_labels.number_format_is_linked = fmt, False
        pl.data_labels.font.size, pl.data_labels.font.bold = Pt(size), True
    return ch


def quiet_axes(ch, vmin=None, vmax=None, gridlines=False):
    va = ch.value_axis
    if vmin is not None:
        va.minimum_scale = vmin
    if vmax is not None:
        va.maximum_scale = vmax
    va.has_major_gridlines = gridlines
    if gridlines:
        va.major_gridlines.format.line.color.rgb = rgb(GRID)
    va.format.line.fill.background()
    va.tick_labels.font.color.rgb = rgb(MUTED)
    ch.category_axis.format.line.color.rgb = rgb(GRID)
    ch.category_axis.tick_labels.font.color.rgb = rgb(INK)


# ---------------------------------------------------------------- slides
# 2004 Parcs i Jardins lists (the dead-tree table is in the CSV's in_table; here the rebuilt-street rows "remodelacions" +
# "excepcionalment", Arbrat viari: selecció d'espècies, rev. 2004, p. 13; notes/tree_master_plan.md §5b.1). Cultivar ignored.
LIST_2004 = {
    "small": ("Cercis siliquastrum", "Citrus aurantium", "Hibiscus syriacus", "Magnolia grandiflora", "Nerium oleander",
              "Prunus cerasifera", "Prunus serrulata", "Pyrus communis", "Acacia saligna", "Acer monspessulanum",
              "Ligustrum lucidum", "Tamarix gallica"),
    "medium": ("Acer saccharinum", "Albizia julibrissin", "Brachychiton populneus", "Catalpa bignonioides", "Celtis australis",
               "Cercis siliquastrum", "Jacaranda mimosifolia", "Koelreuteria paniculata", "Magnolia grandiflora", "Melia azedarach",
               "Populus alba", "Populus simonii", "Prunus serrulata", "Quercus ilex", "Robinia pseudoacacia", "Sophora japonica",
               "Styphnolobium japonicum", "Tilia", "Acacia saligna", "Ceratonia siliqua", "Ficus microcarpa", "Ginkgo biloba",
               "Grevillea robusta", "Morus alba", "Phoenix dactylifera", "Populus nigra", "Washingtonia"),
    "large": ("Ailanthus altissima", "Gleditsia triacanthos", "Jacaranda mimosifolia", "Platanus", "Populus simonii", "Quercus ilex",
              "Robinia pseudoacacia", "Tilia", "Tipuana tipu", "Eucalyptus", "Ficus microcarpa", "Phoenix dactylifera",
              "Pinus pinea", "Washingtonia")}
CW_SRC = ("Outlines: Open Data BCN (CC BY 4.0). Cap: Pla director de l'arbrat 2017–2037. City mix: Betevé, 7 May 2026. "
          "Heat = shade proxy, not UTCI.")


def s01_title(s):
    im = Image.open(ROOT / "slides/fig/01_title_photo.webp").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    buf.seek(0)
    p = s.shapes.add_picture(buf, 0, 0, width=Inches(W))
    ratio = im.size[1] / im.size[0] * W / H          # photo is taller than 16:9 relative to width? crop to fill
    if ratio > 1:
        p.crop_top = p.crop_bottom = (1 - 1 / ratio) / 2
    p.height = Inches(H)
    scrim = box(s, 0, 0, W, H, "#000000", radius=0, name="Scrim")  # full width, black to transparent (Giovanni, 9 Nov)
    scrim.fill.gradient()
    scrim.fill.gradient_angle = 0
    gs = scrim.fill._xPr.find(qn("a:gradFill")).find(qn("a:gsLst"))
    for g in list(gs):
        gs.remove(g)
    for pos, a in ((0, 85000), (45000, 70000), (100000, 0)):
        g = gs.makeelement(qn("a:gs"), {"pos": str(pos)})
        c = g.makeelement(qn("a:srgbClr"), {"val": "000000"})
        c.append(c.makeelement(qn("a:alpha"), {"val": str(a)}))
        g.append(c)
        gs.append(g)
    text(s, 0.75, 2.2, 7.4, 1.0, "Shade and Sponge", 54, "#F2F0EA", True, name="Title")
    text(s, 0.75, 3.35, 7.0, 1.4, "A computational method for replacing the street trees a project must cut, so that summer heat "
         "and storm runoff improve, or at least do not get worse. First case: Barcelona's plane trees (Platanus).", 20, "#F2F0EA")
    text(s, 0.75, 5.15, 7.0, 0.4, "MaCAD, IAAC  ·  Tutor session with A. Chronis, 10 November 2026", 16, "#CFC9BC")
    text(s, 0.75, H - 0.6, 11.5, 0.3, "Horts urbans de Porta, Carrer d'Alcúdia × Carrer de la Maladeta, Nou Barris: "
         "the bare crowns in the foreground are the plane trees this thesis is about.", 11, "#CFC9BC")


def s02_context(s):
    head(s, "The decision is already taken", "Barcelona replaces street trees one at a time; the planes are the largest case")
    for k, (big, small, c) in enumerate([
            ("−56%", "Plane trees in ten years: 27% → 12% of the stock", HEAT),
            ("15% · 30%", "Master plan: max 15% per species; 30% tree cover", TREE),
            ("10,976", "Trees replaced with another species, 2018–2026", WARN)]):
        card(s, M + k * 4.18, 1.75, 3.9, 2.9, big, small, c, 44, 17)
    text(s, M, 5.15, W - 2 * M, 0.8, "This is the context, not the problem: the city has already decided how much of each "
         "species. What follows is what it has not decided.", 19, INK)
    source(s, "Nació Digital, 4 May 2026; Betevé, 7 May 2026; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; "
           "Open Data BCN, arbrat viari, quarterly inventories 2018–2026.")


def s03_gate1(s):
    head(s, "Does the city already decide which tree goes where?", "Yes, on paper. Not with numbers, and not in practice")
    rc = pd.read_csv(DB / "replacement_rule_check.csv")
    text(s, M, 1.6, 6.0, 0.3, "ON PAPER · Parcs i Jardins 2004 / 2005, Nou Barris row", 14, TREE, True)
    tb = s.shapes.add_table(4, 2, Inches(M), Inches(1.95), Inches(6.0), Inches(2.2)).table
    rows = [("Sidewalk width", "Replacement species"), ("< 3.5 m", "Prunus cerasifera"), ("3.5 – 6 m", "Melia or Jacaranda"),
            ("> 6 m", "keep the plane")]
    for i, (a, b) in enumerate(rows):
        for j, v in enumerate((a, b)):
            cell = tb.cell(i, j)
            cell.text = v
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(TREE if i == 0 else tint(TREE, 0.10))
            f = cell.text_frame.paragraphs[0].runs[0].font
            f.name, f.size, f.bold = FONT, Pt(17), i == 0 or j == 1
            f.color.rgb = rgb(WHITE if i == 0 else (TREE if j == 1 else INK))
    tb.columns[0].width, tb.columns[1].width = Inches(2.2), Inches(3.8)
    text(s, M, 4.35, 6.0, 0.4, "Criteria: tolerance, street type, tradition, experience.", 15, INK)
    text(s, M, 4.8, 6.0, 0.5, "No heat. No runoff.", 24, HEAT, True)
    text(s, M, 5.35, 6.0, 0.5, "Rebuilt streets: a longer list per sidewalk class (p. 13).", 14, MUTED)
    # right: practice, as a native bar chart
    text(s, 7.05, 1.6, 5.7, 0.3, "IN PRACTICE · Porta, trees planted 2007–2026", 14, WARN, True)
    cd = CategoryChartData()
    any_list = rc.in_table | rc.apply(lambda r: r.genus_sp.startswith(LIST_2004[r.size_class]), axis=1)
    cats, v1, v2 = [], [], []
    for cls, lab in (("small", "Narrow sidewalks"), ("medium", "Medium sidewalks")):
        g = rc.size_class == cls
        cats.append(f"{lab} ({rc[g].n.sum()} trees)")
        v1.append(rc[g & rc.in_table].n.sum() / rc[g].n.sum())
        v2.append(rc[g & any_list].n.sum() / rc[g].n.sum())
    cd.categories = cats
    cd.add_series("Dead-tree table", v1)
    cd.add_series("Any 2004 list, incl. rebuilt streets", v2)
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(7.05), Inches(1.95), Inches(5.7), Inches(2.9), cd).chart
    style_chart(ch, [WARN, MUTED], legend=True, fmt='0%', size=14)
    quiet_axes(ch, 0, 1)
    ch.category_axis.reverse_order = True
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0%', False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Share matching the table"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
    text(s, 7.05, 4.95, 5.7, 0.5, "Most plantings match none of the 2004 lists.", 15, INK, True)
    box(s, M, 5.95, W - 2 * M, 0.6, tint(INK, 0.06))
    text(s, M + 0.25, 6.07, W - 2 * M - 0.5, 0.4, "A rule exists, it is qualitative, and practice mostly does not follow it.",
         16, INK, True)
    source(s, "Parcs i Jardins, Arbrat viari: selecció d'espècies (rev. 2004) pp. 11–14; Gestió de l'arbrat viari de Barcelona "
           "(2011) p. 28; Open Data BCN, arbrat viari (planting dates 2007–2026).")


def s04_trees(s):
    head(s, "Are there enough trees?", "Not in Porta, and the planes are the largest part of what it has")
    cov = 100 * pd.read_csv(DB / "porta_canopy_cover.csv").iloc[0].canopy_cover
    plane = 5.75                                  # plane crowns clipped to Porta (notes/topic_decision.md §10.3)
    cd = CategoryChartData()
    cd.categories = ["Porta tree cover, % of area"]
    for lab, v in (("Planes", plane), ("All other canopy", cov - plane), ("Gap to the 30% target", 30 - cov)):
        cd.add_series(lab, [v])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, Inches(M), Inches(1.6), Inches(W - 2 * M), Inches(2.2), cd).chart
    style_chart(ch, [HEAT, TREE, GRID], fmt='0.0"%"', size=14)
    quiet_axes(ch, 0, 35)
    ch.category_axis.visible = False
    for ser in list(ch.plots[0].series)[:2]:
        ser.data_labels.font.color.rgb = rgb(WHITE)
        ser.data_labels.font.size, ser.data_labels.font.bold = Pt(14), True
        ser.data_labels.show_value = True
        ser.data_labels.number_format, ser.data_labels.number_format_is_linked = '0.0"%"', False
    ch.plots[0].gap_width = 40
    text(s, M, 3.85, W - 2 * M, 0.4, f"Porta today {cov:.1f}% · city target 30% by 2037",
         16, INK, True)
    card(s, M, 4.45, 5.9, 1.9, "≈ 29%", "of Porta's canopy is plane trees (5.75% of the area, 832 trees)", HEAT)
    card(s, M + 6.33, 4.45, 5.9, 1.9, "16% ↔ 20%", "Small-crowned replacements → ~16%; large-crowned → unchanged", TREE)
    source(s, "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037 (target 1); "
           "Pla Clima 2024 p. 33.")


def s05_problem(s):
    head(s, "The problem", "Context, problem and gap, kept apart")
    box(s, M, 1.6, W - 2 * M, 3.4, tint(INK, 0.06))
    text(s, M + 0.45, 1.6, W - 2 * M - 0.9, 3.4, "When a project in Barcelona must replace street trees, at least ~1,300 a "
         "year, the only documented rule for the new species is qualitative. No rule checks whether a replacement keeps, loses "
         "or improves the street's shade and rain interception, so a project can leave its street hotter or wetter, and nobody "
         "measures by how much.", 24, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    for k, (lab, txt, c) in enumerate((("CONTEXT", "planes going, 15% cap, trees replaced one at a time", MUTED),
                                       ("PROBLEM", "a qualitative rule; a project can make its street worse", HEAT),
                                       ("GAP", "no quantities for heat or runoff, per position", RAIN))):
        text(s, M + k * 4.18, 5.4, 3.9, 1.0, [[(lab, {"bold": True, "color": c, "size": 14})], txt], 17, INK)


def s07_gap(s):
    head(s, "The gap", "Data, rules and tools exist, but nothing links them tree by tree")
    w = 11.8   # slimmed version of the RM seminar "opening the boxes" map
    picture(s, ROOT / "slides/fig_v8/v8_gap_boxes.png", (W - w) / 2, 1.45, w, crop_top=0)
    source(s, "Mannucci et al. 2025; Nicol et al. 2026 (PLoS One); Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026; "
           "Kendal, Dobbs & Lohr 2014 (UFUG 13); Ajuntament de Barcelona, Pla director de l'arbrat 2017.")


def s08_rq(s):
    head(s, "The research question, scrutinised", "One main question, four sub-questions, each with a metric")
    box(s, M, 1.55, W - 2 * M, 1.55, tint(INK, 0.06))
    text(s, M + 0.35, 1.55, W - 2 * M - 0.7, 1.55, "When a street project in Barcelona must replace trees, can a trait-based "
         "layout method, inside the city's tree rules, choose the new species and positions, and new planting spots, so that "
         "pedestrian cooling and storm-water interception improve, or at least do not get worse, compared with the city's own "
         "practice and with today?", 18, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    sq = [("SQ1 · heat", "Is the street as cool as with the city's choice, or cooler? Mean UTCI 12–17 h, hot design day", HEAT),
          ("SQ2 · runoff", "Is runoff no worse? Total and at flood hotspots, 2-yr 60-min storm, against Δmin", RAIN),
          ("SQ3 · trade-off", "Do the heat-best and runoff-best layouts differ, and in which species?", WARN),
          ("SQ4 · additions", "How much of the gap to 30% can new street trees close, and where?", TREE)]
    for k, (hd, txt, c) in enumerate(sq):
        x, y = M + (k % 2) * 6.33, 3.3 + (k // 2) * 1.2
        box(s, x, y, 5.9, 1.05, tint(c, 0.10))
        text(s, x + 0.25, y + 0.12, 5.4, 0.9, [[(hd, {"bold": True, "color": c, "size": 16})], txt], 15, INK)
    text(s, M, 5.8, W - 2 * M, 0.7, "Changed after scrutiny: 'reduce' → 'improve, or at least do no harm' (city's practice first, then today) · "
         "any tree a project replaces, planes as the validated case · "
         "additions co-equal · 'not resolved' is an allowed answer · baseline = the city's observed replacement mix (S1b), "
         "with the announced mix (S1a) beside it", 14, MUTED)


def s09_hyp(s):
    head(s, "Hypotheses", "Do no harm, improve where possible: two to test, one declared limit")
    items = [("H1", "No worse than the city's practice on heat or runoff, better on summer heat", "For any tree a project replaces. Runoff is a check: below Δmin = 91 m³ it is 'not resolved'; pits and grouping matter more than species", TREE),
             ("H2", "The heat-best and runoff-best layouts differ in species", "Tested on the Pareto front (SQ3)", WARN),
             ("Boundary", "At extreme storms, street trees cannot matter", "Was H3; true by construction of the model, so declared, not tested", MUTED)]
    for k, (h, txt, sub, c) in enumerate(items):
        y = 1.6 + k * 1.6
        box(s, M, y, W - 2 * M, 1.35, tint(c, 0.10))
        text(s, M + 0.35, y, 1.9, 1.35, h, 32, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.5, y + 0.25, W - 2 * M - 2.8, 1.0, [[(txt, {"bold": True, "size": 22})], [(sub, {"color": MUTED})]], 16, INK)


def s12_radar(s):
    head(s, "First results: replacing Porta's 832 plane trees",
         "The optimised layout keeps almost all of today's summer shade; the city's announced mix loses about an eighth")
    cd = CategoryChartData()
    cd.categories = [lab for lab, *_ in rv.IND]
    for k in ("S0", "S1a", "Opt"):
        cd.add_series(rv.NAME[k], [max(80, rv.score(rv.ROWS[k], col, sg)) for _, col, sg, _ in rv.IND])
    gf = s.shapes.add_chart(XL_CHART_TYPE.RADAR, Inches(M), Inches(1.5), Inches(7.0), Inches(5.3), cd)
    ch = gf.chart
    style_chart(ch, [rv.COL[k] for k in ("S0", "S1a", "Opt")], labels=False, size=13)
    for ser, k in zip(ch.plots[0].series, ("S0", "S1a", "Opt")):
        ser.format.line.color.rgb, ser.format.line.width = rgb(rv.COL[k]), Pt(3 if k != "S0" else 2)
        ser.smooth = False
        ser.marker.style = None
    ch.value_axis.minimum_scale, ch.value_axis.maximum_scale, ch.value_axis.major_unit = 80, 105, 5
    ch.value_axis.tick_labels.font.size, ch.value_axis.tick_labels.font.color.rgb = Pt(10), rgb(MUTED)
    # the values as an editable table
    tb = s.shapes.add_table(len(rv.IND) + 1, 3, Inches(7.9), Inches(1.7), Inches(4.9), Inches(3.2)).table
    for j, v in enumerate(("Indicator (today = 100)", "City mix S1a", "Optimised")):
        tb.cell(0, j).text = v
    for i, (lab, col, sg, c) in enumerate(rv.IND, 1):
        for j, v in enumerate((lab, f"{rv.score(rv.ROWS['S1a'], col, sg):.1f}", f"{rv.score(rv.ROWS['Opt'], col, sg):.1f}")):
            tb.cell(i, j).text = v
    for i in range(len(rv.IND) + 1):
        for j in range(3):
            cell = tb.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(INK if i == 0 else (tint(INK, 0.05) if i % 2 else BG))
            f = cell.text_frame.paragraphs[0].runs[0].font
            f.name, f.size, f.bold = FONT, Pt(14), i == 0 or j == 2
            f.color.rgb = rgb(WHITE if i == 0 else (TREE if j == 2 else (WARN if j == 1 else INK)))
    tb.columns[0].width, tb.columns[1].width, tb.columns[2].width = Inches(2.3), Inches(1.3), Inches(1.3)
    text(s, 7.9, 5.1, 4.9, 1.3, ["100 = today. Outward = better.", "Observed mix S1b: 90.3% summer shade (backup B9)."], 13, MUTED)
    source(s, "City mix: Betevé, 7 May 2026. Storm: PDISBA, 2-year 60-min. Heat = shade proxy, not yet UTCI.")


def s13_scenarios(s):
    head(s, "Replacement, additions, or both",
         "Once the planes go, only trait-based choice plus additions gets back above today")
    a = pd.read_csv(DB / "additions_summary.csv")
    g = a.assign(group=a.scenario.str.replace(r"_\d+$", "", regex=True)).groupby("group").mean(numeric_only=True)
    s0 = g.loc["S0_current"]
    cats = [f"Replacement\n{g.n_new['R_Opt']:,.0f} planes", f"Additions\n{g.n_new['A_Opt']:,.0f} spots",
            f"Both\n{g.n_new['RA_Opt']:,.0f} positions"]
    panels = [("Summer shade, % of today", "shade_summer_m2h", lambda v, c: 100 * v / s0[c], HEAT),
              ("Winter shade (a cost), % of today", "shade_winter_m2h", lambda v, c: 100 * v / s0[c], HEAT),
              ("Total runoff, m³ vs today (Δmin 91)", "runoff_m3", lambda v, c: v - s0[c], RAIN),
              ("Canopy cover, points vs today (gap to 30% ≈ 10 pts)", "canopy_pct", lambda v, c: v - s0[c], TREE)]
    pw = (W - 2 * M - 0.3) / 2
    for i, (lab, col, f, c) in enumerate(panels):
        x, y = M + (i % 2) * (pw + 0.3), 1.5 + (i // 2) * 2.75
        cd = CategoryChartData()
        cd.categories = cats
        for m, nm in (("S1a", "City rule (S1a, mean of 5)"), ("Opt", "Optimised (balanced)")):
            cd.add_series(nm, [f(g.loc[f"{k}_{m}", col], col) for k in ("R", "A", "RA")])
        ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(pw), Inches(2.6), cd).chart
        style_chart(ch, [WARN, TREE], legend=(i == 3), fmt='0.0', size=11)
        vals = [v for ser in cd for v in ser.values]
        if "% of" in lab:
            quiet_axes(ch, 10 * int((min(vals) - 5) // 10), None)
        else:
            quiet_axes(ch, *((-3, 2) if col == "canopy_pct" else (None, None)))
            ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        ch.has_title = True
        ch.chart_title.text_frame.text = lab
        r = ch.chart_title.text_frame.paragraphs[0].runs[0].font
        r.size, r.bold, r.color.rgb = Pt(13), True, rgb(c)
    source(s, "Free spots by the spacing rules of Gestió de l'arbrat viari de Barcelona (2011); an upper bound. Heat = shade proxy.")


def s15_cap(s):
    head(s, "Two rules: a city cap and a local ceiling",
         "The city's 15% fixes how much of each species; the local ceiling stops any barri ending more concentrated than today")
    box(s, M, 1.6, 5.6, 1.75, tint(TREE, 0.10))
    text(s, M + 0.25, 1.72, 5.1, 1.6, [[("1. CITY CAP: how much of each species", {"bold": True, "color": TREE})],
         "No species above 15% of the city's street trees (master plan)."], 15, INK)
    box(s, M, 3.5, 5.6, 1.95, tint(WARN, 0.10))
    text(s, M + 0.25, 3.62, 5.1, 1.8, [[("2. LOCAL CEILING: no barri more concentrated than today", {"bold": True, "color": WARN})],
         "No species ends with more trees in a barri than it has planes today. Diagonal Mar: Tipuana 48.5% → 37.2%. Costs little shade."], 15, INK)
    text(s, M, 5.6, 5.6, 0.9, "Limit: barris with few planes (Baró de Viver, 15) need a different ceiling.", 13, MUTED)
    n = pd.read_csv(DB / "citylp_local_species.csv").set_index(["barri", "scenario"]).loc[("ALL", cw.LAYOUT)]
    sp = pd.DataFrame(dict(species=n.index.str.split().str[0], n=n.values.astype(int), cap=[cw.CAP[k] for k in n.index]))
    sp = sp.sort_values("cap", ascending=False)
    cd = CategoryChartData()
    cd.categories = list(sp.species)
    cd.add_series("Planted (all 28 barris)", list(sp.n))
    cd.add_series("City cap", list(sp.cap))
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(6.55), Inches(1.5), Inches(6.25), Inches(4.4), cd).chart
    style_chart(ch, [TREE, GRID], fmt='#,##0', size=12)
    quiet_axes(ch, 0)
    ch.plots[0].gap_width, ch.plots[0].overlap = 50, -10
    for i, r in enumerate(sp.itertuples()):         # species at the cap in dark red
        if r.n >= r.cap:
            pt = ch.plots[0].series[0].points[i]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(HEAT)
    text(s, 6.55, 5.95, 6.25, 0.6, "Dark red = at the cap: Celtis and Tipuana.", 13, MUTED)
    source(s, CW_SRC)


def s16_heat(s):
    head(s, "Validation: a first heat check", "UTCI from Ladybug and Honeybee, today's planes (S0) vs the tool's layout (S4)")
    an, po = pd.read_csv(DB / "porous_utci_andreu_nin_epw2011.csv"), pd.read_csv(DB / "porous_utci_porta_epw2011.csv")
    hb = pd.read_csv(DB / "hb_utci_andreu_nin.csv")
    v = pd.read_csv(DB / "ladybug_vs_proxy_andreu_nin.csv")
    dif = lambda df, a, b: (df[b] - df[a]).mean()
    cd = CategoryChartData()
    cd.categories = ["Andreu Nin, Honeybee (Tier 2)", "Andreu Nin, Python (Tier 1)", "All Porta, Python (Tier 1)"]
    cd.add_series("Porous crowns, τ = exp(−0.5·LAI)", [dif(hb, "utci_hb_S0_porous", "utci_hb_S4_porous"),
                                                      dif(an, "utci_lai_S0", "utci_lai_S4"), dif(po, "utci_lai_S0", "utci_lai_S4")])
    cd.add_series("Opaque crowns", [dif(hb, "utci_hb_S0_opaque", "utci_hb_S4_opaque"),
                                    dif(an, "utci_opaque_S0", "utci_opaque_S4"), dif(po, "utci_opaque_S0", "utci_opaque_S4")])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(M), Inches(1.5), Inches(6.6), Inches(3.6), cd).chart
    style_chart(ch, [TREE, MUTED], fmt='+0.00;−0.00', size=12)
    quiet_axes(ch, -0.25, 0.15, gridlines=True)
    ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ch.category_axis.reverse_order = True
    ch.has_title = True
    ch.chart_title.text_frame.text = "S4 − S0, mean UTCI 15 July 12–17 h, °C"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
    text(s, M, 5.2, 6.6, 1.0, "Python chain = Ladybug in Grasshopper within 0.02 °C. 15 July is an ordinary day, not yet the hot design day.",
         12, MUTED)
    r0 = np.corrcoef(v.shade_lai_S0, v.utci_S0)[0, 1]
    r1 = np.corrcoef(v.d_shade_opaque, v.d_utci)[0, 1]
    x = 7.5
    for k, (big, small, c) in enumerate([(f"r = {r0:.2f}".replace("-", "−"), "shade proxy vs Ladybug UTCI across 1,974 points", TREE),
                                         (f"r = {r1:.2f}".replace("-", "−"), "on the S4 − S0 change per point", TREE)]):
        text(s, x, 1.5 + k * 0.95, 5.3, 0.9, [[(big, {"size": 26, "bold": True, "color": c})], small], 13, INK)
    box(s, x, 3.45, 5.3, 0.75, tint(TREE, 0.14))
    text(s, x + 0.2, 3.45, 4.9, 0.75, "Claim: for heat, no worse than today's planes within model uncertainty.", 15, TREE, True,
         anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Ladybug Tools (Ladybug, Honeybee/Radiance); weather: El Prat TMYx 2011–2025 (climate.onebuilding.org); "
           "porous crowns after Peng et al. 2026.")


def s_next(s):
    head(s, "What comes next", "Five weeks to the final delivery, one theme a week")
    steps = [("11–15 Nov", "Every tree", ["Any tree a project replaces, not only planes", "City layout against S1b",
                                            "Demo: Santapau · Emili Roca · Desfar works"], TREE),
             ("16–22 Nov", "Heat", ["UTCI of the final layouts", "Infrared City, ENVI-met check", "Hot design day · priority score"], HEAT),
             ("23–29 Nov", "Transfer", ["Sant Antoni: repeat the checks (tool already run)", "Mataró: Catalan city, ICGC LiDAR",
                                        "Florence: city LiDAR + 1,459 measured trees"], RAIN),
             ("30 Nov–6 Dec", "Tool", ["City screening layer", "GeoPackage + QGIS style · web app", "Co-benefits per layout"], WARN),
             ("7–18 Dec", "Deliver", ["Booklet", "Final presentation", "Defence 10–23 Dec"], INK)]
    n, y0 = len(steps), 2.35
    xs = [M + 1.2 + k * (W - 2 * M - 2.4) / (n - 1) for k in range(n)]
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(xs[0]), Inches(y0), Inches(xs[-1]), Inches(y0))
    ln.line.color.rgb, ln.line.width = rgb(GRID), Pt(4)
    for x, (when, what, items, c) in zip(xs, steps):
        text(s, x - 1.2, 1.55, 2.4, 0.4, when, 15, MUTED, True, align=PP_ALIGN.CENTER)
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x - 0.17), Inches(y0 - 0.17), Inches(0.34), Inches(0.34))
        o.fill.solid()
        o.fill.fore_color.rgb = rgb(c)
        o.line.color.rgb, o.line.width = rgb(BG), Pt(3)
        o.shadow.inherit = False
        text(s, x - 1.2, 2.75, 2.4, 0.5, what, 22, c, True, align=PP_ALIGN.CENTER)
        text(s, x - 1.18, 3.35, 2.36, 2.2, [[(it, {})] for it in items], 13, INK, align=PP_ALIGN.CENTER)
    box(s, M, 5.75, W - 2 * M, 0.62, tint(MUTED, 0.10))
    text(s, M + 0.3, 5.75, W - 2 * M - 0.6, 0.62, [[("Writing, every week:  ", {"bold": True, "color": MUTED}),
                                                  ("update chapters 3 and 5 → write 6 and 7 → then 1, 8, 9 and the abstract", {})]],
         14, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 6.55, W - 2 * M, 0.3, "Florence LiDAR waits on the Comune's delivery agreement; Mataró's per-tree species table "
         "is not yet confirmed.", 12, MUTED)


def s_cobenefits(s):
    head(s, "Co-benefits not optimised (yet)", "Reported after 10 Nov, not objectives of the tool. Replanting and maintenance costs, noise: future work")
    rows = [("Pollen", "Plane pollen gets the top allergen score (4 of 4) in a Spanish species index",
             "Species index exists (IUGZA, Cariñanos et al. 2014). Replacing planes likely gains here; to compute per layout", WARN),
            ("Carbon", "Stored and sequestered carbon grow with trunk size; felling a large tree loses both",
             "The tool's mix may lose here at first. Urban allometry (McPherson et al. 2016); reported even if it loses", INK),
            ("Diversity", "The 15% cap and the local ceiling already act on it",
             "Already computed (effective species, as in SylvCiT): to report per barri, before and after", TREE),
            ("Air", "PM2.5 capture depends on leaf area; some species emit isoprene (ozone)", "Leaf area is already in the model: PM2.5 can be reported; ozone/VOC stays a declared limit", MUTED)]
    for k, (h, txt, sub, c) in enumerate(rows):
        y = 1.5 + k * 1.05
        box(s, M, y, W - 2 * M, 0.92, tint(c, 0.10))
        text(s, M + 0.3, y, 2.2, 0.92, h, 22, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.7, y + 0.1, W - 2 * M - 3.0, 0.8, [[(txt, {"bold": True, "size": 17})], [(sub, {"color": MUTED})]], 13, INK)
    box(s, M, 5.85, W - 2 * M, 0.62, tint(INK, 0.06))
    text(s, M + 0.25, 5.85, W - 2 * M - 0.5, 0.62, "The master plan already lists allergies and VOC among the disservices to avoid, "
         "with no number per species.", 16, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Cariñanos, Casares-Porcel & Quesada-Rubio 2014 (Landsc. Urban Plan. 123:134-144); McPherson, van Doorn & Peper 2016 "
           "(PSW-GTR-253); Pla director de l'arbrat 2017–2037 §1.3.4, p. 14.")


def s_baseline(s):
    head(s, "The city's baseline: from press to practice", "The method beats both the announced and the observed mix")
    bs = pd.read_csv(DB / "barris_summary.csv")
    po = bs[bs.barri == "Porta"].iloc[0]
    for k, (big, small, c) in enumerate([
            ("S1-2004", "Parcs i Jardins table (district × sidewalk): documented, qualitative. Cited, not run", MUTED),
            ("S1a", "The 2026 target mix (press, May 2026), drawn within the sidewalk sizing rule", WARN),
            ("S1b", "What the city actually planted where planes were replaced, 2018–2026: 1,444 cases", HEAT)]):
        card(s, M + k * 4.18, 1.55, 3.9, 1.95, big, small, c, 30, 14)
    cd = CategoryChartData()
    cd.categories = ["S1a press mix", "S1b observed mix", "Method"]
    cd.add_series("Porta, summer shade, % of today", [po.summer_pct_s1a, po.summer_pct_s1b, po.summer_pct_tool])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(M), Inches(3.75), Inches(7.6), Inches(2.75), cd).chart
    style_chart(ch, [TREE], legend=False, fmt='0.0"%"', size=14)
    for i, c in enumerate((WARN, HEAT, TREE)):
        pt = ch.plots[0].series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(c)
    quiet_axes(ch, 0, 110)
    ch.category_axis.reverse_order = True
    ch.has_title = True
    ch.chart_title.text_frame.text = "Porta · summer shade, % of today"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
    card(s, 8.65, 3.85, 4.15, 2.6, f"+{bs.tool_margin_pts.median():.1f} · +{bs.tool_margin_s1b_pts.median():.1f}",
         f"Median margin of the method over {len(bs)} barris (points): vs S1a · vs S1b. No barri ≤ 0", TREE, 30, 14)
    source(s, "Open Data BCN, arbrat viari, 35 quarterly inventories 2018–2026; Betevé, 7 May 2026; "
           "Parcs i Jardins, Arbrat viari: selecció d'espècies (rev. 2004).")


def s_simplifications(s):
    """Backup B10: each model simplification and its risk (asked at RM_L04, 5 Nov; list from study/guide.md §11)."""
    head(s, "Backup B10 · Simplifications and their risks", "How the model was made tractable, and what each choice can hide")
    rows = [("Simplification", "Risk", "How it is handled"),
            ("Same tree pit for every species; no roots, no infiltration under the tree",
             "Runoff depends more on pit size and grouping than on species", "Runoff is a check, not the main gain; pit grouping is future work"),
            ("Canopy bucket, event volume only; no sewer, ponding or peak flow", "Where the water goes is not modelled",
             "Δmin fixed before the runs; ranking stable for s = 0.83–1.75 mm per LAI"),
            ("One storage s for all species; LAI from a LiDAR proxy (probably low)", "Species differences in storage misstated",
             "Sensitivity on s; allometric LAI (Nowak 1996) as an upper bound"),
            ("Heat = shade proxy; Ladybug has no transpiration", "Vegetation cooling underestimated; small UTCI differences uncertain",
             "Porous crowns, Honeybee cross-check; claim is 'no worse'"),
            ("Airport weather (El Prat), afternoon of one day; no night", "Urban heat and night-time trapping missed",
             "Urban offset 0 to +1.5 °C as sensitivity; stated limit"),
            ("Crowns compared at equal trunk size", "Benefits arrive only when the new trees mature", "Stated; young-tree variant later"),
            ("15% cap counted on street trees only", "Different base from the plan's ~201,600 trees", "Revisit before the final results"),
            ("Free spots without driveways or services", "Additions overstated", "Reported as an upper bound"),
            ("UTCI = one average person", "Vulnerable people and night excluded", "Declared, shared limit of the RM cluster")]
    tb = s.shapes.add_table(len(rows), 3, Inches(M), Inches(1.5), Inches(W - 2 * M), Inches(5.0)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = tb.cell(i, j)
            cell.text = v
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(INK if i == 0 else (tint(INK, 0.05) if i % 2 else BG))
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            f = cell.text_frame.paragraphs[0].runs[0].font
            f.name, f.size, f.bold = FONT, Pt(12), i == 0
            f.color.rgb = rgb(WHITE if i == 0 else INK)
    tb.columns[0].width, tb.columns[1].width, tb.columns[2].width = Inches(4.6), Inches(3.8), Inches(3.833)
    source(s, "Anys & Weiler 2024; Xiao & McPherson 2016; Nowak 1996; RM seminar L04 (5 Nov 2026).")



# ---- native flowcharts, map and backups (everything editable; 9 Nov) --------------------------------------------------
def arrow(s, x1, y1, x2, y2, color=MUTED, width=1.25):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb, c.line.width = rgb(color), Pt(width)
    ln = c.line._get_or_add_ln()
    ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    tree = s.shapes._spTree
    tree.remove(c._element)
    tree.insert(2, c._element)  # behind the boxes, after the group properties
    return c


def node(s, cx, cy, w, label, color, sub=None):
    h = 0.62 if sub else 0.5
    b = box(s, cx - w / 2, cy - h / 2, w, h, color, radius=0.12)
    tf = b.text_frame
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor, tf.word_wrap = MSO_ANCHOR.MIDDLE, True
    for i, (t_, sz, bd) in enumerate([(label, 14, True)] + ([(sub, 10.5, False)] if sub else [])):
        p_ = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p_.alignment = PP_ALIGN.CENTER
        r = p_.add_run()
        r.text = t_
        r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(sz), bd, rgb(WHITE)
    return (cx - w / 2, cx + w / 2, cy)


def icon(s, cx, cy, glyph, caption, color):
    r = 0.36
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r), Inches(cy - r), Inches(2 * r), Inches(2 * r))
    o.fill.solid()
    o.fill.fore_color.rgb = rgb(WHITE)
    o.line.color.rgb, o.line.width = rgb(color), Pt(2)
    o.shadow.inherit = False
    tf = o.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = glyph
    run.font.name, run.font.size, run.font.bold, run.font.color.rgb = FONT, Pt(15), True, rgb(color)
    text(s, cx - 1.0, cy + r + 0.06, 2.0, 0.4, caption, 13, color, True, align=PP_ALIGN.CENTER)
    return (cx - r, cx + r, cy)


def nflow(s, title, sub, cols, links, note=None, side=None):
    """cols: [(header, [(key, 'box', label, color, sub?) | (key, 'icon', glyph, caption, color)])]; links: [(key, key)];
    side: (key, label, sub, color) = an input box under that node with an arrow up."""
    head(s, title, sub)
    n = len(cols)
    xs = [M + 0.95 + i * (W - 2 * M - 1.9) / (n - 1) for i in range(n)]
    bw = min(2.3, (W - 2 * M) / n - 0.3)
    pos, yc = {}, 3.75
    for x, (hd, nodes) in zip(xs, cols):
        text(s, x - bw / 2 - 0.2, 1.55, bw + 0.4, 0.3, hd.upper(), 12, MUTED, True, align=PP_ALIGN.CENTER)
        k = len(nodes)
        gap = 1.45 if any(nd[1] == "icon" for nd in nodes) else min(0.95, 3.6 / max(k, 1))
        for j, nd in enumerate(nodes):
            y = yc + (j - (k - 1) / 2) * gap
            pos[nd[0]] = icon(s, x, y, nd[2], nd[3], nd[4]) if nd[1] == "icon" else \
                node(s, x, y, bw, nd[2], nd[3], nd[4] if len(nd) > 4 else None)
    for a, c in links:
        arrow(s, pos[a][1] + 0.03, pos[a][2], pos[c][0] - 0.05, pos[c][2], GRID if len(links) > 8 else MUTED)
    if side:
        key, lab, sb, col = side
        x0, x1, y = pos[key]
        cx = (x0 + x1) / 2
        box(s, cx - 1.35, 5.75, 2.7, 0.62, WHITE, line=col)
        text(s, cx - 1.3, 5.78, 2.6, 0.6, [[(lab, {"bold": True, "color": col, "size": 13})], [(sb, {"color": MUTED, "size": 11})]],
             13, INK, align=PP_ALIGN.CENTER)
        arrow(s, cx, 5.73, cx, y + 0.34, col, 1.5)
    if note:
        text(s, M, 6.6, W - 2 * M, 0.35, note, 13, MUTED, align=PP_ALIGN.CENTER)


def s10_overview(s):
    nflow(s, "Methodology", "Which species replace the trees a project must cut, and where to add new ones",
          [("Focus", [("heat", "icon", "°C", "Heat stress", HEAT), ("rain", "icon", "mm", "Pluvial floods", RAIN)]),
           ("Data", [("inv", "box", "Tree inventory", TREE), ("lid", "box", "LiDAR", TREE), ("sw", "box", "Sidewalk width", WARN),
                     ("dtm", "box", "Terrain · hotspots", RAIN), ("cli", "box", "Hot day · storms", HEAT)]),
           ("Screening", [("scr", "icon", "Map", "Indicators per tree", INK)]),
           ("Project", [("area", "icon", "Area", "Draw an area", WARN)]),
           ("Design", [("rep", "box", "Replacement", TREE, "trees to replace"), ("add", "box", "Additions", TREE, "free spots")]),
           ("Evaluate", [("h", "box", "Heat", HEAT), ("r", "box", "Runoff", RAIN), ("c", "box", "Canopy", TREE)]),
           ("Compare", [("cmp", "icon", "✓", "vs today · vs city", INK)])],
          [("heat", "lid"), ("heat", "cli"), ("rain", "dtm"), ("rain", "cli"), ("inv", "scr"), ("lid", "scr"), ("sw", "scr"),
           ("dtm", "scr"), ("cli", "scr"), ("scr", "area"), ("area", "rep"), ("area", "add"), ("rep", "h"), ("rep", "r"),
           ("rep", "c"), ("add", "h"), ("add", "r"), ("add", "c"), ("h", "cmp"), ("r", "cmp"), ("c", "cmp")],
          "Built and checked on Porta; the screening layer extends it to the whole city.",
          side=("add", "City rules", "15% cap · sidewalk size · catalogue", WARN))


def s11_design(s):
    nflow(s, "Design module", "Inside the project area the designer draws",
          [("Area", [("area", "icon", "Area", "Project area", WARN)]),
           ("Positions", [("rep", "box", "Trees to replace", TREE, "by priority"), ("add", "box", "Free spots", TREE, "sidewalk ≥ 2.5 m")]),
           ("Feasible", [("feas", "box", "Species per spot", WARN, "size class · catalogue")]),
           ("Optimise", [("opt", "box", "Multi-objective", INK, "weighted sum → NSGA-II")]),
           ("Layouts", [("r", "box", "R", TREE, "replacement"), ("a", "box", "A", TREE, "additions"), ("ra", "box", "R + A", TREE, "both")])],
          [("area", "rep"), ("area", "add"), ("rep", "feas"), ("add", "feas"), ("feas", "opt"), ("opt", "r"), ("opt", "a"), ("opt", "ra")],
          "Each layout is compared with the city's practice on the same positions, and with today (S0).",
          side=("feas", "City rules", "15% cap · city mix", WARN))


def b1_heat(s):
    nflow(s, "Backup B1 · Heat module", "Fast proxy inside the loop, full UTCI on the final layouts",
          [("Climate", [("epw", "icon", "°C", "Hot design day", HEAT)]),
           ("Sun", [("sun", "box", "Sun positions", HEAT, "12–17 h"), ("bld", "box", "Buildings", MUTED, "LiDAR heights")]),
           ("Proxy", [("prox", "box", "Effective shade", HEAT, "shadow × (1 − τ), τ = e^(−0.5 LAI)")]),
           ("UTCI", [("t1", "box", "Ladybug Tier 1", HEAT, "final layouts"), ("t2", "box", "Honeybee Tier 2", HEAT, "spot check")]),
           ("Output", [("out", "box", "Mean UTCI", HEAT, "12–17 h, sidewalks")])],
          [("epw", "sun"), ("epw", "t1"), ("sun", "prox"), ("bld", "prox"), ("prox", "t1"), ("prox", "t2"), ("t1", "out"), ("t2", "out")],
          "Winter sun is scored the same way on a January day: shade there is a cost.",
          side=("prox", "Crown model", "LiDAR crowns · leaf calendar", TREE))


def b2_runoff(s):
    nflow(s, "Backup B2 · Runoff module", "Event runoff on a 1 m grid, routed to the flood hotspots",
          [("Storm", [("st", "icon", "mm", "PDISBA design storm", RAIN)]),
           ("Canopy", [("int", "box", "Interception", RAIN, "s · LAI, bucket")]),
           ("Surface", [("cn", "box", "SCS-CN", RAIN, "sealed · pervious · roofs")]),
           ("Routing", [("rt", "box", "Flow routing", RAIN, "terrain + buildings")]),
           ("Output", [("tot", "box", "Total runoff", RAIN, "vs Δmin = 91 m³"), ("hot", "box", "Hotspot runoff", RAIN)])],
          [("st", "int"), ("int", "cn"), ("cn", "rt"), ("rt", "tot"), ("rt", "hot")],
          "2-year 60-min storm in the headline; extreme storms are outside what street trees can affect.",
          side=("int", "Calibration", "s = 1.75 mm/LAI · Anys & Weiler 2024", WARN))


def b3_screening(s):
    nflow(s, "Backup B3 · City screening", "Indicators for every street-tree position",
          [("Data", [("inv", "box", "Tree inventory", TREE), ("lid", "box", "LiDAR", TREE), ("sw", "box", "Sidewalk width", WARN),
                     ("dtm", "box", "Terrain · hotspots", RAIN)]),
           ("Per tree", [("crown", "box", "Crown · LAI", TREE), ("size", "box", "Size class", WARN), ("shade", "box", "Shade potential", HEAT),
                         ("flow", "box", "Water convergence", RAIN)]),
           ("Priority", [("vig", "box", "Crown vigour", TREE), ("ndvi", "box", "NDVI change", TREE), ("age", "box", "Age · trunk", MUTED)]),
           ("Output", [("map", "icon", "Map", "City layer", INK), ("prio", "icon", "!", "Replacement priority", TREE)])],
          [("inv", "crown"), ("lid", "crown"), ("lid", "shade"), ("sw", "size"), ("dtm", "flow"), ("inv", "age"), ("crown", "vig"),
           ("crown", "map"), ("size", "map"), ("shade", "map"), ("flow", "map"), ("vig", "prio"), ("ndvi", "prio"), ("age", "prio")],
          "Priority is a proxy (no open tree-health data), tested against trees removed between inventories.")


def b7_validation(s):
    nflow(s, "Backup B7 · Validation plan", "Each module checked against something it was not fitted to",
          [("Module", [("h", "icon", "°C", "Heat", HEAT), ("w", "icon", "mm", "Runoff", RAIN), ("p", "icon", "!", "Priority", TREE)]),
           ("Check", [("h1", "box", "Proxy vs Ladybug", HEAT), ("h2", "box", "Ladybug vs ENVI-met", HEAT, "Mannucci et al. 2025"),
                      ("w1", "box", "Interception data", RAIN, "Anys & Weiler 2024"), ("p1", "box", "Removed trees", TREE, "inventory snapshots")]),
           ("Transfer", [("tr", "box", "Sant Antoni", INK, "same city, flood-dominant")]),
           ("Verdict", [("v", "icon", "✓", "Verdict per hypothesis", INK)])],
          [("h", "h1"), ("h", "h2"), ("w", "w1"), ("p", "p1"), ("h1", "tr"), ("h2", "tr"), ("w1", "tr"), ("p1", "tr"), ("tr", "v")],
          "Thresholds fixed before the runs: below what the model resolves = \"not resolved\".")


def s06_crowns(s):
    head(s, "Why it matters: the crowns differ", "Crown area as a share of a plane's, same trunk size, Porta's own trees")
    d = pd.read_csv(DB / "crown_by_trunk_class.csv", header=[0, 1], index_col=0)["area_ratio_vs_plane"]
    sp = ["Platanus x acerifolia", "Tipuana tipu", "Jacaranda mimosifolia", "Melia azedarach", "Celtis australis",
          "Pyrus calleryana", "Brachychiton populneus"]
    cd = CategoryChartData()
    cd.categories = [x.replace(" x ", " × ") for x in sp]
    for cls, lab in (("SEGONA", "2nd trunk class"), ("TERCERA", "3rd trunk class")):
        cd.add_series(lab, [None if pd.isna(d.loc[x, cls]) or d.loc[x, cls] == 0 else float(d.loc[x, cls]) for x in sp])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(M), Inches(1.5), Inches(W - 2 * M), Inches(4.9), cd).chart
    style_chart(ch, [tint(TREE, 0.55), TREE], fmt='0%', size=13)
    quiet_axes(ch, 0, 1.2, gridlines=True)
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0%', False
    ch.category_axis.reverse_order = True
    ch.plots[0].gap_width = 60
    text(s, M, 6.5, W - 2 * M, 0.4, "Equal trunk size is not equal age, and street trees are pruned: not mature potential.", 12, MUTED)
    source(s, "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, arbrat viari (trunk class).")


def s14_map(s):
    import json
    import math
    head(s, "City-wide: 28 barris, one layout", "Summer shade gained over the city's mix, one optimisation under the 15% city cap")
    d = cw.d
    gain = dict(zip(d.barri.map(cw.key), d.gain))
    g = json.load(open(ROOT / "web/public/data/barris.geojson", encoding="utf-8"))["features"]
    rings = [(f["properties"]["name"], r) for f in g for poly in
             ([f["geometry"]["coordinates"]] if f["geometry"]["type"] == "Polygon" else f["geometry"]["coordinates"]) for r in poly[:1]]
    allp = np.concatenate([np.array(r) for _, r in rings])
    kx = math.cos(math.radians(allp[:, 1].mean()))
    x0, y0, mw, mh = M, 1.5, 7.6, 4.9
    sc = min(mw / ((allp[:, 0].max() - allp[:, 0].min()) * kx), mh / (allp[:, 1].max() - allp[:, 1].min()))
    px = lambda q: (Inches(x0 + (q[0] - allp[:, 0].min()) * kx * sc), Inches(y0 + (allp[:, 1].max() - q[1]) * sc))
    hi = d.gain.max()
    for name, r in rings:
        pts = [px(q) for q in r]
        ff = s.shapes.build_freeform(*pts[0], scale=1.0)
        ff.add_line_segments(pts[1:], close=True)
        shp = ff.convert_to_shape()
        shp.name = name
        v = gain.get(cw.key(name))
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(GRID if v is None else tint(WARN, 0.9) if v < 0 else tint(TREE, 0.15 + 0.85 * v / hi))
        shp.line.color.rgb, shp.line.width = rgb(INK if name == "Porta" else BG), Pt(2.5 if name == "Porta" else 0.5)
        shp.shadow.inherit = False
    for k, (fill, ln, lab) in enumerate([(tint(TREE, 0.3), BG, "small gain"), (TREE, BG, "large gain"), (tint(WARN, 0.9), BG, "loss"),
                                         (GRID, BG, "not computed"), (BG, INK, "Porta")]):
        x = M + k * 1.55
        sw = box(s, x, 6.5, 0.28, 0.22, fill, radius=0, line=ln)
        sw.shadow.inherit = False
        text(s, x + 0.34, 6.44, 1.2, 0.32, lab, 12, MUTED)
    for k, (big, small, c) in enumerate([(f"+{d.gain.median():.1f} pts", "median gain of summer shade over the city's mix", TREE),
                                         (f"{(d.gain > 0).sum()} of {len(d)}", f"barris gain ({d.planes.sum():,} planes)", TREE),
                                         ("Bonanova", "loses a little: with one city cap the capped species go where they add most", WARN)]):
        card(s, 8.85, 1.55 + k * 1.75, 3.95, 1.55, big, small, c, 28, 13)
    source(s, CW_SRC)


def b4_bars(s):
    head(s, "Backup B4 · Results in real units", "Difference from the city's mix (S1a), Porta; runoff stays inside ±Δmin")
    panels = [("Summer shade", "shade_summer_m2h", "k m²·h · up = better", 1e-3, HEAT),
              ("Winter shade", "shade_winter_m2h", "k m²·h · up = a cost", 1e-3, HEAT),
              ("Total runoff", "runoff_m3", "m³ · down = better", 1, RAIN), ("Hotspot runoff", "runoff_hot_m3", "m³ · down = better", 1, RAIN),
              ("Canopy cover", "canopy_pct", "points · up = better", 1, TREE)]
    pw = (W - 2 * M) / 5
    for i, (lab, col, unit, k, c) in enumerate(panels):
        base = rv.ROWS["S1a"][col]
        cd = CategoryChartData()
        cd.categories = ["Today", "Optimised"]
        vals = [(rv.ROWS[n][col] - base) * k for n in ("S0", "Opt")]
        cd.add_series(lab, vals)
        ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(M + i * pw), Inches(1.6), Inches(pw - 0.1), Inches(4.6), cd).chart
        style_chart(ch, [c], legend=False, fmt='+#,##0.0;−#,##0.0', size=11)
        quiet_axes(ch, float(np.floor(min(0, min(vals)) * 1.25)), float(np.ceil(max(0, max(vals)) * 1.25)))
        ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '#,##0.#', False
        ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        ch.has_title = True
        ch.chart_title.text_frame.text = f"{lab}\n{unit}"
        for p_ in ch.chart_title.text_frame.paragraphs:
            for r in p_.runs:
                r.font.size, r.font.color.rgb = Pt(12), rgb(c)
    text(s, M, 6.35, W - 2 * M, 0.4, "0 = the city's mix (S1a, mean of 10 seeds). Optimised = balanced layout of the weight sweep. Δmin = 91 m³. Heat = shade proxy. Storm: PDISBA 2-year 60-min.", 12, MUTED)


def b4b_palette30(s):
    head(s, "Backup B4b · Wider palette (30 species)", "Same rules, the city's catalogue instead of 7 species: Porta and 32 barris, each optimised alone")
    d = pd.read_csv(DB / "barris_summary_barcelona.csv").sort_values("summer_pct_tool_palette30")
    cd = CategoryChartData()
    cd.categories = list(d.barri)
    cd.add_series("7 species", list(d.summer_pct_tool_palette7))
    cd.add_series("30 species", list(d.summer_pct_tool_palette30))
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(M), Inches(1.35), Inches(7.6), Inches(5.65), cd).chart
    style_chart(ch, [WARN, TREE], labels=False, size=9)
    quiet_axes(ch, 60, 115, gridlines=True)
    ch.plots[0].gap_width, ch.plots[0].overlap = 40, 0
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(7)
    ch.legend.position = XL_LEGEND_POSITION.TOP
    skip = ca._element.makeelement(qn("c:tickLblSkip"), {})   # show all 33 names: PowerPoint and Google otherwise skip every other one
    skip.set("val", "1")
    nm = ca._element.find(qn("c:noMultiLvlLbl"))
    nm.addprevious(skip) if nm is not None else ca._element.append(skip)
    ch.has_title = True
    ch.chart_title.text_frame.text = "Summer shade, % of today"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    b32 = d[d.barri != "Porta"]
    card(s, 8.6, 1.55, 4.2, 1.9, f"+{b32.diff_pts.median():.1f} pts", f"median summer-shade gain over 7 species "
         f"({int((b32.diff_pts > 0).sum())} of {len(b32)} barris gain)", TREE, 30, 13)
    card(s, 8.6, 3.65, 4.2, 1.9, f"{d.winter_pct_tool_palette30.min():.0f}–{d.winter_pct_tool_palette30.max():.0f}%",
         "of today's winter shade: the price (more evergreens)", WARN, 30, 13)
    text(s, 8.6, 5.75, 4.2, 0.8, "30 species = the 2011 guide catalogue minus its 4 'avoid' species. The city-wide LP still uses 7.", 12, MUTED)
    source(s, "Ajuntament de Barcelona, Gestió de l'arbrat viari de Barcelona (2011), species catalogue.")


def b6_optimiser(s):
    head(s, "Backup B6 · How the optimiser finds the layout", "No trial and error: a score table, then one exact solve per weight set")
    steps = [("1", "Score table", "Every position × every species, alone: summer shade, winter shade, water held above the hotspots. "
              "Porta: 832 × 7. The slow step, computed once.", TREE),
             ("2", "Weights", "One score per cell = weighted sum of the three, each scaled to its maximum. 15 weight sets.", WARN),
             ("3", "Exact solve", "One species per position, only species that fit the sidewalk, none above its cap. "
              "A transportation LP (HiGHS): whole-number answer, proven best. ~0.06 s for Porta.", INK),
             ("4", "Re-score", "Each layout re-run with the full models (overlapping crowns, water routing): "
              "these are the numbers on the slides.", RAIN)]
    w = (W - 2 * M - 3 * 0.3) / 4
    for k, (n, h, txt, c) in enumerate(steps):
        x = M + k * (w + 0.3)
        box(s, x, 1.55, w, 3.35, tint(c, 0.10))
        text(s, x + 0.25, 1.7, 0.6, 0.6, n, 30, c, True)
        text(s, x + 0.25, 2.35, w - 0.5, 0.45, h, 19, c, True)
        text(s, x + 0.25, 2.9, w - 0.5, 1.9, txt, 14, INK)
        if k < 3:
            arrow(s, x + w + 0.03, 3.2, x + w + 0.27, 3.2, MUTED, 2)
    box(s, M, 5.15, W - 2 * M, 1.2, tint(MUTED, 0.10))
    text(s, M + 0.3, 5.22, W - 2 * M - 0.6, 1.1,
         [[("Why not a genetic or ant-colony search (Wallacei, Opossum)?  ", {"bold": True}),
           ("They search by trial and error and suit black-box objectives. Here every objective is a sum over positions, "
            "so an exact solver is faster and proves the optimum. They, and an ML surrogate, become useful only if full "
            "UTCI enters the loop: future work.", {})]], 14, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "HiGHS open-source linear optimisation solver (highs.dev), called through SciPy (scipy.optimize.linprog).")


def b5_sizing(s):
    head(s, "Backup B5 · The sizing rule leaves real choice", "Sidewalk width at each Porta plane (2011 guide: < 2.5 m none, < 3.5 small, 3.5–6 medium, > 6 large)")
    picture(s, ROOT / "notes/figures/porta_sidewalk_classes.png", M, 1.5, 7.4, crop_top=0)
    w = pd.read_csv(DB / "porta_sidewalk_width.csv")
    p = w[w.is_plane]
    c = p.size_class.value_counts()
    for k, (big, small, col) in enumerate([(f"{c['large']} + {c['medium']}", "planes keep a real choice: several large or medium species", TREE),
                                           (f"{c['small'] + c['none']}", "forced to a small tree or to none by the literal rule", HEAT),
                                           (f"{c['check']}", "medians and plaza edges: no size filter (ASSUMPTION)", MUTED)]):
        card(s, 8.4, 1.55 + k * 1.65, 4.4, 1.45, big, small, col, 28, 13)
    source(s, "Ajuntament de Barcelona, Mapa base topogràfic 1:1000 (CC BY 4.0); Gestió de l'arbrat viari de Barcelona (2011) pp. 22–23.")


# ---- image versions Giovanni preferred (9 Nov): flowcharts, crowns and radar back as images, footer cropped -------------
def fig_slide(path, title, sub, src=None, crop_bottom=0.075):
    def build(s):
        head(s, title, sub)
        picture(s, ROOT / path, M + 0.15, 1.45, W - 2 * M - 0.3, crop_bottom=crop_bottom)
        if src:
            source(s, src)
    return build


IMG = {
    6: fig_slide("slides/fig_v8/v8_crowns.png", "Why it matters: the crowns differ",
                 "Crown area as a share of a plane's, same trunk size, Porta's own trees",
                 "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, arbrat viari (trunk class)."),
    10: fig_slide("slides/fig_v7/flow_00_overview.png", "Methodology",
                  "Which species replace the trees a project must cut, and where to add new ones"),
    11: fig_slide("slides/fig_v7/flow_04_design.png", "Design module", "Inside the project area the designer draws"),
    12: fig_slide("slides/fig_v7/res_01_radar.png", "First results: replacing Porta's 832 plane trees",
                  "The optimised layout keeps almost all of today's summer shade; the city's announced mix loses about an eighth",
                  "City mix: Betevé, 7 May 2026. Storm: PDISBA, 2-year 60-min. Heat = shade proxy, not yet UTCI."),
    "B1": fig_slide("slides/fig_v7/flow_02_heat.png", "Backup B1 · Heat module", "Fast proxy inside the loop, full UTCI on the final layouts"),
    "B2": fig_slide("slides/fig_v7/flow_03_runoff.png", "Backup B2 · Runoff module", "Event runoff on a 1 m grid, routed to the flood hotspots"),
    "B3": fig_slide("slides/fig_v7/flow_01_screening.png", "Backup B3 · City screening", "Indicators for every street-tree position"),
    "B6": fig_slide("slides/fig_v7/flow_06_optimiser.png", "Backup B6 · How the optimiser finds the layout",
                    "No trial and error: a score table, then one exact solve per weight set",
                    "HiGHS open-source linear optimisation solver (highs.dev), called through SciPy."),
    "B7": fig_slide("slides/fig_v7/flow_05_validation.png", "Backup B7 · Validation plan",
                    "Each module checked against something it was not fitted to"),
}


SLIDES = [  # (outline heading number, builder)
    (1, s01_title), (2, s02_context), (3, s03_gate1), (4, s04_trees), (5, s05_problem), (6, IMG[6]), (7, s07_gap),
    (8, s08_rq), (9, s09_hyp),
    (10, IMG[10]), (11, IMG[11]),
    (12, IMG[12]), (13, s13_scenarios), (14, s14_map), (15, s15_cap), (16, s16_heat),
    (None, s_next), (None, s_cobenefits), (None, s_baseline),
    (None, IMG["B1"]), (None, IMG["B2"]), (None, IMG["B3"]), (None, b4_bars), (None, b4b_palette30), (None, b5_sizing), (None, IMG["B6"]),
    (None, IMG["B7"]),
    (None, s_simplifications),
]


def build():
    text_md = (ROOT / "slides/outline_10nov.md").read_text(encoding="utf-8")
    notes = {int(m.group(1)): m.group(2).strip() for m in
             re.finditer(r"^## (\d+)\..*?\*\*Say \(\d+ words\):\*\*\s*\n\"(.+?)\"\s*$", text_md, re.S | re.M)}
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for n, fn in SLIDES:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        s.notes_slide.notes_text_frame.text = notes.get(n, "Backup.")
    out = ROOT / "slides/shade_and_sponge_10nov_editable.pptx"
    prs.save(out)
    assert len(notes) == 16, sorted(notes)
    print("wrote", out.relative_to(ROOT), f"({len(SLIDES)} slides)")


if __name__ == "__main__":
    build()
