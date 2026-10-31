#!/usr/bin/env python3
"""Generate a film's image plates from its shots.json, through OpenRouter.

    OPENROUTER_API_KEY=... python3 gen_plates.py <project-dir> [shot ...]

Reads  <project>/shots.json   (see references/plates.md for the format)
Writes <project>/assets/gen/<shot>.png and a .jpg copy for opaque plates.

With no shot names it generates every shot that has no image yet; shots with a
"ref" run after the shot they reference. Pass names to (re)generate just those.
The key is read from the environment only and never written anywhere.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://openrouter.ai/api/v1/images/generations"
DEFAULT_MODEL = "black-forest-labs/flux-3-image-klein"
DEFAULT_RESOLUTION = "2K"


def load_shots(project: str) -> dict:
    with open(os.path.join(project, "shots.json")) as f:
        data = json.load(f)
    blocks = data.get("blocks", {})
    shots = {}
    for name, shot in data["shots"].items():
        prompt = shot["prompt"]
        for key, text in sorted(blocks.items(), key=lambda kv: -len(kv[0])):  # "$PHOTO" -> the PHOTO block; longest names first
            prompt = prompt.replace("$" + key, text)
        shots[name] = {**shot, "prompt": prompt}
    return {"model": data.get("model", DEFAULT_MODEL),
            "resolution": data.get("resolution", DEFAULT_RESOLUTION),
            "shots": shots}


def generate(project: str, cfg: dict, name: str) -> str:
    try:
        return _generate(project, cfg, name)
    except Exception as e:  # one bad shot must not abort the batch
        return f"{name}: {type(e).__name__}: {e}"


def _generate(project: str, cfg: dict, name: str) -> str:
    shot = cfg["shots"][name]
    body = {"model": os.environ.get("IMAGE_MODEL", cfg["model"]),
            "prompt": shot["prompt"],
            "aspect_ratio": shot.get("ratio", "16:9"),
            "resolution": cfg["resolution"]}
    if shot.get("ref"):
        with open(os.path.join(project, "assets", "gen", shot["ref"] + ".png"), "rb") as f:
            body["image"] = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        return f"{name}: HTTP {e.code} {e.read()[:300]!r}"
    except urllib.error.URLError as e:
        return f"{name}: network error {e.reason}"
    if not data.get("data"):
        return f"{name}: no image returned ({json.dumps(data)[:300]})"
    item = data["data"][0]
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as r:
            raw = r.read()
    else:
        return f"{name}: response had no image data"
    out = os.path.join(project, "assets", "gen", name + ".png")
    with open(out, "wb") as f:
        f.write(raw)
    if not shot.get("cutout"):
        from PIL import Image  # opaque plates also get a lighter jpg for the compositions
        Image.open(out).convert("RGB").save(out[:-4] + ".jpg", quality=90)
    cost = data.get("usage", {}).get("cost")
    return f"{name}: ok" + (f" (${cost})" if cost is not None else "")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("OPENROUTER_API_KEY is not set. Export it in your shell first.")
    project = sys.argv[1]
    cfg = load_shots(project)
    os.makedirs(os.path.join(project, "assets", "gen"), exist_ok=True)
    wanted = sys.argv[2:]
    unknown = [n for n in wanted if n not in cfg["shots"]]
    if unknown:
        sys.exit(f"Unknown shots: {', '.join(unknown)}")
    if not wanted:
        wanted = [n for n in cfg["shots"]
                  if not os.path.exists(os.path.join(project, "assets", "gen", n + ".png"))]
    first = [n for n in wanted if not cfg["shots"][n].get("ref")]
    second = [n for n in wanted if cfg["shots"][n].get("ref")]
    for batch in (first, second):
        with ThreadPoolExecutor(max_workers=6) as pool:
            for line in pool.map(lambda n: generate(project, cfg, n), batch):
                print(line, flush=True)


if __name__ == "__main__":
    main()
