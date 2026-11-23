"""Co-benefits reported per scenario, NOT optimised (notes/cobenefits_plan.md, decided 3 Nov; resumed 23 Nov).

Three indicators for every layout the tool already produced, each as a share of today (S0 = 100) where that makes sense:
- diversity: effective number of species exp(Shannon H) (as SylvCiT, Nicol et al. 2026), largest species and genus share,
  over the decision positions only (the planes or the replaced trees);
- pollen: allergenic load = sum over trees of ap * pe * ppp * S * H, the numerator of the IUGZA index of Cariñanos,
  Casares-Porcel & Quesada-Rubio 2014 (Landsc. Urban Plan. 123:134-144, Table 1-2; species values in
  databases/traits/allergen_*.csv). S = crown projection area (pi CD^2 / 4), H = height on the paper's simplified scale
  (2, 6, 10, 14, 18 m: nearest class). The paper divides by 378 * park area; on a fixed set of positions that constant
  cancels in the ratio to S0, so only the ratio is reported. Species without a score count 0 (`pollen_load`, lower
  bound) or 4 * 3 * 3 = 36, the top of each Table 1 scale (`pollen_max`, upper bound; ASSUMPTION, more cautious than the paper's
  observed maximum of 27); the crown-area share with a score
  is `pollen_coverage_pct`;
- carbon: above-ground biomass from LiDAR height and crown diameter, AGB [kg] = a * (H * CD)^b, Jucker et al. 2017
  (Global Change Biology 23:177-190, doi:10.1111/gcb.13388, "Allometric equations for integrating remote sensing imagery into forest monitoring
  programmes", Eq. 7): angiosperms a = 0.016, b = 2.013; gymnosperms a = 0.109, b = 1.790. The exp(sigma^2/2)
  bias factor is left out (ASSUMPTION: it is near-constant, so ratios to S0 hold; absolute tonnes are a lower bound).
  Carbon = 0.5 * AGB (carbon fraction as in SylvCiT, Nicol et al. 2026). Fitted on forest trees: open-grown urban crowns
  are wider for the same stem, so absolute values are indicative (ASSUMPTION); the comparison between scenarios is the result.

Replacement crowns are the species' city-wide crowns at equal trunk class (TERCERA), today's trees are measured: the
carbon and pollen ratios therefore compare the current stock with the replacements once they reach that size, the same
basis as the shade and runoff results.

Inputs: exchange/to_gh/layouts_tool_v0<tag>_<date>.csv (Porta; S1b_obs_0 is exported from 23 Nov on) and
databases/barcelona/backtest_works_guide_capsmall_positions.csv (26 real replacement groups; heights = crown diameter x
the species' median H/CD in lidar_species_trees.csv, ASSUMPTION).
Run from the repo root: python scripts/cobenefits.py [layouts.csv]
Outputs: databases/barcelona/cobenefits_species.csv, cobenefits_porta.csv, cobenefits_backtest.csv
"""
import sys, pathlib, numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, TR = ROOT / "databases/barcelona", ROOT / "databases/traits"
GYMNO = ("Pinus", "Cupressus", "Ginkgo", "Cedrus", "Abies", "Picea", "Taxodium", "Sequoia", "Thuja")
H_CLASSES = np.array([2, 6, 10, 14, 18])
ALIAS = {"Platanus × acerifolia": "Platanus hispanica", "Citrus × aurantium": "Citrus aurantium",
         "Ginkgo biloba": "Ginkgo biloba (male)"}          # sex unknown in the inventory: male = worst case (ASSUMPTION)


def allergen_table():
    """Species scores, first source wins. Genus fallback only when the genus has one value in the sources ('genus')."""
    t = pd.concat([pd.read_csv(f).assign(source=f.stem) for f in sorted(TR.glob("allergen_*.csv"))], ignore_index=True)
    t["genus"] = t.taxon.str.split().str[0]
    return t.drop_duplicates("taxon")


def score(species, t):
    name = ALIAS.get(species, species)
    hit = t[t.taxon == name]
    if len(hit):
        return hit.iloc[0][["ap", "pe", "ppp"]].astype(float).tolist() + ["species", hit.iloc[0].source]
    g = t[t.genus == name.split()[0]]
    if len(g) and len(g[["ap", "pe", "ppp"]].drop_duplicates()) == 1:   # one value for the genus (incl. "spp." rows)
        return g.iloc[0][["ap", "pe", "ppp"]].astype(float).tolist() + ["genus", g.iloc[0].source]
    return [np.nan] * 3 + ["none", ""]


