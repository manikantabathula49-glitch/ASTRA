"""
AI vs ML vs DL - 80 explainer clips for "AI with Mani" (Chapters 2-7).

Every clip is a Manim scene named C<NN>_<slug>. Render with render_all.sh,
or a single one:
    manim -r 1920,1080 --frame_rate 30 clips.py C02_ai_ml_dl_circles
"""
import textwrap

import numpy as np
from manim import *

# ---------------------------------------------------------------- style
BG = "#0B0F1A"
PANEL = "#131A2A"
AI_C = "#4F8CFF"
ML_C = "#22C55E"
DL_C = "#F59E0B"
BAD = "#EF4444"
TXT = "#E5E7EB"
MUTED = "#94A3B8"
FONT = "DejaVu Sans"

config.background_color = BG

CH_NAMES = {2: "The Big Picture", 3: "How ML Learns", 4: "Types of ML",
            5: "ML Algorithms", 6: "Deep Learning", 7: "Final Revision"}
CH_COL = {2: AI_C, 3: ML_C, 4: ML_C, 5: ML_C, 6: DL_C, 7: AI_C}


# ---------------------------------------------------------------- helpers
def T(s, size=32, color=TXT, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def P(s, width=40, size=32, color=TXT, weight=NORMAL, align="center"):
    lines = textwrap.wrap(s, width, break_long_words=False) or [""]
    if len(lines) == 1:
        return T(lines[0], size, color, weight)
    g = VGroup(*[T(ln, size, color, weight) for ln in lines])
    return g.arrange(DOWN, buff=0.14 * size / 32, aligned_edge=LEFT if align == "left" else ORIGIN)


def fit(m, w=12.8, h=None):
    if m.width > w:
        m.scale_to_fit_width(w)
    if h is not None and m.height > h:
        m.scale_to_fit_height(h)
    return m


def card(text, color, w, h, size=26, wrap=16, tcolor=TXT, fill=0.15):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color,
                         fill_color=color, fill_opacity=fill, stroke_width=3)
    t = fit(P(text, wrap, size, tcolor, BOLD), w - 0.3, h - 0.2).move_to(r)
    return VGroup(r, t)


def chrome(s, ch):
    s.add(T("AI with Mani", 18, MUTED).set_opacity(0.6).to_corner(DR, buff=0.15))
    if ch:
        s.add(T(f"CH {ch} · {CH_NAMES[ch]}", 18, CH_COL[ch]).set_opacity(0.8).to_corner(DL, buff=0.15))


def header(s, title, color=TXT):
    t = fit(T(title, 40, color, BOLD), 11.5).to_edge(UP, buff=0.6)
    u = Line(LEFT, RIGHT, color=color, stroke_width=4).set_width(min(t.width, 6))
    u.next_to(t, DOWN, buff=0.15)
    s.play(FadeIn(t, shift=DOWN * 0.2), Create(u), run_time=0.8)
    return VGroup(t, u)


def footer(s, text, color=DL_C):
    t = fit(P(text, 64, 28, TXT, BOLD), 12).to_edge(DOWN, buff=0.6)
    b = SurroundingRectangle(t, color=color, buff=0.2, corner_radius=0.15)
    s.play(Write(t), Create(b), run_time=1.2)
    return VGroup(t, b)


def arrow(a, b, color=MUTED):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=4,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=10)


def flow_row(steps, total_w=12.6, h=1.3, size=24, gap=0.6):
    n = len(steps)
    w = min(2.9, (total_w - (n - 1) * gap) / n)
    boxes = VGroup(*[card(t, c, w, h, size, max(8, int(w * 5.5))) for t, c in steps])
    boxes.arrange(RIGHT, buff=gap)
    arrows = VGroup(*[arrow(a.get_right(), b.get_left()) for a, b in zip(boxes[:-1], boxes[1:])])
    return boxes, arrows


def make_net(sizes, colors, center=ORIGIN, xbuf=1.7, r=0.28, ybuf=0.35):
    layers = VGroup()
    for n, c in zip(sizes, colors):
        col = VGroup(*[Circle(radius=r, color=c, fill_opacity=0.25, stroke_width=4)
                       for _ in range(n)]).arrange(DOWN, buff=ybuf)
        layers.add(col)
    layers.arrange(RIGHT, buff=xbuf).move_to(center)
    edges = [VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=1.5, color=MUTED,
                           stroke_opacity=0.35).set_z_index(-1) for a in l1 for b in l2])
             for l1, l2 in zip(layers[:-1], layers[1:])]
    return layers, edges


def pulse(group, color, reverse=False):
    out = []
    for e in group:
        ln = Line(e.get_end(), e.get_start()) if reverse else e.copy()
        ln.set_stroke(color, width=4, opacity=1)
        out.append(ShowPassingFlash(ln, time_width=0.6))
    return out


def xmark(color, s=0.18):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])).set_stroke(color, 7)


def build_table(headers, rows, colw, hcolors, size=24):
    data = [headers] + rows
    texts = []
    for r, row in enumerate(data):
        tr = []
        for j, cell in enumerate(row):
            col = hcolors[j] if r == 0 else (TXT if j else MUTED)
            t = P(cell, max(8, int(colw[j] * 4.6)), size, col, BOLD if r == 0 or j == 0 else NORMAL)
            tr.append(fit(t, colw[j] - 0.25))
        texts.append(tr)
    heights = [max(t.height for t in tr) + 0.35 for tr in texts]
    row_groups, cells = VGroup(), []
    y = 0
    for r, tr in enumerate(texts):
        x = 0
        rg, rc = VGroup(), []
        for j, t in enumerate(tr):
            rect = Rectangle(width=colw[j], height=heights[r], stroke_color=MUTED, stroke_width=1.5,
                             stroke_opacity=0.5, fill_color=PANEL if r == 0 else BG, fill_opacity=1)
            rect.move_to([x + colw[j] / 2, y - heights[r] / 2, 0])
            t.move_to(rect)
            c = VGroup(rect, t)
            rg.add(c)
            rc.append(c)
            x += colw[j]
        row_groups.add(rg)
        cells.append(rc)
        y -= heights[r]
    return row_groups, cells


# ---------------------------------------------------------------- templates
def chapter_card(s, num, title, sub):
    c = CH_COL[num]
    n = T(f"CHAPTER {num}", 30, c, BOLD)
    bar = Line(LEFT * 3, RIGHT * 3, color=c, stroke_width=6)
    t = fit(T(title, 64, TXT, BOLD), 12.5)
    sb = fit(T(sub, 30, MUTED), 12)
    g = VGroup(n, bar, t, sb).arrange(DOWN, buff=0.4)
    glow = Circle(radius=3.6, stroke_width=0, fill_color=c, fill_opacity=0.07).move_to(g)
    s.play(FadeIn(glow, scale=0.6), FadeIn(n, shift=DOWN * 0.3), run_time=0.8)
    s.play(GrowFromCenter(bar), run_time=0.6)
    s.play(Write(t), run_time=1.2)
    s.play(FadeIn(sb, shift=UP * 0.2), run_time=0.7)
    s.wait(2.5)


def bullets(s, title, items, color=TXT, foot=None):
    h = header(s, title, color)
    rows = VGroup()
    for it in items:
        txt, c = it if isinstance(it, tuple) else (it, TXT)
        t = P(txt, 50, 30, c, align="left")
        d = Dot(radius=0.09, color=color if c == TXT else c)
        row = VGroup(d, t).arrange(RIGHT, buff=0.3)
        d.align_to(t, UP).shift(DOWN * 0.12)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    fit(rows, 12.4, 4.4 if foot else 5.2)
    rows.next_to(h, DOWN, buff=0.6).set_x(0)
    for r in rows:
        s.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.6)
        s.wait(0.8)
    if foot:
        footer(s, foot, color if color != TXT else DL_C)
    s.wait(2)


def definition(s, term, color, text, example=None, tip=None):
    parts = [T("DEFINITION", 22, MUTED, BOLD), fit(T(term, 58, color, BOLD), 12),
             fit(P(text, 46, 32, TXT), 12.4)]
    if example:
        parts.append(fit(P("Example: " + example, 60, 26, MUTED), 12.4))
    g = VGroup(*parts).arrange(DOWN, buff=0.4)
    fit(g, 12.8, 4.8 if tip else 6.4)
    if tip:
        g.to_edge(UP, buff=0.8)
    else:
        g.move_to(ORIGIN)
    s.play(FadeIn(parts[0]), FadeIn(parts[1], scale=0.85), run_time=0.9)
    s.play(Write(parts[2]), run_time=1.8)
    s.wait(0.8)
    if example:
        s.play(FadeIn(parts[3], shift=UP * 0.2), run_time=0.7)
        s.wait(0.8)
    if tip:
        lab = card("EXAM TIP", DL_C, 2.3, 0.6, 22, 12, fill=0.4)
        tt = fit(P(tip, 52, 26, TXT), 9.6)
        tg = VGroup(lab, tt).arrange(RIGHT, buff=0.35)
        tb = SurroundingRectangle(tg, color=DL_C, buff=0.22, corner_radius=0.15)
        VGroup(tg, tb).to_edge(DOWN, buff=0.6)
        s.play(FadeIn(tg, shift=UP * 0.2), Create(tb), run_time=1)
    s.wait(2.5)


def compare(s, title, left, right, color=TXT, foot=None):
    h = header(s, title, color)
    cols = []
    for head, c, items in (left, right):
        hd = card(head, c, 5.4, 0.9, 30, 30, fill=0.3)
        its = VGroup(*[P("• " + i, 32, 26, TXT, align="left") for i in items])
        its.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(its, 5.2)
        col = VGroup(hd, its).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        its.shift(RIGHT * 0.15)
        cols.append(col)
    L, R = cols
    both = VGroup(L, R).arrange(RIGHT, buff=1.6, aligned_edge=UP)
    fit(both, 12.6, 4.3 if foot else 5.2)
    both.next_to(h, DOWN, buff=0.5).set_x(0)
    mid = (L.get_right()[0] + R.get_left()[0]) / 2
    div = DashedLine([mid, L[0].get_bottom()[1], 0], [mid, both.get_bottom()[1], 0],
                     color=MUTED, stroke_width=2)
    vs = VGroup(Circle(0.42, color=MUTED, fill_color=BG, fill_opacity=1), T("VS", 22, TXT, BOLD))
    vs.move_to([mid, L[0].get_center()[1], 0])
    s.play(FadeIn(L[0], shift=RIGHT * 0.3), FadeIn(R[0], shift=LEFT * 0.3), run_time=0.8)
    s.play(GrowFromCenter(vs), Create(div), run_time=0.6)
    for a, b in zip(L[1], R[1]):
        s.play(FadeIn(a, shift=UP * 0.15), run_time=0.5)
        s.play(FadeIn(b, shift=UP * 0.15), run_time=0.5)
        s.wait(0.6)
    for extra in list(L[1][len(R[1]):]) + list(R[1][len(L[1]):]):
        s.play(FadeIn(extra), run_time=0.5)
    if foot:
        footer(s, foot, color if color != TXT else DL_C)
    s.wait(2)


def flow(s, title, steps, color=TXT, note=None, loop=False):
    h = header(s, title, color)
    boxes, arrows = flow_row(steps)
    VGroup(boxes, arrows).move_to(UP * 0.4)
    for i, b in enumerate(boxes):
        if i:
            s.play(GrowArrow(arrows[i - 1]), run_time=0.4)
        s.play(FadeIn(b, scale=0.85), run_time=0.5)
        s.wait(0.4)
    if loop:
        back = CurvedArrow(boxes[-1].get_bottom() + DOWN * 0.1, boxes[0].get_bottom() + DOWN * 0.1,
                           angle=-PI / 3, color=DL_C, stroke_width=4)
        lab = T("repeat", 24, DL_C, BOLD).next_to(back, DOWN, buff=0.1)
        s.play(Create(back), FadeIn(lab), run_time=1)
    path = VMobject().set_points_as_corners([b.get_center() for b in boxes])
    dot = Dot(radius=0.12, color=DL_C).move_to(boxes[0])
    s.play(FadeIn(dot))
    s.play(MoveAlongPath(dot, path), run_time=2, rate_func=linear)
    s.play(Indicate(boxes[-1], color=DL_C), FadeOut(dot))
    if note:
        footer(s, note, color if color != TXT else DL_C)
    s.wait(2)


