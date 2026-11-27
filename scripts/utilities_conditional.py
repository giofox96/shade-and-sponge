"""Free planting spots over underground utilities in the Santapau / Emili Roca / Desfar demo area: python scripts/utilities_conditional.py
Flags a spot "conditional" (not excluded) when its tree pit would sit on a gas main, a gas service line or a Telefónica duct.

Rule: PTEV 2024 (IMPJB, Plec de prescripcions tècniques per al disseny, l'execució i la recepció d'espais verds, rev. May 2024),
§2.2.6.2 p.31: no pits "sobre infraestructures soterrades existents" without designed waterproofing and drainage. No numeric
pit-to-service distance is written (§3.2 p.82 only asks for the service plans; §5.3.9 p.116 gives the pit size). So the flag is
"the pit footprint intersects a line", with the footprint = the 1 x 1 m minimum pit (§5.3.9 p.116) taken as a disc of radius
0.5 m around the spot (ASSUMPTION: the pit's orientation is unknown, the inscribed circle is the conservative reading).

Inputs (OMEN only, gitignored, ACEFAT eWise request 872551): databases/barcelona/raw/ewise/GN_872551_Vectorial.dwg/*.dxf
(layers BP = gas mains, ACOMETIDA = gas service lines) and TF1_872551_Vectorial.dwg/*.dxf (Canalizacion_Barna_shape = ducts).
TERMS: raw utility geometry never leaves this script; only per-spot distances (0.1 m) and the flag are written.
Outputs: databases/barcelona/porta_spots_utilities.csv; counts printed (spots and, for context, existing trees). The public web
app uses the synthetic layer instead (scripts/synthetic_utilities.py)."""
import json, pathlib
import numpy as np, pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point, box
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/barcelona/raw/ewise"
AREA = box(431150, 4586830, 431450, 4587110)     # demo rectangle, EPSG:25831 (request 872551)
PIT_R = 0.5                                       # m, ASSUMPTION (see docstring)
NETS = {"gas_main": ("GN", "BP"), "gas_service": ("GN", "ACOMETIDA"), "telecom": ("TF1", "Canalizacion_Barna_shape")}
CREDIT = "Ayuntamiento de Barcelona - Información de base y cartografía (IBC)"


def lines(net, layer):
    """LWPOLYLINE vertices of one layer of an ASCII DXF, as LineStrings (EPSG:25831)."""
    f = next(RAW.glob(f"{net}_872551_Vectorial.dwg/*.dxf"))
    t = [s.strip() for s in open(f, encoding="latin-1")]
    out, ent, lay, pts, x = [], None, None, [], None
    for k, v in zip(t[0::2], t[1::2]):
        if k == "0":
            if ent == "LWPOLYLINE" and lay == layer and len(pts) > 1:
                out.append(LineString(pts))
            ent, lay, pts = v, None, []
        elif k == "8":
            lay = v
        elif k == "10":
            x = float(v)
        elif k == "20":
            pts.append((x, float(v)))
    return out


def nearest(pts, geoms):
    tree = STRtree(geoms)
    return np.array([p.distance(geoms[tree.nearest(p)]) for p in pts])


nets = {k: lines(*v) for k, v in NETS.items()}
for k, g in nets.items():
    xs = np.concatenate([np.asarray(l.coords)[:, 0] for l in g])
    assert 400000 < xs.min() and xs.max() < 460000, f"{k}: not EPSG:25831 metres"   # CRS check

sp = pd.read_csv(ROOT / "databases/barcelona/porta_planting_spots.csv")
sp = sp[(sp.get("excluded_by", pd.Series("", index=sp.index)).fillna("") == "")]  # the free spots the web app shows
P = [Point(x, y) for x, y in zip(sp.x, sp.y)]
sp = sp[[AREA.contains(p) for p in P]].reset_index(drop=True)
P = [Point(x, y) for x, y in zip(sp.x, sp.y)]
out = pd.DataFrame({"spot_id": sp.spot_id})
for k, g in nets.items():
    out[f"d_{k}_m"] = nearest(P, g).round(1)
out["utility_conditional"] = (out.filter(like="d_").min(axis=1) <= PIT_R).astype(int)
dst = ROOT / "databases/barcelona/porta_spots_utilities.csv"
with open(dst, "w", encoding="utf-8", newline="") as fh:
    fh.write(f"# Source: {CREDIT} (ACEFAT eWise request 872551, plans valid to ~18 Feb 2027). Derived distances only; "
             f"rule: PTEV 2024 p.31, pit footprint radius {PIT_R} m (ASSUMPTION). scripts/utilities_conditional.py\n")
    out.to_csv(fh, index=False)

# existing street trees in the rectangle (web export positions + kept trees), for context only: not written to disk
to_utm = Transformer.from_crs(4326, 25831, always_xy=True)
T = json.load(open(ROOT / "web/public/data/porta/trees.json", encoding="utf-8"))
tx, ty = to_utm.transform(T["positions"]["lon"] + T["kept"]["lon"], T["positions"]["lat"] + T["kept"]["lat"])
TP = [p for p in map(Point, tx, ty) if AREA.contains(p)]
td = np.min([nearest(TP, g) for g in nets.values()], axis=0)

# web app: no longer written here. The public app shows the SYNTHETIC layer (scripts/synthetic_utilities.py, tutor feedback
# 24 Nov G2); the real flags stay in the CSV above and are reported as counts only.

within = lambda d, r: int((d <= r).sum())
print(f"lines: " + ", ".join(f"{k} {len(g)}" for k, g in nets.items()))
print(f"free spots in the rectangle: {len(out)}; conditional (pit over a line, <= {PIT_R} m): {out.utility_conditional.sum()}; "
      f"within 1.0 m: {within(out.filter(like='d_').min(axis=1), 1.0)}")
for k in nets:
    print(f"  {k}: spots <= {PIT_R} m {within(out[f'd_{k}_m'], PIT_R)}")
print(f"existing trees in the rectangle: {len(TP)}; would fail the same rule: {within(td, PIT_R)}; within 1.0 m: {within(td, 1.0)}")
