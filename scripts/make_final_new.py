"""Final defense (15 Dec 2026): the NEW slides only, in the midterm style (same helpers, fonts, palette).
They will be merged with the kept midterm slides after Giovanni's one-by-one review.
Numbers: Porta, Barcelona palette, trunk class TERCERA, after the needle-tree fix (PR #184):
  databases/barcelona/tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv (balanced = S4_s0.50_w0.25_r0.25),
  diversity_series.csv, ..._replporta_plan_planes.csv (S1c) and ..._div9.7_..._replporta_plan_planes.csv,
  backtest_works_guide.csv (23/26; added summer shade per tree, median, city 76 vs method 130 m2h).
Slots marked "RHINO" are placeholders for visuals Giovanni will render in Rhino.
Output: slides/final/shade_and_sponge_final_new.pptx. Run from scripts/: python make_final_new.py
"""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
import make_rm_personal as R
from make_rm_personal import ico, ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, rgb, tint, text, box, head, source
from make_midterm_pechakucha import page_number, BCN

OUT = ROOT / "slides/final"
GREY = "#A8A293"


def rhino(s, x, y, w, h, what, kind="RHINO"):
    """Dashed placeholder for a visual still to make (kind: RHINO render, or MAP / VISUAL from the tool or by hand)."""
    b = box(s, x, y, w, h, tint(GREY, 0.12), line=GREY, name="RHINO placeholder")
    b.line.dash_style = 4
    text(s, x + 0.3, y, w - 0.6, h, [[(kind + "  ", {"bold": True, "color": MUTED}), (what, {"color": MUTED})]], 14, MUTED,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def bars(s, x, y, w, h, cats, vals, colors, axis_min=80, axis_max=110):
    """Native horizontal bar chart (editable in PowerPoint), one colour per bar, value labels in %."""
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("summer shade, % of today", vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    ch.has_legend = False
    ch.font.name, ch.font.size, ch.font.color.rgb = R.FONT, Pt(15), rgb(INK)
    va, ca = ch.value_axis, ch.category_axis
    va.minimum_scale, va.maximum_scale = axis_min, axis_max
    va.has_major_gridlines, va.visible = False, False
    ca.reverse_order = True
    ca.format.line.fill.background()
    pl = ch.plots[0]
    pl.gap_width = 45
    pl.has_data_labels = True
    pl.data_labels.number_format, pl.data_labels.number_format_is_linked = '0.0"%"', False
    pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    pl.data_labels.font.bold, pl.data_labels.font.size = True, Pt(16)
    for pt, c in zip(pl.series[0].points, colors):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(c)
    return ch


def pic_h(s, name, x, y, h, w_max=None):
    """Picture from slides/final/fig (make_final_maps.py), sized by height, capped at w_max, centred in w_max."""
    from PIL import Image
    iw, ih = Image.open(ROOT / f"slides/final/fig/{name}.png").size
    w = h * iw / ih
    if w_max and w > w_max:
        w, h = w_max, w_max * ih / iw
    return R.picture(s, ROOT / f"slides/final/fig/{name}.png", x + ((w_max or w) - w) / 2, y, w, crop_top=0)


def n_question(s):
    head(s, "Research question", "Two references: the city's practice first, then today")
    box(s, M, 1.55, W - 2 * M, 1.55, tint(TREE, 0.10))
    text(s, M + 0.4, 1.55, W - 2 * M - 0.8, 1.55,
         [[("When a street project in Barcelona must replace trees, ", {"bold": True}),
           ("can a trait-based method, inside the city's tree rules, choose the new species and positions so that "
            "summer cooling and rain interception improve, or at least do not get worse, compared with the city's practice and with today?", {})]],
         18, INK, anchor=MSO_ANCHOR.MIDDLE)
    for k, (tag, t, c) in enumerate((("H1", "No worse than the city's practice on heat or runoff, better on summer shade, and no more winter shade than today", HEAT),
                                     ("H2", "The heat-best and the runoff-best layouts use different species", RAIN))):
        x = M + k * 6.2
        box(s, x, 4.75, 5.9, 1.4, tint(c, 0.12))
        text(s, x + 0.3, 4.75, 5.4, 1.4, [[(tag + "  ", {"bold": True, "color": c, "size": 30}), (t, {})]], 17, INK, anchor=MSO_ANCHOR.MIDDLE)
    sq = [("SQ1", "Heat: felt temperature, 12–17 h on a hot day", HEAT), ("SQ2", "Runoff: 2-year, 60-min storm, total and at flood spots", RAIN),
          ("SQ3", "Trade-off: do heat and runoff want different species?", WARN), ("SQ4", "How much of the canopy gap can new trees close?", TREE)]
    for k, (tag, t, c) in enumerate(sq):
        x = M + k * 3.1
        text(s, x, 3.3, 2.9, 1.3, [[(tag, {"bold": True, "color": c, "size": 18})], t], 14, INK)
    text(s, M, 6.35, W - 2 * M, 0.4, "Boundary: extreme storms on saturated soil are outside what street trees can change.", 14, MUTED)


def n_heat(s):
    head(s, "Heat module", "Shade where and when people walk: summer shade a benefit, winter shade a cost")
    R.picture(s, ROOT / "slides/fig_v7/flow_02_heat.png", M + 0.1, 1.4, W - 2 * M - 0.2, crop_top=0.17, crop_bottom=0.2)
    text(s, M, 6.3, W - 2 * M, 0.5, [[("Winter: ", {"bold": True}), ("evergreen crowns that shade in summer also shade in winter, "
         "so the same sun check on a January day counts that shade as a cost.", {})]], 15, INK)
    source(s, "ICGC, LiDAR 2021; Ladybug Tools; Infrared City; Bröde et al. 2012 (UTCI).")


def n_runoff(s):
    head(s, "Runoff module", "Rain on a 1 m grid: what the crowns hold, what the ground takes, where the rest flows")
    R.picture(s, ROOT / "slides/fig_v7/flow_03_runoff.png", M + 0.1, 1.4, W - 2 * M - 0.2, crop_top=0.17, crop_bottom=0.2)
    source(s, "Anys & Weiler 2024 (interception); USDA SCS curve number; Barcelona, PDISBA design storms; ICGC, LiDAR 2021.")


def n_scenarios(s):
    head(s, "Scenarios", "Same streets, same tree positions, different choice of species")
    rows = [("S0", "Today", "the trees as they stand", "LiDAR 2021", INK),
            ("S1a", "City, announced", "the 2026 replacement mix the city announced", "press, 2026", RAIN),
            ("S1b", "City, practice", "what the city really planted where it removed a tree, 2018–2026", "tree inventory", RAIN),
            ("S1c", "City, plan", "the species the city has planned for each Porta tree", "Parcs i Jardins", RAIN),
            ("Method", "This thesis", "species chosen by the optimiser, inside the same rules", "HiGHS", TREE)]
    for k, (tag, name, what, src, c) in enumerate(rows):
        y = 1.55 + k * 0.8
        box(s, M, y, W - 2 * M, 0.68, tint(c, 0.10 if k % 2 == 0 else 0.05))
        text(s, M + 0.25, y, 1.5, 0.68, tag, 18, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 1.9, y, 2.6, 0.68, name, 16, INK, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 4.6, y, 5.6, 0.68, what, 15, INK, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 10.3, y, 1.9, 0.68, src, 13, MUTED, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 1.55 + 5 * 0.8 + 0.1, W - 2 * M, 0.5, "Note: the city's 2004/05 district × sidewalk table is cited, not run", 13, MUTED)
    source(s, BCN + " Open Data BCN, arbrat viari 2018–2026; Huangfu & Hall 2018 (HiGHS).")


def dumbbell(s, x, y, w, ic, label, city, method, city_lab, lo=90, hi=112, c=HEAT):
    """One metric as two dots on a % of today track: city (blue) and method (green), dashed tick = today (100)."""
    from pptx.enum.shapes import MSO_SHAPE
    ico(s, ic, c, x, y, 0.38)
    text(s, x + 0.5, y - 0.05, w - 0.5, 0.45, label, 15, c, True)
    ty = y + 1.05
    px = lambda v: x + 0.15 + (w - 0.3) * (v - lo) / (hi - lo)
    box(s, x + 0.15, ty - 0.02, w - 0.3, 0.04, "#DCD8CE", radius=0)
    t = s.shapes.add_connector(1, Inches(px(100)), Inches(ty - 0.3), Inches(px(100)), Inches(ty + 0.3))
    t.line.color.rgb, t.line.dash_style, t.line.width = rgb(MUTED), 4, Pt(1)
    if city != method:
        a, b = sorted((px(city), px(method)))
        box(s, a, ty - 0.05, b - a, 0.1, tint(TREE, 0.35), radius=0)
    for v, col, lab, up in ((city, RAIN, city_lab, True), (method, TREE, "Method", False)):
        d = 0.28 if col == TREE else 0.22
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(px(v) - d / 2), Inches(ty - d / 2), Inches(d), Inches(d))
        o.fill.solid(); o.fill.fore_color.rgb = rgb(col); o.line.fill.background()
        if city == method and col == TREE:
            continue
        yy = ty - 0.72 if up else ty + 0.22
        text(s, px(v) - 0.8, yy, 1.6, 0.5, [[(f"{v:.0f}", {"bold": True, "size": 20 if col == TREE else 15, "color": col})],
             [(lab if city != method else "both", {"size": 10, "color": MUTED})]] if not up else
             [[(lab if city != method else "both", {"size": 10, "color": MUTED})], [(f"{v:.0f}", {"bold": True, "size": 15, "color": col})]],
             12, INK, align=PP_ALIGN.CENTER)


def results_panel(s, rows, city_lab):
    x = M + 8.1
    for k, (ic, lab, cv, mv, c) in enumerate(rows):
        dumbbell(s, x, 1.5 + k * 1.85, W - M - x, ic, lab, cv, mv, city_lab, c=c)
    y = 1.5 + len(rows) * 1.85
    ico(s, "droplets", RAIN, x, y, 0.38)
    text(s, x + 0.5, y - 0.05, W - M - x - 0.5, 0.8, [[("Runoff", {"bold": True, "color": RAIN})], f"method = {city_lab.lower()}"], 15, INK)
    text(s, x, 6.2, W - M - x, 0.35, "% of today's shade;  ┆ = today", 11, MUTED)


def n_porta(s):
    head(s, "Result: Porta", "Replacing the 832 planes")
    rhino(s, M, 1.45, 7.3, 4.9, "Porta map: streets coloured by summer shade gain, method vs city practice", "MAP")
    results_panel(s, [("sun", "Summer shade", 98.9, 106.7, HEAT), ("snowflake", "Winter shade", 109, 99, RAIN)], "City practice")
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari; " + BCN)


def n_cityplan(s):
    head(s, "The city's own plan", "513 Porta planes the city plans to change, at the same diversity")
    rhino(s, M, 1.45, 7.3, 4.9, "Porta map: the 513 planes, coloured by species, city plan vs method", "MAP")
    results_panel(s, [("sun", "Summer shade", 98.2, 101.4, HEAT), ("snowflake", "Winter shade", 104.4, 98.1, RAIN)], "City plan")
    source(s, "Parcs i Jardins, planned species for Porta (2026); ICGC, LiDAR 2021; " + BCN)


def n_backtest(s):
    head(s, "Back-test: what the city really did", "26 groups of trees the city replaced, 2018–2026: its species vs the method's, same positions")
    box(s, M, 1.55, 5.9, 2.1, tint(TREE, 0.10))
    text(s, M + 0.4, 1.55, 5.2, 2.1, [[("23 of 26", {"bold": True, "color": TREE, "size": 44})], "groups where the method gives more summer shade"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    box(s, M, 3.85, 5.9, 2.1, tint(HEAT, 0.10))
    text(s, M + 0.4, 3.85, 5.2, 2.1, [[("1.7 ×", {"bold": True, "color": HEAT, "size": 44})], "the summer shade per tree (median), method vs city"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    R.picture(s, ROOT / "slides/fig_backtest/overview.png", 7.0, 1.4, 5.3, crop_top=0)
    text(s, M, 6.15, W - 2 * M, 0.4, "Runoff at flood spots: never worse than the city's choice (26 of 26).", 15, MUTED)
    source(s, "Open Data BCN, arbrat viari 2018–2026 (quarterly inventory); ICGC, LiDAR 2021.")


def n_diversity(s):
    head(s, "Diversity costs almost nothing", "Asking for more species in Porta, summer shade as a share of today's")
    bars(s, M, 1.5, 7.0, 4.4, ["no floor", "≥ 7.5 species", "≥ 9.4 (city's announced mix)", "≥ 15.6 (city's practice)", "≥ 20"],
         [106.7, 106.6, 106.3, 105.1, 103.5], [TREE, TREE, TREE, TREE, TREE], axis_min=95, axis_max=110)
    text(s, 8.1, 1.7, W - M - 8.1, 4.2,
         [[("−0.4 pts ", {"bold": True, "color": TREE, "size": 30}), ("to match the city's announced diversity", {})],
          [("Top species: 51% → 36% ", {"bold": True}), ("of the replacements", {})],
          [("At 20 effective species ", {"bold": True}), ("the method still beats the city's practice.", {})]], 16, INK)
    source(s, "Nicol et al. 2026 (effective number of species); " + BCN)


def n_stakeholders(s):
    head(s, "Who uses it, who decides", "The tool advises, people decide")
    cols = [("ruler", "Designer of the street project", ["draws the area", "sets keep / move / replace / add", "reads the report"], TREE),
            ("landmark", "City: Parcs i Jardins", ["sets the rules (sizes, 15% cap)", "approves the species", "plans the replacements"], RAIN),
            ("heart", "Neighbours", ["see the before / after"], HEAT)]
    for k, (ic, t, rows, c) in enumerate(cols):
        x = M + k * 4.18
        box(s, x, 1.55, 3.95, 4.4, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 1.8, 0.6)
        text(s, x + 0.3, 2.55, 3.4, 0.9, t, 19, c, True)
        text(s, x + 0.3, 3.5, 3.4, 2.4, rows, 16, INK)
    text(s, M, 6.15, W - 2 * M, 0.4, "Two kinds of designer: the city's own and commissioned firms.", 15, MUTED)
    source(s, BCN)


def n_contribution(s):
    head(s, "What the results say", "Each result, and how I read it")
    rows = [("Porta", "summer shade 107% vs 99%, winter 99% vs 109%", "the gain comes from the species alone: same spots, same works", TREE),
            ("City plan", "101% vs 98% at the same diversity", "diversity is not what costs the shade", TREE),
            ("Back-test", "more shade in 23 of 26 real replacements, 1.7× per tree", "it holds where the city really worked, not only in Porta", HEAT),
            ("Mataró", "83% vs 63% of the planes' shade, 6 of 6 streets", "it travels to another city with its own rules", RAIN),
            ("Runoff", "equal everywhere", "at street scale species barely move runoff: a do-no-harm check", MUTED)]
    for k, (t, res, mean, c) in enumerate(rows):
        y = 1.5 + k * 0.97
        box(s, M, y, W - 2 * M, 0.85, tint(c, 0.10 if k % 2 == 0 else 0.05))
        text(s, M + 0.25, y, 1.9, 0.85, t, 17, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 2.2, y, 4.8, 0.85, res, 14, INK, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 7.2, y, W - 2 * M - 7.4, 0.85, mean, 14, INK, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari 2018–2026; Parcs i Jardins (2026); Ajuntament de Mataró.")


def n_context_maps(s):
    head(s, "Context: replacing trees one at a time", "Barcelona, three numbers on the map")
    for k, (big, small, name, c) in enumerate((("10,976", "street trees replaced, 2018–2026, one dot each", "context_replaced", WARN),
                                              ("15%", "max per species; planes are 29% of street trees, above 15% in 46 of 73 barris (outlined)",
                                               "context_planes", TREE),
                                              ("20.1%", "Porta's canopy today; city target 30%", "context_canopy", HEAT))):
        x = M + k * 4.13
        pic_h(s, name, x, 1.4, 3.9, 3.93)
        text(s, x, 5.4, 3.93, 1.1, [[(big, {"bold": True, "color": c, "size": 30})], small], 13, INK)
    source(s, "Open Data BCN, arbrat viari 2018–2026; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; ICGC, LiDAR 2021.")


def n_crowns(s):
    head(s, "Same trunk, different crowns", "The 30 species at the plane's trunk size; dashed: the median plane crown")
    rhino(s, M, 1.45, W - 2 * M, 4.9, "30 coloured crowns, each with the dashed median plane crown on top (two versions to compare)", "VISUAL")
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari.")


def n_barri(s):
    head(s, "Why Porta", "First among Barcelona's neighbourhoods where flood hazard, heat and plane trees are all high")
    pic_h(s, "barri_screening", M, 1.5, 3.8, W - 2 * M)
    text(s, M, 5.4, W - 2 * M, 0.8, [[("The rule came first: ", {"bold": True}),
         ("a neighbourhood qualifies only if all three are above the city's 60th percentile; Porta ranks first.", {})]], 16, INK)
    source(s, "Barcelona Resilience Atlas (flood hazard); Landsat 8/9 (surface heat); Open Data BCN, arbrat viari.")


def n_porta_site(s):
    head(s, "Porta in numbers", "Nou Barris: 84 ha, 2,825 street trees, 832 planes (29%)")
    pic_h(s, "porta_canopy", M, 1.45, 4.9, 7.6)
    text(s, 8.45, 1.45, W - M - 8.45, 0.9, [[("20.1%", {"bold": True, "color": HEAT, "size": 30}), ("  canopy today, target 30%", {})]], 15, INK)
    pie(s, 8.4, 2.4, 2.4, 2.4, [46, 3, 6, 45], [TREE, RAIN, WARN, "#9DB596"])
    text(s, 10.9, 2.4, W - M - 10.9, 2.4, [[("■ ", {"color": TREE}), ("street trees 46%", {})], [("■ ", {"color": RAIN}), ("parks 3%", {})],
         [("■ ", {"color": WARN}), ("squares, courtyards 6%", {})], [("■ ", {"color": "#9DB596"}), ("not in the inventory 45%", {})]], 13, INK,
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, 8.45, 5.0, W - M - 8.45, 1.3, [[("Street trees alone cannot reach 30%: ", {"bold": True}),
         ("the choice of species is what is left.", {})]], 15, INK)
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari and parks; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


def n_species30(s):
    head(s, "The 30 species", "The palette after the screening: crowns from above, one scale (median Barcelona crown, LiDAR)")
    pic_h(s, "species30_top", M, 1.6, 4.6, W - 2 * M)
    source(s, "Open Data BCN, arbrat viari; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


def n_spots(s):
    head(s, "Where new trees go", "267 candidate spots in Porta")
    pic_h(s, "porta_spots_class", M, 1.45, 4.9, 9.2)
    x = M + 9.5
    text(s, x, 1.45, W - M - x, 4.9, [[("153", {"bold": True, "color": TREE, "size": 28}), ("  free", {})],
         [("103", {"bold": True, "color": WARN, "size": 28}), ("  conditional", {})], [("11", {"bold": True, "color": HEAT, "size": 28}), ("  blocked", {})],
         "", [("Conditional: a field check on underground services.", {"size": 13, "color": MUTED})]], 16, INK)
    source(s, BCN + " Open Data BCN, street furniture; OpenStreetMap.")


def n_species30b(s):
    head(s, "The 30 species", "Side view, one scale, with a 1.7 m person")
    pic_h(s, "species30_elev", M, 1.5, 4.8, W - 2 * M)
    source(s, "ICGC, LiDAR 2021 (median height, crown width and crown base per species); Open Data BCN, arbrat viari.")


def n_obstacles(s):
    head(s, "What stands in the way", "103 conditional spots: a project can move what blocks them")
    pic_h(s, "porta_spots_obstacle", M, 1.45, 4.9, 9.2)
    x = M + 9.5
    text(s, x, 1.45, W - M - x, 4.9, [[("Above ground", {"bold": True})], "signs, lamps, crossings and bollards: from the city's open data",
         "", [("Below ground", {"bold": True})], "water, gas, power: no open data; a field check before planting"], 14, INK)
    source(s, BCN + " Open Data BCN, street furniture; OpenStreetMap.")


def n_water(s):
    head(s, "Where the water goes", "Flow paths from the terrain and the city's flood hotspots in Porta")
    pic_h(s, "porta_water", M, 1.45, 4.9, W - 2 * M)
    source(s, "ICGC, LiDAR 2021 (terrain); Barcelona Resilience Atlas (flood hotspots).")


def n_practice(s):
    head(s, "City practice, not a rule", "The baseline is what the city really planted")
    rhino(s, M, 1.45, 8.4, 4.9, "Barcelona map: new plantings within / above the size their sidewalk allows", "MAP")
    items = [("landmark", "City practice", "the species the city planted, 2018–2026", RAIN),
             ("scale", "Same rules for both", "sidewalk size, 15% cap", WARN),
             ("sliders-horizontal", "What each rule costs", "switch a rule off, re-optimise", TREE)]
    x = M + 8.7
    for k, (ic, b, t, c) in enumerate(items):
        y = 1.45 + k * 1.68
        box(s, x, y, W - M - x, 1.5, tint(c, 0.10))
        ico(s, ic, c, x + 0.25, y + 0.2, 0.45)
        text(s, x + 0.85, y + 0.1, W - M - x - 1.0, 1.3, [[(b, {"bold": True, "color": c, "size": 17})], t], 14, INK)
    source(s, "Open Data BCN, arbrat viari 2018–2026; Parcs i Jardins, Gestió de l'arbrat viari (2011).")


def pie(s, x, y, w, h, vals, colors):
    """Native pie (editable), no legend, no labels."""
    cd = CategoryChartData()
    cd.categories = [str(k) for k in range(len(vals))]
    cd.add_series("share", vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.PIE, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    ch.has_legend, ch.has_title = False, False
    for pt, c in zip(ch.plots[0].series[0].points, colors):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(c)
        pt.format.line.color.rgb = rgb(BG)
    return ch


def n_effective(s):
    """Effective number of species = exp(Shannon); worked examples computed by hand (10 equal -> 10.0; 90% + 9 x 1.1% -> 1.7)."""
    head(s, "How we count diversity", "Effective species: how many equally common species the mix is worth")
    rhino(s, M, 1.45, 7.2, 4.9, "Porta map: street trees coloured by species, today vs method", "MAP")
    shades = [tint(TREE, 0.15 + 0.085 * k) for k in range(10)]
    for k, (vals, cols, eff, lab, c) in enumerate((([1] * 10, shades, "10", "10 species, equal", TREE),
                                                   ([90] + [10 / 9] * 9, [RAIN] + shades[1:], "1.7", "10 species, one at 90%", RAIN))):
        y = 1.45 + k * 2.45
        pie(s, 8.0, y, 2.2, 2.2, vals, cols)
        text(s, 10.3, y, W - M - 10.3, 2.2, [[(eff, {"bold": True, "color": c, "size": 36})], lab], 14, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 6.45, W - 2 * M, 0.4, [[("The city: ", {"bold": True}), ("9.4 in its announced mix, 15.6 in what it really planted.", {})]], 15, INK)
    source(s, "Nicol et al. 2026 (SylvCiT); Jost 2006 (effective number of species).")


def old_tag(s, label):
    """Small grey tag on the kept midterm slides, for the one-by-one review; delete once decided."""
    b = box(s, W - 2.3, 0.1, 2.0, 0.32, "#A8A293", radius=0.3, name="REVIEW tag")
    text(s, W - 2.3, 0.1, 2.0, 0.32, label, 11, BG, True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return b


def n_mataro(s):
    """Transfer test, first run (PR #150): crowns = Barcelona medians, Mataró LiDAR crowns not yet in."""
    head(s, "Transfer: Mataró", "Six plane streets, every plane replaced: summer shade of the new trees, method vs city practice")
    R.picture(s, ROOT / "slides/midterm/fig/mataro_streets.png", M, 1.45, 6.6, crop_top=0)
    text(s, 7.5, 1.6, 5.3, 1.6, [[("83% vs 63%", {"bold": True, "color": TREE, "size": 40})],
                                 "median share of the planes' shade · the method wins 6 of 6 streets"], 16, INK)
    text(s, 7.5, 3.35, 5.3, 0.8, [[("Runoff: ", {"bold": True}), ("never worse (6 of 6)", {})]], 15, INK)
    text(s, 7.5, 4.1, 5.3, 2.0, [[("First run: ", {"bold": True, "color": MUTED}),
                                  ("crowns from Barcelona, Mataró LiDAR next. Florence follows with its own LiDAR.", {})]], 14, MUTED)
    source(s, "Ajuntament de Mataró, arbrat (2026); Overture Maps (ODbL); ICGC, LiDAR 2021.")


def n_cost(s):
    head(s, "Cost and feasibility", "The method changes the species, not the number of works")
    rows = [("refresh-ccw", "Replace: up to 500 € per tree", "fell, remove the stump, plant a 16–18 cm tree", HEAT),
            ("move", "Move: 500 to 2,900 € per tree", "tree spade, root ball 90 to 300 cm", WARN),
            ("ruler", "Widen a pit, 1 → 1.5 m²: about 100 €", "demolish paving, new pit border", TREE)]
    for k, (ic, b, t, c) in enumerate(rows):
        y = 1.6 + k * 1.2
        ico(s, ic, c, M + 0.05, y + 0.1, 0.5)
        text(s, M + 0.8, y, 5.4, 1.1, [[(b, {"bold": True, "color": c, "size": 18})], t], 14, INK)
    text(s, M, 5.3, 5.9, 0.9, "Same trees replaced in both cases: same works, same cost.", 16, INK, True)
    text(s, 6.9, 1.55, 5.9, 0.5, "Candidate sidewalk spots in Porta (267)", 18, INK, True)
    for k, (n, t, c) in enumerate((("153", "free", TREE), ("103", "conditional: a field check", WARN), ("11", "blocked", HEAT))):
        y = 2.2 + k * 1.15
        box(s, 6.9, y, 5.9, 1.0, tint(c, 0.12))
        text(s, 7.2, y, 5.4, 1.0, [[(n + "  ", {"bold": True, "color": c, "size": 30}), (t, {})]], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.9, 5.75, 5.9, 0.5, "Underground services: real plans used privately, a synthetic layer in the public tool.", 13, MUTED)
    source(s, "Diputació de Barcelona, Catàleg 2024–2027; CYPE, Generador de precios; " + BCN)


def n_impact(s):
    head(s, "What 10 M€ would change", "A rough scale-up of the back-test, at replacement cost")
    for k, (big, small, c) in enumerate((("≈ 20,000", "replacements at up to 500 € each", HEAT),
                                         ("≈ 15 years", "of the city's replacements with a change of species (~1,300 a year)", RAIN),
                                         ("1.7 ×", "the new summer shade per tree, method vs city (back-test median)", TREE))):
        x = M + k * 4.13
        box(s, x, 1.6, 3.93, 2.6, tint(c, 0.10))
        text(s, x + 0.3, 1.6, 3.4, 2.6, [[(big, {"bold": True, "color": c, "size": 38})], small], 15, INK, anchor=MSO_ANCHOR.MIDDLE)
    box(s, M, 4.5, W - 2 * M, 1.5, tint(TREE, 0.08))
    text(s, M + 0.5, 4.5, W - 2 * M - 1.0, 1.5,
         [[("Same money, same works: ", {"bold": True}),
           ("the gain comes only from choosing the species, with runoff no worse. Felt temperature and growth over time still to be added.", {})]],
         17, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Diputació de Barcelona, Catàleg 2024–2027; Open Data BCN, arbrat viari 2018–2026.")


def n_limits(s):
    head(s, "Limits and assumptions", "What the method takes as given")
    rows = [("tree-deciduous", "New trees at today's size", "each species at its median Barcelona crown (LiDAR); growth not modelled", TREE),
            ("thermometer-sun", "Heat = shade on a hot day", "a fast proxy, checked with Ladybug and Infrared City, not a full simulation per layout", HEAT),
            ("droplets", "One interception rate", "1.75 mm per unit of leaf area; species rates do not change the ranking", RAIN),
            ("cloud-rain", "Runoff barely moves", "differences are below what the model resolves: runoff is a do-no-harm check", RAIN),
            ("map-pin", "Free spots are an upper bound", "no open data on underground services; conditional spots need a field check", WARN),
            ("chart-pie", "15% cap on street trees only", "the city's plan also counts squares", MUTED)]
    for k, (ic, b, t, c) in enumerate(rows):
        x, y = M + (k % 2) * 6.2, 1.6 + (k // 2) * 1.6
        ico(s, ic, c, x + 0.05, y + 0.1, 0.5)
        text(s, x + 0.8, y, 5.2, 1.5, [[(b, {"bold": True, "color": c, "size": 17})], t], 14, INK)
    source(s, "Anys & Weiler 2024; ICGC, LiDAR 2021; Ladybug Tools; Infrared City; " + BCN)


def n_vision(s):
    head(s, "Next steps, further out", "From replacing a tree to planning the whole urban forest")
    rows = [("trees", "Every tree", "not only the replaced ones: all street, park and square trees, kept, moved or added", TREE),
            ("ruler", "Tree pits", "pit size and soil volume: how big each tree can grow and how much water reaches its roots", WARN),
            ("droplets", "Soil type", "infiltration by soil class instead of one value for all of Porta", RAIN),
            ("thermometer-sun", "Evapotranspiration", "cooling from the water trees give back to the air, not only from shade", HEAT)]
    for k, (ic, t, d, c) in enumerate(rows):
        x = M + k * 3.1
        box(s, x, 1.6, 2.9, 4.4, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 1.9, 0.7)
        text(s, x + 0.3, 2.8, 2.4, 3.1, [[(t, {"bold": True, "color": c, "size": 20})], d], 15, INK)
    text(s, M, 6.2, W - 2 * M, 0.5, "Same core, more layers: each one becomes a new input or a new objective for the optimiser.", 16, INK, True)


SLIDES = [
    (n_question, "My question: when a project must replace trees, can a method inside the city's rules choose species and positions so that shade and rain interception improve, or at least do not get worse, against the city's practice and against today? H1: no worse than the city, better in summer, and no more winter shade than today. H2: heat and runoff want different species."),
    (n_heat, "The heat module asks where the sun hits the street each hour, how much of it each crown stops, and counts summer shade as a gain and winter shade as a cost, because evergreen crowns that shade in summer also take the winter sun. I checked it against felt temperature with Ladybug and Infrared City."),
    (n_scenarios, "Every scenario uses the same streets and the same tree positions: only the species change. Today, three versions of the city's choice, the old table, which I cite, and the method."),
    (n_porta, "In Porta, replacing the 832 planes, the city's practice keeps about 99% of today's summer shade; the method gives 107%, and with the city's diversity still 106%. In winter the method casts 99% of today's shade against 109%. Runoff stays the same."),
    (n_cityplan, "The city has a per-tree plan for 513 Porta planes. At the same diversity, the method gives 101% of today's summer shade against the plan's 98%, with more winter sun and equal runoff."),
    (n_backtest, "I went back to 26 places where the city really replaced a group of trees. With the same positions, the method gives more shade in 23 of them, 1.7 times the shade per tree, and never more runoff."),
    (n_effective, "To count diversity I use the effective number of species: how many equally common species a mix is worth. Ten species in equal shares are worth ten; ten species with one at ninety percent are worth fewer than two."),
    (n_diversity,"Diversity is cheap: matching the city's announced mix costs less than half a point of shade, and even at twenty effective species the method stays above the city's practice."),
    (n_mataro, "Does it travel? In Mataró, replacing every plane on six streets, the method keeps 83% of the planes' shade against 63% for the city's practice, and wins all six streets. Florence follows."),
    (n_cost, "The method replaces the same trees as the city, so the works and the cost are the same: up to 500 euros per replaced tree. Of 267 candidate spots in Porta, 153 are free and 103 need a field check."),
    (n_impact, "With 10 million euros the city could replace about 20,000 trees, around fifteen years of its replacements. Chosen with the method, each new tree gives 1.7 times the shade, for the same money."),
    (n_stakeholders,"The user is the designer of a street project, inside the city or in a commissioned firm. Parcs i Jardins sets the rules and approves the species; neighbours see the before and after."),
    (n_contribution, "What the results say: in Porta the gain comes from the species alone; at the city's own diversity the method still gains; it holds in 23 of 26 real replacements and in Mataró; runoff does not move, so it stays a do-no-harm check."),
    (n_limits, "These are the limits: new trees at today's size, heat as shade checked with felt temperature, one interception rate, runoff that barely moves, free spots as an upper bound, and the cap on street trees only."),
    (n_context_maps, "Barcelona replaced almost eleven thousand street trees in eight years, one at a time. The plan caps any species at fifteen percent, but says nothing about where. Porta's canopy is twenty percent, the target thirty."),
    (n_crowns, "Same trunk, different crowns: at the plane's trunk size, the thirty species cast very different shade."),
    (n_barri, "Why Porta: I wrote the rule before ranking. Flood hazard, heat and planes all above the city's sixtieth percentile; Porta comes first."),
    (n_porta_site, "Porta: 84 hectares, 2,825 street trees, 832 of them planes. Its canopy is twenty percent; street trees hold less than half of it, so they alone cannot reach thirty: the choice of species is what is left."),
    (n_species30, "These are the thirty species left after the screening."),
    (n_spots, "Of 267 candidate spots in Porta, 153 are free, 103 need a field check on underground services, and 11 are blocked."),
    (n_practice, "The baseline is not a rule but what the city really planted; the same rules apply to both, and switching a rule off shows what it costs."),
    (n_vision, "Further out, the idea grows: from replaced trees to every tree in the city, with tree pits, soil type and evapotranspiration as new layers of the same core."),
    (n_species30b, "The same thirty species from the side, at one scale, next to a person."),
    (n_obstacles, "The conditional spots: signs, lamps, crossings and bollards a project can move, and underground services that need a field check."),
    (n_water, "Where the water goes in Porta: the flow paths from the terrain and the city's flood hotspots."),
    (n_runoff, "The runoff module: the design storm falls on a one-metre grid; crowns hold water, the soil takes some, the rest flows downhill to the flood spots."),
]


def divider(s, title):
    """Chapter divider: one word on a plain page, so the audience knows where the story is."""
    text(s, M, 2.9, W - 2 * M, 1.2, title, 44, TREE, True, name="Title")


# Narrative order (26 Nov, after Giovanni's review). NEW N1-N22 = SLIDES above; OLD M1-M15 = midterm; OLD B1-B9 = midterm backup.
ORDER = ["OLD M1", "NEW N15", "NEW N16", "NEW N17", "NEW N18",               # why: replacements, crowns, why Porta, Porta
         "§The gap", "OLD M4",
         "§The question", "NEW N1", "OLD M6", "NEW N12",                    # question, what is fixed/free, who decides
         "§The method", "OLD M7", "OLD M8", "OLD B4", "NEW N19", "NEW N23",            # overview, screening, HiGHS, 30 species
         "OLD M9", "NEW N20", "NEW N24",                                               # rules, spots
         "NEW N2", "NEW N26", "OLD M11", "OLD M12", "NEW N25", "OLD B1",               # heat, runoff, bucket, hill, trade-off triangle
         "NEW N3", "NEW N21",                                               # scenarios, city practice
         "§Results", "NEW N4", "NEW N5", "NEW N6", "OLD B8",                # Porta, city plan, back-test, Rio de Janeiro
         "NEW N7", "NEW N8",                                                # diversity explained, its cost
         "OLD B5", "NEW N9",                                                # Mataró: why, result
         "§In practice", "NEW N10", "NEW N11",                              # cost, 10 M€
         "§Conclusions", "NEW N13", "NEW N14", "OLD M15", "NEW N22"]                   # results read, limits, next/thanks
# Removed in the review (26 Nov): replaced by a new slide, or the appendix.
DROPPED = {"OLD M2", "OLD M3", "OLD M10", "OLD M13", "OLD M5", "OLD M14", "OLD B2", "OLD B3", "OLD B6", "OLD B7", "OLD B9"}


def build():
    OUT.mkdir(exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    import make_midterm_pechakucha as MT
    import re
    md = (ROOT / "slides/midterm/script.md").read_text(encoding="utf-8")
    says = re.findall(r'^\*\*Say \(\d+ words\):\*\* "(.+)"$', md, re.M)
    old = [(fn, f"OLD M{k + 1}", n) for k, (fn, n) in enumerate(zip(MT.SLIDES, says))]
    old += [(fn, f"OLD B{k + 1}", n) for k, (fn, n) in enumerate(MT.BACKUP)]
    pool = {f"NEW N{k + 1}": (f, n) for k, (f, n) in enumerate(SLIDES)}
    pool.update({t: (f, n) for f, t, n in old})
    seq = []
    for item in ORDER:
        if item.startswith("§"):
            seq.append((lambda s, t=item[1:]: divider(s, t), "", None))
        else:
            f, n = pool.pop(item)
            seq.append((f, n, item))
    assert set(pool) == DROPPED, set(pool) ^ DROPPED
    for fn, note, tag in seq:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        if tag:
            old_tag(s, tag.replace("NEW ", "").replace("OLD ", "OLD "))
        for shp in s.shapes:
            if shp.name in ("Mono", "Sources"):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = R.MONO
        page_number(s)
        s.notes_slide.notes_text_frame.text = note
    out = OUT / "shade_and_sponge_final_new.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT), f"({len(prs.slides)} slides)")


if __name__ == "__main__":
    build()
