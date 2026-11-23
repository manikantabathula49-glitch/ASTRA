#!/usr/bin/env bash
# Build 9:16 Shorts/Reels (1080x1920) from the 16:9 clips: hook text on top,
# clip in the middle, call-to-action at the bottom. Silent: add your voice in the editor.
set -euo pipefail
cd "$(dirname "$0")"
FONT=/usr/share/fonts/opentype/inter/Inter-Bold.otf
FONT2=/usr/share/fonts/opentype/inter/Inter-Medium.otf
mkdir -p shorts
TMP=$(mktemp -d)

# file | hook line 1 (white) | hook line 2 (orange) | name
SHORTS=(
  "out/C02_ai_ml_dl_circles.mp4|AI vs ML vs DL|in 15 seconds|01_ai_ml_dl_15s"
  "out_next/CodeVsData.mp4|Programming vs|Machine Learning|02_code_vs_ml"
  "out_next/TeachTheRobot.mp4|How does a machine|actually learn?|03_teach_the_robot"
  "out_next/BigFact.mp4|ChatGPT learned|175 BILLION numbers|04_175_billion"
  "out/C23_overfitting_plots.mp4|Overfitting =|the byheart student|05_overfitting"
  "out/C44_logistic_sigmoid.mp4|Exam trap!|Logistic Regression|06_logistic_trap"
)

for row in "${SHORTS[@]}"; do
  IFS='|' read -r src l1 l2 name <<< "$row"
  printf '%s' "$l1" > "$TMP/l1.txt"; printf '%s' "$l2" > "$TMP/l2.txt"
  printf '%s' "Full video on AI with Mani" > "$TMP/cta.txt"
  printf '%s' "AI vs ML vs DL  |  Telugu" > "$TMP/tag.txt"
  ffmpeg -v error -y -i "$src" -filter_complex "
    color=c=0x0B0F1A:s=1080x1920:r=30[bg];
    [0:v]scale=1080:-2,setsar=1[clip];
    [bg][clip]overlay=0:(H-h)/2:shortest=1,
    drawbox=x=440:y=330:w=200:h=8:color=0xF59E0B:t=fill,
    drawtext=fontfile=$FONT:textfile=$TMP/l1.txt:fontsize=78:fontcolor=white:x=(w-tw)/2:y=380,
    drawtext=fontfile=$FONT:textfile=$TMP/l2.txt:fontsize=78:fontcolor=0xF59E0B:x=(w-tw)/2:y=480,
    drawtext=fontfile=$FONT2:textfile=$TMP/tag.txt:fontsize=38:fontcolor=0x94A3B8:x=(w-tw)/2:y=1460,
    drawbox=x=190:y=1560:w=700:h=110:color=0xFF2D2D:t=fill,
    drawtext=fontfile=$FONT:textfile=$TMP/cta.txt:fontsize=44:fontcolor=white:x=(w-tw)/2:y=1592
  " -c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium -an "shorts/$name.mp4"
  echo "OK $name"
done
rm -rf "$TMP"
