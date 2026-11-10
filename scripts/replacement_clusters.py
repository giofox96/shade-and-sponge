"""Are street trees replaced one by one or street by street? (tutor feedback 10 Nov, notes/tutor_feedback_10nov.md A1)

Groups the observed replacements (scripts/inventory_history.py -> databases/barcelona/inventory_replacements.csv)
that were first seen in the same quarter and lie within EPS metres of each other (single linkage). A large group is the
signature of street works or a campaign; a group of one is a single tree replaced on its own.
ASSUMPTION: EPS = 25 m (about three tree spacings); 15 and 40 m are printed as a sensitivity.
Limits: same-species replants are invisible in the input, so groups are a floor; a large group with one taxon out and
one taxon in may be a re-identification that the input's filters missed, not a planting.

Run: python scripts/replacement_clusters.py
Output: databases/barcelona/replacement_clusters.csv  (one row per group of >= 5)
"""
from pathlib import Path

import numpy as np
import pandas as pd

DB = Path(__file__).resolve().parents[1] / "databases/barcelona"
EPS = 25.0


def link(xy, eps):
    """Single-linkage group label per point (union-find on a grid of eps cells)."""
    par = list(range(len(xy)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    cell = {}
    for i, (x, y) in enumerate(xy):
        cell.setdefault((int(x // eps), int(y // eps)), []).append(i)
    for (cx, cy), ids in cell.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in cell.get((cx + dx, cy + dy), []):
                    for i in ids:
                        if i < j and ((xy[i] - xy[j]) ** 2).sum() <= eps * eps:
                            par[find(i)] = find(j)
    return np.unique([find(i) for i in range(len(xy))], return_inverse=True)[1]


def groups(d, eps):
    lab, k = np.zeros(len(d), int), 0
    for _, g in d.groupby("quarter_added"):
        l = link(g[["x", "y"]].values, eps)
        lab[g.index] = l + k
        k += l.max() + 1
    return lab


d = pd.read_csv(DB / "inventory_replacements.csv")
plane = d.species_out.str.startswith("Platanus")
for eps in (15.0, EPS, 40.0):
    n = pd.Series(groups(d, eps)).pipe(lambda s: s.map(s.value_counts()))
    print(f"eps {eps:.0f} m: alone {100 * (n == 1).mean():.1f}% | in groups >=5 {100 * (n >= 5).mean():.1f}% | >=10 "
          f"{100 * (n >= 10).mean():.1f}% | planes alone {100 * (n == 1)[plane].mean():.1f}%, >=10 {100 * (n >= 10)[plane].mean():.1f}%")
d["group"] = groups(d, EPS)
out = d.groupby("group").agg(n=("x", "size"), quarter=("quarter_added", "first"),
                             barri=("barri", lambda s: s.mode().iat[0] if s.notna().any() else ""),
                             taxa_out=("species_out", "nunique"), top_out=("species_out", lambda s: s.value_counts().index[0]),
                             taxa_in=("species_in", "nunique"), top_in=("species_in", lambda s: s.value_counts().index[0]),
                             x=("x", "mean"), y=("y", "mean"))
out = out[out.n >= 5].sort_values("n", ascending=False).round({"x": 1, "y": 1})
out.to_csv(DB / "replacement_clusters.csv", index=False)
print(len(out), "groups of >= 5;", (out.n >= 10).sum(), "of >= 10;", ((out.n >= 10) & (out.taxa_out == 1) & (out.taxa_in == 1)).sum(),
      "of those have one taxon out and one in")
