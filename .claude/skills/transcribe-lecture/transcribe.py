"""Transcribe lecture recordings with faster-whisper on the GPU.

Usage:
  python transcribe.py <file-or-folder> [...] [--dry-run] [--language en] [--force]

A folder is scanned recursively for recordings that have no transcript yet.
The transcript is written next to the recording as <stem>.txt: a short header,
then paragraphs that each start with a [hh:mm:ss] timestamp.
"""
import argparse
import glob
import os
import site
import sys
import time
from datetime import date
from pathlib import Path

MEDIA = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4a", ".mp3", ".wav", ".ogg", ".flac"}


def add_cuda_dlls():
    # pip's nvidia-cublas/cudnn wheels keep their DLLs in site-packages/nvidia/*/bin; CTranslate2 needs them findable
    for sp in site.getsitepackages():
        for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def todo(paths, force):
    files = []
    for p in map(Path, paths):
        found = sorted(f for f in p.rglob("*") if f.suffix.lower() in MEDIA) if p.is_dir() else [p]
        files += [f for f in found if force or not f.with_suffix(".txt").exists()]
    return files


def stamp(t):
    t = int(t)
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def transcribe(model, model_name, f, language):
    t0 = time.time()
    segments, info = model.transcribe(str(f), language=language, batch_size=16)
    print(f"{f.name}: {stamp(info.duration)} of audio, language {info.language} ({info.language_probability:.2f})", flush=True)

    # Group segments into paragraphs: break on a pause > 2 s or after ~60 s of speech
    paras, cur, start, last_end, next_report = [], [], 0.0, 0.0, 600
    for s in segments:
        if cur and (s.start - last_end > 2 or s.start - start > 60):
            paras.append((start, " ".join(cur)))
            cur = []
        if not cur:
            start = s.start
        cur.append(s.text.strip())
        last_end = s.end
        if s.end > next_report:
            print(f"  {stamp(s.end)} / {stamp(info.duration)}", flush=True)
            next_report += 600
    if cur:
        paras.append((start, " ".join(cur)))

    minutes = (time.time() - t0) / 60
    header = (f"# source: {f.name}\n"
              f"# duration: {stamp(info.duration)} | language: {info.language} ({info.language_probability:.2f}) | "
              f"model: {model_name} | transcribed: {date.today()} in {minutes:.1f} min\n\n")
    body = "\n\n".join(f"[{stamp(t)}] {text}" for t, text in paras)
    # Write to a temporary file first so an interrupted run never looks like a finished transcript
    tmp = f.with_suffix(".txt.part")
    tmp.write_text(header + body + "\n", encoding="utf-8")
    tmp.replace(f.with_suffix(".txt"))
    print(f"  -> {f.with_suffix('.txt').name} ({len(paras)} paragraphs, {minutes:.1f} min)", flush=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="recording(s) or folder(s) to scan")
    ap.add_argument("--language", default=None, help="e.g. en (default: auto-detect)")
    ap.add_argument("--model", default="large-v3-turbo")
    ap.add_argument("--force", action="store_true", help="redo recordings that already have a transcript")
    ap.add_argument("--dry-run", action="store_true", help="only list the recordings to transcribe")
    a = ap.parse_args()

    files = todo(a.paths, a.force)
    print(f"{len(files)} recording(s) to transcribe")
    for f in files:
        print(f"  {f}")
    if a.dry_run or not files:
        return

    add_cuda_dlls()
    from faster_whisper import BatchedInferencePipeline, WhisperModel
    model = BatchedInferencePipeline(WhisperModel(a.model, device="cuda", compute_type="float16"))
    for f in files:
        transcribe(model, a.model, f, a.language)


if __name__ == "__main__":
    main()
