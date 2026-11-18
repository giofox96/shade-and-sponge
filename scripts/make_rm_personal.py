"""RM final presentation, personal part (3 min, 9 slides: 8 of about 22 s + thanks), in the style of the RT Pecha Kucha (same helpers, fonts, palette).
Speaker notes = the "Say" lines of slides/rm_final/personal_script.md.
Output: slides/rm_final/shade_and_sponge_rm_personal.pptx. Run from scripts/: python make_rm_personal.py
"""
import io
import re
from PIL import Image
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches
import make_deck_editable as mde
from make_rm_personal_figs import icon_png
from make_deck_editable import ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, rgb, tint, text, box, head, source, picture

OUT = ROOT / "slides/rm_final"
FONT, MONO = "IBM Plex Sans", "IBM Plex Mono"
mde.FONT = FONT


def s1_photo(s):
    im = Image.open(ROOT / "slides/fig/01_title_photo.webp").convert("RGB")   # same photo and scrim as the RT pitch title
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


def s1(s):
    s1_photo(s)
    text(s, 0.75, 1.5, 7.4, 1.0, "Shade and Sponge", 54, BG, True, name="Title")
    text(s, 0.75, 2.7, 7.0, 3.0, [[("“I am redesigning this street. ", {"bold": True})],
         "Which trees do I keep, move or replace, and where do I add new ones, so the street is cooler in summer "
         "and not worse for flooding, within the city's rules?”"], 22, BG)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Research & Methodologies", 16, "#CFC9BC", name="Mono")


def ico(s, name, color, x, y, size=0.5):
    return s.shapes.add_picture(str(icon_png(name, color)), Inches(x), Inches(y), Inches(size), Inches(size))


def s2(s):
    head(s, "Context: replacing trees one at a time", "Barcelona, and my site, Porta (Nou Barris)")
    for k, (ic, big, small, c) in enumerate([
            ("refresh-ccw", "10,976", "trees replaced, 2018–2026", WARN),
            ("chart-pie", "15%", "max per species; no rule on where", TREE),
            ("trees", "20.1%", "Porta's canopy; city target 30%", HEAT)]):
        y = 1.65 + k * 1.55
        ico(s, ic, c, M, y + 0.15, 0.6)
        text(s, M + 0.85, y, 3.6, 1.4, [[(big, {"bold": True, "color": c, "size": 36})], [(small, {"size": 15})]], 15, INK)
    text(s, M + 4.7, 1.55, 7.6, 0.4, "Same trunk, different crowns: crown area vs a plane tree", 16, INK, True)
    picture(s, ROOT / "slides/fig_v8/v8_crowns.png", M + 4.6, 1.95, 7.7, crop_top=0.17, crop_bottom=0.2)
    text(s, M + 4.7, 4.85, 7.6, 0.4, [[("■ ", {"color": TREE}), ("smaller trunks   ", {}), ("■ ", {"color": tint(TREE, 0.3)}),
                                       ("larger trunks   ", {}), ("┆ plane = 100%   n = trees measured", {})]], 12, MUTED)
    source(s, "Open Data BCN, arbrat viari 2018–2026; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; ICGC, LiDAR 2021.")


def s3(s):
    head(s, "State of the art and gap", "Each piece exists; nobody joins them")
    picture(s, ROOT / "slides/rm_final/fig/gap_flow.png", M + 0.4, 1.5, W - 2 * M - 0.8, crop_top=0)
    source(s, "Mannucci et al. 2025; Wu et al. 2024; Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026; Nicol et al. 2026 (PLoS One).")


def s4(s):
    head(s, "Refined question")
    ico(s, "repeat", MUTED, M, 1.45, 0.4)
    text(s, M + 0.55, 1.45, W - 2 * M - 0.6, 0.5, [[("October: ", {"bold": True}), ("trees against floods, Bologna.  ", {}),
         ("Feedback: ", {"bold": True}), ("runoff depends on the pit more than the species → a do-no-harm check.", {})]], 15, MUTED)
    box(s, M, 2.3, W - 2 * M, 3.9, tint(INK, 0.06))
    text(s, M + 0.6, 2.3, W - 2 * M - 1.2, 3.9, "When a street project in Barcelona must replace or add trees, to what extent "
         "can a trait-based method that chooses species and positions inside the city's tree rules give more summer "
         "cooling than the city's own replacement practice, without losing rain interception?", 26, INK, True,
         anchor=MSO_ANCHOR.MIDDLE)


