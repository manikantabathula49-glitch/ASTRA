"""
IT-style informational scenes for AI vs ML vs DL (original designs, styles
referenced from Pinterest: isometric servers, code typing, neon dashboards, glowing chips).

  manim -r 1920,1080 --frame_rate 30 it_scenes.py IsoPipeline
  manim -r 1920,1080 --frame_rate 30 it_scenes.py CodeVsData
  manim -r 1920,1080 --frame_rate 30 it_scenes.py NeonData
  manim -r 1920,1080 --frame_rate 30 it_scenes.py GpuChip
"""
import numpy as np
from manim import *

BG = "#070B14"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
CYAN = "#22D3EE"
PURPLE = "#A855F7"
PINK = "#EC4899"
TXT = "#F1F5F9"
MUTED = "#64748B"
SANS = "Inter"
MONO = "DejaVu Sans Mono"

config.background_color = BG


def T(s, size=32, color=TXT, weight=BOLD, font=SANS):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def glow(m, color, width=3, layers=4):
    g = VGroup()
    for i in range(layers, 0, -1):
        g.add(m.copy().set_stroke(color, width=width + i * 5, opacity=0.07).set_fill(opacity=0))
    g.add(m.copy().set_stroke(color, width=width, opacity=1))
    return g


def grid_bg(step=0.6, opacity=0.05):
    lines = VGroup()
    for x in np.arange(-7.2, 7.3, step):
        lines.add(Line([x, -4.1, 0], [x, 4.1, 0]))
    for y in np.arange(-4.2, 4.3, step):
        lines.add(Line([-7.2, y, 0], [7.2, y, 0]))
    return lines.set_stroke(CYAN, 1, opacity)


def title(s, color=CYAN):
    t = T(s, 40, TXT).to_edge(UP, buff=0.45)
    bar = Line(LEFT, RIGHT, color=color, stroke_width=4).set_width(min(t.width, 5)).next_to(t, DOWN, buff=0.15)
    return VGroup(t, bar)


# ---------------------------------------------------------------- isometric helpers
C30, S30 = np.cos(PI / 6), np.sin(PI / 6)


def iso(x, y, z):
    return np.array([(x - y) * C30, (x + y) * S30 + z, 0])


def iso_box(w, d, h, color, origin=ORIGIN, top_op=0.55):
    """Isometric box: footprint w x d, height h, sitting on `origin` (screen coords)."""
    o = np.array(origin)
    P = lambda x, y, z: o + iso(x - w / 2, y - d / 2, z)
    top = Polygon(P(0, 0, h), P(w, 0, h), P(w, d, h), P(0, d, h))
    left = Polygon(P(0, 0, 0), P(w, 0, 0), P(w, 0, h), P(0, 0, h))
    right = Polygon(P(0, 0, 0), P(0, d, 0), P(0, d, h), P(0, 0, h))
    top.set_fill(color, top_op).set_stroke(color, 2)
    left.set_fill(interpolate_color(ManimColor(color), ManimColor(BG), 0.45), 0.9).set_stroke(color, 2)
    right.set_fill(interpolate_color(ManimColor(color), ManimColor(BG), 0.7), 0.9).set_stroke(color, 2)
    return VGroup(left, right, top)


def top_center(w, d, h, origin):
    return np.array(origin) + iso(0, 0, h)


