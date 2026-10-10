"""INT02 – Tính chất nguyên hàm & nguyên hàm của hàm lũy thừa.

    python scripts/build_typst.py --ep int02
    python scripts/prepare_voice.py --ep int02 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int02/scene.py INT02
    python scripts/finalize.py --ep int02

One method per narration beat (int02/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, Group, Dot, FadeIn, FadeOut, GrowArrow,
                   GrowFromCenter, Indicate, LaggedStart, Line, Rectangle, ReplacementTransform, ValueTracker,
                   VGroup, Write, always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import (axes, badge, card, check, clipped, cross, dashed, dot, para, slope_field,  # noqa: E402
                        tangent, tx, vn)
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, DIM, GOLD, GREEN, PURPLE, SOFT, STROKE, WHITE  # noqa: E402


def tank_volume(t):
    return t ** 3 + t ** 2 + 10


class INT02(LessonScene):
    EP = 'int02'

    # ================================================================ helpers
    def std_axes(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.55), center=[LEFT_CX, -.12, 0],
                    x_ticks=xt, y_ticks=yt, **kw)

    def show_axes(self, a, frac=.05):
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(frac))

    def centre(self, *mobs, top=2.55, gap=.42):
        """Stack mobjects centred on the full width (no graph column)."""
        g = VGroup(*mobs).arrange(DOWN, buff=gap)
        g.move_to([0, top, 0], aligned_edge=UP)
        return g

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        tag = badge('TẬP 01', CYAN, 18)
        recap = self.M('recap', 1.6)
        top = VGroup(tag, recap, check()).arrange(RIGHT, buff=.35).move_to([0, 2.2, 0])
        hint = tx('đoán được vì đã biết (x²)′ = 2x', 20, SOFT).next_to(top, DOWN, buff=.2)
        self.play(FadeIn(tag), Write(recap), run_time=self.rt(.08))
        self.play(Create(top[2]), FadeIn(hint), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        hard = VGroup(self.M('hook_poly', 1.5), self.M('hook_sqrt', 1.5)).arrange(DOWN, buff=.35).move_to([-.6, -.55, 0])
        self.play(LaggedStart(*[Write(h) for h in hard], lag_ratio=.4), run_time=self.rt(.14))
        self.wait_until(.6, t0)
        guess = VGroup(tx('Đoán mãi?', 26, CORAL, bold=True), cross(CORAL, .35)).arrange(RIGHT, buff=.2) \
            .next_to(hard, RIGHT, buff=.6)
        self.play(FadeIn(guess, shift=LEFT * .2), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        need = tx('→  Cần QUY TẮC, giống như bảng đạo hàm', 26, GOLD, bold=True).move_to([0, -2.45, 0])
        self.play(FadeIn(need, shift=UP * .15), run_time=self.rt(.07))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Nguyên hàm hàm lũy thừa', 'Tăng số mũ, chia cho số mũ mới'),
                         ('Hai tính chất tuyến tính', 'Hằng số ra ngoài · tách tổng, hiệu'),
                         ('Bẫy tích – thương', '∫f·g ≠ ∫f · ∫g: vì sao và cách tránh')], t0, fracs=(.12, .3, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        h1 = tx('ĐẠO HÀM', 24, CYAN, bold=True).move_to([-3.3, 2.35, 0])
        h2 = tx('NGUYÊN HÀM', 24, GOLD, bold=True).move_to([3.3, 2.35, 0])
        rule = Line([-6, 2.0, 0], [6, 2.0, 0], color=STROKE, stroke_width=2)
        self.play(FadeIn(h1), FadeIn(h2), Create(rule), run_time=self.rt(.06))
        self.wait_until(.16, t0)
        rows = (('d_const', 'i_const', 1.0), ('d_x', 'i_x', -.6))
        for k, (d, i, y) in enumerate(rows):
            md = self.M(d, 1.6).move_to([-3.3, y, 0])
            mi = self.M(i, 1.6).move_to([3.3, y, 0])
            arr = Arrow([-1.1, y, 0], [1.1, y, 0], color=GOLD, buff=0, stroke_width=5)
            lbl = tx('đọc ngược', 17, GOLD).next_to(arr, UP, buff=.08)
            self.wait_until((.3, .68)[k], t0)
            self.play(Write(md), run_time=self.rt(.06))
            self.play(GrowArrow(arr), FadeIn(lbl), Write(mi), run_time=self.rt(.1))
        note = tx('Mỗi công thức đạo hàm  ⇄  một công thức nguyên hàm', 22, SOFT).move_to([0, -2.3, 0])
        self.play(FadeIn(note), run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2.5, 2.5, 1), (-3, 7, 1), (-2, -1, 1, 2), (-2, 2, 4, 6))
        self.show_axes(a)
        self.write_board(self.heading('NGUYÊN HÀM CỦA HẰNG SỐ'), self.M('d_kx', 1.3), self.M('i_k', 1.5), frac=.1)
        self.wait_until(.3, t0)
        field = slope_field(a, lambda x, y: 2, np.arange(-2.25, 2.3, .5), np.arange(-2.5, 6.6, .75), seg=.32,
                            color=SOFT, width=2)
        self.write_board(tx('f(x) = 2: mọi đoạn nhỏ cùng độ dốc 2', 22, SOFT), frac=.05)
        self.play(LaggedStart(*[Create(s) for s in field], lag_ratio=.01), run_time=self.rt(.2))
        self.wait_until(.7, t0)
        lines = VGroup(*[clipped(a, lambda v, k=k: 2 * v + k, -2.5, 2.5, GOLD, 3.5) for k in (-2, 0, 2, 4)])
        self.play(field.animate.set_opacity(.35), LaggedStart(*[Create(m) for m in lines], lag_ratio=.25),
                  run_time=self.rt(.14))
        self.write_board(self.M('k2', 1.4), tx('→ các đường thẳng song song', 22, GOLD), frac=.06)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('NGUYÊN HÀM CỦA x mũ n', 26, GOLD, bold=True)
        d1 = self.M('der1', 1.4)
        mid = tx('chia hai vế cho n + 1', 20, SOFT)
        d2 = self.M('der2', 1.4)
        res = self.M('pow_n', 1.65)
        self.centre(head, d1, mid, d2, res, top=2.85, gap=.26)
        self.play(FadeIn(head), Write(d1), run_time=self.rt(.12))
        self.wait_until(.38, t0)
        self.play(FadeIn(mid), Write(d2), run_time=self.rt(.14))
        self.wait_until(.7, t0)
        self.play(Write(res), run_time=self.rt(.12))
        self.play(FadeIn(self.box(res)), run_time=self.rt(.05))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('CÁCH NHỚ', 24, GOLD, bold=True).move_to([0, 2.65, 0])
        a = self.M('step_a', 3.0).move_to([-3.9, .5, 0])
        b = self.M('step_b', 3.0).move_to(a)
        c = self.M('step_c', 3.0).move_to(a)
        plus = badge('① số mũ + 1', CYAN, 20).move_to([-1.2, 1.1, 0])
        div = badge('② chia cho số mũ mới', GREEN, 20).move_to([-1.2, .1, 0])
        self.play(FadeIn(head), Write(a), run_time=self.rt(.07))
        self.wait_until(.16, t0)
        self.play(ReplacementTransform(a, b), FadeIn(plus, shift=LEFT * .2), run_time=self.rt(.08))
        self.wait_until(.27, t0)
        self.play(ReplacementTransform(b, c), FadeIn(div, shift=LEFT * .2), run_time=self.rt(.08))
        exs = VGroup(self.M('ex_x3', 1.35), self.M('ex_x2', 1.35), self.M('ex_x5', 1.35)) \
            .arrange(DOWN, buff=.3, aligned_edge=LEFT).move_to([3.5, .2, 0])
        for frac, m in zip((.36, .62, .8), exs):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.08))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-1.6, 1.9, 1), (-1.5, 3.7, 1), (-1, 1), (-1, 1, 2, 3))
        self.show_axes(a)
        self.write_board(self.heading('KIỂM TRA BẰNG HÌNH'), self.M('f_sq', 1.4), self.M('F_cube', 1.4), frac=.12)
        self.wait_until(.28, t0)
        self.verify_plot(a, lambda v: v * v, lambda v: v ** 3 / 3, -1.4, 1.75, .5)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('MỞ RỘNG: SỐ MŨ THỰC', 26, GOLD, bold=True)
        rule = self.M('pow_alpha', 1.5)
        ex1 = self.M('sqrt_ex', 1.3)
        n1 = tx('xét trên (0; +∞)', 19, SOFT)
        ex2 = self.M('inv2_ex', 1.3)
        n2 = tx('xét trên từng khoảng (−∞; 0) và (0; +∞)', 19, SOFT)
        self.centre(head, rule, ex1, n1, ex2, n2, top=2.85, gap=.22)
        n1.shift(UP * .08)
        n2.shift(UP * .08)
        self.play(FadeIn(head), Write(rule), run_time=self.rt(.12))
        self.play(FadeIn(self.box(rule)), run_time=self.rt(.04))
        self.wait_until(.3, t0)
        self.play(Write(ex1), FadeIn(n1), run_time=self.rt(.14))
        self.wait_until(.66, t0)
        self.play(Write(ex2), FadeIn(n2), run_time=self.rt(.14))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        m = self.M('alpha_m1', 2.0).move_to([0, 1.3, 0])
        self.play(Write(m), run_time=self.rt(.12))
        bad = VGroup(cross(CORAL, .45), tx('chia cho 0: vô nghĩa', 26, CORAL, bold=True)).arrange(RIGHT, buff=.25) \
            .next_to(m, DOWN, buff=.5)
        self.play(FadeIn(bad, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.5, t0)
        box = card(8.6, 1.7, PURPLE).move_to([0, -1.75, 0])
        q = self.M('inv1_q', 1.6).move_to(box.get_center() + LEFT * 1.4)
        tag = badge('học ở INT03', PURPLE, 20).move_to(box.get_center() + RIGHT * 2.6)
        self.play(FadeIn(box), Write(q), FadeIn(tag), run_time=self.rt(.12))

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2, 2, 1), (-1, 9, 1), (-1, 1), (2, 4, 6, 8))
        self.ax = a
        self.show_axes(a)
        self.write_board(self.heading('TÍNH CHẤT 1'), self.M('rule_k', 1.25), frac=.12)
        base = clipped(a, lambda v: v * v, -2, 2, CYAN, 3)
        k = ValueTracker(1)
        live = always_redraw(lambda: clipped(a, lambda v: k.get_value() * v * v, -2, 2, GOLD, 4.5))
        tan = always_redraw(lambda: VGroup(tangent(a, 1, k.get_value(), 2 * k.get_value(), 1.6),
                                           Dot(a.c2p(1, k.get_value()), radius=.08, color=GOLD)))
        reading = always_redraw(lambda: tx(f'k = {vn(k.get_value())}:  độ dốc tại x = 1 là {vn(2 * k.get_value())}',
                                           22, GOLD, bold=True).move_to([BOARD_X, -2.2, 0], aligned_edge=LEFT))
        self.wait_until(.3, t0)
        self.play(Create(base), FadeIn(live), FadeIn(tan), FadeIn(reading), run_time=self.rt(.06))
        self.write_board(self.M('proof_k', 1.4), frac=.08)
        self.wait_until(.55, t0)
        self.play(k.animate.set_value(3), run_time=self.rt(.22), rate_func=smooth)
        for m in (live, tan, reading):
            m.clear_updaters()
        self.write_board(self.M('kex', 1.15), frac=.08)

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_board(.04)
        self.write_board(self.heading('VÌ SAO PHẢI CÓ k ≠ 0?', CORAL), frac=.05)
        self.wait_until(.18, t0)
        self.write_board(self.M('k0a', 1.5), tx('cả một họ hằng số', 20, SOFT), frac=.12)
        self.wait_until(.55, t0)
        self.write_board(self.M('k0b', 1.5), tx('chỉ là một số', 20, SOFT), frac=.12)
        self.write_board(tx('→ hai vế không bằng nhau', 24, CORAL, bold=True), frac=.06)

    def beat_c10(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2, 1.6, 1), (-1.5, 4.6, 1), (-1, 1), (-1, 1, 2, 3, 4))
        self.show_axes(a)
        self.write_board(self.heading('TÍNH CHẤT 2'), self.M('rule_sum', 1.1), frac=.12)
        self.wait_until(.3, t0)
        self.write_board(self.M('proof_sum', 1.4), frac=.08)
        curves = ((lambda v: v * v, lambda v: 2 * v, CYAN, 'F = x²'), (lambda v: v, lambda v: 1.0, PURPLE, 'G = x'),
                  (lambda v: v * v + v, lambda v: 2 * v + 1, GOLD, 'F + G'))
        graphs = VGroup(*[clipped(a, F, -2, 1.6, col, 4) for F, _, col, _ in curves])
        labels = VGroup(*[tx(name, 21, col, bold=True) for _, _, col, name in curves]).arrange(RIGHT, buff=.5)
        self.board(labels, gap=.45)
        self.play(Create(graphs), FadeIn(labels), run_time=self.rt(.1))
        xt = ValueTracker(-1.6)
        tans = always_redraw(lambda: VGroup(*[
            VGroup(tangent(a, xt.get_value(), F(xt.get_value()), dF(xt.get_value()), 1.3, color=col),
                   Dot(a.c2p(xt.get_value(), F(xt.get_value())), radius=.06, color=col))
            for F, dF, col, _ in curves]))
        reading = always_redraw(lambda: tx(
            f'độ dốc:  {vn(2 * xt.get_value())} + {vn(1.0)} = {vn(2 * xt.get_value() + 1)}', 24, GOLD, bold=True)
            .move_to([BOARD_X, -1.9, 0], aligned_edge=LEFT))
        self.play(FadeIn(tans), FadeIn(reading), run_time=self.rt(.04))
        self.play(xt.animate.set_value(1.3), run_time=self.rt(.3), rate_func=linear)
        tans.clear_updaters()
        reading.clear_updaters()

    def beat_c11(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('GỘP HAI TÍNH CHẤT: TÍNH TỪNG HẠNG TỬ', 24, GOLD, bold=True)
        p1 = self.M('poly1', 1.9)
        p2 = self.M('poly2', 1.75)
        p3 = self.M('poly3', 1.9)
        self.centre(head, p1, p2, p3, top=2.75, gap=.42)
        for m in (p2, p3):
            m.align_to(p1, LEFT).shift(RIGHT * 1.2)
        back = tx('↑ chính là câu hỏi ở đầu bài', 19, SOFT).next_to(p1, RIGHT, buff=.3)
        self.play(FadeIn(head), Write(p1), FadeIn(back), run_time=self.rt(.12))
        self.wait_until(.22, t0)
        self.play(Write(p2), run_time=self.rt(.2))
        self.wait_until(.68, t0)
        self.play(Write(p3), run_time=self.rt(.12))
        self.play(FadeIn(self.box(p3, GREEN)), run_time=self.rt(.05))
        self.c11_all = Group(*self.stage())

    def beat_c12(self, T):
        t0 = self.now()
        self.play(self.c11_all.animate.scale(.78).to_edge(UP, buff=.75), run_time=self.rt(.06))
        chips = VGroup(*[badge(f'C{s}', GOLD, 20) for s in '₁₂₃']).arrange(RIGHT, buff=1.2).move_to([0, -2.2, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .2) for c in chips], lag_ratio=.3), run_time=self.rt(.14))
        self.wait_until(.45, t0)
        one = badge('C', GOLD, 24).move_to([0, -2.2, 0])
        self.play(*[c.animate.move_to(one) for c in chips], run_time=self.rt(.12))
        self.play(ReplacementTransform(chips, one), run_time=self.rt(.06))
        m = self.M('oneC', 1.4).next_to(one, RIGHT, buff=.6)
        self.play(Write(m), run_time=self.rt(.1))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((-.8, 1.8, 1), (-2, 5.5, 1), (1,), (-1, 1, 2, 3, 4, 5))
        self.ax = a
        self.show_axes(a)
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('e1_task', 1.6), frac=.18)
        self.wait_until(.45, t0)
        warn = para('Không có quy tắc cho bình phương (hay tích) → KHAI TRIỂN trước.', 23, CORAL, width=32,
                    bold=True)
        self.write_board(warn, frac=.08)

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('e1_task', 1.3), self.M('e1_s1', 1.3), frac=.12)
        self.wait_until(.3, t0)
        s2 = self.M('e1_s2', 1.25)
        self.write_board(s2, frac=.12)
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.04))
        self.wait_until(.55, t0)
        self.verify_plot(self.ax, lambda v: (2 * v - 1) ** 2, lambda v: 4 / 3 * v ** 3 - 2 * v * v + v, -.5, 1.55, .26,
                         readout_at=(BOARD_X, -2.3))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((0, 2.8, 1), (-3, 5, 1), (1, 2), (-2, 2, 4))
        self.ax = a
        self.show_axes(a)
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.6), frac=.2)
        self.wait_until(.5, t0)
        warn = para('Không có quy tắc cho thương → TÁCH thành tổng các lũy thừa.', 23, CORAL, width=32, bold=True)
        self.write_board(warn, frac=.08)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('e2_task', 1.3), self.M('e2_s1', 1.35), frac=.12)
        self.wait_until(.25, t0)
        s2 = self.M('e2_s2', 1.35)
        self.write_board(s2, tx('trên từng khoảng không chứa 0', 19, SOFT), frac=.12)
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.04))
        self.wait_until(.56, t0)
        self.verify_plot(self.ax, lambda v: 1 + v ** -2, lambda v: v - 1 / v, .55, 2.5, .26, x_min=.3,
                         readout_at=(BOARD_X, -2.3))

    # ---------------------------------------------------------------- example 3: water tank
    def tank(self, level_fn, center=(-1.25, -.5)):
        cx, cy = center
        w, h = 1.5, 3.6
        shell = VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0], color=SOFT, stroke_width=3),
                       Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=SOFT, stroke_width=3),
                       Line([cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=SOFT, stroke_width=3))
        ticks = VGroup()
        for v in (25, 50, 75, 100):
            y = cy - h / 2 + h * v / 100
            ticks.add(Line([cx + w / 2, y, 0], [cx + w / 2 + .1, y, 0], color=SOFT, stroke_width=2),
                      tx(str(v), 14, SOFT).move_to([cx + w / 2 + .38, y, 0]))
        water = always_redraw(lambda: Rectangle(width=w - .08, height=max(h * level_fn() / 100, .01),
                                                fill_color=CYAN, fill_opacity=.55, stroke_width=0)
                              .move_to([cx, cy - h / 2 + h * level_fn() / 200, 0]))
        pipe = VGroup(Line([cx - w / 2 - .2, cy + h / 2 + .35, 0], [cx - .1, cy + h / 2 + .35, 0], color=SOFT,
                           stroke_width=6),
                      Line([cx - .1, cy + h / 2 + .35, 0], [cx - .1, cy + h / 2 + .1, 0], color=SOFT, stroke_width=6))
        label = tx('lít', 14, DIM).move_to([cx + w / 2 + .38, cy - h / 2 - .2, 0])
        return VGroup(water, shell, ticks, pipe, label)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.tau = ValueTracker(0)
        self.tank_g = self.tank(lambda: tank_volume(self.tau.get_value()))
        self.play(FadeIn(self.tank_g), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), tx('Nước chảy vào bể với tốc độ', 24, WHITE),
                         self.M('e3_task', 1.4), tx('r tính bằng lít/phút, V tính bằng lít.', 20, SOFT), frac=.26)
        self.wait_until(.75, t0)
        self.write_board(tx('Sau 4 phút:  V(4) = ?', 26, GOLD, bold=True), frac=.08)

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(tx('V′(t) = r(t)  ⇒  V là một nguyên hàm của r', 23, WHITE), frac=.08)
        self.wait_until(.3, t0)
        self.write_board(self.M('e3_s1', 1.25), frac=.14)
        self.wait_until(.7, t0)
        self.write_board(self.M('e3_s2', 1.35), self.M('e3_s3', 1.45), frac=.12)
        a = axes((0, 4.5, 1), (0, 100, 10), 3.9, 4.5, center=[-4.45, -.25, 0], x_ticks=(1, 2, 3, 4),
                 y_ticks=(20, 40, 60, 80, 100), x_label='t', y_label='V', label_size=14)
        self.ax = a
        curve = clipped(a, tank_volume, 0, 4.4, GREEN, 4)
        self.play(FadeIn(a), FadeIn(a.labels), Create(curve), run_time=self.rt(.08))

    def beat_e7(self, T):
        t0 = self.now()
        a = self.ax
        old = self.board_items[:-1]
        self.play(*[FadeOut(m) for m in old], run_time=self.rt(.03))
        self.board_items = self.board_items[-1:]
        self.write_board(self.M('e3_s4', 1.5), frac=.12)
        pt = always_redraw(lambda: Dot(a.c2p(self.tau.get_value(), tank_volume(self.tau.get_value())),
                                       radius=.08, color=GOLD))
        info = always_redraw(lambda: VGroup(
            tx(f't = {vn(self.tau.get_value(), 1)} phút', 24, WHITE),
            tx(f'V = {vn(tank_volume(self.tau.get_value()), 1)} lít', 24, CYAN, bold=True),
        ).arrange(RIGHT, buff=.6).move_to([BOARD_X, -2.3, 0], aligned_edge=LEFT))
        self.wait_until(.36, t0)
        self.play(FadeIn(pt), FadeIn(info), run_time=self.rt(.04))
        self.play(self.tau.animate.set_value(4), run_time=self.rt(.42), rate_func=linear)
        for m in (pt, info, self.tank_g[0]):
            m.clear_updaters()
        mark = VGroup(dashed(a.c2p(4, 0), a.c2p(4, 90), color=GOLD, stroke_width=2),
                      dashed(a.c2p(0, 90), a.c2p(4, 90), color=GOLD, stroke_width=2))
        self.play(Create(mark), Indicate(pt, color=GOLD), run_time=self.rt(.06))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('BẪY KINH ĐIỂN', CORAL, 22).move_to([0, 2.5, 0])
        ok = VGroup(tx('Tổng, hiệu:', 24, SOFT), self.M('sum3', 1.5), check()).arrange(RIGHT, buff=.3) \
            .move_to([0, 1.25, 0])
        bad = VGroup(tx('Tích:', 24, SOFT), self.M('trap1', 1.6)).arrange(RIGHT, buff=.3).move_to([0, -.2, 0])
        stamp = badge('SAI!', CORAL, 30).next_to(bad, DOWN, buff=.45)
        self.play(FadeIn(head), run_time=self.rt(.05))
        self.play(FadeIn(ok[0]), Write(ok[1]), Create(ok[2]), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.play(FadeIn(bad[0]), Write(bad[1]), run_time=self.rt(.14))
        self.wait_until(.85, t0)
        self.play(FadeIn(stamp, scale=1.6), run_time=self.rt(.06))

    def beat_x2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((0, 2.2, 1), (0, 5.2, 1), (1, 2), (1, 2, 3, 4, 5))
        self.show_axes(a)
        self.write_board(self.heading('PHẢN VÍ DỤ: f = g = x'), self.M('trap_ok', 1.15), frac=.12)
        self.wait_until(.25, t0)
        self.write_board(self.M('trap_bad', 1.1), frac=.12)
        self.wait_until(.42, t0)
        self.write_board(self.M('trap_chk', 1.4), frac=.08)
        fx = clipped(a, lambda v: v * v, 0, 2.2, CYAN, 4)
        A = clipped(a, lambda v: v ** 3 / 3, 0, 2.2, GREEN, 4)
        B = clipped(a, lambda v: v ** 4 / 4, 0, 2.2, CORAL, 4)
        names = VGroup(tx('f = x²', 18, CYAN, bold=True), tx('x³/3', 18, GREEN, bold=True),
                       tx('x⁴/4', 18, CORAL, bold=True)).arrange(RIGHT, buff=.45).move_to(a.c2p(.85, 4.85))
        self.wait_until(.6, t0)
        self.play(Create(fx), Create(A), Create(B), FadeIn(names), run_time=self.rt(.07))
        xt = ValueTracker(.5)
        live = always_redraw(lambda: VGroup(
            tangent(a, xt.get_value(), xt.get_value() ** 3 / 3, xt.get_value() ** 2, 1.2, GREEN),
            tangent(a, xt.get_value(), xt.get_value() ** 4 / 4, xt.get_value() ** 3, 1.2, CORAL)))
        reading = always_redraw(lambda: tx(
            f'f(x) = {vn(xt.get_value() ** 2)}   ·   dốc x³/3 = {vn(xt.get_value() ** 2)}   ·   '
            f'dốc x⁴/4 = {vn(xt.get_value() ** 3)}', 19, WHITE).move_to([BOARD_X, -2.35, 0], aligned_edge=LEFT))
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.03))
        self.play(xt.animate.set_value(1.7), run_time=self.rt(.22), rate_func=linear)
        live.clear_updaters()
        reading.clear_updaters()

    def beat_x3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi F là một nguyên hàm của f trên ℝ. Xét các mệnh đề:', 24, WHITE)
        items = (self.M('tf_a', 1.2), self.M('tf_b', 1.2),
                 VGroup(tx('Nếu', 22, WHITE), self.M('tf_c', 1.2)).arrange(RIGHT, buff=.2), self.M('tf_d', 1.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.32, .72))

    def beat_x4(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.07))
        self.wait_until(.25, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.07))
        why = VGroup(tx('Thử lại:', 22, SOFT), self.M('tf_b_chk', 1.1), tx('≠ x·f(x)', 22, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).move_to([0, -2.45, 0]).to_edge(LEFT, buff=.9)
        self.wait_until(.5, t0)
        self.play(FadeIn(why[0]), Write(why[1]), FadeIn(why[2]), run_time=self.rt(.14))
        self.x4_why = why

    def beat_x5(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x4_why), run_time=self.rt(.03))
        c_calc = VGroup(tx('c)', 22, GOLD, bold=True), self.M('tf_c_calc', 1.1)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.45, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(c_calc), run_time=self.rt(.1))
        self.play(self.tf_mark(2, True), run_time=self.rt(.06))
        self.wait_until(.52, t0)
        d_calc = VGroup(tx('d)', 22, GOLD, bold=True), self.M('tf_d_calc', 1.1)).arrange(RIGHT, buff=.2) \
            .move_to([3.3, -2.45, 0])
        self.play(FadeIn(d_calc), run_time=self.rt(.1))
        self.play(self.tf_mark(3, True), run_time=self.rt(.06))
        self.wait_until(.85, t0)
        key = tx('Đáp án:  a) Đ   b) S   c) Đ   d) Đ', 22, GOLD, bold=True).move_to([0, -3.0, 0])
        self.play(FadeIn(key, shift=UP * .1), run_time=self.rt(.06))

    def beat_x6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((-.4, 2.4, 1), (-1, 14, 2), (1, 2), (2, 4, 6, 8, 10, 12))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.15), frac=.12)
        self.wait_until(.3, t0)
        self.write_board(self.M('sa_s1', 1.25), frac=.08)
        self.wait_until(.5, t0)
        self.write_board(self.M('sa_s2', 1.2), frac=.08)
        F = clipped(a, lambda v: 2 * v ** 3 - 2 * v * v + v + 2, -.4, 2.4, GOLD, 4.5)
        A = dot(a, 1, 3, CYAN, .09)
        self.play(Create(F), GrowFromCenter(A), FadeIn(tx('(1; 3)', 18, CYAN, bold=True).next_to(A, RIGHT, buff=.1)),
                  run_time=self.rt(.07))
        self.wait_until(.78, t0)
        P = dot(a, 2, 12, GREEN, .09)
        guide = VGroup(dashed(a.c2p(2, 0), a.c2p(2, 12), color=GREEN, stroke_width=2),
                       dashed(a.c2p(0, 12), a.c2p(2, 12), color=GREEN, stroke_width=2))
        self.play(Create(guide), GrowFromCenter(P), run_time=self.rt(.04))
        self.write_board(self.M('sa_s3', 1.35), self.answer_sheet('12'), frac=.08)

    def beat_x7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO THỰC CHIẾN: ĐỔI VỀ LŨY THỪA', GOLD, 21).move_to([0, 2.55, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        cards = VGroup()
        for i, key in enumerate(('cv1', 'cv2', 'cv3')):
            c = card(3.9, 1.6, (CYAN, GREEN, PURPLE)[i]).move_to([-4.2 + 4.2 * i, 1.0, 0])
            cards.add(VGroup(c, self.M(key, 1.6).move_to(c)))
        for frac, cd in zip((.2, .33, .45), cards):
            self.wait_until(frac, t0)
            self.play(FadeIn(cd, shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.62, t0)
        ex = VGroup(tx('Ví dụ', 22, SOFT), self.M('cv_ex', 1.6)).arrange(RIGHT, buff=.4).move_to([0, -1.3, 0])
        self.play(FadeIn(ex[0]), Write(ex[1]), run_time=self.rt(.14))
        self.play(FadeIn(self.box(ex[1], GREEN)), run_time=self.rt(.04))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Hàm lũy thừa', 'sum1', 'α ≠ −1, trên khoảng hàm xác định'),
                                ('Hằng số ra ngoài', 'sum2', 'với k ≠ 0'),
                                ('Tách tổng, hiệu', 'sum3', 'Tích, thương: KHÔNG tách – khai triển hoặc chia trước')),
                           fracs=(.04, .4, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm (x > 0)', 'hw2'), ('Biết', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.05, .22, .42))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.2), self.M('next2', 1.1)])


class INT02_SMOKE(INT02):
    smoke = True
