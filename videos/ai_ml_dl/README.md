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

## Next-level scenes (`next_level.py`)
Original scenes in styles found on Pinterest: kinetic typography, holographic HUD, object + big counter.
| Scene | Use |
|---|---|
| `HookKinetic` | First 12s of the video: "AI. ML. DL. Confused?" |
| `HudNeural` | Deep Learning chapter: futuristic neural-network dashboard |
| `BigFact` | Fact card: GPT-3's 175 billion parameters counting up |

## IT-style informational scenes (`it_scenes.py`)
Original scenes in styles referenced from Pinterest (isometric servers, code typing, neon dashboards, glowing chips).
| Scene | Teaches | Place near |
|---|---|---|
| `IsoPipeline` | How an ML model is built: Data → Clean → Train → Model → Use | C16 |
| `CodeVsData` | Hand-written rules vs rules learned from data | C07 |
| `NeonData` | How much data rule-based AI, ML and DL need | C64 |
| `GpuChip` | Why GPUs train neural networks faster | C66 |

## People scenes (`people.py`)
Original flat-style characters interacting with tech.
| Scene | What happens | Place near |
|---|---|---|
| `PresenterBoard` | Presenter waves, points at a board drawing AI ⊃ ML ⊃ DL; students go "?" → "!" | C02 / intro |
| `TeachTheRobot` | Person shows labelled Cat/Dog cards to a robot, it learns, then guesses a new card | C30–C31 (supervised) |
| `StudentAndAI` | Student types "What is Deep Learning?", AI answers, "?" turns into a lightbulb | Hook / intro / C57 |
