"""Backup methodology overview for the midterm deck: the one-page 'Focus → Data → City screening → Project area → Design →
Evaluate → Validation' diagram (the v9 figure shown to the tutor on 17 Nov), updated for the 18 Nov decisions
(30-species palette, 'City practice' baseline, four actions per tree). Parametric: edit this script and rerun; the deck
picks up the new PNG. Same grammar and palette as make_flowcharts_v9.py.
Output: slides/midterm/fig/method_overview.svg/.png. Run from scripts/: python make_midterm_overview.py
"""
import make_infographics as mi
from make_infographics import t, rect, save, ROOT, INK, MUTED, GRID, HEAT, RAIN, TREE, WARN
from make_flowcharts import head, box, outline, curve, vline, caption, i_heat, i_rain, i_layers, i_area, i_check, i_radar

mi.OUT = ROOT / "slides/midterm/fig"
mi.OUT.mkdir(parents=True, exist_ok=True)
EXT_SRC = ("Ajuntament de Barcelona: Open Data BCN street-tree inventory, Mapa base topogràfic 1:1000, Pla director de l'arbrat "
           "2017–2037, Gestió de l'arbrat viari 2011; ICGC LiDAR 2021; Barcelona Resilience Atlas; PDISBA design storms.")


def flow_overview():
    X = [110, 330, 545, 720, 965, 1240, 1490]   # Project area compacted towards the screening: more room for the arrows
    MX, RX, ye = 1165, 1315, 535                # metric boxes, radar; ye = centre of the dashed frame (Evaluate, Validation aligned)
    b = "".join(head(x, h) for x, h in zip(X, ("Focus", "Data", "City screening", "Project area", "Design",
                                               "Evaluate", "Validation")))
    y0 = 470
    b += i_heat(X[0], 360) + caption(X[0], 422, "Heat stress", HEAT)
    b += i_rain(X[0], 580) + caption(X[0], 642, "Pluvial floods", RAIN)
    data = [("Tree inventory", TREE, None), ("LiDAR 2021", TREE, "crowns · buildings"), ("Hot day", HEAT, None),
            ("Terrain (DTM)", RAIN, "0.5 m · ground in 3D"), ("Flood hotspots", RAIN, None),
            ("Sidewalks · objects", WARN, "width · lamps · signs"), ("Design storm", RAIN, None)]
    ys = [245, 315, 385, 455, 525, 595, 665]
    for (lab, c, sub), y in zip(data, ys):
        b += box(X[1], y, lab, c, 196, 56 if sub else 48, sub)
    # heat → LiDAR (crowns, buildings: shade), hot day (sun path); floods → LiDAR (crown, LAI: water held on leaves),
    # DTM (where water flows), hotspots (where it does harm), design storm. Inventory and sidewalks serve both (constraints).
    for fy, dy in ((360, 315), (360, 385), (580, 315), (580, 455), (580, 525), (580, 665)):
        b += curve(X[0] + 40, fy, X[1] - 100, dy, GRID)
    b += i_layers(X[2], y0 - 25) + caption(X[2], y0 + 40, "Indicators per tree")
    for y in ys:
        b += curve(X[1] + 100, y, X[2] - 46, y0 - 25, GRID)
    # synthetic array right under the node: each position is a row of indicators x1..xn, grouped tree · place · score
    # (Angelos asked how the indicators are organised). The full table is the screening backup slide.
    cell, cols, rows = 19, 6, 3
    gcol = [TREE, TREE, TREE, WARN, WARN, HEAT]
    mx, my = X[2] - cols * cell / 2, y0 + 70
    for r in range(rows):
        for cc in range(cols):
            b += rect(mx + cc * cell, my + r * cell, cell - 3, cell - 3, gcol[cc], rx=3, op=0.20 + 0.14 * ((r + cc) % 3))
    b += t(X[2], my - 9, "x₁ x₂ … xn", 13, INK, "bold", "middle")
    b += t(X[2], my + rows * cell + 17, "one row per position", 12, MUTED, anchor="middle")
    b += t(X[2], my + rows * cell + 35, "tree · place · score", 12, MUTED, anchor="middle")
    # Project area: the designer sets an action per tree
    b += i_area(X[3], y0 - 25) + caption(X[3], y0 + 40, "The designer decides") + t(X[3], y0 + 62, "an action per tree", 14, MUTED, anchor="middle")
    b += curve(X[2] + 46, y0 - 25, X[3] - 40, y0 - 25, GRID)
    # Design: the four actions per tree (Angelos: four options). Keep and Move stay; Replace and Add go to the optimiser.
    actions = [("Keep", TREE, 330, "tree stays"), ("Move", WARN, 410, "frees a spot"),
               ("Replace", HEAT, 490, "optimiser picks"), ("Add", RAIN, 570, "optimiser picks")]
    for lab, c, y, sub in actions:
        b += box(X[4], y, lab, c, 196, 56, sub)
        b += curve(X[3] + 40, y0 - 25, X[4] - 100, y, GRID)
    b += outline(1044, 738, "City rules", WARN, 280, 64, "30 species · 15% cap · sidewalk size")   # centred on the dashed frame
    b += vline(1044, 706, 668, WARN)
    for k, (lab, c) in enumerate((("Heat", HEAT), ("Runoff", RAIN), ("Canopy", TREE))):
        y = 476 + 60 * k
        b += box(MX, y, lab, c, 110, 44)
        b += curve(X[4] + 100, 490, MX - 57, y, GRID) + curve(X[4] + 100, 570, MX - 57, y, GRID)
    b += i_radar(RX, ye) + t(RX, ye + 59, "vs today", 14, MUTED, anchor="middle")
    b += t(RX, ye + 77, "vs city practice", 14, MUTED, anchor="middle")
    for k in range(3):
        b += curve(MX + 57, 476 + 60 * k, RX - 40, ye, GRID)
    # Keep and Move are not optimised but are evaluated: the radar scores the whole layout. Each arrow starts from its own
    # box, runs above the frame and enters the radar from the top (no arrow into a group, as A. Chronis asked).
    for y in (330, 410):
        b += (f'<path d="M{X[4] + 100},{y} L{RX - 50},{y} Q{RX},{y} {RX},{y + 50} L{RX},{ye - 40}" fill="none" '
              f'stroke="{GRID}" stroke-width="1.8" marker-end="url(#arr)"/>')
    # one exact solve (not an iterative loop): a dashed frame around what the optimiser decides and scores
    b += (f'<rect x="852" y="444" width="384" height="182" rx="12" fill="none" stroke="{MUTED}" '
          'stroke-width="1.6" stroke-dasharray="7 5"/>')
    b += t(1236, 646, "Optimisation · HiGHS (one exact solve)", 14, INK, "bold", "end")
    b += i_check(X[6], ye) + caption(X[6], ye + 65, "Porta") + t(X[6], ye + 87, "→ Sant Antoni", 14, MUTED, anchor="middle")
    b += t(X[6], ye + 105, "Mataró · Florence", 14, MUTED, anchor="middle")
    b += curve(RX + 40, ye, X[6] - 40, ye, GRID)
    b += t(800, 815, "The designer sets an action per tree; the optimiser picks the species for every Replace and Add, within the city's rules.",
           17, MUTED, anchor="middle")
    save("method_overview", "Methodology", "Which species replace the trees a project removes, and where to add new ones: "
         "scored on heat, runoff and canopy", b, EXT_SRC)


if __name__ == "__main__":
    flow_overview()
