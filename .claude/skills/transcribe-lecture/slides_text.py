"""Print the text, speaker notes and image count of each slide in a .pptx (no dependencies).

Usage:
  python slides_text.py deck.pptx [out.txt]

Slides with many images and little text are the ones worth looking at as rendered pages.
"""
import html
import re
import sys
import zipfile
from pathlib import Path


def paras(xml):
    out = []
    for p in re.findall(r"<a:p\b.*?</a:p>", xml, re.S):
        t = "".join(re.findall(r"<a:t(?:\s[^>]*)?>([^<]*)</a:t>", p)).strip()
        if t:
            out.append(html.unescape(t))
    return out


def main():
    src = Path(sys.argv[1])
    z = zipfile.ZipFile(src)
    rel = {}
    for r in re.findall(r"<Relationship\b[^>]*>", z.read("ppt/_rels/presentation.xml.rels").decode("utf8")):
        rel[re.search(r'Id="([^"]+)"', r).group(1)] = re.search(r'Target="([^"]+)"', r).group(1)
    order = re.findall(r'<p:sldId\b[^>]*r:id="([^"]+)"', z.read("ppt/presentation.xml").decode("utf8"))

    lines = []
    for n, rid in enumerate(order, 1):
        path = "ppt/" + rel[rid].split("ppt/")[-1].lstrip("/")
        xml = z.read(path).decode("utf8")
        srels = z.read(path.replace("slides/", "slides/_rels/") + ".rels").decode("utf8")
        hidden = " hidden" if re.search(r'<p:sld\b[^>]*show="0"', xml) else ""
        images = srels.count('relationships/image"')
        lines.append(f"--- slide {n} ({images} images{hidden})")
        lines += paras(xml)
        note = re.search(r"notesSlides/(notesSlide\d+\.xml)", srels)
        if note:
            notes = [t for t in paras(z.read("ppt/notesSlides/" + note.group(1)).decode("utf8"))
                     if not t.isdigit() and t != "‹#›"]
            if notes:
                lines.append("[notes] " + " ".join(notes))

    text = "\n".join(lines) + "\n"
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(text, encoding="utf8")
        print(f"{src.name}: {len(order)} slides -> {sys.argv[2]}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()
