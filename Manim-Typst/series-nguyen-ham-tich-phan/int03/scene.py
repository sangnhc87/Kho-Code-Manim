"""INT03 – Nguyên hàm của 1/x và hàm số mũ.

    python scripts/build_typst.py --ep int03
    python scripts/prepare_voice.py --ep int03 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int03/scene.py INT03
    python scripts/finalize.py --ep int03

One method per narration beat (int03/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Circle, Create, Dot, FadeIn, FadeOut, GrowFromCenter, Indicate,
                   LaggedStart, Line, Transform, ValueTracker, VGroup, Write, always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, cross, dashed, dot, para, tangent, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def bacteria(t):
    return 500 * math.exp(t) + 1000


class INT03(LessonScene):
    EP = 'int03'

    # ================================================================ helpers
    def std_axes(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.55), center=kw.pop('center', [LEFT_CX, -.12, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def show_axes(self, a, frac=.05):
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(frac))

    def centre(self, *mobs, top=2.55, gap=.42):
        g = VGroup(*mobs).arrange(DOWN, buff=gap)
        g.move_to([0, top, 0], aligned_edge=UP)
        return g

    def ln_axes(self, yr=(-2.5, 2.5, 1), yt=(-2, -1, 1, 2)):
        return self.std_axes((-4.3, 4.3, 1), yr, (-4, -2, 2, 4), yt)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        rule = self.M('pow_alpha', 1.6).move_to([0, 2.3, 0])
        self.play(Write(rule), run_time=self.rt(.1))
        self.wait_until(.22, t0)
        y = .55
        axis = Line([-5.2, y, 0], [5.2, y, 0], color=SOFT, stroke_width=3)
        marks = VGroup()
        for v in range(-3, 4):
            p = [1.5 * v, y, 0]
            marks.add(Line([p[0], y - .08, 0], [p[0], y + .08, 0], color=SOFT, stroke_width=2),
                      tx(vn(v, 0), 18, SOFT).move_to([p[0], y - .35, 0]))
        name = tx('số mũ α', 18, SOFT).move_to([5.2, y + .35, 0])
        ok = Line([-5.2, y, 0], [5.2, y, 0], color=GREEN, stroke_width=6)
        self.play(Create(axis), FadeIn(marks), FadeIn(name), run_time=self.rt(.07))
        self.play(Create(ok), run_time=self.rt(.08))
        hole = VGroup(Circle(radius=.16, color=CORAL, stroke_width=4).set_fill('#0B1221', 1).move_to([-1.5, y, 0]),
                      tx('?', 40, CORAL, bold=True).move_to([-1.5, y + .65, 0]))
        self.wait_until(.36, t0)
        self.play(GrowFromCenter(hole), run_time=self.rt(.06))
        self.wait_until(.48, t0)
        q = self.M('inv1_q', 1.6).move_to([-2.6, -1.35, 0])
        self.play(Write(q), run_time=self.rt(.08))
        self.wait_until(.72, t0)
        ex = VGroup(self.M('d_exp', 1.6), tx('đạo hàm bằng chính nó', 20, GOLD, bold=True)) \
            .arrange(DOWN, buff=.15).move_to([3.0, -1.5, 0])
        self.play(Write(ex[0]), FadeIn(ex[1]), run_time=self.rt(.1))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Vì sao có trị tuyệt đối?', 'Hai nhánh của 1/x và trị tuyệt đối'),
                         ('Nguyên hàm eˣ và aˣ', 'Số e: hàm có đạo hàm bằng chính nó'),
                         ('Hai cái bẫy', 'Hằng số trên hai khoảng · nhầm mũ với lũy thừa')], t0,
                        fracs=(.12, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((0, 4.3, 1), (-2.5, 3.2, 1), (1, 2, 3, 4), (-2, -1, 1, 2, 3))
        self.show_axes(a)
        self.write_board(badge('x > 0', CYAN, 20), self.M('d_ln', 1.4), frac=.12)
        self.wait_until(.3, t0)
        self.write_board(self.M('i_ln_pos', 1.3), frac=.1)
        self.wait_until(.58, t0)
        self.verify_plot(a, lambda v: 1 / v, math.log, .45, 3.8, .3, x_min=.3, readout_at=(BOARD_X, -2.3))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ln_axes()
        self.ax = a
        self.show_axes(a)
        right = clipped(a, math.log, .05, 4.3, GOLD, 4.5)
        self.play(Create(right), run_time=self.rt(.06))
        self.write_board(badge('x < 0', PURPLE, 20), tx('ln x không xác định → lấy đối xứng qua Oy', 22, SOFT),
                         frac=.1)
        self.wait_until(.25, t0)
        left = right.copy()
        self.play(left.animate.flip(UP, about_point=a.c2p(0, 0)).set_color(PURPLE), run_time=self.rt(.14))
        lab = tx('y = ln(−x)', 20, PURPLE, bold=True).move_to(a.c2p(-2.6, 1.7))
        self.play(FadeIn(lab), run_time=self.rt(.04))
        self.wait_until(.48, t0)
        self.write_board(self.M('d_lnneg', 1.3), frac=.12)
        self.wait_until(.72, t0)
        tan = VGroup(tangent(a, -2, math.log(2), -.5, 2.2), dot(a, -2, math.log(2)))
        self.play(Create(tan), run_time=self.rt(.06))
        self.write_board(tx('tại x = −2: độ dốc = −0,5 = 1/(−2)', 22, GOLD, bold=True), frac=.06)
        self.lnR, self.lnL, self.tan2 = right, left, VGroup(tan, lab)

    def beat_c3(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.tan2), run_time=self.rt(.03))
        self.clear_board(.03)
        self.write_board(self.heading('GỘP HAI TRƯỜNG HỢP'), frac=.05)
        m = self.M('i_ln', 1.8)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m)), self.lnL.animate.set_color(GOLD), run_time=self.rt(.06))
        lab = tx('y = ln|x|', 22, GOLD, bold=True).move_to(a.c2p(2.9, 1.75))
        f = VGroup(clipped(a, lambda v: 1 / v, .05, 4.3, CYAN, 2.5), clipped(a, lambda v: 1 / v, -4.3, -.05, CYAN, 2.5))
        self.play(FadeIn(lab), Create(f), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.write_board(para('Thiếu trị tuyệt đối, công thức sai với mọi x < 0.', 23, CORAL, width=30, bold=True),
                         frac=.08)
        self.lab3 = lab

    def beat_c4(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.lab3), run_time=self.rt(.03))
        self.clear_board(.03)
        self.write_board(badge('LƯU Ý CHUYÊN SÂU', CORAL, 19), self.M('piece_ln', 1.25), frac=.14)
        ghosts = VGroup(self.lnR.copy().set_stroke(opacity=.25), self.lnL.copy().set_stroke(opacity=.25))
        self.add(ghosts)
        self.wait_until(.4, t0)
        r2 = clipped(a, lambda v: math.log(v) + 1, .05, 4.3, GREEN, 4.5)
        l2 = clipped(a, lambda v: math.log(-v) - 1, -4.3, -.05, PURPLE, 4.5)
        self.play(Transform(self.lnR, r2), FadeIn(tx('C₁ = 1', 22, GREEN, bold=True).move_to(a.c2p(2.8, 2.25))),
                  run_time=self.rt(.12))
        self.play(Transform(self.lnL, l2), FadeIn(tx('C₂ = −1', 22, PURPLE, bold=True).move_to(a.c2p(-2.8, -2.1))),
                  run_time=self.rt(.12))
        self.write_board(tx('Đạo hàm vẫn bằng 1/x trên cả hai nhánh.', 22, SOFT), frac=.06)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2.5, 2.1, 1), (-.5, 7.6, 1), (-2, -1, 1, 2), (2, 4, 6))
        self.show_axes(a)
        self.write_board(self.heading('HÀM SỐ e MŨ x'), self.M('d_exp', 1.6), frac=.1)
        self.wait_until(.25, t0)
        m = self.M('i_exp', 1.7)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m)), run_time=self.rt(.04))
        curve = clipped(a, math.exp, -2.5, 2.1, GOLD, 4.5)
        self.play(Create(curve), run_time=self.rt(.06))
        xt = ValueTracker(-1.6)
        live = always_redraw(lambda: VGroup(
            Line(a.c2p(xt.get_value(), 0), a.c2p(xt.get_value(), math.exp(xt.get_value())), color=CYAN, stroke_width=5),
            tangent(a, xt.get_value(), math.exp(xt.get_value()), math.exp(xt.get_value()), 1.7),
            Dot(a.c2p(xt.get_value(), math.exp(xt.get_value())), radius=.08, color=GOLD)))
        reading = always_redraw(lambda: VGroup(
            tx(f'chiều cao = {vn(math.exp(xt.get_value()))}', 23, CYAN, bold=True),
            tx(f'độ dốc     = {vn(math.exp(xt.get_value()))}', 23, GOLD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.14).move_to([BOARD_X, -2.0, 0], aligned_edge=LEFT))
        self.wait_until(.52, t0)
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(xt.animate.set_value(1.85), run_time=self.rt(.36), rate_func=linear)
        live.clear_updaters()
        reading.clear_updaters()

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.std_axes((-2, 2, 1), (-.5, 5.2, 1), (-1, 1), (1, 2, 3, 4, 5))
        self.show_axes(a)
        self.write_board(self.heading('VÌ SAO LÀ SỐ e?'),
                         para('Độ dốc của a mũ x tại x = 0 bằng ln a.', 23, WHITE, width=34), frac=.1)
        base = ValueTracker(1.6)
        ref = dashed(a.c2p(-1.5, -.5), a.c2p(2, 3), color=SOFT, stroke_width=2)
        ref_lab = tx('độ dốc 1', 17, SOFT).move_to(a.c2p(1.55, 2.0))
        live = always_redraw(lambda: VGroup(
            clipped(a, lambda v: base.get_value() ** v, -2, 2, CYAN, 4.5),
            tangent(a, 0, 1, math.log(base.get_value()), 2.4),
            Dot(a.c2p(0, 1), radius=.08, color=GOLD)))
        reading = always_redraw(lambda: tx(
            f'a = {vn(base.get_value())}  →  độ dốc tại 0 = ln a = {vn(math.log(base.get_value()))}', 23, GOLD,
            bold=True).move_to([BOARD_X, -.9, 0], aligned_edge=LEFT))
        self.wait_until(.2, t0)
        self.play(FadeIn(live), FadeIn(reading), Create(ref), FadeIn(ref_lab), run_time=self.rt(.05))
        self.play(base.animate.set_value(4), run_time=self.rt(.22), rate_func=smooth)
        self.play(base.animate.set_value(math.e), run_time=self.rt(.18), rate_func=smooth)
        live.clear_updaters()
        reading.clear_updaters()
        win = badge('a = e ≈ 2,718  →  độ dốc tại 0 bằng đúng 1', GREEN, 20).move_to([BOARD_X, -1.8, 0],
                                                                                    aligned_edge=LEFT)
        self.play(FadeIn(win, scale=1.1), Indicate(live[1], color=GREEN), run_time=self.rt(.07))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('NGUYÊN HÀM CỦA a MŨ x', 26, GOLD, bold=True)
        d1 = self.M('d_ax', 1.6)
        mid = tx('chia hai vế cho ln a  (a ≠ 1 nên ln a ≠ 0)', 20, SOFT)
        d2 = self.M('d_ax2', 1.6)
        res = self.M('i_ax', 1.7)
        self.centre(head, d1, mid, d2, res, top=2.8, gap=.3)
        self.play(FadeIn(head), Write(d1), run_time=self.rt(.12))
        self.wait_until(.38, t0)
        self.play(FadeIn(mid), Write(d2), run_time=self.rt(.14))
        self.wait_until(.64, t0)
        self.play(Write(res), run_time=self.rt(.12))
        self.play(FadeIn(self.box(res)), run_time=self.rt(.05))

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('ÁP DỤNG', 24, GOLD, bold=True)
        e1, e2, e3 = self.M('ex_2x', 1.35), self.M('ex_half', 1.2), self.M('ex_10x', 1.35)
        note = tx('0 < a < 1  ⇒  ln a < 0: kết quả mang dấu trừ', 21, CORAL, bold=True)
        self.centre(head, e1, e2, note, e3, top=2.8, gap=.3)
        self.play(FadeIn(head), Write(e1), run_time=self.rt(.12))
        self.wait_until(.25, t0)
        self.play(Write(e2), run_time=self.rt(.16))
        self.play(FadeIn(note), run_time=self.rt(.05))
        self.wait_until(.75, t0)
        self.play(Write(e3), run_time=self.rt(.1))

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BẪY: NHẦM HÀM MŨ VỚI LŨY THỪA', CORAL, 21).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        cols = []
        for i, (title, key, col) in enumerate((('x ở CƠ SỐ: lũy thừa', 'pow_vs', CYAN),
                                              ('x ở SỐ MŨ: hàm mũ', 'exp_vs', GOLD))):
            c = card(5.9, 2.3, col).move_to([-3.2 + 6.4 * i, .9, 0])
            t = tx(title, 22, col, bold=True).move_to(c.get_top() + DOWN * .4)
            m = self.M(key, 1.45).move_to(c.get_center() + DOWN * .25)
            cols.append(VGroup(c, t, m))
        for frac, cd in zip((.12, .3), cols):
            self.wait_until(frac, t0)
            self.play(FadeIn(cd, shift=UP * .2), run_time=self.rt(.08))
        self.wait_until(.62, t0)
        bad = VGroup(self.M('trap_ax', 1.6), cross(CORAL, .4), tx('SAI', 26, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.35).move_to([0, -1.6, 0])
        self.play(Write(bad[0]), run_time=self.rt(.12))
        self.play(Create(bad[1]), FadeIn(bad[2]), run_time=self.rt(.05))

    def beat_c10(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('BẢNG NGUYÊN HÀM CƠ BẢN (ĐẾN TẬP 3)', 24, GOLD, bold=True).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        keys = (('tbl6', False), ('tbl1', False), ('tbl2', False), ('tbl3', True), ('tbl4', True), ('tbl5', True))
        cells = VGroup()
        for i, (key, new) in enumerate(keys):
            r, c = divmod(i, 2)
            box = card(6.1, 1.35, GOLD if new else '#293A54').move_to([-3.15 + 6.3 * c, 1.45 - 1.55 * r, 0])
            g = VGroup(box, self.M(key, 1.3, max_w=5.0).move_to(box))
            if new:
                g.add(badge('MỚI', GOLD, 14).move_to(box.get_corner(UP + RIGHT) + LEFT * .45 + DOWN * .25))
            cells.add(g)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .15) for c in cells[:3]], lag_ratio=.3), run_time=self.rt(.18))
        self.wait_until(.45, t0)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .15) for c in cells[3:]], lag_ratio=.3), run_time=self.rt(.2))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = badge('VÍ DỤ 1', GOLD, 20)
        task, s1, s2 = self.M('e1_task', 1.7), self.M('e1_s1', 1.45), self.M('e1_s2', 1.7)
        self.centre(tag, task, s1, s2, top=2.7, gap=.45)
        for m in (s1, s2):
            m.align_to(task, LEFT).shift(RIGHT * .6)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.12))
        self.wait_until(.3, t0)
        self.play(Write(s1), run_time=self.rt(.16))
        self.wait_until(.6, t0)
        self.play(Write(s2), run_time=self.rt(.14))
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.04))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.std_axes((0, 3.3, 1), (-3, 8.5, 1), (1, 2, 3), (-2, 2, 4, 6, 8))
        self.show_axes(a)
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.25), frac=.1, gap=.24)
        self.wait_until(.18, t0)
        self.write_board(self.M('e2_s1', 1.15), frac=.1, gap=.24)
        self.wait_until(.36, t0)
        s2 = self.M('e2_s2', 1.25)
        self.write_board(s2, frac=.1, gap=.24)
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.04))
        self.wait_until(.56, t0)
        self.verify_plot(a, lambda v: (v * v + 2 * v - 3) / v, lambda v: v * v / 2 + 2 * v - 3 * math.log(v),
                         .7, 3.1, .26, x_min=.55, readout_at=(BOARD_X, -2.55))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = badge('VÍ DỤ 3', GOLD, 20)
        task, s1, s2 = self.M('e3_task', 1.8), self.M('e3_s1', 1.5), self.M('e3_s2', 1.7)
        self.centre(tag, task, s1, s2, top=2.6, gap=.5)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.12))
        self.wait_until(.28, t0)
        self.play(Write(s1), run_time=self.rt(.16))
        self.wait_until(.66, t0)
        self.play(Write(s2), run_time=self.rt(.12))
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.04))

    # ---------------------------------------------------------------- bacteria
    def dish(self, t_fn, center=(-4.6, -2.05), radius=.85):
        cx, cy = center
        rnd = random.Random(7)
        pts = []
        while len(pts) < 60:
            px, py = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            if px * px + py * py < .82:
                pts.append((cx + px * radius, cy + py * radius))
        rim = Circle(radius=radius, color=SOFT, stroke_width=3).move_to([cx, cy, 0])
        cells = always_redraw(lambda: VGroup(*[Dot([px, py, 0], radius=.045, color=GREEN)
                                               for px, py in pts[:round(bacteria(t_fn()) / 100)]]))
        count = always_redraw(lambda: VGroup(
            tx(f't = {vn(t_fn(), 1)} giờ', 20, WHITE),
            tx(f'N ≈ {round(bacteria(t_fn()))} con', 22, GREEN, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.12).next_to(rim, RIGHT, buff=.35))
        return VGroup(rim, cells, count)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.tau = ValueTracker(0)
        self.petri = self.dish(self.tau.get_value)
        self.play(FadeIn(self.petri), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), tx('Tốc độ tăng của quần thể vi khuẩn (con/giờ):', 22, WHITE),
                         self.M('e4_task', 1.4), frac=.3)
        self.wait_until(.72, t0)
        self.write_board(tx('Sau 2 giờ:  N(2) ≈ ?', 26, GOLD, bold=True), frac=.08)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        a = axes((0, 2.2, 1), (0, 5000, 1000), 5.2, 3.0, center=[LEFT_CX, 1.15, 0], x_ticks=(1, 2),
                 y_ticks=(1000, 2000, 3000, 4000), x_label='t', y_label='N', label_size=14)
        self.ax = a
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(.05))
        self.write_board(self.M('e4_s1', 1.3), frac=.12)
        self.play(Create(clipped(a, bacteria, 0, 2.2, GREEN, 4)), run_time=self.rt(.06))
        self.wait_until(.36, t0)
        self.write_board(self.M('e4_s2', 1.25), frac=.12)
        self.wait_until(.66, t0)
        res = self.M('e4_s3', 1.45)
        self.write_board(res, frac=.1)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.04))

    def beat_e6(self, T):
        t0 = self.now()
        a = self.ax
        pt = always_redraw(lambda: Dot(a.c2p(self.tau.get_value(), bacteria(self.tau.get_value())), radius=.08,
                                       color=GOLD))
        self.play(FadeIn(pt), run_time=self.rt(.03))
        self.play(self.tau.animate.set_value(2), run_time=self.rt(.5), rate_func=linear)
        pt.clear_updaters()
        for m in self.petri[1:]:
            m.clear_updaters()
        guide = VGroup(dashed(a.c2p(2, 0), a.c2p(2, bacteria(2)), color=GOLD, stroke_width=2),
                       dashed(a.c2p(0, bacteria(2)), a.c2p(2, bacteria(2)), color=GOLD, stroke_width=2))
        self.play(Create(guide), Indicate(pt, color=GOLD), run_time=self.rt(.06))
        self.wait_until(.68, t0)
        self.write_board(badge('Trả lời ngắn: làm tròn → 4695', PURPLE, 19), frac=.06)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi F là một nguyên hàm của f trên (0; +∞). Xét các mệnh đề:', 24, WHITE)
        items = (self.M('tf_a', 1.2), self.M('tf_b', 1.2),
                 VGroup(tx('Nếu', 22, WHITE), self.M('tf_c', 1.15)).arrange(RIGHT, buff=.2), self.M('tf_d', 1.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.07))
        self.wait_until(.3, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.07))
        why = VGroup(tx('Đúng phải là:', 22, SOFT), self.M('ex_2x', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.wait_until(.6, t0)
        self.play(FadeIn(why[0]), Write(why[1]), run_time=self.rt(.12))
        self.x2_why = why

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_why), run_time=self.rt(.03))
        c = VGroup(tx('c)', 22, GOLD, bold=True), self.M('tf_c_calc', 1.1)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(c), run_time=self.rt(.1))
        self.play(self.tf_mark(2, True), run_time=self.rt(.06))
        self.wait_until(.52, t0)
        d = VGroup(tx('d)', 22, GOLD, bold=True), self.M('tf_d_calc', 1.1)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(c), FadeIn(d), run_time=self.rt(.1))
        self.play(self.tf_mark(3, False), run_time=self.rt(.06))
        self.wait_until(.86, t0)
        key = self.tf_key('ĐSĐS')
        self.play(FadeIn(key, shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ln_axes((-1.5, 5.2, 1), (1, 2, 3, 4, 5))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.0), frac=.12)
        self.wait_until(.36, t0)
        self.write_board(self.M('piece_ln', 1.05), self.M('sa_s2', 1.15), frac=.12)
        R = clipped(a, lambda v: math.log(v) + 2, .05, 4.3, GREEN, 4.5)
        L = clipped(a, lambda v: math.log(-v) + 3, -4.3, -.05, PURPLE, 4.5)
        pts = VGroup(dot(a, 1, 2, GREEN), dot(a, -1, 3, PURPLE))
        self.play(Create(R), Create(L), FadeIn(pts), run_time=self.rt(.08))
        self.wait_until(.72, t0)
        ans = VGroup(dot(a, math.e, 3, GOLD, .09), dot(a, -math.e, 4, GOLD, .09),
                     tx('F(e) = 3', 18, GOLD, bold=True).next_to(a.c2p(math.e, 3), DOWN + RIGHT, buff=.05),
                     tx('F(−e) = 4', 18, GOLD, bold=True).next_to(a.c2p(-math.e, 4), DOWN + LEFT, buff=.05))
        self.play(FadeIn(ans), run_time=self.rt(.05))
        self.write_board(self.M('sa_s3', 1.25), self.answer_sheet('7'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO NHẬN DẠNG NHANH', GOLD, 21).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        rows = (('rec1', 'nhớ trị tuyệt đối, xét từng khoảng', CYAN), ('rec2', 'giữ nguyên', GREEN),
                ('rec3', 'giữ nguyên rồi chia ln a', PURPLE))
        for i, (key, note, col) in enumerate(rows):
            c = card(10.8, 1.15, col).move_to([0, 1.45 - 1.3 * i, 0])
            g = VGroup(c, self.M(key, 1.45).move_to(c.get_center() + LEFT * 2.6),
                       tx(note, 22, col, bold=True).move_to(c.get_center() + RIGHT * 2.4))
            self.wait_until((.04, .3, .45)[i], t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.07))
        self.wait_until(.72, t0)
        tip = tx('Biến nằm ở cơ số (xⁿ)  →  quay về quy tắc lũy thừa', 22, CORAL, bold=True).move_to([0, -2.45, 0])
        self.play(FadeIn(tip, shift=UP * .1), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Hàm 1/x', 'sum1', 'Trên từng khoảng, nhớ trị tuyệt đối'),
                                ('Hàm eˣ', 'sum2', 'Đạo hàm bằng chính nó'),
                                ('Hàm aˣ', 'sum3', 'Với 0 < a ≠ 1')),
                           fracs=(.04, .45, .66))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Biết', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.05, .2, .45))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.1), self.M('next2', 1.2)])


class INT03_SMOKE(INT03):
    smoke = True
