"""Which species replaces a Porta plane tree? One tree position through eight stages (RM homework 1, format of a colleague's "plaza photo" map).

Content: notes/methodology.md, notes/topic_decision.md; state-of-the-art spans checked against the full texts in notes/lit/text
(Shaamala 2025, Mannucci 2025, SylvCiT, Davey API) and, for GreenInCities, RT_L02_notes.md + greenincities.eu/tools (14 Oct 2026);
"before computation" from databases/data_inventory_barcelona.md A1, D1. Output: slides/fig/08_plane_tree_map.svg + .png (2000x1250).
"""
import pathlib
from xml.sax.saxutils import escape
import make_infographics as mi

mi.W, mi.H = 2000, 1250
W, H = mi.W, mi.H
INK, MUTED, TEAL = "#1F3A44", "#6B7C85", "#EAF6F5"
CYAN, AMBER, PINK = "#3BB7D8", "#F0A020", "#E8567F"
X0, CW = 205, 214.6                      # first column x, column width
cx = lambda i: X0 + (i - 0.5) * CW       # centre of stage i (1-8)

STAGES = [  # name, question, unit at this stage, people?, body [(tag, text)]
    ("EXPERIENCE", "What is the topic without the tool?", "A Porta street, in summer and in storms", True,
     [("", "People walking under plane trees in Porta: shade in summer, wet pavement in autumn storms. Both hazards are above the city 60th percentile there."),
      ("", "The topic: which species replace the plane trees, and where.")]),
    ("REPRESENTATION", "What must the tree become computable?", "The tree as LiDAR and traits", False,
     [("SEEN", "height, crown diameter and crown base from leaf-on LiDAR (26 Sept 2021)"),
      ("INFERRED", "leaf area (LAI) from point density; shade as an elliptical crown; rain storage as a bucket"),
      ("LOST", "real LAI (proxy is uncalibrated), roots, cooling by transpiration")]),
    ("DATA", "Where does it come from, and what is missing?", "Inventory, LiDAR, storms, traits", False,
     [("", "ICGC LiDAR, street-tree inventory, PDISBA design storms, weather file, trait tables (BROT 2, 3TF)."),
      ("MISSING", "measured interception and LAI for Celtis, Melia, Tipuana, Jacaranda, Brachychiton (genus or leaf-habit values used); one district, one city.")]),
    ("MODEL", "What does it assume, and where is the bias?", "A shade score and a runoff score", False,
     [("", "Heat: sun exposure × crown shadow, opacity from LAI and month. Runoff: storage bucket (1.75 mm per LAI, calibrated on Anys and Weiler 2024) + SCS curve number."),
      ("", "The assumption tested: species and position pull heat and runoff in different directions.")]),
    ("INFRASTRUCTURE", "Who owns the models and the compute?", "Python core, Grasshopper, Ladybug", False,
     [("", "Own Python core (open code). Heat reference: Ladybug (open source). Infrared City is a possible engine; access to confirm."),
      ("", "Lock-in to name: Rhino/Grasshopper licence; Infrared City API if used.")]),
    ("TOOLS", "What does the designer actually touch?", "Ranked replacement layouts", True,
     [("", "Grasshopper: exchange files in, ranked layouts out (trade-off front)."),
      ("", "Later: a web app for non-technical users with the fast heat proxy."),
      ("OPEN", "how much weighting and palette setup the designer must do.")]),
    ("EVALUATION", "How would I know it works? Who notices when it fails?", "Scores checked against field data", True,
     [("", "Interception module vs Freiburg field data (Anys and Weiler 2024); today's trees (S0) as baseline; Florence as transfer test."),
      ("FAILS IF", "young trees mature late; storm beyond T = 10 yr; the LAI proxy is wrong."),
      ("OPEN", "who checks the ranking against reality.")]),
    ("WORLD", "What does it promise designers, and who decides?", "A species and a position per pit", True,
     [("", "Promise: quantified options instead of like-for-like replacement."),
      ("", "Risk: false precision from an uncalibrated LAI proxy."),
      ("", "Left behind: a Porta trait table, scenario results, open code.")]),
]
# state of the art: (label, [(first stage, last stage, caption)])
SOTA = [
    ("T1 Shaamala et al. 2025", [(4, 5, "Ant-colony optimisation of 42 trees × 4 species with Ladybug UTCI in Grasshopper; heat only, species by morphology"),
                                 (7, 7, "ENVI-met check of optimal vs suboptimal")]),
    ("T2 Mannucci et al. 2025", [(3, 3, "OpenStreetMap + USGS DEM"),
                                 (4, 6, "Ladybug UTCI/MOCI + Kangaroo particles + curve number; scenario testing for practitioners; no species traits, no optimisation"),
                                 (7, 7, "Ladybug vs ENVI-met at 4 points")]),
    ("P1 SylvCiT, Nicol et al. 2026", [(3, 3, "Montreal inventory + 3TF traits"),
                                       (4, 6, "Functional groups, diversity and carbon scores; open-source web recommender; no heat or runoff service yet"),
                                       (7, 7, "Diversity gains in 10 parks (simulated)")]),
    ("P2 Davey Tree Benefits Engine", [(3, 5, "Species, DBH and location in; i-Tree Eco benefits per tree (incl. avoided runoff) with growth; paid API, US averages outside supported areas; no placement")]),
    ("P3 GreenInCities 2024–27", [(1, 1, "Experiential mapping walks, neuro-urbanism"),
                                        (3, 4, "NDVI mapping; heatwave risk index (LAND); UTCI for non-humans (IES)"),
                                        (6, 8, "Co-design tools; co-monitoring reruns the baseline; Barcelona pilot in the Besòs area")]),
]
THESIS = ["Starts from the replacement decision, not from a model",
          "Side finding: what a LiDAR crown cannot tell",
          "Species trait gaps reported as a finding, with ranges",
          "Heat and runoff scored together; the trade-off is tested",
          "Open core, Ladybug cross-check, lock-in named",
          "Prototype: ranked layouts in Grasshopper; web app later",
          "Calibrated interception, S0 baseline, Florence transfer",
          "Quantified replacement options, limits stated"]
