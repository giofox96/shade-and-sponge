"""Observed street-tree replacements in Barcelona, 2021-2026, from the quarterly open-data inventory files.

Why: S1a uses the 2026 target mix (press only). The city's quarterly `arbrat-viari` files (Open Data BCN, CC BY 4.0)
let us observe what is actually planted where a tree disappears -> an observed S1 (S1b) and a direct test of whether
replacements follow any rule (notes/data_sources_pemb_30oct.md §1; notes/tree_master_plan.md §5b).

Method: a tree is REMOVED at quarter t if its code is in t and in no later file; a tree is ADDED at t if its code is in
no earlier file. Each removal is paired, one-to-one and nearest first, with an addition within R_M metres appearing
within K_Q quarters after it. ASSUMPTION: R_M = 2 m (one tree pit), K_Q = 4 quarters; a disappearance is not proof of a
felling, nor an appearance of a planting (code changes, re-surveys), so unmatched events are reported, not used.

Run (needs network to opendata-ajuntament.barcelona.cat, i.e. the local PC):
    python scripts/inventory_history.py
Inputs : quarterly CSVs of package `arbrat-viari` (downloaded to databases/barcelona/raw/arbrat_history/, gitignored)
Outputs: databases/barcelona/inventory_snapshots.csv       quarter, file, n trees
         databases/barcelona/inventory_replacements.csv    one row per matched removal -> addition
         databases/barcelona/inventory_replacement_matrix.csv  species out x species in, city and Porta
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy.spatial import cKDTree

API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show"
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/barcelona/raw/arbrat_history"
OUT = ROOT / "databases/barcelona"
R_M, K_Q = 2.0, 4                       # ASSUMPTION: pairing radius (m) and window (quarters), see docstring
SITE = "porta"                          # matched case-insensitively ("Porta", "la Porta", "PORTA" across vintages)
COLS = {"codi": ["codi"], "x": ["x_etrs89", "coord_x"], "y": ["y_etrs89", "coord_y"],
        "species": ["cat_nom_cientific", "nom_cientific"], "size": ["categoria_arbrat"], "barri": ["nom_barri"]}


def quarterly_resources():
    res = requests.get(API, params={"id": "arbrat-viari"}, timeout=60).json()["result"]["resources"]
    out = {}
    for r in res:
        m = re.search(r"(20\d\d)_?(\d)T", r["name"] + " " + r["url"], re.IGNORECASE)
        if m and r["url"].lower().split("?")[0].endswith(".csv"):
            out.setdefault(f"{m[1]}Q{m[2]}", r["url"])     # first CSV per quarter
    return dict(sorted(out.items()))


def load(q, url):
    f = RAW / f"arbrat_viari_{q}.csv"
    if not f.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        f.write_bytes(requests.get(url, timeout=300).content)
    df = pd.read_csv(f, low_memory=False, encoding_errors="replace")
    df.columns = [c.strip().lower() for c in df.columns]
    pick = {k: next((c for c in v if c in df.columns), None) for k, v in COLS.items()}
    missing = [k for k in ("codi", "x", "y", "species") if pick[k] is None]
    if missing:
        raise SystemExit(f"{q}: columns {missing} not found in {list(df.columns)[:20]}")
    df = df.rename(columns={v: k for k, v in pick.items() if v}).reindex(columns=list(COLS))
    df["species"] = df.species.astype(str).str.replace(r"\s*'.*", "", regex=True).str.strip()
    return df.dropna(subset=["codi", "x", "y"]).drop_duplicates("codi").assign(q=q)


def main():
    qs = quarterly_resources()
    print(f"{len(qs)} quarterly files:", ", ".join(qs))
    snaps = [load(q, u) for q, u in qs.items()]
    pd.DataFrame({"quarter": list(qs), "url": list(qs.values()), "n_trees": [len(s) for s in snaps]}).to_csv(
        OUT / "inventory_snapshots.csv", index=False)

    seen_later = [set() for _ in snaps]                     # codes present in any later file
    acc = set()
    for i in range(len(snaps) - 1, -1, -1):
        seen_later[i] = set(acc)
        acc |= set(snaps[i].codi)
    seen_before, acc = [], set()
    for s in snaps:
        seen_before.append(set(acc))
        acc |= set(s.codi)

    rem = pd.concat([s[~s.codi.isin(seen_later[i])].assign(t=i) for i, s in enumerate(snaps[:-1])])
    add = pd.concat([s[~s.codi.isin(seen_before[i])].assign(t=i) for i, s in enumerate(snaps) if i > 0])
    print(f"removed {len(rem):,}  added {len(add):,}")

    tree = cKDTree(add[["x", "y"]].values)
    cand = []
    for j, (ri, r) in enumerate(zip(rem.itertuples(), rem[["x", "y"]].values)):
        for k in tree.query_ball_point(r, R_M):
            dt = add.t.iat[k] - ri.t
            if 1 <= dt <= K_Q:
                cand.append((float(np.hypot(*(add[["x", "y"]].values[k] - r))), dt, j, k))
    used_r, used_a, pairs = set(), set(), []
    for d, dt, j, k in sorted(cand):                        # one-to-one, nearest first, then soonest
        if j in used_r or k in used_a:
            continue
        used_r.add(j); used_a.add(k)
        a, b = rem.iloc[j], add.iloc[k]
        pairs.append({"quarter_removed": snaps[a.t].q.iat[0], "quarter_added": snaps[b.t].q.iat[0], "dist_m": round(d, 2),
                      "codi_out": a.codi, "species_out": a.species, "size_out": a["size"], "codi_in": b.codi,
                      "species_in": b.species, "size_in": b["size"], "barri": b.barri, "x": b.x, "y": b.y})
    p = pd.DataFrame(pairs)
    p.to_csv(OUT / "inventory_replacements.csv", index=False)
    print(f"matched {len(p):,} replacements ({len(p) / max(len(rem), 1):.1%} of removals) within {R_M} m / {K_Q} quarters")

    in_site = p.barri.astype(str).str.lower().str.replace("la ", "").str.strip() == SITE
    m = pd.concat([p.assign(scope="city"), p[in_site].assign(scope="porta")])
    m = m.groupby(["scope", "species_out", "species_in"]).size().rename("n").reset_index()
    m["share_of_out"] = (m.n / m.groupby(["scope", "species_out"]).n.transform("sum")).round(3)
    m.sort_values(["scope", "species_out", "n"], ascending=[True, True, False]).to_csv(
        OUT / "inventory_replacement_matrix.csv", index=False)
    pl = p[p.species_out.str.startswith("Platanus")]
    print(f"Platanus replaced {len(pl):,} times; top species in:", pl.species_in.value_counts().head(8).to_dict())
    print(f"same species replanted: {(p.species_out == p.species_in).mean():.1%}; "
          f"Porta pairs: {in_site.sum()}")


if __name__ == "__main__":
    main()
