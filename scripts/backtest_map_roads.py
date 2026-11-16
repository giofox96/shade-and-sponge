"""Kerb lines (road lines of the city's 1:1000 map) around each back-test group, for the deck's maps (make_backtest_deck.py).

Source: Ajuntament de Barcelona, Mapa base topogràfic 1:1000, WMS layer "Línies_comunicacions" (CC BY 4.0), fetched and
parsed with scripts/porta_sidewalk_width.py (cached SVG tiles). Lines >= MIN_KERB, clipped to the group's positions + PAD_M.
Run on the PC (the WMS blocks the cloud): python scripts/backtest_map_roads.py -> databases/barcelona/backtest_map_roads.geojson
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import porta_sidewalk_width as sw  # noqa: E402

PAD_M = 80.0                       # wider than the deck's map box (positions + 30 m, squared)
DB = ROOT / "databases/barcelona"

p = pd.read_csv(DB / "backtest_works_guide_capsmall_positions.csv")
sw.SVG.mkdir(parents=True, exist_ok=True)
out = []
for g, q in p.groupby("group"):
    x0, y0, x1, y1 = q.x.min() - PAD_M, q.y.min() - PAD_M, q.x.max() + PAD_M, q.y.max() + PAD_M
    xs = np.arange(np.floor(x0 / sw.TILE) * sw.TILE, x1, sw.TILE)
    ys = np.arange(np.floor(y0 / sw.TILE) * sw.TILE, y1, sw.TILE)
    box = shapely.box(x0, y0, x1, y1)
    for ln in sw.lines("road", xs, ys):
        if ln.length >= sw.MIN_KERB and ln.intersects(box):
            out.append(dict(group=g, geometry=ln.intersection(box)))
    print(g, sum(o["group"] == g for o in out), "road lines")
gpd.GeoDataFrame(out, crs=25831).to_file(DB / "backtest_map_roads.geojson", driver="GeoJSON")
