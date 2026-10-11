"""INT10 – Từ tốc độ thay đổi đến đại lượng & tổng ôn Phần A.

    python scripts/build_typst.py --ep int10
    python scripts/prepare_voice.py --ep int10 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int10/scene.py INT10
    python scripts/finalize.py --ep int10

One method per narration beat (int10/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Brace, Create, Dot, FadeIn, FadeOut, Line, ValueTracker, VGroup,
                   Write, always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, car, card, clipped, dashed, dot, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

ROAD_Y = -2.65


def pop(t):
    return 2500 * math.exp(.02 * t) + 7500


def cost(x):
    return .15 * x * x + 20 * x + 500


def temp(t):
    return 20 * math.exp(-.1 * t) + 70


def brake_s(t):
    return 20 * t - 2.5 * t * t


class INT10(LessonScene):
    EP = 'int10'

    def left_axes(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 5.5), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX + .3, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        items = (('Đồng hồ tốc độ', 'vị trí của xe', CYAN), ('Tốc độ tăng dân số', 'dân số', GREEN),
                 ('Chi phí biên', 'tổng chi phí', GOLD), ('Tốc độ nguội', 'nhiệt độ', CORAL))
        for i, (rate, qty, col) in enumerate(items):
            r, c = divmod(i, 2)
            box = card(5.6, 1.7, col).move_to([-3.1 + 6.2 * c, 1.3 - 2.0 * r, 0])
            g = VGroup(box, tx(rate, 24, col, bold=True).move_to(box.get_center() + UP * .35),
                       tx('→  ' + qty, 23, WHITE).move_to(box.get_center() + DOWN * .35))
            self.wait_until((.06, .16, .26, .36)[i], t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(FadeIn(tx('NGUYÊN HÀM: cầu nối từ tốc độ thay đổi về đại lượng', 25, GOLD, bold=True)
                         .move_to([0, -2.6, 0]), shift=UP * .1), run_time=self.rt(.07))

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        self.title_card()
        self.wait_until(.6, t0)
        self.play(FadeIn(badge('TỔNG ÔN PHẦN A · NGUYÊN HÀM', GREEN, 19).move_to([0, -2.6, 0]), shift=UP * .1),
                  run_time=self.rt(.06))

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Quy trình chung', 'Tốc độ + giá trị ban đầu → đại lượng'),
                         ('Đơn vị & hằng số C', 'C thường là giá trị ban đầu'),
                         ('Bốn mô hình', 'Dân số · chi phí · nhiệt độ · chuyển động')], t0, fracs=(.12, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        self.worked(self.now(), 'QUY TRÌNH CHUNG', ('proc1', 'proc2'), (.1, .5), (1.7, 1.6), gap=.9)

    def beat_c2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'ĐƠN VỊ', ('unit1',), (.08,), (1.8,), box_last=False)
        ex = tx('người/năm  ×  năm  =  người', 30, GOLD, bold=True).next_to(lines[-1], DOWN, buff=.8)
        self.wait_until(.35, t0)
        self.play(FadeIn(ex, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('C mang đơn vị của Q, thường chính là giá trị ban đầu', 24, GREEN, bold=True)
                         .next_to(ex, DOWN, buff=.6)), run_time=self.rt(.07))

    def beat_c3(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'ĐỘ THAY ĐỔI', ('diff1',), (.1,), (1.25,))
        self.wait_until(.45, t0)
        self.play(FadeIn(tx('Hai chữ C triệt tiêu: không cần điều kiện ban đầu', 24, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.07))
        self.wait_until(.78, t0)
        self.play(FadeIn(badge('hạt giống của TÍCH PHÂN – Phần B', PURPLE, 20).move_to([0, -2.3, 0]), shift=UP * .1),
                  run_time=self.rt(.06))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        h1 = tx('TỐC ĐỘ THAY ĐỔI', 22, CYAN, bold=True).move_to([-3.0, 2.5, 0])
        h2 = tx('ĐẠI LƯỢNG', 22, GOLD, bold=True).move_to([3.0, 2.5, 0])
        self.play(FadeIn(h1), FadeIn(h2), run_time=self.rt(.04))
        rows = (('vận tốc v(t)', 'vị trí s(t)'), ("chi phí biên C′(x)", 'tổng chi phí C(x)'),
                ("tốc độ tăng P′(t)", 'dân số P(t)'), ('lưu lượng r(t)', 'thể tích V(t)'))
        for i, (a, b) in enumerate(rows):
            y = 1.5 - 1.05 * i
            g = VGroup(card(4.8, .85, CYAN).move_to([-3.0, y, 0]), tx(a, 23, WHITE).move_to([-3.0, y, 0]),
                       tx('∫ →', 24, GOLD, bold=True).move_to([0, y, 0]),
                       card(4.8, .85, GOLD).move_to([3.0, y, 0]), tx(b, 23, WHITE).move_to([3.0, y, 0]))
            self.wait_until((.15, .3, .5, .65)[i], t0)
            self.play(FadeIn(g, shift=UP * .1), run_time=self.rt(.06))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.left_axes((0, 10.5, 1), (0, 620, 100), (2, 4, 6, 8, 10), (100, 300, 500), x_label='t (năm)',
                           y_label='ΔP', label_size=15)
        self.ax = a
        self.show_axes(a)
        self.write_board(badge('MÔ HÌNH 1 · DÂN SỐ', GREEN, 19), self.M('p_task', 1.3), frac=.14)
        self.wait_until(.45, t0)
        self.write_board(self.M('p_s1', 1.0), frac=.14)
        self.play(Create(clipped(a, lambda u: pop(u) - 10000, 0, 10.5, GREEN, 4.5)), run_time=self.rt(.08))

    def beat_e2(self, T):
        t0 = self.now()
        a = self.ax
        res = self.M('p_s2', 1.25)
        self.write_board(res, frac=.1)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.03))
        tau = ValueTracker(0)
        pt = always_redraw(lambda: Dot(a.c2p(tau.get_value(), pop(tau.get_value()) - 10000), radius=.08, color=GOLD))
        info = always_redraw(lambda: tx(f't = {vn(tau.get_value(), 1)} năm   P ≈ {round(pop(tau.get_value()))} người',
                                        23, WHITE).move_to([BOARD_X, -1.9, 0], aligned_edge=LEFT))
        self.play(FadeIn(pt), FadeIn(info), run_time=self.rt(.03))
        self.play(tau.animate.set_value(10), run_time=self.rt(.5), rate_func=linear)
        pt.clear_updaters()
        info.clear_updaters()

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.left_axes((0, 220, 10), (0, 11500, 1000), (50, 100, 150, 200), (2000, 6000, 10000), x_label='x',
                           y_label='C', label_size=14)
        self.ax = a
        self.show_axes(a)
        self.write_board(badge('MÔ HÌNH 2 · CHI PHÍ BIÊN', GOLD, 19), self.M('c_task', 1.3), frac=.14)
        self.wait_until(.6, t0)
        self.write_board(self.M('c_s1', 1.4), frac=.1)
        self.play(Create(clipped(a, cost, 0, 220, GOLD, 4.5)), run_time=self.rt(.08))

    def beat_e4(self, T):
        t0 = self.now()
        a = self.ax
        p1, p2 = dot(a, 100, cost(100), CYAN, .09), dot(a, 200, cost(200), CYAN, .09)
        guides = VGroup(dashed(a.c2p(100, 0), a.c2p(100, cost(100)), color=SOFT, stroke_width=2),
                        dashed(a.c2p(200, 0), a.c2p(200, cost(200)), color=SOFT, stroke_width=2),
                        dashed(a.c2p(100, cost(100)), a.c2p(200, cost(100)), color=SOFT, stroke_width=2))
        self.play(FadeIn(p1), FadeIn(p2), Create(guides), run_time=self.rt(.08))
        jump = Line(a.c2p(200, cost(100)), a.c2p(200, cost(200)), color=CORAL, stroke_width=6)
        br = Brace(jump, RIGHT, color=CORAL)
        self.wait_until(.3, t0)
        self.play(Create(jump), FadeIn(br), FadeIn(tx('6500', 22, CORAL, bold=True).next_to(br, RIGHT, buff=.05)),
                  run_time=self.rt(.08))
        res = self.M('c_s2', 1.35)
        self.write_board(res, frac=.1)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.write_board(tx('chi phí cố định 500 đã triệt tiêu', 22, GREEN, bold=True), frac=.06)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.left_axes((0, 42, 5), (0, 100, 10), (10, 20, 30, 40), (20, 40, 60, 80), x_label='t (phút)',
                           y_label='T', label_size=14)
        self.show_axes(a)
        self.write_board(badge('MÔ HÌNH 3 · NHIỆT ĐỘ', CORAL, 19), self.M('t_task', 1.3), frac=.12)
        room = VGroup(dashed(a.c2p(0, 70), a.c2p(42, 70), color=CYAN, stroke_width=2),
                      tx('70 °C', 16, CYAN).move_to(a.c2p(38, 74)))
        self.wait_until(.3, t0)
        self.write_board(self.M('t_s1', 1.4), frac=.1)
        self.play(Create(clipped(a, temp, 0, 42, CORAL, 4.5)), FadeIn(room), run_time=self.rt(.1))
        self.wait_until(.58, t0)
        res = self.M('t_s2', 1.35)
        self.write_board(res, frac=.08)
        self.play(FadeIn(dot(a, 10, temp(10), GOLD, .09)), FadeIn(self.box(res)), run_time=self.rt(.04))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.left_axes((0, 4.6, 1), (0, 46, 5), (1, 2, 3, 4), (10, 20, 30, 40), h=3.9, center=[LEFT_CX, .75, 0],
                           x_label='t (s)', y_label='s (m)', label_size=14)
        self.show_axes(a)
        road = VGroup(Line([-6.3, ROAD_Y, 0], [6.3, ROAD_Y, 0], color=SOFT, stroke_width=3))
        for m in range(0, 49, 8):
            px = -6.0 + 12.0 * m / 48
            road.add(Line([px, ROAD_Y - .08, 0], [px, ROAD_Y + .08, 0], color=SOFT, stroke_width=2),
                     tx(str(m), 14, SOFT).move_to([px, ROAD_Y - .28, 0]))
        tau = ValueTracker(0)
        vehicle = car(CORAL, .7)
        vehicle.add_updater(lambda m: m.move_to([-6.0 + 12.0 * brake_s(tau.get_value()) / 48, ROAD_Y + .3, 0]))
        self.play(Create(road), FadeIn(vehicle), run_time=self.rt(.05))
        self.write_board(badge('MÔ HÌNH 4 · PHANH XE', CYAN, 19), self.M('b_task', 1.3), frac=.1)
        self.wait_until(.3, t0)
        self.write_board(self.M('b_s1', 1.2), frac=.1)
        self.play(Create(clipped(a, brake_s, 0, 4, CYAN, 4.5)), run_time=self.rt(.06))
        self.play(tau.animate.set_value(4), run_time=self.rt(.25), rate_func=lambda r: 1 - (1 - r) ** 2)
        vehicle.clear_updaters()
        res = self.M('b_s2', 1.4)
        self.write_board(res, frac=.06)
        self.play(FadeIn(self.box(res)), FadeIn(dot(a, 4, 40, GOLD, .09)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Dân số:', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('(t tính bằng năm, P tính bằng người). Xét các mệnh đề:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.07))
        self.wait_until(.35, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.15)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), self.tf_mark(3, False), run_time=self.rt(.14))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐĐĐS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.left_axes((0, 4.4, 1), (0, 2.5, 1), (1, 2, 3, 4), (.5, 1, 1.5, 2), x_label='t (năm)',
                           y_label='h (m)', label_size=15)
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.1), frac=.12)
        self.wait_until(.55, t0)
        self.write_board(self.M('sa_s1', 1.35), frac=.08)
        self.play(Create(clipped(a, lambda u: math.log(u + 1) + .5, 0, 4.4, GREEN, 4.5)), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        v = math.log(5) + .5
        self.play(FadeIn(dot(a, 4, v, GOLD, .09)), Create(dashed(a.c2p(4, 0), a.c2p(4, v), color=GOLD,
                                                                 stroke_width=2)), run_time=self.rt(.03))
        self.write_board(self.M('sa_s2', 1.3), self.answer_sheet('2,11'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('BẢN ĐỒ CHỌN PHƯƠNG PHÁP · PHẦN A', GOLD, 21).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        rows = (('Tổng, hiệu', 'tách từng hạng tử theo bảng', CYAN), ('f(ax + b)', 'chia cho a', GREEN),
                ('Phân thức', 'chia đa thức / tách phân thức', GOLD), ('f(u)·u′', 'đổi biến số', PURPLE),
                ('Tích khác loại', 'từng phần', CORAL), ('Có điều kiện', 'thay vào tìm C', WHITE))
        for i, (k, v, col) in enumerate(rows):
            y = 1.85 - .82 * i
            g = VGroup(card(11.6, .7, col).move_to([0, y, 0]), tx(k, 22, col, bold=True).move_to([-3.7, y, 0]),
                       tx('→  ' + v, 22, WHITE).move_to([1.4, y, 0]))
            self.wait_until(.08 + .13 * i, t0)
            self.play(FadeIn(g, shift=UP * .1), run_time=self.rt(.05))

    def beat_x6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = tx('NHÌN LẠI PHẦN A', 26, GOLD, bold=True).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        names = ('Bản chất nguyên hàm', 'Tính chất & lũy thừa', '1/x và hàm mũ', 'Lượng giác', 'Quy tắc f(ax + b)',
                 'Có điều kiện, từng khúc', 'Phân thức hữu tỉ', 'Đổi biến số', 'Từng phần')
        cols = (CYAN, GREEN, GOLD)
        cells = VGroup()
        for i, n in enumerate(names):
            r, c = divmod(i, 3)
            box = card(3.9, 1.25, cols[c]).move_to([-4.1 + 4.1 * c, 1.5 - 1.45 * r, 0])
            cells.add(VGroup(box, tx(f'INT{i + 1:02d}', 18, cols[c], bold=True).move_to(box.get_center() + UP * .27),
                             tx(n, 19, WHITE, max_w=3.6).move_to(box.get_center() + DOWN * .2)))
        for i, cl in enumerate(cells):
            self.wait_until(.05 + .07 * i, t0)
            self.play(FadeIn(cl, scale=1.05), run_time=self.rt(.035))
        self.wait_until(.8, t0)
        self.play(FadeIn(badge('INT10 · Tốc độ thay đổi → đại lượng', PURPLE, 20).move_to([0, -2.75, 0])),
                  run_time=self.rt(.05))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Đại lượng', 'sum1', 'Nguyên hàm của tốc độ thay đổi'),
                                ('Hằng số C', 'sum2', 'Từ giá trị ban đầu, mang đơn vị của Q'),
                                ('Độ thay đổi', 'sum3', 'Không phụ thuộc C')),
                           fracs=(.04, .4, .68))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Chuyển động:', 'hw1'), ('Doanh thu:', 'hw2'), ('Bể nước:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .35, .65), show_answers=.88)

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.15), self.M('next2', 1.15)])


class INT10_SMOKE(INT10):
    smoke = True

