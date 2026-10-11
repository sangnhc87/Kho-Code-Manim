"""INT11 – Diện tích dưới đường cong & tổng Riemann.

    python scripts/build_typst.py --ep int11
    python scripts/prepare_voice.py --ep int11 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int11/scene.py INT11
    python scripts/finalize.py --ep int11

One method per narration beat (int11/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Brace, Create, FadeIn, FadeOut, Polygon, Rectangle, Transform,
                   ValueTracker, VGroup, Write, always_redraw, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, clipped, dot, tx, vn  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def sq(v):
    return v * v


def rects(a, f, x0, x1, n, mode='right', color=GOLD, opacity=.45):
    """Riemann rectangles in real coordinates (mode: 'right' or 'left')."""
    dx = (x1 - x0) / n
    g = VGroup()
    for k in range(n):
        xl = x0 + k * dx
        h = {'right': f(xl + dx), 'left': f(xl), 'mid': f(xl + dx / 2)}[mode]
        p0, p1 = a.c2p(xl, 0), a.c2p(xl + dx, h)
        r = Rectangle(width=abs(p1[0] - p0[0]), height=max(abs(p1[1] - p0[1]), 1e-3), fill_color=color,
                      fill_opacity=opacity, stroke_color=color, stroke_width=1.2 if n <= 32 else .4)
        g.add(r.move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
    return g


def rsum(f, x0, x1, n, mode='right'):
    dx = (x1 - x0) / n
    return sum(f(x0 + (k + (1 if mode == 'right' else 0)) * dx) for k in range(n)) * dx


def area(a, f, x0, x1, color=CYAN, opacity=.4, samples=60):
    xs = np.linspace(x0, x1, samples)
    return Polygon(a.c2p(x0, 0), *[a.c2p(v, f(v)) for v in xs], a.c2p(x1, 0), stroke_width=0, fill_color=color,
                   fill_opacity=opacity)


class INT11(LessonScene):
    EP = 'int11'

    def sq_axes(self):
        return axes((0, 2.3, 1), (0, 4.6, 1), 5.8, 5.4, center=[LEFT_CX, -.1, 0], x_ticks=(1, 2), y_ticks=(1, 2, 3, 4))

    def show_axes_local(self, a, frac=.05):
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(frac))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = axes((0, 3.6, 1), (0, 8, 1), 6.2, 5.0, center=[-2.6, -.2, 0], x_ticks=(1, 2, 3), y_ticks=(2, 4, 6),
                 x_label='t (s)', y_label='v (m/s)')
        self.show_axes_local(a)
        line = clipped(a, lambda u: 6, 0, 3, GOLD, 4)
        box = area(a, lambda u: 6, 0, 3, GOLD, .35)
        self.play(Create(line), run_time=self.rt(.06))
        self.play(FadeIn(box), FadeIn(tx('18', 34, WHITE, bold=True).move_to(a.c2p(1.5, 3))), run_time=self.rt(.08))
        self.play(FadeIn(self.M('rect', 1.5).move_to([3.6, 2.2, 0])), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        curve = clipped(a, lambda u: 1 + sq(u) * .7, 0, 3.3, CYAN, 4.5)
        q = area(a, lambda u: 1 + sq(u) * .7, 0, 3, CYAN, .3)
        self.play(FadeOut(box), Create(curve), run_time=self.rt(.1))
        self.play(FadeIn(q), FadeIn(tx('?', 48, CYAN, bold=True).move_to(a.c2p(2.2, 1.6))), run_time=self.rt(.08))
        self.play(FadeIn(tx('Diện tích dưới đường cong = ?', 26, CYAN, bold=True).move_to([3.6, .4, 0])),
                  run_time=self.rt(.05))

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        self.title_card()
        self.wait_until(.55, t0)
        self.play(FadeIn(badge('PHẦN B · TÍCH PHÂN', CYAN, 20).move_to([0, -2.6, 0]), shift=UP * .1),
                  run_time=self.rt(.06))

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Tổng Riemann', 'Xấp xỉ bằng hình chữ nhật mảnh'),
                         ('Giới hạn', 'Mảnh dần → diện tích thật'),
                         ('Bất ngờ', 'Diện tích tính bằng nguyên hàm')], t0, fracs=(.12, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 3.6, 1), (0, 8, 1), 5.8, 5.2, center=[LEFT_CX, -.1, 0], x_ticks=(1, 2, 3), y_ticks=(2, 4, 6),
                 x_label='t', y_label='v')
        self.show_axes_local(a)
        self.play(Create(clipped(a, lambda u: 6, 0, 3.4, GOLD, 4)), run_time=self.rt(.06))
        self.wait_until(.25, t0)
        self.play(FadeIn(area(a, lambda u: 6, 0, 3, GOLD, .4)), run_time=self.rt(.1))
        self.write_board(self.heading('VẬN TỐC KHÔNG ĐỔI'), self.M('rect', 1.6),
                         tx('quãng đường = diện tích hình chữ nhật', 23, GOLD, bold=True), frac=.16)

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 4.2, 1), (0, 8, 1), 5.8, 5.2, center=[LEFT_CX, -.1, 0], x_ticks=(1, 2, 3, 4), y_ticks=(2, 4, 6),
                 x_label='t', y_label='v')
        self.show_axes_local(a)
        steps = VGroup()
        for k, h in enumerate((2, 3.5, 5, 6.5)):
            p0, p1 = a.c2p(k, 0), a.c2p(k + 1, h)
            steps.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=(CYAN, GREEN, GOLD, CORAL)[k],
                                fill_opacity=.45, stroke_color=WHITE, stroke_width=1.5)
                      .move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        self.play(LaggedFade(steps), run_time=self.rt(.2))
        self.write_board(self.heading('VẬN TỐC THEO BẬC'), tx('quãng đường = tổng diện tích các hình chữ nhật', 23,
                                                              WHITE), frac=.1)
        self.wait_until(.55, t0)
        curve = clipped(a, lambda u: 1.5 + 1.3 * u, 0, 4.2, WHITE, 4)
        self.play(Create(curve), run_time=self.rt(.1))
        self.write_board(tx('Đường cong ≈ các bậc thang', 25, GOLD, bold=True), frac=.06)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.sq_axes()
        self.ax = a
        self.show_axes_local(a)
        self.play(Create(clipped(a, sq, 0, 2.15, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(self.heading('TỔNG RIEMANN'), self.M('riemann', 1.3), frac=.14)
        self.wait_until(.55, t0)
        self.rr = rects(a, sq, 0, 2, 4)
        self.play(LaggedFade(self.rr), run_time=self.rt(.15))
        self.write_board(tx('n = 4, chiều cao lấy tại mút phải', 22, GOLD), frac=.05)

    def beat_c4(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.heading('TĂNG SỐ HÌNH CHỮ NHẬT'), frac=.05)
        reading = tx(f'n = 4:   R₄ = {vn(rsum(sq, 0, 2, 4))}', 26, GOLD, bold=True)
        self.board(reading, gap=.5)
        self.play(FadeIn(reading), run_time=self.rt(.04))
        for k, frac in ((8, .3), (16, .52), (64, .72)):
            self.wait_until(frac, t0)
            new = rects(a, sq, 0, 2, k)
            label = tx(f'n = {k}:   R{str(k).translate(SUB)} = {vn(rsum(sq, 0, 2, k))}', 26, GOLD, bold=True) \
                .move_to(reading, aligned_edge=LEFT)
            self.play(Transform(self.rr, new), Transform(reading, label), run_time=self.rt(.08))
        self.write_board(tx('phần thừa ngày càng nhỏ', 23, GREEN, bold=True), frac=.05)

    def beat_c5(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.play(FadeOut(self.rr), run_time=self.rt(.03))
        left = rects(a, sq, 0, 2, 8, 'left', CYAN, .5)
        right = rects(a, sq, 0, 2, 8, 'right', GOLD, .25)
        self.play(FadeIn(right), FadeIn(left), run_time=self.rt(.08))
        self.write_board(self.heading('KẸP GIỮA HAI TỔNG'), self.M('squeeze', 1.8), frac=.12)
        self.wait_until(.45, t0)
        self.play(Transform(left, rects(a, sq, 0, 2, 40, 'left', CYAN, .5)),
                  Transform(right, rects(a, sq, 0, 2, 40, 'right', GOLD, .25)), run_time=self.rt(.14))
        self.wait_until(.7, t0)
        m = self.M('limit', 1.4)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m)), run_time=self.rt(.03))
        self.c5_r = VGroup(left, right)

    def beat_c5b(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.c5_r), run_time=self.rt(.03))
        mid = rects(a, sq, 0, 2, 4, 'mid', GREEN, .45)
        self.clear_board(.03)
        self.write_board(self.heading('TỔNG ĐIỂM GIỮA', GREEN), frac=.04)
        self.play(FadeIn(mid), run_time=self.rt(.08))
        dots = VGroup(*[dot(a, .25 + .5 * k, sq(.25 + .5 * k), GOLD, .07) for k in range(4)])
        self.play(FadeIn(dots), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.write_board(self.M('mid4', 1.0), tx('≈ 8/3 ≈ 2,667 chỉ với 4 hình!', 24, GREEN, bold=True), frac=.12)
        self.c5_r = VGroup(mid, dots)

    def beat_c6(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.c5_r), run_time=self.rt(.03))
        exact = area(a, sq, 0, 2, PURPLE, .5)
        self.play(FadeIn(exact), FadeIn(tx('8/3', 30, WHITE, bold=True).move_to(a.c2p(1.45, .7))), run_time=self.rt(.08))
        self.clear_board(.03)
        self.write_board(badge('BẤT NGỜ', PURPLE, 20), frac=.04)
        self.wait_until(.22, t0)
        m = self.M('antider', 1.6)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.04))
        self.wait_until(.7, t0)
        self.write_board(tx('Diện tích = hiệu giá trị nguyên hàm', 25, GREEN, bold=True), frac=.06)

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.sq_axes()
        self.show_axes_local(a)
        self.play(Create(clipped(a, sq, 0, 2.15, CYAN, 4.5)), run_time=self.rt(.05))
        xt = ValueTracker(.8)
        h = .14
        live = always_redraw(lambda: VGroup(
            area(a, sq, 0, xt.get_value(), CYAN, .35),
            area(a, sq, xt.get_value(), xt.get_value() + h, GOLD, .9),
            tx('S(x)', 24, WHITE, bold=True).move_to(a.c2p(xt.get_value() * .65, sq(xt.get_value()) * .22 + .15))))
        self.play(FadeIn(live), run_time=self.rt(.05))
        self.write_board(self.heading('VÌ SAO?'), self.M('strip', 1.15), frac=.14)
        self.wait_until(.45, t0)
        self.play(xt.animate.set_value(1.75), run_time=self.rt(.3), rate_func=smooth)
        live.clear_updaters()
        self.write_board(tx('Hàm diện tích là một nguyên hàm của f', 24, GREEN, bold=True), frac=.06)

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        m = self.M('notation', 3.2).move_to([0, .9, 0])
        self.play(Write(m), run_time=self.rt(.14))
        notes = VGroup()
        for grp, text, col, shift in ((m[0:1], 'chữ S kéo dài = TỔNG', CYAN, LEFT * 1.4),
                                      (m[3:7], 'chiều cao f(x)', GREEN, ORIGIN_SHIFT),
                                      (m[7:9], 'chiều rộng dx', GOLD, RIGHT * .6)):
            br = Brace(grp, DOWN, color=col)
            notes.add(VGroup(br, tx(text, 21, col, bold=True).next_to(br, DOWN, buff=.1).shift(shift)))
        for frac, nt in zip((.25, .38, .5), notes):
            self.wait_until(frac, t0)
            self.play(FadeIn(nt, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.78, t0)
        self.play(FadeIn(badge('Định nghĩa chính xác & Newton–Leibniz: INT12', PURPLE, 20).move_to([0, -2.6, 0])),
                  run_time=self.rt(.06))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 4.4, 1), (0, 26, 5), 5.8, 5.2, center=[LEFT_CX, -.1, 0], x_ticks=(1, 2, 3, 4),
                 y_ticks=(5, 10, 15, 20, 25), x_label='t', y_label='v')
        self.ax = a
        self.show_axes_local(a)
        vals = [0, 3, 8, 15, 24]
        pts = VGroup(*[dot(a, k, v, GOLD, .08) for k, v in enumerate(vals)])
        table = VGroup(tx('t (s):   0    1    2    3    4', 22, WHITE),
                       tx('v (m/s): 0    3    8    15   24', 22, GOLD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=.15)
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), table, frac=.12)
        self.play(FadeIn(pts), run_time=self.rt(.05))
        f = lambda u: vals[min(int(round(u)), 4)]  # noqa: E731
        self.wait_until(.45, t0)
        left = rects(a, f, 0, 4, 4, 'left', CYAN, .45)
        self.play(FadeIn(left), run_time=self.rt(.06))
        self.write_board(self.M('e1_left', 1.3), frac=.06)
        self.wait_until(.75, t0)
        right = rects(a, f, 0, 4, 4, 'right', GOLD, .2)
        self.play(FadeIn(right), run_time=self.rt(.06))
        self.write_board(self.M('e1_right', 1.3), frac=.06)

    def beat_e2(self, T):
        t0 = self.now()
        a = self.ax
        self.wait_until(.05, t0)
        self.write_board(tx('26 < s < 50,  trung bình ≈ 38', 24, WHITE, bold=True), frac=.08)
        self.wait_until(.45, t0)
        self.play(Create(clipped(a, lambda u: u * u + 2 * u, 0, 4.4, GREEN, 4)), run_time=self.rt(.08))
        m = self.M('e1_exact', 1.2)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 2.4, 1), (0, 2.6, 1), 5.6, 5.2, center=[LEFT_CX, -.1, 0], x_ticks=(1, 2), y_ticks=(1, 2))
        self.show_axes_local(a)
        self.play(Create(clipped(a, lambda u: u, 0, 2.4, CYAN, 4.5)), run_time=self.rt(.06))
        self.play(FadeIn(area(a, lambda u: u, 0, 2, CYAN, .45)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e3_tri', 1.6), frac=.12)
        self.wait_until(.5, t0)
        m = self.M('e3_F', 1.5)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.04))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_f', 1.4), tx('chia đều.', 24, WHITE)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi R, L là tổng Riemann điểm phải, điểm trái; S là diện tích. Xét:', 23, WHITE)
        items = (self.M('tf_a', 1.5), self.M('tf_b', 1.5), self.M('tf_c', 1.5), self.M('tf_d', 1.5))
        self.tf_question(t0, [l1, l2], items, fracs=(.25, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        sol = VGroup(self.M('tf_b_calc', 1.3)).move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(Write(sol), self.tf_mark(1, True), run_time=self.rt(.14))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.07))
        self.wait_until(.45, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.3)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(3, False), run_time=self.rt(.12))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐĐS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.sq_axes()
        self.show_axes_local(a, .04)
        self.play(Create(clipped(a, sq, 0, 2.15, CYAN, 4.5)), run_time=self.rt(.04))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), frac=.12)
        self.wait_until(.35, t0)
        self.play(FadeIn(rects(a, sq, 0, 2, 4)), run_time=self.rt(.06))
        self.write_board(self.M('sa_s1', 1.3), frac=.1)
        self.wait_until(.6, t0)
        self.write_board(self.M('sa_s2', 1.15), self.answer_sheet('3,75'), frac=.12)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO NHẬN ĐỊNH NHANH', GOLD, 21).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        for i, (f, key, col) in enumerate(((lambda u: .3 + u * u * .8, 'tip1', GREEN),
                                           (lambda u: 3.5 - u * u * .8, 'tip2', CORAL))):
            a = axes((0, 2.2, 1), (0, 3.8, 1), 4.6, 3.4, center=[-3.3 + 6.6 * i, .2, 0], x_label='', y_label='')
            g = VGroup(a, clipped(a, f, 0, 2.1, col, 4), rects(a, f, 0, 2, 5, 'left', CYAN, .45))
            m = self.M(key, 1.4).next_to(a, DOWN, buff=.35)
            self.wait_until((.08, .5)[i], t0)
            self.play(FadeIn(g), Write(m), run_time=self.rt(.12))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Tổng Riemann', 'sum1', 'Xấp xỉ bằng hình chữ nhật'),
                                ('Giới hạn', 'sum2', 'n → ∞: tổng → diện tích thật'),
                                ('Nguyên hàm', 'sum3', 'Diện tích = F(b) − F(a)')),
                           fracs=(.04, .4, .66))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Tính', 'hw2'), ('Ước lượng', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5), show_answers=.86)

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.15), self.M('next2', 1.05)])


ORIGIN_SHIFT = np.array([0.0, 0.0, 0.0])
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def LaggedFade(group):
    from manim import LaggedStart
    return LaggedStart(*[FadeIn(m, shift=UP * .08) for m in group], lag_ratio=.25)


class INT11_SMOKE(INT11):
    smoke = True
