"""INT12 – Định nghĩa tích phân & Newton–Leibniz, diện tích có dấu.

    python scripts/build_typst.py --ep int12
    python scripts/prepare_voice.py --ep int12 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int12/scene.py INT12
    python scripts/finalize.py --ep int12

One method per narration beat (int12/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, RoundedRectangle, VGroup, Write)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import (area, axes, badge, check, clipped, cross, dashed, signed_area, tx)  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL_2, PURPLE, SOFT, STROKE, WHITE  # noqa: E402

PI_LABELS = ((math.pi / 4, 'π/4'), (math.pi / 2, 'π/2'), (math.pi, 'π'), (3 * math.pi / 2, '3π/2'),
             (2 * math.pi, '2π'))


class INT12(LessonScene):
    EP = 'int12'

    def pi_axes(self, xr, yr, yt, labels=PI_LABELS, **kw):
        a = axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                 x_ticks=(), y_ticks=yt, **kw)
        for v, name in labels:
            if xr[0] < v < xr[1] - .1:
                p = a.c2p(v, 0)
                a.labels.add(Line(p + UP * .06, p + DOWN * .06, color=SOFT, stroke_width=2),
                             tx(name, 16, SOFT).move_to(p + DOWN * .3))
        return a

    def plain_axes(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.plain_axes((0, 2.3, 1), (0, 4.6, 1), (1, 2), (1, 2, 3, 4), w=5.0, h=4.6, center=[-3.4, .3, 0])
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, 0, 2.15, CYAN, 4)), FadeIn(area(a, lambda v: v * v, 0, 2, PURPLE, .5)),
                  run_time=self.rt(.08))
        self.play(Write(self.M('hook1', 1.4).move_to([3.0, 1.6, 0])), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        b = self.pi_axes((0, 6.6, 1), (-1.4, 1.4, 1), (-1, 1), w=5.4, h=2.4, center=[3.0, -1.4, 0])
        self.play(FadeIn(b), FadeIn(b.labels), run_time=self.rt(.05))
        self.play(Create(clipped(b, math.sin, 0, 6.5, GOLD, 4)), FadeIn(signed_area(b, math.sin, 0, 2 * math.pi)),
                  run_time=self.rt(.1))
        self.play(FadeIn(tx('?', 40, CORAL, bold=True).move_to(b.c2p(4.7, -.6))), run_time=self.rt(.04))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Định nghĩa', 'Tích phân = F(b) − F(a)'),
                         ('Không phụ thuộc', 'Hằng số C và tên biến'),
                         ('Diện tích có dấu', 'Tích phân có thể âm hoặc bằng 0')], t0, fracs=(.12, .35, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('ĐỊNH NGHĨA', GOLD, 21)
        cond = VGroup(tx('Cho f liên tục trên [a; b],', 24, SOFT), self.M('cond', 1.3)).arrange(RIGHT, buff=.3)
        d = self.M('def', 2.0)
        name = tx('Công thức Newton – Leibniz', 26, GREEN, bold=True)
        self.centre(head, cond, d, name, top=2.6, gap=.6)
        self.play(FadeIn(head), FadeIn(cond[0]), Write(cond[1]), run_time=self.rt(.14))
        self.wait_until(.3, t0)
        self.play(Write(d), run_time=self.rt(.16))
        self.play(FadeIn(self.box(d)), run_time=self.rt(.04))
        self.wait_until(.8, t0)
        self.play(FadeIn(name, shift=UP * .1), run_time=self.rt(.06))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.plain_axes((0, 2.0, 1), (0, 4.2, 1), (1,), (1, 2, 3, 4))
        self.show_axes(a)
        F = lambda v: v ** 3 / 3  # noqa: E731
        for c, col in ((0, CYAN), (2, GREEN)):
            self.play(Create(clipped(a, lambda v, c=c: F(v) + c, 0, 2.0, col, 4)), run_time=self.rt(.06))
            for xv in (.5, 1.6):
                self.add(dashed(a.c2p(xv, 0), a.c2p(xv, F(xv) + c), color=SOFT, stroke_width=1.5))
            gap = Line(a.c2p(1.6, F(.5) + c), a.c2p(1.6, F(1.6) + c), color=GOLD, stroke_width=6)
            self.play(Create(gap), FadeIn(dashed(a.c2p(.5, F(.5) + c), a.c2p(1.6, F(.5) + c), color=GOLD,
                                                 stroke_width=1.5)), run_time=self.rt(.06))
        self.write_board(self.heading('CHỌN NGUYÊN HÀM NÀO CŨNG ĐƯỢC'), self.M('noC', 1.2), frac=.14)
        self.wait_until(.7, t0)
        self.write_board(tx('Hai đoạn vàng bằng nhau → không cần viết C', 23, GOLD, bold=True), frac=.06)

    def beat_c3(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'BIẾN CÂM', ('dummy',), (.06,), (1.6,))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('Tích phân là một CON SỐ', 28, GOLD, bold=True).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.07))

    def beat_c4(self, T):
        self.worked(self.now(), 'BA VÍ DỤ NHANH', ('q1', 'q2', 'q3'), (.04, .35, .68), (1.4, 1.4, 1.4), box_last=False,
                    gap=.38)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((0, 6.8, 1), (-1.5, 1.5, 1), (-1, 1))
        self.ax = a
        self.show_axes(a)
        self.play(Create(clipped(a, math.sin, 0, 6.6, GOLD, 4.5)), run_time=self.rt(.07))
        self.wait_until(.25, t0)
        self.play(FadeIn(area(a, math.sin, 0, math.pi, GREEN, .5)),
                  FadeIn(tx('+2', 30, GREEN, bold=True).move_to(a.c2p(math.pi / 2, .45))), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(FadeIn(area(a, math.sin, math.pi, 2 * math.pi, CORAL, .5)),
                  FadeIn(tx('−2', 30, CORAL, bold=True).move_to(a.c2p(3 * math.pi / 2, -.45))), run_time=self.rt(.08))
        self.wait_until(.75, t0)
        m = self.M('sgn', 1.3)
        self.write_board(self.heading('DIỆN TÍCH CÓ DẤU'), m, frac=.12)

    def beat_c6(self, T):
        t0 = self.now()
        self.write_board(self.M('sgn2', 1.4), frac=.12, gap=.5)
        self.wait_until(.35, t0)
        self.write_board(VGroup(check(), tx('f ≥ 0: tích phân = diện tích', 23, GREEN, bold=True)).arrange(RIGHT, buff=.2),
                         frac=.06)
        self.wait_until(.6, t0)
        self.write_board(VGroup(cross(CORAL, .28), tx('f đổi dấu: tích phân ≠ diện tích', 23, CORAL, bold=True))
                         .arrange(RIGHT, buff=.2), frac=.06)

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.plain_axes((0, 4.4, 1), (-2.5, 2.5, 1), (1, 2, 3, 4), (-2, -1, 1, 2), x_label='t', y_label='v')
        self.show_axes(a)
        v = lambda u: 2 - u  # noqa: E731
        self.play(Create(clipped(a, v, 0, 4.2, CYAN, 4.5)), run_time=self.rt(.06))
        self.play(FadeIn(signed_area(a, v, 0, 4)), run_time=self.rt(.07))
        self.play(FadeIn(tx('tiến: +2', 22, GREEN, bold=True).move_to(a.c2p(.8, .55))),
                  FadeIn(tx('lùi: −2', 22, CORAL, bold=True).move_to(a.c2p(3.2, -.55))), run_time=self.rt(.05))
        self.write_board(self.heading('Ý NGHĨA VẬT LÝ'), self.M('phys1', 1.3), tx('Δs: độ dời = 2 − 2 = 0', 22, WHITE),
                         frac=.14)
        self.wait_until(.6, t0)
        self.write_board(self.M('phys2', 1.3), tx('L: quãng đường = 2 + 2 = 4', 22, GOLD, bold=True), frac=.1)

    def beat_c8(self, T):
        self.worked(self.now(), 'HAI QUY ƯỚC VỀ CẬN', ('conv1', 'conv2'), (.1, .45), (1.8, 1.8), box_last=False, gap=.8)

    def beat_c9(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'NGUYÊN HÀM ≠ TÍCH PHÂN', ('nh_vs_tp',), (.06,), (1.5,), box_last=False)
        wrong = VGroup(cross(CORAL, .32), tx('Viết "tích phân = x³ + C" là sai trình bày', 24, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).next_to(lines[-1], DOWN, buff=.9)
        self.wait_until(.55, t0)
        self.play(FadeIn(wrong, shift=UP * .1), run_time=self.rt(.07))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1',), (.05,), (1.6,), gap=.8)

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.pi_axes((0, 1.9, 1), (-1.4, 1.4, 1), (-1, 1))
        self.show_axes(a)
        f = lambda v: math.cos(2 * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 1.85, CYAN, 4.5)), run_time=self.rt(.06))
        m = self.M('e2', 1.15)
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), m, frac=.16)
        self.wait_until(.55, t0)
        self.play(FadeIn(signed_area(a, f, 0, math.pi / 2)), run_time=self.rt(.08))
        self.write_board(tx('phần dương và phần âm bù trừ nhau', 23, GOLD, bold=True), frac=.06)

    def beat_e3(self, T):
        self.worked(self.now(), 'VÍ DỤ 3', ('e3',), (.05,), (1.7,), gap=.8)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.plain_axes((-1.4, 2.3, 1), (-1.5, 3.5, 1), (-1, 1, 2), (-1, 1, 2, 3))
        self.show_axes(a)
        f = lambda v: v * v - 1  # noqa: E731
        self.play(Create(clipped(a, f, -1.4, 2.25, CYAN, 4.5)), run_time=self.rt(.06))
        m = self.M('e4', 1.0)
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), m, frac=.16)
        self.wait_until(.55, t0)
        self.play(FadeIn(signed_area(a, f, -1, 2)), run_time=self.rt(.07))
        self.play(FadeIn(tx('−4/3', 24, CORAL, bold=True).move_to(a.c2p(0, -.45))),
                  FadeIn(tx('+4/3', 24, GREEN, bold=True).move_to(a.c2p(1.75, .65))), run_time=self.rt(.05))
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_f', 1.4)).arrange(RIGHT, buff=.25)
        l2 = tx('S là diện tích hình phẳng giới hạn bởi đồ thị f, trục Ox, x = 0, x = 3. Xét:', 23, WHITE)
        items = (self.M('tf_a', 1.4), self.M('tf_b', 1.4), self.M('tf_c', 1.4), self.M('tf_d', 1.4))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .7))

    def beat_x2(self, T):
        t0 = self.now()
        sol = self.M('tf_ab_calc', 1.3).move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.tf_pause), Write(sol), self.tf_mark(0, True), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.07))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.3)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.12))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.07))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.plain_axes((0, 2.3, 1), (0, 10, 1), (1, 2), (2, 4, 6, 8))
        self.show_axes(a, .04)
        f = lambda v: 3 * v * v - 2 * v + 1  # noqa: E731
        self.play(Create(clipped(a, f, 0, 2.2, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), frac=.12)
        self.wait_until(.45, t0)
        self.play(FadeIn(area(a, f, 0, 2, PURPLE, .5)), run_time=self.rt(.06))
        self.write_board(self.M('sa_s1', 1.25), self.answer_sheet('6'), frac=.14)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        body = RoundedRectangle(width=4.0, height=5.6, corner_radius=.3, fill_color='#1A2840', fill_opacity=1,
                                stroke_color=STROKE, stroke_width=2).move_to([LEFT_CX, -.15, 0])
        screen = RoundedRectangle(width=3.4, height=1.7, corner_radius=.12, fill_color='#C9D8C5', fill_opacity=1,
                                  stroke_width=0).move_to(body.get_top() + DOWN * 1.15)
        keys = VGroup(*[RoundedRectangle(width=.6, height=.38, corner_radius=.07, fill_color=PANEL_2,
                                         fill_opacity=1, stroke_color=STROKE, stroke_width=1)
                        for _ in range(20)]).arrange_in_grid(5, 4, buff=(.18, .16)).next_to(screen, DOWN, buff=.35)
        keys[2].set_fill(GOLD, .8)
        expr = self.M('casio', 1.0).set_color('#14202B').move_to(screen)
        self.play(FadeIn(body), FadeIn(screen), FadeIn(keys), run_time=self.rt(.06))
        self.write_board(badge('MẸO: PHÍM TÍCH PHÂN', GOLD, 19),
                         tx('Nhập hàm số, cận dưới, cận trên', 23, WHITE), tx('→ máy cho ngay kết quả số', 23, WHITE),
                         frac=.14)
        self.wait_until(.4, t0)
        self.play(FadeIn(expr), run_time=self.rt(.06))
        self.write_board(VGroup(check(), tx('Dùng để kiểm tra đáp số', 23, GREEN, bold=True)).arrange(RIGHT, buff=.2),
                         frac=.06)
        self.wait_until(.75, t0)
        self.write_board(tx('Lượng giác: chuyển sang chế độ Radian', 23, CORAL, bold=True), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Newton–Leibniz', 'sum1', 'F là một nguyên hàm bất kỳ'),
                                ('Không phụ thuộc C', 'sum2', 'Cũng không phụ thuộc tên biến'),
                                ('Diện tích có dấu', 'sum3', 'Có thể âm hoặc bằng 0')),
                           fracs=(.04, .4, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Tính', 'hw2'), ('Tính', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .25, .45))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.1), self.M('next2', 1.1)])


class INT12_SMOKE(INT12):
    smoke = True
