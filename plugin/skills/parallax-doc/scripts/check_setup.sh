#!/usr/bin/env bash
# Check that everything parallax-doc needs is installed. Prints what is missing and how to get it.
ok=1
need() { if command -v "$1" >/dev/null 2>&1; then echo "ok    $1"; else echo "MISSING $1: $2"; ok=0; fi; }
need ffmpeg "brew install ffmpeg  (or apt install ffmpeg)"
need ffprobe "comes with ffmpeg"
need npx "install Node.js 18+ from nodejs.org"
need python3 "install Python 3.9+"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import PIL, numpy, scipy" 2>/dev/null; then echo "ok    python packages"
  else echo "MISSING python packages: python3 -m pip install -r $(cd "$(dirname "$0")/.." && pwd)/requirements.txt"; ok=0; fi
fi
if command -v npx >/dev/null 2>&1; then
  v=$(npx --yes hyperframes --version 2>/dev/null | tail -1)
  [ -n "$v" ] && echo "ok    hyperframes $v" || { echo "MISSING hyperframes: npx --yes hyperframes --version should print a version"; ok=0; }
fi
[ -n "${OPENROUTER_API_KEY:-}" ] && echo "ok    OPENROUTER_API_KEY is set" || echo "note  OPENROUTER_API_KEY is not set: needed for gen_plates.py (openrouter.ai/keys)"
[ $ok = 1 ] && echo "ready" || { echo "fix the missing items above"; exit 1; }
