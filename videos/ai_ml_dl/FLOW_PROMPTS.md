# Google Flow (Veo) Prompt Pack: 2D Cinematic Character Animation

Style goal: hand-drawn 2D animated film look (expressive characters, painterly backgrounds, soft window light), like premium animated ads. **Original characters and scenes for our video. Do not ask for any brand, ad or studio by name.**

---

## How to keep every clip consistent
1. **Always paste the STYLE block and the CHARACTER block word for word.** Same words = same look.
2. **Make Mani once, reuse him.** Generate scene M1 first. Pick the best frame and save it as an image. In Flow, use it as a reference / starting frame ("Ingredients" or "Frames to video") for every other Mani scene.
3. **No text in the AI video.** AI video garbles text. We add all titles and labels in editing.
4. **One action per clip** (8 seconds). Simple actions look natural; complex ones break.
5. Generate 2 variations, keep the best. If credits are short, do the ⭐ scenes first.

---

## STYLE block (paste into every prompt)
```
2D hand-drawn cel animation in the style of a premium animated short film. Clean expressive ink linework, characters with subtle shading, softly painted textured backgrounds with visible brush strokes, muted teal and warm amber colour palette, gentle cinematic lighting, shallow depth of field, slight film grain, smooth natural character acting with small secondary motions (breathing, blinking, hair movement). No text, no logos, no subtitles.
```

## CHARACTER blocks
**MANI (our presenter):**
```
Mani, a friendly young South Indian man in his mid-20s, warm brown skin, short wavy black hair, light stubble, thin rectangular black glasses, wearing a mustard-yellow knit sweater over a light blue collared shirt and dark jeans.
```
*(Change glasses, hair or clothes to match the real you, then never change it again.)*

**PRIYA (the student):**
```
Priya, a 20-year-old Indian college student, long black hair in a loose braid, round face, small gold stud earrings, wearing a teal kurta top with jeans and a canvas backpack.
```

---

## Scene prompts (in video order)
⭐ = most important. Approx. 13 clips. You have 17 credits, so there's room for retries.

### ⭐ H1: Hook: confused student (0:00)
```
[STYLE] [PRIYA] Night, a small hostel room lit by a warm desk lamp. Priya sits at a cluttered desk surrounded by open textbooks and sticky notes, a laptop glowing in front of her. She leans back, rubs her temples, sighs, then slowly turns her head toward the camera with a puzzled expression. Slow push-in camera move. Rain softly visible on the window behind her.
```

### ⭐ H2: Hook: phone face unlock
```
[STYLE] [MANI] Morning in a cosy apartment kitchen with sunlight through blinds. Mani lifts his smartphone to his face; a soft blue scanning glow passes over his face and the screen lights up. He gives a small satisfied smile. Medium close-up, gentle handheld feel.
```

### M1: Intro: Mani says hello (0:45) (make this first, use it as the reference)
```
[STYLE] [MANI] A calm study room with bookshelves, a plant and a window with soft afternoon light. Mani sits at a round wooden table with a laptop, looks up from the screen toward the camera, smiles warmly and gives a small friendly wave. Static medium shot, eye level.
```

### ⭐ C1a: What is AI: navigation in traffic
```
[STYLE] [MANI] Golden-hour busy Indian city street with auto-rickshaws and scooters. Mani rides a scooter and stops at a junction, glances at a phone mounted on the handlebar showing a glowing map route, nods, and turns confidently into a side street. Side tracking shot, warm dusty light.
```

### C1b: What is AI: voice assistant
```
[STYLE] A sunlit Indian home kitchen with steel vessels. An elderly grandmother in a cotton saree speaks to a small round smart speaker on the counter; the speaker's light ring glows softly as it answers and she laughs with surprise. Medium shot, warm light.
```

### C1c: History: man vs machine chess (1997)
```
[STYLE] A dim 1990s hall with spotlights. A tense chess player in a suit stares at a chessboard; opposite him a computer operator moves a piece on behalf of a large beige computer terminal. The player rests his chin on his hands, deep in thought. Slow dolly-in, dramatic overhead lighting.
```

### ⭐ C2: ML = learning from examples (rules vs learning)
```
[STYLE] A cosy living room in evening lamplight. A father sits on the floor with his 4-year-old daughter, flipping through a big picture book of cats and dogs, pointing at each picture. She points at a new picture, says something excitedly, and he gives her a proud high-five. Warm, gentle, medium shot.
```

### C3a: Train vs test: exam hall
```
[STYLE] [PRIYA] A bright college exam hall with rows of desks and morning light through tall windows. Priya reads the question paper, a smile slowly appears as she recognises the question, and she starts writing confidently. Slow push-in from the side.
```

### ⭐ C3b: Gradient descent: walking downhill in fog
```
[STYLE] A misty green hillside at dawn, thick soft fog. A lone hiker with a backpack carefully feels the slope with each step and walks downhill step by step, slowly emerging from the fog into a calm valley with a small lake. Wide shot, camera slowly following.
```

### ⭐ C4: Reinforcement learning: learning to ride a bicycle
```
[STYLE] A quiet colony lane in late afternoon with trees and parked scooters. A young boy wobbles on a bicycle and falls gently onto the grass, gets up, tries again, and this time rides smoothly while his mother claps and cheers. Wide tracking shot, warm sunlight.
```

### C6a: Deep learning: doctor and AI scan
```
[STYLE] A calm modern hospital reading room with blue monitor light. A woman doctor in a white coat studies a lung X-ray on a large screen; a soft glowing highlight appears around one area of the scan and she leans closer, then nods and makes a note. Over-the-shoulder shot.
```

### C6b: "Neurons" transition (abstract)
```
[STYLE] Extreme close-up transitioning from a student's eye into an abstract space of glowing teal and amber neurons connected by threads of light, with pulses of light travelling between them, camera flying gently forward through the network. Dreamy, cinematic.
```

### ⭐ O1: Outro: goodbye
```
[STYLE] [MANI] The same calm study room in early evening, a warm lamp on. Mani closes his laptop, turns to the camera, smiles and gives a friendly wave goodbye, then leans back relaxed. Static medium shot, cosy lighting.
```

---

## Where they go (with our animations)
| Clip | Script moment | Pair with |
|---|---|---|
| H1, H2 | Hook | HookKinetic text on top |
| M1 | Intro | BrandIntro before it |
| C1a–C1c | Chapter 1 | Your existing Flow clips |
| C2 | "Normal programming vs ML" | CodeVsData right after |
| C3a | Student analogy | C13 table |
| C3b | Gradient descent | C20 graph right after (story, then the maths) |
| C4 | Reinforcement learning | C37 robot grid |
| C6a, C6b | Deep learning | HudNeural / C56 |
| O1 | Outro | Subscribe pop-up on top |

**Edit pattern that works best:** cinematic human clip (3–5s) → our diagram explaining it → back to the human. Story first, then the concept.
