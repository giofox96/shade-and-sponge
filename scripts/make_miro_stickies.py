"""Sticky-note images to paste into the RM cluster-3 Miro board (Elena's colours: yellow hub, blue Elena, green Giovanni).

Content: notes/rm_cluster3_common_points.md and the RM L02 feedback. "?" marks what the owner must fill or check.
Run: python scripts/make_miro_stickies.py  ->  slides/seminar_rm/miro/*.png
"""
import pathlib
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = pathlib.Path(__file__).resolve().parents[1] / "slides" / "seminar_rm" / "miro"
# Colours sampled from Elena's board screenshot (Miro sticky yellow, light blue, light green); grey, pink, dark = Miro palette
HUB, ELENA, GIO, SHARED, PRACT, CENTRE, NOTE = "#fcf59d", "#9ce7fe", "#d3eda2", "#e6e6e6", "#ffc6dd", "#1f3a44", "#f5f6f8"
plt.rcParams["font.family"] = "Segoe UI"   # closest installed font to Miro's Open Sans


def sticky(ax, x, y, text, color, w=2.2, h=None, fs=11, width=22, fg="#1a1a1a", bold=False):
    h = h or w   # Miro sticky notes are square
    ax.add_patch(FancyBboxPatch((x - w / 2 + 0.03, y - h / 2 - 0.06), w, h, boxstyle="square,pad=0", fc="#00000014", ec="none", zorder=2))
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="square,pad=0", fc=color, ec="none", zorder=3))
    ax.text(x, y, "\n".join(textwrap.fill(p, width, break_long_words=False) for p in text.split("\n")), ha="center", va="center", fontsize=fs, color=fg,
            weight="bold" if bold else "normal", zorder=4)


def arrow(ax, a, b, color="#8c8c8c", both=False, rad=0.2):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", color=color, lw=1.2,
                                                    mutation_scale=14, shrinkA=85, shrinkB=85,
                                                    connectionstyle=f"arc3,rad={rad}"), zorder=1)


def canvas(w, h, title=None):   # title kept only as the file's purpose; Elena's board has no canvas titles
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w), ax.set_ylim(0, h), ax.axis("off")
    return fig, ax


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def hub_links():
    fig, ax = canvas(16, 11)
    hubs = {"Comfort": (2.5, 8.6), "Individual traits": (13.5, 8.6), "Model validation": (13.5, 2.2), "Recommender systems": (2.5, 2.2)}
    for t, (x, y) in hubs.items():
        sticky(ax, x, y, t, HUB, 2.4, fs=17, width=11)
    arrow(ax, hubs["Comfort"], hubs["Individual traits"], color="#c0392b", both=True, rad=0)
    sticky(ax, 8, 8.6, "TENSION · UTCI is comfort for a standard person: the average-based 'label' Elena's thesis argues against. "
           "Giovanni's heat metric falls under her critique.", NOTE, 2.7, fs=9.5, width=27)
    arrow(ax, hubs["Individual traits"], hubs["Model validation"], rad=0)
    sticky(ax, 13.5, 5.4, "An individual prediction needs an individual check. E: each persona vs its own participant (Park). "
           "G: per-tree interception vs field data (Anys).", NOTE, 2.7, fs=9.5, width=27)
    arrow(ax, hubs["Model validation"], hubs["Recommender systems"], rad=0)
    sticky(ax, 8, 2.2, "A recommender is only as good as its check. Mauro: tested on 148 people. "
           "Nicol: diversity gains, no heat or runoff outcome. GAP", NOTE, 2.7, fs=9.5, width=27)
    arrow(ax, hubs["Recommender systems"], hubs["Comfort"], rad=0)
    sticky(ax, 2.5, 5.4, "LOOP? What gets recommended changes where people go and what gets planted, and so comfort.",
           NOTE, 2.4, fs=9.5, width=24)
    save(fig, "01_hub_links.png")


