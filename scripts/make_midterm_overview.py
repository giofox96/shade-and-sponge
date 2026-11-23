"""Backup methodology overview for the midterm deck: the one-page 'Focus → Data → City screening → Project area → Design →
Evaluate → Validation' diagram (the v9 figure shown to the tutor on 17 Nov), updated for the 18 Nov decisions
(30-species palette, 'City practice' baseline, four actions per tree). Parametric: edit this script and rerun; the deck
picks up the new PNG. Same grammar and palette as make_flowcharts_v9.py.
Output: slides/midterm/fig/method_overview.svg/.png. Run from scripts/: python make_midterm_overview.py
"""
import make_infographics as mi
from make_infographics import t, save, ROOT, MUTED, GRID, HEAT, RAIN, TREE, WARN
from make_flowcharts import head, box, outline, curve, vline, caption, loop, i_heat, i_rain, i_layers, i_area, i_check, i_radar

mi.OUT = ROOT / "slides/midterm/fig"
mi.OUT.mkdir(parents=True, exist_ok=True)
EXT_SRC = ("Ajuntament de Barcelona: Open Data BCN street-tree inventory, Mapa base topogràfic 1:1000, Pla director de l'arbrat "
           "2017–2037, Gestió de l'arbrat viari 2011; ICGC LiDAR 2021; Barcelona Resilience Atlas; PDISBA design storms.")


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
    # Project area: the designer's four actions, per tree
    b += i_area(X[3], y0 - 25) + caption(X[3], y0 + 40, "The designer decides") + t(X[3], y0 + 62, "keep · move · replace · add", 14, MUTED, anchor="middle")
    b += curve(X[2] + 46, y0 - 25, X[3] - 40, y0 - 25)
    b += box(X[4], 380, "Replacement", TREE, 190, 56, "trees the project removes")
    b += box(X[4], 560, "Additions", TREE, 190, 56, "free planting spots")
    b += curve(X[3] + 40, y0 - 25, X[4] - 97, 380) + curve(X[3] + 40, y0 - 25, X[4] - 97, 560)
    b += outline(X[4], 735, "City rules", WARN, 280, 70, "30 species · 15% cap · sidewalk size")
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
    b += t(800, 815, "The designer sets an action per tree; the optimiser picks the species for every Replace and Add, within the city's rules.",
           17, MUTED, anchor="middle")
    save("method_overview", "Methodology", "Which species replace the trees a project removes, and where to add new ones: "
         "scored on heat, runoff and canopy", b, EXT_SRC)


if __name__ == "__main__":
    flow_overview()
