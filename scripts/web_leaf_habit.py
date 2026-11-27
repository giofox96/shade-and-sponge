"""Leaf habit of every tree species the web app draws: python scripts/web_leaf_habit.py
Writes web/public/data/leaf_habit.json ({species: deciduous | evergreen | semi-deciduous}) from, in order:
the palette's leaf_habit (meta.json), the monthly leaf-on share in meta.json leaf_by_species (ASSUMPTION: min >= 0.9 evergreen,
min <= 0.3 deciduous, otherwise semi-deciduous), and databases/traits/leaf_habit_extra.csv (street and park species with no phenology
row, each with its source, checked 27 Nov 2026). Species found nowhere stay out of the file and are drawn as unknown;
the app also matches a cultivar to its species (first two words)."""
import json, glob, pathlib, csv
ROOT = pathlib.Path(__file__).resolve().parents[1]
norm = lambda h: "evergreen" if "evergreen" in h else "semi-deciduous" if "semi" in h else "deciduous"
out = {}
for f in sorted(glob.glob(str(ROOT / "web/public/data/*/meta.json"))):
    m = json.load(open(f, encoding="utf-8"))
    for s, leaf in m.get("leaf_by_species", {}).items():
        out.setdefault(s, "evergreen" if min(leaf) >= 0.9 else "deciduous" if min(leaf) <= 0.3 else "semi-deciduous")
    for p in m["palette"]:
        if p.get("leaf_habit"):
            out[p["species"]] = norm(p["leaf_habit"])
for r in csv.DictReader(open(ROOT / "databases/traits/leaf_habit_extra.csv", encoding="utf-8")):
    out.setdefault(r["species"], r["habit"])
assert set(out.values()) <= {"deciduous", "evergreen", "semi-deciduous"}
json.dump(dict(sorted(out.items())), open(ROOT / "web/public/data/leaf_habit.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "species")
