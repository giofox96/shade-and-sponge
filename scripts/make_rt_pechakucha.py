"""Build the RT final-assignment Pecha Kucha deck (15 slides, 20 s each).

Spoken script = speaker notes, read from slides/rt_pechakucha/pitch_script.md.
Figures are reused from slides/fig, fig_v6, fig_v7.
"""
import re
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "slides"
OUT = S / "rt_pechakucha" / "shade_and_sponge_pechakucha.pptx"
BG, INK, MUTED = RGBColor(0xEF, 0xED, 0xE7), RGBColor(0x22, 0x22, 0x22), RGBColor(0x6B, 0x6B, 0x6B)
GREEN, BROWN, BLUE, GOLD = (RGBColor(0x3E, 0x6B, 0x45), RGBColor(0x6E, 0x3B, 0x24),
                            RGBColor(0x24, 0x3B, 0x6B), RGBColor(0x9A, 0x7A, 0x2E))
W, H = Emu(12192000), Emu(6858000)
FONT = "Inter"

says = re.findall(r'\*\*Say:\*\* "(.*?)"\n', (S / "rt_pechakucha" / "pitch_script.md").read_text(encoding="utf-8"))
assert len(says) == 15
prs = Presentation()
prs.slide_width, prs.slide_height = W, H


def new(i):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = BG
    sl.notes_slide.notes_text_frame.text = says[i]
    return sl


