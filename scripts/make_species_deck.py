"""Two slides: the species league table and "who replaces whom" (scripts/species_ranking.py). Native text only.
Output: slides/species_ranking.pptx. Run from scripts/: python make_species_deck.py
"""
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
from make_deck_editable import text, box, head, source, rgb, tint, W, H, M, BG, ROOT, INK, MUTED, TREE, WARN

DB = ROOT / "databases/barcelona"
d = pd.read_csv(DB / "species_ranking.csv")
rep = pd.read_csv(DB / "species_replaces.csv")
PL = d[d.species.str.startswith("Platanus")].iloc[0]
SRC = ("Crowns: ICGC LiDAR 2021–2022, street trees of trunk class TERCERA (Open Data BCN inventory, CC BY 4.0). "
       "Interception: Anys & Weiler 2024. Size classes: Gestió de l'arbrat viari de Barcelona (2011). Survival: Open Data BCN "
       "quarterly inventory 2018–2026.")


def pct(v):
    return "–" if pd.isna(v) else f"{100 * v:.0f}"


def s_league(s):
    head(s, "Which species give the most, tree for tree?",
         "One tree on open ground at equal trunk size; plane tree = 100. Ranked by the method's balanced weights")
    p = d[d.palette].reset_index(drop=True).head(12)
    xs, ws = [M, M + 0.5, M + 4.0, M + 5.3, M + 6.6, M + 7.9, M + 9.2], [0.5, 3.5, 1.3, 1.3, 1.3, 1.3, 1.4]
    for x, w, h in zip(xs, ws, ("#", "Species", "Size", "Summer shade", "Winter shade", "Rain held", "Survival")):
        text(s, x, 1.45, w, 0.3, h.upper(), 11, MUTED, True)
    for k, q in enumerate(p.itertuples()):
        y = 1.8 + k * 0.42
        if k % 2 == 0:
            box(s, M - 0.1, y - 0.04, 10.7, 0.4, tint(MUTED, 0.06), radius=0)
        text(s, xs[0], y, ws[0], 0.35, str(k + 1), 13, MUTED, True)
        text(s, xs[1], y, ws[1], 0.35, [[(q.species, {"italic": True})]], 13, INK, True)
        text(s, xs[2], y, ws[2], 0.35, q.size_class if isinstance(q.size_class, str) else "–", 13, INK)
        for x, w, v, c in ((xs[3], ws[3], q.summer_m2h / PL.summer_m2h, TREE), (xs[4], ws[4], q.winter_m2h / PL.winter_m2h, WARN),
                           (xs[5], ws[5], q.storage_l / PL.storage_l, TREE)):
            text(s, x, y, w, 0.35, pct(v), 13, c, True)
        text(s, xs[6], y, ws[6], 0.35, "–" if pd.isna(q.survival) else f"{100 * q.survival:.0f}%", 13, INK)
    text(s, 11.1, 1.45, 1.9, 5.3, [
        [("Plane tree ", {"bold": True}), (f"(not in the palette): 100 on all three, survival {100 * PL.survival:.0f}%.", {})],
        [("Winter shade ", {"bold": True, "color": WARN}), ("is a cost: lower is better.", {})],
        [("Survival: ", {"bold": True}), ("share of the city's plantings still standing, at a standard age mix. "
                                          "– = fewer than 30 plantings.", {})],
        [(f"Top 12 of {d.palette.sum()} palette species.", {"color": MUTED})]], 11, INK)
    source(s, SRC)


def s_replaces(s):
    head(s, "Who replaces whom, without losing anything?",
         "The species the city removes most: its most planted successor vs the best one of the same size class. Removed tree = 100")
    xs = [M, M + 3.2, M + 6.6, M + 9.6]
    for x, w, h in zip(xs, (3.1, 3.3, 3.0, 3.0), ("Removed (trees, 2018–26)", "City planted most", "Best like-for-like", "")):
        text(s, x, 1.45, w, 0.3, h.upper(), 11, MUTED, True)
    text(s, xs[1], 1.72, 3.3, 0.3, "summer · winter · rain", 10, MUTED)
    text(s, xs[2], 1.72, 3.0, 0.3, "summer · winter · rain", 10, MUTED)
    r = rep[rep.city_summer.notna()].head(8)
    for k, q in enumerate(r.itertuples()):
        y = 2.05 + k * 0.6
        if k % 2 == 0:
            box(s, M - 0.1, y - 0.05, 9.6, 0.56, tint(MUTED, 0.06), radius=0)
        text(s, xs[0], y, 3.1, 0.5, [[(q.removed, {"italic": True, "bold": True}), (f"  {q.n_removed}", {"color": MUTED})]], 13, INK)
        text(s, xs[1], y, 3.3, 0.5, [[(q.city_top, {"italic": True}), (f"  {100 * q.city_top_share:.0f}%", {"color": MUTED})],
                                     [(f"{pct(q.city_summer)} · {pct(q.city_winter)} · {pct(q.city_storage)}", {"bold": True})]], 11, INK)
        keep = q.n_keep_all > 0
        text(s, xs[2], y, 3.0, 0.5, [[(q.best1, {"italic": True}), ("" if keep else "  closest", {"color": WARN})],
                                     [(f"{pct(q.best1_summer)} · {pct(q.best1_winter)} · {pct(q.best1_storage)}",
                                       {"bold": True, "color": TREE if keep else WARN})]], 11, INK)
    box(s, 9.9, 1.45, 2.9, 5.0, tint(TREE, 0.08))
    text(s, 10.1, 1.6, 2.5, 4.8, [
        [("Like-for-like ", {"bold": True, "color": TREE}), ("= same size class, at least 100 on summer shade and rain held, at most "
                                                           "100 on winter shade.", {})],
        [("No species replaces the plane tree ", {"bold": True}), ("on all three; Gleditsia comes closest.", {})],
        [("The city's choice ", {"bold": True}), ("may follow the sidewalk, which this table ignores: the tool decides per position.", {})]],
        12, INK)
    source(s, SRC + " City successors: observed replacements, same inventory.")


SAY = {
    "league": "If you rank the species tree for tree, at the same trunk size and on open ground, the plane tree still sets the bar. "
              "Of the species the city can plant, Firmiana, Gleditsia, Celtis and Melia give the most summer shade and hold the most "
              "rain, and Gleditsia also has one of the best survival records in the city's own plantings.",
    "replaces": "And here is who replaces whom. For each species the city removes most, what it planted most in its place, and the best "
                "species of the same size class. For poplars, false acacia and Siberian elm there are species that keep everything. "
                "For the plane tree there is none: every successor loses something, so the choice has to be made position by position.",
}


def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    for key, fn in (("league", s_league), ("replaces", s_replaces)):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(BG)
        fn(s)
        s.notes_slide.notes_text_frame.text = SAY[key]
    out = ROOT / "slides/species_ranking.pptx"
    prs.save(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
