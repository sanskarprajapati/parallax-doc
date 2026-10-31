# Breaking down a reference video

When the person gives a reference, study every frame before building anything. Skimming
a few frames misses the transitions, which are the style.

```bash
python3 $SKILL/scripts/frames.py breakdown reference.mp4 work/ref
```

This writes every frame, labelled 16-up contact sheets (`#frame time`), `diffs.txt`
(mean difference from the previous frame) and `audio16k.wav`. It reports hard cuts and
whether the video was cut at 24 fps inside a 30 fps export.

Then:

1. **Read every sheet**, in order. Note for each frame range: what is on screen, what the
   camera does (push, pull, truck, tilt, boom, handheld), what enters or leaves and how,
   what text appears letter by letter (write down the frame of each letter), and any
   overlay (grain, dust, scratches, streaks, dots).
2. **Find the hand-offs**: where one world becomes another. Diffs rise smoothly through
   a camera move and spike on a cut. Look at those frames at full size.
3. **Transcribe**: `npx hyperframes transcribe work/ref/audio16k.wav` for word timings.
   Line up each typed text with its word.
4. **Measure the look** on a few full-size frames: saturation, contrast, vignette, the
   accent colour, the fonts (match them with a side-by-side of candidates), grain size.
5. **Write BREAKDOWN.md**: specs, narration with timings, shot by shot with frame
   numbers, the look, the type system and an asset list. That document is the spec you
   build against.

## Comparing your render to the reference

```bash
ffmpeg -i reference.mp4 -vsync 0 -q:v 3 work/ref/frames/f%04d.jpg   # done by breakdown
ffmpeg -i film/renders/raw.mp4 -vsync 0 -q:v 3 work/mine/f%04d.jpg
python3 $SKILL/scripts/frames.py compare work/ref/frames work/mine work/cmp_seam1.jpg 116,124,132,138,144,150,158,168
```

Eight moments across each hand-off, reference above, yours below. This is how the
transition problems get found: the two moves in a boom running one after the other, a
crossfade where the reference passes behind an object, a black frame in a dive. Fix and
compare again until they move the same way.
