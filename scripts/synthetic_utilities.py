"""SYNTHETIC underground utilities for the public web app: python scripts/synthetic_utilities.py
The real plans (ACEFAT eWise request 872551, scripts/utilities_conditional.py) cannot be published, so the public app shows
a mock layer. v2 (user 27 Nov: "study the eWise data and generate believable ones"): the layer now copies how the real
networks sit in the street, measured by scripts/utilities_study.py in the demo rectangle and read here as aggregates only
(databases/barcelona/utility_params.json: aggregates only, published with the user's approval on 27 Nov): for each network, the share of façade length with a line in front, how
long a continuous piece runs, whether it lies under the sidewalk or the road, and how far from the façade (as a share of the
sidewalk width) or past the kerb; for gas service lines, how often one leaves a façade and how long it is. Positions are
random draws from those distributions: it says nothing about where Porta's real services run. Every label says "synthetic".

Networks: gas mains and service lines (Nedgia DXF), Telefónica ducts (DXF), and from the PDF plans georeferenced by
scripts/utilities_pdf.py water mains and service lines (Aigües de Barcelona), Vodafone-ONO ducts and street lighting
(Ajuntament), and low/medium-voltage electricity traced from Endesa's raster plans (scripts/utilities_raster.py). Not
generated: sewers (under the road; BCASA draws no house connections) and traffic lights (drawn in the base-map colour, not
separable).
The flag: a spot is "conditional" when its pit would sit on a line: PTEV 2024 §2.2.6.2 p.31, pit footprint = disc of radius
PIT_R_M (ASSUMPTION, as scripts/utilities_conditional.py).
Inputs: web/public/data/porta/sidewalks.geojson (façade and kerb lines, city 1:1000 map), the spots in trees.json, the
aggregates. Outputs: web/public/data/porta*/utilities.geojson, `utility_conditional` per spot in each trees.json, a
`utilities` entry in each meta.json, databases/barcelona/porta_spots_utilities_synthetic.csv. Re-run after
python -m shade_sponge.web_export. Self-check: python scripts/utilities_study.py compares the real and the synthetic numbers."""
import glob, json, os, pathlib
import numpy as np, pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
WEB = ROOT / "web/public/data"
PARAMS = ROOT / "databases/barcelona/utility_params.json"   # aggregates from scripts/utilities_study.py (copy of EWISE_DIR/derived/)
SEED = int(os.environ.get("SEED", 1))
MAX_W_M = 12.0                # a façade point with no kerb this close has no sidewalk of its own (squares, courtyards)
MIN_W_M = 1.0
STEP_M = 1.0                  # sampling step along a façade
MIN_OFF_M = 0.3               # a line never touches the façade
PIT_R_M = 0.5                 # pit footprint radius (ASSUMPTION, scripts/utilities_conditional.py)
NOTE = "SYNTHETIC: random positions drawn from how the real networks sit in the street (demo rectangle), not Porta's real services"
LONG = {"gas_main": "gas", "water_main": "water", "electricity_lv": "electricity (LV)", "electricity_mv": "electricity (MV)",
        "telecom": "telecom", "telecom_ono": "telecom (ONO)", "lighting": "lighting"}
SERVICES = {"gas_service": "gas service", "water_service": "water service", "electricity_service": "electricity service"}
# Real services and today's trees: in the rectangle no gas service line passes within PIT_R_M of a trunk, so a synthetic one
# slides up to SLIDE_M along the façade to miss one, or is dropped. Mains and ducts drawn at random already hit about as many
# trunks as the real ones (seeds 1-6: 19-43 trunks of 244 vs 26 real, same rectangle, in-sample), so they take one draw;
# AVOID_TRIES > 1 keeps the best of several offset draws (fewest trunks hit) if a future check asks for more avoidance.
AVOID_TRIES = int(os.environ.get("AVOID_TRIES", 1))
SLIDE_M = 3

to_utm = Transformer.from_crs(4326, 25831, always_xy=True)
to_ll = Transformer.from_crs(25831, 4326, always_xy=True)
rng = np.random.default_rng(SEED)


def utm(coords):
    x, y = to_utm.transform(*np.asarray(coords).T)
    return np.c_[x, y]


sw = json.load(open(WEB / "porta/sidewalks.geojson", encoding="utf-8"))["features"]
fac = [LineString(utm(f["geometry"]["coordinates"])) for f in sw if f["properties"]["kind"] == "facade"]
kerb = [LineString(utm(f["geometry"]["coordinates"])) for f in sw if f["properties"]["kind"] == "kerb"]
kp = np.vstack([np.asarray([k.interpolate(s).coords[0] for s in np.arange(0, k.length + 0.25, 0.25)]) for k in kerb])
kd = cKDTree(kp)

R = json.load(open(PARAMS, encoding="utf-8"))["real"]
QP = [0.1, 0.25, 0.5, 0.75, 0.9]


def draw(q, lo=None, hi=None):
    """One value from the 10/25/50/75/90% quantiles (piecewise-linear inverse CDF, tails held flat)."""
    return float(np.interp(rng.uniform(0, 1), [0] + QP + [1], [lo if lo is not None else q[0]] + q + [hi if hi is not None else q[-1]]))


T = json.load(open(WEB / "porta/trees.json", encoding="utf-8"))
trunks = cKDTree(utm(np.c_[T["positions"]["lon"] + T["kept"]["lon"], T["positions"]["lat"] + T["kept"]["lat"]]))
hits = lambda q: len(set(j for js in trunks.query_ball_point(q, PIT_R_M) for j in js))  # trunks within a pit radius of points q


