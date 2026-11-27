"""How the real buried services sit in the street, to make the synthetic layer believable: python scripts/utilities_study.py
Reads the eWise vector plans (ACEFAT request 872551: gas mains BP, gas service lines ACOMETIDA, Telefónica ducts; entrance
numbers PORTAL_500) and the PDF plans georeferenced by scripts/utilities_pdf.py (water mains and service lines, Vodafone-ONO
ducts, street lighting) inside the demo rectangle, and measures each network against the city's façade and kerb lines
(web/public/data/porta/sidewalks.geojson): how much of it runs under the sidewalk or the road, how far from the façade (in
metres and as a share of the sidewalk width), how much of the façade has one in front, and how often service lines leave a
façade. The same measures run on the synthetic layer (web/public/data/porta/utilities.geojson) so the two can be compared.

TERMS: raw utility geometry never leaves this script (AGBAR: exclusive use; Nedgia: confidential, notes/utilities_demo.md).
Only aggregate numbers are written, and only to EWISE_DIR/derived/ (gitignored, next to the raw plans): utility_params.json.
Whether those aggregates may be published is the user's call; scripts/synthetic_utilities.py reads them when present.
Raw plans: EWISE_DIR (default databases/barcelona/raw/ewise), so a worktree can point at the main checkout."""
import json, os, pathlib, sys
import numpy as np
from pyproj import Transformer
from shapely.geometry import LineString, Point, box
from shapely.ops import linemerge, nearest_points, unary_union
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = pathlib.Path(os.environ.get("EWISE_DIR", ROOT / "databases/barcelona/raw/ewise"))
AREA = box(431150, 4586830, 431450, 4587110)     # demo rectangle of request 872551, EPSG:25831 (scripts/utilities_conditional.py)
STEP = 1.0                                        # m, sampling step along lines and façades
MAX_W = 12.0                                      # m, a façade point with no kerb this close has no sidewalk (synthetic_utilities.py)
FRONT = 0.5                                       # m of tolerance when asking "between façade and kerb"
SYMBOL_M = 1.2                                    # m, PDF strokes shorter than this are symbols (arrowheads), not pipes
Q = [0.1, 0.25, 0.5, 0.75, 0.9]
to_utm = Transformer.from_crs(4326, 25831, always_xy=True)


def dxf(net, layer, kind="LWPOLYLINE"):
    """Entities of one layer of an ASCII DXF: polylines as LineStrings, TEXT/POINT as Points (EPSG:25831)."""
    f = next(RAW.glob(f"{net}_872551_Vectorial.dwg/*.dxf"))
    t = [s.strip() for s in open(f, encoding="latin-1")]
    out, ent, lay, pts, x = [], None, None, [], None
    for k, v in zip(t[0::2], t[1::2]):
        if k == "0":
            if ent == kind == "LWPOLYLINE" and lay == layer and len(pts) > 1:
                out.append(LineString(pts))
            elif ent == kind and lay == layer and pts:
                out.append(Point(pts[0]))
            ent, lay, pts = v, None, []
        elif k == "8":
            lay = v
        elif k == "10":
            x = float(v)
        elif k == "20" and x is not None:
            pts.append((x, float(v)))
            x = None
    return out


def sample(lines, step=STEP):
    return np.asarray([l.interpolate(s).coords[0] for l in lines for s in np.arange(step / 2, l.length, step)])


sw = json.load(open(ROOT / "web/public/data/porta/sidewalks.geojson", encoding="utf-8"))["features"]
utm = lambda c: LineString(np.c_[to_utm.transform(*np.asarray(c).T)])
big = AREA.buffer(40)
FAC = [g for f in sw if f["properties"]["kind"] == "facade" and (g := utm(f["geometry"]["coordinates"])).intersects(big)]
KERB = [g for f in sw if f["properties"]["kind"] == "kerb" and (g := utm(f["geometry"]["coordinates"])).intersects(big)]
tf, tk = STRtree(FAC), STRtree(KERB)


