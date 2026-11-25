"""Transcribe voice recordings with Whisper: native-language text + English translation, with timestamps.
Usage: python transcribe.py <model_dir> <audio files...>   -> writes voice/<name>.json"""
import json, sys, os
import whisper

model_dir, files = sys.argv[1], sys.argv[2:]
m = whisper.load_model("medium", download_root=model_dir)
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    out = {}
    for task in ("transcribe", "translate"):
        r = m.transcribe(f, task=task, language="te", fp16=False, condition_on_previous_text=False)
        out[task] = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()} for s in r["segments"]]
    json.dump(out, open(os.path.join(os.path.dirname(f), name + ".json"), "w"), ensure_ascii=False, indent=1)
    print("done", name, flush=True)
