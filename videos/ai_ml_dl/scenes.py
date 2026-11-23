"""
AI vs ML vs DL - explainer animations for "AI with Mani".

Render one scene (1080p, 30fps):
    manim -r 1920,1080 --frame_rate 30 scenes.py NestedCircles
Render all:
    manim -r 1920,1080 --frame_rate 30 -a scenes.py
"""
from manim import *

BG = "#0B0F1A"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
TXT = "#E5E7EB"
MUTED = "#94A3B8"
FONT = "DejaVu Sans"

config.background_color = BG


def label(text, size=36, color=TXT, weight=NORMAL):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


class NestedCircles(Scene):
    """AI contains ML, ML contains DL - the core relationship."""

    def construct(self):
        title = label("AI  vs  ML  vs  DL", 56, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)

        ai = Circle(radius=3.0, color=AI_C, fill_opacity=0.12, stroke_width=6).shift(DOWN * 0.5)
        ml = Circle(radius=2.0, color=ML_C, fill_opacity=0.15, stroke_width=6).move_to(ai.get_center() + DOWN * 0.5)
        dl = Circle(radius=1.05, color=DL_C, fill_opacity=0.2, stroke_width=6).move_to(ml.get_center() + DOWN * 0.45)

        ai_t = label("Artificial Intelligence", 30, AI_C, BOLD).move_to(ai.get_top() + DOWN * 0.45)
        ml_t = label("Machine Learning", 28, ML_C, BOLD).move_to(ml.get_top() + DOWN * 0.4)
        dl_t = label("Deep\nLearning", 26, DL_C, BOLD).move_to(dl.get_center())

        self.play(DrawBorderThenFill(ai), FadeIn(ai_t, shift=DOWN * 0.2), run_time=1.2)
        self.wait(0.4)
        self.play(DrawBorderThenFill(ml), FadeIn(ml_t, shift=DOWN * 0.2), run_time=1.2)
        self.wait(0.4)
        self.play(DrawBorderThenFill(dl), FadeIn(dl_t, scale=0.8), run_time=1.2)
        self.wait(0.6)

        # side notes
        notes = VGroup(
            label("AI  - machines that act smart", 26, AI_C),
            label("ML  - learns patterns from data", 26, ML_C),
            label("DL  - ML using neural networks", 26, DL_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        diagram = VGroup(ai, ml, dl, ai_t, ml_t, dl_t)
        self.play(diagram.animate.scale(0.8).to_edge(LEFT, buff=0.6), run_time=1)
        notes.next_to(diagram, RIGHT, buff=0.7)
        for n in notes:
            self.play(FadeIn(n, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.5)

        key = label("Every DL is ML.  Every ML is AI.  Not the other way round!", 28, TXT, BOLD)
        key.to_edge(DOWN, buff=0.4)
        box = SurroundingRectangle(key, color=DL_C, buff=0.2, corner_radius=0.15)
        self.play(Write(key), Create(box), run_time=1.5)
        self.wait(2)


class RulesVsLearning(Scene):
    """Traditional programming vs Machine Learning - the key ML idea."""

    def make_row(self, inputs, output, out_color, y):
        boxes = VGroup()
        for text, color in inputs:
            r = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, color=color,
                                 fill_opacity=0.15, stroke_width=4)
            boxes.add(VGroup(r, label(text, 30, color, BOLD)))
        boxes.arrange(DOWN, buff=0.3)
        machine = RoundedRectangle(width=3.0, height=2.0, corner_radius=0.3, color=MUTED,
                                   fill_opacity=0.08, stroke_width=4)
        machine_t = label("Computer", 30, TXT)
        m = VGroup(machine, machine_t)
        out = VGroup(
            RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2, color=out_color,
                             fill_opacity=0.25, stroke_width=4),
            label(output, 30, out_color, BOLD),
        )
        row = VGroup(boxes, m, out).arrange(RIGHT, buff=1.0).move_to(UP * y)
        a1 = Arrow(boxes.get_right(), m.get_left(), buff=0.15, color=TXT)
        a2 = Arrow(m.get_right(), out.get_left(), buff=0.15, color=TXT)
        return boxes, m, out, a1, a2

    def construct(self):
        t1 = label("Traditional Programming", 34, AI_C, BOLD).to_edge(UP, buff=0.35)
        b, m, o, a1, a2 = self.make_row([("Rules", AI_C), ("Data", MUTED)], "Answers", TXT, 0.6)
        self.play(FadeIn(t1, shift=DOWN * 0.2))
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in b], lag_ratio=0.3))
        self.play(GrowArrow(a1), FadeIn(m))
        self.play(GrowArrow(a2), FadeIn(o, scale=0.8))
        hint = label("Human writes the rules  (if marks > 35 then pass)", 26, MUTED).to_edge(DOWN, buff=0.6)
        self.play(Write(hint))
        self.wait(2)

        group1 = VGroup(t1, b, m, o, a1, a2, hint)
        self.play(FadeOut(group1, shift=UP * 0.5))

        t2 = label("Machine Learning", 34, ML_C, BOLD).to_edge(UP, buff=0.35)
        b, m, o, a1, a2 = self.make_row([("Data", MUTED), ("Answers", TXT)], "Rules", ML_C, 0.6)
        self.play(FadeIn(t2, shift=DOWN * 0.2))
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in b], lag_ratio=0.3))
        self.play(GrowArrow(a1), FadeIn(m))
        self.play(Indicate(m[0], color=ML_C, scale_factor=1.08), run_time=1)
        self.play(GrowArrow(a2), FadeIn(o, scale=0.8))
        hint = label("Machine finds the rules itself from examples", 28, ML_C, BOLD).to_edge(DOWN, buff=0.6)
        box = SurroundingRectangle(hint, color=ML_C, buff=0.2, corner_radius=0.15)
        self.play(Write(hint), Create(box))
        self.wait(2.5)


