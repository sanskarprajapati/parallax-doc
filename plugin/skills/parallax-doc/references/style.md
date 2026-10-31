# The style, in numbers

Measured frame by frame from the reference this style was built on (a 21.5 s documentary
opener, 646 frames), then held across a 60 s film. "Measured" means read off frames;
"set" means chosen to match by eye.

## Format

| | |
|---|---|
| Frame | 1920x1080, 16:9 |
| Rate | Cut at 24 fps in the reference (every 5th frame of its 30 fps export repeats). Render at 30; the motion reads the same. |
| Length | 60 s works: 13 scenes, 4.6 s average, 3-7 s each |
| Cuts | None. 0 hard cuts in 646 frames (measured). Every change of world happens inside a camera move. |

## Camera

- Always moving. Even a "hold" drifts: scale +0.03-0.07 over the hold.
- Eases: camera trucks and pans `sine.inOut`; arrivals `power2.out`/`power3.out`;
  dives and zoom-throughs into a detail `power3.in` or `sine.out` for a zoom that lands
  softly; drops out of frame `power2.in`. No linear moves except constant drift.
- Typical pushes: 1.0 -> 1.12-1.6 over a scene; zoom-throughs 0.8 -> 3.3-3.9.
- Parallax: 3-5 planes. Factors used: far plate 0.2, mid subject 1.15-1.2, the column
  1.35, foreground strip 1.6-2.2 (set).
- Motion blur on fast moves: 5 px horizontal at the peak of a truck, 10-22 px on objects
  passing the lens, vertical 10-14 px on a drop (set).
- Handheld: rotation up to 0.9 deg and 7 px of vertical sway over about 2 s (set).
- Shake for armour or artillery: about 3 px, layered sines (set).

## Type

| Role | Face | Size | Colour | Animation |
|---|---|---|---|---|
| Opening title | Inter 800 | 112 px | #f4f1ea, dark drop shadow | static; the camera pulls back off it |
| Date / place label | Inter 500-600, letter-spacing 0.18em for caps | 34 px | #f4f1ea | typed, 3 frames a letter |
| Emphasis line | Cormorant Upright 600 (the reference used Gabriola) | 96-150 px | #f4f1ea, white glow 12 px + dark shadow | typed, 1.5-3 frames a letter |
| The red word | same | same | #ff1f35, bloom 12/34/70 px | typed with its line |

- Typing starts on the narrated word, or up to 0.5 s after it (measured: the reference's
  "That is not in question" lands 0.5 s after the voice). Never before.
- One emphasis line per scene, at most two short lines. One red word per line.
- Placement in depth (measured in the reference, used throughout): the words sit behind
  a foreground object (a headstone's top redrawn over them), lie in perspective on a
  surface (`perspective(1100px) rotateX(18deg) rotateY(-12deg) rotateZ(-3deg)`), or are
  pinned to a plate so they move with the camera. Free-floating screen text is the
  exception (labels).
- Text leaves with its world (covered by the next scene) or blurs out in 0.25 s.

## Colour and look (the finish pass)

The grade on the whole film, as HyperFrames media-treatment values:

| Control | Value |
|---|---|
| exposure | +0.04 |
| contrast | +0.14 |
| highlights | -0.15 |
| shadows | +0.04 |
| blacks | +0.08 (lifted, never pure black) |
| temperature | -0.12 (cool) |
| saturation | -0.24 |
| vignette | 0.42, midpoint 0.38, feather 0.7 |
| grain | 0.35, size 0.3 |
| film artifacts (dust) | 0.5 |
| channel separation | 0.14 |

Plus a 6 px dot grid at 12% multiply over everything, and 2 px vertical scratches at
50% white for 6-11 frames, every 4-5 s, at varying x. The reference also has thin
bright horizontal streaks on sea horizons; add them per scene when a horizon is in shot.

Too strong reads cheap: the first pass at -0.38 saturation, 0.28 channel split and
0.55 vignette was darker and duller than the reference and killed the red. Compare
against the reference before raising any of these.

## Palette in the plates

Muted olive, steel blue-grey, sand, overcast white skies; colour scenes at roughly half
saturation before the grade. Archival plates are true black and white. The red accent
appears only as the text bloom, red pen and red route lines, and small props (a stamp, a
circled date).

## Sound

Narration around -21 dB mean, peaks -4 dB; a low drone bed about 9 dB under the voice
(-30 LUFS). The reference had a quiet score; replace the drone with music when you have
one.
