"""INT25 – Thể tích vật thể theo thiết diện S(x).

    python scripts/build_typst.py --ep int25
    python scripts/prepare_voice.py --ep int25 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int25/scene.py INT25
    python scripts/finalize.py --ep int25

One method per narration beat (int25/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().

Solids are drawn in a cabinet (oblique) projection with plain 2D polygons:
x to the right, y up, depth z receding at 35°.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, LaggedStart, Line, Polygon,
                   ValueTracker, VGroup, Write, always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, card, check, cross, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

ANG = math.radians(35)


class Space:
    """Cabinet projection: (x, y, z) → scene point."""

    def __init__(self, origin=(-6.0, -2.2), kx=1.2, ky=1.2, kz=.6):
        self.o, self.kx, self.ky, self.kz = origin, kx, ky, kz

    def p(self, xv, yv, zv):
        return [self.o[0] + self.kx * xv + self.kz * zv * math.cos(ANG),
                self.o[1] + self.ky * yv + self.kz * zv * math.sin(ANG), 0]

    def axes(self, xmax, ymax, zmax):
        g = VGroup()
        for end, name in (((xmax, 0, 0), 'x'), ((0, ymax, 0), 'y'), ((0, 0, zmax), 'z')):
            g.add(Arrow(self.p(0, 0, 0), self.p(*end), buff=0, color=SOFT, stroke_width=2.5,
                        max_tip_length_to_length_ratio=.06),
                  tx(name, 20, SOFT, slant=True).move_to(self.p(*end)).shift(RIGHT * .2 + UP * .1))
        return g

    def square(self, xv, s, color=CYAN, opacity=.55):
        return Polygon(self.p(xv, 0, 0), self.p(xv, s, 0), self.p(xv, s, s), self.p(xv, 0, s),
                       fill_color=color, fill_opacity=opacity, stroke_color=WHITE, stroke_width=1.2)

    def triangle(self, xv, s, color=GREEN, opacity=.55):
        return Polygon(self.p(xv, 0, 0), self.p(xv, 0, s), self.p(xv, s * math.sqrt(3) / 2, s / 2),
                       fill_color=color, fill_opacity=opacity, stroke_color=WHITE, stroke_width=1.2)

    def rect(self, xv, w, hgt, color=PURPLE, opacity=.55):
        return Polygon(self.p(xv, 0, 0), self.p(xv, hgt, 0), self.p(xv, hgt, w), self.p(xv, 0, w),
                       fill_color=color, fill_opacity=opacity, stroke_color=WHITE, stroke_width=1.2)

    def centred_square(self, xv, s, color=GOLD, opacity=.5):
        """Square slice centred on the x axis (for the pyramid)."""
        return Polygon(self.p(xv, -s / 2, -s / 2), self.p(xv, s / 2, -s / 2), self.p(xv, s / 2, s / 2),
                       self.p(xv, -s / 2, s / 2), fill_color=color, fill_opacity=opacity, stroke_color=WHITE,
                       stroke_width=1.2)


def stack(space, maker, x0, x1, n, side):
    xs = [x0 + (x1 - x0) * (k + .5) / n for k in range(n)]
    return VGroup(*[maker(xv, side(xv)) for xv in xs])


class INT25(LessonScene):
    EP = 'int25'

    def sweep(self, space, maker, side, x0, x1, frac, label, area_fn, at=(BOARD_X, -2.0)):
        """A highlighted slice moving along x with a live S(x) readout."""
        xt = ValueTracker(x0 + .02)
        live = always_redraw(lambda: maker(xt.get_value(), side(xt.get_value())).set_fill(GOLD, .85))
        rd = always_redraw(lambda: tx(f'x = {vn(xt.get_value(), 2)}   {label} = {vn(area_fn(xt.get_value()), 2)}', 23,
                                      GOLD, bold=True).move_to([at[0], at[1], 0], aligned_edge=LEFT))
        self.add(live, rd)
        self.play(xt.animate.set_value(x1 - .02), run_time=self.rt(frac), rate_func=linear)
        live.clear_updaters()
        rd.clear_updaters()
        self.play(FadeOut(rd), run_time=self.rt(.03))
        return live

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        sp_ = Space(origin=(-6.3, -2.0), kx=.72, ky=1.0, kz=.8)
        loaf = lambda v: 1.4 + .5 * math.sin(math.pi * v / 8) + .25 * math.sin(1.7 * v)  # noqa: E731
        slices = VGroup(*[sp_.rect(v, 2.2, loaf(v), GOLD, .6) for v in [.25 + .5 * k for k in range(16)]])
        self.play(LaggedStart(*[FadeIn(s) for s in slices], lag_ratio=.15), run_time=self.rt(.3))
        self.wait_until(.35, t0)
        self.play(*[s.animate.shift(RIGHT * .05 * k) for k, s in enumerate(slices)], run_time=self.rt(.1))
        self.play(FadeIn(self.M('slice', 1.5).move_to([3.6, 1.6, 0])), run_time=self.rt(.08))
        self.wait_until(.75, t0)
        self.play(Write(self.M('vol', 1.7).move_to([3.6, -.2, 0])), run_time=self.rt(.1))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('V = ∫S(x)dx', 'Cắt lát và cộng dồn'),
                         ('Tìm S(x)', 'Diện tích thiết diện'),
                         ('Hình chóp', 'Chứng minh V = Sh/3')], t0, fracs=(.1, .4, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        sp_ = Space(origin=(-6.2, -2.0), kx=1.15, ky=1.1, kz=.8)
        self.play(FadeIn(sp_.axes(4.8, 3.0, 2.6)), run_time=self.rt(.05))
        side = lambda v: 1.0 + .25 * v  # noqa: E731
        body = stack(sp_, sp_.square, .5, 4.2, 26, side).set_fill(CYAN, .25).set_stroke(width=.5)
        self.play(FadeIn(body), run_time=self.rt(.08))
        self.write_board(self.heading('THIẾT DIỆN TẠI x'), tx('mặt phẳng vuông góc Ox cắt vật thể', 22, SOFT),
                         frac=.1)
        self.wait_until(.3, t0)
        self.sweep(sp_, sp_.square, side, .5, 4.2, .35, 'S(x)', lambda v: side(v) ** 2, at=(BOARD_X, .4))
        self.wait_until(.75, t0)
        m = self.M('vol', 1.5)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        sp_ = Space(origin=(-6.2, -2.0), kx=1.15, ky=1.1, kz=.8)
        self.play(FadeIn(sp_.axes(4.8, 3.0, 2.6)), run_time=self.rt(.04))
        side = lambda v: 1.0 + .25 * v  # noqa: E731
        layers = None
        for n, frac in ((4, .05), (8, .25), (16, .45)):
            self.wait_until(frac, t0)
            w = 3.7 / n
            blocks = VGroup()
            for k in range(n):
                xv = .5 + w * k
                s = side(xv + w / 2)
                blocks.add(VGroup(sp_.square(xv, s, PURPLE, .35), sp_.square(xv + w, s, PURPLE, .55),
                                  Line(sp_.p(xv, s, 0), sp_.p(xv + w, s, 0), color=WHITE, stroke_width=1),
                                  Line(sp_.p(xv, s, s), sp_.p(xv + w, s, s), color=WHITE, stroke_width=1)))
            if layers is None:
                self.play(FadeIn(blocks), run_time=self.rt(.06))
            else:
                self.play(FadeOut(layers), FadeIn(blocks), run_time=self.rt(.06))
            layers = blocks
        self.write_board(self.heading('CỘNG DỒN CÁC LÁT MỎNG'), self.M('slice', 1.3), frac=.1)
        self.wait_until(.65, t0)
        self.write_board(self.M('riemann', .95), frac=.12)

    def beat_c2b(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'KIỂM TRA BẰNG ĐƠN VỊ', ('units',), (.1,), (1.6,), box_last=False)
        r1 = VGroup(check(GREEN, .28), tx('dưới dấu tích phân phải là DIỆN TÍCH thiết diện', 25, GREEN)).arrange(RIGHT, buff=.25)
        r2 = VGroup(cross(CORAL, .26), tx('tích phân của độ dài cạnh → chỉ ra một diện tích', 25, CORAL)).arrange(RIGHT, buff=.25)
        VGroup(r1, r2).arrange(DOWN, buff=.45, aligned_edge=LEFT).next_to(lines[-1], DOWN, buff=.8)
        self.wait_until(.35, t0)
        self.play(FadeIn(r1), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.play(FadeIn(r2), run_time=self.rt(.05))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 3 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Chọn trục', 'vật thể nằm từ a đến b', CYAN), ('Tìm S(x)', 'mô tả thiết diện tại x', GOLD),
                 ('Tích phân', 'V = tích phân của S(x)', GREEN))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.05, .3, .55))):
            c = card(4.05, 3.0, col).move_to([-4.3 + 4.3 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 26, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 18, SOFT, max_w=3.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('Bước 2 quan trọng nhất!', 26, GOLD, bold=True).move_to([0, -2.4, 0])), run_time=self.rt(.04))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('DIỆN TÍCH THIẾT DIỆN HAY GẶP', 26, GOLD, bold=True).move_to([0, 2.55, 0])),
                  run_time=self.rt(.04))
        from manim import Polygon as Pg, Sector, Square
        shapes = (Square(1.3, color=CYAN, fill_opacity=.4),
                  Pg([-.75, -.6, 0], [.75, -.6, 0], [0, .7, 0], color=GREEN, fill_opacity=.4),
                  Sector(radius=.9, angle=math.pi, color=GOLD, fill_opacity=.4).shift(DOWN * .3),
                  Pg([-.9, -.5, 0], [.9, -.5, 0], [.9, .5, 0], [-.9, .5, 0], color=PURPLE, fill_opacity=.4))
        names = ('hình vuông', 'tam giác đều', 'nửa hình tròn', 'hình chữ nhật')
        keys = ('sq', 'tri', 'semi', 'rect')
        for i, (shp, nm, k) in enumerate(zip(shapes, names, keys)):
            cx = -4.65 + 3.1 * i
            g = VGroup(shp.move_to([cx, .8, 0]), tx(nm, 21, WHITE).move_to([cx, -.4, 0]),
                       self.M(k, 1.25).move_to([cx, -1.5, 0]))
            self.wait_until((.05, .25, .5, .72)[i], t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.06))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        from manim import Ellipse
        coins = [VGroup(*[Ellipse(width=1.6, height=.4, color=GOLD, fill_color=GOLD, fill_opacity=.5)
                          .move_to([cx + (0 if i == 0 else .35 * math.sin(k / 2.2)), -2.0 + .22 * k, 0])
                          for k in range(16)]) for i, cx in enumerate((-4.5, -1.8))]
        self.play(FadeIn(coins[0]), run_time=self.rt(.08))
        self.wait_until(.25, t0)
        self.play(FadeIn(coins[1]), run_time=self.rt(.08))
        self.write_board(self.heading('NGUYÊN LÝ CAVALIERI'),
                         tx('thiết diện bằng nhau tại mọi x', 23, WHITE), tx('→ thể tích bằng nhau', 23, GREEN, bold=True),
                         frac=.12)
        self.wait_until(.7, t0)
        self.write_board(tx('đó chính là nội dung của V = ∫S(x)dx', 22, SOFT), frac=.05)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_ = Space(origin=(-6.2, -2.0), kx=1.05, ky=1.1, kz=.8)
        self.play(FadeIn(sp_.axes(4.8, 2.6, 2.6)), run_time=self.rt(.04))
        side = math.sqrt
        body = stack(sp_, sp_.square, 0, 4, 30, side).set_fill(CYAN, .22).set_stroke(width=.5)
        self.play(FadeIn(body), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), tx('x ∈ [0; 4], thiết diện: hình vuông cạnh √x', 22, WHITE),
                         frac=.08)
        self.wait_until(.2, t0)
        self.sweep(sp_, sp_.square, side, 0, 4, .3, 'S(x)', lambda v: v, at=(BOARD_X, .6))
        self.wait_until(.6, t0)
        m = self.M('e1_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_ = Space(origin=(-6.2, -2.0), kx=1.35, ky=1.15, kz=.8)
        self.play(FadeIn(sp_.axes(3.6, 3.0, 3.4)), run_time=self.rt(.04))
        side = lambda v: v  # noqa: E731
        body = stack(sp_, sp_.triangle, 0, 3, 26, side).set_fill(GREEN, .22).set_stroke(width=.5)
        self.play(FadeIn(body), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), tx('x ∈ [0; 3], thiết diện: tam giác đều cạnh x', 22, WHITE),
                         frac=.08)
        self.wait_until(.2, t0)
        self.sweep(sp_, sp_.triangle, side, 0, 3, .3, 'S(x)', lambda v: math.sqrt(3) / 4 * v * v, at=(BOARD_X, .6))
        self.wait_until(.6, t0)
        m = self.M('e2_s1', .95)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2b(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_ = Space(origin=(-6.2, -1.6), kx=1.05, ky=1.15, kz=.8)
        self.play(FadeIn(sp_.axes(4.8, 2.0, 2.6)), run_time=self.rt(.04))
        base = Polygon(*[sp_.p(v, 0, math.sqrt(v)) for v in [4 * k / 40 for k in range(41)]], sp_.p(4, 0, 0), sp_.p(0, 0, 0),
                       fill_color=CYAN, fill_opacity=.35, stroke_color=CYAN, stroke_width=2)
        self.play(FadeIn(base), run_time=self.rt(.06))
        self.write_board(badge('ĐÁY LÀ MIỀN PHẲNG', GOLD, 20), tx('đáy: y = √x, trục hoành, x ∈ [0; 4]', 22, WHITE),
                         tx('thiết diện: nửa hình tròn, đường kính √x', 22, WHITE), frac=.12)

        def semi(xv, d):
            r = d / 2
            pts = [sp_.p(xv, r * math.sin(math.pi * k / 24), r - r * math.cos(math.pi * k / 24)) for k in range(25)]
            return Polygon(*pts, fill_color=GOLD, fill_opacity=.5, stroke_color=WHITE, stroke_width=1)
        self.wait_until(.3, t0)
        body = VGroup(*[semi(v, math.sqrt(v)) for v in [4 * (k + .5) / 18 for k in range(18)]])
        self.play(LaggedStart(*[FadeIn(sl) for sl in body], lag_ratio=.1), run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.write_board(self.M('base_s', 1.05), frac=.1)
        m = self.M('base_v', 1.2)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def pyramid_space(self):
        sp_ = Space(origin=(-6.0, -.3), kx=1.3, ky=1.0, kz=.8)
        apex, hgt, a = sp_.p(0, 0, 0), 4.0, 2.6
        base = [sp_.p(hgt, yy, zz) for yy, zz in ((-a / 2, -a / 2), (a / 2, -a / 2), (a / 2, a / 2), (-a / 2, a / 2))]
        edges = VGroup(*[Line(apex, b, color=SOFT, stroke_width=2) for b in base],
                       Polygon(*base, color=SOFT, stroke_width=2, fill_opacity=.1))
        axis = Arrow(apex, sp_.p(hgt + .9, 0, 0), buff=0, color=SOFT, stroke_width=2.5, max_tip_length_to_length_ratio=.05)
        return sp_, hgt, a, VGroup(edges, axis, tx('x', 20, SOFT, slant=True).move_to(sp_.p(hgt + 1.0, .3, 0)))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_, hgt, a, frame = self.pyramid_space()
        self.play(Create(frame), run_time=self.rt(.1))
        self.write_board(badge('VÍ DỤ 3: HÌNH CHÓP', GOLD, 20), tx('đáy hình vuông cạnh a, chiều cao h', 22, WHITE),
                         tx('trục Ox từ đỉnh xuống đáy', 22, SOFT), frac=.12)
        self.wait_until(.4, t0)
        self.sweep(sp_, sp_.centred_square, lambda v: a * v / hgt, 0, hgt, .3, 'cạnh', lambda v: a * v / hgt,
                   at=(BOARD_X, -.4))
        self.write_board(self.M('e3_s1', 1.3), tx('(tam giác đồng dạng)', 21, SOFT), frac=.1)

    def beat_e4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'VÍ DỤ 3 (TIẾP)', ('e4_s1', 'e4_s2'), (.05, .55), (1.25, 1.5), gap=.8)
        self.wait_until(.85, t0)
        self.play(FadeIn(tx('công thức lớp 9 – nay chứng minh bằng tích phân', 24, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.7)), run_time=self.rt(.05))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_ = Space(origin=(-6.2, -2.1), kx=1.4, ky=1.15, kz=.75)
        self.play(FadeIn(sp_.axes(3.6, 3.4, 3.6)), run_time=self.rt(.04))
        w = lambda v: math.sqrt(max(0, 9 - v * v))  # noqa: E731
        slices = VGroup(*[sp_.rect(v, v, w(v), PURPLE, .3).set_stroke(width=.5)
                          for v in [3 * (k + .5) / 24 for k in range(24)]])
        self.play(FadeIn(slices), run_time=self.rt(.1))
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), tx('thiết diện: hình chữ nhật cạnh x và √(9 − x²)', 22, WHITE),
                         frac=.1)
        self.wait_until(.5, t0)
        m = self.M('e5_s1', .95)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        from manim import Ellipse
        sp_ = Space(origin=(-6.2, -.4), kx=1.2, ky=1.0, kz=.0)
        f = lambda v: .6 + .35 * v  # noqa: E731
        discs = VGroup(*[Ellipse(width=.35 * f(v) * 1.0, height=2 * f(v), color=CYAN, fill_color=CYAN, fill_opacity=.35,
                                 stroke_width=1.5).move_to(sp_.p(v, 0, 0)) for v in [.3 + .35 * k for k in range(12)]])
        axis = Arrow(sp_.p(0, 0, 0), sp_.p(4.8, 0, 0), buff=0, color=SOFT, stroke_width=2.5, max_tip_length_to_length_ratio=.05)
        self.play(Create(axis), LaggedStart(*[FadeIn(d) for d in discs], lag_ratio=.12), run_time=self.rt(.25))
        self.write_board(self.heading('THIẾT DIỆN LÀ HÌNH TRÒN'), frac=.04)
        self.wait_until(.35, t0)
        m = self.M('disk', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.write_board(tx('→ khối tròn xoay (tập 26)', 23, GOLD, bold=True), frac=.05)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Vật thể với', 24, WHITE), self.M('tf_given', 1.3),
                    tx('(thiết diện: hình vuông)', 22, SOFT)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi V là thể tích. Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.35, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c, d)', 22, SOFT), self.M('tf_c_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.75, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, True), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐSĐĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        sp_ = Space(origin=(-6.2, -2.0), kx=1.45, ky=1.2, kz=.8)
        self.play(FadeIn(sp_.axes(3.6, 2.4, 2.8)), run_time=self.rt(.04))
        side = lambda v: 2 * math.sqrt(max(0, math.sin(v)))  # noqa: E731
        body = stack(sp_, sp_.triangle, 0, math.pi, 30, side).set_fill(GREEN, .25).set_stroke(width=.5)
        self.play(FadeIn(body), run_time=self.rt(.1))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.15), tx('thiết diện: tam giác đều', 22, WHITE),
                         tx('(làm tròn đến hàng phần trăm)', 21, SOFT), frac=.16)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', 1.15), frac=.12)
        self.wait_until(.35, t0)
        self.write_board(self.M('sa_s2', 1.0), frac=.12)
        self.wait_until(.72, t0)
        self.write_board(self.answer_sheet('3,46'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Cắt lát – cộng dồn', 'sum1', 'Thể tích = tích phân của diện tích'),
                                ('Tìm S(x)', 'sum2', 'Bước quan trọng nhất'),
                                ('Hình chóp', 'sum3', 'Chứng minh bằng tích phân')),
                           fracs=(.04, .35, .58))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính V:', 'hw1'), ('Tính V:', 'hw2'), ('Tính V:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Quay miền phẳng quanh Ox · thiết diện là hình tròn', 26, GOLD, bold=True),
                            self.M('next1', 1.4)])


class INT25_SMOKE(INT25):
    smoke = True
