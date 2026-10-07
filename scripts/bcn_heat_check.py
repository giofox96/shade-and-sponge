"""Physical heat check + weight sensitivity for the Barcelona site screening.

Run after scripts/bcn_site_screening.py, with the project env (see CLAUDE.md).
1. Summer daytime land-surface temperature (LST) anomaly from Landsat 8/9 Collection 2 L2 (Microsoft Planetary Computer),
   June-August 2022-2025, cloud cover < 10%; per scene LST minus the city median, then median over scenes (30 m).
2. Re-rank barris with LST anomaly instead of the 2015 heat-vulnerability index.
3. Random-weight test (1000 Dirichlet draws): how often each barri ranks first / top-3.
Outputs: databases/barcelona/raw/lst_summer_anomaly.tif, databases/barcelona/site_screening_heatcheck.csv,
         notes/figures/bcn_lst_anomaly.png
"""
import pathlib, numpy as np, pandas as pd, geopandas as gpd, rasterio, matplotlib.pyplot as plt
import pystac_client, planetary_computer
from rasterio.vrt import WarpedVRT
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterstats import zonal_stats

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/barcelona/raw"
TIF = RAW / "lst_summer_anomaly.tif"
CRS, RES = 25831, 30

b = pd.read_csv(RAW / "BarcelonaCiutat_Barris.csv")
barris = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b["geometria_etrs89"]), crs=CRS).rename(columns={"nom_barri": "barri"})
x0, y0, x1, y1 = barris.total_bounds
W, H = int((x1 - x0) / RES) + 1, int((y1 - y0) / RES) + 1
T = from_origin(x0, y1, RES, RES)
city = ~geometry_mask(barris.geometry, (H, W), T)

if not TIF.exists():
    cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
    items = [i for i in cat.search(collections=["landsat-c2-l2"], bbox=list(barris.to_crs(4326).total_bounds),
                                   datetime="2022-06-01/2025-08-31", query={"eo:cloud_cover": {"lt": 10}}).items()
             if i.datetime.month in (6, 7, 8) and i.properties.get("platform") in ("landsat-8", "landsat-9")]
    print(f"{len(items)} summer scenes")
    stack = []
    for it in items:
        bands = {}
        for k in ("lwir11", "qa_pixel"):
            with rasterio.open(it.assets[k].href) as src, WarpedVRT(src, crs=f"EPSG:{CRS}", transform=T, width=W, height=H,
                                                                     resampling=rasterio.enums.Resampling.nearest) as v:
                bands[k] = v.read(1).astype("float64")
        qa = bands["qa_pixel"].astype("uint16")
        bad = (qa & (1 << 1 | 1 << 3 | 1 << 4)) > 0 | (bands["lwir11"] == 0)   # dilated cloud, cloud, shadow, nodata
        lst = bands["lwir11"] * 0.00341802 + 149.0 - 273.15
        lst[bad | ~city] = np.nan
        if np.isfinite(lst[city]).mean() < 0.8:          # skip scenes with <80% clear city pixels
            continue
        stack.append(lst - np.nanmedian(lst))
        print(it.datetime.date(), it.properties["platform"], f"city median {np.nanmedian(lst + 0):.1f} C")
    anom = np.nanmedian(np.stack(stack), axis=0)
    with rasterio.open(TIF, "w", driver="GTiff", width=W, height=H, count=1, dtype="float32", crs=f"EPSG:{CRS}",
                       transform=T, nodata=np.nan) as dst:
        dst.write(anom.astype("float32"), 1)
    print(f"used {len(stack)} scenes")

s = pd.read_csv(ROOT / "databases/barcelona/site_screening_barris.csv")
zs = zonal_stats(barris.geometry, str(TIF), stats=["mean"], nodata=np.nan)
lst = pd.Series([z["mean"] for z in zs], index=barris.barri, name="lst_anom_C")
s = s.join(lst, on="barri")
norm = lambda v: (v - v.min()) / (v.max() - v.min())
F, Hv, L, P = (norm(s[c]) for c in ("flood_high_share", "heat_high_share", "lst_anom_C", "plane_per_km2"))
s["score_lst"] = (F + L + P) / 3
rng = np.random.default_rng(1)
for name, heat in (("vuln", Hv), ("lst", L)):
    first, top3 = pd.Series(0, index=s.barri), pd.Series(0, index=s.barri)
    for w in rng.dirichlet([1, 1, 1], 1000):
        r = (w[0] * F + w[1] * heat + w[2] * P).values
        order = s.barri.values[np.argsort(-r)]
        first[order[0]] += 1
        top3[list(order[:3])] += 1
    s[f"p_first_{name}"], s[f"p_top3_{name}"] = s.barri.map(first / 1000), s.barri.map(top3 / 1000)
s = s.sort_values("score_lst", ascending=False)
s.round(3).to_csv(ROOT / "databases/barcelona/site_screening_heatcheck.csv", index=False)
print(s[["barri", "lst_anom_C", "flood_high_share", "plane_per_km2", "score", "score_lst",
         "p_first_vuln", "p_top3_vuln", "p_first_lst", "p_top3_lst"]].head(10).round(2).to_string(index=False))

with rasterio.open(TIF) as r:
    a = r.read(1)
fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(a, cmap="RdYlBu_r", vmin=-6, vmax=6, extent=(x0, x0 + W * RES, y1 - H * RES, y1))
barris.boundary.plot(ax=ax, color="grey", linewidth=0.3)
barris[barris.barri == "Sant Antoni"].boundary.plot(ax=ax, color="black", linewidth=1.5)
plt.colorbar(im, ax=ax, shrink=0.7, label="Summer daytime LST anomaly vs city median (°C)")
ax.set_title("Barcelona summer land-surface temperature anomaly, Landsat 8/9 2022–2025 (Sant Antoni outlined)", fontsize=10)
ax.set_axis_off()
fig.savefig(ROOT / "notes/figures/bcn_lst_anomaly.png", dpi=150, bbox_inches="tight")
