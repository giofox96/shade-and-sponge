"""Methodology section for the 17 Nov tutor session: the one-page method (v9), the HiGHS slide, "why replace" and the
declared assumptions (native, from notes/tutor_feedback_10nov.md §2 and databases/barcelona/sensitivity_capture_margin.csv),
then the method backups of the
10 Nov deck (design, heat, runoff, screening, optimiser steps, validation). Figures from make_flowcharts_v9.py and
make_flowcharts.py, placed as in make_deck_editable.py (figure title and footer cropped, native title and sources).
Output: slides/methodology_17nov.pptx. Run from scripts/: python make_deck_method_17nov.py
"""
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN
from make_deck_editable import fig_slide, rgb, tint, text, box, head, source, W, H, M, BG, ROOT, INK, MUTED, TREE, RAIN, WARN, HEAT

SAY = {
    "main": "Here is the method on one page. Two hazards, heat and pluvial flooding. The data are open: the tree inventory, the "
            "LiDAR for crowns and buildings, the terrain model, the flood hotspots, sidewalks with their street objects, the hot "
            "day and the design storms. The terrain is what routes the storm water to the hotspots, and in the tool you now see "
            "it in 3D. A screening layer gives indicators for every tree. Then a designer draws a project area and says, tree by "
            "tree, what stays, what moves and what is replaced. Two branches: replacing the trees the project removes, and adding "
            "trees in free spots, always inside the city's rules. Every layout is scored on heat, runoff and canopy, against "
            "today and against the city's practice. The species choice is one exact optimisation, HiGHS, on the next slide. "
            "Validation: Porta first, then Sant Antoni, Mataró and Florence.",
    "highs": "HiGHS is the solver that picks every species. It needs three things. A score table: how good each species is at "
             "each position, for shade, winter sun and water held. In Porta that is 832 positions by 7 species. Then the city's "
             "rules: one species per position, only species that fit the sidewalk, and no species above its 15% cap. Every "
             "layout that obeys the rules is a point inside this shape, and the best one is always a corner. HiGHS finds the "
             "highest corner and stops with a proof that no corner is higher. In the small example, picking "
             "the best species everywhere would plant A three times and break the cap. HiGHS keeps A where its lead is largest "
             "and gives position 2 to B, losing only 0.1. A genetic or ant-colony search would obey the rules too, but would never "
             "know if it had found the best. HiGHS does it for Porta in 0.06 seconds, for the whole city in about ten, and the "
             "answer is always whole trees.",
    "why": "Angelos, you said it was too bold that every tree in a project area is felled. You were right, and the city's own "
           "documents say so. For replacing a plane or an elm, Parcs i Jardins lists five reasons, and street works come last: a "
           "project is an occasion to replace a tree that already qualifies. The inventory agrees. Of almost eleven thousand "
           "replacements since 2018, almost half stand alone, and only eight percent come in groups of ten or more. Even "
           "around those groups, about half of the trees stay. So the tool no longer assumes anything: the designer marks each "
           "tree as keep, move or replace, keep is the default, and 'replace all' is only the worst case. One thing I declare: "
           "layouts compare mature crowns, which favours replacing; in the first years a healthy tree always wins.",
    "assume": "Here are the assumptions, each with its basis and status. Green ones are tested: which trees leave is now an "
              "input, the free spots are a range, the cap was also run city-wide, interception was tested from 0.83 to 1.75, and "
              "the two that had no source, the hotspot capture distance and the façade clearance, were tested this week. Blue "
              "ones come from the literature with a range. Ochre ones are declared: underground services, the curve numbers and "
              "mature crown sizes. Where tested, the ranking of the layouts holds: with a capture distance of 50 or 200 metres "
              "and with one or two metres of extra façade clearance, the method stays about eight points of summer shade ahead "
              "of the city's practice, and no worse on hotspot runoff.",
}

