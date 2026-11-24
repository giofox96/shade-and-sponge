"""Park and zone trees for the web app's "Park trees" layer (context only): python scripts/web_export_parks.py
Inventories `arbrat-parcs` and `arbrat-zona` (Open Data BCN, CC BY 4.0; the latest CSV of each package, found through the
portal's CKAN API and cached in databases/barcelona/raw/) are cut to the Porta site grid. Height and crown come from the
LiDAR canopy height model of scripts/bcn_lidar_porta.py (raw/lidar/porta_chm_05m.tif, flown 26 Sept 2021).
Display only: these trees are not decision rows and are not scored. Their canopy is already in the model as fixed
background canopy (site.py `background`: CHM >= 2 m outside the street-tree crowns).
Writes web/public/data/porta*/parks.json and a `parks` entry in each meta.json. Run after python -m shade_sponge.web_export."""
import sys, json, glob, numpy as np, pandas as pd, requests, rasterio
from pyproj import Transformer
from scipy.spatial import cKDTree
sys.path.insert(0, ".")
from shade_sponge.site import load_site, ROOT

RAW = ROOT / "databases/barcelona/raw"
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show?id="
PACKAGES = {"park": "arbrat-parcs", "zone": "arbrat-zona"}
R_MAX, R_MIN, R_TOP = 6.0, 1.5, 2.0   # m: crown search radius cap/floor, radius for the top height (ASSUMPTION, display only)
BASE_FRAC = 0.35                       # crown base / height (ASSUMPTION, display only)
NO_CANOPY = (3.0, 2.0)                 # height, crown (m) drawn when the CHM shows no crown (young or missing tree; ASSUMPTION)


def inventory(kind, pkg):
    f = RAW / f"{pkg.replace('-', '_')}.csv"
    if not f.exists():
        res = requests.get(API + pkg, timeout=60).json()["result"]["resources"]
        csv = [r for r in res if r.get("format", "").upper() == "CSV"]
        url = max(csv, key=lambda r: r.get("last_modified") or r.get("created") or "")["url"]
        f.write_bytes(requests.get(url, timeout=600).content)
        print("downloaded", url)
    t = pd.read_csv(f, low_memory=False)
    if "espai_verd" not in t:                     # the green space's name, when the inventory has it
        t["espai_verd"] = ""
    return t[["codi", "x_etrs89", "y_etrs89", "cat_nom_cientific", "espai_verd"]].assign(kind=kind)


site = load_site("porta")
H, W = site.domain.shape
t = pd.concat([inventory(k, p) for k, p in PACKAGES.items()], ignore_index=True).dropna(subset=["x_etrs89", "y_etrs89"])
col, row = ((t.x_etrs89 - site.x0) / site.res).astype(int), ((site.y1 - t.y_etrs89) / site.res).astype(int)
ok = (col >= 0) & (col < W) & (row >= 0) & (row < H)
ok[ok] = site.domain[row[ok], col[ok]]                      # inside Porta
t = t[ok].reset_index(drop=True)

with rasterio.open(RAW / "lidar/porta_chm_05m.tif") as src:
    chm, T = np.nan_to_num(src.read(1)), src.transform
cres = T.a
yy, xx = np.mgrid[0:chm.shape[0], 0:chm.shape[1]]
# crown search radius: half the distance to the nearest other tree (park, zone or street), within [R_MIN, R_MAX]
allxy = np.r_[t[["x_etrs89", "y_etrs89"]].to_numpy(), site.trees[["x", "y"]].to_numpy()]
d, _ = cKDTree(allxy).query(t[["x_etrs89", "y_etrs89"]].to_numpy(), k=2)
radius = np.clip(d[:, 1] / 2, R_MIN, R_MAX)
h, cd, none = [], [], []
for (x, y), r in zip(t[["x_etrs89", "y_etrs89"]].to_numpy(), radius):
    c0, r0 = (x - T.c) / cres, (T.f - y) / cres
    sl = (slice(max(int(r0 - R_MAX / cres), 0), int(r0 + R_MAX / cres) + 1), slice(max(int(c0 - R_MAX / cres), 0), int(c0 + R_MAX / cres) + 1))
    dist = np.hypot(xx[sl] + 0.5 - c0, yy[sl] + 0.5 - r0) * cres
    z = chm[sl]
    top = z[dist <= R_TOP].max(initial=0)
    none.append(top < 2)
    if top < 2:
        h.append(NO_CANOPY[0]); cd.append(NO_CANOPY[1]); continue
    area = ((z >= 2) & (dist <= r)).sum() * cres ** 2
    h.append(round(float(top), 1)); cd.append(round(float(2 * np.sqrt(area / np.pi)), 1))

lon, lat = Transformer.from_crs(25831, 4326, always_xy=True).transform(t.x_etrs89.to_numpy(), t.y_etrs89.to_numpy())
out = dict(id=t.codi.astype(str).tolist(), kind=t.kind.tolist(), place=t.espai_verd.fillna("").tolist(),
           species=t.cat_nom_cientific.fillna("unknown").tolist(), lon=np.round(lon, 6).tolist(), lat=np.round(lat, 6).tolist(),
           height_m=h, crown_diam_m=cd, crown_base_m=[round(BASE_FRAC * v, 1) for v in h])
entry = dict(file="parks.json", n=len(t), park=int((t.kind == "park").sum()), zone=int((t.kind == "zone").sum()),
             no_canopy=int(sum(none)))
for f in sorted(glob.glob(str(ROOT / "web/public/data/porta*/meta.json"))):
    json.dump(out, open(f.replace("meta.json", "parks.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    meta = json.load(open(f, encoding="utf-8"))
    meta["parks"] = entry
    json.dump(meta, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(entry)
