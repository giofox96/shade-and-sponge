"""Species trait table for Porta's street-tree palette (species-level values only, every value with its source).

Inputs: databases/barcelona/porta_species.csv (counts), databases/barcelona/porta_species_lidar_summary.csv (LiDAR 2021),
        BROT 2.0 (databases/traits/raw/BROT2_dat.csv, CC0, Tavsanoglu & Pausas 2018), 3TF (databases/TRY_DATABASE/
        Tree_Trait_Task_Force_BDD_1.3.txt), SylvCiT BDD (databases/TRY_DATABASE/BDD_SylvCiT_2025.xlsx, tolerances),
        notes/lit/species_measurements.csv (interception / cooling measurements from the literature).
Output: databases/traits/porta_trait_table.csv
Genus-level gap filling is NOT done here: it is a flagged modelling step (methodology section 3).
"""
import re, pathlib, warnings, numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOP = 20
EXTRA = ["Styphnolobium japonicum"]          # named by the city as a replacement species
SYN = {"platanus x hispanica": "platanus x acerifolia", "sophora japonica": "styphnolobium japonicum",
       "pyrus calleriana": "pyrus calleryana"}


def norm(s):
    s = str(s).replace("×", "x").lower()
    s = re.sub(r"['\"\[].*|\bvar\..*|\bsubsp\..*|\bssp\..*", "", s).strip()
    s = " ".join(s.split()[:3] if " x " in s else s.split()[:2])
    return SYN.get(s, s)


porta = pd.read_csv(ROOT / "databases/barcelona/porta_species.csv", index_col=0)
sp = list(porta.index[:TOP]) + [e for e in EXTRA if norm(e) not in {norm(s) for s in porta.index[:TOP]}]
T = pd.DataFrame({"species": sp, "key": [norm(s) for s in sp]})
T["n_porta"] = [int(porta.trees.get(s, 0)) for s in sp]
T["share_porta"] = (T.n_porta / porta.trees.sum()).round(3)
src = {k: [] for k in T.key}

# LiDAR (Porta, 26 Sept 2021)
L = pd.read_csv(ROOT / "databases/barcelona/porta_species_lidar_summary.csv")
L["key"] = L.species.map(norm)
L = L[L.n >= 10].set_index("key")
for c in ("height_med", "crown_diam_med", "crown_base_med", "lai_proxy_med"):
    T["lidar_" + c] = T.key.map(L[c])
for k in T.key[T.key.isin(L.index)]:
    src[k].append("LiDAR ICGC 2021 (this study)")

# BROT 2.0
B = pd.read_csv(ROOT / "databases/traits/raw/BROT2_dat.csv", encoding="latin-1", low_memory=False)
B["key"] = B.Taxon.map(norm)
B = B[B.key.isin(T.key)]
num = {"SLA": "brot_SLA_mm2_mg", "LDMC": "brot_LDMC", "P50": "brot_P50_MPa", "RootDepth": "brot_root_depth",
       "Height": "brot_height_max_m", "StemDensity": "brot_wood_density_g_cm3", "LeafLifespan": "brot_leaf_lifespan_months"}
for trait, col in num.items():
    v = B[B.Trait == trait].assign(x=lambda d: pd.to_numeric(d.Data, errors="coerce")).groupby("key").x.median()
    T[col] = T.key.map(v).round(3)
for trait, col in {"LeafPhenology": "brot_leaf_phenology", "LeafArea": "brot_leaf_area_class"}.items():
    v = B[B.Trait == trait].groupby("key").Data.agg(lambda s: s.mode().iloc[0])
    T[col] = T.key.map(v)
for k in B.key.unique():
    src[k].append("BROT 2.0")

# 3TF (TRY-based)
F = pd.read_csv(ROOT / "databases/TRY_DATABASE/Tree_Trait_Task_Force_BDD_1.3.txt", sep=";", encoding="utf-8", encoding_errors="replace")
F["key"] = F.FinalName.map(norm)
F = F[F.key.isin(T.key)]
for trait in ("SLA", "LDMC", "WD", "Nmass"):
    T["3tf_" + trait] = T.key.map(F[F.TraitAcc == trait].groupby("key").StdValue.median()).round(3)
for k in F.key.unique():
    src[k].append("3TF v1.3")

# SylvCiT tolerances (0-5 scales as in the SylvCiT database)
S = pd.read_excel(ROOT / "databases/TRY_DATABASE/BDD_SylvCiT_2025.xlsx", sheet_name="BDD_SylvCiT")
S["key"] = S.vascanName.map(norm)
S = S[S.key.isin(T.key)].groupby("key")[["Drought_tol_fac", "Shade_tol_fac", "Flood_tol_fac"]].first()
for c in S.columns:
    T["sylvcit_" + c.replace("_fac", "")] = T.key.map(S[c])
for k in S.index:
    src[k].append("SylvCiT BDD 2025")

# literature measurements (runoff / heat)
M = pd.read_csv(ROOT / "notes/lit/species_measurements.csv")
M["key"] = M.species.map(norm)
for obj in ("runoff", "heat"):
    g = M[M.objective == obj].groupby("key").apply(lambda d: "; ".join(f"{m} = {v} ({s})" for m, v, s in zip(d.measure, d.value, d.source)))
    T[f"lit_{obj}"] = T.key.map(g)
for k in M.key[M.key.isin(T.key)].unique():
    src[k].append("literature (notes/lit/species_measurements.csv)")

T["sources"] = T.key.map(lambda k: "; ".join(dict.fromkeys(src[k])))
need = {"leaf habit": "brot_leaf_phenology", "interception value": "lit_runoff", "cooling value": "lit_heat",
        "drought vulnerability (P50)": "brot_P50_MPa", "LiDAR crown": "lidar_crown_diam_med"}
T["gaps"] = T.apply(lambda r: ", ".join(n for n, c in need.items() if pd.isna(r[c])), axis=1)
T.drop(columns="key").to_csv(ROOT / "databases/traits/porta_trait_table.csv", index=False)
print(T[["species", "n_porta", "lidar_height_med", "lidar_lai_proxy_med", "brot_leaf_phenology", "brot_P50_MPa",
         "3tf_SLA", "gaps"]].to_string(index=False))
