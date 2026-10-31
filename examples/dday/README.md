# Example: D-Day, the strategic reality (60 s)

The film this style was built on, as scene code plus every image prompt. No images or
audio are included: you regenerate them (about $0.30 of images on OpenRouter, plus a
narration take from any TTS or your own voice).

These scenes are hand-built (they came before the block library), so they are the best
place to see every transition done for real: open `film/compositions/landing.html` for
the seam pass and boom, `cemetery.html` for the object wipe with text behind a
headstone, `news.html` for the handheld paper and zoom-through.

## Build it

```bash
SKILL=path/to/plugin/skills/parallax-doc       # where the plugin's skill lives
FILM=~/films/dday
$SKILL/scripts/new_film.sh $FILM 60
cp -R film/. $FILM/film/
cp shots.json SCRIPT.md $FILM/

export OPENROUTER_API_KEY=...                   # your key, from openrouter.ai
python3 $SKILL/scripts/gen_plates.py $FILM      # 22 plates, about $0.30
python3 $SKILL/scripts/cut_layers.py $FILM      # cutouts into assets/cut
ffmpeg -i $FILM/film/assets/gen/stone_tex.jpg -vf transpose=2 $FILM/film/assets/gen/stone_tex_h2.jpg

# narration: record or synthesise SCRIPT.md's text as one take, then fit it to 60 s
python3 $SKILL/scripts/fit_voice.py $FILM take.mp3 60
$SKILL/scripts/make_bed.sh $FILM 60

$SKILL/scripts/render.sh $FILM dday
```

Generated plates differ from run to run. Where a scene points at something inside a
plate (the headstone the text hides behind, the photo box on the newspaper, the
calendar on the desk), re-measure it on your plate with a grid (see
references/plates.md) and update the numbers in that scene.
