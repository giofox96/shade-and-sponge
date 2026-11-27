"""Florence transfer test (T2 transfer, notes/transferability.md): the forward what-if of scripts/mataro_transfer_test.py on
Firenze Nova. On each test site a project must replace every plane tree; the method's layout is compared with the
Barcelona city-practice draws (S1a announced mix, S1b built mix), with Florence's own recent planting mix (S1f) and with
random draws, at the same positions.

Same core and rules as the Mataró test (shade_sponge.layout / heat / runoff / season, 30-species Barcelona palette, 15% cap,
façade clearance, LP sweep, balanced weights 0.50 / 0.25 / 0.25, five seeds per draw). What differs, all declared:
- Trees: the Life Escapos census (Comune di Firenze, CC BY-NC 4.0, 1,459 public trees of Firenze Nova, EPSG:7791;
  databases/florence/raw/escapos_tree_census.shp, as scripts/florence_lidar_trees.py). The census has no street name and no
  street-vs-park flag, so ASSUMPTION test sites = groups of census planes linked at <= LINK m (a row of planes), kept if
  >= MIN_N planes. Every census tree counts as a street tree for the cap (no flag to split them).
- Crowns of the existing trees: Florence 2023 LiDAR (databases/florence/florence_tree_lidar.csv, scripts/florence_lidar_trees.py):
  crown diameter, height and crown base for every tree with flag "ok". ASSUMPTION LAI: the Barcelona LiDAR pool median of the
  species and trunk class (mataro_transfer_test.trait_table), not the Florence LAI proxy, which is about twice Porta's for
  the same species because the cloud is unclassified (notes/florence_lidar_validation.md, "LAI proxy"); mixing it with the
  Barcelona palette's LAI would favour the "before" planes. Trees without a crown take the pool values for all four.
  LiDAR heights run +1.1 m above the census (same note); not corrected. New trees take the Barcelona palette values.
- Trunk class of kept trees from the census DBH: circumference pi x dbh <= 30 cm PRIMERA, <= 60 cm SEGONA, else TERCERA
  (Mataró's girth bands). Decision positions: TERCERA for every layout.
- ASSUMPTION buildings: Overture Maps (ODbL), fetched once with the overturemaps CLI for the sites' box + 500 m. Height =
  `height` if >= 2.5 m, else num_floors x 3 m, else 9 m. No LiDAR roof heights (the Florence cloud is unclassified).
  Flat ground (no DTM): shadows on a plane.
- ASSUMPTION runoff: as Mataró. Pacetti et al.'s pluvial index is a relative rank under CC BY-NC-ND (databases/data_inventory.md
  §6), so the runoff objective and check use all open ground, all open ground sealed (interception differences only), design
  storm = Barcelona PDISBA T2-60 (runoff.design_storm), only to rank layouts.
- ASSUMPTION sizing: no sidewalk widths measured in Florence, so the 2011 guide sizing rule is off (façade clearance only).
- Cap: 15% of the census trees (the method's rule; Florence has no such rule), the same for every draw.
- Florence practice (S1f): species mix of the municipal inventory's trees with trunk circumference <= 30 cm (Mataró's
  youngest band), taken as recent plantings (ASSUMPTION), planes out, restricted to palette species like S1b. Source:
  Comune di Firenze "Alberi" (CC BY 4.0), databases/florence/alberi.geojson, fetched once as scripts/species_coverage.py
  does. It is city-wide and holds all public trees, parks included (not street trees only).

Run on the PC (the census and the LiDAR stay local):
  python scripts/florence_transfer_test.py
Inputs: databases/florence/raw/escapos_tree_census.shp, databases/florence/florence_tree_lidar.csv,
  databases/florence/alberi.geojson (fetched if missing), databases/florence/raw/overture_buildings.parquet (fetched if missing).
Outputs (aggregates only): databases/florence/transfer_test.csv, notes/figures/florence_transfer_test.png
"""
import json, re, subprocess, sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import geopandas as gpd
import requests
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from shapely import wkb
from shapely.geometry import MultiPoint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from shade_sponge.site import city_trees, norm  # noqa: E402
from shade_sponge import heat, layout, runoff, season  # noqa: E402
import mataro_transfer_test as mt  # noqa: E402  (key, trait_table, R_DOM, BUF, RES, SEEDS, weights)

