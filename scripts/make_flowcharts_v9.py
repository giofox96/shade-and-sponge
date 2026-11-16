"""Methodology figures for the 17 Nov session (tutor feedback of 10 Nov, notes/tutor_feedback_10nov.md): the one-page method
updated (terrain shown as its own input, keep / move / replace per tree, street objects, three validation cities) and a new
figure on what HiGHS does, with a five-position example. Same grammar and palette as make_flowcharts.py (v7 figures stay).
Output: slides/fig_v9/flow_00_overview.svg/.png, flow_07_highs.svg/.png. Run from scripts/: python make_flowcharts_v9.py
"""
import make_infographics as mi
from make_infographics import t, rect, save, ROOT, INK, MUTED, GRID, BG, HEAT, RAIN, TREE, WARN
from make_flowcharts import head, box, outline, curve, vline, caption, loop, i_heat, i_rain, i_layers, i_area, i_check, i_radar

mi.OUT = ROOT / "slides/fig_v9"
mi.OUT.mkdir(exist_ok=True)
WHITE = "#FFFFFF"
EXT_SRC = ("Ajuntament de Barcelona: Open Data BCN street-tree inventory, Mapa base topogràfic 1:1000, Pla director de l'arbrat "
           "2017–2037; ICGC LiDAR 2021; Barcelona Resilience Atlas; PDISBA design storms.")


def flow_overview():
    X = [110, 330, 560, 770, 1000, 1240, 1480]
    b = "".join(head(x, h) for x, h in zip(X, ("Focus", "Data", "City screening", "Project area", "Design",
                                               "Evaluate", "Validation")))
    y0 = 470
    b += i_heat(X[0], 360) + caption(X[0], 422, "Heat stress", HEAT)
    b += i_rain(X[0], 580) + caption(X[0], 642, "Pluvial floods", RAIN)
    data = [("Tree inventory", TREE, None), ("LiDAR 2021", TREE, "crowns · buildings"), ("Terrain (DTM)", RAIN, "0.5 m · ground in 3D"),
            ("Flood hotspots", RAIN, None), ("Sidewalks · objects", WARN, "width · lamps · signs"), ("Hot day · storms", HEAT, None)]
    ys = [255, 335, 415, 495, 575, 655]
    for (lab, c, sub), y in zip(data, ys):
        b += box(X[1], y, lab, c, 196, 56 if sub else 48, sub)
    for fy, dy in ((360, 335), (360, 655), (580, 415), (580, 495), (580, 655)):   # heat → LiDAR, hot day; floods → DTM, hotspots, storms
        b += curve(X[0] + 40, fy, X[1] - 100, dy, GRID)
    b += i_layers(X[2], y0 - 25) + caption(X[2], y0 + 40, "Indicators per tree") + t(X[2], y0 + 62, "shade · water flow · size", 14, MUTED, anchor="middle")
    for y in ys:
        b += curve(X[1] + 100, y, X[2] - 46, y0 - 25, GRID)
    b += i_area(X[3], y0 - 25) + caption(X[3], y0 + 40, "Draw an area") + t(X[3], y0 + 62, "keep · move · replace", 14, MUTED, anchor="middle")
    b += curve(X[2] + 46, y0 - 25, X[3] - 40, y0 - 25)
    b += box(X[4], 380, "Replacement", TREE, 190, 56, "trees the project removes")
    b += box(X[4], 560, "Additions", TREE, 190, 56, "free planting spots")
    b += curve(X[3] + 40, y0 - 25, X[4] - 97, 380) + curve(X[3] + 40, y0 - 25, X[4] - 97, 560)
    b += outline(X[4], 735, "City rules", WARN, 260, 70, "15% cap · sidewalk size · street objects")
    b += vline(X[4], 698, 592, WARN)
    for k, (lab, c) in enumerate((("Heat", HEAT), ("Runoff", RAIN), ("Canopy", TREE))):
        y = 360 + 110 * k
        b += box(X[5] - 70, y, lab, c, 110, 44)
        b += curve(X[4] + 97, 380, X[5] - 127, y, GRID) + curve(X[4] + 97, 560, X[5] - 127, y, GRID)
    b += i_radar(X[5] + 70, y0 - 25) + t(X[5] + 70, y0 + 34, "vs today", 14, MUTED, anchor="middle")
    b += t(X[5] + 70, y0 + 52, "vs city practice", 14, MUTED, anchor="middle")
    for k in range(3):
        b += curve(X[5] - 15, 360 + 110 * k, X[5] + 30, y0 - 25, GRID)
    b += loop(X[4], X[5] - 70, 360 - 22 + 44, "Optimisation · HiGHS")
    b += i_check(X[6], y0 - 25) + caption(X[6], y0 + 40, "Porta") + t(X[6], y0 + 62, "→ Sant Antoni", 14, MUTED, anchor="middle")
    b += t(X[6], y0 + 80, "Mataró · Florence", 14, MUTED, anchor="middle")
    b += curve(X[5] + 110, y0 - 25, X[6] - 40, y0 - 25)
    b += t(800, 815, "The terrain routes the storm water to the hotspots; the same ground carries trees and buildings in the 3D view.",
           17, MUTED, anchor="middle")
    save("flow_00_overview", "Methodology", "Which species replace the trees a project removes, and where to add new ones: "
         "scored on heat, runoff and canopy", b, EXT_SRC)


# ---- HiGHS, with a five-position example (scores are illustrative, not Porta's)
SP = [("A", "large", TREE), ("B", "medium", WARN), ("C", "small", RAIN)]
ROWS = [("1", "wide", [.9, .6, .3]), ("2", "wide", [.8, .7, .3]), ("3", "wide", [.7, .4, .2]),
        ("4", "medium", [None, .6, .5]), ("5", "narrow", [None, None, .4])]