# ---------------------------------------------------------------- 1. ML pipeline, isometric
class IsoPipeline(Scene):
    def construct(self):
        self.add(grid_bg())
        hd = title("How an ML model is built")
        self.play(FadeIn(hd, shift=DOWN * 0.2), run_time=0.6)

        xs = np.linspace(-5.4, 5.4, 5)
        base_y = -0.6
        specs = [("1. Data", "collect lots|of examples", AI_C),
                 ("2. Clean", "fix errors,|remove junk", CYAN),
                 ("3. Train", "GPU finds|the patterns", DL_C),
                 ("4. Model", "the learned|rules", ML_C),
                 ("5. Use", "app makes|predictions", PURPLE)]

        stations = []
        # 1 database: three stacked slabs
        db = VGroup(*[iso_box(1.1, 1.1, 0.28, AI_C, [xs[0], base_y + i * 0.36, 0]) for i in range(3)])
        # 2 clean: slab + funnel-ish triangle
        cl = VGroup(iso_box(1.2, 1.2, 0.35, CYAN, [xs[1], base_y, 0]),
                    Triangle(color=CYAN, fill_opacity=0.35).scale(0.35).rotate(PI).move_to([xs[1], base_y + 0.95, 0]))
        # 3 train: tall server tower with lit stripes
        tw = iso_box(0.9, 0.9, 1.6, DL_C, [xs[2], base_y, 0], top_op=0.4)
        stripes = VGroup(*[Line(np.array([xs[2], base_y, 0]) + iso(-0.45, -0.3, z),
                                np.array([xs[2], base_y, 0]) + iso(0.35, -0.45, z)).set_stroke(DL_C, 3)
                           for z in (0.35, 0.7, 1.05, 1.4)])
        trn = VGroup(tw, stripes)
        # 4 model: cube with glowing dots on top
        cb = iso_box(1.1, 1.1, 1.0, ML_C, [xs[3], base_y, 0])
        tc = top_center(1.1, 1.1, 1.0, [xs[3], base_y, 0])
        dots = VGroup(*[Dot(tc + iso(dx, dy, 0), radius=0.06, color=TXT) for dx in (-0.3, 0, 0.3) for dy in (-0.3, 0.3)])
        mdl = VGroup(cb, dots)
        # 5 app: phone slab
        ph = iso_box(0.7, 0.12, 1.3, PURPLE, [xs[4], base_y, 0], top_op=0.8)
        scr = Polygon(*[np.array([xs[4], base_y, 0]) + iso(x - 0.35, -0.06, z)
                        for x, z in ((0.08, 0.15), (0.62, 0.15), (0.62, 1.15), (0.08, 1.15))])
        scr.set_fill(PURPLE, 0.25).set_stroke(TXT, 1.5)
        app = VGroup(ph, scr)
        objs = [db, cl, trn, mdl, app]

        labels = VGroup()
        for (name, sub, c), x in zip(specs, xs):
            subl = VGroup(*[T(part, 18, MUTED, NORMAL) for part in sub.split("|")]).arrange(DOWN, buff=0.06)
            g = VGroup(T(name, 26, c), subl).arrange(DOWN, buff=0.1).move_to([x, -2.45, 0])
            labels.add(g)

        # paths between stations
        path_y = base_y - 0.15
        paths = VGroup(*[DashedLine([xs[i] + 0.85, path_y, 0], [xs[i + 1] - 0.85, path_y, 0],
                                    dash_length=0.12).set_stroke(DL_C, 3) for i in range(4)])

        for i, (o, lab) in enumerate(zip(objs, labels)):
            if i:
                self.play(Create(paths[i - 1]), run_time=0.3)
            self.play(FadeIn(o, shift=UP * 0.4), FadeIn(lab, shift=UP * 0.2), run_time=0.5)
            self.wait(0.15)

        # data packets: messy before cleaning, uniform after
        rng = np.random.default_rng(1)
        for wave in range(3):
            pk = VGroup(*[Square(0.14 + rng.uniform(-0.05, 0.06), stroke_width=0,
                                 fill_color=rng.choice([MUTED, PINK, AI_C]), fill_opacity=1)
                          .rotate(rng.uniform(0, 1)).move_to([xs[0] + 0.85, path_y + rng.uniform(-0.1, 0.1), 0])
                          for _ in range(3)])
            self.add(pk)
            self.play(*[p.animate.move_to([xs[1] - 0.6, path_y, 0]) for p in pk], run_time=0.5,
                      lag_ratio=0.2)
            clean = VGroup(*[Square(0.14, stroke_width=0, fill_color=CYAN, fill_opacity=1)
                             .move_to([xs[1] + 0.85 + k * 0.22, path_y, 0]) for k in range(3)])
            self.remove(pk)
            self.add(clean)
            self.play(clean.animate.shift(RIGHT * (xs[2] - xs[1] - 1.9)),
                      stripes.animate.set_stroke(TXT if wave % 2 == 0 else DL_C), run_time=0.45)
            self.remove(clean)
        self.play(Indicate(trn, color=DL_C, scale_factor=1.05), run_time=0.5)
        out = VGroup(*[Dot(radius=0.08, color=ML_C).move_to([xs[2] + 0.85, path_y, 0]) for _ in range(2)])
        self.add(out)
        self.play(out[0].animate.move_to([xs[3] - 0.8, path_y, 0]), run_time=0.5)
        self.play(dots.animate.set_color(ML_C), Flash(tc, color=ML_C, flash_radius=0.6), run_time=0.4)
        self.play(out[1].animate.move_to([xs[4] - 0.6, path_y, 0]), run_time=0.5)
        pred = T("\"98% spam\"", 22, PURPLE).next_to(app, UP, buff=0.25)
        self.play(FadeIn(pred, shift=UP * 0.2), scr.animate.set_fill(PURPLE, 0.6), run_time=0.4)
        foot = T("In real projects, most of the time goes into steps 1 and 2: good data", 24, DL_C).to_edge(DOWN, buff=0.4)
        self.play(Write(foot), run_time=1.0)
        self.wait(2)


