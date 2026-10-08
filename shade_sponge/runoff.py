"""Runoff module v1 as a library: same model and parameters as scripts/runoff_model.py (methodology §4b).
Canopy storage bucket I = min(P, s·LAI) under each crown disk (not over roofs), then SCS-CN on the effective rain."""
import json, numpy as np, pandas as pd, rasterio
from rasterio.features import rasterize
from shapely.geometry import Point
from .site import DB

P_ = json.load(open(DB / "runoff_params.json"))   # written by scripts/runoff_model.py: s calibrated, CNs = ASSUMPTION


def design_storm(T=2, d=60):
    """Rain depth (mm) of the PDISBA design storm, return period T (yr), duration d (min)."""
    idf = pd.read_csv(DB / "pdisba_idf_city.csv").set_index(["T_years", "duration_min"])
    return float(idf.loc[(T, d), "design_intensity_mmh"] * d / 60)


def scs(p, cn):
    s = 25.4 * (1000.0 / cn - 10.0)
    ia = 0.2 * s
    return np.where(p > ia, (p - ia) ** 2 / (p - ia + s), 0.0)


def storage(site, trees):
    """trees: x, y (EPSG:25831), crown_diam_m, lai -> canopy storage S (mm) per cell (max where crowns overlap)."""
    shapes = [(Point(x, y).buffer(d / 2), P_["s_mm_per_lai"] * l)
              for x, y, d, l in zip(trees.x, trees.y, trees.crown_diam_m, trees.lai) if d > 0 and l > 0]
    shapes.sort(key=lambda t: t[1])                     # largest storage wins on overlap
    S = rasterize(shapes, out_shape=site.domain.shape, transform=site.transform, fill=0, dtype="float32",
                  merge_alg=rasterio.enums.MergeAlg.replace) if shapes else np.zeros(site.domain.shape, "float32")
    S[site.roof] = 0                                    # crowns over roofs do not change roof runoff (downpipes)
    bg = site.background & (S == 0)
    S[bg] = P_["s_mm_per_lai"] * P_["background_lai"]
    return S


def event(site, trees, p):
    """Event runoff (m³) over the site, the part generated on open ground that drains to high flood-hazard cells,
    and canopy interception (m³), for rain depth p (mm)."""
    S = storage(site, trees)
    q = scs(np.clip(p - S, 0, None), site.cn)
    m, a = site.domain, site.res ** 2 / 1000
    return dict(runoff_m3=float(q[m].sum() * a), runoff_hot_m3=float(q[m & site.to_hot & ~site.roof].sum() * a),
                interception_m3=float(np.minimum(S, p)[m].sum() * a))
