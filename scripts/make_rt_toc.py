from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
import sys

# Deck palette "Earth" and font, as in scripts/make_infographics.py
C = lambda h: RGBColor.from_string(h)
INK, MUTED, GRID, BG = C("2A2622"), C("665E4F"), C("DCD8CE"), C("F2F0EA")
HEAT, RAIN, TREE, WARN = C("663825"), C("283F66"), C("3F663E"), C("8C6A24")
DARK, DARK_INK, DARK_MUTED = C("283F2A"), C("F2F0EA"), C("B3BAB9")
FONT = "IBM Plex Sans"

TOP = [
    ("WHAT IS THE CHANGE I WANT TO CREATE?", [
        "Barcelona will replace thousands of plane trees. It surely has criteria for the new species, but they are not published, and no public document says what a choice means for heat or flooding.",
        "For every tree to replace, designers and the city should see which species gives more summer shade and holds back more rain at that spot.",
        "Always within the city's rules: no species above 15% of the trees, and bigger trees only on wider sidewalks.",
    ]),
    ("OUTPUT", [
        "Shade & Sponge: an open-source tool (Python core, web app, Grasshopper link).",
        "In: tree inventory, LiDAR crowns, terrain, design storm, summer weather file.",
        "Out: a species and position for each replacement, scored on summer shade / UTCI and runoff against the city's own replacement mix.",
        "Tested in Porta (Nou Barris); run on 33 neighbourhoods.",
    ]),
    ("SHORT-TERM OUTCOMES", [
        "Technological: a reproducible method and open code, checked in Ladybug and Honeybee.",
        "Environmental (simulated): more summer shade than the city's real replacement mix in all 33 neighbourhoods; pedestrian heat stays as with today's planes (±0.2 °C UTCI). Gains: shade, runoff, diversity, winter sun.",
        "Knowledge: species and positions chosen for heat and runoff together, not done yet in the literature reviewed.",
    ]),
    ("MEDIUM-TERM OUTCOMES", [
        "Technological: designers and Parcs i Jardins test it on real replacement campaigns or pilot streets.",
        "Replication: a transferability test in two other cities, Florence and Mataró, with the same method and their own data.",
        "Social: streets keep their shade and comfort while the planes are replaced, starting where heat and flooding overlap.",
        "Economic: fewer trial-and-error plantings, faster design.",
    ]),
    ("LONG-TERM IMPACT", [
        "Environmental: canopy moves toward the city's 30% target for 2037 with no species above 15%; less runoff to sewers in flood hotspots.",
        "Social: no loss of pedestrian comfort during the plane replacement, with more canopy where it is lacking.",
        "Economic: avoided drainage and heat-health costs.",
        "A replicable method for cities replacing monocultures.",
    ]),
]

BOTTOM = [
    ("ASSUMPTIONS", [
        "The city keeps replacing plane trees over the next decade (press, 2026: more than half).",
        "A fast shade proxy and a simple runoff model rank species correctly. Partly checked for heat: proxy shade tracks Ladybug UTCI (r = −0.82).",
        "LiDAR crowns and LAI represent mature trees; light through a crown depends on its LAI.",
        "The city keeps its current rules (no species above 15%, tree size set by sidewalk width): the tool is built on them.",
        "The city and designers are willing to use an open tool.",
    ]),
    ("RISKS", [
        "Optimising two services can concentrate on a few 'best' species: pest risk (mitigated by the cap and a genus check).",
        "Results over-trusted: simulated, not measured. The heat difference is small, and its sign flips between solid and porous crowns.",
        "Big crowns vs winter sun, façades, roots, maintenance, allergies.",
        "Benefits arrive only when trees mature (decades).",
        "Used to justify removing healthy trees.",
    ]),
    ("POTENTIAL INDICATORS", [
        "% sidewalk in summer shade vs city mix (pts)",
        "Δ UTCI, 12–17 h, July day (°C; Ladybug, Honeybee)",
        "Δ runoff, design storm (m³, %)",
        "Agreement: proxy vs Ladybug (r), Python vs Grasshopper (r)",
        "Neighbourhoods where the tool beats the city mix (n / 33)",
    ]),
    ("POTENTIAL INDICATORS", [
        "Streets or projects that use the tool (n)",
        "Design time per street, before vs after (h)",
        "Measured air / surface temperature in pilot streets",
        "Results in Florence and Mataró vs Porta",
        "Designer feedback (interviews, ease of use)",
    ]),
    ("POTENTIAL INDICATORS", [
        "Canopy cover per neighbourhood (LiDAR; Porta 20.1% in 2021 vs 30% target)",
        "Share of the largest species (planes ~27% → ≤15%)",
        "Hours above strong heat stress (UTCI > 32 °C)",
        "Sewer overflows and flood reports in hotspot streets",
        "Cities that adopt the method",
    ]),
]

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
s = prs.slides.add_slide(prs.slide_layouts[6])
W, H = prs.slide_width, prs.slide_height
s.background.fill.solid()
s.background.fill.fore_color.rgb = BG
M = Emu(110000)  # outer margin and gap
foot_h = int(H * 0.085)
colw = (W - 6 * M) // 5
top_h = int((H - foot_h - 3 * M) * 0.505)
bot_h = H - foot_h - 3 * M - top_h


def run(p, text, size, color, bold=False):
    r = p.add_run()
    r.text = text
    r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
    r.font.color.rgb = color


def cell(x, y, w, h, title, items, size, accent):
    card = s.shapes.add_shape(1, x, y, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = C("FFFFFF")
    card.line.color.rgb = GRID
    card.line.width = Pt(0.75)
    card.shadow.inherit = False
    bar = s.shapes.add_shape(1, x, y, w, Emu(55000))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()
    bar.shadow.inherit = False
    tb = s.shapes.add_textbox(x + Emu(50000), y + Emu(70000), w - Emu(100000), h - Emu(110000))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE  # PowerPoint shrinks text if a substitute font is wider
    run(tf.paragraphs[0], title, 11.5, accent, bold=True)
    for it in items:
        p = tf.add_paragraph()
        p.space_before = Pt(3)
        run(p, "• " + it, size, INK)


TOP_ACC = [TREE, TREE, RAIN, RAIN, RAIN]
BOT_ACC = [WARN, HEAT, MUTED, MUTED, MUTED]
for i, (t, items) in enumerate(TOP):
    cell(M + (colw + M) * i, M, colw, top_h, t, items, 9.5, TOP_ACC[i])
for i, (t, items) in enumerate(BOTTOM):
    cell(M + (colw + M) * i, 2 * M + top_h, colw, bot_h, t, items, 9, BOT_ACC[i])

band = s.shapes.add_shape(1, 0, H - foot_h, W, foot_h)
band.fill.solid()
band.fill.fore_color.rgb = DARK
band.line.fill.background()
band.shadow.inherit = False
tb = s.shapes.add_textbox(M + Emu(50000), H - foot_h + Emu(40000), W - 2 * M, foot_h - Emu(60000))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
run(p, "Shade & Sponge · Theory of Change", 12, DARK_INK, bold=True)
run(p, "   choosing replacement street trees for shade and runoff (Barcelona, Porta)", 10.5, DARK_MUTED)
p = tf.add_paragraph()
run(p, "Impact level: short-term = demonstrated early (simulation, 33 neighbourhoods); medium and long term = expected.", 9, DARK_MUTED)

prs.save(sys.argv[1])