BEST = [0, 1, 0, 1, 2]          # scipy.optimize.linprog(method="highs") on this table, cap 2 per species: total 3.3
GREEDY = [0, 0, 0, 1, 2]        # best species per position, ignoring the cap: A three times


def table(x0, y0, pick=None, bad=None):
    cw, rh = 62, 52
    s = "".join(t(x0 + 70 + k * cw + cw / 2, y0 - 12, n, 17, c, "bold", "middle") for k, (n, _, c) in enumerate(SP))
    for r, (pid, side, sc) in enumerate(ROWS):
        y = y0 + r * rh
        s += t(x0, y + 33, pid, 17, INK, "bold") + t(x0 + 18, y + 33, side, 13, MUTED)
        for k, v in enumerate(sc):
            x = x0 + 70 + k * cw
            on = pick is not None and pick[r] == k
            if v is None:
                s += rect(x + 3, y + 3, cw - 6, rh - 6, GRID, rx=4, op=0.5) + t(x + cw / 2, y + 33, "✗", 17, MUTED, anchor="middle")
                continue
            col = SP[k][2]
            s += rect(x + 3, y + 3, cw - 6, rh - 6, col if on else WHITE, rx=4, op=1 if on else 1, stroke=col if not on else "none")
            s += t(x + cw / 2, y + 33, f"{v:.1f}", 17, WHITE if on else INK, "bold" if on else "normal", "middle")
            if on and bad is not None and bad[r]:
                s += rect(x + 1, y + 1, cw - 2, rh - 2, "none", rx=5, stroke=HEAT)
    return s


def flow_highs():
    b = "".join(head(x, h) for x, h in zip((230, 620, 960, 1340), ("Score table", "City rules", "Exact solver", "Answer")))
    # 1. score table
    b += table(110, 290)
    b += t(230, 600, "Each species at each position:", 15, MUTED, anchor="middle")
    b += t(230, 620, "shade + winter sun + water held, weighted", 15, MUTED, anchor="middle")
    b += t(230, 640, "Porta: 832 positions × 7 species", 15, INK, "bold", "middle")
    # 2. rules
    rules = [("One species per position", "every tree gets exactly one", INK),
             ("Only species that fit", "✗ = sidewalk too narrow", WARN),
             ("No species above its cap", "15% (here: at most 2 of 5)", HEAT)]
    for k, (lab, sub, c) in enumerate(rules):
        b += outline(620, 330 + 115 * k, lab, c, 270, 74, sub)
    # 3. solver: a feasible region, the simplex path to the best corner
    cx, cy = 960, 440
    pts = [(cx - 110, cy + 90), (cx - 125, cy - 10), (cx - 55, cy - 95), (cx + 60, cy - 110), (cx + 120, cy - 30), (cx + 85, cy + 85)]
    b += '<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + f'" fill="{TREE}" fill-opacity="0.12" stroke="{TREE}" stroke-width="2"/>'
    path = [pts[0], pts[1], pts[2], pts[3]]
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        b += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="3" marker-end="url(#arr)"/>'
    for x, y in pts:
        b += f'<circle cx="{x}" cy="{y}" r="5" fill="{BG}" stroke="{TREE}" stroke-width="2"/>'
    b += f'<circle cx="{pts[3][0]}" cy="{pts[3][1]}" r="9" fill="{HEAT}"/>' + t(pts[3][0] + 14, pts[3][1] - 10, "best", 16, HEAT, "bold")
    b += t(pts[0][0] - 8, pts[0][1] + 24, "start", 14, MUTED, anchor="middle")
    b += t(cx, cy + 150, "Every layout that obeys the rules", 15, MUTED, anchor="middle")
    b += t(cx, cy + 170, "is a point in this shape; the best is a corner.", 15, MUTED, anchor="middle")
    b += t(cx, cy + 194, "HiGHS walks corner to corner, always uphill,", 15, INK, "bold", "middle")
    b += t(cx, cy + 214, "and proves no corner is higher.", 15, INK, "bold", "middle")
    # 4. answer
    b += table(1220, 290, pick=BEST)
    b += t(1340, 600, "Total 3.3: the best possible", 15, INK, "bold", "middle")
    b += t(1340, 620, "A goes where its lead is largest (1, 3);", 15, MUTED, anchor="middle")
    b += t(1340, 640, "position 2 takes B, losing only 0.1", 15, MUTED, anchor="middle")
    # flow between columns
    for x1, x2 in ((360, 480), (760, 830), (1095, 1205)):
        b += curve(x1, 440, x2, 440, MUTED)
    # bottom: why not simpler routes
    b += rect(110, 700, 1380, 92, WHITE, rx=10)
    b += t(140, 735, "Best-per-position (greedy):", 16, INK, "bold") + t(470, 735, "A, A, A, B, C: breaks the cap.", 16, MUTED)
    b += t(140, 770, "Trial and error (genetic, ant colony):", 16, INK, "bold") + t(470, 770, "obeys the rules, but never knows if it found the best.", 16, MUTED)
    b += t(1060, 735, "Porta: 0.06 s · whole city: ~10 s", 16, INK, "bold")
    b += t(1060, 770, "Answer is always whole trees", 16, MUTED)
    save("flow_07_highs", "HiGHS: the solver that picks every species", "One exact solve: the best layout that obeys every rule, "
         "and a proof that no other layout scores higher", b,
         "HiGHS open-source linear optimisation solver (highs.dev; Huangfu & Hall 2018, Math. Prog. Comp. 10:119–142), "
         "called through SciPy. Example scores are illustrative.")


if __name__ == "__main__":
    flow_overview()
    flow_highs()
