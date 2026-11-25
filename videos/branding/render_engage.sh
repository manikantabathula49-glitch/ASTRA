#!/usr/bin/env bash
# Render the engagement bars with click sounds into out/:
#   Engage_<x>_alpha.mov  (transparent video + sound)   Engage_<x>_green.mp4  Engage_<x>.mp4
# Sounds are synthesised here (no third-party audio), placed at the click times manim records.
set -euo pipefail
cd "$(dirname "$0")"
MANIM="${MANIM:-manim}"; WORK="${WORK:-/tmp/engage_work}"; RES="${RES:-1920,1080}"; FPS="${FPS:-30}"
mkdir -p out sfx "$WORK"
# --- sound effects
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.9*sin(2*PI*2300*t)*exp(-90*t)+0.35*(2*random(0)-1)*exp(-170*t)':s=48000:d=0.09" sfx/click.wav
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.75*sin(2*PI*(520+1400*t)*t)*exp(-13*t)':s=48000:d=0.3" sfx/pop.wav
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.45*sin(2*PI*1568*t)*exp(-3.5*t)+0.22*sin(2*PI*3136*t)*exp(-6*t)+0.15*sin(2*PI*2349*t)*exp(-4.5*t)':s=48000:d=1.3" sfx/ding.wav
ffmpeg -v error -y -f lavfi -i "anoisesrc=d=0.35:c=pink:a=0.25,lowpass=f=1800,afade=t=in:d=0.12,afade=t=out:st=0.15:d=0.2" -ar 48000 sfx/whoosh.wav

SCENES=${ONLY:-"Engage_ai_ml_dl Engage_quantum Engage_general"}
for s in $SCENES; do
  "$MANIM" -t --format mov -r $RES --frame_rate $FPS --media_dir "$WORK/$s-a" engage.py "$s" >/dev/null 2>&1
  GREEN=1 "$MANIM" -r $RES --frame_rate $FPS --media_dir "$WORK/$s-g" engage.py "$s" >/dev/null 2>&1
  "$MANIM" -r $RES --frame_rate $FPS --media_dir "$WORK/$s-d" engage.py "$s" >/dev/null 2>&1
  A=$(find "$WORK/$s-a" -name "$s.mov" -not -path "*partial*" | head -1)
  G=$(find "$WORK/$s-g" -name "$s.mp4" -not -path "*partial*" | head -1)
  D=$(find "$WORK/$s-d" -name "$s.mp4" -not -path "*partial*" | head -1)
  # build the sound track from the recorded click times
  python3 - "$s" > "$WORK/$s.args" <<'EOF'
import json, sys
ev = json.load(open(f"{sys.argv[1]}_events.json"))
ins, chains, labels = [], [], []
for i, e in enumerate(ev["events"]):
    f = {"click": "click", "pop": "pop", "ding": "ding", "whoosh_in": "whoosh", "whoosh_out": "whoosh"}[e["type"]]
    ins.append(f"-i sfx/{f}.wav")
    ms = max(0, int(e["t"] * 1000) - (150 if f == "whoosh" else 0))
    chains.append(f"[{i+1}:a]adelay={ms}|{ms}[a{i}]")
    labels.append(f"[a{i}]")
n = len(labels)
fc = ";".join(chains) + ";" + "".join(labels) + f"amix=inputs={n}:normalize=0,apad=whole_dur={ev['duration']}[aout]"
print(" ".join(ins)); print(fc)
EOF
  INS=$(sed -n 1p "$WORK/$s.args"); FC=$(sed -n 2p "$WORK/$s.args")
  ffmpeg -v error -y -i "$A" $INS -filter_complex "$FC" -map 0:v -map "[aout]" -c:v copy -c:a pcm_s16le -shortest "out/${s}_alpha.mov"
  ffmpeg -v error -y -i "$G" $INS -filter_complex "$FC" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "out/${s}_green.mp4"
  ffmpeg -v error -y -i "$D" $INS -filter_complex "$FC" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "out/${s}.mp4"
  echo "OK $s"
done