def why_replace(s):
    head(s, "Why replace? Street works come last in the city's own order",
         "Barcelona replaces trees mostly one by one: the tool takes the trees that must go as an input, it does not choose them")
    cw = (W - 2 * M - 2 * 0.35) / 3
    x = [M + k * (cw + 0.35) for k in range(3)]
    for k, (hd, c) in enumerate((("The city's order for replacing a plane or elm", INK), ("What the city actually did, 2018–2026", TREE),
                                 ("So the tool", WARN))):
        box(s, x[k], 1.55, cw, 4.75, tint(c, 0.08))
        text(s, x[k] + 0.3, 1.72, cw - 0.6, 0.5, hd, 16, c, True)
    order = ["Road-safety problems", "Dead", "Unrecoverable or declining", "To unify a stretch", "Taking advantage of street works"]
    for k, o in enumerate(order):
        y = 2.35 + k * 0.68
        last = k == 4
        box(s, x[0] + 0.3, y, cw - 0.6, 0.55, tint(HEAT, 0.18) if last else "#FFFFFF", line=HEAT if last else None)
        text(s, x[0] + 0.45, y + 0.1, cw - 0.9, 0.4, [[(f"{k + 1}  ", {"bold": True, "color": HEAT if last else MUTED}),
                                                       (o, {"bold": last})]], 14, INK)
    text(s, x[0] + 0.3, 5.75, cw - 0.6, 0.5, "A project is an occasion to replace a tree that already qualifies.", 13, MUTED)
    stats = [("46.8%", "of 10,976 replacements stand alone"), ("8.1%", "in groups of ten or more: 57 groups in 8.5 years"),
             ("53%", "of the trees around those groups are kept (median; an upper bound)")]
    for k, (big, small) in enumerate(stats):
        y = 2.35 + k * 1.2
        text(s, x[1] + 0.3, y, cw - 0.6, 0.6, big, 32, TREE, True)
        text(s, x[1] + 0.3, y + 0.6, cw - 0.6, 0.5, small, 14, INK)
    tool = [[("Each tree: ", {"bold": True}), ("keep (default) · move · replace", {})],
            [("“Replace all” ", {"bold": True}), ("stays as one button: the worst case, not the rule", {})],
            [("Life cycle: ", {"bold": True}), ("layouts compare mature crowns, which favours replacing. "
              "A healthy tree always wins the first years; the ≈ 10-year check shows it", {})]]
    text(s, x[2] + 0.3, 2.35, cw - 0.6, 3.6, tool, 15, INK)
    source(s, "Parcs i Jardins, Arbrat viari: selecció d'espècies (rev. 2004) §2.4.2; Pla de gestió de l'arbrat viari de Barcelona "
              "(2005) §3.4.2; Open Data BCN, 35 quarterly street-tree inventories 2018–2026.")


def _sens():
    """Result text for the two sensitivity rows, from the OMEN run (or 'running' if the table is not there yet)."""
    f = ROOT / "databases/barcelona/sensitivity_capture_margin.csv"
    if not f.exists():
        return "running", "running"
    d = pd.read_csv(f)
    gap = d.opt_summer_pct_today - d.s1b_summer_pct_today
    c, m = d[d.margin_m == 0], d[d.margin_m > 0]
    alt = c[c.capture_m != 100]
    lo, hi = gap[alt.index].min(), gap[alt.index].max()
    cap_txt = (f"50 / 200 m: +{lo:.1f}" + (f" to +{hi:.1f}" if f"{lo:.1f}" != f"{hi:.1f}" else "") + " pts summer shade vs city; "
               f"hotspot {alt.opt_hot_vs_s1b_pct.max():+.1f}%")
    mar_txt = "+1 / +2 m: " + " / ".join(f"+{gap[i]:.1f}" for i in m.index) + " pts summer shade vs city"
    return cap_txt, mar_txt


