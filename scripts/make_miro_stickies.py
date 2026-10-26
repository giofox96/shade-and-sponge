"""Sticky-note images to paste into the RM cluster-3 Miro board (Elena's colours: yellow hub, blue Elena, green Giovanni).

Content: notes/rm_cluster3_common_points.md and the RM L02 feedback. "?" marks what the owner must fill or check.
Run: python scripts/make_miro_stickies.py  ->  slides/seminar_rm/miro/*.png
"""
import pathlib
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = pathlib.Path(__file__).resolve().parents[1] / "slides" / "seminar_rm" / "miro"
HUB, ELENA, GIO, SHARED, PRACT, CENTRE, NOTE = "#fdf2a1", "#a6e3f7", "#d4f0a0", "#e6e6e6", "#f7c6d9", "#1f3a44", "#ffffff"


def sticky(ax, x, y, text, color, w=2.2, h=1.5, fs=11, width=22, fg="#1b1b1b", bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="square,pad=0", fc=color, ec="#00000022", lw=1, zorder=3))
    ax.text(x, y, "\n".join(textwrap.fill(p, width) for p in text.split("\n")), ha="center", va="center", fontsize=fs, color=fg,
            weight="bold" if bold else "normal", zorder=4)


def arrow(ax, a, b, text=None, color="#555", both=False, rad=0.15):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", color=color, lw=1.6,
                                                    shrinkA=85, shrinkB=85, connectionstyle=f"arc3,rad={rad}"), zorder=1)


def canvas(w, h, title):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w), ax.set_ylim(0, h), ax.axis("off")
    ax.text(0.3, h - 0.4, title, fontsize=15, weight="bold", va="top", color="#1b1b1b")
    return fig, ax


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def hub_links():
    fig, ax = canvas(16, 10, "1 · Links between the hubs (not only hub → paper)")
    hubs = {"Comfort": (3, 7.3), "Individual traits": (13, 7.3), "Model validation": (13, 1.8), "Recommender systems": (3, 1.8)}
    for t, (x, y) in hubs.items():
        sticky(ax, x, y, t, HUB, 2.6, 1.8, fs=16, width=12)
    arrow(ax, hubs["Comfort"], hubs["Individual traits"], color="#c0392b", both=True, rad=0)
    sticky(ax, 8, 7.3, "TENSION · UTCI is comfort for a standard person: the average-based 'label' Elena's thesis argues against. "
           "Giovanni's heat metric falls under her critique.", NOTE, 4.4, 1.6, fs=10, width=46)
    arrow(ax, hubs["Individual traits"], hubs["Model validation"], rad=0)
    sticky(ax, 13, 4.55, "An individual prediction needs an individual check. E: each persona vs its own participant (Park). "
           "G: per-tree interception vs field data (Anys).", NOTE, 4.0, 1.6, fs=10, width=42)
    arrow(ax, hubs["Model validation"], hubs["Recommender systems"], rad=0)
    sticky(ax, 8, 1.8, "A recommender is only as good as its check. Mauro: tested on 148 people. "
           "Nicol: diversity gains, no heat or runoff outcome. GAP", NOTE, 4.4, 1.6, fs=10, width=46)
    arrow(ax, hubs["Recommender systems"], hubs["Comfort"], color="#888", rad=0)
    sticky(ax, 3, 4.55, "LOOP? What gets recommended changes where people go and what gets planted, and so comfort.",
           NOTE, 3.6, 1.5, fs=10, width=32)
    save(fig, "01_hub_links.png")


def centre():
    fig, ax = canvas(12, 6.2, "2 · One centre on top (hierarchy: centre > hubs > papers)")
    sticky(ax, 6, 3.9, "How computation turns information about places and the people in them into options for designers",
           CENTRE, 9, 1.9, fs=17, width=44, fg="white", bold=True)
    ax.text(6, 2.75, "the lecturers' frame, RM L02 [01:29:35]", ha="center", fontsize=9, color="#666")
    sticky(ax, 6, 1.3, "Draft shared claim: cities decide with averages; we predict for the single case and test it against the rule",
           HUB, 9, 1.4, fs=13, width=64)
    save(fig, "02_centre.png")


