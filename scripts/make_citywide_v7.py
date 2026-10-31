"""City-wide results for the 10 Nov deck: the city LP with the 15% cap and the local ceiling over 28 barris
(notes/citywide_plan.md §6.8-6.9).
Input: databases/barcelona/citylp_local_summary.csv, citylp_local_species.csv (python scripts/city_lp.py --local-ceiling),
       web/public/data/barris.geojson (official outlines, Open Data BCN, CC BY 4.0; scripts/make_barris_web.py).
Output: slides/fig_v7/res_04_city_map.svg/.png (summer shade gain per barri), res_05_city_cap.svg/.png (the rule).
Run from scripts/: python make_citywide_v7.py
"""
import json, math, re, unicodedata
import numpy as np
import pandas as pd
import make_infographics as mi
from make_infographics import t, para, rect, save, ROOT, INK, MUTED, GRID, BG, HEAT, TREE, WARN

mi.OUT = ROOT / "slides/fig_v7"
DB = ROOT / "databases/barcelona"
d = pd.read_csv(DB / "citylp_local_summary.csv")
d["gain"] = d.summer_pct_citylp - d.summer_pct_s1a          # points of today's summer shade, city LP vs city mix
key = lambda n: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower())
LAYOUT = d.layout.iloc[0]
# city cap over these 28 barris, as printed by city_lp.py (31 Oct run, notes/citywide_plan.md §6.9); the street-tree
# inventory it is computed from (arbrat_viari.csv) is not in the repo
CAP = {"Celtis australis": 1318, "Melia azedarach": 11642, "Pyrus calleryana": 16569, "Jacaranda mimosifolia": 14024,
       "Tipuana tipu": 11348, "Brachychiton populneus": 12438, "Styphnolobium japonicum": 10142}
SRC = ("databases/barcelona/citylp_local_summary.csv and citylp_local_species.csv (scripts/city_lp.py --local-ceiling, "
       f"joint layout {LAYOUT}); outlines: Ajuntament de Barcelona, Open Data BCN (CC BY 4.0). Heat = effective-shade proxy, "
       "not UTCI; city mix = S1a, the city's 2026 replacement mix placed by its sidewalk rule.")


def fig_map():
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
    hi = d.gain.max()
    b = ""
    for name, r in rings:
        v = gain.get(key(name))
        fill, op = (GRID, 1.0) if v is None else (WARN, 0.9) if v < 0 else (TREE, 0.15 + 0.85 * v / hi)
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in map(px, r))
        sw = 3 if name == "Porta" else 0.8
        b += f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op:.2f}" stroke="{INK if name == "Porta" else BG}" stroke-width="{sw}"/>'
    xp, yp = px(np.array([r for n, r in rings if n == "Porta"][0]).mean(0))
    b += t(xp + 40, yp - 30, "Porta", 16, INK, "bold", halo=True)

    # legend: colour ramp in points
    for i in range(6):
        v = i * hi / 5
        b += rect(980 + i * 50, 180, 50, 22, TREE, rx=0, op=0.15 + 0.85 * v / hi) + t(980 + i * 50, 222, f"{v:.0f}", 13, MUTED)
    b += t(980, 168, "Summer shade gain over the city mix (points)", 16, INK, "bold")
    b += rect(980, 236, 22, 22, WARN, rx=0, op=0.9) + t(1010, 253, "below the city mix", 14, MUTED)
    b += rect(1180, 236, 22, 22, GRID, rx=0) + t(1210, 253, "not computed (<500 planes)", 14, MUTED)

    # key numbers
    n_above = int((d.summer_pct_citylp >= 100).sum())
    lines = [(f"+{d.gain.median():.1f}", f"median gain over the city mix in {len(d)} barris ({d.planes.sum():,} planes)"),
             (f"{int((d.gain > 0).sum())} of {len(d)}", f"barris beat the city mix; range {d.gain.min():+.1f} to {d.gain.max():+.1f} points"),
             (f"{n_above}", "barris end above today's summer shade (" +
              ", ".join(f"{r.barri} {r.summer_pct_citylp:.0f}%" for r in d[d.summer_pct_citylp >= 100].itertuples()) + ")")]
    y = 320
    for big, small in lines:
        b += t(980, y, big, 40, TREE, "bold")
        p, h = para(980, y + 30, small, 560, 17, fill=MUTED)
        b += p
        y += 50 + h + 24
    worst = d.loc[d.gain.idxmin()]
    p, _ = para(980, y + 10, f"One barri loses: {worst.barri} ({worst.summer_pct_citylp:.1f}% against {worst.summer_pct_s1a:.1f}%). "
                "Under one city cap, the capped species go where they add most shade; a barri can lose while the city gains.",
                560, 17, fill=INK)
    b += p
    save("res_04_city_map", "From one barri to 28: the same rules, one city-wide layout",
         "Replacing every plane in 28 barris under the city's 15% cap and a local ceiling: summer shade, against the city's own mix",
         b, SRC)


