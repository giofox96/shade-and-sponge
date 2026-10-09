"""Candidate species for the palette: street-tree species already common in Barcelona (local evidence they suit the
climate), minus exclusions, plus the LiDAR tiles needed to measure their crowns outside Porta.
Inputs: databases/barcelona/arbrat_viari.csv (Open Data BCN, CC BY 4.0), databases/barcelona/porta_species_lidar_summary.csv
Outputs: databases/barcelona/species_shortlist.csv, databases/barcelona/lidar_tiles_species.csv"""
import pathlib, re, numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
MIN_CITY = 500        # ASSUMPTION: >= 500 street trees in the city = established in Barcelona's climate (35 species)
TARGET = 40           # LiDAR-measured trees wanted per species (Porta summary already gives n >= 30 for some)
EDGE = 12.0           # trees closer than this to a tile edge are skipped (crowns cut by the tile border)
PALMS = ("Washingtonia", "Phoenix", "Chamaerops", "Trachycarpus", "Syagrus", "Butia", "Livistona", "Archontophoenix",
         "Brahea", "Jubaea")                                   # design choice: palms give little crown shade
# (palms are inventoried as PALMERA VIARI, so the ARBRE VIARI filter below already leaves them out; kept as a guard)
LEGAL_INVASIVE = ("Ailanthus altissima", "Acacia dealbata", "Acacia melanoxylon", "Myoporum laetum")
# Spanish catalogue of invasive alien species: tree taxa applying in Catalonia (MITECO table CEEEI, 21 Oct 2025)
INVASIVE_REPORTED = {
    "Robinia pseudoacacia": "riparian invasion in Spain (Cabra-Rivas, Castro-Díez & Saldaña 2015, Ecosistemas 24(1):18-28)",
    "Ulmus pumila": "riparian invasion in Spain (Cabra-Rivas, Castro-Díez & Saldaña 2015, Ecosistemas 24(1):18-28)",
    "Ligustrum lucidum": "global review of its invasion (Fernandez et al. 2020, Bot. Rev. 86:93-118)",
}                                                              # not legally listed: kept, flagged


def norm(name):
    """Species without cultivar, trade mark, variety or form: "Gleditsia triacanthos f. inermis" -> "Gleditsia triacanthos"."""
    return re.sub(r"\s*'[^']*'|\s+\S*®|\s+(var|f|subsp)\.\s+\S+", "", name).strip()


if __name__ == "__main__":
    t = pd.read_csv(DB / "arbrat_viari.csv", usecols=["codi", "x_etrs89", "y_etrs89", "cat_nom_cientific", "tipus_element", "nom_barri"])
    t = t[(t.tipus_element == "ARBRE VIARI") & t.cat_nom_cientific.notna()].copy()
    t["sp"] = t.cat_nom_cientific.map(norm)
    t["tile"] = (t.x_etrs89 // 1000).astype(int).astype(str) + (t.y_etrs89 // 1000 % 1000).astype(int).map("{:03d}".format)
    ex, ey = t.x_etrs89 % 1000, t.y_etrs89 % 1000
    t["inner"] = (ex > EDGE) & (ex < 1000 - EDGE) & (ey > EDGE) & (ey < 1000 - EDGE)

    c = t.sp.value_counts()
    lid = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species").n
    s = pd.DataFrame({"n_city": c, "n_porta": t[t.nom_barri.str.lower() == "porta"].sp.value_counts()}).fillna(0).astype(int)
    s = s[s.n_city >= MIN_CITY]
    s["lidar_porta_n"] = lid.reindex(s.index).fillna(0).astype(int)
    s["status"], s["reason"] = "candidate", ""
    for sp in s.index:
        if sp.startswith("Platanus"):
            s.loc[sp, ["status", "reason"]] = ["excluded", "being replaced (tree master plan)"]
        elif sp.startswith(PALMS):
            s.loc[sp, ["status", "reason"]] = ["excluded", "palm: little crown shade (design choice)"]
        elif sp in LEGAL_INVASIVE:
            s.loc[sp, ["status", "reason"]] = ["excluded", "Spanish invasive species catalogue (MITECO, Oct 2025)"]
    s["flag"] = [INVASIVE_REPORTED.get(sp, "") for sp in s.index]
    s["need"] = np.where(s.status == "candidate", (TARGET - s.lidar_porta_n).clip(0), 0)

    # greedy tile choice: add the tile that covers the most still-needed trees until every candidate has TARGET trees
    cand = t[t.inner & t.sp.isin(s.index[s.need > 0])]
    counts = cand.groupby(["tile", "sp"]).size().unstack(fill_value=0)
    need = s.need[s.need > 0].copy()
    tiles = []
    while need.sum() > 0 and len(counts):
        gain = counts[need.index].clip(upper=need, axis=1).sum(axis=1)
        best = gain.idxmax()
        if gain[best] == 0:
            break
        got = counts.loc[best, need.index].clip(upper=need)
        tiles.append(dict(tile=best, new_trees=int(got.sum()), species_covered=int((got > 0).sum())))
        need -= got
        counts = counts.drop(best)
    s["still_missing"] = need.reindex(s.index).fillna(0).astype(int)
    s.index.name = "species"
    s.sort_values("n_city", ascending=False).to_csv(DB / "species_shortlist.csv")
    pd.DataFrame(tiles).to_csv(DB / "lidar_tiles_species.csv", index=False)
    print(s.status.value_counts().to_dict(), "| tiles needed:", len(tiles), "| still missing:", int(need.sum()))
    print(s.sort_values("n_city", ascending=False)[["n_city", "n_porta", "lidar_porta_n", "status", "need", "still_missing"]].to_string())
    print(pd.DataFrame(tiles).to_string(index=False))
