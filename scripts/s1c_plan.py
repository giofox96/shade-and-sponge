"""S1c input: the city's own replacement plan for Porta's planes. python scripts/s1c_plan.py
Reads the Parcs i Jardins spreadsheet (received 24 Nov 2026; internal document, kept in the gitignored
databases/barcelona/raw/parcs_jardins/) and writes raw/parcs_jardins/porta_plan_planes.csv: tree_id, species for every Porta
plane (the tool's trees) whose planned species (NOM_SUBST) differs from today's. Planes with no plan or the same species stay.
Then: python -m shade_sponge porta --palette=barcelona --size=exact --trunk=TERCERA --plan=<that CSV>
Credit: Parcs i Jardins de Barcelona, Institut Municipal. Ajuntament de Barcelona."""
import sys, pandas as pd
sys.path.insert(0, ".")
from shade_sponge.site import trees_porta, RAW

D = RAW / "parcs_jardins"
x = pd.read_excel(D / "Arbrat_Barri_Porta_planned_species.xlsx")
t = trees_porta()
planes = set(t.tree_id[t.is_plane])
x = x[x.CODI_ELEM.isin(planes) & x.NOM_SUBST.notna() & (x.NOM_SUBST != x.NOM_ESPECIE)]
out = x.rename(columns=dict(CODI_ELEM="tree_id", NOM_SUBST="species"))[["tree_id", "species"]]
out.to_csv(D / "porta_plan_planes.csv", index=False)
print(f"{len(out)} of {len(planes)} planes change in the plan:\n{out.species.value_counts().to_string()}")