def quiz(s, q, options, answer, explain=None):
    tag = card("QUICK QUIZ", DL_C, 3.2, 0.7, 24, 20, fill=0.4).to_edge(UP, buff=0.55)
    qt = fit(P(q, 44, 36, TXT, BOLD), 12.4).next_to(tag, DOWN, buff=0.45)
    opts = VGroup(*[card(f"{L})  {o}", AI_C, 5.9, 1.0, 26, 36, fill=0.1)
                    for L, o in zip("ABCD", options)])
    opts.arrange_in_grid(2, 2, buff=(0.4, 0.35))
    fit(opts, 12.6).next_to(qt, DOWN, buff=0.55)
    ring = Circle(0.38, color=DL_C, stroke_width=5).next_to(tag, RIGHT, buff=0.5)
    num = T("3", 32, DL_C, BOLD).move_to(ring)
    s.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.6)
    s.play(Write(qt), run_time=1.4)
    s.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in opts], lag_ratio=0.25), run_time=1.6)
    s.play(Create(ring), FadeIn(num), run_time=0.5)
    for k in "21":
        s.wait(0.7)
        s.play(Transform(num, T(k, 32, DL_C, BOLD).move_to(ring)), run_time=0.3)
    s.wait(0.7)
    right = opts[answer]
    tick = VGroup(Circle(0.26, stroke_width=0, fill_color=ML_C, fill_opacity=1), T("✓", 30, BG, BOLD))
    tick.move_to(right.get_corner(UR))
    s.play(FadeOut(ring), FadeOut(num),
           right[0].animate.set_fill(ML_C, 0.35).set_stroke(ML_C),
           *[o.animate.fade(0.65) for i, o in enumerate(opts) if i != answer], run_time=0.8)
    s.play(FadeIn(tick, scale=1.5), Indicate(right, color=ML_C, scale_factor=1.05))
    if explain:
        e = fit(P(explain, 64, 26, ML_C), 12.4).to_edge(DOWN, buff=0.6)
        s.play(FadeIn(e, shift=UP * 0.2))
    s.wait(2.5)


def timeline(s, title, events, color=TXT):
    h = header(s, title, color)
    n = len(events)
    xs = np.linspace(-6, 6, n)
    y0 = -0.3
    line = Line([-6.6, y0, 0], [6.6, y0, 0], color=MUTED, stroke_width=4)
    s.play(Create(line), run_time=0.8)
    for i, (yr, txt, c) in enumerate(events):
        dot = Dot([xs[i], y0, 0], radius=0.13, color=c)
        g = VGroup(T(yr, 26, c, BOLD), fit(P(txt, 14, 20, TXT), 3.0)).arrange(DOWN, buff=0.12)
        if i % 2 == 0:
            g.next_to(dot, UP, buff=0.5)
            stem = Line(dot.get_center(), g.get_bottom() + DOWN * 0.08, color=c, stroke_width=2)
        else:
            g[0], g[1]  # same order below the line
            g.next_to(dot, DOWN, buff=0.5)
            stem = Line(dot.get_center(), g.get_top() + UP * 0.08, color=c, stroke_width=2)
        s.play(GrowFromCenter(dot), Create(stem), FadeIn(g, shift=(UP if i % 2 == 0 else DOWN) * 0.2),
               run_time=0.6)
        s.wait(0.5)
    s.wait(2)


def table(s, title, headers, rows, hcolors=None, colw=None, color=TXT, foot=None, size=24):
    h = header(s, title, color)
    n = len(headers)
    hcolors = hcolors or [TXT] * n
    if colw is None:
        colw = [2.8] + [(12.8 - 2.8) / (n - 1)] * (n - 1)
    rg, _ = build_table(headers, rows, colw, hcolors, size)
    fit(rg, 12.8, 4.6 if foot else 5.4)
    rg.next_to(h, DOWN, buff=0.45).set_x(0)
    s.play(FadeIn(rg[0], shift=DOWN * 0.15), run_time=0.6)
    for r in rg[1:]:
        s.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
        s.wait(0.9)
    if foot:
        footer(s, foot, color if color != TXT else DL_C)
    s.wait(2.5)


def mapping(s, title, buckets, items, color=TXT, foot=None):
    h = header(s, title, color)
    nb = len(buckets)
    bw = min(3.8, (12.6 - (nb - 1) * 0.4) / nb)
    bins = VGroup()
    for name, c in buckets:
        r = RoundedRectangle(width=bw, height=3.3, corner_radius=0.2, stroke_color=c,
                             fill_color=c, fill_opacity=0.06, stroke_width=3)
        lab = fit(T(name, 26, c, BOLD), bw - 0.3).move_to(r.get_top() + DOWN * 0.38)
        bins.add(VGroup(r, lab))
    bins.arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.85 if foot else 0.5)
    s.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bins], lag_ratio=0.2), run_time=1)
    count = [0] * nb
    spawn = (h.get_bottom()[1] + bins.get_top()[1]) / 2
    for text, k in items:
        c = card(text, MUTED, bw - 0.3, 0.62, 22, 30, fill=0.12).move_to([0, spawn, 0])
        s.play(FadeIn(c, scale=0.8), run_time=0.5)
        s.wait(0.6)
        target = bins[k][0].get_top() + DOWN * (1.05 + 0.72 * count[k])
        count[k] += 1
        s.play(c.animate.move_to(target), c[0].animate.set_stroke(buckets[k][1]).move_to(target),
               run_time=0.7)
        s.wait(0.3)
    if foot:
        t = fit(P(foot, 70, 24, DL_C, BOLD), 12.4).to_edge(DOWN, buff=0.22)
        s.play(FadeIn(t))
    s.wait(2.5)


# ---------------------------------------------------------------- custom scenes
def nested_circles(s, title="AI  vs  ML  vs  DL"):
    t = T(title, 50, TXT, BOLD).to_edge(UP, buff=0.55)
    s.play(Write(t), run_time=1)
    ai = Circle(radius=3.0, color=AI_C, fill_opacity=0.12, stroke_width=6).shift(DOWN * 0.5)
    ml = Circle(radius=2.0, color=ML_C, fill_opacity=0.15, stroke_width=6).move_to(ai.get_center() + DOWN * 0.5)
    dl = Circle(radius=1.05, color=DL_C, fill_opacity=0.2, stroke_width=6).move_to(ml.get_center() + DOWN * 0.45)
    ai_t = T("Artificial Intelligence", 22, AI_C, BOLD).move_to(ai.get_top() + DOWN * 0.6)
    ml_t = T("Machine Learning", 21, ML_C, BOLD).move_to(ml.get_top() + DOWN * 0.55)
    dl_t = Paragraph("Deep", "Learning", font=FONT, font_size=24, color=DL_C, weight=BOLD,
                     alignment="center").move_to(dl)
    for circ, lab in ((ai, ai_t), (ml, ml_t), (dl, dl_t)):
        s.play(DrawBorderThenFill(circ), FadeIn(lab, shift=DOWN * 0.2), run_time=1.1)
        s.wait(0.4)
    notes = VGroup(T("AI  - machines that act smart", 26, AI_C),
                   T("ML  - learns patterns from data", 26, ML_C),
                   T("DL  - ML using deep neural networks", 26, DL_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    diagram = VGroup(ai, ml, dl, ai_t, ml_t, dl_t)
    s.play(diagram.animate.scale(0.8).to_edge(LEFT, buff=0.6), run_time=1)
    notes.next_to(diagram, RIGHT, buff=0.6)
    fit(notes, 13.4 - diagram.get_right()[0] - 6.7)
    notes.next_to(diagram, RIGHT, buff=0.6)
    for n in notes:
        s.play(FadeIn(n, shift=RIGHT * 0.3), run_time=0.6)
        s.wait(0.5)
    footer(s, "Every DL is ML. Every ML is AI. Not the other way round!", DL_C)
    s.wait(2)


def rules_vs_learning(s):
    def row(inputs, output, out_color):
        boxes = VGroup(*[card(t, c, 2.6, 1.0, 30, 12) for t, c in inputs]).arrange(DOWN, buff=0.3)
        m = card("Computer", MUTED, 3.0, 2.0, 30, 12, fill=0.08)
        o = card(output, out_color, 2.6, 1.0, 30, 12, fill=0.25)
        g = VGroup(boxes, m, o).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        return boxes, m, o, arrow(boxes.get_right(), m.get_left(), TXT), arrow(m.get_right(), o.get_left(), TXT)

    for title, col, ins, out, oc, hint in (
            ("Traditional Programming", AI_C, [("Rules", AI_C), ("Data", MUTED)], "Answers", TXT,
             "Human writes the rules  (if marks > 35 then PASS)"),
            ("Machine Learning", ML_C, [("Data", MUTED), ("Answers", TXT)], "Rules", ML_C,
             "Machine finds the rules itself from examples")):
        t = T(title, 40, col, BOLD).to_edge(UP, buff=0.6)
        b, m, o, a1, a2 = row(ins, out, oc)
        s.play(FadeIn(t, shift=DOWN * 0.2))
        s.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in b], lag_ratio=0.3))
        s.play(GrowArrow(a1), FadeIn(m))
        s.play(Indicate(m[0], color=col, scale_factor=1.06))
        s.play(GrowArrow(a2), FadeIn(o, scale=0.8))
        f = footer(s, hint, col)
        s.wait(2)
        if col == AI_C:
            s.play(FadeOut(VGroup(t, b, m, o, a1, a2, f), shift=UP * 0.5))
    s.wait(0.5)


def dataset_table(s):
    h = header(s, "A Dataset: House Prices", ML_C)
    headers = ["Size (sq ft)", "Bedrooms", "Location", "Price (lakh)"]
    rows = [["1000", "2", "City", "45"], ["1500", "3", "City", "68"], ["800", "2", "Village", "22"],
            ["2000", "4", "City", "95"], ["1200", "3", "Town", "40"], ["1300", "3", "City", "?"]]
    rg, cells = build_table(headers, rows, [3.0] * 4, [AI_C, AI_C, AI_C, ML_C], 26)
    fit(rg, 12, 4.4).next_to(h, DOWN, buff=0.4).set_x(0)
    s.play(FadeIn(rg[0]))
    s.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rg[1:6]], lag_ratio=0.25), run_time=1.6)
    feat = SurroundingRectangle(VGroup(*[cells[r][j] for r in range(6) for j in range(3)]),
                                color=AI_C, buff=0.06, stroke_width=5)
    lab = VGroup(SurroundingRectangle(VGroup(*[cells[r][3] for r in range(6)]),
                                      color=ML_C, buff=0.06, stroke_width=5))
    ft = T("FEATURES (inputs / clues)", 24, AI_C, BOLD).to_edge(DOWN, buff=0.6).set_x(-2.5)
    lt = T("LABEL (answer)", 24, ML_C, BOLD).to_edge(DOWN, buff=0.6).set_x(3.6)
    s.play(Create(feat), FadeIn(ft), run_time=0.8)
    s.wait(0.6)
    s.play(Create(lab), FadeIn(lt), run_time=0.8)
    s.wait(0.8)
    s.play(FadeOut(feat), FadeOut(lab), FadeOut(ft), FadeOut(lt))
    s.play(FadeIn(rg[6], shift=UP * 0.1))
    q = cells[6][3][1]
    s.play(q.animate.set_color(DL_C).scale(1.4))
    s.play(Indicate(q, color=DL_C))
    ans = T("≈ 58", 26, DL_C, BOLD).move_to(cells[6][3][0])
    s.play(Transform(q, ans))
    s.play(FadeIn(T("New house → model predicts the price!", 26, DL_C, BOLD).to_edge(DOWN, buff=0.6)))
    s.wait(2.5)