def dense(a, b, step=0.5):
    n = max(2, int(np.hypot(*(b - a)) / step) + 1)
    return a + np.linspace(0, 1, n)[:, None] * (b - a)


lines = []                                                   # (kind, network, LineString)
for f in fac:
    if f.length < 3:
        continue
    s = np.r_[np.arange(0, f.length, STEP_M), f.length]
    p = np.asarray([f.interpolate(v).coords[0] for v in s])
    d, j = kd.query(p)
    ok = (d >= MIN_W_M) & (d <= MAX_W_M)
    u = (kp[j] - p) / np.maximum(d, 1e-9)[:, None]          # unit vector façade -> kerb
    for key, label in LONG.items():
        if key not in R:
            continue
        r = R[key]
        c = min(max(r["facade_coverage"], 0.01), 0.99)
        on, t = rng.uniform() < c, 0.0                        # alternate pieces with and without the network along the façade
        while t < f.length:
            L = draw(r["piece_len_q"], 1.0) if on else draw(r["piece_len_q"], 1.0) * (1 - c) / c
            if on:
                run = np.flatnonzero((s >= t) & (s <= t + L) & ok)
                if len(run) > 1:
                    road = rng.uniform() < r["share_road"] / (r["share_road"] + r["share_sidewalk"])
                    best = None
                    for _ in range(AVOID_TRIES):
                        if road:
                            o = d[run] + draw(r["d_past_kerb_q"], 0.2)          # under the road, at a set distance past the kerb
                        else:
                            o = np.clip(draw(r["ratio_q"], 0.02, 0.98) * d[run], MIN_OFF_M, d[run] - 0.2)
                        q = p[run] + u[run] * o[:, None]
                        h = hits(q)
                        if best is None or h < best[0]:
                            best = (h, q)
                    lines.append(("service", label, LineString(best[1]).simplify(0.2)))
            t += L
            on = not on
    # service lines: straight across, from the façade outwards, at the measured rate and length
    for key, label in SERVICES.items():
        if key not in R:
            continue
        gap = 100 / max(R[key]["across_per_100m_facade"], 0.1)
        t = rng.uniform(0, gap)
        while t < f.length:
            i = min(int(round(t / STEP_M)), len(s) - 1)
            L = draw(R[key]["piece_len_q"], 1.0)
            for k in sorted(range(max(0, i - SLIDE_M), min(len(s), i + SLIDE_M + 1)), key=lambda k: abs(k - i)):
                if ok[k] and not hits(dense(p[k], p[k] + u[k] * L)):
                    lines.append(("connection", label, LineString([p[k], p[k] + u[k] * L])))
                    break
            t += rng.exponential(gap)

geoms = [g for _, _, g in lines]
tree = STRtree(geoms)
print(f"synthetic lines: {sum(k == 'service' for k, _, _ in lines)} longitudinal, {sum(k == 'connection' for k, _, _ in lines)} service lines across the sidewalk")


def ll(g):
    x, y = to_ll.transform(*np.asarray(g.coords).T)
    return np.round(np.c_[x, y], 6).tolist()


fc = {"type": "FeatureCollection", "note": NOTE, "features": [
    {"type": "Feature", "properties": {"kind": k, "network": n}, "geometry": {"type": "LineString", "coordinates": ll(g)}}
    for k, n, g in lines]}
for f in sorted(glob.glob(str(WEB / "porta*/trees.json"))):
    d_ = pathlib.Path(f).parent
    j = json.load(open(f, encoding="utf-8"))
    S = j["spots"]
    x, y = to_utm.transform(S["lon"], S["lat"])
    dist = np.array([Point(a, b).distance(geoms[tree.nearest(Point(a, b))]) for a, b in zip(x, y)])
    flag = (dist <= PIT_R_M).astype(int)
    S["utility_conditional"] = flag.tolist()
    json.dump(j, open(f, "w", encoding="utf-8"), separators=(",", ":"))
    json.dump(fc, open(d_ / "utilities.geojson", "w", encoding="utf-8"), separators=(",", ":"))
    meta = json.load(open(d_ / "meta.json", encoding="utf-8"))
    cls = pd.Series(S.get("spot_class", ["free"] * len(flag)))
    meta["utilities"] = dict(file="utilities.geojson", synthetic=True, note=NOTE, seed=SEED, n_lines=len(lines),
                             spots_flagged=int(flag.sum()), free_spots_flagged=int(flag[(cls == "free").values].sum()), pit_r_m=PIT_R_M)
    json.dump(meta, open(d_ / "meta.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if d_.name == "porta":
        out = pd.DataFrame(dict(spot_id=S["id"], spot_class=cls, d_synthetic_m=dist.round(1), utility_conditional=flag))
        dst = ROOT / "databases/barcelona/porta_spots_utilities_synthetic.csv"
        with open(dst, "w", encoding="utf-8", newline="") as fh:
            fh.write(f"# {NOTE}. scripts/synthetic_utilities.py, seed {SEED}\n")
            out.to_csv(fh, index=False)
        print(f"spots: {len(flag)}; over a synthetic line (<= {PIT_R_M} m): {flag.sum()}; of the free ones: "
              f"{flag[(cls == 'free').values].sum()} of {(cls == 'free').sum()} become conditional")
