"""Check the tool's surface-water routing against RESCCUE flood depth in Porta (methodology §4, validation iii).

Run with the project env, after scripts/bcn_resccue_depth.py:  python scripts/compare_resccue_runoff.py
Question: do the cells where our routing concentrates water (upstream open area, shade_sponge/topo.py on DTM + buildings)
coincide with the cells RESCCUE floods? RESCCUE is a 1D/2D model with the sewer network; ours has no sewer and no
inflow from outside Porta, so this tests where water collects, not how much (no depth or volume comparison).
Metrics on open ground (Porta minus roofs), per RESCCUE scenario:
  - ROC AUC of log upstream area as a predictor of wet (depth > 0) and deep (depth >= DEPTH_DEEP) cells (0.5 = no skill)
  - area-matched hit rate: of the N cells with the largest upstream area (N = RESCCUE wet cells), the share that is wet,
    exactly and within TOL_M; lift = hit rate / wet share of open ground (what a random pick of N cells would get)
  - Spearman rank correlation of upstream area and depth on wet cells
  - overlap with the Resilience Atlas hotspots used by the tool (index >= 40) and with the ground that drains to them
Outputs: databases/barcelona/resccue_runoff_comparison.csv, notes/figures/resccue_vs_routing.png
"""
import pathlib, sys, numpy as np, pandas as pd, rasterio, matplotlib.pyplot as plt
from rasterio.warp import reproject, Resampling
from scipy import ndimage, stats
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from shade_sponge.site import load_site, RAW, DB  # noqa: E402

FIG = pathlib.Path(__file__).resolve().parents[1] / "notes/figures"
SCENARIOS = {"t10_actual": "T10 present", "t100_actual": "T100 present", "t10_futur": "T10 future", "t100_futur": "T100 future"}
DEPTH_DEEP = 0.15   # m, same reporting threshold as bcn_resccue_depth.py (not a hazard criterion). ASSUMPTION
TOL_M = 5.0         # m, positional tolerance: RESCCUE elements are ~44 m² (~7 m across), LiDAR DTM 0.5 m. ASSUMPTION


def depth_on(site, tag):
    """RESCCUE depth raster resampled (max) onto the site grid; robust to the < 1 m shift of the atlas-boundary fallback."""
    out = np.full(site.domain.shape, np.nan, "float32")
    with rasterio.open(RAW / f"porta_resccue_depth_{tag}.tif") as src:
        reproject(rasterio.band(src, 1), out, dst_transform=site.transform, dst_crs="EPSG:25831",
                  resampling=Resampling.max, dst_nodata=np.nan)
    return np.nan_to_num(out)


def auc(score, label):
    """ROC AUC via the Mann-Whitney U statistic (ties count half)."""
    r = stats.rankdata(score)
    n1 = label.sum()
    n0 = label.size - n1
    return float((r[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


site = load_site("porta")
m = site.domain & ~site.roof                              # open ground
score = np.log10(site.acc[m])
order = np.argsort(-site.acc[m], kind="stable")
rows, maps = [], {}
for tag, label in SCENARIOS.items():
    if not (RAW / f"porta_resccue_depth_{tag}.tif").exists():
        print(f"{label}: no depth raster, run scripts/bcn_resccue_depth.py first")
        continue
    d = depth_on(site, tag)
    wet, deep = d > 0, d >= DEPTH_DEEP
    near = ndimage.distance_transform_edt(~wet) * site.res <= TOL_M     # within TOL_M of a wet cell
    w = wet[m]
    n = int(w.sum())
    top = np.zeros(m.sum(), bool)
    top[order[:n]] = True
    hot_open = site.hot & m
    row = dict(scenario=label, open_ground_ha=m.sum() * site.res ** 2 / 1e4, wet_open_ha=n * site.res ** 2 / 1e4,
               wet_share=w.mean(), auc_wet=auc(score, w), auc_deep=auc(score, deep[m]),
               hit_rate=w[top].mean(), hit_rate_tol=near[m][top].mean(), lift=w[top].mean() / w.mean(),
               lift_tol=near[m][top].mean() / near[m].mean(),
               spearman_acc_depth_wet=stats.spearmanr(site.acc[m][w], d[m][w])[0],
               hotspot_cells_wet_share=wet[hot_open].mean() if hot_open.any() else np.nan,
               wet_in_hotspot_share=hot_open[wet & m].mean(),
               wet_draining_to_hotspot_share=site.to_hot[wet & m].mean())
    rows.append(row)
    maps[label] = (d, top)
    print(f"{label}: AUC wet {row['auc_wet']:.2f}, deep {row['auc_deep']:.2f}; area-matched hit rate {row['hit_rate']:.0%} "
          f"(random {row['wet_share']:.0%}), within {TOL_M:.0f} m {row['hit_rate_tol']:.0%}")

if not rows:
    sys.exit("no RESCCUE rasters found")
out = pd.DataFrame(rows).round(3)
out.to_csv(DB / "resccue_runoff_comparison.csv", index=False)
print(out.T.to_string())

# figure: T10 present (or the first scenario available) on the map, hit rate vs share of cells picked for all scenarios
label = "T10 present" if "T10 present" in maps else next(iter(maps))
d, top = maps[label]
H, W = site.domain.shape
img = np.full((H, W, 3), 1.0)
img[site.roof] = 0.85
model = np.zeros((H, W), bool)
model[np.where(m)[0][top], np.where(m)[1][top]] = True
img[(d > 0) & ~model] = (0.55, 0.75, 0.95)               # RESCCUE wet only
img[model & ~(d > 0)] = (0.95, 0.55, 0.35)               # routing only
img[model & (d > 0)] = (0.35, 0.2, 0.55)                 # both
img[~site.domain] = 1.0
fig, ax = plt.subplots(1, 2, figsize=(13, 6.2), constrained_layout=True, gridspec_kw=dict(width_ratios=[1.1, 1]))
ax[0].imshow(img, extent=(site.x0, site.x0 + W * site.res, site.y1 - H * site.res, site.y1))
ax[0].set_axis_off()
ax[0].set_title(f"{label}: RESCCUE wet cells vs the same area of highest upstream area")
for c, t in (((0.55, 0.75, 0.95), "RESCCUE wet only"), ((0.95, 0.55, 0.35), "routing only"), ((0.35, 0.2, 0.55), "both")):
    ax[0].plot([], [], "s", color=c, ms=9, label=t)
ax[0].legend(loc="lower left", frameon=False)
k = np.linspace(0.005, 0.5, 100)
for lab, (d, _) in maps.items():
    w = (d > 0)[m][order]
    ax[1].plot(100 * k, [100 * w[: int(x * w.size)].mean() for x in k], label=lab)
    ax[1].axhline(100 * w.mean(), ls=":", lw=0.8, color=ax[1].lines[-1].get_color())
ax[1].set_xlabel("Open ground picked, highest upstream area first (%)")
ax[1].set_ylabel("Picked cells that RESCCUE floods (%)")
ax[1].set_title("Hit rate (dotted: random pick)")
ax[1].legend(frameon=False)
fig.suptitle("Porta: surface-water routing (no sewer) vs RESCCUE 1D/2D flood depth\n"
             "Source: PDISBA'19-RESCCUE (Barcelona Regional / Ajuntament de Barcelona); routing: shade_sponge/topo.py")
fig.savefig(FIG / "resccue_vs_routing.png", dpi=150)
