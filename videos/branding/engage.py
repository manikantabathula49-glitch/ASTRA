"""
Engagement bar: avatar + Like, Share, Comment, Subscribe, Bell, clicked one by one.
Click times are written to <Scene>_events.json so render_engage.sh can add sounds exactly on each click.

  manim -t --format mov -r 1920,1080 --frame_rate 30 engage.py Engage_ai_ml_dl
"""
import json
import os

import numpy as np
from manim import *

from branding import BG, AI_C, ML_C, DL_C, TXT, MUTED, RED, T, bell, cursor, GREEN

HERE = os.path.dirname(os.path.abspath(__file__))
PILL = "#1F2937"


def thumb(color=TXT, s=1.0):
    palm = RoundedRectangle(width=0.30, height=0.30, corner_radius=0.07, stroke_width=0, fill_color=color, fill_opacity=1)
    cuff = RoundedRectangle(width=0.09, height=0.32, corner_radius=0.03, stroke_width=0, fill_color=color, fill_opacity=1)
    cuff.next_to(palm, LEFT, buff=0.04)
    th = RoundedRectangle(width=0.11, height=0.26, corner_radius=0.05, stroke_width=0, fill_color=color, fill_opacity=1)
    th.rotate(-0.35).move_to(palm.get_corner(UL) + RIGHT * 0.1 + UP * 0.1)
    return VGroup(cuff, palm, th).scale(s)


def share_icon(color=TXT):
    a = CurvedArrow(LEFT * 0.2 + DOWN * 0.13, RIGHT * 0.2 + UP * 0.1, angle=-PI / 2.5, color=color, stroke_width=5,
                    tip_length=0.14)
    return VGroup(a)


def comment_icon(color=TXT, dots_color=PILL):
    box = RoundedRectangle(width=0.44, height=0.32, corner_radius=0.08, stroke_width=0, fill_color=color, fill_opacity=1)
    tail = Polygon(box.get_corner(DL) + RIGHT * 0.07, box.get_corner(DL) + RIGHT * 0.2, box.get_corner(DL) + DOWN * 0.12 + RIGHT * 0.04,
                   stroke_width=0, fill_color=color, fill_opacity=1)
    dots = VGroup(*[Dot(radius=0.03, color=dots_color) for _ in range(3)]).arrange(RIGHT, buff=0.06).move_to(box)
    return VGroup(box, tail, dots)


def pill(icon, label, w):
    r = RoundedRectangle(width=w, height=0.72, corner_radius=0.36, stroke_width=0, fill_color=PILL, fill_opacity=1)
    t = T(label, 24, TXT)
    g = VGroup(icon, t).arrange(RIGHT, buff=0.18).move_to(r)
    return VGroup(r, g)


