"""Editable 10 Nov deck: the same 26 slides as make_slides_v7.py, but text, cards, tables and charts are native
PowerPoint objects (python-pptx). Only the flowcharts, the city map, the crown figure and three backups stay as images
(their baked-in title is cropped and a native title is added). Speaker notes = the "Say" scripts of slides/outline_10nov.md.
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
from pptx.enum.shapes import MSO_SHAPE
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
    scrim = box(s, 0, 0, W * 0.62, H, "#1E1C19", radius=0, name="Scrim")
    alpha = scrim.fill._xPr.find(qn("a:solidFill"))[0]
    alpha.append(alpha.makeelement(qn("a:alpha"), {"val": "72000"}))
    text(s, 0.75, 2.2, 7.4, 1.0, "Shade and Sponge", 54, "#F2F0EA", True, name="Title")
    text(s, 0.75, 3.35, 7.0, 1.4, "A computational method for choosing which species replace a city's street trees, and where, "
         "scored on summer heat and on storm runoff. First case: Barcelona's plane trees (Platanus).", 22, "#F2F0EA")
    text(s, 0.75, 5.15, 7.0, 0.4, "MaCAD, IAAC  ·  Tutor session with A. Chronis, 10 November 2026", 16, "#CFC9BC")
    text(s, 0.75, H - 0.6, 11.5, 0.3, "Horts urbans de Porta, Carrer d'Alcúdia × Carrer de la Maladeta, Nou Barris: "
         "the bare crowns in the foreground are the plane trees this thesis is about.", 11, "#CFC9BC")


def s02_context(s):
    head(s, "The decision is already taken", "Barcelona is replacing its plane trees, one at a time")
    for k, (big, small, c) in enumerate([
            ("−56%", "Plane trees in ten years: 43,722 trees, 27.45% of the stock → 12% (press, May 2026)", HEAT),
            ("15% · 30%", "Master plan 2017–2037: no species above 15%; tree cover up to 30% of the urban surface", TREE),
            ("1 by 1", "Each tree is replaced when it dies or when its street is rebuilt: thousands of decisions", WARN)]):
        card(s, M + k * 4.18, 1.75, 3.9, 2.9, big, small, c, 44, 17)
    text(s, M, 5.15, W - 2 * M, 0.8, "This is the context, not the problem: the city has already decided how much of each "
         "species. What follows is what it has not decided.", 19, INK)
    source(s, "Nació Digital 4 May 2026 and Betevé 7 May 2026 (press); Arbres per viure, Pla director de l'arbrat 2017–2037, "
           "targets 1 and 3; notes/tree_master_plan.md.")


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
    text(s, M, 4.35, 6.0, 0.4, "Criteria: tolerance, street type, tradition, technicians' experience.", 15, INK)
    text(s, M, 4.8, 6.0, 0.5, "No heat. No runoff.", 24, HEAT, True)
    text(s, M, 5.35, 6.0, 0.5, "The 2011 guide, still in force, no longer prints the table: only a species catalogue.", 14, MUTED)
    # right: practice, as a native bar chart
    text(s, 7.05, 1.6, 5.7, 0.3, "IN PRACTICE · Porta, trees planted 2007–2026", 14, WARN, True)
    cd = CategoryChartData()
    cats, vals = [], []
    for cls, lab in (("small", "Narrow sidewalks"), ("medium", "Medium sidewalks")):
        g = rc[rc.size_class == cls]
        cats.append(f"{lab} ({g.n.sum()} trees)")
        vals.append(g[g.in_table].n.sum() / g.n.sum())
    cd.categories = cats
    cd.add_series("Share matching the 2004/2005 table", vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(7.05), Inches(1.95), Inches(5.7), Inches(2.3), cd).chart
    style_chart(ch, [WARN], legend=False, fmt='0%', size=14)
    quiet_axes(ch, 0, 1)
    ch.category_axis.reverse_order = True
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0%', False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Share matching the table"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
    big = rc[rc.size_class == "large"]
    pl = big[big.genus_sp.str.startswith("Platanus")].n.sum()
    text(s, 7.05, 4.4, 5.7, 0.4, f"Wide sidewalks · {big.n.sum()} trees planted, {pl} of them planes", 15, INK, True)
    text(s, 7.05, 4.8, 5.7, 0.8, "Rebuilt streets and exceptions follow other lists and cannot be told apart in the inventory, "
         "so ~90% is an upper bound on non-compliance.", 13, MUTED)
    box(s, M, 5.95, W - 2 * M, 0.6, tint(INK, 0.06))
    text(s, M + 0.25, 6.07, W - 2 * M - 0.5, 0.4, "A rule exists, it is qualitative, and it is not visible in practice. "
         "Current list: asked the city (email sent 24 Oct).", 16, INK, True)
    source(s, "Arbrat viari: selecció d'espècies (2002, rev. 2004) p. 11; Pla de gestió de l'arbrat viari (2005, rev. 2006) §3.4.3; "
           "Gestió de l'arbrat viari (2011) §11; scripts/replacement_rule_check.py; notes/tree_master_plan.md §5b.")


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
    text(s, M, 3.85, W - 2 * M, 0.4, f"Porta today {cov:.1f}% (LiDAR 2021) · city target 30% by 2037 · gap ≈ 8.3 ha of crown",
         16, INK, True)
    card(s, M, 4.45, 5.9, 1.9, "≈ 29%", "of Porta's canopy is plane trees (5.75% of the area, 832 trees)", HEAT)
    card(s, M + 6.33, 4.45, 5.9, 1.9, "16% ↔ 20%", "All planes replaced by a Brachychiton-size crown → ~16%; "
         "by a Tipuana or Jacaranda-size crown → roughly unchanged", TREE)
    source(s, "ICGC LiDAR 26 Sept 2021, canopy = CHM > 2 m (scripts/porta_canopy_cover.py); plan target 1 (30%); "
           "crown ratios at equal trunk size, notes/topic_decision.md §9.9 and §10.3.")


def s05_problem(s):
    head(s, "The problem", "Context, problem and gap, kept apart")
    box(s, M, 1.6, W - 2 * M, 3.4, tint(INK, 0.06))
    text(s, M + 0.45, 1.6, W - 2 * M - 0.9, 3.4, "When Barcelona replaces a plane tree, the only documented rule for the new "
         "species is qualitative (district, sidewalk width, tradition). No rule quantifies heat or runoff, so thousands of "
         "replacements will change each street's shade and rain interception, and nobody measures by how much.",
         26, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    for k, (lab, txt, c) in enumerate((("CONTEXT", "plane removal, 15% cap, one tree at a time", MUTED),
                                       ("PROBLEM", "a qualitative rule, not visible in practice", HEAT),
                                       ("GAP", "no quantities for heat or runoff, per position", RAIN))):
        text(s, M + k * 4.18, 5.4, 3.9, 1.0, [[(lab, {"bold": True, "color": c, "size": 14})], txt], 17, INK)
    source(s, "notes/topic_decision.md §10.1–10.2.")


def s06_crowns(s):
    head(s, "Why it matters: the crowns differ", "At equal trunk size, the allowed species carry very different crowns")
    picture(s, ROOT / "slides/fig_v6/v6_04_crowns.png", M + 0.6, 1.5, W - 2 * M - 1.2)


def s07_gap(s):
    head(s, "The gap", "Rules without numbers, tools without species or runoff, and a cap with no evidence behind it")
    cols = [("IN PRACTICE", HEAT, ["Rules for which species: catalogue, sidewalk size, 15% cap",
                                   "No number for what a choice does to heat or runoff",
                                   "City strategy in hectares; Nature Plan project 83 (p.114): \"which species for shade, where\" still to study"]),
            ("IN RESEARCH", RAIN, ["Heat and runoff for fixed scenarios, without species traits (Mannucci et al. 2025; Wu et al. 2024)",
                                   "Optimisers for heat only (Shaamala et al. 2025; Peng et al. 2026)",
                                   "Trait-based recommender with the runoff module switched off (SylvCiT; Nicol et al. 2026)"])]
    for k, (hd, c, items) in enumerate(cols):
        x = M + k * 6.33
        text(s, x, 1.55, 5.9, 0.3, hd, 14, c, True)
        for j, it in enumerate(items):
            box(s, x, 1.9 + j * 0.88, 5.9, 0.76, tint(c, 0.10))
            text(s, x + 0.25, 1.9 + j * 0.88, 5.4, 0.76, it, 14, INK, anchor=MSO_ANCHOR.MIDDLE)
    box(s, M, 4.65, W - 2 * M, 1.0, tint(WARN, 0.10))
    text(s, M + 0.25, 4.72, W - 2 * M - 0.5, 0.9, [[("IN THE DIVERSITY LITERATURE", {"bold": True, "color": WARN, "size": 13})],
         "Species caps are rules of thumb (Kendal et al. 2014, after Santamour 1990). Targets far below the current share risk that "
         "“well adapted species may be abandoned for underperforming species” (Kendal et al. 2014, p. 415): the planes, ~27% vs a 15% cap."],
         14, INK)
    box(s, M, 5.85, W - 2 * M, 0.7, tint(TREE, 0.14))
    text(s, M + 0.25, 5.85, W - 2 * M - 0.5, 0.7, "This method: trait-based, inside the city's rules, scored on heat and runoff, per position.",
         19, TREE, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "notes/topic_decision.md §7, §9.2, §10.2; Santamour 1990 (METRIA 7) pp. 57-65; Kendal, Dobbs & Lohr 2014 (UFUG 13:411-417); "
           "Ajuntament de Barcelona, Pla Natura 2021–2030 p. 114.")


def s08_rq(s):
    head(s, "The research question, scrutinised", "One main question, four sub-questions, each with a metric")
    box(s, M, 1.55, W - 2 * M, 1.55, tint(INK, 0.06))
    text(s, M + 0.35, 1.55, W - 2 * M - 0.7, 1.55, "Can a trait-based layout method, inside Barcelona's tree rules, choose "
         "replacement species for plane trees and new planting spots that retain and add more pedestrian cooling and "
         "storm-water interception than the city's own practice?", 21, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    sq = [("SQ1 · heat", "Mean UTCI 12–17 h on a hot design day", HEAT),
          ("SQ2 · runoff", "Total and at flood hotspots, 2-yr 60-min storm; larger than the model resolves (Δmin)?", RAIN),
          ("SQ3 · trade-off", "Do the heat-best and runoff-best layouts differ, and in which species?", WARN),
          ("SQ4 · additions", "How much of the gap to 30% can new street trees close, and where?", TREE)]
    for k, (hd, txt, c) in enumerate(sq):
        x, y = M + (k % 2) * 6.33, 3.3 + (k // 2) * 1.2
        box(s, x, y, 5.9, 1.05, tint(c, 0.10))
        text(s, x + 0.25, y + 0.12, 5.4, 0.9, [[(hd, {"bold": True, "color": c, "size": 16})], txt], 15, INK)
    text(s, M, 5.8, W - 2 * M, 0.7, "Changed after scrutiny: 'reduce' → 'retain' (against the city's practice, today as reference) · "
         "additions co-equal · 'not resolved' is an allowed answer · baseline = the city's observed replacement mix (S1b), "
         "with the announced mix (S1a) beside it", 14, MUTED)
    source(s, "notes/topic_decision.md §10.5 (scrutiny table) and §10.6; notes/methodology.md §7.")


def s09_hyp(s):
    head(s, "Hypotheses", "Two to test, one declared limit")
    items = [("H1", "Trait-based layouts beat the city's practice on heat and on runoff", "Runoff is a check: below Δmin = 91 m³ it is 'not resolved'; tree pits and grouping matter more than species", TREE),
             ("H2", "The heat-best and runoff-best layouts differ in species", "Tested on the Pareto front (SQ3)", WARN),
             ("Boundary", "At extreme storms, street trees cannot matter", "Was H3; true by construction of the model, so declared, not tested", MUTED)]
    for k, (h, txt, sub, c) in enumerate(items):
        y = 1.6 + k * 1.6
        box(s, M, y, W - 2 * M, 1.35, tint(c, 0.10))
        text(s, M + 0.35, y, 1.9, 1.35, h, 32, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.5, y + 0.25, W - 2 * M - 2.8, 1.0, [[(txt, {"bold": True, "size": 22})], [(sub, {"color": MUTED})]], 16, INK)
    source(s, "notes/topic_decision.md §8, §9.5, §10.5.")


def flow(s, fig, title, sub):
    head(s, title, sub)
    picture(s, ROOT / "slides/fig_v7" / fig, M + 0.15, 1.45, W - 2 * M - 0.3)


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
    text(s, 7.9, 5.1, 4.9, 1.3, ["100 = today. Outward = better. Read axis by axis: the polygon's area means nothing.",
                                 "Observed mix S1b: 90.3% summer shade (backup B9)."], 13, MUTED)
    source(s, "databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv. Heat = effective-shade proxy, not yet UTCI. Runoff: T2-60 storm. "
           "S1a = 2026 mix (press) placed at random within the sidewalk rule, 10 seeds.")


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
              ("Canopy cover, points vs today", "canopy_pct", lambda v, c: v - s0[c], TREE)]
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
        if "%" in lab:
            quiet_axes(ch, 10 * int((min(vals) - 5) // 10), None)
        else:
            quiet_axes(ch)
            ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        ch.has_title = True
        ch.chart_title.text_frame.text = lab
        r = ch.chart_title.text_frame.paragraphs[0].runs[0].font
        r.size, r.bold, r.color.rgb = Pt(13), True, rgb(c)
    source(s, "databases/barcelona/additions_summary.csv (scripts/run_additions.py); spots: scripts/porta_planting_spots.py and "
           "porta_spot_exclusions.py (2011 guide spacing; an upper bound: driveways and services not in the data). Heat = effective-shade proxy.")


def s14_map(s):
    head(s, "City-wide: 28 barris, one layout", "Summer shade gained over the city's mix, one optimisation under the 15% city cap")
    picture(s, ROOT / "slides/fig_v7/res_04_city_map.png", M, 1.45, 7.6, crop_bottom=0.10, crop_right=0.43)
    text(s, M, 6.45, 7.6, 0.3, "Darker green = larger gain over the city's mix · ochre = loss (Bonanova) · grey = not computed (< 500 planes)", 12, MUTED)
    d = cw.d
    for k, (big, small, c) in enumerate([(f"+{d.gain.median():.1f} pts", "median gain of summer shade over the city's mix", TREE),
                                         (f"{(d.gain > 0).sum()} of {len(d)}", f"barris gain ({d.planes.sum():,} planes)", TREE),
                                         ("Bonanova", "loses a little: with one city cap the capped species go where they add most", WARN)]):
        card(s, 8.85, 1.55 + k * 1.75, 3.95, 1.55, big, small, c, 28, 13)
    source(s, cw.SRC)


def s15_cap(s):
    head(s, "Two rules: a city cap and a local ceiling",
         "The city's 15% fixes how much of each species; the local ceiling stops any barri ending more concentrated than today")
    box(s, M, 1.6, 5.6, 1.75, tint(TREE, 0.10))
    text(s, M + 0.25, 1.72, 5.1, 1.6, [[("1. CITY CAP: how much of each species", {"bold": True, "color": TREE})],
         "No species above 15% of the city's street trees (tree master plan). The headroom left today is shared across barris "
         "pro rata to the planes each replaces (ASSUMPTION)."], 14, INK)
    box(s, M, 3.5, 5.6, 1.95, tint(WARN, 0.10))
    text(s, M + 0.25, 3.62, 5.1, 1.8, [[("2. LOCAL CEILING: no barri more concentrated than today", {"bold": True, "color": WARN})],
         "In each barri, no species ends with more trees than the barri has planes today. Without it, the city cap alone put "
         "Tipuana at 48.5% of Diagonal Mar's street trees; with it, 37.2% (17-barri run). It costs little shade."], 14, INK)
    text(s, M, 5.6, 5.6, 0.9, "Limit: where few planes are replaced the ceiling can leave no species that fits a position "
         "(Baró de Viver, 15 planes; la Trinitat Vella, 167). These barris need a different ceiling.", 13, MUTED)
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
    text(s, 6.55, 5.95, 6.25, 0.6, "Dark red = at the cap: Celtis (already common, little headroom) and Tipuana. "
         "Within the cap the LP decides which barri gets them.", 13, MUTED)
    source(s, cw.SRC + " Cap: floor(15% × 140,404 street trees) minus each species today, pro rata to 31,580 of 40,137 city planes.")


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
    text(s, M, 5.2, 6.6, 1.3, "TMYx 2011–2025. The Python chain reproduces Ladybug in Grasshopper (bias −0.01/−0.02 °C, r 0.998–0.999), "
         "so it can let light through the crowns. 15 July is an ordinary July day, not yet the hot design day.", 12, MUTED)
    r0 = np.corrcoef(v.shade_lai_S0, v.utci_S0)[0, 1]
    r1 = np.corrcoef(v.d_shade_opaque, v.d_utci)[0, 1]
    x = 7.5
    for k, (big, small, c) in enumerate([(f"r = {r0:.2f}".replace("-", "−"), "shade proxy vs Ladybug UTCI across 1,974 points", TREE),
                                         (f"r = {r1:.2f}".replace("-", "−"), "on the S4 − S0 change per point", TREE)]):
        text(s, x, 1.5 + k * 0.95, 5.3, 0.9, [[(big, {"size": 26, "bold": True, "color": c})], small], 13, INK)
    box(s, x, 3.45, 5.3, 0.75, tint(TREE, 0.14))
    text(s, x + 0.2, 3.45, 4.9, 0.75, "Claim: for heat, no worse than today's planes within model uncertainty.", 15, TREE, True,
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x, 4.35, 5.3, 2.3, [[("Next", {"bold": True, "color": WARN})],
         "To 1 Dec: UTCI of the final layouts (Infrared City), hot design day, priority score, city screening layer.",
         "To 18 Dec: project tool anywhere in Barcelona, Sant Antoni transfer test.",
         [("Asks: ", {"bold": True}), ("porous crowns in Infrared? · Sant Antoni enough as transfer? · may a barri lose while the city gains?", {})]],
         13, INK)
    source(s, "databases/barcelona/hb_utci_andreu_nin.csv, porous_utci_*_epw2011.csv, ladybug_vs_proxy_andreu_nin.csv; "
           "notes/methodology.md §5b. Porous crowns after Peng et al. 2026.")


def s_next(s):
    head(s, "What comes next", "Porta first, then the whole city")
    steps = [("to 1 Dec", "UTCI of the final layouts (Infrared City) · hot design day · priority score · city screening layer", HEAT),
             ("after 10 Nov", "City LP rerun against the observed mix (S1b) · co-benefits reported per layout", TREE),
             ("to 18 Dec", "Project tool anywhere in Barcelona · Sant Antoni transfer test · booklet · final presentation", RAIN)]
    for k, (when, what, c) in enumerate(steps):
        y = 1.6 + k * 1.15
        box(s, M, y, 7.6, 0.95, tint(c, 0.10))
        text(s, M + 0.25, y, 1.7, 0.95, when, 18, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.05, y, 5.4, 0.95, what, 15, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 8.65, 1.6, 4.1, 0.4, "QUESTIONS FOR YOU", 15, WARN, True)
    for k, q in enumerate(("Does Infrared City model porous crowns?", "Is a within-city transfer (Sant Antoni) enough?",
                           "May a barri lose while the city gains?")):
        text(s, 8.65, 2.15 + k * 0.95, 4.1, 0.9, q, 17, INK, True)
    source(s, "notes/citywide_plan.md §4; notes/methodology.md §10; slides/outline_10nov.md slide 16.")


def s_cobenefits(s):
    head(s, "Co-benefits not optimised (yet)", "Reported after 10 Nov, not objectives of the tool")
    rows = [("Pollen", "Plane pollen gets the top allergen score (4 of 4) in a Spanish species index",
             "Species index exists (IUGZA, Cariñanos et al. 2014). Replacing planes likely gains here; to compute per layout", WARN),
            ("Carbon", "Storage grows steeply with trunk size, and the planes are large",
             "The tool's mix may lose here at first. Urban allometry (McPherson et al. 2016); reported even if it loses", INK),
            ("Diversity", "The 15% cap and the local ceiling already act on it",
             "Already computed (effective species, as in SylvCiT): to report per barri, before and after", TREE),
            ("Ozone · VOC", "Some species emit isoprene; ozone also depends on local NOx", "Not modelled: a declared limit", MUTED)]
    for k, (h, txt, sub, c) in enumerate(rows):
        y = 1.5 + k * 1.05
        box(s, M, y, W - 2 * M, 0.92, tint(c, 0.10))
        text(s, M + 0.3, y, 2.2, 0.92, h, 22, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.7, y + 0.1, W - 2 * M - 3.0, 0.8, [[(txt, {"bold": True, "size": 17})], [(sub, {"color": MUTED})]], 13, INK)
    box(s, M, 5.85, W - 2 * M, 0.62, tint(INK, 0.06))
    text(s, M + 0.25, 5.85, W - 2 * M - 0.5, 0.62, "The master plan already lists allergies and VOC among the disservices to avoid, "
         "with no number per species.", 16, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Cariñanos, Casares-Porcel & Quesada-Rubio 2014 (Landsc. Urban Plan. 123:134-144); McPherson, van Doorn & Peper 2016 "
           "(PSW-GTR-253); Pla director de l'arbrat 2017–2037 §1.3.4, p. 14; notes/cobenefits_plan.md.")


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
    source(s, "Open Data BCN arbrat-viari, 35 quarterly files 2018–2026 (scripts/inventory_history.py); layout.s1b_mix(); "
           "databases/barcelona/barris_summary.csv; notes/data_sources_pemb_30oct.md §6; notes/topic_decision.md §10.4.")


def backup_img(fig, title, sub):
    return lambda s: flow(s, fig, title, sub) if fig.startswith(("flow", "res")) else (
        head(s, title, sub), picture(s, ROOT / "slides" / fig, M + 0.15, 1.45, W - 2 * M - 0.3))


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
    source(s, "study/guide.md §11; notes/methodology.md §4b, §5b; RM seminar L04 (5 Nov), feedback on the runoff module.")


SLIDES = [  # (outline heading number, builder)
    (1, s01_title), (2, s02_context), (3, s03_gate1), (4, s04_trees), (5, s05_problem), (6, s06_crowns), (7, s07_gap),
    (8, s08_rq), (9, s09_hyp),
    (10, lambda s: flow(s, "flow_00_overview.png", "Methodology",
                        "Which species replace Barcelona's plane trees, and where to add new ones: scored on heat, runoff and canopy")),
    (11, lambda s: flow(s, "flow_04_design.png", "Design module", "Inside the project area the designer draws")),
    (12, s12_radar), (13, s13_scenarios), (14, s14_map), (15, s15_cap), (16, s16_heat),
    (None, s_next), (None, s_cobenefits), (None, s_baseline),
    (None, lambda s: flow(s, "flow_02_heat.png", "Backup B1 · Heat module", "Effective shade, checked against Ladybug UTCI")),
    (None, lambda s: flow(s, "flow_03_runoff.png", "Backup B2 · Runoff module", "Canopy bucket, then curve number, event volume")),
    (None, lambda s: flow(s, "flow_01_screening.png", "Backup B3 · City screening", "Indicators for every tree")),
    (None, lambda s: flow(s, "res_02_bars.png", "Backup B4 · Results in real units", "Differences from the city's rule, with the model threshold Δmin")),
    (None, lambda s: flow(s, "res_07_palette30.png", "Backup B4b · Wider palette (30 species)", "Porta and 32 barris, each optimised alone")),
    (None, backup_img("fig_v6/v6_09_sizing_rule.png", "Backup B5 · The sizing rule leaves real choice", "Several species per sidewalk size class")),
    (None, lambda s: flow(s, "flow_05_validation.png", "Backup B7 · Validation plan", "Each module against data it was not fitted to")),
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
