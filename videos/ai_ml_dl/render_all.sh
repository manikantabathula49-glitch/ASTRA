#!/usr/bin/env bash
# Render all 80 clips in parallel.
#   ./render_all.sh            -> 1080p30 final renders into out/
#   ./render_all.sh preview    -> fast 480p15 previews into out_preview/
# Optional: MANIM=/path/to/manim  JOBS=4  ONLY="C01_x C02_y"
set -euo pipefail
cd "$(dirname "$0")"
MANIM="${MANIM:-manim}"
JOBS="${JOBS:-4}"
WORK="${WORK:-/tmp/manim_work}"
if [ "${1:-}" = "preview" ]; then
  RES="854,480"; FPS=15; OUT=out_preview
else
  RES="1920,1080"; FPS=30; OUT=out
fi
mkdir -p "$OUT" "$WORK"
if [ -n "${ONLY:-}" ]; then
  SCENES="$ONLY"
else
  SCENES=$(grep -oE '^    \([0-9], "[a-z0-9_]+"' clips.py | awk -F'"' '{printf "C%02d_%s\n", NR, $2}')
fi
export MANIM RES FPS OUT WORK
printf '%s\n' $SCENES | xargs -P "$JOBS" -I{} bash -c '
  s={}
  if "$MANIM" -r "$RES" --frame_rate "$FPS" --media_dir "$WORK/$s" -o "$s" clips.py "$s" > "$WORK/$s.log" 2>&1; then
    f=$(find "$WORK/$s/videos" -name "$s.mp4" -not -path "*partial*" | head -1)
    cp "$f" "$OUT/$s.mp4" && echo "OK   $s"
  else
    echo "FAIL $s (see $WORK/$s.log)"
  fi'