def train_test_split(s):
    h = header(s, "Split the Data: Train vs Test", ML_C)
    sq = VGroup(*[Square(0.28, stroke_width=1, stroke_color=BG, fill_color=MUTED, fill_opacity=0.8)
                  for _ in range(100)]).arrange_in_grid(10, 10, buff=0.08).move_to(UP * 0.15)
    s.play(LaggedStart(*[FadeIn(x) for x in sq], lag_ratio=0.01), run_time=1.5)
    s.wait(0.5)
    train = VGroup(*[x for i, x in enumerate(sq) if i % 10 < 8])
    test = VGroup(*[x for i, x in enumerate(sq) if i % 10 >= 8])
    s.play(train.animate.set_fill(ML_C), test.animate.set_fill(DL_C), run_time=1)
    s.play(test.animate.shift(RIGHT * 0.9), run_time=0.8)
    b1 = Brace(train, DOWN, color=ML_C)
    t1 = T("80% Training: model learns", 24, ML_C, BOLD).next_to(b1, DOWN, buff=0.1)
    t2 = Paragraph("20% Testing:", "the final exam", font=FONT, font_size=24, color=DL_C,
                   weight=BOLD).next_to(test, RIGHT, buff=0.4)
    s.play(GrowFromCenter(b1), FadeIn(t1))
    s.wait(0.6)
    s.play(FadeIn(t2, shift=LEFT * 0.2))
    s.wait(0.8)
    footer(s, "Never test the model on data it has already seen!", DL_C)
    s.wait(2)


def regression_fit(s):
    h = header(s, "Linear Regression: find the best line", ML_C)
    ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=7, y_length=4.6,
              axis_config={"color": MUTED, "include_tip": False}).shift(LEFT * 2 + DOWN * 0.6)
    xl = T("House size", 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
    yl = T("Price", 22, MUTED).next_to(ax.y_axis, UP, buff=0.15)
    rng = np.random.default_rng(3)
    xs = np.linspace(1, 9, 12)
    ys = np.clip(0.8 * xs + 1 + rng.normal(0, 0.7, 12), 0.4, 9.6)
    m, c = np.polyfit(xs, ys, 1)
    dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=AI_C) for x, y in zip(xs, ys)])
    mt, ct = ValueTracker(-0.3), ValueTracker(6)
    f = lambda x: mt.get_value() * x + ct.get_value()
    line = always_redraw(lambda: ax.plot(f, x_range=[0, 10], color=DL_C, stroke_width=5))
    errs = always_redraw(lambda: VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, f(x)), color=BAD, stroke_width=2.5)
                                          for x, y in zip(xs, ys)]))
    total = lambda: float(np.sum(np.abs(ys - (mt.get_value() * xs + ct.get_value()))))
    panel_t = T("Total error", 26, MUTED).move_to([4.4, 1.2, 0])
    val = always_redraw(lambda: T(f"{total():.1f}", 54, BAD, BOLD).move_to([4.4, 0.3, 0]))
    form = T("y = m·x + c", 32, DL_C, BOLD).move_to([4.4, -1.0, 0])
    s.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1)
    s.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.08), run_time=1.2)
    s.play(Create(line), FadeIn(form))
    s.play(FadeIn(errs), FadeIn(panel_t), FadeIn(val))
    s.wait(0.6)
    s.play(mt.animate.set_value(0.25), ct.animate.set_value(3.5), run_time=1.8)
    s.play(mt.animate.set_value(m), ct.animate.set_value(c), run_time=2)
    best = T("Best fit = smallest error", 28, ML_C, BOLD).move_to([4.4, -2.0, 0])
    s.play(FadeIn(best, shift=UP * 0.2), Indicate(val, color=ML_C))
    s.wait(2.5)


def gradient_descent(s):
    h = header(s, "Gradient Descent: walk downhill to the lowest error", ML_C)
    ax = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=8, y_length=4.4,
              axis_config={"color": MUTED, "include_tip": False}).shift(LEFT * 1.4 + DOWN * 0.6)
    f = lambda w: (w - 2) ** 2 + 0.4
    curve = ax.plot(f, x_range=[0, 4], color=AI_C, stroke_width=5)
    xl = T("Weight (w)", 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
    yl = T("Loss (error)", 22, MUTED).next_to(ax.y_axis, UP, buff=0.15)
    s.play(Create(ax), FadeIn(xl), FadeIn(yl))
    s.play(Create(curve), run_time=1.2)
    w = 0.2
    ball = Dot(ax.c2p(w, f(w)), radius=0.16, color=DL_C)
    info = T(f"Step 0   loss = {f(w):.2f}", 26, TXT).move_to([4.9, 1.0, 0])
    s.play(FadeIn(ball, scale=2), FadeIn(info))
    for k in range(1, 5):
        wn = w + 0.7 * (2 - w)
        s.play(MoveAlongPath(ball, ax.plot(f, x_range=[w, wn])), run_time=0.9)
        s.play(Transform(info, T(f"Step {k}   loss = {f(wn):.2f}", 26, TXT).move_to(info)), run_time=0.3)
        w = wn
    mn = DashedLine(ax.c2p(2, 0), ax.c2p(2, 0.4), color=ML_C)
    lab = Paragraph("Minimum loss", "= best model", font=FONT, font_size=26, color=ML_C,
                    weight=BOLD).move_to([4.9, -0.3, 0])
    s.play(Create(mn), FadeIn(lab), Flash(ball, color=ML_C))
    s.play(FadeIn(P("Each step moves opposite to the slope", 20, 22, MUTED).move_to([4.9, -1.6, 0])))
    s.wait(2.5)


def loss_curve(s):
    h = header(s, "Training: loss goes down, accuracy goes up", ML_C)
    axes = []
    for title, col, fn, end in (("Loss", BAD, lambda x: 0.9 * np.exp(-x / 3) + 0.08, "8%"),
                                ("Accuracy", ML_C, lambda x: 1 - 0.85 * np.exp(-x / 4), "99%")):
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 1, 0.5], x_length=5.2, y_length=3.6,
                  axis_config={"color": MUTED, "include_tip": False})
        t = T(title + (" ↓" if col == BAD else " ↑"), 30, col, BOLD).next_to(ax, UP, buff=0.25)
        xl = T("Epochs", 20, MUTED).next_to(ax.x_axis, DOWN, buff=0.15)
        axes.append((VGroup(ax, t, xl), ax, col, fn, end))
    VGroup(axes[0][0], axes[1][0]).arrange(RIGHT, buff=1.4).shift(DOWN * 0.3)
    s.play(*[FadeIn(a[0]) for a in axes])
    curves = [a[1].plot(a[3], x_range=[0, 20], color=a[2], stroke_width=5) for a in axes]
    s.play(*[Create(c) for c in curves], run_time=3, rate_func=linear)
    for a in axes:
        p = a[1].c2p(20, a[3](20))
        s.play(FadeIn(Dot(p, color=a[2])), FadeIn(T(a[4], 24, a[2], BOLD).next_to(p, UP, buff=0.15)),
               run_time=0.5)
    footer(s, "1 epoch = the model sees the whole training data once", ML_C)
    s.wait(2)


def overfitting(s):
    h = header(s, "Underfit  vs  Good fit  vs  Overfit", ML_C)
    rng = np.random.default_rng(7)
    xs = np.linspace(0.6, 9.4, 9)
    ys = 0.12 * (xs - 5) ** 2 + 1.6 + rng.normal(0, 0.45, 9)
    panels = VGroup()
    specs = [("Underfit", AI_C, "Too simple: didn't learn"),
             ("Good fit", ML_C, "Learned the real pattern"),
             ("Overfit", BAD, "Memorized the noise")]
    built = []
    for name, col, cap in specs:
        ax = Axes(x_range=[0, 10], y_range=[0, 6], x_length=3.7, y_length=2.8,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False})
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=TXT) for x, y in zip(xs, ys)])
        t = T(name, 28, col, BOLD).next_to(ax, UP, buff=0.2)
        cp = fit(P(cap, 20, 22, MUTED), 3.7).next_to(ax, DOWN, buff=0.25)
        g = VGroup(t, ax, dots, cp)
        panels.add(g)
        built.append((ax, col))
    panels.arrange(RIGHT, buff=0.6).next_to(h, DOWN, buff=0.4)
    for g in panels:
        s.play(FadeIn(g[0]), Create(g[1]), FadeIn(g[2]), run_time=0.6)
    a0, a1, a2 = [b[0] for b in built]
    under = a0.plot(lambda x: ys.mean(), x_range=[0, 10], color=AI_C, stroke_width=4)
    p = np.polyfit(xs, ys, 2)
    good = a1.plot(lambda x: np.polyval(p, x), x_range=[0.2, 9.8], color=ML_C, stroke_width=4)
    over = VMobject(color=BAD, stroke_width=4).set_points_smoothly([a2.c2p(x, y) for x, y in zip(xs, ys)])
    for curve, g in ((under, panels[0]), (good, panels[1]), (over, panels[2])):
        s.play(Create(curve), FadeIn(g[3]), run_time=1)
        s.wait(0.6)
    footer(s, "Overfit = student who memorized answers and fails new questions", BAD)
    s.wait(2)


def classification(s):
    h = header(s, "Classification: draw a boundary", ML_C)
    ax = Axes(x_range=[0, 10], y_range=[0, 10], x_length=6, y_length=4.6,
              axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).shift(LEFT * 2 + DOWN * 0.6)
    xl = T("Study hours", 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
    yl = T("Practice tests", 22, MUTED).next_to(ax.y_axis, UP, buff=0.15)
    rng = np.random.default_rng(11)

    def blob(cx, cy, n):
        pts = []
        while len(pts) < n:
            x, y = rng.normal(cx, 1.3), rng.normal(cy, 1.3)
            if 0.5 < x < 9.5 and 0.5 < y < 9.5 and abs(x + y - 10) > 1.3:
                pts.append((x, y))
        return pts
    good = [p for p in blob(7, 7, 30) if p[0] + p[1] > 10][:12]
    badp = [p for p in blob(3, 3, 30) if p[0] + p[1] < 10][:12]
    gd = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=ML_C) for p in good])
    bd = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=BAD) for p in badp])
    leg = VGroup(VGroup(Dot(color=ML_C), T("Pass", 26, ML_C)).arrange(RIGHT),
                 VGroup(Dot(color=BAD), T("Fail", 26, BAD)).arrange(RIGHT)).arrange(DOWN, aligned_edge=LEFT)
    leg.move_to([4.3, 1.2, 0])
    s.play(Create(ax), FadeIn(xl), FadeIn(yl))
    s.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in list(gd) + list(bd)], lag_ratio=0.04), FadeIn(leg),
           run_time=1.5)
    bound = DashedLine(ax.c2p(1, 9), ax.c2p(9, 1), color=DL_C, stroke_width=5)
    bl = T("Decision boundary", 22, DL_C, BOLD).next_to(ax.c2p(1, 9), RIGHT, buff=0.2)
    s.play(Create(bound), FadeIn(bl), run_time=1.2)
    s.wait(0.6)
    newp = Dot(ax.c2p(6.6, 5.6), radius=0.14, color=TXT)
    q = T("?", 28, TXT, BOLD).next_to(newp, UP, buff=0.1)
    nl = T("New student", 24, TXT).move_to([4.3, -0.4, 0])
    s.play(FadeIn(newp, scale=2), FadeIn(q), FadeIn(nl))
    s.wait(0.8)
    pred = T("Predicted: PASS ✓", 28, ML_C, BOLD).move_to([4.3, -1.2, 0])
    s.play(newp.animate.set_color(ML_C), FadeOut(q), FadeIn(pred), Flash(newp, color=ML_C))
    s.wait(2.5)


