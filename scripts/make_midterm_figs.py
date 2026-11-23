"""Figures for the 24 Nov midterm Pecha Kucha (thesis studio, 5 min): method with the four actions per tree, city rules
sketch, "a crown is a bucket", "the tree on the hill" and the free-spot classes. Same style and helpers as the RM personal deck.
Numbers: notes/tutor_feedback_17nov.md §1c, §9d, §10; notes/tutor_feedback_10nov.md (position test, 17 Nov).
Run from scripts/: python make_midterm_figs.py   (needs cairosvg, Node Playwright)
"""
from make_rm_personal_figs import svg, page, arrows, tint, render, ROOT, INK, MUTED, BG, HEAT, RAIN, TREE, WARN
import make_rm_personal_figs as F

FIG = ROOT / "slides/midterm/fig"
FIG.mkdir(parents=True, exist_ok=True)
F.FIG = FIG
FIRE = "#D9622B"


def label(x, y, t, c=MUTED):
    return f'<div class="k" style="position:absolute;left:{x}px;top:{y}px;color:{c}">{t}</div>'


def method_actions():
    """Four steps; the four actions are the designer's input, the optimiser fills Replace and Add positions."""
    h = 600
    b = arrows(["M455 320H500", "M865 320H910", "M1235 320H1275"], h)
    b += label(30, 14, "1 · Screening") + label(510, 14, "2 · Designer decides") + label(920, 14, "3 · Optimiser") + label(1285, 14, "4 · Compare")
    rows = [(TREE, ("tree-deciduous",), "What stands there", "species · crown · leaves"),
            (WARN, ("map-pin", "ruler"), "Where it is", "sidewalk · objects · flood route"),
            (HEAT, ("sun", "snowflake", "cloud-rain"), "What 30 species would do", "summer shade · winter shade · rain held")]
    for k, (c, ics, t, s) in enumerate(rows):
        y = 60 + k * 180
        b += (f'<div class="n" style="left:30px;top:{y}px;width:425px;height:160px;background:{tint(c, .12)}">'
              f'<div class="row">{"".join(svg(i, c, 40) for i in ics)}</div><div class="t" style="color:{c};font-size:28px">{t}</div>'
              f'<div class="s" style="font-size:21px">{s}</div></div>')
    acts = [(TREE, "tree-deciduous", "Keep"), (WARN, "move", "Move"), (HEAT, "refresh-ccw", "Replace"), (RAIN, "circle-plus", "Add")]
    for k, (c, i, t) in enumerate(acts):
        x, y = 510 + (k % 2) * 180, 60 + (k // 2) * 150
        b += (f'<div class="n" style="left:{x}px;top:{y}px;width:165px;height:135px;background:{tint(c, .14)};align-items:center">'
              f'{svg(i, c, 44)}<div class="t" style="color:{c};font-size:28px">{t}</div></div>')
    b += (f'<div class="n" style="left:510px;top:375px;width:345px;height:205px;background:#FBFAF6;border:2px dashed {MUTED}">'
          f'<div class="s" style="font-size:21px"><b style="color:{INK}">per tree, with a reason:</b> dead · diseased · '
          f'dangerous · roots · works</div><div class="s" style="font-size:21px"><b style="color:{INK}">never</b> remove '
          f'without replacing</div></div>')
    b += (f'<div class="n" style="left:910px;top:60px;width:325px;height:520px;background:{tint(INK, .08)};align-items:center;text-align:center">'
          f'{svg("target", INK, 60)}<div class="t">Picks the species</div><div class="s">for every <b style="color:{HEAT}">Replace</b> '
          f'and <b style="color:{RAIN}">Add</b></div><div class="s">best layout, proven</div>'
          f'<div class="row" style="flex-direction:column;gap:8px;margin-top:10px">'
          f'<span class="chip">{svg("lock", MUTED, 18)}15% per species</span><span class="chip">{svg("lock", MUTED, 18)}sidewalk → size</span>'
          f'<span class="chip">{svg("lock", MUTED, 18)}distances to objects</span></div></div>')
    b += (f'<div class="n" style="left:1275px;top:60px;width:300px;height:520px;background:#FBFAF6;border:2px solid {INK};gap:22px;justify-content:center">'
          f'<div class="row">{svg("git-compare", INK, 34)}<div class="t" style="font-size:27px">vs today<br>vs city practice</div></div>'
          f'<div class="row">{svg("sun", HEAT, 30)}<div class="s" style="font-size:22px">summer shade, UTCI</div></div>'
          f'<div class="row">{svg("snowflake", HEAT, 30)}<div class="s" style="font-size:22px">winter sun</div></div>'
          f'<div class="row">{svg("droplets", RAIN, 30)}<div class="s" style="font-size:22px">runoff: never worse</div></div>'
          f'<div class="row">{svg("trees", TREE, 30)}<div class="s" style="font-size:22px">canopy cover</div></div></div>')
    return page(b, h), h


def rules_sketch():
    """Plan view of four sidewalks: width -> tree size class and spacing (2011 street-tree guide pp. 22-23)."""
    h, x0, x1 = 760, 330, 1560
    b = ""
    cases = [("< 2.5 m", "no tree", 0, None), ("2.5–3.5 m", "small · every 7 m", 22, 7), ("3.5–6 m", "medium · every 9 m", 34, 9),
             ("> 6 m", "large · every 13 m", 50, 13)]
    y = 20
    for lab, sub, r, sp in cases:
        hh = 62 + 2 * r
        b += (f'<div style="position:absolute;left:{x0}px;top:{y}px;width:{x1 - x0}px;height:{hh}px;background:#E6E1D6;'
              f'border-top:5px solid {INK};border-bottom:3px dashed {MUTED}"></div>')
        b += (f'<div style="position:absolute;left:30px;top:{y}px;width:280px;height:{hh}px;display:flex;flex-direction:column;justify-content:center">'
              f'<div class="t" style="font-size:30px">{lab}</div><div class="s" style="font-size:21px;color:{TREE if r else HEAT}">{sub}</div></div>')
        if sp:
            step = sp * 12
            cx = x0 + 60
            while cx + r < x1:
                cy = y + 5 + hh - 14 - r
                b += (f'<div style="position:absolute;left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;'
                      f'background:{tint(TREE, .55)};border:2px solid {TREE}"></div>')
                cx += step
        else:
            b += (f'<div class="s" style="position:absolute;left:{x0 + 30}px;top:{y + 14}px;font-size:22px;color:{HEAT}">'
                  f'too narrow: kept free for walking</div>')
        y += hh + 58
    b += (f'<div class="row" style="position:absolute;left:{x0}px;top:{y + 6}px;gap:28px;font-size:20px;color:{MUTED}">'
          f'<span>▬ façade</span><span>┄ kerb</span><span>● crown at maturity, 0.7 m from the kerb</span></div>')
    return page(b, h), h


def bucket():
    """1 mm on 1 m² = 1 litre; Celtis crown 6.3 m (31 m²), s·LAI ≈ 4 mm -> ≈125 L held of ≈1,000 L in the T2-60 storm."""
    h = 560
    b = ""
    for k in range(22):
        x = 160 + k * 26
        b += f'<div style="position:absolute;left:{x}px;top:{20 + (k % 3) * 14}px;width:3px;height:44px;background:{RAIN};opacity:.55;transform:rotate(12deg)"></div>'
    b += (f'<div style="position:absolute;left:150px;top:120px;width:560px;height:200px;border-radius:50%;background:{tint(TREE, .6)};'
          f'border:3px solid {TREE}"></div><div style="position:absolute;left:418px;top:300px;width:24px;height:200px;background:#6B5640"></div>'
          f'<div style="position:absolute;left:40px;top:500px;width:780px;height:6px;background:{INK}"></div>')
    b += (f'<div class="t" style="position:absolute;left:250px;top:180px;width:360px;text-align:center;color:{BG}">≈ 125 L held</div>')
    stats = [(RAIN, "cloud-rain", "≈ 1,000 L", "fall on the crown (31.9 mm in 1 h, 2-year storm)"),
             (TREE, "tree-deciduous", "≈ 125 L", "stay on the leaves: 1.75 mm × leaf area index ≈ 4 mm"),
             (MUTED, "droplets", "≈ 875 L", "reach the ground")]
    for k, (c, i, big, small) in enumerate(stats):
        y = 40 + k * 150
        b += (f'<div class="n" style="left:880px;top:{y}px;width:690px;height:130px;background:{tint(c, .12)}">'
              f'<div class="row">{svg(i, c, 40)}<div class="t" style="color:{c};font-size:38px">{big}</div></div>'
              f'<div class="s" style="font-size:22px">{small}</div></div>')
    b += (f'<div class="n" style="left:880px;top:490px;width:690px;height:56px;background:{INK};color:{BG};border-radius:999px;align-items:center">'
          f'<div class="t" style="font-size:25px">1 mm of rain on 1 m² = 1 litre</div></div>')
    return page(b, h), h


def hill():
    """Same tree, same water held; only position decides whether that water would have reached the flood spot."""
    h = 600
    ground = "M0 150 C300 160 500 250 800 330 S1250 430 1600 440 L1600 600 L0 600 Z"
    b = (f'<svg class="e" width="1600" height="{h}"><path d="{ground}" fill="#E6E1D6" stroke="{INK}" stroke-width="4"/>'
         f'<ellipse cx="1380" cy="440" rx="170" ry="26" fill="{RAIN}" opacity=".75"/>'
         f'<path d="M330 205 C560 260 900 360 1250 425" fill="none" stroke="{RAIN}" stroke-width="5" stroke-dasharray="14 10"/>'
         f'<path d="M1250 425 l-22 -14 l4 22 z" fill="{RAIN}"/></svg>')
    b += (f'<div style="position:absolute;left:250px;top:80px;width:150px;height:95px;border-radius:50%;background:{tint(TREE, .6)};border:3px solid {TREE}"></div>'
          f'<div style="position:absolute;left:318px;top:170px;width:12px;height:30px;background:#6B5640"></div>')
    b += (f'<div class="n" style="left:40px;top:250px;width:520px;height:120px;background:{tint(TREE, .14)}">'
          f'<div class="t" style="color:{TREE};font-size:27px">Upstream of the flood spot</div>'
          f'<div class="s" style="font-size:21px">its ≈125 L never reach the hotspot</div></div>')
    b += (f'<div class="n" style="left:1210px;top:480px;width:360px;height:100px;background:{tint(RAIN, .14)}">'
          f'<div class="t" style="color:{RAIN};font-size:27px">Flood hotspot</div><div class="s" style="font-size:20px">collects the water from upslope</div></div>')
    b += (f'<div class="n" style="left:640px;top:20px;width:930px;height:200px;background:#FBFAF6;border:2px solid {INK}">'
          f'<div class="row"><span class="chip"><b>74%</b> of Porta\'s tree positions drain to no hotspot</span></div>'
          f'<div class="row"><span class="chip"><b>× 5.6</b> water kept from hotspots: 100 trees placed by the method vs at random</span></div>'
          f'<div class="row"><span class="chip" style="border:2px dashed {HEAT}"><b style="color:{HEAT}">0.5%</b> of the hotspot water → a do-no-harm check</span></div></div>')
    return page(b, h), h


def spots():
    """Free planting spots in Porta by class (decided 18 Nov): 267 candidates."""
    h = 470
    total, x0, wmax = 267, 40, 1520
    parts = [(153, "Free", "plant", TREE), (103, "Conditional", "move a sign, crossing, lamp, bollard or bus stop · field check", WARN),
             (11, "Blocked", "traffic lights (incl. crossings within 3 m of one), driveways", HEAT)]
    b = (f'<div class="t" style="position:absolute;left:{x0}px;top:10px;font-size:30px">267 candidate spots '
         f'<span class="s">(sidewalk ≥ 2.5 m, spacing by size)</span></div>')
    x = x0
    for n, lab, sub, c in parts:
        w = wmax * n / total
        b += (f'<div style="position:absolute;left:{x}px;top:70px;width:{w - 6}px;height:120px;background:{c};border-radius:10px;'
              f'display:flex;align-items:center;justify-content:center;color:{BG};font-size:44px;font-weight:700">{n}</div>')
        x += w
    for k, (n, lab, sub, c) in enumerate(parts):
        y = 220 + k * 80
        b += (f'<div class="row" style="position:absolute;left:{x0}px;top:{y}px"><div style="width:26px;height:26px;border-radius:6px;background:{c}"></div>'
              f'<div class="t" style="font-size:30px;color:{c}">{lab}</div><div class="s" style="font-size:24px">{sub}</div></div>')
    return page(b, h), h


if __name__ == "__main__":
    render("method_actions", method_actions())
    render("rules_sketch", rules_sketch())
    render("bucket", bucket())
    render("hill", hill())
    render("spots", spots())
