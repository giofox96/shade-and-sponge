"""Tree canopy cover of Porta from the 2021 leaf-on LiDAR, against the plan's 30% target (plan 2017, target 1).

Input: databases/barcelona/raw/lidar/porta_chm_05m.tif (from scripts/bcn_lidar_porta.py; vegetation classes 3-5, 0.5 m)
       and the Porta polygon (BarcelonaCiutat_Barris.csv). Canopy = CHM > 2 m after a 1-cell opening, the same mask
       bcn_lidar_porta.py uses to segment crowns. Street-tree share: canopy cells within 9 m (crown-radius cap) of an
       inventory street tree. ASSUMPTION: CHM > 2 m counts tall shrubs as canopy.
Run from the repo root with the project env. Usage: python scripts/porta_canopy_cover.py [<main repo root>]
"""
import sys, pathlib, numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.features import geometry_mask
from scipy import ndimage

DATA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".") / "databases/barcelona"
with rasterio.open(DATA / "raw/lidar/porta_chm_05m.tif") as r:
    chm, T = r.read(1), r.transform
b = pd.read_csv(DATA / "raw/BarcelonaCiutat_Barris.csv")
site = gpd.GeoSeries.from_wkt(b.loc[b.nom_barri == "Porta", "geometria_etrs89"], crs=25831)
inside = geometry_mask(site, chm.shape, T, invert=True)
canopy = ndimage.binary_opening(chm > 2.0, iterations=1) & inside

a = pd.read_csv(DATA / "arbrat_viari.csv", usecols=["x_etrs89", "y_etrs89", "nom_barri", "tipus_element"])
a = a[(a.nom_barri.str.upper() == "PORTA") & (a.tipus_element == "ARBRE VIARI")]
near = geometry_mask(gpd.points_from_xy(a.x_etrs89, a.y_etrs89).buffer(9.0), chm.shape, T, invert=True)

area = inside.sum() * 0.25
cov, street = canopy.sum() / inside.sum(), (canopy & near).sum() / inside.sum()
assert 0 < street <= cov < 1
print(f"Porta {area / 1e4:.1f} ha: canopy cover {cov:.1%} (street-tree crowns {street:.1%}, other {cov - street:.1%}); "
      f"plan target 30% -> gap {max(0, 0.30 - cov):.1%} of the area, {max(0, 0.30 - cov) * area / 1e4:.1f} ha")
pd.DataFrame([{"area_ha": area / 1e4, "canopy_cover": cov, "street_tree_canopy": street,
               "other_canopy": cov - street, "target": 0.30}]).round(4).to_csv(
    pathlib.Path(__file__).resolve().parents[1] / "databases/barcelona/porta_canopy_cover.csv", index=False)
