"""Batch run over many barris (notes/citywide_plan.md §6.3): for each barri, LiDAR (scripts/bcn_lidar_barri.py), sidewalk
widths (scripts/porta_sidewalk_width.py) and the tool, scenario R with the options of Porta's reference run
(python -m shade_sponge "<barri>" --size=exact --trunk=TERCERA). Steps already done are skipped, so the batch can be
stopped and restarted; a failed step is logged and the batch moves on. Each step runs in its own process (memory).

Usage (PC, project env):  python scripts/run_barris.py                       # Eixample + Sant Martí (default)
                          python scripts/run_barris.py "Gràcia" "Sant Andreu"  # districts or barri names
                          python scripts/run_barris.py --summary               # only rebuild the summary table
                          python scripts/run_barris.py --osm                   # redo buildings + tool where footprints are LiDAR
Outputs: databases/barcelona/barris/run_log.csv, databases/barcelona/barris_summary.csv (one row per barri, shares of
today's S0: S1 random and S1a city mix = mean of 10 seeds, tool = the optimised layout with the most summer shade)."""
import re, sys, time, subprocess, pathlib, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]

DB = ROOT / "databases/barcelona"
TAG = "_sizeexact_trunkTERCERA"
DEFAULT = ["Eixample", "Sant Martí"]


def summary_file(s):
    return DB / f"tool_v0_summary_{s}{TAG}.csv"


def steps(name, s):
    d = DB / "barris" / s
    return [("lidar", d / "buildings.geojson", ["scripts/bcn_lidar_barri.py", name]),
            ("sidewalks", d / "sidewalk_width.csv", ["scripts/porta_sidewalk_width.py", name]),
            ("tool", summary_file(s), ["-m", "shade_sponge", name, "--size=exact", "--trunk=TERCERA"])]


def redo_osm(barris, log):
    """Barris whose buildings came from the LiDAR fallback (Overpass busy): fetch OSM footprints again and, if that
    works, rebuild the site cache and rerun the tool. Barris where Overpass still fails keep their LiDAR footprints."""
    for name, s in barris:
        f = DB / "barris" / s / "buildings.geojson"
        if not f.exists() or not re.search(r'"source": ?"lidar"', f.read_text(encoding="utf-8")[:2000]):
            continue
        for step, cmd in (("buildings_osm", ["scripts/bcn_lidar_barri.py", name, "--osm-only"]), ("tool", steps(name, s)[2][2])):
            t = time.time()
            print(f"\n=== {name}: {step} ===", flush=True)
            if step == "tool":
                (ROOT / f"cache/site_{s}.npz").unlink(missing_ok=True)
            r = subprocess.run([sys.executable, *cmd], cwd=ROOT)
            status = "ok" if r.returncode == 0 else f"failed ({r.returncode})"
            pd.DataFrame([dict(barri=name, step=step, status=status, minutes=round((time.time() - t) / 60, 1),
                               when=time.strftime("%Y-%m-%d %H:%M"))]).to_csv(log, mode="a", header=not log.exists(), index=False)
            if status != "ok":
                break


def summarise(barris):
    rows = []
    for name, s in barris:
        f = summary_file(s) if s != "porta" else DB / f"tool_v0_summary{TAG}.csv"
        if not f.exists():
            continue
        d = pd.read_csv(f)
        s0 = d.iloc[0]
        opt = d[d.scenario.str.startswith("S4_")]
        best = opt.loc[opt.shade_summer_m2h.idxmax()]
        row = dict(barri=name, canopy_s0=s0.canopy_pct, max_genus_s0=s0.max_genus, max_genus_pct_s0=s0.max_genus_pct)
        for k, x in (("random", d[d.scenario.str.startswith("S1_random")].mean(numeric_only=True)),
                     ("s1a", d[d.scenario.str.startswith("S1a")].mean(numeric_only=True)), ("tool", best)):
            row[f"summer_pct_{k}"] = round(100 * x.shade_summer_m2h / s0.shade_summer_m2h, 1)
            row[f"winter_pct_{k}"] = round(100 * x.shade_winter_m2h / s0.shade_winter_m2h, 1)
            row[f"runoff_hot_change_pct_{k}"] = round(100 * (x.runoff_hot_m3 / s0.runoff_hot_m3 - 1), 1)
        row["tool_margin_pts"] = round(row["summer_pct_tool"] - row["summer_pct_s1a"], 1)
        rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(DB / "barris_summary.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or DEFAULT
    idx = pd.read_csv(DB / "lidar_tiles_barris.csv").drop_duplicates("barri")
    sel = idx[idx.district.isin(args) | idx.barri.isin(args)]
    barris = [("Porta", "porta")] + list(zip(sel.barri, sel.slug))
    log = DB / "barris" / "run_log.csv"
    if "--osm" in sys.argv:
        redo_osm(barris[1:], log)
    elif "--summary" not in sys.argv:
        for name, s in barris[1:]:
            for step, done, cmd in steps(name, s):
                if done.exists():
                    continue
                t = time.time()
                print(f"\n=== {name}: {step} ===", flush=True)
                r = subprocess.run([sys.executable, *cmd], cwd=ROOT)
                status = "ok" if r.returncode == 0 and done.exists() else f"failed ({r.returncode})"
                pd.DataFrame([dict(barri=name, step=step, status=status, minutes=round((time.time() - t) / 60, 1),
                                   when=time.strftime("%Y-%m-%d %H:%M"))]).to_csv(log, mode="a", header=not log.exists(), index=False)
                if status != "ok":
                    print(f"*** {name}: {step} {status}; moving on to the next barri", flush=True)
                    break
    summarise(barris)