def clustering(s):
    h = header(s, "K-Means Clustering: find groups without labels", ML_C)
    rng = np.random.default_rng(5)
    origin = np.array([-1.6, -0.5, 0])
    centers = [(-3, 1), (0, -1.4), (2, 1.2)]
    pts = np.array([[cx + rng.normal(0, 0.55), cy + rng.normal(0, 0.5)] for cx, cy in centers for _ in range(11)])
    dots = VGroup(*[Dot(origin + [x, y, 0], radius=0.08, color=MUTED) for x, y in pts])
    cols = [AI_C, ML_C, DL_C]
    cent = np.array([[-1.0, 1.6], [-2.2, -1.5], [2.6, -1.2]])
    marks = VGroup(*[xmark(c).move_to(origin + [x, y, 0]) for c, (x, y) in zip(cols, cent)])
    steps = VGroup(*[T(t, 24, MUTED) for t in ("1. Place K centres", "2. Join nearest centre",
                                                 "3. Move centre to average", "4. Repeat")])
    steps.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.5, 0, 0])
    s.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), FadeIn(steps), run_time=1.5)
    s.play(steps[0].animate.set_color(TXT), LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.3))
    for it in range(3):
        lab = np.argmin(((pts[:, None, :] - cent[None, :, :]) ** 2).sum(-1), axis=1)
        s.play(steps[1].animate.set_color(TXT), steps[0].animate.set_color(MUTED),
               steps[2].animate.set_color(MUTED),
               *[d.animate.set_color(cols[l]) for d, l in zip(dots, lab)], run_time=0.8)
        cent = np.array([pts[lab == k].mean(0) if np.any(lab == k) else cent[k] for k in range(3)])
        s.play(steps[2].animate.set_color(TXT), steps[1].animate.set_color(MUTED),
               *[m.animate.move_to(origin + [x, y, 0]) for m, (x, y) in zip(marks, cent)], run_time=0.9)
        if it == 0:
            s.play(steps[3].animate.set_color(DL_C), run_time=0.4)
    footer(s, "3 groups found automatically, like 3 types of customers", ML_C)
    s.wait(2)


def rl_grid(s):
    h = header(s, "Reinforcement Learning: trial & error", ML_C)
    size = 0.8
    origin = np.array([-2.6, -0.5, 0])
    cell = lambda r, c: origin + np.array([(c - 2) * size, (2 - r) * size, 0])
    grid = VGroup(*[Square(size, stroke_color=MUTED, stroke_width=2).move_to(cell(r, c))
                    for r in range(5) for c in range(5)])
    goal = Star(5, outer_radius=0.3, color=DL_C, fill_opacity=1).move_to(cell(0, 4))
    pits = VGroup(*[Square(size - 0.1, stroke_width=0, fill_color=BAD, fill_opacity=0.5).move_to(cell(r, c))
                    for r, c in ((1, 2), (3, 3))])
    agent = Circle(0.25, color=AI_C, fill_opacity=0.9).move_to(cell(4, 0))
    leg = VGroup(VGroup(Circle(0.15, color=AI_C, fill_opacity=0.9), T("Agent (robot)", 24)).arrange(RIGHT),
                 VGroup(Star(5, outer_radius=0.17, color=DL_C, fill_opacity=1), T("Goal: +10", 24, DL_C)).arrange(RIGHT),
                 VGroup(Square(0.3, stroke_width=0, fill_color=BAD, fill_opacity=0.6), T("Trap: −10", 24, BAD)).arrange(RIGHT))
    leg.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.0, 0])
    s.play(Create(grid), FadeIn(goal), FadeIn(pits), FadeIn(agent), FadeIn(leg), run_time=1.2)
    log = VGroup()
    for ep, path, ok in ((1, [(3, 0), (2, 0), (2, 1), (1, 1), (1, 2)], False),
                         (2, [(4, 1), (3, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 4)], True)):
        for rc in path:
            s.play(agent.animate.move_to(cell(*rc)), run_time=0.28)
        res = T(f"Episode {ep}: {'+10 ✓' if ok else '−10 ✗'}", 26, ML_C if ok else BAD, BOLD)
        log.add(res)
        res.move_to([3.6, -0.8 - 0.55 * (ep - 1), 0])
        s.play(Flash(agent, color=ML_C if ok else BAD), FadeIn(res))
        if not ok:
            s.play(agent.animate.move_to(cell(4, 0)), run_time=0.5)
    footer(s, "Good moves get rewards. The agent learns which actions work.", ML_C)
    s.wait(2)


def decision_tree(s):
    h = header(s, "Decision Tree: a flowchart of questions", ML_C)
    root = card("Has 'FREE money' in it?", AI_C, 4.4, 0.9, 26, 26).move_to([0, 1.6, 0])
    spam1 = card("SPAM", BAD, 2.2, 0.8, 28, 10, tcolor=BAD, fill=0.2).move_to([-3.6, -0.3, 0])
    q2 = card("Sender in your contacts?", AI_C, 4.4, 0.9, 26, 26).move_to([2.8, -0.3, 0])
    ok = card("NOT SPAM", ML_C, 2.6, 0.8, 28, 10, tcolor=ML_C, fill=0.2).move_to([1.2, -2.3, 0])
    spam2 = card("SPAM", BAD, 2.2, 0.8, 28, 10, tcolor=BAD, fill=0.2).move_to([4.6, -2.3, 0])
    e1 = Line(root.get_bottom(), spam1.get_top(), color=MUTED)
    e2 = Line(root.get_bottom(), q2.get_top(), color=MUTED)
    e3 = Line(q2.get_bottom(), ok.get_top(), color=MUTED)
    e4 = Line(q2.get_bottom(), spam2.get_top(), color=MUTED)
    labs = [T("Yes", 22, MUTED).next_to(e1.get_center(), LEFT, buff=0.15),
            T("No", 22, MUTED).next_to(e2.get_center(), RIGHT, buff=0.15),
            T("Yes", 22, MUTED).next_to(e3.get_center(), LEFT, buff=0.15),
            T("No", 22, MUTED).next_to(e4.get_center(), RIGHT, buff=0.15)]
    s.play(FadeIn(root, scale=0.85))
    s.play(Create(e1), Create(e2), FadeIn(labs[0]), FadeIn(labs[1]))
    s.play(FadeIn(spam1), FadeIn(q2))
    s.play(Create(e3), Create(e4), FadeIn(labs[2]), FadeIn(labs[3]))
    s.play(FadeIn(ok), FadeIn(spam2))
    s.wait(0.6)
    ex = card("Email: 'Meeting at 5pm' from Ravi", MUTED, 4.6, 0.9, 22, 24, fill=0.1).move_to([-3.6, -2.3, 0])
    s.play(FadeIn(ex, shift=UP * 0.2))
    for m in (root, e2, q2, e3, ok):
        anim = m.animate.set_stroke(DL_C, width=6) if isinstance(m, Line) else m[0].animate.set_stroke(DL_C, width=6)
        s.play(anim, run_time=0.45)
    s.play(Indicate(ok, color=ML_C))
    s.wait(2.5)


def knn(s):
    h = header(s, "K-Nearest Neighbours (KNN): ask your neighbours", ML_C)
    off = np.array([0.2, -0.4, 0])
    cats = [(-2.6, 0.1), (-1.5, 0.3), (-2.6, -1.0), (-4.0, 1.2), (-3.8, 0.2), (-3.4, 1.6), (-4.4, -0.6), (-3.2, -1.8)]
    dogs = [(-1.3, -1.0), (-1.2, 0.0), (0.2, -1.6), (0.5, -0.4), (-0.2, 0.8), (0.8, -2.0), (-0.4, -2.2)]
    cd = VGroup(*[Dot(off + [x, y, 0], radius=0.11, color=AI_C) for x, y in cats])
    dd = VGroup(*[Square(0.2, color=DL_C, fill_opacity=1).move_to(off + [x, y, 0]) for x, y in dogs])
    leg = VGroup(VGroup(Dot(color=AI_C), T("Cat", 26, AI_C)).arrange(RIGHT),
                 VGroup(Square(0.2, color=DL_C, fill_opacity=1), T("Dog", 26, DL_C)).arrange(RIGHT))
    leg.arrange(DOWN, aligned_edge=LEFT).move_to([4.2, 1.4, 0])
    s.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in list(cd) + list(dd)], lag_ratio=0.05), FadeIn(leg))
    p = off + np.array([-2.0, -0.4, 0])
    new = Star(5, outer_radius=0.2, color=TXT, fill_opacity=1).move_to(p)
    s.play(FadeIn(new, scale=2), FadeIn(T("New animal: ?", 26).move_to([4.2, 0.2, 0])))
    ring = Circle(radius=1.0, color=TXT, stroke_width=3).move_to(p)
    s.play(Create(ring), run_time=1)
    near = [cd[0], cd[1], cd[2], dd[0], dd[1]]
    lines = VGroup(*[DashedLine(p, n.get_center(), color=MUTED, stroke_width=2) for n in near])
    s.play(Create(lines), *[Indicate(n, scale_factor=1.6) for n in near])
    vote = T("K = 5:  Cat 3  vs  Dog 2", 26, TXT, BOLD).move_to([4.2, -0.6, 0])
    s.play(FadeIn(vote))
    s.wait(0.8)
    res = T("Prediction: CAT", 28, AI_C, BOLD).move_to([4.2, -1.4, 0])
    s.play(new.animate.set_color(AI_C), FadeIn(res), Flash(new, color=AI_C))
    s.wait(2.5)


def sigmoid_scene(s):
    h = header(s, "Logistic Regression: gives a probability (0 to 1)", ML_C)
    ax = Axes(x_range=[-6, 6, 2], y_range=[0, 1, 0.5], x_length=8.5, y_length=3.5,
              axis_config={"color": MUTED, "include_tip": False}).shift(LEFT * 1.3 + DOWN * 0.15)
    sg = lambda x: 1 / (1 + np.exp(-x))
    curve = ax.plot(sg, x_range=[-6, 6], color=ML_C, stroke_width=5)
    th = DashedLine(ax.c2p(-6, 0.5), ax.c2p(6, 0.5), color=MUTED)
    labs = VGroup(T("1", 22, MUTED).next_to(ax.c2p(-6, 1), LEFT, buff=0.15),
                  T("0.5", 22, MUTED).next_to(ax.c2p(-6, 0.5), LEFT, buff=0.15),
                  T("0", 22, MUTED).next_to(ax.c2p(-6, 0), LEFT, buff=0.15),
                  T("Spam score (bad words, links...)", 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.2),
                  T("P(spam)", 22, MUTED).next_to(ax.c2p(-6, 1), UP, buff=0.2))
    s.play(Create(ax), FadeIn(labs))
    s.play(Create(curve), run_time=1.5)
    s.play(Create(th))
    for x in (-4, -1, 2, 4.5):
        y = sg(x)
        c = BAD if y > 0.5 else ML_C
        d = Dot(ax.c2p(x, y), radius=0.12, color=c)
        t = T(f"{y:.2f}", 22, c, BOLD).next_to(d, UP if y < 0.5 else DOWN, buff=0.15).shift(RIGHT * 0.3)
        s.play(FadeIn(d, scale=2), FadeIn(t), run_time=0.5)
    rules = VGroup(T("Above 0.5 → SPAM", 26, BAD, BOLD), T("Below 0.5 → NOT SPAM", 26, ML_C, BOLD))
    rules.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.2, 0])
    fit(rules, 3.6)
    s.play(FadeIn(rules[0]), run_time=0.6)
    s.play(FadeIn(rules[1]), run_time=0.6)
    footer(s, "Despite the name, Logistic Regression is used for CLASSIFICATION", DL_C)
    s.wait(2)


