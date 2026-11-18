# Thesis text

Markdown chapters, built with Pandoc. Citations come from Zotero in **Harvard** (IAAC rule, 17 Nov).

- `outline.md` gives the chapter plan, mapped to `notes/`, with the status of each section.
- Chapters are named `01_introduction.md`, `02_background_trees.md`, … and are added as they are drafted.
- `metadata.yaml` holds the title, author, bibliography and citation style.

## One-time setup (user)
1. **Pandoc:** `conda install -n shade-and-sponge -c conda-forge pandoc`. For a PDF you also need a LaTeX engine (e.g. MiKTeX); for Word you need nothing more.
2. **Bibliography:** in Zotero, right-click the `THESIS_MACAD` collection → *Export Collection…* → **Better BibTeX**, tick *Keep updated*, and save it as `thesis/references.bib`. Commit that file.
3. **Style:** save the Harvard CSL file as `thesis/harvard-cite-them-right.csl` (citation-style-language/styles on GitHub). Commit it.

## Cite
Use Better BibTeX keys: `[@anys2024]` → (Anys and Weiler, 2024); `@anys2024` → Anys and Weiler (2024); `[@anys2024, p. 5]`.

## Build
From the repository root:
```bash
pandoc thesis/metadata.yaml thesis/0*.md --citeproc -o thesis/build/thesis.docx
```
Add `-o thesis/build/thesis.pdf` for a PDF (needs LaTeX). The `build/` folder is gitignored.

## Layout (DesignCraft, IAAC A4)
Tables and figures are labelled and numbered per chapter: caption `: Text {#tbl:name}`, figure `![Text](path){#fig:name}`, reference `@tbl:name` / `@fig:name` (→ "Table 3.1"). `thesis/layout/number_refs.py` resolves them; `thesis/layout/build_layout.py` lays the chapters out in two columns with contents and a list of tables and figures (usage in its docstring).
