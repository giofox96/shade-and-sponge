---
name: lit-review
description: Search, screen, fetch, digest and synthesise papers for the thesis, then update the literature matrix and the problem / research question / hypothesis. Use when the user asks to find new papers, extend the literature review, or re-check the topic against the evidence.
---

# Literature workflow (search → screen → fetch → digest → extract → synthesise)

Follow CLAUDE.md rules: English only, never invent citations or numbers, mark abstract-only claims "(abs)".

1. **Queries.** Write `scripts/queries_<topic>.txt`, one `bucket | query` per line (buckets B1–B6 as in CLAUDE.md). Use short keyword queries (3–6 words); OpenAlex matches title + abstract.
2. **Search.** `python scripts/search_papers.py scripts/queries_<topic>.txt candidates_<topic>.csv` writes `notes/lit/candidates_<topic>.csv` (title, year, citations, OA PDF link, abstract). Do not send the user's email to any API.
3. **Screen.** Print id | year | citations | OA | title | first 200 characters of the abstract (set `PYTHONIOENCODING=utf-8`). Keep only papers that inform the problem, gap, method or validation. Mark tier 1 (must read) and tier 2 (abstract is enough). Append them to `notes/lit/shortlist.csv`, skipping ones already listed.
4. **Fetch.** `python scripts/fetch_pdfs.py` saves open-access PDFs into `papers/` and lists the rest in `notes/lit/to_get_manually.md`. MDPI and most publishers block scripts; the user gets those via Zotero or university access. Do not bypass paywalls.
5. **Digest.** `python scripts/digest_pdfs.py` writes `notes/lit/digest/*.md` (abstract, conclusions, numeric sentences) per PDF. Read digests, not full texts. Open `notes/lit/text/*.txt` with grep only for specific facts (data sources, parameters). For tier-1 papers without a PDF, use the abstract from `shortlist.csv`. If it is empty, use the Semantic Scholar `abstract` field.
6. **Extract.** Add one row per paper to `notes/lit/literature_matrix.csv` with these columns: citation, doi, file, read_level, bucket, location, method, traits/metrics, key quantified results, limits, relevance. Copy numbers exactly as written in the source.
7. **Synthesise.** Update `notes/topic_decision.md`: the evidence per known weakness, the option scores (CLAUDE.md criteria), then problem statement, research question and hypothesis with citations. Data consequences go into `databases/data_inventory.md`.
8. **Report.** Tell the user what changed in the PS/RQ/H, which claims rest on abstracts only, and which full texts they need to fetch.
