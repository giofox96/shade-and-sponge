"""Infrared City UTCI on three documented works of the back-test (scripts/backtest_works.py): the city's planting vs the
method's, same positions, same day and hours as the Andreu Nin runs (15 July, 12-17 h CEST, plain TMYx).

Areas: Av. Rio de Janeiro (Porta, group 6128), Gran Via (el Clot, 6687), C. Piquer (el Poble-sec, 4504).
Geometry from the repo only: buildings (1:1000 map, LiDAR heights), the barri's LiDAR street trees within CONTEXT_M, minus
the trees at the group's positions, plus the layout's trees. Layout trees take the crown and height of their species at
trunk class TERCERA (backtest_works.traits_lookup, city LiDAR pool), as in the back-test.
Metric: mean UTCI over the ground cells within NEAR_M of the positions and outside building footprints.
ASSUMPTION: run polygon = positions' bounding box + PAD_M; trees passed as genus + height + crown diameter (model default
canopy), as in scripts/infrared_utci_andreu_nin.py.

Default = free cost preview only. `--run` bills tokens and writes databases/barcelona/infrared_backtest.csv.
Run on the PC (INFRARED_API_KEY, infrared_sdk, the EPW of the Andreu Nin run): python scripts/infrared_backtest.py [--run]
"""
import json
import math
import os
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
import shapely.ops
from pyproj import Transformer
from shapely.geometry import Polygon, Point
from shapely.geometry.polygon import orient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from shade_sponge.site import DB, BARRIS, trees_porta, trees_barri, city_trees  # noqa: E402
from backtest_works import traits_lookup  # noqa: E402

GROUPS = {6128: "Av. Rio de Janeiro", 6687: "Gran Via", 4504: "C. Piquer"}
LAYOUTS = ("city", "method_bal")
PAD_M, CONTEXT_M, BLD_M, NEAR_M, R_MATCH = 10.0, 30.0, 60.0, 4.0, 2.0     # ASSUMPTION, see docstring
R = 6_371_000.0
to_wgs = Transformer.from_crs(25831, 4326, always_xy=True)
EPW = ROOT / "grasshopper/ladybug_andreu_nin_20261102/ladybug/ladybug_porta/dati/ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.epw"


