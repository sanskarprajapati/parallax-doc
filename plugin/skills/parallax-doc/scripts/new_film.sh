#!/usr/bin/env bash
# Scaffold a parallax-doc film:
#   new_film.sh <dir> [seconds, default 60]
# Creates <dir>/film   (the scenes: a HyperFrames project) and
#         <dir>/finish (the film look applied to the rendered film)
# plus <dir>/shots.json (the image plates) and <dir>/SCRIPT.md (narration and beats).
set -euo pipefail
DIR=${1:?usage: new_film.sh <dir> [seconds]}
DUR=${2:-60}
[[ $DUR =~ ^[0-9]+$ ]] || { echo "seconds must be a whole number" >&2; exit 1; }
HERE="$(cd "$(dirname "$0")/.." && pwd)"
if [ -e "$DIR/film" ] || [ -e "$DIR/finish" ]; then
  echo "$DIR already has a film/ or finish/ folder; pick a new directory" >&2
  exit 1
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (brew install ffmpeg)" >&2; exit 1; }
command -v npx >/dev/null || { echo "Node.js 18+ is required for the HyperFrames CLI" >&2; exit 1; }

mkdir -p "$DIR"
for part in film finish; do
  npx --yes hyperframes init "$DIR/$part" >/dev/null
  cp -R "$HERE/template/$part/." "$DIR/$part/"
done
mkdir -p "$DIR/film/compositions" "$DIR/film/assets/gen" "$DIR/film/assets/cut" "$DIR/film/assets/vo"
sed -i.bak "s/data-duration=\"60\"/data-duration=\"$DUR\"/g" "$DIR/film/index.html" "$DIR/finish/index.html"
rm -f "$DIR/film/index.html.bak" "$DIR/finish/index.html.bak"
cp "$HERE/template/shots.json" "$DIR/shots.json"
cp "$HERE/template/SCRIPT.md" "$DIR/SCRIPT.md"
# plates are generated and cut into the film's assets
ln -s film/assets "$DIR/assets"
echo "film scaffolded in $DIR ($DUR s)"
echo "  $DIR/SCRIPT.md    narration and beat sheet"
echo "  $DIR/shots.json   image plates (gen_plates.py / cut_layers.py read it)"
echo "  $DIR/film         scenes: add_scene.py $DIR/film <block> <id> <start> <dur>"
echo "  $DIR/finish       the look; render.sh $DIR renders both passes"
