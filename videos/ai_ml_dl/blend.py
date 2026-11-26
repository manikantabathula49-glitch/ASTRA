"""
Pieces that blend the hand-drawn Flow clips with our diagrams.

  BrushMask    1s white brush strokes on black: luma mask for a painted wipe (use with ffmpeg maskedmerge)
  PopBubbles   transparent overlay: AI / ML / DL "thought" cards pop out next to a character
               render with: manim -t --format mov -r 1920,1080 --frame_rate 30 blend.py PopBubbles
"""
import numpy as np
from manim import *

AI_C = "#2563EB"
ML_C = "#16A34A"
DL_C = "#D97706"
INK = "#2B2118"
PAPER = "#FFF7E6"
SERIF = "DejaVu Serif"


class BrushMask(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        rng = np.random.default_rng(4)
        strokes = []
        ys = np.linspace(-4.6, 4.6, 7)
        for i, y in enumerate(ys):
            tilt = rng.uniform(-0.25, 0.25)
            a = np.array([-9.5, y + tilt * 3, 0])
            b = np.array([9.5, y - tilt * 3, 0])
            s = Line(a, b, stroke_width=rng.uniform(150, 190), color=WHITE).set_cap_style(CapStyleType.ROUND)
            strokes.append(s)
        self.play(LaggedStart(*[Create(s, rate_func=rate_functions.ease_in_out_cubic) for s in strokes],
                              lag_ratio=0.09), run_time=0.95)
        self.add(Rectangle(width=16, height=10, fill_color=WHITE, fill_opacity=1, stroke_width=0))
        self.wait(0.1)


def card(word, sub, color):
    t = Text(word, font=SERIF, font_size=46, color=color, weight=BOLD)
    s = Text(sub, font=SERIF, font_size=20, color=INK, slant=ITALIC)
    g = VGroup(t, s).arrange(DOWN, buff=0.12)
    bg = RoundedRectangle(width=g.width + 0.7, height=g.height + 0.5, corner_radius=0.25,
                          fill_color=PAPER, fill_opacity=0.96, stroke_color=INK, stroke_width=4)
    shadow = bg.copy().set_fill(INK, 0.25).set_stroke(width=0).shift(DR * 0.08)
    return VGroup(shadow, bg, g).move_to(ORIGIN)


class PopBubbles(Scene):
    def construct(self):
        # head of the character sits around (-1.5, 1.6) in a 1920x1080 frame of M1
        head = np.array([-0.45, 2.2, 0])
        cards = [card("AI", "machines acting smart", AI_C),
                 card("ML", "learns from data", ML_C),
                 card("DL", "deep neural networks", DL_C)]
        spots = [np.array([5.1, 2.75, 0]), np.array([5.1, 0.95, 0]), np.array([5.1, -0.85, 0])]
        trail = VGroup(*[Circle(r, fill_color=PAPER, fill_opacity=0.95, stroke_color=INK, stroke_width=3)
                         .move_to(head + RIGHT * (0.9 + 0.7 * i) + UP * (0.25 + 0.12 * i)) for i, r in enumerate((0.08, 0.12, 0.16))])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in trail], lag_ratio=0.3), run_time=0.45)
        for c, p in zip(cards, spots):
            c.move_to(p).scale(0.01)
            self.add(c)
            self.play(c.animate.scale(100), run_time=0.45, rate_func=rate_functions.ease_out_back)
            self.wait(0.25)
        # small "inside" links between the cards: DL inside ML inside AI
        links = VGroup(*[Text("⊂", font=SERIF, font_size=40, color=INK).move_to((spots[i] + spots[i + 1]) / 2)
                         for i in range(2)])
        self.play(FadeIn(links, scale=0.5), run_time=0.4)
        self.wait(1.6)
        self.play(*[FadeOut(m, scale=0.8) for m in (*cards, trail, links)], run_time=0.4)
