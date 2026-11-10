"""Infrared City UTCI on Pg Andreu Nin, S0 (current trees): third engine next to the shade proxy and Ladybug.

Same geometry as the Ladybug Tier 1 test (exchange/to_gh/street_andreu-nin_*_20261031.*).
Default = free cost preview only. `--run` bills tokens and writes databases/barcelona/infrared_utci_andreu_nin.csv.
API reference: infrared-skills plugin 1.0.3 (python/own-data.md, weather-and-time.md, geospatial-crs.md).
"""
import json
import math
import os
import sys
import winreg
from pathlib import Path

import numpy as np
import pandas as pd
import shapely
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from infrared_sdk import InfraredClient, parse_epw
from infrared_sdk.analyses.types import AnalysesName, UtciModelBaseRequest, UtciModelRequest
from infrared_sdk.models import Location, TimePeriod

ROOT = Path(__file__).resolve().parents[1]
TG = ROOT / "exchange" / "to_gh"
OX, OY = 430800.0, 4586800.0  # local origin in EPSG:25831 (exchange/README.md rule 1)
R = 6_371_000.0  # sphere of the SDK run frame (geospatial-crs.md)
to_wgs = Transformer.from_crs(25831, 4326, always_xy=True)


def lonlat(x, y):
    return to_wgs.transform(x + OX, y + OY)


pts = pd.read_csv(TG / "street_andreu-nin_testpoints_20261031.csv")
# Run polygon = bbox of the Ladybug test points + 2 m, as lon/lat.
x0, y0, x1, y1 = pts.x.min() - 2, pts.y.min() - 2, pts.x.max() + 2, pts.y.max() + 2
ring = [lonlat(x, y) for x, y in [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]]
polygon = {"type": "Polygon", "coordinates": [[list(p) for p in ring]]}
lon0, lat0 = min(p[0] for p in ring), min(p[1] for p in ring)


def run_xy(x, y):  # local metres -> SDK run frame (origin = SW corner of the polygon bbox)
    lon, lat = lonlat(x, y)
    return math.radians(lon - lon0) * R * math.cos(math.radians(lat0)), math.radians(lat - lat0) * R


def extrude(coords, height):  # closed solid, from own-data.md
    poly = orient(Polygon([run_xy(*p) for p in coords[:-1]]), 1.0)
    rg = list(poly.exterior.coords)[:-1]
    slot = {p: i for i, p in enumerate(rg)}
    n = len(rg)
    xyz = [c for z in (0.0, height) for x, y in rg for c in (x, y, z)]
    idx = []
    for tri in shapely.constrained_delaunay_triangles(poly).geoms:
        a, b, c = [slot[p] for p in list(tri.exterior.coords)[:3]]
        (xa, ya), (xb, yb), (xc, yc) = rg[a], rg[b], rg[c]
        if (xb - xa) * (yc - ya) - (xc - xa) * (yb - ya) < 0:
            b, c = c, b
        idx += [n + a, n + b, n + c, a, c, b]
    for i in range(n):
        j = (i + 1) % n
        idx += [i, j, n + j, i, n + j, n + i]
    return {"coordinates": xyz, "indices": idx}


feats = json.load(open(TG / "street_andreu-nin_buildings_20261031.geojson"))["features"]
buildings = {f"b{i}": extrude(f["geometry"]["coordinates"][0], f["properties"]["height_m"]) for i, f in enumerate(feats)}

tr = pd.concat([pd.read_csv(TG / "street_andreu-nin_trees_S0_current_20261031.csv"),
                pd.read_csv(TG / "street_andreu-nin_context_trees_20261031.csv")], ignore_index=True)
# shortcut: genus + height + crown diameter only; LAI / gap fraction not passed (model default canopy), revisit before comparing engines
trees = {str(t.tree_id): {"type": "Feature", "geometry": {"type": "Point", "coordinates": list(lonlat(t.x, t.y))},
                          "properties": {"genus": t.species.split()[0].lower(), "height": float(t.height_m),
                                         "crownDiameter": float(t.crown_diam_m)}} for t in tr.itertuples()}

# Key from the Windows user variables when the session predates `setx`; never printed.
key = os.environ.get("INFRARED_API_KEY") or winreg.QueryValueEx(
    winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "INFRARED_API_KEY")[0]
client = InfraredClient(api_key=key)

lon_c, lat_c = lonlat((x0 + x1) / 2, (y0 + y1) / 2)
# Infrared hour h = EPW record h+1 (interval start); Ladybug hour h = record h. start 10 / end 15 selects the same
# six EPW records 11-16 as Ladybug 11-16 (= 12-17 h CEST); checked on 15 July, TMYx 2011-2025.
window = TimePeriod(start_month=7, start_day=15, start_hour=10, end_month=7, end_day=15, end_hour=15)
# EPW: default = the plain TMYx (1973-2023) the Grasshopper Ladybug run used (hb_utci_andreu_nin_sameepw.csv);
# `--epw2011` = TMYx 2011-2025, the hotter file of the first Honeybee run (hb_utci_andreu_nin.csv).
LB = ROOT / "grasshopper/ladybug_andreu_nin_20261102/ladybug"
TAG = "_epw2011" if "--epw2011" in sys.argv else ""
EPW = (LB / "ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2011-2025/ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2011-2025.epw" if TAG
       else LB / "ladybug_porta/dati/ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.epw")
rows = parse_epw(str(EPW))
print(f"weather: {EPW.name}; {len(buildings)} buildings, {len(trees)} trees")

request = UtciModelRequest.from_weatherfile_payload(
    payload=UtciModelBaseRequest(analysis_type=AnalysesName.thermal_comfort_index),
    location=Location(latitude=lat_c, longitude=lon_c), time_period=window, weather_data=rows)
layers = dict(buildings=buildings, vegetation=trees)
p = client.preview_area(polygon, payload=request, **layers)
print(f"area {x1 - x0:.0f} x {y1 - y0:.0f} m: tiles {p.tile_count}, jobs {p.would_bill_jobs}, cost {p.estimated_cost_tokens} tokens")

if "--run" in sys.argv:
    grid = client.run_area_and_wait(request, polygon, **layers).physical_grid()  # row 0 = south, 1 m cells from the SW corner
    ij = [tuple(int(round(v)) for v in run_xy(x, y)) for x, y in zip(pts.x, pts.y)]
    pts["utci_infrared"] = [grid[j, i] if 0 <= j < grid.shape[0] and 0 <= i < grid.shape[1] else np.nan for i, j in ij]
    pts.to_csv(ROOT / "databases" / "barcelona" / f"infrared_utci_andreu_nin{TAG}.csv", index=False)
    print(f"grid {grid.shape}, mean UTCI at the {pts.utci_infrared.notna().sum()} test points: {pts.utci_infrared.mean():.2f} C")
