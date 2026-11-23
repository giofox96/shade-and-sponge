"""First transfer test of the method on Mataró (T1/T2 transfer, notes/transferability.md): a forward what-if, not a back-test.
Mataró has one inventory snapshot (T_C_ARBRAT, 12 Nov 2026), so there are no observed replacements to replay. Instead:
on each test street, a project must replace every plane tree; the method's layout is compared with the city-practice
draws used in Barcelona (S1a announced mix, S1b built mix) and with Mataró's own recent planting mix, at the same positions.

Same core as scripts/backtest_works.py (shade_sponge.layout / heat / runoff / season, 30-species Barcelona palette,
15% cap, façade clearance, LP sweep, balanced weights 0.50 / 0.25 / 0.25). What differs, all declared:
- ASSUMPTION crowns: no Mataró LiDAR in the cloud (ICGC blocked), so every tree takes the median crown, height, base and
  LAI of its species in Barcelona's LiDAR pool (shade_sponge.site.city_trees). Decision positions: TERCERA for every
  layout (equal trunk size, as in the back-test). Kept trees: Mataró trunk-girth band -> Barcelona class
  ("Fins a 30 cm" PRIMERA, "30 a 60 cm" SEGONA, "60 a 100 cm" and "Més de 100 cm" TERCERA). Fallbacks: all classes of
  the species, then the genus, then the pool median of that class. Palms are left out (not in Barcelona's street pool).
- ASSUMPTION buildings: Overture Maps buildings, release 2026-11-18.0 (ODbL). Height = `height` if >= 2.5 m, else
  num_floors x 3 m, else 9 m (3 floors). Flat ground (no DTM): shadows on a plane.
- ASSUMPTION runoff: no pluvial hazard map for Mataró (notes/catalan_transfer_city.md), so the runoff objective and
  check use all open ground, not hotspots. All open ground sealed (no NDVI layer), so runoff differences come from
  interception only. Design storm = Barcelona PDISBA T2-60 (runoff.design_storm), only to rank layouts; Mataró's own
  PDCLAM storm is not harmonised yet.
- ASSUMPTION sizing: Mataró sidewalk widths are not measured, so the 2011 guide sizing rule is off (façade clearance only),
  for the method and the practice draws alike.
- Cap: 15% of the barri's street trees (Mataró has no such rule; it is the method's rule, applied the same to all draws).
- Mataró practice (S1m): species mix of the street trees in the smallest girth band ("Fins a 30 cm", n ~ 3,400), taken
  as recent plantings (ASSUMPTION), restricted to palette species like S1b.
Street trees = inventory rows whose `ubicacio` is not a park, garden, square or school (text match, ASSUMPTION).

Inputs (not in the repo, licence): the inventory CSV (databases/RESTRICTED_DATA.md), Overture extract
databases/mataro/raw/overture_buildings_20261118.parquet.
Run: python scripts/mataro_transfer_test.py [path/to/mataro_t_c_arbrat.csv]
Outputs (aggregates only): databases/mataro/transfer_test.csv, notes/figures/mataro_transfer_test.png
"""
import re, sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely import wkb
from shapely.geometry import MultiPoint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import city_trees, norm  # noqa: E402
from shade_sponge import heat, layout, runoff, season  # noqa: E402

INV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/project-files/mataro/mataro_t_c_arbrat_20261112.csv")
BLD = ROOT / "databases/mataro/raw/overture_buildings_20261118.parquet"
OUT = ROOT / "databases/mataro"
R_DOM, BUF, RES, SEEDS = 40.0, 150.0, 1.0, 5
BAL, SUM = (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)
GIRTH = {"Fins a 30 cm": "PRIMERA", "30 a 60 cm": "SEGONA", "60 a 100 cm": "TERCERA", "Més de 100 cm": "TERCERA"}
# Test streets: the five with most plane trees in five different barris (one street per barri)
STREETS = [("Jaume Isern, Carrer de", "EIXAMPLE"), ("ALFONS X EL SAVI, RONDA D'", "EIXAMPLE"),
           ("Francesc Layret, Carrer de", "PLA D'EN BOET"), ("Foneria, Carrer de la", "VISTA ALEGRE"),
           ("València, Carrer de", "CERDANYOLA"), ("MIGUEL DE CERVANTES, RONDA DE", "EL PALAU-ESCORXADOR")]
PARK = r"parc|jard|plaça|pl\.|escola"


def key(s):
    """Name key across the two inventories: no synonym in brackets, no cultivar, '×' = 'x'."""
    s = norm(re.sub(r"\s*\(.*?\)", "", s)).replace("×", " x ").lower()
    return " ".join(s.split())


