"""First Porta results for the 10 Nov deck (replacement scenarios; RQ v7, notes/topic_decision.md §10.5-10.6).
Input: databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv
       (python -m shade_sponge porta --size=exact --trunk=TERCERA). Output: slides/fig_v7/res_*.svg + .png.
Radar: each indicator normalised to today (S0 = 100, outward = better), read axis by axis (no area meaning).
Bars: the same indicators in real units, as differences from S1a (the city's rule), with the model threshold Δmin.
Run from scripts/: python make_results_v7.py
"""
import math
import pandas as pd
import make_infographics as mi
from make_infographics import t, rect, save, ROOT, INK, MUTED, GRID, HEAT, RAIN, TREE, WARN

mi.OUT = ROOT / "slides/fig_v7"
d = pd.read_csv(ROOT / "databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv").set_index("scenario")
BAL = "S4_s0.50_w0.25_r0.25"            # balanced weights: summer 0.5, winter 0.25, hotspot runoff 0.25
s1a = d[d.index.str.startswith("S1a_city")]
ROWS = {"S0": d.loc["S0_current"], "S1a": s1a.mean(), "Opt": d.loc[BAL]}
COL = {"S0": MUTED, "S1a": WARN, "Opt": TREE}
NAME = {"S0": "Today (S0)", "S1a": "City rule (S1a, mean of 10)", "Opt": "Optimised (balanced)"}
DMIN = 91.0                               # m³, notes/decisions/runoff_metric_sensitivity.md §10
# (label, column, +1 if more is better, colour)
IND = [("Summer shade", "shade_summer_m2h", 1, HEAT), ("Winter sun", "shade_winter_m2h", -1, HEAT),
       ("Total runoff", "runoff_m3", -1, RAIN), ("Hotspot runoff", "runoff_hot_m3", -1, RAIN),
       ("Canopy cover", "canopy_pct", 1, TREE)]


def score(r, col, sign):
    s0 = ROWS["S0"][col]
    return 100 * (r[col] / s0 if sign > 0 else s0 / r[col])


def fig_radar():
    cx, cy, R, lo, hi = 560, 500, 290, 80, 105
    rad = lambda v: R * (v - lo) / (hi - lo)
    ang = [2 * math.pi * k / len(IND) for k in range(len(IND))]
    xy = lambda a, r: (cx + r * math.sin(a), cy - r * math.cos(a))
    b = ""
    for v in (85, 90, 95, 100, 105):
        pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in (xy(a, rad(v)) for a in ang))
        b += f'<polygon points="{pts}" fill="none" stroke="{INK if v == 100 else GRID}" stroke-width="{2 if v == 100 else 1.2}"/>'
        b += t(cx + 6, cy - rad(v) - 4, f"{v}", 13, MUTED)
    for (lab, _, _, c), a in zip(IND, ang):
        x, y = xy(a, R + 40)
        b += f'<line x1="{cx}" y1="{cy}" x2="{xy(a, R)[0]:.0f}" y2="{xy(a, R)[1]:.0f}" stroke="{GRID}"/>'
        b += t(x, y + 6, lab, 19, c, "bold", "middle")
    for k in ("S0", "S1a", "Opt"):
        pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in (xy(a, rad(max(lo, score(ROWS[k], col, s))))
                                                      for (_, col, s, _), a in zip(IND, ang)))
        b += f'<polygon points="{pts}" fill="{COL[k]}" fill-opacity="{0.08 if k == "S0" else 0.22}" stroke="{COL[k]}" stroke-width="3"/>'
    y = 300
    for k in ("S0", "S1a", "Opt"):
        b += rect(980, y - 16, 22, 22, COL[k], rx=4) + t(1014, y + 2, NAME[k], 20)
        y += 40
    y += 20
    for lab, col, s, c in IND:
        b += t(980, y, lab, 17, c, "bold") + t(1200, y, f"S1a {score(ROWS['S1a'], col, s):.1f}", 17, WARN)
        b += t(1330, y, f"Opt {score(ROWS['Opt'], col, s):.1f}", 17, TREE)
        y += 30
    b += t(980, y + 30, "100 = today. Outward = better. Read axis by axis:", 16, MUTED)
    b += t(980, y + 54, "the polygon's area means nothing.", 16, MUTED)
    save("res_01_radar", "First results: replacing Porta's 832 plane trees",
         "The optimised layout keeps almost all of today's summer shade; the city's rule loses about an eighth", b,
         "databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv (python -m shade_sponge porta --size=exact --trunk=TERCERA). "
         "Heat = effective-shade proxy, not yet UTCI. Runoff: T2-60 storm, season-weighted. Traits at equal trunk size (TERCERA; Pyrus SEGONA). "
         "S1a = 2026 mix (press) placed at random within the sidewalk sizing rule, 10 seeds. Canopy = crown-disc model, compare between layouts only.")