def assumptions(s):
    head(s, "Declared assumptions", "Each one sourced, tested, or stated as an assumption")
    cap_txt, mar_txt = _sens()
    rows = [("Which trees leave", "set per tree: keep · move · replace", "City practice: 47% replaced alone", "tested", "measured"),
            ("Free planting spots", "152 in Porta (range 116–232)", "2011 guide, lamps at half its distance", "tested", "range"),
            ("Underground services", "not modelled", "No open data", "declared", "spots are an upper bound"),
            ("15% species cap", "per study area", "Plan: city-wide", "tested", "city-wide run"),
            ("Interception", "1.75 mm per unit LAI, all species", "Anys & Weiler 2024", "tested", "0.83–1.75: runoff change < 1%"),
            ("Hotspot capture distance", "100 m", "None (stand-in for sewer inlets)", "tested" if cap_txt != "running" else "declared", cap_txt),
            ("Crown–façade clearance", "no margin", "None", "tested" if mar_txt != "running" else "declared", mar_txt),
            ("Curve numbers", "98 sealed · 74 pervious", "TR-55, soil group C", "declared", ""),
            ("Leafless crowns", "opacity 0.35 · storage 0.5", "McPherson 1984; Heisler 1982; Herbst et al. 2008", "sourced", "ranges 0.25–0.54 · 0.3–0.7"),
            ("Crown size compared", "mature (Porta LiDAR median)", "Favours replacing", "declared", "≈ 10-year check in the app"),
            ("Design days", "15 Jul 12–17 h · 15 Jan 10–15 h", "Window decided; days assumed", "tested", "21 Dec, 15 Feb variants")]
    col = {"tested": TREE, "sourced": RAIN, "declared": WARN}
    xs, ws = [M, M + 2.55, M + 5.55, M + 8.75, M + 9.95], [2.45, 2.9, 3.1, 1.1, 2.3]
    for x, w, h in zip(xs, ws, ("Assumption", "Value", "Basis", "Status", "Range or result")):
        text(s, x, 1.5, w, 0.3, h.upper(), 11, MUTED, True)
    rh = 0.43
    for k, (a, v, b, st, res) in enumerate(rows):
        y = 1.85 + k * rh
        if k % 2 == 0:
            box(s, M - 0.1, y - 0.05, W - 2 * M + 0.2, rh, tint(MUTED, 0.06), radius=0)
        text(s, xs[0], y + 0.03, ws[0], rh, a, 13, INK, True)
        text(s, xs[1], y + 0.03, ws[1], rh, v, 13, INK)
        text(s, xs[2], y + 0.03, ws[2], rh, b, 12, MUTED)
        box(s, xs[3], y + 0.02, 0.95, 0.27, tint(col[st], 0.18), radius=0.5)
        text(s, xs[3], y + 0.05, 0.95, 0.25, st, 11, col[st], True, align=PP_ALIGN.CENTER)
        text(s, xs[4], y + 0.03, ws[4], rh, res, 11, INK)
    source(s, "Anys & Weiler 2024; McPherson 1984; Heisler 1982, 1984; Herbst et al. 2008; USDA NRCS TR-55; Ajuntament de Barcelona, Gestió de l'arbrat "
              "viari de Barcelona (2011) and Pla director de l'arbrat 2017–2037; Open Data BCN.")


SLIDES = [
    ("main", fig_slide("slides/fig_v9/flow_00_overview.png", "Methodology",
                       "Which species replace the trees a project removes, and where to add new ones",
                       "Ajuntament de Barcelona: Open Data BCN street trees, Mapa base topogràfic 1:1000, Pla director de l'arbrat "
                       "2017–2037; ICGC LiDAR 2021; Barcelona Resilience Atlas; PDISBA.")),
    ("highs", fig_slide("slides/fig_v9/flow_07_highs.png", "HiGHS: the solver that picks every species",
                        "One exact solve: the best layout that obeys every rule, and a proof that no other scores higher",
                        "HiGHS open-source solver (highs.dev; Huangfu & Hall 2018, Math. Prog. Comp. 10:119–142), via SciPy. "
                        "Example scores are illustrative.")),
    ("why", why_replace),
    ("assume", assumptions),
    (None, fig_slide("slides/fig_v7/flow_04_design.png", "Backup · Design module", "Inside the project area the designer draws",
                     "Ajuntament de Barcelona, Gestió de l'arbrat viari de Barcelona (2011); Pla director de l'arbrat 2017–2037.")),
    (None, fig_slide("slides/fig_v7/flow_06_optimiser.png", "Backup · How the optimiser finds the layout",
                     "No trial and error: a score table, then one exact solve per weight set",
                     "HiGHS open-source linear optimisation solver (highs.dev), called through SciPy.")),
    (None, fig_slide("slides/fig_v7/flow_02_heat.png", "Backup · Heat module", "Fast proxy inside the loop, full UTCI on the final layouts",
                     "Ladybug Tools (Ladybug, Honeybee/Radiance); weather: El Prat TMYx 2011–2025 (climate.onebuilding.org).")),
    (None, fig_slide("slides/fig_v7/flow_03_runoff.png", "Backup · Runoff module", "Event runoff on a 1 m grid, routed to the flood hotspots",
                     "PDISBA design storms; Anys & Weiler 2024 (interception); ICGC LiDAR 2021 (terrain).")),
    (None, fig_slide("slides/fig_v7/flow_01_screening.png", "Backup · City screening", "Indicators for every street-tree position",
                     "Open Data BCN street-tree inventory; ICGC LiDAR 2021; Mapa base topogràfic 1:1000; Barcelona Resilience Atlas.")),
    (None, fig_slide("slides/fig_v9/flow_05_validation.png", "Backup · Validation plan",
                     "Each module checked against something it was not fitted to",
                     "Ladybug Tools; Infrared City; Anys & Weiler 2024.")),
]


def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for key, fn in SLIDES:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        s.notes_slide.notes_text_frame.text = SAY.get(key, "Backup.")
    out = ROOT / "slides/methodology_17nov.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT), f"({len(SLIDES)} slides)")


if __name__ == "__main__":
    build()