class NeuralNetwork(Scene):
    """Deep Learning: a neural network with signals flowing through layers."""

    def construct(self):
        title = label("Deep Learning = many layers of neurons", 40, DL_C, BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1)

        sizes = [3, 5, 5, 5, 2]
        names = ["Input", "Hidden 1", "Hidden 2", "Hidden 3", "Output"]
        colors = [AI_C, DL_C, DL_C, DL_C, ML_C]
        layers = VGroup()
        for n, c in zip(sizes, colors):
            col = VGroup(*[Circle(radius=0.28, color=c, fill_opacity=0.25, stroke_width=4) for _ in range(n)])
            col.arrange(DOWN, buff=0.35)
            layers.add(col)
        layers.arrange(RIGHT, buff=1.7).shift(DOWN * 0.3)

        edges = VGroup()
        edge_layers = []
        for l1, l2 in zip(layers[:-1], layers[1:]):
            group = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=1.5,
                                  color=MUTED, stroke_opacity=0.35).set_z_index(-1)
                             for a in l1 for b in l2])
            edges.add(group)
            edge_layers.append(group)

        tags = VGroup(*[label(nm, 22, MUTED).next_to(layer, DOWN, buff=0.35)
                        for nm, layer in zip(names, layers)])

        self.play(LaggedStart(*[FadeIn(l, scale=0.7) for l in layers], lag_ratio=0.2), run_time=1.5)
        self.play(Create(edges), FadeIn(tags), run_time=1.5)

        in_t = label("cat photo", 24, AI_C).next_to(layers[0], LEFT, buff=0.4)
        self.play(FadeIn(in_t, shift=RIGHT * 0.2))

        for _ in range(2):
            for i, group in enumerate(edge_layers):
                pulses = [ShowPassingFlash(e.copy().set_stroke(DL_C, width=4, opacity=1), time_width=0.6)
                          for e in group]
                self.play(*pulses,
                          layers[i + 1].animate.set_fill(opacity=0.7),
                          run_time=0.45)
                self.play(layers[i + 1].animate.set_fill(opacity=0.25), run_time=0.1)

        out_t = label("Cat  97%", 28, ML_C, BOLD).next_to(layers[-1][0], RIGHT, buff=0.35)
        out_t2 = label("Dog   3%", 24, MUTED).next_to(layers[-1][1], RIGHT, buff=0.35)
        self.play(layers[-1][0].animate.set_fill(ML_C, opacity=0.9), FadeIn(out_t), FadeIn(out_t2))

        note = label("Each hidden layer learns features by itself: edges > shapes > ears, eyes", 24, TXT)
        note.to_edge(DOWN, buff=0.35)
        self.play(Write(note), run_time=1.5)
        self.wait(2.5)
