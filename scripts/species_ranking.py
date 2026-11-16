"""Species league table and "who replaces whom": the per-tree properties the method scores, for every species of the
Barcelona palette (30) and for the species the city removes most, on one isolated tree on open flat ground.

Per species, at equal trunk size (TERCERA medians of the city LiDAR pool, else SEGONA, as layout.palette 'barcelona'):
  summer shade  = sum over the design hours of shadow area × crown opacity in July (heat.py), m²·h per tree
  winter shade  = the same on 15 January, m²·h (a cost)
  storage       = s·LAI × storm-season leaf factor × crown area (runoff.py, season.py), litres per tree per storm
  survival      = share of the city's plantings of the species still standing, age-standardised (backtest_survival.py)
ASSUMPTION: no buildings, no neighbours, flat ground: this ranks what a species can give, not what it gives at a given
position (that is the tool's job). Balanced score = the method's balanced weights (0.50 summer, 0.25 winter, 0.25
storage) on min-max normalised values within the table. Survival is reported, not scored.
Who replaces whom: for each removed species, palette species of the same size class (2011 guide, layout.SIZE_CLASS) that
keep summer shade and storage (>= 100%) without adding winter shade (<= 100%), ranked by the balanced score (if none does:
the closest, by the worst of the three ratios); plus the
species the city actually planted most in its place (inventory_replacement_matrix.csv).

Run: python scripts/species_ranking.py
Outputs: databases/barcelona/species_ranking.csv, species_replaces.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from shade_sponge import heat, season, runoff  # noqa: E402
from shade_sponge.layout import palette_names, SIZE_CLASS, MIN_CLASS  # noqa: E402
from shade_sponge.site import DB, city_trees  # noqa: E402
from backtest_survival import ih_norm  # noqa: E402

LAT, LON = 41.39, 2.17          # Barcelona; the design suns differ by less than a degree across the city
N_OUT = 10                      # most-removed species to match
W = dict(summer=0.5, winter=0.25, storage=0.25)


def traits(pool, sp):
    for cls in ("TERCERA", "SEGONA"):
        g = pool[(pool.sp == sp) & (pool.size_category == cls)]
        if len(g) >= MIN_CLASS:
            return dict(trunk_class=cls, n_lidar=len(g), crown_diam_m=g.crown_diam_m.median(), height_m=g.height_m.median(),
                        crown_base_m=g.crown_base_m.median(), lai=g.lai.median())
    return None


def main():
    key = ih_norm()
    pool = city_trees()
    names = palette_names("barcelona")[0]
    m = pd.read_csv(DB / "inventory_replacement_matrix.csv")
    m = m[m.scope == "city"]
    by_key = {key(s): s for s in pool.sp.unique() if key(s)}
    out = [by_key[s] for s in m.groupby("species_out").n.sum().sort_values(ascending=False).index
           if s in by_key and traits(pool, by_key[s])][:N_OUT]
    surv = pd.read_csv(DB / "backtest_survival_species.csv").set_index("species")
    suns = {s: [heat.sun(LAT, LON, v["doy"], h) for h in v["hours_utc"]] for s, v in heat.SEASONS.items()}
    rows = []
    for sp in dict.fromkeys(names + out):
        t = traits(pool, sp)
        if t is None:
            continue
        r = dict(species=sp, palette=sp in names, removed_rank=out.index(sp) + 1 if sp in out else np.nan,
                 size_class=SIZE_CLASS.get(sp.replace("×", "x"), SIZE_CLASS.get(sp, "")), **t)
        for s, v in heat.SEASONS.items():
            op = float(heat.opacity([sp], [t["lai"]], v["month"])[0])
            r[f"{s}_m2h"] = sum(heat.shadow_xy_area(t["crown_diam_m"], t["height_m"], t["crown_base_m"], a, z)[2] * op
                                for a, z in suns[s])
        r["storage_l"] = runoff.P_["s_mm_per_lai"] * t["lai"] * float(season.storm_factor([sp])[0]) * np.pi * t["crown_diam_m"] ** 2 / 4
        k = key(sp)
        r["survival"] = surv.alive_std.get(k, np.nan) if surv.n.get(k, 0) >= 30 else np.nan
        r["survival_n"] = surv.n.get(k, 0)
        rows.append(r)
    d = pd.DataFrame(rows)
    nz = {c: (d[c] - d[c].min()) / (d[c].max() - d[c].min()) for c in ("summer_m2h", "winter_m2h", "storage_l")}
    d["score"] = W["summer"] * nz["summer_m2h"] + W["winter"] * (1 - nz["winter_m2h"]) + W["storage"] * nz["storage_l"]
    d = d.sort_values("score", ascending=False)
    d.round(3).to_csv(DB / "species_ranking.csv", index=False)

    p = d[d.palette].set_index("species")
    rep = []
    for x in out:
        X = d.set_index("species").loc[x]
        same = p[(p.size_class == X.size_class) | (X.size_class == "")].drop(index=x, errors="ignore")
        ret = pd.DataFrame(dict(summer=same.summer_m2h / X.summer_m2h, winter=same.winter_m2h / X.winter_m2h,
                                storage=same.storage_l / X.storage_l, score=same.score, survival=same.survival))
        ok = ret[(ret.summer >= 1) & (ret.storage >= 1) & (ret.winter <= 1)].sort_values("score", ascending=False)
        if ok.empty:                                    # nobody keeps everything: closest = best worst-case retention
            ok = ret.assign(worst=np.minimum(np.minimum(ret.summer, ret.storage), 1 / ret.winter)) \
                .sort_values("worst", ascending=False).drop(columns="worst")
        city = m[(m.species_out == key(x))].sort_values("n", ascending=False).iloc[0]
        cs = by_key.get(city.species_in, city.species_in)
        c = d.set_index("species").reindex([cs]).iloc[0]
        rep.append(dict(removed=x, size_class=X.size_class, n_removed=int(m[m.species_out == key(x)].n.sum()),
                        city_top=cs, city_top_share=city.share_of_out, city_summer=c.summer_m2h / X.summer_m2h,
                        city_winter=c.winter_m2h / X.winter_m2h, city_storage=c.storage_l / X.storage_l,
                        n_keep_all=int(((ret.summer >= 1) & (ret.storage >= 1) & (ret.winter <= 1)).sum()), **{f"best{i + 1}": s for i, s in enumerate(ok.index[:3])},
                        **{f"best{i + 1}_{c}": v for i, (_, o) in enumerate(ok.head(3).iterrows())
                           for c, v in (("summer", o.summer), ("winter", o.winter), ("storage", o.storage))}))
    pd.DataFrame(rep).round(3).to_csv(DB / "species_replaces.csv", index=False)
    print(d[["species", "size_class", "summer_m2h", "winter_m2h", "storage_l", "survival", "score"]].round(2).to_string(index=False))
    print(pd.DataFrame(rep).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
