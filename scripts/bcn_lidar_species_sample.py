"""City-wide LiDAR sample of one street-tree species (issue #42): crown, height, crown base, LAI proxy.

Same method as scripts/bcn_lidar_porta.py: 0.5 m DTM (min of ground points, nearest-filled, median 5) and CHM, crowns by
watershed seeded at ALL inventory trees in the crop (neighbours compete for canopy), 9 m cap from the seed, crown base =
10th percentile of vegetation heights > 1.5 m, gap fraction = ground / labelled points, LAI proxy = -ln(gap) / k (k = 0.5).

Usage (project env, see CLAUDE.md):
  python scripts/bcn_lidar_species_sample.py --select-only     # step 1: counts + tiles to download (no LiDAR needed)
  python scripts/bcn_lidar_species_sample.py                   # step 2: after the tiles are in databases/barcelona/raw/lidar/
Options: --species "Styphnolobium japonicum" --min-trees 30 --min-streets 5 --max-tiles 6
Inputs:  databases/barcelona/arbrat_viari.csv (gitignored; open data 'arbrat-viari')
         databases/barcelona/raw/lidar/lidar_<ID1K>.laz (ICGC Territorial LiDAR v3.1, flown 26 Sept 2021; URL printed by step 1)
Outputs: databases/barcelona/<genus>_lidar_sample.csv   per tree (columns of porta_trees_lidar.csv + nom_barri, nn_dist_m, merge_flag)
         databases/barcelona/<genus>_lidar_summary.csv  medians and IQR: all ok trees, without merge_flag, per size class
ASSUMPTIONS: a tree is used only if it is >= 12 m from its tile edge (9 m crown cap + 3 m), so one tile per tree is enough;
merge_flag = crown radius > 0.6 x distance to the nearest inventory tree (possible merged crowns).
"""
import argparse, pathlib, numpy as np, pandas as pd, laspy
from scipy import ndimage
from skimage.segmentation import watershed

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES, BUF, EDGE, CAP, K = 0.5, 15.0, 12.0, 9.0, 0.5   # cell (m), crop buffer (m), tile-edge margin (m), crown cap (m), Beer-Lambert k
GROUND, VEG = (2, 8, 75), (3, 4, 5)                 # as bcn_lidar_porta.py; class 12 = overlap, used only in gap fraction
URL = ("https://datacloud.icgc.cat/datacloud/lidar-territorial/laz_unzip/full10km{b}/"
       "lidar-territorial-v3r1-full1km{t}-2021-2023.laz")

ap = argparse.ArgumentParser()
ap.add_argument("--species", default="Styphnolobium japonicum")
ap.add_argument("--min-trees", type=int, default=30)
ap.add_argument("--min-streets", type=int, default=5)
ap.add_argument("--max-tiles", type=int, default=6)
ap.add_argument("--select-only", action="store_true")
ap.add_argument("--inventory", default=str(ROOT / "databases/barcelona/arbrat_viari.csv"))
ap.add_argument("--lidar-dir", default=str(ROOT / "databases/barcelona/raw/lidar"))
ap.add_argument("--out-dir", default=str(ROOT / "databases/barcelona"))
a = ap.parse_args()
LID, OUT = pathlib.Path(a.lidar_dir), pathlib.Path(a.out_dir)
tag = a.species.split()[0].lower()

