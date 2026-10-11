"""INT06 – Nguyên hàm có điều kiện & hàm từng khúc.

    python scripts/build_typst.py --ep int06
    python scripts/prepare_voice.py --ep int06 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int06/scene.py INT06
    python scripts/finalize.py --ep int06

One method per narration beat (int06/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, FadeOut, GrowArrow, Indicate, Line,
                   ValueTracker, VGroup, Write, always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, car, card, clipped, cross, dashed, dot, para, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

ROAD_Y = -2.6


def s_car(t):
    return t * t if t <= 3 else 6 * t - 9


def v_car(t):
    return 2 * t if t <= 3 else 6.0


class INT06(LessonScene):
    EP = 'int06'

    def std_axes(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.55), center=kw.pop('center', [LEFT_CX, -.12, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def piece_axes(self):
        return self.std_axes((-1.5, 2.6, 1), (-2, 8.5, 1), (-1, 1, 2), (2, 4, 6, 8))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.std_axes((0, 6, 1), (0, 7.5, 1), (1, 2, 3, 4, 5), (2, 4, 6), x_label='t (s)', y_label='v (m/s)')
        self.show_axes(a)
        rise = clipped(a, lambda u: 2 * u, 0, 3, CYAN, 5)
        flat = clipped(a, lambda u: 6, 3, 6, GOLD, 5)
        self.play(Create(rise), run_time=self.rt(.1))
        self.play(Create(flat), run_time=self.rt(.08))
        self.write_board(self.heading('VẬN TỐC CHO THEO TỪNG KHÚC'), self.M('hook_v', 1.5), frac=.14)
        self.wait_until(.55, t0)
        self.write_board(tx('Vị trí s(t) = ?', 28, GOLD, bold=True), frac=.06, gap=.5)
        self.wait_until(.78, t0)
        self.write_board(para('Nối các mảnh sao cho xe không "dịch chuyển tức thời".', 23, SOFT, width=30), frac=.07)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Điều kiện → C', 'Một hay nhiều điều kiện, mỗi lần thay là một C'),
                         ('Nguyên hàm hai lần', 'Gia tốc → vận tốc → vị trí'),
                         ('Hàm từng khúc', 'Mỗi khúc một C, hàn bằng tính liên tục')], t0, fracs=(.12, .36, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2.2, 2.2, 1), (-2, 7, 1), (-2, -1, 1, 2), (2, 4, 6))
        self.show_axes(a)
        self.write_board(badge('DẠNG 1', CYAN, 19), self.M('c1_a', 1.4), frac=.12)
        fam = VGroup(*[clipped(a, lambda v, k=k: v * v + k, -2.2, 2.2, SOFT, 2).set_stroke(opacity=.35)
                       for k in (-1, 0, 1, 3, 4)])
        self.play(Create(fam), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('c1_b', 1.25), frac=.12)
        self.wait_until(.68, t0)
        chosen = clipped(a, lambda v: v * v + 2, -2.2, 2.2, GOLD, 5)
        p = dot(a, 1, 3, GOLD, .1)
        self.play(Create(chosen), FadeIn(p), FadeIn(tx('(x₀; y₀)', 19, GOLD, bold=True).next_to(p, RIGHT, buff=.12)),
                  run_time=self.rt(.1))

    def beat_c2(self, T):
        self.worked(self.now(), 'NHIỀU GIÁ TRỊ TRONG MỘT ĐIỀU KIỆN', ('c2_task', 'c2_s1', 'c2_s2'), (.06, .4, .6),
                    (1.6, 1.6, 1.6), gap=.55)

    def beat_c3(self, T):
        self.worked(self.now(), 'DẠNG 2: NGUYÊN HÀM HAI LẦN', ('c3_task', 'c3_s1', 'c3_s2', 'c3_s3'),
                    (.04, .3, .56, .78), (1.5, 1.5, 1.5, 1.6), gap=.42)

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        top = self.M('chain', 1.9).move_to([0, 2.2, 0])
        self.play(Write(top), run_time=self.rt(.1))
        names = (('GIA TỐC', 'a(t)', CORAL), ('VẬN TỐC', 'v(t)', CYAN), ('VỊ TRÍ', 's(t)', GOLD))
        boxes = VGroup()
        for i, (lab, sym, col) in enumerate(names):
            c = card(3.2, 1.5, col).move_to([-4.4 + 4.4 * i, .1, 0])
            boxes.add(VGroup(c, tx(lab, 19, SOFT, bold=True).move_to(c.get_top() + DOWN * .32),
                             tx(sym, 34, WHITE, slant=True).move_to(c.get_center() + DOWN * .15)))
        arrows = VGroup()
        for i, (cst, cond) in enumerate((('+ C₁', 'cần v(0)'), ('+ C₂', 'cần s(0)'))):
            ar = Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), color=GOLD, buff=.1, stroke_width=5)
            arrows.add(VGroup(ar, tx('∫  ' + cst, 20, GOLD, bold=True).next_to(ar, UP, buff=.08),
                              tx(cond, 18, GREEN).next_to(ar, DOWN, buff=.1)))
        self.play(FadeIn(boxes[0], shift=UP * .15), run_time=self.rt(.06))
        for i in range(2):
            self.wait_until((.2, .4)[i], t0)
            self.play(GrowArrow(arrows[i][0]), FadeIn(arrows[i][1:]), FadeIn(boxes[i + 1], shift=UP * .15),
                      run_time=self.rt(.1))
        self.wait_until(.72, t0)
        warn = tx('Hai hằng số  ⇒  cần đúng hai điều kiện', 25, CORAL, bold=True).move_to([0, -2.2, 0])
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.07))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-1.5, 2.6, 1), (-1, 5.5, 1), (-1, 1, 2), (1, 2, 3, 4, 5))
        self.show_axes(a)
        self.write_board(badge('DẠNG 3', GOLD, 19), self.M('pw_f', 1.5), frac=.14)
        left = clipped(a, lambda v: 2, -1.5, 1, PURPLE, 5)
        right = clipped(a, lambda v: 2 * v, 1, 2.6, GREEN, 5)
        self.wait_until(.3, t0)
        self.play(Create(left), run_time=self.rt(.08))
        self.play(Create(right), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        j = dot(a, 1, 2, GOLD, .1)
        self.play(FadeIn(j, scale=1.6), run_time=self.rt(.05))
        self.write_board(tx('Tại x = 1: 2·1 = 2  →  f liên tục', 23, GOLD, bold=True),
                         tx('(đồ thị gãy góc, không đứt)', 20, SOFT), frac=.1)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.piece_axes()
        self.ax = a
        self.show_axes(a)
        self.write_board(self.heading('NGUYÊN HÀM TỪNG KHÚC'), self.M('pw_F', 1.4), frac=.16)
        self.c1 = ValueTracker(4)
        self.left_F = clipped(a, lambda v: 2 * v + 1, -1.5, 1, PURPLE, 5)
        self.right_F = always_redraw(lambda: clipped(a, lambda v: v * v + self.c1.get_value(), 1, 2.6, GREEN, 5))
        self.wait_until(.35, t0)
        self.play(Create(self.left_F), FadeIn(self.right_F), run_time=self.rt(.12))
        self.gap = always_redraw(lambda: VGroup(
            Line(a.c2p(1, 3), a.c2p(1, 1 + self.c1.get_value()), color=CORAL, stroke_width=5),
            Dot(a.c2p(1, 3), radius=.07, color=PURPLE), Dot(a.c2p(1, 1 + self.c1.get_value()), radius=.07,
                                                           color=GREEN)))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.gap), run_time=self.rt(.05))
        self.write_board(tx('C₁, C₂ tùy ý  →  hai mảnh bị lệch!', 23, CORAL, bold=True), frac=.07)

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(badge('HÀN TẠI x = 1', GOLD, 19),
                         para('F có đạo hàm tại mọi điểm  ⇒  F liên tục.', 23, WHITE, width=32), frac=.12)
        self.wait_until(.3, t0)
        self.write_board(self.M('weld', 1.7), frac=.1)
        self.wait_until(.48, t0)
        self.play(self.c1.animate.set_value(2), run_time=self.rt(.25), rate_func=smooth)
        for m in (self.right_F, self.gap):
            m.clear_updaters()
        self.play(FadeOut(self.gap[0]), Indicate(self.gap[1], color=GOLD, scale_factor=2), run_time=self.rt(.07))

    def beat_c8(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.M('pw_c2', 1.3), frac=.12)
        p0 = dot(a, 0, 1, CYAN, .1)
        self.play(FadeIn(p0, scale=1.6), FadeIn(tx('F(0) = 1', 18, CYAN, bold=True).next_to(p0, UP + LEFT, buff=.05)),
                  run_time=self.rt(.05))
        self.wait_until(.42, t0)
        res = self.M('pw_res', 1.4)
        self.write_board(res, frac=.12)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.04))
        self.wait_until(.78, t0)
        p2 = dot(a, 2, 6, GOLD, .1)
        self.play(FadeIn(p2), Create(dashed(a.c2p(2, 0), a.c2p(2, 6), color=GOLD, stroke_width=2)),
                  run_time=self.rt(.04))
        self.write_board(self.M('pw_val', 1.4), frac=.06)

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-1.5, 2.6, 1), (-1, 4.5, 1), (-1, 1, 2), (1, 2, 3, 4))
        self.show_axes(a)
        low = clipped(a, lambda v: 1, -1.5, 1, PURPLE, 5)
        high = clipped(a, lambda v: 3, 1, 2.6, GREEN, 5)
        hole = VGroup(dot(a, 1, 1, PURPLE, .09), dot(a, 1, 3, GREEN, .09),
                      dashed(a.c2p(1, 1), a.c2p(1, 3), color=CORAL, stroke_width=2))
        self.play(Create(low), Create(high), FadeIn(hole), run_time=self.rt(.12))
        self.write_board(badge('LƯU Ý CHUYÊN SÂU', CORAL, 19),
                         para('f có bước nhảy  →  F′ không thể nhảy giá trị  →  f không có nguyên hàm trên ℝ.', 23,
                              WHITE, width=32), frac=.16)
        self.wait_until(.6, t0)
        self.write_board(VGroup(cross(CORAL, .3), tx('Đề thi luôn cho f liên tục tại điểm nối', 22, GOLD, bold=True))
                         .arrange(RIGHT, buff=.2), frac=.07)
        self.write_board(tx('→ hãy kiểm tra trước khi giải', 22, SOFT), frac=.05)

    # ================================================================ PHẦN 2
    def road(self):
        g = VGroup(Line([-6.3, ROAD_Y, 0], [6.3, ROAD_Y, 0], color=SOFT, stroke_width=3))
        for m in range(0, 25, 4):
            p = np.array([self.rx(m), ROAD_Y, 0])
            g.add(Line(p + UP * .08, p + DOWN * .08, color=SOFT, stroke_width=2), tx(str(m), 14, SOFT).move_to(p + DOWN * .28))
        return g

    def rx(self, meters):
        return -6.0 + 12.0 * meters / 24

    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((0, 5.5, 1), (0, 24, 4), (1, 2, 3, 4, 5), (8, 16, 24), h=3.9, center=[LEFT_CX, .75, 0],
                           x_label='t', y_label='s', label_size=15)
        self.ax = a
        self.show_axes(a)
        self.tau = ValueTracker(0)
        self.vehicle = car(CORAL, .7)
        self.vehicle.add_updater(lambda m: m.move_to([self.rx(s_car(self.tau.get_value())), ROAD_Y + .3, 0]))
        self.play(Create(self.road()), FadeIn(self.vehicle), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('hook_v', 1.25), frac=.1)
        self.wait_until(.36, t0)
        self.write_board(self.M('e1_s1', 1.25), frac=.12)
        self.play(Create(clipped(a, lambda u: u * u, 0, 3, CYAN, 4.5)), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.write_board(self.M('e1_s2', 1.35), frac=.08)
        self.play(Create(clipped(a, lambda u: 6 * u - 9, 3, 5.5, GOLD, 4.5)), run_time=self.rt(.05))

    def beat_e2(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.M('e1_s1', 1.15), self.M('e1_s2', 1.2), self.M('e1_s3', 1.5), frac=.08)
        pt = always_redraw(lambda: Dot(a.c2p(self.tau.get_value(), s_car(self.tau.get_value())), radius=.08,
                                       color=GOLD))
        info = always_redraw(lambda: tx(
            f't = {vn(self.tau.get_value(), 1)} s   v = {vn(v_car(self.tau.get_value()), 1)} m/s   '
            f's = {vn(s_car(self.tau.get_value()), 1)} m', 21, WHITE).move_to([BOARD_X, -1.65, 0], aligned_edge=LEFT))
        self.play(FadeIn(pt), FadeIn(info), run_time=self.rt(.04))
        self.play(self.tau.animate.set_value(5), run_time=self.rt(.6), rate_func=linear)
        for m in (pt, info, self.vehicle):
            m.clear_updaters()
        self.play(Indicate(pt, color=GOLD), run_time=self.rt(.06))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((-2, 2, 1), (-2, 2.2, 1), (-1, 1), (-1, 1, 2))
        self.show_axes(a)
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e3_s1', 1.05), frac=.18)
        self.wait_until(.5, t0)
        res = self.M('e3_s2', 1.15)
        self.write_board(res, frac=.1)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.03))
        self.verify_plot(a, abs, lambda v: v * abs(v) / 2, -1.8, 1.8, .2, readout_at=(BOARD_X, -2.2))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_f', 1.2)).arrange(RIGHT, buff=.25)
        l2 = tx('F là nguyên hàm của f trên ℝ. Xét các mệnh đề:', 24, WHITE)
        items = (self.M('tf_a', 1.3), self.M('tf_b', 1.3), self.M('tf_c', 1.3), self.M('tf_d', 1.3))
        self.tf_question(t0, [l1, l2], items, fracs=(.36, .74))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))
        sol = VGroup(tx('b) hàn tại 1:', 22, SOFT), self.M('tf_b_calc', 1.25)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.12))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_sol), run_time=self.rt(.04))
        sol = VGroup(tx('c), d):', 22, SOFT), self.M('tf_cd_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.play(self.tf_mark(2, True), run_time=self.rt(.07))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.07))
        self.wait_until(.84, t0)
        self.play(FadeIn(self.tf_key('ĐSĐĐ'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((-2.6, 2.3, 1), (-.5, 8, 1), (-2, -1, 1, 2), (2, 4, 6, 8))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.0), frac=.12)
        self.wait_until(.45, t0)
        self.write_board(self.M('sa_s1', .95), frac=.12)
        R = clipped(a, lambda v: v * v + v + 1, 0, 2.3, GREEN, 4.5)
        L = clipped(a, math.exp, -2.6, 0, PURPLE, 4.5)
        self.play(Create(L), Create(R), FadeIn(dot(a, 0, 1, GOLD, .09)), run_time=self.rt(.08))
        self.wait_until(.8, t0)
        self.play(FadeIn(dot(a, 2, 7, GREEN, .09)), FadeIn(dot(a, -math.log(2), .5, PURPLE, .09)),
                  run_time=self.rt(.03))
        self.write_board(self.M('sa_s2', 1.25), self.answer_sheet('7,5'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('QUY TRÌNH 3 BƯỚC CHO HÀM TỪNG KHÚC', GOLD, 21).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        steps = (('Bước 1', 'Nguyên hàm từng khúc, mỗi khúc một hằng số riêng', CYAN),
                 ('Bước 2', 'Hàn tại điểm nối bằng tính liên tục', GREEN),
                 ('Bước 3', 'Dùng điều kiện đề cho – xem điểm thuộc khúc nào', GOLD))
        for i, (tag, text, col) in enumerate(steps):
            c = card(11.2, 1.1, col).move_to([0, 1.45 - 1.25 * i, 0])
            g = VGroup(c, badge(tag, col, 17).move_to(c.get_left() + RIGHT * .8),
                       tx(text, 23, WHITE).next_to(c.get_left(), RIGHT, buff=1.7))
            self.wait_until((.06, .32, .55)[i], t0)
            self.play(FadeIn(g, shift=UP * .12), run_time=self.rt(.07))
        warn = VGroup(cross(CORAL, .3), tx('Bẫy: dùng chung một C cho tất cả các khúc', 23, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).move_to([0, -2.4, 0])
        self.wait_until(.82, t0)
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.07))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Điều kiện → C', 'sum1', 'Mỗi điều kiện một phương trình'),
                                ('Nguyên hàm hai lần', 'sum2', 'Hai hằng số, cần hai điều kiện'),
                                ('Hàm từng khúc', 'sum3', 'Mỗi khúc một C, hàn bằng tính liên tục')),
                           fracs=(.04, .32, .58))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm F:', 'hw1'), ('Biết', 'hw2'), ('Cho', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .28, .58), show_answers=.86)

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.1), self.M('next2', 1.05)])


class INT06_SMOKE(INT06):
    smoke = True
