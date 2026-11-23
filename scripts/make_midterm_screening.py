"""Backup slide for the midterm deck: what the city screening is, and how its indicators are organised — as a matrix,
one row per street-tree position (the question A. Chronis asked, 17 Nov). Groups: A the existing tree, B the place,
C a score for each of the 30 species (the table HiGHS reads). Parametric: edit and rerun; the deck picks up the PNG.
Output: slides/midterm/fig/screening_matrix.svg/.png. Run from scripts/: python make_midterm_screening.py
"""
import make_infographics as mi
from make_infographics import t, rect, save, ROOT, INK, MUTED, GRID, BG, HEAT, RAIN, TREE, WARN

mi.OUT = ROOT / "slides/midterm/fig"
mi.OUT.mkdir(parents=True, exist_ok=True)
WHITE = "#FFFFFF"

# columns: (key label, x-centre, width, group colour). A = the tree, B = the place.
COLS = [("Position", 150, 150, INK),
        ("Species", 300, 140, TREE), ("Trunk", 410, 80, TREE), ("Crown Ø", 495, 86, TREE),
        ("LAI", 575, 70, TREE), ("Priority", 655, 86, TREE),
        ("Sidewalk", 760, 96, WARN), ("Size", 850, 80, WARN), ("→ hotspot", 945, 96, WARN)]
ROWS = [["#0412", "Platanus", "TERCERA", "6.3 m", "2.3", "0.58", "4.2 m", "large", "no"],
        ["#0587", "Celtis", "SEGONA", "4.8 m", "2.0", "0.66", "3.1 m", "medium", "yes"],
        ["#0931", "Tilia", "TERCERA", "7.1 m", "2.6", "0.31", "6.4 m", "large", "no"],
        ["spot S-014", "— free —", "—", "—", "—", "—", "5.0 m", "large", "yes"]]
# C block: a score for each species (illustrative); the starred cell is the optimiser's pick for that row.
SCORES = [[.82, .61, .74, .55, .90, .48, .70, .66], [.60, .88, .52, .71, .49, .63, .80, .58],
          [.77, .59, .85, .50, .68, .72, .61, .55], [.71, .80, .64, .58, .83, .60, .52, .69]]
BEST = [4, 1, 2, 4]


def screening():
    b = ""
    yb, rh, y0 = 236, 60, 300
    # group bands
    for lab, x1, x2, c in (("A · THE EXISTING TREE", 232, 698, TREE), ("B · THE PLACE", 714, 996, WARN)):
        b += rect(x1, yb - 34, x2 - x1, 30, c, rx=6, op=0.16) + t((x1 + x2) / 2, yb - 13, lab, 14, c, "bold", "middle")
    b += rect(1012, yb - 34, 476, 30, HEAT, rx=6, op=0.16) + t(1250, yb - 13, "C · A SCORE FOR EACH OF THE 30 SPECIES", 14, HEAT, "bold", "middle")
    # column headers + x1..x9 tags
    for k, (lab, cx, w, c) in enumerate(COLS):
        b += t(cx, yb + 2, lab, 15, INK, "bold", "middle")
        if k:
            b += t(cx, yb + 20, f"x{chr(0x2080 + k)}", 12, MUTED, anchor="middle")
    b += t(1250, yb + 2, "weighted: summer shade + winter sun − water held", 14, MUTED, anchor="middle")
    b += t(1250, yb + 20, "x₉ … x₃₈ · one column per species", 12, MUTED, anchor="middle")
    # rows
    for r, row in enumerate(ROWS):
        y = y0 + r * rh
        b += rect(60, y, 952, rh - 8, WHITE if r % 2 else BG, rx=6, stroke=GRID)
        for (lab, cx, w, c), v in zip(COLS, row):
            b += t(cx, y + 36, v, 16, INK if lab == "Position" else MUTED, "bold" if lab == "Position" else "normal", "middle")
        # C: score cells per species
        cw = 52
        for j, v in enumerate(SCORES[r]):
            x = 1020 + j * cw
            on = j == BEST[r]
            b += rect(x, y + 6, cw - 6, rh - 20, HEAT if on else WHITE, rx=4, op=0.25 + 0.6 * v if on else 1,
                      stroke="none" if on else GRID)
            b += t(x + (cw - 6) / 2, y + 34, f"{v:.2f}", 14, WHITE if on else INK, "bold" if on else "normal", "middle")
            if on:
                b += t(x + cw - 11, y + 16, "★", 12, WHITE, anchor="middle")
        b += t(1020 + 8 * cw + 16, y + 36, "…", 18, MUTED, "bold")
    b += t(540, y0 + 4 * rh + 2, "… one row for every one of Porta's 2,825 street-tree positions and 153 free spots", 15, MUTED, anchor="middle")
    b += t(1250, y0 + 4 * rh + 2, "★ = the species HiGHS picks for that row", 15, HEAT, "bold", "middle")
    # reading guide
    gy = 772
    b += rect(60, gy, 1428, 56, WHITE, rx=10)
    for k, (c, lab, txt) in enumerate((
            (TREE, "A", "ranks which trees are candidates to replace"),
            (WARN, "B", "decides which species fit the sidewalk"),
            (HEAT, "C", "the matrix the optimiser solves: one species per row, within the 15% cap"))):
        x = 90 + k * 478
        b += rect(x, gy + 16, 24, 24, c, rx=5) + t(x + 12, gy + 33, lab, 14, WHITE, "bold", "middle")
        b += t(x + 36, gy + 33, txt, 15, INK)
    save("screening_matrix", "City screening", "Compute the same indicators once for every street-tree position and free "
         "spot — one row per position; three groups of columns", b,
         "Open Data BCN street-tree inventory; ICGC LiDAR 2021; Ajuntament de Barcelona, Mapa base topogràfic 1:1000, "
         "Gestió de l'arbrat viari 2011; Barcelona Resilience Atlas. Values illustrative.")


if __name__ == "__main__":
    screening()
