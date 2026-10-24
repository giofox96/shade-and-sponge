"""Do Porta's recent plantings follow the city's district replacement table?

Table: Parcs i Jardins, "Arbrat viari: selecció d'espècies" (2002, rev. May 2004) p. 11,
repeated in "Pla de gestió de l'arbrat viari de Barcelona" (Dec 2005, rev. Jan 2006) §3.4.3.
Row 8, Nou Barris: sidewalk < 3.5 m -> Prunus cerasifera 'Atropurpurea';
3.5-6 m -> Melia azedarach or Jacaranda mimosifolia; > 6 m -> keep Platanus or the existing species.
Inputs: Porta sidewalk size class (porta_sidewalk_width.csv) + planting date (Open Data BCN inventory).
Output: databases/barcelona/replacement_rule_check.csv (species planted per size class, 2007-2026).
"""
import sys
import pandas as pd

INV = sys.argv[1] if len(sys.argv) > 1 else "databases/barcelona/arbrat_viari.csv"
# Run from the repo root. Match is on genus + species only, so Prunus cerasifera 'Pissardii' counts as 'Atropurpurea'.
TABLE = {"small": {"Prunus cerasifera"}, "medium": {"Melia azedarach", "Jacaranda mimosifolia"}}

a = pd.read_csv(INV, dtype=str, usecols=["codi", "data_plantacio"])
w = pd.read_csv("databases/barcelona/porta_sidewalk_width.csv", dtype=str)
m = w.merge(a, left_on="tree_id", right_on="codi", how="left")
m = m[m.data_plantacio.notna() & m.size_class.isin(["small", "medium", "large"])]
m["genus_sp"] = m.species.str.split().str[:2].str.join(" ")
m["in_table"] = [g in TABLE.get(c, set()) for g, c in zip(m.genus_sp, m.size_class)]

out = (m.groupby(["size_class", "genus_sp"]).agg(n=("tree_id", "size"), in_table=("in_table", "first"))
       .reset_index().sort_values(["size_class", "n"], ascending=[True, False]))
out.to_csv("databases/barcelona/replacement_rule_check.csv", index=False)
for c in ["small", "medium", "large"]:
    s = m[m.size_class == c]
    print(f"{c}: {len(s)} planted 2007-2026, {s.in_table.mean():.0%} as the table says" if c in TABLE else
          f"{c}: {len(s)} planted 2007-2026 (table: keep Platanus/existing)")
    print("  ", s.genus_sp.value_counts().head(6).to_dict())
