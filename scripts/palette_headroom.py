"""Cap headroom per species and Shannon diversity of Porta S0 / candidate S1 mixes (issue #9).

Usage: python scripts/palette_headroom.py
Inputs:  exchange/to_gh/porta_street_trees.csv (2,825 Porta street trees), databases/barcelona/species_coverage.csv
         (top-30 city species, denominator 140,404 trees), databases/barcelona/porta_recent_plantings.csv
Output:  databases/barcelona/palette_headroom.csv ; prints min plane replacements and Shannon values.
Headroom = cap - current trees of the species (replacement keeps the total constant). (a) Porta 15% of 2,825;
(b) city 15% of 140,404; (c) city 12% of 140,404. City counts exist only for the top-30 species (>= 588 trees).
Platanus trees incl. the 3 PLATANOR 'Vallis Clausa' are planes (as in bcn_lidar_porta.py is_plane).
"""
import re, math, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
CITY_N = 140404
SRC = "Porta: exchange/to_gh/porta_street_trees.csv; city: species_coverage.csv (top-30 only)"


def key(s):                                           # same cultivar stripping as species_coverage.norm
    n = re.sub(r"['‘’\"].*", "", s.lower())
    n = re.sub(r"\s+\S*®.*$", "", n)
    n = re.sub(r"\s+×\s+|\s+x\s+", " x ", n).strip()
    return " ".join(n.split()[:3] if " x " in n else n.split()[:2])


t = pd.read_csv(ROOT / "exchange/to_gh/porta_street_trees.csv")
t["k"] = t.species.map(key)
por = t.groupby("k").size()
cit = pd.read_csv(DB / "species_coverage.csv").set_index("species").trees
N = len(t)
cap = {"a": math.floor(0.15 * N), "b": math.floor(0.15 * CITY_N), "c": math.floor(0.12 * CITY_N)}
rows = []
for k in por.index.union(cit.index):
    p, c = int(por.get(k, 0)), cit.get(k)
    rows.append(dict(species=k, trees_porta=p, trees_city=c, headroom_a=cap["a"] - p,
                     headroom_b=None if pd.isna(c) else cap["b"] - int(c), headroom_c=None if pd.isna(c) else cap["c"] - int(c),
                     source=SRC + ("" if not pd.isna(c) else "; city count < 588 (outside top-30): headroom_b/c not computed")))
H = pd.DataFrame(rows).sort_values(["trees_porta", "trees_city"], ascending=False)
H.to_csv(DB / "palette_headroom.csv", index=False)
print("caps", cap, "Porta N", N)

pl, plc = int(por["platanus x acerifolia"]), int(cit["platanus x acerifolia"])
print(f"Porta planes {pl}; (a) min replace {pl - cap['a']}")
for s in "bc":
    ex = plc - cap[s]
    print(f"({s}) city excess {ex}; Porta alone cannot meet it; pro-rata Porta share (ASSUMPTION) {math.ceil(ex * pl / plc)}")


def shannon(counts):
    c = pd.Series(counts, dtype=float)
    p = c[c > 0] / c.sum()
    h = -(p * p.map(math.log)).sum()
    return round(float(h), 3), round(float(math.exp(h)), 2)


s0 = por.to_dict()
print("S0 species", len(s0), "H, expH", shannon(s0))
genus = pd.Series(s0).groupby(lambda k: k.split()[0]).sum()
print("S0 genus H, expH", shannon(genus), "max species share", round(max(s0.values()) / N, 3), "max genus share", round(genus.max() / N, 3))


def s1(mix):                                          # replace all planes by mix (fractional counts), report H and cap check
    c = {k: v for k, v in s0.items() if k != "platanus x acerifolia"}
    for k, w in mix.items():
        c[k] = c.get(k, 0) + w * pl
    over = {k: round(v) for k, v in c.items() if v > cap["a"]}
    g = pd.Series(c).groupby(lambda k: k.split()[0]).sum()
    return shannon(c), len(c), over, round(float(g.max() / N), 3)


rec = pd.read_csv(DB / "porta_recent_plantings.csv")
rec["k"] = rec.species.map(key)
rec = rec[rec.k != "platanus x acerifolia"].groupby("k").trees.sum()
palA = ["celtis australis", "melia azedarach", "pyrus calleryana", "jacaranda mimosifolia", "tipuana tipu", "brachychiton populneus"]
palB = ["celtis australis", "styphnolobium japonicum", "melia azedarach", "tipuana tipu"]
mixes = {"recent (non-plane, 2017+)": (rec / rec.sum()).to_dict(),
         "equal palette A (topic_decision 6 spp.)": {k: 1 / 6 for k in palA},
         "equal palette B (press 4 spp.)": {k: 1 / 4 for k in palB},
         "Porta proportions palette A": {k: s0[k] / sum(s0[x] for x in palA) for k in palA},
         "Porta proportions palette B": {k: s0.get(k, 0) / sum(s0.get(x, 0) for x in palB) for k in palB}}
for n, m in mixes.items():
    print(n, s1(m))
