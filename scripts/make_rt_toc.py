from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import sys

ORANGE = RGBColor(0xF2, 0xA0, 0x1F)
NAVY = RGBColor(0x1F, 0x2A, 0x44)
GREY = RGBColor(0x55, 0x55, 0x55)

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
        "Technological: a reproducible method and public code (MIT), with a heat check in Ladybug and Honeybee.",
        "Environmental (simulated): more summer shade than the city's real replacement mix in all 33 neighbourhoods. Ladybug and Honeybee show pedestrian heat stays as with today's planes (within ±0.2 °C UTCI), so the gains are in shade, runoff, species diversity and winter sun.",
        "Knowledge: species and positions chosen against pedestrian heat and runoff together, which the literature reviewed does not do yet.",
    ]),
    ("MEDIUM-TERM OUTCOMES", [
        "Technological: designers and Parcs i Jardins test it on real replacement campaigns or pilot streets.",
        "Replication: transfer to a second Mediterranean city (Florence or Mataró).",
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
        "Result quality in the transfer city",
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
colw = W // 5
top_h = int(H * 0.46)
bot_h = int(H * 0.45)
footer_y = top_h + bot_h


def cell(x, y, w, h, title, items, size):
    shp = s.shapes.add_shape(1, x, y, w, h)
    shp.fill.background()
    shp.line.color.rgb = ORANGE
    shp.line.width = Pt(1.5)
    tb = s.shapes.add_textbox(x + Emu(60000), y + Emu(50000), w - Emu(120000), h - Emu(100000))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = title
    r.font.size, r.font.bold, r.font.name = Pt(12), True, "Arial"
    for it in items:
        p = tf.add_paragraph()
        p.space_before = Pt(2.5)
        r = p.add_run()
        r.text = "• " + it
        r.font.size, r.font.name = Pt(size), "Arial"
        r.font.color.rgb = GREY


for i, (t, items) in enumerate(TOP):
    cell(colw * i, 0, colw, top_h, t, items, 10.5)
for i, (t, items) in enumerate(BOTTOM):
    cell(colw * i, top_h, colw, bot_h, t, items, 10)

foot = s.shapes.add_textbox(Emu(150000), footer_y + Emu(60000), W - Emu(300000), H - footer_y - Emu(100000))
tf = foot.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Shade & Sponge: choosing replacement street trees for shade and runoff (Barcelona, Porta)"
r.font.size, r.font.bold, r.font.name = Pt(11), True, "Arial"
r.font.color.rgb = NAVY
p = tf.add_paragraph()
r = p.add_run()
r.text = ("Impact level: short-term = demonstrated early (simulation, 33 neighbourhoods); medium and long term = expected."
          "")
r.font.size, r.font.name = Pt(9), "Arial"
r.font.color.rgb = GREY

prs.save(sys.argv[1])
