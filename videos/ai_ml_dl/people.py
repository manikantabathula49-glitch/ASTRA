"""
Flat-style people scenes (original characters, friendly corporate-illustration look).

  manim -r 1920,1080 --frame_rate 30 people.py PresenterBoard
  manim -r 1920,1080 --frame_rate 30 people.py TeachTheRobot
  manim -r 1920,1080 --frame_rate 30 people.py StudentAndAI
"""
import numpy as np
from manim import *

BG = "#0B1020"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
PINK = "#EC4899"
TXT = "#F1F5F9"
MUTED = "#94A3B8"
SANS = "Inter"

SKIN = ["#F2C29A", "#C68642", "#8D5524"]
HAIR = ["#1F1B16", "#3B2A1A", "#111111"]

config.background_color = BG
EASE = rate_functions.ease_in_out_sine


def T(s, size=30, color=TXT, weight=BOLD):
    return Text(s, font=SANS, font_size=size, color=color, weight=weight)


def blob(color, r, pos, op=0.10):
    return Circle(r, stroke_width=0, fill_color=color, fill_opacity=op).move_to(pos)


def limb(a, b, color, w=16):
    return Line(a, b, color=color, stroke_width=w).set_cap_style(CapStyleType.ROUND)


class Person(VGroup):
    """Flat character. Keeps handles to arms/head so scenes can animate them."""

    def __init__(self, skin=SKIN[0], hair=HAIR[0], shirt=AI_C, pants="#1E293B", long_hair=False,
                 sitting=False, **kw):
        super().__init__(**kw)
        hip = np.array([0, -0.35, 0])
        if sitting:
            self.legs = VGroup(limb(hip + LEFT * 0.18, hip + LEFT * 0.18 + RIGHT * 0.7 + DOWN * 0.05, pants, 20),
                               limb(hip + RIGHT * 0.12, hip + RIGHT * 0.82 + DOWN * 0.05, pants, 20),
                               limb(hip + RIGHT * 0.65 + DOWN * 0.05, hip + RIGHT * 0.65 + DOWN * 0.9, pants, 18),
                               limb(hip + RIGHT * 0.82 + DOWN * 0.05, hip + RIGHT * 0.82 + DOWN * 0.9, pants, 18))
        else:
            self.legs = VGroup(limb(hip + LEFT * 0.17, hip + LEFT * 0.24 + DOWN * 1.25, pants, 20),
                               limb(hip + RIGHT * 0.17, hip + RIGHT * 0.24 + DOWN * 1.25, pants, 20))
            shoes = VGroup(*[RoundedRectangle(width=0.36, height=0.14, corner_radius=0.07, stroke_width=0,
                                              fill_color="#0F172A", fill_opacity=1)
                             .move_to(hip + s * RIGHT * 0.27 + DOWN * 1.36 + RIGHT * 0.05 * s) for s in (-1, 1)])
            self.legs.add(shoes)
        self.torso = RoundedRectangle(width=0.95, height=1.35, corner_radius=0.38, stroke_width=0,
                                      fill_color=shirt, fill_opacity=1).move_to([0, 0.28, 0])
        self.neck = Rectangle(width=0.2, height=0.2, stroke_width=0, fill_color=skin, fill_opacity=1).move_to([0, 0.98, 0])
        self.head = VGroup(Circle(0.33, stroke_width=0, fill_color=skin, fill_opacity=1).move_to([0, 1.33, 0]))
        hc = self.head[0].get_center()
        hair_cap = Arc(radius=0.34, start_angle=-0.15, angle=PI + 0.3, stroke_width=0, fill_color=hair, fill_opacity=1)
        hair_cap.move_arc_center_to(hc + UP * 0.03)
        hair_cap.close_path()
        self.head.add(hair_cap)
        if long_hair:
            self.head.add(RoundedRectangle(width=0.78, height=0.7, corner_radius=0.3, stroke_width=0,
                                           fill_color=hair, fill_opacity=1).move_to(hc + DOWN * 0.18).set_z_index(-1))
        self.eyes = VGroup(*[Dot(hc + RIGHT * dx + DOWN * 0.02, radius=0.035, color="#111827") for dx in (-0.11, 0.11)])
        self.mouth = Arc(radius=0.09, start_angle=PI + 0.5, angle=PI - 1.0, color="#111827", stroke_width=3).move_to(hc + DOWN * 0.14)
        self.head.add(self.eyes, self.mouth)
        self.l_sh = np.array([-0.4, 0.75, 0])
        self.r_sh = np.array([0.4, 0.75, 0])
        self.arm_l = VGroup(limb(self.l_sh, self.l_sh + DOWN * 0.95 + LEFT * 0.12, shirt, 15),
                            Dot(self.l_sh + DOWN * 0.98 + LEFT * 0.13, radius=0.1, color=skin))
        self.arm_r = VGroup(limb(self.r_sh, self.r_sh + DOWN * 0.95 + RIGHT * 0.12, shirt, 15),
                            Dot(self.r_sh + DOWN * 0.98 + RIGHT * 0.13, radius=0.1, color=skin))
        # darker sleeve tone so arms read in front of the torso
        for a in (self.arm_l, self.arm_r):
            a[0].set_color(interpolate_color(ManimColor(shirt), ManimColor("#000000"), 0.18))
        self.add(self.legs, self.arm_l, self.torso, self.neck, self.head, self.arm_r)

    def shoulder(self, side):
        # shoulder points move with the character, so read them from the torso
        t = self.torso
        x = t.get_left()[0] + 0.075 if side == "l" else t.get_right()[0] - 0.075
        return np.array([x, t.get_top()[1] - 0.2, 0])

    def raise_arm(self, side, angle):
        arm = self.arm_l if side == "l" else self.arm_r
        return Rotate(arm, angle=angle, about_point=self.shoulder(side), rate_func=EASE)


