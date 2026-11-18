"""Figures for the RM personal deck (v3, 18 Nov): state of the art + gap flow, method + screening flow, and coloured icon PNGs.
Icons: Lucide (ISC licence, slides/rm_final/icons/). Diagrams are HTML rendered to PNG with Node Playwright (2x).
Run from scripts/: python make_rm_personal_figs.py   (needs cairosvg)
"""
import re
import subprocess
from pathlib import Path
import cairosvg
from make_infographics import ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN

IC = ROOT / "slides/rm_final/icons"
FIG = ROOT / "slides/rm_final/fig"


def svg(name, color, size=28, sw=2):
    s = (IC / f"{name}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S).replace('class="', 'data-c="')
    return (s.replace('stroke="currentColor"', f'stroke="{color}"').replace('width="24"', f'width="{size}"')
             .replace('height="24"', f'height="{size}"').replace('stroke-width="2"', f'stroke-width="{sw}"'))


def icon_png(name, color, px=256):
    out = IC / "png" / f"{name}_{color.lstrip('#')}.png"
    out.parent.mkdir(exist_ok=True)
    if not out.exists():
        cairosvg.svg2png(bytestring=svg(name, color, 24, 1.8).encode(), write_to=str(out), output_width=px, output_height=px)
    return out


CSS = f"""<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>
body{{margin:0;width:1600px;height:HPX;background:{BG};font-family:"IBM Plex Sans",Arial,sans-serif;color:{INK};position:relative;overflow:hidden}}
.n{{position:absolute;box-sizing:border-box;padding:16px 22px;border-radius:14px;display:flex;flex-direction:column;justify-content:center;gap:6px}}
.k{{font-size:17px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.t{{font-size:31px;font-weight:600;line-height:1.25}}
.s{{font-size:25px;color:{MUTED}}}
.r{{font-size:19px;font-style:italic;color:{MUTED}}}
.row{{display:flex;align-items:center;gap:12px}}
.chip{{display:inline-flex;align-items:center;gap:6px;background:{BG};border:1.5px solid #A8A293;border-radius:999px;padding:5px 14px;font-size:21px;color:{MUTED};white-space:nowrap}}
.chip b{{font-size:28px;color:{INK}}}
svg.e{{position:absolute;left:0;top:0}}
</style>"""


def page(body, h):
    return "<!doctype html><html><head><meta charset='utf-8'>" + CSS.replace("HPX", f"{h}px") + "</head><body>" + body + "</body></html>"


def arrows(paths, h, color="#A8A293"):
    m = (f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0L10 5L0 10z" fill="{color}"/></marker></defs>')
    return (f'<svg class="e" width="1600" height="{h}">' + m +
            "".join(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#a)"/>' for d in paths) + "</svg>")


def tint(h, op):
    a, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)], [int(BG[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(op * x + (1 - op) * y):02X}" for x, y in zip(a, b))


def gap_flow():
    h = 640
    b = arrows(["M400 230V318", "M1200 230V318", "M800 486V540"], h)
    for x, c, ics, k, t, s, r in [
            (40, RAIN, ("flame", "droplets"), "Heat + runoff models", "Both services", "✕ no choice of species",
             "Mannucci et al. 2025 · Wu et al. 2024"),
            (840, WARN, ("sliders-horizontal", "tree-deciduous"), "Species tools", "Optimisers, rankings, recommenders",
             "✕ one service, or no positions", "Shaamala 2025 · Peng 2026 · Dong 2026 · Nicol 2026 (SylvCiT)")]:
        b += (f'<div class="n" style="left:{x}px;top:20px;width:720px;height:210px;background:{tint(c, .12)}">'
              f'<div class="row">{"".join(svg(i, c, 40) for i in ics)}<div class="k" style="color:{c}">{k}</div></div>'
              f'<div class="t">{t}</div><div class="t" style="color:{HEAT}">{s}</div><div class="r">{r}</div></div>')
    b += (f'<div class="n" style="left:120px;top:322px;width:1360px;height:164px;background:#FBFAF6;border:3px dashed {HEAT};'
          f'align-items:center;text-align:center"><div class="k" style="color:{HEAT}">Gap</div>'
          f'<div class="t">No method picks the species tree by tree, on heat and runoff, inside a city\'s rules</div>'
          f'<div class="row" style="font-size:21px;color:{MUTED}">Of tools that place or assess urban trees:'
          f'<span class="chip"><b>18</b></span>→<span class="chip"><b>7</b>heat + runoff</span>→'
          f'<span class="chip"><b>1</b>picks species</span>→'
          f'<span class="chip" style="border:2px dashed {HEAT}"><b style="color:{HEAT}">0</b>per tree, inside city rules</span></div></div>')
    b += (f'<div class="n" style="left:220px;top:544px;width:1160px;height:76px;background:#283F2A;color:{BG};border-radius:999px;'
          f'align-items:center"><div class="row">{svg("circle-check", BG, 32)}<div class="t">This method: species and position per tree, '
          f'inside the city\'s rules</div></div></div>')
    return page(b, h), h


def method_flow():
    h = 570
    b = arrows(["M700 295H770", "M1110 295H1170"], h)
    b += f'<div class="k" style="position:absolute;left:40px;top:14px;color:{MUTED}">1 · Screening, once per tree and free spot</div>'
    rows = [(TREE, ("tree-deciduous",), "What stands there", "species · crown · leaf density (LiDAR)"),
            (WARN, ("map-pin", "ruler"), "Where it is", "sidewalk width · lamps, signs · drains to a flood spot?"),
            (HEAT, ("sun", "snowflake", "cloud-rain"), "What 30 species would do", "summer shade + · winter shade − · rain held +")]
    for k, (c, ics, t, s) in enumerate(rows):
        y = 50 + k * 172
        b += (f'<div class="n" style="left:40px;top:{y}px;width:660px;height:152px;background:{tint(c, .12)}">'
              f'<div class="row">{"".join(svg(i, c, 46) for i in ics)}<div class="t" style="color:{c}">{t}</div></div>'
              f'<div class="s">{s}</div></div>')
    b += f'<div class="k" style="position:absolute;left:780px;top:14px;color:{MUTED}">2 · Choose</div>'
    b += (f'<div class="n" style="left:770px;top:110px;width:350px;height:370px;background:{tint(INK, .08)};align-items:center;text-align:center">'
          f'{svg("target", INK, 64)}<div class="t">Exact optimiser</div><div class="s">best layout, proven</div>'
          f'<div class="row" style="flex-wrap:wrap;justify-content:center;gap:8px;margin-top:8px">'
          f'<span class="chip">{svg("lock", MUTED, 18)}15% per species</span><span class="chip">{svg("lock", MUTED, 18)}sidewalk → size</span>'
          f'</div></div>')
    b += f'<div class="k" style="position:absolute;left:1180px;top:14px;color:{MUTED}">3 · Out, and compared</div>'
    acts = [(TREE, "tree-deciduous", "Keep"), (WARN, "move", "Move"), (HEAT, "refresh-ccw", "Replace"), (RAIN, "circle-plus", "Add")]
    for k, (c, i, t) in enumerate(acts):
        x, y = 1180 + (k % 2) * 200, 50 + (k // 2) * 140
        b += (f'<div class="n" style="left:{x}px;top:{y}px;width:180px;height:120px;background:{tint(c, .12)};align-items:center">'
              f'{svg(i, c, 44)}<div class="t" style="color:{c}">{t}</div></div>')
    b += (f'<div class="n" style="left:1170px;top:330px;width:400px;height:210px;background:#FBFAF6;border:2px solid {INK}">'
          f'<div class="row">{svg("git-compare", INK, 36)}<div class="t">vs today,<br>vs city practice</div></div>'
          f'<div class="row">{svg("thermometer-sun", HEAT, 30)}<div class="s">UTCI check: Ladybug, Infrared City</div></div>'
          f'<div class="row">{svg("droplets", RAIN, 30)}<div class="s">runoff: never worse</div></div></div>')
    return page(b, h), h


def render(name, html_h):
    html, h = html_h
    src = FIG / f"{name}.html"
    src.write_text(html, encoding="utf-8")
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();"
          f"const p=await b.newPage({{viewport:{{width:1600,height:{h}}},deviceScaleFactor:2}});"
          f"await p.goto('file://{src.as_posix()}');await p.waitForTimeout(1500);"
          f"await p.screenshot({{path:'{(FIG / f'{name}.png').as_posix()}'}});await b.close();}})();")
    subprocess.run(["node", "-e", js], check=True)
    print("wrote", (FIG / f"{name}.png").relative_to(ROOT))


if __name__ == "__main__":
    render("gap_flow", gap_flow())
    render("method_flow", method_flow())
