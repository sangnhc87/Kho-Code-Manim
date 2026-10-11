"""INT24 – Đọc diện tích từ đồ thị f'.

    python scripts/build_typst.py --ep int24
    python scripts/prepare_voice.py --ep int24 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int24/scene.py INT24
    python scripts/finalize.py --ep int24

One method per narration beat (int24/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, FadeOut, Line, ValueTracker, VGroup, Write,
                   always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, check, clipped, cross, dashed, dot, signed_area, tx, vn  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def fp_hook(v):
    """Witness f' of the hook: area +4 on [0, 2], −7 on [2, 5]."""
    return 3 * v * (2 - v) if v <= 2 else 14 / 9 * (v - 2) * (v - 5)


def f_hook(v):
    if v <= 2:
        return 3 * v * v - v ** 3
    prim = lambda t: t ** 3 / 3 - 3.5 * t * t + 10 * t  # noqa: E731
    return 4 + 14 / 9 * (prim(v) - prim(2))


class INT24(LessonScene):
    EP = 'int24'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def hook_axes(self, h=5.3, center=None):
        a = self.ax((0, 5.4, 1), (-4, 3.6, 1), (1, 2, 3, 4, 5), (), h=h, y_label="f'",
                    center=center or [LEFT_CX, -.1, 0])
        self.show_axes(a)
        self.play(Create(clipped(a, fp_hook, 0, 5.2, CYAN, 4.5)), run_time=self.rt(.05))
        return a

    def ladder(self, values, x=4.9, base=-.2, unit=.32, color=GOLD):
        """Vertical number line for f-values given relative to a reference (label → offset)."""
        lo, hi = min(values.values()), max(values.values())
        line = Line([x, base + unit * lo - .3, 0], [x, base + unit * hi + .3, 0], color=SOFT, stroke_width=3)
        marks = VGroup()
        for label, v in values.items():
            y = base + unit * v
            marks.add(VGroup(Dot([x, y, 0], radius=.07, color=color),
                             tx(label, 21, WHITE).next_to([x, y, 0], RIGHT, buff=.18)))
        return line, marks

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.hook_axes()
        self.play(FadeIn(signed_area(a, fp_hook, 0, 5, opacity=.5)), run_time=self.rt(.06))
        self.play(FadeIn(tx('S1 = 4', 22, WHITE, bold=True).move_to(a.c2p(1, 1.2))),
                  FadeIn(tx('S2 = 7', 22, WHITE, bold=True).move_to(a.c2p(3.5, -1.4))), run_time=self.rt(.05))
        self.write_board(self.heading("CHỈ CÓ ĐỒ THỊ f'"), self.M('hook', 1.0), frac=.12)
        self.wait_until(.45, t0)
        self.write_board(tx('Sắp xếp:', 23, WHITE), self.M('hook_q', 1.3), frac=.1)
        self.wait_until(.8, t0)
        self.write_board(tx('không cần công thức của f!', 24, GOLD, bold=True), frac=.06)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([("Diện tích dưới f'", 'Là độ biến thiên của f'),
                         ('So sánh', 'Giá trị lớn nhất, nhỏ nhất'),
                         ('Hình học', 'Tam giác, hình thang, cung tròn')], t0, fracs=(.1, .38, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'NEWTON – LEIBNIZ ĐỌC NGƯỢC', ('nl',), (.08,), (1.7,))
        self.wait_until(.55, t0)
        self.play(FadeIn(tx("diện tích có dấu dưới f'  =  f tăng / giảm bao nhiêu", 26, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.9)), run_time=self.rt(.06))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        top = self.ax((0, 5.4, 1), (-4, 3.6, 2), (1, 2, 3, 4, 5), (), h=2.6, y_label="f'", center=[LEFT_CX, 1.45, 0])
        bot = self.ax((0, 5.4, 1), (-3.6, 4.8, 2), (1, 2, 3, 4, 5), (), h=2.6, y_label='f', center=[LEFT_CX, -1.7, 0])
        self.show_axes(top)
        self.show_axes(bot)
        self.play(Create(clipped(top, fp_hook, 0, 5.2, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(self.M('up', 1.2), self.M('down', 1.2), frac=.12)
        xt = ValueTracker(.01)
        live = always_redraw(lambda: VGroup(
            signed_area(top, fp_hook, 0, max(xt.get_value(), .02), opacity=.5, samples=80),
            clipped(bot, f_hook, 0, max(xt.get_value(), .02), GOLD, 4.5),
            Dot(bot.c2p(xt.get_value(), f_hook(xt.get_value())), radius=.08, color=GOLD),
            dashed(top.c2p(xt.get_value(), 0), bot.c2p(xt.get_value(), f_hook(xt.get_value())), color=SOFT,
                   stroke_width=1.5)))
        self.add(live)
        self.wait_until(.3, t0)
        self.play(xt.animate.set_value(5), run_time=self.rt(.55), rate_func=linear)
        live.clear_updaters()
        self.write_board(tx('mỗi mảnh: một bước lên hoặc xuống của f', 22, GOLD), frac=.05)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH SO SÁNH', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        from common.kit import card
        steps = (("Dấu của f'", 'bảng biến thiên của f', CYAN), ('Đọc diện tích', 'từng mảnh trên / dưới', GREEN),
                 ('Quy về gốc', 'f(c) = f(a) ± S rồi so sánh', GOLD))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.05, .25, .45))):
            c = card(4.05, 3.0, col).move_to([-4.3 + 4.3 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 26, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 18, SOFT, max_w=3.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('LỚN NHẤT – NHỎ NHẤT', GOLD, 20)
        r1 = VGroup(tx("f' đổi dấu + → −", 26, GREEN, bold=True), tx('cực đại', 26, WHITE)).arrange(RIGHT, buff=.4)
        r2 = VGroup(tx("f' đổi dấu − → +", 26, CORAL, bold=True), tx('cực tiểu', 26, WHITE)).arrange(RIGHT, buff=.4)
        r3 = tx('So với hai đầu mút: lại dùng diện tích!', 26, GOLD, bold=True)
        self.centre(head, r1, r2, r3, top=2.0, gap=.6)
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.wait_until(.05, t0)
        self.play(FadeIn(r1, shift=RIGHT * .2), run_time=self.rt(.05))
        self.wait_until(.25, t0)
        self.play(FadeIn(r2, shift=RIGHT * .2), run_time=self.rt(.05))
        self.wait_until(.55, t0)
        self.play(FadeIn(r3), run_time=self.rt(.05))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        shapes = VGroup()
        for i, (name, col) in enumerate((('tam giác', CYAN), ('hình thang', GREEN), ('1/4 hình tròn', GOLD))):
            a = axes((0, 2.4, 1), (0, 2.4, 1), 3.4, 2.8, center=[-4.3 + 4.3 * i, .3, 0], x_label='', y_label='')
            f = (lambda v: v, lambda v: .8 + .4 * v, lambda v: math.sqrt(max(0, 4 - v * v)))[i]
            shapes.add(VGroup(a, a.labels, clipped(a, f, 0, 2, col, 4), area(a, f, 0, 2, col, .45, samples=80),
                              tx(name, 22, col, bold=True).next_to(a, DOWN, buff=.25)))
        for i, g in enumerate(shapes):
            self.wait_until((.05, .2, .35)[i], t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('đề thường vẽ trên lưới ô vuông → đếm ô', 25, SOFT).move_to([0, -2.45, 0])),
                  run_time=self.rt(.05))

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge("BẪY: NHẦM f VỚI f'", CORAL, 20)
        rows = (VGroup(cross(CORAL, .26), tx("f' nằm trên trục  ≠  f dương", 27, WHITE)).arrange(RIGHT, buff=.25),
                VGroup(check(GREEN, .28), tx("f' nằm trên trục  →  f đang tăng", 27, GREEN)).arrange(RIGHT, buff=.25),
                VGroup(cross(CORAL, .26), tx("đỉnh của f'  ≠  cực đại của f", 27, WHITE)).arrange(RIGHT, buff=.25),
                VGroup(check(GREEN, .28), tx("đỉnh của f'  →  f tăng nhanh nhất", 27, GREEN)).arrange(RIGHT, buff=.25))
        self.centre(head, *rows, top=2.3, gap=.5)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, r in zip((.05, .3, .5, .7), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.hook_axes()
        self.play(FadeIn(signed_area(a, fp_hook, 0, 5, opacity=.5)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('root', 1.05), frac=.12)
        self.wait_until(.4, t0)
        line, marks = self.ladder({'f(0)': 0, 'f(2)': 4, 'f(5)': -3}, x=1.6, base=-.55, unit=.27)
        self.play(Create(line), run_time=self.rt(.03))
        for mk in marks:
            self.play(FadeIn(mk, shift=LEFT * .1), run_time=self.rt(.04))
        self.wait_until(.75, t0)
        m = self.M('e1_s1', 1.0).move_to([3.9, -2.62, 0])
        self.play(Write(m), run_time=self.rt(.1))
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-.2, 3.4, 1), (-1.4, 2.4, 1), (1, 2, 3), (-1, 1, 2), y_label="f'")
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v - 1, 0, 3, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.25), frac=.08)
        self.wait_until(.25, t0)
        self.play(FadeIn(signed_area(a, lambda v: v - 1, 0, 3, opacity=.5)),
                  FadeIn(tx('1/2', 20, WHITE, bold=True).move_to(a.c2p(.35, -.3))),
                  FadeIn(tx('2', 22, WHITE, bold=True).move_to(a.c2p(2.3, .55))), run_time=self.rt(.06))
        self.write_board(self.M('e2_s1', 1.0), frac=.12)
        self.wait_until(.7, t0)
        m = self.M('e2_s2', 1.15)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 2.5, 1), (0, 2.5, 1), (1, 2), (1, 2), w=5.0, h=5.0, y_label="f'")
        self.show_axes(a)
        q = lambda v: math.sqrt(max(0, 4 - v * v))  # noqa: E731
        self.play(Create(clipped(a, q, 0, 2, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), self.M('e3_task', 1.2), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(area(a, q, 0, 2, GOLD, .5, samples=120)),
                  FadeIn(tx('π', 34, WHITE, bold=True).move_to(a.c2p(.85, .85))), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        m = self.M('e3_s1', 1.1)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        g = lambda v: v * v - 2 * v  # noqa: E731
        a = self.ax((-1.3, 3.4, 1), (-1.4, 3.4, 1), (-1, 1, 2, 3), (-1, 1, 2, 3), y_label="f'")
        self.show_axes(a)
        self.play(Create(clipped(a, g, -1.2, 3.2, CYAN, 4.5)), FadeIn(signed_area(a, g, -1, 3, opacity=.5)),
                  run_time=self.rt(.07))
        for xv, yv in ((-.45, .45), (1, -.45), (2.55, .45)):
            self.add(tx('4/3', 19, WHITE, bold=True).move_to(a.c2p(xv, yv)))
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_task', 1.2), frac=.08)
        self.wait_until(.3, t0)
        self.write_board(self.M('e4_s1', .85), frac=.12)
        self.wait_until(.65, t0)
        m = self.M('e4_s2', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(badge('MẸO: TRỤC SỐ DỌC CHO f', GOLD, 20).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        line, marks = self.ladder({'f(1) = f(0) + 3': 3, 'f(0)': 0, 'f(4) = f(0) − 2': -2, 'f(6) = f(0) + 2': 2},
                                  x=-1.5, base=-.2, unit=.6)
        self.play(Create(line), run_time=self.rt(.05))
        for frac, mk in zip((.15, .3, .45, .6), (marks[1], marks[0], marks[2], marks[3])):
            self.wait_until(frac, t0)
            self.play(FadeIn(mk, shift=LEFT * .1), run_time=self.rt(.05))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('thứ tự trên trục = đáp án so sánh', 25, GREEN, bold=True).move_to([0, -2.6, 0])),
                  run_time=self.rt(.05))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 5.4, 1), (-2.6, 5.6, 1), (1, 2, 3, 4, 5), (-2, 1, 3, 5), y_label='f')
        self.show_axes(a)
        self.write_board(badge('VÍ DỤ 5: ĐẾM NGHIỆM', GOLD, 20), self.M('e6_s1', 1.15), frac=.1)
        self.wait_until(.2, t0)
        self.play(Create(clipped(a, lambda v: 1 + f_hook(v), 0, 5, GOLD, 4.5)), run_time=self.rt(.25))
        for xv, yv in ((0, 1), (2, 5), (5, -2)):
            self.add(dot(a, xv, yv))
        self.wait_until(.6, t0)
        lo, hi = 2.0, 5.0  # bisection for the single root on (2; 5) (counted exactly in lesson.validate())
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if 1 + f_hook(mid) > 0 else (lo, mid)
        root = (lo + hi) / 2
        self.play(FadeIn(dot(a, root, 1 + f_hook(root), CORAL, .1)), run_time=self.rt(.04))
        self.write_board(tx('f giảm từ 5 xuống −2: cắt Ox đúng 1 lần', 22, GREEN, bold=True),
                         tx('→ phương trình f(x) = 0 có đúng 1 nghiệm', 22, GOLD, bold=True), frac=.1)

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 2.3, 1), (-.4, 4.6, 1), (1, 2), (1, 2, 3, 4), y_label="f'")
        self.show_axes(a)
        sq = lambda v: v * v  # noqa: E731
        self.play(Create(clipped(a, sq, 0, 2.1, CYAN, 4.5)),
                  Create(clipped(a, lambda v: 1, 0, 2.3, GOLD, 4)), run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 6: g = f − x', GOLD, 20), self.M('e7_s1', 1.2), frac=.1)
        self.wait_until(.3, t0)
        from common.kit import band
        self.play(FadeIn(band(a, lambda v: 1, sq, 0, 1, CORAL, .55)), FadeIn(band(a, sq, lambda v: 1, 1, 2, GREEN, .55)),
                  run_time=self.rt(.08))
        self.write_board(tx("diện tích giữa f' và đường y = 1", 22, SOFT), frac=.05)
        self.wait_until(.62, t0)
        m = self.M('e7_s2', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx("Đồ thị f' trên [0; 6]:", 24, WHITE), self.M('tf_given', 1.05)).arrange(RIGHT, buff=.25)
        l2 = tx('(S1, S3 trên trục; S2 dưới trục). Xét các mệnh đề sau:', 23, WHITE)
        items = (VGroup(tx('f đồng biến trên', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.35), self.M('tf_c', 1.35), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.5, .78))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c, d)', 22, SOFT), self.M('tf_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(3, False), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-.2, 4.4, 1), (-.6, 6.6, 1), (1, 2, 3, 4), (2, 4, 6), y_label="f'")
        self.show_axes(a)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), tx('Tính f(4).', 23, WHITE), frac=.12)
        self.wait_until(.45, t0)
        self.play(FadeIn(dot(a, 1, 0)), FadeIn(dot(a, 3, 4)),
                  Create(clipped(a, lambda v: 2 * (v - 1), 0, 4.2, CYAN, 4.5, y_min=-.6, y_max=6.6)), run_time=self.rt(.1))
        self.x4_axes = a

    def beat_x5(self, T):
        t0 = self.now()
        a = self.x4_axes
        self.play(FadeIn(area(a, lambda v: 2 * (v - 1), 1, 4, GREEN, .5)),
                  FadeIn(tx('9', 30, WHITE, bold=True).move_to(a.c2p(3.0, 1.6))), run_time=self.rt(.08))
        self.clear_board(.03)
        m = self.M('sa_s1', 1.0)
        self.write_board(m, frac=.14)
        self.wait_until(.6, t0)
        self.write_board(self.answer_sheet('14'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Diện tích = biến thiên', 'sum1', "Đọc từ đồ thị f'"),
                                ('So sánh', 'sum2', 'Quy về một giá trị gốc'),
                                ('Đừng nhầm', 'sum3', "f' dương: f tăng, không phải f dương")),
                           fracs=(.04, .35, .6))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('So sánh:', 'hw1'), ('Tính:', 'hw2'), ('Tìm:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Cắt lát · xếp chồng · cộng dồn', 26, GOLD, bold=True), self.M('next1', 1.4)])


class INT24_SMOKE(INT24):
    smoke = True
