---
name: parallax-doc
description: Make a short history documentary in the parallax-doc style - one continuous 2.5D camera through layered archival and AI plates, no hard cuts, worlds handing over behind objects passing the lens, calligraphic text typed on with the narration with one word in glowing red, and a desaturated film look with grain, dust and scratches. Use when asked for a documentary or history explainer video about a topic, or to recreate this D-Day style, or to break down a reference video frame by frame and rebuild its style.
---

# parallax-doc

A film in this style is one continuous camera move. There are no hard cuts: every scene
hands over to the next through something on screen (a column of spray, a stone cross
passing the lens, a newspaper held up to camera, a zoom into a photograph, a calendar
date, a tank rolling past). The camera never stops. Text is typed on letter by letter
with the narration, and exactly one word per line is glowing red.

It is built with HyperFrames (HTML scenes rendered frame by frame) in two passes: `film/`
holds the scenes, `finish/` applies the look to the rendered film. Read the HyperFrames
skill (`/hyperframes`) once if it is installed; this skill covers everything specific.

The scripts live in this skill's `scripts/` folder; `$SKILL` below means this skill's
directory.

## Requirements (run `$SKILL/scripts/check_setup.sh` and tell the person what is missing)

- Node.js 18+ (`npx hyperframes`), ffmpeg/ffprobe, Python 3.9+ with `pillow numpy scipy`
- `OPENROUTER_API_KEY` in the environment for images (about $0.014 an image at 2K).
  Never write the key to a file or echo it back.
- A narration take: any TTS (ElevenLabs, `npx hyperframes tts` with Kokoro for free) or
  the person's own recording. Paid TTS: confirm the cost before generating.

## The workflow

1. **Brief.** Topic, length (default 60 s), and the angle. If the person gave a
   reference video, break it down first: `references/analyze-reference.md`.
2. **Script.** `references/script-and-voice.md`. About 2.3 words a second before
   pauses; a turn in the middle ("that's not in question... what is in question").
   Fact-check every claim; prefer a softer true statement over a sharper doubtful one.
   Show the script and get a yes before spending on voice or images.
3. **Scaffold.** `$SKILL/scripts/new_film.sh <dir> <seconds>`.
4. **Voice.** Generate one take of the whole script, then
   `python3 $SKILL/scripts/fit_voice.py <dir> take.mp3 <seconds>`: pauses tightened,
   tempo fitted, `assets/vo/words.json` word timings. Every scene and every typed line
   is timed from words.json, so do this before building scenes.
   `$SKILL/scripts/make_bed.sh <dir> <seconds>` adds a low ambient drone.
5. **Beat sheet.** In SCRIPT.md: one row per scene, its words, plates, block, how it hands
   over, its emphasis line and red word. Scenes run 3-7 s. Choose hand-offs from
   `references/transitions.md`; use at least four kinds and never the same twice in a
   row.
6. **Plates.** Write `shots.json` (`references/plates.md`), then
   `python3 $SKILL/scripts/gen_plates.py <dir>` and `python3 $SKILL/scripts/cut_layers.py <dir>`.
   Look at every plate and cutout (contact sheet on a checkerboard) and regenerate the
   bad ones before building on them.
7. **Scenes.** For each beat: `python3 $SKILL/scripts/add_scene.py <dir>/film <block> <id> <start> <dur>`,
   then edit that file's CONFIG, plate paths and `data-text` lines. Measure targets on
   the plate with `frames.py grid` (a headstone, a photo box, a city). Blocks and their
   knobs: `references/blocks.md`. Scenes overlap: the next host starts where the
   previous one's exit begins.
8. **Check and look.** `cd <dir>/film && npx hyperframes check` (fix errors; "dead
   stretch" warnings are false positives for rig-driven cameras), then
   `npx hyperframes snapshot --at <every hand-off ±0.2 s>` and read the frames.
9. **Render.** `$SKILL/scripts/render.sh <dir> <name>`: film, then the finish pass,
   then a 720p preview.
10. **Review** (`references/review.md`): a 0.5 s contact sheet of the whole film, every
    hand-off frame by frame, and against the reference if there is one. Fix, re-render,
    and send the preview.

## The style in one screen (numbers in references/style.md)

- **Camera:** always moving. Eased moves only (sine.inOut for camera, power2/3 for
  arrivals and dives). Pushes 1.0 -> 1.1-1.6 across a scene. 3-5 depth planes per
  scene, each at its own parallax factor of one camera value.
- **Hand-offs:** the new world appears behind something passing the lens, inside a
  photo the camera zooms into, or under a blur the camera dives through. Never a
  crossfade between two worlds, never a hard cut.
- **Text:** a calligraphic serif (Cormorant Upright 600) in warm white with a soft glow,
  typed at 1.5-3 frames a letter, starting on the narrated word. One red word
  (#ff1f35 with a heavy bloom). Placed in depth: behind a headstone, flat on a table,
  on a map. Small spaced caps (Inter 600) for places and dates. A heavy sans for the
  opening title only.
- **Plates:** muted, overcast, cinematic AI stills mixed with black-and-white
  "archival" photographs; cutouts generated on plain white so they key cleanly.
- **Look:** desaturated and cool, contrast up, a heavy vignette, grain, dust, a fine dot
  grid, vertical scratches, a slight channel split. Sound: narration over a low drone.
- **Red line:** a glowing red line that draws itself (a route on a map, a pen arc on a
  calendar) is the style's second accent. Use it once or twice a minute.

## Rules that keep it working

- Everything visible is a function of timeline time: cameras are rigs whose setters GSAP
  calls on every seek (`cameraRig`, `driver` in assets/lib/parallax.js). No timers, no
  `Math.random`, no `onUpdate` side effects.
- A zoom-through lands exactly on the next scene's first frame: the inset picture is
  16:9 and is the next scene's plate, so the next scene starts at scale 1.
- Two moves that should read as one (a boom: near layer sinks while far layer pushes in)
  share one start, one length and one window. If one finishes first the viewer sees
  two steps.
- Never a blank frame at a hand-off. Snapshot every seam at -0.2, 0, +0.2 s.
- Scene element ids are prefixed with the scene id (blocks do this); a scene's root is
  `id="root"` and is never tweened (tween a child).
- Generated text in plates (signs, maps, newspapers) is often garbled. Keep the words
  that matter as prompt text the model renders well (big headlines) or put them in HTML.
- Real people in AI plates are reconstructions; mention it when you deliver.