def neuron(s):
    h = header(s, "An Artificial Neuron", DL_C)
    vals, ws = ["0.5", "0.2", "0.9"], ["w=0.8", "w=−0.4", "w=0.6"]
    ins = VGroup(*[VGroup(Circle(0.4, color=AI_C, fill_opacity=0.25), T(v, 22, TXT, BOLD))
                   for v in vals]).arrange(DOWN, buff=0.55).move_to([-5.0, 0.2, 0])
    for c in ins:
        c[1].move_to(c[0])
    itl = T("Inputs", 22, MUTED).next_to(ins, UP, buff=0.25)
    sm = VGroup(Circle(0.65, color=DL_C, fill_opacity=0.2), T("Σ", 44, DL_C, BOLD)).move_to([-0.8, 0.2, 0])
    sm[1].move_to(sm[0])
    act = card("ReLU", DL_C, 1.7, 1.0, 28, 8).move_to([1.9, 0.2, 0])
    out = VGroup(Circle(0.45, color=ML_C, fill_opacity=0.3), T("0.86", 22, TXT, BOLD)).move_to([4.6, 0.2, 0])
    out[1].move_to(out[0])
    otl = T("Output", 22, MUTED).next_to(out, UP, buff=0.25)
    arrs = VGroup(*[arrow(c.get_right(), sm.get_left(), MUTED) for c in ins])
    wl = VGroup(*[T(w, 20, DL_C).move_to(a.get_center() + UP * 0.28) for w, a in zip(ws, arrs)])
    a2, a3 = arrow(sm.get_right(), act.get_left()), arrow(act.get_right(), out.get_left())
    s.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in ins], lag_ratio=0.2), FadeIn(itl))
    s.play(*[GrowArrow(a) for a in arrs], FadeIn(wl))
    s.play(FadeIn(sm, scale=0.7))
    s.play(*pulse(arrs, DL_C), sm[0].animate.set_fill(opacity=0.6), run_time=0.9)
    calc = T("0.5×0.8 + 0.2×(−0.4) + 0.9×0.6 = 0.86", 28, TXT).move_to([0, -2.1, 0])
    s.play(Write(calc), run_time=1.6)
    s.play(GrowArrow(a2), FadeIn(act))
    s.play(GrowArrow(a3), FadeIn(out, scale=0.7), FadeIn(otl))
    calc2 = T("ReLU(0.86) = 0.86  →  sent to the next layer", 26, ML_C, BOLD).next_to(calc, DOWN, buff=0.35)
    s.play(FadeIn(calc2, shift=UP * 0.2))
    s.wait(2.5)


def activation(s):
    h = header(s, "Activation Functions", DL_C)
    panels = VGroup()
    for name, col, xr, yr, fn, form, cap in (
            ("ReLU", DL_C, [-3, 3], [-0.5, 3], lambda x: max(0, x), "max(0, x)", "Fast. Used in hidden layers"),
            ("Sigmoid", ML_C, [-6, 6], [0, 1], lambda x: 1 / (1 + np.exp(-x)), "1 / (1 + e^(−x))",
             "Squashes to 0–1 (probability)")):
        ax = Axes(x_range=xr, y_range=yr, x_length=5, y_length=3.2,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False})
        c = ax.plot(fn, x_range=xr, color=col, stroke_width=5, use_smoothing=False)
        g = VGroup(T(name, 32, col, BOLD), VGroup(ax, c), T(form, 24, TXT), T(cap, 22, MUTED))
        g.arrange(DOWN, buff=0.25)
        panels.add(g)
    panels.arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(h, DOWN, buff=0.35)
    for g in panels:
        s.play(FadeIn(g[0]), Create(g[1][0]), run_time=0.7)
        s.play(Create(g[1][1]), run_time=1.2)
        s.play(FadeIn(g[2]), FadeIn(g[3]), run_time=0.6)
        s.wait(0.5)
    footer(s, "Without activation, the whole network is just a straight line", DL_C)
    s.wait(2)


def neural_network(s):
    h = header(s, "Deep Learning = many layers of neurons", DL_C)
    layers, edges = make_net([3, 5, 5, 5, 2], [AI_C, DL_C, DL_C, DL_C, ML_C], UP * 0.25, ybuf=0.3)
    tags = VGroup(*[T(nm, 20, MUTED).next_to(l, DOWN, buff=0.2) for nm, l in
                    zip(["Input", "Hidden 1", "Hidden 2", "Hidden 3", "Output"], layers)])
    s.play(LaggedStart(*[FadeIn(l, scale=0.7) for l in layers], lag_ratio=0.2), run_time=1.4)
    s.play(*[Create(e) for e in edges], FadeIn(tags), run_time=1.4)
    s.play(FadeIn(T("cat photo", 24, AI_C).next_to(layers[0], LEFT, buff=0.35)))
    for _ in range(2):
        for i, g in enumerate(edges):
            s.play(*pulse(g, DL_C), layers[i + 1].animate.set_fill(opacity=0.7), run_time=0.45)
            s.play(layers[i + 1].animate.set_fill(opacity=0.25), run_time=0.1)
    o1 = T("Cat 97%", 26, ML_C, BOLD).next_to(layers[-1][0], RIGHT, buff=0.3)
    o2 = T("Dog 3%", 22, MUTED).next_to(layers[-1][1], RIGHT, buff=0.3)
    s.play(layers[-1][0].animate.set_fill(ML_C, opacity=0.9), FadeIn(o1), FadeIn(o2))
    footer(s, "Each hidden layer learns features by itself", DL_C)
    s.wait(2)


def backprop(s):
    h = header(s, "Backpropagation: learning from mistakes", DL_C)
    layers, edges = make_net([3, 4, 4, 2], [AI_C, DL_C, DL_C, ML_C], LEFT * 2.5 + DOWN * 0.4, xbuf=1.7)
    s.play(FadeIn(layers), *[Create(e) for e in edges], run_time=1.2)
    px = 4.3
    st = T("1. Forward pass", 26, AI_C, BOLD).move_to([px, 1.5, 0])
    s.play(FadeIn(st))
    for g in edges:
        s.play(*pulse(g, AI_C), run_time=0.45)
    p1 = T("Predicted: Dog", 24, BAD, BOLD).move_to([px, 0.8, 0])
    p2 = T("Actual: Cat  ✗", 24, ML_C, BOLD).move_to([px, 0.3, 0])
    s.play(FadeIn(p1), FadeIn(p2))
    st2 = T("2. Send error backward", 26, BAD, BOLD).move_to([px, -0.5, 0])
    s.play(FadeIn(st2))
    for g in reversed(edges):
        s.play(*pulse(g, BAD, reverse=True), run_time=0.45)
    st3 = T("3. Adjust the weights", 26, DL_C, BOLD).move_to([px, -1.2, 0])
    rng = np.random.default_rng(2)
    s.play(FadeIn(st3), *[e.animate.set_stroke(color=DL_C if rng.random() > 0.5 else MUTED,
                                                width=rng.uniform(1, 5), opacity=0.8)
                          for g in edges for e in g], run_time=1.2)
    for g in edges:
        s.play(*pulse(g, ML_C), run_time=0.35)
    fin = T("Predicted: Cat  ✓", 26, ML_C, BOLD).move_to([px, -2.0, 0])
    s.play(FadeIn(fin), Flash(layers[-1][0], color=ML_C))
    s.wait(2.5)


def feature_engineering(s):
    h = header(s, "ML vs DL: who finds the features?", DL_C)
    l1 = T("Machine Learning", 28, ML_C, BOLD)
    r1b, r1a = flow_row([("Raw photo", MUTED), ("Human picks features: ears, whiskers", AI_C),
                         ("ML model", ML_C), ("Cat", ML_C)], total_w=12.4, h=1.2)
    l2 = T("Deep Learning", 28, DL_C, BOLD)
    r2b, r2a = flow_row([("Raw photo", MUTED), ("Neural network learns the features itself", DL_C),
                         ("Cat", DL_C)], total_w=12.4, h=1.2)
    VGroup(r1b, r1a).move_to(UP * 0.9)
    VGroup(r2b, r2a).move_to(DOWN * 1.6)
    l1.next_to(r1b, UP, buff=0.25).align_to(r1b, LEFT)
    l2.next_to(r2b, UP, buff=0.25).align_to(r2b, LEFT)
    for lab, b, a in ((l1, r1b, r1a), (l2, r2b, r2a)):
        s.play(FadeIn(lab, shift=RIGHT * 0.2))
        for i, x in enumerate(b):
            if i:
                s.play(GrowArrow(a[i - 1]), run_time=0.3)
            s.play(FadeIn(x, scale=0.85), run_time=0.45)
        s.wait(0.8)
    s.play(Indicate(r1b[1], color=AI_C), Indicate(r2b[1], color=DL_C), run_time=1.2)
    cap = T("DL needs more data, but no manual feature work", 26, DL_C, BOLD).to_edge(DOWN, buff=0.55)
    s.play(FadeIn(cap, shift=UP * 0.2))
    s.wait(2.5)


def feature_hierarchy(s):
    h = header(s, "What each layer learns (face recognition)", DL_C)
    boxes = VGroup(*[RoundedRectangle(width=2.6, height=2.6, corner_radius=0.2, stroke_color=DL_C,
                                      stroke_width=3, fill_color=PANEL, fill_opacity=1) for _ in range(4)])
    boxes.arrange(RIGHT, buff=0.75).shift(DOWN * 0.1)
    arrs = VGroup(*[arrow(a.get_right(), b.get_left(), DL_C) for a, b in zip(boxes[:-1], boxes[1:])])
    names = ["Layer 1: Edges", "Layer 2: Shapes", "Layer 3: Parts", "Layer 4: Face"]
    labs = VGroup(*[T(n, 22, TXT, BOLD).next_to(b, DOWN, buff=0.25) for n, b in zip(names, boxes)])
    c0, c1, c2, c3 = [b.get_center() for b in boxes]
    edges = VGroup(*[Line(LEFT * 0.4, RIGHT * 0.4, color=AI_C, stroke_width=5).rotate(a).move_to(c0 + off)
                     for a, off in ((0, UL * 0.6), (PI / 2, UR * 0.6), (PI / 4, DL * 0.6),
                                    (-PI / 4, DR * 0.6), (PI / 3, ORIGIN), (0, DOWN * 0.95))])
    shapes = VGroup(Circle(0.3, color=AI_C).move_to(c1 + UL * 0.55),
                    Arc(radius=0.35, start_angle=PI, angle=PI, color=AI_C).move_to(c1 + UR * 0.55),
                    Triangle(color=AI_C).scale(0.3).move_to(c1 + DL * 0.55),
                    Square(0.5, color=AI_C).move_to(c1 + DR * 0.55))
    eye = VGroup(Ellipse(0.7, 0.4, color=ML_C), Dot(radius=0.1, color=ML_C)).move_to(c2 + UL * 0.55)
    ear = Triangle(color=ML_C).scale(0.35).move_to(c2 + UR * 0.55)
    nose = Triangle(color=ML_C).scale(0.22).rotate(PI).move_to(c2 + DL * 0.55)
    mouth = Arc(radius=0.35, start_angle=PI + 0.3, angle=PI - 0.6, color=ML_C).move_to(c2 + DR * 0.55)
    parts = VGroup(eye, ear, nose, mouth)
    head = Circle(0.95, color=DL_C, stroke_width=4).move_to(c3 + DOWN * 0.1)
    face = VGroup(head,
                  Triangle(color=DL_C).scale(0.3).move_to(head.get_top() + LEFT * 0.55 + DOWN * 0.05),
                  Triangle(color=DL_C).scale(0.3).move_to(head.get_top() + RIGHT * 0.55 + DOWN * 0.05),
                  Dot(c3 + UL * 0.3 + DOWN * 0.05, radius=0.09, color=DL_C),
                  Dot(c3 + UR * 0.3 + DOWN * 0.05, radius=0.09, color=DL_C),
                  Arc(radius=0.4, start_angle=PI + 0.5, angle=PI - 1.0, color=DL_C).move_to(c3 + DOWN * 0.45))
    s.play(FadeIn(boxes), FadeIn(labs), run_time=0.8)
    for i, content in enumerate((edges, shapes, parts, face)):
        if i:
            s.play(GrowArrow(arrs[i - 1]), run_time=0.4)
        s.play(LaggedStart(*[Create(x) for x in content], lag_ratio=0.15), run_time=1.1)
        s.wait(0.4)
    footer(s, "Simple patterns combine into complex ones, layer by layer", DL_C)
    s.wait(2)


