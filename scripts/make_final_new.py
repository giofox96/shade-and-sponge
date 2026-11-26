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


def rhino(s, x, y, w, h, what):
    """Dashed placeholder for a Rhino render."""
    b = box(s, x, y, w, h, tint(GREY, 0.12), line=GREY, name="RHINO placeholder")
    b.line.dash_style = 4
    text(s, x + 0.3, y, w - 0.6, h, [[("RHINO  ", {"bold": True, "color": MUTED}), (what, {"color": MUTED})]], 14, MUTED,
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


def n_question(s):
    head(s, "Research question", "Two references: the city's practice first, then today")
    box(s, M, 1.55, W - 2 * M, 1.55, tint(TREE, 0.10))
    text(s, M + 0.4, 1.55, W - 2 * M - 0.8, 1.55,
         [[("When a street project in Barcelona must replace trees, ", {"bold": True}),
           ("can a trait-based method, inside the city's tree rules, choose the new species and positions so that "
            "summer cooling and rain interception improve, or at least do not get worse, compared with the city's practice and with today?", {})]],
         18, INK, anchor=MSO_ANCHOR.MIDDLE)
    for k, (tag, t, c) in enumerate((("H1", "No worse than the city's practice on heat or runoff, and better on summer shade", HEAT),
                                     ("H2", "The heat-best and the runoff-best layouts use different species", RAIN))):
        x = M + k * 6.2
        box(s, x, 3.35, 5.9, 1.4, tint(c, 0.12))
        text(s, x + 0.3, 3.35, 5.4, 1.4, [[(tag + "  ", {"bold": True, "color": c, "size": 30}), (t, {})]], 17, INK, anchor=MSO_ANCHOR.MIDDLE)
    sq = [("SQ1", "Heat: felt temperature, 12–17 h on a hot day", HEAT), ("SQ2", "Runoff: 2-year, 60-min storm, total and at flood spots", RAIN),
          ("SQ3", "Trade-off: do heat and runoff want different species?", WARN), ("SQ4", "How much of the canopy gap can new trees close?", TREE)]
    for k, (tag, t, c) in enumerate(sq):
        x = M + k * 3.1
        text(s, x, 5.0, 2.9, 1.3, [[(tag, {"bold": True, "color": c, "size": 18})], t], 14, INK)
    text(s, M, 6.35, W - 2 * M, 0.4, "Boundary: extreme storms on saturated soil are outside what street trees can change.", 14, MUTED)


def n_heat(s):
    head(s, "Heat module", "Shade where and when people walk, summer as benefit, winter as cost")
    steps = [("sun", "Sun on the street", "every hour of a hot day and of winter, from buildings and terrain", WARN),
             ("tree-deciduous", "Crown shadow", "each crown from LiDAR casts an elliptical shadow; leaf density sets how much light passes", TREE),
             ("thermometer-sun", "Summer + / winter −", "shade counts as gain in summer and as cost in winter, by the species' leaf-on months", HEAT)]
    for k, (ic, t, d, c) in enumerate(steps):
        x = M + k * 4.18
        box(s, x, 1.6, 3.95, 2.9, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 1.85, 0.6)
        text(s, x + 0.3, 2.6, 3.4, 1.8, [[(t, {"bold": True, "color": c, "size": 20})], d], 15, INK)
    box(s, M, 4.75, W - 2 * M, 1.5, tint(RAIN, 0.08))
    ico(s, "circle-check", TREE, M + 0.35, 5.15, 0.6)
    text(s, M + 1.2, 4.75, W - 2 * M - 1.5, 1.5,
         [[("Checked against felt temperature (UTCI): ", {"bold": True}),
           ("Ladybug on all of Porta and Infrared City on one street. Fast enough to compare thousands of layouts; "
            "the full simulation is used to check, not to choose.", {})]], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "ICGC, LiDAR 2021; Ladybug Tools; Infrared City; Bröde et al. 2012 (UTCI).")


def n_scenarios(s):
    head(s, "Scenarios", "Same streets, same tree positions, different choice of species")
    rows = [("S0", "Today", "the trees as they stand", "LiDAR 2021", INK),
            ("S1a", "City, announced", "the 2026 replacement mix the city announced", "press, 2026", RAIN),
            ("S1b", "City, practice", "what the city really planted where it removed a tree, 2018–2026", "tree inventory", RAIN),
            ("S1c", "City, plan", "the species the city has planned for each Porta tree", "Parcs i Jardins", RAIN),
            ("S1-2004", "City, old table", "district × sidewalk table of 2004/05 (cited, not run)", "Parcs i Jardins", MUTED),
            ("Method", "This thesis", "species chosen by the optimiser, inside the same rules", "HiGHS", TREE)]
    for k, (tag, name, what, src, c) in enumerate(rows):
        y = 1.55 + k * 0.8
        box(s, M, y, W - 2 * M, 0.68, tint(c, 0.10 if k % 2 == 0 else 0.05))
        text(s, M + 0.25, y, 1.5, 0.68, tag, 18, c, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 1.9, y, 2.6, 0.68, name, 16, INK, True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 4.6, y, 5.6, 0.68, what, 15, INK, anchor=MSO_ANCHOR.MIDDLE)
        text(s, M + 10.3, y, 1.9, 0.68, src, 13, MUTED, anchor=MSO_ANCHOR.MIDDLE)
    source(s, BCN + " Open Data BCN, arbrat viari 2018–2026; Huangfu & Hall 2018 (HiGHS).")


def n_porta(s):
    head(s, "Result: Porta", "Replacing the 832 planes: summer shade as a share of today's")
    bars(s, M, 1.5, 6.4, 4.6, ["Today (S0)", "City, announced (S1a)", "City, practice (S1b)", "Method", "Method, diversity ≥ 9.4"],
         [100.0, 100.3, 98.9, 106.7, 106.3], [GREY, RAIN, RAIN, TREE, TREE])
    rhino(s, 7.3, 1.55, W - M - 7.3, 3.2, "Porta map: streets coloured by summer shade gain, method vs city practice")
    text(s, 7.3, 5.0, W - M - 7.3, 1.3,
         [[("Winter: ", {"bold": True}), ("method 99% of today's shade, city practice 109%: more winter sun.", {})],
          [("Runoff: ", {"bold": True}), ("equal (differences below what the model resolves).", {})]], 15, INK)
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari; " + BCN)


def n_cityplan(s):
    head(s, "The city's own plan", "513 Porta planes the city plans to change: its species vs the method's, at the same diversity")
    bars(s, M, 1.5, 7.0, 3.6, ["Today (S0)", "City plan (S1c)", "Method, same diversity (9.7)"],
         [100.0, 98.2, 101.4], [GREY, RAIN, TREE], axis_min=90, axis_max=104)
    for k, (big, small, c) in enumerate((("+3.2 pts", "summer shade, method vs city plan", TREE),
                                         ("98% vs 104%", "winter shade, method vs city plan", RAIN),
                                         ("=", "runoff, both", MUTED))):
        y = 1.55 + k * 1.2
        box(s, 8.1, y, W - M - 8.1, 1.05, tint(c, 0.10))
        text(s, 8.35, y, W - M - 8.6, 1.05, [[(big + "  ", {"bold": True, "color": c, "size": 24}), (small, {})]], 14, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 5.45, W - 2 * M, 0.8, [[("The city's plan keeps the shade close to today. ", {"bold": True}),
                                        ("The method, with the same number of species, turns the loss into a small gain and gives back winter sun.", {})]], 17, INK)
    source(s, "Parcs i Jardins, planned species for Porta (2026); ICGC, LiDAR 2021; " + BCN)


def n_backtest(s):
    head(s, "Back-test: what the city really did", "26 groups of trees the city replaced, 2018–2026: its species vs the method's, same positions")
    box(s, M, 1.55, 5.9, 2.1, tint(TREE, 0.10))
    text(s, M + 0.4, 1.55, 5.2, 2.1, [[("23 of 26", {"bold": True, "color": TREE, "size": 44})], "groups where the method gives more summer shade"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    box(s, M, 3.85, 5.9, 2.1, tint(HEAT, 0.10))
    text(s, M + 0.4, 3.85, 5.2, 2.1, [[("1.7 ×", {"bold": True, "color": HEAT, "size": 44})], "the summer shade per tree (median), method vs city"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    rhino(s, 6.75, 1.55, W - M - 6.75, 4.4, "one or two replaced groups, before / city / method, crowns in 3D on the street")
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
    head(s, "What this brings", "From 18 tools reviewed to none that does all of it")
    for k, (n, t) in enumerate((("18", "tools reviewed"), ("7", "treat heat and runoff together"),
                                ("1", "also chooses species"), ("0", "per tree, inside a city's rules"))):
        x = M + k * 3.1
        box(s, x, 1.6, 2.9, 2.2, tint(TREE, 0.06 + 0.05 * k))
        text(s, x + 0.25, 1.6, 2.4, 2.2, [[(n, {"bold": True, "color": TREE, "size": 44})], t], 15, INK, anchor=MSO_ANCHOR.MIDDLE)
    box(s, M, 4.15, W - 2 * M, 1.9, tint(HEAT, 0.08))
    text(s, M + 0.5, 4.15, W - 2 * M - 1.0, 1.9,
         [[("A method that picks the species and position of every replaced street tree, for shade and rain together, inside the city's own rules, ",
            {"bold": True}),
           ("and tests it against what the city really planted.", {})]], 19, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Dong et al. 2026; Mannucci et al. 2025; Nicol et al. 2026 (SylvCiT); full list in the thesis.")


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


SLIDES = [
    (n_question, "My question: when a project must replace trees, can a method inside the city's rules choose species and positions so that shade and rain interception improve, or at least do not get worse, against the city's practice and against today? H1: no worse than the city, better in summer. H2: heat and runoff want different species."),
    (n_heat, "The heat module asks where the sun hits the street each hour, how much of it each crown stops, and counts summer shade as a gain and winter shade as a cost. I checked it against felt temperature with Ladybug and Infrared City."),
    (n_scenarios, "Every scenario uses the same streets and the same tree positions: only the species change. Today, three versions of the city's choice, the old table, which I cite, and the method."),
    (n_porta, "In Porta, replacing the 832 planes, the city's practice keeps about 99% of today's summer shade; the method gives 107%, and with the city's diversity still 106%. In winter the method lets more sun through. Runoff stays the same."),
    (n_cityplan, "The city has a per-tree plan for 513 Porta planes. At the same diversity, the method gives 101% of today's summer shade against the plan's 98%, with more winter sun and equal runoff."),
    (n_backtest, "I went back to 26 places where the city really replaced a group of trees. With the same positions, the method gives more shade in 23 of them, 1.7 times the shade per tree, and never more runoff."),
    (n_diversity, "Diversity is cheap: matching the city's announced mix costs less than half a point of shade, and even at twenty effective species the method stays above the city's practice."),
    (n_mataro, "Does it travel? In Mataró, replacing every plane on six streets, the method keeps 83% of the planes' shade against 63% for the city's practice, and wins all six streets. Florence follows."),
    (n_cost, "The method replaces the same trees as the city, so the works and the cost are the same: up to 500 euros per replaced tree. Of 267 candidate spots in Porta, 153 are free and 103 need a field check."),
    (n_impact, "With 10 million euros the city could replace about 20,000 trees, around fifteen years of its replacements. Chosen with the method, each new tree gives 1.7 times the shade, for the same money."),
    (n_stakeholders,"The user is the designer of a street project, inside the city or in a commissioned firm. Parcs i Jardins sets the rules and approves the species; neighbours see the before and after."),
    (n_contribution, "Of the eighteen tools I reviewed, none chooses species and positions for heat and runoff inside a city's rules. That is what this method adds, tested against what the city really planted."),
    (n_limits, "These are the limits: new trees at today's size, heat as shade checked with felt temperature, one interception rate, runoff that barely moves, free spots as an upper bound, and the cap on street trees only."),
]


def build():
    OUT.mkdir(exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for fn, note in SLIDES:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        for shp in s.shapes:
            if shp.name in ("Mono", "Sources"):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = R.MONO
        page_number(s)
        s.notes_slide.notes_text_frame.text = note
    out = OUT / "shade_and_sponge_final_new.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT), f"({len(SLIDES)} slides)")


if __name__ == "__main__":
    build()
