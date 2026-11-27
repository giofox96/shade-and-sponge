"""Georeference the eWise PDF plans and pull out their networks: python scripts/utilities_pdf.py
The water (Aigües de Barcelona), municipal (BCASA: sewers; Ajuntament: lighting, traffic lights, fibre) and Vodafone-ONO plans
came as PDFs. Their lines are vectors (scripts/pdf_lines.py) but in page units. Each sheet is placed in EPSG:25831 by matching
its base-map lines (the city cartography every operator draws under its network) to the same cartography in Nedgia's DXF
(layers FINCA, MANZANA, FONDO_LINEA, already in EPSG:25831): scale from a short list of plan scales, translation by FFT
cross-correlation of 1 m occupancy grids, then a few rounds of least-squares similarity fit (ICP) on nearby point pairs. The
fit residual is printed per sheet; a sheet that does not fit (median > 1.5 m) is skipped.

TERMS: everything stays on the OMEN, under EWISE_DIR/derived/ (gitignored): the per-network lines (networks_pdf.geojson) feed
scripts/utilities_study.py, which writes aggregates only. Raw geometry never goes into the repo, the web app or slides."""
import json, os, pathlib, sys
import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pdf_lines import pages  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = pathlib.Path(os.environ.get("EWISE_DIR", ROOT / "databases/barcelona/raw/ewise"))
OUT = RAW / "derived"
PT_M = 0.0254 / 72                     # one PDF point on paper, in metres
SCALES = (250, 500, 1000, 2000)        # candidate plan scales 1:n
MAX_RES = 1.5                          # m, median residual above which a sheet is not used

# per PDF: which stroke colours are base map (to fit) and which are networks (to keep), from each plan's legend and a render
# of the sheet checked by eye; keys are (r, g, b) rounded to 2 decimals, widths in points
PLANS = {
    # water: blue mains and service lines; grey = cadastral base
    "872551_AG-BCN-N_Compact.pdf": dict(base=[(0.31, 0.31, 0.31)], nets=[("water", (0.0, 0.0, 1.0), 0.5, None)]),
    # Vodafone-ONO: green ducts; black = base
    "872551_ONO_Compact.pdf": dict(base=[(0.0, 0.0, 0.0)], nets=[("telecom_ono", (0.0, 0.71, 0.0), 2.0, None)]),
    # Ajuntament, one network per sheet (two sheets each: pages 5-7 and 8-10, in the order of the Cond files FIB, SMF, LLU,
    # read from the "S" signal symbols on 6/9 and the lighting points on 7/10); black thin = base
    "pr872551_parcial/872551_AJBCN_Compact.pdf": dict(base=[(0.0, 0.0, 0.0), (0.74, 0.74, 0.74)], nets=[
        ("fibre_city", (0.0, 0.92, 0.0), 2.0, {5, 8}), ("lighting", (0.12, 0.37, 0.55), 2.0, {7, 10})]),
        # traffic lights (pages 6/9) are drawn in the same black as the base map: on an overlay they fell inside the blocks, so
        # they are not used
}
# not used: BCASA (sewer collectors run under the road and its plan draws no house connections; its colours need BCASA's own
# catalogue) and Endesa electricity (raster images, see the report)


def dxf_lines(layers):
    f = next(RAW.glob("GN_872551_Vectorial.dwg/*.dxf"))
    t = [s.strip() for s in open(f, encoding="latin-1")]
    out, ent, lay, pts, x = [], None, None, [], None
    for k, v in zip(t[0::2], t[1::2]):
        if k == "0":
            if ent == "LWPOLYLINE" and lay in layers and len(pts) > 1:
                out.append(np.asarray(pts))
            ent, lay, pts = v, None, []
        elif k == "8":
            lay = v
        elif k == "10":
            x = float(v)
        elif k == "20" and x is not None:
            pts.append((x, float(v))); x = None
    return out


def dense(lines, step):
    out = []
    for p in lines:
        p = np.asarray(p, float)
        for a, b in zip(p[:-1], p[1:]):
            n = max(1, int(np.hypot(*(b - a)) / step))
            out.append(a + np.linspace(0, 1, n, endpoint=False)[:, None] * (b - a))
    return np.vstack(out) if out else np.zeros((0, 2))


