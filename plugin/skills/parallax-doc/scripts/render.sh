#!/usr/bin/env bash
# Render a parallax-doc film in two passes and make a small preview copy.
#   render.sh <dir> [name]
# 1. film/   -> film/renders/raw.mp4       (the scenes, no look)
# 2. finish/ -> <dir>/<name>.mp4           (grade, grain, dust, dots, scratches + voice and bed)
# 3. <dir>/<name>-preview.mp4              (720p, small enough to send around)
set -euo pipefail
DIR=${1:?usage: render.sh <dir> [name]}
NAME=${2:-$(basename "$(cd "$DIR" && pwd)")}
[ -f "$DIR/film/assets/vo/vo.m4a" ] || { echo "no narration: run fit_voice.py first" >&2; exit 1; }

(cd "$DIR/film" && npx --yes hyperframes render --output renders/raw.mp4)
cp "$DIR/film/renders/raw.mp4" "$DIR/finish/assets/raw.mp4"
cp "$DIR/film/assets/vo/vo.m4a" "$DIR/finish/assets/vo.m4a"
if [ -f "$DIR/film/assets/vo/bed.m4a" ]; then
  cp "$DIR/film/assets/vo/bed.m4a" "$DIR/finish/assets/bed.m4a"
else
  echo "no bed.m4a: using silence (make_bed.sh adds an ambient drone)"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/film/assets/vo/vo.m4a")
  ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=stereo -t "$DUR" -c:a aac "$DIR/finish/assets/bed.m4a"
fi
(cd "$DIR/finish" && npx --yes hyperframes render --output "renders/$NAME.mp4")
cp "$DIR/finish/renders/$NAME.mp4" "$DIR/$NAME.mp4"
ffmpeg -v error -y -i "$DIR/$NAME.mp4" -vf scale=1280:720 -c:v libx264 -crf 26 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 128k "$DIR/$NAME-preview.mp4"
echo "done: $DIR/$NAME.mp4 and $DIR/$NAME-preview.mp4"
