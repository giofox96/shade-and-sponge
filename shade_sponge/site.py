"""Site bundle: what the tool needs about one site on one grid, built once and cached in cache/site_<name>.npz.
A new site = a new build_<name>() + trees_<name>() returning the same keys/columns. Coordinates: EPSG:25831, 1 m cells."""
import json, pathlib, re, numpy as np, pandas as pd, geopandas as gpd, rasterio
from types import SimpleNamespace
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from scipy import ndimage
from shapely.geometry import Point
from . import topo

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, DB, EX = ROOT / "databases/barcelona/raw", ROOT / "databases/barcelona", ROOT / "exchange"
RES = 1.0
HAZARD_HIGH = 40        # Resilience Atlas flood-hazard index classes >= 40 = "high hazard" (same threshold as the site screening)
CAPTURE_M = 100.0       # ASSUMPTION: surface water reaches a hotspot only if its flow path gets there within this distance
                        # (stand-in for sewer inlets taking it on the way; test 50–200 m). Unlimited: 97% of open ground
                        # would drain to some hotspot, so position would no longer matter


def norm(name):
    """Species without cultivar or trade mark: "Pyrus calleryana 'Chanticleer'" -> "Pyrus calleryana"."""
    return re.sub(r"\s*'[^']*'|\s+\S*®", "", name).strip()


def rc(site, x, y):
    """Row, column of EPSG:25831 coordinates on the site grid (clipped to the grid)."""
    r = np.clip(((site.y1 - np.asarray(y)) / site.res).astype(int), 0, site.domain.shape[0] - 1)
    c = np.clip(((np.asarray(x) - site.x0) / site.res).astype(int), 0, site.domain.shape[1] - 1)
    return r, c


def trees_porta():
    """All street trees with LiDAR crowns (exchange/to_gh/porta_trees_lidar.csv), back in EPSG:25831."""
    o = json.load(open(EX / "site_origin.json"))
    t = pd.read_csv(EX / "to_gh/porta_trees_lidar.csv")
    t["x"], t["y"], t["lai"], t["sp"] = t.x + o["origin_x"], t.y + o["origin_y"], t.lai_proxy, t.species.map(norm)
    return t


def build_porta():
    """Surfaces exactly as runoff module v1 (scripts/runoff_model.py), plus LiDAR DTM and building heights,
    the flood-hazard index and the surface-water routing (topo.py)."""
    import osmnx as ox
    o = json.load(open(EX / "site_origin.json"))
    b = pd.read_csv(RAW / "BarcelonaCiutat_Barris.csv")
    site = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
    site = site[site.nom_barri == "Porta"]
    x0, y0, x1, y1 = site.total_bounds
    W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
    T = from_origin(x0, y1, RES, RES)
    domain = rasterize([(site.geometry.iloc[0], 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)

    def grid(path):
        out = np.full((H, W), np.nan, "float32")
        with rasterio.open(path) as src:
            reproject(rasterio.band(src, 1), out, dst_transform=T, dst_crs="EPSG:25831", resampling=Resampling.average,
                      dst_nodata=np.nan)
        return out

    def fill_nan(a):                                     # nearest valid value (DTM holes under buildings, grid edges)
        return a[tuple(ndimage.distance_transform_edt(np.isnan(a), return_distances=False, return_indices=True))]

    # surfaces (runoff module v1)
    bld = gpd.read_file(EX / "to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
    bld = bld.set_geometry(bld.translate(o["origin_x"], o["origin_y"])).set_crs(25831)
    roof = rasterize(((g, 1) for g in bld.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    with rasterio.open(RAW / "porta_ndvi_2017.tif") as s:      # cropped by scripts/runoff_model.py
        ndvi = s.read(1)
    ndvi[(ndvi < -1) | (ndvi > 1)] = np.nan
    chm = grid(RAW / "lidar/porta_chm_05m.tif")
    green = ox.features_from_polygon(site.to_crs(4326).iloc[0].geometry,
                                     tags={"leisure": ["park", "garden"], "landuse": ["grass"]})
    green = green[green.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(25831)
    osm_green = rasterize(((g, 1) for g in green.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    P = json.load(open(DB / "runoff_params.json"))
    pervious = domain & ~roof & (((np.nan_to_num(ndvi) >= P["ndvi_green"]) & (np.nan_to_num(chm) < 2)) | osm_green)
    cn = np.where(roof, P["cn_roof"], np.where(pervious, P["cn_pervious"], P["cn_sealed"])).astype("float32")
    t = trees_porta()
    t = t[t.flag == "ok"]
    street = rasterize(((Point(r.x, r.y).buffer(r.crown_diam_m / 2), 1) for r in t.itertuples()), out_shape=(H, W),
                       transform=T, fill=0).astype(bool)
    background = domain & ~roof & (np.nan_to_num(chm) >= 2) & ~street   # park/private canopy, fixed in every layout

    # topography, buildings, flood hazard
    dtm = fill_nan(grid(RAW / "lidar/porta_dtm_05m.tif"))
    bldg_h = np.nan_to_num(grid(RAW / "lidar/porta_bldg_05m.tif")).clip(0, None)   # LiDAR building height above ground
                                                         # (whole grid, also outside Porta, so edge streets get shaded)
    hz = gpd.read_file(RAW / "flood_hazard_present.geojson").to_crs(25831).cx[x0:x1, y0:y1]
    hot = rasterize(((g, 1) for g, v in zip(hz.geometry, hz.grid_code) if v >= HAZARD_HIGH), out_shape=(H, W),
                    transform=T, fill=0).astype(bool)
    recv, order = topo.route(dtm + bldg_h)               # buildings are obstacles to surface flow
    acc = topo.accumulate(recv, order, (~roof) * RES ** 2)
    dist_hot = topo.flow_distance(recv, order, hot & ~roof, RES)
    lon, lat = gpd.GeoSeries(site.centroid, crs=25831).to_crs(4326).iloc[0].coords[0]
    return dict(x0=x0, y1=y1, res=RES, lat=lat, lon=lon, domain=domain, roof=roof, cn=cn, background=background,
                dtm=dtm.astype("float32"), bldg_h=bldg_h.astype("float32"), hot=hot, acc=acc.astype("float32"),
                dist_hot=dist_hot.astype("float32"))


def load_site(name="porta", capture_m=CAPTURE_M):
    f = ROOT / f"cache/site_{name}.npz"
    if not f.exists():
        f.parent.mkdir(exist_ok=True)
        np.savez_compressed(f, **globals()[f"build_{name}"]())
    z = np.load(f)
    s = SimpleNamespace(**{k: (z[k].item() if z[k].ndim == 0 else z[k]) for k in z.files}, name=name)
    s.transform = from_origin(s.x0, s.y1, s.res, s.res)
    s.to_hot = s.dist_hot <= capture_m                    # ground whose runoff reaches a high-hazard cell
    s.trees = globals()[f"trees_{name}"]()
    return s