def species_table(names):
    t = allergen_table()
    rows = [[s, *score(s, t), s.split()[0] in GYMNO] for s in sorted(set(names) - {"none"})]
    return pd.DataFrame(rows, columns=["species", "ap", "pe", "ppp", "allergen_match", "allergen_source", "gymnosperm"])


def indicators(sp, cd, h, spt):
    """Per-layout indicators for arrays of species, crown diameter [m] and height [m]."""
    m = spt.set_index("species").reindex(sp)
    area = np.pi * cd ** 2 / 4
    hcls = H_CLASSES[np.abs(np.asarray(h)[:, None] - H_CLASSES[None]).argmin(1)]
    w = (m.ap * m.pe * m.ppp).values
    pollen = np.nansum(w * area * hcls)
    pollen_max = np.sum(np.where(np.isnan(w), 36, w) * area * hcls)   # unscored species at the top of each scale, 4 * 3 * 3
    a, b = np.where(m.gymnosperm.fillna(False).values, 0.109, 0.016), np.where(m.gymnosperm.fillna(False).values, 1.790, 2.013)
    carbon_t = 0.5 * np.nansum(a * (h * cd) ** b) / 1000
    p = pd.Series(sp).value_counts(normalize=True)
    g = pd.Series(sp).str.split().str[0].value_counts(normalize=True)
    return dict(n=len(sp), eff_species=float(np.exp(-(p * np.log(p)).sum())), max_species_pct=100 * p.iloc[0],
                max_species=p.index[0], max_genus_pct=100 * g.iloc[0], pollen_load=pollen, pollen_max=pollen_max,
                pollen_coverage_pct=100 * area[~np.isnan(w)].sum() / area.sum(), carbon_t=carbon_t)


def relative(df, ref):
    for k in ("pollen_load", "pollen_max", "carbon_t"):
        df[f"{k}_pct_S0"] = 100 * df[k] / df.loc[ref, k]
    return df


def porta(f, spt):
    lay = pd.read_csv(f)
    out = pd.DataFrame({sc: indicators(g.species.values, g.crown_diam_m.values, g.height_m.values, spt)
                        for sc, g in lay.groupby("scenario", sort=False)}).T
    out = relative(out, "S0_current")
    out.index.name = "scenario"
    return out


def backtest(spt):
    p = pd.read_csv(DB / "backtest_works_guide_capsmall_positions.csv")
    tr = pd.read_csv(DB / "lidar_species_trees.csv").query("flag == 'ok'")
    ratio = (tr.height_m / tr.crown_diam_m).groupby(tr.species).median()
    rows = {}
    for k in ("before", "city", "method_bal", "method_sum"):
        sp, cd = p[f"sp_{k}"].values, p[f"crown_{k}"].values
        h = cd * ratio.reindex(sp).fillna(ratio.median()).values
        rows[k] = indicators(sp, cd, h, spt)
    out = relative(pd.DataFrame(rows).T, "before")
    out.index.name = "layout"
    return out


if __name__ == "__main__":
    f = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else \
        sorted((ROOT / "exchange/to_gh").glob("layouts_tool_v0_barcelona_sizeexact_trunkTERCERA_*.csv"))[-1]
    names = set(pd.read_csv(f).species)
    bt = pd.read_csv(DB / "backtest_works_guide_capsmall_positions.csv")
    for k in ("before", "city", "method_bal", "method_sum"):
        names |= set(bt[f"sp_{k}"])
    spt = species_table(names)
    spt.to_csv(DB / "cobenefits_species.csv", index=False)
    print(spt.allergen_match.value_counts().to_string(), "\nno score:", ", ".join(spt[spt.allergen_match == "none"].species))
    po = porta(f, spt)
    po.round(2).to_csv(DB / "cobenefits_porta.csv")
    print(f"\nPorta ({f.name})\n", po.round(1).to_string())
    b = backtest(spt)
    b.round(2).to_csv(DB / "cobenefits_backtest.csv")
    print("\nBack-test, 26 groups\n", b.round(1).to_string())
