"""Planting date (data_plantacio) of every back-test group member, before and after the change, for the
inventory-correction filter in scripts/backtest_works.py (works_groups).

For each member of the candidate groups: data_plantacio of codi_out in the quarter_removed release and of codi_in in the
quarter_added release (quarterly releases of package `arbrat-viari`, Open Data BCN, CC BY 4.0; URLs in
databases/barcelona/inventory_snapshots.csv; streamed, nothing kept on disk but the output).
Run (PC, internet): python scripts/backtest_planting_dates.py -> databases/barcelona/backtest_planting_dates.csv
"""
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from backtest_works import works_groups  # noqa: E402

DB = ROOT / "databases/barcelona"


def release(url):
    b = requests.get(url, timeout=300).content
    try:
        z = zipfile.ZipFile(io.BytesIO(b))
        b = z.read([n for n in z.namelist() if n.lower().endswith(".csv")][0])
    except zipfile.BadZipFile:
        pass
    r = pd.read_csv(io.BytesIO(b), dtype=str, encoding_errors="replace")
    r.columns = [c.strip().lower() for c in r.columns]
    return r.set_index("codi").data_plantacio


def main():
    d = works_groups(filter_corrections=False)
    urls = pd.read_csv(DB / "inventory_snapshots.csv").set_index("quarter").url
    rows = []
    for q in sorted(set(d.quarter_removed) | set(d.quarter_added)):
        pdate = release(urls[q])
        for col, qcol in (("codi_out", "quarter_removed"), ("codi_in", "quarter_added")):
            c = d.loc[d[qcol] == q, col].dropna().unique()
            rows += [dict(codi=k, quarter=q, data_plantacio=pdate.get(k)) for k in c]
        print(q, len(rows), flush=True)
    out = pd.DataFrame(rows).drop_duplicates(["codi", "quarter"])
    out.to_csv(DB / "backtest_planting_dates.csv", index=False)
    print("wrote", len(out), "rows")


if __name__ == "__main__":
    main()
