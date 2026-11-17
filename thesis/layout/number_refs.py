"""Number tables and figures per chapter and resolve @tbl:/@fig: references.

Usage: python thesis/layout/number_refs.py OUT.md thesis/02_*.md thesis/03_*.md ...
Chapter number = the file name's numeric prefix. Labels:
  table caption  ": Caption text {#tbl:name}"
  figure         "![Caption text](path){#fig:name}"
  reference      "@tbl:name" / "@fig:name"  ->  "Table 3.1" / "Figure 3.1"
"""
import re
import sys
from pathlib import Path

TBL = re.compile(r"^: (.*?)[ \t]*\{#tbl:([\w-]+)\}[ \t]*$", re.M)
FIG = re.compile(r"!\[(.*?)\]\(([^)]*)\)\{#fig:([\w-]+)\}")
REF = re.compile(r"@(tbl|fig):([\w-]+)")


def main(out, files):
    labels, texts = {}, []
    for f in files:
        ch = int(re.match(r"(\d+)", Path(f).name).group(1))
        s = re.sub(r"<!--.*?-->", "", Path(f).read_text(encoding="utf-8"), flags=re.S)
        for kind, rx in (("tbl", TBL), ("fig", FIG)):
            for n, m in enumerate(rx.finditer(s), 1):
                labels[(kind, m.group(m.lastindex))] = f"{ch}.{n}"
        s = TBL.sub(lambda m: f": Table {labels[('tbl', m.group(2))]}. {m.group(1)}", s)
        s = FIG.sub(lambda m: f"![Figure {labels[('fig', m.group(3))]}. {m.group(1)}]({m.group(2)})", s)
        texts.append(re.sub(r"\s*\{#sec:[\w-]+\}", "", s).strip())
    out_text = "\n\n".join(texts) + "\n"
    missing = sorted({m.group(0) for m in REF.finditer(out_text) if (m.group(1), m.group(2)) not in labels})
    if missing:
        sys.exit(f"unknown labels: {missing}")
    name = {"tbl": "Table", "fig": "Figure"}
    out_text = REF.sub(lambda m: f"{name[m.group(1)]} {labels[(m.group(1), m.group(2))]}", out_text)
    Path(out).write_text(out_text, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
