"""Methodology section for the 17 Nov tutor session: the one-page method (v9), the HiGHS slide, then the method backups of the
10 Nov deck (design, heat, runoff, screening, optimiser steps, validation). Figures from make_flowcharts_v9.py and
make_flowcharts.py, placed as in make_deck_editable.py (figure title and footer cropped, native title and sources).
Output: slides/methodology_17nov.pptx. Run from scripts/: python make_deck_method_17nov.py
"""
from pptx import Presentation
from pptx.util import Inches
from make_deck_editable import fig_slide, rgb, W, H, BG, ROOT

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
             "layout that obeys the rules is a point inside this shape, and the best one is always a corner. HiGHS walks from "
             "corner to corner, always uphill, and stops with a proof that no corner is higher. In the small example, picking "
             "the best species everywhere would plant A three times and break the cap. HiGHS keeps A where its lead is largest "
             "and gives position 2 to B, losing only 0.1. A genetic or ant-colony search would obey the rules too, but would never "
             "know if it had found the best. HiGHS does it for Porta in 0.06 seconds, for the whole city in about ten, and the "
             "answer is always whole trees.",
}

SLIDES = [
    ("main", fig_slide("slides/fig_v9/flow_00_overview.png", "Methodology",
                       "Which species replace the trees a project removes, and where to add new ones",
                       "Ajuntament de Barcelona: Open Data BCN street trees, Mapa base topogràfic 1:1000, Pla director de l'arbrat "
                       "2017–2037; ICGC LiDAR 2021; Barcelona Resilience Atlas; PDISBA.")),
    ("highs", fig_slide("slides/fig_v9/flow_07_highs.png", "HiGHS: the solver that picks every species",
                        "One exact solve: the best layout that obeys every rule, and a proof that no other scores higher",
                        "HiGHS open-source solver (highs.dev; Huangfu & Hall 2018, Math. Prog. Comp. 10:119–142), via SciPy. "
                        "Example scores are illustrative.")),
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
    (None, fig_slide("slides/fig_v7/flow_05_validation.png", "Backup · Validation plan",
                     "Each module checked against something it was not fitted to",
                     "Mannucci et al. 2025; Anys & Weiler 2024.")),
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
