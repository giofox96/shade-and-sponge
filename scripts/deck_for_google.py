"""Google Slides copy of the 10 Nov deck. Google converts native PowerPoint charts into low-resolution images and
re-lays out their labels, so this copy swaps each chart for a sharp 300-dpi crop of the same chart rendered by
LibreOffice; everything else (text, boxes, flowcharts, map, tables) stays native and editable.
Needs LibreOffice and pdftoppm. Run from scripts/: python deck_for_google.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image
from pptx import Presentation
from make_infographics import ROOT

SRC = ROOT / "slides/shade_and_sponge_10nov_editable.pptx"
OUT = ROOT / "slides/shade_and_sponge_10nov_google.pptx"
DPI = 300
SOFFICE = "/mnt/skills/public/pptx/scripts/office/soffice.py"

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    subprocess.run([sys.executable, SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(SRC)],
                   check=True, capture_output=True)
    prs = Presentation(SRC)
    emu_px = DPI / 914400
    n = 0
    for i, slide in enumerate(prs.slides, 1):
        charts = [sh for sh in slide.shapes if sh.has_chart]
        if not charts:
            continue
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", str(i), "-l", str(i), "-singlefile",
                        str(tmp / f"{SRC.stem}.pdf"), str(tmp / f"p{i}")], check=True, capture_output=True)
        page = Image.open(tmp / f"p{i}.png")
        for sh in charts:
            box = [round(v * emu_px) for v in (sh.left, sh.top, sh.left + sh.width, sh.top + sh.height)]
            png = tmp / f"c{i}_{n}.png"
            page.crop(box).save(png)
            pic = slide.shapes.add_picture(str(png), sh.left, sh.top, sh.width, sh.height)
            pic.name = f"{sh.name} (image)"
            sh._element.addprevious(pic._element)  # keep the chart's place in the z-order
            sh._element.getparent().remove(sh._element)
            n += 1
    prs.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} ({n} charts as {DPI}-dpi images)")
