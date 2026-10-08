"""Runoff module v1: event runoff volume for Porta under design storms, per tree-layout scenario.

Method (notes/methodology.md section 4), on a 1 m grid over Porta:
  1. Storm depth P = PDISBA design intensity(T, d) x d   (databases/barcelona/pdisba_idf_city.csv)
  2. Canopy interception under each crown disk: I = min(P, s * LAI)  (storage bucket; overlapping crowns -> max)
  3. Effective rain P_eff = P - I  ->  SCS curve number runoff Q(P_eff, CN) per cell; volume = sum(Q * area)
Surfaces: roofs (OSM footprints) CN 98; sealed open space CN 98; pervious (NDVI >= 0.3 and CHM < 2 m, or OSM park/garden/grass) CN 74.
Stemflow ignored (<1% of rain; Anys & Weiler 2024). Wet-canopy evaporation during the event ignored (short storms; conservative).
Parameters marked ASSUMPTION must be calibrated/verified (s against Anys & Weiler 2024 open data; CN values from USDA TR-55).
Outputs: databases/barcelona/runoff_scenarios.csv, exchange/to_gh/porta_tree_interception_S0.csv
"""
import json, pathlib, numpy as np, pandas as pd, geopandas as gpd, rasterio, osmnx as ox
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from shapely.geometry import Point

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, DB, EX = ROOT / "databases/barcelona/raw", ROOT / "databases/barcelona", ROOT / "exchange"
RES = 1.0
P_ = dict(
    s_mm_per_lai=1.75,          # CALIBRATED: effective event storage per unit LAI, Anys & Weiler 2024 data (scripts/calibrate_interception.py;
                                # pooled median 1.75, IQR ~1.45-1.92; includes evaporation during events). Lower bound 0.86 = surface storage only (Xiao et al. 2015, abstract)
    cn_sealed=98, cn_roof=98,   # ASSUMPTION: USDA TR-55 impervious
    cn_pervious=74,             # ASSUMPTION: TR-55 open space, good condition, HSG C (soil group unknown)
    ndvi_green=0.3,
    background_lai=2.3,         # ASSUMPTION: LAI of non-street canopy (median LiDAR proxy of street trees)
)
STORMS = [(1, 60), (2, 60), (10, 60), (2, 20)]          # (return period yr, duration min)
CANDIDATES = ["Celtis australis", "Melia azedarach", "Tipuana tipu", "Jacaranda mimosifolia",
              "Pyrus calleryana", "Brachychiton populneus"]
YOUNG_CROWN_M = 3.0                                      # ASSUMPTION: crown diameter of a newly planted tree

