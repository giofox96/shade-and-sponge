# Study section

Material for **learning** the thesis (not for writing it; content checked against `notes/` on 19 Oct 2026), so that you can explain and defend it without notes at the 20 Oct session and at the final review.

| File | What it is | How to use it |
|---|---|---|
| `guide.md` | The thesis condensed into 16 chapters (§0–§15), each with "Check yourself" questions, a glossary and a key-numbers sheet | Read one chapter, close it, answer the questions, then check |
| `flashcards.csv` | Question → answer cards, tagged by chapter | Use in the study app, or import into Anki |
| `quiz.csv` | Multiple-choice questions with explanations | Use in the study app |
| `study_app.html` | Flashcards with spaced repetition (Leitner boxes), a mixed quiz and a "say it out loud" mode | Open in a browser (works offline, phone too). Rebuild after editing the CSVs: `python scripts/make_study_app.py` |

**Keep it current:** when a note in `notes/` changes a number or a decision, update `guide.md` and the matching cards, then rebuild the app. Each card names its source file.

---

## Which study methods work (and which do not)

| Method | Evidence | How this folder applies it |
|---|---|---|
| **Practice testing (retrieval practice)**: recalling from memory, not rereading | Rated "high utility" in a review of 10 learning techniques (Dunlosky et al. 2013, *Psychological Science in the Public Interest* 14(1), 4–58). Taking memory tests improves long-term retention more than restudying (Roediger & Karpicke 2006, *Psychological Science* 17(3), 249–255) | Flashcards, quiz, the "Check yourself" blocks with answers hidden |
| **Distributed practice (spacing)**: several short sessions spread over days | Also "high utility" (Dunlosky et al. 2013). In a meta-analysis of 317 experiments, the best gap between sessions grows with how long you need to remember (Cepeda et al. 2006, *Psychological Bulletin* 132(3), 354–380) | Leitner boxes in the app; the 11-day plan below |
| **Interleaving**: mixing topics instead of studying one block at a time | Interleaved practice gave better delayed-test scores than blocked practice in mathematics (Rohrer & Taylor 2007, cited in later Rohrer papers) | "Mixed" mode in the app shuffles all chapters |
| **Rereading, highlighting, summarising** | Rated "low utility" (Dunlosky et al. 2013) | Avoid as your main method; reread only what you got wrong |
| **Explaining it simply** (the "Feynman technique") | A practical heuristic, not one of the techniques tested by Dunlosky et al.; close to self-explanation, which they did review | "Say it" mode: explain a concept aloud in 30 s, then compare with the answer |
| **Mnemonics for lists** (acronyms, a sentence, a route through a familiar place) | Use for fixed lists only (species, scenarios, hypotheses); not checked here for evidence strength | Given in `guide.md` (e.g. S-T-B for the hypotheses) |

**Rules of thumb:**
1. **Try to recall before you look.** Getting it wrong first and then checking still helps.
2. **Short and often** beats long and once: 20–30 min a day.
3. **Mix chapters** once you know each one a little.
4. **Say it out loud.** The 20 Oct deliverable is a spoken 5-minute talk; train the voice, not only the eyes.

### NotebookLM as a complement
Upload `guide.md` and the notes in `notes/` (`topic_decision.md`, `methodology.md`, `site_selection.md`, `transferability.md`, `catalan_transfer_city.md`) and `slides/outline_20oct.md` as sources. Useful there: the audio overview (listen on the go) and asking it to quiz you. Check any number it gives against `guide.md`; it can mix up figures.

---

## Tonight and tomorrow morning (19–20 Oct)

The chapter numbers moved on 19 Oct: **§10 is the new Transferability chapter**, so Limits is **§11**, tutor questions **§12**, glossary **§13**, key numbers **§14**, open decisions **§15**. The two RM-seminar figures (plane-tree map, cluster map) are **out of the tutor deck** and parked in `slides/seminar_rm/`, the deck was rebuilt on 19 Oct to follow this guide's rhythm: **17 slides plus 3 backups**, each with its spoken script, in `slides/outline_20oct.md` v3. Figure file numbers are now slide numbers (`slides/fig/NN_*.png`); slides 1, 4, 11, 12, 14 and 15 use a photo, a `notes/figures/` plot or plain text.

| Block | ≈ time | Do |
|---|---|---|
| 1 | 20 min | Read **§10 Transferability** once, close it, answer its 7 **Check yourself** questions aloud. This is new material and it is slide 16 of the talk, so it is the weakest part. |
| 2 | 10 min | App → Cards, chapter **Transfer** only (20 new cards). Anything you miss, read back in §10, then repeat. |
| 3 | 10 min | App → Quiz, mixed. Aim ≥ 90%. |
| 4 | 15 min | Full run-through with the slides, timed (target 5:00; the script is ~5:17 at 140 wpm, so speak at your normal pace). |
| 5 | 10 min | The six new transfer rows in **§12** (why Mataró, why not Badalona, method vs climate, the two hard dependencies), each in 20 s aloud. |
| 6 | 5 min | Skim **§14 Key numbers**, the transfer block last. |
| Morning | 15 min | One timed run-through, then only §14 and the three backup slides (B1 tree pit, B2 the 22-city screening, B3 method vs climate). |

**Three things not to say wrong tomorrow:**
1. The harmonised 0.93 ratio is **an identity, not a finding** — the evidence is the *raw* ratio reversing direction with duration.
2. The 52% vs 43% species overlap is **not like-for-like** (Florence's inventory includes park trees).
3. Every Mataró asset has an **UNKNOWN licence** — do not call it CC BY.

---

## The original plan to 20 Oct (≈ 25 min a day; kept for reference)

| Day | Date | New material | Review |
|---|---|---|---|
| 1 | Fri 9 Oct | §0 (learn the 30-s pitch by heart), §1 Problem | — |
| 2 | Sat 10 | §2 Site, §3 Runoff | App: due cards |
| 3 | Sun 11 | §4 Heat, §5 Synergy / trade-off | App: due cards |
| 4 | Mon 12 | §6 Gap, §7 RQ + H (word-perfect) | App: due cards; say the pitch aloud |
| 5 | Tue 13 | §8 Method and tool | App: due cards |
| 6 | Wed 14 | §9 Results, §10 Transferability, §11 Limits | Quiz, mixed |
| 7 | Thu 15 | §12 Tutor questions: answer each in 20 s, aloud | App: due cards |
| 8 | Fri 16 | Rehearse the talk with slides (`slides/outline_20oct.md`), timed | Quiz, mixed |
| 9 | Sat 17 | Rehearse without the script | Key-numbers sheet (§14) |
| 10 | Sun 18 | Rest or light review | App: due cards only |
| 11 | Mon 19 | Full run-through ×2, timed; tutor questions | Quiz: aim ≥ 90% |

After 20 Oct, keep 10 min every two or three days with the app's due cards; add cards when the methodology changes.

## Sources
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*, 14(1), 4–58.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249–255.
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354–380.
- Rohrer, D., & Taylor, K. (2007). The shuffling of mathematics problems improves learning. *Instructional Science*, 35, 481–498. (Seen only as cited by later Rohrer papers; not read.)

These are not in `papers/`; they support the study method, not the thesis.
