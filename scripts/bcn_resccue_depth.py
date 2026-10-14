"""RESCCUE flood depth for Porta: download the 1D/2D model results and put depth on the runoff-model 1 m grid.

Run with the project env:  ~/miniconda3/envs/shade-and-sponge/python.exe scripts/bcn_resccue_depth.py
Source: PDISBA'19-RESCCUE project (Barcelona Regional / BCASA / Ajuntament de Barcelona), tables rcc_iu1_* read
anonymously from the Resilience Atlas public CARTO account (urbisadmin). Licence not stated: cite the source, keep raw
data and rasters out of git (databases/*/raw/ is gitignored); licence request drafted: notes/resccue_data_request.md.
Columns used: depth2d (assumed m), speed2d (assumed m/s), hzped / hzveh (model hazard classes; hazardped / hazardveh
in t10_futur). Units not stated.
Outputs: databases/barcelona/raw/resccue_<scenario>.geojson + porta_resccue_depth_<scenario>.tif (1 m, EPSG:25831,
same grid as scripts/runoff_model.py), databases/barcelona/resccue_porta_summary.csv, notes/figures/resccue_porta_depth.png
"""
import pathlib, numpy as np, pandas as pd, geopandas as gpd, requests, rasterio, matplotlib.pyplot as plt
from rasterio.features import rasterize
from rasterio.transform import from_origin

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, DB, FIG = ROOT / "databases/barcelona/raw", ROOT / "databases/barcelona", ROOT / "notes/figures"
RAW.mkdir(parents=True, exist_ok=True)
CARTO = "https://urbisadmin.carto.com/api/v2/sql"
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show"
SCENARIOS = {"t10_actual": "T10 present", "t100_actual": "T100 present", "t10_futur": "T10 future", "t100_futur": "T100 future"}
RES = 1.0          # m, as runoff_model.py
BUFFER = 100       # m around Porta for the download, so edge elements are complete. ASSUMPTION
DEPTH_REPORT = 0.15  # m, reporting threshold only (not a hazard criterion; hazard comes from hzped/hzveh). ASSUMPTION


def porta():
    """Porta boundary from the open-data barris file (same as runoff_model.py); if the portal blocks the download
    (it serves a bot-check page to cloud sessions), fall back to the atlas copy barris_bcn (grid may shift by < 1 m)."""
    p = RAW / "BarcelonaCiutat_Barris.csv"
    if not p.exists():
        try:
            r = requests.get(API, params={"id": "20170706-districtes-barris"}, timeout=60).json()["result"]["resources"]
            c = requests.get(next(x["url"] for x in r if x["name"] == p.name), timeout=300).content
            if not c.lstrip().startswith(b"<"):
                p.write_bytes(c)
        except (requests.RequestException, ValueError):
            pass
    if p.exists():
        b = pd.read_csv(p)
        b = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
        return b[b.nom_barri == "Porta"]
    print("open-data barris unavailable: using atlas barris_bcn for the Porta boundary")
    q = "SELECT n_barri, the_geom FROM barris_bcn WHERE n_barri = 'Porta'"
    return gpd.read_file(requests.get(CARTO, params={"q": q, "format": "GeoJSON"}, timeout=120).text).to_crs(25831)


def resccue(tag, bbox):
    p = RAW / f"resccue_{tag}.geojson"
    if not p.exists():
        hz = "hazardped AS hzped, hazardveh AS hzveh" if tag == "t10_futur" else "hzped, hzveh"  # names differ per table
        q = (f"SELECT cartodb_id, depth2d, speed2d, {hz}, the_geom FROM rcc_iu1_{tag} "
             f"WHERE ST_Intersects(the_geom, ST_MakeEnvelope({','.join(map(str, bbox))}, 4326))")
        r = requests.get(CARTO, params={"q": q, "format": "GeoJSON"}, timeout=600)
        r.raise_for_status()
        p.write_bytes(r.content)
    return gpd.read_file(p).to_crs(25831)


site = porta()
bbox = site.buffer(BUFFER).to_crs(4326).total_bounds
x0, y0, x1, y1 = site.total_bounds
W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
T = from_origin(x0, y1, RES, RES)
domain = rasterize([(site.geometry.iloc[0], 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)
cell = RES * RES

rows, grids = [], {}
for tag, label in SCENARIOS.items():
    g = resccue(tag, bbox)
    d = rasterize(zip(g.geometry, g.depth2d), out_shape=(H, W), transform=T, fill=0, dtype="float32")
    d[~domain] = np.nan
    with rasterio.open(RAW / f"porta_resccue_depth_{tag}.tif", "w", driver="GTiff", width=W, height=H, count=1,
                       dtype="float32", crs="EPSG:25831", transform=T, nodata=np.nan) as dst:
        dst.write(d, 1)
    grids[label] = d
    wet = d[domain] > 0
    inside = g[g.intersects(site.geometry.iloc[0])]
    row = {"scenario": label, "elements_in_porta": len(inside),
           "wet_area_ha": wet.sum() * cell / 1e4, "wet_share": wet.mean(),
           f"area_depth_ge_{DEPTH_REPORT}m_ha": (d[domain] >= DEPTH_REPORT).sum() * cell / 1e4,
           "depth_mean_wet_m": d[domain][wet].mean(), "depth_p95_wet_m": np.percentile(d[domain][wet], 95),
           "depth_max_m": d[domain].max()}
    for col in ("hzped", "hzveh"):  # area per hazard class, from element areas clipped to Porta
        a = gpd.clip(g[[col, "geometry"]], site).assign(a=lambda x: x.area / 1e4).groupby(col).a.sum()
        row.update({f"{col}_{k}_ha": v for k, v in a.items()})
    rows.append(row)
    print(f"{label}: {len(g)} elements downloaded, wet {row['wet_area_ha']:.1f} ha, max depth {row['depth_max_m']:.2f}")

out = pd.DataFrame(rows).round(3)
out.to_csv(DB / "resccue_porta_summary.csv", index=False)
print(out.T.to_string())

vmax = np.nanpercentile(grids["T100 present"][grids["T100 present"] > 0], 99)
fig, ax = plt.subplots(2, 2, figsize=(10, 10), constrained_layout=True)
for a, (label, d) in zip(ax.flat, grids.items()):
    im = a.imshow(np.where(d > 0, d, np.nan), cmap="Blues", vmin=0, vmax=vmax, extent=(x0, x0 + W * RES, y1 - H * RES, y1))
    site.boundary.plot(ax=a, color="k", lw=0.6)
    a.set_title(label); a.set_axis_off()
fig.colorbar(im, ax=ax, shrink=0.6, label="Water depth (depth2d, assumed m)")
fig.suptitle("Porta: RESCCUE 1D/2D model flood depth\nSource: PDISBA'19-RESCCUE (Barcelona Regional / Ajuntament de Barcelona)")
fig.savefig(FIG / "resccue_porta_depth.png", dpi=150)
