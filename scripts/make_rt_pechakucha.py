"""RT Pecha Kucha (15 x 20 s) in the style of the 10 Nov deck: same font, palette and helpers as make_deck_editable.py.
Text, cards and tables are native; the diagrams (crowns, method flow, city map) are the same PNGs as the 10 Nov deck.
Speaker notes = the "Say" lines of slides/rt_pechakucha/pitch_script.md.
Output: slides/rt_pechakucha/shade_and_sponge_pechakucha.pptx. Run from scripts/: python make_rt_pechakucha.py
"""
import io
import re
from PIL import Image
from pptx import Presentation
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
import make_deck_editable as mde
from make_deck_editable import (ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, WHITE,
                                rgb, tint, text, box, card, head, source, picture, s02_context)

OUT = ROOT / "slides/rt_pechakucha"
# the deck's two fonts (same as the figures and the web app); both are Google Fonts, so Google Slides keeps them
FONT, MONO = "IBM Plex Sans", "IBM Plex Mono"
mde.FONT = FONT   # the shared helpers read this global at call time


def s01(s):
    im = Image.open(ROOT / "slides/fig/01_title_photo.webp").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    buf.seek(0)
    p = s.shapes.add_picture(buf, 0, 0, width=Inches(W))
    ratio = im.size[1] / im.size[0] * W / H
    if ratio > 1:
        p.crop_top = p.crop_bottom = (1 - 1 / ratio) / 2
    p.height = Inches(H)
    scrim = box(s, 0, 0, W, H, "#000000", radius=0, name="Scrim")
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
    text(s, 0.75, 2.2, 7.4, 1.0, "Shade and Sponge", 54, BG, True, name="Title")
    text(s, 0.75, 3.35, 7.0, 1.4, "When a project must cut street trees, what is the best way to replace them? "
         "First case: Barcelona's plane trees, in Porta.", 22, BG)
    text(s, 0.75, 5.15, 11.0, 0.4, "MaCAD, IAAC  ·  Research & Technologies, Pecha Kucha, 11 November 2026", 16, "#CFC9BC")


