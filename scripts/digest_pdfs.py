"""Step 4: turn every PDF in papers/ into a short digest for reading.

Usage: python scripts/digest_pdfs.py
Needs pdftotext (Git for Windows ships it). Output: notes/lit/digest/<pdf name>.md with
abstract (start of text), conclusions section, and sentences that carry key numbers.
Full text is cached in notes/lit/text/ (local only, do not share).
"""
import re, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TXT, DIG = ROOT / "notes/lit/text", ROOT / "notes/lit/digest"
TXT.mkdir(parents=True, exist_ok=True)
DIG.mkdir(parents=True, exist_ok=True)
KEY = re.compile(r"(interception|runoff|infiltration|storage capacity|peak|stemflow|throughfall|curve number|"
                 r"evapotranspiration|transpiration|retention|UTCI|cooling)", re.I)
NUM = re.compile(r"\d+(\.\d+)?\s?(%|mm|L\b|m3|m³|°C|K\b)")

for pdf in sorted((ROOT / "papers").glob("*.pdf")):
    txt = TXT / (pdf.stem + ".txt")
    if not txt.exists():
        tmp = TXT / "_tmp.pdf"  # pdftotext on Windows fails on non-ASCII file names
        tmp.write_bytes(pdf.read_bytes())
        subprocess.run(["pdftotext", "-enc", "UTF-8", str(tmp), str(TXT / "_tmp.txt")], check=False)
        tmp.unlink()
        (TXT / "_tmp.txt").replace(txt)
    if not txt.exists():
        continue
    t = re.sub(r"-\n(\w)", r"\1", txt.read_text(encoding="utf-8", errors="ignore"))
    flat = re.sub(r"\s+", " ", t)
    body = re.split(r"\b(References|REFERENCES|Bibliography|Literature Cited)\b", flat)[0]
    m = list(re.finditer(r"\b(\d\.?\s*)?(Conclusions?|CONCLUSIONS?|Concluding remarks)\b", body))
    concl = body[m[-1].start():][:3500] if m else ""
    sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", body) if KEY.search(s) and NUM.search(s) and len(s) < 400]
    (DIG / (pdf.stem + ".md")).write_text(
        f"# {pdf.name}\n\n## Start (abstract)\n{flat[:2500]}\n\n## Conclusions\n{concl}\n\n## Key numeric sentences\n"
        + "\n".join(f"- {s}" for s in sents[:15]) + "\n", encoding="utf-8")
    print("ok", pdf.name[:70], len(flat))
