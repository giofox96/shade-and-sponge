"""Sidewalk width at each Porta street tree, from the city's 1:1000 topographic map (WMS vectors).

Source: Ajuntament de Barcelona, Mapa base topografic 1:1000, WMS http://w133.bcn.cat/WMSTOPOGRAFIC/service.svc/get
(open data `mapa-base-topografic`, CC BY 4.0). Layers: facade lines and road lines (kerbs), fetched as SVG in tiles
because the 652 MB GeoPackage download keeps failing (notes/sidewalk_width.md).
Input:  exchange/to_gh/porta_trees_lidar.csv (tree positions, local coords; origin in exchange/site_origin.json)
Output: databases/barcelona/porta_sidewalk_width.csv; raw SVG tiles cached in databases/barcelona/raw/topo_1000/svg/
Width = distance from the nearest facade, through the tree, to the first long road line beyond it (the kerb).
Size class from the 2011 street-tree guide pp. 22-23 (one class per sidewalk type).
"""
import json, pathlib, re, time, numpy as np, pandas as pd, requests
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVG = ROOT / "databases/barcelona/raw/topo_1000/svg"
WMS = "http://w133.bcn.cat/WMSTOPOGRAFIC/service.svc/get"
LAYERS = {"facade": "Línies_construccions_façanes", "road": "Línies_comunicacions"}
TILE, PX = 250.0, 2500                  # 250 m tiles at 0.1 m per SVG unit
RAY, MIN_KERB = 30.0, 4.0               # ASSUMPTION: max sidewalk search 30 m; kerb lines >= 4 m (skips tree-pit edges)
TOL = 1.0                               # ASSUMPTION: tree points sit at the pit, up to 1 m past the kerb line


def fetch(layer, x0, y0):
    f = SVG / f"{layer}_{int(x0)}_{int(y0)}.svg"
    if not f.exists():
        q = dict(SERVICE="WMS", VERSION="1.3.0", REQUEST="GetMap", LAYERS=LAYERS[layer], STYLES="", CRS="EPSG:25831",
                 BBOX=f"{x0},{y0},{x0 + TILE},{y0 + TILE}", WIDTH=PX, HEIGHT=PX, FORMAT="image/svg+xml")
        for k in range(5):
            try:
                r = requests.get(WMS, params=q, timeout=120)
                r.raise_for_status()
                f.write_text(r.text, encoding="utf-8")
                break
            except requests.RequestException:
                time.sleep(5 * (k + 1))
        else:
            raise RuntimeError(f"WMS failed for {f.name}")
    return f.read_text(encoding="utf-8")


def parse(svg, x0, y0):
    """SVG path d-strings (absolute/relative M, L, H, V, Z) -> LineStrings in EPSG:25831."""
    s = PX / TILE
    out = []
    for d in re.findall(r'<path[^>]*\sd="([^"]+)"', svg):
        cur, pts = (0.0, 0.0), []
        for cmd, args in re.findall(r"([A-Za-z])([^A-Za-z]*)", d):
            v = [float(a) for a in re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", args)]
            if cmd not in "MmLlHhVvZz":
                raise ValueError(f"unsupported SVG command {cmd}")
            if cmd in "Mm" and len(pts) > 1:
                out.append(pts)
            if cmd in "Mm":
                pts = []
            if cmd in "Zz" and pts:
                pts.append(pts[0])
            step = 1 if cmd in "HhVv" else 2
            for k in range(0, len(v) - step + 1, step):
                if cmd in "ML": cur = (v[k], v[k + 1])
                elif cmd in "ml": cur = (cur[0] + v[k], cur[1] + v[k + 1])
                elif cmd == "H": cur = (v[k], cur[1])
                elif cmd == "h": cur = (cur[0] + v[k], cur[1])
                elif cmd == "V": cur = (cur[0], v[k])
                else: cur = (cur[0], cur[1] + v[k])
                pts.append(cur)
        if len(pts) > 1:
            out.append(pts)
    return [LineString([(x0 + px / s, y0 + TILE - py / s) for px, py in line]) for line in out]


def lines(layer, xs, ys):
    return [g for x0 in xs for y0 in ys for g in parse(fetch(layer, x0, y0), x0, y0)]


def size_class(w):
    return np.select([w < 2.5, w < 3.5, w <= 6.0], ["none", "small", "medium"], "large")


if __name__ == "__main__":
    SVG.mkdir(parents=True, exist_ok=True)
    o = json.load(open(ROOT / "exchange/site_origin.json"))
    t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
    X, Y = t.x + o["origin_x"], t.y + o["origin_y"]
    xs = np.arange(np.floor((X.min() - RAY) / TILE) * TILE, X.max() + RAY, TILE)
    ys = np.arange(np.floor((Y.min() - RAY) / TILE) * TILE, Y.max() + RAY, TILE)
    fac, road = lines("facade", xs, ys), lines("road", xs, ys)
    road = [g for g in road if g.length >= MIN_KERB]
    tf, tr = STRtree(fac), STRtree(road)
    rows = []
    for tid, x, y in zip(t.tree_id, X, Y):
        p = Point(x, y)
        i = tf.nearest(p)
        df = fac[i].distance(p)
        if df > RAY:
            rows.append((tid, np.nan, df, "no_facade")); continue
        q = fac[i].interpolate(fac[i].project(p))            # foot of the perpendicular on the facade
        u = (np.array([x, y]) - np.array([q.x, q.y])) / max(df, 1e-6)
        ray = LineString([(q.x, q.y), (q.x + u[0] * RAY, q.y + u[1] * RAY)])
        hits = [ray.intersection(road[j]) for j in tr.query(ray)]
        d = sorted(Point(q.x, q.y).distance(h) for h in hits if not h.is_empty)
        if any(x < df - TOL for x in d):                      # a road line between facade and tree: median or far side
            rows.append((tid, np.nan, df, "median")); continue
        rows.append((tid, d[0] if d else np.nan, df, "ok" if d else "no_kerb"))
    out = pd.DataFrame(rows, columns=["tree_id", "width_m", "facade_dist_m", "flag"])
    out["width_m"] = out.width_m.round(2); out["facade_dist_m"] = out.facade_dist_m.round(2)
    out["size_class"] = np.where(out.flag == "ok", size_class(out.width_m.fillna(0)), "check")
    out = t[["tree_id", "species", "is_plane", "street"]].merge(out, on="tree_id")
    assert len(out) == len(t) and out.tree_id.is_unique
    out.to_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv", index=False)
    print(f"{len(fac)} facade lines, {len(road)} road lines >= {MIN_KERB} m")
    print(out.flag.value_counts().to_dict())
    print("all trees:", out.size_class.value_counts().to_dict())
    print("planes:", out[out.is_plane].size_class.value_counts().to_dict())
    print(out[out.flag == "ok"].width_m.describe().round(2).to_dict())
