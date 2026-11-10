"""Second pass of spot exclusions for Porta, from the city's own point data. Runs AFTER scripts/porta_spot_exclusions.py
(OSM) and only looks at the spots that script kept. It does NOT change databases/barcelona/porta_planting_spots.csv, so
the tool's spots stay as they are: the result goes to databases/barcelona/porta_planting_spots_city.csv (spot_id,
size_class, excluded_by with the OSM and the city rule, dist_m to the city object) until the user decides whether the
guide's lamp distance should bind (half of Porta's existing trees stand closer to a lamp than it allows; see the last
printout and notes/tutor_feedback_10nov.md A3).

Objects, clipped to the Porta boundary (exchange/to_gh/porta_boundary.csv) + 50 m, cached in
databases/barcelona/porta_street_objects.csv (type, x, y in EPSG:25831, source, date; CC BY 4.0, Ajuntament de Barcelona):
  lamp          1:1000 topographic base map WMS, layer Punts_energia, 250 m SVG tiles as in scripts/porta_sidewalk_width.py;
                each point is typed by GetFeatureInfo and only INSPIRE_SUBCONJUNT 02-Fanal is a lamp (the layer also
                holds 01-Suports / 06-Pal poles; cached as energy_point_other, not applied). Clearance by the spot's size_class: 3 m small, 4.5 m medium, 6.5 m large
                (2011 street-tree guide pp. 22-23, "minimum distance to lamp"; notes/tree_master_plan.md §5 point 4)
  traffic_light Open Data BCN infraestructures-inventari-semafors, ground-standing elements only (columns Col800/Col2400/
                Col4000, Baculo, Mastil); heads, boxes (arquetes) and cabinets are left out. 3 m (same guide: > 3 m from
                traffic lights and signs)
  sign_support  Open Data BCN infraestructures-inventari-suports, all support types except Paret (wall-mounted), active
                rows only (no Data_Baixa). 3 m (same guide)
  The semafors and suports datasets were last modified on 5 Dec 2022 (CKAN metadata), although some rows carry later
  Data_Alta dates; objects installed or removed since then are not seen.
  bollard, bench, fountain  Open Data BCN infraestructures-inventari-pilones / -bancs (Oct 2026) and fonts (drinking
                fountains, 2026). 1 m. ASSUMPTION: no source; about one tree pit
  bus_stop      Open Data BCN estacions-bus (Nov 2025): only reported (extra spots within 8 m beyond the OSM bus-stop
                rule), not applied.
Raw downloads (gitignored): <raw>/street_objects/*.csv and WMS tiles in <raw>/topo_1000/svg/, where <raw> defaults to
databases/barcelona/raw/ or is the first argument. They are only needed when the object cache is missing.
Run from the repo root (on the PC; the WMS blocks the cloud): python scripts/porta_spot_exclusions_city.py [raw_dir]
"""
import json, pathlib, re, sys, time, numpy as np, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import porta_sidewalk_width as psw  # noqa: E402  reuse the WMS tile fetch (fetch, TILE, PX)

RAW = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "databases/barcelona/raw"
SPOTS, OBJ = ROOT / "databases/barcelona/porta_planting_spots.csv", ROOT / "databases/barcelona/porta_street_objects.csv"
CITY = ROOT / "databases/barcelona/porta_planting_spots_city.csv"
O = json.load(open(ROOT / "exchange/site_origin.json"))
LAMP = {"small": 3.0, "medium": 4.5, "large": 6.5}                       # 2011 guide pp. 22-23
FIXED = {"traffic_light": 3.0, "sign_support": 3.0}                      # 2011 guide
SMALL = {"bollard": 1.0, "bench": 1.0, "fountain": 1.0}                  # ASSUMPTION
BUS = 8.0                                                                # as the OSM rule (ASSUMPTION there)
B = "https://opendata-ajuntament.barcelona.cat/data/dataset/"
SRC = {  # file: (url, x col, y col, source tag, date)
    "semafors": (B + "802c9d1b-11d5-4f74-a319-0fcf23b96d56/resource/20bd3dd1-efb0-490e-acd1-c7d0be170419/download", "X_ETRS89", "Y_ETRS89", "infraestructures-inventari-semafors", "2022-12-05"),
    "suports": (B + "d317dc43-f086-4060-a177-634c6db7d916/resource/8329e9e9-1ead-4b28-acd8-8a7cd461ea7f/download", "X_ETRS89", "Y_ETRS89", "infraestructures-inventari-suports", "2022-12-05"),
    "pilones": (B + "ac086225-31d6-4fc7-b39d-7fe8d2dbb0a6/resource/af372084-9941-445a-9f30-692927cd31f4/download", "x_etrs89", "y_etrs89", "infraestructures-inventari-pilones", "2026-10-01"),
    "bancs": (B + "d066b8ee-ebba-4423-b64f-31c16ee2d416/resource/cdec2de4-9098-4b88-94bb-d1ec12959b3a/download", "x_etrs89", "y_etrs89", "infraestructures-inventari-bancs", "2026-10-01"),
    "fonts": (B + "889c583e-6c11-46c3-bc45-7f3ae5e6c621/resource/8f63c3cf-399a-4a8d-a73d-eb1fca80d7f0/download/fonts_beure_2026.csv", "X_ETRS89", "Y_ETRS89", "fonts", "2026-10-28"),
    "bus": (B + "d395e808-697d-4722-8eb9-b672a8ba0916/resource/2d190658-93ac-4c43-a23f-c5d313b1ae9c/download", "ETRS89_COORD_X", "ETRS89_COORD_Y", "estacions-bus", "2025-11-06"),
}
TL_KEEP = ("Col800", "Col2400", "Col4000", "Baculo", "Mastil")