def centre():
    fig, ax = canvas(12, 5.4)
    sticky(ax, 6, 3.6, "How computation turns information about places and the people in them into options for designers",
           CENTRE, 9, 1.9, fs=17, width=44, fg="white", bold=True)
    ax.text(6, 2.45, "the lecturers' frame, RM L02 [01:29:35]", ha="center", fontsize=9, color="#666")
    sticky(ax, 6, 1.1, "Draft shared claim: cities decide with averages; we predict for the single case and test it against the rule",
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
    fig, ax = canvas(11.4, 11)
    for i, (hub, e, g, sh) in enumerate(rows):
        y = 9.5 - i * 2.65
        sticky(ax, 1.4, y, hub, HUB, 2.3, fs=13, width=14)
        sticky(ax, 4.2, y, e, ELENA, 2.3, fs=10.5, width=20)
        sticky(ax, 7.0, y, g, GIO, 2.3, fs=10.5, width=20)
        sticky(ax, 9.8, y, sh, SHARED, 2.3, fs=11.5, width=18)
    save(fig, "03_new_hubs.png")


def before_and_practice():
    fig, ax = canvas(14.2, 5.8)
    for y, hub, b1, b2 in [(4.3, "Comfort", "BEFORE · judged on site, being there (stage 1 of both journeys)",
                            "BEFORE · Lynch 1960, The Image of the City"),
                           (1.5, "Recommender systems", "BEFORE · Barcelona master plan + the 2004/05 replacement table",
                            "BEFORE · sensory and autism-friendly guides ? (Elena to name one)")]:
        sticky(ax, 1.4, y, hub, HUB, 2.3, fs=15, width=11)
        sticky(ax, 4.1, y, b1, SHARED, 2.3, fs=10, width=21)
        sticky(ax, 6.8, y, b2, SHARED, 2.3, fs=10, width=21)
    sticky(ax, 10.1, 4.3, "PRACTICE · Treepedia, MIT Senseable City Lab: greenery seen from street-level images", PRACT, 2.3, fs=10, width=21)
    sticky(ax, 12.8, 4.3, "PRACTICE · GreenInCities: neuro-urbanism mapping walks + a Barcelona heat pilot. BRIDGE between both",
           PRACT, 2.3, fs=10, width=21)
    sticky(ax, 10.1, 1.5, "PRACTICE · Smelly Maps, Daniele Quercia ? (name to verify)", PRACT, 2.3, fs=10, width=21)
    sticky(ax, 12.8, 1.5, "Each one: source / does / does not", NOTE, 2.3, fs=10, width=18)
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
    fig, ax = canvas(15.4, 6.2)
    for i, (c, name, does, dnot) in enumerate(papers):
        x, y = 1.5 + (i % 5) * 3.1, 4.6 - (i // 5) * 3.1
        sticky(ax, x, y, f"{name}\n\nDOES · {does}\n\nDOES NOT · {dnot}", c, 2.9, fs=9.5, width=28)
    save(fig, "05_does_does_not.png")


def hub_block(name, hub, desc, blue, green, hub_w=2.4):
    """One hub in the format of Elena's 27 Oct board: hub -> description <- brace -> blue (top) and green (bottom)."""
    fig, ax = canvas(11.6, 5.6)
    y = 2.8
    sticky(ax, 9.6, y, hub, HUB, hub_w, fs=19, width=8)
    sticky(ax, 6.2, y, desc, HUB, 2.2, fs=12, width=15)
    sticky(ax, 1.4, y + 1.05, blue, ELENA, 1.8, fs=11, width=16)
    sticky(ax, 1.4, y - 1.05, green, GIO, 1.8, fs=11, width=16)
    kw = dict(arrowstyle="-|>", color="#222", lw=1.3, mutation_scale=14, shrinkA=0, shrinkB=0)
    ax.annotate("", xy=(7.35, y), xytext=(8.35, y), arrowprops=kw)                                   # hub -> description
    for ny, rad in ((y + 1.05, 0.3), (y - 1.05, -0.3)):                                              # description -> notes (curved, as hers)
        ax.annotate("", xy=(2.4, ny), xytext=(5.05, y), arrowprops=dict(kw, connectionstyle=f"arc3,rad={rad}"))
    save(fig, name)


def new_hubs_v2():   # 27 Oct: two new hubs drawn like Elena's; her convention links hubs to authors only (see notes)
    hub_block("06_preference.png", "Preference", "Whose preferences shape the outcome",
              "Each person decides what to avoid or seek",
              "The planner sets the weight between heat and runoff")
    hub_block("07_lack_of_data.png", "Lack of data", "What is not measured or recorded, and what stands in for it",
              "Neurodivergent people's urban experience is little researched",
              "Trees without measured LAI or species traits: proxies are used")


if __name__ == "__main__":
    for f in (hub_links, centre, new_hubs, before_and_practice, does_not):
        f()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
