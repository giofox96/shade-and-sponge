"""Shared cluster map on the RM p. 37 template ("Before you draw: open up your topic"): two theses around one cluster topic.

A = this thesis (notes/methodology.md, notes/miro_map_proposal.md). B = the colleague's "plaza photo" map, as drawn by her (B to check).
The centre text is a draft to agree. Output: slides/fig/09_cluster_map.svg + .png (2400x1580).
"""
import math
from xml.sax.saxutils import escape
import make_infographics as mi

mi.W, mi.H = 2400, 1580
W, H = mi.W, mi.H
INK, MUTED, LINE = "#1F3A44", "#6B7C85", "#9AA9AF"
A, B, BOTH = mi.TREE, "#E8567F", "#5B6B73"   # thesis A green, thesis B pink, shared grey
CX, CY, RX, RY, BW, BH = 1200, 830, 960, 600, 400, 195

# clockwise from the top, in the template's order: (title, A, B, shared)
BOXES = [
    ("USERS", "Computational designer; municipal climate planner; urban hydrologist",
     "Planners; sensory-sensitive and neurodivergent people, rarely reached by consultation", "Designers and planners in early design"),
    ("IMPACTS", "Summer heat stress (UTCI) and storm runoff on Porta streets",
     "Whose experience of the square counts; risk of tokenism", "Public space in hotter summers"),
    ("APPLICATIONS", "Species and position for each plane tree replaced",
     "Scoring street-level images and design options", "Comparing design options before they are built"),
    ("BY-PRODUCTS", "Porta trait table, LiDAR tree table, scenario results",
     "A rated photo set of a Vienna square; a corpus of persona reasons", "Open datasets left behind"),
    ("MONITORING", "Open: no tracking after planting yet",
     "Keeps collecting real experience", "Same metrics before and after (GreenInCities co-monitoring)"),
    ("DISCIPLINES", "Urban hydrology, urban climatology, landscape design, plant ecology",
     "Participatory planning, AI / language models, sensory experience", "Computational design"),
    ("↓ DATA OUT", "Ranked layouts; shade and runoff maps",
     "Scores and reasons on a dashboard", "A ranking a designer can question"),
    ("SERVING INFRASTRUCTURE", "Python core, Grasshopper + Ladybug; Infrared City to confirm",
     "Commercial model via paid API + open-weight model run locally; university survey tool", "Lock-in: own code vs paid services"),
    ("↑ DATA IN", "ICGC LiDAR 2021, tree inventory, PDISBA storms, weather file, trait tables",
     "Photos of the square; participants' profiles, sensory self-ratings, lived experience", "Who is missing from the data?"),
    ("DRIVERS", "Plane trees cut toward the 15% species cap; pluvial floods",
     "Planners adopting AI 'synthetic participants'", "Hotter summers"),
    ("VERIFICATION", "Interception vs Freiburg field data; today's trees (S0) as baseline; Florence transfer",
     "Each persona vs its own participant's ratings; agreement, bias gap", "Who decides it worked, and against what?"),
    ("KNOWLEDGE", "Does species choice trade heat against runoff?",
     "Which people can synthetic participants stand in for?", "What the model cannot see (LAI proxy; smell, sound, heat on the skin)"),
]


def txt(x, y, s, size=13, fill=INK, weight="normal", anchor="start", italic=False):
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{it}>{escape(s)}</text>'


def centre(i):
    th = math.radians(i * 360 / len(BOXES))
    return CX + RX * math.sin(th), CY - RY * math.cos(th)


def box(i, title, a, b, both):
    x, y = centre(i)
    x0, y0 = x - BW / 2, y - BH / 2
    s = f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{BW}" height="{BH}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    s += txt(x0 + 18, y0 + 30, title, 16, INK, "bold")
    yy = y0 + 56
    for col, tag, t_ in ((A, "A", a), (B, "B", b), (BOTH, "A+B", both)):
        s += f'<rect x="{x0 + 18:.0f}" y="{yy - 12:.0f}" width="{30 if tag == "A+B" else 18}" height="16" rx="3" fill="{col}"/>'
        s += txt(x0 + (33 if tag == "A+B" else 27), yy + 1, tag, 10, "#fff", "bold", "middle")
        p, h = mi.para(x0 + 58, yy, t_, BW - 76, 13, 1.25, fill=col if tag != "A+B" else INK)
        s += p
        yy += max(h, 18) + 12
    return s


def build():
    b = [txt(60, 62, "One cluster, two theses: heat-adapted public space, computed", 36, INK, "bold"),
         txt(60, 96, "Slide p. 37 template. A and B unpack the same cluster topic from their own research; grey notes are the shared ground. "
                     "Draft for discussion: centre text and B's notes to be checked by B.", 15, MUTED)]
    pts = [centre(i) for i in range(len(BOXES))]
    loop = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts + pts[:1])
    b.append(f'<polyline points="{loop}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    b += [box(i, *bx) for i, bx in enumerate(BOXES)]
    # centre: cluster topic + the two units followed
    b.append(f'<rect x="{CX - 230}" y="{CY - 120}" width="460" height="110" fill="{INK}"/>')
    b.append(txt(CX, CY - 88, "CLUSTER TOPIC (draft)", 13, "#fff", "bold", "middle"))
    b.append(mi.para(CX - 205, CY - 60, "Computational prediction of how public space performs in hotter summers", 410, 17, 1.25, fill="#fff", weight="bold")[0])
    for k, (col, s_) in enumerate(((A, "A · unit followed: one plane-tree position in Porta, Barcelona"),
                                   (B, "B · unit followed: one photo of a Vienna square"))):
        y = CY + 20 + k * 52
        b.append(f'<rect x="{CX - 230}" y="{y}" width="460" height="40" fill="{col}" fill-opacity="0.12" stroke="{col}"/>')
        b.append(txt(CX, y + 25, s_, 13.5, col, "bold", "middle"))
    # key
    ky = H - 60
    for k, (col, lab) in enumerate(((A, "A · trait-based tree selection for heat and runoff"),
                                    (B, "B · synthetic participants for sensory-sensitive people"),
                                    (BOTH, "A+B · shared ground"))):
        x = 60 + k * 0
        y = ky - 40 + k * 22
        b.append(f'<rect x="{x}" y="{y - 12}" width="14" height="14" rx="3" fill="{col}"/>' + txt(x + 22, y, lab, 13, MUTED))
    return "".join(b)


if __name__ == "__main__":
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{mi.FONT}">'
           f'<rect width="{W}" height="{H}" fill="#fff"/>{build()}</svg>')
    p = mi.OUT / "09_cluster_map.svg"
    mi.OUT.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
    mi.to_png(p)
    print("wrote", p.relative_to(mi.ROOT))
