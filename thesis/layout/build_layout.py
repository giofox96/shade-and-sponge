"""Lay out thesis chapters in DesignCraft on the IAAC A4 template, in the project's identity.

Usage:
  python thesis/layout/number_refs.py build/body.md thesis/02_*.md thesis/03_*.md ...
  pandoc build/body.md -f markdown-citations -t docx -o build/body.docx
  DESIGNCRAFT_CLI=path/to/designcraft-cli python thesis/layout/build_layout.py TEMPLATE.designcraft build/body.docx OUT_DIR

TEMPLATE is the IAAC "A4 - Activity Report.indd" saved once as .designcraft (file.open + --save).
Fonts (IBM Plex Sans, OFL) must sit in a "Document Fonts" folder next to TEMPLATE.
Writes OUT_DIR/thesis_layout.{designcraft,pdf,idml}.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DC = os.environ.get("DESIGNCRAFT_CLI", "designcraft-cli")
TITLE = "Shade and Sponge"
SUBTITLE = ("A computational method for choosing street-tree replacements "
            "that keep shade and rain interception in Barcelona")
AUTHOR = "Giovanni Carlo Volpe  |  MaCAD 2025 - 2026"
# Web app palette (web/src styles)
SWATCHES = {"SS Green": "#3F663E", "SS Blue": "#283F66", "SS Terracotta": "#8A3E22",
            "SS Cream": "#F2F0EA", "SS Ink": "#2A2622"}
MARGINS = {"top": 62, "bottom": 72, "inside": 64, "outside": 48}
COLS, GUTTER = 2, 18
# Template object ids (IAAC A4 template): cover/back background frames and grey masks,
# IAAC pixel-art groups, cover title/subtitle/author stories and frames.
COVER_FILLS, PIXEL_ART = [259, 412, 743, 892], [263, 744]
FRONT_PAGES = 2  # contents + list of tables/figures


def run(lines, inp, out):
    r = subprocess.run([DC, "script", "-", "--in", str(inp), "--keep-going", "--save", str(out)],
                       input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=900)
    res = json.loads(r.stdout)["results"]
    for i, x in enumerate(res):
        if isinstance(x, dict) and "error" in x:
            print("ERR", i, lines[i][:80], x["error"])
    return res


def j(cmd, **p):
    return f"{cmd} {json.dumps(p)}"


def font(style, size, leading, fill):
    return {"fontFamily": "IBM Plex Sans", "fontStyle": style, "size": size,
            "leading": {"kind": "points", "value": leading}, "fill": fill}


def set_story(story, text, chars):
    return [j("story.setText", story=story, text=text),
            j("text.select", story=story, anchor=0, focus=len(text.encode())),
            j("style.paragraph.apply", name="[Basic Paragraph]", clearOverrides=True),  # keep covers out of the contents
            j("type.char", attrs=chars)]


def setup(docx):
    L = [j("swatch.create", name=n, color=c) for n, c in SWATCHES.items()]
    L += set_story(2, TITLE, font("SemiBold", 60, 62, "SS Green"))
    L += [j("transform.resize", ids=[262], **{"from": [32.598, 248.274, 380.094, 287.474], "to": [32.6, 190, 470, 290]})]
    L += set_story(4, SUBTITLE, font("Regular", 17, 23, "SS Ink"))
    L += [j("transform.resize", ids=[261], **{"from": [32.598, 580.492, 145.782, 599.692], "to": [32.6, 560, 400, 600]})]
    L += set_story(3, AUTHOR, font("Medium", 10.5, 15, "SS Ink"))
    L += [j("object.fill", swatch="SS Cream", ids=COVER_FILLS), j("edit.clear", ids=PIXEL_ART),
          j("frame.create", spread=0, rect=[0, 300, 595.28, 306], content="graphic"),
          j("object.fill", swatch="SS Green", ids=["$last.id"])]
    span = {"spanColumns": {"kind": "span", "columns": 0}}
    L += [j("style.paragraph.edit", name="[Basic Paragraph]", para={"spaceAfter": 5},
            chars=font("Regular", 9.5, 14, "SS Ink")),
          j("style.paragraph.edit", name="H1", para={"startParagraph": "nextPage", "spaceAfter": 30, "align": "left", **span},
            chars={**font("SemiBold", 28, 33, "SS Green"), "capitalization": "normal"}),
          j("style.paragraph.edit", name="H2", para={"spaceBefore": 16, "spaceAfter": 6},
            chars={**font("SemiBold", 12.5, 16, "SS Blue"), "capitalization": "normal", "tracking": 0}),
          j("style.paragraph.edit", name="H3", para={"spaceBefore": 10, "spaceAfter": 4},
            chars=font("Medium", 10.5, 14, "SS Terracotta"))]
    for cap in ("Table Caption", "Figure Caption"):
        L.append(j("style.paragraph.create", name=cap, basedOn="[Basic Paragraph]",
                   para={"spaceBefore": 8, "spaceAfter": 4, **span}, chars=font("Medium", 8.5, 12, "SS Blue")))
    n_old = 24  # template pages 1..24; page 0 = cover, last = back cover
    L += [j("layout.pages.delete", pages=list(range(1, n_old + 1))),
          j("layout.pages.insert", count=FRONT_PAGES + 2, after=0, parent=None),
          j("layout.marginsAndColumns", margins=MARGINS, columns=1),
          j("layout.marginsAndColumns", parent="A", margins=MARGINS, columns=1),
          j("frame.create", spread=2, rect=[48, 62, 531, 770], content="text"),
          j("object.textFrameOptions", columns=COLS, gutter=GUTTER, ids=["$last.id"]),
          j("file.place", path=str(docx), frame="$-1.id", autoflow=True, styleConflicts="useExisting",
            styleMap={"Heading 1": "H1", "Heading 2": "H2", "Heading 3": "H3", "Normal": "[Basic Paragraph]",
                      "Body Text": "[Basic Paragraph]", "First Paragraph": "[Basic Paragraph]",
                      "Compact": "[Basic Paragraph]", "Block Text": "[Basic Paragraph]",
                      "Table Caption": "Table Caption", "Image Caption": "Figure Caption"}),
          "document.inspect {}"]
    return L


def pages_of(ins):
    return [(sp["index"], p) for sp in ins["spreads"] for p in sp["pages"]]


def main(template, docx, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    work = Path(template).parent
    a, b = work / "_a.designcraft", work / "_b.designcraft"
    res = run([j("file.open", path=str(Path(template).resolve()))] + setup(Path(docx).resolve()), template, a)
    ins, story = res[-1], res[-2]["story"]
    pages = pages_of(ins)
    back = next(i for i, (_, p) in enumerate(pages) if i > 0 and p["parent"] == "A-Parent")
    si, pb = pages[back][0], pages[back][1]["bounds"]
    on_back = [it["id"] for sp in ins["spreads"] if sp["index"] == si for it in sp["items"]
               if it.get("story") == story and pb[0] - 1 <= it["bounds"][0] < pb[2]]
    L = []
    for i in on_back:
        L += [j("text.removeFromThread", frame=i), j("edit.clear", ids=[i])]
    n = len(pages)
    L += [j("layout.pages.move", **{"from": back, "to": n - 1}),
          j("layout.pages.applyParent", pages=list(range(1, n - 1)), parent=None),
          j("story.get", story=story)]
    g = run(L, a, b)[-1]
    g = run([j("object.textFrameOptions", columns=COLS, gutter=GUTTER, ids=g["frames"]),
             j("story.get", story=story)], b, a)[-1]
    shutil.copy(a, b)
    while g.get("overset") is not None:  # add a spread before the back cover until the text fits
        n = run(["document.inspect {}"], b, a)[0]["pageCount"]
        ins = run([j("layout.pages.insert", count=2, after=n - 2, parent=None),
                   j("layout.marginsAndColumns", pages=[n - 1, n], margins=MARGINS, columns=1),
                   "document.inspect {}"], b, a)[-1]
        si, p = pages_of(ins)[n - 1]
        x0 = p["bounds"][0] + MARGINS["outside" if p["side"] == "left" else "inside"]
        x1 = p["bounds"][2] - MARGINS["inside" if p["side"] == "left" else "outside"]
        t = run([j("text.thread", **{"from": g["frames"][-1]}, spread=si, rect=[x0, 62, x1, 770])], a, a)[-1]
        g = run([j("object.textFrameOptions", columns=COLS, gutter=GUTTER, ids=[t["to"]]),
                 j("story.get", story=story)], a, b)[-1]
    # tables span both columns
    L = []
    text = g["text"].encode()
    full = 483.0  # column-span width = page width - inside - outside margins
    for off in [i for i in range(len(text)) if text[i:i + 3] == "".encode()]:
        L += [j("text.select", story=story, anchor=off, focus=off),
              j("type.para", attrs={"spanColumns": {"kind": "span", "columns": 0}}),
              j("table.get", cells=False)]
    res = run(L, b, a)
    tables = [r for r in res if isinstance(r, dict) and "columns" in r and "anchor" in r]
    L = []
    for t in tables:
        w = full / len(t["columns"])
        L.append(j("text.select", story=story, anchor=t["anchor"], focus=t["anchor"]))
        L += [j("table.resizeBorder", axis="column", index=k, size=w) for k in range(len(t["columns"]))]
    # front matter: contents and list of tables, on pages 2 and 3 (1-based)
    L += [j("toc.generate", styles=["H1", "H2"], title="Contents", page=2, createBookmarks=True),
          j("toc.generate", entries=[{"style": "Table Caption", "level": 1}, {"style": "Figure Caption", "level": 1}],
            title="List of tables and figures", page=3, replace=False),
          j("story.get", story=story)]
    res = run(L, a, b)
    print("overset after columns:", res[-1].get("oversetChars"))
    final = out_dir / "thesis_layout.designcraft"
    shutil.copy(b, final)
    subprocess.run([DC, "run", "--in", str(final), "--export", str(out_dir / "thesis_layout.pdf"),
                    "--export", str(out_dir / "thesis_layout.idml")], check=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
