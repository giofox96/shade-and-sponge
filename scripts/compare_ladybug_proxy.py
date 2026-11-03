"""Shade proxy vs Ladybug UTCI on Pg Andreu Nin (Tier 1 test, 2 Nov 2026; exchange/README.md).
Re-computes the proxy's shade (shade_sponge.heat: ellipsoid crown shadow, opacity 1 - exp(-0.5 LAI)) at the same 1,974 test
points and hours as the Ladybug run, for S0 (today) and S4 (tool layout), twice: with the proxy's LAI opacity and with opaque
crowns, as Ladybug modelled them. A point counts as shaded by a crown only where the buildings leave it in the sun.
Input: exchange/to_gh/street_andreu-nin_* (geometry the Ladybug loader read), exchange/from_gh/utci_*_mesh_20261102.csv (Grasshopper rerun with mesh crowns).
Output: databases/barcelona/ladybug_vs_proxy_andreu_nin.csv (one row per point) and a printed summary.
Run: python scripts/compare_ladybug_proxy.py"""
import json, pathlib, sys
import numpy as np, pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point, shape
from shapely.strtree import STRtree

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge import heat  # noqa: E402

TG, FG = ROOT / "exchange/to_gh", ROOT / "exchange/from_gh"
SC = {"S0": "S0_current", "S4": "S4_s1.00_w0.00_r0.00"}
O = json.load(open(ROOT / "exchange/to_gh/site_origin.json")) if (TG / "site_origin.json").exists() else dict(origin_x=430800, origin_y=4586800)

pts = pd.read_csv(TG / "street_andreu-nin_testpoints_20261031.csv")
bl = json.load(open(TG / "street_andreu-nin_buildings_20261031.geojson"))["features"]
bgeo = [shape(f["geometry"]) for f in bl]
btop = np.array([f["properties"]["ground_z"] + f["properties"]["height_m"] for f in bl])
btree = STRtree(bgeo)
ctx = pd.read_csv(TG / "street_andreu-nin_context_trees_20261031.csv")
ctx = ctx[ctx.flag == "ok"].rename(columns={"lai_proxy": "lai"})
lon, lat = Transformer.from_crs(25831, 4326, always_xy=True).transform(O["origin_x"] + pts.x.mean(), O["origin_y"] + pts.y.mean())
suns = [heat.sun(lat, lon, heat.SEASONS["summer"]["doy"], h) for h in heat.SEASONS["summer"]["hours_utc"]]  # 10-15 UTC = EPW 11-16


def sunlit(p, z, alt, az):
    """True if the sun ray from a point at height z clears every building."""
    L = (btop.max() - z) / np.tan(alt) + 1
    ray = LineString([(p.x, p.y), (p.x + L * np.sin(az), p.y + L * np.cos(az))])
    for i in btree.query(ray):
        g = bgeo[i]
        if g.contains(p):
            return False
        hit = ray.intersection(g)
        if not hit.is_empty and btop[i] > z + p.distance(hit) * np.tan(alt):
            return False
    return True


def shade(trees, opaque):
    """Per point, the proxy's effective shade summed over the 6 hours (hours of full shade)."""
    op = np.ones(len(trees)) if opaque else heat.opacity(trees.species, trees.lai.values, 7)
    out = np.zeros(len(pts))
    for alt, az in suns:
        sh = [heat.shadow(x, y, d, h, b, alt, az) for x, y, d, h, b in
              zip(trees.x, trees.y, trees.crown_diam_m, trees.height_m, trees.crown_base_m)]
        st = STRtree(sh)
        for k, (p, lit) in enumerate(zip(P, LIT[(alt, az)])):
            if lit:
                ids = [i for i in st.query(p) if sh[i].contains(p)]
                out[k] += max((op[i] for i in ids), default=0.0)
    return out


P = [Point(x, y) for x, y in zip(pts.x, pts.y)]
LIT = {s: [sunlit(p, z, *s) for p, z in zip(P, pts.z)] for s in suns}
res = pts[["point_id", "x", "y"]].copy()
res["sunlit_h"] = np.sum([LIT[s] for s in suns], 0)
for k, s in SC.items():
    u = pd.read_csv(FG / f"utci_{s}_mesh_20261102.csv").groupby("point_id").utci_C.mean()
    res[f"utci_{k}"] = res.point_id.map(u)
    tr = pd.concat([pd.read_csv(TG / f"street_andreu-nin_trees_{s}_20261031.csv"), ctx], ignore_index=True)
    res[f"shade_lai_{k}"] = shade(tr, False)
    res[f"shade_opaque_{k}"] = shade(tr, True)
res["d_utci"] = res.utci_S4 - res.utci_S0
for m in ("lai", "opaque"):
    res[f"d_shade_{m}"] = res[f"shade_{m}_S4"] - res[f"shade_{m}_S0"]
res.round(3).to_csv(ROOT / "databases/barcelona/ladybug_vs_proxy_andreu_nin.csv", index=False)

print(f"sun at lat {lat:.3f} lon {lon:.3f}; alt {[round(np.degrees(a)) for a, _ in suns]}")
print(f"points sunlit (by buildings) on average {res.sunlit_h.mean():.2f} of 6 h")
print(f"Ladybug mean UTCI  S0 {res.utci_S0.mean():.2f}  S4 {res.utci_S4.mean():.2f}  diff {res.d_utci.mean():+.2f} C")
for m in ("lai", "opaque"):
    a, b = res[f"shade_{m}_S0"].sum(), res[f"shade_{m}_S4"].sum()
    r = np.corrcoef(res[f"d_shade_{m}"], res.d_utci)[0, 1]
    print(f"proxy {m:6s}: S4/S0 shade {100 * b / a:.1f}%   corr(d_shade, d_utci) {r:+.2f}")
r0 = np.corrcoef(res.shade_lai_S0, res.utci_S0)[0, 1]
print(f"S0 across points: corr(proxy shade, UTCI) {r0:+.2f} (expected negative)")