# ---- 1. sample selection
inv = pd.read_csv(a.inventory)
inv = inv[inv.tipus_element == "ARBRE VIARI"].reset_index(drop=True)
inv["street"] = inv.adreca.str.replace(r",.*", "", regex=True)
sp_names = {a.species, "Sophora japonica"} if a.species == "Styphnolobium japonicum" else {a.species}
spc = inv[inv.cat_nom_cientific.str.replace(r"\s*'.*", "", regex=True).isin(sp_names)].copy()
spc["tile"] = ((spc.x_etrs89 // 1000).astype(int).astype(str)                 # ID1K = x km + last 3 digits of y km,
               + ((spc.y_etrs89 // 1000).astype(int) % 1000).astype(str).str.zfill(3))   # e.g. 430586 (Porta TILES)
fx, fy = spc.x_etrs89 % 1000, spc.y_etrs89 % 1000
spc["interior"] = (fx >= EDGE) & (fx <= 1000 - EDGE) & (fy >= EDGE) & (fy <= 1000 - EDGE)
print(f"{a.species}: {len(spc)} street trees city-wide ({spc.interior.sum()} >= {EDGE:.0f} m from a tile edge)")
print("by size class:", spc.categoria_arbrat.value_counts().to_dict())
print("top neighbourhoods:", spc.nom_barri.value_counts().head(10).to_dict())
print("top streets:", spc.street.value_counts().head(10).to_dict())
cand = spc[spc.interior]
tiles, chosen = [], cand.iloc[0:0]
for t, _ in cand.tile.value_counts().items():                     # greedy: most trees per tile first
    if len(tiles) >= a.max_tiles or (len(chosen) >= a.min_trees and chosen.street.nunique() >= a.min_streets):
        break
    tiles.append(t)
    chosen = cand[cand.tile.isin(tiles)]
print(f"\nselected {len(tiles)} tiles -> {len(chosen)} trees on {chosen.street.nunique()} streets in "
      f"{chosen.nom_barri.nunique()} neighbourhoods; size classes {chosen.categoria_arbrat.value_counts().to_dict()}")
for t in tiles:
    b = f"{int(t[:3]) // 10}{int(t[3:]) // 10}"                     # 10 km block, as in the Porta URL (430586 -> 4358)
    have = (LID / f"lidar_{t}.laz").exists()
    print(f"  {t}: {(chosen.tile == t).sum():3d} trees  {'present' if have else 'MISSING'}  save as lidar_{t}.laz  <- "
          + URL.format(b=b, t=t))
if a.select_only:
    raise SystemExit
missing = [t for t in tiles if not (LID / f"lidar_{t}.laz").exists()]
if missing:
    raise SystemExit(f"download first: {missing}")

# ---- 2. per tile: crop, DTM/CHM, watershed seeded at all inventory trees, metrics for the sampled trees
rows = []
for t in tiles:
    tgt = chosen[chosen.tile == t]
    x0, y0 = tgt.x_etrs89.min() - BUF, tgt.y_etrs89.min() - BUF
    x1, y1 = tgt.x_etrs89.max() + BUF, tgt.y_etrs89.max() + BUF
    W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
    parts = []
    with laspy.open(LID / f"lidar_{t}.laz") as f:
        for p in f.chunk_iterator(5_000_000):
            x, y = np.asarray(p.x), np.asarray(p.y)
            m = (x >= x0) & (x < x1) & (y > y0) & (y <= y1)
            if m.any():
                parts.append(np.c_[x[m], y[m], np.asarray(p.z)[m], np.asarray(p.classification)[m]])
    pa = np.vstack(parts)
    x, y, z, c = pa[:, 0], pa[:, 1], pa[:, 2], pa[:, 3].astype(int)
    idx = ((y1 - y) / RES).astype(int).clip(0, H - 1) * W + ((x - x0) / RES).astype(int).clip(0, W - 1)

    def grid(mask, how):
        out = np.full(W * H, np.nan, "float32")
        (np.fmin if how == "min" else np.fmax).at(out, idx[mask], z[mask])
        return out.reshape(H, W)

    g = grid(np.isin(c, GROUND), "min")
    near = ndimage.distance_transform_edt(np.isnan(g), return_distances=False, return_indices=True)
    dtm = ndimage.median_filter(g[tuple(near)], size=5)
    chm = np.nan_to_num(grid(np.isin(c, VEG), "max") - dtm, nan=0).clip(0, 45)
    seeds = inv[inv.x_etrs89.between(x0, x1) & inv.y_etrs89.between(y0, y1)].reset_index(drop=True)
    tc = ((seeds.x_etrs89 - x0) / RES).astype(int).clip(0, W - 1).values
    tr = ((y1 - seeds.y_etrs89) / RES).astype(int).clip(0, H - 1).values
    canopy = ndimage.binary_opening(chm > 2.0, iterations=1)
    markers = np.zeros((H, W), "int32")
    markers[tr, tc] = np.arange(1, len(seeds) + 1)
    markers = ndimage.grey_dilation(markers, size=(3, 3))
    crowns = watershed(-ndimage.gaussian_filter(chm, 1), markers, mask=canopy | (markers > 0))
    rr, cc = np.indices((H, W))
    lab = crowns.ravel()
    has = lab > 0
    far = np.zeros(W * H, bool)
    far[has] = np.hypot(rr.ravel()[has] - tr[lab[has] - 1], cc.ravel()[has] - tc[lab[has] - 1]) * RES > CAP
    lab[far] = 0
    crowns[~canopy] = 0
    ids = np.arange(1, len(seeds) + 1)
    area = ndimage.sum(np.ones_like(chm), crowns, ids) * RES ** 2
    hmax = np.where(area > 0, ndimage.maximum(chm, crowns, ids), np.nan)
    pid = crowns.ravel()[idx]
    hag = z - dtm.ravel()[idx]
    sel = pid > 0
    P = pd.DataFrame({"id": pid[sel], "h": hag[sel], "veg": np.isin(c[sel], VEG), "gnd": np.isin(c[sel], GROUND),
                      "lab": c[sel] != 12})
    base = P[P.veg & (P.h > 1.5)].groupby("id").h.quantile(0.10).reindex(ids)
    lp = P[P.lab].groupby("id")
    gap = (lp.gnd.sum() / lp.size()).reindex(ids)
    npts = P.groupby("id").size().reindex(ids).fillna(0).astype(int)
    xy = seeds[["x_etrs89", "y_etrs89"]].values
    for i, s in seeds.iterrows():
        if s.codi not in set(tgt.codi):
            continue
        d = np.hypot(*(xy - xy[i]).T)
        d[i] = np.inf
        rows.append({"tree_id": s.codi, "x_etrs89": s.x_etrs89, "y_etrs89": s.y_etrs89, "ground_z": round(float(dtm[tr[i], tc[i]]), 2),
                     "species": s.cat_nom_cientific, "size_category": s.categoria_arbrat, "street": s.street,
                     "nom_barri": s.nom_barri, "tile": t, "height_m": round(float(hmax[i]), 2),
                     "crown_area_m2": round(float(area[i]), 1), "crown_diam_m": round(float(2 * np.sqrt(area[i] / np.pi)), 2),
                     "crown_base_m": round(float(base.iloc[i]), 2), "gap_fraction": round(float(gap.iloc[i]), 3),
                     "lai_proxy": round(float(-np.log(np.clip(gap.iloc[i], 0.02, 1)) / K), 2), "n_points": int(npts.iloc[i]),
                     "nn_dist_m": round(float(d.min()), 2)})
    print(f"tile {t}: {len(pa):,} points, {len(seeds)} inventory seeds, {len(tgt)} sampled trees")

out = pd.DataFrame(rows)
out["flag"] = np.select([out.crown_area_m2.fillna(0) < 2, out.n_points < 50, out.height_m < 3],
                        ["no_crown_detected", "few_points", "low_tree"], "ok")
out["merge_flag"] = out.crown_diam_m / 2 > 0.6 * out.nn_dist_m
out.to_csv(OUT / f"{tag}_lidar_sample.csv", index=False)

# ---- 3. summary
ok = out[out.flag == "ok"]
iqr = lambda s: s.quantile(0.75) - s.quantile(0.25)
groups = [("all_ok", ok), ("no_merge_flag", ok[~ok.merge_flag])] + [(f"class_{k}", g) for k, g in ok.groupby("size_category")]
summ = pd.DataFrame([{"group": n, "n": len(g), "n_streets": g.street.nunique(),
                      **{f"{v}_{f.__name__ if f is not iqr else 'iqr'}": f(g[v]) for v in
                         ("height_m", "crown_diam_m", "crown_base_m", "lai_proxy") for f in (np.median, iqr)}}
                     for n, g in groups]).round(2)
summ.to_csv(OUT / f"{tag}_lidar_summary.csv", index=False)
print(f"\n{len(out)} trees, ok {len(ok)}; flags {out.flag.value_counts().to_dict()}; merge_flag share among ok "
      f"{ok.merge_flag.mean():.0%}")
print(summ.to_string(index=False))
print("Compare: Porta n = 5 (crown 8.85 m, LAI proxy 3.32); Verd urba crown class 6-8 m; Yang et al. 2019 LAI 2.61 (TLS, one tree)")