# ---------------------------------------------------------------- 2. code vs data
def editor(w, h, label, color):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color, stroke_width=2,
                             fill_color="#0D1424", fill_opacity=1)
    bar = Rectangle(width=w, height=0.45, stroke_width=0, fill_color="#111C30", fill_opacity=1)
    bar.align_to(frame, UP)
    dots = VGroup(*[Dot(radius=0.06, color=c) for c in ("#EF4444", "#F59E0B", "#22C55E")]).arrange(RIGHT, buff=0.12)
    dots.move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.25)
    lab = T(label, 18, MUTED, NORMAL).move_to(bar)
    return VGroup(frame, bar, dots, lab)


class CodeVsData(Scene):
    def construct(self):
        self.add(grid_bg())
        lt = T("Traditional programming", 30, AI_C).move_to([-3.6, 3.2, 0])
        rt = T("Machine Learning", 30, ML_C).move_to([3.6, 3.2, 0])
        le = editor(6.4, 4.4, "rules.py", AI_C).move_to([-3.6, 0.45, 0])
        re = editor(6.4, 4.4, "training data", ML_C).move_to([3.6, 0.45, 0])
        self.play(FadeIn(lt), FadeIn(rt), FadeIn(le), FadeIn(re), run_time=0.7)

        code = [(0, 'def result(marks):'), (1, 'if marks > 25:'), (2, 'return "PASS"'), (1, 'return "FAIL"')]
        lines = VGroup(*[Text(src, font=MONO, font_size=24, color=TXT,
                              t2c={"def": PURPLE, "if": PURPLE, "return": PURPLE, '"PASS"': ML_C, '"FAIL"': PINK})
                         for _, src in code])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(le[0]).align_to(le[0], LEFT).shift(RIGHT * 0.35 + DOWN * 0.2)
        for (lvl, _), ln in zip(code, lines):
            ln.shift(RIGHT * 0.55 * lvl)
        for ln in lines:
            self.play(AddTextLetterByLetter(ln), run_time=0.6)
        cap_l = T("A human writes every rule", 24, AI_C, NORMAL).next_to(le, DOWN, buff=0.3)
        self.play(FadeIn(cap_l, shift=UP * 0.2), run_time=0.4)

        rows = [("72", "PASS", ML_C), ("20", "FAIL", PINK), ("55", "PASS", ML_C), ("18", "FAIL", PINK),
                ("90", "PASS", ML_C), ("12", "FAIL", PINK)]
        data = VGroup(*[VGroup(T(f"marks: {m}", 22, TXT, NORMAL, MONO), T("→", 22, MUTED, NORMAL, MONO),
                               T(r, 22, c, BOLD, MONO)).arrange(RIGHT, buff=0.25) for m, r, c in rows])
        data.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(re[0]).align_to(re[0], LEFT).shift(RIGHT * 0.4 + DOWN * 0.15)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in data], lag_ratio=0.15), run_time=1.2)
        brain = VGroup(Circle(0.5, color=ML_C, fill_opacity=0.15), T("ML", 26, ML_C)).move_to(re[0].get_right() + LEFT * 1.1 + DOWN * 0.2)
        brain[1].move_to(brain[0])
        self.play(FadeIn(brain, scale=0.5), run_time=0.4)
        self.play(*[d.animate.scale(0.6).move_to(brain).set_opacity(0) for d in data], run_time=0.9, lag_ratio=0.1)
        self.play(Indicate(brain, color=ML_C), run_time=0.5)
        learned = VGroup(T("learned rule:", 22, MUTED, NORMAL, MONO),
                         T("marks > 25 → PASS", 26, ML_C, BOLD, MONO)).arrange(DOWN, buff=0.12)
        learned.move_to(re[0]).shift(LEFT * 0.6 + DOWN * 0.2)
        box = glow(SurroundingRectangle(learned, buff=0.2, corner_radius=0.12), ML_C, 2, 3)
        self.play(FadeIn(learned, shift=UP * 0.2), Create(box), run_time=0.6)
        cap_r = T("The machine finds the rule from examples", 24, ML_C, NORMAL).next_to(re, DOWN, buff=0.3)
        self.play(FadeIn(cap_r, shift=UP * 0.2), run_time=0.4)
        foot = T("Faces, voices, languages: nobody can write those rules. So we use ML.", 26, DL_C)
        foot.to_edge(DOWN, buff=0.35)
        self.play(Write(foot), run_time=1.2)
        self.wait(2)


