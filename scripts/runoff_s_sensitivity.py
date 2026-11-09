"""Sensitivity of Porta runoff to the canopy storage coefficient s (mm per unit LAI), layouts fixed (no re-optimisation).
Layouts are rebuilt as in `python -m shade_sponge porta --size=exact --trunk=TERCERA` (city palette): S0_current,
S1a (city mix, mean of its 10 seeds) and every S4 sweep layout. s values (methodology §4b): 1.75 calibrated on
Anys & Weiler (2024); 0.86 Xiao & McPherson (2016) mean surface storage, lower bound; 0.83 Quercus ilex (Hassan et al. 2017).
Storms: PDISBA T = 2 and 10 yr, 60 min. basis = leafon (runoff.event, LiDAR full leaf) or seasonal (storm-month weighted,
the tool's main runoff columns).
Usage: python scripts/runoff_s_sensitivity.py -> databases/barcelona/runoff_s_sensitivity_porta.csv"""
import numpy as np, pandas as pd
from shade_sponge.site import load_site, DB
from shade_sponge import heat, runoff, layout, season

site = load_site("porta")
sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
p2 = runoff.design_storm(2, 60)
pal = layout.palette(site, "city", "TERCERA")
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
fit = layout.fits(site, pos, pal, "exact", cap=pal.cap.values)
pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
objs = {"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (layout.water_potential(site, pos, pal, p2), 1)}
trees = {"S0_current": [site.trees[site.trees.flag == "ok"]]}   # each scenario = list of tree tables, results averaged
trees["S1a_city_mean"] = [layout.apply(site, pos, pal, layout.s1a_layout(pal, pal.cap.values, fit, np.random.default_rng(100 + k)))
                          for k in range(10)]
for w, ch in layout.sweep(objs, pal.cap.values, fit).items():
    trees["S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w)] = [layout.apply(site, pos, pal, ch)]

rows = []
for s in (1.75, 0.86, 0.83):
    runoff.P_["s_mm_per_lai"] = s
    for T in (2, 10):
        p = runoff.design_storm(T, 60)
        for sc, ts in trees.items():
            for basis, f in (("leafon", runoff.event), ("seasonal", season.runoff_seasonal)):
                r = pd.DataFrame([f(site, t, p) for t in ts]).mean()
                rows.append(dict(s=s, storm=f"T{T}_60min", basis=basis, scenario=sc, **r.round(1)))
out = pd.DataFrame(rows)
out.to_csv(DB / "runoff_s_sensitivity_porta.csv", index=False)

# self-check: s = 1.75, T2 reproduces the tool's summary (seasonal = main columns, leafon = *_leafon)
ref = pd.read_csv(DB / "tool_v0_summary_sizeexact_trunkTERCERA.csv").set_index("scenario")
ref.loc["S1a_city_mean"] = ref[ref.index.str.startswith("S1a_city")].mean(numeric_only=True)
chk = out[(out.s == 1.75) & (out.storm == "T2_60min")]
for basis, suf in (("seasonal", ""), ("leafon", "_leafon")):
    c = chk[chk.basis == basis].set_index("scenario")
    for k in ("runoff_m3", "runoff_hot_m3", "interception_m3"):
        d = (c[k] - ref.loc[c.index, k + suf]).abs().max()
        print(f"check {basis} {k}: max |diff| vs summary = {d:.2f} m³")
        assert d < 1.0, "mismatch with the tool summary"