def load_trees():
    d = pd.read_csv(INV)
    d = d[d.icona == "Arbre.png"].copy()                          # palms (Palmera.png) and unknown icons out
    d["x"], d["y"] = Transformer.from_crs(4326, 25831, always_xy=True).transform(d.lon.values, d.lat.values)
    d["street"] = ~d.ubicacio.str.contains(PARK, case=False, na=False)
    d["k"] = d.especie.map(key)
    d["is_plane"] = d.k.str.startswith("platanus")
    d["size_category"] = d.categoria.map(GIRTH).fillna("SEGONA")  # 'categoria' missing: SEGONA (ASSUMPTION)
    d["tree_id"] = "m" + d.index.astype(str)
    return d.reset_index(drop=True)


def trait_table(pool):
    """Median traits per (name key, class), with the docstring's fallbacks."""
    pool = pool.assign(k=pool.sp.map(key), g=pool.sp.str.split().str[0].str.lower())
    cols = ["crown_diam_m", "height_m", "crown_base_m", "lai"]
    by_kc = pool.groupby(["k", "size_category"])[cols].agg(["median", "size"])
    by_k, by_g = pool.groupby("k")[cols].median(), pool.groupby("g")[cols].median()
    by_c = pool.groupby("size_category")[cols].median()
    nk, ng = pool.k.value_counts(), pool.g.value_counts()
    cache = {}

    def get(k, cls):
        if (k, cls) not in cache:
            if (k, cls) in by_kc.index and by_kc.loc[(k, cls), ("lai", "size")] >= 20:
                r, src = by_kc.loc[(k, cls)].xs("median", level=1), "class"
            elif nk.get(k, 0) >= 5:
                r, src = by_k.loc[k], "species"
            elif ng.get(k.split()[0], 0) >= 20:
                r, src = by_g.loc[k.split()[0]], "genus"
            else:
                r, src = by_c.loc[cls], "pool"
            cache[(k, cls)] = (r[cols].astype(float).to_dict(), src)
        return cache[(k, cls)]
    return get


def buildings(x0, y0, x1, y1):
    b = pd.read_parquet(BLD)
    g = gpd.GeoDataFrame(b, geometry=[wkb.loads(bytes(w)) for w in b.geometry], crs=4326).to_crs(25831).cx[x0:x1, y0:y1]
    h = np.where(g.height >= 2.5, g.height, np.where(g.num_floors.notna(), g.num_floors * 3.0, 9.0))
    src = np.where(g.height >= 2.5, "height", np.where(g.num_floors.notna(), "floors", "default"))
    return g.assign(h=h, hsrc=src)


