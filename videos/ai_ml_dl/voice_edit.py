"""Remove ranges from a recording, joining the pieces with 15 ms crossfades.
Usage: python voice_edit.py in.mp3 out.wav  a-b  c-d ...   (ranges to REMOVE, seconds)
Prints a JSON time map so later edits can shift their cue times."""
import json, subprocess, sys
src, out, *ranges = sys.argv[1:]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
cuts = sorted(tuple(map(float, r.split("-"))) for r in ranges)
keep, t = [], 0.0
for a, b in cuts:
    if a > t: keep.append((t, a))
    t = max(t, b)
if t < total: keep.append((t, total))
fc, labels = [], []
for i, (a, b) in enumerate(keep):
    fc.append(f"[0:a]atrim={a}:{b},asetpts=N/SR/TB[p{i}]"); labels.append(f"p{i}")
cur = labels[0]
for i in range(1, len(labels)):
    nxt = f"x{i}"; fc.append(f"[{cur}][{labels[i]}]acrossfade=d=0.015:c1=tri:c2=tri[{nxt}]"); cur = nxt
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(fc), "-map", f"[{cur}]",
                "-ar", "48000", "-ac", "2", out], check=True)
print(json.dumps({"keep": keep, "removed": cuts}))
