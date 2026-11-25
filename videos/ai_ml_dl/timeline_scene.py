"""
AI history timeline synced to the voiceover (voice/timeline.mp3).
Cue times (seconds) come from voice/timeline_cues.json: {"1950": t, "1956": t, ...}.

  manim -r 1920,1080 --frame_rate 30 timeline_scene.py AITimeline
"""
import json
import os

import numpy as np
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
BG = "#0B0F1A"
AI_C, ML_C, DL_C = "#4F8CFF", "#22C55E", "#F59E0B"
TXT, MUTED, PAPER = "#F1F5F9", "#94A3B8", "#FFF7E6"
SANS = "Inter"
config.background_color = BG
SPACING = 7.5


def T(s, size, color=TXT, weight=BOLD):
    return Text(s, font=SANS, font_size=size, color=color, weight=weight)


def photo_card(path, credit, w=3.3, h=3.9):
    img = ImageMobject(os.path.join(HERE, "photos", path))
    img.scale_to_fit_height(h) if img.width / img.height < w / h else img.scale_to_fit_width(w)
    frame = RoundedRectangle(width=img.width + 0.3, height=img.height + 0.75, corner_radius=0.12, stroke_width=0,
                             fill_color=PAPER, fill_opacity=1)
    img.move_to(frame.get_center() + UP * 0.22)
    cr = T(credit, 13, "#6B7280", NORMAL)
    if cr.width > frame.width - 0.2:
        cr.scale_to_fit_width(frame.width - 0.2)
    cr.move_to(frame.get_bottom() + UP * 0.25)
    shadow = frame.copy().set_fill(BLACK, 0.45).shift(DR * 0.12)
    return Group(shadow, frame, img, cr), img


def text_block(year, title, sub, color):
    y = T(year, 84, color)
    t = T(title, 34, TXT)
    s = Paragraph(*sub, font=SANS, font_size=24, color=MUTED, alignment="left")
    g = VGroup(y, t, s).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    if g.width > 5.6:
        g.scale_to_fit_width(5.6)
    return g


def imagenet_grid():
    rng = np.random.default_rng(1)
    cols = ["#EF4444", "#F59E0B", "#22C55E", "#3B82F6", "#A855F7", "#EC4899", "#14B8A6", "#EAB308"]
    g = VGroup(*[RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, stroke_width=0,
                                  fill_color=cols[rng.integers(0, 8)], fill_opacity=rng.uniform(0.45, 0.95))
                 for _ in range(48)]).arrange_in_grid(6, 8, buff=0.08)
    return g


def paper_card():
    page = RoundedRectangle(width=3.2, height=4.0, corner_radius=0.08, stroke_width=0, fill_color=PAPER, fill_opacity=1)
    title = Paragraph("Attention Is", "All You Need", font=SANS, font_size=30, color="#111827", weight=BOLD,
                      alignment="center").move_to(page.get_top() + DOWN * 0.75)
    auth = T("Vaswani et al., 2017", 16, "#4B5563", NORMAL).next_to(title, DOWN, buff=0.2)
    lines = VGroup(*[Line(LEFT * 1.2, RIGHT * 1.2, stroke_width=3, color="#D1D5DB") for _ in range(9)])
    lines.arrange(DOWN, buff=0.18).next_to(auth, DOWN, buff=0.3)
    return VGroup(page, title, auth, lines)


def chat_card():
    win = RoundedRectangle(width=4.2, height=3.4, corner_radius=0.25, stroke_color="#334155", stroke_width=2,
                           fill_color="#111827", fill_opacity=1)
    q = VGroup(RoundedRectangle(width=2.6, height=0.6, corner_radius=0.25, stroke_width=0, fill_color=AI_C, fill_opacity=1),
               T("What is AI?", 22, WHITE))
    q[1].move_to(q[0])
    q.move_to(win.get_top() + DOWN * 0.7 + RIGHT * 0.55)
    a_box = RoundedRectangle(width=3.4, height=1.4, corner_radius=0.25, stroke_width=0, fill_color="#1F2937", fill_opacity=1)
    a_box.move_to(win.get_center() + DOWN * 0.55 + LEFT * 0.2)
    a_txt = Paragraph("AI means machines doing", "tasks that need human", "intelligence...", font=SANS,
                      font_size=20, color=TXT, alignment="left").move_to(a_box)
    return VGroup(win, q), a_box, a_txt


