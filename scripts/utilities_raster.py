"""Electricity from the Endesa (e-distribución) raster plans: python scripts/utilities_raster.py
Endesa answered the eWise request with one RGB image per sheet inside the PDF, not vectors. Per sheet: decode the image
(Flate, no PDF library), split its pixels by colour into the cable network and the faint base map, place the sheet in
EPSG:25831 by matching the base-map pixels to the façade and kerb lines (scripts/utilities_pdf.py fit, target), then turn the cable
pixels into lines: a 0.25 m grid in metres, closed over the dash gaps, thinned to one cell, and traced into polylines.
Precision is about the size of one image pixel on the ground; lengths of dashed pieces are approximate.

TERMS: everything stays on the OMEN under EWISE_DIR/derived/ (gitignored): networks_raster.geojson feeds
scripts/utilities_study.py, which writes aggregates only."""
import json, re, sys, zlib, pathlib
import numpy as np
from scipy import ndimage
from skimage.morphology import skeletonize

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from utilities_pdf import OUT, RAW, fit, target, MAX_RES  # noqa: E402

FILE = "872551_FE_Compact.pdf"
CELL = 0.25          # m, grid for tracing
CLOSE = 3            # cells (0.75 m) of closing to join dashes (ASSUMPTION, from the dash gap seen on the sheets)
MIN_LEN = 1.0        # m, traced pieces shorter than this are symbols or noise


def sheets():
    b = open(RAW / FILE, "rb").read()
    O = {int(m.group(1)): m.group(2) for m in re.finditer(rb"(\d+) 0 obj(.*?)endobj", b, re.S)}
    kids = [int(x) for x in re.findall(rb"(\d+) 0 R", re.search(rb"/Type/Pages/Count \d+/Kids\[([^\]]*)\]", b).group(1))]
    for n, k in enumerate(kids, 1):
        v = O[k]
        if b"/img0" not in v:
            continue
        img = int(re.search(rb"/img0 (\d+) 0 R", v).group(1))
        cs = int(re.search(rb"/Contents (\d+) 0 R", v).group(1))
        t = zlib.decompress(O[cs].split(b"stream", 1)[1].lstrip(b"\r\n")).decode("latin-1")
        m = re.search(r"([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) cm /img0 Do", t)
        M = [float(x) for x in m.groups()]
        h = O[img].split(b"stream")[0]
        W, H = int(re.search(rb"/Width (\d+)", h).group(1)), int(re.search(rb"/Height (\d+)", h).group(1))
        a = np.frombuffer(zlib.decompress(O[img].split(b"stream", 1)[1].lstrip(b"\r\n")), np.uint8)[: W * H * 3].reshape(H, W, 3)
        yield n, a, M


def to_page(rows, cols, M, H, W):
    u, v = (cols + 0.5) / W, 1 - (rows + 0.5) / H          # image space, origin bottom-left
    return np.c_[M[0] * u + M[2] * v + M[4], M[1] * u + M[3] * v + M[5]]


def trace(mask):
    """Skeleton pixels -> polylines (chains between ends and junctions)."""
    sk = skeletonize(mask)
    pts = {tuple(p) for p in np.argwhere(sk)}
    nb = lambda p: [(p[0] + i, p[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i or j) and (p[0] + i, p[1] + j) in pts]
    deg = {p: len(nb(p)) for p in pts}
    seen, out = set(), []
    for s in [p for p in pts if deg[p] != 2] + list(pts):
        for q in nb(s):
            if (s, q) in seen:
                continue
            line, a, b = [s], s, q
            while True:
                seen.add((a, b)); seen.add((b, a)); line.append(b)
                if deg[b] != 2:
                    break
                nxt = [c for c in nb(b) if c != a and (b, c) not in seen]
                if not nxt:
                    break
                a, b = b, nxt[0]
            out.append(np.array(line))
    return out


if __name__ == "__main__":
    T, tree, box = target()
    feats = []
    for n, a, M in sheets():
        r, g, bl = (a[..., i].astype(int) for i in range(3))
        cable = (r < 80) & (g > 90) & (g < 190) & (bl > 90) & (bl < 190) & (abs(g - bl) < 40)     # teal: low voltage
        mv = (r < 60) & (g < 60) & (bl > 180)                                                      # blue: medium voltage
        base = (r > 220) & (g > 150) & (g < 235) & (bl > 100) & (bl < 220) & (r - bl > 25)       # faint orange cadastre
        H, W = cable.shape
        src = to_page(*np.nonzero(base), M, H, W)
        if len(src) < 200:
            print(f"sheet {n}: base map too thin ({len(src)} px), skipped"); continue
        f, res, scale = fit(src[:: max(1, len(src) // 20000)], T, tree, box)
        used = res <= MAX_RES
        print(f"sheet {n}: 1:{scale}, median residual {res:.2f} m, cable px {cable.sum()}, MV px {mv.sum()}{'' if used else '  -> skipped'}")
        if not used:
            continue
        for name, m in (("electricity_lv", cable), ("electricity_mv", mv)):
            if m.sum() < 20:
                continue
            P = f(to_page(*np.nonzero(m), M, H, W))
            o = P.min(0) - 2
            ij = np.floor((P - o) / CELL).astype(int)
            G = np.zeros(ij.max(0)[::-1] + 3, bool)
            G[ij[:, 1], ij[:, 0]] = True
            G = ndimage.binary_closing(ndimage.binary_dilation(G), iterations=CLOSE)
            for line in trace(G):
                xy = o + (line[:, ::-1] + 0.5) * CELL
                if np.hypot(*np.diff(xy, axis=0).T).sum() >= MIN_LEN:
                    feats.append({"type": "Feature", "properties": {"network": name, "sheet": n, "res_m": round(res, 2)},
                                  "geometry": {"type": "LineString", "coordinates": np.round(xy[:: 2] if len(xy) > 4 else xy, 2).tolist()}})
    json.dump({"type": "FeatureCollection", "crs": "EPSG:25831", "note": "RAW-DERIVED, never publish", "features": feats},
              open(OUT / "networks_raster.geojson", "w"))
    from collections import Counter
    print(Counter(f["properties"]["network"] for f in feats), "->", OUT / "networks_raster.geojson")
