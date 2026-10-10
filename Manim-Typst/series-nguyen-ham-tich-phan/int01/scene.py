"""INT01 – Đi ngược đạo hàm: bản chất nguyên hàm.

    python scripts/build_typst.py --ep int01
    python scripts/prepare_voice.py --ep int01 --voice off|on
    manim -ql -r 426,240 --fps 8 int01/scene.py INT01_SMOKE   # technical pass
    manim -ql -r 854,480 --fps 24 int01/scene.py INT01        # preview
    manim -qh -r 1920,1080 --fps 30 int01/scene.py INT01      # Full HD
    python scripts/finalize.py --ep int01                      # SRT + YouTube description

One method per narration beat (see int01/lesson.py). All graphs use real
coordinates (Axes.c2p); every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, UL, Arrow, Brace, Circumscribe, Create, CurvedArrow,
                   DashedLine, Dot, FadeIn, FadeOut, GrowArrow, GrowFromCenter, Indicate,
                   LaggedStart, Line, MoveAlongPath, ParametricFunction, ReplacementTransform,
                   RoundedRectangle, SurroundingRectangle, Transform, ValueTracker, VGroup, Write,
                   always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import (badge, car, card, check, clipped, cross, dashed, dot, gauge, para, slope_field,  # noqa: E402
                        tangent, tx, vn, axes)
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import (CORAL, CYAN, DIM, GOLD, GREEN, PANEL, PANEL_2, PURPLE, SOFT,  # noqa: E402
                          STROKE, WHITE)

# Road used by the hook and example 2: 0 … 16 m mapped onto the screen.
ROAD_Y = -2.45
ROAD_X0, ROAD_X1, ROAD_M = -6.1, 6.1, 16.0


def road_x(meters):
    return ROAD_X0 + (ROAD_X1 - ROAD_X0) * meters / ROAD_M


def s_of(t):
    return t * t + t + 2


def v_of(t):
    return 2 * t + 1


class INT01(LessonScene):
    EP = 'int01'

    # ================================================================ helpers
    def road(self, y=ROAD_Y):
        g = VGroup(Line([ROAD_X0 - .2, y, 0], [ROAD_X1 + .2, y, 0], color=SOFT, stroke_width=3))
        for m in range(0, 17, 2):
            p = np.array([road_x(m), y, 0])
            g.add(Line(p + UP * .08, p + DOWN * .08, color=SOFT, stroke_width=2),
                  tx(f'{m}', 15, SOFT).move_to(p + DOWN * .3))
        g.add(tx('mét', 15, DIM).move_to([ROAD_X1 + .05, y - .62, 0]))
        return g

    def car_at(self, meters, y=ROAD_Y):
        c = car(CORAL, .85)
        return c.move_to([road_x(meters), y + .33, 0])

    def core_axes(self):
        a = axes((-2.5, 2.5, 1), (-3, 7, 1), 6.0, 5.55, center=[LEFT_CX, -.12, 0],
                 x_ticks=(-2, -1, 1, 2), y_ticks=(-2, 2, 4, 6))
        return a

    def heading(self, text, color=GOLD):
        return tx(text, 22, color, bold=True)

    def write_board(self, *mobs, frac=0.08, gap=0.32):
        for m in mobs:
            self.board(m, gap=gap)
        self.play(LaggedStart(*[Write(m) if m.__class__.__name__ == 'SVGMobject' else FadeIn(m, shift=.1 * UP)
                                for m in mobs], lag_ratio=.35), run_time=self.rt(frac))

    def wait_until(self, frac, start):
        """Hold until ``frac`` of the beat has elapsed (keeps visuals on the narration)."""
        target = start + frac * self.T
        now = self.renderer.time
        if target - now > 1.5 / 30:
            self.wait(target - now)

    def now(self):
        return self.renderer.time

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        road = self.road()
        tau = ValueTracker(0)
        vehicle = self.car_at(2)
        vehicle.add_updater(lambda m: m.move_to([road_x(s_of(tau.get_value())), ROAD_Y + .33, 0]))
        meter = gauge(lambda: v_of(tau.get_value()), 8, center=np.array([3.9, 1.05, 0]), radius=1.25)
        meter_title = tx('ĐỒNG HỒ TỐC ĐỘ', 17, CYAN, bold=True).next_to(meter, UP, buff=.18)
        odo_box = card(4.2, 1.35).move_to([-3.6, 1.15, 0])
        odo_title = tx('ĐỒNG HỒ QUÃNG ĐƯỜNG', 17, SOFT, bold=True).move_to(odo_box.get_top() + DOWN * .32)
        odo_val = tx('— — — m', 30, DIM, bold=True).move_to(odo_box.get_center() + DOWN * .2)
        broken = cross(CORAL, .4).next_to(odo_val, RIGHT, buff=.3)
        q = tx('?', 40, GOLD, bold=True)
        q.add_updater(lambda m: m.next_to(vehicle, UP, buff=.12))
        self.play(Create(road), FadeIn(vehicle, shift=RIGHT * .3), run_time=self.rt(.07))
        self.play(FadeIn(odo_box), FadeIn(odo_title), FadeIn(odo_val), run_time=self.rt(.05))
        self.play(Create(broken), run_time=self.rt(.04))
        self.play(FadeIn(meter), FadeIn(meter_title), run_time=self.rt(.06))
        self.play(tau.animate.set_value(2.4), FadeIn(q), run_time=self.rt(.5), rate_func=linear)
        self.play(Indicate(q, color=GOLD, scale_factor=1.4), run_time=self.rt(.08))
        vehicle.clear_updaters()
        q.clear_updaters()
        self.wait_until(.9, t0)

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        box_s = VGroup(card(3.6, 1.6, CYAN), tx('VỊ TRÍ', 20, SOFT, bold=True), tx('s(t)', 40, WHITE, slant=True))
        box_v = VGroup(card(3.6, 1.6, GOLD), tx('VẬN TỐC', 20, SOFT, bold=True), tx('v(t)', 40, WHITE, slant=True))
        for b, x in ((box_s, -3.4), (box_v, 3.4)):
            b[0].move_to([x, .5, 0])
            b[1].move_to(b[0].get_top() + DOWN * .35)
            b[2].move_to(b[0].get_center() + DOWN * .18)
        top = Arrow([-1.45, 1.0, 0], [1.45, 1.0, 0], color=CYAN, buff=0, stroke_width=6)
        top_lbl = tx('ĐẠO HÀM', 20, CYAN, bold=True).next_to(top, UP, buff=.12)
        grade = tx('đã học ở lớp 11', 16, SOFT).next_to(top_lbl, UP, buff=.08)
        bottom = Arrow([1.45, 0.0, 0], [-1.45, 0.0, 0], color=CORAL, buff=0, stroke_width=6)
        bottom_lbl = tx('?', 44, CORAL, bold=True).next_to(bottom, DOWN, buff=.12)
        hint = tx('Biết vận tốc tại mọi thời điểm  →  tìm lại vị trí?', 24, WHITE).move_to([0, -2.1, 0])
        self.play(FadeIn(box_s, shift=RIGHT * .2), run_time=self.rt(.07))
        self.play(FadeIn(box_v, shift=LEFT * .2), run_time=self.rt(.07))
        self.play(FadeIn(hint), run_time=self.rt(.06))
        self.wait_until(.42, t0)
        self.play(GrowArrow(top), FadeIn(top_lbl), FadeIn(grade), run_time=self.rt(.1))
        self.wait_until(.72, t0)
        self.play(GrowArrow(bottom), FadeIn(bottom_lbl, scale=1.5), run_time=self.rt(.1))
        self.bottom_lbl = bottom_lbl

    def beat_h3(self, T):
        t0 = self.now()
        name = tx('NGUYÊN HÀM', 24, CORAL, bold=True).move_to(self.bottom_lbl)
        self.play(ReplacementTransform(self.bottom_lbl, name), run_time=self.rt(.07))
        self.play(Circumscribe(name, color=CORAL), run_time=self.rt(.1))
        self.wait_until(.3, t0)
        self.clear_stage(.05)
        frame = card(10.6, 4.4, CYAN, PANEL, radius=.3, stroke_width=2.4).move_to([0, .1, 0])
        tag = badge('TẬP 01 / 36', CYAN, 20).move_to(frame.get_top() + DOWN * .55)
        title = tx('ĐI NGƯỢC ĐẠO HÀM', 58, WHITE, bold=True).move_to([0, .55, 0])
        sub = tx('Bản chất của nguyên hàm', 32, GOLD).next_to(title, DOWN, buff=.28)
        series = tx('Series Nguyên hàm – Tích phân – Ứng dụng chuyên sâu', 20, SOFT).next_to(sub, DOWN, buff=.42)
        self.play(FadeIn(frame), FadeIn(tag, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(Write(title), run_time=self.rt(.14))
        self.play(FadeIn(sub, shift=UP * .15), FadeIn(series), run_time=self.rt(.1))

    def beat_h4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('MỤC TIÊU CỦA BÀI', 26, GOLD, bold=True).move_to([0, 2.55, 0])
        goals = [('1', 'Nguyên hàm là gì?', 'Hiểu bằng hình ảnh, không học thuộc', CYAN),
                 ('2', 'Vì sao có hằng số C?', 'Họ đường cong và các tiếp tuyến song song', GREEN),
                 ('3', 'Chọn đúng một nguyên hàm', 'Dùng điều kiện ban đầu · bài toán chuyển động', GOLD)]
        cards = VGroup()
        for i, (n, title, desc, col) in enumerate(goals):
            c = card(4.05, 3.3, col).move_to([-4.3 + 4.3 * i, -.15, 0])
            num = tx(n, 54, col, bold=True).move_to(c.get_top() + DOWN * .7)
            t = para(title, 24, WHITE, width=18, bold=True, center=True).move_to(c.get_center() + DOWN * .05)
            d = para(desc, 17, SOFT, width=24, center=True).move_to(c.get_bottom() + UP * .62)
            cards.add(VGroup(c, num, t, d))
        self.play(FadeIn(head), run_time=self.rt(.05))
        for frac, cd in zip((.1, .3, .52), cards):
            self.wait_until(frac, t0)
            self.play(FadeIn(cd, shift=UP * .25), run_time=self.rt(.07))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.core_axes()
        self.ax = a
        self.play(Create(a), FadeIn(a.labels), run_time=self.rt(.18))
        self.write_board(self.heading('BÀI TOÁN'), tx('Tìm một hàm số F sao cho', 24, WHITE),
                         self.M('task', 1.5), tx('với mọi x thuộc ℝ.', 24, SOFT), frac=.3)
        self.play(Circumscribe(self.board_items[2], color=GOLD), run_time=self.rt(.14))

    def beat_c2(self, T):
        t0 = self.now()
        a = self.ax
        line = clipped(a, lambda v: 2 * v, -2.5, 2.5, CYAN, 4)
        lbl = tx('y = 2x', 22, CYAN, bold=True).move_to(a.c2p(-1.35, 6.1))
        tag = tx('đồ thị của ĐẠO HÀM', 17, CYAN).next_to(lbl, DOWN, buff=.1)
        pointer = Arrow(tag.get_right() + RIGHT * .05, a.c2p(1.9, 3.8), color=CYAN, buff=.1, stroke_width=3,
                        max_tip_length_to_length_ratio=.12)
        self.play(Create(line), FadeIn(lbl), FadeIn(tag), GrowArrow(pointer), run_time=self.rt(.12))
        self.write_board(self.M('f_2x', 1.3), frac=.06, gap=.45)
        xt = ValueTracker(0)
        mover = always_redraw(lambda: Dot(a.c2p(xt.get_value(), 2 * xt.get_value()), radius=.09, color=GOLD))
        guide = always_redraw(lambda: dashed(a.c2p(xt.get_value(), 0), a.c2p(xt.get_value(), 2 * xt.get_value()),
                                             color=GOLD, stroke_width=2))
        readout = always_redraw(lambda: VGroup(
            tx(f'x = {vn(xt.get_value())}', 26, WHITE),
            tx(f'độ dốc cần có của F:  {vn(2 * xt.get_value())}', 26, GOLD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.2).move_to([BOARD_X, -1.55, 0], aligned_edge=LEFT))
        self.play(FadeIn(mover), FadeIn(guide), FadeIn(readout), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.play(xt.animate.set_value(1), run_time=self.rt(.14))
        self.wait_until(.72, t0)
        self.play(xt.animate.set_value(-1), run_time=self.rt(.16))
        self.wait_until(.95, t0)
        for m in (mover, guide, readout):
            m.clear_updaters()
        self.c2_tmp = VGroup(mover, guide, readout)
        self.f_line = VGroup(line, lbl, tag, pointer)

    def beat_c3(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.c2_tmp), self.f_line.animate.set_opacity(.18), run_time=self.rt(.05))
        self.clear_board(.03)
        xs = np.arange(-2.25, 2.3, .5)
        ys = np.arange(-2.5, 6.6, .75)
        field = slope_field(a, lambda x, y: 2 * x, xs, ys, seg=.34, color=SOFT, width=2.2)
        self.field = field
        self.write_board(self.heading('TRƯỜNG HƯỚNG'),
                         para('Tại mỗi điểm (x; y), vẽ một đoạn nhỏ có hệ số góc bằng 2x.', 24, WHITE, width=32),
                         frac=.1)
        self.play(LaggedStart(*[Create(s) for s in field], lag_ratio=.012), run_time=self.rt(.3))
        self.wait_until(.55, t0)
        left = [s for s in field if s.get_center()[0] < a.c2p(0, 0)[0] - .01]
        right = [s for s in field if s.get_center()[0] > a.c2p(0, 0)[0] + .01]
        lbl_l = badge('dốc xuống', CORAL, 17).move_to(a.c2p(-1.5, 6.55))
        lbl_r = badge('dốc lên', GREEN, 17).move_to(a.c2p(1.5, 6.55))
        self.play(*[s.animate.set_color(CORAL) for s in left], FadeIn(lbl_l), run_time=self.rt(.07))
        self.play(*[s.animate.set_color(GREEN) for s in right], FadeIn(lbl_r), run_time=self.rt(.07))
        self.wait_until(.9, t0)
        self.play(*[s.animate.set_color(SOFT).set_opacity(.55) for s in field], FadeOut(lbl_l), FadeOut(lbl_r),
                  run_time=self.rt(.06))

    def stage_board_tail(self):
        """Mobjects on the right column (x > 0.3) that are not chrome."""
        return [m for m in self.stage() if m.get_center()[0] > .3]

    def clear_board(self, frac=.04):
        tail = self.stage_board_tail()
        if tail:
            self.play(*[FadeOut(m) for m in tail], run_time=self.rt(frac))
        self.board_items = []

    def trace_parabola(self, c, color, frac):
        a = self.ax
        reach = min(2.5, np.sqrt(7 - c))
        right = ParametricFunction(lambda u: a.c2p(u, u * u + c), t_range=[0, reach],
                                   color=color, stroke_width=4.5)
        left = ParametricFunction(lambda u: a.c2p(-u, u * u + c), t_range=[0, reach],
                                  color=color, stroke_width=4.5)
        start = Dot(a.c2p(0, c), radius=.1, color=GOLD)
        d1, d2 = Dot(a.c2p(0, c), radius=.07, color=color), Dot(a.c2p(0, c), radius=.07, color=color)
        self.play(GrowFromCenter(start), run_time=self.rt(.04))
        self.play(Create(right), Create(left), MoveAlongPath(d1, right), MoveAlongPath(d2, left),
                  run_time=self.rt(frac), rate_func=smooth)
        self.play(FadeOut(d1), FadeOut(d2), run_time=self.rt(.02))
        return VGroup(right, left), start

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_board(.04)
        self.write_board(self.heading('THẢ MỘT ĐIỂM XUẤT PHÁT'),
                         para('Đường cong luôn đi theo hướng của các đoạn nhỏ.', 24, SOFT, width=32), frac=.1)
        self.wait_until(.4, t0)
        curve, start = self.trace_parabola(0, CYAN, .3)
        self.parab0, self.start0 = curve, start
        f = self.M('F_x2', 1.5)
        self.write_board(f, frac=.08)

    def beat_c5(self, T):
        t0 = self.now()
        a = self.ax
        chk = self.M('x2_deriv', 1.4)
        self.write_board(chk, frac=.1)
        mark = check().next_to(chk, RIGHT, buff=.3)
        self.play(Create(mark), run_time=self.rt(.05))
        t1 = tangent(a, 1, 1, 2, 2.0)
        t2 = tangent(a, -1, 1, -2, 2.0)
        d1, d2 = dot(a, 1, 1), dot(a, -1, 1)
        self.play(Create(t1), FadeIn(d1), Create(t2), FadeIn(d2), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        concl = VGroup(tx('F(x) = x²  là  MỘT  nguyên hàm', 25, WHITE, bold=True),
                       tx('của  f(x) = 2x', 25, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        self.write_board(concl, frac=.1, gap=.45)
        box = SurroundingRectangle(concl, color=GOLD, buff=.16, corner_radius=.1)
        self.play(Create(box), run_time=self.rt(.07))
        self.c5_tmp = VGroup(t1, t2, d1, d2)

    def beat_c6(self, T):
        t0 = self.now()
        self.play(FadeOut(self.c5_tmp), run_time=self.rt(.03))
        self.clear_board(.03)
        self.write_board(self.heading('THẢ Ở CHỖ KHÁC?'), frac=.05)
        self.wait_until(.18, t0)
        c2, s2 = self.trace_parabola(2, GREEN, .2)
        self.write_board(tx('Thả tại (0; 2)  →  y = x² + 2', 25, GREEN), frac=.06)
        self.wait_until(.62, t0)
        c3, s3 = self.trace_parabola(-1, PURPLE, .2)
        self.write_board(tx('Thả tại (0; −1)  →  y = x² − 1', 25, PURPLE), frac=.06)
        self.family3 = VGroup(c2, s2, c3, s3)

    def beat_c7(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.family3), FadeOut(self.parab0), FadeOut(self.start0), run_time=self.rt(.03))
        self.clear_board(.03)
        C = ValueTracker(0)
        live = always_redraw(lambda: clipped(a, lambda v: v * v + C.get_value(), -2.5, 2.5, GOLD, 5))
        start = always_redraw(lambda: Dot(a.c2p(0, C.get_value()), radius=.1, color=GOLD))
        clabel = always_redraw(lambda: tx(f'C = {vn(C.get_value())}', 24, GOLD, bold=True)
                               .next_to(a.c2p(0, C.get_value()), RIGHT, buff=.15).shift(DOWN * .22))
        self.play(FadeIn(live), FadeIn(start), FadeIn(clabel), run_time=self.rt(.04))
        self.write_board(self.heading('HỌ NGUYÊN HÀM'), self.M('family', 1.6),
                         para('Mỗi giá trị của C cho một đồ thị. Tất cả đều khớp với trường hướng.', 24, SOFT,
                              width=32), frac=.12)
        ghosts = VGroup()
        for target in (3, -2, 1, -1, 2, 0):
            self.play(C.animate.set_value(target), run_time=self.rt(.085), rate_func=smooth)
            ghosts.add(clipped(a, lambda v, k=target: v * v + k, -2.5, 2.5, GOLD, 2).set_stroke(opacity=.28))
            self.add(ghosts[-1])
        for m in (live, start, clabel):
            m.clear_updaters()
        self.c7_live = VGroup(live, start, clabel)
        self.ghosts = ghosts

    def beat_c8(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.c7_live), FadeOut(self.ghosts), self.field.animate.set_opacity(.2),
                  run_time=self.rt(.03))
        self.clear_board(.03)
        cs = ((-1, PURPLE), (0, CYAN), (2, GREEN))
        curves = VGroup(*[clipped(a, lambda v, k=k: v * v + k, -2.5, 2.5, col, 4) for k, col in cs])
        self.play(Create(curves), run_time=self.rt(.08))
        self.write_board(self.heading('VÌ SAO C KHÔNG ẢNH HƯỞNG?'), self.M('c_deriv', 1.3), frac=.1)
        xt = ValueTracker(1)
        tans = always_redraw(lambda: VGroup(*[
            VGroup(tangent(a, xt.get_value(), xt.get_value() ** 2 + k, 2 * xt.get_value(), 1.7),
                   Dot(a.c2p(xt.get_value(), xt.get_value() ** 2 + k), radius=.07, color=GOLD))
            for k, _ in cs]))
        vline = always_redraw(lambda: DashedLine(a.c2p(xt.get_value(), -3), a.c2p(xt.get_value(), 7),
                                                 color=SOFT, stroke_width=1.6, dash_length=.1))
        self.wait_until(.36, t0)
        self.play(FadeIn(tans), FadeIn(vline), run_time=self.rt(.05))
        info = always_redraw(lambda: VGroup(
            tx('Cộng C: tịnh tiến lên / xuống', 23, WHITE),
            tx(f'Tại x = {vn(xt.get_value())}: cùng hệ số góc {vn(2 * xt.get_value())}', 23, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.18).move_to([BOARD_X, -.7, 0], aligned_edge=LEFT))
        self.play(FadeIn(info), run_time=self.rt(.04))
        self.play(xt.animate.set_value(-1.2), run_time=self.rt(.18))
        self.play(xt.animate.set_value(1.5), run_time=self.rt(.18))
        for m in (tans, vline, info):
            m.clear_updaters()

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        box = card(12.6, 2.75, GOLD, PANEL, radius=.2, stroke_width=2.2).move_to([0, 1.62, 0])
        head = badge('ĐỊNH NGHĨA', GOLD, 19).move_to(box.get_corner(UL) + RIGHT * 1.1 + DOWN * .02)
        l1 = tx('Cho hàm số f xác định trên K  (K là một khoảng, một đoạn hoặc một nửa khoảng).', 24, SOFT, max_w=11.6)
        l2 = tx('Hàm số F được gọi là nguyên hàm của f trên K nếu', 25, WHITE)
        m = self.M('def', 1.45)
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=.2).move_to(box.get_center() + UP * .45)
        m.move_to(box.get_center() + DOWN * .72)
        self.play(FadeIn(box), FadeIn(head), run_time=self.rt(.05))
        self.play(FadeIn(l1, shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(FadeIn(l2, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.62, t0)
        self.play(Write(m), run_time=self.rt(.14))
        self.play(Circumscribe(m, color=GOLD), run_time=self.rt(.1))

    def beat_c10(self, T):
        t0 = self.now()
        box = card(12.6, 2.95, CYAN, PANEL, radius=.2, stroke_width=2.2).move_to([0, -1.45, 0])
        head = badge('ĐỊNH LÝ', CYAN, 19).move_to(box.get_corner(UL) + RIGHT * .85 + DOWN * .02)
        l1 = tx('Nếu F là một nguyên hàm của f trên K thì mọi nguyên hàm của f trên K đều có dạng', 24, WHITE,
                max_w=11.6)
        m = self.M('thm', 1.5)
        l2 = tx('Ngược lại, với mỗi hằng số C, hàm F(x) + C cũng là một nguyên hàm của f trên K.', 22, SOFT,
                max_w=11.6)
        l1.move_to(box.get_center() + UP * .8)
        m.move_to(box.get_center() + UP * .02)
        l2.move_to(box.get_center() + DOWN * .82)
        self.play(FadeIn(box), FadeIn(head), run_time=self.rt(.05))
        self.wait_until(.12, t0)
        self.play(FadeIn(l1, shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(.36, t0)
        self.play(Write(m), run_time=self.rt(.12))
        self.play(Indicate(m[4:6], color=GOLD), run_time=self.rt(.08))
        self.wait_until(.7, t0)
        self.play(FadeIn(l2, shift=UP * .1), run_time=self.rt(.08))

    def beat_c11(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.core_axes()
        self.ax = a
        f1 = clipped(a, lambda v: v * v - 1, -2.5, 2.5, PURPLE, 4.5)
        f2 = clipped(a, lambda v: v * v + 2, -2.5, 2.5, GREEN, 4.5)
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(.05))
        self.play(Create(f1), Create(f2), run_time=self.rt(.1))
        self.write_board(self.heading('HAI NGUYÊN HÀM CỦA 2x'),
                         self.M('F1', 1.25), self.M('F2', 1.25), frac=.1)
        xt = ValueTracker(-2)
        gap = always_redraw(lambda: VGroup(
            Line(a.c2p(xt.get_value(), xt.get_value() ** 2 - 1), a.c2p(xt.get_value(), xt.get_value() ** 2 + 2),
                 color=GOLD, stroke_width=5),
            Dot(a.c2p(xt.get_value(), xt.get_value() ** 2 - 1), radius=.07, color=GOLD),
            Dot(a.c2p(xt.get_value(), xt.get_value() ** 2 + 2), radius=.07, color=GOLD)))
        meter = always_redraw(lambda: VGroup(
            tx(f'x = {vn(xt.get_value())}', 24, WHITE),
            tx(f'khoảng cách thẳng đứng = {vn((xt.get_value() ** 2 + 2) - (xt.get_value() ** 2 - 1))}', 24, GOLD,
               bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.18).move_to([BOARD_X, -1.75, 0], aligned_edge=LEFT))
        self.wait_until(.42, t0)
        self.play(FadeIn(gap), FadeIn(meter), run_time=self.rt(.04))
        self.play(xt.animate.set_value(1.9), run_time=self.rt(.3), rate_func=linear)
        self.write_board(self.M('gap', 1.1), frac=.08, gap=.4)
        gap.clear_updaters()
        meter.clear_updaters()

    def beat_c12(self, T):
        t0 = self.now()
        self.clear_board(.04)
        self.write_board(self.heading('TỔNG QUÁT'), tx('G, F cùng là nguyên hàm của f trên K:', 24, WHITE),
                         self.M('proof1', 1.4), frac=.14)
        self.wait_until(.42, t0)
        self.write_board(tx('Đạo hàm bằng 0 trên một khoảng  ⇒  hàm hằng', 23, SOFT), self.M('proof2', 1.4),
                         frac=.14)
        self.wait_until(.78, t0)
        last = self.M('proof3', 1.5)
        self.write_board(last, frac=.08)
        self.play(Create(SurroundingRectangle(last, color=GOLD, buff=.15, corner_radius=.1)), run_time=self.rt(.06))

    def beat_c13(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = tx('KÍ HIỆU HỌ NGUYÊN HÀM', 28, GOLD, bold=True).move_to([0, 2.6, 0])
        m = self.M('notation', 2.0).move_to([0, 1.2, 0])
        self.play(FadeIn(head), Write(m), run_time=self.rt(.14))
        sign = tx('dấu nguyên hàm', 19, CYAN).next_to(m[0], LEFT, buff=.9).shift(UP * .2)
        notes = VGroup(VGroup(sign, Arrow(sign.get_right(), m[0].get_left() + UP * .2, color=CYAN, buff=.08,
                                          stroke_width=3, max_tip_length_to_length_ratio=.2)))
        base = m[1:].get_bottom()[1] - .08
        for grp, text, col, row in ((m[1:5], 'hàm số dưới dấu ∫', GREEN, 0), (m[5:7], 'biến lấy nguyên hàm', PURPLE, 1),
                                    (m[8:14], 'họ nguyên hàm', GOLD, 0)):
            br = Brace(grp, DOWN, buff=0, color=col)
            br.shift(UP * (br.get_top()[1] - base) * -1)
            lab = tx(text, 19, col).next_to(br, DOWN, buff=.08 + .42 * row)
            notes.add(VGroup(br, lab))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * .1) for n in notes], lag_ratio=.4), run_time=self.rt(.22))
        self.wait_until(.66, t0)
        ex_lbl = tx('Ví dụ', 22, SOFT).move_to([-3.3, -1.75, 0])
        ex = self.M('notation_ex', 1.7).move_to([.6, -1.75, 0])
        self.play(FadeIn(ex_lbl), Write(ex), run_time=self.rt(.14))
        self.play(Circumscribe(ex, color=GOLD), run_time=self.rt(.08))

    def beat_c14(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-3, 3, 1), (-4.5, 4.5, 1), 6.0, 5.5, center=[LEFT_CX, -.12, 0],
                 x_ticks=(-2, -1, 1, 2), y_ticks=(-4, -2, 2, 4))
        self.ax = a
        right = clipped(a, lambda v: 1 / v, .02, 3, CYAN, 4.5)
        left = clipped(a, lambda v: 1 / v, -3, -.02, CYAN, 4.5)
        asym = DashedLine(a.c2p(0, -4.5), a.c2p(0, 4.5), color=CORAL, stroke_width=2.5)
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(.05))
        self.write_board(badge('BẪY CHUYÊN SÂU', CORAL, 19), self.M('inv_x', 1.4), frac=.12)
        self.wait_until(.32, t0)
        no = tx('x = 0: không xác định', 18, CORAL).move_to(a.c2p(1.55, -2.6))
        self.play(Create(asym), FadeIn(no), run_time=self.rt(.07))
        self.wait_until(.55, t0)
        self.play(Create(left), Create(right), run_time=self.rt(.12))
        self.write_board(para('F(x) = 1/x là nguyên hàm của −1/x² trên (−∞; 0) và trên (0; +∞) — '
                              'hai khoảng tách rời.', 23, WHITE, width=36), frac=.1)
        self.branches = (left, right)

    def beat_c15(self, T):
        t0 = self.now()
        a = self.ax
        left, right = self.branches
        r2 = clipped(a, lambda v: 1 / v + 1, .02, 3, GREEN, 4.5)
        l2 = clipped(a, lambda v: 1 / v - 2, -3, -.02, PURPLE, 4.5)
        ghost = VGroup(left.copy().set_stroke(opacity=.25), right.copy().set_stroke(opacity=.25))
        self.add(ghost)
        c1 = tx('+1', 24, GREEN, bold=True).move_to(a.c2p(1.6, 2.6))
        c2 = tx('−2', 24, PURPLE, bold=True).move_to(a.c2p(-1.6, -3.4))
        self.play(Transform(right, r2), FadeIn(c1, shift=UP * .3), run_time=self.rt(.12))
        self.wait_until(.2, t0)
        self.play(Transform(left, l2), FadeIn(c2, shift=DOWN * .3), run_time=self.rt(.12))
        old = self.board_items[1:]
        self.play(*[FadeOut(m) for m in old], run_time=self.rt(.03))
        self.board_items = self.board_items[:1]
        self.write_board(self.M('piece', 1.25), frac=.1)
        self.wait_until(.6, t0)
        self.write_board(para("Vẫn có G'(x) = −1/x² với mọi x ≠ 0, nhưng G không có dạng 1/x + C "
                              'với một hằng số chung!', 23, CORAL, width=36), frac=.1)

    # ================================================================ PHẦN 2
    def cubic_axes(self):
        return axes((-1.8, 1.8, 1), (-3, 9, 1), 5.6, 5.55, center=[LEFT_CX, -.12, 0],
                    x_ticks=(-1, 1), y_ticks=(-2, 2, 4, 6, 8))

    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        a = self.cubic_axes()
        self.ax = a
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), tx('Tìm nguyên hàm F của hàm số', 24, WHITE),
                         self.M('ex1_task', 1.4), frac=.3)
        p = dot(a, 1, 5, GOLD, .1)
        pl = tx('(1; 5)', 20, GOLD, bold=True).next_to(p, RIGHT, buff=.12)
        self.play(GrowFromCenter(p), FadeIn(pl), run_time=self.rt(.1))
        self.pt = VGroup(p, pl)

    def beat_e2(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.M('ex1_task', 1.2), tx('Bước 1 · Tìm họ nguyên hàm', 24, CYAN, bold=True), frac=.06)
        self.wait_until(.18, t0)
        self.write_board(tx('(x³)′ = 3x²  nên', 24, SOFT), self.M('ex1_s1', 1.35), frac=.16)
        self.wait_until(.6, t0)
        fam = VGroup(*[clipped(a, lambda v, k=k: v ** 3 + k, -1.8, 1.8, PURPLE, 2.5).set_stroke(opacity=.55)
                       for k in (-2, -1, 0, 1, 2)])
        self.play(LaggedStart(*[Create(f) for f in fam], lag_ratio=.25), run_time=self.rt(.22))
        self.fam = fam

    def beat_e3(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.M('ex1_s1', 1.2), tx('Bước 2 · Dùng điều kiện F(1) = 5', 24, CYAN, bold=True),
                         frac=.06)
        self.wait_until(.22, t0)
        self.write_board(self.M('ex1_s2', 1.3), frac=.14)
        C = ValueTracker(0)
        live = always_redraw(lambda: clipped(a, lambda v: v ** 3 + C.get_value(), -1.8, 1.8, GOLD, 5))
        lab = always_redraw(lambda: tx(f'C = {vn(C.get_value())}', 22, GOLD, bold=True).move_to(a.c2p(-1.05, 7.6)))
        self.wait_until(.6, t0)
        self.play(self.fam.animate.set_stroke(opacity=.18), FadeIn(live), FadeIn(lab), run_time=self.rt(.04))
        self.play(C.animate.set_value(4), run_time=self.rt(.22), rate_func=smooth)
        self.play(Indicate(self.pt[0], color=GOLD, scale_factor=1.8), run_time=self.rt(.06))
        live.clear_updaters()
        lab.clear_updaters()

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_board(.04)
        ans = self.M('ex1_ans', 1.8)
        self.write_board(tx('KẾT LUẬN', 22, GREEN, bold=True), ans, frac=.12)
        box = SurroundingRectangle(ans, color=GREEN, buff=.18, corner_radius=.1)
        self.play(Create(box), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        chk = self.M('ex1_check', 1.0)
        self.write_board(tx('Kiểm tra:', 22, SOFT), chk, frac=.14, gap=.45)
        mark = check().next_to(chk, RIGHT, buff=.25)
        self.wait_until(.8, t0)
        self.play(Create(mark), run_time=self.rt(.06))

    # ---------------------------------------------------------------- example 2
    def motion_axes(self):
        return axes((0, 3.5, 1), (0, 16, 2), 5.0, 3.65, center=[LEFT_CX + .1, .95, 0],
                    x_ticks=(1, 2, 3), y_ticks=(4, 8, 12), x_label='t (s)', y_label='s (m)', label_size=15)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        road = self.road()
        vehicle = self.car_at(2)
        self.play(Create(road), FadeIn(vehicle, shift=RIGHT * .3), run_time=self.rt(.08))
        self.vehicle = vehicle
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), tx('Xe chuyển động thẳng với', 24, WHITE),
                         self.M('ex2_task', 1.35), tx('v tính bằng m/s, s tính bằng m.', 20, SOFT), frac=.24)
        a = self.motion_axes()
        self.ax = a
        vline = clipped(a, v_of, 0, 3.4, CYAN, 4)
        vlab = tx('v(t) = 2t + 1', 19, CYAN, bold=True).move_to(a.c2p(2.6, 9.3))
        self.play(FadeIn(a), FadeIn(a.labels), Create(vline), FadeIn(vlab), run_time=self.rt(.12))
        self.vplot = VGroup(vline, vlab)
        self.wait_until(.72, t0)
        q = tx('Tìm vị trí của xe sau 3 giây:  s(3) = ?', 24, GOLD, bold=True)
        self.write_board(q, frac=.08)

    def beat_e6(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(self.M('ex2_task', 1.2), tx('s′(t) = v(t)  ⇒  s là một nguyên hàm của v', 23, WHITE),
                         frac=.1)
        self.wait_until(.38, t0)
        self.write_board(self.M('ex2_s1', 1.2), frac=.14)
        fam = VGroup(*[clipped(a, lambda u, k=k: u * u + u + k, 0, 3.4, GREEN, 2.2).set_stroke(opacity=.4)
                       for k in (0, 1, 2, 3, 4)])
        self.play(self.vplot.animate.set_opacity(.25), LaggedStart(*[Create(f) for f in fam], lag_ratio=.2),
                  run_time=self.rt(.2))
        self.sfam = fam

    def beat_e7(self, T):
        t0 = self.now()
        a = self.ax
        self.write_board(self.M('ex2_s2', 1.25), frac=.1)
        p0 = dot(a, 0, 2, GOLD, .09)
        self.play(GrowFromCenter(p0), run_time=self.rt(.04))
        self.wait_until(.25, t0)
        s_curve = clipped(a, s_of, 0, 3.4, GREEN, 5)
        slab = tx('s(t) = t² + t + 2', 19, GREEN, bold=True).move_to(a.c2p(1.25, 13.2))
        self.play(self.sfam.animate.set_stroke(opacity=.12), Create(s_curve), FadeIn(slab), run_time=self.rt(.12))
        self.write_board(self.M('ex2_s3', 1.35), frac=.08)
        self.wait_until(.62, t0)
        arrow = CurvedArrow(p0.get_center() + DOWN * .15, self.vehicle.get_top() + UP * .1, color=GOLD,
                            angle=.6)
        note = tx('C = vị trí ban đầu', 20, GOLD, bold=True).next_to(self.vehicle, RIGHT, buff=.45)
        self.play(Create(arrow), FadeIn(note), run_time=self.rt(.1))
        self.s_curve, self.p0 = s_curve, p0
        self.e7_tmp = VGroup(arrow, note)

    def beat_e8(self, T):
        t0 = self.now()
        a = self.ax
        self.play(FadeOut(self.e7_tmp), run_time=self.rt(.03))
        self.clear_board(.03)
        self.write_board(self.M('ex2_s3', 1.35), self.M('ex2_s4', 1.35), frac=.12)
        tau = ValueTracker(0)
        pt = always_redraw(lambda: Dot(a.c2p(tau.get_value(), s_of(tau.get_value())), radius=.09, color=GOLD))
        self.vehicle.add_updater(lambda m: m.move_to([road_x(s_of(tau.get_value())), ROAD_Y + .33, 0]))
        info = always_redraw(lambda: VGroup(
            tx(f't = {vn(tau.get_value(), 1)} s', 24, WHITE),
            tx(f'v = {vn(v_of(tau.get_value()), 1)} m/s', 24, CYAN),
            tx(f's = {vn(s_of(tau.get_value()), 1)} m', 24, GREEN, bold=True),
        ).arrange(RIGHT, buff=.5).move_to([BOARD_X, -.35, 0], aligned_edge=LEFT))
        self.wait_until(.36, t0)
        self.play(FadeIn(pt), FadeIn(info), run_time=self.rt(.04))
        self.play(tau.animate.set_value(3), run_time=self.rt(.4), rate_func=linear)
        self.vehicle.clear_updaters()
        for m in (pt, info):
            m.clear_updaters()
        flag = VGroup(Line([road_x(14), ROAD_Y, 0], [road_x(14), ROAD_Y + 1.3, 0], color=GOLD, stroke_width=3),
                      tx('14 m', 22, GOLD, bold=True).move_to([road_x(14), ROAD_Y + 1.55, 0]))
        self.play(FadeIn(flag), Indicate(pt, color=GOLD), run_time=self.rt(.08))
        self.flag14 = flag
        self.e8_info = info

    def beat_e9(self, T):
        t0 = self.now()
        start = Line([road_x(2), ROAD_Y, 0], [road_x(2), ROAD_Y + 1.25, 0], color=CYAN, stroke_width=3)
        span = Arrow([road_x(2), ROAD_Y + .95, 0], [road_x(14), ROAD_Y + .95, 0], color=GOLD, buff=0,
                     stroke_width=5, max_tip_length_to_length_ratio=.04)
        lbl = tx('đi thêm 12 m', 22, GOLD, bold=True).next_to(span, DOWN, buff=.08).shift(RIGHT * 1.6)
        self.play(FadeOut(self.e8_info), Create(start), GrowArrow(span), FadeIn(lbl), run_time=self.rt(.14))
        self.write_board(self.M('ex2_disp', 1.3), frac=.12, gap=.36)
        self.wait_until(.55, t0)
        teaser = badge('Hẹn gặp lại ở INT12: TÍCH PHÂN', PURPLE, 18)
        self.write_board(teaser, frac=.08)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('ĐÚNG / SAI', CORAL, 20), tx('dạng câu hỏi Phần II – đề thi tốt nghiệp THPT', 19, SOFT)) \
            .arrange(RIGHT, buff=.3).move_to([0, 2.72, 0]).to_edge(LEFT, buff=.6)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi F là nguyên hàm của f trên ℝ thỏa mãn F(0) = 1. Xét các mệnh đề:', 24, WHITE)
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=.22).next_to(head, DOWN, buff=.35).align_to(head, LEFT)
        rows = VGroup()
        items = (('a)', self.M('tf_a', 1.2)), ('b)', self.M('tf_b', 1.2)), ('c)', self.M('tf_c', 1.2)),
                 ('d)', VGroup(self.M('tf_d', 1.2), tx('là một nguyên hàm của f trên ℝ', 22, WHITE))
                  .arrange(RIGHT, buff=.2)))
        for i, (k, body) in enumerate(items):
            r = VGroup(tx(k, 24, GOLD, bold=True), body).arrange(RIGHT, buff=.3)
            r.move_to([0, .55 - .7 * i, 0]).align_to(head, LEFT).shift(RIGHT * .3)
            slot = RoundedRectangle(width=1.25, height=.5, corner_radius=.08, stroke_color=STROKE,
                                    stroke_width=2, fill_color=PANEL_2, fill_opacity=1).move_to([5.6, r.get_y(), 0])
            rows.add(VGroup(r, slot))
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.play(FadeIn(l1, shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        self.play(FadeIn(l2, shift=UP * .1), run_time=self.rt(.07))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * .2) for r in rows], lag_ratio=.3), run_time=self.rt(.2))
        self.wait_until(.78, t0)
        pause = VGroup(VGroup(RoundedRectangle(width=.12, height=.42, corner_radius=.03, fill_color=GOLD,
                                               fill_opacity=1, stroke_width=0),
                              RoundedRectangle(width=.12, height=.42, corner_radius=.03, fill_color=GOLD,
                                               fill_opacity=1, stroke_width=0)).arrange(RIGHT, buff=.1),
                       tx('Tạm dừng video và tự làm!', 22, GOLD, bold=True)).arrange(RIGHT, buff=.2)
        pause.move_to([0, -2.6, 0])
        self.play(FadeIn(pause, scale=1.1), run_time=self.rt(.06))
        self.tf_rows, self.tf_pause = rows, pause

    def mark_row(self, i, ok):
        slot = self.tf_rows[i][1]
        b = badge('ĐÚNG' if ok else 'SAI', GREEN if ok else CORAL, 18).move_to(slot)
        return FadeIn(b, scale=1.3)

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.mark_row(0, True), run_time=self.rt(.07))
        self.wait_until(.22, t0)
        self.play(self.mark_row(1, False), run_time=self.rt(.07))
        why = VGroup(tx('F(0) = 0 ≠ 1', 22, CORAL, bold=True)).next_to(self.tf_rows[1][0], RIGHT, buff=.6)
        self.play(FadeIn(why), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        sol = VGroup(tx('Đúng phải là:', 22, SOFT), self.M('tf_sol', 1.25)).arrange(RIGHT, buff=.25)
        sol.move_to([0, -2.45, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))

    def beat_x3(self, T):
        t0 = self.now()
        c_calc = self.M('tf_c_calc', 1.05).next_to(self.tf_rows[2][0], RIGHT, buff=.8)
        self.play(Write(c_calc), run_time=self.rt(.1))
        self.play(self.mark_row(2, True), run_time=self.rt(.06))
        self.wait_until(.42, t0)
        d_calc = self.M('tf_d_calc', 1.05).move_to([3.2, -2.45, 0])
        self.play(Write(d_calc), run_time=self.rt(.1))
        self.play(self.mark_row(3, True), run_time=self.rt(.06))
        key = tx('Đáp án:  a) Đ   b) S   c) Đ   d) Đ', 22, GOLD, bold=True).move_to([0, -3.0, 0])
        self.wait_until(.85, t0)
        self.play(FadeIn(key, shift=UP * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-1.2, 3.6, 1), (-4, 8, 1), 5.8, 5.5, center=[LEFT_CX, -.12, 0],
                 x_ticks=(1, 2, 3), y_ticks=(-2, 2, 4, 6))
        self.ax = a
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(.04))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.2), frac=.12)
        A = dot(a, 2, 1, GOLD, .09)
        Al = tx('A(2; 1)', 19, GOLD, bold=True).next_to(A, RIGHT, buff=.12)
        self.play(GrowFromCenter(A), FadeIn(Al), run_time=self.rt(.04))
        C = ValueTracker(0)
        live = always_redraw(lambda: clipped(a, lambda v: v * v + C.get_value(), -1.2, 3.6, GOLD, 4.5))
        self.wait_until(.3, t0)
        self.play(FadeIn(live), run_time=self.rt(.03))
        self.write_board(self.M('sa_s1', 1.1), frac=.1)
        self.play(C.animate.set_value(-3), run_time=self.rt(.14))
        live.clear_updaters()
        self.wait_until(.72, t0)
        P = dot(a, 3, 6, GREEN, .09)
        guide = VGroup(DashedLine(a.c2p(3, 0), a.c2p(3, 6), color=GREEN, stroke_width=2),
                       DashedLine(a.c2p(0, 6), a.c2p(3, 6), color=GREEN, stroke_width=2))
        self.play(Create(guide), GrowFromCenter(P), run_time=self.rt(.06))
        self.write_board(self.M('sa_s2', 1.35), frac=.06)
        cells = VGroup(*[RoundedRectangle(width=.55, height=.68, corner_radius=.06, stroke_color=SOFT,
                                          stroke_width=2) for _ in range(4)]).arrange(RIGHT, buff=.08)
        digit = tx('6', 30, GREEN, bold=True).move_to(cells[0])
        sheet = VGroup(tx('Phiếu trả lời:', 20, SOFT), VGroup(cells, digit)).arrange(RIGHT, buff=.25)
        self.write_board(sheet, frac=.05)

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
        keys[0].set_fill(CYAN, .7)
        expr = self.M('casio1', .95).set_color('#14202B').move_to(screen.get_center() + UP * .32)
        expr[-2:].set_opacity(0)
        res = tx('12', 34, '#14202B', bold=True).move_to(screen.get_corner(DOWN + RIGHT) + UL * .38)
        self.play(FadeIn(body), FadeIn(screen), FadeIn(keys), run_time=self.rt(.06))
        self.write_board(badge('MẸO THỰC CHIẾN', GOLD, 19),
                         para('Muốn kiểm tra nguyên hàm: lấy đạo hàm ngược lại.', 24, WHITE, width=32), frac=.1)
        self.wait_until(.25, t0)
        self.play(Indicate(keys[0], color=CYAN), FadeIn(expr), run_time=self.rt(.08))
        self.write_board(tx('1)  Tính đạo hàm của F tại một điểm:', 22, SOFT), self.M('casio1', 1.2), frac=.1)
        self.play(FadeIn(res, scale=1.4), run_time=self.rt(.04))
        self.wait_until(.7, t0)
        self.write_board(tx('2)  So sánh với giá trị của f:', 22, SOFT), self.M('casio2', 1.2), frac=.1)
        ok = VGroup(check(), tx('Bằng nhau  →  kết quả đáng tin cậy', 22, GREEN, bold=True)).arrange(RIGHT, buff=.2)
        self.write_board(ok, frac=.05)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('3 Ý CẦN NHỚ', 28, GOLD, bold=True).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        data = (('1', 'Đi ngược đạo hàm', 'sum1', CYAN, 'F là nguyên hàm của f khi'),
                ('2', 'Sai khác hằng số C', 'sum2', GREEN, 'Trên một khoảng: các đồ thị tịnh tiến dọc'),
                ('3', 'Điều kiện xác định C', 'sum3', GOLD, 'Một điểm thuộc đồ thị cho đúng một C'))
        for i, (n, title, key, col, note) in enumerate(data):
            c = card(4.05, 4.4, col).move_to([-4.3 + 4.3 * i, -.35, 0])
            num = tx(n, 46, col, bold=True).move_to(c.get_top() + DOWN * .6)
            t = tx(title, 24, WHITE, bold=True, max_w=3.7).next_to(num, DOWN, buff=.25)
            nt = para(note, 18, SOFT, width=24, center=True).next_to(t, DOWN, buff=.3)
            m = self.M(key, 1.05, max_w=3.6).move_to(c.get_bottom() + UP * .8)
            self.wait_until((.04, .3, .72)[i], t0)
            self.play(FadeIn(VGroup(c, num, t, nt), shift=UP * .2), Write(m), run_time=self.rt(.08))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = VGroup(badge('BÀI TẬP TỰ LUYỆN', CYAN, 20)).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        rows = VGroup()
        for i, (key, intro) in enumerate((('hw1', 'Tìm'), ('hw2', 'Tìm F biết'), ('hw3', 'Vật chuyển động:'))):
            r = VGroup(tx(f'{i + 1}.', 26, CYAN, bold=True), tx(intro, 24, WHITE), self.M(key, 1.2)) \
                .arrange(RIGHT, buff=.25)
            if r.width > 8.6:
                r.scale_to_fit_width(8.6)
            r.move_to([0, 1.45 - 1.15 * i, 0]).to_edge(LEFT, buff=.8)
            rows.add(r)
        for frac, r in zip((.05, .2, .45), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        answers = VGroup(*[self.M(k, 1.15).set_color(GREEN) for k in ('hw_ans1', 'hw_ans2', 'hw_ans3')])
        for ans, r in zip(answers, rows):
            ans.move_to([5.35, r.get_y(), 0])
        lbl = tx('Đáp số', 20, GREEN, bold=True).move_to([5.35, 2.2, 0])
        rule = Line([4.0, 2.0, 0], [4.0, -1.3, 0], color=STROKE, stroke_width=2)
        self.play(FadeIn(lbl), FadeIn(rule), LaggedStart(*[FadeIn(a) for a in answers], lag_ratio=.3),
                  run_time=self.rt(.1))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        box = card(10.8, 4.7, PURPLE, PANEL, radius=.3, stroke_width=2.4).move_to([0, .6, 0])
        tag = badge('TẬP SAU · INT02', PURPLE, 20).move_to(box.get_top() + DOWN * .55)
        title = tx('Tính chất nguyên hàm & hàm lũy thừa', 38, WHITE, bold=True).move_to(box.get_center() + UP * .75)
        bullets = VGroup(self.M('next1', 1.0),
                         VGroup(badge('BẪY', CORAL, 16), self.M('next2', 1.0)).arrange(RIGHT, buff=.3)) \
            .arrange(DOWN, buff=.3).next_to(title, DOWN, buff=.4)
        thanks = tx('Cảm ơn các em đã theo dõi!', 28, GOLD, bold=True).move_to([0, -2.5, 0])
        self.play(FadeIn(box), FadeIn(tag, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(Write(title), run_time=self.rt(.14))
        self.play(FadeIn(bullets, shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(.58, t0)
        self.play(FadeIn(thanks, shift=UP * .15), run_time=self.rt(.08))
        self.wait_until(.88, t0)
        self.play(*[FadeOut(m) for m in self.stage()], run_time=self.rt(.08))


class INT01_SMOKE(INT01):
    """Every beat at ~1 s and low resolution: catches errors in all code paths."""
    smoke = True
