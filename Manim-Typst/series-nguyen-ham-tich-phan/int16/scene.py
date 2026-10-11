"""INT16 – Tích phân đổi biến số.

    python scripts/build_typst.py --ep int16
    python scripts/prepare_voice.py --ep int16 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int16/scene.py INT16
    python scripts/finalize.py --ep int16

One method per narration beat (int16/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Line, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, card, check, clipped, cross, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def g_x(v):
    return 2 * v * (v * v + 1) ** 3


class INT16(LessonScene):
    EP = 'int16'

    def sub_example(self, t0, tag, task, s1, xs, us, s2, fracs, var='u'):
        """Centred substitution example: task, choice of u, bound table, new integral."""
        self.clear_stage(.05)
        head = VGroup(badge(tag, GOLD, 20), self.M(task, 1.35)).arrange(RIGHT, buff=.4)
        m1 = self.M(s1, 1.25)
        table = self.bound_table(xs, us, var)
        m2 = self.M(s2, 1.35)
        self.centre(head, m1, table, m2, top=2.8, gap=.38)
        self.play(FadeIn(head[0]), Write(head[1]), run_time=self.rt(.1))
        for frac, m in zip(fracs, (m1, table, m2)):
            self.wait_until(frac, t0)
            self.play(Write(m) if m is not table else FadeIn(m), run_time=self.rt(.1))
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m, wrong, right = self.M('hook', 1.55), self.M('hook_wrong', 1.35), self.M('hook_right', 1.35)
        why = tx('Lỗi nằm ở đâu?', 30, GOLD, bold=True)
        self.centre(m, wrong, right, why, top=2.6, gap=.5)
        self.play(Write(m), run_time=self.rt(.1))
        self.wait_until(.2, t0)
        self.play(Write(wrong), run_time=self.rt(.12))
        self.wait_until(.58, t0)
        self.play(Write(right), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(FadeIn(why, shift=UP * .1), run_time=self.rt(.06))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Đổi biến, đổi cận', 'Công thức và lý do'),
                         ('Bốn bước', 'Bảng đổi cận, không quay về x'),
                         ('Đổi biến lượng giác', 'Căn của 1 − x²: đặt x = sin t')], t0, fracs=(.12, .4, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CÔNG THỨC ĐỔI BIẾN', ('sub',), (.06,), (1.55,))
        row = VGroup(tx('đổi hàm', 26, CYAN, bold=True), tx('·', 26, SOFT), tx('đổi vi phân', 26, PURPLE, bold=True),
                     tx('·', 26, SOFT), tx('đổi cận', 26, GOLD, bold=True)).arrange(RIGHT, buff=.3) \
            .next_to(lines[-1], DOWN, buff=.8)
        self.wait_until(.5, t0)
        self.play(FadeIn(row, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.72, t0)
        self.play(FadeIn(tx('nguồn gốc: đạo hàm của hàm hợp', 23, SOFT).next_to(row, DOWN, buff=.45)),
                  run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        X = lambda v: -5.2 + 3.6 * v  # noqa: E731
        ys = (1.4, -1.0)
        lines = VGroup()
        for y, name, col, lo, hi in ((ys[0], 'x', CYAN, 0, 1), (ys[1], 'u', GOLD, 1, 2)):
            g = VGroup(Line([X(-.15), y, 0], [X(2.35), y, 0], color=SOFT, stroke_width=2),
                       Line([X(lo), y, 0], [X(hi), y, 0], color=col, stroke_width=7),
                       tx(name, 26, col, bold=True, slant=True).move_to([X(-.4), y, 0]))
            for v in (0, 1, 2):
                g.add(Line([X(v), y - .1, 0], [X(v), y + .1, 0], color=SOFT, stroke_width=2),
                      tx(str(v), 20, SOFT).move_to([X(v), y - .35, 0]))
            lines.add(g)
        self.play(FadeIn(lines[0]), run_time=self.rt(.06))
        self.wait_until(.2, t0)
        arrows = VGroup(*[Arrow([X(v), ys[0] - .45, 0], [X(v * v + 1), ys[1] + .2, 0], buff=.05, color=SOFT,
                                stroke_width=3, max_tip_length_to_length_ratio=.08) for v in (0, .25, .5, .75, 1)])
        self.play(FadeIn(lines[1]), Create(arrows), run_time=self.rt(.14))
        self.wait_until(.55, t0)
        self.play(Write(self.M('bounds', 1.45).move_to([0, -2.4, 0])), run_time=self.rt(.1))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        specs = ((g_x, (0, 1.2, 1), 1, 0, 1, CYAN, 'x', 'y = 2x(x² + 1)³'),
                 (lambda v: v ** 3, (0, 2.4, 1), 2, 1, 2, GOLD, 'u', 'y = u³'))
        for i, (f, xr, tick, lo, hi, col, xl, name) in enumerate(specs):
            a = axes(xr, (0, 17, 4), 4.6, 3.8, center=[-3.4 + 6.8 * i, .45, 0], x_ticks=(1, 2)[:tick],
                     y_ticks=(4, 8, 12, 16), x_label=xl, y_label='')
            top = xr[1] if i == 0 else 2.3
            grp = VGroup(a, a.labels, clipped(a, f, xr[0], top, col, 4, y_max=17),
                         tx(name, 20, col, bold=True).next_to(a, UP, buff=.05))
            self.wait_until((.04, .3)[i], t0)
            self.play(FadeIn(grp), run_time=self.rt(.07))
            self.play(FadeIn(area(a, f, lo, hi, col, .45)),
                      FadeIn(tx('15/4', 24, WHITE, bold=True).move_to(a.c2p((lo + hi) / 2 + .1 * i, 2.2 + 1.2 * i))),
                      run_time=self.rt(.06))
        self.wait_until(.62, t0)
        m = self.M('eq_area', 1.25).move_to([0, -2.35, 0])
        self.play(Write(m), run_time=self.rt(.12))
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 4 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Chọn u', 'biểu thức bên trong hàm hợp', CYAN), ('Tính du', 'du = u′(x) dx', PURPLE),
                 ('Đổi cận', 'bảng x → u', GOLD), ('Tính theo u', 'không cần thay lại x', GREEN))
        for i, (title, desc, col) in enumerate(steps):
            c = card(3.0, 3.0, col).move_to([-4.65 + 3.1 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 24, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 17, SOFT, max_w=2.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until((.05, .25, .42, .68)[i], t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))

    def beat_c5(self, T):
        self.sub_example(self.now(), 'BÀI MỞ ĐẦU', 'hook', 'c5_s1', ('0', '1'), ('1', '2'), 'c5_s2', (.05, .28, .5))

    def beat_c6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CÁCH 2: NGUYÊN HÀM THEO x', ('c6_s1', 'c6_s2'), (.06, .3), (1.3, 1.35), gap=.45)
        warn = VGroup(cross(CORAL, .28), tx('Đã chuyển sang u thì phải dùng cận của u', 26, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).next_to(lines[-1], DOWN, buff=.55)
        self.wait_until(.68, t0)
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.07))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('DẤU HIỆU CHỌN u', GOLD, 20)
        idea = tx('Hàm hợp  +  đạo hàm phần bên trong làm thừa số', 25, WHITE)
        pats = [self.M(k, 1.25) for k in ('pat1', 'pat2', 'pat3')]
        foot = tx('Thiếu hệ số? Bù bằng một hằng số', 24, CORAL, bold=True)
        self.centre(head, idea, *pats, foot, top=2.7, gap=.3)
        self.play(FadeIn(head), FadeIn(idea), run_time=self.rt(.08))
        for frac, m in zip((.25, .45, .62), pats):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.08))
        self.wait_until(.82, t0)
        self.play(FadeIn(foot, shift=UP * .1), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.sub_example(self.now(), 'VÍ DỤ 1', 'e1_task', 'e1_s1', ('0', 'π/2'), ('0', '1'), 'e1_s2', (.1, .35, .68))

    def beat_e2(self, T):
        self.sub_example(self.now(), 'VÍ DỤ 2', 'e2_task', 'e2_s1', ('1', 'e'), ('0', '1'), 'e2_s2', (.1, .4, .7))

    def beat_e3(self, T):
        self.sub_example(self.now(), 'VÍ DỤ 3', 'e3_task', 'e3_s1', ('0', '1'), ('0', '1'), 'e3_s2', (.12, .4, .65))

    def beat_e3b(self, T):
        self.sub_example(self.now(), 'CẬN ĐẢO CHIỀU', 'rev_task', 'rev_s1', ('0', '1'), ('1', '0'), 'rev_s2',
                         (.15, .35, .62))

    def beat_e4(self, T):
        self.sub_example(self.now(), 'VÍ DỤ 4', 'e4_task', 'e4_s1', ('0', '1'), ('0', 'π/2'), 'e4_s2', (.15, .35, .6),
                         var='t')

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((-1.3, 1.3, 1), (0, 1.3, 1), 6.0, 3.0, center=[LEFT_CX, 0, 0], x_ticks=(-1, 1), y_ticks=(1,))
        self.show_axes(a)
        f = lambda v: math.sqrt(max(0.0, 1 - v * v))  # noqa: E731
        self.play(Create(clipped(a, f, -1, 1, CYAN, 4.5)), run_time=self.rt(.1))
        self.write_board(self.heading('NỬA ĐƯỜNG TRÒN BÁN KÍNH 1'), frac=.05)
        self.wait_until(.4, t0)
        self.play(FadeIn(area(a, f, 0, 1, GOLD, .5, samples=120)), run_time=self.rt(.08))
        self.write_board(tx('Miền từ 0 đến 1: một phần tư hình tròn', 23, GOLD), frac=.06)
        self.wait_until(.6, t0)
        m = self.M('e5', 1.5)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.35, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.42, t0)
        sol = VGroup(tx('b)', 22, SOFT), self.M('tf_b_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(1, False), run_time=self.rt(.1))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(3, True), run_time=self.rt(.1))
        self.wait_until(.8, t0)
        self.play(FadeIn(self.tf_key('ĐSĐĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task = VGroup(self.M('sa_task', 1.45), tx('(làm tròn đến hàng phần trăm)', 22, SOFT)).arrange(RIGHT, buff=.3)
        s1 = self.M('sa_s1', 1.4)
        table = self.bound_table(('0', '√3'), ('1', '4'))
        self.centre(tag, task, s1, table, top=2.6, gap=.5)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.14))
        self.wait_until(.5, t0)
        self.play(Write(s1), FadeIn(table), run_time=self.rt(.12))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s2 = self.M('sa_s2', 1.3)
        sheet = self.answer_sheet('2,33')
        tip = VGroup(check(GREEN, .28), tx('Bấm máy tính tích phân ban đầu để kiểm tra', 22, GREEN)).arrange(RIGHT, buff=.2)
        self.centre(s2, sheet, tip, top=2.0, gap=.7)
        self.play(Write(s2), run_time=self.rt(.2))
        self.wait_until(.72, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))
        self.play(FadeIn(tip, shift=UP * .1), run_time=self.rt(.05))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Đổi biến', 'sum1', 'Đổi hàm, vi phân và cận'),
                                ('Bảng đổi cận', 'sum2', 'Tính theo u, không quay về x'),
                                ('Lượng giác', 'sum3', 'Căn của 1 − x²')),
                           fracs=(.04, .35, .7))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Tính', 'hw2'), ('Tính', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .4, .62))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.2)])


class INT16_SMOKE(INT16):
    smoke = True
