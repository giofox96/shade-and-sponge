"""Observed street-tree replacements in Barcelona, 2018-2026, from the quarterly open-data inventory files.

Why: S1a uses the 2026 target mix (press only). The city's quarterly `arbrat-viari` files (Open Data BCN, CC BY 4.0)
let us observe what is actually planted where a tree disappears -> an observed S1 (S1b) and a direct test of whether
replacements follow any rule (notes/data_sources_pemb_30oct.md §1; notes/tree_master_plan.md §5b).

Method, two kinds of replacement (column `kind`):
- same_code: the city keeps a pit's code when it replants it, so most replacements are a code whose taxon changes
  between quarters. Taxa are reduced to genus + epithet (cultivars, trade names, hybrid signs dropped; placeholders
  such as "Eliminar posicio" skipped, the last real taxon carried through them). Re-identification is removed by
  three ASSUMPTION filters: same-genus changes are dropped, a (taxon out, taxon in) change made more than MASS_N times
  in one quarter is re-coding (e.g. 42k Platanus x hispanica -> P. x acerifolia in 2023Q1), and a change later
  reversed on the same code is a correction. quarter_removed is the quarter before the change was seen. A
  same-species replant cannot be seen this way (the taxon does not change).
- new_code: a tree is REMOVED at quarter t if its code is in t and in no later file; a tree is ADDED at t if its code is in
no earlier file. Each removal is paired, one-to-one and nearest first, with an addition within R_M metres appearing
within K_Q quarters after it. ASSUMPTION: R_M = 2 m (one tree pit), K_Q = 4 quarters; a disappearance is not proof of a
felling, nor an appearance of a planting (code changes, re-surveys), so unmatched events are reported, not used.

Run (needs network to opendata-ajuntament.barcelona.cat, i.e. the local PC):
    python scripts/inventory_history.py
Inputs : quarterly CSVs of package `arbrat-viari` (downloaded to databases/barcelona/raw/arbrat_history/, gitignored)
Outputs: databases/barcelona/inventory_snapshots.csv       quarter, file, n trees
         databases/barcelona/inventory_replacements.csv    one row per replacement (both kinds)
         databases/barcelona/inventory_replacement_matrix.csv  taxon out x taxon in, both kinds pooled, city and Porta
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
MASS_N = 50                             # ASSUMPTION: more identical same-code changes per quarter = re-coding
PLACEHOLDER = r"^(eliminar|indeterminat|sense planta|prova|platanuss de prova)"
# Names the files switch between for one taxon (a misspelling, a synonym, genus renames seen in the 2018-2026 files).
# ASSUMPTION: read as re-coding, not replanting; checked against the change counts, not against a taxonomic authority.
SYNONYM = {"Platanus acerifolia": "Platanus hispanica", "Melia azederach": "Melia azedarach",
           "Hesperocyparis glabra": "Cupressus glabra", "Hesperocyparis macrocarpa": "Cupressus macrocarpa",
           "Hesperotropsis leylandii": "Cupressus leylandii", "Cuprocyparis leylandii": "Cupressus leylandii",
           "Cormus domestica": "Sorbus domestica", "Heptapleurum actinophyllum": "Schefflera actinophylla",
           "Feijoa sellowiana": "Acca sellowiana"}
SITE = "porta"                          # matched case-insensitively ("Porta", "la Porta", "PORTA" across vintages)
COLS = {"codi": ["codi"], "x": ["x_etrs89", "coord_x"], "y": ["y_etrs89", "coord_y"],
        "species": ["cat_nom_cientific", "nom_cientific"], "size": ["categoria_arbrat"], "barri": ["nom_barri"]}


def norm(s):
    """Genus + epithet, None for placeholders: 'Platanus � acerifolia PLATANOR' -> 'Platanus hispanica'."""
    s = str(s).replace("×", " ").replace("�", " ")
    t = [w for w in re.sub(r"'.*", "", s).split() if w.lower() != "x"]
    if not t or t[0] == "nan" or re.match(PLACEHOLDER, s, re.IGNORECASE):
        return None
    b = t[0].capitalize() + (f" {t[1].lower()}" if len(t) > 1 and t[1][0].islower() else "")
    return SYNONYM.get(b, b)


def quarterly_resources():
    res = requests.get(API, params={"id": "arbrat-viari"}, timeout=60).json()["result"]["resources"]
    out = {}
    for r in res:
        m = re.search(r"(20\d\d)_?(\d)T", r["name"], re.IGNORECASE)
        if m and r["name"].lower().endswith(".csv.zip"):      # quarterly files are zipped CSVs; URLs end in /download
            out.setdefault(f"{m[1]}Q{m[2]}", r["url"])     # first CSV per quarter
    return dict(sorted(out.items()))


def load(q, url):
    f = RAW / f"arbrat_viari_{q}.csv.zip"            # pandas infers zip from the suffix
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
    df["species"] = df.species.map(norm)
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
    p = pd.DataFrame(pairs).assign(kind="new_code")
    print(f"new_code: matched {len(p):,} ({len(p) / max(len(rem), 1):.1%} of removals) within {R_M} m / {K_Q} quarters")

    W = pd.concat([s.set_index("codi").species.rename(i) for i, s in enumerate(snaps)], axis=1)
    last, ev = W[0].copy(), []
    for i in range(1, len(snaps)):
        ch = W[i].notna() & last.notna() & (W[i] != last)
        ev.append(pd.DataFrame({"t": i, "codi": W.index[ch], "species_out": last[ch].values, "species_in": W[i][ch].values}))
        last = W[i].where(W[i].notna(), last)              # carry the last real taxon through gaps and placeholders
    sc = pd.concat(ev)
    n0 = len(sc)
    sc = sc[sc.species_out.str.split().str[0] != sc.species_in.str.split().str[0]]
    sc = sc[sc.groupby(["t", "species_out", "species_in"]).codi.transform("size") <= MASS_N]
    back = sc.merge(sc, left_on=["codi", "species_out", "species_in"], right_on=["codi", "species_in", "species_out"])
    sc = sc[~sc.codi.isin(back.codi)]
    print(f"same_code: {n0:,} taxon changes -> {len(sc):,} after genus / mass / reversal filters")
    att = pd.concat([s.assign(t=i) for i, s in enumerate(snaps)])[["t", "codi", "size", "x", "y"]]
    sc = sc.merge(att, on=["t", "codi"]).rename(columns={"codi": "codi_in", "size": "size_in"})
    sc = sc.assign(kind="same_code", codi_out=sc.codi_in, dist_m=0.0,
                   quarter_removed=[snaps[t - 1].q.iat[0] for t in sc.t], quarter_added=[snaps[t].q.iat[0] for t in sc.t])
    barri = pd.concat(snaps[::-1]).dropna(subset=["barri"]).drop_duplicates("codi").set_index("codi").barri
    p = pd.concat([p, sc.drop(columns="t")], ignore_index=True)
    p["barri"] = p.codi_in.map(barri)                      # 2018-2020 files have no barri: latest known name per code
    p = p.dropna(subset=["species_out", "species_in"])     # new_code pairs with a placeholder on either side
    p.to_csv(OUT / "inventory_replacements.csv", index=False)

    in_site = p.barri.astype(str).str.lower().str.replace("la ", "").str.strip() == SITE
    m = pd.concat([p.assign(scope="city"), p[in_site].assign(scope="porta")])
    m = m.groupby(["scope", "species_out", "species_in"]).size().rename("n").reset_index()
    m["share_of_out"] = (m.n / m.groupby(["scope", "species_out"]).n.transform("sum")).round(3)
    m.sort_values(["scope", "species_out", "n"], ascending=[True, True, False]).to_csv(
        OUT / "inventory_replacement_matrix.csv", index=False)
    pl = p[p.species_out.str.startswith("Platanus")]
    print(f"Platanus replaced {len(pl):,} times; top species in:", pl.species_in.value_counts().head(8).to_dict())
    nc = p[p.kind == "new_code"]
    print(f"same species replanted (new_code only): {(nc.species_out == nc.species_in).mean():.1%}; "
          f"by kind: {p.kind.value_counts().to_dict()}; Porta pairs: {in_site.sum()}")
    print("Porta top pairs:", m[m.scope == "porta"].nlargest(8, "n")[["species_out", "species_in", "n"]].values.tolist())
    print("new_code dist_m:", nc.dist_m.describe().round(2).to_dict())


if __name__ == "__main__":
    main()
