"""Two untested assumptions of the register (notes/tutor_feedback_10nov.md §2, A4), Porta, thesis configuration
(city palette, --size=exact, --trunk=TERCERA, plane replacement R):
  hotspot capture distance (site.CAPTURE_M = 100 m): 50 / 100 / 200 m;
  crown clearance from façades (layout.fits, no margin): margin 0 / 1 / 2 m added to the crown radius.
For each value: the balanced optimised layout (summer 0.5, winter 0.25, runoff 0.25) and the city's observed practice
(S1b, 10 seeds, mean), evaluated as in python -m shade_sponge. Question: does the ranking hold?
Output: databases/barcelona/sensitivity_capture_margin.csv. Needs the Porta raw data (run on the OMEN)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from shade_sponge.site import load_site, DB
from shade_sponge import heat, runoff, layout

W = (0.5, 0.25, 0.25)
COLS = ["shade_summer_m2h", "shade_winter_m2h", "runoff_hot_m3", "runoff_m3", "canopy_pct"]


def run(capture_m=100.0, margin=0.0):
    site = load_site("porta", capture_m=capture_m)
    sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
    lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
    p = runoff.design_storm(2, 60)
    gone = layout.removed(site.trees, None)
    pal = layout.palette(site, "city", "TERCERA", gone)
    pos = site.trees[gone].reset_index(drop=True)
    fit = layout.fits(site, pos, pal, "exact", cap=pal.cap.values, margin=margin)
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    objs = {"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (layout.water_potential(site, pos, pal, p), 1)}
    norm = [sg * m / m.max() if m.max() > 0 else np.zeros_like(m, float) for m, sg in objs.values()]
    opt = layout.assign(sum(w * m for w, m in zip(W, norm)) + 1e-3 * sum(norm), pal.cap.values, fit)
    ev = lambda ch: layout.evaluate(site, layout.apply(site, pos, pal, ch), sun, lit, p)
    s0 = layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p)
    s1b = pd.DataFrame([ev(layout.s1a_layout(pal, pal.cap.values, fit, np.random.default_rng(200 + k), layout.s1b_mix()))
                        for k in range(10)])[COLS].mean()
    o = pd.Series(ev(opt))[COLS]
    row = dict(capture_m=capture_m, margin_m=margin, positions_fit_any_large=int((fit[:, pal.crown_diam_m.values > 7].any(1)).sum()))
    for k in COLS:
        row[f"opt_{k}"], row[f"s1b_{k}"], row[f"s0_{k}"] = o[k], s1b[k], s0[k]
    row["opt_summer_pct_today"] = 100 * o.shade_summer_m2h / s0["shade_summer_m2h"]
    row["s1b_summer_pct_today"] = 100 * s1b.shade_summer_m2h / s0["shade_summer_m2h"]
    row["opt_hot_vs_s1b_pct"] = 100 * (o.runoff_hot_m3 / s1b.runoff_hot_m3 - 1)
    print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in row.items() if "pct" in k or k in ("capture_m", "margin_m")}, flush=True)
    return row


rows = [run(capture_m=c) for c in (50.0, 100.0, 200.0)] + [run(margin=m) for m in (1.0, 2.0)]
pd.DataFrame(rows).round(2).to_csv(DB / "sensitivity_capture_margin.csv", index=False)
print("wrote", DB / "sensitivity_capture_margin.csv")
