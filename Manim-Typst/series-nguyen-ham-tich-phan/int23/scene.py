"""INT23 – Diện tích hình ghép & bài toán tham số.

    python scripts/build_typst.py --ep int23
    python scripts/prepare_voice.py --ep int23 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int23/scene.py INT23
    python scripts/finalize.py --ep int23

One method per narration beat (int23/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, ValueTracker, VGroup, Write,
                   always_redraw, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, band, card, clipped, cross, dashed, dot, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def cap(v):
    return 4 - v * v


M_HALF = 4 - 2 * 2 ** (1 / 3)


class INT23(LessonScene):
    EP = 'int23'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def cap_axes(self):
        a = self.ax((-2.5, 2.5, 1), (-.4, 4.6, 1), (-2, -1, 1, 2), (1, 2, 3, 4))
        self.show_axes(a)
        self.play(Create(clipped(a, cap, -2.3, 2.3, CYAN, 4.5)), run_time=self.rt(.05))
        return a

    def live_split(self, a, mt):
        """Region under the cap split by y = m: gold above, green below; live readout of both areas."""
        def parts():
            mv = mt.get_value()
            w = math.sqrt(max(4 - mv, 1e-6))
            upper = band(a, cap, lambda v: mv, -w, w, GOLD, .55)
            lower = VGroup(area(a, cap, -2, -w, GREEN, .45), area(a, lambda v: mv, -w, w, GREEN, .45),
                           area(a, cap, w, 2, GREEN, .45))
            ln = Line(a.c2p(-2.4, mv), a.c2p(2.4, mv), color=WHITE, stroke_width=3)
            return VGroup(lower, upper, ln)
        return always_redraw(parts)

    def readout(self, mt, fn, label, color=GOLD, at=(BOARD_X, -1.9)):
        return always_redraw(lambda: tx(f'{label} = {vn(fn(mt.get_value()), 2)}', 24, color, bold=True)
                             .move_to([at[0], at[1], 0], aligned_edge=LEFT))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.cap_axes()
        self.write_board(self.M('hook', 1.2), frac=.08)
        self.play(FadeIn(area(a, cap, -2, 2, GREEN, .45)), run_time=self.rt(.05))
        self.wait_until(.25, t0)
        mt = ValueTracker(.2)
        live = self.live_split(a, mt)
        top = self.readout(mt, lambda mv: 4 / 3 * (4 - mv) ** 1.5, 'phần trên', GOLD, (BOARD_X, -.8))
        self.add(live, top)
        self.play(mt.animate.set_value(3.2), run_time=self.rt(.22), rate_func=smooth)
        self.play(mt.animate.set_value(M_HALF), run_time=self.rt(.12), rate_func=smooth)
        live.clear_updaters()
        top.clear_updaters()
        self.wait_until(.8, t0)
        m = self.M('hook_q', 1.05)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Hình ghép', 'Cộng các miền, hoặc lớn trừ thừa'),
                         ('Tham số', 'Diện tích là hàm S(m)'),
                         ('Tối ưu', 'Công thức nhanh a·d³/6')], t0, fracs=(.1, .35, .6))

    # ================================================================ PHẦN 1
    def comp_axes(self):
        a = self.ax((0, 4.6, 1), (-.4, 2.6, 1), (1, 2, 3, 4), (1, 2), h=4.6)
        self.show_axes(a)
        self.play(Create(clipped(a, math.sqrt, 0, 4.5, GOLD, 4.5)),
                  Create(clipped(a, lambda v: v - 2, 1.8, 4.5, CYAN, 4.5)), run_time=self.rt(.06))
        return a

    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.comp_axes()
        self.write_board(self.heading('HÌNH GHÉP'), tx('cộng các miền đơn giản, hoặc lớn trừ thừa', 22, SOFT), frac=.1)
        self.wait_until(.45, t0)
        big = area(a, math.sqrt, 0, 4, GREEN, .45)
        tri = area(a, lambda v: v - 2, 2, 4, CORAL, .7)
        self.play(FadeIn(big), run_time=self.rt(.06))
        self.play(FadeIn(tri), run_time=self.rt(.06))
        self.write_board(self.M('comp', 1.0), frac=.12)

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.4, 1), (0, 9.6, 2), (1, 2, 3), (2, 4, 6, 8))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, 0, 3.1, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(self.heading('THAM SỐ TRONG CẬN'), frac=.04)
        at = ValueTracker(.6)
        live = always_redraw(lambda: VGroup(area(a, lambda v: v * v, 0, at.get_value(), GOLD, .5),
                                            Line(a.c2p(at.get_value(), 0), a.c2p(at.get_value(), 9.4), color=WHITE,
                                                 stroke_width=3)))
        rd = self.readout(at, lambda av: av ** 3 / 3, 'S(a)', GOLD, (BOARD_X, -1.0))
        self.add(live, rd)
        self.play(at.animate.set_value(3), run_time=self.rt(.3), rate_func=smooth)
        live.clear_updaters()
        rd.clear_updaters()
        self.wait_until(.55, t0)
        m = self.M('pa', 1.05)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-.3, 3.3, 1), (-.4, 9.6, 2), (1, 2, 3), (2, 4, 6, 8))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, -.3, 3.1, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(self.heading('THAM SỐ TRONG HÀM: y = mx'), frac=.04)
        mt = ValueTracker(1)
        live = always_redraw(lambda: VGroup(
            band(a, lambda v: mt.get_value() * v, lambda v: v * v, 0, mt.get_value(), GOLD, .55),
            clipped(a, lambda v: mt.get_value() * v, -.2, 3.3, GOLD, 4, y_max=9.6)))
        rd = self.readout(mt, lambda mv: mv ** 3 / 6, 'S(m)', GOLD, (BOARD_X, -1.0))
        self.add(live, rd)
        self.wait_until(.25, t0)
        self.write_board(self.M('pm', 1.05), frac=.1)
        self.play(mt.animate.set_value(3), run_time=self.rt(.35), rate_func=smooth)
        live.clear_updaters()
        rd.clear_updaters()
        self.write_board(tx('m tăng → S tăng theo lập phương', 22, SOFT), frac=.05)

    def beat_c4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CÔNG THỨC NHANH', ('quick',), (.15,), (1.7,))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('parabol hệ số a cắt đường thẳng tại x1, x2', 25, SOFT)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def through_line(self, a, kt):
        def build():
            kv = kt.get_value()
            d = math.sqrt(kv * kv - 4 * kv + 8)
            x1, x2 = (kv - d) / 2, (kv + d) / 2
            ln = lambda v: kv * (v - 1) + 2  # noqa: E731
            return VGroup(band(a, ln, lambda v: v * v, x1, x2, GOLD, .55),
                          clipped(a, ln, -2.4, 3.4, GOLD, 4, y_min=-.5, y_max=9.4))
        return always_redraw(build)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-2.4, 3.4, 1), (-.5, 9.4, 2), (-2, -1, 1, 2, 3), (2, 4, 6, 8))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, -2.4, 3.05, CYAN, 4.5, y_max=9.4)), FadeIn(dot(a, 1, 2, WHITE)),
                  run_time=self.rt(.06))
        self.write_board(self.heading('XOAY ĐƯỜNG THẲNG QUA (1; 2)'), frac=.05)
        kt = ValueTracker(-1.5)
        live = self.through_line(a, kt)
        rd = self.readout(kt, lambda kv: (kv * kv - 4 * kv + 8) ** 1.5 / 6, 'S', GOLD, (BOARD_X, -.6))
        self.add(live, rd)
        self.play(kt.animate.set_value(5), run_time=self.rt(.3), rate_func=smooth)
        self.play(kt.animate.set_value(2), run_time=self.rt(.2), rate_func=smooth)
        live.clear_updaters()
        rd.clear_updaters()
        self.write_board(self.M('opt', 1.2), frac=.08)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('pm', 'e1_s1'), (.05, .4), (1.4, 1.5), gap=.7)

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_s1',), (.25,), (1.4,))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.cap_axes()
        mt = ValueTracker(M_HALF)
        live = self.live_split(a, mt)
        self.add(live)
        live.clear_updaters()
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), tx('giao điểm: x = ±√(4 − m)', 22, SOFT), frac=.08)
        self.wait_until(.45, t0)
        m = self.M('e3_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'VÍ DỤ 3 (TIẾP)', ('e4_s1', 'e4_s2'), (.05, .4), (1.35, 1.5), gap=.7)
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('thấp hơn giữa chiều cao (m = 2): phần dưới rộng hơn', 24, SOFT)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_e5(self, T):
        self.worked(self.now(), 'VÍ DỤ 4: DIỆN TÍCH NHỎ NHẤT', ('e5_s1',), (.25,), (1.25,), box_last=False)

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.4, 3.4, 1), (-.5, 9.4, 2), (-2, -1, 1, 2, 3), (2, 4, 6, 8))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, -2.4, 3.05, CYAN, 4.5, y_max=9.4)), FadeIn(dot(a, 1, 2, WHITE)),
                  run_time=self.rt(.05))
        kt = ValueTracker(2)
        live = self.through_line(a, kt)
        self.add(live)
        live.clear_updaters()
        self.write_board(self.M('e6_s1', 1.1), frac=.12)
        self.wait_until(.55, t0)
        m = self.M('e6_s2', 1.1)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.comp_axes()
        self.write_board(badge('VÍ DỤ 5', GOLD, 20), tx('y = √x, y = x − 2, trục Ox', 23, WHITE), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(area(a, math.sqrt, 0, 4, GREEN, .45)), run_time=self.rt(.06))
        self.write_board(tx('dưới √x từ 0 đến 4: 16/3', 22, GREEN), frac=.05)
        self.wait_until(.55, t0)
        self.play(FadeIn(area(a, lambda v: v - 2, 2, 4, CORAL, .75)), run_time=self.rt(.06))
        self.write_board(tx('trừ tam giác: 2', 22, CORAL), frac=.05)
        self.wait_until(.75, t0)
        m = self.M('e7_s1', 1.5)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('S(m) là diện tích hình phẳng giới hạn bởi hai đường. Xét các mệnh đề:', 23, WHITE)
        items = (VGroup(tx('Giao tại', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.35), self.M('tf_c', 1.35), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.4, .75))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', .95)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.4, 2.4, 1), (-.5, 5.4, 1), (-2, -1, 1, 2), (1, 2, 3, 4, 5))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, -2.3, 2.3, CYAN, 4.5, y_max=5.4)), FadeIn(dot(a, 0, 1, WHITE)),
                  run_time=self.rt(.06))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), tx('S nhỏ nhất = ? (làm tròn đến hàng phần trăm)', 21, SOFT), frac=.14)
        kt = ValueTracker(-2)

        def build():
            kv = kt.get_value()
            d = math.sqrt(kv * kv + 4)
            ln = lambda v: kv * v + 1  # noqa: E731
            return VGroup(band(a, ln, lambda v: v * v, (kv - d) / 2, (kv + d) / 2, GOLD, .55),
                          clipped(a, ln, -2.4, 2.4, GOLD, 4, y_min=-.5, y_max=5.4))
        live = always_redraw(build)
        self.add(live)
        self.wait_until(.45, t0)
        self.play(kt.animate.set_value(2), run_time=self.rt(.25), rate_func=smooth)
        self.play(kt.animate.set_value(0), run_time=self.rt(.15), rate_func=smooth)
        live.clear_updaters()

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', 1.15), frac=.1)
        self.wait_until(.3, t0)
        m = self.M('sa_s2', 1.1)
        self.write_board(m, frac=.12)
        self.wait_until(.7, t0)
        self.write_board(self.answer_sheet('1,33'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Hình ghép', 'sum1', 'Cộng các phần, hoặc lớn trừ thừa'),
                                ('Tham số', 'sum2', 'Viết S(m) rồi giải phương trình'),
                                ('Tối ưu', 'sum3', 'Tìm khoảng cách d nhỏ nhất')),
                           fracs=(.04, .33, .58))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm m:', 'hw1'), ('Tìm a:', 'hw2'), ('Tìm m:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .4, .6))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx("Diện tích dưới đồ thị f' = độ biến thiên của f", 26, GOLD, bold=True),
                            self.M('next1', 1.3)])


class INT23_SMOKE(INT23):
    smoke = True
