"""INT22 – Diện tích giữa hai đường cong.

    python scripts/build_typst.py --ep int22
    python scripts/prepare_voice.py --ep int22 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int22/scene.py INT22
    python scripts/finalize.py --ep int22

One method per narration beat (int22/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Rectangle, ValueTracker, VGroup, Write,
                   always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, band, check, clipped, cross, dashed, dot, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def para(v):
    return v * v


def line(v):
    return v + 2


class INT22(LessonScene):
    EP = 'int22'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def boat(self, shift=0.0):
        a = self.ax((-1.6, 2.6, 1), (-.6 + min(shift, 0), 4.6 + max(shift, 0), 1), (-1, 1, 2), (1, 2, 3, 4))
        self.show_axes(a)
        f, g = (lambda v: para(v) + shift), (lambda v: line(v) + shift)
        self.play(Create(clipped(a, f, -1.6, 2.2, CYAN, 4.5)), Create(clipped(a, g, -1.6, 2.6, GOLD, 4.5)),
                  run_time=self.rt(.06))
        return a

    def strip_sweep(self, a, top, bot, x0, x1, frac):
        xt = ValueTracker(x0 + .05)
        strip = always_redraw(lambda: Rectangle(
            width=abs(a.c2p(.12, 0)[0] - a.c2p(0, 0)[0]),
            height=max(abs(a.c2p(0, top(xt.get_value()))[1] - a.c2p(0, bot(xt.get_value()))[1]), .01),
            fill_color=WHITE, fill_opacity=.55, stroke_width=0).move_to(
            a.c2p(xt.get_value(), (top(xt.get_value()) + bot(xt.get_value())) / 2)))
        self.add(strip)
        self.play(xt.animate.set_value(x1 - .05), run_time=self.rt(frac), rate_func=linear)
        strip.clear_updaters()
        self.play(FadeOut(strip), run_time=self.rt(.03))
        return strip

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.boat()
        self.write_board(self.M('hook', 1.4), frac=.08)
        self.wait_until(.15, t0)
        self.play(FadeIn(band(a, line, para, -1, 2, GREEN, .5)), FadeIn(dot(a, -1, 1)), FadeIn(dot(a, 2, 4)),
                  run_time=self.rt(.1))
        self.write_board(tx('diện tích "chiếc thuyền" = ?', 24, WHITE), frac=.06)
        self.wait_until(.6, t0)
        m = self.M('hook_s', 1.8)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Trên trừ dưới', 'Dải mỏng quét ngang'),
                         ('Ba bước', 'Giao điểm, chia khoảng, thử điểm'),
                         ('Theo biến y', 'Khi biên thay đổi')], t0, fracs=(.1, .38, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.4, 1), (0, 3.4, 1), (), ())
        self.show_axes(a)
        f = lambda v: 2.4 + .4 * math.sin(1.5 * v)  # noqa: E731
        g = lambda v: .6 + .3 * v + .25 * math.sin(2.2 * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 3.3, GOLD, 4.5)), Create(clipped(a, g, 0, 3.3, CYAN, 4.5)),
                  run_time=self.rt(.08))
        self.play(FadeIn(band(a, f, g, .5, 2.8, GREEN, .45)),
                  FadeIn(tx('y = f(x)', 20, GOLD, bold=True).move_to(a.c2p(1.0, 3.15))),
                  FadeIn(tx('y = g(x)', 20, CYAN, bold=True).move_to(a.c2p(2.6, .5))), run_time=self.rt(.08))
        self.write_board(self.heading('DIỆN TÍCH GIỮA HAI ĐƯỜNG'), frac=.05)
        self.wait_until(.4, t0)
        m = self.M('area2', 1.3)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.8, t0)
        self.write_board(tx('g = 0: trở về công thức của tập 21', 22, SOFT), frac=.05)

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.boat()
        self.play(FadeIn(band(a, line, para, -1, 2, GREEN, .3)), run_time=self.rt(.05))
        self.write_board(self.heading('DẢI MỎNG: TRÊN TRỪ DƯỚI'), frac=.05)
        self.strip_sweep(a, line, para, -1, 2, .45)
        self.write_board(self.M('strip', 1.2), tx('y1: đường trên  ·  y2: đường dưới', 22, SOFT), frac=.12)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-1.6, 2.6, 1), (-3.4, 4.6, 1), (-1, 1, 2), (-2, 2, 4), h=5.5)
        self.show_axes(a)
        reg = band(a, line, para, -1, 2, GREEN, .45)
        curves = VGroup(clipped(a, para, -1.6, 2.15, CYAN, 4.5), clipped(a, line, -1.6, 2.6, GOLD, 4.5))
        self.play(Create(curves), FadeIn(reg), run_time=self.rt(.07))
        self.write_board(self.heading('DỜI CẢ HAI ĐỒ THỊ'), self.M('shift', 1.3), frac=.12)
        self.wait_until(.3, t0)
        down = VGroup(curves, reg)
        self.play(down.animate.shift(a.c2p(0, -3)[1] * UP - a.c2p(0, 0)[1] * UP), run_time=self.rt(.15))
        self.write_board(tx('miền nằm dưới trục: diện tích vẫn là 9/2', 22, GREEN, bold=True), frac=.06)
        self.wait_until(.75, t0)
        self.write_board(tx('không cần quan tâm vị trí trục Ox', 22, SOFT), frac=.05)

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 3 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        from common.kit import card
        steps = (('Giao điểm', 'giải f(x) = g(x)', CYAN), ('Chia khoảng', 'thử một điểm: đường nào trên?', GREEN),
                 ('Tích phân', 'trên trừ dưới, cộng lại', GOLD))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.04, .3, .62))):
            c = card(4.05, 3.0, col).move_to([-4.3 + 4.3 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 26, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 18, SOFT, max_w=3.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-1.5, 1.5, 1), (-1.3, 1.3, 1), (-1, 1), (-1, 1), h=4.8)
        self.show_axes(a)
        cub = lambda v: v ** 3  # noqa: E731
        self.play(Create(clipped(a, cub, -1.3, 1.3, CYAN, 4.5, y_min=-1.3, y_max=1.3)),
                  Create(clipped(a, lambda v: v, -1.3, 1.3, GOLD, 4.5)), run_time=self.rt(.07))
        self.write_board(self.heading('CẮT NHAU NHIỀU LẦN'), frac=.05)
        self.wait_until(.25, t0)
        self.play(FadeIn(band(a, cub, lambda v: v, -1, 0, PURPLE, .5)), run_time=self.rt(.05))
        self.write_board(tx('(−1; 0): đường bậc ba ở trên', 22, PURPLE), frac=.05)
        self.play(FadeIn(band(a, lambda v: v, cub, 0, 1, GREEN, .5)), run_time=self.rt(.05))
        self.write_board(tx('(0; 1): đường thẳng ở trên', 22, GREEN), frac=.05)
        self.wait_until(.7, t0)
        self.write_board(tx('một tích phân cho cả đoạn → triệt tiêu!', 23, CORAL, bold=True), frac=.06)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('3 BẪY THƯỜNG GẶP', CORAL, 20)
        rows = [VGroup(cross(CORAL, .26), tx(t, 26, WHITE)).arrange(RIGHT, buff=.25) for t in
                ('lấy dưới trừ trên → ra số âm', 'quên tách khoảng khi hai đường cắt nhau ở giữa',
                 'viết bình phương của (f − g): đó là thể tích, không phải diện tích')]
        self.centre(head, *rows, top=2.0, gap=.6)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, r in zip((.1, .35, .6), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.boat()
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('e1_s0', 1.15), frac=.1)
        self.play(FadeIn(dot(a, -1, 1)), FadeIn(dot(a, 2, 4)), run_time=self.rt(.04))
        self.wait_until(.35, t0)
        self.play(Create(dashed(a.c2p(0, 0), a.c2p(0, 2), color=WHITE)), FadeIn(dot(a, 0, 2, GOLD)),
                  FadeIn(dot(a, 0, 0, CYAN)), run_time=self.rt(.05))
        self.write_board(tx('x = 0: đường thẳng = 2 > 0 = parabol', 22, SOFT), frac=.06)
        self.wait_until(.6, t0)
        self.play(FadeIn(band(a, line, para, -1, 2, GREEN, .5)), run_time=self.rt(.05))
        m = self.M('e1_s1', 1.1)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-1.5, 1.5, 1), (-1.3, 1.3, 1), (-1, 1), (-1, 1), h=4.8)
        self.show_axes(a)
        cub = lambda v: v ** 3  # noqa: E731
        self.play(Create(clipped(a, cub, -1.3, 1.3, CYAN, 4.5, y_min=-1.3, y_max=1.3)),
                  Create(clipped(a, lambda v: v, -1.3, 1.3, GOLD, 4.5)), run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.3), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(band(a, cub, lambda v: v, -1, 0, PURPLE, .5)),
                  FadeIn(band(a, lambda v: v, cub, 0, 1, GREEN, .5)), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        m = self.M('e2_s1', .9)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 1.4, 1), (0, 1.4, 1), (1,), (1,), w=5.2, h=5.2)
        self.show_axes(a)
        self.play(Create(clipped(a, math.sqrt, 0, 1.35, GOLD, 4.5)), Create(clipped(a, para, 0, 1.18, CYAN, 4.5)),
                  run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), self.M('e3_task', 1.3), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(band(a, math.sqrt, para, 0, 1, GREEN, .5)), run_time=self.rt(.06))
        m = self.M('e3_s1', 1.1)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.play(Create(dashed(a.c2p(0, 0), a.c2p(1.35, 1.35), color=SOFT)), run_time=self.rt(.05))
        self.write_board(tx('"chiếc lá" đối xứng qua y = x', 22, SOFT), frac=.05)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 1.5, 1), (0, 3.4, 1), (1,), (1, 2, 3), w=5.0)
        self.show_axes(a)
        self.play(Create(clipped(a, math.exp, 0, 1.2, CYAN, 4.5)),
                  Create(clipped(a, lambda v: math.e, 0, 1.45, GOLD, 4.5)), run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_task', 1.3), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(dot(a, 1, math.e)), FadeIn(band(a, lambda v: math.e, math.exp, 0, 1, GREEN, .5)),
                  run_time=self.rt(.07))
        m = self.M('e4_s1', 1.15)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def e5_axes(self):
        a = self.ax((0, 2.3, 1), (0, 1.6, 1), (1, 2), (1,), w=6.0, h=4.2)
        self.show_axes(a)
        self.play(Create(clipped(a, math.sqrt, 0, 2.2, GOLD, 4.5)), Create(clipped(a, lambda v: 2 - v, .4, 2.2, CYAN, 4.5)),
                  run_time=self.rt(.06))
        return a

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.e5_axes()
        self.write_board(badge('VÍ DỤ 5', GOLD, 20), self.M('e5_task', 1.2), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(band(a, math.sqrt, lambda v: 0, 0, 1, GREEN, .5)),
                  FadeIn(band(a, lambda v: 2 - v, lambda v: 0, 1, 2, PURPLE, .5)),
                  Create(dashed(a.c2p(1, 0), a.c2p(1, 1), color=WHITE)), run_time=self.rt(.08))
        self.write_board(tx('biên trên đổi tại x = 1', 22, SOFT), frac=.05)
        self.wait_until(.6, t0)
        m = self.M('e5_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.e5_axes()
        self.play(FadeIn(band(a, math.sqrt, lambda v: 0, 0, 1, GREEN, .35)),
                  FadeIn(band(a, lambda v: 2 - v, lambda v: 0, 1, 2, GREEN, .35)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 6: THEO BIẾN y', GOLD, 20), frac=.04)
        self.wait_until(.12, t0)
        yt = ValueTracker(.05)
        strip = always_redraw(lambda: Rectangle(
            width=max(abs(a.c2p(2 - yt.get_value(), 0)[0] - a.c2p(yt.get_value() ** 2, 0)[0]), .01),
            height=abs(a.c2p(0, .07)[1] - a.c2p(0, 0)[1]), fill_color=WHITE, fill_opacity=.6, stroke_width=0)
            .move_to(a.c2p((2 - yt.get_value() + yt.get_value() ** 2) / 2, yt.get_value())))
        self.add(strip)
        self.play(yt.animate.set_value(.95), run_time=self.rt(.3), rate_func=linear)
        strip.clear_updaters()
        self.play(FadeOut(strip), run_time=self.rt(.03))
        self.write_board(self.M('e6_s1', 1.15), frac=.1)
        self.wait_until(.65, t0)
        m = self.M('e6_s2', 1.05)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-.3, 2.0, 1), (-1.4, 3.4, 1), (1,), (1, 2, 3), w=5.6)
        self.show_axes(a)
        self.play(Create(clipped(a, para, -.3, 1.8, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 7', GOLD, 20), self.M('e7_task', 1.25), frac=.08)
        self.wait_until(.25, t0)
        self.play(Create(clipped(a, lambda v: 2 * v - 1, -.2, 2.0, GOLD, 4.5)), FadeIn(dot(a, 1, 1)),
                  run_time=self.rt(.07))
        self.wait_until(.45, t0)
        self.play(FadeIn(band(a, para, lambda v: 2 * v - 1, 0, 1, GREEN, .55)), run_time=self.rt(.06))
        m = self.M('e7_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('D giới hạn bởi', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi S là diện tích của D. Xét các mệnh đề sau:', 24, WHITE)
        items = (VGroup(tx('Hai đồ thị cắt nhau tại', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.35), self.M('tf_c', 1.3), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.35, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', .95)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐĐĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.6, 3.6, 1), (0, 9.8, 2), (-2, -1, 1, 2, 3), (2, 4, 6, 8))
        self.show_axes(a)
        self.play(Create(clipped(a, para, -2.6, 3.1, CYAN, 4.5, y_max=9.8)),
                  Create(clipped(a, lambda v: v + 6, -2.6, 3.6, GOLD, 4.5, y_max=9.8)), run_time=self.rt(.06))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.35), tx('(làm tròn đến hàng phần mười)', 21, SOFT), frac=.14)
        self.wait_until(.7, t0)
        self.play(FadeIn(dot(a, -2, 4)), FadeIn(dot(a, 3, 9)), FadeIn(band(a, lambda v: v + 6, para, -2, 3, GREEN, .45)),
                  run_time=self.rt(.08))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('sa_s1', 1.0)
        self.write_board(m, frac=.14)
        self.wait_until(.4, t0)
        self.write_board(self.answer_sheet('20,8'), frac=.06)
        self.wait_until(.7, t0)
        self.write_board(tx('Mẹo parabol – đường thẳng:', 21, GOLD, bold=True), self.M('sa_tip', 1.05), frac=.1)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Trên trừ dưới', 'sum1', 'Diện tích giữa hai đường'),
                                ('Ba bước', 'sum2', 'Giao điểm, chia khoảng, thử điểm'),
                                ('Theo biến y', 'sum3', 'Phải trừ trái khi biên thay đổi')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính S:', 'hw1'), ('Tính S:', 'hw2'), ('Tính S:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Kéo tham số m · diện tích thay đổi trực tiếp', 26, GOLD, bold=True),
                            self.M('next1', 1.3)])


class INT22_SMOKE(INT22):
    smoke = True
