"""Write SHOT_LIST.md from clips.py (clip order, durations, voiceover lines)."""
import json
import subprocess
from pathlib import Path

import clips

here = Path(__file__).parent
out_dir = here / "out"
lines = ["# AI vs ML vs DL: shot list (80 clips, Chapters 2-7)", "",
         "Every clip is 1080p30 MP4 in `out/`. The voiceover lines are suggestions: say them in your own",
         "Telugu + English style. Trim or slow down clips in your editor to match your voice.", ""]
total = 0.0
chapter = None
for i, (ch, slug, fn, kw, vo) in enumerate(clips.CLIPS, start=1):
    name = f"C{i:02d}_{slug}"
    if ch != chapter:
        chapter = ch
        lines += ["", f"## Chapter {ch}: {clips.CH_NAMES[ch]}", "",
                  "| # | File | Length | Suggested voiceover |", "|---|---|---|---|"]
    f = out_dir / f"{name}.mp4"
    dur = ""
    if f.exists():
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(f)],
                           capture_output=True, text=True)
        d = float(json.loads(r.stdout)["format"]["duration"])
        total += d
        dur = f"{d:.0f}s"
    lines.append(f"| {i} | `{name}.mp4` | {dur} | {vo} |")
lines += ["", f"**Total animation time: {total / 60:.1f} minutes**", ""]
(here / "SHOT_LIST.md").write_text("\n".join(lines))
print(f"wrote SHOT_LIST.md, total {total / 60:.1f} min")
