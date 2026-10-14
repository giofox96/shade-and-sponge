"""Shared cluster map on the RM p. 37 template ("Before you draw: open up your topic"): three theses around one cluster topic.

Giovanni (green) = this thesis (notes/methodology.md, notes/miro_map_proposal.md). Elena (light blue) = her "plaza photo" map,
as drawn by her (Elena to check). David (red) = only his topic is known; his notes start with "?" and are guesses for him to replace.
Cluster topic = proposal 1, agreed 14 Oct. Output: slides/fig/09_cluster_map.svg + .png (2400x1720).
"""
import csv, math
from xml.sax.saxutils import escape
import make_infographics as mi

mi.W, mi.H = 2400, 1720
W, H = mi.W, mi.H
INK, MUTED, LINE = "#1F3A44", "#6B7C85", "#9AA9AF"
PEOPLE = [("G", mi.TREE, "Giovanni"), ("E", "#2B8FD0", "Elena"), ("D", "#D64545", "David"), ("ALL", "#5B6B73", "shared")]
CX, CY, RX, RY, BW, BH = 1200, 900, 960, 650, 400, 205

# clockwise from the top, in the template's order: (title, Giovanni, Elena, David, shared)
BOXES = [
    ("USERS", "Computational designer; municipal climate planner; urban hydrologist",
     "Planners; sensory-sensitive and neurodivergent people", "? Architects and designers without climate-analysis training",
     "Designers who are not climate experts"),
    ("IMPACTS", "Summer heat stress (UTCI) and storm runoff on Porta streets",
     "Whose experience of the square counts; risk of tokenism", "? More climate-aware projects",
     "Decisions that change how people live hotter summers"),
    ("APPLICATIONS", "Species and position for each plane tree replaced",
     "Scoring street-level images and design options", "? Explaining climate analyses while designing",
     "Comparing options before they are built"),
    ("BY-PRODUCTS", "Porta trait table, LiDAR tree table, scenario results",
     "Rated photo set of a Vienna square; corpus of persona reasons", "? Plain-language glossary of climate terms",
     "Open datasets left behind"),
    ("MONITORING", "Open: no tracking after planting yet",
     "Keeps collecting real experience", "? Do designers' choices change over time?",
     "Same metrics before and after"),
    ("DISCIPLINES", "Urban hydrology and climatology, landscape design, plant ecology",
     "Participatory planning, AI / language models, sensory experience", "? Building physics, design education, interaction design",
     "Computational design"),
    ("↓ DATA OUT", "Ranked layouts; shade and runoff maps",
     "Scores and reasons on a dashboard", "? Explanations a designer can read",
     "An answer a designer can question"),
    ("SERVING INFRASTRUCTURE", "Python core, Grasshopper + Ladybug; Infrared City to confirm",
     "Paid model API + open-weight model run locally; survey tool", "? Climate-analysis plug-ins + a language model",
     "Lock-in: own code vs paid services"),
    ("↑ DATA IN", "ICGC LiDAR 2021, tree inventory, PDISBA storms, weather file, traits",
     "Photos of the square; profiles, sensory self-ratings, lived experience", "? Outputs of climate analyses (comfort, sun, wind)",
     "Who or what is missing from the data?"),
    ("DRIVERS", "Plane trees cut toward the 15% species cap; pluvial floods",
     "Planners adopting AI 'synthetic participants'", "? Climate analyses too technical for most designers",
     "Hotter summers"),
    ("VERIFICATION", "Interception vs field data; today's trees as baseline; Florence transfer",
     "Each persona vs its own participant's ratings; bias gap", "? Do designers understand and decide better?",
     "Who decides the translation is right?"),
    ("KNOWLEDGE", "Does species choice trade heat against runoff?",
     "Which people can synthetic participants stand in for?", "? Which terms block designers, and why?",
     "What gets lost in translation"),
]


def txt(x, y, s, size=13, fill=INK, weight="normal", anchor="start", italic=False):
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{it}>{escape(s)}</text>'


def chip(x, y, tag, col):
    w = 32 if tag == "ALL" else 18
    return (f'<rect x="{x:.0f}" y="{y - 12:.0f}" width="{w}" height="16" rx="3" fill="{col}"/>'
            + txt(x + w / 2, y + 1, tag, 10, "#fff", "bold", "middle"))


def centre(i):
    th = math.radians(i * 360 / len(BOXES))
    return CX + RX * math.sin(th), CY - RY * math.cos(th)


