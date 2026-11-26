"""
"Next level" scenes for AI vs ML vs DL, in styles found on Pinterest
(kinetic typography, holographic HUD, object + big counter). Original designs.

  manim -r 1920,1080 --frame_rate 30 next_level.py HookKinetic
  manim -r 1920,1080 --frame_rate 30 next_level.py HudNeural
  manim -r 1920,1080 --frame_rate 30 next_level.py BigFact
"""
import numpy as np
from manim import *

BG = "#070B14"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
CYAN = "#22D3EE"
PURPLE = "#A855F7"
TXT = "#F1F5F9"
MUTED = "#64748B"
SANS = "Inter"
SERIF = "DejaVu Serif"

config.background_color = BG


def T(s, size=40, color=TXT, weight=BOLD, font=SANS, slant=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight, slant=slant)


def glow(m, color, width=4, layers=4):
    """Neon glow: wide, faint copies behind a thin bright stroke."""
    g = VGroup()
    for i in range(layers, 0, -1):
        g.add(m.copy().set_stroke(color, width=width + i * 5, opacity=0.06).set_fill(opacity=0))
    g.add(m.copy().set_stroke(color, width=width, opacity=1))
    return g


def cursor(size=0.55):
    pts = np.array([[0, 0], [0, -1], [0.27, -0.75], [0.45, -1.1], [0.58, -1.04], [0.4, -0.7], [0.75, -0.7]]) * size
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=BLACK, stroke_width=3,
                   fill_color=WHITE, fill_opacity=1)


def chamfer_frame(w, h, c=0.3, color=CYAN):
    pts = [[-w / 2 + c, h / 2], [w / 2, h / 2], [w / 2, -h / 2 + c], [w / 2 - c, -h / 2],
           [-w / 2, -h / 2], [-w / 2, h / 2 - c]]
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.05)


def grid_bg(step=0.6, opacity=0.07):
    lines = VGroup()
    for x in np.arange(-7.2, 7.3, step):
        lines.add(Line([x, -4.1, 0], [x, 4.1, 0]))
    for y in np.arange(-4.2, 4.3, step):
        lines.add(Line([-7.2, y, 0], [7.2, y, 0]))
    return lines.set_stroke(CYAN, 1, opacity)