def cnn_filter(s):
    h = header(s, "CNN: a filter slides over the image", DL_C)
    n, sz = 6, 0.55
    img = VGroup(*[Square(sz, stroke_color=MUTED, stroke_width=1, fill_color=WHITE if c >= 3 else "#1E293B",
                          fill_opacity=0.9 if c >= 3 else 1) for r in range(n) for c in range(n)])
    img.arrange_in_grid(n, n, buff=0).move_to([-4.2, -0.2, 0])
    il = T("Image (pixels)", 22, MUTED).next_to(img, DOWN, buff=0.25)
    kv = ["−1", "0", "1"] * 3
    ker = VGroup(*[VGroup(Square(0.6, color=DL_C, fill_opacity=0.15), T(v, 22, DL_C, BOLD)) for v in kv])
    for k in ker:
        k[1].move_to(k[0])
    ker.arrange_in_grid(3, 3, buff=0).move_to([0, 0.2, 0])
    kl = T("Edge filter", 22, DL_C, BOLD).next_to(ker, DOWN, buff=0.25)
    m = n - 2
    outg = VGroup(*[Square(sz, stroke_color=MUTED, stroke_width=1, fill_color="#1E293B", fill_opacity=1)
                    for _ in range(m * m)]).arrange_in_grid(m, m, buff=0).move_to([4.2, -0.2, 0])
    ol = T("Feature map", 22, ML_C, BOLD).next_to(outg, DOWN, buff=0.25)
    s.play(FadeIn(img), FadeIn(il), run_time=0.8)
    s.play(FadeIn(ker), FadeIn(kl), run_time=0.8)
    s.play(FadeIn(outg), FadeIn(ol), run_time=0.6)
    win = Square(sz * 3, color=DL_C, stroke_width=6).move_to(img[0 * n + 0].get_center() + (RIGHT + DOWN) * sz)
    s.play(Create(win))
    for r in range(m):
        for c in range(m):
            tgt = img[r * n + c].get_center() + (RIGHT + DOWN) * sz
            bright = c in (1, 2)
            fill = outg[r * m + c].animate.set_fill(ML_C if bright else "#334155", opacity=1)
            rt = 0.35 if r == 0 else 0.15
            s.play(win.animate.move_to(tgt), fill, run_time=rt)
    s.play(FadeOut(win))
    footer(s, "Bright = the filter found a vertical edge here", DL_C)
    s.wait(2)


def llm_tokens(s):
    h = header(s, "LLMs like ChatGPT: predict the next word", DL_C)
    words = ["Machine", "learning", "is", "a", "part", "of"]
    toks = VGroup(*[card(w, AI_C, 0.32 * len(w) + 0.7, 0.75, 26, 20) for w in words])
    qm = card("?", DL_C, 1.0, 0.75, 30, 4, fill=0.35)
    row = VGroup(*toks, qm).arrange(RIGHT, buff=0.2).move_to(UP * 0.5)
    s.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in toks], lag_ratio=0.15), run_time=1.3)
    s.play(FadeIn(qm, scale=1.3))
    wts = [0.9, 0.75, 0.2, 0.1, 0.6, 0.5]
    arcs = VGroup(*[ArcBetweenPoints(qm.get_top(), t.get_top(), angle=PI / 3, color=DL_C,
                                     stroke_width=1 + 6 * w, stroke_opacity=0.3 + 0.7 * w)
                    for t, w in zip(toks, wts)])
    al = T("Attention: which words matter most?", 22, DL_C).next_to(row, DOWN, buff=0.3)
    s.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), FadeIn(al), run_time=1.5)
    s.wait(0.5)
    cands = [("AI", 0.72), ("science", 0.12), ("computers", 0.09), ("maths", 0.04)]
    bars = VGroup()
    for i, (w, p) in enumerate(cands):
        y = -1.2 - 0.55 * i
        lab = T(w, 24, TXT).move_to([-2.2, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(0.05, 6 * p), height=0.35, stroke_width=0,
                        fill_color=ML_C if i == 0 else MUTED, fill_opacity=0.9)
        bar.move_to([-1.9, y, 0], aligned_edge=LEFT)
        pct = T(f"{int(p * 100)}%", 22, ML_C if i == 0 else MUTED).next_to(bar, RIGHT, buff=0.15)
        bars.add(VGroup(lab, bar, pct))
    s.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bars], lag_ratio=0.2), run_time=1.4)
    s.wait(0.6)
    ai = card("AI", ML_C, 1.0, 0.75, 30, 4, fill=0.4).move_to(qm)
    s.play(Transform(qm, ai), Indicate(bars[0], color=ML_C))
    s.play(FadeIn(T("Trained on huge text using Transformers (deep networks)", 22, MUTED).to_edge(DOWN, buff=0.45)))
    s.wait(2.5)


