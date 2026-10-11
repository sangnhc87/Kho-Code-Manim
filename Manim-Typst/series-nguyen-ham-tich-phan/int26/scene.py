"""INT26 – Thể tích khối tròn xoay quanh Ox: phương pháp đĩa.

    python scripts/build_typst.py --ep int26
    python scripts/prepare_voice.py --ep int26 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int26/scene.py INT26
    python scripts/finalize.py --ep int26

One method per narration beat (int26/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().

Solids of revolution are drawn in 2D: the profile y = ±f(x) plus thin
ellipses (discs seen slightly from the side). Rotation is suggested by
squashing the region with cos θ.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, ValueTracker, VGroup, Write, always_redraw, linear

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.revolve import disc, region, solid  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT26(LessonScene):
    EP = 'int26'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def spin(self, a, f, x0, x1, frac, color=CYAN):
        """Rotate the region once around Ox (squash with cos θ), leaving the solid behind."""
        th = ValueTracker(0)
        live = always_redraw(lambda: region(a, f, x0, x1, math.cos(th.get_value()), color, .5))
        self.add(live)
        self.play(th.animate.set_value(2 * math.pi), run_time=self.rt(frac), rate_func=linear)
        live.clear_updaters()
        self.remove(live)
        body = solid(a, f, x0, x1, color=color)
        self.add(body)
        return body

    def slide_disc(self, a, f, x0, x1, frac, label='S(x) = πf²', area=None):
        xt = ValueTracker(x0 + .02)
        live = always_redraw(lambda: disc(a, f, xt.get_value()))
        rd = always_redraw(lambda: tx(f'{label} = {vn(area(xt.get_value()), 2)}', 22, GOLD, bold=True)
                           .move_to([BOARD_X, -2.2, 0], aligned_edge=LEFT))
        self.add(live, rd)
        self.play(xt.animate.set_value(x1 - .02), run_time=self.rt(frac), rate_func=linear)
        live.clear_updaters()
        rd.clear_updaters()
        return VGroup(live, rd)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.ax((0, 4.6, 1), (-2.4, 2.4, 1), (1, 2, 3, 4), (-2, -1, 1, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, math.sqrt, 0, 4.3, CYAN, 4.5)), FadeIn(region(a, math.sqrt, 0, 4)),
                  run_time=self.rt(.08))
        self.write_board(self.M('hook', 1.1), frac=.08)
        self.wait_until(.2, t0)
        self.spin(a, math.sqrt, 0, 4, .35)
        self.write_board(tx('giống một chiếc chén', 23, SOFT), tx('Thể tích = ?', 26, WHITE, bold=True), frac=.08)
        self.wait_until(.75, t0)
        m = self.M('hook_v', 1.7)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('V = π∫f²', 'Phương pháp đĩa'),
                         ('Bẫy bình phương', 'Bình phương đúng, nhớ nhân π'),
                         ('Nón và cầu', 'Chứng minh bằng tích phân')], t0, fracs=(.1, .38, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        f = lambda v: 1.0 + .5 * math.sin(1.1 * v) + .15 * v  # noqa: E731
        a = self.ax((0, 4.6, 1), (-2.4, 2.4, 1), (), ())
        self.show_axes(a)
        self.play(Create(clipped(a, f, 0, 4.3, CYAN, 4.5)), FadeIn(region(a, f, .3, 4)), run_time=self.rt(.07))
        self.write_board(self.heading('MỖI ĐIỂM VẠCH MỘT ĐƯỜNG TRÒN'), frac=.05)
        self.wait_until(.2, t0)
        self.spin(a, f, .3, 4, .25)
        self.write_board(tx('thiết diện tại x: hình tròn bán kính f(x)', 22, WHITE),
                         frac=.06)
        self.wait_until(.6, t0)
        self.slide_disc(a, f, .3, 4, .2, 'πf²', lambda v: math.pi * f(v) ** 2)
        self.write_board(self.M('disc', 1.4), frac=.06)

    def beat_c2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'PHƯƠNG PHÁP ĐĨA', ('vol',), (.25,), (1.8,))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('mỗi lát mỏng là một chiếc đĩa tròn', 26, SOFT).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.05))

    def beat_c2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        cards = []
        for i, (title, key, col, note) in enumerate((('DIỆN TÍCH', 'cmp_s', GREEN, 'không π, không bình phương'),
                                                    ('THỂ TÍCH (quay quanh Ox)', 'cmp_v', GOLD, 'có π, có bình phương'))):
            c = card(5.9, 3.4, col).move_to([-3.1 + 6.2 * i, .1, 0])
            g = VGroup(c, tx(title, 24, col, bold=True).move_to(c.get_top() + DOWN * .55),
                       self.M(key, 1.25, max_w=5.4).move_to(c.get_center() + DOWN * .05),
                       tx(note, 21, SOFT).move_to(c.get_bottom() + UP * .5))
            cards.append(g)
        self.play(FadeIn(cards[0], shift=UP * .2), run_time=self.rt(.07))
        self.wait_until(.35, t0)
        self.play(FadeIn(cards[1], shift=UP * .2), run_time=self.rt(.07))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('thường hỏi cả hai trong một câu đúng sai', 25, CORAL, bold=True).move_to([0, -2.4, 0])),
                  run_time=self.rt(.05))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 4 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('f, a, b', 'xác định hàm và cận', CYAN), ('Bình phương', 'rút gọn f²', CORAL),
                 ('Tích phân', 'tính từ a đến b', GREEN), ('Nhân π', 'đừng quên!', CORAL))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.05, .2, .35, .5))):
            c = card(3.0, 3.0, col).move_to([-4.65 + 3.1 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 25, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 18, SOFT, max_w=2.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('lỗi hay nằm ở bước 2 và bước 4', 25, CORAL, bold=True).move_to([0, -2.45, 0])),
                  run_time=self.rt(.04))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        g = lambda v: v * v - 2 * v  # noqa: E731
        a = self.ax((0, 2.4, 1), (-1.4, 1.4, 1), (1, 2), (-1, 1))
        self.show_axes(a)
        self.play(Create(clipped(a, g, 0, 2.2, CYAN, 4.5)), FadeIn(region(a, g, 0, 2, color=CORAL)),
                  run_time=self.rt(.07))
        self.write_board(self.heading('MIỀN DƯỚI TRỤC'), frac=.04)
        self.wait_until(.2, t0)
        self.spin(a, g, 0, 2, .3, CORAL)
        self.write_board(tx('quay vẫn cho cùng một khối', 23, WHITE), self.M('neg', 1.5),
                         tx('không cần tách cận như diện tích', 22, GREEN, bold=True), frac=.12)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BA BẪY VỀ BÌNH PHƯƠNG', CORAL, 20)
        rows = [self.M(k, 1.3) for k in ('trap1', 'trap2', 'trap3')]
        self.centre(head, *rows, top=2.4, gap=.6)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, m in zip((.08, .28, .55), rows):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.08))

    # ================================================================ PHẦN 2
    def example(self, t0, tag, f, x0, x1, xr, yr, xt, yt, key, scale=1.1, color=CYAN, spin_frac=.3, fracs=(.12, .55)):
        self.clear_stage(.05)
        a = self.ax(xr, yr, xt, yt)
        self.show_axes(a)
        self.play(Create(clipped(a, f, max(xr[0], x0 - .2), min(xr[1], x1 + .2), color, 4.5,
                                 y_min=yr[0], y_max=yr[1])), FadeIn(region(a, f, x0, x1, color=color)),
                  run_time=self.rt(.07))
        self.write_board(badge(tag, GOLD, 20), frac=.04)
        self.wait_until(fracs[0], t0)
        self.spin(a, f, x0, x1, spin_frac, color)
        self.wait_until(fracs[1], t0)
        m = self.M(key, scale)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        return a

    def beat_e1(self, T):
        self.example(self.now(), 'VÍ DỤ 1', math.sqrt, 0, 4, (0, 4.6, 1), (-2.4, 2.4, 1), (1, 2, 3, 4), (-2, 2),
                     'e1_s1', 1.0, fracs=(.08, .45))

    def beat_e2(self, T):
        a = self.example(self.now(), 'VÍ DỤ 2: HÌNH NÓN', lambda v: .5 * v, 0, 4, (0, 4.6, 1), (-2.4, 2.4, 1), (), (),
                         'e2_s1', 1.15, GOLD, fracs=(.1, .55))
        self.add(tx('r', 22, WHITE).move_to(a.c2p(4.25, 1)), tx('h', 22, WHITE).move_to(a.c2p(2, -.3)))

    def beat_e3(self, T):
        self.example(self.now(), 'VÍ DỤ 3: HÌNH CẦU', lambda v: math.sqrt(max(0, 4 - v * v)), -2, 2,
                     (-2.6, 2.6, 1), (-2.6, 2.6, 1), (), (), 'e3_s1', 1.15, GREEN, fracs=(.12, .6))

    def beat_e4(self, T):
        self.example(self.now(), 'VÍ DỤ 4', math.sin, 0, math.pi, (0, 3.6, 1), (-1.4, 1.4, 1), (1, 2, 3), (-1, 1),
                     'e4_s1', .9, PURPLE, fracs=(.1, .5))

    def beat_e5(self, T):
        self.example(self.now(), 'VÍ DỤ 5', math.exp, 0, 1, (0, 1.4, 1), (-3, 3, 1), (1,), (-2, 2), 'e5_s1', 1.2,
                     GOLD, fracs=(.1, .5))

    def beat_e6(self, T):
        self.example(self.now(), 'VÍ DỤ 6', lambda v: v * v - 2 * v, 0, 2, (0, 2.4, 1), (-1.4, 1.4, 1), (1, 2), (-1, 1),
                     'e6_s1', 1.1, CORAL, fracs=(.15, .55))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 4.6, 1), (-2.4, 2.4, 1), (1, 2, 3, 4), (-2, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, math.sqrt, 0, 4.4, CYAN, 4.5)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 7: TÌM CẬN', GOLD, 20), tx('quay y = √x, x ∈ [0; a] được V = 8π', 22, WHITE), frac=.08)
        at = ValueTracker(1)
        live = always_redraw(lambda: VGroup(region(a, math.sqrt, 0, at.get_value(), opacity=.35),
                                            solid(a, math.sqrt, 0, at.get_value(), n=10)))
        rd = always_redraw(lambda: tx(f'a = {vn(at.get_value(), 2)}   V = {vn(math.pi * at.get_value() ** 2 / 2, 2)}', 22,
                                      GOLD, bold=True).move_to([BOARD_X, -2.2, 0], aligned_edge=LEFT))
        self.add(live, rd)
        self.wait_until(.25, t0)
        self.play(at.animate.set_value(4), run_time=self.rt(.3), rate_func=linear)
        live.clear_updaters()
        rd.clear_updaters()
        m = self.M('e7_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e8(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'KIỂM TRA BẰNG MÁY TÍNH', ('vol', 'e8_s1'), (.08, .45), (1.35, 1.4), box_last=False, gap=.5)
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('trắc nghiệm: bấm từng phương án để so sánh', 25, GREEN, bold=True)
                         .next_to(lines[-1], DOWN, buff=.5)), run_time=self.rt(.05))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('H giới hạn bởi', 24, WHITE), self.M('tf_given', 1.3),
                    tx('; quay H quanh Ox.', 24, WHITE)).arrange(RIGHT, buff=.2)
        l2 = tx('Gọi V là thể tích khối tròn xoay. Xét các mệnh đề:', 24, WHITE)
        items = (VGroup(tx('H cắt Ox tại', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.3), self.M('tf_c', 1.3), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .75))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 3.4, 1), (-1.4, 1.4, 1), (1, 2, 3), (-1, 1))
        self.show_axes(a)
        inv = lambda v: 1 / v  # noqa: E731
        self.play(Create(clipped(a, inv, .75, 3.3, CYAN, 4.5)), FadeIn(region(a, inv, 1, 3)), run_time=self.rt(.07))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), tx('quay quanh Ox · làm tròn đến hàng phần trăm', 21, SOFT), frac=.14)
        self.wait_until(.5, t0)
        self.spin(a, inv, 1, 3, .35)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', .95), frac=.14)
        self.wait_until(.7, t0)
        self.write_board(self.answer_sheet('2,09'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Phương pháp đĩa', 'sum1', 'Thiết diện là hình tròn'),
                                ('Bình phương đúng', 'sum2', 'Và nhớ nhân π'),
                                ('Nón và cầu', 'sum3', 'Chứng minh bằng tích phân')),
                           fracs=(.04, .4, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Quay:', 'hw1'), ('Quay:', 'hw2'), ('Quay:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Đĩa có lỗ ở giữa · vành khăn', 26, GOLD, bold=True), self.M('next1', 1.4)])


class INT26_SMOKE(INT26):
    smoke = True
