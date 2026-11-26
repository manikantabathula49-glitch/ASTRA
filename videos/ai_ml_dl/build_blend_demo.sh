#!/usr/bin/env bash
# Demo: Flow clip -> zoom into laptop -> diagram -> brush wipe -> Flow clip with pop-out bubbles.
# Usage: ./build_blend_demo.sh <flow_clip.mp4> <diagram.mp4> <BrushMask.mp4> <PopBubbles.mov> <out.mp4>
# LAPTOP_X/LAPTOP_Y = where to zoom (in 1920x1080 coordinates).
set -euo pipefail
FLOW=$1; DIAG=$2; MASK=$3; BUB=$4; OUT=$5
LX=${LAPTOP_X:-1290}; LY=${LAPTOP_Y:-740}
T=$(mktemp -d)
V="-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -an"
N="fps=30,format=yuv420p,setsar=1"

# 1. normalise the Flow clip to 1080p30
ffmpeg -v error -y -i "$FLOW" -vf "scale=1920:1080:flags=lanczos,$N" $V $T/flow.mp4
# 2. intro part (0-4s) + 1s push-in toward the laptop
ffmpeg -v error -y -i $T/flow.mp4 -t 4 $V $T/a.mp4
ffmpeg -v error -y -ss 4 -t 1 -i $T/flow.mp4 -vf "zoompan=z='1+0.075*on':x='$LX-iw/zoom/2':y='$LY-ih/zoom/2':d=1:s=1920x1080:fps=30,$N" $V $T/zoom.mp4
ffmpeg -v error -y -i $T/a.mp4 -i $T/zoom.mp4 -filter_complex "[0][1]concat=n=2:v=1" $V $T/a2.mp4
# 3. diagram (first 9s), entered with a white flash cross-fade
ffmpeg -v error -y -t 9 -i "$DIAG" -vf "$N" $V $T/diag.mp4
ffmpeg -v error -y -i $T/a2.mp4 -i $T/diag.mp4 -filter_complex "[0][1]xfade=transition=fadewhite:duration=0.4:offset=4.6,$N" $V $T/part1.mp4
# 4. Flow clip 5-8s slowed to 5s, with pop-out bubbles from 1.0s
ffmpeg -v error -y -ss 5 -i $T/flow.mp4 -i "$BUB" -filter_complex \
  "[0]setpts=PTS*1.667,$N[b];[1]setpts=PTS+1.0/TB[o];[b][o]overlay=0:0:eof_action=pass,$N" -t 5 $V $T/c.mp4
# 5. brush wipe: last 1s of the diagram -> first 1s of part c, through the painted mask
D1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/part1.mp4)
ffmpeg -v error -y -sseof -1 -i $T/part1.mp4 -t 1 -i $T/c.mp4 -t 1 -i "$MASK" -filter_complex \
  "[0]format=gbrp[x];[1]format=gbrp[y];[2]scale=1920:1080,fps=30,format=gbrp[m];[x][y][m]maskedmerge,$N" -t 1 $V $T/wipe.mp4
ffmpeg -v error -y -t $(python3 -c "print($D1-1)") -i $T/part1.mp4 $V $T/p1cut.mp4
ffmpeg -v error -y -ss 1 -i $T/c.mp4 $V $T/c2.mp4
ffmpeg -v error -y -i $T/p1cut.mp4 -i $T/wipe.mp4 -i $T/c2.mp4 -filter_complex "[0][1][2]concat=n=3:v=1" $V "$OUT"
rm -rf $T
echo "done: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s)"
