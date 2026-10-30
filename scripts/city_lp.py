"""City-wide 15% cap: one layout LP over several barris at once (notes/citywide_plan.md §6.2 step 6, §6.8).
Each barri is set up as its reference run (python -m shade_sponge "<barri>" --size=exact --trunk=TERCERA, scenario R:
replace every plane): per-position potentials (summer shade, winter shade, hotspot runoff) and the sizing/facade fit.
The positions of all barris are stacked into one transportation LP (layout.assign), so species go where they work best
across barris; the cap is the city's (layout.city_cap), not one per barri. The same weight sweep as the tool
(layout.sweep, 15 combinations); every layout is then re-scored barri by barri with the full raster models.
Usage (PC, project env; needs the site caches and databases/barcelona/arbrat_viari.csv):
    python scripts/city_lp.py                         # Porta + Eixample + Sant Martí (the barris of run_barris.py)
    python scripts/city_lp.py "Gràcia" ...            # other districts or barri names, plus Porta
Outputs: databases/barcelona/citylp/tool_v0_citylp_<slug>.csv (S0 + the 15 swept layouts, as tool_v0_summary_*),
         databases/barcelona/citylp_summary.csv (one row per barri: local-cap tool, city-cap tool, city mix S1a),
         databases/barcelona/citylp_species.csv (species counts per barri and layout, and the city cap)."""
import sys, pathlib, numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge import heat, runoff, layout  # noqa: E402
from shade_sponge.site import load_site, DB  # noqa: E402

TRUNK, SIZE = "TERCERA", "exact"                          # Porta's reference options (run_barris.py)
OUT = DB / "citylp"


def setup(name):
    site = load_site(name)
    sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
    lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
    pal = layout.palette(site, "city", TRUNK)
    pos = site.trees[site.trees.is_plane].reset_index(drop=True)
    pot = {s: layout.shade_potential(site, pos, pal, sun[s], lit[s], heat.SEASONS[s]["month"]) for s in sun}
    return site, sun, lit, pal, pos, pot


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or ["Eixample", "Sant Martí"]
    idx = pd.read_csv(DB / "lidar_tiles_barris.csv").drop_duplicates("barri")
    sel = idx[idx.district.isin(args) | idx.barri.isin(args)]
    barris = [("Porta", "porta")] + list(zip(sel.barri, sel.slug))
    p = runoff.design_storm(2, 60)

    # 1. potentials and fit per barri (palette species are the same everywhere; their traits are each barri's medians)
    parts = []
    for name, s in barris:
        print(f"setup {name}", flush=True)
        site, sun, lit, pal, pos, pot = setup(name if s != "porta" else "porta")
        parts.append(dict(name=name, slug=s, pal=pal, pos=pos, summer=pot["summer"], winter=pot["winter"],
                          water=layout.water_potential(site, pos, pal, p), fit=layout.fits(site, pos, pal, SIZE)))
    species = list(parts[0]["pal"].species)

    # 2. the city cap (street-tree inventory, notes/citywide_plan.md §6.5)
    t = pd.read_csv(DB / "arbrat_viari.csv", usecols=["cat_nom_cientific", "tipus_element"])
    t = t[t.tipus_element == "ARBRE VIARI"]
    n_sp = t.cat_nom_cientific.value_counts().reindex(species).fillna(0).values
    planes_city = int(t.cat_nom_cientific.str.startswith("Platanus").sum())
    P = sum(len(q["pos"]) for q in parts)
    cap = layout.city_cap(n_sp, len(t), P, planes_city)
    print(f"{len(t)} street trees, {planes_city} planes; {P} planes in {len(parts)} barris; city cap here:",
          dict(zip(species, cap)))

    # 3. one sweep over the stacked positions
    stack = lambda k: np.vstack([q[k] for q in parts])
    objs = {"summer": (stack("summer"), 1), "winter": (stack("winter"), -1), "runoff": (stack("water"), 1)}
    lay = layout.sweep(objs, cap, stack("fit"))
    cut = np.cumsum([0] + [len(q["pos"]) for q in parts])

    # 4. re-score each barri with the full models
    OUT.mkdir(exist_ok=True)
    rows, counts = [], []
    for k, q in enumerate(parts):
        print(f"evaluate {q['name']}", flush=True)
        site = load_site(q["name"] if q["slug"] != "porta" else "porta")
        sun = {s: heat.design_suns(site, s) for s in heat.SEASONS}
        lit = {s: [heat.sunlit(site, *x) for x in sun[s]] for s in sun}
        res = [dict(scenario="S0_current", **layout.evaluate(site, site.trees[site.trees.flag == "ok"], sun, lit, p))]
        for w, ch in lay.items():
            c = ch[cut[k]:cut[k + 1]]
            sc = "S4_s{:.2f}_w{:.2f}_r{:.2f}".format(*w)
            n = {sp: int((c == j).sum()) for j, sp in enumerate(species)}
            res.append(dict(scenario=sc, **layout.evaluate(site, layout.apply(site, q["pos"], q["pal"], c), sun, lit, p),
                            eff_species=layout.eff_species(c, len(species)), **n))
            counts.append(dict(barri=q["name"], scenario=sc, **n))
        res = pd.DataFrame(res)
        res.round(1).to_csv(OUT / f"tool_v0_citylp_{q['slug']}.csv", index=False)
        s0, best = res.iloc[0], res.iloc[1:].loc[res.iloc[1:].shade_summer_m2h.idxmax()]
        rows.append(dict(barri=q["name"], planes=len(q["pos"]), **{f"{v}_pct_citylp": round(100 * best[f"shade_{v}_m2h"] / s0[f"shade_{v}_m2h"], 1)
                                                                   for v in ("summer", "winter")},
                         runoff_hot_change_pct_citylp=round(100 * (best.runoff_hot_m3 / s0.runoff_hot_m3 - 1), 1)))
    out = pd.DataFrame(rows)
    local = pd.read_csv(DB / "barris_summary.csv")[["barri", "summer_pct_s1a", "summer_pct_tool"]]
    out = out.merge(local, on="barri", how="left")
    out["citylp_minus_local_pts"] = (out.summer_pct_citylp - out.summer_pct_tool).round(1)
    out.to_csv(DB / "citylp_summary.csv", index=False)
    c = pd.DataFrame(counts)
    tot = c.groupby("scenario")[species].sum().reset_index().assign(barri="ALL")
    pd.concat([c, tot, pd.DataFrame([dict(barri="CITY_CAP", scenario="", **dict(zip(species, cap)))])]).to_csv(
        DB / "citylp_species.csv", index=False)
    print(out.to_string(index=False))