def box(i, title, *notes):
    x, y = centre(i)
    x0, y0 = x - BW / 2, y - BH / 2
    s = f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{BW}" height="{BH}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    s += txt(x0 + 18, y0 + 30, title, 16, INK, "bold")
    yy = y0 + 54
    for (tag, col, _), note in zip(PEOPLE, notes):
        guess = note.startswith("?")
        s += chip(x0 + 18, yy, tag, col)
        p, h = mi.para(x0 + 60, yy, note, BW - 78, 12.5, 1.22, fill=INK if tag == "ALL" else col, italic=guess)
        s += p
        yy += max(h, 16) + 8
    return s


def build():
    b = [txt(60, 58, "Cluster map draft: from climate data to design decisions", 36, INK, "bold"),
         txt(60, 90, "Slide p. 37 template. Giovanni, Elena and David unpack the same cluster topic from their own research; grey notes are the shared ground. "
                     "Draft for discussion: Elena's notes to check, David's notes (marked ?) are guesses to replace.", 15, MUTED)]
    pts = [centre(i) for i in range(len(BOXES))]
    loop = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts + pts[:1])
    b.append(f'<polyline points="{loop}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    b += [box(i, *bx) for i, bx in enumerate(BOXES)]
    # centre: cluster topic + the unit each person follows
    b.append(f'<rect x="{CX - 260}" y="{CY - 175}" width="520" height="150" fill="{INK}"/>')
    b.append(txt(CX, CY - 143, "CLUSTER TOPIC", 13, "#fff", "bold", "middle"))
    b.append(txt(CX, CY - 108, "From climate data to design decisions", 24, "#fff", "bold", "middle"))
    b.append(mi.para(CX - 235, CY - 78, "How computation translates climate information into choices designers can understand and act on",
                     470, 14, 1.3, fill="#fff")[0])
    units = ["unit: one plane-tree position in Porta, Barcelona", "unit: one photo of a Vienna square", "unit: one climate analysis (to confirm)"]
    for k, ((tag, col, name), u) in enumerate(zip(PEOPLE, units)):
        y = CY - 5 + k * 48
        b.append(f'<rect x="{CX - 260}" y="{y}" width="520" height="38" fill="{col}" fill-opacity="0.12" stroke="{col}"/>')
        b.append(txt(CX, y + 24, f"{name} · {u}", 13.5, col, "bold", "middle"))
    # key
    topics = ["trait-based tree selection for heat and runoff", "synthetic participants for sensory-sensitive people",
              "climate analyses explained to non-expert designers", "shared ground"]
    for k, ((tag, col, name), t_) in enumerate(zip(PEOPLE, topics)):
        y = H - 92 + k * 22
        b.append(chip(60, y, tag, col) + txt(102, y + 1, f"{name} · {t_}" if tag != "ALL" else t_, 13, MUTED))
    return "".join(b)


if __name__ == "__main__":
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{mi.FONT}">'
           f'<rect width="{W}" height="{H}" fill="#fff"/>{build()}</svg>')
    p = mi.OUT / "09_cluster_map.svg"
    mi.OUT.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
    mi.to_png(p)
    print("wrote", p.relative_to(mi.ROOT))
    # one row per Miro sticky; colour = Miro sticky colour name
    miro = {"G": "green", "E": "light_blue", "D": "red", "ALL": "gray"}
    rows = [("CLUSTER TOPIC", "ALL", "black", "From climate data to design decisions: how computation translates climate "
                                               "information into choices designers can understand and act on")]
    rows += [("CLUSTER TOPIC", tag, miro[tag], f"{name} · {u}") for (tag, _, name), u in
             zip(PEOPLE, ["unit: one plane-tree position in Porta, Barcelona", "unit: one photo of a Vienna square",
                          "unit: one climate analysis (to confirm)"])]
    rows += [(title, tag, miro[tag], note) for title, *notes in BOXES for (tag, _, _), note in zip(PEOPLE, notes)]
    with open(mi.OUT / "09_cluster_map_stickies.csv", "w", newline="", encoding="utf-8-sig") as f:   # BOM: Excel/Sheets read UTF-8
        w = csv.writer(f)
        w.writerow(["box", "person", "sticky_colour", "text"])
        w.writerows(rows)
    print("wrote", len(rows), "stickies to slides/fig/09_cluster_map_stickies.csv")
