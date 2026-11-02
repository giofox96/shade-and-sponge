"""Ladybug Tier 1 UTCI with porous crowns, in Python (methodology §5, §5b; route 1, 2 Nov 2026).
Re-implements the Grasshopper chain the user ran on Pg Andreu Nin (LB Human to Sky Relation -> LB Outdoor Solar MRT ->
LB UTCI Comfort, ladybug_grasshopper 1.10 sources) with the same inputs, but the ray tests are done here so that a crown can
pass part of the light: transmittance tau = exp(-0.5 LAI) per crown crossed (Peng et al. 2026; heat.K), buildings opaque.
Like the component: one human point per position, 0.918 m above the test point (midpoint of a 1.8 m line starting 1.8 cm up);
fract_body_exp = transmission towards the sun at each hour; sky_exposure = weighted transmission over the 145 Tregenza patches.
ASSUMPTION: the same tau for direct sun and for the sky view (diffuse and longwave).
Mode "opaque" (tau = 0) must reproduce the Grasshopper run (exchange/from_gh/utci_*_20261102.csv) before "lai" is trusted.
Input: exchange/to_gh/street_andreu-nin_* (geometry), the EPW the user ran (not in the repo: licence unconfirmed).
Output: databases/barcelona/porous_utci_andreu_nin.csv (per point: UTCI 12-17 h mean, S0/S4, opaque/lai), printed summary.
Run: python scripts/porous_utci.py <path to ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.epw>   (needs pip ladybug-comfort)"""
import json, pathlib, sys
import numpy as np, pandas as pd
from shapely.geometry import shape, LineString, Point
from shapely.strtree import STRtree
from ladybug.epw import EPW
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.sunpath import Sunpath
from ladybug.viewsphere import view_sphere
from ladybug.datacollection import HourlyDiscontinuousCollection
from ladybug.header import Header
from ladybug.datatype.fraction import Fraction
from ladybug_comfort.collection.solarcal import OutdoorSolarCal
from ladybug_comfort.collection.utci import UTCI

ROOT = pathlib.Path(__file__).resolve().parents[1]
TG = ROOT / (sys.argv[2] if len(sys.argv) > 2 else "exchange/to_gh")             # optional: another set with the same file names
FG = TG / "from_gh" if len(sys.argv) > 2 else ROOT / "exchange/from_gh"
OUT = sys.argv[3] if len(sys.argv) > 3 else "porous_utci_andreu_nin.csv"
SC = {"S0": "S0_current", "S4": "S4_s1.00_w0.00_r0.00"}
K, H_UP, GROUND_REF = 0.5, 0.018 + 0.9, 0.25      # Beer-Lambert k (heat.K); LB human point; ground reflectance used in the GH run
PERIOD = AnalysisPeriod(7, 15, 11, 7, 15, 16)    # EPW standard time 11-16 = 12-17 h CEST

pts = pd.read_csv(TG / "street_andreu-nin_testpoints_20261031.csv")
P = np.c_[pts.x, pts.y, pts.z + H_UP]
bl = json.load(open(TG / "street_andreu-nin_buildings_20261031.geojson"))["features"]
bgeo = [shape(f["geometry"]) for f in bl]
btop = np.array([f["properties"]["ground_z"] + f["properties"]["height_m"] for f in bl])
bbot = np.array([f["properties"]["ground_z"] for f in bl])
btree = STRtree(bgeo)
ctx = pd.read_csv(TG / "street_andreu-nin_context_trees_20261031.csv").rename(columns={"lai_proxy": "lai"})  # all, as the loader


def building_free(dirs):
    """(n_pts, n_dirs) bool: the ray from each point clears every building (prisms, as the loader extrudes them)."""
    out = np.ones((len(P), len(dirs)), bool)
    for j, d in enumerate(dirs):
        h = np.hypot(d[0], d[1])
        if h < 1e-9:                                          # zenith patch: blocked only under a roof
            for k, p in enumerate(P):
                out[k, j] = not any(bgeo[i].contains(Point(p[0], p[1])) and btop[i] > p[2] for i in btree.query(Point(p[0], p[1])))
            continue
        tan = d[2] / h
        L = max((btop.max() - P[:, 2].min()) / tan, 1) + 1
        u = d[:2] / h
        for k, p in enumerate(P):
            ray = LineString([(p[0], p[1]), (p[0] + L * u[0], p[1] + L * u[1])])
            for i in btree.query(ray):
                g = bgeo[i]
                if g.contains(Point(p[0], p[1])):
                    if bbot[i] <= p[2] <= btop[i]:
                        out[k, j] = False
                        break
                    continue
                hit = ray.intersection(g)
                if not hit.is_empty and p[2] + Point(p[0], p[1]).distance(hit) * tan < btop[i]:
                    out[k, j] = False
                    break
    return out


