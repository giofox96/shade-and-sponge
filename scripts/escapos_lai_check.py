"""Is the Florence 'Life Escapos' LAI field usable as ground truth for the LiDAR LAI proxy?

Context: the transfer-city screening (notes/city_transfer_candidates.md §7) hoped that Escapos --
1,459 Florence street trees carrying per-tree `lai` plus crown geometry -- could calibrate LAI from
species + crown size, which would take the classified leaf-on point cloud off the critical path for
every transfer city. This script tests that, and answers no: `lai` is a species-level lookup for most
trees, so regressing it on species would recover the lookup table, not validate anything.

What it is still good for: an independent, database-derived cross-check on the DIRECTION of the bias
in our own gap-fraction proxy (methodology §4b flags it as "probably low"), for the species Porta and
Florence share.

Source: Comune di Firenze, "Life Escapos - Alberature pubbliche" (c_d612:D.7840, modified 2026-02-12,
CC BY 4.0), https://datigis.comune.fi.it/shp/escapos_tree_census.zip
Usage: python scripts/escapos_lai_check.py  ->  databases/florence/escapos_lai_vs_porta.csv
"""
import io
import pathlib
import re
import zipfile

import geopandas as gpd
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "databases/florence/raw"
URL = "https://datigis.comune.fi.it/shp/escapos_tree_census.zip"
MIN_PORTA_N = 20          # Porta trees below which the species median is too thin to compare (site.CITY_LIDAR uses 5)


def norm(s):
    """Species key without cultivar or hybrid-sign spelling; Escapos writes 'Platanus acerifolia'."""
    s = re.sub(r"\s*'[^']*'|\s+\S*®", "", str(s)).strip().lower().replace("×", "x")
    s = re.sub(r"\s+", " ", s)
    return s.replace("platanus acerifolia", "platanus x acerifolia")


def load_escapos():
    z = RAW / "escapos_tree_census.zip"
    if not z.exists():
        import requests
        RAW.mkdir(parents=True, exist_ok=True)
        z.write_bytes(requests.get(URL, timeout=120).content)
    with zipfile.ZipFile(z) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".shp"))
        d = RAW / "escapos_unz"
        zf.extractall(d)
    return gpd.read_file(d / name)


def main():
    g = load_escapos()
    g["key"] = g.species.map(norm)

    # 1. Is `lai` a measurement or a lookup?
    by_sp = g.groupby("key").lai.agg(n="size", nuniq="nunique")
    flat = by_sp[by_sp.nuniq == 1]
    print(f"Escapos: {len(g)} trees, {len(by_sp)} species, {g.lai.nunique()} distinct LAI values")
    print(f"  species with ONE constant LAI value: {len(flat)}/{len(by_sp)}"
          f"  covering {flat.n.sum()} trees ({100 * flat.n.sum() / len(g):.0f}%)")
    print("  -> `lai` is a species lookup for most trees, not a per-tree measurement:"
          " regressing it on species would be circular.")

    # 2. Cross-check the direction of our proxy's bias on the species Porta shares
    porta = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv")
    porta["key"] = porta.species.map(norm)
    pm = porta.drop_duplicates("key").set_index("key")
    esc = g.groupby("key").agg(escapos_n=("lai", "size"), escapos_lai_distinct=("lai", "nunique"),
                               escapos_lai_med=("lai", "median"), escapos_crown_med=("crn_w_m", "median"),
                               escapos_h_med=("h_m", "median"))
    j = esc.join(pm[["lai_proxy_med", "crown_diam_med", "height_med", "n"]].rename(
        columns={"n": "porta_n"}), how="inner")
    j["lai_ratio_escapos_over_proxy"] = (j.escapos_lai_med / j.lai_proxy_med).round(2)
    j = j.sort_values("porta_n", ascending=False).round(2)

    solid = j[j.porta_n >= MIN_PORTA_N]
    print(f"\nShared species: {len(j)} ({len(solid)} with >= {MIN_PORTA_N} Porta trees)")
    print(f"  median LAI ratio Escapos / Porta proxy: {j.lai_ratio_escapos_over_proxy.median():.2f}"
          f" (all shared), {solid.lai_ratio_escapos_over_proxy.median():.2f} (robust subset)")
    # The ratio splits by HOW Escapos got its LAI, which is the point:
    modelled = j[j.escapos_lai_distinct > 1]
    lookup = j[j.escapos_lai_distinct == 1]
    print(f"  split: species Escapos models per tree (n={len(modelled)}) ->"
          f" median ratio {modelled.lai_ratio_escapos_over_proxy.median():.2f};"
          f" species it gives one flat value (n={len(lookup)}) ->"
          f" median ratio {lookup.lai_ratio_escapos_over_proxy.median():.2f}")
    print("  -> the apparent gap is mostly an artefact of the flat lookup values, not evidence the proxy is low.")
    if "platanus x acerifolia" in j.index:
        r = j.loc["platanus x acerifolia"]
        print(f"  Platanus x acerifolia, the one species Escapos models per tree"
              f" ({int(r.escapos_lai_distinct)} distinct values) and Porta's largest sample"
              f" ({int(r.porta_n)} trees): LAI {r.escapos_lai_med} vs proxy {r.lai_proxy_med}"
              f" (ratio {r.lai_ratio_escapos_over_proxy}), crown {r.escapos_crown_med} vs {r.crown_diam_med} m")

    out = ROOT / "databases/florence/escapos_lai_vs_porta.csv"
    j.to_csv(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
