"""Step 1: search OpenAlex per knowledge bucket and write a deduplicated candidate list.

Usage: python scripts/search_papers.py [queries.txt]
queries file format: one "bucket | query" per line (# for comments).
Output: notes/lit/candidates.csv
"""
import csv, sys, time, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "notes" / "lit" / (sys.argv[2] if len(sys.argv) > 2 else "candidates.csv")
QFILE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts" / "queries.txt"
PER_QUERY = 20


def abstract(inv):
    if not inv:
        return ""
    words = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in words)


def search(q):
    r = requests.get("https://api.openalex.org/works", params={
        "filter": f"title_and_abstract.search:{q},from_publication_date:2005-01-01,type:article|review",
        "sort": "relevance_score:desc", "per-page": PER_QUERY}, timeout=60)
    r.raise_for_status()
    return r.json()["results"]


rows = {}
for line in QFILE.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    bucket, q = (s.strip() for s in line.split("|", 1))
    for rank, w in enumerate(search(q)):
        key = w["id"]
        if key in rows:
            rows[key]["buckets"] += f";{bucket}"
            continue
        oa = w.get("best_oa_location") or {}
        rows[key] = {
            "openalex": key.rsplit("/", 1)[-1], "buckets": bucket, "rank": rank,
            "year": w.get("publication_year"), "cited": w.get("cited_by_count"),
            "first_author": (w["authorships"][0]["author"]["display_name"] if w["authorships"] else ""),
            "title": w.get("display_name"), "doi": w.get("doi") or "",
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
            "oa_pdf": oa.get("pdf_url") or "", "abstract": abstract(w.get("abstract_inverted_index"))[:1500],
        }
    print(f"{bucket:3} {len(rows):4}  {q}")
    time.sleep(0.2)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(next(iter(rows.values())).keys()))
    wr.writeheader()
    wr.writerows(sorted(rows.values(), key=lambda r: (r["buckets"], r["rank"])))
print(f"{len(rows)} candidates -> {OUT}")
