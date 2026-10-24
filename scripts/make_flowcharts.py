"""Methodology flowcharts for the 10 Nov session, in the grammar of the tutor's reference (IAAC Internet of Buildings,
slides/flowchart_reference_iob.md): phase columns with one-word headers, icons in circles, one colour per variable,
curved connectors, one optimisation loop, almost no text. Deck palette and fonts from make_infographics.py.
Content: notes/topic_decision.md §10 (v7, RQ v7, decisions 24 Oct), notes/methodology.md, notes/citywide_plan.md.
Output: slides/fig_v7/flow_*.svg + .png. Run from scripts/: python make_flowcharts.py
"""
import make_infographics as mi
from make_infographics import t, rect, save, ROOT, INK, MUTED, GRID, BG, HEAT, RAIN, TREE, WARN

mi.OUT = ROOT / "slides/fig_v7"
mi.OUT.mkdir(exist_ok=True)
WHITE = "#FFFFFF"


# ---- drawing grammar
def head(x, s):
    return t(x, 185, s.upper(), 17, MUTED, "bold", "middle")


def box(cx, cy, label, color, w=170, h=56, sub=None):
    s = rect(cx - w / 2, cy - h / 2, w, h, color, rx=6)
    if sub:
        return s + t(cx, cy - 3, label, 17, WHITE, "bold", "middle") + t(cx, cy + 17, sub, 13, WHITE, anchor="middle")
    return s + t(cx, cy + 6, label, 17, WHITE, "bold", "middle")


def outline(cx, cy, label, color, w=200, h=64, sub=None):
    s = rect(cx - w / 2, cy - h / 2, w, h, BG, rx=10, stroke=color)
    if sub:
        return s + t(cx, cy - 4, label, 16, color, "bold", "middle") + t(cx, cy + 17, sub, 13, MUTED, anchor="middle")
    return s + t(cx, cy + 6, label, 16, color, "bold", "middle")


def curve(x1, y1, x2, y2, color=MUTED, dash=""):
    mx = (x1 + x2) / 2
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1:.0f},{y1:.0f} C{mx:.0f},{y1:.0f} {mx:.0f},{y2:.0f} {x2:.0f},{y2:.0f}" fill="none" '
            f'stroke="{color}" stroke-width="1.8"{d} marker-end="url(#arr)"/>')


def vline(x, y1, y2, color, label=None):
    s = f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#arr)"/>'
    return s + (t(x + 8, (y1 + y2) / 2, label, 13, color) if label else "")


def disc(cx, cy, r=38):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'


def caption(cx, cy, s, color=INK, size=16):
    return t(cx, cy, s, size, color, "bold", "middle")


# icons (drawn inside a white disc of radius 38 centred at cx, cy)
def i_heat(cx, cy):
    return (disc(cx, cy) + f'<rect x="{cx - 5}" y="{cy - 24}" width="10" height="34" rx="5" fill="none" stroke="{HEAT}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy + 14}" r="9" fill="{HEAT}"/><line x1="{cx}" y1="{cy - 8}" x2="{cx}" y2="{cy + 10}" stroke="{HEAT}" stroke-width="4"/>')


def i_rain(cx, cy):
    s = disc(cx, cy) + "".join(f'<circle cx="{cx + dx}" cy="{cy - 8 + dy}" r="{r}" fill="{RAIN}"/>'
                               for dx, dy, r in ((-10, 2, 9), (2, -4, 12), (13, 3, 8)))
    s += f'<rect x="{cx - 19}" y="{cy - 4}" width="40" height="10" rx="5" fill="{RAIN}"/>'
    return s + "".join(f'<line x1="{cx + dx}" y1="{cy + 12}" x2="{cx + dx - 4}" y2="{cy + 22}" stroke="{RAIN}" stroke-width="3"/>'
                       for dx in (-10, 0, 10))


