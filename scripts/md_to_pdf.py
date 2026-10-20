"""Markdown -> PDF for the study material, using the same headless browser as the infographics.

    python scripts/md_to_pdf.py study/guide.md          -> study/guide.pdf
    python scripts/md_to_pdf.py study/guide.md out.pdf

The "Check yourself" answers live in <details> blocks, which a PDF cannot expand, so they are
printed open, indented and greyed: cover them with your hand before you look.
"""
import pathlib
import subprocess
import sys
import tempfile
import time

import mistune

import make_infographics as mi

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font: 11pt/1.45 "Segoe UI", Arial, sans-serif; color: #1F2933; max-width: none; }
h1 { font-size: 20pt; margin: 0 0 4pt; }
h2 { font-size: 15pt; margin: 18pt 0 6pt; padding-top: 6pt; border-top: 2px solid #3B7F4A;
     break-after: avoid; }
h3 { font-size: 12pt; margin: 12pt 0 4pt; color: #3B7F4A; break-after: avoid; }
p, li { orphans: 2; widows: 2; }
ul, ol { margin: 4pt 0 4pt 16pt; padding: 0; }
li { margin: 2pt 0; }
code { font-family: Consolas, monospace; font-size: 9.5pt; background: #F3F5F6; padding: 0 2px; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.5pt;
        break-inside: avoid; }
th, td { border: 1px solid #D6DCDF; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #EDF2F3; }
blockquote { margin: 6pt 0; padding: 4pt 10pt; border-left: 3px solid #3B7F4A; background: #F6F9F7; }
details { margin: 4pt 0 10pt; padding: 4pt 10pt; border-left: 3px solid #C9D3D7; background: #FAFBFB;
          color: #51606A; break-inside: avoid; }
summary { font-weight: bold; color: #6B7280; }
hr { border: 0; border-top: 1px solid #E5E7EB; margin: 10pt 0; }
"""


def to_pdf(src: pathlib.Path, out: pathlib.Path) -> None:
    md = mistune.create_markdown(plugins=["table", "strikethrough"], escape=False)
    body = md(src.read_text(encoding="utf-8")).replace("<details>", "<details open>")
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{src.stem}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    exe = mi.browser_exe()
    if not exe:
        sys.exit("no Edge/Chrome found: cannot print to PDF")
    out.unlink(missing_ok=True)          # headless Edge exits BEFORE the file is on disk: see the wait below
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        page = pathlib.Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run([exe, "--headless", "--disable-gpu", f"--user-data-dir={tmp}/prof",
                        f"--print-to-pdf={out}", "--no-pdf-header-footer", page.as_uri()],
                       capture_output=True, timeout=180)
        size = -1
        for _ in range(200):             # wait for the file to appear and stop growing (max ~60 s)
            time.sleep(0.3)
            now = out.stat().st_size if out.exists() else -1
            if now > 0 and now == size:
                break
            size = now
    if not out.exists():
        sys.exit(f"{out} was not written")
    print(f"wrote {out.relative_to(mi.ROOT)} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    source = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else mi.ROOT / "study/guide.md")
    target = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else source.with_suffix(".pdf")
    to_pdf(source if source.is_absolute() else mi.ROOT / source,
           target if target.is_absolute() else mi.ROOT / target)
