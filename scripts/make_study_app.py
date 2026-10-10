"""Build study/study_app.html from the study CSVs (flashcards + quiz) and the HTML template."""
import csv
import json
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1] / "study"


def read(name):
    with open(STUDY / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


data = {"cards": read("flashcards.csv"), "quiz": read("quiz.csv")}
html = (STUDY / "app_template.html").read_text(encoding="utf-8")
html = html.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
(STUDY / "study_app.html").write_text(html, encoding="utf-8")
print(f"study_app.html: {len(data['cards'])} cards, {len(data['quiz'])} quiz questions")