def i_tree(cx, cy, color=TREE):
    return (disc(cx, cy) + f'<rect x="{cx - 3}" y="{cy + 2}" width="6" height="22" fill="{INK}"/>'
            f'<circle cx="{cx}" cy="{cy - 6}" r="17" fill="{color}"/>')


def i_layers(cx, cy):
    s = ""
    for k, c in enumerate((RAIN, HEAT, TREE)):        # bottom to top, as the IoB "results" stack
        y = cy + 18 - 14 * k
        s += f'<path d="M{cx - 42},{y} L{cx},{y - 18} L{cx + 42},{y} L{cx},{y + 18} Z" fill="{c}" stroke="{BG}" stroke-width="2"/>'
    return s


def i_area(cx, cy):
    return (disc(cx, cy) + f'<path d="M{cx - 22},{cy - 10} L{cx + 2},{cy - 22} L{cx + 22},{cy - 4} L{cx + 12},{cy + 20} '
            f'L{cx - 18},{cy + 16} Z" fill="{WARN}" fill-opacity="0.25" stroke="{WARN}" stroke-width="2.5" stroke-dasharray="5 3"/>'
            + "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="4" fill="{TREE}"/>' for dx, dy in ((-6, -4), (6, 4), (-4, 9))))


def i_check(cx, cy):
    s = disc(cx, cy) + f'<rect x="{cx - 15}" y="{cy - 20}" width="30" height="40" rx="3" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s += "".join(f'<line x1="{cx - 8}" y1="{cy - 10 + 9 * k}" x2="{cx + 8}" y2="{cy - 10 + 9 * k}" stroke="{INK}" stroke-width="2"/>'
                 for k in range(3))
    return s + f'<path d="M{cx + 2},{cy + 16} l6,6 l12,-14" fill="none" stroke="{TREE}" stroke-width="4"/>'


def i_radar(cx, cy):
    import math
    pts = lambda r: " ".join(f"{cx + r[k] * math.sin(2 * math.pi * k / 6):.0f},{cy - r[k] * math.cos(2 * math.pi * k / 6):.0f}"
                             for k in range(6))
    s = disc(cx, cy) + f'<polygon points="{pts([28] * 6)}" fill="none" stroke="{GRID}" stroke-width="1.5"/>'
    s += f'<polygon points="{pts([22, 14, 24, 12, 20, 16])}" fill="{HEAT}" fill-opacity="0.35" stroke="{HEAT}" stroke-width="2"/>'
    return s + f'<polygon points="{pts([14, 24, 12, 22, 15, 24])}" fill="{RAIN}" fill-opacity="0.35" stroke="{RAIN}" stroke-width="2"/>'


def loop(x1, x2, y, label):
    """The one feedback loop of the figure: from x2 back to x1, above the row at y."""
    top = y - 75
    return (f'<path d="M{x2},{y - 42} L{x2},{top} L{x1},{top} L{x1},{y - 44}" fill="none" stroke="{INK}" stroke-width="2" '
            f'marker-end="url(#arr)"/>' + t((x1 + x2) / 2, top - 10, label, 16, INK, "bold", "middle"))


