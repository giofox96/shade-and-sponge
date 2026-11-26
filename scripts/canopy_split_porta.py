"""Porta canopy today split by who owns the tree: street trees, park trees, zone trees (Open Data BCN inventories),
and canopy with no inventory point (private gardens, courtyards, unmapped park canopy). 26 Nov 2026, final deck.
Inputs: the web export of Porta (grid.bin.gz bit 3 = canopy today: LiDAR background canopy + street-tree crown discs;
trees.json; parks.json). Crowns are discs of the LiDAR crown diameter, so the total is the disc measure (23.4%),
not the CHM measure (20.1%): use the shares, not the absolute total. Run from the repo root: python scripts/canopy_split_porta.py"""
import json, gzip
import numpy as np
from pyproj import Transformer

D = "web/public/data/porta/"
m = json.load(open(D + "meta.json"))
g = m["grid"]
W, H, x0, y1 = g["W"], g["H"], g["x0"], g["y1"]
n = W * H
flags = np.frombuffer(gzip.open(D + "grid.bin.gz").read()[2 * n:3 * n], np.uint8).reshape(H, W)
ground, canopy = (flags & 1) > 0, ((flags >> 3) & 1) > 0          # bit 0 = site minus roofs, bit 3 = canopy today
tr = Transformer.from_crs(4326, 25831, always_xy=True)
yy, xx = np.mgrid[0:H, 0:W]


def discs(lon, lat, dia):
    M = np.zeros((H, W), bool)
    for lo, la, di in zip(lon, lat, dia):
        if not di or di != di:
            continue
        x, y = tr.transform(lo, la)
        c, r, R = x - x0 - 0.5, y1 - y - 0.5, di / 2
        r0, r1, c0, c1 = int(max(r - R - 1, 0)), int(min(r + R + 2, H)), int(max(c - R - 1, 0)), int(min(c + R + 2, W))
        if r0 < r1 and c0 < c1:
            M[r0:r1, c0:c1] |= (yy[r0:r1, c0:c1] - r) ** 2 + (xx[r0:r1, c0:c1] - c) ** 2 <= R * R
    return M


t = json.load(open(D + "trees.json"))
p, k = t["positions"], t["kept"]
street = discs(p["lon"], p["lat"], p["s0_crown_diam_m"]) | discs(k["lon"], k["lat"], k["crown_diam_m"])
pk = json.load(open(D + "parks.json"))
kind = np.array(pk["kind"])
sel = lambda mk: [np.array(pk[c], dtype=object)[mk] for c in ("lon", "lat", "crown_diam_m")]
park, zone = discs(*sel(kind == "park")), discs(*sel(kind == "zone"))
C = canopy & ground
parts = {"street trees": C & street, "park trees": C & ~street & park, "zone trees": C & ~street & ~park & zone,
         "no inventory point (private, courtyards, unmapped)": C & ~street & ~park & ~zone}
A = m["cover"]["area_m2"]
for name, X in parts.items():
    print(f"{name:52s} {X.sum() / 1e4:5.2f} ha  {100 * X.sum() / C.sum():5.1f}% of canopy  {100 * X.sum() / A:5.2f} pts of Porta")
print(f"{'total (disc measure)':52s} {C.sum() / 1e4:5.2f} ha  100.0%  {100 * C.sum() / A:5.2f}%  (CHM measure: {m['cover']['measured_pct']}%)")
