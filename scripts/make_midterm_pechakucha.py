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
    for k, (ic, big, small, c) in enumerate(items):
        x, y = M + (k % 2) * 6.2, 1.6 + (k // 2) * 2.2
        box(s, x, y, 5.9, 1.95, tint(c, 0.10))
        ico(s, ic, c, x + 0.35, y + 0.6, 0.7)
        text(s, x + 1.35, y, 4.4, 1.95, [[(big, {"bold": True, "color": c, "size": 40})], small], 17, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 6.15, W - 2 * M, 0.5, [[("Street trees alone cannot reach 30%: ", {"bold": True}), ("the choice of species is what is left.", {})]], 18, INK)
    source(s, "ICGC, LiDAR 2021; Open Data BCN, arbrat viari; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


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
    fig(s, "sketch_rules", 1.55)                 # hand-drawn plan (ComfyUI on the OMEN, 23 Nov), 3:1
    source(s, BCN)


def s10(s):
    head(s, "Where new trees go", "Porta: most blocked spots are blocked by things a project can move")
    fig(s, "sketch_classes", 1.55)               # hand-drawn plan (ComfyUI on the OMEN, 23 Nov), 3:1
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
    R.s8(s)
    for shp in s.shapes:
        if shp.has_text_frame and shp.text_frame.text.startswith("Next:"):
            shp.text_frame.paragraphs[0].runs[0].text = "And: "
            shp.text_frame.paragraphs[0].runs[1].text = "in 26 of 26 groups, no more water to flood spots than the city's choice"


def s15(s):
    s1_photo(s)
    text(s, 0.75, 1.3, 7.4, 1.0, "Next", 54, BG, True, name="Title")
    text(s, 0.75, 2.5, 7.2, 2.6, ["Felt temperature (UTCI): Ladybug, Infrared City", "Same method in Mataró and Florence",
                                  "Tool: action per tree, trade-offs on screen"], 22, BG)
    text(s, 0.75, 5.1, 7.2, 0.8, "The right tree, in the right place, within the city's rules. Thank you.", 22, BG, True)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Thesis midterm", 16, "#CFC9BC", name="Mono")


def b1_method(s):
    """Backup: the one-page methodology overview (make_midterm_overview.py), full-bleed with its own baked title."""
    picture(s, FIG / "method_overview.png", 0, 0, W, crop_top=0)


def b2_screening(s):
    """Backup: the screening as a matrix — one row per position, groups A/B/C (the question A. Chronis asked, 17 Nov)."""
    picture(s, FIG / "screening_matrix.png", 0, 0, W, crop_top=0)


def b3_highs(s):
    """Backup: what HiGHS does, on a five-position example (make_midterm_highs.py)."""
    picture(s, FIG / "flow_07_highs.png", 0, 0, W, crop_top=0)


SLIDES = [s1, R.s2, s3, R.s3, R.s4, s5, s7, s8, s9, s10, s11, s12, s13, s14, s15]
BACKUP = [(b1_method, "Backup: the full method on one page."),
          (b2_screening, "Backup: the screening indicators as a matrix, one row per position."),
          (b3_highs, "Backup: how HiGHS picks the species, on a five-position example.")]
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