def new_hubs():
    rows = [("Vulnerability", "Sensory sensitivity: noise, glare, heat, crowds",
             "Summer heat stress (UTCI) and storm runoff; a plane-dominated street stock", "Heat is in both"),
            ("Non-experts · who decides", "The people themselves; planners",
             "Planners without an ecologist's background", "Who is left out?"),
            ("Diversity and sampling", "Demographic labels flatten groups (Wang)",
             "15% species cap; the 'three species' critique in class", "How representative is one case?"),
            ("Representation", "One photo: sound, smell, heat on the skin are lost",
             "LiDAR + traits: roots and transpiration lost; LAI is a proxy", "What is lost when a place becomes data")]
    fig, ax = canvas(14, 9.6, "3 · Hubs the lecturers named for cluster 3")
    for i, (hub, e, g, s) in enumerate(rows):
        y = 7.6 - i * 2.1
        sticky(ax, 1.8, y, hub, HUB, 2.8, 1.7, fs=13, width=14)
        sticky(ax, 5.1, y, "Elena · " + e, ELENA, 3.0, 1.7, fs=10, width=28)
        sticky(ax, 8.4, y, "Giovanni · " + g, GIO, 3.0, 1.7, fs=10, width=28)
        sticky(ax, 11.7, y, s, SHARED, 3.0, 1.7, fs=11, width=26)
    ax.text(5.1, 8.75, "Elena", ha="center", color="#555"), ax.text(8.4, 8.75, "Giovanni", ha="center", color="#555")
    ax.text(11.7, 8.75, "shared / question", ha="center", color="#555")
    save(fig, "03_new_hubs.png")


def before_and_practice():
    fig, ax = canvas(15, 7.2, "4 · Before the tool, and practice projects (brief: 2 theoretical + 3 practice)")
    sticky(ax, 1.8, 4.9, "Comfort", HUB, 2.4, 1.6, fs=15)
    sticky(ax, 5.0, 4.9, "BEFORE · judged on site, being there (stage 1 of both journeys)", SHARED, 3.0, 1.6, fs=10, width=28)
    sticky(ax, 8.2, 4.9, "BEFORE · Lynch 1960, The Image of the City", SHARED, 3.0, 1.6, fs=10, width=28)
    sticky(ax, 1.8, 2.6, "Recommender systems", HUB, 2.4, 1.6, fs=13, width=12)
    sticky(ax, 5.0, 2.6, "BEFORE · Barcelona master plan + the 2004/05 replacement table", SHARED, 3.0, 1.6, fs=10, width=28)
    sticky(ax, 8.2, 2.6, "BEFORE · sensory and autism-friendly guides ? (Elena to name one)", SHARED, 3.0, 1.6, fs=10, width=28)
    sticky(ax, 12.6, 5.6, "PRACTICE · Treepedia, MIT Senseable City Lab: greenery seen from street-level images", PRACT, 3.6, 1.4, fs=10, width=36)
    sticky(ax, 12.6, 3.9, "PRACTICE · GreenInCities: neuro-urbanism mapping walks + a Barcelona heat pilot. BRIDGE between both", PRACT, 3.6, 1.4, fs=10, width=32)
    sticky(ax, 12.6, 2.2, "PRACTICE · Smelly Maps, Daniele Quercia ? (name to verify)", PRACT, 3.6, 1.4, fs=10, width=36)
    sticky(ax, 12.6, 0.8, "each one: source / does / does not", NOTE, 3.6, 0.8, fs=9, width=40)
    save(fig, "04_before_and_practice.png")


def does_not():
    papers = [(ELENA, "Kenna 2022", "Research agenda for neurodiversity in the city; embodied, multi-sensory methods", "A computational method"),
              (ELENA, "Wang 2025", "LLMs replacing participants misportray and flatten identity groups", "Places or urban perception"),
              (ELENA, "Park 2026", "Agents from interviews/surveys predict 1,052 people's own answers", "Places or perception"),
              (ELENA, "Mushkani 2025", "VLMs vs people on 100 Montreal scenes: better on objective than subjective", "Model one person"),
              (ELENA, "Mauro 2022", "PoI recommender combining aversions and preferences; 148 adults, 20 autistic", "?"),
              (GIO, "Anys 2024", "Interception measured on urban trees vs events and traits", "Heat"),
              (GIO, "Peng 2026", "Evolutionary workflow for tree planting vs outdoor heat", "Runoff ? (check)"),
              (GIO, "Shaamala 2025", "AI-optimised placement and species; Ladybug UTCI in Grasshopper", "Runoff"),
              (GIO, "Mannucci 2025", "Parametric heat + flood workflow for small outdoor spaces", "Species traits; optimisation"),
              (GIO, "Nicol 2026", "SylvCiT: diversity and carbon recommender, open source", "Heat or runoff (yet)")]
    fig, ax = canvas(16, 7.4, "5 · Does / does not, one note per paper (the 'does not' shows the gaps)")
    for i, (c, name, does, dnot) in enumerate(papers):
        x, y = 1.6 + (i % 5) * 3.2, 4.9 - (i // 5) * 3.1
        sticky(ax, x, y, f"{name}\n\nDOES · {does}\n\nDOES NOT · {dnot}", c, 3.0, 2.8, fs=9, width=30)
    save(fig, "05_does_does_not.png")


if __name__ == "__main__":
    for f in (hub_links, centre, new_hubs, before_and_practice, does_not):
        f()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