# ---------------------------------------------------------------- 3. neon data needs
class NeonData(Scene):
    def construct(self):
        self.add(grid_bg(opacity=0.04))
        # faint neon line chart in the background
        rng = np.random.default_rng(3)
        for col, off in ((PINK, 0.0), (CYAN, 1.2), (PURPLE, 2.4)):
            ys = np.cumsum(rng.normal(0, 0.18, 40)) + off - 2
            pts = [[-7 + i * 14 / 39, y, 0] for i, y in enumerate(ys)]
            self.add(VMobject().set_points_smoothly(pts).set_stroke(col, 2, 0.12))
        hd = title("How much data does each one need?", PINK)
        self.play(FadeIn(hd, shift=DOWN * 0.2), run_time=0.6)

        rows = [("Rule-based AI", AI_C, 0.25, "0", "no examples, humans write rules"),
                ("Machine Learning", ML_C, 0.5, "1,000s", "thousands of examples"),
                ("Deep Learning", DL_C, 1.0, "1,000,000s", "millions of examples")]
        maxw = 7.0
        y0 = 1.3
        for i, (name, c, frac, num, sub) in enumerate(rows):
            y = y0 - i * 1.55
            lab = T(name, 28, c).move_to([-4.95, y + 0.18, 0])
            sl = T(sub, 17, MUTED, NORMAL).next_to(lab, DOWN, buff=0.08)
            track = Rectangle(width=maxw, height=0.42, stroke_width=0,
                              fill_color=MUTED, fill_opacity=0.15).move_to([0.75, y, 0])
            w = max(0.3, maxw * frac)
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.95)
            bar.align_to(track, LEFT).set_y(y)
            halo = Rectangle(width=w, height=0.8, stroke_width=0, fill_color=c, fill_opacity=0.15)
            halo.align_to(track, LEFT).set_y(y)
            self.play(FadeIn(lab, shift=RIGHT * 0.2), FadeIn(sl), FadeIn(track), run_time=0.4)
            nlab = T(num, 30, c).next_to(track, RIGHT, buff=0.3)
            self.play(GrowFromEdge(bar, LEFT), GrowFromEdge(halo, LEFT),
                      FadeIn(nlab, shift=LEFT * 0.2), run_time=0.9, rate_func=smooth)
            self.wait(0.3)
        note = T("More data → Deep Learning keeps improving. Small data → classic ML is often better.", 24, TXT, NORMAL)
        note.to_edge(DOWN, buff=0.75)
        tiny = T("Typical scale; the real amount depends on the task", 16, MUTED, NORMAL).next_to(note, DOWN, buff=0.15)
        self.play(Write(note), FadeIn(tiny), run_time=1.2)
        self.wait(2)