# ---- 0. Overview
def flow_overview():
    X = [110, 330, 560, 760, 990, 1240, 1480]
    b = "".join(head(x, h) for x, h in zip(X, ("Focus", "Data", "City screening", "Project area", "Design",
                                               "Evaluate", "Validation")))
    y0 = 470
    b += i_heat(X[0], 360) + caption(X[0], 422, "Heat stress", HEAT)
    b += i_rain(X[0], 560) + caption(X[0], 622, "Pluvial floods", RAIN)
    data = [("Tree inventory", TREE), ("LiDAR 2021–22", TREE), ("Sidewalk width", WARN),
            ("DTM + hotspots", RAIN), ("Hot day · storms", HEAT)]
    ys = [290, 380, 470, 560, 650]
    for (lab, c), y in zip(data, ys):
        b += box(X[1], y, lab, c, 180, 50)
    for fy, dy in ((360, 380), (360, 650), (560, 560), (560, 650)):   # heat → LiDAR, hot day; floods → DTM, storms
        b += curve(X[0] + 40, fy, X[1] - 92, dy, GRID)
    b += i_layers(X[2], y0 - 25) + caption(X[2], y0 + 40, "Indicators per tree") + t(X[2], y0 + 62, "+ replacement priority", 14, MUTED, anchor="middle")
    for y in ys:
        b += curve(X[1] + 92, y, X[2] - 46, y0 - 25, GRID)
    b += i_area(X[3], y0 - 25) + caption(X[3], y0 + 40, "Draw an area") + t(X[3], y0 + 62, "any street, any district", 14, MUTED, anchor="middle")
    b += curve(X[2] + 46, y0 - 25, X[3] - 40, y0 - 25)
    b += box(X[4], 380, "Replacement", TREE, 180, 56, "dying planes · works")
    b += box(X[4], 560, "Additions", TREE, 180, 56, "free planting spots")
    b += curve(X[3] + 40, y0 - 25, X[4] - 92, 380) + curve(X[3] + 40, y0 - 25, X[4] - 92, 560)
    b += outline(X[4], 735, "City rules", WARN, 230, 70, "15% cap · sidewalk size · S1a mix")
    b += vline(X[4], 698, 592, WARN)
    for k, (lab, c) in enumerate((("Heat", HEAT), ("Runoff", RAIN), ("Canopy", TREE))):
        y = 360 + 110 * k
        b += box(X[5] - 70, y, lab, c, 110, 44)
        b += curve(X[4] + 92, 380, X[5] - 127, y, GRID) + curve(X[4] + 92, 560, X[5] - 127, y, GRID)
    b += i_radar(X[5] + 70, y0 - 25) + t(X[5] + 70, y0 + 34, "S0 · S1a", 14, MUTED, anchor="middle")
    b += t(X[5] + 70, y0 + 52, "R · A · R+A", 14, MUTED, anchor="middle")
    for k in range(3):
        b += curve(X[5] - 15, 360 + 110 * k, X[5] + 30, y0 - 25, GRID)
    b += loop(X[4], X[5] - 70, 360 - 22 + 44, "Optimisation")
    b += i_check(X[6], y0 - 25) + caption(X[6], y0 + 40, "Porta → Sant Antoni")
    b += curve(X[5] + 110, y0 - 25, X[6] - 40, y0 - 25)
    b += t(800, 815, "Built and validated on Porta (Nou Barris); the screening layer and the project tool extend it to "
           "the whole city.", 17, MUTED, anchor="middle")
    save("flow_00_overview", "Methodology", "Which species replace Barcelona's plane trees, and where to add new ones: "
         "scored on heat, runoff and canopy", b,
         "notes/topic_decision.md §10 (problem v7, RQ v7, scenarios and decisions of 24 Oct); notes/methodology.md; "
         "notes/citywide_plan.md. S0 today · S1a the city's rule (2026 mix) · R replacement · A additions · R+A both.")


# ---- generic module figure: phase columns, a few nodes per column, curved links
def module(name, title, subtitle, cols, links, note, source, side=None):
    X = [150 + i * (1300 / max(1, len(cols) - 1)) for i in range(len(cols))]
    pos, b, nb = {}, "", ""                              # links are drawn under the nodes
    for x, (hd, nodes) in zip(X, cols):
        b += head(x, hd)
        n = len(nodes)
        for k, nd in enumerate(nodes):
            y = 470 + (k - (n - 1) / 2) * (140 if any(m[1] == "icon" for m in nodes) else 105)
            key, kind = nd[0], nd[1]
            if kind == "icon":
                nb += nd[2](x, y) + caption(x, y + 62, nd[3], nd[4] if len(nd) > 4 else INK)
                pos[key] = (x, y, 42)
            else:
                lab, c, sub = nd[2], nd[3], (nd[4] if len(nd) > 4 else None)
                w = max(200, 0.56 * 13 * len(sub or "") + 24, 0.6 * 17 * len(lab) + 24)
                nb += box(x, y, lab, c, w, 58 if sub else 50, sub)
                pos[key] = (x, y, w / 2 + 2)
    for a, c in links:
        (x1, y1, w1), (x2, y2, w2) = pos[a], pos[c]
        b += curve(x1 + w1, y1, x2 - w2 - 4, y2, GRID)
    b += nb
    if side:                                            # one side input, IoB "catalogue" style
        key, lab, sub, color = side
        x, y, _ = pos[key]
        b += outline(x, 760, lab, color, 250, 70, sub) + vline(x, 723, y + 34, color)
    b += t(800, 840 - 10, note, 16, MUTED, anchor="middle")
    save(name, title, subtitle, b, source)


