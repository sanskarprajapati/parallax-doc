#!/usr/bin/env python3
"""Cut foreground layers out of generated plates.

    python3 cut_layers.py <project-dir> [shot ...]

Every shot in shots.json with a "cutout" object is cut from
assets/gen/<shot>.png into assets/cut/<shot>.png (RGBA). Modes:

  flood   background = pixels near the border colour that touch the given frame
          edges ("edges": any of t, l, r, b). Keeps light areas inside the subject.
          "hard"/"soft": colour distance where the matte starts and how wide it ramps.
  luma    alpha from darkness (smoke or dust on white); recoloured to neutral grey.
  bright  alpha from brightness (spray or sparks on black).

Options: "erode" (px, pulls the matte inside a light fringe), "flip" ("v" or "h").
Plates are generated on plain white or black on purpose so this stays deterministic;
a person-only matting model drops smoke, stones and props.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def border_colour(rgb, edges):
    strips = {"t": rgb[:6], "b": rgb[-6:], "l": rgb[:, :6], "r": rgb[:, -6:]}
    return np.median(np.concatenate([strips[e].reshape(-1, 3) for e in edges]), axis=0)


def flood_alpha(rgb, hard, soft, edges):
    dist = np.linalg.norm(rgb - border_colour(rgb, edges), axis=2)
    labels, _ = ndimage.label(dist < hard + soft)
    sides = {"t": labels[0], "b": labels[-1], "l": labels[:, 0], "r": labels[:, -1]}
    touching = set()
    for e in edges:
        touching.update(np.unique(sides[e]).tolist())
    touching.discard(0)
    background = np.isin(labels, list(touching))
    alpha = np.where(background, np.clip((dist - hard) / soft, 0, 1), 1.0)
    return np.clip(ndimage.gaussian_filter(alpha, 1.2), 0, 1)


def luma(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def cut(project, name, spec):
    src = os.path.join(project, "assets", "gen", name + ".png")
    if not os.path.exists(src):
        return f"{name}: missing {src} (generate it first)"
    rgb = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32)
    mode = spec.get("mode", "flood")
    if mode == "luma":
        lum = luma(rgb)
        paper = np.percentile(lum, 99)
        alpha = np.clip((paper - lum) / (paper * 0.3), 0, 1) ** 0.55
        rgb = np.dstack([lum * 0.55 + 40] * 3)
    elif mode == "bright":
        alpha = np.clip((luma(rgb) - 14) / 70, 0, 1) ** 0.7
    elif mode == "flood":
        alpha = flood_alpha(rgb, spec.get("hard", 28), spec.get("soft", 18), spec.get("edges", "tlrb"))
    else:
        return f"{name}: unknown cutout mode {mode!r}"
    if spec.get("erode"):
        alpha = ndimage.grey_erosion(alpha, size=(spec["erode"], spec["erode"]))
    img = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8))
    if spec.get("flip") == "v":
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif spec.get("flip") == "h":
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    os.makedirs(os.path.join(project, "assets", "cut"), exist_ok=True)
    img.save(os.path.join(project, "assets", "cut", name + ".png"))
    return f"{name}: {mode}, {np.mean(alpha > 0.5):.0%} opaque"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    project = sys.argv[1]
    with open(os.path.join(project, "shots.json")) as f:
        shots = json.load(f)["shots"]
    names = sys.argv[2:] or [n for n, s in shots.items() if s.get("cutout")]
    for n in names:
        if n not in shots or not shots[n].get("cutout"):
            print(f"{n}: no cutout spec in shots.json")
            continue
        print(cut(project, n, shots[n]["cutout"]))


if __name__ == "__main__":
    main()
