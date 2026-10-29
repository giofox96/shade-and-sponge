"""Site bundle: what the tool needs about one site on one grid, built once and cached in cache/site_<name>.npz.
Porta: build_porta() (validated bundle); any other barri: build_barri(name), same model with a BUFFER_M margin. Coordinates: EPSG:25831, 1 m cells."""
import json, pathlib, re, unicodedata, numpy as np, pandas as pd, geopandas as gpd, rasterio
from types import SimpleNamespace
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from scipy import ndimage
from shapely.geometry import Point
from . import topo

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, DB, EX = ROOT / "databases/barcelona/raw", ROOT / "databases/barcelona", ROOT / "exchange"
BARRIS = DB / "barris"   # per-barri inputs (scripts/bcn_lidar_barri.py)
RES = 1.0
BUFFER_M = 150.0        # grid margin around a barri: at the lowest winter design sun (15°) a 40 m building casts a 149 m
                        # shadow, and the CAPTURE_M flow path stays on the grid (notes/citywide_plan.md §6.2 step 3)
# Species whose Porta LiDAR sample is too small: crown/height/LAI medians replaced by a city-wide LiDAR sample (user, 15 Oct, issue #42).
# Styphnolobium: 5 trees in Porta; no_merge_flag row = 367 trees on 25 streets in one 1 km tile (scripts/bcn_lidar_species_sample.py).
CITY_LIDAR = {"Styphnolobium japonicum": ("styphnolobium_lidar_summary.csv", "no_merge_flag")}
HAZARD_HIGH = 40        # Resilience Atlas flood-hazard index classes >= 40 = "high hazard" (same threshold as the site screening)
CAPTURE_M = 100.0       # ASSUMPTION: surface water reaches a hotspot only if its flow path gets there within this distance
                        # (stand-in for sewer inlets taking it on the way; test 50–200 m). Unlimited: 97% of open ground
                        # would drain to some hotspot, so position would no longer matter


def osm(polygon, tags, tries=6):
    """OSM features (osmnx) inside a WGS84 polygon, retried with backoff over two Overpass servers (the main one answers
    502 when at capacity)."""
    import time, osmnx as ox
    urls = ["https://overpass-api.de/api", "https://overpass.kumi.systems/api"]
    for i in range(tries):
        ox.settings.overpass_url = urls[i % 2]
        try:
            return ox.features_from_polygon(polygon, tags=tags)
        except Exception as e:                               # 502/504 or a non-JSON answer from a busy server
            if i == tries - 1:
                raise
            print(f"Overpass: {type(e).__name__}; retrying in {15 * 2 ** i} s on {urls[(i + 1) % 2]}")
            time.sleep(15 * 2 ** i)


def species_lidar(summary="porta_species_lidar_summary.csv"):
    """Per-species LiDAR medians (Porta, or species_lidar_summary.csv for the Barcelona palette), with the CITY_LIDAR
    overrides applied. The one place where the tool and the runoff scripts get species crown, height and LAI."""
    sp = pd.read_csv(DB / summary).set_index("species")
    for name, (f, group) in CITY_LIDAR.items():
        c = pd.read_csv(DB / f).set_index("group").loc[group]
        sp.loc[name, ["n", "height_med", "crown_diam_med", "crown_base_med", "lai_proxy_med", "lai_proxy_iqr"]] = [
            c.n, c.height_m_median, c.crown_diam_m_median, c.crown_base_m_median, c.lai_proxy_median, c.lai_proxy_iqr]
        sp.loc[name, "gap_med"] = float("nan")     # not in the city summary; unused by the tool
    return sp


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
    the flood-hazard index and the surface-water routing (topo.py). Grid = Porta's bare bounding box (kept for regression)."""
    o = json.load(open(EX / "site_origin.json"))
    bld = gpd.read_file(EX / "to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
    bld = bld.set_geometry(bld.translate(o["origin_x"], o["origin_y"])).set_crs(25831)

    def ndvi(grid):
        with rasterio.open(RAW / "porta_ndvi_2017.tif") as s:      # cropped by scripts/runoff_model.py
            return s.read(1)
    return _build(barri("Porta"), 0.0, bld, ndvi, RAW / "lidar/porta", trees_porta())


def slug(name):
    """File name of a barri: "la Vila de Gràcia" -> "la-vila-de-gracia"."""
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()).strip("-")


