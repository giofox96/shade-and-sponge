"""Spot classes for Porta's candidate planting spots (user decision, 18 Nov: notes/tutor_feedback_17nov.md §9d).
  blocked      traffic lights / signals, parking entrances: moving them means changing traffic or private property
  conditional  sign supports, crossings, lamps, bollards, bus stops: a street project can move them (field check)
  free         nothing, or only benches / fountains (no longer an obstacle)
A spot takes the strictest class among ALL the objects within clearance, not only the first rule that hit it
(`excluded_by` keeps the first rule only). Reasons come from two places:
  - the city's point objects (databases/barcelona/porta_street_objects.csv), re-tested here with the clearances and the
    lamp factor of scripts/porta_spot_exclusions_city.py;
  - the OSM rules of scripts/porta_spot_exclusions.py (crossings, signals, parking entrances, bus stops). Only their first
    hit is stored in `excluded_by` (they run first, in the order signals, crossings, parking entrances, bus stops). So a
    spot first hit by a crossing can still be near an OSM parking entrance that is not counted here (limit; the OSM cut
    raw/osm/porta.osm is only on the PC).
Writes `spot_class` and `reasons` (all hits, ';'-separated) into databases/barcelona/porta_planting_spots.csv.
Run from the repo root AFTER both exclusion scripts (they rewrite the CSV): python scripts/porta_spot_classes.py"""
import pathlib, sys, numpy as np, pandas as pd
from scipy.spatial import cKDTree

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPOTS, OBJ = ROOT / "databases/barcelona/porta_planting_spots.csv", ROOT / "databases/barcelona/porta_street_objects.csv"
LAMP = {"small": 3.0, "medium": 4.5, "large": 6.5}           # 2011 guide pp. 22-23, as porta_spot_exclusions_city.py
LAMP_K = 0.5                                                  # ASSUMPTION, user decision 11 Nov (same script)
CLEAR = {"traffic_light": 3.0, "sign_support": 3.0, "bollard": 1.0, "bench": 1.0, "fountain": 1.0}  # same script
OSM = {"traffic_signals", "crossing", "parking_entrance", "bus_stop"}
BLOCKED = {"traffic_light", "traffic_signals", "parking_entrance"}
CONDITIONAL = {"sign_support", "crossing", "lamp", "bollard", "bus_stop"}


def classify(reasons):
    r = set(reasons)
    return "blocked" if r & BLOCKED else "conditional" if r & CONDITIONAL else "free"


def main():
    s = pd.read_csv(SPOTS)
    ob = pd.read_csv(OBJ)
    xy = s[["x", "y"]].values
    hits = [[e] if e in OSM else [] for e in s.excluded_by.fillna("")]
    rules = [("lamp", s.size_class.map(LAMP).fillna(LAMP["small"]).values * LAMP_K)] + [(t, np.full(len(s), d)) for t, d in CLEAR.items()]
    for t, clear in rules:
        o = ob[ob.type == t]
        d = cKDTree(o[["x", "y"]].values).query(xy)[0]
        for i in np.flatnonzero(d < clear):
            hits[i].append(t)
    # a city rule recorded in excluded_by must be found again here (same data, same clearances)
    miss = [i for i, e in enumerate(s.excluded_by.fillna("")) if e and e not in OSM and e not in hits[i]]
    if miss:
        sys.exit(f"{len(miss)} spots lose their recorded reason: check clearances against porta_spot_exclusions_city.py")
    s["reasons"] = [";".join(sorted(set(h))) for h in hits]
    s["spot_class"] = [classify(h) for h in hits]
    s.to_csv(SPOTS, index=False)
    first = s.excluded_by.fillna("").map(lambda e: classify([e] if e else []))
    print("by first rule:", first.value_counts().to_dict())
    print("by all rules: ", s.spot_class.value_counts().to_dict())
    moved = s[first != s.spot_class]
    print("changed:", moved.groupby(["excluded_by", "spot_class"]).size().to_dict())


if __name__ == "__main__":
    main()