def engage(scene, note):
    events = []
    mark = lambda kind: events.append({"t": round(scene.renderer.time, 3), "type": kind})

    av = ImageMobject(os.path.join(HERE, "assets", "mani_avatar.png")).scale_to_fit_height(1.05)
    ring = Circle(radius=0.55, stroke_color=AI_C, stroke_width=5)
    avatar = Group(av, ring)
    name = VGroup(T("AI with Mani", 28, TXT), T(note, 18, MUTED, NORMAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    if name[1].width > 2.6:
        name[1].scale_to_fit_width(2.6)
    who = Group(avatar, name).arrange(RIGHT, buff=0.22)

    like = pill(thumb(), "Like", 1.75)
    share = pill(share_icon(), "Share", 1.85)
    comment = pill(comment_icon(), "Comment", 2.25)
    sub_r = RoundedRectangle(width=2.45, height=0.72, corner_radius=0.36, stroke_width=0, fill_color=RED, fill_opacity=1)
    sub_t = T("SUBSCRIBE", 26, WHITE).move_to(sub_r)
    sub = VGroup(sub_r, sub_t)
    bell_c = Circle(0.36, stroke_width=0, fill_color=PILL, fill_opacity=1)
    bl = bell(0.36, TXT).move_to(bell_c)
    bellb = VGroup(bell_c, bl)

    row = Group(who, like, share, comment, sub, bellb).arrange(RIGHT, buff=0.22)
    panel = RoundedRectangle(width=row.width + 0.7, height=1.5, corner_radius=0.4, stroke_color=AI_C, stroke_width=2,
                             fill_color="#0F172A", fill_opacity=1 if GREEN else 0.94).move_to(row)
    bar = Group(panel, row)
    if bar.width > 13.8:
        bar.scale_to_fit_width(13.8)
    bar.to_edge(DOWN, buff=0.55)
    home = bar.get_center()
    bar.shift(DOWN * 3)

    scene.play(bar.animate.move_to(home), run_time=0.55, rate_func=rate_functions.ease_out_back)
    mark("whoosh_in")

    cur = cursor(0.55).move_to(like.get_center() + RIGHT * 1.5 + UP * 1.6)
    scene.play(FadeIn(cur), run_time=0.15)

    def click(target, kind, after):
        scene.play(cur.animate.move_to(target.get_center() + RIGHT * 0.18 + DOWN * 0.22), run_time=0.45,
                   rate_func=rate_functions.ease_in_out_sine)
        scene.play(cur.animate.scale(0.85), target.animate.scale(0.93), run_time=0.07)
        mark(kind)
        ripple = Circle(0.12, color=WHITE, stroke_width=3).move_to(cur.get_corner(UL))
        scene.play(cur.animate.scale(1 / 0.85), target.animate.scale(1 / 0.93),
                   ripple.animate.scale(4).set_stroke(opacity=0), run_time=0.18)
        scene.remove(ripple)
        scene.play(*after, run_time=0.22)

    # 1 like: icon turns blue and pops
    click(like, "click", [like[1][0].animate.set_color(AI_C), like[1][1].animate.set_color(AI_C)])
    scene.play(Indicate(like[1][0], scale_factor=1.35, color=AI_C), run_time=0.35)
    # 2 share: arrow turns green, little sparks fly
    sparks = VGroup(*[Dot(radius=0.04, color=ML_C).move_to(share.get_center()) for _ in range(6)])
    click(share, "click", [share[1].animate.set_color(ML_C)])
    scene.add(sparks)
    scene.play(*[s.animate.shift(0.55 * np.array([np.cos(a), np.sin(a), 0])).set_opacity(0)
                 for s, a in zip(sparks, np.linspace(0, TAU, 6, endpoint=False))], run_time=0.35)
    scene.remove(sparks)
    # 3 comment: bubble turns amber, dots bounce
    click(comment, "click", [comment[1][0][0].animate.set_color(DL_C), comment[1][0][1].animate.set_color(DL_C)])
    scene.play(*[d.animate.shift(UP * 0.06) for d in comment[1][0][2]], lag_ratio=0.3, run_time=0.3,
               rate_func=there_and_back)
    # 4 subscribe: red -> grey, SUBSCRIBED
    click(sub, "pop", [sub_r.animate.set_fill("#3F3F46"),
                       Transform(sub_t, T("SUBSCRIBED ✓", 22, WHITE).scale_to_fit_width(sub_r.width - 0.4).move_to(sub_r))])
    # 5 bell: rings and turns amber
    click(bellb, "ding", [bl.animate.set_color(DL_C)])
    scene.play(Wiggle(bl, scale_value=1.25, rotation_angle=0.25 * PI, n_wiggles=5), run_time=0.8)
    scene.play(FadeOut(cur), Flash(bl, color=DL_C, flash_radius=0.5, line_length=0.18), run_time=0.35)
    scene.wait(1.1)
    mark("whoosh_out")
    scene.play(bar.animate.shift(DOWN * 3), run_time=0.45, rate_func=rate_functions.ease_in_back)

    with open(os.path.join(HERE, f"{type(scene).__name__}_events.json"), "w") as f:
        json.dump({"duration": round(scene.renderer.time, 3), "events": events}, f)


NOTES = [
    ("ai_ml_dl", "Exams ki ready? Save this video!"),
    ("quantum", "Quantum series: next episode soon"),
    ("general", "AI, ML & Quantum in Telugu"),
]
for _slug, _note in NOTES:
    globals()[f"Engage_{_slug}"] = type(f"Engage_{_slug}", (Scene,),
                                        {"construct": (lambda n: lambda self: engage(self, n))(_note)})
