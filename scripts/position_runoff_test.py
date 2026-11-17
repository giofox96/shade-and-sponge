"""Does a tree's position change runoff? (tutor feedback F6 / A2, user request 17 Nov)
The same tree (Celtis australis, city LiDAR medians: crown, LAI) is placed alone at every Porta street-tree position,
with no other street tree (park/private canopy kept), on the tool's design storm (PDISBA T = 2 yr, 60 min), leaf-on.
For each position: what lies under the crown (roof / open ground / ground draining to a flood hotspot within
site.CAPTURE_M), the canopy storage, and the drop in total runoff and in hotspot runoff (m³) against no tree there.
Same model as runoff.event (bucket min(P, s·LAI), then SCS-CN), computed only under the crown.
Output: databases/barcelona/position_runoff_test.csv (+ summary printed). Needs the Porta site bundle (OMEN)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from shade_sponge.site import load_site, species_lidar, rc, DB
from shade_sponge import runoff

SPECIES = "Celtis australis"     # the city's most planted plane replacement (notes/tree_master_plan.md)
N = 100                          # trees to place in the "where to put N trees" comparison

site = load_site("porta")
sp = species_lidar("species_lidar_summary.csv").loc[SPECIES]
d, lai, s = float(sp.crown_diam_med), float(sp.lai_proxy_med), runoff.P_["s_mm_per_lai"]
p = runoff.design_storm(2, 60)
S0 = runoff.storage(site, site.trees.iloc[:0])          # no street trees: background canopy only
q0 = runoff.scs(np.clip(p - S0, 0, None), site.cn)
a = site.res ** 2 / 1000                                               # mm·m² -> m³

R = int(np.ceil(d / 2 / site.res)) + 1
di, dj = np.mgrid[-R:R + 1, -R:R + 1]
disk = np.hypot(di, dj) * site.res <= d / 2
di, dj = di[disk], dj[disk]
rows = []
r_, c_ = rc(site, site.trees.x.values, site.trees.y.values)
for i, (r, c) in enumerate(zip(r_, c_)):
    rr, cc = r + di, c + dj
    ok = (rr >= 0) & (rr < site.domain.shape[0]) & (cc >= 0) & (cc < site.domain.shape[1])
    rr, cc = rr[ok], cc[ok]
    dom, roof, hot = site.domain[rr, cc], site.roof[rr, cc], site.to_hot[rr, cc]
    S1 = np.where(roof, 0, np.maximum(S0[rr, cc], s * lai))           # largest storage wins, roofs unchanged
    dq = (q0[rr, cc] - runoff.scs(np.clip(p - S1, 0, None), site.cn[rr, cc])) * dom
    n = max(dom.sum(), 1)
    rows.append(dict(tree=i, x=site.trees.x.iat[i], y=site.trees.y.iat[i], roof_pct=100 * (roof & dom).sum() / n, hot_pct=100 * (hot & ~roof & dom).sum() / n,
                     drop_total_m3=float(dq.sum() * a), drop_hot_m3=float((dq * (hot & ~roof)).sum() * a)))
t = pd.DataFrame(rows)
t.to_csv(DB / "position_runoff_test.csv", index=False, float_format="%.4f")

print(f"{SPECIES}: crown {d:.2f} m, LAI {lai:.2f}, storage {s * lai:.2f} mm; storm {p:.1f} mm; {len(t)} positions")
print(t[["drop_total_m3", "drop_hot_m3", "roof_pct", "hot_pct"]].describe().round(3).to_string())
print(f"positions with no hotspot gain: {(t.drop_hot_m3 < 1e-6).mean():.1%}")
best = t.drop_hot_m3.nlargest(N).sum()
rand = np.mean([t.drop_hot_m3.sample(N, random_state=k).sum() for k in range(200)])
print(f"{N} trees, hotspot runoff drop: best positions {best:.2f} m³, random positions {rand:.2f} m³ (x{best / rand:.1f}), "
      f"total drop best-{N}-for-hotspot {t.loc[t.drop_hot_m3.nlargest(N).index, 'drop_total_m3'].sum():.2f} m³ "
      f"vs random {np.mean([t.drop_total_m3.sample(N, random_state=k).sum() for k in range(200)]):.2f} m³")
ex = {"over a roof": t.roof_pct.idxmax(),
      "street, not draining to a hotspot": t[(t.roof_pct == 0) & (t.hot_pct == 0)].drop_total_m3.idxmax(),
      "street, upstream of a hotspot": t.drop_hot_m3.idxmax()}
print(t.loc[list(ex.values())].assign(case=list(ex)).round(3).to_string())
