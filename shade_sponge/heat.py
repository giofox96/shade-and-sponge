"""Heat proxy: fast, for the optimiser and the web app. Must be calibrated against Ladybug UTCI (methodology §5–6).
Metric: effective shade on sunlit open ground over the design hours (m²·h). Each crown casts a disk shadow of opacity
1 − τ, with τ = exp(−0.5·LAI) (Beer–Lambert, k = 0.5 as in Peng et al. 2026; methodology §3), shifted away from the sun.
The shadow counts only where buildings leave pedestrians (1.1 m) in the sun. Overlapping shadows take the max."""
import numpy as np
from rasterio.features import rasterize
from shapely.geometry import Point

DESIGN_DOY = 196                     # ASSUMPTION: 15 July, until the hottest week is taken from the EPW (methodology §1)
DESIGN_HOURS_UTC = range(10, 16)     # 12–17 h local summer time (CEST = UTC+2), methodology §1
K = 0.5
Z_PED = 1.1                          # pedestrian height of the UTCI test points (methodology §5)


def sun(lat, lon, doy, hour_utc):
    """Solar altitude and azimuth (rad, azimuth clockwise from north), NOAA general solar position equations."""
    g = 2 * np.pi / 365 * (doy - 1 + (hour_utc - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g)
                    - 0.040849 * np.sin(2 * g))
    dec = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g) + 0.000907 * np.sin(2 * g)
           - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    ha = np.radians((hour_utc * 60 + eqt + 4 * lon) / 4 - 180)
    la = np.radians(lat)
    alt = np.arcsin(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(ha))
    az = np.arctan2(np.sin(ha), np.cos(ha) * np.sin(la) - np.tan(dec) * np.cos(la)) + np.pi
    return float(alt), float(az)


def design_suns(site):
    return [sun(site.lat, site.lon, DESIGN_DOY, h) for h in DESIGN_HOURS_UTC]


def sunlit(site, alt, az, dmax=150.0):
    """Cells where a pedestrian (1.1 m) sees the sun past the buildings: march towards the sun over the building DSM."""
    dsm, z0 = site.dtm + site.bldg_h, site.dtm + Z_PED
    H, W = dsm.shape
    lit, last = np.ones((H, W), bool), None
    for d in np.arange(site.res, dmax, site.res / 2):
        dr, dc = int(round(-d * np.cos(az) / site.res)), int(round(d * np.sin(az) / site.res))
        if (dr, dc) == last:
            continue
        last = (dr, dc)
        s = np.full((H, W), -np.inf, "float32")       # s[r, c] = dsm[r + dr, c + dc]
        s[max(0, -dr):H - max(0, dr), max(0, -dc):W - max(0, dc)] = dsm[max(0, dr):H + min(0, dr), max(0, dc):W + min(0, dc)]
        lit &= ~(s > z0 + d * np.tan(alt))
    return lit


def shadow_xy(x, y, zc, alt, az):
    """Centre of the ground shadow of a crown centred at height zc."""
    off = np.maximum(zc - Z_PED, 0) / np.tan(alt)
    return x - off * np.sin(az), y - off * np.cos(az)


def shade_m2h(site, trees, suns, lits):
    """Effective shade (m²·h) of a layout. trees: x, y, crown_diam_m, height_m, crown_base_m, lai."""
    t = trees[(trees.crown_diam_m > 0) & (trees.lai > 0)]
    op, zc = 1 - np.exp(-K * t.lai.values), (t.height_m.values + t.crown_base_m.values) / 2
    target = site.domain & ~site.roof
    tot = 0.0
    for (alt, az), lit in zip(suns, lits):
        xs, ys = shadow_xy(t.x.values, t.y.values, zc, alt, az)
        shapes = sorted(((Point(x, y).buffer(d / 2), o) for x, y, d, o in zip(xs, ys, t.crown_diam_m.values, op)),
                        key=lambda s: s[1])
        O = rasterize(shapes, out_shape=site.domain.shape, transform=site.transform, fill=0, dtype="float32")
        tot += float(O[lit & target].sum()) * site.res ** 2
    return tot
