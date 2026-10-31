#!/usr/bin/env bash
# A low, dark ambient drone to sit under the narration (no music licence needed).
#   make_bed.sh <project-dir> <seconds> [loudness LUFS, default -30]
# Writes <project>/assets/vo/bed.m4a. Replace it with a real score when you have one.
set -euo pipefail
PROJECT=${1:?project dir}; DUR=${2:?seconds}; LUFS=${3:--30}
[[ $DUR =~ ^[0-9]+(\.[0-9]+)?$ ]] || { echo "seconds must be a number" >&2; exit 1; }
[[ $LUFS =~ ^-[0-9]+(\.[0-9]+)?$ ]] || { echo "loudness must be a negative number, e.g. -30" >&2; exit 1; }
mkdir -p "$PROJECT/assets/vo"
FADE_OUT=$(awk -v d="$DUR" 'BEGIN { f = d - 2.5; if (f < 0) f = 0; print f }')
L="0.30*sin(2*PI*55*t)*(0.75+0.25*sin(2*PI*0.07*t))+0.20*sin(2*PI*82.4*t)*(0.7+0.3*sin(2*PI*0.05*t+1))+0.12*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.09*t+2))+0.05*sin(2*PI*164.8*t)*(0.5+0.5*sin(2*PI*0.11*t))"
R="0.30*sin(2*PI*55.3*t)*(0.75+0.25*sin(2*PI*0.07*t+0.5))+0.20*sin(2*PI*82.1*t)*(0.7+0.3*sin(2*PI*0.05*t+1.5))+0.12*sin(2*PI*110.4*t)*(0.6+0.4*sin(2*PI*0.09*t+2.5))+0.05*sin(2*PI*165.2*t)*(0.5+0.5*sin(2*PI*0.11*t+1))"
ffmpeg -v error -y \
  -f lavfi -i "aevalsrc='$L|$R':s=44100:d=$DUR" \
  -f lavfi -i "anoisesrc=color=brown:amplitude=0.25:seed=7:d=$DUR:r=44100" \
  -filter_complex "[1]lowpass=f=300,volume=0.35,aformat=channel_layouts=stereo[n];[0][n]amix=inputs=2,lowpass=f=900,afade=t=in:d=2,afade=t=out:st=$FADE_OUT:d=2.5,loudnorm=I=$LUFS:TP=-6[a]" \
  -map "[a]" -c:a aac -b:a 192k "$PROJECT/assets/vo/bed.m4a"
echo "wrote $PROJECT/assets/vo/bed.m4a ($DUR s, $LUFS LUFS)"