class AITimeline(MovingCameraScene):
    def construct(self):
        cues = json.load(open(os.path.join(HERE, "voice", "timeline_cues.json")))
        total = cues.get("_end", 43.7)
        events = [
            ("1950", "Can machines think?", ["Alan Turing asks the question", "that starts it all"], AI_C,
             ("turing.jpg", "Photo: public domain")),
            ("1956", "\"Artificial Intelligence\" is born", ["John McCarthy & the Dartmouth", "workshop name the field"], AI_C,
             ("mccarthy.jpg", "Photo: null0, CC BY-SA 2.0")),
            ("1959", "\"Machine Learning\"", ["Arthur Samuel's checkers program", "learns on an IBM 701"], ML_C,
             ("ibm701.jpg", "IBM 701 photo: Dan, CC BY 2.0")),
            ("1986", "Backpropagation popular", ["Rumelhart, Hinton & Williams:", "how neural networks learn"], DL_C,
             ("hinton.jpg", "Geoffrey Hinton. Photo: Arthur Petron, CC BY-SA 4.0")),
            ("1997", "Deep Blue wins", ["IBM's computer beats world", "chess champion Garry Kasparov"], AI_C,
             ("deepblue.jpg", "Photo: James the photographer, CC BY 2.0")),
            ("2012", "AlexNet: the DL boom", ["Wins the ImageNet competition", "by a huge margin"], DL_C, "imagenet"),
            ("2017", "Transformers", ["The architecture behind", "ChatGPT, Gemini and Claude"], DL_C, "paper"),
            ("2022", "ChatGPT launches", ["AI reaches everyone.", "And now... we're in this story."], ML_C, "chat"),
        ]
        n = len(events)
        track = Line(LEFT * 3, RIGHT * (SPACING * (n - 1) + 6), stroke_width=4, color="#334155").shift(DOWN * 2.9)
        glow = track.copy().set_stroke(AI_C, 10, 0.12)
        self.add(glow, track)
        title = T("A short history of AI", 44, TXT).move_to(UP * 3.3)
        self.add(title)
        self.camera.frame.move_to(ORIGIN)

        def wait_until(t):
            dt = t - self.renderer.time
            if dt > 0.02:
                self.wait(dt)

        for i, (year, head, sub, color, media) in enumerate(events):
            cx = i * SPACING
            t_cue = cues.get(year, i * total / n)
            move = 0.9 if i else 0.0
            wait_until(max(0, t_cue - move - 0.1))
            if i:
                self.play(self.camera.frame.animate.move_to([cx, 0, 0]), title.animate.move_to([cx, 3.3, 0]),
                          run_time=move, rate_func=rate_functions.ease_in_out_cubic)
            dot = Dot([cx, -2.9, 0], radius=0.16, color=color)
            ring = Circle(0.16, color=color, stroke_width=4).move_to(dot)
            yr_tick = T(year, 22, MUTED, NORMAL).next_to(dot, DOWN, buff=0.18)
            tb = text_block(year, head, sub, color).move_to([cx + 2.6, 0.2, 0], aligned_edge=LEFT)
            tb.set_x(cx + 0.35, direction=LEFT)
            left = cx - 2.6
            if isinstance(media, tuple):
                card, img = photo_card(*media)
                card.move_to([left, 0.15, 0]).rotate(-0.04)
                self.play(GrowFromCenter(dot), ring.animate.scale(2.5).set_stroke(opacity=0), FadeIn(yr_tick),
                          FadeIn(card, shift=UP * 0.6, scale=0.92), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in tb], lag_ratio=0.25), run_time=0.8)
                card.add_updater(lambda m, dt: m.scale(1 + 0.006 * dt))  # gentle push-in while it's on screen
            elif media == "imagenet":
                grid = imagenet_grid().move_to([left, 0.3, 0])
                err = VGroup(T("Top-5 error", 22, MUTED, NORMAL), T("26.2%  →  15.3%", 40, DL_C)).arrange(DOWN, buff=0.1)
                err.next_to(grid, DOWN, buff=0.3)
                self.play(GrowFromCenter(dot), FadeIn(yr_tick), LaggedStart(*[FadeIn(c, scale=0.5) for c in grid],
                                                                            lag_ratio=0.01), run_time=0.9)
                self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in tb], lag_ratio=0.25), FadeIn(err),
                          run_time=0.8)
            elif media == "paper":
                pc = paper_card().move_to([left, 0.15, 0]).rotate(0.04)
                arcs = VGroup(*[ArcBetweenPoints(pc.get_right() + UP * y1, pc.get_right() + UP * y2, angle=-PI / 2,
                                                 color=DL_C, stroke_width=3, stroke_opacity=0.7)
                                for y1, y2 in ((1.2, -0.4), (0.6, -1.1), (0.0, -1.6))])
                self.play(GrowFromCenter(dot), FadeIn(yr_tick), FadeIn(pc, shift=UP * 0.6), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in tb], lag_ratio=0.25),
                          LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), run_time=0.9)
            else:
                win, a_box, a_txt = chat_card()
                VGroup(win, a_box, a_txt).move_to([left, 0.2, 0])
                self.play(GrowFromCenter(dot), FadeIn(yr_tick), FadeIn(win, shift=UP * 0.6), run_time=0.6)
                self.play(FadeIn(a_box), AddTextLetterByLetter(a_txt[0]), run_time=0.6)
                self.play(AddTextLetterByLetter(a_txt[1]), run_time=0.5)
                self.play(AddTextLetterByLetter(a_txt[2]), run_time=0.4)
                self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in tb], lag_ratio=0.25), run_time=0.8)
            # progress line fills up to this event
            prog = Line([cx - SPACING if i else -3, -2.9, 0], [cx, -2.9, 0], stroke_width=6, color=color)
            self.play(Create(prog), run_time=0.4)

        # "you are here": the camera pulls back over the whole history
        wait_until(cues.get("_now", total - 4.5))
        here = VGroup(Triangle(fill_color=DL_C, fill_opacity=1, stroke_width=0).scale(0.18).rotate(PI),
                      T("YOU ARE HERE", 26, DL_C)).arrange(DOWN, buff=0.12)
        here.move_to([(n - 1) * SPACING + 1.8, -2.2, 0])
        self.play(self.camera.frame.animate.scale(2.45).move_to([(n - 1) * SPACING / 2, -0.2, 0]),
                  title.animate.scale(2.2).move_to([(n - 1) * SPACING / 2, 6.6, 0]), run_time=1.8,
                  rate_func=rate_functions.ease_in_out_cubic)
        self.play(FadeIn(here, shift=DOWN * 0.4, scale=2.0), run_time=0.5)
        wait_until(total)
