"""Rhino kit for the final deck (15 Dec): plain CSV / GeoJSON in local metres, read by the GH snippets in exchange/to_rhino/gh/.

Three visuals (slots marked RHINO in scripts/make_final_new.py):
  1. Porta map: the 832 plane positions coloured by summer-shade gain, method vs city practice, per street.
  2. Back-test areas: the 26 real replacement groups, crowns before / city / method in 3D (one local origin per group).
  3. Streets before / after: the same plane crowns, S0 today vs method, filtered by street.
Sources, all on main after PR #184 (needle fix): web/public/data/porta-barcelona/{meta,trees,potentials}.json (Barcelona
palette, balanced weights S4_s0.50_w0.25_r0.25 = "method"; S1b_obs_0 = one draw of city practice),
exchange/to_gh/porta_*.{csv,geojson}, databases/barcelona/backtest_works_guide{,_positions}.csv, barris/<barri>/.
Per-tree shade = the tool's per-position potential (each tree alone, no crown overlap): use it to colour and rank, not as
a total. Totals for the slides come from the full model (tool_v0_summary_barcelona_sizeexact_trunkTERCERA.csv).
Back-test heights / crown bases: same lookup rule as scripts/backtest_works.py (palette, else city LiDAR pool TERCERA,
SEGONA, all classes n>=20, n>=5, genus, pool TERCERA median); crown diameters are the back-test's own.
Run from the repo root: python scripts/make_rhino_kit.py  (needs pyproj for the sidewalk lines)
"""
import json
import pathlib
import shutil

import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, WEB, GH = ROOT / "databases/barcelona", ROOT / "web/public/data/porta-barcelona", ROOT / "exchange/to_gh"
OUT = ROOT / "exchange/to_rhino"
OX, OY = 430800, 4586800                       # exchange/site_origin.json
METHOD, CITY = "S4_s0.50_w0.25_r0.25", "S1b_obs_0"
R_CTX = 60                                      # m around a back-test group: buildings and context trees
GREY = "#9a9a9a"


def crown_cols(df):
    return df[["crown_diam_m", "height_m", "crown_base_m"]].round(2)


def porta():
    meta = json.loads((WEB / "meta.json").read_text(encoding="utf-8"))
    trees = json.loads((WEB / "trees.json").read_text(encoding="utf-8"))
    pot = json.loads((WEB / "potentials.json").read_text(encoding="utf-8"))
    pal = pd.DataFrame(meta["palette"])
    pos = pd.DataFrame(trees["positions"])
    lid = pd.read_csv(GH / "porta_trees_lidar.csv").set_index("tree_id")
    pos = pos.join(lid[["x", "y", "ground_z", "street"]], on="tree_id")
    shade = np.array(pot["shade_summer"])                                   # 832 positions x 30 species, m2h
    rows = []
    for scen, key in (("S0_today", "S0_current"), ("S1b_city_practice", CITY), ("method", METHOD)):
        k = np.array(trees["layouts"][key])
        p = pal.iloc[k].reset_index(drop=True)
        d = pos[["tree_id", "street", "x", "y", "ground_z"]].copy()
        d["scenario"], d["species"], d["short"], d["color"] = scen, p.species, p.short, p.color
        if scen == "S0_today":                                              # measured LiDAR crowns of the planes
            d["crown_diam_m"], d["height_m"], d["crown_base_m"] = pos.s0_crown_diam_m, pos.s0_height_m, pos.s0_crown_base_m
            d["shade_summer_m2h"] = np.nan                                  # no per-position potential for the planes
        else:
            d[["crown_diam_m", "height_m", "crown_base_m"]] = crown_cols(p).values
            d["shade_summer_m2h"] = shade[np.arange(len(k)), k].round(1)
        rows.append(d)
    long = pd.concat(rows, ignore_index=True)
    # per street: method vs city practice, sum of per-tree potentials
    w = long.pivot_table(index=["tree_id", "street"], columns="scenario", values="shade_summer_m2h").reset_index()
    st = w.groupby("street").agg(n_planes=("tree_id", "size"), shade_city_m2h=("S1b_city_practice", "sum"),
                                 shade_method_m2h=("method", "sum"))
    st["gain_pct"] = (100 * (st.shade_method_m2h / st.shade_city_m2h - 1)).round(1)
    xy = long[long.scenario == "method"].groupby("street")[["x", "y"]].mean().round(1)
    top = lambda s: long[long.scenario == s].groupby("street").short.agg(lambda v: v.mode()[0])  # noqa: E731
    st = st.join(xy).assign(top_city=top("S1b_city_practice"), top_method=top("method")).round(1)
    st = st.sort_values("n_planes", ascending=False)
    long = long.join(st.gain_pct.rename("street_gain_pct"), on="street")
    tree_gain = w.set_index("tree_id").eval("method - S1b_city_practice").round(1)
    long["tree_gain_m2h"] = long.tree_id.map(tree_gain)
    long.to_csv(OUT / "porta/porta_crowns_planes.csv", index=False)
    st.to_csv(OUT / "porta/porta_streets_gain.csv")
    ctx = lid[(~lid.is_plane) & (lid.flag == "ok")].reset_index()
    ctx = ctx[["tree_id", "x", "y", "ground_z", "species", "street"]].join(crown_cols(ctx)).assign(color=GREY)
    ctx.to_csv(OUT / "porta/porta_context_trees.csv", index=False)
    for f in ("porta_boundary.csv", "porta_buildings.geojson"):
        shutil.copy(GH / f, OUT / "porta" / f)
    to_utm = Transformer.from_crs(4326, 25831, always_xy=True)
    sw = json.loads((WEB / "sidewalks.geojson").read_text(encoding="utf-8"))
    for f in sw["features"]:
        lon, lat = np.array(f["geometry"]["coordinates"]).T
        x, y = to_utm.transform(lon, lat)
        f["geometry"]["coordinates"] = np.c_[x - OX, y - OY].round(2).tolist()
    (OUT / "porta/porta_sidewalks.geojson").write_text(json.dumps(sw), encoding="utf-8")
    return pal, st