def place(p):
    """A point against the street section: (where, distance from the façade, sidewalk width there)."""
    P = Point(p)
    f = FAC[tf.nearest(P)]
    fp = nearest_points(f, P)[0]
    k = KERB[tk.nearest(fp)]
    w = fp.distance(k)
    df, dk = P.distance(f), P.distance(k)
    if w > MAX_W:
        return "open", df, w                                       # square, courtyard: no sidewalk of its own
    return ("sidewalk" if df + dk <= w + FRONT else "road"), df, w


def angle(l):
    """Degrees between a piece (end to end) and the façade normal: 0 = straight across, 90 = along the façade."""
    a, b = np.asarray(l.coords)[[0, -1]]
    m = Point((a + b) / 2)
    f = FAC[tf.nearest(m)]
    s = f.project(m)
    t = np.subtract(f.interpolate(min(s + 0.5, f.length)).coords[0], f.interpolate(max(s - 0.5, 0)).coords[0])
    c = abs(np.dot(b - a, t)) / (np.linalg.norm(b - a) * np.linalg.norm(t) + 1e-9)
    return float(np.degrees(np.arcsin(min(1, c))))


def split(ls):
    """Mains and service lines drawn in one colour (the water plan). Strokes under SYMBOL_M are arrowheads and other symbols;
    short pieces straight across are service lines; the rest, joined end to end, are mains."""
    ls = [l for l in ls if l.length >= SYMBOL_M]
    srv = [l for l in ls if l.length < 15 and angle(l) < 30]
    ids = set(map(id, srv))
    m = linemerge(unary_union([l for l in ls if id(l) not in ids]))
    return list(getattr(m, "geoms", [m])), srv


def measure(nets, portals=None):
    """Aggregate numbers per network; nets = {name: [LineString]} already in EPSG:25831."""
    out = {}
    fpts = sample([f.intersection(AREA) for f in FAC if f.intersects(AREA)])
    for name, ls in nets.items():
        cut = [l.intersection(AREA) for l in ls]
        ls = [p for c in cut if not c.is_empty for p in getattr(c, "geoms", [c]) if p.length > 0]
        if not ls:
            continue
        pts = sample(ls)
        pl = [place(p) for p in pts]
        where = np.array([a for a, _, _ in pl])
        df = np.array([b for _, b, _ in pl]); w = np.array([c for _, _, c in pl])
        sd = where == "sidewalk"
        r = dict(length_m=round(float(sum(l.length for l in ls))), n_pieces=len(ls),
                 share_sidewalk=round(float(sd.mean()), 2), share_road=round(float((where == "road").mean()), 2),
                 share_open=round(float((where == "open").mean()), 2))
        if sd.sum() > 5:
            r["d_facade_q"] = np.round(np.quantile(df[sd], Q), 2).tolist()
            r["ratio_q"] = np.round(np.quantile(df[sd] / w[sd], Q), 2).tolist()
        rd = where == "road"
        if rd.sum() > 5:   # beyond the kerb: how far into the road
            dk = np.array([Point(p).distance(KERB[tk.nearest(Point(p))]) for p in pts[rd]])
            r["d_past_kerb_q"] = np.round(np.quantile(dk, Q), 2).tolist()
        # how much of the façade has this network under its own sidewalk (a sample point within the façade-kerb strip)
        tl = STRtree(ls)
        cov = []
        for p in fpts:
            P = Point(p)
            k = KERB[tk.nearest(P)]
            wk = P.distance(k)
            if wk > MAX_W:
                continue
            cov.append(any(P.distance(ls[i]) <= wk + FRONT and place(nearest_points(ls[i], P)[0].coords[0])[0] == "sidewalk"
                           for i in tl.query(P.buffer(wk + FRONT))))
        r["facade_coverage"] = round(float(np.mean(cov)), 2) if cov else None
        r["facade_m"] = len(cov)
        # pieces that cross the sidewalk (service lines): angle to the façade normal, rate per 100 m of façade
        ang = np.array([angle(l) for l in ls if l.length >= 0.5])
        r["angle_to_normal_q"] = np.round(np.quantile(ang, Q), 0).tolist() if len(ang) else None
        r["share_across"] = round(float((ang < 30).mean()), 2) if len(ang) else None
        r["across_per_100m_facade"] = round(100 * float((ang < 30).sum()) / max(len(cov), 1), 1)
        r["piece_len_q"] = np.round(np.quantile([l.length for l in ls], Q), 1).tolist()
        out[name] = r
    if portals is not None:
        P = [p for p in portals if AREA.contains(p)]
        out["entrances"] = dict(n=len(P), per_100m_facade=round(100 * len(P) / max(len(fpts), 1), 1))
        if "gas_service" in nets:
            gs = STRtree(nets["gas_service"])
            out["entrances"]["share_with_gas_service_3m"] = round(float(np.mean(
                [p.distance(nets["gas_service"][gs.nearest(p)]) <= 3 for p in P])), 2)
    return out


