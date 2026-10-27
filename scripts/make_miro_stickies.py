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


DAVID = "#ffd9a8"   # third colour for David's column (placeholder, his thesis not received yet)


def row(ax, y, cells, h=2.3):
    """cells: (x, text, colour, fs, width); one sticky each."""
    for x, text, c, fs, w in cells:
        sticky(ax, x, y, text, c, h, fs=fs, width=w)


def preference_and_gaps():   # v2 (27 Oct): new hub Preference + two notes under existing hubs
    rows = [("Preference", "Whose preferences shape the outcome", "Each person decides what to avoid or seek",
             "The planner sets the weight between heat and runoff"),
            ("Failure and uncertainty", "Who notices when the model is wrong", "A confident rating that is wrong for the person who relies on it",
             "False precision from an uncalibrated LAI proxy"),
            ("Lack of data", "Who or what is invisible in the data", "The people missing from the data (Kenna)",
             "Trees without species or leaf area")]
    fig, ax = canvas(11.4, 8.2)
    for i, (hub, d, e, g) in enumerate(rows):
        y = 6.9 - i * 2.65
        row(ax, y, [(1.4, hub, HUB, 13, 14), (4.2, d, HUB, 10.5, 20), (7.0, e, ELENA, 10.5, 20), (9.8, g, GIO, 10.5, 20)])
    save(fig, "06_preference_and_gaps.png")


def tension():
    fig, ax = canvas(11, 5.4)
    sticky(ax, 1.4, 3.8, "Comfort", HUB, 2.4, fs=17, width=11)
    sticky(ax, 4.6, 3.8, "Perceived comfort across senses", ELENA, 2.4, fs=11, width=18)
    sticky(ax, 8.6, 3.8, "Computed thermal comfort (UTCI)", GIO, 2.4, fs=11, width=18)
    arrow(ax, (4.6, 3.8), (8.6, 3.8), color="#c0392b", both=True, rad=0)
    sticky(ax, 6.6, 1.0, "TENSION · UTCI is the comfort of a standard person: the average Elena argues against", NOTE, 2.0, fs=9.5, width=22)
    save(fig, "07_tension.png")


def hub_to_hub():
    links = [("Representation", "What you keep of a place or a person decides what you can predict", "Impact prediction"),
             ("Impact prediction", "A prediction for the single case needs a check on the single case", "Model validation"),
             ("Model validation", "The check decides how far the advice can be trusted", "Decision support"),
             ("Decision support", "LOOP · decisions change who and what is exposed", "Vulnerability")]
    fig, ax = canvas(10.6, 10.6)
    for i, (a, note, b) in enumerate(links):
        y = 9.3 - i * 2.8
        row(ax, y, [(1.4, a, HUB, 13, 11), (5.3, note, NOTE, 10, 22), (9.2, b, HUB, 13, 11)])
        arrow(ax, (1.4, y), (9.2, y), rad=0)
    save(fig, "08_hub_to_hub_links.png")


def david_column():
    qs = [("Comfort", "Does your thesis predict how a person feels in a place? Which senses?"),
          ("Representation", "What does your thesis keep of a place or a person, and what does it lose?"),
          ("Impact prediction", "What do you predict without measuring on site, and with which proxy?"),
          ("Vulnerability", "Who or what bears the most harm in your case, and is there data on it?"),
          ("Model validation", "What is your ground truth, and what simple rule must you beat?"),
          ("Decision support", "Who takes the decision with your output, and what do they see?"),
          ("Preference", "Whose preferences shape your result?")]
    fig, ax = canvas(8.6, 19)
    for i, (hub, q) in enumerate(qs):
        y = 17.9 - i * 2.65
        row(ax, y, [(1.4, hub, HUB, 13, 11), (4.2, q, NOTE, 10, 20)])
        ax.add_patch(FancyBboxPatch((6.15, y - 1.15), 2.3, 2.3, boxstyle="square,pad=0", fc=DAVID + "55", ec="#d98a2b", ls="--", lw=1.4, zorder=3))
        ax.text(7.3, y, "David", ha="center", va="center", fontsize=11, color="#b06a10", zorder=4)
    save(fig, "09_david_column.png")


if __name__ == "__main__":
    for f in (hub_links, centre, new_hubs, before_and_practice, does_not):
        f()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