def pool():
    """City LiDAR tree pool (Porta + every barri table), UTM coordinates."""
    p = pd.read_csv(GH / "porta_trees_lidar.csv").assign(barri="porta")
    p["x"], p["y"] = p.x + OX, p.y + OY
    t = [p] + [pd.read_csv(f).assign(barri=f.parent.name) for f in sorted((DB / "barris").glob("*/trees_lidar.csv"))]
    t = pd.concat(t, ignore_index=True)
    t = t[t.flag == "ok"].rename(columns={"lai_proxy": "lai"})
    t["sp"] = t.species.str.replace(r" '.*'$", "", regex=True).str.strip()
    return t


def lookup(pal, t):
    """Height and crown base per species, rule of scripts/backtest_works.py traits_lookup."""
    p = pal.set_index("species")
    ref = t[t.size_category == "TERCERA"][["height_m", "crown_base_m"]].median()

    def get(sp):
        if sp in p.index:
            return p.loc[sp, ["height_m", "crown_base_m"]], "palette"
        g, gen = t[t.sp == sp], t[t.sp.str.split().str[0] == sp.split()[0]]
        for sub, src, k in ((g[g.size_category == "TERCERA"], "TERCERA", 20), (g[g.size_category == "SEGONA"], "SEGONA", 20),
                            (g, "all", 20), (g, "all n>=5", 5), (gen, "genus", 20)):
            if len(sub) >= k:
                return sub[["height_m", "crown_base_m"]].median(), src
        return ref, "pool TERCERA median"
    return get


