"""Quality check of scripts/porta_sidewalk_width.py: 20 random measured trees plotted for a visual check,
a LiDAR cross-check of the facade lines, and the share of widths close to a size-class threshold.

Inputs: databases/barcelona/porta_sidewalk_width.csv, the cached WMS SVG tiles, raw/lidar/porta_bldg_05m.tif
Output: databases/barcelona/sidewalk_width_qa.csv, notes/figures/sidewalk_width_qa_20.png
LiDAR facade = first cell with a building height > 2.5 m, walking from the tree back along the measuring ray.
The LiDAR DTM (0.5 m) was also tried for kerbs and does not resolve them (notes/sidewalk_width.md, QA section).
"""
import json, numpy as np, pandas as pd, rasterio, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.strtree import STRtree
import porta_sidewalk_width as sw

ROOT = sw.ROOT
N, SEED = 20, 21
BLDG_H, STEP = 2.5, 0.25          # ASSUMPTION: building cells > 2.5 m; ray sampled every 0.25 m
BAND = 0.3                        # the plan's +-0.3 m tolerance, used as the class-uncertainty band
CUTS = (2.5, 3.5, 6.0)            # 2011 guide pp. 22-23


def sample(r, a, xs, ys):
    row, col = rasterio.transform.rowcol(r.transform, xs, ys)
    return a[np.clip(row, 0, a.shape[0] - 1), np.clip(col, 0, a.shape[1] - 1)]


if __name__ == "__main__":
    o = json.load(open(ROOT / "exchange/site_origin.json"))
    t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv").drop(columns="flag")
    w = pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv")
    t = t.merge(w[["tree_id", "width_m", "flag", "size_class"]], on="tree_id")
    t["X"], t["Y"] = t.x + o["origin_x"], t.y + o["origin_y"]
    s = t[t.flag == "ok"].sample(N, random_state=SEED).reset_index(drop=True)

    xs = np.arange(np.floor((t.X.min() - sw.RAY) / sw.TILE) * sw.TILE, t.X.max() + sw.RAY, sw.TILE)
    ys = np.arange(np.floor((t.Y.min() - sw.RAY) / sw.TILE) * sw.TILE, t.Y.max() + sw.RAY, sw.TILE)
    fac = sw.lines("facade", xs, ys)
    road = [g for g in sw.lines("road", xs, ys) if g.length >= sw.MIN_KERB]
    tf, tr = STRtree(fac), STRtree(road)
    rb = rasterio.open(ROOT / "databases/barcelona/raw/lidar/porta_bldg_05m.tif")
    B = rb.read(1)

    rows, geo = [], []
    for _, r in s.iterrows():
        p = Point(r.X, r.Y)
        f = fac[tf.nearest(p)]
        q, df = f.interpolate(f.project(p)), f.distance(p)
        u = np.array([r.X - q.x, r.Y - q.y]) / df
        k = np.arange(0, df + 3, STEP)
        hb = np.nan_to_num(sample(rb, B, r.X - u[0] * k, r.Y - u[1] * k), nan=0) > BLDG_H
        off = df - k[np.argmax(hb)] if hb.any() else np.nan   # > 0: LiDAR building edge nearer the street
        near = min(abs(r.width_m - c) for c in CUTS) <= BAND
        rows.append((r.tree_id, r.species, r.street, r.width_m, r.size_class, round(off, 2), near))
        geo.append((p, q, u, r.width_m))
    out = pd.DataFrame(rows, columns=["tree_id", "species", "street", "width_m", "size_class",
                                      "lidar_facade_offset_m", "near_threshold"])
    out.to_csv(ROOT / "databases/barcelona/sidewalk_width_qa.csv", index=False)

    fig, ax = plt.subplots(4, 5, figsize=(20, 16))
    for i, (a, (p, q, u, wm)) in enumerate(zip(ax.flat, geo)):
        box = (p.x - 25, p.y - 25, p.x + 25, p.y + 25)
        c0, r0 = ~rb.transform * (box[0], box[3])
        a.imshow(B[int(r0):int(r0) + 100, int(c0):int(c0) + 100] > BLDG_H, cmap="Greys", alpha=0.35,
                 extent=(box[0], box[0] + 50, box[3] - 50, box[3]))
        for g in tf.query(p.buffer(25)):
            a.plot(*fac[g].xy, color="red", lw=1)
        for g in tr.query(p.buffer(25)):
            a.plot(*road[g].xy, color="dimgrey", lw=1)
        a.plot([q.x, q.x + u[0] * wm], [q.y, q.y + u[1] * wm], color="blue", lw=2)
        a.plot(p.x, p.y, "go", ms=6)
        a.set_xlim(box[0], box[2]); a.set_ylim(box[1], box[3]); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"#{i} {out.street[i][:22]}\n{wm} m, {out.size_class[i]}", fontsize=9)
    fig.suptitle("Sidewalk width QA, 20 random measured trees (red facade, grey road lines, blue measured width, "
                 "grey fill LiDAR buildings > 2.5 m)", fontsize=12)
    fig.tight_layout()
    fig.savefig(ROOT / "notes/figures/sidewalk_width_qa_20.png", dpi=110)

    print(out.to_string())
    o_ = out.lidar_facade_offset_m
    print(f"LiDAR facade offset: median {o_.median():.2f} m, |offset| <= 0.5 m: {(o_.abs() <= 0.5).sum()}/{o_.notna().sum()}, "
          f"> 1 m: {(o_ > 1).sum()}")
    for name, g in (("all ok trees", t[t.flag == "ok"]), ("ok planes", t[(t.flag == "ok") & t.is_plane])):
        near = g.width_m.apply(lambda v: min(abs(v - c) for c in CUTS) <= BAND)
        print(f"{name}: {near.sum()}/{len(g)} within {BAND} m of a class threshold")