def s03(s):
    head(s, "The problem", "Thousands of small decisions, unmeasured")
    box(s, M, 1.7, W - 2 * M, 3.2, tint(INK, 0.06))
    text(s, M + 0.5, 1.7, W - 2 * M - 1.0, 3.2, [[("When a project must replace street trees, the only rule for the new "
         "species is qualitative.", {"bold": True})], [("Nobody measures whether the street ends up hotter or wetter.",
                                                          {"bold": True, "color": HEAT})]], 28, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Parcs i Jardins, Arbrat viari: selecció d'espècies (rev. 2004); Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


def s04(s):
    head(s, "Same rules, very different crowns", "Crown area as a share of a plane's, same trunk size, Porta's own trees")
    picture(s, ROOT / "slides/fig_v8/v8_crowns.png", M + 0.9, 1.4, W - 2 * M - 1.8, crop_top=0.17, crop_bottom=0.2)
    box(s, M, 5.9, W - 2 * M, 0.7, tint(HEAT, 0.12))
    text(s, M + 0.3, 5.9, W - 2 * M - 0.6, 0.7, "Of 18 tools that place or assess urban trees, none chooses species tree by "
         "tree inside a city's rules.", 18, HEAT, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, arbrat viari; Mannucci et al. 2025; Nicol et al. 2026; "
           "Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026.")


def s05(s):
    head(s, "The research question")
    box(s, M, 1.5, W - 2 * M, 4.2, tint(INK, 0.06))
    text(s, M + 0.6, 1.5, W - 2 * M - 1.2, 4.2, "When a project must replace street trees, can a trait-based method, inside "
         "the city's rules, choose the new species and positions so that cooling and storm-water interception improve, or at "
         "least do not get worse, compared with the city's own practice?", 28, INK, True, anchor=MSO_ANCHOR.MIDDLE)


def s06(s):
    head(s, "Shade and Sponge: how it works", "Open data in, a species and a position for every tree out")
    picture(s, ROOT / "slides/fig_v7/flow_00_overview.png", M + 0.15, 1.35, W - 2 * M - 0.3, crop_top=0.17, crop_bottom=0.075)


def s07(s):
    head(s, "A tool for designers", "Pick an area, set priorities, compare today, the city's rule and the optimised layout")
    picture(s, ROOT / "slides/rt_pechakucha/webapp_porta.jpg", 1.9, 1.45, W - 3.8, crop_top=0)
    text(s, M, H - 0.5, W - 2 * M, 0.3, "giofox96.github.io/shade-and-sponge  ·  open source", 12, MUTED, name="Mono")


def three(s, items, y=1.7, h=3.6, big=24, small=17):
    """Three cards; title and body in one text box, so a two-line title pushes the body down instead of overlapping it."""
    for k, (b, t, c) in enumerate(items):
        x = M + k * 4.18
        box(s, x, y, 3.9, h, tint(c, 0.10))
        text(s, x + 0.3, y + 0.25, 3.3, h - 0.5, [[(b, {"bold": True, "color": c, "size": big})], t], small, INK)


def s08(s):
    head(s, "Innovation", "The city's rules are inside the tool, not checked afterwards")
    three(s, [("Two services, one choice", "Species and position for every tree, scored on summer shade / UTCI and runoff together.", TREE),
              ("Rules inside, not after", "15% species cap, sidewalk width → tree size, the city's own species list.", WARN),
              ("Real baseline, any tree", "Compared with what the city actually plants (its inventory, 2018–2026). Any tree a "
               "project replaces; one data adapter per city.", RAIN)])


def s09(s):
    head(s, "First evidence", "28 barris, one layout under the city's 15% cap, against the city's announced mix")
    picture(s, ROOT / "slides/fig_v7/res_04_city_map.png", M + 0.4, 1.4, 4.8, crop_top=0.17, crop_bottom=0.075,
            crop_left=0.02, crop_right=0.6)
    text(s, M + 0.4, 6.55, 5.5, 0.3, "Green = gain over the city's mix · ochre = loss · grey = not computed", 11, MUTED)
    for k, (b, t, c) in enumerate([("+9.2 pts", "median summer-shade gain over the city's announced mix", TREE),
                                   ("27 of 28", "barris gain; against what the city actually plants, none of 33 loses", TREE),
                                   ("≤ 0.2 °C", "change in pedestrian heat (UTCI) vs today's planes, Ladybug / Honeybee", HEAT)]):
        text(s, 6.6, 1.6 + k * 1.6, 6.2, 1.5, [[(b, {"size": 34, "bold": True, "color": c})], t], 15, INK)
    source(s, "Outlines: Open Data BCN (CC BY 4.0). Cap: Pla director de l'arbrat 2017–2037. City mix: Betevé, 7 May 2026. "
           "Ladybug Tools. Heat on the map = shade proxy.")


def s10(s):
    head(s, "Limits, said upfront")
    items = [("Simulated, not measured", "no field data yet", MUTED),
             ("Heat gain is small", "its sign depends on how porous the crowns are", HEAT),
             ("Runoff is a check", "differences stay below what the model can resolve", RAIN),
             ("Benefits take time", "they arrive only when the new trees mature", TREE)]
    for k, (b, t, c) in enumerate(items):
        y = 1.5 + k * 1.25
        box(s, M, y, W - 2 * M, 1.05, tint(c, 0.10))
        text(s, M + 0.35, y, W - 2 * M - 0.7, 1.05, [[(b + "  ", {"bold": True, "color": c, "size": 22}), (t, {})]], 19, INK,
             anchor=MSO_ANCHOR.MIDDLE)


def s11(s):
    head(s, "Actors")
    items = [("Decide", "Parcs i Jardins, Ajuntament de Barcelona (tree master plan, 15% cap)", TREE),
             ("Use", "Landscape architects, computational designers, urban planners", WARN),
             ("Data & testing", "ICGC (LiDAR) · BCASA (drainage) · Ladybug / Honeybee · Infrared City (in contact) · "
              "Comune di Firenze (LiDAR, transfer)", RAIN),
             ("Benefit", "Residents and pedestrians in streets that are both hot and flood-prone", HEAT)]
    for k, (b, t, c) in enumerate(items):
        x, y = M + (k % 2) * 6.33, 1.5 + (k // 2) * 2.6
        box(s, x, y, 5.9, 2.3, tint(c, 0.10))
        text(s, x + 0.3, y + 0.25, 5.3, 1.9, [[(b, {"bold": True, "color": c, "size": 24})], t], 18, INK)


def table(s, rows, x, y, w, h, col_w, color, size=17):
    tb = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(h)).table
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = tb.cell(i, j)
            cell.text = v
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(color if i == 0 else tint(color, 0.08 if i % 2 else 0.16))
            f = cell.text_frame.paragraphs[0].runs[0].font
            f.name, f.size, f.bold = FONT, Pt(size), i == 0 or j == 0
            f.color.rgb = rgb(WHITE if i == 0 else INK)
    for j, cw in enumerate(col_w):
        tb.columns[j].width = Inches(cw)
    return tb


def s12(s):
    head(s, "Exploitation", "What, how, for whom")
    table(s, [("What", "How", "For whom"),
              ("Method: trait-based layout under city rules", "Thesis, paper", "Researchers, city technicians"),
              ("Python core + web app", "Open source (MIT), online", "Designers, other cities"),
              ("Per-tree crown and trait dataset", "Open data (own data only)", "City, researchers"),
              ("Transfer guide", "Florence / Mataró test", "Cities replacing a monoculture")],
          M, 1.6, W - 2 * M, 4.2, (4.9, 3.6, 3.73), TREE, 18)


def s13(s):
    head(s, "Impact over time")
    three(s, [("Short term · now", "Open, reproducible method · simulated gains in 28 barris · checked in Ladybug / Honeybee", WARN),
              ("Medium term · 1–3 yrs", "Pilot streets with Parcs i Jardins · transfer test: Florence, Mataró", RAIN),
              ("Long term · 2037", "Canopy toward 30%, no species above 15% · no more runoff where streets flood · a method "
               "for cities replacing monocultures", TREE)], big=22)


def s14(s):
    head(s, "Impact dimensions · technology readiness")
    for k, (d, c) in enumerate((("Environmental", TREE), ("Social", HEAT), ("Technological", RAIN), ("Economic", WARN),
                                ("Policy", MUTED))):
        box(s, M + k * 2.5, 1.5, 2.3, 0.8, tint(c, 0.14))
        text(s, M + k * 2.5, 1.5, 2.3, 0.8, d, 17, c, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, M, 2.55, W - 2 * M, 0.4, "It turns a quota plan into a spatial one.", 18, INK)
    cw = (W - 2 * M) / 9
    for i in range(9):
        c = TREE if i in (2, 3) else (WARN if i in (4, 5) else MUTED)
        box(s, M + i * cw + 0.04, 3.4, cw - 0.08, 0.8, tint(c, 0.9 if i in (2, 3) else 0.18), radius=0.1)
        text(s, M + i * cw, 3.4, cw, 0.8, f"TRL {i + 1}", 16, WHITE if i in (2, 3) else c, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    for x, b, t, c in ((M + 2 * cw, "TRL 3 now → 4 by December", "validated in simulation, on real city data", TREE),
                       (M + 4 * cw, "TRL 5", "a test with a real designer", WARN),
                       (M + 6 * cw, "TRL 6+", "a pilot street, after the thesis", MUTED)):
        text(s, x, 4.4, 2 * cw + 0.3, 1.4, [[(b, {"bold": True, "color": c, "size": 18})], t], 15, INK)


def s15(s):
    box(s, 0, 0, W, H, TREE, radius=0)
    text(s, M + 0.4, 1.4, W - 2 * M, 0.5, "MY ASK", 20, "#CFC9BC", True, name="Mono")
    text(s, M + 0.4, 2.1, W - 2 * M - 0.8, 2.4, [[("Test it on one real street rebuild, with a designer or Parcs i Jardins.",
                                                   {"bold": True})], "Least loss, inside the city's rules."], 36, BG)
    text(s, M + 0.4, 5.8, W - 2 * M, 0.4, "giofox96.github.io/shade-and-sponge", 18, "#CFC9BC", name="Mono")


SLIDES = [s01, s02_context, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15]


def build():
    md = (OUT / "pitch_script.md").read_text(encoding="utf-8")
    notes = re.findall(r'^\*\*Say \(\d+ words\):\*\* "(.+)"$', md, re.M)
    assert len(notes) == len(SLIDES) == 15, len(notes)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for fn, n in zip(SLIDES, notes):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        for shp in s.shapes:   # labels, URLs and source lines in the mono face
            if shp.name in ("Mono", "Sources"):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = MONO
        s.notes_slide.notes_text_frame.text = n
    out = OUT / "shade_and_sponge_pechakucha.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
