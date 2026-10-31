# Plates: generating and cutting images

## shots.json

```json
{
  "model": "black-forest-labs/flux-3-image-klein",
  "resolution": "2K",
  "blocks": { "PHOTO": "Cinematic photoreal film still, ...", "ISOLATE": "Isolated on a plain pure white background, ..." },
  "shots": {
    "cemetery": { "ratio": "16:9", "prompt": "The Normandy American Cemetery ... $PHOTO" },
    "column":   { "ratio": "9:16", "prompt": "A tall classical stone column ... $ISOLATE",
                  "cutout": { "mode": "flood", "edges": "tlrb", "hard": 26, "soft": 18 } },
    "newspaper": { "ratio": "16:9", "ref": "warroom", "prompt": "... a photo that is exactly the attached image ...",
                  "cutout": { "mode": "flood", "edges": "tlrb", "hard": 22, "soft": 16, "erode": 7 } }
  }
}
```

- `$NAME` pulls in a shared block, so every plate carries the same look words.
- `ratio`: 16:9 for scene plates, 21:9 for maps and wide passers, 9:16 for tall columns
  and objects, 1:1 for textures.
- `ref`: another shot passed as a reference image (generated after it). Use it to put
  the next scene's plate inside a newspaper or photo, so a zoom-through matches.
- 2K returns 2736x1536 at 16:9 (3136x1344 at 21:9). That leaves room to push in to about
  1.4x before softness shows.
- Cost: about $0.014 a plate. `IMAGE_MODEL=<openrouter id>` overrides the model for one
  run; `gen_plates.py <dir> name1 name2` regenerates just those.

## Writing prompts that work in this style

- Say the period, the place, the light and the lens. Overcast, diffuse, muted. Name the
  film stock feel for archival plates: "Authentic 1943 black and white press photograph,
  grainy".
- Compose for the camera move: where the subject sits, what is in the foreground, what
  the camera will travel across. A plate that will be panned must be wider than it
  looks in one frame.
- Cutouts go on plain white (or black for bright matter like spray) with "nothing else in
  the image", full height of the frame, sharp edges. The keyer then needs no AI matte.
- Text in plates: a big headline renders well; small print, city names on maps and
  numbers on calendars come out garbled. Build anything the viewer must read in HTML
  (the calendar block does).
- Real people: the model approximates them. Archival framing (black and white, distance,
  a group) hides the gap better than a close-up.

## Cutouts

`cut_layers.py <dir>` cuts every shot with a `cutout` spec into `assets/cut/<name>.png`:

| mode | for | knobs |
|---|---|---|
| flood | objects, people, paper on white | `edges` the background touches (t l r b), `hard`/`soft` colour distance, `erode` px to pull in a light fringe |
| luma | smoke or dust on white | none |
| bright | spray, sparks, snow on black | none |

`flip: "v"` or `"h"` flips the result. Check every cutout on a checkerboard before
using it: the flood mode keeps light areas inside the subject (a grey hull, tan paper)
only when they don't touch the chosen edges, so pick the edges the background actually
reaches.

## Measuring a plate

`python3 frames.py grid assets/gen/plate.jpg /tmp/grid.jpg` draws a labelled pixel grid.
Read off what a scene points at: the box a zoom lands in, the headstone the text hides
behind, the route's start city, the photo on a desk. Re-measure after regenerating a
plate.