if __name__ == "__main__":
    real = {"gas_main": dxf("GN", "BP"), "gas_service": dxf("GN", "ACOMETIDA"), "telecom": dxf("TF1", "Canalizacion_Barna_shape")}
    for k, g in real.items():
        assert g and 400000 < g[0].coords[0][0] < 460000, f"{k}: empty or not EPSG:25831"
    # the PDF plans, georeferenced by scripts/utilities_pdf.py (water, Vodafone-ONO, street lighting)
    pdf_f = RAW / "derived/networks_pdf.geojson"
    if pdf_f.exists():
        pdf = {}
        for f in json.load(open(pdf_f))["features"]:
            pdf.setdefault(f["properties"]["network"], []).append(LineString(f["geometry"]["coordinates"]))
        if "water" in pdf:
            real["water_main"], real["water_service"] = split(pdf["water"])
        for k in ("telecom_ono", "lighting"):
            if k in pdf:
                real[k] = pdf[k]
    R = measure(real, dxf("GN", "PORTAL_500", "TEXT"))
    syn_f = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "web/public/data/porta/utilities.geojson")
    S = {}
    if syn_f.exists():
        fc = json.load(open(syn_f, encoding="utf-8"))["features"]
        for f in fc:
            S.setdefault(f["properties"]["network"], []).append(utm(f["geometry"]["coordinates"]))
        S = measure(S)
    # the number that matters to the tool: how many of today's street trees in the rectangle would stand on a line (pit disc 0.5 m)
    T = json.load(open(ROOT / "web/public/data/porta/trees.json", encoding="utf-8"))
    tx, ty = to_utm.transform(T["positions"]["lon"] + T["kept"]["lon"], T["positions"]["lat"] + T["kept"]["lat"])
    TP = [p for p in map(Point, tx, ty) if AREA.contains(p)]

    def on_line(nets):
        g = [l for v in nets.values() for l in v]
        t = STRtree(g)
        return sum(p.distance(g[t.nearest(p)]) <= 0.5 for p in TP)
    R["trees_on_a_line"] = dict(n=len(TP), on=int(on_line(real)))
    if S:
        syn = {}
        for f in fc:
            syn.setdefault(f["properties"]["network"], []).append(utm(f["geometry"]["coordinates"]))
        S["trees_on_a_line"] = dict(n=len(TP), on=int(on_line(syn)))
    keys = ["share_sidewalk", "share_road", "facade_coverage", "ratio_q", "d_past_kerb_q", "piece_len_q", "across_per_100m_facade"]
    for k in sorted(set(R) | set(S)):
        print(f"\n{k}")
        for side, D in (("real", R), ("synthetic", S)):
            v = D.get(k)
            print(f"  {side:9s} " + ("-" if v is None else json.dumps({a: v[a] for a in keys if a in v} if "length_m" in v else v)))
    d = RAW / "derived"
    d.mkdir(exist_ok=True)
    json.dump(dict(source="ACEFAT eWise request 872551, demo rectangle; aggregates only (scripts/utilities_study.py)",
                   rectangle=list(AREA.bounds), real=R), open(d / "utility_params.json", "w", encoding="utf-8"), indent=1)
    print(f"written: {d / 'utility_params.json'} (gitignored, aggregates only)")