def data_vs_perf(s):
    h = header(s, "Why Deep Learning needs BIG data", DL_C)
    ax = Axes(x_range=[0, 10], y_range=[0, 10], x_length=8, y_length=4.4,
              axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).shift(LEFT * 1.6 + DOWN * 0.5)
    ml = lambda x: 6 * (1 - np.exp(-x / 1.5)) + 0.5
    dl = lambda x: 9.5 / (1 + np.exp(-(x - 5)))
    xs = np.linspace(0, 10, 2001)
    xc = xs[np.argmin(np.abs(np.array([ml(x) - dl(x) for x in xs])))]
    xl = T("Amount of data →", 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
    yl = T("Performance", 22, MUTED).next_to(ax.y_axis, UP, buff=0.15)
    s.play(Create(ax), FadeIn(xl), FadeIn(yl))
    c1 = ax.plot(ml, x_range=[0, 10], color=ML_C, stroke_width=5)
    c2 = ax.plot(dl, x_range=[0, 10], color=DL_C, stroke_width=5)
    s.play(Create(c1), Create(c2), run_time=3, rate_func=linear)
    l1 = T("Traditional ML", 24, ML_C, BOLD).next_to(ax.c2p(10, ml(10)), RIGHT, buff=0.2)
    l2 = T("Deep Learning", 24, DL_C, BOLD).next_to(ax.c2p(10, dl(10)), RIGHT, buff=0.2)
    s.play(FadeIn(l1), FadeIn(l2))
    vl = DashedLine(ax.c2p(xc, 0), ax.c2p(xc, 9.8), color=MUTED)
    t1 = T("Small data: ML wins", 22, ML_C).next_to(ax.c2p(xc / 2, 9.4), ORIGIN)
    t2 = T("Big data: DL wins", 22, DL_C).next_to(ax.c2p((xc + 10) / 2, 2.3), ORIGIN)
    s.play(Create(vl), FadeIn(t1), FadeIn(t2))
    s.wait(3)


def cpu_vs_gpu(s):
    h = header(s, "CPU vs GPU", DL_C)
    cpu = VGroup(*[Square(0.95, color=AI_C, fill_opacity=0.2, stroke_width=4) for _ in range(4)])
    cpu.arrange_in_grid(2, 2, buff=0.2)
    gpu = VGroup(*[Square(0.15, stroke_width=0, fill_color=DL_C, fill_opacity=0.25) for _ in range(196)])
    gpu.arrange_in_grid(14, 14, buff=0.05)
    lc = VGroup(T("CPU", 36, AI_C, BOLD), cpu, T("A few powerful cores", 24, TXT),
                T("Great for step-by-step tasks", 22, MUTED)).arrange(DOWN, buff=0.3)
    rc = VGroup(T("GPU", 36, DL_C, BOLD), gpu, T("Thousands of small cores", 24, TXT),
                T("Millions of multiplications at once", 22, MUTED)).arrange(DOWN, buff=0.3)
    VGroup(lc, rc).arrange(RIGHT, buff=2.4).next_to(h, DOWN, buff=0.4)
    s.play(FadeIn(lc[0]), FadeIn(rc[0]), FadeIn(cpu), FadeIn(gpu), run_time=0.8)
    for k in range(4):
        s.play(cpu[k].animate.set_fill(opacity=0.9), run_time=0.3)
        s.play(cpu[k].animate.set_fill(opacity=0.2), run_time=0.15)
    s.play(gpu.animate.set_fill(opacity=1), run_time=0.4)
    s.play(gpu.animate.set_fill(opacity=0.25), run_time=0.3)
    s.play(gpu.animate.set_fill(opacity=1), run_time=0.4)
    s.play(FadeIn(lc[2:]), FadeIn(rc[2:]))
    footer(s, "Neural networks = matrix maths, so GPUs train them fast", DL_C)
    s.wait(2)


def outro(s, nxt):
    t = T("Thanks for watching!", 56, TXT, BOLD).shift(UP * 1.8)
    sub = RoundedRectangle(width=4.4, height=1.1, corner_radius=0.2, stroke_width=0,
                           fill_color="#FF0000", fill_opacity=1).shift(UP * 0.1)
    st = T("SUBSCRIBE", 36, WHITE, BOLD).move_to(sub)
    extra = T("Like  •  Share  •  Comment your doubts", 28, MUTED).shift(DOWN * 1.3)
    nx = T(nxt, 30, DL_C, BOLD).shift(DOWN * 2.3)
    brand = T("AI with Mani", 30, AI_C, BOLD).to_edge(DOWN, buff=0.5)
    s.play(Write(t), run_time=1)
    s.play(FadeIn(sub, scale=0.6), FadeIn(st, scale=0.6))
    s.play(Indicate(VGroup(sub, st), scale_factor=1.12, color=WHITE))
    s.play(sub.animate.set_fill("#3F3F46"),
           Transform(st, T("SUBSCRIBED ✓", 32, WHITE, BOLD).move_to(sub)))
    s.play(FadeIn(extra, shift=UP * 0.2))
    s.play(FadeIn(nx, shift=UP * 0.2), FadeIn(brand))
    s.wait(3)


# ---------------------------------------------------------------- the 80 clips
# (chapter, slug, function, kwargs, suggested voiceover)
CLIPS = [
    # ---- Chapter 2: The Big Picture
    (2, "chapter2_card", chapter_card, dict(num=2, title="The Big Picture", sub="How AI, ML and DL fit together"),
     "Chapter 2. First, let's see the big picture: how AI, ML and DL are connected."),
    (2, "ai_ml_dl_circles", nested_circles, {},
     "Think of three circles. AI is the biggest. Machine Learning is inside AI. Deep Learning is inside Machine Learning."),
    (2, "define_ai", definition, dict(term="Artificial Intelligence", color=AI_C,
                                      text="Making machines do tasks that normally need human intelligence: thinking, deciding, understanding.",
                                      example="Chess engines, Google Maps routes, voice assistants",
                                      tip="AI is the BIGGEST circle. ML and DL are inside it."),
     "AI means making machines do tasks that normally need human intelligence."),
    (2, "define_ml", definition, dict(term="Machine Learning", color=ML_C,
                                      text="A branch of AI where machines learn patterns from data, instead of following fixed rules written by humans.",
                                      example="A spam filter learns from thousands of emails",
                                      tip="Arthur Samuel (1959): learning without being explicitly programmed."),
     "Machine Learning is a part of AI where the machine learns from data instead of fixed rules."),
    (2, "define_dl", definition, dict(term="Deep Learning", color=DL_C,
                                      text="A branch of ML that uses neural networks with many layers to learn directly from raw data like images, audio and text.",
                                      example="Face unlock, ChatGPT, Google Translate",
                                      tip="DL = Machine Learning + deep neural networks."),
     "Deep Learning is a part of ML that uses neural networks with many layers."),
    (2, "history_timeline", timeline, dict(title="A Short History", color=AI_C, events=[
        ("1950", "Turing Test idea", AI_C), ("1956", "The word 'AI' is born", AI_C),
        ("1959", "'Machine Learning' named", ML_C), ("1986", "Backpropagation popular", DL_C),
        ("1997", "Deep Blue beats Kasparov", AI_C), ("2012", "AlexNet: DL boom", DL_C),
        ("2017", "Transformers invented", DL_C), ("2022", "ChatGPT launched", DL_C)]),
     "AI started in the 1950s. ML came next. Deep Learning exploded after 2012, and ChatGPT arrived in 2022."),
    (2, "rules_vs_learning", rules_vs_learning, {},
     "In normal programming, we give rules and data to get answers. In ML, we give data and answers, and the machine finds the rules."),
    (2, "rule_ai_vs_ml", compare, dict(title="Rule-based AI vs Machine Learning", color=AI_C,
                                       left=("Rule-based AI", AI_C, ["Humans write if-else rules",
                                                                     "Works only for cases we planned",
                                                                     "Example: old chatbots, ATM menus"]),
                                       right=("Machine Learning", ML_C, ["Learns rules from examples",
                                                                         "Handles new, unseen cases",
                                                                         "Example: spam filter, YouTube suggestions"])),
     "Rule-based AI only follows the rules we write. ML learns from examples, so it can handle new cases."),
    (2, "ai_without_ml", bullets, dict(title="AI that is NOT Machine Learning", color=AI_C, items=[
        "Old chess programs (search + rules)", "GPS shortest path (Dijkstra / A* algorithm)",
        "Expert systems (doctor-style if-else rules)", "Video game enemies (scripted behaviour)"],
        foot="AI is bigger than ML!"),
     "Not every AI learns. GPS route finding and old chess programs are AI, but not Machine Learning."),
    (2, "sort_examples", mapping, dict(title="AI, ML or DL?", color=AI_C,
                                       buckets=[("AI (rules)", AI_C), ("ML", ML_C), ("DL", DL_C)],
                                       items=[("Old chess engine", 0), ("Spam filter", 1), ("Face unlock", 2),
                                              ("GPS shortest route", 0), ("Movie recommendations", 1), ("ChatGPT", 2)],
                                       foot="Remember: every ML and DL example is also AI!"),
     "Let's sort some examples into AI, ML and DL."),
    (2, "quiz_chatgpt", quiz, dict(q="ChatGPT belongs to which field?",
                                   options=["Only AI, not ML", "ML but not DL", "Deep Learning (so also ML & AI)", "None of these"],
                                   answer=2, explain="Every DL system is also ML and AI."),
     "Quick quiz! ChatGPT belongs to which field? Pause and think."),

    # ---- Chapter 3: How ML Learns
    (3, "chapter3_card", chapter_card, dict(num=3, title="How Machine Learning Learns", sub="Data, training, testing and errors"),
     "Chapter 3. Now the most important part: how does a machine actually learn?"),
    (3, "student_analogy", table, dict(title="ML is like a student preparing for exams", color=ML_C,
                                       headers=["Student", "Machine Learning"], hcolors=[AI_C, ML_C], colw=[6.4, 6.4],
                                       rows=[["Practice questions with answers", "Training data (with labels)"],
                                             ["Learning the method", "Training the model"],
                                             ["Final exam (new questions)", "Test data"],
                                             ["Marks", "Accuracy"],
                                             ["Memorizing answers only", "Overfitting"]]),
     "ML is just like a student. Practice questions are training data, and the final exam is test data."),
    (3, "dataset_table", dataset_table, {},
     "Here is a dataset of houses. Size, bedrooms and location are features. Price is the label we want to predict."),
    (3, "define_features_label", definition, dict(term="Features & Label", color=ML_C,
                                                  text="Features are the inputs (clues). The label is the correct answer we want the model to predict.",
                                                  example="Size, bedrooms → Price",
                                                  tip="Supervised learning needs LABELLED data."),
     "Features are the inputs. The label is the answer."),
    (3, "ml_pipeline", flow, dict(title="The Machine Learning Pipeline", color=ML_C,
                                  steps=[("Collect data", AI_C), ("Clean data", AI_C), ("Choose model", ML_C),
                                         ("Train", ML_C), ("Test", DL_C), ("Use it", DL_C)],
                                  note="Good data matters more than a fancy model"),
     "Every ML project follows these steps: collect data, clean it, choose a model, train, test and use it."),
    (3, "train_test_split", train_test_split, {},
     "We split the data: 80% to train the model, and 20% kept hidden to test it, like a final exam."),
    (3, "regression_fit", regression_fit, {},
     "The model starts with a bad line. Training moves the line until the total error is the smallest."),
    (3, "define_loss", definition, dict(term="Loss (Error)", color=BAD,
                                        text="A number that tells how wrong the model's predictions are. Training means making this number as small as possible.",
                                        tip="Common loss for numbers: Mean Squared Error (MSE)."),
     "Loss is a number that shows how wrong the model is. Training tries to make it as small as possible."),
    (3, "gradient_descent", gradient_descent, {},
     "Gradient descent is like walking downhill in fog. Each step goes towards lower error, until we reach the bottom."),
    (3, "loss_curve", loss_curve, {},
     "As training goes on, the loss goes down and the accuracy goes up."),
    (3, "training_loop", flow, dict(title="The Training Loop", color=ML_C,
                                    steps=[("Predict", AI_C), ("Measure error (loss)", BAD), ("Adjust weights", DL_C),
                                           ("Better model", ML_C)], loop=True,
                                    note="Repeat thousands of times = training"),
     "Training is a loop: predict, measure the error, adjust, and repeat thousands of times."),
    (3, "overfitting_plots", overfitting, {},
     "Underfit is too simple. Overfit memorizes the noise. We want a good fit in the middle."),
    (3, "under_vs_overfit", compare, dict(title="Underfitting vs Overfitting", color=ML_C,
                                          left=("Underfitting", AI_C, ["Model is too simple", "Bad on training AND test data",
                                                                       "Student who didn't study"]),
                                          right=("Overfitting", BAD, ["Model memorized training data", "Great on training, bad on test",
                                                                      "Student who memorized answers"]),
                                          foot="Goal: learn the pattern, not the noise"),
     "Underfitting is like not studying. Overfitting is like memorizing answers without understanding."),
    (3, "what_is_model", bullets, dict(title="What is a 'Model'?", color=ML_C, items=[
        "A model = a maths function learned from data", "Input → Model → Prediction",
        "Parameters (weights) = the numbers it learns", "Training = finding the best parameters"]),
     "A model is simply a maths function. Training finds the best numbers inside it."),
    (3, "spam_example", flow, dict(title="Example: Spam Filter", color=ML_C,
                                   steps=[("New email", MUTED), ("Trained ML model", ML_C), ("SPAM (98%)", BAD)],
                                   note="It uses patterns it learned: words, links, sender"),
     "When a new email arrives, the trained model checks the patterns and says: spam, 98% sure."),
    (3, "quiz_label", quiz, dict(q="In a dataset, the 'label' is...",
                                 options=["The input data", "The answer we want to predict", "The algorithm", "The computer's GPU"],
                                 answer=1, explain="Features = inputs.  Label = correct answer."),
     "Quiz time! What is a label?"),

    # ---- Chapter 4: Types of ML
    (4, "chapter4_card", chapter_card, dict(num=4, title="3 Types of Machine Learning", sub="Supervised, Unsupervised, Reinforcement"),
     "Chapter 4. Machine Learning has three main types."),
    (4, "three_types", bullets, dict(title="3 Types of Machine Learning", color=ML_C, items=[
        ("Supervised: learn with answers (labels)", ML_C), ("Unsupervised: find patterns without answers", AI_C),
        ("Reinforcement: learn from rewards and penalties", DL_C)]),
     "Supervised learns with answers, unsupervised finds patterns alone, and reinforcement learns from rewards."),
    (4, "define_supervised", definition, dict(term="Supervised Learning", color=ML_C,
                                              text="Learning from labelled examples: every input comes with the correct answer.",
                                              example="Photos labelled 'cat' or 'dog'",
                                              tip="Two kinds: Classification (category) and Regression (number)."),
     "Supervised learning means learning with a teacher. Every example has the correct answer."),
    (4, "classification", classification, {},
     "Classification draws a boundary. For a new student, the model checks which side they fall on."),
    (4, "class_vs_regression", compare, dict(title="Classification vs Regression", color=ML_C,
                                             left=("Classification", AI_C, ["Output = a category", "Spam / Not spam",
                                                                            "Cat / Dog", "Pass / Fail"]),
                                             right=("Regression", ML_C, ["Output = a number", "House price",
                                                                         "Tomorrow's temperature", "Exam marks"])),
     "Classification gives a category. Regression gives a number."),
    (4, "define_unsupervised", definition, dict(term="Unsupervised Learning", color=AI_C,
                                                text="Learning from data WITHOUT labels: the model finds hidden groups or patterns by itself.",
                                                example="Grouping customers by shopping habits",
                                                tip="Main task: Clustering (e.g. K-Means)."),
     "Unsupervised learning has no answers. The model finds the groups by itself."),
    (4, "clustering", clustering, {},
     "K-Means places centres, groups nearby points, moves the centres, and repeats until the groups are clear."),
    (4, "unsupervised_uses", bullets, dict(title="Where is Unsupervised Learning used?", color=AI_C, items=[
        "Customer segmentation (groups of buyers)", "Fraud detection (finding unusual transactions)",
        "Grouping similar news articles", "Recommendation systems (similar users)"]),
     "Unsupervised learning is used for customer groups, fraud detection and recommendations."),
    (4, "define_rl", definition, dict(term="Reinforcement Learning", color=DL_C,
                                      text="An agent learns by trial and error. Good actions get rewards, bad actions get penalties.",
                                      example="AlphaGo, robots learning to walk, game-playing AI",
                                      tip="Key words: Agent, Environment, Action, Reward."),
     "Reinforcement learning is learning by trial and error, with rewards and penalties."),
    (4, "rl_grid", rl_grid, {},
     "The robot falls into a trap first and gets minus ten. Next time it finds the goal and gets plus ten."),
    (4, "rl_loop", flow, dict(title="The Reinforcement Learning Loop", color=DL_C,
                              steps=[("Agent", AI_C), ("Action", DL_C), ("Environment", MUTED), ("Reward / Penalty", ML_C)],
                              loop=True, note="Goal: get the maximum total reward"),
     "The agent takes an action, the environment gives a reward, and the loop repeats."),
    (4, "types_table", table, dict(title="3 Types: Summary", color=ML_C,
                                   headers=["Type", "Data", "Goal", "Example"], hcolors=[TXT, AI_C, ML_C, DL_C],
                                   rows=[["Supervised", "Labelled", "Predict the answer", "Spam filter"],
                                         ["Unsupervised", "No labels", "Find groups / patterns", "Customer groups"],
                                         ["Reinforcement", "Rewards from environment", "Learn best actions", "Game-playing AI"]]),
     "Here's the summary of all three types. Screenshot this for your exams!"),
    (4, "sort_types", mapping, dict(title="Which type of ML?", color=ML_C,
                                    buckets=[("Supervised", ML_C), ("Unsupervised", AI_C), ("Reinforcement", DL_C)],
                                    items=[("Predict exam marks", 0), ("Customer groups", 1), ("Robot learns to walk", 2),
                                           ("Spam or not spam", 0), ("Unusual bank transactions", 1), ("AI playing games", 2)]),
     "Let's sort these examples into the three types."),
    (4, "quiz_unsupervised", quiz, dict(q="Grouping customers WITHOUT any labels is...",
                                        options=["Supervised learning", "Unsupervised learning", "Reinforcement learning", "Regression"],
                                        answer=1, explain="No labels → Unsupervised (Clustering)."),
     "Quiz! Grouping customers without labels is which type?"),

    # ---- Chapter 5: Algorithms
    (5, "chapter5_card", chapter_card, dict(num=5, title="Popular ML Algorithms", sub="The ones every exam asks about"),
     "Chapter 5. Let's meet the most popular ML algorithms."),
    (5, "define_linear_regression", definition, dict(term="Linear Regression", color=ML_C,
                                                     text="Predicts a NUMBER by fitting the best straight line through the data:  y = m·x + c",
                                                     example="Predict house price from size",
                                                     tip="Output is continuous (any number)."),
     "Linear regression predicts a number by drawing the best straight line."),
    (5, "logistic_sigmoid", sigmoid_scene, {},
     "Logistic regression gives a probability between zero and one. Above 0.5 we say spam."),
    (5, "decision_tree", decision_tree, {},
     "A decision tree asks yes or no questions, step by step, until it reaches an answer."),
    (5, "random_forest", bullets, dict(title="Random Forest: many trees vote", color=ML_C, items=[
        "Builds many decision trees", "Each tree trains on a random part of the data",
        "Every tree votes", "Majority vote = final answer"],
        foot="More accurate and overfits less than one tree"),
     "Random forest builds many trees and lets them vote. The majority wins."),
    (5, "knn", knn, {},
     "KNN looks at the nearest neighbours. Three are cats and two are dogs, so it predicts cat."),
    (5, "define_kmeans", definition, dict(term="K-Means Clustering", color=AI_C,
                                          text="An unsupervised algorithm that splits data into K groups, each around a centre (centroid).",
                                          example="Grouping customers into 3 types",
                                          tip="You must choose K (the number of groups)."),
     "K-Means splits data into K groups. You choose K."),
    (5, "define_svm", definition, dict(term="Support Vector Machine", color=ML_C,
                                       text="A supervised algorithm that draws the boundary with the WIDEST possible gap (margin) between classes.",
                                       example="Text classification, handwriting recognition",
                                       tip="Support vectors = the points closest to the boundary."),
     "SVM draws the boundary with the widest gap between the classes."),
    (5, "algorithms_table", table, dict(title="Algorithms Cheat Sheet", color=ML_C,
                                        headers=["Algorithm", "Type", "Output", "Example"], hcolors=[TXT, AI_C, ML_C, DL_C],
                                        colw=[3.4, 3.0, 3.0, 3.4], size=22,
                                        rows=[["Linear Regression", "Supervised", "Number", "House price"],
                                              ["Logistic Regression", "Supervised", "Category", "Spam or not"],
                                              ["Decision Tree", "Supervised", "Category / Number", "Loan approval"],
                                              ["Random Forest", "Supervised", "Category / Number", "Disease prediction"],
                                              ["KNN", "Supervised", "Category", "Handwritten digits"],
                                              ["K-Means", "Unsupervised", "Groups", "Customer segments"],
                                              ["SVM", "Supervised", "Category", "Text classification"]]),
     "Here's your algorithm cheat sheet. Save it for revision."),
    (5, "quiz_regression", quiz, dict(q="Which algorithm predicts a NUMBER like house price?",
                                      options=["K-Means", "Logistic Regression", "Linear Regression", "KNN"],
                                      answer=2, explain="Regression = number. Logistic Regression is used for classification!"),
     "Quiz! Which algorithm predicts a number?"),

    # ---- Chapter 6: Deep Learning
    (6, "chapter6_card", chapter_card, dict(num=6, title="Deep Learning & Neural Networks", sub="The engine behind ChatGPT and face unlock"),
     "Chapter 6. Now, Deep Learning: the technology behind ChatGPT."),
    (6, "brain_vs_artificial", compare, dict(title="Brain Neuron vs Artificial Neuron", color=DL_C,
                                             left=("Brain neuron", DL_C, ["Dendrites receive signals", "Cell body adds them up",
                                                                          "Fires if the signal is strong", "Axon sends the output"]),
                                             right=("Artificial neuron", AI_C, ["Inputs (x1, x2, x3)", "Weighted sum (Σ w·x + b)",
                                                                                "Activation function", "Output to the next layer"]),
                                             foot="Inspired by the brain, but much simpler!"),
     "An artificial neuron is inspired by brain neurons, but it's much simpler."),
    (6, "neuron", neuron, {},
     "Each input is multiplied by a weight, added up, passed through an activation, and sent forward."),
    (6, "activation_functions", activation, {},
     "Activation functions add curves. ReLU is used in hidden layers, sigmoid gives probabilities."),
    (6, "neural_network", neural_network, {},
     "Connect many neurons in layers and you get a neural network. Many hidden layers means deep learning."),
    (6, "define_deep", definition, dict(term="Why 'Deep'?", color=DL_C,
                                        text="'Deep' means many hidden layers between input and output. More layers can learn more complex patterns.",
                                        tip="1-2 hidden layers = shallow. Many layers = deep."),
     "Why is it called deep? Because it has many hidden layers."),
    (6, "backprop", backprop, {},
     "The network makes a wrong guess, sends the error backward, fixes its weights, and gets it right."),
    (6, "feature_engineering", feature_engineering, {},
     "In ML, humans pick the features. In DL, the network learns the features by itself."),
    (6, "feature_hierarchy", feature_hierarchy, {},
     "Early layers find edges, then shapes, then parts like eyes, and finally a whole face."),
    (6, "cnn_filter", cnn_filter, {},
     "A CNN slides small filters over the image to detect patterns like edges."),
    (6, "network_types", bullets, dict(title="Types of Neural Networks", color=DL_C, items=[
        ("CNN: images and video (face unlock)", AI_C), ("RNN / LSTM: sequences (old speech models)", ML_C),
        ("Transformer: language (ChatGPT, Gemini, Claude)", DL_C), ("GAN / Diffusion: create images", TXT)]),
     "Different networks for different jobs: CNNs for images, Transformers for language."),
    (6, "llm_next_word", llm_tokens, {},
     "LLMs like ChatGPT predict the next word. Attention decides which words matter most."),
    (6, "data_vs_performance", data_vs_perf, {},
     "With small data, traditional ML wins. With big data, deep learning keeps getting better."),
    (6, "dl_needs", bullets, dict(title="What Deep Learning needs", color=DL_C, items=[
        "Huge data (millions of examples)", "Powerful GPUs / TPUs", "Long training (hours to weeks)",
        "Lots of electricity and money"]),
     "Deep learning needs huge data, powerful GPUs and a lot of training time."),
    (6, "cpu_vs_gpu", cpu_vs_gpu, {},
     "A CPU has a few strong cores. A GPU has thousands of small cores, perfect for neural networks."),
    (6, "dl_around_you", bullets, dict(title="Deep Learning around you", color=DL_C, items=[
        "Face unlock on your phone", "Voice assistants (Google Assistant, Siri)", "Google Translate and Google Lens",
        "ChatGPT, Gemini, Claude", "Self-driving cars", "Medical scan analysis"]),
     "You use deep learning every day: face unlock, Google Translate, ChatGPT."),
    (6, "dl_limits", bullets, dict(title="Limitations of Deep Learning", color=BAD, items=[
        "Black box: hard to explain its decisions", "Needs a LOT of data", "Expensive to train",
        "Can be confidently wrong"]),
     "But deep learning has limits: it's a black box, data hungry, and can be confidently wrong."),
    (6, "quiz_deep", quiz, dict(q="Deep Learning is called 'deep' because...",
                                options=["It thinks deeply", "It uses many hidden layers", "It needs deep pockets", "It works underwater"],
                                answer=1, explain="More hidden layers = deeper network."),
     "Quiz! Why is deep learning called deep?"),

    # ---- Chapter 7: Final revision
    (7, "chapter7_card", chapter_card, dict(num=7, title="Final Comparison", sub="Everything in one place, ready for your exam"),
     "Chapter 7. Let's put everything together for your exams."),
    (7, "final_table_1", table, dict(title="AI vs ML vs DL", color=AI_C, size=22,
                                     headers=["", "AI", "ML", "DL"], hcolors=[TXT, AI_C, ML_C, DL_C],
                                     rows=[["Meaning", "Machines acting smart", "Learning from data", "Learning with deep neural networks"],
                                           ["Scope", "Biggest field", "Subset of AI", "Subset of ML"],
                                           ["Data needed", "Can work with rules", "Medium", "Huge"],
                                           ["Features", "Written by humans", "Mostly picked by humans", "Learned automatically"],
                                           ["Example", "Chess engine, GPS", "Spam filter, recommendations", "Face unlock, ChatGPT"]]),
     "Here is the full comparison. Pause and screenshot this one."),
    (7, "final_table_2", table, dict(title="Traditional ML vs Deep Learning", color=DL_C, size=22,
                                     headers=["", "Traditional ML", "Deep Learning"], hcolors=[TXT, ML_C, DL_C],
                                     colw=[3.4, 4.7, 4.7],
                                     rows=[["Hardware", "Normal CPU is fine", "Needs GPUs"],
                                           ["Training time", "Minutes to hours", "Hours to weeks"],
                                           ["Explainable?", "Easier to explain", "Black box"],
                                           ["Best for", "Tables, small data", "Images, audio, text"],
                                           ["With more data", "Stops improving", "Keeps improving"]]),
     "And here is ML versus DL, the most common exam question."),
    (7, "self_driving_levels", bullets, dict(title="One example, 3 levels: a self-driving car", color=AI_C, items=[
        ("AI: the whole car making driving decisions", AI_C),
        ("ML: learns driving patterns from millions of km of data", ML_C),
        ("DL: cameras spot people and signs using CNNs", DL_C)]),
     "One self-driving car uses all three: AI for decisions, ML for patterns, DL for vision."),
    (7, "exam_definitions", bullets, dict(title="Exam: 2-mark answers", color=AI_C, items=[
        ("AI: machines doing tasks that need human intelligence", AI_C),
        ("ML: subset of AI that learns patterns from data", ML_C),
        ("DL: subset of ML using multi-layer neural networks", DL_C),
        "Supervised = labels, Unsupervised = no labels, RL = rewards"]),
     "For 2-mark questions, write these one-line definitions."),
    (7, "exam_differences", bullets, dict(title="Exam: 5 key differences", color=AI_C, items=[
        "1. Scope: DL is inside ML, ML is inside AI", "2. Data: DL needs the most data",
        "3. Features: ML (humans pick) vs DL (learns itself)", "4. Hardware: DL needs GPUs",
        "5. Explainability: ML is easier, DL is a black box"]),
     "For long answers, remember these five differences."),
    (7, "quiz_most_data", quiz, dict(q="Which needs the MOST data and computing power?",
                                     options=["Rule-based AI", "Traditional ML", "Deep Learning", "A calculator"],
                                     answer=2, explain="Deep networks have millions of weights to learn."),
     "Final quiz round! Which needs the most data?"),
    (7, "quiz_netflix", quiz, dict(q="Netflix suggesting movies from your watch history is...",
                                   options=["A rule-based system", "Machine Learning", "Not AI at all", "Hardware"],
                                   answer=1, explain="It learns your taste from data (modern systems also use DL)."),
     "Netflix recommendations: which one is it?"),
    (7, "quiz_robot", quiz, dict(q="A robot learns to walk by getting rewards. This is...",
                                 options=["Supervised learning", "Unsupervised learning", "Reinforcement learning", "Clustering"],
                                 answer=2, explain="Rewards and penalties = Reinforcement Learning."),
     "Last one: a robot learning to walk with rewards?"),
    (7, "recap_circles", nested_circles, dict(title="Recap"),
     "So remember: AI is the big circle, ML is inside it, and DL is inside ML."),
    (7, "outro", outro, dict(nxt="Next: Neural Networks, explained in Telugu"),
     "If this helped, subscribe to AI with Mani and share it with your friends preparing for exams."),
]

assert len(CLIPS) == 80, len(CLIPS)


def _make(idx, ch, fn, kw, is_card):
    def construct(self):
        chrome(self, None if is_card else ch)
        fn(self, **kw)
    return construct


SCENE_NAMES = []
for _i, (_ch, _slug, _fn, _kw, _vo) in enumerate(CLIPS, start=1):
    _name = f"C{_i:02d}_{_slug}"
    _card = _fn in (chapter_card, outro)
    globals()[_name] = type(_name, (Scene,), {"construct": _make(_i, _ch, _fn, _kw, _card)})
    SCENE_NAMES.append(_name)