o = json.load(open(EX / "site_origin.json"))
OX, OY = o["origin_x"], o["origin_y"]
b = pd.read_csv(RAW / "BarcelonaCiutat_Barris.csv")
site = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
site = site[site.nom_barri == "Porta"]
x0, y0, x1, y1 = site.total_bounds
W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
T = from_origin(x0, y1, RES, RES)
domain = rasterize([(site.geometry.iloc[0], 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)


def to_grid(path):
    out = np.full((H, W), np.nan, "float32")
    with rasterio.open(path) as src:
        reproject(rasterio.band(src, 1), out, dst_transform=T, dst_crs="EPSG:25831", resampling=Resampling.average,
                  dst_nodata=np.nan)
    return out


# ---- surfaces
bld = gpd.read_file(EX / "to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
bld = bld.set_geometry(bld.translate(OX, OY)).set_crs(25831)
roof = rasterize(((g, 1) for g in bld.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
ndvi_crop = RAW / "porta_ndvi_2017.tif"
if not ndvi_crop.exists():
    a = to_grid(RAW / "2017_NDVI.tif")
    with rasterio.open(ndvi_crop, "w", driver="GTiff", width=W, height=H, count=1, dtype="float32", crs="EPSG:25831",
                       transform=T, nodata=np.nan, compress="deflate") as d:
        d.write(a, 1)
with rasterio.open(ndvi_crop) as s:
    ndvi = s.read(1)
ndvi[(ndvi < -1) | (ndvi > 1)] = np.nan
chm = to_grid(RAW / "lidar/porta_chm_05m.tif")
green = ox.features_from_polygon(site.to_crs(4326).iloc[0].geometry,
                                 tags={"leisure": ["park", "garden"], "landuse": ["grass"]})
green = green[green.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(25831)
osm_green = rasterize(((g, 1) for g in green.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool) if len(green) else np.zeros((H, W), bool)
pervious = domain & ~roof & (((np.nan_to_num(ndvi) >= P_["ndvi_green"]) & (np.nan_to_num(chm) < 2)) | osm_green)
sealed = domain & ~roof & ~pervious
CN = np.where(roof, P_["cn_roof"], np.where(pervious, P_["cn_pervious"], P_["cn_sealed"])).astype("float32")
print(f"Porta {domain.sum() / 1e4:.1f} ha: roofs {roof[domain].mean():.0%}, sealed open space {sealed[domain].mean():.0%}, "
      f"pervious {pervious[domain].mean():.0%}")


BACKGROUND = np.zeros((H, W), bool)                      # set after the street trees are loaded


def scs(p, cn):
    s = 25.4 * (1000.0 / cn - 10.0)
    ia = 0.2 * s
    return np.where(p > ia, (p - ia) ** 2 / (p - ia + s), 0.0)


def storage_raster(trees):
    """trees: DataFrame with x, y (EPSG:25831), crown_diam_m, lai -> canopy storage S (mm) per cell (max where crowns overlap)."""
    shapes = [(Point(r.x, r.y).buffer(r.crown_diam_m / 2), P_["s_mm_per_lai"] * r.lai)
              for r in trees.itertuples() if r.crown_diam_m > 0 and r.lai > 0]
    shapes.sort(key=lambda t: t[1])                  # rasterize ascending so the largest storage wins on overlap
    S = rasterize(shapes, out_shape=(H, W), transform=T, fill=0, dtype="float32", merge_alg=rasterio.enums.MergeAlg.replace)
    S[roof] = 0                                      # crowns over roofs do not change roof runoff (downpipes)
    bg = BACKGROUND & (S == 0)                       # park/private canopy, fixed across scenarios
    S[bg] = P_["s_mm_per_lai"] * P_["background_lai"]
    return S


def run(S, p):
    peff = np.clip(p - S, 0, None)
    q = scs(peff, CN)
    m = domain
    return dict(runoff_m3=float((q[m] * RES ** 2).sum() / 1000), runoff_open_space_m3=float((q[m & ~roof] * RES ** 2).sum() / 1000),
                interception_m3=float((np.minimum(S, p)[m] * RES ** 2).sum() / 1000), canopy_ha=float((S[m] > 0).sum() * RES ** 2 / 1e4))


# ---- trees and scenarios
t = pd.read_csv(EX / "to_gh/porta_trees_lidar.csv")
t = t[t.flag == "ok"].copy()
t["x"], t["y"], t["lai"] = t.x + OX, t.y + OY, t.lai_proxy
sp = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species")
# background canopy = LiDAR canopy > 2 m that is NOT a current street-tree crown (parks, squares, private gardens)
street_now = rasterize(((Point(r.x, r.y).buffer(r.crown_diam_m / 2), 1) for r in t.itertuples()), out_shape=(H, W),
                       transform=T, fill=0).astype(bool)
BACKGROUND = domain & ~roof & (np.nan_to_num(chm) >= 2) & ~street_now
print(f"canopy: street trees {street_now[domain].sum() / 1e4:.1f} ha, background {BACKGROUND.sum() / 1e4:.1f} ha")
planes = t.is_plane
scen = {"S_none_street": t.iloc[0:0], "S0_current": t}
for c in CANDIDATES:
    for tag, diam in (("mature", sp.loc[c, "crown_diam_med"]), ("young", YOUNG_CROWN_M)):
        r = t.copy()
        r.loc[planes, "crown_diam_m"] = diam
        r.loc[planes, "lai"] = sp.loc[c, "lai_proxy_med"]
        scen[f"R_{c.split()[0]}_{tag}"] = r
idf = pd.read_csv(DB / "pdisba_idf_city.csv").set_index(["T_years", "duration_min"])
rows = []
for name, trees in scen.items():
    S = storage_raster(trees)
    for T_, d in STORMS:
        p = idf.loc[(T_, d), "design_intensity_mmh"] * d / 60
        rows.append(dict(scenario=name, T_years=T_, duration_min=d, P_mm=round(p, 1), **run(S, p)))
res = pd.DataFrame(rows)
base = res[res.scenario == "S0_current"].set_index(["T_years", "duration_min"]).runoff_m3
none = res[res.scenario == "S_none_street"].set_index(["T_years", "duration_min"]).runoff_m3
k = list(zip(res.T_years, res.duration_min))
res["d_runoff_vs_S0_pct"] = [round(100 * (v / base[i] - 1), 2) for v, i in zip(res.runoff_m3, k)]
res["tree_effect_vs_none_pct"] = [round(100 * (v / none[i] - 1), 2) for v, i in zip(res.runoff_m3, k)]
res.round(2).to_csv(DB / "runoff_scenarios.csv", index=False)
print(res[(res.T_years == 2) & (res.duration_min == 60)][["scenario", "P_mm", "canopy_ha", "interception_m3", "runoff_m3",
                                                            "d_runoff_vs_S0_pct", "tree_effect_vs_none_pct"]].to_string(index=False))

# per-tree interception for S0 (litres per storm) -> Grasshopper
out = t[["tree_id", "species", "crown_diam_m", "lai"]].copy()
out["x"], out["y"] = (t.x - OX).round(2), (t.y - OY).round(2)
area = np.pi * (t.crown_diam_m / 2) ** 2
for T_, d in STORMS:
    p = idf.loc[(T_, d), "design_intensity_mmh"] * d / 60
    out[f"interception_L_T{T_}_{d}min"] = (area * np.minimum(p, P_["s_mm_per_lai"] * t.lai)).round(1)
out.to_csv(EX / "to_gh/porta_tree_interception_S0.csv", index=False)
json.dump(P_, open(DB / "runoff_params.json", "w"), indent=2)

# sensitivity of the storage coefficient (S0 vs no street trees), all storms
sens = []
for s_ in (0.86, 1.75, 2.2):
    P_["s_mm_per_lai"] = s_
    S0, Sn = storage_raster(t), storage_raster(t.iloc[0:0])
    for T_, d in STORMS:
        p = idf.loc[(T_, d), "design_intensity_mmh"] * d / 60
        a, z = run(S0, p), run(Sn, p)
        sens.append(dict(s_mm_per_lai=s_, T_years=T_, duration_min=d, P_mm=round(p, 1),
                         street_tree_effect_pct=round(100 * (a["runoff_m3"] / z["runoff_m3"] - 1), 2),
                         street_tree_effect_open_space_pct=round(100 * (a["runoff_open_space_m3"] / z["runoff_open_space_m3"] - 1), 2)))
sens = pd.DataFrame(sens)
sens.to_csv(DB / "runoff_sensitivity_storage.csv", index=False)
print(sens.to_string(index=False))
