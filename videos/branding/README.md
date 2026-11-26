# AI with Mani: branding pack

Original designs in the channel colours (AI blue, ML green, DL orange).

| File | Use |
|---|---|
| `BrandIntro.mp4` | 5s channel intro: particles form the logo, then name and tagline |
| `BrandTransition_*` | 1.2s colour-bar wipe to place between scenes |
| `Sub_<video>_*` | 7s subscribe pop-up: cursor clicks Subscribe, bell rings, special message |

Each overlay comes in 3 versions:
- `_alpha.mov`: transparent, for Premiere, DaVinci Resolve, Final Cut, CapCut desktop
- `_green.mp4`: green screen, for CapCut mobile / VN (use **Chroma Key**)
- `.mp4`: dark background preview

Special messages (edit `SUB_NOTES` in `branding.py`, then `./render_branding.sh`):
| Video | Message |
|---|---|
| `ai_ml_dl` | Exams ki prepare avtunnara? Ee video save cheyyandi! |
| `quantum` | Quantum series continue avtundi. Next episode miss avvakandi! |
| `ai_agents` | AI Agents future! Next level content vasthundi |
| `neural_networks` | Neural Networks next video lo, deep ga! |
| `general` | Video nachithe like cheyyandi! |

Tip: place the subscribe pop-up around 30-60 seconds in, right after a "wow" moment, not at the very start.

## Transitions (`transitions.py`)
Each ~1s, in `_alpha.mov` (transparent), `_green.mp4` and `.mp4` versions. **Cut from clip A to clip B at the midpoint**, when the screen is fully covered.
| File | Look | Best for |
|---|---|---|
| `TrIris` | Blue/green/orange rings expand, then open like a camera iris | Chapter changes |
| `TrSlidePanels` | 5 coloured panels drop in and lift away | Section changes |
| `TrBlobs` | Soft colour blobs swell and slide off | Calm topic changes |
| `TrSpeedLines` | Light streaks + flash | Fast, exciting moments (hook, reveals) |

## Engagement bar with sounds (`engage.py`, `render_engage.sh`)
Your photo + **Like, Share, Comment, Subscribe, Bell**, clicked one by one with sound effects (click, pop, bell ding, whoosh), all generated, no third-party audio.
| File | Use |
|---|---|
| `Engage_<video>_alpha.mov` | Transparent + sound (Premiere, DaVinci, CapCut desktop) |
| `Engage_<video>_green.mp4` | Green screen + sound (CapCut mobile: Chroma Key) |
| `Engage_<video>.mp4` | Preview with sound |
Versions: `ai_ml_dl`, `quantum`, `general`. Add more in `NOTES` inside `engage.py`, then run `./render_engage.sh`.
