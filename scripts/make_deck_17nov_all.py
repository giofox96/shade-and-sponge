"""One deck for the 17 Nov tutor session: a title + agenda slide, the method slides (make_deck_method_17nov.py), the
back-test deck (make_backtest_deck.py, Street View version kept outside the public repo), the web-map slide, then the
method backups. Slides are copied as they are (merge_decks.copy_slide), notes included.
Run from scripts/: python make_deck_17nov_all.py METHOD.pptx BACKTEST.pptx OUT.pptx [MAP_BEFORE.png MAP_AFTER.png [MAP_DETAIL.png]]
"""
import sys
from pptx import Presentation
from pptx.util import Inches
from make_deck_editable import rgb, text, box, head, source, tint, W, H, M, BG, INK, MUTED, TREE, RAIN, WARN, HEAT
from merge_decks import copy_slide

METHOD, BACKTEST, OUT = sys.argv[1:4]
MAPS = sys.argv[4:7]
N_MAIN = 6          # method deck: overview, HiGHS, new trees, why replace, assumptions, position; the rest are backups

AGENDA = [("Method", "one page, the solver, where new trees go", INK),
          ("Your points of 10 Nov", "why replace, declared assumptions, what position changes for runoff", WARN),
          ("Back-test", "the method on the city's real street works, 2018–2026", TREE),
          ("Tool", "the cleaned-up 3D map", RAIN)]


def new_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)
    return s


def title(prs):
    s = new_slide(prs)
    text(s, M, 1.2, W - 2 * M, 0.9, "Shade and Sponge · 17 November", 40, INK, True)
    text(s, M, 2.05, W - 2 * M, 0.6, "Answers to the feedback of 10 November", 22, MUTED)
    for k, (h, sub, c) in enumerate(AGENDA):
        y = 3.1 + k * 0.85
        box(s, M, y, 0.12, 0.6, c, radius=0.02)
        text(s, M + 0.35, y - 0.02, W - 2 * M, 0.4, f"{k + 1}  {h}", 20, c, True)
        text(s, M + 0.35, y + 0.33, W - 2 * M, 0.35, sub, 15, MUTED)
    s.notes_slide.notes_text_frame.text = ("Four parts today: the method on one page with the solver and the new-tree rule; "
                                          "your points of last week; a back-test on the city's real street works; and the tool.")


def map_slide(prs, before, after, detail=None):
    s = new_slide(prs)
    head(s, "The tool: a cleaner 3D map", "Porta in the web app, same view before and after today's changes")
    n = 3 if detail else 2
    w = (W - 2 * M - 0.3 * (n - 1)) / n
    for k, (p, lab) in enumerate(((before, "Before"), (after, "After"), (detail, "Distances on click"))[:n]):
        pic = s.shapes.add_picture(p, Inches(M + k * (w + 0.3)), Inches(1.75), width=Inches(w))
        if pic.height > Inches(4.6):                       # keep the picture inside the slide
            r = Inches(4.6) / pic.height
            pic.height, pic.width = Inches(4.6), int(pic.width * r)
        text(s, M + k * (w + 0.3), 1.4, w, 0.35, lab, 15, MUTED, True)
    text(s, M, 6.45, W - 2 * M, 0.5, "Lighter façade and kerb lines; trunks down to the ground; free spots drawn as a dot "
         "inside the crown they would have; distance to façade and kerb shown only on click; basemap watermark removed.", 14, INK)
    source(s, "ICGC LiDAR 2021 and orthophoto; Ajuntament de Barcelona, Mapa base topogràfic 1:1000; OpenStreetMap; MapLibre; deck.gl.")
    s.notes_slide.notes_text_frame.text = ("Same view of Porta before and after today's changes. The drawing is lighter: thinner "
                                          "façade and kerb lines, trunks down to the ground, and each free spot shown as a dot "
                                          "inside the crown it would have. Clicking a spot shows its distance to the façade and "
                                          "to the kerb, the two numbers the spot rule uses.")


m, b = Presentation(METHOD), Presentation(BACKTEST)
out = Presentation()
out.slide_width, out.slide_height = m.slide_width, m.slide_height
title(out)
ms = list(m.slides)
for s in ms[:N_MAIN]:
    copy_slide(s, out)
for s in b.slides:
    copy_slide(s, out)
if len(MAPS) >= 2:
    map_slide(out, *MAPS)
for s in ms[N_MAIN:]:
    copy_slide(s, out)
out.save(OUT)
print("wrote", OUT, f"({len(out.slides)} slides)")
