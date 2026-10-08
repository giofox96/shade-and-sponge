"""Heat proxy: fast, for the optimiser and the web app. Must be calibrated against Ladybug UTCI (methodology §5–6).
Metric: effective shade on sunlit open ground over the design hours (m²·h). Each crown (an ellipsoid) casts an elliptical
shadow, shifted away from the sun. Its opacity is 1 − τ in leaf, with τ = exp(−0.5·LAI) (Beer–Lambert, k = 0.5 as in
Peng et al. 2026; methodology §3), and OP_BARE when leafless. The shadow counts only where buildings leave pedestrians
(1.1 m) in the sun. Overlapping shadows take the max.
Summer: shade is a benefit (heat stress). Winter: the same metric is a cost (sun access for cold-season comfort)."""
import numpy as np
from rasterio.features import rasterize
from shapely.geometry import Point
from shapely import affinity
from . import season

SEASONS = dict(
    summer=dict(doy=196, month=7, hours_utc=range(10, 16)),   # ASSUMPTION 15 July, 12–17 h CEST (methodology §1), until the EPW hottest week
    winter=dict(doy=15, month=1, hours_utc=range(9, 15)),     # ASSUMPTION 15 January, 10–15 h CET, until the EPW coldest week
)
DESIGN_MONTH = SEASONS["summer"]["month"]
K = 0.5
Z_PED = 1.1           # pedestrian height of the UTCI test points (methodology §5)
OP_BARE = 0.35        # ASSUMPTION: irradiance reduction by a leafless deciduous crown. Mean of measured crowns ~35%, typical
                      # range 25–50% (McPherson 1984); leafless London plane up to ~54% in the shadow centre (Heisler 1982,
                      # 1984); both as cited in Thayer & Maeda 1985, J. Arboric. 11(1):1–12. Test 0.25–0.54


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


def design_suns(site, season_="summer"):
    s = SEASONS[season_]
    return [sun(site.lat, site.lon, s["doy"], h) for h in s["hours_utc"]]


def sunlit(site, alt, az):
    """Cells where a pedestrian (1.1 m) sees the sun past the buildings: march towards the sun over the building DSM."""
    dsm, z0 = site.dtm + site.bldg_h, site.dtm + Z_PED
    H, W = dsm.shape
    lit, last = np.ones((H, W), bool), None
    for d in np.arange(site.res, max(150.0, float(site.bldg_h.max()) / np.tan(alt)), site.res / 2):
        dr, dc = int(round(-d * np.cos(az) / site.res)), int(round(d * np.sin(az) / site.res))
        if (dr, dc) == last:
            continue
        last = (dr, dc)
        s = np.full((H, W), -np.inf, "float32")       # s[r, c] = dsm[r + dr, c + dc]
        s[max(0, -dr):H - max(0, dr), max(0, -dc):W - max(0, dc)] = dsm[max(0, dr):H + min(0, dr), max(0, dc):W + min(0, dc)]
        lit &= ~(s > z0 + d * np.tan(alt))
    return lit


def opacity(species, lai, month):
    """Crown opacity: leaf fraction f(month) × (1 − exp(−K·LAI)) + (1 − f) × OP_BARE."""
    f = (season.factor(species, month, r_off=0.0))            # plain leaf fraction (species without calendar: 1)
    return f * (1 - np.exp(-K * np.asarray(lai))) + (1 - f) * OP_BARE


def shadow(x, y, diam, height, base, alt, az):
    """Ground shadow (at 1.1 m) of an ellipsoid crown: across-sun semi-axis a, along-sun (a²sin²α + b²cos²α)^½ / sinα,
    centre shifted away from the sun by (crown-centre height − 1.1 m) / tanα."""
    a, b = diam / 2, max(height - base, 1.0) / 2
    zc = (height + base) / 2
    along = np.sqrt(a ** 2 * np.sin(alt) ** 2 + b ** 2 * np.cos(alt) ** 2) / np.sin(alt)
    off = max(zc - Z_PED, 0) / np.tan(alt)
    e = affinity.rotate(affinity.scale(Point(0, 0).buffer(1.0), a, along), -np.degrees(az), origin=(0, 0))
    return affinity.translate(e, x - off * np.sin(az), y - off * np.cos(az))


def shadow_xy_area(diam, height, base, alt, az):
    """Shadow centre offset (dx, dy) and shadow area for the per-position potentials."""
    a, b = diam / 2, np.maximum(height - base, 1.0) / 2
    along = np.sqrt(a ** 2 * np.sin(alt) ** 2 + b ** 2 * np.cos(alt) ** 2) / np.sin(alt)
    off = np.maximum((height + base) / 2 - Z_PED, 0) / np.tan(alt)
    return -off * np.sin(az), -off * np.cos(az), np.pi * a * along


def shade_m2h(site, trees, suns, lits, month):
    """Effective shade (m²·h) of a layout. trees: x, y, sp, crown_diam_m, height_m, crown_base_m, lai."""
    t = trees[(trees.crown_diam_m > 0) & (trees.lai > 0)]
    op = opacity(t.sp, t.lai.values, month)
    target = site.domain & ~site.roof
    tot = 0.0
    for (alt, az), lit in zip(suns, lits):
        shapes = sorted(((shadow(x, y, d, h, hb, alt, az), o) for x, y, d, h, hb, o in
                         zip(t.x.values, t.y.values, t.crown_diam_m.values, t.height_m.values, t.crown_base_m.values, op)),
                        key=lambda s: s[1])
        O = rasterize(shapes, out_shape=site.domain.shape, transform=site.transform, fill=0, dtype="float32")
        tot += float(O[lit & target].sum()) * site.res ** 2
    return tot
