# AI vs ML vs DL: animated clips

80 explainer animations (Chapters 2-7) for the AI with Mani video, built with [Manim](https://www.manim.community/).

| File | What it is |
|---|---|
| `clips.py` | All 80 scenes. Edit text, colours or order in the `CLIPS` list at the bottom. |
| `render_all.sh` | Renders every clip in parallel into `out/` (1080p30). `./render_all.sh preview` for fast 480p. |
| `make_shotlist.py` | Writes `SHOT_LIST.md` (clip order, length, suggested voiceover). |
| `SHOT_LIST.md` | Which clip goes where, with a voiceover line for each. |

## Setup (Windows / Mac / Linux)
```
pip install manim        # needs FFmpeg; on Linux also libpango1.0-dev, libcairo2-dev
./render_all.sh          # or: manim -r 1920,1080 --frame_rate 30 clips.py C02_ai_ml_dl_circles
```

Colour code used everywhere: AI = blue, ML = green, DL = orange.
