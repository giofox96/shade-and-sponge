"""Honeybee models for the Tier 2 UTCI check on Pg Andreu Nin (methodology §5, §5b): one HBJSON per scenario, for the
"utci-comfort-map" recipe (the "HB UTCI Comfort Map" component) with Radiance shortwave through porous crowns.
Geometry as the Grasshopper loader (exchange/gh_scripts/load_andreu_nin.py): buildings extruded from footprints, crowns as
ellipsoid meshes. Crowns get a Radiance glass modifier with transmittance sqrt(tau) per surface, tau = exp(-0.5 LAI)
(Peng et al. 2026; heat.K), so a ray through a whole crown (two surfaces) keeps tau (ASSUMPTION: thin-glass surfaces,
no scattering inside the crown). Buildings keep Honeybee's generic context modifier. Sensors: the test points at 1.1 m,
facing up. No Honeybee rooms, so the recipe takes buildings, crowns and ground at the EPW air temperature.
Output: exchange/to_gh/hb_andreu_nin_<S0|S4>_<porous|opaque>.hbjson
Run: python scripts/make_hb_model.py   (needs pip honeybee-radiance)"""
import json, math, pathlib
import pandas as pd
from ladybug_geometry.geometry3d import Point3D, Face3D, Mesh3D
from honeybee.model import Model
from honeybee.shade import Shade
from honeybee.shademesh import ShadeMesh
from honeybee_radiance.modifier.material import Glass
from honeybee_radiance.sensorgrid import SensorGrid

ROOT = pathlib.Path(__file__).resolve().parents[1]
TG = ROOT / "exchange/to_gh"
TAG, K, NU, NV = "20261031", 0.5, 16, 8                 # NU x NV facets per crown
SC = {"S0": "S0_current", "S4": "S4_s1.00_w0.00_r0.00"}


def ellipsoid(x, y, zc, a, b):
    """UV ellipsoid mesh, semi-axes a (horizontal) and b (vertical), quads with triangle caps."""
    verts = [Point3D(x, y, zc + b)]
    for i in range(1, NV):
        th = math.pi * i / NV
        for j in range(NU):
            ph = 2 * math.pi * j / NU
            verts.append(Point3D(x + a * math.sin(th) * math.cos(ph), y + a * math.sin(th) * math.sin(ph), zc + b * math.cos(th)))
    verts.append(Point3D(x, y, zc - b))
    ring = lambda i, j: 1 + (i - 1) * NU + j % NU
    faces = [(0, ring(1, j + 1), ring(1, j)) for j in range(NU)]
    faces += [(ring(i, j), ring(i, j + 1), ring(i + 1, j + 1), ring(i + 1, j)) for i in range(1, NV - 1) for j in range(NU)]
    last = len(verts) - 1
    faces += [(ring(NV - 1, j), ring(NV - 1, j + 1), last) for j in range(NU)]
    return Mesh3D(verts, faces)


def buildings():
    out = []
    for n, f in enumerate(json.load(open(TG / f"street_andreu-nin_buildings_{TAG}.geojson"))["features"]):
        g, p = f["geometry"], f["properties"]
        z0, z1 = p["ground_z"], p["ground_z"] + p["height_m"]
        for k, poly in enumerate([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            ring = poly[0][:-1] if poly[0][0] == poly[0][-1] else poly[0]
            out.append(Shade(f"bld_{n}_{k}_roof", Face3D([Point3D(x, y, z1) for x, y in ring])))
            for i in range(len(ring)):
                (xa, ya), (xb, yb) = ring[i], ring[(i + 1) % len(ring)]
                if math.hypot(xb - xa, yb - ya) > 0.01:
                    out.append(Shade(f"bld_{n}_{k}_w{i}", Face3D([Point3D(xa, ya, z0), Point3D(xb, yb, z0),
                                                                    Point3D(xb, yb, z1), Point3D(xa, ya, z1)])))
    return out


def crowns(trees, porous, prefix):
    out = []
    for i, r in enumerate(trees.itertuples()):
        if not (r.crown_diam_m > 0):
            continue
        m = ShadeMesh(f"{prefix}_{i}", ellipsoid(r.x, r.y, r.ground_z + (r.height_m + r.crown_base_m) / 2,
                                                 r.crown_diam_m / 2, max(r.height_m - r.crown_base_m, 1.0) / 2))
        if porous:
            t = round(math.sqrt(math.exp(-K * r.lai)), 3)
            m.properties.radiance.modifier = Glass.from_single_transmittance(f"crown_t{int(1000 * t)}", t)
        out.append(m)
    return out


pts = pd.read_csv(TG / f"street_andreu-nin_testpoints_{TAG}.csv")
grid = SensorGrid.from_planar_positions("andreu_nin", [(x, y, z) for x, y, z in zip(pts.x, pts.y, pts.z)], (0, 0, 1))
ctx = pd.read_csv(TG / f"street_andreu-nin_context_trees_{TAG}.csv").rename(columns={"lai_proxy": "lai"})
bld = buildings()
for k, s in SC.items():
    st = pd.read_csv(TG / f"street_andreu-nin_trees_{s}_{TAG}.csv")
    for porous in (True, False):
        name = f"hb_andreu_nin_{k}_{'porous' if porous else 'opaque'}"
        model = Model(name, orphaned_shades=bld, shade_meshes=crowns(ctx, porous, "ctx") + crowns(st, porous, "st"),
                      tolerance=0.01)
        model.properties.radiance.add_sensor_grid(grid.duplicate())
        model.to_hbjson(name, str(TG))
        print(name, len(bld), "building faces,", len(model.shade_meshes), "crowns,", len(pts), "sensors")
