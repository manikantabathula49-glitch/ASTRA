"""
Smooth transitions in the channel colours. Render with -t for transparent .mov:
  manim -t -r 1920,1080 --frame_rate 30 --format mov transitions.py TrIris
Cut from clip A to clip B at the midpoint of the transition (when the screen is covered).
"""
import os

import numpy as np
from manim import *

AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
BG = "#0B0F1A"
GREEN = os.environ.get("GREEN") == "1"
config.background_color = "#00FF00" if GREEN else BG
EASE_IN = rate_functions.ease_in_cubic
EASE_OUT = rate_functions.ease_out_cubic


def full(color):
    return Rectangle(width=16, height=9.5, stroke_width=0, fill_color=color, fill_opacity=1)


class TrIris(Scene):
    """Three rings expand from the centre, then open out like a camera iris."""
    def construct(self):
        discs = [Circle(0.01, stroke_width=0, fill_color=c, fill_opacity=1) for c in (AI_C, ML_C, DL_C)]
        for i, d in enumerate(discs):
            self.add(d)
        self.play(LaggedStart(*[d.animate.scale(900) for d in discs], lag_ratio=0.15), run_time=0.55, rate_func=EASE_IN)
        hole = Circle(0.01, stroke_width=0, fill_color=BG if not GREEN else "#00FF00", fill_opacity=1)
        for d in discs[:-1]:
            self.remove(d)
        top = discs[-1]
        # open: shrink the cover by turning it into a ring that grows outward
        ring = Annulus(inner_radius=0.01, outer_radius=10, stroke_width=0, fill_color=DL_C, fill_opacity=1)
        self.remove(top)
        self.add(ring)
        self.play(ring.animate.become(Annulus(inner_radius=10, outer_radius=10.05, stroke_width=0, fill_color=DL_C, fill_opacity=1)),
                  run_time=0.5, rate_func=EASE_OUT)
        self.remove(ring, hole)


class TrSlidePanels(Scene):
    """Five vertical panels drop in, then lift away."""
    def construct(self):
        cols = [AI_C, ML_C, DL_C, AI_C, ML_C]
        w = 14.4 / 5
        panels = [Rectangle(width=w + 0.02, height=8.2, stroke_width=0, fill_color=c, fill_opacity=1)
                  .move_to([-7.2 + w / 2 + i * w, 8.2, 0]) for i, c in enumerate(cols)]
        self.add(*panels)
        self.play(LaggedStart(*[p.animate.set_y(0) for p in panels], lag_ratio=0.1), run_time=0.55, rate_func=EASE_IN)
        self.play(LaggedStart(*[p.animate.set_y(-8.2) for p in panels], lag_ratio=0.1), run_time=0.55, rate_func=EASE_OUT)


class TrBlobs(Scene):
    """Soft colour blobs swell to cover the screen, then slide off to the right."""
    def construct(self):
        pos = [[-4, 2, 0], [0.5, -2, 0], [4.5, 1.5, 0], [-1.5, 0.5, 0]]
        cols = [AI_C, ML_C, DL_C, AI_C]
        blobs = [Circle(0.01, stroke_width=0, fill_color=c, fill_opacity=1).move_to(p) for c, p in zip(cols, pos)]
        self.add(*blobs)
        self.play(LaggedStart(*[b.animate.scale(700) for b in blobs], lag_ratio=0.12), run_time=0.55, rate_func=EASE_IN)
        self.play(LaggedStart(*[b.animate.shift(RIGHT * 22) for b in blobs], lag_ratio=0.08), run_time=0.55, rate_func=EASE_OUT)


class TrSpeedLines(Scene):
    """Diagonal light streaks race across with a short flash: for a fast topic change."""
    def construct(self):
        rng = np.random.default_rng(2)
        lines = VGroup()
        for i in range(40):
            y = rng.uniform(-6, 6)
            L = rng.uniform(3, 8)
            c = [AI_C, ML_C, DL_C, WHITE][i % 4]
            lines.add(Line([-9, y, 0], [-9 + L, y, 0], stroke_width=rng.uniform(3, 14), color=c).rotate(0.35))
        lines.shift(LEFT * 10)
        self.add(lines)
        flash = full(WHITE).set_opacity(0)
        self.add(flash)
        self.play(lines.animate.shift(RIGHT * 30), flash.animate.set_opacity(0.9),
                  run_time=0.5, rate_func=EASE_IN)
        self.play(flash.animate.set_opacity(0), run_time=0.35, rate_func=EASE_OUT)
