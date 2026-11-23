"""Co-benefits for the web app: python scripts/web_export_cobenefits.py
Adds a `cobenefits` entry to web/public/data/porta-barcelona/meta.json from scripts/cobenefits.py's outputs
(databases/barcelona/cobenefits_porta.csv and, if present, the diversity-floor runs cobenefits_porta_div<floor>.csv).
Those were computed on the Barcelona-palette, TERCERA layouts, so only that web site gets them. Reported indicators,
not optimised (notes/cobenefits_plan.md). Run after `python -m shade_sponge.web_export` (it rewrites meta.json)."""
import json, pathlib, re, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, META = ROOT / "databases/barcelona", ROOT / "web/public/data/porta-barcelona/meta.json"


def rows(f, tag=""):
    d = pd.read_csv(f).set_index("scenario")
    # summer shade, % of today, from the tool run that made these layouts (tool_v0_summary_barcelona<tag>_..._TERCERA.csv)
    sm = DB / f"tool_v0_summary_barcelona{tag}_sizeexact_trunkTERCERA.csv"
    sh = pd.read_csv(sm).set_index("scenario").shade_summer_m2h if sm.exists() else None
    return {s: dict(eff_species=round(r.eff_species, 1), pollen_lo=round(r.pollen_load_pct_S0, 1),
                    pollen_hi=round(r.pollen_max_pct_S0, 1), pollen_cov=round(r.pollen_coverage_pct, 1),
                    carbon=round(r.carbon_t_pct_S0, 1),
                    summer=None if sh is None or s not in sh else round(100 * sh[s] / sh["S0_current"], 1)) for s, r in d.iterrows()}


tags = {re.search(r"_div([\d.]+)$", f.stem).group(1): f for f in DB.glob("cobenefits_porta_div*.csv")}
entry = dict(base=rows(DB / "cobenefits_porta.csv"),
             floors={k: rows(tags[k], f"_div{k}") for k in sorted(tags, key=float)})
meta = json.load(open(META, encoding="utf-8"))
meta["cobenefits"] = entry
json.dump(meta, open(META, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(META, len(entry["base"]), "scenarios, floors", list(entry["floors"]))