BEFORE = ["Being on the street", "Inventory: species, planting date, size class", "Open-data tree inventory (arbrat-viari)",
          "Master-plan rules: no species > 15%", "Municipal tree services", "Street projects, planting plans",
          "Inventory updates", "Plane share cut toward the 15% cap"]


def txt(x, y, s, size=13, fill=INK, weight="normal", anchor="start", italic=False, strike=False):
    extra = (' font-style="italic"' if italic else "") + (' text-decoration="line-through"' if strike else "")
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'


def wrap(x, y, s, width, size=13, lh=1.28, **k):
    return mi.para(x, y, s, width, size, lh, **k)


def tree(x, y, k=1.0):
    """Little plane-tree icon standing on (x, y)."""
    return (f'<rect x="{x - 2 * k:.0f}" y="{y - 14 * k:.0f}" width="{4 * k:.0f}" height="{14 * k:.0f}" fill="#6B4F2A"/>'
            f'<circle cx="{x:.0f}" cy="{y - 24 * k:.0f}" r="{13 * k:.0f}" fill="{mi.TREE}"/>'
            f'<circle cx="{x - 8 * k:.0f}" cy="{y - 19 * k:.0f}" r="{8 * k:.0f}" fill="{mi.TREE}"/>'
            f'<circle cx="{x + 8 * k:.0f}" cy="{y - 19 * k:.0f}" r="{8 * k:.0f}" fill="{mi.TREE}"/>')


