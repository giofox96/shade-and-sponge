"""Whole-city figure for the final deck: every plane replaced in all barris under one city-wide 15% cap.
Input: databases/barcelona/citylp_summary.csv + citylp_city.csv (python scripts/city_lp.py --all),
       web/public/data/barris.geojson (official outlines, Open Data BCN, CC BY 4.0; scripts/make_barris_web.py).
--per-barri: plot the per-barri runs instead (barris_summary.csv; each barri with its own cap), the baseline.
Output: slides/fig_v7/res_08_city_all[_per_barri].svg/.png. Run from scripts/: python make_citywide_all.py [--per-barri]
"""
import json, math, re, sys, unicodedata
import numpy as np
import pandas as pd
import make_infographics as mi
from make_infographics import t, para, rect, save, ROOT, INK, MUTED, GRID, BG, TREE, WARN

mi.OUT = ROOT / "slides/fig_v7"
DB = ROOT / "databases/barcelona"
PER = "--per-barri" in sys.argv
key = lambda n: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower())

if PER:
    d = pd.read_csv(DB / "barris_summary.csv").drop_duplicates("barri").rename(columns={"summer_pct_tool": "method"})
    m = "method_per_barri_sum"
else:
    d = pd.read_csv(DB / "citylp_summary.csv").rename(columns={"summer_pct_citylp": "method"})
    m = "method_city_lp"
d["gain"] = d.method - d.summer_pct_s1b                      # points of today's summer shade, method vs city practice
c = pd.read_csv(DB / "citylp_city.csv").set_index("scenario")


def fig():
    g = json.load(open(ROOT / "web/public/data/barris.geojson", encoding="utf-8"))["features"]
    gain = dict(zip(d.barri.map(key), d.gain))
    rings = [(f["properties"]["name"], r) for f in g for poly in
             ([f["geometry"]["coordinates"]] if f["geometry"]["type"] == "Polygon" else f["geometry"]["coordinates"])
             for r in poly[:1]]
    lon = np.concatenate([np.array(r)[:, 0] for _, r in rings])
    lat = np.concatenate([np.array(r)[:, 1] for _, r in rings])
    kx = math.cos(math.radians(lat.mean()))
    s = min(860 / ((lon.max() - lon.min()) * kx), 640 / (lat.max() - lat.min()))
    px = lambda p: (60 + (p[0] - lon.min()) * kx * s, 170 + (lat.max() - p[1]) * s)
    hi = max(d.gain.max(), 1e-9)
    b = ""
    for name, r in rings:
        v = gain.get(key(name))
        fill, op = (GRID, 1.0) if v is None else (WARN, 0.9) if v < 0 else (TREE, 0.15 + 0.85 * v / hi)
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in map(px, r))
        b += f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op:.2f}" stroke="{BG}" stroke-width="0.8"/>'

    for i in range(6):                                         # legend
        v = i * hi / 5
        b += rect(980 + i * 50, 180, 50, 22, TREE, rx=0, op=0.15 + 0.85 * v / hi) + t(980 + i * 50, 222, f"{v:.0f}", 13, MUTED)
    b += t(980, 168, "Summer shade gain over city practice (points)", 16, INK, "bold")
    b += rect(980, 236, 22, 22, WARN, rx=0, op=0.9) + t(1010, 253, "below city practice", 14, MUTED)
    b += rect(1180, 236, 22, 22, GRID, rx=0) + t(1210, 253, "no planes or no LiDAR", 14, MUTED)

    y = 320                                                    # city totals: % of today's summer shade
    bars = [("Method", c.loc[m]), ("City practice", c.loc["S1b_city_practice"]), ("City announced mix", c.loc["S1a_city_announced_mix"])]
    b += t(980, y, "Whole city, summer shade (% of today)", 16, INK, "bold")
    for i, (lab, r) in enumerate(bars):
        yy = y + 30 + i * 52
        w = 3.6 * r.summer_pct_of_today
        b += t(980, yy + 20, lab, 16, INK, "bold" if i == 0 else "normal")
        b += rect(1150, yy, w, 30, TREE if i == 0 else MUTED, rx=3, op=0.9 if i == 0 else 0.5)
        b += t(1150 + w + 8, yy + 22, f"{r.summer_pct_of_today:.1f}%", 17, INK, "bold" if i == 0 else "normal")
    y += 220
    n_win = int((d.gain > 0).sum())
    for big, small in [(f"{n_win} of {len(d)}", "barris where the method beats city practice"),
                       (f"{c.loc[m].eff_species:.1f} vs {c.loc['S1b_city_practice'].eff_species:.1f}",
                        "effective species of the new trees, method vs city practice")]:
        b += t(980, y, big, 40, TREE, "bold")
        b += para(980, y + 30, small, 560, 17, fill=MUTED)[0]
        y += 100
    sub = ("Each barri with its own 15% cap" if PER else "One city-wide 15% cap") + \
          f": every plane replaced in {len(d)} barris, against the city's own practice"
    save("res_08_city_all" + ("_per_barri" if PER else ""), "The whole city: same rules, every plane", sub, b,
         "Ajuntament de Barcelona, Open Data BCN (street tree inventory; barri outlines, CC BY 4.0); ICGC LiDAR 2021; "
         "Pla director de l'arbrat de Barcelona 2017-2037 (15% species cap). Heat = effective-shade proxy, not UTCI.")


if __name__ == "__main__":
    fig()
