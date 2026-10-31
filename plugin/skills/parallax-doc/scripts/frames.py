#!/usr/bin/env python3
"""Frame tools for studying a reference and checking a render against it.

  frames.py breakdown <video> <out-dir>
      Every frame as a jpg, labelled 16-up contact sheets (frame number and time),
      a per-frame difference list (finds cuts, holds and 24fps-in-30 duplicates),
      and the audio as 16 kHz wav for transcription.

  frames.py compare <reference-frames-dir> <render-frames-dir> <out.jpg> <frame,frame,...>
      Reference over render, 4 moments a row. Extract each video's frames first:
      ffmpeg -i in.mp4 -vsync 0 -q:v 3 <dir>/f%06d.jpg

  frames.py sheet <video> <out.jpg> [--every 0.5] [--from 0] [--to end]
      A labelled sheet of one frame every N seconds, for reviewing a long render.

  frames.py grid <image> <out.jpg> [--step 200]
      The image with a labelled pixel grid, to read off where something sits on a plate
      (a headstone, a photo box, a city on a map) before you point a camera or a matte at it.
"""
import argparse
import glob
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def font(size):
    for path in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fps_of(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", video],
                         capture_output=True, text=True).stdout.strip()
    num, den = out.split("/")
    return float(num) / float(den)


def label(im, text, colour="yellow"):
    d = ImageDraw.Draw(im)
    f = font(max(14, im.width // 20))
    w = d.textlength(text, font=f)
    d.rectangle([0, 0, w + 10, getattr(f, "size", 11) + 8], fill="black")
    d.text((5, 3), text, fill=colour, font=f)
    return im


def breakdown(video, out):
    frames = os.path.join(out, "frames")
    os.makedirs(frames, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vsync", "0", "-q:v", "3",
                    os.path.join(frames, "f%06d.jpg")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ar", "16000", "-ac", "1",
                    os.path.join(out, "audio16k.wav")], check=False)
    fps = fps_of(video)
    paths = sorted(glob.glob(os.path.join(frames, "*.jpg")))
    W, H = 480, 270
    prev, diffs = None, []
    for k in range(0, len(paths), 16):
        sheet = Image.new("RGB", (W * 4, H * 4))
        for j, p in enumerate(paths[k:k + 16]):
            i = k + j
            im = Image.open(p).convert("RGB").resize((W, H))
            small = np.asarray(im.resize((96, 54)), dtype=float)
            diffs.append(0.0 if prev is None else float(np.abs(small - prev).mean()))
            prev = small
            sheet.paste(label(im, f"#{i} {i / fps:.2f}s"), ((j % 4) * W, (j // 4) * H))
        sheet.save(os.path.join(out, f"sheet_{k // 16:03d}.jpg"), quality=85)
    with open(os.path.join(out, "diffs.txt"), "w") as f:
        f.write("\n".join(f"{i} {d:.1f}" for i, d in enumerate(diffs)))
    dupes = [i for i, d in enumerate(diffs) if i and d < 0.6]
    print(f"{len(paths)} frames at {fps:g} fps -> {len(range(0, len(paths), 16))} sheets in {out}")
    if len(dupes) > len(paths) * 0.15:
        gaps = np.diff(dupes)
        print(f"{len(dupes)} near-duplicate frames, typical gap {int(np.median(gaps))}: "
              "a gap of 5 at 30fps means it was cut at 24fps")
    big = [i for i, d in enumerate(diffs) if d > 30]
    print("hard cuts (diff > 30):", big or "none")


def compare(ref_dir, mine_dir, out, frames):
    W, H = 480, 270
    cols = 4
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (W * cols, (H * 2 + 10) * rows), "black")
    for i, n in enumerate(frames):
        x, y = (i % cols) * W, (i // cols) * (H * 2 + 10)
        for r, (d, tag, colour) in enumerate(((ref_dir, "REF", "yellow"), (mine_dir, "MINE", "cyan"))):
            p = os.path.join(d, f"f{n + 1:06d}.jpg")
            im = Image.open(p).convert("RGB").resize((W, H)) if os.path.exists(p) else Image.new("RGB", (W, H))
            sheet.paste(label(im, f"{tag} #{n}", colour), (x, y + r * H))
    sheet.save(out, quality=82)
    print("wrote", out)


def sheet(video, out, every, start, end):
    fps = fps_of(video)
    tmp = out + ".frames"
    os.makedirs(tmp, exist_ok=True)
    vf = f"select='gte(t\\,{start})*lte(t\\,{end})',fps={1 / every},scale=384:216"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-vsync", "0", "-q:v", "4",
                    os.path.join(tmp, "s%04d.jpg")], check=True)
    paths = sorted(glob.glob(os.path.join(tmp, "*.jpg")))
    cols = 8
    rows = (len(paths) + cols - 1) // cols
    canvas = Image.new("RGB", (384 * cols, 216 * rows))
    for i, p in enumerate(paths):
        canvas.paste(label(Image.open(p), f"{start + i * every:.1f}s"), ((i % cols) * 384, (i // cols) * 216))
    canvas.save(out, quality=80)
    for p in paths:
        os.remove(p)
    os.rmdir(tmp)
    print(f"wrote {out} ({len(paths)} frames, {fps:g} fps source)")


def grid(image, out, step):
    im = Image.open(image).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    f = font(max(18, W // 120))
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=(255, 0, 0), width=max(1, W // 900))
        d.text((x + 4, 4), str(x), fill=(255, 255, 0), font=f)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=(255, 0, 0), width=max(1, W // 900))
        d.text((4, y + 4), str(y), fill=(255, 255, 0), font=f)
    scale = min(1, 1600 / W)
    im.resize((int(W * scale), int(H * scale))).save(out, quality=82)
    print(f"wrote {out}: {W}x{H} plate, grid every {step}px (labels are plate pixels)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("breakdown")
    b.add_argument("video")
    b.add_argument("out")
    c = sub.add_parser("compare")
    c.add_argument("ref_dir")
    c.add_argument("mine_dir")
    c.add_argument("out")
    c.add_argument("frames")
    s = sub.add_parser("sheet")
    s.add_argument("video")
    s.add_argument("out")
    s.add_argument("--every", type=float, default=0.5)
    s.add_argument("--from", dest="start", type=float, default=0)
    s.add_argument("--to", dest="end", type=float, default=1e9)
    g = sub.add_parser("grid")
    g.add_argument("image")
    g.add_argument("out")
    g.add_argument("--step", type=int, default=200)
    a = ap.parse_args()
    if a.cmd == "grid":
        grid(a.image, a.out, a.step)
    elif a.cmd == "breakdown":
        breakdown(a.video, a.out)
    elif a.cmd == "compare":
        compare(a.ref_dir, a.mine_dir, a.out, [int(x) for x in a.frames.split(",")])
    else:
        sheet(a.video, a.out, a.every, a.start, a.end)


if __name__ == "__main__":
    sys.exit(main())
