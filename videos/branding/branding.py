"""
AI with Mani - channel branding pack (original designs, channel colours).

Scenes
  BrandIntro           5s full-frame channel intro
  BrandTransition      1.2s colour-bar wipe (render with -t for transparency)
  Sub_<video>          7s subscribe reminder lower-third with a per-video message

Render (see render_branding.sh):
  manim -r 1920,1080 --frame_rate 30 branding.py BrandIntro
  manim -t -r 1920,1080 --frame_rate 30 --format mov branding.py Sub_ai_ml_dl     # transparent
  GREEN=1 manim -r 1920,1080 --frame_rate 30 branding.py Sub_ai_ml_dl           # green screen
"""
import os

import numpy as np
from manim import *

BG = "#0B0F1A"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
TXT = "#F1F5F9"
MUTED = "#94A3B8"
RED = "#FF2D2D"
FONT = "Inter"

GREEN = os.environ.get("GREEN") == "1"
config.background_color = "#00FF00" if GREEN else BG


def T(s, size=32, color=TXT, weight=BOLD):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def avatar(r=0.62):
    ring = VGroup(*[Arc(radius=r, start_angle=a, angle=TAU / 3, stroke_width=7, color=c)
                    for a, c in zip((PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3), (AI_C, ML_C, DL_C))])
    disc = Circle(radius=r - 0.08, stroke_width=0, fill_color="#111827", fill_opacity=1)
    mono = T("AI", int(r * 52), TXT).move_to(disc)
    return VGroup(disc, ring, mono)


def bell(h=0.42, color=TXT):
    body = VMobject(stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=1)
    w = h * 0.9
    pts = [[-w / 2, -h / 2, 0], [-w * 0.38, -h * 0.25, 0], [-w * 0.36, h * 0.15, 0], [-w * 0.2, h * 0.42, 0],
           [0, h * 0.5, 0], [w * 0.2, h * 0.42, 0], [w * 0.36, h * 0.15, 0], [w * 0.38, -h * 0.25, 0],
           [w / 2, -h / 2, 0]]
    body.set_points_smoothly(pts)
    body.add_line_to(np.array(pts[0]))
    clap = Dot([0, -h * 0.62, 0], radius=h * 0.12, color=color)
    knob = Dot([0, h * 0.58, 0], radius=h * 0.07, color=color)
    return VGroup(body, clap, knob)


def cursor(size=0.5):
    pts = np.array([[0, 0], [0, -1], [0.27, -0.75], [0.45, -1.1], [0.58, -1.04], [0.4, -0.7], [0.75, -0.7]]) * size
    arrow = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=BLACK, stroke_width=3,
                    fill_color=WHITE, fill_opacity=1)
    return arrow


# ---------------------------------------------------------------- intro
class BrandIntro(Scene):
    def construct(self):
        rng = np.random.default_rng(4)
        cols = [AI_C, ML_C, DL_C]
        dots = VGroup(*[Dot(radius=rng.uniform(0.03, 0.07), color=cols[i % 3]).move_to(
            [rng.uniform(-7, 7), rng.uniform(-4, 4), 0]) for i in range(90)])
        self.play(FadeIn(dots, lag_ratio=0.01), run_time=0.6)
        av = avatar(1.0).shift(UP * 0.6)
        targets = [av.get_center() + 1.0 * np.array([np.cos(a), np.sin(a), 0])
                   for a in np.linspace(0, TAU, 90, endpoint=False)]
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=1.0, rate_func=rush_into)
        self.play(FadeOut(dots, scale=1.4), FadeIn(av, scale=0.6), Flash(av, color=DL_C, line_length=0.5,
                                                                         num_lines=16, flash_radius=1.25), run_time=0.6)
        name = T("AI with Mani", 64, TXT).next_to(av, DOWN, buff=0.45)
        tag = VGroup(T("Learn AI.", 28, AI_C), T("Explore Quantum.", 28, ML_C), T("Build the Future.", 28, DL_C))
        tag.arrange(RIGHT, buff=0.35).next_to(name, DOWN, buff=0.35)
        self.play(Write(name), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tag], lag_ratio=0.3), run_time=0.9)
        self.wait(0.9)
        self.play(FadeOut(VGroup(av, name, tag), scale=1.1), run_time=0.4)


# ---------------------------------------------------------------- transition
class BrandTransition(Scene):
    def construct(self):
        bars = VGroup(*[Rectangle(width=16, height=9, stroke_width=0, fill_color=c, fill_opacity=1)
                        for c in (AI_C, ML_C, DL_C)])
        for i, b in enumerate(bars):
            b.move_to(LEFT * 16).rotate(-0.25)
        logo = avatar(0.9)
        self.play(LaggedStart(*[b.animate.move_to(ORIGIN) for b in bars], lag_ratio=0.18),
                  run_time=0.5, rate_func=rush_into)
        self.add(logo)
        self.play(FadeIn(logo, scale=0.7), run_time=0.15)
        self.remove(logo)
        self.play(LaggedStart(*[b.animate.move_to(RIGHT * 16) for b in reversed(bars)], lag_ratio=0.18),
                  run_time=0.5, rate_func=rush_from)