def area():
    b = pd.read_csv(ROOT / "exchange/to_gh/porta_boundary.csv")
    return Polygon(zip(b.x + O["origin_x"], b.y + O["origin_y"])).buffer(50)


def lamps(poly):
    psw.SVG = RAW / "topo_1000/svg"
    psw.SVG.mkdir(parents=True, exist_ok=True)
    psw.LAYERS["lamp"] = "Punts_energia"
    x0, y0, x1, y1 = poly.bounds
    out = []
    for tx in np.arange(np.floor(x0 / psw.TILE) * psw.TILE, x1, psw.TILE):
        for ty in np.arange(np.floor(y0 / psw.TILE) * psw.TILE, y1, psw.TILE):
            for a, b in re.findall(r"<use[^>]*translate\(([-\d.]+),([-\d.]+)\)", psw.fetch("lamp", tx, ty)):
                a, b = float(a), float(b)
                if 0 <= a < psw.PX and 0 <= b < psw.PX:          # symbols outside the tile are drawn too; keep each once
                    out.append((tx + a * psw.TILE / psw.PX, ty + psw.TILE - b * psw.TILE / psw.PX))
    return pd.DataFrame(out, columns=["x", "y"]).assign(type="lamp", source="mapa-base-topografic WMS Punts_energia", date="")


def lamp_type(xy):
    """INSPIRE_SUBCONJUNT of the Punts_energia feature at each point (GetFeatureInfo in a 0.4 m box)."""
    def one(p):
        x, y = p
        q = dict(SERVICE="WMS", VERSION="1.3.0", REQUEST="GetFeatureInfo", LAYERS="Punts_energia", QUERY_LAYERS="Punts_energia",
                 STYLES="", CRS="EPSG:25831", BBOX=f"{x-0.2},{y-0.2},{x+0.2},{y+0.2}", WIDTH=21, HEIGHT=21, I=10, J=10,
                 INFO_FORMAT="application/gml+xml; version=3.1", FEATURE_COUNT=5, FORMAT="image/png")
        for k in range(4):
            try:
                t = requests.get(psw.WMS, params=q, timeout=60).text
                break
            except requests.RequestException:
                time.sleep(5 * (k + 1))
        else:
            raise RuntimeError(f"GetFeatureInfo failed at {x}, {y}")
        e = re.findall(r'INSPIRE_SUBCONJUNT">([^<]*)<', t)
        return "02-Fanal" if "02-Fanal" in e else (e[0] if e else "(none)")
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(one, xy))


def city(poly):
    D = RAW / "street_objects"
    D.mkdir(parents=True, exist_ok=True)
    parts = []
    for f, (url, xc, yc, src, date) in SRC.items():
        p = D / f"{f}.csv"
        if not p.exists():
            r = requests.get(url, timeout=300)
            r.raise_for_status()
            p.write_bytes(r.content)
        d = pd.read_csv(p, low_memory=False, encoding_errors="replace")
        if f == "semafors":
            d = d[d.Codi_Semafor.isin(TL_KEEP)].assign(type="traffic_light")
        elif f == "suports":
            d = d[d.Data_Baixa.isna() & ~d.Desc_Tipus_Suport.eq("Paret")].assign(type="sign_support")
        elif f in ("pilones", "bancs"):
            d = d[d.data_baixa.astype(str).str.startswith("9999")].assign(type="bollard" if f == "pilones" else "bench")
        elif f == "bus":
            d = d[d.NOM_CAPA.str.startswith("Autobusos")].assign(type="bus_stop")
        else:
            d = d.assign(type="fountain")
        d = d.rename(columns={xc: "x", yc: "y"})[["type", "x", "y"]].drop_duplicates(["type", "x", "y"])
        parts.append(d.assign(source=src, date=date))
    return pd.concat(parts)