def flow_screening():
    module("flow_01_screening", "1 · City screening", "Indicators for every street-tree position, computed once, district by district",
           [("Data", [("inv", "box", "Tree inventory", TREE, "Open Data BCN"), ("lid", "box", "LiDAR", TREE, "ICGC 2021–22"),
                      ("sw", "box", "Sidewalk width", WARN, "1:1000 map"), ("dtm", "box", "DTM + hotspots", RAIN, "LiDAR · Atlas")]),
            ("Per tree", [("crown", "box", "Crown · LAI", TREE), ("size", "box", "Size class", WARN),
                          ("shade", "box", "Shade potential", HEAT), ("flow", "box", "Water convergence", RAIN)]),
            ("Priority", [("vig", "box", "Crown vigour", TREE, "vs same species"), ("ndvi", "box", "NDVI change", TREE),
                          ("age", "box", "Age · trunk class", MUTED)]),
            ("Output", [("map", "icon", i_layers, "City layer"), ("prio", "icon", i_tree, "Replacement priority", TREE)])],
           [("inv", "crown"), ("lid", "crown"), ("lid", "shade"), ("sw", "size"), ("dtm", "flow"), ("inv", "age"),
            ("crown", "vig"), ("crown", "map"), ("size", "map"), ("shade", "map"), ("flow", "map"), ("vig", "prio"),
            ("ndvi", "prio"), ("age", "prio")],
           "Priority is a proxy (no open tree-health data): tested against trees removed between inventory snapshots.",
           "notes/citywide_plan.md §1–3; scripts/bcn_lidar_porta.py; scripts/porta_sidewalk_width.py; notes/sidewalk_width.md.")


def flow_heat():
    module("flow_02_heat", "2 · Heat", "Fast proxy inside the loop, full UTCI on the final layouts",
           [("Climate", [("epw", "icon", i_heat, "Hot design day", HEAT)]),
            ("Sun", [("sun", "box", "Sun positions", HEAT, "12–17 h"), ("bld", "box", "Buildings", MUTED, "LiDAR heights")]),
            ("Proxy", [("prox", "box", "Effective shade", HEAT, "shadow × (1 − τ), τ = e^(−0.5 LAI)")]),
            ("UTCI", [("t1", "box", "Ladybug Tier 1", HEAT, "final layouts"), ("t2", "box", "Honeybee Tier 2", HEAT, "spot check")]),
            ("Output", [("out", "box", "Mean UTCI", HEAT, "12–17 h, sunlit sidewalks")])],
           [("epw", "sun"), ("epw", "t1"), ("sun", "prox"), ("bld", "prox"), ("prox", "t1"), ("prox", "t2"), ("t1", "out"), ("t2", "out")],
           "Winter sun access is scored the same way on a January day: shade there is a cost.",
           "notes/methodology.md §5; notes/topic_decision.md §8 (metric), §10.5 row 4; shade_sponge/README.md (heat.py).",
           side=("prox", "Crown model", "LiDAR crowns · leaf calendar", TREE))


