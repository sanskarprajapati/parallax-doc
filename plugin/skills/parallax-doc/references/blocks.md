# The block library

Each block is one scene: `blocks/<name>.html`, copied into a film by
`scripts/add_scene.py <film> <block> <id> <start> <dur>`, which swaps `{{id}}` for the
scene id and adds the host to `film/index.html`. Then edit three things in the copy:

1. **Plate paths**: the `src` of each `<img>` (`assets/gen/*.jpg` for opaque plates,
   `assets/cut/*.png` for cutouts).
2. **Text**: each text element's `data-text`. `|` toggles red on and off
   (`"That is not\nin |question|"`); `&#10;` or `\n` breaks the line. Empty `data-text`
   means no text.
3. **CONFIG**: the object at the top of the script. Times are seconds on the scene's own
   clock (0 = its host's `data-start`). Camera framings are `[scale, cx, cy]`: the plate
   point (cx, cy) sits at the frame centre at that scale. Read cx, cy off the plate with
   `frames.py grid`.

All blocks load `assets/lib/parallax.js` (typeOn, cameraRig, driver, frame, seamMask,
clipRightOf, motionBlur) and share the type classes in `film/index.html`
(`.pd-script`, `.pd-label`, `.pd-title`).

## title-open

The cold open: waving flag or banner, an archival cutout rising from the bottom edge, a
heavy title and a typed date, the camera pulling back off the title.
Plates: `flag.jpg` (opaque, waves via canvas), `archival.png` (cutout, white background
keyed with edges "t").
CONFIG: `wave`, `pullBack`, `drift`, `riser`, `date`, `exit` (truck left for a seam pass:
same `at`, `distance`, `dur` as the next scene's camera, measured from this scene's start).

## seam-pass

Camera trucks right past a column; the new world is right of the column's centre; layers
at parallax factors; a near layer sweeps in; optional boom-up at the end.
Plates: `far` (opaque, about 2688x1510 on screen), `subject` (cutout, figure in motion),
`near` (cutout, a crowd or vehicle), `column` (cutout, spray on black keyed with mode
"bright", used twice mirrored), `strip` (cutout, ground texture along the bottom).
Host start = the previous scene's `exit.at`.

## object-wipe

A soft giant object passes right to left; the new plate opens behind it; dolly between
two framings; label and emphasis line; an occluder redraws a polygon of the plate over
the text so the words sit behind something.
Plates: `plate` (opaque), `object` (cutout, tall). Set `object.centre` to the object's
centre line in its scaled image. Occluder: set `#<id>-occluder { clip-path: polygon(...) }`
in plate pixels around the thing in front (measure with `frames.py grid`).

## handheld-paper

Paper in two hands: lead in, pull back, sway; exit `zoom` into the printed picture or
`drop` to reveal a desk with a line in perspective.
Plates: `paper` (cutout incl. hands, white background, erode 6-7 px), `next` (the next
scene's plate, for zoom) or `under` (for drop). Measure the picture box on the paper
plate, keep it 16:9, and set `zoom.to` to `[1920 / box width, box centre x, box centre y]`.

## plate-push

The workhorse: a plate, a moving camera, label + emphasis line, optional passer
(foreground object drifting past), shake, red line, perspective text, defocus, and a
`dive` exit. Text stays on screen while the camera moves unless `textOnPlate: true`
(words lying on a table or a map, moving with it). `entry: "cut-in"` when a zoom-through landed on this plate (start at scale 1),
`"blur-in"` after a dive.

## map-route

A wide old map; arrives under a dive's blur; red route draws while the camera follows;
a pinned print at the far end that the camera turns and zooms into.
Plates: `map` (opaque, 21:9; city names will be garbled, so keep labels you need in
HTML), `print` (the next scene's plate). Route: an SVG path in map pixels.

## calendar-dive

A month built in HTML (correct weekdays), paper texture, first date circled, a red pen
arc and note to the second date, then a dive into it.
Plates: `paper` (opaque flat texture). CONFIG `month.firstWeekday`: 0 = Sunday. Check
the weekday of the 1st for your month and year (June 1944 = Thursday = 4).

## cover-pass

A passer wider than the frame rolls left to right; the world swaps while it covers the
frame; slow push; one or two lines in turn; optional fade to black to end the film.
Plates: `plate` (opaque), `passer` (cutout, 21:9, "edges": "tb").

## Hand-built scenes

The D-Day example's scenes (examples/dday/film/compositions) predate the blocks and do
the same moves by hand. When a scene needs something no block does (text behind a
headstone with its own dolly, a stone cross built from texture divs), start from the
closest example file instead.