def fig_cap():
    n = pd.read_csv(DB / "citylp_local_species.csv").set_index(["barri", "scenario"]).loc[("ALL", LAYOUT)]
    sp = pd.DataFrame(dict(species=n.index.str.split().str[0], n=n.values.astype(int), cap=[CAP[k] for k in n.index]))
    b = ""
    # left: the rule, in two layers
    b += rect(60, 170, 620, 200, TREE, rx=12, op=0.08) + rect(60, 170, 620, 6, TREE, rx=0)
    b += t(84, 210, "1. CITY CAP: how much of each species", 18, TREE, "bold")
    p, _ = para(84, 244, "No species above 15% of the city's street trees (tree master plan). The headroom left today is shared "
                "across barris pro rata to the planes each replaces (ASSUMPTION).", 580, 18, fill=INK)
    b += p
    b += rect(60, 410, 620, 230, WARN, rx=12, op=0.08) + rect(60, 410, 620, 6, WARN, rx=0)
    b += t(84, 450, "2. LOCAL CEILING: no barri more concentrated than today", 18, WARN, "bold")
    p, _ = para(84, 484, "In each barri, no species ends with more trees than the barri has planes today. Without it, the city cap "
                "alone put Tipuana at 48.5% of Diagonal Mar's street trees; with it, 37.2% (17-barri run). It costs little shade.",
                580, 18, fill=INK)
    b += p
    p, _ = para(60, 690, "Limit found: where few planes are replaced the ceiling can leave no species that fits a position "
                "(Baró de Viver, 15 planes; la Trinitat Vella, 167). These barris need a different ceiling.", 620, 16, fill=MUTED)
    b += p
    # right: city totals against the cap
    x0, y0, bw = 760, 200, 420
    b += t(x0, 180, "Trees planted against each species' cap, all 28 barris", 18, INK, "bold")
    sp = sp.sort_values("cap")
    hi = sp.cap.max()
    for i, r in enumerate(sp.itertuples()):
        y = y0 + 20 + i * 70
        full = r.n >= r.cap
        b += t(x0, y + 4, r.species, 17, INK, "bold" if full else "normal")
        b += rect(x0 + 200, y - 16, bw * r.cap / hi, 26, GRID, rx=3)
        b += rect(x0 + 200, y - 16, bw * r.n / hi, 26, HEAT if full else TREE, rx=3)
        b += t(x0 + 200 + bw * r.cap / hi + 8, y + 4, f"{r.n:,} / {r.cap:,}" + ("  at cap" if full else ""), 15,
               HEAT if full else MUTED, "bold" if full else "normal")
    b += para(x0, y0 + 20 + len(sp) * 70, "Celtis and Tipuana hit the city cap (Celtis has little headroom left: it is "
              "already common). Within the cap the LP decides which barri gets them.", 760, 16, fill=MUTED)[0]
    save("res_05_city_cap", "Two rules: a city cap and a local ceiling",
         "The city's 15% fixes how much of each species; the local ceiling stops any barri ending more concentrated than today",
         b, SRC + " Cap: floor(15% × 140,404 street trees) minus each species today, pro rata to 31,580 of 40,137 city planes.")


if __name__ == "__main__":
    fig_map()
    fig_cap()
