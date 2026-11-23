"""
YouTube thumbnails (1280x720). Render a still:
  manim -s -r 1280,720 thumbs.py ThumbA
"""
import numpy as np
from manim import *

from people import Person, SKIN, HAIR, bubble

BG = "#070B14"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
TXT = "#FFFFFF"
SANS = "Inter"
config.background_color = BG


def T(s, size, color=TXT, weight=HEAVY):
    return Text(s, font=SANS, font_size=size, color=color, weight=weight)


def neon_circle(r, color, pos):
    g = VGroup(*[Circle(r, color=color, stroke_width=6 + 7 * i, stroke_opacity=0.08).move_to(pos) for i in range(4, 0, -1)])
    g.add(Circle(r, color=color, stroke_width=7, fill_color=color, fill_opacity=0.12).move_to(pos))
    return g


def confused_mascot():
    m = Person(SKIN[1], HAIR[0], shirt=AI_C)
    # hand scratching head
    m.arm_r.rotate(3.22, about_point=m.shoulder("r"))
    # worried mouth
    hc = m.head[0].get_center()
    m.head.remove(m.mouth)
    m.head.add(Arc(radius=0.09, start_angle=0.4, angle=PI - 0.8, color="#111827", stroke_width=3).move_to(hc + DOWN * 0.16))
    return m


def circles(center, s=1.0):
    ai = neon_circle(1.9 * s, AI_C, center)
    ml = neon_circle(1.25 * s, ML_C, center + DOWN * 0.6 * s)
    dl = neon_circle(0.62 * s, DL_C, center + DOWN * 1.2 * s)
    la = T("AI", int(44 * s), AI_C).move_to(center + UP * 1.45 * s)
    lm = T("ML", int(40 * s), ML_C).move_to(center + UP * 0.25 * s)
    ld = T("DL", int(36 * s), DL_C).move_to(center + DOWN * 1.2 * s)
    return VGroup(ai, ml, dl, la, lm, ld)


class ThumbA(Scene):
    """Mascot confused on the left, glowing AI/ML/DL circles on the right, big question."""
    def construct(self):
        self.add(Circle(4.5, stroke_width=0, fill_color=AI_C, fill_opacity=0.10).move_to([-4.5, -1, 0]))
        self.add(Circle(4.0, stroke_width=0, fill_color=DL_C, fill_opacity=0.08).move_to([4.5, 0, 0]))
        m = confused_mascot().scale(1.35).move_to([-4.6, -1.0, 0])
        qs = VGroup(T("?", 110, DL_C).move_to([-3.2, 2.0, 0]).rotate(0.2),
                    T("?", 80, ML_C).move_to([-6.1, 1.6, 0]).rotate(-0.25),
                    T("?", 60, AI_C).move_to([-2.6, 0.9, 0]).rotate(0.35))
        c = circles(np.array([3.4, -0.4, 0]), 1.15)
        head = VGroup(T("AI vs ML vs DL", 92, TXT)).to_edge(UP, buff=0.35)
        head.set_x(1.2)
        tag = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, stroke_width=0, fill_color="#FF2D2D", fill_opacity=1),
                     T("Telugu lo!", 46, TXT)).rotate(0.08)
        tag[1].move_to(tag[0])
        tag.move_to([-0.6, -2.95, 0])
        self.add(m, qs, c, head, tag)


class ThumbB(Scene):
    """Big 'CONFUSED?' text, three coloured words, exam badge, small mascot."""
    def construct(self):
        for col, pos in ((AI_C, [-5, 2.5, 0]), (ML_C, [0, -3, 0]), (DL_C, [5.5, 2.5, 0])):
            self.add(Circle(3.2, stroke_width=0, fill_color=col, fill_opacity=0.09).move_to(pos))
        big = T("CONFUSED?", 150, TXT).move_to([0.9, 1.75, 0])
        words = VGroup(T("AI", 120, AI_C), T("ML", 120, ML_C), T("DL", 120, DL_C)).arrange(RIGHT, buff=0.8)
        words.move_to([0.9, -0.5, 0])
        seps = VGroup(*[T("·", 120, "#64748B") for _ in range(2)])
        seps[0].move_to((words[0].get_right() + words[1].get_left()) / 2)
        seps[1].move_to((words[1].get_right() + words[2].get_left()) / 2)
        bt = T("EXAM-READY in Telugu", 42, "#06210F")
        badge = VGroup(RoundedRectangle(width=bt.width + 0.9, height=1.05, corner_radius=0.25, stroke_width=0,
                                        fill_color=ML_C, fill_opacity=1), bt)
        bt.move_to(badge[0])
        badge.move_to([1.0, -2.55, 0])
        m = confused_mascot().scale(1.1).move_to([-5.6, -1.1, 0])
        if big.width > 10.5:
            big.scale_to_fit_width(10.5)
        self.add(big, words, seps, badge, m)
