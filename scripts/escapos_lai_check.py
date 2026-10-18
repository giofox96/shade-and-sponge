"""Is the Florence 'Life Escapos' LAI field usable as ground truth for the LiDAR LAI proxy?

Context: the transfer-city screening (notes/city_transfer_candidates.md §7) hoped that Escapos --
1,459 Florence street trees carrying per-tree `lai` plus crown geometry -- could calibrate LAI from
species and crown size, which would take the classified leaf-on point cloud off the critical path for
every transfer city.

Answer: no. Every LAI value in the table is a deterministic function of species and DBH. For most
species it is a single flat constant; for the rest it is that constant times DBH^~0.2 (log-log
R2 = 1.0000 within each species, distinct-LAI count == distinct-DBH count). Nothing is measured, so
the field cannot calibrate or validate an independent LAI estimate.

The script also compares the table against our own gap-fraction proxy for the species Porta and
Florence share, and shows why that comparison measures tree SIZE rather than proxy accuracy.

Source: Comune di Firenze, "Life Escapos - Alberature pubbliche" (c_d612:D.7840, metadata modified
Feb 2026), https://datigis.comune.fi.it/shp/escapos_tree_census.zip
Licence: CC BY-NC 4.0 -- NON-COMMERCIAL, `isopen: false` in the CKAN record. Not CC BY.
Usage: python scripts/escapos_lai_check.py  ->  databases/florence/escapos_lai_vs_porta.csv
"""
import pathlib
import re
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/florence/raw"
URL = "https://datigis.comune.fi.it/shp/escapos_tree_census.zip"
MIN_PORTA_N = 20     # a species LAI median from fewer Porta trees is too noisy for a city-to-city ratio.
                     # Deliberately stricter than the repo's usual bar of 5 (scripts/transfer_species_overlap.py),
                     # because here the quantity compared is a median of a median, not a presence test.
ALIAS = {"platanus acerifolia": "platanus x acerifolia",   # Escapos drops the hybrid sign; Porta keeps it
         "tilia europaea": "tilia x europaea"}             # same taxon, Tilia x europaea L.


def norm(s):
    """Species key without cultivar or hybrid-sign spelling, with the Escapos spellings aliased."""
    s = re.sub(r"\s*'[^']*'|\s+\S*®", "", str(s)).strip().lower().replace("×", "x")
    s = re.sub(r"\s+", " ", s)
    return ALIAS.get(s, s)


def load_escapos():
    z = RAW / "escapos_tree_census.zip"
    if not z.exists():
        import requests
        RAW.mkdir(parents=True, exist_ok=True)
        z.write_bytes(requests.get(URL, timeout=120).content)
    d = RAW / "escapos_unz"
    with zipfile.ZipFile(z) as zf:
        names = [n for n in zf.namelist() if not n.startswith(("/", "..")) and ".." not in n]
        zf.extractall(d, members=names)                    # third-party zip: no absolute or parent paths
        shp = next(n for n in names if n.endswith(".shp"))
    return gpd.read_file(d / shp)


def main():
    g = load_escapos()
    g["key"] = g.species.map(norm)

    # 1. Where does `lai` come from? Flat per species, or a function of DBH?
    by_sp = g.groupby("species").lai.agg(n="size", nuniq="nunique")
    flat, varying = by_sp[by_sp.nuniq == 1], by_sp[by_sp.nuniq > 1]
    print(f"Escapos: {len(g)} trees, {len(by_sp)} species, {g.lai.nunique()} distinct LAI values")
    print(f"  one flat LAI value for the whole species: {len(flat)}/{len(by_sp)} species"
          f" ({int((flat.n >= 5).sum())} of them with >= 5 trees), {flat.n.sum()} trees"
          f" ({100 * flat.n.sum() / len(g):.0f}%)")

    rows = []
    for sp in varying.index:
        d = g[g.species == sp]
        x, y = np.log(d.dbh_cm.values), np.log(d.lai.values)
        b, _ = np.polyfit(x, y, 1)
        rows.append((sp, len(d), d.lai.nunique(), d.dbh_cm.nunique(), np.corrcoef(x, y)[0, 1] ** 2, b))
    law = pd.DataFrame(rows, columns=["species", "n", "lai_distinct", "dbh_distinct", "loglog_r2", "exponent"])
    law = law.sort_values("n", ascending=False)
    exact = law[(law.lai_distinct == law.dbh_distinct) & (law.loglog_r2 > 0.9999)]
    print(f"  the other {len(varying)} species: LAI is an exact power law of DBH in {len(exact)}/{len(law)}"
          f" (distinct-LAI == distinct-DBH, log-log R2 > 0.9999, exponent"
          f" {law.exponent.min():.2f}-{law.exponent.max():.2f})")
    print(law.head(5).round(4).to_string(index=False))
    print("  -> nothing in this table is measured: `lai` = species constant x DBH^~0.2.")
    print("     It cannot calibrate or validate an independent LAI estimate.")

    # 2. Compare with our proxy anyway -- and show what the comparison actually tracks
    porta = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv")
    porta["key"] = porta.species.map(norm)
    pm = porta.sort_values("n", ascending=False).drop_duplicates("key").set_index("key")   # keep the dominant row
    esc = g.groupby("key").agg(escapos_n=("lai", "size"), escapos_lai_distinct=("lai", "nunique"),
                               escapos_lai_med=("lai", "median"), escapos_crown_med=("crn_w_m", "median"),
                               escapos_dbh_med=("dbh_cm", "median"))
    j = esc.join(pm[["lai_proxy_med", "crown_diam_med", "n"]].rename(columns={"n": "porta_n"}), how="inner")
    j["lai_ratio"] = (j.escapos_lai_med / j.lai_proxy_med).round(2)
    j["crown_ratio"] = (j.escapos_crown_med / j.crown_diam_med).round(2)
    j = j.sort_values("porta_n", ascending=False).round(2)
    solid = j[j.porta_n >= MIN_PORTA_N]

    print(f"\nShared species: {len(j)} ({len(solid)} with >= {MIN_PORTA_N} Porta trees)")
    print(f"  LAI ratio Escapos/proxy: median {j.lai_ratio.median():.2f} (all),"
          f" {solid.lai_ratio.median():.2f} (robust); range {j.lai_ratio.min():.2f}-{j.lai_ratio.max():.2f}")
    print(f"  Spearman(LAI ratio, crown ratio) = {j.lai_ratio.corr(j.crown_ratio, method='spearman'):+.2f}"
          "  <- the ratio tracks how much bigger the Florence trees are, not proxy accuracy")
    for k in ("tilia x europaea", "platanus x acerifolia"):
        if k in j.index:
            r = j.loc[k]
            print(f"  {k:<22} LAI {r.escapos_lai_med} vs proxy {r.lai_proxy_med} (ratio {r.lai_ratio});"
                  f" crown {r.escapos_crown_med} vs {r.crown_diam_med} m (ratio {r.crown_ratio});"
                  f" Porta n={int(r.porta_n)}")

    out = ROOT / "databases/florence/escapos_lai_vs_porta.csv"
    j.to_csv(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
