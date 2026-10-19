# RM seminar figures (parked, 19 Oct 2026)

Two figures made for the **Research and Methodologies** seminar, not for the thesis talk. They were figures `08` and `09` in `slides/fig/`; the user decided on 19 Oct to leave them out of the 20 Oct tutor presentation and come back to them later, so they live here and the talk figures are a clean `01-09` run.

| File | What it is | Script |
|---|---|---|
| `plane_tree_map.svg` / `.png` | RM homework 1: one Porta plane-tree position through eight stages, from the lived experience to the computed decision | `scripts/make_plane_tree_map.py` |
| `cluster_map.svg` / `.png` | Shared cluster map on the RM p. 37 template ("Before you draw: open up your topic"): this thesis (A) and a colleague's thesis (B) around one cluster topic. Thesis B and the centre text are **drafts to agree with her** | `scripts/make_cluster_map.py` |

Both scripts import `make_infographics.py` for the house style and write back into this folder. Regenerate with `python scripts/make_plane_tree_map.py` (and `make_cluster_map.py`) from `scripts/`.

**Open, when you pick this up again:** the RM deadline and format for both (not recorded), and whether thesis B's column is accepted by the colleague.
