"""Add papers by DOI to a Zotero collection through the Zotero Web API.

Usage: python scripts/zotero_add.py <collectionKey> [doi_file]
Reads ZOTERO_API_KEY / ZOTERO_USER_ID from the environment (never printed). Skips DOIs already in the library.
Metadata: Crossref; abstract from OpenAlex when Crossref has none. PDFs are not uploaded:
in Zotero select the items -> right-click -> "Find Available PDFs".
"""
import os, re, sys, html, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
COLL = sys.argv[1]
DOIS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "notes/lit/zotero_import_dois.txt"
KEY, UID = os.environ["ZOTERO_API_KEY"], os.environ["ZOTERO_USER_ID"]
API = f"https://api.zotero.org/users/{UID}"
H = {"Zotero-API-Key": KEY, "Zotero-API-Version": "3"}
TYPES = {"journal-article": "journalArticle", "book-chapter": "bookSection", "proceedings-article": "conferencePaper",
         "posted-content": "preprint", "book": "book", "report": "report"}
FIELDS = {"journalArticle": "publicationTitle", "bookSection": "bookTitle", "conferencePaper": "proceedingsTitle",
          "preprint": "repository", "report": "institution"}


def existing_dois():
    out, start = set(), 0
    while True:
        r = requests.get(f"{API}/items/top", headers=H, params={"format": "json", "limit": 100, "start": start}, timeout=60)
        r.raise_for_status()
        items = r.json()
        out |= {(i["data"].get("DOI") or "").lower() for i in items}
        if len(items) < 100:
            return out
        start += 100


def item(doi):
    m = requests.get(f"https://api.crossref.org/works/{doi}", timeout=60).json()["message"]
    t = TYPES.get(m.get("type"), "journalArticle")
    d = m.get("published-print") or m.get("published-online") or m.get("issued") or {}
    date = "-".join(str(x).zfill(2) for x in (d.get("date-parts") or [[None]])[0] if x)
    ab = re.sub(r"<[^>]+>", "", html.unescape(m.get("abstract", ""))).strip()
    if not ab:
        w = requests.get(f"https://api.openalex.org/works/doi:{doi}", timeout=60).json()
        inv = w.get("abstract_inverted_index") or {}
        ab = " ".join(x for _, x in sorted((i, k) for k, v in inv.items() for i in v))
    it = {"itemType": t, "title": (m.get("title") or [""])[0], "date": date, "DOI": doi,
          "url": f"https://doi.org/{doi}", "abstractNote": ab, "collections": [COLL],
          "creators": [{"creatorType": "author", "firstName": a.get("given", ""), "lastName": a.get("family", a.get("name", ""))}
                       for a in m.get("author", [])]}
    if t in FIELDS and m.get("container-title"):
        it[FIELDS[t]] = m["container-title"][0]
    if t in ("journalArticle", "bookSection", "conferencePaper"):
        it.update({k: m.get(s, "") for k, s in (("volume", "volume"), ("pages", "page"))})
    if t == "journalArticle":
        it["issue"] = m.get("issue", "")
    return it


dois = [l.strip().lower() for l in DOIS.read_text(encoding="utf-8").splitlines() if l.strip().startswith("10.")]
have = existing_dois()
todo = [d for d in dois if d not in have]
print(f"{len(dois)} DOIs, {len(dois) - len(todo)} already in library, adding {len(todo)}")
items, failed = [], []
for d in todo:
    try:
        items.append(item(d))
    except Exception as e:  # DOI unknown to Crossref (e.g. DataCite) -> report, do not guess
        failed.append(f"{d} ({type(e).__name__})")
for i in range(0, len(items), 50):
    r = requests.post(f"{API}/items", headers=H, json=items[i:i + 50], timeout=120)
    r.raise_for_status()
    res = r.json()
    print(f"batch {i // 50 + 1}: {len(res.get('successful', {}))} added, {len(res.get('failed', {}))} failed")
    for k, v in res.get("failed", {}).items():
        print("  failed:", items[i + int(k)]["DOI"], v.get("message"))
for f in failed:
    print("  no Crossref record:", f)
