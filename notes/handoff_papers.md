# Handoff to the local session (12 Oct 2026)

Run this from the Windows project folder (`1_THESIS_PROJECT`), where `papers/` and the Zotero MCP exist. First `git pull` on branch `claude/optimistic-cannon-0adgxq` (PR #32).

## Task
The user added new PDFs to `papers/` on the Omen. Do, in this order:
1. **Duplicates:** compare every PDF in `papers/` by SHA-256 and by DOI (`pdftotext` first page). Same hash = exact duplicate; same DOI, different hash = another version. List them and ask before deleting anything.
2. **Rename** to `Author Year - Short title.pdf`, as in `notes/lit/literature_matrix.csv` column `file_in_papers`.
3. **Zotero:** write the new DOIs to a text file (one per line) and run `python scripts/zotero_add.py R2AH2P65 <file>` (collection THESIS_MACAD; duplicates are skipped). Remind the user to run "Find Available PDFs" in Zotero.
4. **Matrix:** set `file_in_papers` for rows already in the matrix.

## Context from the cloud session
- The matrix has 93 rows. Rows 4, 8, 34, 38, 45 were read in full on 12 Oct from the uploaded PDFs; rows 88-93 are six uploads (Chen 2026, Hu 2026, Xue 2026, Tilly 2025, Faisal 2026, Bouaziz 2026). Their `file_in_papers` still says "uploaded 12 Oct, not in papers/".
- The 18 earlier uploads were 15 distinct papers: Grey 2018, Thom 2020 and Dowtin 2023 were each uploaded twice.
- Rahman et al. 2020 (online Dec 2019) is cited in the notes as "Rahman 2019"; keep the file name consistent with the year printed in the PDF.
- Not read yet: Speak 2020 (`10.1016/j.landurbplan.2020.103748`).

## Status (12 Oct, local session)
- **Done:** 11 PDFs renamed (rows 4, 8, 34, 38, 45 and 88-93); `file_in_papers` set for rows 38 (now `Rahman 2020 - ...`, the year printed in the PDF) and 88-93; the other five already carried the target names. Zotero: 15 DOIs from the batch sent to collection THESIS_MACAD, 6 added, 9 already in the library (run "Find Available PDFs").
- **Pending the user's OK (nothing deleted yet):** re-downloads of papers already named in `papers/`. Same bytes: the unnamed copies of Baptista 2018, Xiao 2016 and the soil-infiltration paper (keep the file the matrix names). Same DOI and identical extracted text, different bytes: the `1-s2.0-...` copies of Grey 2018 (2), Thom 2020 (2), Dowtin 2023 (`(1)`), Tan 2026 and `atmosphere-09-00012-v2.pdf` (Santos Nouri 2018), plus one of the two "Urban Forest and Ecosystem Services" files (different text, check first). Deleting the unnamed copies also leaves stale `notes/lit/digest/*.md`, `to_get_manually.md` and `todo_manual.md` entries.
- **Not read yet:** Speak 2020 (`10.1016/j.landurbplan.2020.103748`), no PDF in `papers/`.
