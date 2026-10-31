#!/usr/bin/env python3
"""Add a scene to a film from a block.

    python3 add_scene.py <film-dir> <block> <scene-id> <start-seconds> <duration-seconds>

Copies blocks/<block>.html to <film>/compositions/<scene-id>.html with every {{id}}
replaced, and adds its host to <film>/index.html (z-index = order added, so a later
scene paints over an earlier one where they overlap). Scene ids: lowercase letters,
digits and dashes, unique in the film.
"""
import os
import re
import sys

BLOCKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blocks")

HOST = """      <div
        id="{id}"
        data-composition-id="{id}"
        data-composition-src="compositions/{id}.html"
        data-start="{start}"
        data-duration="{dur}"
        data-track-index="{z}"
        data-track-kind="graphics"
        data-width="1920"
        data-height="1080"
        style="z-index: {z}"
      ></div>
"""


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    film, block, sid, start, dur = sys.argv[1:]
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,30}", sid):
        sys.exit("scene id: lowercase letters, digits and dashes, starting with a letter")
    src = os.path.join(BLOCKS, block + ".html")
    if not os.path.exists(src):
        names = sorted(f[:-5] for f in os.listdir(BLOCKS) if f.endswith(".html"))
        sys.exit(f"no block {block!r}. Blocks: {', '.join(names)}")
    float(start), float(dur)  # validate numbers early
    index = os.path.join(film, "index.html")
    with open(index) as f:
        html = f.read()
    if f'id="{sid}"' in html:
        sys.exit(f"scene {sid!r} is already in {index}")
    marker = "      <!-- SCENES -->\n"
    if marker not in html:
        sys.exit(f"{index} has no '<!-- SCENES -->' marker to insert after")
    dst = os.path.join(film, "compositions", sid + ".html")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src) as f:
        body = f.read().replace("{{id}}", sid)
    with open(dst, "w") as f:
        f.write(body)
    z = len(re.findall(r'data-composition-src="compositions/', html)) + 1
    # keep hosts in the order they were added: insert before the audio after the last host
    pos = html.index(marker) + len(marker)
    tail = html[pos:]
    hosts = list(re.finditer(r"      <div\n        id=\"[^\"]+\"\n        data-composition-id.*?></div>\n", tail, re.S))
    insert_at = pos + (hosts[-1].end() if hosts else 0)
    html = html[:insert_at] + HOST.format(id=sid, start=start, dur=dur, z=z) + html[insert_at:]
    with open(index, "w") as f:
        f.write(html)
    print(f"added {sid} ({block}) at {start}s for {dur}s -> {dst}")
    print("next: open it and set CONFIG, the plate src paths and the data-text lines")


if __name__ == "__main__":
    main()
