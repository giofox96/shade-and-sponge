"""Midterm Pecha Kucha for the thesis studio (24 Nov 2026): 15 slides x 20 s = 5 min, built on the RM personal deck
(make_rm_personal.py: same helpers, fonts, palette; slides 1, 2, 4, 5 reused) and the 17 Nov tutor feedback.
Speaker notes = the "Say" lines of slides/midterm/script.md. Figures: make_midterm_figs.py.
Output: slides/midterm/shade_and_sponge_midterm_pechakucha.pptx. Run from scripts/: python make_midterm_pechakucha.py
"""
import re
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches
import make_rm_personal as R
from make_rm_personal import ico, s1_photo, ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, rgb, tint, text, box, head, source, picture

OUT = ROOT / "slides/midterm"
FIG = OUT / "fig"
BCN = "Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; Parcs i Jardins, Gestió de l'arbrat viari (2011)."


def fig(s, name, y=1.5, w=None):
    picture(s, FIG / f"{name}.png", M + 0.1, y, w or W - 2 * M - 0.2, crop_top=0)


def page_number(s, dark=False):
    """Bottom-right slide-number FIELD: PowerPoint keeps it in sync when slides are added, moved or removed (parametric)."""
    tb = s.shapes.add_textbox(Inches(W - 1.1), Inches(H - 0.52), Inches(0.75), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.alignment = 2                                           # right
    run = p.add_run()._r
    fld = run.makeelement(qn("a:fld"), {"id": "{B3E8C2F0-0000-4A2B-9D1A-000000000001}", "type": "slidenum"})
    rpr = fld.makeelement(qn("a:rPr"), {"lang": "en-US", "sz": "1100"})
    fill = rpr.makeelement(qn("a:solidFill"), {})
    clr = fill.makeelement(qn("a:srgbClr"), {"val": ("CFC9BC" if dark else MUTED).lstrip("#")})
    fill.append(clr)
    rpr.append(fill)
    latin = rpr.makeelement(qn("a:latin"), {"typeface": R.MONO})
    rpr.append(latin)
    txt = fld.makeelement(qn("a:t"), {})
    txt.text = "1"
    fld.append(rpr)
    fld.append(txt)
    p._p.append(fld)


def s1(s):
    s1_photo(s)
    text(s, 0.75, 1.5, 7.4, 1.0, "Shade and Sponge", 54, BG, True, name="Title")
    text(s, 0.75, 2.7, 7.0, 3.0, [[("“I am redesigning this street. ", {"bold": True})],
         "Which trees do I keep, move or replace, and where do I add new ones, so the street is cooler in summer "
         "and not worse for flooding, within the city's rules?”"], 22, BG)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Thesis midterm", 16, "#CFC9BC", name="Mono")


def s3(s):
    head(s, "Porta in numbers", "Nou Barris, Barcelona: why the species in each spot matters")
    items = [("map-pin", "84 ha", "neighbourhood · 2,825 street trees", MUTED),
             ("trees", "17 ha", "under tree crowns today (20%)", TREE),
             ("target", "−8 ha", "missing to the city's 30% target", HEAT),
             ("circle-plus", "+0.3 ha", "if every free sidewalk spot is planted", RAIN)]
    # why this neighbourhood (site selection, 8 Oct): all three criteria above the city's 60th percentile, Porta ranks first
    text(s, M, 1.45, W - 2 * M, 0.45, [[("Why Porta? ", {"bold": True}), ("first among Barcelona's neighbourhoods where heat, flood hazard and plane trees are all high", {})]], 17, INK)
    for k, (ic, lab, c) in enumerate((("thermometer-sun", "summer surface: +1.4 °C vs city", HEAT),
                                      ("droplets", "flood hazard: top 20% of the city", RAIN),
                                      ("tree-deciduous", "832 planes, 29% of its street trees", TREE))):
        x = M + k * 4.13
        box(s, x, 1.95, 3.93, 0.55, tint(c, 0.12))
        ico(s, ic, c, x + 0.15, 2.02, 0.4)
        text(s, x + 0.65, 1.95, 3.2, 0.55, lab, 14, c, True, anchor=MSO_ANCHOR.MIDDLE)
    for k, (ic, big, small, c) in enumerate(items):
        x, y = M + (k % 2) * 6.2, 2.75 + (k // 2) * 1.7
        box(s, x, y, 5.9, 1.5, tint(c, 0.10))
        ico(s, ic, c, x + 0.35, y + 0.4, 0.7)
        text(s, x + 1.35, y, 4.4, 1.5, [[(big, {"bold": True, "color": c, "size": 36})], small], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 6.2, W - 2 * M, 0.5, [[("Street trees alone cannot reach 30%: ", {"bold": True}), ("the choice of species is what is left.", {})]], 18, INK)
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; "
              "Barcelona Resilience Atlas; Landsat 8/9.")


def s5(s):
    R.s5(s)
    for shp in s.shapes:                       # fixed list after the 18 Nov decisions: only traffic lights and driveways block
        if shp.has_text_frame and shp.text_frame.text.startswith("Street layout"):
            ps = shp.text_frame.paragraphs
            ps[-1].runs[0].text = "Traffic lights, driveways"


def s7(s):
    head(s, "Method", "Screen, let the designer decide, optimise the species, compare")
    fig(s, "method_actions", 1.45)
    source(s, "Open Data BCN, arbrat viari; ICGC, LiDAR 2021; Huangfu & Hall 2018 (HiGHS); Ladybug Tools; Infrared City.")


def s8(s):
    head(s, "Screening", "Three questions for every tree and free spot, computed once")
    cols = [(TREE, "tree-deciduous", "What stands there", ["species, trunk class", "crown size, leaf density", "condition hint: weak crown"]),
            (WARN, "ruler", "Where it is", ["sidewalk width → size", "lamps, signs, crossings", "rain flows to a flood spot?"]),
            (HEAT, "sun", "What 30 species would do", ["summer shade  +", "winter shade  −", "rain held  +"])]
    for k, (c, ic, t, rows) in enumerate(cols):
        x = M + k * 4.18
        box(s, x, 1.55, 3.95, 4.6, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 1.8, 0.6)
        text(s, x + 0.3, 2.5, 3.5, 0.6, t, 19, c, True)
        text(s, x + 0.3, 3.2, 3.5, 2.8, rows, 17, INK)
    source(s, "Open Data BCN, arbrat viari; ICGC, LiDAR 2021; Ajuntament de Barcelona, Mapa topogràfic 1:1000; Barcelona Resilience Atlas.")


def s9(s):
    head(s, "City rules", "Sidewalk width sets the tree size and spacing; no species above 15%")
    fig(s, "rules_sketch", 1.45, 11.3)
    source(s, BCN)


def s10(s):
    head(s, "Where new trees go", "Porta: most blocked spots are blocked by things a project can move")
    fig(s, "spots", 1.7)
    source(s, BCN + " Open Data BCN, street furniture; OpenStreetMap.")


def s11(s):
    head(s, "A crown is a bucket", "Same tree, same water held, wherever it stands")
    fig(s, "bucket", 1.6)
    source(s, "Anys & Weiler 2024 (interception); Barcelona, PDISBA design storms; ICGC, LiDAR 2021.")


def s12(s):
    head(s, "The tree on the hill", "Position decides whether the water held would have reached a flood spot")
    fig(s, "hill", 1.5)
    source(s, "ICGC, LiDAR 2021 (terrain); Barcelona Resilience Atlas (flood hotspots); PDISBA design storm.")


def s13(s):
    head(s, "City practice, not a rule", "The baseline is what the city really planted")
    box(s, M, 1.6, W - 2 * M, 2.0, tint(HEAT, 0.10))
    text(s, M + 0.5, 1.6, W - 2 * M - 1.0, 2.0, [[("1 in 5 ", {"bold": True, "color": HEAT, "size": 44}),
         ("new city plantings is larger than its sidewalk allows", {"size": 22})]], 18, INK, anchor=MSO_ANCHOR.MIDDLE)
    items = [("landmark", "City practice", "the species the city planted, 2018–2026", RAIN),
             ("scale", "Same rules for both", "sidewalk size, 15% cap", WARN),
             ("sliders-horizontal", "What each rule costs", "switch a rule off, re-optimise", TREE)]
    for k, (ic, b, t, c) in enumerate(items):
        x = M + k * 4.18
        box(s, x, 3.95, 3.9, 2.2, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 4.2, 0.55)
        text(s, x + 0.3, 4.9, 3.4, 1.2, [[(b, {"bold": True, "color": c, "size": 20})], t], 15, INK)
    source(s, "Open Data BCN, arbrat viari 2018–2026; Parcs i Jardins, Gestió de l'arbrat viari (2011).")


def s14(s):
    """Back-test (26 real replacement groups) on top; co-benefits of the Porta layouts below (cobenefits_porta*.csv, PR #163):
    balanced layout S4_s0.25_w0.25_r0.50, today S0 = 100, replacements at equal trunk class (TERCERA), reported not optimised."""
    head(s, "First evidence: back-test and co-benefits", "26 groups where the city replaced trees: same positions, city's choice vs method")
    box(s, M, 1.55, W - 2 * M, 2.2, tint(TREE, 0.08))
    for x, ic, big, small in ((M, "tree-deciduous", "59 → 139", "m²·h summer shade per tree (median), city vs method"),
                              (M + 6.1, "circle-check", "22 of 26", "groups where the method gives more shade")):
        ico(s, ic, TREE, x + 0.5, 2.25, 0.8)
        text(s, x + 1.5, 1.55, 4.6, 2.2, [[(big, {"bold": True, "color": TREE, "size": 40})], small], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 3.9, W - 2 * M, 0.45, [[("And: ", {"bold": True}), ("in 26 of 26 groups, no more water to flood spots than the city's choice", {})]], 17, INK)
    text(s, M, 4.55, W - 2 * M, 0.4, [[("Co-benefits in Porta ", {"bold": True}), ("· reported, not optimised · today = 100", {"color": MUTED})]], 16, INK)
    for k, (ic, big, small, c) in enumerate((
            ("trees", "56 vs 42", "carbon stored once grown, method vs city practice", TREE),
            ("heart", "< 100", "pollen load in every replacement: today's planes are highly allergenic", HEAT),
            ("chart-pie", "−0.3 pts", "summer shade to lift diversity from 6.2 to 9.4 species (city practice 15.6)", RAIN))):
        x = M + k * 4.13
        box(s, x, 5.0, 3.93, 1.6, tint(c, 0.10))
        ico(s, ic, c, x + 0.25, 5.5, 0.6)
        text(s, x + 1.0, 5.0, 2.85, 1.6, [[(big, {"bold": True, "color": c, "size": 26})], small], 12, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Open Data BCN, arbrat viari 2018–2026; ICGC LiDAR 2021; Jucker et al. 2017 (carbon); "
              "Cariñanos et al. 2014 (pollen); Nicol et al. 2026 (diversity).")


def s15(s):
    s1_photo(s)
    text(s, 0.75, 1.3, 7.4, 1.0, "Next", 54, BG, True, name="Title")
    text(s, 0.75, 2.5, 7.2, 2.6, ["Felt temperature (UTCI): Ladybug, Infrared City", "Mataró: 83% vs 63% summer shade, 6 of 6 streets", "Florence next",
                                  "Tool: action per tree, trade-offs on screen"], 22, BG)
    text(s, 0.75, 5.1, 7.2, 0.8, "The right tree, in the right place, within the city's rules. Thank you.", 22, BG, True)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Thesis midterm", 16, "#CFC9BC", name="Mono")


def b1_method(s):
    """Backup: the one-page methodology overview (make_midterm_overview.py), full-bleed with its own baked title."""
    picture(s, FIG / "method_overview.png", 0, 0, W, crop_top=0)


def b2_screening(s):
    """Backup: the screening as a matrix — one row per position, groups A/B/C (the question A. Chronis asked, 17 Nov)."""
    picture(s, FIG / "screening_matrix.png", 0, 0, W, crop_top=0)


def b4_mataro_why(s):
    """Backup: why Mataró is the transfer city (notes/catalan_transfer_city.md §3b, §5b, §6) and where it is."""
    head(s, "Why Mataró", "The transfer test: does the method work in a city with other data and other practice?")
    rows = [("database", "Full tree inventory", "species and position for every tree (city, Nov 2026)", TREE),
            ("scan-search", "Same LiDAR as Porta", "ICGC, leaf-on summer flight, same coordinate system", WARN),
            ("cloud-rain", "Its own design storm", "the only finalist city with one (PDCLAM)", RAIN),
            ("droplets", "Pluvial flood risk", "one of ACA's 44 Catalan municipalities", RAIN),
            ("trees", "Same climate, other practice", "Mediterranean coast, planes too, different planting choices", HEAT)]
    for k, (ic, b, t, c) in enumerate(rows):
        y = 1.6 + k * 1.0
        ico(s, ic, c, M + 0.1, y + 0.12, 0.5)
        text(s, M + 0.85, y, 5.6, 0.95, [[(b, {"bold": True, "color": c, "size": 18})], t], 14, INK)
    picture(s, FIG / "mataro_locator.png", 7.0, 1.5, 5.8, crop_top=0)
    source(s, "Ajuntament de Mataró, arbrat (2026) and PDCLAM (2003); ICGC, LiDAR 2021; ACA, PGRI 3rd cycle (2026); "
              "land mask: GLOBE via global-land-mask.")


def b5_mataro_streets(s):
    """Backup: the six test streets and their result (databases/mataro/transfer_test.csv, PR #150)."""
    head(s, "Mataró: six plane streets, every plane replaced", "Summer shade of the new trees, % of planes of the same size: method vs city practice")
    picture(s, FIG / "mataro_streets.png", M, 1.45, 6.6, crop_top=0)
    text(s, 7.5, 1.6, 5.3, 1.6, [[("83% vs 63%", {"bold": True, "color": TREE, "size": 40})],
                                 "median, method vs city practice · the method wins 6 of 6 streets"], 16, INK)
    text(s, 7.5, 3.35, 5.3, 1.0, [[("Runoff: ", {"bold": True}), ("never worse than any practice (6 of 6)", {})]], 15, INK)
    text(s, 7.5, 4.05, 5.3, 2.6, [[("Approximate, first run:", {"bold": True, "color": MUTED})],
                                  "crowns = Barcelona medians per species (Mataró LiDAR next)",
                                  "buildings = Overture Maps; flat ground",
                                  "no hotspot map: runoff on all open ground",
                                  "València (narrow) is the weak case: 42% vs 35%"], 13, MUTED)
    source(s, "Ajuntament de Mataró, arbrat (2026); Overture Maps (ODbL); ICGC, LiDAR 2021 (Barcelona crowns).")


def b6_assumptions(s):
    """Backup: the declared assumptions (A. Chronis, 10 Nov: declare them, soften the bold ones; notes/tutor_feedback_10nov.md §2)."""
    head(s, "Declared assumptions", "What the method takes as given, and why it is acceptable for now")
    rows = [("tree-deciduous", "New trees at the size of today's trees", "each species at the crown it has in Porta today (LiDAR median): "
             "growth and life cycle are not modelled; a ≈10-year view is in the tool", TREE),
            ("thermometer-sun", "Heat = summer shade, not felt temperature", "a shade proxy on a hot day; UTCI with Ladybug and Infrared City is next", HEAT),
            ("droplets", "One interception rate for every species", "1.75 mm per unit of leaf area; species-specific rates "
             "do not change the ranking", RAIN),
            ("map-pin", "Free spots are an upper bound", "no open data on underground services; replacements reuse the existing pit, "
             "conditional spots need a field check", WARN),
            ("chart-pie", "15% cap on street trees only", "the plan counts squares too; to revisit before the final results", TREE),
            ("move", "A moved tree leaves the site", "its position is freed or replanted; where it lands is outside the tool", MUTED)]
    for k, (ic, b, t, c) in enumerate(rows):
        x, y = M + (k % 2) * 6.2, 1.6 + (k // 2) * 1.75
        ico(s, ic, c, x + 0.05, y + 0.1, 0.5)
        text(s, x + 0.8, y, 5.2, 1.6, [[(b, {"bold": True, "color": c, "size": 17})], t], 13, INK)
    source(s, "Anys & Weiler 2024; Xiao & McPherson 2016; ICGC, LiDAR 2021; "
              "Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


def b7_tradeoff(s):
    """Backup: the tool's priority triangle and trade-off chart, screenshots of https://giofox96.github.io/shade-and-sponge/
    (Barcelona 30-species palette, balanced layout); the live demo follows the talk."""
    head(s, "In the tool: priorities and trade-offs", "Pick a point on the triangle, the optimiser re-solves; every layout is a dot on the chart")
    text(s, M, 1.6, 5.2, 0.4, "Priorities: click to re-optimise", 16, INK, True)
    picture(s, FIG / "tool_triangle.png", M + 0.6, 2.05, 4.0, crop_top=0)
    text(s, M, 5.7, 5.6, 1.0, ["Each corner is one objective: summer shade, winter sun, runoff.",
                                      "Dots = precomputed layouts; any other point is solved in the browser."], 14, MUTED)
    text(s, 6.9, 1.6, 5.9, 0.4, "Trade-off: summer shade vs winter shade", 16, INK, True)
    picture(s, FIG / "tool_tradeoff.png", 7.7, 1.95, 4.1, crop_top=0)
    source(s, "Huangfu & Hall 2018 (HiGHS).")


def b3_highs(s):
    """Backup: what HiGHS does, on a five-position example (make_midterm_highs.py)."""
    picture(s, FIG / "flow_07_highs.png", 0, 0, W, crop_top=0)


SLIDES = [s1, R.s2, s3, R.s3, R.s4, s5, b1_method, s8, s9, s10, s11, s12, s13, s14, s15]
BACKUP = [(b7_tradeoff, "Backup: the tool's priority triangle and trade-off chart; the live demo follows."),
          (s7, "Backup: the method in four steps (the simple version)."),
          (b2_screening, "Backup: the screening indicators as a matrix, one row per position."),
          (b3_highs, "Backup: how HiGHS picks the species, on a five-position example."),
          (b4_mataro_why, "Backup: why Mataró is the transfer city, and where it is."),
          (b5_mataro_streets, "Backup: the six Mataró test streets and their result."),
          (b6_assumptions, "Backup: the declared assumptions.")]
DARK = {s1, s15}                                             # photo-background slides: a light page number


def build():
    md = (OUT / "script.md").read_text(encoding="utf-8")
    notes = re.findall(r'^\*\*Say \(\d+ words\):\*\* "(.+)"$', md, re.M)
    assert len(notes) == len(SLIDES), len(notes)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for fn, n in list(zip(SLIDES, notes)) + BACKUP:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        for shp in s.shapes:
            if shp.name in ("Mono", "Sources"):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = R.MONO
        page_number(s, dark=fn in DARK)
        s.notes_slide.notes_text_frame.text = n
    out = OUT / "shade_and_sponge_midterm_pechakucha.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT), f"({len(SLIDES) + len(BACKUP)} slides)")


if __name__ == "__main__":
    build()