def make_site(street_trees_barri, pos_xy, all_trees, get):
    """Site namespace with the keys shade_sponge needs (see shade_sponge.site._build)."""
    area = MultiPoint(pos_xy).buffer(R_DOM)
    x0, y0, x1, y1 = np.array(area.bounds) + [-BUF, -BUF, BUF, BUF]
    W, H = int(np.ceil((x1 - x0) / RES)), int(np.ceil((y1 - y0) / RES))
    T = from_origin(x0, y1, RES, RES)
    bld = buildings(x0, y0, x1, y1)
    roof = rasterize(((g, 1) for g in bld.geometry), out_shape=(H, W), transform=T, fill=0).astype(bool)
    bh = rasterize(((g, h) for g, h in zip(bld.geometry, bld.h)), out_shape=(H, W), transform=T, fill=0, dtype="float32")
    domain = rasterize([(area, 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)
    P = runoff.P_
    lon, lat = Transformer.from_crs(25831, 4326, always_xy=True).transform(*area.centroid.coords[0])
    s = SimpleNamespace(x0=x0, y1=y1, res=RES, lat=lat, lon=lon, domain=domain, roof=roof, transform=T,
                        cn=np.where(roof, P["cn_roof"], P["cn_sealed"]).astype("float32"),
                        background=np.zeros((H, W), bool), dtm=np.zeros((H, W), "float32"), bldg_h=bh,
                        hot=domain & ~roof, name="mataro")
    s.to_hot = domain & ~roof                                    # no hazard map: all open ground counts
    t = all_trees[(all_trees.x.between(x0, x1)) & (all_trees.y.between(y0, y1))].copy()
    tr = [get(k, c)[0] for k, c in zip(t.k, t.size_category)]
    for c in ("crown_diam_m", "height_m", "crown_base_m", "lai"):
        t[c] = [r[c] for r in tr]
    t["sp"], t["species"], t["flag"] = t.especie.map(lambda v: norm(re.sub(r"\s*\(.*?\)", "", v))), t.especie, "ok"
    s.grid_trees = t
    s.trees = street_trees_barri.assign(sp=street_trees_barri.especie.map(lambda v: norm(re.sub(r"\s*\(.*?\)", "", v))),
                                        flag="ok")
    h_src = bld[bld.intersects(area)].hsrc.value_counts(normalize=True).to_dict()
    return s, h_src


def main():
    d = load_trees()
    pool = city_trees()
    get = trait_table(pool)
    young = d[d.street & (d.categoria == "Fins a 30 cm") & ~d.is_plane]
    p_mm = runoff.design_storm(2, 60)
    rows = []
    for street, barri in STREETS:
        m = d[(d.ubicacio == street) & (d.barri == barri) & d.is_plane & d.street].reset_index(drop=True)
        sb = d[(d.barri == barri) & d.street]
        site, h_src = make_site(sb, m[["x", "y"]].values, d, get)
        pal = layout.palette(site, "barcelona", "TERCERA", sb.is_plane.values & sb.tree_id.isin(m.tree_id).values)
        pal_key = pal.species.map(key)
        cap = pal.cap.values
        pos = m[["tree_id", "x", "y"]]
        fit = layout.fits(site, pos, pal, None, cap=cap)
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
        water = layout.water_potential(site, pos, pal, p_mm, runoff_target="all")
        sw = layout.sweep({"summer": (pot["summer"], 1), "winter": (pot["winter"], -1), "runoff": (water, 1)}, cap, fit)
        ymix = young.k.value_counts()
        mixes = {"S1a": layout.S1A_MIX, "S1b": layout.s1b_mix(),
                 "S1m": {sp: ymix.get(k, 0) for sp, k in zip(pal.species, pal_key)}}
        rng = np.random.default_rng(0)
        lay = {"none": None, "before": None, "method_bal": sw[BAL], "method_sum": sw[SUM]}
        for k, mix in mixes.items():
            for i in range(SEEDS):
                lay[f"{k}_{i}"] = layout.s1a_layout(pal, cap, fit, rng, mix)
        for i in range(SEEDS):
            lay[f"random_{i}"] = layout.random_layout(cap, fit, rng)
        kept = site.grid_trees[~site.grid_trees.tree_id.isin(m.tree_id)]
        plane = get(key("Platanus x acerifolia"), "TERCERA")[0]
        r = dict(street=street, barri=barri, n=len(m), lat=site.lat, lon=site.lon,
                 bld_height_src="; ".join(f"{k} {v:.0%}" for k, v in h_src.items()),
                 fallback_share=float((fit.sum(1) == 1).mean()))
        for name, ch in lay.items():
            if name == "none":
                new = pd.DataFrame()
            else:
                new = pos.copy()
                if name == "before":
                    new = new.assign(sp="Platanus x acerifolia", **plane)
                else:
                    new = new.assign(sp=pal.species.values[ch], **{c: pal[c].values[ch] for c in
                                                                    ("crown_diam_m", "height_m", "crown_base_m", "lai")})
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
                r[f"{v}_{k}"] = float(np.mean([r[f"{v}_{k}_{i}"] for i in range(SEEDS)]))
        rows.append(r)
        print(f"{street} ({barri}) n={len(m)}: method {r['summer_pct_method_bal']:.0f}% | S1a {r['summer_pct_S1a']:.0f}% "
              f"S1b {r['summer_pct_S1b']:.0f}% S1m {r['summer_pct_S1m']:.0f}% random {r['summer_pct_random']:.0f}% "
              f"of the planes' summer shade; {r['top_method_bal']}", flush=True)
    df = pd.DataFrame(rows)
    keep = [c for c in df.columns if not re.search(r"_\d$", c)]       # seed means only
    df[keep].round(3).to_csv(OUT / "transfer_test.csv", index=False)
    figure(df)


def figure(df):
    import matplotlib.pyplot as plt
    cols = [("S1a", "City practice: announced mix (BCN S1a)", "#bdbdbd"), ("S1b", "City practice: built mix (BCN S1b)", "#8c8c8c"),
            ("S1m", "Mataró recent plantings (S1m)", "#d9a441"), ("method_bal", "Method (balanced)", "#2e7d32")]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    x = np.arange(len(df))
    for i, (k, lab, c) in enumerate(cols):
        ax.bar(x + (i - 1.5) * 0.2, df[f"summer_pct_{k}"], 0.2, label=lab, color=c)
    ax.axhline(100, color="k", lw=0.8, ls="--")
    ax.text(len(df) - 0.5, 98, "mature-size planes = 100%", ha="right", va="top", fontsize=8)
    ax.set_xticks(x, [f"{s.split(',')[0].title()}\n({b.title()}, n={n})" for s, b, n in zip(df.street, df.barri, df.n)], fontsize=8)
    ax.set_ylabel("Summer shade of the new trees\n(% of the plane trees', same trunk size)")
    ax.set_title("Mataró transfer test: replacing every plane on six streets", fontsize=11, loc="left")
    ax.set_ylim(0, 128)
    ax.legend(fontsize=8, frameon=False, ncol=2, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "Proxy model, 15 July 12-17 h. Crowns: Barcelona LiDAR medians per species; buildings: Overture Maps "
             "(ODbL); trees: Ajuntament de Mataró inventory (Nov 2026).", fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(ROOT / "notes/figures/mataro_transfer_test.png", dpi=200)


if __name__ == "__main__":
    main()
