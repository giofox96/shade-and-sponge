# Thesis text

Markdown chapters, built with Pandoc. Citations come from Zotero in **APA 7** (no IAAC/UdL style rule found, 26 Oct; confirm with the tutor).

- `outline.md` gives the chapter plan, mapped to `notes/`, with the status of each section.
- Chapters are named `01_introduction.md`, `02_background_trees.md`, … and are added as they are drafted.
- `metadata.yaml` holds the title, author, bibliography and citation style.

## One-time setup (user)
1. **Pandoc:** `conda install -n shade-and-sponge -c conda-forge pandoc`. For a PDF you also need a LaTeX engine (e.g. MiKTeX); for Word you need nothing more.
2. **Bibliography:** in Zotero, right-click the `THESIS_MACAD` collection → *Export Collection…* → **Better BibTeX**, tick *Keep updated*, and save it as `thesis/references.bib`. Commit that file.
3. **Style:** save the APA 7 CSL file as `thesis/apa.csl`. It is `apa.csl` in the Zotero Style Repository / citation-style-language/styles on GitHub. Commit it.

## Cite
Use Better BibTeX keys: `[@anys2024]` → (Anys & Weiler, 2024); `@anys2024` → Anys and Weiler (2024); `[@anys2024, p. 5]`.

## Build
From the repository root:
```bash
pandoc thesis/metadata.yaml thesis/0*.md --citeproc -o thesis/build/thesis.docx
```
Add `-o thesis/build/thesis.pdf` for a PDF (needs LaTeX). The `build/` folder is gitignored.