FL = ROOT / "databases/florence"
CENSUS = FL / "raw/escapos_tree_census.shp"
LIDAR = FL / "florence_tree_lidar.csv"
INV = FL / "alberi.geojson"
INV_URL = "https://data.comune.fi.it/datastore/download.php?id=6370&type=99&format=url&file_format=geojson&file_id=23066"
BLD = FL / "raw/overture_buildings.parquet"
CRS = 7791                                                       # RDN2008 / UTM 32N, the census and LiDAR CRS
LINK, MIN_N = 15.0, 8                                            # ASSUMPTION: test-site grouping of planes


def girth_class(dbh_cm):
    c = np.pi * np.asarray(dbh_cm, float)
    return np.where(c <= 30, "PRIMERA", np.where(c <= 60, "SEGONA", "TERCERA"))


def load_trees():
    t = gpd.read_file(CENSUS)
    assert t.crs.to_epsg() == CRS
    d = pd.DataFrame({"tree_id": t["id"].values, "especie": t.species.values, "x": t.geometry.x.values,
                      "y": t.geometry.y.values, "dbh_cm": t.dbh_cm.values})
    d["k"] = d.especie.map(mt.key)
    d["is_plane"] = d.k.str.startswith("platanus")
    d["size_category"] = girth_class(d.dbh_cm.fillna(30 / np.pi + 1))   # no DBH: SEGONA (ASSUMPTION, as Mataró)
    return d


def sites(d):
    """Groups of planes linked at <= LINK m, with >= MIN_N planes, largest first."""
    p = d[d.is_plane]
    pairs = np.array(sorted(cKDTree(p[["x", "y"]].values).query_pairs(LINK)))
    n = len(p)
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n)) if len(pairs) else coo_matrix((n, n))
    _, lab = connected_components(g, directed=False)
    sizes = pd.Series(lab).value_counts()
    keep = sizes[sizes >= MIN_N].index
    return [p[lab == k].reset_index(drop=True) for k in keep]


def fetch_buildings(groups):
    xy = np.concatenate([g[["x", "y"]].values for g in groups])
    x0, y0 = xy.min(0) - 500
    x1, y1 = xy.max(0) + 500
    (w, e), (s, n) = Transformer.from_crs(CRS, 4326, always_xy=True).transform([x0, x1], [y0, y1])
    BLD.parent.mkdir(parents=True, exist_ok=True)
    print(f"fetching Overture buildings, bbox {w:.5f},{s:.5f},{e:.5f},{n:.5f}", flush=True)
    subprocess.run(["overturemaps", "download", f"--bbox={w:.5f},{s:.5f},{e:.5f},{n:.5f}", "-f", "geoparquet",
                    "--type=building", "-o", str(BLD)], check=True)


def buildings(x0, y0, x1, y1):
    b = pd.read_parquet(BLD)
    g = gpd.GeoDataFrame(b, geometry=[wkb.loads(bytes(w)) for w in b.geometry], crs=4326).to_crs(CRS).cx[x0:x1, y0:y1]
    h = np.where(g.height >= 2.5, g.height, np.where(g.num_floors.notna(), g.num_floors * 3.0, 9.0))
    src = np.where(g.height >= 2.5, "height", np.where(g.num_floors.notna(), "floors", "default"))
    return g.assign(h=h, hsrc=src)


def young_mix():
    """S1f counts by name key: inventory trees with circumference <= 30 cm, planes out."""
    if not INV.exists():
        INV.write_bytes(requests.get(INV_URL, timeout=600).content)
    f = json.loads(INV.read_text(encoding="utf-8"))["features"]
    y = pd.DataFrame([(p.get("SPECIE"), p.get("CIRCONF_CM")) for p in (x["properties"] for x in f)], columns=["sp", "circ"])
    y = y[pd.to_numeric(y.circ, errors="coerce").le(30) & y.sp.notna()]
    k = y.sp.map(mt.key)
    print(f"S1f: {len(y)} inventory trees with circumference <= 30 cm", flush=True)
    return k[~k.str.startswith("platanus")].value_counts()


