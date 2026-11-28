"""City view data for the web app: one light file with every barri's numbers and the method's new trees.
Numbers: databases/barcelona/barris_summary.csv (per-barri runs: method, S1a, S1b, % of today's summer shade),
         citylp_summary.csv (the joint city LP with one city-wide 15% cap, python scripts/city_lp.py --all) and
         citylp_add_only.csv when present (barris with no planes: shade added in free spots).
Trees:   the method's layout with the most summer shade in each barri's own run, from the Grasshopper export
         exchange/to_gh/layouts_tool_v0_<slug>_sizeexact_trunkTERCERA_<date>.csv (latest date; python -m shade_sponge,
         written on the PC). Barris without that file get numbers only. The city LP layout is not saved per tree.
Output:  web/public/data/city.json  {species: [...], barris: {name: {numbers..., trees: [[lon, lat, species, crown_m], ...]}}}
Run from the repo root (on the PC, where the layout exports are): python scripts/make_city_web.py"""
import json, pathlib, sys
import pandas as pd
from pyproj import Transformer

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shade_sponge.site import slug  # noqa: E402

DB, TG, TAG = ROOT / "databases/barcelona", ROOT / "exchange/to_gh", "_sizeexact_trunkTERCERA"
o = json.load(open(ROOT / "exchange/site_origin.json"))
to_ll = Transformer.from_crs(25831, 4326, always_xy=True).transform

b = pd.read_csv(DB / "barris_summary.csv").drop_duplicates("barri").set_index("barri")
c = pd.read_csv(DB / "citylp_summary.csv").set_index("barri") if (DB / "citylp_summary.csv").exists() else pd.DataFrame()
a = pd.read_csv(DB / "citylp_add_only.csv").set_index("barri") if (DB / "citylp_add_only.csv").exists() else pd.DataFrame()
num = lambda v: None if pd.isna(v) else round(float(v), 1)

species, out, missing = [], {}, []
for name, r in b.iterrows():
    s = slug(name)
    d = dict(summer_pct_method=num(r.summer_pct_tool), summer_pct_s1a=num(r.summer_pct_s1a), summer_pct_s1b=num(r.summer_pct_s1b),
             summer_pct_citylp=num(c.summer_pct_citylp.get(name)) if len(c) else None,
             planes=int(c.planes.get(name)) if len(c) and name in c.index else None)
    summ = DB / (f"tool_v0_summary{TAG}.csv" if s == "porta" else f"tool_v0_summary_{s}{TAG}.csv")
    lays = sorted(TG.glob(f"layouts_tool_v0{'' if s == 'porta' else '_' + s}{TAG}_2*.csv"))
    if summ.exists() and lays:
        t = pd.read_csv(summ)
        opt = t[t.scenario.str.startswith("S4_")]
        best = opt.loc[opt.shade_summer_m2h.idxmax(), "scenario"]
        L = pd.read_csv(lays[-1])
        L = L[L.scenario == best]
        lon, lat = to_ll((L.x + o["origin_x"]).values, (L.y + o["origin_y"]).values)
        for sp in L.species.unique():
            if sp not in species:
                species.append(sp)
        d["layout"] = best
        d["trees"] = [[round(x, 6), round(y, 6), species.index(sp), round(float(cd), 1)]
                      for x, y, sp, cd in zip(lon, lat, L.species, L.crown_diam_m)]
    else:
        missing.append(name)
    out[name] = d
for name, r in a.iterrows():                                   # no planes: shade added in free spots
    out[name] = dict(add_only=True, spots=int(r.spots), summer_added_pct_method=num(r.summer_added_pct_method),
                     summer_added_pct_s1a=num(r.summer_added_pct_s1a), summer_added_pct_s1b=num(r.summer_added_pct_s1b))

city = pd.read_csv(DB / "citylp_city.csv").set_index("scenario").summer_pct_of_today.to_dict() if (DB / "citylp_city.csv").exists() else {}
f = ROOT / "web/public/data/city.json"
f.write_text(json.dumps(dict(species=species, city_summer_pct=city, barris=out), separators=(",", ":")), encoding="utf-8")
print(f"wrote {f} ({f.stat().st_size / 1024:.0f} KB): {len(out)} barris, {sum('trees' in v for v in out.values())} with trees;"
      f" no layout export for {len(missing)}: {missing[:8]}{'...' if len(missing) > 8 else ''}")