def fig_bars():
    panels = [("Summer shade", "shade_summer_m2h", "thousand m²·h", 1e-3, HEAT, None),
              ("Winter shade (a cost)", "shade_winter_m2h", "thousand m²·h", 1e-3, HEAT, None),
              ("Total runoff", "runoff_m3", "m³", 1, RAIN, DMIN),
              ("Hotspot runoff", "runoff_hot_m3", "m³", 1, RAIN, None),
              ("Canopy cover", "canopy_pct", "percentage points", 1, TREE, None)]
    b, pw = "", 280
    for i, (lab, col, unit, k, c, thr) in enumerate(panels):
        x0 = 70 + i * (pw + 20)
        base = ROWS["S1a"][col]
        vals = {n: (ROWS[n][col] - base) * k for n in ("S0", "Opt")}
        lo_, hi_ = (s1a[col].min() - base) * k, (s1a[col].max() - base) * k
        m = max(abs(v) for v in list(vals.values()) + [lo_, hi_, (thr or 0)]) * 1.15
        y0, hh = 520, 230                                  # zero line, half height
        sc = lambda v: y0 - v / m * hh
        b += t(x0, 200, lab, 20, c, "bold") + t(x0, 224, f"difference from S1a, {unit}", 14, MUTED)
        if thr:
            b += rect(x0, sc(thr), pw - 20, sc(-thr) - sc(thr), RAIN, rx=0, op=0.10)
            b += t(x0 + pw - 24, sc(thr) - 6, f"± Δmin = {thr:.0f} m³: not resolved", 13, RAIN, anchor="end")
        b += f'<line x1="{x0}" y1="{y0}" x2="{x0 + pw - 20}" y2="{y0}" stroke="{INK}" stroke-width="1.5"/>'
        b += f'<line x1="{x0 + 50}" y1="{sc(lo_):.0f}" x2="{x0 + 50}" y2="{sc(hi_):.0f}" stroke="{WARN}" stroke-width="10"/>'
        b += t(x0 + 50, y0 + hh + 40, "S1a", 15, WARN, "bold", "middle") + t(x0 + 50, y0 + hh + 58, "range", 13, MUTED, anchor="middle")
        for j, n in enumerate(("S0", "Opt")):
            xc, v = x0 + 130 + j * 90, vals[n]
            b += rect(xc - 28, min(sc(v), y0), 56, abs(sc(v) - y0), COL[n], rx=3)
            b += t(xc, sc(v) + (-10 if v >= 0 else 24), f"{v:+,.1f}" if k == 1 else f"{v:+,.0f}", 15, INK, "bold", "middle")
            b += t(xc, y0 + hh + 40, "Today" if n == "S0" else "Optimised", 15, COL[n], "bold", "middle")
    save("res_02_bars", "The same results in real units, against the city's rule",
         "Heat separates clearly; runoff differences stay below what the model can resolve (inside ±Δmin)", b,
         "databases/barcelona/tool_v0_summary_sizeexact_trunkTERCERA.csv; Δmin = 0.9 mm × S0 street crown area "
         "(notes/decisions/runoff_metric_sensitivity.md §10). Optimised = weights summer 0.5, winter 0.25, hotspot runoff 0.25. "
         "Bars: Today and Optimised minus the S1a mean; ochre whisker = the 10 S1a seeds.")


if __name__ == "__main__":
    fig_radar()
    fig_bars()