def make_site(census, pos_xy, get, lidar):
    """Site namespace with the keys shade_sponge needs, as mataro_transfer_test.make_site, in EPSG:7791."""
    area = MultiPoint(pos_xy).buffer(mt.R_DOM)
    x0, y0, x1, y1 = np.array(area.bounds) + [-mt.BUF, -mt.BUF, mt.BUF, mt.BUF]
    W, H = int(np.ceil((x1 - x0) / mt.RES)), int(np.ceil((y1 - y0) / mt.RES))
    T = from_origin(x0, y1, mt.RES, mt.RES)
    bld = buildings(x0, y0, x1, y1)
    roof = rasterize(((g, 1) for g in bld.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    bh = rasterize(((g, h) for g, h in zip(bld.geometry, bld.h)), out_shape=(H, W), transform=T, fill=0, dtype="float32")
    domain = rasterize([(area, 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)
    P = runoff.P_
    lon, lat = Transformer.from_crs(CRS, 4326, always_xy=True).transform(*area.centroid.coords[0])
    s = SimpleNamespace(x0=x0, y1=y1, res=mt.RES, lat=lat, lon=lon, domain=domain, roof=roof, transform=T,
                        cn=np.where(roof, P["cn_roof"], P["cn_sealed"]).astype("float32"),
                        background=np.zeros((H, W), bool), dtm=np.zeros((H, W), "float32"), bldg_h=bh,
                        hot=domain & ~roof, name="florence")
    s.to_hot = domain & ~roof                                    # no usable hazard map: all open ground counts
    t = census[census.x.between(x0, x1) & census.y.between(y0, y1)].copy()
    tr = [get(k, c)[0] for k, c in zip(t.k, t.size_category)]
    for c in ("crown_diam_m", "height_m", "crown_base_m", "lai"):
        t[c] = [r[c] for r in tr]                                # LAI stays the pool's (docstring)
    L = lidar.set_index("tree_id").reindex(t.tree_id)
    ok = (L.flag == "ok").values
    for c in ("crown_diam_m", "height_m", "crown_base_m"):
        v = L[c].values
        t[c] = np.where(ok & np.isfinite(v), v, t[c].values)
    t["crown_src"] = np.where(ok, "lidar", "bcn_pool")
    t["sp"], t["species"], t["flag"] = t.especie.map(norm), t.especie, "ok"
    s.grid_trees = t
    s.trees = census.assign(sp=census.especie.map(norm), flag="ok")
    h_src = bld[bld.intersects(area)].hsrc.value_counts(normalize=True).to_dict()
    return s, h_src


def main():
    d = load_trees()
    groups = sites(d)
    print(f"{d.is_plane.sum()} planes; {len(groups)} test sites (>= {MIN_N} planes linked at <= {LINK:.0f} m): "
          f"{[len(g) for g in groups]}", flush=True)
    if not BLD.exists():
        fetch_buildings(groups)
    lidar = pd.read_csv(LIDAR)
    get = mt.trait_table(city_trees())
    ymix = young_mix()
    p_mm = runoff.design_storm(2, 60)
    rows = []
    for n_site, m in enumerate(groups, 1):
        site, h_src = make_site(d, m[["x", "y"]].values, get, lidar)
        pal = layout.palette(site, "barcelona", "TERCERA", d.tree_id.isin(m.tree_id).values)
        pal_key = pal.species.map(mt.key)
        cap = pal.cap.values
        pos = m[["tree_id", "x", "y"]]
        fit = layout.fits(site, pos, pal, None, cap=cap)
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
        water = layout.water_potential(site, pos, pal, p_mm, runoff_target="all")
        sw = layout.sweep({"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)}, cap, fit)
        mixes = {"S1a": layout.S1A_MIX, "S1b": layout.s1b_mix(),
                 "S1f": {sp: ymix.get(k, 0) for sp, k in zip(pal.species, pal_key)}}
        rng = np.random.default_rng(0)
        lay = {"none": None, "before": None, "method_bal": sw[mt.BAL], "method_sum": sw[mt.SUM]}
        for k, mix in mixes.items():
            for i in range(mt.SEEDS):
                lay[f"{k}_{i}"] = layout.s1a_layout(pal, cap, fit, rng, mix)
        for i in range(mt.SEEDS):
            lay[f"random_{i}"] = layout.random_layout(cap, fit, rng)
        kept = site.grid_trees[~site.grid_trees.tree_id.isin(m.tree_id)]
        cols = ["crown_diam_m", "height_m", "crown_base_m", "lai"]
        r = dict(site=f"F{n_site}", n=len(m), lat=site.lat, lon=site.lon,
                 bld_height_src="; ".join(f"{k} {v:.0%}" for k, v in h_src.items()),
                 fallback_share=float((fit.sum(1) == 1).mean()),
                 lidar_crown_share=float((site.grid_trees.crown_src == "lidar").mean()))
        for name, ch in lay.items():
            if name == "none":
                new = pd.DataFrame()
            elif name == "before":                                   # today's planes as measured (pool where no crown)
                new = pos.assign(sp="Platanus x acerifolia",
                                 **site.grid_trees.set_index("tree_id").loc[pos.tree_id, cols].reset_index(drop=True))
            else:
                new = pos.assign(sp=pal.species.values[ch], **{c: pal[c].values[ch] for c in cols})
            trees = pd.concat([kept, new], ignore_index=True)
            for s in sun:
                r[f"shade_{s}_{name}"] = heat.shade_m2h(site, trees, sun[s], lit[s], heat.SEASONS[s]["month"])
            r[f"runoff_{name}"] = season.runoff_seasonal(site, trees, p_mm)["runoff_m3"]
            if name.startswith("method"):
                r[f"top_{name}"] = "; ".join(f"{s} {n}" for s, n in pd.Series(pal.species.values[ch]).value_counts().head(3).items())
                r[f"eff_species_{name}"] = layout.eff_species(ch, len(pal))
        base = r["shade_summer_before"] - r["shade_summer_none"]
        for name in lay:
            if name not in ("none", "before"):
                r[f"summer_pct_{name}"] = 100 * (r[f"shade_summer_{name}"] - r["shade_summer_none"]) / base
        for k in list(mixes) + ["random"]:
            for v in ("summer_pct", "shade_winter", "runoff"):
                r[f"{v}_{k}"] = float(np.mean([r[f"{v}_{k}_{i}"] for i in range(mt.SEEDS)]))
        rows.append(r)
        print(f"F{n_site} n={len(m)}: method {r['summer_pct_method_bal']:.0f}% | S1a {r['summer_pct_S1a']:.0f}% "
              f"S1b {r['summer_pct_S1b']:.0f}% S1f {r['summer_pct_S1f']:.0f}% random {r['summer_pct_random']:.0f}% "
              f"of the planes' summer shade; {r['top_method_bal']}", flush=True)
    df = pd.DataFrame(rows)
    keep = [c for c in df.columns if not re.search(r"_\d$", c)]       # seed means only
    df[keep].round(3).to_csv(FL / "transfer_test.csv", index=False)
    figure(df)


def figure(df):
    import matplotlib.pyplot as plt
    cols = [("S1a", "City practice: announced mix (BCN S1a)", "#bdbdbd"), ("S1b", "City practice: built mix (BCN S1b)", "#8c8c8c"),
            ("S1f", "Florence recent plantings (S1f)", "#d9a441"), ("method_bal", "Method (balanced)", "#2e7d32")]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    x = np.arange(len(df))
    for i, (k, lab, c) in enumerate(cols):
        ax.bar(x + (i - 1.5) * 0.2, df[f"summer_pct_{k}"], 0.2, label=lab, color=c)
    ax.axhline(100, color="k", lw=0.8, ls="--")
    ax.text(len(df) - 0.5, 98, "today's planes (LiDAR) = 100%", ha="right", va="top", fontsize=8)
    ax.set_xticks(x, [f"{s}\n(n={n})" for s, n in zip(df.site, df.n)], fontsize=8)
    ax.set_ylabel("Summer shade of the new trees\n(% of today's plane trees)")
    ax.set_title(f"Florence transfer test: replacing every plane in {len(df)} groups of Firenze Nova", fontsize=11, loc="left")
    ax.set_ylim(0, 128)
    ax.legend(fontsize=8, frameon=False, ncol=2, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "Proxy model, 15 July 12-17 h. Crowns: existing trees from Comune di Firenze LiDAR 2023 (LAI from Barcelona "
             "medians), new trees Barcelona LiDAR medians; buildings: Overture Maps (ODbL); trees: Comune di Firenze, Life Escapos "
             "(CC BY-NC 4.0) and Alberi (CC BY 4.0).", fontsize=6.5, color="#555", wrap=True)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(ROOT / "notes/figures/florence_transfer_test.png", dpi=200)


if __name__ == "__main__":
    main()