def buildings_of(slug):
    if slug == "porta":
        o = json.load(open(ROOT / "exchange/site_origin.json"))
        b = gpd.read_file(ROOT / "exchange/to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
        return b.set_geometry(b.translate(o["origin_x"], o["origin_y"])).set_crs(25831)
    return gpd.read_file(BARRIS / slug / "buildings.geojson").to_crs(25831)


def scene(g, pos, slug, layout, get):
    x0, y0, x1, y1 = pos.x.min() - PAD_M, pos.y.min() - PAD_M, pos.x.max() + PAD_M, pos.y.max() + PAD_M
    box = shapely.box(x0, y0, x1, y1)
    t = trees_porta() if slug == "porta" else trees_barri(slug)
    t = t[(t.flag == "ok") & t.x.between(x0 - CONTEXT_M, x1 + CONTEXT_M) & t.y.between(y0 - CONTEXT_M, y1 + CONTEXT_M)]
    d = np.hypot(t.x.values[:, None] - pos.x.values[None], t.y.values[:, None] - pos.y.values[None]).min(axis=1)
    kept = t[d > R_MATCH][["x", "y", "sp", "height_m", "crown_diam_m"]]
    new = pd.DataFrame([dict(x=x, y=y, sp=s, height_m=get(s)[0]["height_m"], crown_diam_m=get(s)[0]["crown_diam_m"])
                        for x, y, s in zip(pos.x, pos.y, pos[f"sp_{layout}"])])
    b = buildings_of(slug)
    b = b[b.intersects(box.buffer(BLD_M))].explode(index_parts=False)
    return box, pd.concat([kept, new], ignore_index=True), b


def main():
    from infrared_sdk import InfraredClient, parse_epw
    from infrared_sdk.analyses.types import AnalysesName, UtciModelBaseRequest, UtciModelRequest
    from infrared_sdk.models import Location, TimePeriod
    key = os.environ.get("INFRARED_API_KEY")
    if not key:
        import winreg
        key = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "INFRARED_API_KEY")[0]
    client = InfraredClient(api_key=key)
    rows_epw = parse_epw(str(EPW))
    window = TimePeriod(start_month=7, start_day=15, start_hour=10, end_month=7, end_day=15, end_hour=15)  # see andreu_nin
    p = pd.read_csv(DB / "backtest_works_positions.csv")
    get = traits_lookup(pd.DataFrame(columns=["species"]), city_trees())
    out, total = [], 0
    for g, name in GROUPS.items():
        pos = p[p.group == g]
        slug = pos.barri.iloc[0]
        for lay in LAYOUTS:
            box, trees, bld = scene(g, pos, slug, lay, get)
            x0, y0, x1, y1 = box.bounds
            ring = [to_wgs.transform(x, y) for x, y in [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]]
            lon0, lat0 = ring[0]

            def run_xy(x, y):
                lon, lat = to_wgs.transform(x, y)
                return np.radians(np.subtract(lon, lon0)) * R * math.cos(math.radians(lat0)), np.radians(np.subtract(lat, lat0)) * R

            def extrude(poly, h):                           # closed solid (scripts/infrared_utci_andreu_nin.py)
                pl = orient(Polygon([run_xy(*c) for c in list(poly.exterior.coords)[:-1]]), 1.0)
                rg = list(pl.exterior.coords)[:-1]
                slot, n = {q: i for i, q in enumerate(rg)}, len(rg)
                xyz = [c for z in (0.0, h) for x, y in rg for c in (x, y, z)]
                idx = []
                for tri in shapely.constrained_delaunay_triangles(pl).geoms:
                    a, b_, c = [slot[q] for q in list(tri.exterior.coords)[:3]]
                    (xa, ya), (xb, yb), (xc, yc) = rg[a], rg[b_], rg[c]
                    if (xb - xa) * (yc - ya) - (xc - xa) * (yb - ya) < 0:
                        b_, c = c, b_
                    idx += [n + a, n + b_, n + c, a, c, b_]
                for i in range(n):
                    j = (i + 1) % n
                    idx += [i, j, n + j, i, n + j, n + i]
                return {"coordinates": xyz, "indices": idx}

            buildings = {f"b{i}": extrude(geom, float(h)) for i, (geom, h) in enumerate(zip(bld.geometry, bld.height_m))
                         if h and h > 0 and geom.is_valid}
            veg = {f"t{i}": {"type": "Feature", "geometry": {"type": "Point", "coordinates": list(to_wgs.transform(t.x, t.y))},
                             "properties": {"genus": t.sp.split()[0].lower(), "height": float(t.height_m),
                                            "crownDiameter": float(t.crown_diam_m)}} for i, t in enumerate(trees.itertuples())}
            polygon = {"type": "Polygon", "coordinates": [[list(q) for q in ring]]}
            lc = to_wgs.transform((x0 + x1) / 2, (y0 + y1) / 2)
            req = UtciModelRequest.from_weatherfile_payload(
                payload=UtciModelBaseRequest(analysis_type=AnalysesName.thermal_comfort_index),
                location=Location(latitude=lc[1], longitude=lc[0]), time_period=window, weather_data=rows_epw)
            pv = client.preview_area(polygon, payload=req, buildings=buildings, vegetation=veg)
            total += pv.estimated_cost_tokens
            print(f"{name} {lay}: {x1 - x0:.0f} x {y1 - y0:.0f} m, {len(buildings)} buildings, {len(veg)} trees, "
                  f"tiles {pv.tile_count}, cost {pv.estimated_cost_tokens} tokens")
            if "--run" not in sys.argv:
                continue
            grid = client.run_area_and_wait(req, polygon, buildings=buildings, vegetation=veg).physical_grid()
            near = shapely.union_all([Point(x, y).buffer(NEAR_M) for x, y in zip(pos.x, pos.y)]).difference(
                shapely.union_all(bld.geometry.values))
            near_run = shapely.ops.transform(lambda x, y, z=None: run_xy(x, y), near)     # 1 m cells, row 0 = south
            jj, ii = np.mgrid[0:grid.shape[0], 0:grid.shape[1]]
            inside = shapely.contains_xy(near_run, ii.ravel() + 0.5, jj.ravel() + 0.5).reshape(grid.shape)
            vals = grid[inside & np.isfinite(grid)]
            out.append(dict(group=g, area=name, layout=lay, n_cells=len(vals), utci_mean=float(np.mean(vals))))
            print(f"   mean UTCI near the positions: {out[-1]['utci_mean']:.2f} C over {len(vals)} cells")
    print(f"total preview cost: {total} tokens")
    if out:
        pd.DataFrame(out).round(3).to_csv(DB / "infrared_backtest.csv", index=False)


if __name__ == "__main__":
    main()
