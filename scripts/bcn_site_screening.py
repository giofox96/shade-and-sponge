"""Rank Barcelona neighbourhoods (barris) where pluvial flood hazard, heat vulnerability and plane trees overlap.

Run with the project env:  ~/miniconda3/envs/shade-and-sponge/python.exe scripts/bcn_site_screening.py
Inputs (downloaded once into databases/barcelona/raw/):
  - Flood hazard index 5-50, present scenario (Barcelona Regional, via Resilience Atlas public CARTO layer ar_in_perill_inun)
  - Heat-wave global vulnerability 2015 (open data: factor-de-vulnerabilitat / 2015_vulnera_global.gpkg)
  - Neighbourhood boundaries (open data: 20170706-districtes-barris)
  - Street trees (databases/barcelona/arbrat_viari.csv, from scripts/species_coverage.py)
Outputs: databases/barcelona/site_screening_barris.csv, notes/figures/bcn_site_screening.png
"""
import pathlib, re, unicodedata, requests, pandas as pd, geopandas as gpd, matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/barcelona/raw"
RAW.mkdir(parents=True, exist_ok=True)
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show"
CRS = 25831
FLOOD_HIGH = 40   # warm-tone classes of the atlas colour ramp (5-50)


def key(name):
    """Match barri names across files: no accents, case, punctuation or articles."""
    n = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", n)


def opendata(ds, name):
    p = RAW / name
    if not p.exists():
        url = next(r["url"] for r in requests.get(API, params={"id": ds}, timeout=60).json()["result"]["resources"] if r["name"] == name)
        p.write_bytes(requests.get(url, timeout=300).content)
    return p


def flood():
    p = RAW / "flood_hazard_present.geojson"
    if not p.exists():  # anonymous public read of the layer shown in the atlas viewer
        q = "SELECT cartodb_id, grid_code, the_geom FROM ar_in_perill_inun"
        p.write_bytes(requests.get("https://urbisadmin.carto.com/api/v2/sql", params={"q": q, "format": "GeoJSON"}, timeout=600).content)
    return gpd.read_file(p).to_crs(CRS)


def area_stats(barris, layer, col, high):
    """Area-weighted mean of `col` and share of covered area with col >= high, per barri."""
    x = gpd.overlay(barris[["barri", "geometry"]], layer[[col, "geometry"]], how="intersection", keep_geom_type=True)
    x["a"] = x.area
    g = x.groupby("barri")
    return pd.DataFrame({"mean": g.apply(lambda d: (d[col] * d.a).sum() / d.a.sum()),
                         "high_share": g.apply(lambda d: d.a[d[col] >= high].sum() / d.a.sum())})


b = pd.read_csv(opendata("20170706-districtes-barris", "BarcelonaCiutat_Barris.csv"))
barris = gpd.GeoDataFrame(b, geometry=gpd.GeoSeries.from_wkt(b["geometria_etrs89"]), crs=CRS).rename(columns={"nom_barri": "barri"})
fl = flood()
heat = gpd.read_file(opendata("factor-de-vulnerabilitat", "2015_vulnera_global.gpkg")).to_crs(CRS)
heat["VulnTot_On"] = pd.to_numeric(heat["VulnTot_On"], errors="coerce")
HEAT_HIGH = heat["VulnTot_On"].quantile(0.8)
print(f"flood index {fl.grid_code.min()}-{fl.grid_code.max()} ({len(fl)} polygons); "
      f"heat class {heat.VulnTot_On.min()}-{heat.VulnTot_On.max()}, top-20% threshold {HEAT_HIGH}")

f = area_stats(barris, fl, "grid_code", FLOOD_HIGH).add_prefix("flood_")
h = area_stats(barris, heat, "VulnTot_On", HEAT_HIGH).add_prefix("heat_")
t = pd.read_csv(ROOT / "databases/barcelona/arbrat_viari.csv", usecols=["cat_nom_cientific", "nom_barri", "tipus_element"])
t = t[t.tipus_element == "ARBRE VIARI"]
t["plane"] = t.cat_nom_cientific.str.startswith("Platanus")
trees = t.groupby(t.nom_barri.map(key)).agg(street_trees=("plane", "size"), plane_trees=("plane", "sum"))

out = barris[["barri", "nom_districte", "geometry"]].copy()
out["key"] = out.barri.map(key)
out = out.join(f, on="barri").join(h, on="barri").join(trees, on="key").drop(columns="key")
out["area_km2"] = out.area / 1e6
out["plane_per_km2"] = out.plane_trees / out.area_km2
norm = lambda s: (s - s.min()) / (s.max() - s.min())
out["score"] = (norm(out.flood_high_share) + norm(out.heat_high_share) + norm(out.plane_per_km2)) / 3
out = out.sort_values("score", ascending=False)
cols = ["barri", "nom_districte", "flood_mean", "flood_high_share", "heat_mean", "heat_high_share",
        "street_trees", "plane_trees", "plane_per_km2", "score"]
out[cols].round(3).to_csv(ROOT / "databases/barcelona/site_screening_barris.csv", index=False)
print(out[cols].head(12).round(2).to_string(index=False))
missing = out[out.street_trees.isna()].barri.tolist()
if missing:
    print("warning: no tree match for", missing)

fig, ax = plt.subplots(1, 4, figsize=(22, 6))
for a, (c, title) in zip(ax, [("flood_high_share", f"Flood hazard: share of area with index >= {FLOOD_HIGH}"),
                              ("heat_high_share", "Heat-wave vulnerability: share in top 20% class"),
                              ("plane_per_km2", "Plane street trees per km²"), ("score", "Combined score (equal weights)")]):
    out.plot(column=c, ax=a, cmap="magma_r", legend=True, edgecolor="white", linewidth=0.3)
    a.set_title(title, fontsize=10)
    a.set_axis_off()
for _, r in out.head(5).iterrows():
    ax[3].annotate(r.barri, r.geometry.representative_point().coords[0], fontsize=7, ha="center")
fig.suptitle("Barcelona: where pluvial flood hazard, heat vulnerability and plane-tree replacement overlap", fontsize=12)
(ROOT / "notes/figures").mkdir(parents=True, exist_ok=True)
fig.savefig(ROOT / "notes/figures/bcn_site_screening.png", dpi=150, bbox_inches="tight")
