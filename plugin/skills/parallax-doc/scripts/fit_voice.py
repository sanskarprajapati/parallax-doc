#!/usr/bin/env python3
"""Fit a narration take to the film's length and get word timings.

    python3 fit_voice.py <project-dir> <voice-audio> <target-seconds> [--max-pause 0.32] [--tail 1.4]

1. Shortens every pause longer than --max-pause to --max-pause (TTS takes run long
   mostly because of pauses, not words).
2. Speeds the result up or down (atempo, pitch kept) so the speech ends --tail seconds
   before <target-seconds>. Refuses factors outside 0.85-1.25, which sound wrong:
   trim the script instead.
3. Writes <project>/assets/vo/vo.m4a (exactly target-seconds long) and
   <project>/assets/vo/words.json: [[start, end, "word"], ...] for timing text and cuts.

Needs ffmpeg and the HyperFrames CLI (`npx hyperframes transcribe`).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:4])} ...\n{p.stderr[-800:]}")
    return p.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", path]).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("audio")
    ap.add_argument("target", type=float)
    ap.add_argument("--max-pause", type=float, default=0.32)
    ap.add_argument("--tail", type=float, default=1.4)
    a = ap.parse_args()
    for tool in ("ffmpeg", "ffprobe", "npx"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH")

    if a.target <= a.tail:
        sys.exit("target seconds must be longer than --tail")
    out_dir = os.path.join(a.project, "assets", "vo")
    os.makedirs(out_dir, exist_ok=True)
    tmp = tempfile.mkdtemp()
    try:
        fit(a, out_dir, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def fit(a, out_dir, tmp):
    tight = os.path.join(tmp, "tight.wav")
    p = f"{a.max_pause:.2f}"
    run(["ffmpeg", "-v", "error", "-y", "-i", a.audio, "-af",
         f"silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:"
         f"stop_duration={p}:stop_threshold=-38dB:stop_silence={p}", "-ar", "44100", tight])
    speech = duration(tight)
    factor = speech / (a.target - a.tail)
    print(f"original {duration(a.audio):.2f}s, pauses tightened {speech:.2f}s, tempo x{factor:.3f}")
    if not 0.85 <= factor <= 1.25:
        sys.exit(f"tempo x{factor:.2f} is outside 0.85-1.25: change the script length instead "
                 f"(about {round((a.target - a.tail) * 2.3)} words fit at a documentary pace)")

    vo = os.path.join(out_dir, "vo.m4a")
    run(["ffmpeg", "-v", "error", "-y", "-i", tight, "-af", f"atempo={factor:.4f},apad=pad_dur={a.tail + 1}",
         "-t", f"{a.target}", "-ar", "44100", "-ac", "2", "-c:a", "aac", "-b:a", "192k", vo])

    wav = os.path.join(tmp, "vo.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-ar", "16000", "-ac", "1", wav])
    run(["npx", "--yes", "hyperframes", "transcribe", wav, "--dir", tmp])
    with open(os.path.join(tmp, "transcript.json")) as f:
        words = [[round(w["start"], 2), round(w["end"], 2), w["text"]] for w in json.load(f)]
    if not words:
        sys.exit("the transcriber found no words in the take: check the audio")
    with open(os.path.join(out_dir, "words.json"), "w") as f:
        json.dump(words, f)
    print(f"wrote {vo} ({a.target}s) and words.json ({len(words)} words, speech ends {words[-1][1]:.2f}s)")
    print(" ".join(f"{t}@{s:.2f}" for s, _, t in words))


if __name__ == "__main__":
    main()
