"""Species mix of Porta street trees planted in 2017 or later (the Arbres per viure plan period).

Usage: python scripts/porta_recent_plantings.py [min_year]
Input:  exchange/to_gh/porta_street_trees.csv (planting_date is empty for most trees: bias caveat, printed)
Output: databases/barcelona/porta_recent_plantings.csv (species, trees, share, first_year, last_year); cultivars stripped.
City-wide version: not produced (needs databases/barcelona/arbrat_viari.csv, blocked by bot detection in cloud).
"""
import re, sys, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
Y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2017


def species(s):
    n = re.sub(r"\s*['‘].*", "", s)                       # cultivar in quotes
    m = re.sub(r"\s+[A-Z ]+®.*$", "", n)                    # trade names (PLATANOR®, RESISTA®)
    return m if len(m.split()) >= 2 else n


t = pd.read_csv(ROOT / "exchange/to_gh/porta_street_trees.csv")
t["sp"] = t.species.map(species)
t["year"] = pd.to_datetime(t.planting_date, errors="coerce").dt.year
print(f"{len(t)} trees; undated {t.year.isna().sum()} ({t.year.isna().mean():.1%}); dated {t.year.notna().sum()}")
r = t[t.year >= Y0]
out = (r.groupby("sp").agg(trees=("sp", "size"), first_year=("year", "min"), last_year=("year", "max"))
       .sort_values("trees", ascending=False).reset_index().rename(columns={"sp": "species"}))
out["share"] = (out.trees / out.trees.sum()).round(3)
out[["species", "trees", "share", "first_year", "last_year"]].astype({"first_year": int, "last_year": int}).to_csv(
    ROOT / "databases/barcelona/porta_recent_plantings.csv", index=False)
print(f"{len(r)} trees dated >= {Y0}, {len(out)} species")
print(pd.crosstab(r.year, r.sp.where(r.sp.isin(out.species.head(6)), "other")).to_string())
