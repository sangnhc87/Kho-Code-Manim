"""INT08 – Phương pháp đổi biến số (mở rộng).

    python scripts/build_typst.py --ep int08
    python scripts/prepare_voice.py --ep int08 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int08/scene.py INT08
    python scripts/finalize.py --ep int08

One method per narration beat (int08/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Indicate, Line, Polygon, ValueTracker, VGroup,
                   Write, always_redraw, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, cross, dashed, dot, tx, vn  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

X_Y, U_Y = .9, -1.5


def sx(v):
    return -5.2 + 5.0 * v        # x in [0, 2]


def su(v):
    return -5.2 + 2.5 * v        # u in [0, 4]


class INT08(LessonScene):
    EP = 'int08'

    def cards(self, t0, head_text, rows, fracs, top=1.55, step=1.2, h=1.0, fscale=1.3):
        head = badge(head_text, GOLD, 21).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        for i, (tag, body, col, *math) in enumerate(rows):
            c = card(11.4, h, col).move_to([0, top - step * i, 0])
            parts = [c, badge(tag, col, 17).move_to(c.get_left() + RIGHT * .85)]
            if math:  # (tag, formula key, colour, True)
                parts.append(self.M(body, fscale, max_w=8.6).next_to(c.get_left(), RIGHT, buff=1.8))
            else:
                parts.append(tx(body, 23, WHITE).next_to(c.get_left(), RIGHT, buff=1.8))
            self.wait_until(fracs[i], t0)
            self.play(FadeIn(VGroup(*parts), shift=UP * .12), run_time=self.rt(.07))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.M('hook1', 1.8).move_to([-1.5, 1.9, 0])
        no = VGroup(cross(CORAL, .32), tx('không dùng được quy tắc 1/a (INT05)', 21, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.2).next_to(a, RIGHT, buff=.5)
        self.play(Write(a), FadeIn(no), run_time=self.rt(.1))
        self.wait_until(.3, t0)
        b = self.M('hook2', 1.9).move_to([0, .1, 0])
        self.play(Write(b), run_time=self.rt(.12))
        self.wait_until(.58, t0)
        self.play(Indicate(b, color=GOLD, scale_factor=1.05), run_time=self.rt(.07))
        key = tx('Đạo hàm của phần bên trong xuất hiện  →  ĐỔI BIẾN', 26, GOLD, bold=True).move_to([0, -2.0, 0])
        self.wait_until(.8, t0)
        self.play(FadeIn(key, shift=UP * .1), run_time=self.rt(.07))

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        self.title_card()
        self.wait_until(.55, t0)
        self.play(FadeIn(badge('NỘI DUNG MỞ RỘNG · HỌC SINH GIỎI / ĐÁNH GIÁ NĂNG LỰC', PURPLE, 19)
                         .move_to([0, -2.6, 0]), shift=UP * .1), run_time=self.rt(.06))

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Bản chất', 'Đạo hàm hàm hợp đọc ngược'),
                         ('Quy trình 4 bước', 'Chọn u · tính du · đổi hết · trả về x'),
                         ('Nhận diện & bẫy', 'Bảng dạng thường gặp, lỗi hay mắc')], t0, fracs=(.12, .32, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('ĐẠO HÀM HÀM HỢP ĐỌC NGƯỢC', 26, GOLD, bold=True)
        ch, rule = self.M('chain', 1.9), self.M('rule', 1.9)
        self.centre(head, ch, tx('đọc ngược', 22, SOFT), rule, top=2.5, gap=.55)
        self.play(FadeIn(head), Write(ch), run_time=self.rt(.14))
        self.wait_until(.4, t0)
        self.play(Write(rule), run_time=self.rt(.14))
        self.play(FadeIn(self.box(rule)), run_time=self.rt(.04))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('VI PHÂN du', 26, GOLD, bold=True)
        d, r = self.M('diff', 2.0), self.M('rule_u', 1.9)
        self.centre(head, d, r, top=2.3, gap=.75)
        self.play(FadeIn(head), Write(d), run_time=self.rt(.14))
        self.wait_until(.42, t0)
        self.play(Write(r), run_time=self.rt(.14))
        self.play(FadeIn(self.box(r, GREEN)), run_time=self.rt(.04))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        top = self.M('map', 1.7).move_to([0, 2.55, 0])
        self.play(Write(top), run_time=self.rt(.08))
        xl = VGroup(Line([sx(0) - .2, X_Y, 0], [sx(2) + .3, X_Y, 0], color=SOFT, stroke_width=3),
                    tx('trục x', 19, CYAN, bold=True).move_to([sx(2) + .9, X_Y, 0]))
        ul = VGroup(Line([su(0) - .2, U_Y, 0], [su(4) + .3, U_Y, 0], color=SOFT, stroke_width=3),
                    tx('trục u = x²', 19, GOLD, bold=True).move_to([su(4) + 1.05, U_Y, 0]))
        for v in (0, .5, 1, 1.5, 2):
            xl.add(Line([sx(v), X_Y - .08, 0], [sx(v), X_Y + .08, 0], color=SOFT, stroke_width=2),
                   tx(vn(v, 1), 15, SOFT).move_to([sx(v), X_Y + .3, 0]))
        for v in range(5):
            ul.add(Line([su(v), U_Y - .08, 0], [su(v), U_Y + .08, 0], color=SOFT, stroke_width=2),
                   tx(str(v), 15, SOFT).move_to([su(v), U_Y - .3, 0]))
        self.play(Create(xl), Create(ul), run_time=self.rt(.08))
        x0, dx = ValueTracker(.3), .18

        def band():
            a, b = x0.get_value(), x0.get_value() + dx
            return VGroup(
                Line([sx(a), X_Y, 0], [sx(b), X_Y, 0], color=CYAN, stroke_width=10),
                Line([su(a * a), U_Y, 0], [su(b * b), U_Y, 0], color=GOLD, stroke_width=10),
                Polygon([sx(a), X_Y, 0], [sx(b), X_Y, 0], [su(b * b), U_Y, 0], [su(a * a), U_Y, 0],
                        stroke_width=0, fill_color=PURPLE, fill_opacity=.25))

        live = always_redraw(band)
        reading = always_redraw(lambda: tx(
            f'x = {vn(x0.get_value())}:   du ≈ 2x·dx = {vn(2 * x0.get_value())} × dx   '
            f'(đoạn vàng dài gấp {vn(2 * x0.get_value() + dx)} lần)', 21, WHITE).move_to([0, -2.6, 0]))
        self.wait_until(.3, t0)
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(x0.animate.set_value(1.65), run_time=self.rt(.42), rate_func=smooth)
        live.clear_updaters()
        reading.clear_updaters()

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.cards(t0, 'QUY TRÌNH 4 BƯỚC', (('Bước 1', 'step1', CYAN, True), ('Bước 2', 'step2', GREEN, True),
                                           ('Bước 3', 'step3', GOLD, True), ('Bước 4', 'step4', PURPLE, True)),
                   (.04, .3, .45, .7), top=1.6, step=1.15, h=.95, fscale=1.4)

    def beat_c5(self, T):
        self.worked(self.now(), 'ÁP DỤNG', ('ex0_1', 'ex0_2', 'ex0_chk'), (.04, .25, .72), (1.6, 1.4, 1.6), gap=.6)

    def beat_c6(self, T):
        self.worked(self.now(), 'u′ SAI KHÁC HẰNG SỐ', ('k1', 'k2'), (.1, .55), (1.4, 1.6), gap=.8)

    def beat_c7(self, T):
        self.worked(self.now(), 'LƯỢNG GIÁC', ('tr1', 'tr2'), (.06, .55), (1.4, 1.7), gap=.8)

    def beat_c8(self, T):
        self.worked(self.now(), 'LOGARIT', ('lg1', 'lg2'), (.06, .55), (1.5, 1.7), gap=.8)

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.cards(t0, 'BẢNG NHẬN DIỆN NHANH', (('Dạng 1', 'rec1', CYAN, True), ('Dạng 2', 'rec2', GREEN, True),
                                               ('Dạng 3', 'rec3', GOLD, True), ('Dạng 4', 'rec4', PURPLE, True)),
                   (.04, .25, .5, .76), top=1.6, step=1.18, h=1.05, fscale=1.2)

    def beat_c10(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.cards(t0, 'BA CÁI BẪY', (('Bẫy 1', 'Quên trả về biến x ở bước cuối', CORAL),
                                      ('Bẫy 2', 'Quên đổi dx → thiếu hệ số như 1/2', CORAL),
                                      ('Bẫy 3', 'Chọn u mà u′ không có mặt → bế tắc', CORAL)),
                   (.12, .35, .62), top=1.4, step=1.3, h=1.05)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1_task', 'e1_s1'), (.04, .45), (1.3, 1.7), gap=.8)

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_task', 'e2_s1'), (.04, .5), (1.25, 1.6), gap=.8)

    def beat_e3(self, T):
        self.worked(self.now(), 'VÍ DỤ 3', ('e3_task', 'e3_s1'), (.04, .55), (1.2, 1.7), gap=.8)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.4)).arrange(RIGHT, buff=.25)
        l2 = tx('F là một nguyên hàm của f trên ℝ. Xét các mệnh đề:', 24, WHITE)
        items = (VGroup(tx('Đặt', 22, WHITE), self.M('tf_a', 1.3)).arrange(RIGHT, buff=.2), self.M('tf_b', 1.3),
                 self.M('tf_c', 1.3), VGroup(tx('Nếu', 22, WHITE), self.M('tf_d', 1.3)).arrange(RIGHT, buff=.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.28, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))
        sol = VGroup(tx('b) thử lại:', 22, SOFT), self.M('tf_b_calc', 1.25)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_sol), self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.32, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.play(self.tf_mark(3, True), run_time=self.rt(.06))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐĐ'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-.2, 3.4, 1), (-.15, .5, 1), 5.8, 5.4, center=[LEFT_CX, -.12, 0], x_ticks=(1, 2, 3),
                 y_ticks=(.1, .2, .3, .4))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.05), frac=.12)
        self.wait_until(.42, t0)
        self.write_board(self.M('sa_s1', 1.0), frac=.12)
        self.play(Create(clipped(a, lambda v: math.sin(v) ** 3 / 3, 0, 3.4, GOLD, 4.5)), run_time=self.rt(.08))
        self.wait_until(.78, t0)
        self.play(FadeIn(dot(a, math.pi / 2, 1 / 3, GREEN, .09)),
                  Create(dashed(a.c2p(math.pi / 2, 0), a.c2p(math.pi / 2, 1 / 3), color=GREEN, stroke_width=2)),
                  run_time=self.rt(.03))
        self.write_board(self.M('sa_s2', 1.25), self.answer_sheet('0,33'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO KIỂM TRA NHANH', GOLD, 21).move_to([0, 2.5, 0])
        m = self.M('chk', 2.0).move_to([0, 1.1, 0])
        self.play(FadeIn(head), Write(m), run_time=self.rt(.14))
        self.wait_until(.42, t0)
        t1 = tx('Đạo hàm ra đúng biểu thức ban đầu, kể cả hệ số  →  chắc chắn đúng', 23, GREEN, bold=True)
        t2 = tx('Lệch một hằng số (2 hay 1/2)  →  em đã quên đổi dx', 23, CORAL, bold=True)
        VGroup(t1, t2).arrange(DOWN, buff=.45).move_to([0, -1.2, 0])
        self.play(FadeIn(t1, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.7, t0)
        self.play(FadeIn(t2, shift=UP * .1), run_time=self.rt(.07))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Bản chất', 'sum1', 'Đạo hàm hàm hợp đọc ngược'),
                                ('Quy trình', 'sum2', 'Chọn u, tính du, đổi hết, trả về x'),
                                ('Bù hằng số', 'sum3', 'u′ sai khác hằng số vẫn đổi được')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Tìm', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.4), self.M('next2', 1.3)])


class INT08_SMOKE(INT08):
    smoke = True