def bubble(text, color=TXT, fill="#1E293B", w=None, tail=DL):
    t = T(text, 26, color)
    r = RoundedRectangle(width=w or t.width + 0.5, height=t.height + 0.4, corner_radius=0.2, stroke_width=0,
                         fill_color=fill, fill_opacity=1)
    t.move_to(r)
    tip = r.get_corner(tail) + (RIGHT * 0.35 if tail[0] < 0 else LEFT * 0.35)
    tri = Polygon(tip + UP * 0.05, tip + RIGHT * 0.25 * (1 if tail[0] < 0 else -1) + UP * 0.05,
                  tip + DOWN * 0.25 + LEFT * 0.05 * (1 if tail[0] < 0 else -1),
                  stroke_width=0, fill_color=fill, fill_opacity=1)
    return VGroup(r, tri, t)


def bulb(color=DL_C):
    g = Circle(0.22, stroke_width=0, fill_color=color, fill_opacity=1)
    base = RoundedRectangle(width=0.2, height=0.14, corner_radius=0.04, stroke_width=0, fill_color=MUTED, fill_opacity=1)
    base.next_to(g, DOWN, buff=-0.03)
    rays = VGroup(*[Line(ORIGIN, UP * 0.14, stroke_width=4, color=color).shift(UP * 0.33).rotate(a, about_point=ORIGIN)
                    for a in np.linspace(-1.1, 1.1, 5)]).move_to(g.get_center() + UP * 0.08)
    return VGroup(rays, g, base)


