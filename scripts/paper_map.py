"""Embedding map of the literature: where the papers cluster, where the gaps are, where the thesis falls.

Two representations of the same papers, reduced with the same UMAP settings so the maps can be compared:
  1. text  : title + abstract -> SPECTER2 (allenai/specter2_base, CLS token; free, trained on citation links).
             The base model is used without the proximity adapter (no extra `adapters` dependency); ASSUMPTION
             that this is close enough for a visual map.
  2. tags  : the matrix's `bucket` column (B1..B9), one-hot. Shows whether our tags see the same affinities.
A chat model cannot compute an embedding, so everything here is computed, nothing is asked of an LLM.

Inputs
  notes/lit/literature_matrix.csv      the matrix (id, citation, doi, bucket, method, key_quantified_results, ...)
  notes/lit/{shortlist,candidates*}.csv abstracts already fetched by search_papers.py (joined on DOI)
  OpenAlex                             title + abstract for the rest (cached in notes/lit/matrix_abstracts.csv)
  notes/lit/paper_map_extra.csv        extra points: kind=thesis (label, owner, title, text) or kind=core (doi, owner;
                                       with label, title, text = abstract it is added as a new paper if not in the matrix)
Papers with no abstract anywhere fall back to citation + method + results from the matrix (flagged `text_src`).

Outputs
  notes/lit/paper_map_coords.csv       per paper: 2D + 3D UMAP (text and tags), cluster, flags -> Grasshopper
  notes/lit/paper_map_neighbours.csv   the K nearest papers to each thesis (cosine, full 768-d space)
  notes/lit/paper_map_clusters.md      cluster members, to label (by hand or LLM, from the abstracts)
  notes/figures/paper_map.html         interactive Plotly page, 2D + 3D, text vs tags
Run: python scripts/paper_map.py   (needs torch, transformers, umap-learn, scikit-learn; ~2 min on CPU)
"""
import json
import pathlib
import time

import numpy as np
import pandas as pd
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIT = ROOT / "notes" / "lit"
CACHE = LIT / "matrix_abstracts.csv"
MODEL = "allenai/specter2_base"
SEED = 42
K_NEIGH = 10
N_NEIGHBORS = 12   # UMAP; ASSUMPTION: ~sqrt(n) for n ~ 140, small enough to keep local structure


def norm_doi(d):
    return str(d).lower().replace("https://doi.org/", "").strip() if pd.notna(d) else None


def openalex(doi):
    r = requests.get(f"https://api.openalex.org/works/doi:{doi}",
                     params={"select": "title,abstract_inverted_index"}, timeout=30)
    if r.status_code != 200:
        return None, None
    j = r.json()
    inv = j.get("abstract_inverted_index") or {}
    words = sorted((p, w) for w, ps in inv.items() for p in ps)
    return j.get("title"), " ".join(w for _, w in words) or None


def load_papers():
    m = pd.read_csv(LIT / "literature_matrix.csv")
    m["doi_n"] = m.doi.map(norm_doi)
    local = pd.concat(pd.read_csv(LIT / f"{f}.csv") for f in ["shortlist", "candidates", "candidates_2", "candidates_heat"])
    local["doi_n"] = local.doi.map(norm_doi)
    local = local.dropna(subset=["doi_n"]).drop_duplicates("doi_n").set_index("doi_n")
    cache = pd.read_csv(CACHE).set_index("doi_n") if CACHE.exists() else pd.DataFrame(columns=["title", "abstract"])
    rows = []
    for d in m.doi_n:
        if d is None:
            rows.append((None, None, None))
        elif d in cache.index:
            rows.append((d, cache.at[d, "title"], cache.at[d, "abstract"]))
        else:
            t, a = openalex(d)
            if d in local.index:
                t = t or local.at[d, "title"]
                a = a or (local.at[d, "abstract"] if pd.notna(local.at[d, "abstract"]) else None)
            rows.append((d, t, a))
            time.sleep(0.1)
    fetched = pd.DataFrame(rows, columns=["doi_n", "title", "abstract"])
    fetched.dropna(subset=["doi_n"]).drop_duplicates("doi_n").to_csv(CACHE, index=False)
    m["title"] = fetched.title.fillna(m.citation).values
    m["abstract"] = fetched.abstract.values
    has = m.abstract.notna() & (m.abstract.str.len() > 200)
    m["text_src"] = np.where(has, "abstract", "matrix")
    fallback = m.method.fillna("") + ". " + m.key_quantified_results.fillna("")
    m["text"] = m.title + " [SEP] " + np.where(has, m.abstract, fallback)
    m["kind"], m["owner"] = "paper", ""
    return m


def add_extra(m):
    f = LIT / "paper_map_extra.csv"
    if not f.exists():
        return m
    x = pd.read_csv(f).fillna("")
    for _, r in x[x.kind == "core"].iterrows():                # highlight an existing paper
        sel = m.doi_n == norm_doi(r.doi)
        m.loc[sel, "kind"], m.loc[sel, "owner"] = "core", r.owner
    new = x[(x.kind == "core") & (x.text != "") & ~x.doi.map(norm_doi).isin(m.doi_n.dropna())]  # a cluster mate's paper not in our matrix
    ext = pd.concat([x[x.kind == "thesis"].assign(text_src="thesis", bucket="thesis"),
                     new.assign(text_src="abstract", bucket=new.owner)])
    ext = ext.assign(citation=ext.label, text=ext.title + " [SEP] " + ext.text)
    return pd.concat([m, ext[["kind", "owner", "title", "citation", "doi", "text", "text_src", "bucket"]]], ignore_index=True)


