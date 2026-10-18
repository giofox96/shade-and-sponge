"""How much of a candidate transfer city's tree stock is already parameterised by Porta's LiDAR?

Transfer cost is mostly data (notes/transferability.md). This measures one part of it: the share of a city's
most common street trees whose species already has crown, height and LAI-proxy medians measured in Porta
(databases/barcelona/porta_species_lidar_summary.csv). A species-level match means the trait table, the
leaf-on calendar and the gap-filling class carry over; the crown geometry itself must still be re-measured
from the new city's own LiDAR (Porta's medians reflect Barcelona's planting age and pruning regime).

Input: databases/<city>/species_coverage.csv (top-30 species per city, from scripts/species_coverage.py).
Output: databases/transfer_species_overlap.csv + a printed summary.
"""
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
CITIES = ["florence", "barcelona"]          # barcelona = sanity check (city-wide top-30 vs the Porta subset)
TOTALS = {"florence": 82226, "barcelona": 140404}   # trees in the full inventory (databases/data_inventory*.md F1, A1)


def norm(s):
    """Species key without cultivar, trade mark or hybrid-sign spelling: "Platanus × acerifolia PLATANOR®" -> "platanus x acerifolia"."""
    s = re.sub(r"\s*'[^']*'|\s+\S*®", "", str(s)).strip().lower().replace("×", "x")
    return re.sub(r"\s+", " ", s)


def main():
    porta = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv")
    porta["key"] = porta.species.map(norm)
    measured = porta.drop_duplicates("key").set_index("key")
    genera = {k.split()[0] for k in measured.index}

    out = []
    for city in CITIES:
        c = pd.read_csv(ROOT / f"databases/{city}/species_coverage.csv")
        c["key"] = c.species.map(norm)
        c["city"] = city
        c["in_porta_lidar"] = c.key.isin(measured.index)
        c["genus_in_porta_lidar"] = c.key.str.split().str[0].isin(genera)
        c["porta_crown_diam_m"] = c.key.map(measured.crown_diam_med)
        c["porta_lai_proxy"] = c.key.map(measured.lai_proxy_med)
        c["porta_n_trees"] = c.key.map(measured.n)
        out.append(c)

        top, sp, gen = c.trees.sum(), c.loc[c.in_porta_lidar, "trees"].sum(), c.loc[c.genus_in_porta_lidar, "trees"].sum()
        print(f"{city}: top-{len(c)} species = {top:,} trees ({100 * top / TOTALS[city]:.1f}% of the inventory)")
        print(f"  species measured in Porta: {c.in_porta_lidar.sum()} species, {sp:,} trees ({100 * sp / top:.1f}% of the top-30)")
        print(f"  genus measured in Porta:   {gen:,} trees ({100 * gen / top:.1f}%)")
        miss = c[~c.genus_in_porta_lidar].nlargest(5, "trees")
        print("  largest gaps (not even the genus):", ", ".join(f"{r.species} {r['share_%']}%" for _, r in miss.iterrows()) or "none")

    cols = ["city", "species", "trees", "share_%", "in_porta_lidar", "genus_in_porta_lidar",
            "porta_n_trees", "porta_crown_diam_m", "porta_lai_proxy", "runoff_measured", "heat_measured"]
    p = ROOT / "databases/transfer_species_overlap.csv"
    pd.concat(out)[cols].to_csv(p, index=False)
    print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
