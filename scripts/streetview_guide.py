"""Street View guide for the documented works of the back-test: for each group, the stretch (main street between two
cross streets), a Street View link standing at one end and looking along the planted trees, and a small locator map with
the camera and its view cone. Output: /mnt/project-files/slides/streetview/ (guide .md + one PNG per group) or argv[1].
Run from scripts/: python streetview_guide.py [out_dir]
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge
from pyproj import Transformer
import make_backtest_deck as dk

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/project-files/slides/streetview")
OUT.mkdir(parents=True, exist_ok=True)
BACK, FOV = 6.0, 70.0                    # camera stands 6 m beyond the first tree, looking along the row; view cone width
# Cross streets at the two ends of each row, from OpenStreetMap (nearest named way that is not the main street, same
# end order as below); the tree inventory's street names alone gave wrong ends. None = end not at a crossing.
CROSS = {6128: ("Av. Rio de Janeiro", "C. Garrofers", None), 3050: ("C. Bassols", "C. Independència", "C. Rogent"),
         4466: ("C. Piquer", "C. Fontrodona", "C. Nou de la Rambla"), 4504: ("C. Piquer", "C. Nou de la Rambla", "C. Cabanes"),
         4506: ("C. Piquer", "C. Palaudàries", "C. Mata"), 6687: ("C. Guatemala", "C. Monturiol", "Gran Via")}
to_wgs = Transformer.from_crs(25831, 4326, always_xy=True)


def clean(st):
    return st.replace("C\\ ", "C. ").replace("Av\\ ", "Av. ").replace("Pg\\ ", "Pg. ").replace("Pl\\ ", "Pl. ") \
        .replace("G.V. Corts Catalanes", "Gran Via").replace("\\", ".").replace("Av ", "Av. ")


lines = ["# Street View guide: documented works of the back-test", "",
         "Each link opens Street View standing at one end of the planted stretch, looking along the trees (the map shows "
         "the camera and the view cone). Click the clock (top left, \"See more dates\") and take one image before and one "
         "after the quarter shown. Save to `databases\\barcelona\\raw\\streetview\\` as `<group>_<street>_<before|after>_<YYYY-MM>.jpg`.", ""]
for _, row in dk.r[dk.DOC].sort_values(["street", "quarter"]).iterrows():
    q = dk.p[dk.p.group == row.group]
    xy = q[["x", "y"]].values
    c = xy.mean(0)
    v = np.linalg.svd(xy - c, full_matrices=False)[2][0]
    t = (xy - c) @ v
    a, b = xy[t.argmin()], xy[t.argmax()]
    pad = 60
    bb = (c[0] - max(np.ptp(xy[:, 0]) / 2 + pad, 80), c[1] - max(np.ptp(xy[:, 1]) / 2 + pad, 80),
          c[0] + max(np.ptp(xy[:, 0]) / 2 + pad, 80), c[1] + max(np.ptp(xy[:, 1]) / 2 + pad, 80))
    bld, trees = dk.context(row.barri, bb)
    tt = trees.dropna(subset=["street"])
    d = np.min(np.hypot(tt.x.values[:, None] - xy[:, 0], tt.y.values[:, None] - xy[:, 1]), 1)
    main = tt[d < 3].street.mode().iloc[0] if (d < 3).any() else row.street

    def cross(e):
        o = tt[tt.street != main]
        if o.empty:
            return "?"
        return clean(o.iloc[np.argmin(np.hypot(o.x - e[0], o.y - e[1]))].street)
    ca, cb = cross(a), cross(b)
    if row.group in CROSS:
        main_name, ca, cb = CROSS[row.group]
    else:
        main_name = clean(main)
    cam = a - v * BACK if np.dot(b - a, v) > 0 else a + v * BACK
    look = b - cam
    heading = (np.degrees(np.arctan2(look[0], look[1])) + 360) % 360       # compass, from north (grid north ≈ true north)
    lon, lat = to_wgs.transform(*cam)
    url = (f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat:.6f},{lon:.6f}"
           f"&heading={heading:.0f}&pitch=0&fov=80")
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=160)
    kerb = dk.roads[dk.roads.group == row.group] if dk.roads is not None else None
    if kerb is not None and len(kerb):
        kerb.plot(ax=ax, color="#9A9488", linewidth=0.35, alpha=0.5, zorder=0)
    bld.plot(ax=ax, color="#D3CEC2", edgecolor="none")
    for x, y in xy:
        ax.add_patch(Circle((x, y), 2.0, color=dk.TREE, zorder=3))
    ang = np.degrees(np.arctan2(look[1], look[0]))
    ax.add_patch(Wedge(cam, np.hypot(*look) + 10, ang - FOV / 2, ang + FOV / 2, color=dk.WARN, alpha=0.25, zorder=2))
    ax.add_patch(Circle(cam, 3.0, color=dk.WARN, zorder=4))
    for name, x, y, an, _ in dk.street_labels(trees, xy, bb):
        ax.text(x, y, name, rotation=an, rotation_mode="anchor", ha="center", va="center", fontsize=6.5, color=dk.MUTED,
                zorder=5, bbox=dict(facecolor=dk.BG, edgecolor="none", alpha=0.75, pad=1))
    ax.set_xlim(bb[0], bb[2])
    ax.set_ylim(bb[1], bb[3])
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(f"{main_name} · group {row.group}", fontsize=9, color=dk.INK, loc="left")
    png = f"{row.group}_{main_name.split('. ')[-1].lower().replace(' ', '-')}.png"
    fig.savefig(OUT / png, facecolor=dk.BG, bbox_inches="tight")
    plt.close(fig)
    where = f"between {ca} and {cb}" if cb else f"from {ca} for {np.ptp(t):.0f} m (no crossing at the other end)"
    lines += [f"## {main_name}, {where} (group {row.group})", "",
              f"{row.n} trees changed in {row.quarter}: {row.top_before} → {row.top_city}. "
              f"Camera at the {ca} end, looking along the trees (heading {heading:.0f}°).", "",
              f"[Open Street View]({url})", "", f"![locator]({png})", ""]
    print(row.group, main_name, ca, cb, f"{heading:.0f}")
(OUT / "streetview_guide.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT / "streetview_guide.md")
