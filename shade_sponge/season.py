"""Leaf-on calendar and storm season.
LAI in month m = LAI at the LiDAR flight (26 Sept 2021, full leaf) × (R_OFF + (1 − R_OFF) · f(m)), where f = leaf fraction
per species and month (databases/traits/phenology_palette.csv). Runoff objective = expected runoff of the design storm
over the months when intense storms occur (databases/barcelona/storm_months.csv, Esbrí et al. 2026, Fig. 4)."""
import pandas as pd
from .site import ROOT, DB
from . import runoff

R_OFF = 0.5   # ASSUMPTION: canopy storage of a leafless crown as a share of the full-leaf value (test 0.3–0.7). Anchors:
              # interception loss leafless/leafed = 20/29 % in a deciduous forest, an upper bound because the leafless
              # canopy stored less but evaporated faster (Herbst et al. 2008); deciduous pear 15% vs evergreen oak 27% of
              # winter rain (Xiao et al. 2000)
PHEN = pd.read_csv(ROOT / "databases/traits/phenology_palette.csv").set_index("species")
STORM = pd.read_csv(DB / "storm_months.csv", comment="#").set_index("month").share_pct / 100
STORM = STORM[STORM > 0]


def factor(species, month, r_off=R_OFF):
    """LAI multiplier per tree. Species without a calendar keep full leaf (ASSUMPTION; they are the same in every layout)."""
    f = pd.Series(list(species)).map(PHEN[f"m{month:02d}"]).fillna(1.0).values
    return r_off + (1 - r_off) * f


def storm_factor(species, r_off=R_OFF, storms=None):
    """Season-weighted LAI multiplier over the storm months (1 = full leaf in every storm)."""
    s = STORM if storms is None else storms
    return sum(w * factor(species, m, r_off) for m, w in s.items()) / s.sum()


def at_month(trees, month):
    t = trees.copy()
    t["lai"] = t.lai * factor(t.sp, month)
    return t


def runoff_seasonal(site, trees, p):
    """Expected runoff (m³) of a storm of depth p, weighted by the month in which intense storms occur."""
    out = {}
    for m, w in STORM.items():
        for k, v in runoff.event(site, at_month(trees, m), p).items():
            out[k] = out.get(k, 0.0) + w * v / STORM.sum()
    return out
