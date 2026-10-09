"""Export one site for the web app: python -m shade_sponge.web_export [site]   (run python -m shade_sponge first)
Writes web/public/data/<site>/: meta.json (palette, scenarios + metrics, sensitivity, overlays), trees.json (positions,
kept trees, layouts), potentials.json (per-position potentials + fit, for live optimisation), buildings.geojson,
overlay PNGs. Coordinates in WGS84; heights in m above local ground (the web map is flat)."""
import sys, json, glob, numpy as np, pandas as pd, geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import Transformer
from .site import load_site, rc, ROOT, DB, EX
from . import heat, layout, season

COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]   # palette order, as notes/figures/tool_v0.png
PLANE = "Platanus × acerifolia"

name = sys.argv[1] if len(sys.argv) > 1 else "porta"
out = ROOT / "web/public/data" / name
out.mkdir(parents=True, exist_ok=True)
site = load_site(name)
o = json.load(open(EX / "site_origin.json"))
to_ll = Transformer.from_crs(25831, 4326, always_xy=True).transform
day = sorted(glob.glob(str(EX / "to_gh/positions_tool_v0_*.csv")))[-1][-12:-4]
P = pd.read_csv(EX / f"to_gh/positions_tool_v0_{day}.csv")
L = pd.read_csv(EX / f"to_gh/layouts_tool_v0_{day}.csv")
S = pd.read_csv(DB / "tool_v0_summary.csv")
pal = layout.palette(site)
pos = site.trees[site.trees.is_plane].reset_index(drop=True)
assert list(pos.tree_id) == list(P.tree_id)
r6 = lambda a: np.round(np.asarray(a, float), 6).tolist()
r2 = lambda a: np.round(np.asarray(a, float), 2).tolist()

# palette (+ the current plane, display only)
sp = list(pal.species) + [PLANE]
phen = season.PHEN
lid = pd.read_csv(DB / "porta_species_lidar_summary.csv").set_index("species")
palette = []
for i, s in enumerate(sp):
    row = pal[pal.species == s].iloc[0] if s in set(pal.species) else None
    palette.append(dict(species=s, short=s.split()[0], color=COLORS[i] if i < len(COLORS) else "#8a8a86",
                        crown_diam_m=float(lid.loc[s, "crown_diam_med"]), height_m=float(lid.loc[s, "height_med"]),
                        crown_base_m=float(lid.loc[s, "crown_base_med"]), lai=float(lid.loc[s, "lai_proxy_med"]),
                        cap=int(row.cap) if row is not None else None, in_palette=row is not None,
                        leaf_habit=phen.loc[s, "leaf_habit"], leaf=[float(phen.loc[s, f"m{m:02d}"]) for m in range(1, 13)],
                        leaf_basis=phen.loc[s, "months_basis"], source=phen.loc[s, "source"]))

# scenarios with metrics (layout species per position only for the ones in the layouts file)
idx = {s: i for i, s in enumerate(sp)}
metrics = ["shade_summer_m2h", "shade_winter_m2h", "runoff_hot_m3", "runoff_m3", "interception_m3"]
scen, layouts = [], {}
for _, r in S.iterrows():
    sc = r.scenario
    w = [float(x) for x in sc[4:].replace("s", "").replace("w", "").replace("r", "").split("_")] if sc.startswith("S4") else None
    scen.append(dict(id=sc, group=sc[:2], weights=w, pareto=bool(r.pareto), in_layouts=sc in set(L.scenario),
                     metrics={m: round(float(r[m]), 1) for m in metrics},
                     counts={s: int(r[s]) for s in pal.species if not pd.isna(r[s])}))
for sc, d in L.groupby("scenario"):
    d = d.set_index("tree_id").loc[P.tree_id]
    layouts[sc] = [idx[s] for s in d.species.map(lambda x: x if x in idx else PLANE)]
s0 = L[L.scenario == "S0_current"].set_index("tree_id").loc[P.tree_id]