# ------------------------------------------------------------------ 1. hook
class HookKinetic(Scene):
    def construct(self):
        self.add(grid_bg(opacity=0.04))
        # beat 1: AI. ML. DL. snap in one by one
        words = [("AI.", AI_C), ("ML.", ML_C), ("DL.", DL_C)]
        stack = VGroup()
        for i, (w, c) in enumerate(words):
            t = T(w, 130, c)
            stack.add(t)
        stack.arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to(LEFT * 4.3)
        for t in stack:
            hit = Line(t.get_left() + LEFT * 0.3, t.get_right() + RIGHT * 0.3, color=t.get_color(),
                       stroke_width=6).next_to(t, DOWN, buff=0.02)
            self.play(FadeIn(t, scale=1.7), run_time=0.22, rate_func=rush_into)
            self.play(t.animate.shift(RIGHT * 0.08), ShowPassingFlash(hit, time_width=0.6), run_time=0.08)
            self.play(t.animate.shift(LEFT * 0.08), run_time=0.08)
            self.wait(0.35)

        # beat 2: "Confused?" in italic serif + cursor selects it
        q = T("Confused?", 100, TXT, NORMAL, SERIF, ITALIC).next_to(stack, RIGHT, buff=0.8)
        if q.get_right()[0] > 6.4:
            q.scale_to_fit_width(6.4 - q.get_left()[0])
        self.play(Write(q), run_time=0.8)
        box = DashedVMobject(SurroundingRectangle(q, buff=0.22, color=DL_C, stroke_width=4), num_dashes=46)
        handles = VGroup(*[Square(0.16, color=DL_C, fill_color=BG, fill_opacity=1, stroke_width=3)
                           .move_to(box.get_corner(v)) for v in (UL, UR, DL, DR)])
        cur = cursor().move_to(q.get_corner(DR) + RIGHT * 2 + DOWN * 1.5)
        self.play(FadeIn(cur), run_time=0.2)
        self.play(cur.animate.move_to(q.get_corner(DR) + LEFT * 0.2 + DOWN * 0.1), run_time=0.5)
        self.play(Create(box), FadeIn(handles), run_time=0.45)
        hl = BackgroundRectangle(q, color=DL_C, fill_opacity=0.22, buff=0.22)
        self.play(FadeIn(hl), q.animate.set_color(DL_C), run_time=0.3)
        self.wait(0.6)
        self.play(*[FadeOut(m, shift=UP * 0.4) for m in (stack, q, box, handles, cur, hl)], run_time=0.45)

        # beat 3: words travel along a curve
        path = FunctionGraph(lambda x: 0.9 * np.sin(x * 0.75), x_range=[-6.2, 6.2]).set_stroke(MUTED, 3)
        pts = [path.point_from_proportion(p) for p in (0.12, 0.5, 0.88)]
        labels = [("Artificial Intelligence", AI_C), ("Machine Learning", ML_C), ("Deep Learning", DL_C)]
        self.play(Create(path), run_time=0.7)
        dot = Dot(path.get_start(), radius=0.12, color=TXT)
        self.add(dot)
        prev = 0
        for (txt, c), p, prop in zip(labels, pts, (0.12, 0.5, 0.88)):
            seg = path.get_subcurve(prev, prop) if prop > prev else path
            self.play(MoveAlongPath(dot, seg), run_time=0.45, rate_func=linear)
            node = glow(Circle(0.16).move_to(p), c, 4, 3)
            lab = T(txt, 34, c).next_to(p, UP if prop != 0.5 else DOWN, buff=0.35)
            self.play(FadeIn(node, scale=2), FadeIn(lab, shift=UP * 0.2), run_time=0.3)
            prev = prop
        self.wait(0.5)
        self.play(FadeOut(VGroup(path, dot), shift=DOWN * 0.3), *[FadeOut(m) for m in self.mobjects
                                                                   if m not in (path, dot)], run_time=0.4)

        # beat 4: promise
        l1 = T("One video. All 3.", 84, TXT)
        l2 = T("Exam-ready.", 84, DL_C)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        self.play(FadeIn(l1, shift=UP * 0.4), run_time=0.4)
        self.play(FadeIn(l2, scale=1.4), run_time=0.3)
        stamp = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, stroke_color=ML_C,
                                        stroke_width=5, fill_color=ML_C, fill_opacity=0.15),
                       T("Telugu lo!", 44, ML_C)).rotate(0.18).move_to(g.get_corner(DR) + DOWN * 0.75 + LEFT * 0.4)
        stamp[1].move_to(stamp[0])
        self.play(FadeIn(stamp, scale=2.2), run_time=0.25, rate_func=rush_into)
        self.wait(1.6)


