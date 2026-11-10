"""How many trees does a street project keep? (coordinator brief 10 Nov, Job B; tutor feedback notes/tutor_feedback_10nov.md)

For each replacement group of n >= 10 (scripts/replacement_clusters.py, groups recovered with its own link/groups
functions on databases/barcelona/inventory_replacements.csv): area = inventory trees within R_AREA of any member;
each tree in the BEFORE snapshot is classed by the AFTER snapshot as kept (same normalised taxon at the same code, or
at the nearest tree within R_MATCH if the code is gone), changed (different taxon) or gone (nothing within R_MATCH).
Added = AFTER trees in the area with no BEFORE tree within R_MATCH.

ASSUMPTION: R_AREA = 25 m (the clustering EPS), R_MATCH = 2 m (one pit, as inventory_history.R_M).
ASSUMPTION: BEFORE = walking back from the earliest quarter_removed among the members, the latest snapshot in which
  >= PRESENT (80%) of the members' old codes (codi_out) still carry a real taxon. quarter_removed alone is not enough:
  inventory_history carries the last real taxon through placeholder quarters, so works that empty the pits for months
  or years (e.g. Porta 2025Q4: poplars last listed 2022Q4) would leave the old trees out of the count. gap_q = quarters
  from BEFORE to the group's quarter. AFTER = group quarter + 4 quarters, or the latest snapshot if that is not yet published.
ASSUMPTION: the area is the 25 m buffer of the member points as recorded in inventory_replacements.csv (x, y).
ASSUMPTION: placeholder taxa (norm() -> None: "Eliminar posicio", "sense planta" ...) are empty pits, not trees.
Limits: a same-species replant at the same code reads as kept; the area buffer can take in trees of a crossing street.

Inputs: the quarterly inventory snapshots arbrat_viari_<YYYYQn>.csv.zip (35 quarters, 2018Q1-2026Q3) in
databases/barcelona/raw/arbrat_history/ (gitignored; inventory_history.py downloads them), or pass another folder.
Run from the repo root: python scripts/works_kept_changed_gone.py [path/to/arbrat_history]
Output: databases/barcelona/works_kept_changed_gone.csv
"""
import ast, sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import inventory_history as ih  # noqa: E402  reuse load() and norm()

R_AREA, R_MATCH, LAG, PRESENT = 25.0, 2.0, 4, 0.8
if len(sys.argv) > 1:
    ih.RAW = Path(sys.argv[1])

# reuse link()/groups() from replacement_clusters.py without running its top-level side effects (it writes a CSV)
src = (ROOT / "scripts/replacement_clusters.py").read_text(encoding="utf-8")
ns = {"np": np, "pd": pd}
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) or
                         (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "EPS")], []), "replacement_clusters", "exec"), ns)

d = pd.read_csv(ROOT / "databases/barcelona/inventory_replacements.csv")
d["group"] = ns["groups"](d, ns["EPS"])
ref = pd.read_csv(ROOT / "databases/barcelona/replacement_clusters.csv")
qs = sorted(f.name[13:19] for f in ih.RAW.glob("arbrat_viari_20*.csv.zip"))
snap = {}


def get(q):
    if q not in snap:
        snap[q] = ih.load(q, None).dropna(subset=["species"]).reset_index(drop=True)
    return snap[q]


rows = []
for gid, m in d.groupby("group"):
    if len(m) < 10:
        continue
    qa = m.quarter_added.iat[0]
    qa_i = qs.index(qa)
    i = qs.index(m.quarter_removed.min())
    while i > 0 and get(qs[i]).codi.isin(m.codi_out).sum() < PRESENT * m.codi_out.nunique():
        i -= 1
    qb = qs[i]
    qafter = qs[min(qa_i + LAG, len(qs) - 1)]
    B, A = get(qb), get(qafter)
    mt = cKDTree(m[["x", "y"]].values)
    inB = B[np.isfinite(mt.query(B[["x", "y"]].values, distance_upper_bound=R_AREA)[0])]
    inA = A[np.isfinite(mt.query(A[["x", "y"]].values, distance_upper_bound=R_AREA)[0])]
    a_by_code = A.set_index("codi").species
    ta = cKDTree(A[["x", "y"]].values)
    kept = changed = gone = 0
    for codi, sp, x, y in inB[["codi", "species", "x", "y"]].itertuples(index=False):
        if codi in a_by_code.index:
            sp2 = a_by_code[codi]
        else:
            dist, k = ta.query((x, y), distance_upper_bound=R_MATCH)
            sp2 = A.species.iat[k] if np.isfinite(dist) else None
        if sp2 is None:
            gone += 1
        elif sp2 == sp:
            kept += 1
        else:
            changed += 1
    tb = cKDTree(inB[["x", "y"]].values) if len(inB) else None
    added = int((~np.isfinite(tb.query(inA[["x", "y"]].values, distance_upper_bound=R_MATCH)[0])).sum()) if tb else len(inA)
    top = lambda s: s.value_counts().index[0]
    rows.append(dict(n=len(m), quarter=qa, before_q=qb, after_q=qafter, gap_q=qa_i - i,
                     members_in_before=int(B.codi.isin(m.codi_out).sum()),
                     barri=m.barri.mode().iat[0] if m.barri.notna().any() else "",
                     taxa_out=m.species_out.nunique(), taxa_in=m.species_in.nunique(), top_out=top(m.species_out),
                     top_in=top(m.species_in), before=len(inB), kept=kept, changed=changed, gone=gone, added=added,
                     kept_pct=round(100 * kept / len(inB), 1) if len(inB) else np.nan,
                     x=round(m.x.mean(), 1), y=round(m.y.mean(), 1)))

out = pd.DataFrame(rows).sort_values("n", ascending=False)
# self-check: the recovered groups are the published ones
r10 = ref[ref.n >= 10].sort_values(["n", "quarter", "x"]).reset_index(drop=True)
o10 = out.sort_values(["n", "quarter", "x"]).reset_index(drop=True)
assert len(r10) == len(o10) and (r10.n.values == o10.n.values).all() and (r10.quarter.values == o10.quarter.values).all() \
    and np.allclose(r10.x.values, o10.x.values, atol=0.11), "groups differ from replacement_clusters.csv"
assert (out.kept + out.changed + out.gone == out.before).all()
cols = ["n", "quarter", "barri", "top_out", "top_in", "before", "kept", "changed", "gone", "added", "kept_pct"]
out[cols + ["before_q", "gap_q", "members_in_before", "after_q", "taxa_out", "taxa_in", "x", "y"]].to_csv(ROOT / "databases/barcelona/works_kept_changed_gone.csv", index=False)
pd.set_option("display.width", 250, "display.max_colwidth", 28)
print(out[cols].head(20).to_string(index=False))


def iqr(s):
    return f"median {s.median():.1f}% (IQR {s.quantile(.25):.1f}-{s.quantile(.75):.1f}), n={len(s)}"


reid = (out.taxa_out == 1) & (out.taxa_in == 1)
print("all n>=10:", iqr(out.kept_pct))
print("one taxon out, one in (possible re-identification):", iqr(out.kept_pct[reid]))
print("the rest:", iqr(out.kept_pct[~reid]))
print("BEFORE more than 1 quarter before the group (pits emptied first):", (out.gap_q > 1).sum(), "groups; median gap", out.gap_q.median())
print("after = latest snapshot (lag < 4 quarters):", (out.after_q == qs[-1]).sum(), "groups")