def crown_trans(trees, dirs, opaque):
    """(n_pts, n_dirs) transmission through the crowns (ellipsoids, as the loader builds them): product of tau per crown hit."""
    trees = trees[trees.crown_diam_m > 0]                     # no crown (their NaN rays counted as misses anyway)
    a = trees.crown_diam_m.values / 2
    b = np.maximum(trees.height_m.values - trees.crown_base_m.values, 1.0) / 2
    c = np.c_[trees.x, trees.y, trees.ground_z + (trees.height_m + trees.crown_base_m) / 2]
    s = np.c_[a, a, b]
    tau = np.zeros(len(trees)) if opaque else np.exp(-K * trees.lai.values)
    T = np.ones((len(P), len(dirs)))
    for lo in range(0, len(P), 400):                          # chunks of points: memory
        T[lo:lo + 400] = _trans(P[lo:lo + 400], c, s, tau, dirs)
    return T


def _trans(P, c, s, tau, dirs):
    T = np.ones((len(P), len(dirs)))
    for j, d in enumerate(dirs):
        o = (P[:, None, :] - c[None]) / s[None]               # (n_pts, n_trees, 3) in unit-sphere space
        v = d[None, None, :] / s[None]
        A = (v ** 2).sum(-1)
        B = 2 * (o * v).sum(-1)
        C = (o ** 2).sum(-1) - 1
        disc = B ** 2 - 4 * A * C
        hit = (disc > 0) & ((-B + np.sqrt(np.maximum(disc, 0))) > 0)   # far root ahead of the point
        T[:, j] = np.where(hit, tau[None], 1.0).prod(1)
    return T


epw = EPW(sys.argv[1])
sp = Sunpath.from_location(epw.location)
hoys = PERIOD.hoys
sun = np.array([tuple(sp.calculate_sun_from_hoy(h).sun_vector_reversed) for h in hoys])
sky = np.array([tuple(v) for v in view_sphere.tregenza_dome_vectors])
w = np.array(view_sphere.dome_patch_weights(1)) / 145
print("buildings: sun rays", flush=True)
B_sun = building_free(sun)
print("buildings: sky rays", flush=True)
B_sky = building_free(sky)
wx = {k: getattr(epw, k).filter_by_analysis_period(PERIOD) for k in
      ("dry_bulb_temperature", "relative_humidity", "wind_speed", "direct_normal_radiation",
       "diffuse_horizontal_radiation", "horizontal_infrared_radiation_intensity")}

DT = wx["dry_bulb_temperature"].datetimes
res = pts[["point_id"]].copy()
for k, s in SC.items():
    tr = pd.concat([pd.read_csv(TG / f"street_andreu-nin_trees_{s}_20261031.csv"), ctx], ignore_index=True)
    f = next(iter(sorted(FG.glob(f"utci_{s}_*.csv"), reverse=True)), None) \
        or next(iter(FG.glob(f"utci_{k}.csv")), None)        # "_mesh_" sorts after the date: the corrected rerun first
    if f:                                                     # the Grasshopper run, when there is one
        res[f"utci_gh_{k}"] = res.point_id.map(pd.read_csv(f).groupby("point_id").utci_C.mean())
    for mode in ("opaque", "lai"):
        fb = B_sun * crown_trans(tr, sun, mode == "opaque")
        se = (B_sky * crown_trans(tr, sky, mode == "opaque")) @ w
        u = []
        for i in range(len(P)):
            f = HourlyDiscontinuousCollection(Header(Fraction(), "fraction", PERIOD), list(fb[i]), DT)
            mrt = OutdoorSolarCal(epw.location, wx["direct_normal_radiation"], wx["diffuse_horizontal_radiation"],
                                  wx["horizontal_infrared_radiation_intensity"], wx["dry_bulb_temperature"], f, float(se[i]),
                                  GROUND_REF).mean_radiant_temperature
            u.append(np.mean(UTCI(wx["dry_bulb_temperature"], wx["relative_humidity"], mrt, wx["wind_speed"])
                             .universal_thermal_climate_index.values))
        res[f"utci_{mode}_{k}"] = u
        res[f"sky_exp_{mode}_{k}"] = se
        print(f"{k} {mode}: mean UTCI {np.mean(u):.2f} C, sky exposure {se.mean():.3f}", flush=True)
res.round(3).to_csv(ROOT / "databases/barcelona" / OUT, index=False)

for k in SC if "utci_gh_S0" in res else []:
    e = res[f"utci_opaque_{k}"] - res[f"utci_gh_{k}"]
    print(f"check {k}: opaque here vs Grasshopper, mean diff {e.mean():+.2f} C, MAE {e.abs().mean():.2f}, "
          f"r {np.corrcoef(res[f'utci_opaque_{k}'], res[f'utci_gh_{k}'])[0, 1]:.3f}")
for m in [x for x in ("gh", "opaque", "lai") if f"utci_{x}_S0" in res]:
    d = res[f"utci_{m}_S4"] - res[f"utci_{m}_S0"]
    print(f"{m:6s}: S0 {res[f'utci_{m}_S0'].mean():.2f}  S4 {res[f'utci_{m}_S4'].mean():.2f}  S4-S0 {d.mean():+.2f} C "
          f"(median {d.median():+.2f}; S4 warmer at {100 * (d > 0.05).mean():.0f}% of points)")
