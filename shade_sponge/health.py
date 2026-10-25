"""Replacement-priority proxy v0 (notes/citywide_plan.md §3): which trees are likely to be replaced first.
No open tree-condition data exists, so the score combines two proxies (both ASSUMPTION, to validate against the trees
removed between two Open Data BCN inventory snapshots, not done yet):
- crown vigour deficit: a small or open crown for its species and trunk class (LiDAR 2021, crown area and gap fraction);
- age: the trunk class of the inventory (perimeter classes SEGONA 41–80 cm, TERCERA 81–110 cm, 2011 guide p. 18;
  PRIMERA below and EXEMPLAR above are ASSUMPTION, EXEMPLAR is undefined; trunk class read as age is ASSUMPTION).
Run: python -m shade_sponge.health [site] -> databases/barcelona/<site>_priority.csv"""
import sys

CLASS_AGE = {"PRIMERA": 0, "SEGONA": 1, "TERCERA": 2, "EXEMPLAR": 3}
MIN_PEERS = 10      # ASSUMPTION: fewer LiDAR-measured peers in a species × trunk class -> compare within the species
W_VIGOUR = 0.5      # ASSUMPTION: vigour deficit and age weigh equally


def priority(trees):
    """Per tree: vigour_deficit (near 0 = strongest crown among its peers, 1 = weakest), age (0–1), priority (0–1).
    Peers = same species and trunk class (else the same species). ASSUMPTION: a mapped tree without a usable LiDAR crown
    (flag != ok: none detected, few points, low) gets deficit 1, as it may be missing, dead or heavily pruned."""
    t = trees[["tree_id", "sp", "size_category", "crown_area_m2", "gap_fraction", "flag"]].copy()
    ok = t.flag == "ok"
    n = t[ok].groupby(["sp", "size_category"]).tree_id.transform("size")
    t["peer_group"] = "species"
    t.loc[n[n >= MIN_PEERS].index, "peer_group"] = "species_class"
    t["vigour_deficit"] = 1.0
    for level, keys in (("species_class", ["sp", "size_category"]), ("species", ["sp"])):
        m = ok & (t.peer_group == level)
        g = t[m].groupby(keys)
        # average of two percentile ranks within the peers: smaller crown area, larger gap fraction = weaker
        t.loc[m, "vigour_deficit"] = 0.5 * (g.crown_area_m2.rank(pct=True, ascending=False) + g.gap_fraction.rank(pct=True))
    t["age"] = t.size_category.map(CLASS_AGE) / max(CLASS_AGE.values())
    t["priority"] = W_VIGOUR * t.vigour_deficit + (1 - W_VIGOUR) * t.age.fillna(0)   # ASSUMPTION: unknown trunk class -> age 0
    return t.drop(columns=["crown_area_m2", "gap_fraction"])


if __name__ == "__main__":
    from .site import DB
    from . import site as S
    name = ([a for a in sys.argv[1:] if not a.startswith("--")] or ["porta"])[0]
    t = getattr(S, f"trees_{name}")()
    p = priority(t).merge(t[["tree_id", "x", "y", "is_plane", "street"]], on="tree_id")
    p.round(3).to_csv(DB / f"{name}_priority.csv", index=False)
    pl = p[p.is_plane]
    print(f"{len(p)} trees, {len(pl)} planes; plane priority quartiles:", pl.priority.quantile([.25, .5, .75]).round(2).tolist())
    print("mean plane priority by trunk class:", pl.groupby("size_category").priority.mean().round(2).to_dict())
    print("planes without a usable crown:", int((pl.flag != "ok").sum()))