# ---------------------------------------------------------------- subscribe reminder
def subscribe(scene, line1, line2):
    av = avatar(0.55)
    name = T("AI with Mani", 30, TXT)
    msg1 = T(line1, 24, DL_C)
    msg2 = T(line2, 22, MUTED, NORMAL)
    for m in (msg1, msg2):
        if m.width > 6.4:
            m.scale_to_fit_width(6.4)
    text = VGroup(name, msg1, msg2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    btn = RoundedRectangle(width=2.7, height=0.75, corner_radius=0.37, stroke_width=0,
                           fill_color=RED, fill_opacity=1)
    btn_t = T("SUBSCRIBE", 24, WHITE).move_to(btn)
    button = VGroup(btn, btn_t)
    bl = bell(0.42)
    row = VGroup(av, text, button, bl).arrange(RIGHT, buff=0.4)
    panel = RoundedRectangle(width=row.width + 0.8, height=max(row.height, 1.3) + 0.5, corner_radius=0.3,
                             stroke_color=AI_C, stroke_width=2, fill_color="#0F172A", fill_opacity=1 if GREEN else 0.92)
    panel.move_to(row)
    glow = panel.copy().set_fill(opacity=0).set_stroke(DL_C, width=6, opacity=0.35).scale(1.02)
    card = VGroup(glow, panel, row)
    card.to_corner(DL, buff=0.6)
    home = card.get_center()
    card.shift(DOWN * 3)

    scene.play(card.animate.move_to(home), run_time=0.6, rate_func=smooth)
    scene.play(Write(msg1), run_time=0.6)
    scene.play(Indicate(button, scale_factor=1.08, color=WHITE), run_time=0.6)

    cur = cursor(0.55).move_to(btn.get_center() + RIGHT * 2.5 + DOWN * 1.5)
    scene.play(FadeIn(cur), run_time=0.2)
    scene.play(cur.animate.move_to(btn.get_center() + RIGHT * 0.25 + DOWN * 0.2), run_time=0.6)
    scene.play(cur.animate.scale(0.85), btn.animate.scale(0.94), run_time=0.1)
    scene.play(cur.animate.scale(1 / 0.85), btn.animate.scale(1 / 0.94).set_fill("#3F3F46"),
               Transform(btn_t, T("SUBSCRIBED ✓", 21, WHITE).move_to(btn)), run_time=0.15)
    ring = Circle(radius=0.15, color=WHITE, stroke_width=3).move_to(cur.get_corner(UL))
    scene.play(ring.animate.scale(4).set_stroke(opacity=0), run_time=0.35)
    scene.play(cur.animate.move_to(bl.get_center() + RIGHT * 0.15 + DOWN * 0.25), run_time=0.45)
    scene.play(cur.animate.scale(0.85), run_time=0.08)
    scene.play(cur.animate.scale(1 / 0.85), bl.animate.set_color(DL_C), run_time=0.08)
    scene.play(Wiggle(bl, scale_value=1.25, rotation_angle=0.25 * PI, n_wiggles=4), run_time=0.7)
    scene.play(FadeOut(cur), Flash(bl, color=DL_C, flash_radius=0.45, line_length=0.18), run_time=0.4)
    scene.wait(1.3)
    scene.play(card.animate.shift(DOWN * 3), run_time=0.5, rate_func=rush_into)


# one special message per video: (slug, line 1, line 2)
SUB_NOTES = [
    ("ai_ml_dl", "Exams ki prepare avtunnara? Ee video save cheyyandi!", "Subscribe for AI & ML in Telugu"),
    ("quantum", "Quantum series continue avtundi. Next episode miss avvakandi!", "Subscribe + bell for every new episode"),
    ("ai_agents", "AI Agents future! Next level content vasthundi", "Subscribe for the latest AI in Telugu"),
    ("neural_networks", "Neural Networks next video lo, deep ga!", "Subscribe so you don't miss it"),
    ("general", "Video nachithe like cheyyandi!", "Subscribe for AI, ML & Quantum in Telugu"),
]

for _slug, _l1, _l2 in SUB_NOTES:
    def _construct(self, l1=_l1, l2=_l2):
        subscribe(self, l1, l2)
    globals()[f"Sub_{_slug}"] = type(f"Sub_{_slug}", (Scene,), {"construct": _construct})
