# Hand-offs: how one world becomes the next

Every scene change is caused by something on screen. Pick from this list in the beat
sheet; use four or more kinds in a minute and never the same kind twice in a row.

| Hand-off | What the viewer sees | Block | Timing that matters |
|---|---|---|---|
| Seam pass | The camera trucks right past a tall column of spray or smoke close to the lens; the old world is left of its centre, the new world right of it | title-open exit + seam-pass | One camera value for every layer. The previous scene's exit and this scene's camera share start, distance, length and ease. Blur peaks mid-move. |
| Boom up | The near layer (soldiers in a boat) sinks and grows out of the bottom while the far plate (the lone boat) pushes in | seam-pass `boom` | The drop and the push share one window (about 1.45 s); the drop eases in (power2.in) so the near layer lingers, the push eases both ways. If the push starts late the viewer sees "slide, then zoom". |
| Object wipe | A huge soft object (cross, column, trunk) sweeps right to left; the new world exists only right of its centre line | object-wipe | The object is 1.5-2x frame height, blurred 7-9 px, darker than the scene. Hard clip at its centre line, so the line is never visible. |
| Handheld paper in | A document in two hands slides in from the side, very close and soft, then pulls back to a handheld hold | handheld-paper | One continuous move: a 0.45 s lead with no ease, then a 1.25 s power2.out pull-back. Blur 16 px to 0 over 1 s. The scene behind defocuses (9-10 px). |
| Zoom-through | The camera pushes into a picture (a newspaper photo, a pinned print) until the picture is the next scene | handheld-paper `zoom`, map-route | The picture box is 16:9 and holds the next scene's plate, so the next scene starts at scale 1 on the same pixels. Desaturate the inset and bring its colour back during the zoom. |
| Drop away | The paper fills the frame, then the hands lower it out of frame, revealing a desk | handheld-paper `drop` | Swap the under-plate in only while the paper covers the frame. 1.0 s power2.in drop with vertical blur. |
| Dive | The camera pushes hard into a detail (the map on a table, a date) and blurs; the next scene sharpens in underneath | plate-push `dive`, calendar-dive | Push 1.45 s power2.in to about 2.5x; blur 0 -> 16 px over the last 0.7 s; the next scene starts 0.3 s before the dive ends, blur 18-20 px -> 0 over 0.6-0.75 s. Aim the dive at something bright, never at a dark corner (a black frame reads as a glitch). |
| Cover pass | Something wider than the frame (a tank hull) rolls past; while it covers everything, the world changes | cover-pass | The passer is wider than the frame; swap at the middle of the covered stretch; horizontal blur peaks mid-pass. |
| Red line | A glowing line draws itself (a route east, a pen arc to a date) and the camera follows its head | map-route, calendar-dive, plate-push `line` | Draw 0.5-2.7 s, sine.inOut; the camera follows with the same ease, starting 0.05 s earlier. |

## Not in this style

Crossfades between two worlds, hard cuts, whip pans with smears, wipes with shapes,
zoom-blur "punches", text that slides or bounces in, kinetic typography.
