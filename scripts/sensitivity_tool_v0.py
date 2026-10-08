"""Sensitivity of the winter-sun result of tool v0 (shade_sponge/README.md): leafless crown opacity, the January leaf
state of Tipuana and Jacaranda, and the winter design day. Each variant re-optimises three weight sets (summer-only,
balanced, winter-heavy) and scores them against 3 random palettes.
Outputs: databases/barcelona/tool_v0_sensitivity_raw.csv, tool_v0_sensitivity.csv"""
import numpy as np, pandas as pd
from shade_sponge.site import load_site, DB
from shade_sponge import heat, runoff, layout, season

VARIANTS = {
    "base": {},
    "op_bare_0.25": dict(op=0.25),                                   # low end of McPherson 1984 range
    "op_bare_0.54": dict(op=0.54),                                   # leafless London plane, Heisler (Thayer & Maeda 1985)
    "tipuana_bare_jan_feb": dict(phen={("Tipuana tipu", m): 0.0 for m in ("m01", "m02")}),   # 'briefly deciduous in winter'
    "jacaranda_half_jan_mar": dict(phen={("Jacaranda mimosifolia", m): 0.5 for m in ("m01", "m02", "m03")}),
    "winter_21dec": dict(doy=355, month=12),
    "winter_15feb": dict(doy=46, month=2),
}
WEIGHTS = {"summer_only": (1.0, 0.0, 0.0), "balanced": (0.5, 0.25, 0.25), "winter_heavy": (0.0, 0.5, 0.5)}

site = load_site("porta")
p = runoff.design_storm(2, 60)
pal = layout.palette(site)
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
fit = layout.fits(site, pos, pal)
water = layout.water_potential(site, pos, pal, p)
PHEN0, OP0, WIN0 = season.PHEN.copy(), heat.OP_BARE, dict(heat.SEASONS["winter"])
MONTHS = [f"m{i:02d}" for i in range(1, 13)]
PHEN0[MONTHS] = PHEN0[MONTHS].astype(float)
lit_cache, rows = {}, []
for v, cfg in VARIANTS.items():
    season.PHEN = PHEN0.copy()
    for (sp, m), val in cfg.get("phen", {}).items():
        season.PHEN.loc[sp, m] = val
    heat.OP_BARE = cfg.get("op", OP0)
    heat.SEASONS["winter"] = dict(WIN0, doy=cfg.get("doy", WIN0["doy"]), month=cfg.get("month", WIN0["month"]))
    sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
    lit = {s: lit_cache.setdefault((s, heat.SEASONS[s]["doy"]), [heat.sunlit(site, *x) for x in sun[s]]) for s in sun}
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    sw = layout.sweep({"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)}, pal.cap.values, fit)
    lays = {k: sw[w] for k, w in WEIGHTS.items()}
    lays.update({f"random_{k}": layout.random_layout(pal.cap.values, fit, np.random.default_rng(k)) for k in range(3)})
    for k, ch in lays.items():
        rows.append(dict(variant=v, layout=k, **layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p),
                         **{s.split()[0]: int((ch == j).sum()) for j, s in enumerate(pal.species)}))
    print(v, "done", flush=True)

raw = pd.DataFrame(rows)
raw.round(1).to_csv(DB / "tool_v0_sensitivity_raw.csv", index=False)
out = []
for v, d in raw.groupby("variant", sort=False):
    L = d.set_index("layout")
    rnd = d[d.layout.str.startswith("random")].mean(numeric_only=True)
    pct = lambda a, b: round(100 * (a / b - 1), 1)
    out.append(dict(variant=v,
                    free_gain_winter_pct=pct(L.loc["balanced", "shade_winter_m2h"], L.loc["summer_only", "shade_winter_m2h"]),
                    free_gain_summer_pct=pct(L.loc["balanced", "shade_summer_m2h"], L.loc["summer_only", "shade_summer_m2h"]),
                    bal_vs_random_summer_pct=pct(L.loc["balanced", "shade_summer_m2h"], rnd.shade_summer_m2h),
                    bal_vs_random_winter_pct=pct(L.loc["balanced", "shade_winter_m2h"], rnd.shade_winter_m2h),
                    heavy_vs_bal_winter_pct=pct(L.loc["winter_heavy", "shade_winter_m2h"], L.loc["balanced", "shade_winter_m2h"]),
                    heavy_vs_bal_summer_pct=pct(L.loc["winter_heavy", "shade_summer_m2h"], L.loc["balanced", "shade_summer_m2h"]),
                    tipuana_summer_only=int(L.loc["summer_only", "Tipuana"]), tipuana_balanced=int(L.loc["balanced", "Tipuana"]),
                    jacaranda_summer_only=int(L.loc["summer_only", "Jacaranda"]), jacaranda_balanced=int(L.loc["balanced", "Jacaranda"])))
out = pd.DataFrame(out)
out.to_csv(DB / "tool_v0_sensitivity.csv", index=False)
print(out.to_string(index=False))
