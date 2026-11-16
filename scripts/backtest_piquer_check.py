"""Why does the method lose on C. Piquer? The back-test (scripts/backtest_works.py) has the method pick Citrus × aurantium
where the city planted Pyrus calleryana, and the full shade score then favours the city. This compares, for the three
Piquer groups, the optimiser's per-position estimate (layout.shade_potential: shadow area × share of sunlit open ground in a
square around the shadow centre) with the full raster score (heat.shade_m2h) of the same species on every position.
If the two disagree, the estimate, not the rule, makes the method lose.

Run on the PC (barri rasters): python scripts/backtest_piquer_check.py -> databases/barcelona/backtest_piquer_check.csv
"""
import copy
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from rasterio.features import rasterize
from shapely.geometry import MultiPoint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from shade_sponge import heat, layout  # noqa: E402
from shade_sponge.site import DB, load_site  # noqa: E402
from backtest_works import R_DOM, R_MATCH  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

GROUPS, SPECIES = (4466, 4504, 4506), ("Pyrus calleryana", "Citrus × aurantium", "Hibiscus syriacus")


def main():
    p = pd.read_csv(DB / "backtest_works_positions.csv")
    site = load_site("el-poble-sec")
    sun = heat.design_suns(site, "summer")
    lit = [heat.sunlit(site, *s) for s in sun]
    T = site.trees
    kd = cKDTree(T[["x", "y"]].values)
    rows = []
    for g in GROUPS:
        m = p[p.group == g].reset_index(drop=True)
        xy = m[["x", "y"]].values
        gone = np.isin(np.arange(len(T)), sorted({i for h in kd.query_ball_point(xy, R_MATCH) for i in h}))
        loc = copy.copy(site)
        loc.domain = rasterize([(MultiPoint(xy).buffer(R_DOM), 1)], out_shape=site.domain.shape, transform=site.transform,
                               fill=0).astype(bool)
        pal = layout.palette(site, "barcelona", "TERCERA", gone)
        pal = pal[pal.species.isin(SPECIES)].reset_index(drop=True)
        pos = pd.DataFrame(dict(tree_id=[f"w{i}" for i in range(len(m))], x=m.x, y=m.y))
        est = layout.shade_potential(loc, pos, pal, sun, lit, heat.SEASONS["summer"]["month"]).sum(axis=0)
        kept = T[~gone & (T.flag == "ok")]
        base = heat.shade_m2h(loc, kept, sun, lit, heat.SEASONS["summer"]["month"])
        for j, r in pal.iterrows():
            new = pos.assign(species=r.species, sp=r.species, crown_diam_m=r.crown_diam_m, height_m=r.height_m,
                             crown_base_m=r.crown_base_m, lai=r.lai)
            full = heat.shade_m2h(loc, pd.concat([kept, new], ignore_index=True), sun, lit, heat.SEASONS["summer"]["month"])
            rows.append(dict(group=g, n=len(m), species=r.species, crown_diam_m=r.crown_diam_m, height_m=r.height_m,
                             crown_base_m=r.crown_base_m, lai=r.lai, estimate_m2h=est[j], full_m2h=full - base))
            print(rows[-1])
    pd.DataFrame(rows).round(2).to_csv(DB / "backtest_piquer_check.csv", index=False)


if __name__ == "__main__":
    main()
