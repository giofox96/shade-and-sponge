"""Figures for the v6 deck (slides/outline_v6.md): 1600x900 SVG + PNG in slides/fig_v6/, same style as
make_infographics.py (whose helpers are reused). Numbers: notes/topic_decision.md section 9, notes/tree_master_plan.md,
databases/barcelona/crown_by_trunk_class.csv, databases/barcelona/porta_sidewalk_width.csv.
Run from scripts/: python make_slides_v6.py
"""
import pandas as pd
import make_infographics as mi
from make_infographics import t, para, rect, line, save, ROOT, INK, MUTED, GRID, HEAT, RAIN, TREE, WARN

mi.OUT = ROOT / "slides/fig_v6"


def fig_decided():
    yes = [("How much of each species", "No species above 15% of the urban fabric by 2037; planes cut by 56%, to 12%, in ten years",
            "plan target 3; press May 2026"),
           ("How and when", "Gradually, as trees die and when streets are rebuilt", "press 2022, 2026"),
           ("Which species may be used", "The species catalogue, plus a target mix for the replacements",
            "2011 guide pp. 49–56; press 2026"),
           ("Which tree size fits which street", "Sidewalk width sets the size class and the spacing", "2011 guide pp. 22–23")]
    no = [("Which species at each position", "Chosen one tree at a time from qualitative criteria (orientation, space, "
           "soil, desired shade); no public list", "press 2022"),
          ("What each choice does to heat and runoff", "No document quantifies it, per species or per position",
           "plan; 2011 guide"),
          ("Where heat and flooding overlap", "The plan is city-wide, with no link to the flood or heat-vulnerability maps",
           "plan")]
    b = ""
    for col, (head, rows, color, mark) in enumerate((("DECIDED BY THE CITY", yes, TREE, "✓"),
                                                     ("LEFT OPEN", no, HEAT, "✗"))):
        x = 60 + col * 760
        b += t(x, 175, head, 18, color, "bold")
        y = 200
        for q, a, src in rows:
            h = 135 if col else 120
            b += rect(x, y, 720, h - 14, color, rx=10, op=0.07)
            b += t(x + 22, y + 40, mark, 30, color, "bold") + t(x + 64, y + 36, q, 22, INK, "bold")
            b += para(x + 64, y + 64, a, 630, 17)[0] + t(x + 690, y + h - 26, src, 13, MUTED, anchor="end", italic=True)
            y += h
    b += rect(820, 640, 720, 150, INK, rx=12, op=0.05)
    b += para(844, 680, "The thesis sits in the right-hand column: a method that takes the left-hand column as hard "
              "constraints and fills in the three open questions with numbers.", 680, 21, fill=INK, weight="bold")[0]
    save("v6_03_decided", "The city decided how much, not which species where",
         "Barcelona's tree master plan (2017–2037) and street-tree guide (2011), read 20 Oct", b,
         "Ajuntament de Barcelona, Pla director de l'arbrat 2017-2037; Gestio de l'arbrat viari de Barcelona (2011); "
         "press marked as such (Time Out 2022, Beteve May 2026). notes/topic_decision.md 9.1, notes/tree_master_plan.md.")


def fig_crowns():
    d = pd.read_csv(ROOT / "databases/barcelona/crown_by_trunk_class.csv", header=[0, 1], index_col=0)
    r, n = d["area_ratio_vs_plane"], d["n"]
    sp = ["Platanus x acerifolia", "Tipuana tipu", "Jacaranda mimosifolia", "Melia azedarach", "Celtis australis",
          "Pyrus calleryana", "Brachychiton populneus"]
    named = {"Celtis australis", "Melia azedarach", "Tipuana tipu", "Pyrus calleryana"}
    x0, sc, b = 480, 820, ""
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        b += line(x0 + v * sc, 170, x0 + v * sc, 690, GRID, 1)
        b += t(x0 + v * sc, 715, f"{v:.0%}", 16, MUTED, anchor="middle")
    b += line(x0 + sc, 170, x0 + sc, 690, INK, 2, dash="6 4")
    for i, s in enumerate(sp):
        y = 200 + i * 72
        lo, hi = r.loc[s, ["SEGONA", "TERCERA"]].min(), r.loc[s, ["SEGONA", "TERCERA"]].max()
        col = INK if s.startswith("Platanus") else (TREE if s in named else WARN)
        b += t(60, y + 8, s.replace(" x ", " × "), 22, col, "bold", italic=True)
        tag = "plane (reference)" if s.startswith("Platanus") else ("named by the city" if s in named else "not named")
        b += t(60, y + 32, tag, 14, MUTED)
        b += rect(x0, y - 14, max(hi, 0.005) * sc, 30, col, rx=6, op=0.25) + rect(x0, y - 14, lo * sc, 30, col, rx=6, op=0.8)
        lab = f"{lo:.0%}" if lo == hi else f"{lo:.0%}–{hi:.0%}"
        nn = "/".join(str(int(v)) for v in n.loc[s, ["SEGONA", "TERCERA"]].dropna() if v > 0)
        lx = x0 + max(hi, 1.0) * sc + 18 if hi > 0.85 else x0 + hi * sc + 14     # labels clear of the 100% line
        b += t(lx, y + 8, lab, 20, col, "bold") + t(lx, y + 28, f"n = {nn}", 13, MUTED)
    b += para(60, 760, "Crown area as a share of a plane's, in the same trunk class (2nd and 3rd: 41–110 cm perimeter), "
              "as the trees stand in Porta (LiDAR 2021). Dark bar = the lower of the two class values, light = the higher; n = trees in the 2nd/3rd class. "
              "Equal trunk size is not equal age, and street trees are pruned: this is not mature potential.", 1480, 17,
              fill=MUTED)[0]
    save("v6_04_crowns", "The replacements differ: from a full crown to a quarter of one",
         "Same trunk size, very different shade and interception — the choice of species decides the canopy", b,
         "databases/barcelona/crown_by_trunk_class.csv (scripts/crown_by_trunk_class.py), Porta street trees, "
         "ICGC LiDAR 26 Sept 2021; notes/topic_decision.md 9.9. Styphnolobium left out (5 trees in Porta).")