def s5(s):
    head(s, "What is fixed, what is free", "The project sets the street; the tool advises, the designer decides")
    box(s, M, 1.55, 5.0, 4.9, tint(MUTED, 0.10))
    ico(s, "lock", MUTED, M + 0.3, 1.8, 0.5)
    text(s, M + 0.95, 1.83, 3.8, 0.5, "FIXED", 20, MUTED, True)
    text(s, M + 0.3, 2.6, 4.4, 3.6, ["Street layout", "15% cap per species", "Sidewalk width → tree size",
                                     "Lamps, signs, traffic lights"], 18, INK)
    acts = [("tree-deciduous", "Keep", TREE), ("move", "Move", WARN), ("refresh-ccw", "Replace", HEAT), ("circle-plus", "Add", RAIN)]
    for k, (ic, b, c) in enumerate(acts):
        x, y = M + 5.3 + (k % 2) * 3.5, 1.55 + (k // 2) * 2.0
        box(s, x, y, 3.3, 1.8, tint(c, 0.12))
        ico(s, ic, c, x + 0.3, y + 0.55, 0.7)
        text(s, x + 1.2, y, 2.0, 1.8, b, 26, c, True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + 5.3, 5.65, 6.8, 0.8, [[("FREE: ", {"bold": True}), ("four actions per tree; never remove without replacing.", {})]], 16, INK)
    source(s, "Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; Parcs i Jardins, street-tree guide (2011).")


def s6(s):
    head(s, "Method", "Screen every tree and spot, choose within the rules, compare")
    picture(s, ROOT / "slides/rm_final/fig/method_flow.png", M + 0.15, 1.5, W - 2 * M - 0.3, crop_top=0)
    source(s, "Open Data BCN, arbrat viari; ICGC, LiDAR 2021; Parcs i Jardins, street-tree guide (2011); Huangfu & Hall 2018 (HiGHS); "
           "Ladybug Tools; Infrared City.")


def s7(s):
    head(s, "Why this way, and not another")
    items = [("target", "Exact optimiser", "rules are hard limits; proves the best", WARN),
             ("database", "Open data only", "any Barcelona neighbourhood", TREE),
             ("landmark", "City practice", "what the city really planted", RAIN)]
    for k, (ic, b, t, c) in enumerate(items):
        x = M + k * 4.18
        box(s, x, 1.5, 3.9, 2.3, tint(c, 0.10))
        ico(s, ic, c, x + 0.3, 1.75, 0.6)
        text(s, x + 0.3, 2.5, 3.3, 1.2, [[(b, {"bold": True, "color": c, "size": 21})], t], 15, INK)
    ico(s, "circle-x", MUTED, M, 4.05, 0.35)
    text(s, M + 0.5, 4.05, W - 2 * M - 0.5, 0.5, [[("Not: ", {"bold": True}), ("field measurement · machine learning · "
         "full microclimate simulation everywhere", {})]], 16, MUTED)
    box(s, M, 4.8, W - 2 * M, 1.5, tint(HEAT, 0.10))
    text(s, M + 0.5, 4.8, W - 2 * M - 1.0, 1.5, [[("1 in 5 ", {"bold": True, "color": HEAT, "size": 40}),
         ("new city plantings is larger than its sidewalk allows", {"size": 20})]], 18, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Huangfu & Hall 2018 (HiGHS); Open Data BCN, arbrat viari 2018–2026; Parcs i Jardins, street-tree guide (2011).")


def s8(s):
    head(s, "First evidence: back-test", "26 groups where the city replaced trees: same positions, city's choice vs method")
    box(s, M, 1.6, W - 2 * M, 2.9, tint(TREE, 0.08))
    ico(s, "sun", WARN, M + 0.5, 2.05, 0.8)
    text(s, M + 1.5, 1.6, 4.6, 2.9, [[("59 → 139", {"bold": True, "color": TREE, "size": 44})],
                                     "m²·h summer shade per tree (median), city vs method"], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    ico(s, "circle-check", TREE, M + 6.6, 2.05, 0.8)
    text(s, M + 7.6, 1.6, 4.5, 2.9, [[("22 of 26", {"bold": True, "color": TREE, "size": 44})],
                                     "groups where the method gives more shade"], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 4.9, W - 2 * M, 1.0, [[("Next: ", {"bold": True}), ("UTCI in Ladybug and Infrared City · Mataró and Florence", {})]], 18, INK)
    source(s, "Open Data BCN, arbrat viari 2018–2026; ICGC LiDAR 2021.")


def s9(s):
    s1_photo(s)
    text(s, 0.75, 2.4, 7.4, 1.2, "Thank you", 60, BG, True, name="Title")
    text(s, 0.75, 3.7, 7.0, 1.0, "Shade and Sponge: the right tree, in the right place, within the city's rules.", 22, BG)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Research & Methodologies", 16, "#CFC9BC", name="Mono")


SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def build():
    md = (OUT / "personal_script.md").read_text(encoding="utf-8")
    notes = re.findall(r'^\*\*Say \(\d+ words\):\*\* "(.+)"$', md, re.M)
    assert len(notes) == len(SLIDES), len(notes)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for fn, n in zip(SLIDES, notes):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        for shp in s.shapes:
            if shp.name in ("Mono", "Sources"):
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = MONO
        s.notes_slide.notes_text_frame.text = n
    out = OUT / "shade_and_sponge_rm_personal.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