def text(sl, x, y, w, h, s, size=28, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = tb.text_frame
    tf.word_wrap, tf.vertical_anchor = True, anchor
    for k, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, color, FONT
    return tb


def box(sl, x, y, w, h, fill, title, body, tsize=22, bsize=16):
    sh = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    text(sl, x + 150000, y + 120000, w - 300000, h - 240000, title, tsize, True, RGBColor(255, 255, 255))
    text(sl, x + 150000, y + 1150000, w - 300000, h - 1300000, body, bsize, False, RGBColor(255, 255, 255))


def figure(i, rel):
    sl = new(i)
    im = Image.open(S / rel)
    r = min(W / im.width, H / im.height)
    w, h = int(im.width * r), int(im.height * r)
    sl.shapes.add_picture(str(S / rel), Emu((W - w) // 2), Emu((H - h) // 2), Emu(w), Emu(h))
    return sl


def statement(i, kicker, s, size=40):
    sl = new(i)
    text(sl, 700000, 600000, 10800000, 500000, kicker, 20, True, GREEN)
    text(sl, 700000, 1300000, 10800000, 4800000, s, size, True, INK, anchor=MSO_ANCHOR.MIDDLE)
    return sl


M = 600000  # margin
# 1 hook
sl = new(0)
photo = S / "fig" / "01_title_photo.webp"
png = S / "rt_pechakucha" / "title_photo.jpg"
im = Image.open(photo).convert("RGB")
cw = int(im.height * (W // 2 + 400000) / H)
im.crop(((im.width - cw) // 2, 0, (im.width + cw) // 2, im.height)).save(png)
sl.shapes.add_picture(str(png), 0, 0, W // 2 + 400000, H)
text(sl, W // 2 + 700000, 1300000, 5300000, 1000000, "Shade & Sponge", 44, True)
text(sl, W // 2 + 800000, 2700000, 5000000, 1600000, "Barcelona is replacing its plane trees.\nWhich tree goes back, and where?", 26, False, MUTED)
text(sl, W // 2 + 800000, 5600000, 5000000, 600000, "MaCAD thesis · IAAC 2026", 16, False, MUTED)
# 2-3 context figures
figure(1, "fig_v7/v7_02_context.png")
figure(2, "fig/04_why_porta.png")
# 4 gap
statement(3, "THE GAP", "The city fixes how many of each species.\nNobody decides which species where,\nand nobody measures what it does\nto heat or runoff.")
# 5-6
figure(4, "fig_v6/v6_04_crowns.png")
figure(5, "fig/09_gap_matrix.png")
# 7 RQ
statement(6, "RESEARCH QUESTION", "Can a trait-based layout method, inside Barcelona's tree rules, choose replacement species and new spots that keep more pedestrian cooling and storm-water interception than the city's own practice?", 32)
# 8 tool
figure(7, "fig_v7/flow_00_overview.png")
# 9 innovation
sl = new(8)
text(sl, M, 450000, 11000000, 700000, "Innovation: the city's rules are inside the tool", 34, True)
cw = (W - 2 * M - 2 * 250000) // 3
for k, (c, t, b) in enumerate([
        (GREEN, "Two services, one choice", "Species and position for every tree, scored on summer shade / UTCI and runoff together."),
        (BROWN, "Rules inside, not after", "15% species cap, sidewalk width → tree size, a palette of 30 allowed species."),
        (BLUE, "Real baseline, any city", "Compared with the city's own replacement mix. One data adapter per site: open data in, layout out.")]):
    box(sl, M + k * (cw + 250000), 1600000, cw, 4200000, c, t, b, 24, 20)
# 10 evidence
figure(9, "fig_v7/res_04_city_map.png")
# 11 actors
sl = new(10)
text(sl, M, 450000, 11000000, 700000, "Actors", 34, True)
cw = (W - 2 * M - 3 * 200000) // 4
for k, (c, t, b) in enumerate([
        (BROWN, "Decide", "Parcs i Jardins\nAjuntament de Barcelona\n(tree master plan, 15% cap)"),
        (GREEN, "Use", "Landscape architects\nComputational designers\nUrban planners"),
        (BLUE, "Data & testing", "ICGC (LiDAR) · BCASA (drainage)\nLadybug / Honeybee check\nInfrared City (in contact)\nComune di Firenze (LiDAR, transfer)"),
        (GOLD, "Benefit", "Residents and pedestrians\nin streets that are both hot and flood-prone")]):
    box(sl, M + k * (cw + 200000), 1600000, cw, 4200000, c, t, b, 24, 17)
# 12 exploitation
sl = new(11)
text(sl, M, 450000, 11000000, 700000, "Exploitation: what, how, for whom", 34, True)
rows = [("What", "How", "For whom"),
        ("Method (trait-based layout under city rules)", "Thesis, paper", "Researchers, city technicians"),
        ("Python core + web app", "Open source (MIT), online", "Designers, other cities"),
        ("Per-tree crown and trait dataset", "Open data (CC BY, own data only)", "City, researchers"),
        ("Transfer guide", "Florence / Mataró test", "Cities replacing a monoculture")]
tbl = sl.shapes.add_table(len(rows), 3, Emu(M), Emu(1600000), Emu(W - 2 * M), Emu(3800000)).table
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        cell = tbl.cell(r, c)
        cell.text = v
        f = cell.text_frame.paragraphs[0].runs[0].font
        f.size, f.bold, f.name = Pt(20), r == 0, FONT
        cell.fill.solid()
        cell.fill.fore_color.rgb = GREEN if r == 0 else RGBColor(0xF8, 0xF7, 0xF3)
        f.color.rgb = RGBColor(255, 255, 255) if r == 0 else INK
# 13 impact time
sl = new(12)
text(sl, M, 450000, 11000000, 700000, "Impact over time", 34, True)
cw = (W - 2 * M - 2 * 250000) // 3
for k, (c, t, b) in enumerate([
        (GREEN, "Short term · now", "Open, reproducible method\nSimulated gains in 28 neighbourhoods\nChecked in Ladybug / Honeybee"),
        (BLUE, "Medium term · 1–3 yrs", "Pilot streets with Parcs i Jardins\nTransfer test: Florence, Mataró"),
        (BROWN, "Long term · 2037", "Canopy toward 30%, no species above 15%\nLess runoff in flood hotspots\nA method for cities replacing monocultures")]):
    box(sl, M + k * (cw + 250000), 1600000, cw, 4200000, c, t, b, 24, 20)
# 14 dimensions + TRL
sl = new(13)
text(sl, M, 450000, 11000000, 700000, "Impact dimensions · Technology readiness", 34, True)
dims = ["Environmental", "Social", "Technological", "Economic", "Policy"]
dw = (W - 2 * M - 4 * 150000) // 5
for k, d in enumerate(dims):
    sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(M + k * (dw + 150000)), Emu(1400000), Emu(dw), Emu(700000))
    sh.fill.solid()
    sh.fill.fore_color.rgb = GREEN
    sh.line.fill.background()
    sh.text_frame.text = d
    f = sh.text_frame.paragraphs[0].runs[0].font
    f.size, f.bold, f.name, f.color.rgb = Pt(18), True, FONT, RGBColor(255, 255, 255)
    sh.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
tw = (W - 2 * M) // 9
for n in range(1, 10):
    fill = GREEN if n <= 4 else (GOLD if n == 5 else RGBColor(0xD6, 0xD3, 0xCB))
    sh = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(M + (n - 1) * tw), Emu(3100000), Emu(tw - 60000), Emu(900000))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.text_frame.text = str(n)
    f = sh.text_frame.paragraphs[0].runs[0].font
    f.size, f.bold, f.name = Pt(28), True, FONT
    f.color.rgb = RGBColor(255, 255, 255) if n <= 5 else MUTED
    sh.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
text(sl, M, 2600000, 4000000, 450000, "TRL", 20, True, MUTED)
text(sl, M, 4150000, 4 * tw, 1500000, "TRL 4 by December\nvalidated in simulation, on real city data", 18, True, GREEN)
text(sl, M + 4 * tw, 4150000, 2 * tw, 1500000, "TRL 5\na test with a real designer", 18, True, GOLD)
text(sl, M + 6 * tw, 4150000, 3 * tw, 1500000, "TRL 6+\na pilot street, after the thesis", 18, True, MUTED)
# 15 close
statement(14, "SHADE & SPONGE", "Replace trees with the least loss,\ninside the city's own rules.", 44)
text(prs.slides[14], 700000, 5600000, 10800000, 500000, "giofox96.github.io/shade-and-sponge", 20, False, MUTED)

prs.save(OUT)
print(OUT)