def grid(pts, x0, y0, W, H):
    g = np.zeros((H, W), np.float32)
    i, j = (pts[:, 1] - y0).astype(int), (pts[:, 0] - x0).astype(int)
    ok = (i >= 0) & (i < H) & (j >= 0) & (j < W)
    g[i[ok], j[ok]] = 1
    return g


def similarity(A, B):
    """Least-squares s, R, t with B ≈ s R A + t (Umeyama)."""
    ma, mb = A.mean(0), B.mean(0)
    a, b = A - ma, B - mb
    U, S, Vt = np.linalg.svd(b.T @ a / len(A))
    D = np.diag([1, np.sign(np.linalg.det(U @ Vt))])
    R = U @ D @ Vt
    s = np.trace(np.diag(S) @ D) / a.var(0).sum()
    return s, R, mb - s * R @ ma


def fit(src, tgt_pts, tree, box):
    """src: base-map points in page points. Returns (transform function, median residual m, scale n)."""
    x0, y0 = box[0], box[1]
    W, H = int(box[2] - x0), int(box[3] - y0)
    G = np.fft.rfft2(grid(tgt_pts, x0, y0, W, H))
    best = None
    for n in SCALES:
        P = src * PT_M * n
        P = P - P.min(0)
        S = grid(P + 0.5, 0, 0, W, H)
        if P[:, 0].max() > W or P[:, 1].max() > H:
            continue
        c = np.fft.irfft2(G * np.conj(np.fft.rfft2(S)), s=(H, W))
        k = np.unravel_index(np.argmax(c), c.shape)
        sc = c[k] / max(S.sum(), 1)
        if best is None or sc > best[0]:
            best = (sc, n, np.array([x0 + k[1], y0 + k[0]]) - (src * PT_M * n).min(0))
    if best is None:
        return None, np.inf, None
    _, n, t = best
    s, R = PT_M * n, np.eye(2)
    for it in range(25):                                     # ICP on pairs closer than a shrinking radius
        Q = s * src @ R.T + t
        d, j = tree.query(Q)
        keep = d < max(1.0, 6.0 - it * 0.4)
        if keep.sum() < 50:
            break
        s, R, t = similarity(src[keep], tgt_pts[j[keep]])
    d, _ = tree.query(s * src @ R.T + t)
    return (lambda p: s * np.asarray(p) @ R.T + t), float(np.median(d)), round(s / PT_M)


def close(c, ref):
    return all(abs(a - b) <= 0.02 for a, b in zip(c, ref))


if __name__ == "__main__":
    base = dxf_lines({"FINCA", "MANZANA", "FONDO_LINEA"})
    T = dense(base, 0.5)
    tree = cKDTree(T)
    box = (T[:, 0].min() - 150, T[:, 1].min() - 150, T[:, 0].max() + 150, T[:, 1].max() + 150)
    feats = []
    for fn, cfg in PLANS.items():
        for p in pages(str(RAW / fn)):
            src_l = [l["pts"] for l in p["lines"] if any(close(l["c"], b) for b in cfg["base"]) and l["w"] < 1.6]
            if len(src_l) < 50:
                continue
            src = dense(src_l, 1.0)
            f, res, n = fit(src, T, tree, box)
            used = res <= MAX_RES
            print(f"{fn} page {p['page']}: 1:{n}, median residual {res:.2f} m, base lines {len(src_l)}{'' if used else '  -> skipped'}")
            if not used:
                continue
            for name, col, wmin, pgs in cfg["nets"]:
                if pgs and p["page"] not in pgs:
                    continue
                for l in p["lines"]:
                    if close(l["c"], col) and l["w"] >= wmin:
                        xy = f(l["pts"])
                        feats.append({"type": "Feature", "properties": {"network": name, "sheet": f"{fn}#{p['page']}", "res_m": round(res, 2)},
                                      "geometry": {"type": "LineString", "coordinates": np.round(xy, 2).tolist()}})
    OUT.mkdir(exist_ok=True)
    json.dump({"type": "FeatureCollection", "crs": "EPSG:25831", "note": "RAW-DERIVED, never publish", "features": feats},
              open(OUT / "networks_pdf.geojson", "w"))
    from collections import Counter
    print(Counter(f["properties"]["network"] for f in feats), "->", OUT / "networks_pdf.geojson")
