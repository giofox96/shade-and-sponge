"""Crown size of the palette species vs the plane tree in Porta, raw and at equal trunk size.

Input:  exchange/to_gh/porta_trees_lidar.csv (scripts/bcn_lidar_porta.py; ICGC LiDAR 2021, watershed crowns)
Output: databases/barcelona/crown_by_trunk_class.csv
Trunk class = the inventory's categoria_arbrat: PRIMERA <= 40 cm, SEGONA 41-80, TERCERA 81-110, EXEMPLAR > 110 cm
perimeter at 1 m (Ajuntament de Barcelona 2011, Gestio de l'arbrat viari, p. 18). Raw medians mix trunk classes,
so a species with many old trees looks bigger than it is at equal size (notes/topic_decision.md §9.9).
"""
import pathlib, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANE = "Platanus x acerifolia"
SPECIES = [PLANE, "Melia azedarach", "Tipuana tipu", "Jacaranda mimosifolia", "Celtis australis",
           "Brachychiton populneus", "Pyrus calleryana", "Styphnolobium japonicum"]

t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
t["sp"] = t.species.str.replace(r"\s*'.*", "", regex=True).str.replace("×", "x")
ok = t[(t.flag == "ok") & t.sp.isin(SPECIES)]
med = ok.pivot_table(index="sp", columns="size_category", values="crown_diam_m", aggfunc="median").reindex(SPECIES)
n = ok.pivot_table(index="sp", columns="size_category", values="crown_diam_m", aggfunc="size").reindex(SPECIES)
med["ALL"] = ok.groupby("sp").crown_diam_m.median()
n["ALL"] = ok.groupby("sp").size()
ratio = (med / med.loc[PLANE]) ** 2                       # crown-area ratio vs the plane, same trunk class
out = pd.concat({"crown_diam_med_m": med.round(2), "n": n, "area_ratio_vs_plane": ratio.round(2)}, axis=1)

summary = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv", index_col="species")
summary.index = summary.index.str.replace("×", "x")
for s in SPECIES:                                          # self-check: raw medians match the published summary
    assert abs(med.loc[s, "ALL"] - summary.loc[s, "crown_diam_med"]) < 0.01, s
out.to_csv(ROOT / "databases/barcelona/crown_by_trunk_class.csv")
print(out.xs("area_ratio_vs_plane", axis=1, level=0).to_string())
