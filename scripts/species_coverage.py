"""Which of a city's most common tree species have measured runoff / heat parameters?

Usage: python scripts/species_coverage.py [florence|barcelona] [top_n]
Downloads the municipal tree inventory once (databases/<city>/), ranks species, and joins:
  - notes/lit/species_measurements.csv  (interception / storage / transpiration / shade values from papers)
  - databases/TRY_DATABASE/Tree_Trait_Task_Force_BDD_1.3.txt  (3TF leaf/wood traits)
Output: databases/<city>/species_coverage.csv
"""
import csv, re, sys, json, pathlib, collections, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
CITY = sys.argv[1] if len(sys.argv) > 1 else "florence"
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 30
SRC = {
    "florence": ("https://data.comune.fi.it/datastore/download.php?id=6370&type=99&format=url&file_format=geojson&file_id=23066", "alberi.geojson"),
    "barcelona": ("https://opendata-ajuntament.barcelona.cat/data/dataset/27b3f8a7-e536-4eea-b025-ce094817b2bd/resource/23124fd5-521f-40f8-85b8-efb1e71c2ec8/download", "arbrat_viari.csv"),
}
# inventory name -> accepted name used in trait sources
SYN = {"quercus pedunculata": "quercus robur", "sophora japonica": "styphnolobium japonicum",
       "platanus x hispanica": "platanus x acerifolia", "platanus acerifolia": "platanus x acerifolia",
       "tilia intermedia": "tilia x europaea", "ulmus carpinifolia": "ulmus minor", "pyrus calleriana": "pyrus calleryana"}


def norm(name):
    n = re.sub(r"['‘’\"].*", "", (name or "").lower())        # drop cultivar names
    n = re.sub(r"\(.*?\)|\bvar\..*|\bsubsp\..*|\bspp?\.?$", "", n)
    n = re.sub(r"\s+×\s+|\s+x\s+", " x ", n).strip()
    n = " ".join(n.split()[:3] if " x " in n else n.split()[:2])
    return SYN.get(n, n)


def inventory():
    url, fname = SRC[CITY]
    path = ROOT / "databases" / CITY / fname
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(requests.get(url, timeout=600).content)
    if fname.endswith(".geojson"):
        feats = json.loads(path.read_text(encoding="utf-8"))["features"]
        return [(f["properties"].get("SPECIE"), f["properties"].get("CIRCONF_CM")) for f in feats]
    with path.open(encoding="utf-8") as f:
        return [(r["cat_nom_cientific"], None) for r in csv.DictReader(f) if r["tipus_element"] == "ARBRE VIARI"]


trees = inventory()
count, circ = collections.Counter(), collections.defaultdict(list)
for sp, c in trees:
    k = norm(sp)
    if len(k.split()) < 2:
        k = (k or "unknown") + " (genus only)"
    count[k] += 1
    if c:
        circ[k].append(float(c))

meas = collections.defaultdict(list)
for r in csv.DictReader((ROOT / "notes/lit/species_measurements.csv").open(encoding="utf-8")):
    meas[norm(r["species"])].append(r)
ttf = collections.defaultdict(set)
with (ROOT / "databases/TRY_DATABASE/Tree_Trait_Task_Force_BDD_1.3.txt").open(encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f, delimiter=";"):
        ttf[norm(r["FinalName"])].add(r["TraitAcc"])

out, total = [], len(trees)
for sp, n in count.most_common(TOP):
    genus = sp.split()[0]
    m = meas.get(sp, [])
    g = [r for k, v in meas.items() if k.split()[0] == genus and k != sp for r in v]
    out.append({
        "species": sp, "trees": n, "share_%": round(100 * n / total, 1),
        "mean_circumference_cm": round(sum(circ[sp]) / len(circ[sp])) if circ[sp] else "",
        "runoff_measured": "; ".join(sorted({f"{r['measure']} ({r['source']})" for r in m if r["objective"] == "runoff"})),
        "heat_measured": "; ".join(sorted({f"{r['measure']} ({r['source']})" for r in m if r["objective"] == "heat"})),
        "same_genus_only": "; ".join(sorted({f"{r['species']} {r['objective']}" for r in g})) if not m else "",
        "3TF_traits": ",".join(sorted(ttf.get(sp, []))),
    })

dst = ROOT / "databases" / CITY / "species_coverage.csv"
with dst.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
covered = sum(r["trees"] for r in out if r["runoff_measured"] or r["heat_measured"])
both = sum(r["trees"] for r in out if r["runoff_measured"] and r["heat_measured"])
print(f"{CITY}: {total} trees; top {TOP} species = {sum(r['trees'] for r in out)} trees "
      f"({100 * sum(r['trees'] for r in out) / total:.0f}%)")
print(f"  species-level runoff or heat value: {covered} trees ({100 * covered / total:.0f}%); both: {both} ({100 * both / total:.0f}%)")
print(f"-> {dst}")
