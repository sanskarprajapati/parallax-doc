# Review before you deliver

1. **Whole film at a glance**:
   `python3 $SKILL/scripts/frames.py sheet film/renders/raw.mp4 /tmp/sheet.jpg --every 0.5`.
   Read it start to end. Look for a blank or black frame, a plate that pops, text cut off
   by the frame edge, or text unreadable on a bright area (move it or darken under it).
2. **Every hand-off frame by frame**: `npx hyperframes snapshot --at t-0.2,t,t+0.2` for
   each seam, or a compare sheet against the reference. Each seam must read as one
   continuous move, never two steps.
3. **Text against the voice**: each typed line starts on its word in words.json (up to
   0.5 s after, never before) and is fully on screen long enough to read: about 0.5 s
   plus 0.3 s a word.
4. **The finished file**: check that it is exactly the target length, the narration
   sits around -21 dB mean with peaks no higher than -3 dB, and the bed is audible but
   under the voice.
5. **Deliver**: send the 720p preview, say where the full file is, and list honestly what
   is still rough (garbled plate text, reconstructed faces, any seam you would still
   fix).
