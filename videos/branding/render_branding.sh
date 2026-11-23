#!/usr/bin/env bash
# Render the branding pack into out/
#   *.mp4        dark background (preview / full-frame use)
#   *_alpha.mov  transparent background (Premiere, DaVinci, Final Cut, CapCut desktop)
#   *_green.mp4  green screen (CapCut mobile, VN: use Chroma Key)
set -euo pipefail
cd "$(dirname "$0")"
MANIM="${MANIM:-manim}"
WORK="${WORK:-/tmp/branding_work}"
mkdir -p out
SCENES=$(grep -oE '^    \("[a-z_]+"' branding.py | tr -d ' ("' | sed 's/^/Sub_/')
R="-r 1920,1080 --frame_rate 30"
pick() { find "$WORK/$1" -name "$2" -not -path "*partial*" | head -1; }
# intro: full frame only
$MANIM $R --media_dir "$WORK/intro" branding.py BrandIntro >/dev/null 2>&1
cp "$(pick intro BrandIntro.mp4)" out/BrandIntro.mp4 && echo "OK BrandIntro"
for s in BrandTransition $SCENES; do
  (
    $MANIM $R -t --format mov --media_dir "$WORK/$s-a" branding.py "$s" >/dev/null 2>&1
    cp "$(pick "$s-a" "$s.mov")" "out/${s}_alpha.mov"
    GREEN=1 $MANIM $R --media_dir "$WORK/$s-g" branding.py "$s" >/dev/null 2>&1
    cp "$(pick "$s-g" "$s.mp4")" "out/${s}_green.mp4"
    $MANIM $R --media_dir "$WORK/$s-d" branding.py "$s" >/dev/null 2>&1
    cp "$(pick "$s-d" "$s.mp4")" "out/${s}.mp4"
    echo "OK $s"
  ) &
done
wait