def apply(s, ob, lamp_k=1.0, small_m=None):
    """Fill excluded_by where empty; first rule that applies. Returns the new column and the distance that triggered it."""
    ex, dist = s.excluded_by.copy(), pd.Series(np.nan, index=s.index)
    xy = s[["x", "y"]].values
    lamp_d = s.size_class.map(LAMP).values * lamp_k
    rules = [("lamp", lamp_d)] + [(t, np.full(len(s), d)) for t, d in FIXED.items()] + \
            [(t, np.full(len(s), small_m or d)) for t, d in SMALL.items()]
    for t, clear in rules:
        o = ob[ob.type == t]
        if not len(o):
            continue
        dd = cKDTree(o[["x", "y"]].values).query(xy)[0]
        hit = (dd < clear) & (ex == "").values
        ex[hit], dist[hit] = t, dd[hit]
    return ex, dist


if __name__ == "__main__":
    poly = area()
    if not OBJ.exists():
        ob = pd.concat([lamps(poly), city(poly)])
        ob = ob[[poly.contains(Point(x, y)) for x, y in ob[["x", "y"]].values]].round({"x": 2, "y": 2})
        lt = pd.Series(lamp_type(ob.loc[ob.type == "lamp", ["x", "y"]].values))
        print("Punts_energia points by INSPIRE_SUBCONJUNT:", lt.value_counts().to_dict())
        ob.loc[ob.type == "lamp", "type"] = np.where(lt == "02-Fanal", "lamp", "energy_point_other").tolist()  # kept, not applied
        ob.to_csv(OBJ, index=False)
    ob = pd.read_csv(OBJ, keep_default_na=False)
    print(f"objects in Porta + 50 m ({OBJ.stat().st_size / 1e3:.0f} kB):", ob.type.value_counts().to_dict())

    s = pd.read_csv(SPOTS, keep_default_na=False)
    city_rules = {"lamp", *FIXED, *SMALL}
    s.loc[s.excluded_by.isin(city_rules), "excluded_by"] = ""              # re-runs start from the OSM result
    n0 = (s.excluded_by == "").sum()
    s["excluded_by"], dist = apply(s, ob)
    new = s.excluded_by.isin(city_rules)
    clear = np.where(s.excluded_by == "lamp", s.size_class.map(LAMP), s.excluded_by.map({**FIXED, **SMALL}))
    assert (dist[new] < clear[new]).all() and (s.excluded_by == "").sum() == n0 - new.sum()
    s.assign(dist_m=dist.round(2))[["spot_id", "size_class", "excluded_by", "dist_m"]].to_csv(CITY, index=False)
    kept = s[s.excluded_by == ""]
    print(f"{len(s)} spots; after OSM {n0} -> after city rules {len(kept)} kept")
    print("excluded by city rule:", s[new].excluded_by.value_counts().to_dict())
    print("kept by size class:", kept.size_class.value_counts().to_dict())
    print("examples:", [(r.spot_id, r.excluded_by, round(dist[i], 2)) for i, r in s[new].sample(5, random_state=1).iterrows()])

    base = s.excluded_by.where(~new, "")
    sb = s.assign(excluded_by=base)
    for lab, kw in [("lamp x0.5", dict(lamp_k=0.5)), ("lamp x2", dict(lamp_k=2.0)),
                    ("1 m rule at 0.5 m", dict(small_m=0.5)), ("1 m rule at 2 m", dict(small_m=2.0))]:
        print(f"sensitivity {lab}: {(apply(sb, ob, **kw)[0] == '').sum()} kept")

    bus = ob[ob.type == "bus_stop"]
    near_bus = cKDTree(bus[["x", "y"]].values).query(s[["x", "y"]].values)[0] < BUS
    print(f"bus stops (Open Data BCN, {len(bus)}): {int((near_bus & (base == '')).sum())} spots kept after OSM and "
          f"{int((near_bus & (s.excluded_by == '')).sum())} kept after the city rules lie within {BUS} m (not applied)")

    # do existing street trees respect the lamp rule? (sidewalk class from scripts/porta_sidewalk_width.py)
    t = pd.read_csv(ROOT / "exchange/to_gh/porta_street_trees.csv").merge(
        pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv")[["tree_id", "size_class"]], on="tree_id")
    t["d"] = cKDTree(ob[ob.type == "lamp"][["x", "y"]].values).query(np.c_[t.x + O["origin_x"], t.y + O["origin_y"]])[0]
    t["need"] = t.size_class.map(LAMP)
    for c, g in t.groupby("size_class"):
        v = g.d < g.need if g.need.notna().all() else g.d < LAMP["small"]
        print(f"existing trees, class {c}: {len(g)}, closer to a lamp than {g.need.iat[0] if g.need.notna().all() else '3 (small, for reference)'} m: "
              f"{v.sum()} ({100 * v.mean():.0f}%), median distance {g.d.median():.1f} m")
    v = t.need.notna()
    print(f"existing trees with a sidewalk class: {(t.d[v] < t.need[v]).mean() * 100:.0f}% violate the guide lamp distance")