def hazards(x, y):
    """The two hazards of the thesis: heat (sun) and runoff (drop), in the figure colours."""
    sun = "".join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + 13 * c:.0f}" y2="{y + 13 * d:.0f}" stroke="{mi.HEAT}" stroke-width="2"/>'
                  for c, d in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, -.7), (.7, -.7), (-.7, .7)))
    drop = (f'<path d="M{x + 160:.0f},{y - 9:.0f} q9,12 0,17 q-9,-5 0,-17 z" fill="{mi.RAIN}"/>')
    return (sun + f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{mi.HEAT}"/>' + txt(x + 18, y + 5, "heat in summer", 13, mi.HEAT, "bold")
            + drop + txt(x + 174, y + 5, "runoff in storms", 13, mi.RAIN, "bold"))


def build():
    b = [txt(90, 62, "Which species replaces a Porta plane tree?", 40, INK, "bold"),
         txt(90, 96, "One plane-tree position due for replacement in Porta (Nou Barris, Barcelona), followed through eight stages and back to the street. "
                     "The dark lines show the state of the art; the pink line, this thesis. Cyan stages involve people, amber stages happen in the machine.", 15, MUTED)]
    b.append(f'<line x1="90" y1="128" x2="1915" y2="128" stroke="#D5DBDE"/>')
    b.append(txt(90, 152, "CONTEXT", 11, MUTED) + txt(160, 152,
              "Plane trees are replaced one by one · Heat and pluvial runoff both matter in Porta · Species choice rarely uses traits (SylvCiT has no heat or runoff service yet)", 14, INK))
    b.append(hazards(1300, 148))
    b.append('<line x1="90" y1="176" x2="1915" y2="176" stroke="#D5DBDE"/>')
    body_h = 1000
    for i, (name, q, unit, people, body) in enumerate(STAGES, 1):
        x = X0 + (i - 1) * CW
        b.append(f'<rect x="{x + 2:.0f}" y="198" width="{CW - 4:.0f}" height="{body_h - 198 + 24}" fill="{TEAL}"/>')
        b.append(txt(x + 22, 218, f"0{i}", 11, CYAN if people else AMBER))
        b.append(txt(x + 22, 238, name, 18, INK, "bold"))
        s, _ = wrap(x + 22, 256, q, CW - 36, 12, italic=True, fill=MUTED)
        b.append(s)
        s, _ = wrap(x + 22, 314, unit, CW - 36, 13.5, weight="bold")
        b.append(s)
        y = 384
        for tag, text in body:
            if tag:
                b.append(txt(x + 22, y, tag, 10, MUTED, "bold"))
                y += 15
            st = dict(fill=MUTED) if tag == "LOST" else {}
            s, h = wrap(x + 22, y, text, CW - 40, 12.5, **st)
            if tag == "LOST":
                s = s.replace("<text ", '<text text-decoration="line-through" ')
            b.append(s)
            y += h + 10
    # photo path, loop-back rectangle, nodes
    b.append(f'<rect x="55" y="356" width="1895" height="{1134 - 356}" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="10 9"/>')
    b.append(f'<line x1="55" y1="356" x2="1950" y2="356" stroke="{INK}" stroke-width="5"/>')
    b.append(tree(130, 356, 1.4))
    for i, st in enumerate(STAGES, 1):
        b.append(f'<circle cx="{cx(i):.0f}" cy="356" r="9" fill="#fff" stroke="{CYAN if st[3] else AMBER}" stroke-width="4"/>')
    # state of the art
    y0 = 666
    b.append(txt(72, y0 - 16, "STATE OF THE ART · solid where a paper covers a stage, dotted where it passes without", 11, MUTED))
    for r, (lab, segs) in enumerate(SOTA):
        y = y0 + 22 + r * 50
        b.append(txt(72, y - 18, lab[:2], 11.5, INK, "bold") + txt(96, y - 18, lab[3:], 11.5, INK))
        b.append(f'<line x1="224" y1="{y}" x2="1905" y2="{y}" stroke="#C9D1D4" stroke-dasharray="2 4"/>')
        for a, z, cap in segs:
            xa, xz = X0 + (a - 1) * CW + 20, X0 + z * CW - 20
            b.append(f'<line x1="{xa:.0f}" y1="{y}" x2="{xz:.0f}" y2="{y}" stroke="{INK}" stroke-width="2.5"/>')
            s, _ = wrap(xa, y - 24, cap, xz - xa, 11, fill=INK)
            b.append(s)
    # this thesis
    yt = y0 + 22 + 5 * 50 + 6
    b.append(txt(72, yt + 34, "This thesis", 12, PINK, "bold"))
    for i, s_ in enumerate(THESIS, 1):
        s, _ = wrap(cx(i) - CW / 2 + 20, yt + 4, s_, CW - 36, 11.5, weight="bold", fill=PINK)
        b.append(s)
    yl = yt + 66
    b.append(f'<line x1="224" y1="{yl}" x2="1905" y2="{yl}" stroke="{PINK}" stroke-width="5"/>')
    # before computation
    yb = yl + 56
    b.append(txt(72, yb - 14, "BEFORE COMPUTATION · the same stages, done by hand", 11, MUTED))
    b.append(f'<line x1="224" y1="{yb + 14}" x2="1905" y2="{yb + 14}" stroke="#9AA9AF" stroke-width="2" stroke-dasharray="9 7"/>')
    for i, s_ in enumerate(BEFORE, 1):
        b.append(f'<circle cx="{cx(i):.0f}" cy="{yb + 14}" r="6" fill="#fff" stroke="#9AA9AF" stroke-width="2"/>')
        b.append(wrap(cx(i) - CW / 2 + 20, yb + 42, s_, CW - 36, 12, fill=MUTED)[0])
    b.append(txt(1000, 1156, "Back to the street: the new tree shades and drains the same place, or it does not", 15, INK, "bold", "middle"))
    # key
    b.append(tree(668, 1160, 1.0))
    ky = 1212
    b.append(txt(90, ky - 24, "KEY", 10, MUTED))
    items = [("line", INK, 5, "", "the tree's path"), ("line", INK, 5, "10 7", "back to the street"), ("dot", CYAN, 0, "", "stage with people"),
             ("dot", AMBER, 0, "", "stage in the machine"), ("line", INK, 2.5, "", "a paper covers this stage"),
             ("line", "#C9D1D4", 2, "2 4", "passes without covering it"), ("line", PINK, 5, "", "this thesis: what is new"),
             ("line", "#9AA9AF", 2, "9 7", "before computation")]
    x = 90
    for kind, col, sw, dash, lab in items:
        if kind == "line":
            d = f' stroke-dasharray="{dash}"' if dash else ""
            b.append(f'<line x1="{x}" y1="{ky}" x2="{x + 44}" y2="{ky}" stroke="{col}" stroke-width="{sw}"{d}/>')
        else:
            b.append(f'<circle cx="{x + 12}" cy="{ky}" r="8" fill="#fff" stroke="{col}" stroke-width="3.5"/>')
        w = 56 if kind == "line" else 28
        b.append(txt(x + w, ky + 4, lab, 12, MUTED))
        x += w + len(lab) * 6.6 + 34
    b.append(txt(90, H - 8, "Sources: notes/methodology.md, notes/topic_decision.md, notes/lit/literature_matrix.csv (Shaamala, Mannucci), prior_art_matrix.csv (SylvCiT), "
                            "Davey API usage document, RT L02 notes + greenincities.eu (GreenInCities), data_inventory_barcelona.md A1, D1 (before computation).", 10, MUTED))
    return "".join(b)


if __name__ == "__main__":
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{mi.FONT}">'
           f'<rect width="{W}" height="{H}" fill="#fff"/>{build()}</svg>')
    p = mi.OUT / "08_plane_tree_map.svg"
    mi.OUT.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
    mi.to_png(p)
    print("wrote", p.relative_to(mi.ROOT))
