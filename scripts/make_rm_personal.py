"""RM final presentation, personal part (3 min, 6 slides), in the style of the RT Pecha Kucha (same helpers, fonts, palette).
Speaker notes = the "Say" lines of slides/rm_final/personal_script.md.
Output: slides/rm_final/shade_and_sponge_rm_personal.pptx. Run from scripts/: python make_rm_personal.py
"""
import re
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches
import make_deck_editable as mde
from make_deck_editable import ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN, W, H, M, rgb, tint, text, box, card, head, source, picture

OUT = ROOT / "slides/rm_final"
FONT, MONO = "IBM Plex Sans", "IBM Plex Mono"
mde.FONT = FONT


def s1(s):
    head(s, "Shade and Sponge", "Which species should replace the street trees a project removes?")
    for k, (big, small, c) in enumerate([
            ("10,976", "street trees replaced with another species in Barcelona, 2018–2026", WARN),
            ("13%", "of them plane trees (Platanus), the largest single case", HEAT),
            ("15%", "maximum share per species in the master plan; nothing says which species goes where", TREE)]):
        card(s, M + k * 4.18, 1.75, 3.9, 3.0, big, small, c, 48, 18)
    text(s, M, 5.2, W - 2 * M, 0.8, "Topic: choosing replacement species and positions for summer heat and storm water, "
         "inside the city's rules.", 19, INK)
    source(s, "Open Data BCN, arbrat viari, quarterly inventories 2018–2026; Ajuntament de Barcelona, Pla director de l'arbrat 2017–2037.")


def s2(s):
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


def s3(s):
    head(s, "Research gap: methodological", "Same trunk size, very different crowns (Porta's street trees)")
    picture(s, ROOT / "slides/fig_v8/v8_crowns.png", M + 1.4, 1.35, W - 2 * M - 2.8, crop_top=0.17, crop_bottom=0.2)
    box(s, M, 5.9, W - 2 * M, 0.7, tint(HEAT, 0.12))
    text(s, M + 0.3, 5.9, W - 2 * M - 0.6, 0.7, "Of 18 tools that place or assess urban trees, none chooses species tree by "
         "tree inside a city's rules.", 19, HEAT, True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "ICGC, LiDAR flight of 26 Sept 2021; Ajuntament de Barcelona, arbrat viari.")


def s4(s):
    head(s, "Refined question", "From trees against floods to replacing trees without harm")
    steps = [("October", "Trees against pluvial floods, Bologna / Florence", MUTED),
             ("Feedback", "Runoff depends on the tree pit more than the species: a check, not a promise. Any tree, not only planes.", WARN),
             ("Now", "Any tree a project replaces in Barcelona; plane trees = first case", TREE)]
    for k, (b, t, c) in enumerate(steps):
        x = M + k * 4.18
        box(s, x, 1.55, 3.9, 1.55, tint(c, 0.10))
        text(s, x + 0.25, 1.65, 3.4, 1.4, [[(b, {"bold": True, "color": c, "size": 17})], t], 14, INK)
    box(s, M, 3.4, W - 2 * M, 3.0, tint(INK, 0.06))
    text(s, M + 0.5, 3.4, W - 2 * M - 1.0, 3.0, "When a street project in Barcelona must replace trees, can a trait-based "
         "method, inside the city's tree rules, choose species and positions so that pedestrian cooling and storm-water "
         "interception improve, or at least do not get worse, compared with the city's own practice?", 24, INK, True,
         anchor=MSO_ANCHOR.MIDDLE)


def s5(s):
    head(s, "Method", "Open data in; a species for every tree to replace and for every free spot out")
    picture(s, ROOT / "slides/fig_v9/flow_00_overview.png", M + 0.15, 1.35, W - 2 * M - 0.3, crop_top=0.17, crop_bottom=0.075)


def s6(s):
    head(s, "Why this way")
    items = [("Exact optimiser", "The rules are hard limits: the best layout, reproducible (linear programme, HiGHS).", WARN),
             ("Open data only", "Any barri of Barcelona; transfer test in Mataró and Florence.", TREE),
             ("Real baseline", "What the city actually plants, from its own inventory.", RAIN),
             ("Checked", "Heat in Ladybug and Infrared City; back-test on real replacements.", HEAT)]
    for k, (b, t, c) in enumerate(items):
        x = M + k * 3.11
        box(s, x, 1.45, 2.9, 2.45, tint(c, 0.10))
        text(s, x + 0.25, 1.6, 2.4, 2.2, [[(b, {"bold": True, "color": c, "size": 20})], t], 15, INK)
    box(s, M, 4.2, W - 2 * M, 2.2, tint(TREE, 0.08))
    text(s, M + 0.5, 4.2, 4.8, 2.2, [[("59 → 139 m²·h", {"bold": True, "color": TREE, "size": 40})],
                                       "summer shade per replaced tree (median), city vs method"], 16, INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + 6.2, 4.2, 5.8, 2.2, [[("22 of 26", {"bold": True, "color": TREE, "size": 40})],
                                       "real replacement groups where the method gives more shade, at the same positions"],
         16, INK, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Huangfu & Hall 2018 (HiGHS); Ladybug Tools; Infrared City; Open Data BCN, arbrat viari quarterly inventories 2018–2026.")


SLIDES = [s1, s2, s3, s4, s5, s6]


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
