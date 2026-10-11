"""INT05 – Nguyên hàm của f(ax + b): hàm hợp tuyến tính.

    python scripts/build_typst.py --ep int05
    python scripts/prepare_voice.py --ep int05 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int05/scene.py INT05
    python scripts/finalize.py --ep int05

One method per narration beat (int05/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, Dot, FadeIn, FadeOut, Indicate, Line, ValueTracker,
                   VGroup, Write, always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, check, clipped, cross, dashed, dot, tangent, tank, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

PI_LABELS = ((-math.pi, '−π'), (-math.pi / 2, '−π/2'), (math.pi / 2, 'π/2'), (math.pi, 'π'),
             (3 * math.pi / 2, '3π/2'), (2 * math.pi, '2π'))


def leaked(t):
    return 200 * (1 - math.exp(-t / 10))


class INT05(LessonScene):
    EP = 'int05'

    # ================================================================ helpers
    def pi_axes(self, xr, yr, yt, w=6.0, h=5.55, center=None, label_size=17):
        a = axes(xr, yr, w, h, center=center or [LEFT_CX, -.12, 0], x_ticks=(), y_ticks=yt, label_size=label_size)
        for v, name in PI_LABELS:
            if xr[0] < v < xr[1] - .15:
                p = a.c2p(v, 0)
                a.labels.add(Line(p + UP * .06, p + DOWN * .06, color=SOFT, stroke_width=2),
                             tx(name, label_size, SOFT).move_to(p + DOWN * .3))
        return a

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        tag = badge('từ INT04', PURPLE, 18).move_to([0, 2.55, 0])
        m1 = self.M('hook1', 2.0).move_to([0, 1.4, 0])
        self.play(FadeIn(tag), Write(m1), run_time=self.rt(.12))
        self.wait_until(.18, t0)
        self.play(Indicate(m1[-4:-2], color=GOLD, scale_factor=1.5), run_time=self.rt(.08))
        q = tx('Số 2 ở mẫu từ đâu ra?', 28, GOLD, bold=True).move_to([0, .2, 0])
        self.play(FadeIn(q, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        m2 = self.M('hook2', 1.7).move_to([0, -1.2, 0])
        self.play(Write(m2), run_time=self.rt(.12))
        self.wait_until(.75, t0)
        goal = tx('Hôm nay: quy tắc cho mọi f(ax + b)', 26, GREEN, bold=True).move_to([0, -2.5, 0])
        self.play(FadeIn(goal, shift=UP * .1), run_time=self.rt(.06))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Quy tắc tổng quát', 'Chứng minh bằng đạo hàm hàm hợp'),
                         ('Ý nghĩa hình học', 'Nén ngang a lần → độ dốc gấp a lần'),
                         ('Hai cái bẫy', 'Quên chia a · bên trong không bậc nhất')], t0, fracs=(.12, .36, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('ĐẠO HÀM HÀM HỢP ĐỌC NGƯỢC', 26, GOLD, bold=True)
        chain = self.M('chain', 1.9)
        mid = tx('thừa ra thừa số a  →  chia cho a để bù lại', 22, SOFT)
        rule = self.M('rule', 1.9)
        self.centre(head, chain, mid, rule, top=2.6, gap=.55)
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.wait_until(.08, t0)
        self.play(Write(chain), run_time=self.rt(.14))
        self.wait_until(.36, t0)
        self.play(FadeIn(mid), run_time=self.rt(.05))
        self.wait_until(.55, t0)
        self.play(Write(rule), run_time=self.rt(.14))
        self.play(FadeIn(self.box(rule)), run_time=self.rt(.04))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-.2, 6.6, 1), (-1.6, 1.6, 1), (-1, 1))
        self.show_axes(a)
        g1 = clipped(a, math.sin, -.2, 6.6, CYAN, 4)
        g2 = clipped(a, lambda v: math.sin(2 * v), -.2, 6.6, GOLD, 4)
        self.write_board(self.M('sin_x', 1.5), frac=.05)
        self.play(Create(g1), run_time=self.rt(.07))
        self.wait_until(.2, t0)
        self.write_board(self.M('sin_2x', 1.5), frac=.05)
        self.play(Create(g2), run_time=self.rt(.07))
        u = ValueTracker(.4)
        live = always_redraw(lambda: VGroup(
            tangent(a, u.get_value(), math.sin(u.get_value()), math.cos(u.get_value()), 1.3, CYAN),
            Dot(a.c2p(u.get_value(), math.sin(u.get_value())), radius=.07, color=CYAN),
            tangent(a, u.get_value() / 2, math.sin(u.get_value()), 2 * math.cos(u.get_value()), 1.3, GOLD),
            Dot(a.c2p(u.get_value() / 2, math.sin(u.get_value())), radius=.07, color=GOLD)))
        reading = always_redraw(lambda: VGroup(
            tx(f'độ dốc sin x       = {vn(math.cos(u.get_value()))}', 22, CYAN),
            tx(f'độ dốc sin 2x (điểm tương ứng) = {vn(2 * math.cos(u.get_value()))}', 22, GOLD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.14).move_to([BOARD_X, -.9, 0], aligned_edge=LEFT))
        self.wait_until(.42, t0)
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(u.animate.set_value(5.6), run_time=self.rt(.32), rate_func=linear)
        live.clear_updaters()
        reading.clear_updaters()
        self.write_board(self.M('slope_rel', 1.4), frac=.06, gap=1.5)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-1.7, 3.3, 1), (-1.6, 1.6, 1), (-1, 1))
        self.show_axes(a)
        self.write_board(self.heading('NÉN NGANG HỆ SỐ a'), self.M('chain', 1.4), frac=.1)
        k = ValueTracker(1)
        live = always_redraw(lambda: VGroup(
            clipped(a, lambda v: math.sin(k.get_value() * v), -1.7, 3.3, GOLD, 4),
            tangent(a, 0, 0, k.get_value(), 1.8), Dot(a.c2p(0, 0), radius=.08, color=GOLD)))
        reading = always_redraw(lambda: tx(f'a = {vn(k.get_value())}  →  độ dốc tại O = {vn(k.get_value())}',
                                           24, GOLD, bold=True).move_to([BOARD_X, -.6, 0], aligned_edge=LEFT))
        self.wait_until(.25, t0)
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(k.animate.set_value(3), run_time=self.rt(.32), rate_func=smooth)
        self.play(k.animate.set_value(2), run_time=self.rt(.12), rate_func=smooth)
        live.clear_updaters()
        reading.clear_updaters()
        self.write_board(tx('→ nguyên hàm phải chia cho a', 24, GREEN, bold=True), frac=.06, gap=1.1)

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-1.7, 4.8, 1), (-1.6, 1.6, 1), (-1, 1))
        self.show_axes(a)
        self.write_board(self.heading('CÒN b THÌ SAO?'), self.M('shift_b', 1.4), frac=.1)
        bt = ValueTracker(0)
        live = always_redraw(lambda: VGroup(
            clipped(a, lambda v: math.sin(v + bt.get_value()), -1.7, 4.8, CYAN, 4),
            tangent(a, -bt.get_value(), 0, 1, 1.8), Dot(a.c2p(-bt.get_value(), 0), radius=.08, color=GOLD)))
        reading = always_redraw(lambda: tx(f'b = {vn(bt.get_value())}  →  độ dốc tại điểm tương ứng = 1', 22, GOLD,
                                           bold=True).move_to([BOARD_X, -.6, 0], aligned_edge=LEFT))
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(bt.animate.set_value(1.4), run_time=self.rt(.32), rate_func=smooth)
        live.clear_updaters()
        reading.clear_updaters()
        self.write_board(tx('b chỉ tịnh tiến  →  chỉ có a ở mẫu số', 24, GREEN, bold=True), frac=.06, gap=1.1)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('BẢNG NGUYÊN HÀM MỞ RỘNG', 24, GOLD, bold=True).move_to([0, 2.7, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        keys = ('tb_pow', 'tb_inv', 'tb_exp', 'tb_cos', 'tb_sin')
        rows = VGroup()
        for i, key in enumerate(keys):
            c = card(11.6, 1.04, (CYAN, GREEN, GOLD, PURPLE, CORAL)[i]).move_to([0, 1.95 - 1.12 * i, 0])
            m = self.M(key, 1.2, max_w=11)
            if m.height > .9:
                m.scale_to_fit_height(.9)
            rows.add(VGroup(c, m.move_to(c)))
        for frac, r in zip((.12, .3, .45, .55, .65), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=UP * .12), run_time=self.rt(.06))

    def beat_c6(self, T):
        lines = self.worked(self.now(), 'ÁP DỤNG NHANH', ('q1', 'q2', 'q3'), (.04, .3, .58), (1.35, 1.35, 1.35),
                            box_last=False, gap=.3)
        note = tx('a = −2 < 0  →  kết quả mang dấu trừ', 22, CORAL, bold=True).next_to(lines[-1], DOWN, buff=.22)
        self.play(FadeIn(note), run_time=self.rt(.05))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BẪY 1: QUÊN CHIA a', CORAL, 21)
        bad = VGroup(self.M('trap1', 1.7), cross(CORAL, .4)).arrange(RIGHT, buff=.35)
        why = tx('Thử lại: (3 sin 3x)′ = 9 cos 3x  ≠  cos 3x', 24, SOFT)
        good = self.M('trap1_ok', 1.8)
        self.centre(head, bad, why, good, top=2.6, gap=.6)
        self.play(FadeIn(head), Write(bad[0]), run_time=self.rt(.14))
        self.play(Create(bad[1]), run_time=self.rt(.04))
        self.wait_until(.45, t0)
        self.play(FadeIn(why), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(Write(good), run_time=self.rt(.1))
        self.play(FadeIn(self.box(good, GREEN)), run_time=self.rt(.04))

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BẪY 2: BÊN TRONG KHÔNG BẬC NHẤT', CORAL, 21)
        bad = VGroup(self.M('trap2', 1.8), cross(CORAL, .4)).arrange(RIGHT, buff=.35)
        why = tx('x² không phải bậc nhất  →  quy tắc 1/a không áp dụng', 24, CORAL, bold=True)
        rule = VGroup(tx('Chỉ dùng khi bên trong có dạng', 22, SOFT), self.M('tip1', 1.5)).arrange(RIGHT, buff=.3)
        self.centre(head, bad, why, rule, top=2.6, gap=.65)
        self.play(FadeIn(head), Write(bad[0]), run_time=self.rt(.14))
        self.play(Create(bad[1]), run_time=self.rt(.04))
        self.wait_until(.4, t0)
        self.play(FadeIn(why), run_time=self.rt(.06))
        self.wait_until(.7, t0)
        self.play(FadeIn(rule, shift=UP * .1), run_time=self.rt(.08))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1_task', 'e1_s1'), (.04, .35), (1.8, 1.7), gap=.6)

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_task', 'e2_s1'), (.04, .4), (1.7, 1.7), gap=.6)

    def beat_e3(self, T):
        self.worked(self.now(), 'VÍ DỤ 3', ('e3_task', 'e3_s1', 'e3_s2'), (.04, .4, .66), (1.6, 1.6, 1.5), gap=.5)

    def beat_e4(self, T):
        self.worked(self.now(), 'VÍ DỤ 4', ('e4_task', 'e4_s1'), (.04, .42), (1.5, 1.5), gap=.6)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.tau = ValueTracker(0)
        self.tank_g = tank(lambda: 500 - leaked(self.tau.get_value()), capacity=500)
        self.play(FadeIn(self.tank_g), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 5', GOLD, 20), tx('Bể 500 lít bị rò với tốc độ (lít/giờ)', 23, WHITE),
                         self.M('e5_task', 1.45), frac=.24)
        self.wait_until(.7, t0)
        self.write_board(tx('Sau 10 giờ, bể mất bao nhiêu lít?', 25, GOLD, bold=True), frac=.08)

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_board(.03)
        a = axes((0, 10.5, 1), (0, 210, 10), 3.9, 4.5, center=[-4.45, -.25, 0], x_ticks=(5, 10),
                 y_ticks=(50, 100, 150, 200), x_label='t', y_label='L', label_size=14)
        self.show_axes(a, .04)
        self.write_board(self.M('e5_s1', 1.1), frac=.12)
        self.wait_until(.3, t0)
        self.write_board(self.M('e5_s2', 1.2), frac=.1)
        self.play(Create(clipped(a, leaked, 0, 10.5, CORAL, 4)), run_time=self.rt(.05))
        self.wait_until(.52, t0)
        res = self.M('e5_s3', 1.4)
        self.write_board(res, frac=.08)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.03))
        pt = always_redraw(lambda: Dot(a.c2p(self.tau.get_value(), leaked(self.tau.get_value())), radius=.08,
                                       color=GOLD))
        info = always_redraw(lambda: VGroup(
            tx(f't = {vn(self.tau.get_value(), 1)} giờ', 22, WHITE),
            tx(f'đã mất ≈ {vn(leaked(self.tau.get_value()), 1)} lít', 22, CORAL, bold=True),
        ).arrange(RIGHT, buff=.5).move_to([BOARD_X, -2.4, 0], aligned_edge=LEFT))
        self.play(FadeIn(pt), FadeIn(info), run_time=self.rt(.03))
        self.play(self.tau.animate.set_value(10), run_time=self.rt(.22), rate_func=linear)
        for m in (pt, info, self.tank_g[0]):
            m.clear_updaters()

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        intro = [tx('Xét các mệnh đề sau (C là hằng số, x thuộc khoảng xác định):', 24, WHITE)]
        items = (self.M('tf_a', 1.3), self.M('tf_b', 1.3), self.M('tf_c', 1.3), self.M('tf_d', 1.3))
        self.tf_question(t0, intro, items, fracs=(.12, .62))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))
        sol = VGroup(tx('b) đúng phải là:', 22, SOFT), self.M('tf_b_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.wait_until(.5, t0)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_sol), self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.42, t0)
        self.play(self.tf_mark(3, False), run_time=self.rt(.08))
        sol = VGroup(tx('d) đúng phải là:', 22, SOFT), self.M('tf_d_calc', 1.1)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 2.3, 1), (0, 5, 1), 5.8, 5.4, center=[LEFT_CX, -.12, 0], x_ticks=(1, 2), y_ticks=(1, 2, 3, 4))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.1), frac=.12)
        self.wait_until(.4, t0)
        self.write_board(self.M('sa_s1', 1.05), frac=.1)
        F = clipped(a, lambda v: math.exp(2 * v - 2) / 2 + .5, 0, 2.3, GOLD, 4.5)
        self.play(Create(F), FadeIn(dot(a, 1, 1, CYAN, .09)), run_time=self.rt(.08))
        self.wait_until(.72, t0)
        v2 = math.exp(2) / 2 + .5
        self.play(FadeIn(dot(a, 2, v2, GREEN, .09)),
                  Create(dashed(a.c2p(2, 0), a.c2p(2, v2), color=GREEN, stroke_width=2)), run_time=self.rt(.04))
        self.write_board(self.M('sa_s2', 1.3), self.answer_sheet('4,19'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO NHẨM NHANH 2 BƯỚC', GOLD, 21).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        steps = (('Đặt', 'Coi ax + b là một biến mới', 'tip1', CYAN),
                 ('Bước 1', 'Nguyên hàm theo bảng cơ bản', 'tip2', GREEN),
                 ('Bước 2', 'Chia kết quả cho a', 'tip3', GOLD))
        for i, (tag, text, key, col) in enumerate(steps):
            c = card(11.2, 1.1, col).move_to([0, 1.45 - 1.25 * i, 0])
            g = VGroup(c, badge(tag, col, 17).move_to(c.get_left() + RIGHT * .75),
                       tx(text, 22, WHITE).next_to(c.get_left(), RIGHT, buff=1.6),
                       self.M(key, 1.25, max_w=3.6).move_to(c.get_right() + LEFT * 2.1))
            self.wait_until((.08, .22, .4)[i], t0)
            self.play(FadeIn(g, shift=UP * .12), run_time=self.rt(.07))
        self.wait_until(.62, t0)
        warn = VGroup(check(CORAL), tx('Trước tiên: bên trong có đúng là bậc nhất không?', 23, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).move_to([0, -2.4, 0])
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.07))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Quy tắc 1/a', 'sum1', 'Đọc ngược đạo hàm hàm hợp'),
                                ('Vì sao chia a', 'sum2', 'Nén ngang a lần → dốc gấp a lần; b chỉ tịnh tiến'),
                                ('Chỉ bậc nhất', 'sum3', 'Bên trong bậc hai trở lên: không dùng quy tắc')),
                           fracs=(.04, .4, .68))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Biết', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .22, .42))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.3)])


class INT05_SMOKE(INT05):
    smoke = True