def fig_rq():
    b = rect(60, 160, 1480, 400, INK, rx=12, op=0.05)
    b += t(84, 206, "In Porta, as plane trees are replaced under Barcelona's tree master plan,", 26, MUTED)
    b += t(84, 250, "which replacement species, chosen within the plan's rules, and at which plane positions,", 28, INK, "bold")
    for i, (h, c) in enumerate((("≤ 15% per species", TREE), ("size class set by sidewalk width", TREE),
                                ("the city's species catalogue", TREE))):
        b += rect(84 + i * 480, 272, 450, 44, c, rx=22, op=0.12) + t(309 + i * 480, 301, h, 19, c, "bold", "middle")
    b += t(84, 356, "jointly reduce", 26, INK, "bold")
    b += rect(84, 372, 700, 92, HEAT, rx=10, op=0.10)
    b += t(104, 404, "(a)  pedestrian heat stress", 23, HEAT, "bold")
    b += t(104, 436, "mean UTCI over 12–17 h on a hot design day, sun-exposed routes", 19)
    b += rect(816, 372, 700, 92, RAIN, rx=10, op=0.10)
    b += t(836, 404, "(b)  event runoff volume", 23, RAIN, "bold")
    b += t(836, 436, "sealed street surfaces, 1-, 2- and 10-year PDISBA design storms", 19)
    b += t(84, 508, "How large is the trade-off, and how far do rule-compliant optimised choices differ", 24, INK, "bold")
    b += t(84, 540, "from the current trees (S0) and from the city's own replacement (S1)?", 24, INK, "bold")
    b += t(60, 610, "What changed from v5 (21 Oct)", 18, TREE, "bold")
    for i, (h, d) in enumerate((
            ("THE RULES ARE EXPLICIT", "the 15% cap, the sizing rule and the catalogue are hard constraints, not "
             "background"),
            ("S1 IS THE CITY", "the 2026 target mix, placed by the city's own sizing rule at random — what happens "
             "anyway, not a like-for-like swap"),
            ("ONE OPPORTUNITY AT A TIME", "the method must work for any subset of positions: one street rebuild, "
             "not all 832 at once"))):
        x = 60 + i * 500
        b += t(x, 648, h, 16, MUTED, "bold")
        b += para(x, 678, d, 460, 19)[0]
    save("v6_08_research_question", "The research question (v6)", "Rebuilt on the tree master plan, 21 Oct", b,
         "notes/topic_decision.md 9.4 (RQ v6), 9.6 (S1), 9.7 (scope); heat metric: section 8 and "
         "notes/decisions/heat_objective.md.")


def fig_sizing():
    w = pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv")
    p = w[w.is_plane]
    c = p.size_class.value_counts()
    mer = int((p.street.str.contains("Meridiana") & (p.size_class == "check")).sum())
    b = ('<image x="40" y="140" width="1000" height="680" preserveAspectRatio="xMidYMid meet" '
         'href="../../notes/figures/porta_sidewalk_classes.png"/>')
    tiles = [(TREE, f"{int((p.flag == 'ok').sum())} of {len(p)}", "plane positions with a façade-bounded sidewalk "
              "(measured façade to kerb)"),
             (TREE, f"{c['large']} + {c['medium']}", "keep a real choice: three large or three medium species"),
             (HEAT, f"{c['small'] + c['none']}", "forced to Pyrus (14) or to no tree (1) by the literal rule"),
             (MUTED, f"{c['check']}", f"medians, boulevards, plaza edges ({mer} on Av. Meridiana): no size filter, "
              "an ASSUMPTION")]
    for i, (col, big, small) in enumerate(tiles):
        y = 160 + i * 150
        b += rect(1080, y, 460, 132, col, rx=12, op=0.08) + rect(1080, y, 6, 132, col, rx=0)
        b += t(1106, y + 50, big, 34, col, "bold") + para(1106, y + 82, small, 410, 16)[0]
    save("v6_09_sizing_rule", "The sizing rule leaves the optimisation room",
         "Sidewalk width at each Porta plane, from the city's 1:1000 map; 2011 guide: < 2.5 m none, < 3.5 small, "
         "3.5–6 medium, > 6 m large", b,
         "databases/barcelona/porta_sidewalk_width.csv (scripts/porta_sidewalk_width.py; Mapa base topografic 1:1000, "
         "Ajuntament de Barcelona, CC BY 4.0); 20-tree check 18/20 correct (notes/sidewalk_width.md).")


if __name__ == "__main__":
    mi.OUT.mkdir(parents=True, exist_ok=True)
    fig_decided()
    fig_crowns()
    fig_rq()
    fig_sizing()