def flow_runoff():
    module("flow_03_runoff", "3 · Runoff", "Event runoff on a 1 m grid, routed to the flood hotspots",
           [("Storm", [("st", "icon", i_rain, "PDISBA design storm", RAIN)]),
            ("Canopy", [("int", "box", "Interception", RAIN, "s · LAI, bucket")]),
            ("Surface", [("cn", "box", "SCS-CN", RAIN, "sealed · pervious · roofs")]),
            ("Routing", [("rt", "box", "Flow routing", RAIN, "DTM + buildings")]),
            ("Output", [("tot", "box", "Total runoff", RAIN, "vs Δmin = 91 m³"), ("hot", "box", "Hotspot runoff", RAIN, "optimised")])],
           [("st", "int"), ("int", "cn"), ("cn", "rt"), ("rt", "tot"), ("rt", "hot")],
           "T2-60 is the headline storm; T1 and T10 are reported. Extreme events are outside what street trees can affect.",
           "notes/methodology.md §4b; notes/decisions/runoff_metric_sensitivity.md §10 (Δmin); notes/topic_decision.md §8, §10.5 row 5.",
           side=("int", "Calibration", "s = 1.75 mm/LAI · Anys & Weiler 2024", WARN))


def flow_design():
    module("flow_04_design", "4 · Design", "Inside a project area: which species at which position, within the city's rules",
           [("Area", [("area", "icon", i_area, "Project area", WARN)]),
            ("Positions", [("rep", "box", "Planes to replace", TREE, "by priority"), ("add", "box", "Free spots", TREE, "sidewalk ≥ 2.5 m, spacing")]),
            ("Feasible", [("feas", "box", "Species per spot", WARN, "size class · catalogue")]),
            ("Optimise", [("opt", "box", "Multi-objective", INK, "weighted sum → NSGA-II")]),
            ("Layouts", [("r", "box", "R", TREE, "replacement"), ("a", "box", "A", TREE, "additions"), ("ra", "box", "R + A", TREE, "both")])],
           [("area", "rep"), ("area", "add"), ("rep", "feas"), ("add", "feas"), ("feas", "opt"), ("opt", "r"), ("opt", "a"), ("opt", "ra")],
           "Each layout is compared with S1a (the city's rule) on the same positions, and with today (S0).",
           "notes/topic_decision.md §9.7, §10.4–10.6; notes/tree_master_plan.md §5 (sizing rule, spacing); notes/methodology.md §6.",
           side=("feas", "City rules", "15% cap (city-wide headroom) · S1a mix", WARN))


def flow_validation():
    module("flow_05_validation", "5 · Validation", "Each module checked against something it was not fitted to",
           [("Module", [("h", "icon", i_heat, "Heat", HEAT), ("w", "icon", i_rain, "Runoff", RAIN), ("p", "icon", i_tree, "Priority", TREE)]),
            ("Check", [("h1", "box", "Proxy vs Ladybug", HEAT, "same layouts"), ("h2", "box", "Ladybug vs ENVI-met", HEAT, "Mannucci et al. 2025"),
                       ("w1", "box", "Interception data", RAIN, "Freiburg, Anys & Weiler 2024"), ("p1", "box", "Removed trees", TREE, "inventory snapshots")]),
            ("Transfer", [("tr", "box", "Sant Antoni", INK, "same city, flood-dominant")]),
            ("Verdict", [("v", "icon", i_check, "Verdict per hypothesis")])],
           [("h", "h1"), ("h", "h2"), ("w", "w1"), ("p", "p1"), ("h1", "tr"), ("h2", "tr"), ("w1", "tr"), ("p1", "tr"), ("tr", "v")],
           "Thresholds are fixed before the runs: a difference below what the model resolves is reported as \"not resolved\".",
           "notes/methodology.md §4b, §5; notes/decisions/hypothesis_tests.md; notes/citywide_plan.md §3–4.")


if __name__ == "__main__":
    flow_overview()
    flow_screening()
    flow_heat()
    flow_runoff()
    flow_design()
    flow_validation()