# ---------------------------------------------------------------- 4. GPU chip
class GpuChip(Scene):
    def construct(self):
        self.add(grid_bg(opacity=0.04))
        c = LEFT * 2.2 + DOWN * 0.2
        # circuit traces radiating out
        rng = np.random.default_rng(8)
        traces = VGroup()
        for side in (UP, DOWN, LEFT, RIGHT):
            for k in np.linspace(-1.2, 1.2, 6):
                perp = np.array([side[1], side[0], 0])
                start = c + side * 1.6 + perp * k
                mid = start + side * rng.uniform(0.5, 1.1)
                end = mid + perp * rng.choice([-0.5, 0.5]) + side * rng.uniform(0.4, 0.9)
                traces.add(VMobject().set_points_as_corners([start, mid, end]).set_stroke(CYAN, 2, 0.45))
                traces.add(Dot(end, radius=0.05, color=CYAN).set_opacity(0.6))
        chip = RoundedRectangle(width=3.2, height=3.2, corner_radius=0.2, stroke_color=CYAN, stroke_width=3,
                                fill_color="#0D1424", fill_opacity=1).move_to(c)
        pins = VGroup()
        for side in (UP, DOWN, LEFT, RIGHT):
            perp = np.array([side[1], side[0], 0])
            for k in np.linspace(-1.3, 1.3, 10):
                pins.add(Line(c + side * 1.6 + perp * k, c + side * 1.78 + perp * k).set_stroke(MUTED, 3))
        cores = VGroup(*[Square(0.12, stroke_width=0, fill_color=CYAN, fill_opacity=0.15) for _ in range(196)])
        cores.arrange_in_grid(14, 14, buff=0.045).move_to(c + DOWN * 0.22)
        lab = T("GPU", 26, CYAN).move_to(c + UP * 1.3)

        self.play(Create(traces), run_time=1.0)
        self.play(FadeIn(chip), FadeIn(pins), FadeIn(lab), run_time=0.5)
        self.play(FadeIn(cores, lag_ratio=0.002), run_time=0.6)

        info = VGroup(
            VGroup(T("CPU", 30, AI_C), T("a few big cores (8–24 in most PCs)", 24, TXT, NORMAL),
                   T("one task after another", 20, MUTED, NORMAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(T("GPU", 30, CYAN), T("thousands of small cores", 24, TXT, NORMAL),
                   T("all working at the same time", 20, MUTED, NORMAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([4.2, 0.6, 0])
        self.play(FadeIn(info[0], shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(info[1], shift=LEFT * 0.2), run_time=0.5)

        # waves of parallel work
        for wave in range(3):
            self.play(cores.animate.set_fill(CYAN, 0.95),
                      *[ShowPassingFlash(t.copy().set_stroke(CYAN, 4, 1), time_width=0.5)
                        for t in traces if isinstance(t, VMobject) and not isinstance(t, Dot)],
                      run_time=0.45)
            self.play(cores.animate.set_fill(CYAN, 0.15), run_time=0.3)
        mult = T("1 neural network step = millions of multiplications", 24, DL_C).move_to([4.2, -1.6, 0])
        if mult.width > 5.6:
            mult.scale_to_fit_width(5.6)
        mult2 = T("GPU does them in parallel → training is many times faster", 22, TXT, NORMAL).next_to(mult, DOWN, buff=0.15)
        if mult2.width > 5.6:
            mult2.scale_to_fit_width(5.6)
        self.play(Write(mult), run_time=0.8)
        self.play(FadeIn(mult2, shift=UP * 0.2), cores.animate.set_fill(ML_C, 0.9), run_time=0.6)
        self.wait(2)