def backtest(pal, st):
    g = pd.read_csv(DB / "backtest_works_guide.csv")
    pos = pd.read_csv(DB / "backtest_works_guide_positions.csv")
    t = pool()
    get = lookup(pal, t)
    color = dict(zip(pal.species, pal.color))
    g["origin_x"], g["origin_y"] = (g.x / 10).round() * 10, (g.y / 10).round() * 10
    g["method_wins_summer"] = g.summer_pct_method_bal > g.summer_pct_city
    pc = (g.shade_summer_city - g.shade_summer_none) / g.n
    pm = (g.shade_summer_method_bal - g.shade_summer_none) / g.n
    g["added_summer_m2h_per_tree_city"], g["added_summer_m2h_per_tree_method"] = pc.round(1), pm.round(1)
    keep = ["group", "barri", "quarter", "n", "origin_x", "origin_y", "top_before", "top_city", "top_method_bal",
            "summer_pct_city", "summer_pct_method_bal", "added_summer_m2h_per_tree_city", "added_summer_m2h_per_tree_method",
            "runoff_hot_city", "runoff_hot_method_bal", "method_wins_summer"]
    g[keep].round(1).to_csv(OUT / "backtest/backtest_groups.csv", index=False)
    org = g.set_index("group")[["origin_x", "origin_y", "barri"]]
    rows = []
    for scen, sp_col, cr_col in (("before", "sp_before", "crown_before"), ("city", "sp_city", "crown_city"),
                                 ("method", "sp_method_bal", "crown_method_bal")):
        for i, r in pos.iterrows():
            hb, src = get(r[sp_col])
            o = org.loc[r.group]
            rows.append(dict(group=r.group, scenario=scen, pos_id=i, x=round(r.x - o.origin_x, 2), y=round(r.y - o.origin_y, 2),
                             species=r[sp_col], color=color.get(r[sp_col], GREY), crown_diam_m=r[cr_col],
                             height_m=round(float(hb.height_m), 2), crown_base_m=round(float(hb.crown_base_m), 2),
                             height_source=src))
    long = pd.DataFrame(rows)
    kd = cKDTree(t[["x", "y"]].values)
    _, j = kd.query(pos[["x", "y"]].values)
    long["ground_z"] = np.tile(t.ground_z.values[j].round(2), 3)
    long.to_csv(OUT / "backtest/backtest_crowns.csv", index=False)
    # context per group: kept trees and buildings within R_CTX of the group's positions (removed positions excluded)
    for grp, o in org.iterrows():
        P = pos[pos.group == grp][["x", "y"]].values
        near = np.unique(np.concatenate(kd.query_ball_point(P, R_CTX)))
        gone = np.unique(np.concatenate(kd.query_ball_point(P, 1.5)))
        c = t.iloc[np.setdiff1d(near, gone)]
        c = c[["tree_id", "x", "y", "ground_z", "species"]].join(crown_cols(c)).assign(color=GREY)
        c["x"], c["y"] = (c.x - o.origin_x).round(2), (c.y - o.origin_y).round(2)
        c.to_csv(OUT / f"backtest/context/backtest_{grp}_context_trees.csv", index=False)
        bfile = GH / "porta_buildings.geojson" if o.barri == "porta" else DB / "barris" / o.barri / "buildings.geojson"
        bj = json.loads(bfile.read_text(encoding="utf-8"))
        dx, dy = (o.origin_x - OX, o.origin_y - OY) if o.barri == "porta" else (o.origin_x, o.origin_y)
        cx, cy = P[:, 0].mean() - o.origin_x, P[:, 1].mean() - o.origin_y
        reach = R_CTX + np.hypot(*(P - P.mean(0)).T).max()
        feats = []
        for f in bj["features"]:
            gm = f["geometry"]
            polys = [gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]
            polys = [[[[round(x - dx, 2), round(y - dy, 2)] for x, y in ring[:]] for ring in poly] for poly in polys]
            ring = np.array(polys[0][0])
            if np.hypot(ring[:, 0] - cx, ring[:, 1] - cy).min() <= reach:
                feats.append(dict(type="Feature", properties={k: f["properties"][k] for k in ("height_m", "ground_z")},
                                  geometry=dict(type="MultiPolygon", coordinates=polys)))
        (OUT / f"backtest/context/backtest_{grp}_buildings.geojson").write_text(
            json.dumps(dict(type="FeatureCollection", features=feats)), encoding="utf-8")
    return g


def main():
    for d in ("porta", "backtest/context"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    pal, st = porta()
    g = backtest(pal, st)
    print(st.head(12).to_string())
    print(f"back-test: {g.method_wins_summer.sum()}/{len(g)} groups, method more summer shade than the city")


if __name__ == "__main__":
    main()
