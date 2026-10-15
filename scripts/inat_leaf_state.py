"""Leaf state of Tipuana tipu and Jacaranda mimosifolia per month, from iNaturalist "Leaves" annotations.

Remote substitute for field photos in Porta (user lives in Florence; notes/todo_manual.md).
Counts all observations, cultivated (captive) included since street trees are planted, per month of year, by annotation value (term 36 "Leaves":
37 Breaking Leaf Buds, 38 Green Leaves, 39 Colored Leaves, 40 No Live Leaves), plus all observations.
Places: Barcelona city (30022), Spain (6774), Portugal (7122), Italy (6973).
Output: databases/barcelona/inat_leaf_state.csv (one row per species x place x state x month).
"""
import csv, json, pathlib, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "databases/barcelona/inat_leaf_state.csv"
API = "https://api.inaturalist.org/v1/observations/histogram"
TAXA = {"Tipuana tipu": 121263, "Jacaranda mimosifolia": 77541}
PLACES = {"Barcelona": 30022, "Spain": 6774, "Portugal": 7122, "Italy": 6973}
STATES = {"all": None, "breaking_buds": 37, "green_leaves": 38, "colored_leaves": 39, "no_live_leaves": 40}


def month_counts(taxon, place, value):
    q = dict(taxon_id=taxon, place_id=place, interval="month_of_year", date_field="observed")
    if value:
        q.update(term_id=36, term_value_id=value)
    with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q), timeout=60) as r:
        res = json.load(r)["results"]["month_of_year"]
    time.sleep(1.1)  # iNaturalist asks for <= 1 request per second
    return [res.get(str(m), 0) for m in range(1, 13)]


rows = []
for sp, t in TAXA.items():
    for pl, p in PLACES.items():
        for st, v in STATES.items():
            for m, n in enumerate(month_counts(t, p, v), 1):
                rows.append(dict(species=sp, place=pl, state=st, month=m, n_obs=n))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"{OUT.name}: {len(rows)} rows (queried {time.strftime('%Y-%m-%d')})")