def barri(name):
    """One barri polygon (Open Data BCN, EPSG:25831), by name or slug."""
    b = pd.read_csv(RAW / "BarcelonaCiutat_Barris.csv")
    b = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
    b = b[(b.nom_barri == name) | (b.nom_barri.map(slug) == name)]
    if b.empty:
        raise SystemExit(f"no barri called {name!r} in BarcelonaCiutat_Barris.csv")
    return b


def trees_barri(name):
    """Street trees of one barri with LiDAR crowns (scripts/bcn_lidar_barri.py), EPSG:25831."""
    t = pd.read_csv(BARRIS / slug(name) / "trees_lidar.csv")
    t["lai"], t["sp"] = t.lai_proxy, t.species.map(norm)
    return t


def build_barri(name):
    """Any barri, same model as Porta: grid = barri + BUFFER_M, domain = the barri polygon (notes/citywide_plan.md §6.2).
    Inputs from scripts/bcn_lidar_barri.py; NDVI cropped from the city raster raw/2017_NDVI.tif."""
    d = BARRIS / slug(name)
    bld = gpd.read_file(d / "buildings.geojson").to_crs(25831)
    return _build(barri(name), BUFFER_M, bld, lambda grid: grid(RAW / "2017_NDVI.tif"), RAW / f"lidar/{slug(name)}",
                  trees_barri(name))


def _build(site, buf, bld, ndvi_of, lidar, trees):
    x0, y0, x1, y1 = site.total_bounds + np.array([-buf, -buf, buf, buf])
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
    roof = rasterize(((g, 1) for g in bld.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    ndvi = ndvi_of(grid)
    ndvi[(ndvi < -1) | (ndvi > 1)] = np.nan
    chm = grid(f"{lidar}_chm_05m.tif")
    try:
        local = RAW / "osm/green.gpkg"                    # scripts/osm_buildings.py (BBBike extract), no Overpass needed
        green = gpd.read_file(local, mask=site.geometry.iloc[0]) if local.exists() else \
            osm(site.to_crs(4326).iloc[0].geometry, {"leisure": ["park", "garden"], "landuse": ["grass"]}, tries=3)
        green = green[green.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(25831)
        osm_green = rasterize(((g, 1) for g in green.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    except Exception as e:                               # pervious ground then comes from NDVI alone
        print(f"WARNING: no OSM green areas ({type(e).__name__}); pervious ground from NDVI only. Delete the cache and rebuild later")
        osm_green = np.zeros((H, W), bool)
    P = json.load(open(DB / "runoff_params.json"))
    pervious = domain & ~roof & (((np.nan_to_num(ndvi) >= P["ndvi_green"]) & (np.nan_to_num(chm) < 2)) | osm_green)
    cn = np.where(roof, P["cn_roof"], np.where(pervious, P["cn_pervious"], P["cn_sealed"])).astype("float32")
    t = trees[trees.flag == "ok"]
    street = rasterize(((Point(r.x, r.y).buffer(r.crown_diam_m / 2), 1) for r in t.itertuples()), out_shape=(H, W),
                       transform=T, fill=0).astype(bool)
    background = domain & ~roof & (np.nan_to_num(chm) >= 2) & ~street   # park/private canopy, fixed in every layout

    # topography, buildings, flood hazard
    dtm = fill_nan(grid(f"{lidar}_dtm_05m.tif"))
    bldg_h = np.nan_to_num(grid(f"{lidar}_bldg_05m.tif")).clip(0, None)   # LiDAR building height above ground
                                                         # (whole grid, also outside the barri, so edge streets get shaded)
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
    """Porta (build_porta, the validated bundle) or any other barri by name or slug (build_barri)."""
    name = slug(name)
    porta = name == "porta"
    f = ROOT / f"cache/site_{name}.npz"
    if not f.exists():
        f.parent.mkdir(exist_ok=True)
        np.savez_compressed(f, **(build_porta() if porta else build_barri(name)))
    z = np.load(f)
    s = SimpleNamespace(**{k: (z[k].item() if z[k].ndim == 0 else z[k]) for k in z.files}, name=name)
    s.transform = from_origin(s.x0, s.y1, s.res, s.res)
    s.to_hot = s.dist_hot <= capture_m                    # ground whose runoff reaches a high-hazard cell
    s.trees = trees_porta() if porta else trees_barri(name)
    return s
