"""Did the city's new trees survive? Every observed replacement 2018–2026 (scripts/inventory_history.py) checked against
the latest quarterly inventory file, plus the 385 positions of the back-test (scripts/backtest_works.py).

A planted tree is `alive` if its code is still in the latest file with the same taxon, or a tree of the same taxon stands
within R_M of it; `species changed` if the code or a tree within R_M now holds another taxon; `gone` otherwise.
ASSUMPTION: R_M = 2 m (one tree pit, as in inventory_history.py). A missing code is not proof of a death (re-surveys,
inventory lag), and a taxon change can be a re-identification, so `alive` is a lower bound on what still stands
and an upper bound on nothing.
Survival per species is age-standardised: the share alive in each class of years since planting, weighted by the
age mix of all replacements, so species planted earlier are not penalised for having had more time to fail.

Run (the latest quarterly file is gitignored, on the PC): python scripts/backtest_survival.py <arbrat_viari CSV>
Outputs: databases/barcelona/backtest_survival_age.csv (age class x set), backtest_survival_species.csv (one row per taxon)
"""
import ast
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
sys.path.insert(0, str(ROOT / "scripts"))
from backtest_works import works_groups  # noqa: E402

R_M = 2.0                                                  # ASSUMPTION: see docstring
AGE = ([0, 1, 2, 3, 5, 9], ["<1", "1-2", "2-3", "3-5", "5+"])


def ih_norm():
    """inventory_history.norm (same taxon reduction as the replacements file), without running that script."""
    src = (ROOT / "scripts/inventory_history.py").read_text(encoding="utf-8")
    keep = [n for n in ast.parse(src).body if (isinstance(n, ast.FunctionDef) and n.name == "norm") or
            (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in ("PLACEHOLDER", "SYNONYM"))]
    ns = {"re": re}
    exec(compile(ast.Module(keep, []), "inventory_history", "exec"), ns)
    return ns["norm"]


def main(latest):
    norm = ih_norm()
    q = pd.read_csv(latest, dtype=str)
    q["x"], q["y"], q["sp"] = q.x_etrs89.astype(float), q.y_etrs89.astype(float), q.cat_nom_cientific.map(norm)
    now = q.drop_duplicates("codi").set_index("codi").sp
    kd = cKDTree(q[["x", "y"]].values)
    last = 2026.5 if "2026_3T" in str(latest) else None     # years since planting counted to mid-2026 (file 2026 Q3)
    assert last, "set the quarter of the latest file"

    def status(d):
        d = d.copy()
        d["sp_in"] = d.species_in.map(norm)
        pres = d.codi_in.isin(now.index)
        dist, i = kd.query(d[["x", "y"]].values)
        same = (pres & (d.codi_in.map(now) == d.sp_in)) | ((dist <= R_M) & (q.sp.values[i] == d.sp_in))
        d["status"] = np.select([same, pres | (dist <= R_M)], ["alive", "species changed"], "gone")
        yr = d.quarter_added.str[:4].astype(int) + (d.quarter_added.str[-1].astype(int) - 1) / 4
        d["age"] = pd.cut(last - yr, AGE[0], labels=AGE[1])
        return d

    a = status(pd.read_csv(DB / "inventory_replacements.csv", dtype={"codi_in": str, "codi_out": str}))
    b = works_groups()
    b = status(b[b.group.isin(pd.read_csv(DB / "backtest_works.csv").group)])
    rows = []
    for name, d in (("all replacements", a), ("back-test", b)):
        for age, g in d.groupby("age", observed=True):
            rows.append(dict(set=name, age=age, n=len(g), alive=(g.status == "alive").mean(),
                             gone=(g.status == "gone").mean(), species_changed=(g.status == "species changed").mean()))
        rows.append(dict(set=name, age="all", n=len(d), alive=(d.status == "alive").mean(),
                         gone=(d.status == "gone").mean(), species_changed=(d.status == "species changed").mean()))
    pd.DataFrame(rows).round(3).to_csv(DB / "backtest_survival_age.csv", index=False)

    a["al"] = a.status == "alive"
    w = a.age.value_counts(normalize=True)
    t = a.groupby(["sp_in", "age"], observed=True).al.mean().unstack()
    sp = pd.DataFrame(dict(n=a.groupby("sp_in").size(), alive_raw=a.groupby("sp_in").al.mean(),
                           alive_std=(t * w).sum(axis=1) / t.notna().mul(w).sum(axis=1)))
    sp.index.name = "species"
    sp.round(3).sort_values("n", ascending=False).to_csv(DB / "backtest_survival_species.csv")
    print(pd.DataFrame(rows).round(2).to_string(index=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
