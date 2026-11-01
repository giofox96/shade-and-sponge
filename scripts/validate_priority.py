"""First validation of the replacement-priority proxy (shade_sponge/health.py) on Porta: forward test between two
Open Data BCN street-tree snapshots ('arbrat-viari', quarterly files).
The run's inventory (arbrat_viari.csv, Oct 2026) is the newest, so the proxy is recomputed on the 2021 Q3 snapshot
(the LiDAR was flown 26 Sept 2021): crowns re-segmented with the 2021 positions as seeds, same CHM, points and rules as
scripts/bcn_lidar_porta.py step 3. A 2021 tree whose codi is missing in 2026 Q3 counts as removed.
Inputs:  databases/barcelona/raw/arbrat_snapshots/<YYYY_QT>/<YYYY_QT>_OD_Arbrat_Viari_BCN.csv (gitignored)
         databases/barcelona/raw/lidar/porta_{chm,dtm}_05m.tif, porta_points.npz (from bcn_lidar_porta.py)
Output:  databases/barcelona/porta_priority_validation.csv
Run with the project env:  python scripts/validate_priority.py"""
import pathlib, numpy as np, pandas as pd, rasterio
from scipy import ndimage
from scipy.stats import mannwhitneyu
from scipy.spatial import cKDTree
from skimage.segmentation import watershed
from shade_sponge import health, site

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
SNAP = DB / "raw/arbrat_snapshots"
OLD, NEW = "2021_3T", "2026_3T"
LIDAR_DATE = "2021-09-26"   # ICGC flight; ISO date strings compare correctly as text
GROUND, VEG = (2, 8, 75), (3, 4, 5)


def porta(q):
    t = pd.read_csv(SNAP / q / f"{q}_OD_Arbrat_Viari_BCN.csv")
    t = t.rename(columns={"nom_cientific": "cat_nom_cientific"})   # older snapshots drop the "cat_" prefix
    return t[(t.tipus_element == "ARBRE VIARI") & (t.nom_barri.str.lower() == "porta")].reset_index(drop=True)


def crowns(t):
    """Seeded watershed crowns as bcn_lidar_porta.py step 3 (kept in step by hand: same thresholds)."""
    with rasterio.open(DB / "raw/lidar/porta_chm_05m.tif") as r:
        chm, T = r.read(1), r.transform
    with rasterio.open(DB / "raw/lidar/porta_dtm_05m.tif") as r:
        dtm = r.read(1)
    H, W = chm.shape
    res, x0, y1 = T.a, T.c, T.f
    tc = ((t.x_etrs89 - x0) / res).astype(int).values
    tr = ((y1 - t.y_etrs89) / res).astype(int).values
    canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
    markers = np.zeros((H, W), "int32")
    markers[tr, tc] = np.arange(1, len(t) + 1)
    markers = ndimage.grey_dilation(markers, size=(3, 3))
    lab = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
    rr, cc = np.indices((H, W))
    f, has = lab.ravel(), lab.ravel() > 0
    far = np.zeros(W * H, bool)
    far[has] = np.hypot(rr.ravel()[has] - tr[f[has] - 1], cc.ravel()[has] - tc[f[has] - 1]) * res > 9.0
    lab.ravel()[far] = 0
    lab[~canopy] = 0
    ids = np.arange(1, len(t) + 1)
    area = ndimage.sum(np.ones_like(chm), lab, ids) * res ** 2
    hmax = np.where(area > 0, ndimage.maximum(chm, lab, ids), np.nan)
    d = np.load(DB / "raw/lidar/porta_points.npz")
    col = ((d["x"] - x0) / res).astype(int).clip(0, W - 1)
    row = ((y1 - d["y"]) / res).astype(int).clip(0, H - 1)
    pid = lab[row, col]
    s = pid > 0
    P = pd.DataFrame({"id": pid[s], "gnd": np.isin(d["c"][s], GROUND), "lab": d["c"][s] != 12})
    lp = P[P.lab].groupby("id")
    out = pd.DataFrame({"tree_id": t.codi, "sp": t.cat_nom_cientific.map(site.norm), "size_category": t.categoria_arbrat,
                        "crown_area_m2": area, "height_m": hmax,
                        "gap_fraction": (lp.gnd.sum() / lp.size()).reindex(ids).values,
                        "n_points": P.groupby("id").size().reindex(ids).fillna(0).values})
    out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                            ["no_crown_detected", "few_points", "low_tree"], "ok")
    return out