def embed(texts):
    import torch
    from transformers import AutoModel, AutoTokenizer
    tok, mod = AutoTokenizer.from_pretrained(MODEL), AutoModel.from_pretrained(MODEL).eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(texts), 16):
            b = tok([t.replace("[SEP]", tok.sep_token) for t in texts[i:i + 16]],
                    padding=True, truncation=True, max_length=512, return_tensors="pt")
            out.append(mod(**b).last_hidden_state[:, 0].numpy())
    e = np.vstack(out)
    e -= e.mean(axis=0)   # raw CLS vectors share one dominant direction (all cosines ~0.94); centring removes it
    return e / np.linalg.norm(e, axis=1, keepdims=True)


def reduce(x, dim, metric):
    import umap
    return umap.UMAP(n_components=dim, n_neighbors=N_NEIGHBORS, min_dist=0.1, metric=metric,
                     random_state=SEED).fit_transform(x)


def knn_overlap(a, b, k=K_NEIGH):
    """Mean Jaccard of each paper's k nearest neighbours in two spaces (1 = same neighbours, ~k/n = random)."""
    from sklearn.neighbors import NearestNeighbors
    ia = NearestNeighbors(n_neighbors=k + 1, metric="cosine").fit(a).kneighbors(a)[1][:, 1:]
    ib = NearestNeighbors(n_neighbors=k + 1, metric="cosine").fit(b).kneighbors(b)[1][:, 1:]
    return float(np.mean([len(set(p) & set(q)) / len(set(p) | set(q)) for p, q in zip(ia, ib)]))


def clusters(e):
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import silhouette_score
    # Ward on unit vectors (euclidean ~ cosine); k = best silhouette in 4-10
    fit = {k: AgglomerativeClustering(k, linkage="ward").fit_predict(e) for k in range(4, 11)}
    return fit[max(fit, key=lambda k: silhouette_score(e, fit[k]))]


def tag_matrix(buckets):
    tags = buckets.fillna("").str.split("/")
    cols = sorted({t for ts in tags for t in ts if t})   # B1..B9, "thesis", or a cluster mate's name
    x = np.array([[float(c in ts) for c in cols] for ts in tags])
    return x + 1e-6, cols   # epsilon: cosine needs non-zero rows (two papers have no bucket)


def main():
    p = add_extra(load_papers())
    print(f"{len(p)} points; text source: {p.text_src.value_counts().to_dict()}")
    e = embed(p.text.tolist())
    t, cols = tag_matrix(p.bucket)
    paper = (p.kind != "thesis").values
    p["cluster"] = -1
    p.loc[paper, "cluster"] = clusters(e[paper])
    for name, x, metric in [("text", e, "cosine"), ("tags", t, "cosine")]:
        p[[f"{name}_x2", f"{name}_y2"]] = reduce(x, 2, metric)
        p[[f"{name}_x3", f"{name}_y3", f"{name}_z3"]] = reduce(x, 3, metric)
    ov = knn_overlap(e[paper], t[paper])
    print(f"text vs tags, {K_NEIGH}-NN overlap (Jaccard): {ov:.2f}  (random ~{K_NEIGH / paper.sum():.2f})")

    p["id"] = p.id.astype("Int64")
    keep = ["id", "kind", "owner", "citation", "title", "doi", "bucket", "cluster", "text_src"]
    coords = [c for c in p.columns if c.startswith(("text_", "tags_")) and c != "text_src"]
    p[keep + coords].to_csv(LIT / "paper_map_coords.csv", index=False, float_format="%.4f")

    nb = []
    for i in np.where(~paper)[0]:
        sim = e[paper] @ e[i]
        for r, j in enumerate(np.argsort(-sim)[:K_NEIGH], 1):
            q = p[paper].iloc[j]
            nb.append({"thesis": p.citation.iloc[i], "rank": r, "cosine": round(float(sim[j]), 3),
                       "id": None if pd.isna(q.id) else int(q.id), "citation": q.citation, "cluster": int(q.cluster)})
    pd.DataFrame(nb).to_csv(LIT / "paper_map_neighbours.csv", index=False)

    with open(LIT / "paper_map_clusters.md", "w", encoding="utf-8") as f:
        f.write("# Paper map clusters (generated by scripts/paper_map.py; labels go in paper_map_labels.csv)\n")
        for c, g in p[paper].groupby("cluster"):
            f.write(f"\n## Cluster {c} ({len(g)} papers)\n" + "".join(f"- #{r.id} {r.citation}\n" for r in g.itertuples()))

    lab = LIT / "paper_map_labels.csv"
    labels = pd.read_csv(lab).set_index("cluster").label.to_dict() if lab.exists() else {}
    write_html(p, labels, ov, nb)


def write_html(p, labels, overlap, near):
    pts = [{"title": r.title, "cit": r.citation, "kind": r.kind, "owner": r.owner, "bucket": str(r.bucket),
            "cl": int(r.cluster), "src": r.text_src,
            **{c: round(float(getattr(r, c)), 3) for c in p.columns if c.startswith(("text_", "tags_")) and c != "text_src"}}
           for r in p.itertuples()]
    tpl = (ROOT / "scripts" / "paper_map_template.html").read_text(encoding="utf-8")
    out = tpl.replace("/*DATA*/null", json.dumps({"pts": pts, "labels": {str(k): v for k, v in labels.items()},
                                                   "overlap": round(overlap, 2), "near": near}, default=str))
    (ROOT / "notes" / "figures" / "paper_map.html").write_text(out, encoding="utf-8")
    print("wrote notes/figures/paper_map.html")


if __name__ == "__main__":
    main()
