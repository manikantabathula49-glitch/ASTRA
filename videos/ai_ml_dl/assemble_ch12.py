"""
Assemble Chapters 1-2 from the voice recordings + clips (edit decision list below).
Each shot runs from its start (seconds into that recording) until the next shot; short clips hold their last frame.
Usage: python assemble_ch12.py  -> out_next/Ch1_Ch2_cut.mp4
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
TMP = os.environ.get("TMPDIR_CUT", "/tmp/cut_work")
os.makedirs(TMP, exist_ok=True)
BR = "../branding/out"
VF = "fps=30,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
GAP = 0.35  # breathing room between recordings


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def shot(src, offset, length, out):
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{offset}", "-i", src, "-an", "-vf",
         f"{VF},tpad=stop_mode=clone:stop_duration={length + 1}", "-t", f"{length}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out])


# (voice file or None, total length if no voice, [(start, clip, clip_offset), ...], extras)
SECTIONS = [
    (None, 5.2, [(0, f"{BR}/BrandIntro.mp4", 0)], {}),
    ("voice/rec07.mp3", None, [(0, "flow/M1_mani_waving.mp4", 0), (11.0, "out/C03_define_ai.mp4", 0)], {}),
    ("voice/rec08.mp3", None, [(0, "out/C09_ai_without_ml.mp4", 0), (13.0, "out_next/StudentAndAI.mp4", 0),
                               (22.0, "out_next/AITimeline_voiced.mp4", 19.8), (30.8, "out_next/HudNeural.mp4", 0),
                               (36.1, "out/C02_ai_ml_dl_circles.mp4", 0), (43.0, "out/C08_rule_ai_vs_ml.mp4", 0),
                               (54.6, "out_next/TeachTheRobot.mp4", 0), (68.6, "out_next/PresenterBoard.mp4", 0)], {}),
    (None, 5.8, [(0, "out/C01_chapter2_card.mp4", 0)], {}),
    ("voice/rec09.mp3", None, [(0, "out/C02_ai_ml_dl_circles.mp4", 0), (16.2, "out_next/PresenterBoard.mp4", 0),
                               (29.5, "out/C03_define_ai.mp4", 0)], {}),
    ("voice/rec10.mp3", None, [(0, "out/C04_define_ml.mp4", 0), (7.0, "out/C26_spam_example.mp4", 0),
                               (21.0, "out_next/AITimeline_voiced.mp4", 9.9), (28.0, "out/C04_define_ml.mp4", 4.0)], {}),
    ("TIMELINE", None, [(0, "out_next/AITimeline_voiced.mp4", 0)], {}),
    ("voice/rec12.mp3", None, [(0, "out_next/HookKinetic.mp4", 0), (6.3, "out/C07_rules_vs_learning.mp4", 0)], {}),
    ("voice/rec13.mp3", None, [(0, "out_next/CodeVsData.mp4", 0), (15.0, "out/C08_rule_ai_vs_ml.mp4", 0),
                               (24.0, "out_next/TeachTheRobot.mp4", 2.0), (30.8, "out/C09_ai_without_ml.mp4", 0),
                               (44.2, "out_next/AITimeline_voiced.mp4", 19.8), (50.8, "out/C10_sort_examples.mp4", 0),
                               (68.8, "out/C11_quiz_chatgpt.mp4", 0), (87.3, "out/C02_ai_ml_dl_circles.mp4", 6.0)],
     {"engage_at": 90.3}),
]

parts = []
for si, (voice, fixed, shots, extra) in enumerate(SECTIONS):
    if voice == "TIMELINE":
        parts.append("out_next/AITimeline_voiced.mp4")
        continue
    total = dur(voice) + GAP if voice else fixed
    files = []
    for k, (start, clip, off) in enumerate(shots):
        end = shots[k + 1][0] if k + 1 < len(shots) else total
        f = f"{TMP}/s{si:02d}_{k:02d}.mp4"
        shot(clip, off, end - start, f)
        files.append(f)
    lst = f"{TMP}/s{si:02d}.txt"
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    vid = f"{TMP}/s{si:02d}_v.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    out = f"{TMP}/s{si:02d}.mp4"
    if "engage_at" in extra:
        t = extra["engage_at"]
        eng = f"{BR}/Engage_ai_ml_dl_alpha.mov"
        run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", voice, "-itsoffset", f"{t}", "-i", eng, "-filter_complex",
             f"[0:v][2:v]overlay=0:0:eof_action=pass,format=yuv420p[v];[2:a]volume=0.8[e];[1:a][e]amix=inputs=2:normalize=0,apad[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{total}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out])
    elif voice:
        run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", voice, "-filter_complex", "[1:a]apad[a]", "-map", "0:v",
             "-map", "[a]", "-t", f"{total}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out])
    else:
        run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v",
             "-map", "1:a", "-t", f"{total}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])
    parts.append(out)
    print("section", si, f"{total:.1f}s", flush=True)

# join all sections (re-encode so timestamps are clean)
inputs, fc = [], ""
for i, p in enumerate(parts):
    inputs += ["-i", p]
    fc += f"[{i}:v]{VF}[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];"
fc += "".join(f"[v{i}][a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
os.makedirs("out_next", exist_ok=True)
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
     "out_next/Ch1_Ch2_cut.mp4"])
print("final", f"{dur('out_next/Ch1_Ch2_cut.mp4'):.1f}s")