def auc(score, removed):
    """P(removed tree scores higher than a kept one), ties count half (Mann-Whitney U / n1 n0)."""
    return mannwhitneyu(score[removed], score[~removed]).statistic / (removed.sum() * (~removed).sum())


if __name__ == "__main__":
    old, new = porta(OLD), porta(NEW)
    cr = crowns(old)
    p = health.priority(cr).merge(old[["codi", "x_etrs89", "y_etrs89"]], left_on="tree_id", right_on="codi")
    p["is_plane"] = p.sp.str.startswith("Platanus")
    p["removed"] = ~p.tree_id.isin(new.codi)
    # removed id with a new id within 1 m in the later snapshot = replaced at the same pit
    fresh = new[~new.codi.isin(old.codi)]
    dist = cKDTree(fresh[["x_etrs89", "y_etrs89"]].to_numpy()).query(p[["x_etrs89", "y_etrs89"]].to_numpy())[0]
    p["replaced_1m"] = p.removed & (dist <= 1.0)
    # most replacements keep the codi and get a new planting date (e.g. Populus -> Fraxinus in the same pit)
    pl = p[["tree_id"]].merge(old[["codi", "data_plantacio"]], left_on="tree_id", right_on="codi").merge(
        new[["codi", "data_plantacio"]], on="codi", how="left", suffixes=("_old", "_new"))
    p["replanted"] = (pl.data_plantacio_new > LIDAR_DATE).to_numpy() & (pl.data_plantacio_new != pl.data_plantacio_old).to_numpy()
    p["gone"] = p.removed | p.replanted

    # check: re-segmented crowns vs the run's crowns (2026 seeds) for trees present in both
    run = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
    m = cr.merge(run[["tree_id", "crown_area_m2"]], on="tree_id", suffixes=("", "_run"))
    print(f"crown check, {len(m)} trees in both: r = {m.crown_area_m2.corr(m.crown_area_m2_run):.3f}, "
          f"median ratio {np.nanmedian(m.crown_area_m2 / m.crown_area_m2_run):.2f}")

    rows = []
    for outcome in ("removed", "replanted", "gone"):
        for group, g in (("all", p), ("planes", p[p.is_plane]), ("others", p[~p.is_plane])):
            r = g[outcome].to_numpy()
            for col in ("priority", "vigour_deficit", "age"):
                v = g[col].to_numpy()
                rows.append(dict(outcome=outcome, group=group, score=col, n=len(g), n_event=int(r.sum()),
                                 n_replaced_1m=int(g.replaced_1m.sum()),
                                 mean_event=v[r].mean(), mean_kept=v[~r].mean(),
                                 median_event=np.median(v[r]), median_kept=np.median(v[~r]), auc=auc(v, r)))
    res = pd.DataFrame(rows).round(3)
    res.insert(0, "snapshots", f"{OLD}->{NEW}")
    res.to_csv(DB / "porta_priority_validation.csv", index=False)
    print(f"{OLD}: {len(old)} Porta street trees; {NEW}: {len(new)}; removed {int(p.removed.sum())} "
          f"(planes {int(p[p.is_plane].removed.sum())}), of which a new id within 1 m: {int(p.replaced_1m.sum())}; "
          f"replanted (same codi, planting date after {LIDAR_DATE}) {int(p.replanted.sum())} "
          f"(planes {int(p[p.is_plane].replanted.sum())})")
    print("flags 2021 crowns:", p.flag.value_counts().to_dict(), "| removed by flag:", p[p.removed].flag.value_counts().to_dict())
    print(res.to_string(index=False))