# ---------------------------------------------------------------- 1. presenter + board
class PresenterBoard(Scene):
    def construct(self):
        self.add(blob(AI_C, 3.2, [-4.5, 1.5, 0]), blob(DL_C, 2.5, [5.5, -2.5, 0], 0.07))
        floor = Line([-7.2, -2.35, 0], [7.2, -2.35, 0], stroke_width=2, color=MUTED).set_opacity(0.3)
        board = RoundedRectangle(width=6.6, height=4.2, corner_radius=0.2, stroke_color=MUTED, stroke_width=3,
                                 fill_color="#0F172A", fill_opacity=1).move_to([2.75, 0.9, 0])
        legs = VGroup(limb(board.get_bottom() + LEFT * 2, board.get_bottom() + LEFT * 2.3 + DOWN * 1.2, MUTED, 6),
                      limb(board.get_bottom() + RIGHT * 2, board.get_bottom() + RIGHT * 2.3 + DOWN * 1.2, MUTED, 6))
        mani = Person(SKIN[1], HAIR[0], shirt=AI_C).move_to([-1.9, -0.5, 0])
        mani.shift(UP * (-2.35 - mani.get_bottom()[1]))

        self.play(FadeIn(floor), FadeIn(board), FadeIn(legs), run_time=0.6)
        self.play(FadeIn(mani, shift=RIGHT * 1.2), run_time=0.9, rate_func=EASE)
        self.play(mani.raise_arm("r", 1.25), run_time=0.6)   # wave hello
        self.play(Rotate(mani.arm_r, angle=-0.4, about_point=mani.shoulder("r")), run_time=0.25, rate_func=there_and_back)
        self.play(Rotate(mani.arm_r, angle=-0.4, about_point=mani.shoulder("r")), run_time=0.25, rate_func=there_and_back)
        self.play(mani.raise_arm("r", -0.45), run_time=0.4)  # point at the board

        c = board.get_center() + DOWN * 0.15
        ai = Circle(1.7, color=AI_C, fill_opacity=0.12).move_to(c)
        ml = Circle(1.15, color=ML_C, fill_opacity=0.15).move_to(c + DOWN * 0.5)
        dl = Circle(0.6, color=DL_C, fill_opacity=0.22).move_to(c + DOWN * 0.95)
        la = T("AI", 28, AI_C).move_to(ai.get_top() + DOWN * 0.3)
        lm = T("ML", 26, ML_C).move_to(ml.get_top() + DOWN * 0.3)
        ld = T("DL", 24, DL_C).move_to(dl)
        for circ, lab in ((ai, la), (ml, lm), (dl, ld)):
            self.play(Create(circ), FadeIn(lab, scale=0.6), run_time=0.7, rate_func=EASE)

        # two students at the front
        s1 = Person(SKIN[0], HAIR[1], shirt=PINK, long_hair=True).scale(0.8)
        s2 = Person(SKIN[2], HAIR[2], shirt=ML_C).scale(0.8)
        studs = VGroup(s1, s2).arrange(RIGHT, buff=0.55).move_to([-5.3, -1.1, 0])
        studs.shift(UP * (-2.35 - studs.get_bottom()[1]))
        q1 = bubble("?", DL_C, w=0.7, tail=DL).next_to(s1, UP, buff=0.1)
        q2 = bubble("?", DL_C, w=0.7, tail=DL).next_to(s2, UP, buff=0.1)
        self.play(FadeIn(studs, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.4)
        self.wait(0.5)
        say = bubble("Every DL is ML. Every ML is AI!", TXT, tail=DR).next_to(mani, UP, buff=0.15).shift(LEFT * 1.4)
        self.play(FadeIn(say, shift=UP * 0.2), Indicate(dl, color=DL_C), run_time=0.7)
        a1 = bubble("!", ML_C, w=0.7, tail=DL).move_to(q1)
        a2 = bubble("!", ML_C, w=0.7, tail=DL).move_to(q2)
        self.play(Transform(q1, a1), Transform(q2, a2), s1.head.animate.shift(UP * 0.06), s2.head.animate.shift(UP * 0.06),
                  run_time=0.4, rate_func=there_and_back_with_pause)
        self.play(Transform(q1, a1), Transform(q2, a2), run_time=0.1)
        self.play(s1.raise_arm("r", 2.4), s2.raise_arm("l", -2.4), run_time=0.5)
        self.wait(1.8)


# ---------------------------------------------------------------- 2. teach the robot
def robot():
    body = RoundedRectangle(width=1.4, height=1.5, corner_radius=0.3, stroke_width=0, fill_color="#CBD5E1", fill_opacity=1)
    head = RoundedRectangle(width=1.6, height=1.15, corner_radius=0.35, stroke_width=0, fill_color="#E2E8F0", fill_opacity=1)
    head.next_to(body, UP, buff=0.12)
    screen = RoundedRectangle(width=1.25, height=0.75, corner_radius=0.2, stroke_width=0, fill_color="#0F172A", fill_opacity=1).move_to(head)
    eyes = VGroup(*[RoundedRectangle(width=0.18, height=0.26, corner_radius=0.09, stroke_width=0, fill_color=AI_C,
                                     fill_opacity=1).move_to(screen.get_center() + RIGHT * dx) for dx in (-0.25, 0.25)])
    ant = VGroup(Line(head.get_top(), head.get_top() + UP * 0.3, color="#CBD5E1", stroke_width=6),
                 Dot(head.get_top() + UP * 0.33, radius=0.09, color=DL_C))
    arms = VGroup(limb(body.get_left() + UP * 0.4, body.get_left() + LEFT * 0.3 + DOWN * 0.4, "#94A3B8", 16),
                  limb(body.get_right() + UP * 0.4, body.get_right() + RIGHT * 0.3 + DOWN * 0.4, "#94A3B8", 16))
    wheels = VGroup(*[Circle(0.18, stroke_width=0, fill_color="#475569", fill_opacity=1).move_to(body.get_bottom() + RIGHT * dx + DOWN * 0.12)
                      for dx in (-0.4, 0.4)])
    bar_back = Rectangle(width=0.9, height=0.12, stroke_width=0, fill_color="#334155", fill_opacity=1).move_to(body.get_center() + DOWN * 0.2)
    r = VGroup(arms, wheels, body, head, screen, eyes, ant, bar_back)
    r.screen, r.eyes, r.bar_back, r.head_grp = screen, eyes, bar_back, VGroup(head, screen, eyes, ant)
    return r


def photo_card(kind):
    card = RoundedRectangle(width=1.3, height=1.6, corner_radius=0.12, stroke_width=0, fill_color=TXT, fill_opacity=1)
    face_c = card.get_center() + UP * 0.15
    if kind == "cat":
        face = Circle(0.36, stroke_width=0, fill_color=DL_C, fill_opacity=1).move_to(face_c)
        ears = VGroup(*[Triangle(stroke_width=0, fill_color=DL_C, fill_opacity=1).scale(0.16).move_to(face_c + UP * 0.33 + RIGHT * dx)
                        for dx in (-0.22, 0.22)])
        extra = VGroup(*[Line(face_c + RIGHT * s * 0.12 + DOWN * 0.08, face_c + RIGHT * s * 0.42 + DOWN * 0.04 + UP * k * 0.07,
                              color="#111827", stroke_width=2) for s in (-1, 1) for k in (-1, 1)])
        label, lc = "Cat", DL_C
    elif kind == "dog":
        face = Circle(0.36, stroke_width=0, fill_color="#A16207", fill_opacity=1).move_to(face_c)
        ears = VGroup(*[Ellipse(width=0.2, height=0.42, stroke_width=0, fill_color="#713F12", fill_opacity=1)
                        .move_to(face_c + RIGHT * dx + UP * 0.05) for dx in (-0.38, 0.38)])
        extra = Dot(face_c + DOWN * 0.08, radius=0.07, color="#111827")
        label, lc = "Dog", "#A16207"
    else:
        face = Circle(0.36, stroke_width=0, fill_color=DL_C, fill_opacity=1).move_to(face_c)
        ears = VGroup(*[Triangle(stroke_width=0, fill_color=DL_C, fill_opacity=1).scale(0.16).move_to(face_c + UP * 0.33 + RIGHT * dx)
                        for dx in (-0.22, 0.22)])
        extra = VGroup()
        label, lc = "?", PINK
    eyes = VGroup(*[Dot(face_c + RIGHT * dx + UP * 0.05, radius=0.04, color="#111827") for dx in (-0.12, 0.12)])
    tag = T(label, 24, lc).move_to(card.get_bottom() + UP * 0.25)
    return VGroup(card, ears, face, eyes, extra, tag)


class TeachTheRobot(Scene):
    def construct(self):
        self.add(blob(ML_C, 3.0, [-4.8, 0.5, 0]), blob(AI_C, 3.0, [4.8, 0.2, 0], 0.08))
        floor = Line([-7.2, -2.4, 0], [7.2, -2.4, 0], stroke_width=2, color=MUTED).set_opacity(0.3)
        hdr = T("Supervised Learning = teaching with labelled examples", 30, TXT).to_edge(UP, buff=0.45)
        p = Person(SKIN[0], HAIR[1], shirt=ML_C, long_hair=True).move_to([-4.2, 0, 0])
        p.shift(UP * (-2.4 - p.get_bottom()[1]))
        rb = robot().move_to([3.6, 0, 0])
        rb.shift(UP * (-2.4 - rb.get_bottom()[1]))
        self.play(FadeIn(floor), FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(p, shift=RIGHT), FadeIn(rb, shift=LEFT), run_time=0.8, rate_func=EASE)
        pct = T("learning 0%", 20, ML_C).next_to(rb, UP, buff=0.5)
        fill = Rectangle(width=0.01, height=0.12, stroke_width=0, fill_color=ML_C, fill_opacity=1).align_to(rb.bar_back, LEFT).set_y(rb.bar_back.get_y())
        self.add(fill)
        self.play(FadeIn(pct), run_time=0.3)
        self.play(p.raise_arm("r", 1.6), run_time=0.4)
        hand = lambda: p.arm_r[1].get_center()
        kinds = ["cat", "dog", "cat", "dog"]
        for i, k in enumerate(kinds):
            card = photo_card(k).scale(0.85).move_to(hand() + UP * 0.6 + RIGHT * 0.2)
            self.play(FadeIn(card, scale=0.6), run_time=0.3)
            self.play(card.animate.scale(0.25).move_to(rb.screen), run_time=0.55, rate_func=EASE)
            self.remove(card)
            frac = (i + 1) / len(kinds)
            self.play(fill.animate.stretch_to_fit_width(0.9 * frac).align_to(rb.bar_back, LEFT),
                      Transform(pct, T(f"learning {int(frac * 100)}%", 20, ML_C).move_to(pct)),
                      rb.eyes.animate.set_color(ML_C if i % 2 else AI_C), run_time=0.35)
        # test with an unlabeled card
        card = photo_card("q").scale(0.95).move_to(hand() + UP * 0.6 + RIGHT * 0.2)
        ask = bubble("What is this?", TXT, tail=DR).next_to(p, UP, buff=0.15).shift(LEFT * 1.1)
        self.play(FadeIn(card, scale=0.6), FadeIn(ask, shift=UP * 0.2), run_time=0.5)
        self.play(Rotate(rb.head_grp, 0.12, about_point=rb.head_grp.get_bottom()), run_time=0.3, rate_func=there_and_back)
        ans = bubble("Cat! 96%", ML_C, tail=DL).next_to(rb, UP, buff=0.15).shift(LEFT * 0.4)
        self.play(FadeOut(pct), FadeIn(ans, scale=0.6), rb.eyes.animate.set_color(ML_C), run_time=0.5)
        self.play(p.raise_arm("l", -2.6), run_time=0.45)
        foot = T("Show examples with answers → the machine learns → it predicts new ones", 24, ML_C).to_edge(DOWN, buff=0.4)
        self.play(Write(foot), run_time=1.0)
        self.wait(1.6)


# ---------------------------------------------------------------- 3. student + AI
class StudentAndAI(Scene):
    def construct(self):
        self.add(blob(PINK, 3.0, [-4.0, -0.5, 0], 0.08), blob(AI_C, 3.2, [4.0, 1.0, 0], 0.09))
        desk = RoundedRectangle(width=4.6, height=0.18, corner_radius=0.06, stroke_width=0, fill_color="#334155", fill_opacity=1).move_to([-2.0, -0.95, 0])
        dleg = VGroup(*[Rectangle(width=0.14, height=1.35, stroke_width=0, fill_color="#334155", fill_opacity=1)
                        .move_to(desk.get_center() + RIGHT * dx + DOWN * 0.75) for dx in (-2.0, 2.0)])
        chair = VGroup(Rectangle(width=0.9, height=0.14, stroke_width=0, fill_color="#475569", fill_opacity=1).move_to([-3.55, -1.25, 0]),
                       Rectangle(width=0.14, height=1.1, stroke_width=0, fill_color="#475569", fill_opacity=1).move_to([-4.0, -0.7, 0]),
                       Rectangle(width=0.1, height=0.95, stroke_width=0, fill_color="#475569", fill_opacity=1).move_to([-3.55, -1.8, 0]))
        st = Person(SKIN[1], HAIR[2], shirt=PINK, sitting=True).move_to([-3.25, -0.35, 0])
        lap_base = Polygon([-2.25, -0.86, 0], [-1.05, -0.86, 0], [-1.15, -0.78, 0], [-2.15, -0.78, 0],
                           stroke_width=0, fill_color="#94A3B8", fill_opacity=1)
        lap_screen = Polygon([-2.15, -0.78, 0], [-1.55, 0.2, 0], [-1.25, 0.2, 0], [-1.85, -0.78, 0],
                             stroke_width=0, fill_color="#CBD5E1", fill_opacity=1)
        glow_ = Circle(0.5, stroke_width=0, fill_color=AI_C, fill_opacity=0.25).move_to([-1.7, -0.3, 0])
        self.play(FadeIn(VGroup(desk, dleg, chair)), run_time=0.4)
        self.play(FadeIn(st, shift=UP * 0.3), FadeIn(lap_base), FadeIn(lap_screen), FadeIn(glow_), run_time=0.7)
        # forearms reach the keyboard
        self.play(st.raise_arm("r", 1.15), st.raise_arm("l", 1.0), run_time=0.5)
        # typing bob
        for _ in range(3):
            self.play(st.arm_r.animate.shift(DOWN * 0.05), st.arm_l.animate.shift(UP * 0.04), run_time=0.12)
            self.play(st.arm_r.animate.shift(UP * 0.05), st.arm_l.animate.shift(DOWN * 0.04), run_time=0.12)
        q = bubble("What is Deep Learning?", TXT, fill="#1E293B", tail=DL).move_to([1.6, 1.6, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.5)
        think = bubble("?", DL_C, w=0.7, tail=DR).next_to(st.head, UP, buff=0.15).shift(LEFT * 0.4)
        self.play(FadeIn(think, scale=0.5), run_time=0.3)
        dots = VGroup(*[Dot(radius=0.07, color=MUTED) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        ai_b = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.2, stroke_width=0, fill_color=AI_C, fill_opacity=0.25).move_to([3.3, 0.5, 0])
        dots.move_to(ai_b)
        self.play(FadeIn(ai_b), FadeIn(dots), run_time=0.3)
        self.play(*[d.animate.shift(UP * 0.12) for d in dots], lag_ratio=0.3, run_time=0.5, rate_func=there_and_back)
        reply = VGroup(T("Neural networks with many layers,", 24, TXT, NORMAL),
                       T("learning patterns from lots of data.", 24, TXT, NORMAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rb = RoundedRectangle(width=reply.width + 0.6, height=reply.height + 0.45, corner_radius=0.22, stroke_width=0,
                              fill_color=AI_C, fill_opacity=0.25)
        rgrp = VGroup(rb, reply).move_to([3.0, 0.2, 0])
        reply.move_to(rb)
        self.play(FadeOut(dots), ReplacementTransform(ai_b, rb), FadeIn(reply, shift=UP * 0.1), run_time=0.6)
        light = bulb().move_to(think)
        self.play(FadeOut(think, scale=0.5), FadeIn(light, scale=1.6), st.head.animate.shift(UP * 0.05), run_time=0.5)
        self.play(Flash(light, color=DL_C, flash_radius=0.45, line_length=0.15), run_time=0.4)
        foot = T("Ask. Understand. Build.", 34, TXT).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(foot, shift=UP * 0.2), run_time=0.6)
        self.wait(1.6)
