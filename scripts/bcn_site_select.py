"""Explicit two-step site selection + profile of the chosen barri (Porta).

Run after bcn_site_screening.py and bcn_heat_check.py (project env, see CLAUDE.md).
Step 1 (eligibility, non-compensatory): flood-hazard share, summer LST anomaly and plane density all above the
city's Q-th percentile (Q = 60; also reported for 50 and 70).
Step 2 (ranking of eligible barris): equal-weight mean of 4 normalised criteria (flood, LST, heat vulnerability,
plane density) + share of 2000 random-weight draws in which the barri is top-3.
Outputs: databases/barcelona/site_selection.csv, databases/barcelona/porta_species.csv, notes/figures/porta_profile.png
"""
import pathlib, numpy as np, pandas as pd, geopandas as gpd, rasterio, rasterio.mask, matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, RAW = ROOT / "databases/barcelona", ROOT / "databases/barcelona/raw"
SITE, CRS = "Porta", 25831
C = ["flood_high_share", "lst_anom_C", "heat_high_share", "plane_per_km2"]

s = pd.read_csv(DB / "site_screening_heatcheck.csv").dropna(subset=C).reset_index(drop=True)
norm = lambda v: (v - v.min()) / (v.max() - v.min())
N = pd.concat([norm(s[c]) for c in C], axis=1)
s["score4"] = N.mean(axis=1)
top3 = pd.Series(0, index=s.barri)
for w in np.random.default_rng(2).dirichlet([1] * 4, 2000):
    top3[list(s.barri.values[np.argsort(-(N.values @ w))][:3])] += 1
s["p_top3_4crit"] = s.barri.map(top3 / 2000)
for c in C:
    s[c + "_rank"] = s[c].rank(ascending=False, method="min").astype(int)
for q in (50, 60, 70):
    th = s[C[0]].quantile(q / 100), s[C[1]].quantile(q / 100), s[C[3]].quantile(q / 100)
    s[f"eligible_q{q}"] = (s[C[0]] > th[0]) & (s[C[1]] > th[1]) & (s[C[3]] > th[2])
    e = s[s[f"eligible_q{q}"]].sort_values("score4", ascending=False)
    print(f"Q{q}: {len(e)} eligible -> " + ", ".join(f"{b} ({v:.2f})" for b, v in zip(e.barri, e.score4)))
s.sort_values("score4", ascending=False).round(3).to_csv(DB / "site_selection.csv", index=False)
print(s[s.barri.isin([SITE, "Sant Antoni"])][["barri"] + [c + "_rank" for c in C] + ["score4", "p_top3_4crit"]].round(2).to_string(index=False))

# --- profile of the chosen barri
b = pd.read_csv(RAW / "BarcelonaCiutat_Barris.csv")
barris = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b["geometria_etrs89"]), crs=CRS)
site = barris[barris.nom_barri == SITE]
t = pd.read_csv(DB / "arbrat_viari.csv")
t = t[(t.tipus_element == "ARBRE VIARI") & (t.nom_barri.str.lower() == SITE.lower())]
sp = t.cat_nom_cientific.str.replace(r"\s*'.*", "", regex=True).value_counts()
sp.rename("trees").to_frame().assign(share=lambda d: (d.trees / d.trees.sum()).round(3)).to_csv(DB / "porta_species.csv")
t["street"] = t.adreca.str.replace(r",.*", "", regex=True)
planes = t[t.cat_nom_cientific.str.startswith("Platanus")]
print(f"\n{SITE}: area {site.area.iloc[0] / 1e6:.2f} km2, {len(t)} street trees, {len(planes)} plane trees, {sp.size} taxa")
print("top species:", ", ".join(f"{k} {v}" for k, v in sp.head(8).items()))
print("streets with most plane trees:", ", ".join(f"{k} ({v})" for k, v in planes.street.value_counts().head(6).items()))

fl = gpd.read_file(RAW / "flood_hazard_present.geojson").to_crs(CRS).clip(site)
pts = gpd.GeoDataFrame(t, geometry=gpd.points_from_xy(t.x_etrs89, t.y_etrs89), crs=CRS)
with rasterio.open(RAW / "lst_summer_anomaly.tif") as r:
    lst, tr = rasterio.mask.mask(r, site.geometry, crop=True, nodata=np.nan)
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
fl.plot(column="grid_code", ax=ax[0], cmap="YlGnBu", vmin=5, vmax=50, legend=True, legend_kwds={"label": "Flood-hazard index (5-50)"})
x0, y1 = tr.c, tr.f
im = ax[1].imshow(lst[0], cmap="RdYlBu_r", vmin=-4, vmax=4, extent=(x0, x0 + lst.shape[2] * tr.a, y1 + lst.shape[1] * tr.e, y1))
plt.colorbar(im, ax=ax[1], label="Summer LST anomaly vs city median (°C)")
pts.plot(ax=ax[2], color="lightgrey", markersize=3)
pts[pts.cat_nom_cientific.str.startswith("Platanus")].plot(ax=ax[2], color="darkgreen", markersize=5)
for a, ttl in zip(ax, ["Pluvial flood hazard (Barcelona Regional)", "Surface heat (Landsat 2022-2025)",
                       f"Street trees: plane trees in green ({len(planes)} of {len(t)})"]):
    site.boundary.plot(ax=a, color="black", linewidth=1)
    a.set_title(ttl, fontsize=10)
    a.set_axis_off()
fig.suptitle(f"{SITE} (Nou Barris): study area profile", fontsize=12)
fig.savefig(ROOT / "notes/figures/porta_profile.png", dpi=150, bbox_inches="tight")