# positions, kept trees
lon, lat = to_ll(pos.x.values, pos.y.values)
kept = site.trees[~site.trees.is_plane & (site.trees.flag == "ok")]
klon, klat = to_ll(kept.x.values, kept.y.values)
trees = dict(
    positions=dict(tree_id=P.tree_id.tolist(), lon=r6(lon), lat=r6(lat), sun_summer=r2(P.sun_share_summer),
                   sun_winter=r2(P.sun_share_winter), drains_to_hotspot=r2(P.drains_to_hotspot),
                   water_convergence_m2=P.water_convergence_m2.astype(int).tolist(),
                   s0_crown_diam_m=r2(s0.crown_diam_m.fillna(0)), s0_height_m=r2(s0.height_m.fillna(0)),
                   s0_crown_base_m=r2(s0.crown_base_m.fillna(0))),
    kept=dict(lon=r6(klon), lat=r6(klat), species=kept.sp.tolist(), crown_diam_m=r2(kept.crown_diam_m),
              height_m=r2(kept.height_m), crown_base_m=r2(kept.crown_base_m)),
    layouts=layouts)
json.dump(trees, open(out / "trees.json", "w"), separators=(",", ":"))

# per-position potentials (palette order) + fit, for live optimisation
g = [s.split()[0].lower() for s in pal.species]
kept_n = site.trees[~site.trees.is_plane].sp.value_counts().reindex(pal.species).fillna(0).astype(int)   # as layout.palette()
pot = dict(species=list(pal.species), cap=pal.cap.tolist(), n_total=len(site.trees), kept=kept_n.tolist(),
           max_share=layout.MAX_SHARE, fit=layout.fits(site, pos, pal).astype(int).tolist(),
           shade_summer=P[[f"shade_summer_m2h_{x}" for x in g]].values.tolist(),
           shade_winter=P[[f"shade_winter_m2h_{x}" for x in g]].values.tolist(),
           water=P[[f"water_m3_{x}" for x in g]].values.tolist())
json.dump(pot, open(out / "potentials.json", "w"), separators=(",", ":"))

# buildings (local -> UTM -> WGS84), height above ground
b = gpd.read_file(EX / "to_gh/porta_buildings.geojson").set_crs(None, allow_override=True)
b = b.set_geometry(b.translate(o["origin_x"], o["origin_y"])).set_crs(25831).to_crs(4326)
b[["height_m", "geometry"]].assign(height_m=b.height_m.round(1)).to_file(out / "buildings.geojson", driver="GeoJSON",
                                                                          COORDINATE_PRECISION=6)

# overlays: RGBA PNGs on the site grid, placed by their four corners
H, W = site.domain.shape
x0, y1 = site.x0, site.y1
corners = [to_ll(x, y) for x, y in ((x0, y1 - H), (x0, y1), (x0 + W, y1), (x0 + W, y1 - H))]   # bl, tl, tr, br
show = site.domain & ~site.roof
sun = {s: np.mean([heat.sunlit(site, *x) for x in heat.design_suns(site, s)], axis=0) for s in heat.SEASONS}
layers = [("sun_winter", "Winter sun (15 Jan 10–15 h)", sun["winter"], "cividis", 0, 1),
          ("sun_summer", "Summer sun (15 Jul 12–17 h)", sun["summer"], "cividis", 0, 1),
          ("water", "Water convergence (log10 upstream m²)", np.log10(np.maximum(site.acc, 1)), "Blues", 0, 5),
          ("hotspots", "Flood hotspots (hazard index ≥ 40)", site.hot.astype(float), "Reds", 0, 1.2)]
overlays = []
for key, label, a, cmap, vmin, vmax in layers:
    rgba = plt.get_cmap(cmap)((np.clip(a, vmin, vmax) - vmin) / (vmax - vmin))
    rgba[..., 3] = np.where(show & ((a > 0) if key == "hotspots" else True), 0.85, 0)
    plt.imsave(out / f"{key}.png", rgba)
    overlays.append(dict(id=key, label=label, file=f"{key}.png", cmap=cmap, vmin=vmin, vmax=vmax))

sens = pd.read_csv(DB / "tool_v0_sensitivity.csv")
lon_c, lat_c = to_ll(x0 + W / 2, y1 - H / 2)
meta = dict(site=dict(name=name.capitalize(), center=[round(lon_c, 6), round(lat_c, 6)], corners=[r6(c) for c in corners]),
            palette=palette, scenarios=scen, overlays=overlays, storm="PDISBA T = 2 yr, 1 h (31.9 mm), season-weighted",
            sensitivity=sens.to_dict(orient="records"),
            assumptions=["Leafless crown opacity 0.35 (test 0.25–0.54)", "Design days 15 Jul and 15 Jan (until EPW)",
                         "Runoff reaches a hotspot only within 100 m of flow path", "Tipuana leafless spell Mar–Apr"])
json.dump(meta, open(out / "meta.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, sorted(p.name for p in out.iterdir()))
