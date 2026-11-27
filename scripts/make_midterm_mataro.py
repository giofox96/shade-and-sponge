"""Backup slides for the midterm deck: why Mataró, where it is, and where the transfer test ran (notes/mataro_transfer_test.md,
notes/catalan_transfer_city.md). Rendered images, as for every map in the deck.
- mataro_locator.png: land/sea from global-land-mask (GLOBE 1 km land mask, pip global-land-mask), Barcelona (Porta) and Mataró.
- mataro_streets.png: every inventory tree as a light dot, the planes of the six test streets in colour, labelled with the
  result (summer shade of the new trees, % of planes of the same trunk size; method vs city practice S1b) from
  databases/mataro/transfer_test.csv. Only this derived image goes in the repo: the inventory is not sublicensable
  (databases/RESTRICTED_DATA.md) and is read from outside the repo.
Run from the repo root: python scripts/make_midterm_mataro.py [path/to/mataro_t_c_arbrat.csv]
Needs matplotlib, pandas, numpy, scipy, global-land-mask. Output: slides/midterm/fig/mataro_locator.png, mataro_streets.png
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from global_land_mask import globe
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides/midterm/fig"
INV = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/mataro/mataro_t_c_arbrat_20261112.csv")
INK, MUTED, GRID, BG = "#2A2622", "#665E4F", "#DCD8CE", "#F2F0EA"
HEAT, RAIN, TREE, WARN = "#663825", "#283F66", "#3F663E", "#8C6A24"
SEA = "#DCE3EA"
plt.rcParams.update({"font.family": "IBM Plex Sans", "font.size": 13, "text.color": INK})
PORTA = (2.178, 41.437)        # Porta (Nou Barris), Barcelona: near the repo's local origin 430800, 4586800 (EPSG:25831)
MATARO = (2.444, 41.540)       # Mataró centre
OFFSET = {"ALFONS X EL SAVI, RONDA D'": (-175, 30), "València, Carrer de": (-118, 14), "MIGUEL DE CERVANTES, RONDA DE": (16, -60)}   # label placement, points
KX = 111.32 * np.cos(np.radians(41.45))   # km per degree of longitude at this latitude


def frame(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    return fig, ax


def locator():
    lo0, lo1, la0, la1 = 1.95, 2.75, 41.28, 41.72
    lon, lat = np.meshgrid(np.arange(lo0, lo1, 0.004), np.arange(la0, la1, 0.004))
    land = gaussian_filter(globe.is_land(lat, lon).astype(float), 1.2)   # smooth the 1 km raster steps for display
    fig, ax = frame(6.4, 6.4 * (la1 - la0) * 111.32 / ((lo1 - lo0) * KX))
    ax.set_facecolor(SEA)
    ax.contourf(lon, lat, land, levels=[-0.5, 0.5, 1.5], colors=[SEA, "#E9E5DB"])
    ax.contour(lon, lat, land, levels=[0.5], colors=[MUTED], linewidths=0.8)
    ax.set_xlim(lo0, lo1)
    ax.set_ylim(la0, la1)
    ax.set_aspect(111.32 / KX)
    ax.plot(*zip(PORTA, MATARO), color=MUTED, lw=1.2, ls=(0, (4, 3)))
    d = np.hypot((MATARO[0] - PORTA[0]) * KX, (MATARO[1] - PORTA[1]) * 111.32)
    ax.text((PORTA[0] + MATARO[0]) / 2 - 0.02, (PORTA[1] + MATARO[1]) / 2 + 0.012, f"{d:.0f} km", color=MUTED,
            rotation=np.degrees(np.arctan2((MATARO[1] - PORTA[1]) * 111.32, (MATARO[0] - PORTA[0]) * KX)), ha="center")
    for (x, y), name, c, sub in ((PORTA, "Barcelona", HEAT, "site: Porta"), (MATARO, "Mataró", TREE, "transfer test")):
        ax.scatter([x], [y], s=110, color=c, zorder=3, edgecolor="white", lw=1.5)
        ax.text(x - 0.02, y + 0.018, name, fontsize=17, weight="bold", color=c, ha="right")
        ax.text(x - 0.02, y + 0.003, sub, fontsize=12, color=MUTED, ha="right")
    ax.text(2.62, 41.36, "Mediterranean Sea", color=RAIN, fontsize=13, style="italic", ha="center")
    x0, y0 = lo0 + 0.04, la0 + 0.03                                  # 10 km scale bar
    ax.plot([x0, x0 + 10 / KX], [y0, y0], color=INK, lw=2.5)
    ax.text(x0 + 5 / KX, y0 + 0.01, "10 km", ha="center", fontsize=11)
    fig.savefig(OUT / "mataro_locator.png", facecolor=BG)
    plt.close(fig)
    return d


def streets():
    d = pd.read_csv(INV)
    d = d[d.icona == "Arbre.png"]
    t = pd.read_csv(ROOT / "databases/mataro/transfer_test.csv")
    lo0, lo1, la0, la1 = 2.405, 2.482, 41.522, 41.565
    fig, ax = frame(7.2, 7.2 * (la1 - la0) * 111.32 / ((lo1 - lo0) * KX))
    ax.set_facecolor(BG)
    ax.scatter(d.lon, d.lat, s=0.6, color="#BDB7A8", lw=0)
    for _, r in t.iterrows():
        m = d[(d.ubicacio == r.street) & (d.barri == r.barri) & d.especie.str.startswith("Platanus")]
        ax.scatter(m.lon, m.lat, s=12, color=TREE, lw=0, zorder=3)
        name = r.street.split(",")[0].title().replace("D'", "d'").replace(" De ", " de ")
        ax.annotate(f"{name}\n{r.summer_pct_method_bal:.0f}% vs {r.summer_pct_S1b:.0f}%", (m.lon.mean(), m.lat.mean()),
                    xytext=OFFSET.get(r.street, (10, 8)), textcoords="offset points", fontsize=14,
                    arrowprops=dict(arrowstyle="-", color=TREE, lw=0.8), color=INK, weight="semibold", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=TREE, lw=0.8, alpha=0.92))
    ax.set_xlim(lo0, lo1)
    ax.set_ylim(la0, la1)
    ax.set_aspect(111.32 / KX)
    x0, y0 = lo0 + 0.003, la0 + 0.002
    ax.plot([x0, x0 + 1 / KX], [y0, y0], color=INK, lw=2.5)
    ax.text(x0 + 0.5 / KX, y0 + 0.0008, "1 km", ha="center", fontsize=11)
    fig.savefig(OUT / "mataro_streets.png", facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Porta–Mataró {locator():.1f} km")
    streets()