# ------------------------------------------------------------------ 2. HUD
class HudNeural(Scene):
    def construct(self):
        self.add(grid_bg())
        c = LEFT * 0.0 + DOWN * 0.2
        # rings
        r1 = glow(Circle(1.95).move_to(c), CYAN, 2, 3)
        r2 = DashedVMobject(Circle(2.35).move_to(c), num_dashes=72).set_stroke(PURPLE, 3)
        r3 = VGroup(*[glow(Arc(radius=2.75, start_angle=a, angle=0.9).move_arc_center_to(c), CYAN, 5, 3)
                      for a in (0, 2.1, 4.2)])
        ticks = VGroup(*[Line(c + 3.05 * np.array([np.cos(a), np.sin(a), 0]),
                              c + (3.18 if i % 6 else 3.32) * np.array([np.cos(a), np.sin(a), 0]))
                         for i, a in enumerate(np.linspace(0, TAU, 96, endpoint=False))]).set_stroke(CYAN, 2, 0.6)
        r2.add_updater(lambda m, dt: m.rotate(0.35 * dt, about_point=c))
        r3.add_updater(lambda m, dt: m.rotate(-0.6 * dt, about_point=c))
        ticks.add_updater(lambda m, dt: m.rotate(0.12 * dt, about_point=c))

        # network inside
        sizes = [3, 4, 4, 2]
        xs = np.linspace(-1.2, 1.2, 4)
        layers = []
        for x, n in zip(xs, sizes):
            ys = np.linspace(-(n - 1) * 0.42, (n - 1) * 0.42, n)
            layers.append([c + np.array([x, y, 0]) for y in ys])
        edges = VGroup(*[Line(a, b).set_stroke(CYAN, 1.2, 0.35) for l1, l2 in zip(layers, layers[1:])
                         for a in l1 for b in l2])
        nodes = VGroup(*[VGroup(Circle(0.12).move_to(p).set_stroke(CYAN, 2).set_fill(BG, 1),
                                Dot(p, radius=0.05, color=CYAN)) for l in layers for p in l])

        # header
        dot = Dot(radius=0.08, color=ML_C)
        head = VGroup(dot, T("NEURAL NETWORK  //  ONLINE", 28, CYAN)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.4)
        dot.add_updater(lambda m, dt: m.set_opacity(0.3 + 0.7 * (np.sin(self.renderer.time * 8) > 0)))

        # left panel
        lp = chamfer_frame(3.3, 3.4).move_to(LEFT * 5.2 + DOWN * 0.2)
        lt = T("MODEL", 22, PURPLE).move_to(lp.get_top() + DOWN * 0.4).align_to(lp, LEFT).shift(RIGHT * 0.3)
        rows = [("TYPE", "DEEP NET"), ("LAYERS", "04"), ("NEURONS", "13"), ("TASK", "CAT / DOG")]
        rowg = VGroup(*[VGroup(T(k, 18, MUTED, NORMAL), T(v, 22, TXT)).arrange(RIGHT, buff=0.3)
                        for k, v in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(lt, DOWN, buff=0.35, aligned_edge=LEFT)
        # right panel
        rp = chamfer_frame(3.3, 3.4, color=PURPLE).move_to(RIGHT * 5.2 + DOWN * 0.2)
        rt = T("ACCURACY", 22, PURPLE).move_to(rp.get_top() + DOWN * 0.4).align_to(rp, LEFT).shift(RIGHT * 0.3)
        acc = ValueTracker(0)
        accv = always_redraw(lambda: T(f"{acc.get_value():.1f}%", 52, ML_C).next_to(rt, DOWN, buff=0.3, aligned_edge=LEFT))
        bars = VGroup()
        for i, (name, target) in enumerate((("EPOCH", 0.9), ("LOSS", 0.12), ("DATA", 0.75))):
            back = Rectangle(width=2.6, height=0.14, stroke_width=0, fill_color=MUTED, fill_opacity=0.3)
            lab = T(name, 16, MUTED, NORMAL)
            row = VGroup(lab, back).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            bars.add(row)
        bars.arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(rt, DOWN, buff=1.25, aligned_edge=LEFT)
        fills = VGroup(*[Rectangle(width=0.01, height=0.14, stroke_width=0, fill_color=col, fill_opacity=1)
                         .move_to(b[1].get_left(), aligned_edge=LEFT)
                         for b, col in zip(bars, (CYAN, DL_C, PURPLE))])

        # scan line
        scan = Line(LEFT * 7.2, RIGHT * 7.2).set_stroke(CYAN, 2, 0.5).move_to(UP * 4)

        self.play(FadeIn(head, shift=DOWN * 0.2), Create(ticks), run_time=0.8)
        self.play(Create(r1), Create(r2), Create(r3), run_time=1.0)
        self.play(Create(lp), Create(rp), FadeIn(lt), FadeIn(rt), run_time=0.6)
        self.play(Create(edges), LaggedStart(*[FadeIn(n, scale=0.4) for n in nodes], lag_ratio=0.05), run_time=1.0)
        self.add(accv)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rowg], lag_ratio=0.2),
                  FadeIn(bars), run_time=0.8)
        self.add(fills)
        self.play(acc.animate.set_value(97.4),
                  *[f.animate.stretch_to_fit_width(2.6 * t).align_to(b[1], LEFT)
                    for f, b, t in zip(fills, bars, (0.9, 0.12, 0.75))],
                  scan.animate.move_to(DOWN * 4),
                  *[ShowPassingFlash(e.copy().set_stroke(CYAN, 4, 1), time_width=0.5) for e in edges],
                  run_time=3.0, rate_func=smooth)
        out = T("CAT ✓", 26, ML_C).move_to(c + DOWN * 1.68)
        self.play(FadeIn(out, shift=UP * 0.2), Flash(c + RIGHT * 1.2 + UP * 0.42, color=ML_C), run_time=0.6)
        cap = T("Deep Learning: many layers, learning by itself", 30, TXT).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)


