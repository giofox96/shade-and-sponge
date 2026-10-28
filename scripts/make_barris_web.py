"""Neighbourhood (barri) outlines for the web app's picker: web/public/data/barris.geojson (WGS84, simplified).
Source: the official boundaries (Open Data BCN, BarcelonaCiutat_Barris.csv, CC BY 4.0) when databases/barcelona/raw/ has
them; otherwise OSM admin_level 10 inside the municipality (raw/osm/admin.gpkg from scripts/osm_sidewalks.py, ODbL).
Properties: name, district, site (folder under web/public/data/ when the tool has been run there, else null), and the
plane and street-tree counts of the screening (databases/barcelona/site_screening_barris.csv).
Run from the repo root: python scripts/make_barris_web.py"""
import pathlib, re, unicodedata, shapely, pandas as pd, geopandas as gpd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "databases/barcelona/raw", ROOT / "web/public/data/barris.geojson"
SITES = {"Porta": "porta"}            # barris with exported tool data (python -m shade_sponge.web_export)
TOL = 8.0                             # m, simplification tolerance (display only)
key = lambda n: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower())

off = RAW / "BarcelonaCiutat_Barris.csv"
if off.exists():
    b = pd.read_csv(off)
    g = gpd.GeoDataFrame(dict(name=b.nom_barri), geometry=gpd.GeoSeries.from_wkt(b.geometria_etrs89), crs=25831)
    source = "Ajuntament de Barcelona, Open Data BCN (CC BY 4.0)"
else:
    a = gpd.read_file(RAW / "osm/admin.gpkg")
    city = a[(a.level == "8") & (a.name == "Barcelona")].union_all()
    g = a[(a.level == "10") & a.representative_point().within(city)][["name", "geometry"]]
    g["name"] = g.name.replace({"el Gòtic": "el Barri Gòtic", "Sant Andreu de Palomar": "Sant Andreu"})  # official names
    source = "OpenStreetMap contributors (ODbL), provisional"
s = pd.read_csv(ROOT / "databases/barcelona/site_screening_barris.csv")
s.index = s.barri.map(key)
g["k"] = g.name.map(key)
missing = sorted(set(s.index) - set(g.k))
print(f"{len(g)} barris from {source}; screening names not matched: {missing}")
g["district"] = g.k.map(s.nom_districte)
g["planes"] = g.k.map(s.plane_trees).astype("Int64")
g["street_trees"] = g.k.map(s.street_trees).astype("Int64")
g["site"] = g.name.map(SITES)
g["geometry"] = g.simplify(TOL)
g = g.drop(columns="k").sort_values(["district", "name"]).to_crs(4326)
g["geometry"] = shapely.set_precision(g.geometry.values, 1e-5)             # ~1 m, enough for a 200 px mini-map
OUT.write_text(g.to_json(drop_id=True, to_wgs84=True).replace('"type": "FeatureCollection"',
               f'"type": "FeatureCollection", "source": "{source}"', 1), encoding="utf-8")
print("wrote", OUT, f"{OUT.stat().st_size / 1024:.0f} KB")
