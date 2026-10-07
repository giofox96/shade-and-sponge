"""Step 3: download open-access PDFs for the shortlist into papers/.

Usage: python scripts/fetch_pdfs.py
Input: notes/lit/shortlist.csv (column openalex). Tries every OA location OpenAlex knows.
Output: PDFs in papers/, status column written back to notes/lit/shortlist.csv,
        paywalled items listed in notes/lit/to_get_manually.md (get them via Zotero / university access).
"""
import csv, re, time, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
SL = ROOT / "notes" / "lit" / "shortlist.csv"
PAPERS = ROOT / "papers"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}


def landing_pdf(url):
    """Repository landing pages usually expose <meta name="citation_pdf_url">."""
    try:
        html = requests.get(url, headers=UA, timeout=30).text
    except requests.RequestException:
        return None
    m = re.search(r'name="citation_pdf_url"\s+content="([^"]+)"', html)
    return m.group(1) if m else None


def s2_pdf(doi):
    if not doi:
        return None
    try:
        d = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi.replace('https://doi.org/', '')}",
                         params={"fields": "openAccessPdf"}, timeout=30).json()
        return (d.get("openAccessPdf") or {}).get("url") or None
    except (requests.RequestException, ValueError):
        return None


def fname(w):
    a = w["authorships"][0]["author"]["display_name"].split()[-1] if w["authorships"] else "Anon"
    t = re.sub(r"[^\w\s-]", "", w["display_name"])[:60].strip()
    return f"{a} {w['publication_year']} - {t}.pdf"


def try_pdf(url):
    try:
        r = requests.get(url, headers=UA, timeout=60, allow_redirects=True)
        return r.content if r.ok and r.content[:4] == b"%PDF" else None
    except requests.RequestException:
        return None


rows = list(csv.DictReader(SL.open(encoding="utf-8")))
for r in rows:
    if r.get("status"):  # already tried; clear the cell to retry
        continue
    w = requests.get(f"https://api.openalex.org/works/{r['openalex']}", timeout=60).json()
    urls = [l.get("pdf_url") for l in w.get("locations", []) if l.get("pdf_url")]
    pdf = next((p for p in map(try_pdf, urls) if p), None)
    if not pdf:  # fallbacks: repository landing pages, then Semantic Scholar
        lands = [l["landing_page_url"] for l in w.get("locations", [])
                 if l.get("landing_page_url") and "doi.org" not in l["landing_page_url"]]
        extra = [u for u in map(landing_pdf, lands) if u] + [s2_pdf(r["doi"])]
        pdf = next((p for p in map(try_pdf, filter(None, extra)) if p), None)
    if pdf:
        name = fname(w)
        (PAPERS / name).write_bytes(pdf)
        r["status"], r["file"] = "ok", name
    else:
        r["status"], r["file"] = "manual", ""
    print(r["status"], r["title"][:80])
    time.sleep(0.3)

with SL.open("w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader()
    wr.writerows(rows)
manual = [f"- [T{r['tier']}] {r['first_author']} ({r['year']}). {r['title']}. {r['doi']}"
          for r in sorted(rows, key=lambda r: r["tier"]) if r["status"] == "manual"]
(ROOT / "notes" / "lit" / "to_get_manually.md").write_text(
    "# Paywalled or no OA PDF found: get via Zotero / university access, save in papers/\n\n" + "\n".join(manual) + "\n",
    encoding="utf-8")