# ------------------------------------------------------------------ 3. big fact
class BigFact(Scene):
    def construct(self):
        self.add(grid_bg(opacity=0.035))
        c = UP * 1.75
        R = 1.2
        t0 = ValueTracker(0)

        def globe():
            g = VGroup()
            ph = t0.get_value()
            for k in range(8):
                a = ph + k * PI / 8
                w = abs(np.cos(a)) * 2 * R
                g.add(Ellipse(width=max(w, 0.02), height=2 * R).move_to(c)
                      .set_stroke(CYAN if np.cos(a) > 0 else PURPLE, 2, 0.75 if np.cos(a) > 0 else 0.3))
            for y in np.linspace(-0.8, 0.8, 5):
                rr = R * np.sqrt(1 - y * y)
                g.add(Ellipse(width=2 * rr, height=0.35 * rr).move_to(c + UP * y * R).set_stroke(CYAN, 1.5, 0.45))
            return g

        sphere = always_redraw(globe)
        halo = glow(Circle(R).move_to(c), CYAN, 2, 4)
        orbit = DashedVMobject(Circle(R + 0.45).move_to(c), num_dashes=50).set_stroke(MUTED, 2)
        sat = Dot(c + RIGHT * (R + 0.45), radius=0.08, color=DL_C)
        sat.add_updater(lambda m, dt: m.rotate(1.2 * dt, about_point=c))
        orbit.add_updater(lambda m, dt: m.rotate(-0.15 * dt, about_point=c))

        self.play(FadeIn(halo), Create(orbit), FadeIn(sphere), run_time=0.8)
        self.add(sat)
        self.play(t0.animate.set_value(PI / 2), run_time=1.0, rate_func=linear)

        pre = T("GPT-3 learned", 32, MUTED, NORMAL).next_to(halo, DOWN, buff=0.75)
        n = ValueTracker(0)
        num = always_redraw(lambda: T(f"{int(n.get_value()):,}", 84, DL_C).next_to(pre, DOWN, buff=0.15))
        post = T("parameters (numbers it tuned while training)", 30, TXT, NORMAL)
        self.play(FadeIn(pre, shift=UP * 0.2), t0.animate.increment_value(PI / 4), run_time=0.5, rate_func=linear)
        self.add(num)
        self.play(n.animate.set_value(175_000_000_000), t0.animate.increment_value(PI * 1.2),
                  run_time=2.4, rate_func=rush_from)
        post.next_to(num, DOWN, buff=0.2)
        word = T("175 BILLION", 40, DL_C).next_to(post, DOWN, buff=0.25)
        self.play(FadeIn(post, shift=UP * 0.2), t0.animate.increment_value(PI / 3), run_time=0.6, rate_func=linear)
        self.play(FadeIn(word, scale=1.4), Flash(halo, color=DL_C, flash_radius=R + 0.2, num_lines=20),
                  t0.animate.increment_value(PI / 3), run_time=0.6, rate_func=linear)
        self.play(t0.animate.increment_value(PI), run_time=2.0, rate_func=linear)
