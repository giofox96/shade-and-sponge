"""RM final presentation, personal part (mini Pecha Kucha, 3 min, 10 slides of about 18 s), in the style of the RT Pecha Kucha (same helpers, fonts, palette).
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
from make_deck_editable import ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, rgb, tint, text, box, card, head, source, picture

OUT = ROOT / "slides/rm_final"
FONT, MONO = "IBM Plex Sans", "IBM Plex Mono"
mde.FONT = FONT


def s1(s):
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
    text(s, 0.75, 1.5, 7.4, 1.0, "Shade and Sponge", 54, BG, True, name="Title")
    text(s, 0.75, 2.7, 7.0, 3.0, [[("“I am redesigning this street. ", {"bold": True})],
         "Which trees do I keep, move or replace, and where do I add new ones, so the street is cooler in summer "
         "and not worse for flooding, within the city's rules?”"], 22, BG)
    text(s, 0.75, 6.2, 11.0, 0.4, "Giovanni Volpe · MaCAD, IAAC · Research & Methodologies", 16, "#CFC9BC", name="Mono")


def s2(s):
    head(s, "Context: replacing trees one at a time", "Barcelona city-wide, and my site, Porta (Nou Barris)")
    for k, (big, small, c) in enumerate([
            ("10,976", "street trees replaced with another species, 2018–2026; plane trees (Platanus) the largest case, 13%", WARN),
            ("15%", "maximum share per species (master plan); nothing says which species goes where", TREE),
            ("20.1%", "Porta's canopy today (16.8 ha); 8.3 ha short of the city's 30% target", HEAT)]):
        card(s, M + k * 4.18, 1.75, 3.9, 3.2, big, small, c, 48, 17)
    source(s, "Open Data BCN, arbrat viari, quarterly inventories 2018–2026; Ajuntament de Barcelona, Pla director de l'arbrat "
           "2017–2037; ICGC, LiDAR flight of 26 Sept 2021.")


def s3(s):
    head(s, "State of the art", "Each piece exists; nobody joins them")
    items = [("Heat + runoff, fixed scenarios", "No choice of species", "Mannucci et al. 2025; Wu et al. 2024", RAIN),
             ("Tree placement optimisers", "Heat only", "Shaamala et al. 2025; Peng et al. 2026", HEAT),
             ("Species rankings by services", "No positions", "Dong et al. 2026", WARN),
             ("Trait-based recommender", "Runoff module switched off", "SylvCiT, Nicol et al. 2026", TREE)]
    for k, (b, t, ref, c) in enumerate(items):
        x = M + k * 3.11
        box(s, x, 1.7, 2.9, 2.7, tint(c, 0.10))
        text(s, x + 0.25, 1.95, 2.4, 2.3, [[(b, {"bold": True, "color": c, "size": 21})], t, [(ref, {"size": 13, "color": MUTED})]],
             18, INK)
    text(s, M, 4.85, W - 2 * M, 0.8, "Missing: species and positions together, scored on both services, inside a city's rules.",
         20, INK, True)
    source(s, "Mannucci et al. 2025; Wu et al. 2024; Shaamala et al. 2025; Peng et al. 2026; Dong et al. 2026; Nicol et al. 2026 (PLoS One).")


def s4(s):
    head(s, "Research gap: methodological", "Same trunk size, very different crowns (Porta's street trees)")
    picture(s, ROOT / "slides/fig_v8/v8_crowns.png", M + 1.4, 1.35, W - 2 * M - 2.8, crop_top=0.17, crop_bottom=0.2)
    text(s, M + 1.4, 4.75, W - 2 * M - 2.8, 1.2, [
        [("Why these species: ", {"bold": True}), ("the six most common on Porta's streets after the plane tree, all "
                                                 "candidates to replace it.", {})],
        [("Bar = crown area as a share of a plane's with the same trunk (41–110 cm perimeter). Dark = smaller of the two "
          "trunk classes, light = larger; dashed line = plane, 100%; n = trees measured.", {"color": MUTED, "size": 12})]],
        14, INK)
    box(s, M, 6.05, W - 2 * M, 0.75, tint(HEAT, 0.12))
    text(s, M + 0.3, 6.05, W - 2 * M - 0.6, 0.75, "Of 18 tools that place or assess urban trees, none chooses species tree by "
         "tree inside a city's rules.", 18, HEAT, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, arbrat viari (Porta).")


def s5(s):
    head(s, "Refined question", "From trees against floods to replacing trees without harm")
    steps = [("October", "Trees against pluvial floods, Bologna / Florence", MUTED),
             ("Feedback", "Runoff depends on the tree pit more than the species: a check, not a promise. Any tree, not only planes.", WARN),
             ("Now", "Any tree a project replaces in Barcelona; plane trees = first case", TREE)]
    for k, (b, t, c) in enumerate(steps):
        x = M + k * 4.18
        box(s, x, 1.55, 3.9, 1.55, tint(c, 0.10))
        text(s, x + 0.25, 1.65, 3.4, 1.4, [[(b, {"bold": True, "color": c, "size": 17})], t], 14, INK)
    box(s, M, 3.4, W - 2 * M, 3.0, tint(INK, 0.06))
    text(s, M + 0.5, 3.4, W - 2 * M - 1.0, 3.0, "When a street project in Barcelona must replace or add trees, to what extent "
         "can a trait-based method that chooses species and positions inside the city's tree rules give more summer "
         "cooling than the city's own replacement practice, without losing rain interception?", 24, INK, True,
         anchor=MSO_ANCHOR.MIDDLE)


def s6(s):
    head(s, "What is fixed, what is free", "The street project sets the layout; the tool advises, the designer decides")
    box(s, M, 1.55, 5.0, 4.9, tint(MUTED, 0.10))
    text(s, M + 0.3, 1.7, 4.4, 4.6, [[("FIXED", {"bold": True, "color": MUTED, "size": 18})],
         "Street geometry, sidewalk width, kerbs", "15% cap per species", "Sidewalk width → tree size class",
         "Distance to lamps, signs, traffic lights"], 17, INK)
    acts = [("Keep", "the default", TREE), ("Move", "if the project needs it", WARN),
            ("Replace", "cut + a new species", HEAT), ("Add", "on a free spot", RAIN)]
    for k, (b, t, c) in enumerate(acts):
        x, y = M + 5.3 + (k % 2) * 3.5, 1.55 + (k // 2) * 2.0
        box(s, x, y, 3.3, 1.8, tint(c, 0.12))
        text(s, x + 0.3, y + 0.2, 2.8, 1.5, [[(b, {"bold": True, "color": c, "size": 26})], t], 16, INK)
    text(s, M + 5.3, 5.65, 6.8, 0.8, [[("FREE: four actions per tree. ", {"bold": True}), ("Removing without replacing is not an option.", {})]],
         16, INK)
    source(s, "Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037; Parcs i Jardins, street-tree guide (2011).")


def s7(s):
    head(s, "Method", "Open data in; a species for every tree to replace and for every free spot out")
    picture(s, ROOT / "slides/fig_v9/flow_00_overview.png", M + 0.15, 1.35, W - 2 * M - 0.3, crop_top=0.17, crop_bottom=0.075)


def s8(s):
    head(s, "The screening", "Computed once for every street tree and free spot, before any design")
    cols = [("A · What stands there", ["Species and trunk class (city inventory)", "Crown, height, leaf density (LiDAR 2021)",
                                       "Crown vigour → replacement priority: a hint, not a diagnosis"], TREE,
             "suggests which trees to replace"),
            ("B · Where it is", ["Sidewalk width → allowed tree size", "Distance to façade, lamps, signs, crossings",
                                 "Does its rain flow to a flood hotspot?"], WARN, "decides which species fit"),
            ("C · What each species would do", ["Summer shade (benefit)", "Winter shade (cost)",
                                                 "Rain held before a hotspot (benefit)", "Fits: yes / no"], HEAT,
             "the optimiser's table: 30 species × every position")]
    for k, (b, items, c, role) in enumerate(cols):
        x = M + k * 4.18
        box(s, x, 1.55, 3.9, 3.5, tint(c, 0.10))
        text(s, x + 0.3, 1.75, 3.3, 3.6, [[(b, {"bold": True, "color": c, "size": 20})]] + ["· " + i for i in items], 16, INK)
        box(s, x, 5.2, 3.9, 0.75, tint(c, 0.22))
        text(s, x + 0.3, 5.2, 3.3, 0.75, [[("→ " + role, {"bold": True, "color": c})]], 15, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Open Data BCN, arbrat viari; ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, Mapa topogràfic 1:1000; "
           "Parcs i Jardins, street-tree guide (2011); Barcelona Resilience Atlas.")


def s9(s):
    head(s, "Why this way")
    items = [("Exact optimiser", "The rules are hard limits: it finds the best layout and proves it (linear programme, HiGHS).", WARN),
             ("Open data only", "Any neighbourhood of Barcelona; transfer test in Mataró and Florence.", TREE),
             ("City practice as baseline", "What the city actually planted 2018–2026, not what it announced. A practice, not a rule.", RAIN)]
    for k, (b, t, c) in enumerate(items):
        x = M + k * 4.18
        box(s, x, 1.5, 3.9, 2.6, tint(c, 0.10))
        text(s, x + 0.3, 1.7, 3.3, 2.3, [[(b, {"bold": True, "color": c, "size": 21})], t], 16, INK)
    box(s, M, 4.4, W - 2 * M, 1.9, tint(HEAT, 0.10))
    text(s, M + 0.5, 4.4, W - 2 * M - 1.0, 1.9, [[("1 in 5 ", {"bold": True, "color": HEAT, "size": 40}),
         ("of the city's new plantings is larger than its sidewalk allows (2011 guide).", {"size": 20})],
         [("The method also measures what each rule costs.", {"size": 18, "color": MUTED})]], 18, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Huangfu & Hall 2018 (HiGHS); Open Data BCN, arbrat viari quarterly inventories 2018–2026; Parcs i Jardins, street-tree guide (2011).")


def s10(s):
    head(s, "First evidence: back-test on real replacements", "26 groups where the city replaced trees; same positions, city's choice vs method")
    box(s, M, 1.6, W - 2 * M, 2.6, tint(TREE, 0.08))
    text(s, M + 0.5, 1.6, 4.8, 2.6, [[("59 → 139 m²·h", {"bold": True, "color": TREE, "size": 40})],
                                       "summer shade per replaced tree (median): city practice vs method"], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + 6.2, 1.6, 5.8, 2.6, [[("22 of 26", {"bold": True, "color": TREE, "size": 40})],
                                       "real replacement groups where the method gives more shade, at the same positions"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 4.6, W - 2 * M, 1.4, [[("Next: ", {"bold": True}), ("heat checked in Ladybug and Infrared City (UTCI); transfer to Mataró "
         "and Florence.", {})], [("Runoff stays a do-no-harm check.", {"color": MUTED})]], 19, INK)
    source(s, "Open Data BCN, arbrat viari quarterly inventories 2018–2026; ICGC LiDAR 2021; Ladybug Tools; Infrared City.")


SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]


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
