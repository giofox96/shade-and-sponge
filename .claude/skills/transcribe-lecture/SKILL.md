---
name: transcribe-lecture
description: Transcribe a seminar lecture recording (Research and Technologies "RT", Research and Methodologies "RM") with local GPU Whisper, then split the lecture into chapters using the transcript plus the slides PDF and other sources, and write lecture notes. Use whenever the user says they added, uploaded or dropped a lecture video or recording, asks to transcribe a lecture, or wants chapters, notes or a summary of a seminar lecture, even if they don't say "transcribe".
---

# Lecture recording → transcript → chapter notes

The seminar material lives in `seminars/research_and_technologies/` (RT) and `seminars/research_and_methodologies/` (RM). The folder is gitignored because it holds course material, so nothing here gets committed.

The file names tie the recording, transcript, slides and notes of one lecture together:

| File | Name |
|---|---|
| Recording (video or audio) | `RM_L03.mp4`, or `RM_L03_p1.mp4`, `RM_L03_p2.mp4` if recorded in parts |
| Transcript (made by the script) | `RM_L03.txt`, next to the recording |
| Slides | `RM_L03_slides.pdf` |
| Other sources for that lecture | `RM_L03_<anything>.pdf/.md/.txt` (readings, NotebookLM notes) |
| Notes (written by you) | `RM_L03_notes.md` |

Homework files (`RM_HW01_brief/draft/final`) are not part of this skill.

## Steps

`PY=~/miniconda3/envs/whisper/python.exe`, script: `.claude/skills/transcribe-lecture/transcribe.py`.

1. **Find the work.** `"$PY" <script> seminars --dry-run` lists recordings without a transcript. If the user named one file, pass only that file.
2. **Check the names.** If a recording doesn't follow the pattern, propose the right name (seminar code and lecture number; ask the user if unclear) and rename after they agree.
3. **Transcribe.** Run the script without `--dry-run` using Bash with `run_in_background: true`. On the GPU, Whisper runs about 80× faster than real time (tested 8 Oct: 16.5 minutes of audio in 18 seconds, including model loading), so a 90-minute lecture takes 1–2 minutes. Read the slides while it runs; you are notified when it ends. If auto-detection reports a non-English language for an English lecture, rerun that file with `--language en --force`. If the GPU fails, fix the setup (below) rather than running on the CPU: the user found CPU Whisper too slow.
4. **Check the transcript.** Read the header (duration, language, time taken) and skim for repeated-line loops or long gaps. Whisper mishears names, acronyms and jargon; use the slides as the reference for spelling and fix terms in the notes. Keep the `.txt` untouched, since it is the verbatim source.
5. **Read the sources.** The slides PDF with Read (`pages`, at most 20 per call) and any other files with the same lecture prefix. Parts `_p1`, `_p2` are one lecture and get one notes file.
6. **Write `<prefix>_notes.md`** next to the transcript, using the template below.
7. **Report** to the user: the files written, audio length and transcription time, the chapter list, and any homework or deadlines. Offer to fold rules worth keeping into `notes/research_method_guidelines.md`.

## Chapters

A chapter is a topic shift in the talk, not a slide: usually 4 to 10 for a 90-minute lecture. When the lecturer follows the slide section titles, use them; when they digress (examples, Q&A), that can be its own chapter. Each chapter gets its start and end time and the slides it covers, so the user can jump to it in the video.

Every point cites a timestamp `[00:03:12]` or a slide `(slide 4)`, so the user can check it against the source. Add nothing that is in neither the transcript nor the sources (CLAUDE.md rule). Keep what the lecturer said separate from your own suggestions, which go only in the last section.

## Notes template

```markdown
# RM L03 · <lecture title, from the slides or the lecturer>

Lecturer: <if stated> · Date: <if known> · Sources: RM_L03.txt (01:32:10, en), RM_L03_slides.pdf (48 pages)

## Chapters

| # | Start | Slides | Chapter |
|---|---|---|---|
| 1 | 00:00:00 | 1–5 | <title> |

## 1. <Chapter title> (00:00:00–00:14:20, slides 1–5)

- <point> [00:03:12]
- <point> (slide 4)

## Homework, deadlines and readings mentioned

- <item> [timestamp]

## Takeaways for the thesis (Claude's suggestions)

- <suggestion> → <file it affects, e.g. notes/topic_decision.md §7>
```

## Setup (once)

```bash
~/miniconda3/Scripts/conda.exe create -n whisper --override-channels -c conda-forge python=3.11 -y
~/miniconda3/envs/whisper/python.exe -m pip install faster-whisper nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
```

The laptop GPU is an RTX 3080 Laptop (16 GB). The script puts the NVIDIA DLL folders on the search path itself. Don't use the `genai` env: importing torch there fails with an OpenMP DLL clash.
