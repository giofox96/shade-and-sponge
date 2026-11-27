"""SYNTHETIC underground utilities for the public web app: python scripts/synthetic_utilities.py
The real plans (ACEFAT eWise request 872551, scripts/utilities_conditional.py) cannot be published, so the public app shows
a mock layer built from published layout rules plus declared random choices (tutor feedback 24 Nov, G1–G2,
notes/tutor_feedback_24nov.md §3a). It shows how the tool uses a utility layer; it says nothing about where Porta's real
services run. Every file and map label says "synthetic".

Rules (sources in notes/data_requests.md §6.2):
- Sewer mains run along the carriageway axis (BCASA, Guia de criteris tècnics generals de la xarxa de clavegueram, 2015, §3.1
  p.3), so they never cross a sidewalk pit: not drawn.
- Each building gets house connections that cross the sidewalk from the façade to the street (BCASA §3.5.1 crit. 7 p.17: a
  connection manhole on the sidewalk for each new connection). Drawn as one line per entrance, façade to 1 m past the kerb.
  ASSUMPTION: entrances are unknown, so they are placed along every façade at a random gap of 0.5–1.5 × ENTRY_GAP_M.
- Distribution networks (water, gas, low-voltage electricity, telecom) run under the sidewalk, parallel to the façade.
  ASSUMPTION: NETWORKS lines per façade, each at a random distance from the façade drawn once per façade line from OFFSET_M,
  kept at least KERB_CLEAR_M inside the kerb.
- A spot is "conditional" when its pit would sit on a line: PTEV 2024 §2.2.6.2 p.31 (no pits over buried services without a
  designed solution), pit footprint = disc of radius PIT_R_M (ASSUMPTION, as scripts/utilities_conditional.py).
Inputs: web/public/data/porta/sidewalks.geojson (façade and kerb lines of the city's 1:1000 map) and the spots in trees.json.
Outputs: web/public/data/porta*/utilities.geojson, `utility_conditional` per spot in each trees.json, a `utilities` entry in
each meta.json, databases/barcelona/porta_spots_utilities_synthetic.csv. Re-run after python -m shade_sponge.web_export."""
import glob, json, pathlib
import numpy as np, pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
WEB = ROOT / "web/public/data"
SEED = 1
ENTRY_GAP_M = 15.0            # mean gap between house connections along a façade (ASSUMPTION, no source)
NETWORKS = ("water", "gas", "electricity")    # longitudinal lines per façade (ASSUMPTION: telecom shares the electricity trench)
OFFSET_M = (0.5, 1.5)         # distance from the façade of each longitudinal line (ASSUMPTION)
KERB_CLEAR_M = 0.5            # a line stays at least this far inside the kerb (ASSUMPTION)
MAX_W_M = 12.0                # a façade point with no kerb this close has no sidewalk of its own (squares, courtyards)
MIN_W_M = 1.0
STEP_M = 1.0                  # sampling step along a façade
PIT_R_M = 0.5                 # pit footprint radius (ASSUMPTION, scripts/utilities_conditional.py)
NOTE = "SYNTHETIC: generated from published layout rules and random choices, not Porta's real services"

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

lines = []                                                   # (kind, network, LineString)
for f in fac:
    if f.length < 3:
        continue
    s = np.r_[np.arange(0, f.length, STEP_M), f.length]
    p = np.asarray([f.interpolate(v).coords[0] for v in s])
    d, j = kd.query(p)
    ok = (d >= MIN_W_M) & (d <= MAX_W_M)
    u = (kp[j] - p) / np.maximum(d, 1e-9)[:, None]          # unit vector façade -> kerb
    for net in NETWORKS:
        o = np.minimum(rng.uniform(*OFFSET_M), d - KERB_CLEAR_M)
        q = p + u * o[:, None]
        good = ok & (o >= 0.3)
        for run in np.split(np.arange(len(s)), np.flatnonzero(np.diff(good.astype(int))) + 1):   # consecutive valid points
            if good[run[0]] and len(run) > 1:
                lines.append(("service", net, LineString(q[run]).simplify(0.2)))
    t = rng.uniform(0, ENTRY_GAP_M)
    while t < f.length:
        i = int(round(t / STEP_M)) if t < s[-2] else len(s) - 1
        if ok[i]:
            lines.append(("connection", "house connection", LineString([p[i], kp[j[i]] + u[i] * 1.0])))
        t += rng.uniform(0.5, 1.5) * ENTRY_GAP_M

geoms = [g for _, _, g in lines]
tree = STRtree(geoms)
print(f"synthetic lines: {sum(k == 'service' for k, _, _ in lines)} longitudinal, {sum(k == 'connection' for k, _, _ in lines)} house connections")


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
