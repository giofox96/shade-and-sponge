"""Pull the spoken script out of slides/outline_20oct.md into slides/speech_20oct.md.

Only what you say out loud: no figure paths, no on-slide bullets, no sources. Re-run it after
every edit to the outline, so the two never drift apart:

    python scripts/make_speech.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "slides/outline_20oct.md"
OUT = ROOT / "slides/speech_20oct.md"
WPM = 150

lines = SRC.read_text(encoding="utf-8").split("\n")
slides, backups, questions = [], [], []
cur = None
for i, ln in enumerate(lines):
    m = re.match(r"^## (\d+)\. (.*?) — (CORE|EXTRA) \[(\d+:\d\d)\]$", ln)
    if m:
        cur = m.groups()
    m = re.match(r"^\*\*Say \((\d+) words\):\*\*$", ln)
    if m and cur:
        slides.append((*cur, lines[i + 1].strip().strip('"')))
        cur = None
    m = re.match(r"^## (B\d)\. (.*)$", ln)
    if m:
        cur = m.groups()
    m = re.match(r"^\*\*Say \(~\d+ words\):\*\* \"(.*)\"$", ln)
    if m and cur:
        backups.append((cur[0], cur[1], m.group(1)))
        cur = None
    m = re.match(r"^- \*\*(.+?)\*\* (.+)$", ln)
    if m and ln.startswith("- **") and questions is not None and "## Likely tutor questions" in "\n".join(lines[:i]):
        questions.append(m.groups())

core = sum(int(w) for _, _, k, _, w in ((s[0], s[1], s[2], s[3], len(s[4].split())) for s in slides) if k == "CORE")
total = sum(len(s[4].split()) for s in slides)


def mmss(n):
    sec = round(n / WPM * 60)
    return f"{sec // 60}:{sec % 60:02d}"


md = ["# What to say, 20 October 2026",
      "",
      f"Generated from `slides/outline_20oct.md` by `scripts/make_speech.py` — spoken text only. "
      f"**{total:,} words, {mmss(total)}** at 150 wpm for all 17 slides; **{core:,} words, {mmss(core)}** "
      f"if you drop the five marked *extra*. The time in brackets is where you should be when you finish "
      f"that slide.", ""]
for n, title, kind, clock, say in slides:
    tag = "" if kind == "CORE" else "  ·  *extra, cut this first*"
    md += [f"### {n}. {title}  ·  {clock}{tag}", "", say, ""]
md += ["---", "", "## Only if the tutor asks", ""]
for tag, title, say in backups:
    md += [f"### {tag}. {title}", "", say, ""]
md += ["### One-line answers", ""]
md += [f"- **{q}** {a}" for q, a in questions]
OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)}: {len(slides)} slides, {len(backups)} backups, "
      f"{len(questions)} answers, {total} spoken words")
