"""INT21 – Diện tích hình phẳng giới hạn bởi đồ thị và trục Ox.

    python scripts/build_typst.py --ep int21
    python scripts/prepare_voice.py --ep int21 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int21/scene.py INT21
    python scripts/finalize.py --ep int21

One method per narration beat (int21/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Rectangle, Transform, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, check, clipped, cross, dashed, signed_area, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def hook_f(v):
    return v * v - 2 * v


class INT21(LessonScene):
    EP = 'int21'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def hook_axes(self):
        a = self.ax((-.3, 3.4, 1), (-1.6, 3.4, 1), (1, 2, 3), (-1, 1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, hook_f, -.2, 3.2, CYAN, 4.5)), run_time=self.rt(.05))
        return a

    def flip(self, a, f, x0, x1):
        """Lift the part below the axis: coral region → green region above."""
        return VGroup(area(a, lambda v: -f(v), x0, x1, GREEN, .5), clipped(a, lambda v: -f(v), x0, x1, GOLD, 4))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.hook_axes()
        self.write_board(self.M('hook', 1.0), frac=.1)
        self.play(FadeIn(signed_area(a, hook_f, 0, 3, opacity=.5)),
                  Create(dashed(a.c2p(3, 0), a.c2p(3, 3), color=SOFT)), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.write_board(self.M('hook_int', 1.25), frac=.1)
        self.wait_until(.55, t0)
        self.write_board(tx('nhưng trên hình có hai mảnh!', 23, GOLD, bold=True), frac=.06)
        self.wait_until(.82, t0)
        m = self.M('hook_s', 1.7)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Công thức', 'Tích phân của trị tuyệt đối f'),
                         ('Tìm cận', 'Khi đề không cho đường thẳng đứng'),
                         ('Bẫy', 'Quên trị tuyệt đối')], t0, fracs=(.1, .36, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.4, 1), (0, 3.2, 1), (), ())
        self.show_axes(a)
        f = lambda v: 1.2 + .6 * math.sin(1.6 * v) + .2 * v  # noqa: E731
        self.play(Create(clipped(a, f, 0, 3.3, CYAN, 4.5)), run_time=self.rt(.06))
        self.play(FadeIn(area(a, f, .5, 2.8, CYAN, .45)),
                  Create(dashed(a.c2p(.5, 0), a.c2p(.5, f(.5)), color=WHITE)),
                  Create(dashed(a.c2p(2.8, 0), a.c2p(2.8, f(2.8)), color=WHITE)),
                  FadeIn(tx('a', 22, WHITE).move_to(a.c2p(.5, -.25))), FadeIn(tx('b', 22, WHITE).move_to(a.c2p(2.8, -.25))),
                  run_time=self.rt(.08))
        self.write_board(self.heading('HÌNH PHẲNG GIỚI HẠN BỞI'),
                         tx('y = f(x), trục Ox, x = a, x = b', 23, WHITE), frac=.12)
        self.wait_until(.55, t0)
        m = self.M('area', 1.5)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.hook_axes()
        n, w = 12, 3 / 12
        strips = VGroup()
        for k in range(n):
            xm = (k + .5) * w
            hgt = hook_f(xm)
            p, q = a.c2p(k * w, 0), a.c2p((k + 1) * w, hgt)
            strips.add(Rectangle(width=abs(q[0] - p[0]), height=max(abs(q[1] - p[1]), .01),
                                 fill_color=GREEN if hgt >= 0 else CORAL, fill_opacity=.55, stroke_width=1,
                                 stroke_color=WHITE).move_to((p + q) / 2))
        self.write_board(self.heading('DẢI HẸP: CAO = KHOẢNG CÁCH TỚI Ox'), frac=.05)
        self.play(FadeIn(strips), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        lifted = VGroup(*[s.copy().set_fill(GREEN).move_to(s.get_center() * [1, 0, 0] + [0, a.c2p(0, 0)[1] + s.height / 2, 0])
                          for s in strips])
        self.play(Transform(strips, lifted), run_time=self.rt(.12))
        self.write_board(tx('diện tích: mọi dải đều dương', 23, GREEN, bold=True),
                         tx('tích phân: dải dưới trục mang dấu âm', 23, CORAL), frac=.1)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BA TRƯỜNG HỢP', GOLD, 20)
        rows = [self.M(k, 1.35) for k in ('case1', 'case2', 'case3')]
        note = tx('f đổi dấu tại c: tách cận, đoạn âm thì đổi dấu', 23, SOFT)
        self.centre(head, *rows, note, top=2.5, gap=.5)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, m in zip((.08, .32, .58), rows):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.1))
        self.play(FadeIn(note), run_time=self.rt(.04))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        g = lambda v: v * v - 4 * v + 3  # noqa: E731
        a = self.ax((0, 4.2, 1), (-1.4, 3.4, 1), (1, 2, 3, 4), (-1, 1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, g, 0, 4.1, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(self.heading('CẬN = NGHIỆM CỦA f(x) = 0'), frac=.06)
        self.wait_until(.45, t0)
        self.write_board(self.M('roots', 1.2), frac=.1)
        self.play(FadeIn(area(a, g, 1, 3, CORAL, .5)), FadeIn(dot_pair(a, (1, 3))), run_time=self.rt(.08))

    def beat_c5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'MẸO TÍNH NHANH', ('split',), (.15,), (1.3,), box_last=False)
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('mỗi khoảng giữa hai nghiệm: f không đổi dấu', 25, SOFT).next_to(lines[-1], DOWN, buff=.7)),
                  run_time=self.rt(.05))
        self.wait_until(.82, t0)
        self.play(FadeIn(tx('→ tiện bấm máy tính', 25, GREEN, bold=True).next_to(lines[-1], DOWN, buff=1.4)),
                  run_time=self.rt(.05))

    def beat_c5b(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'BẤM MÁY TÍNH', ('casio',), (.1,), (1.6,), box_last=False)
        r1 = VGroup(check(GREEN, .28), tx('máy tự xử lý trị tuyệt đối', 25, GREEN)).arrange(RIGHT, buff=.25)
        r2 = VGroup(cross(CORAL, .26), tx('nhiều nghiệm: chậm, có thể kém chính xác', 25, CORAL)).arrange(RIGHT, buff=.25)
        r3 = tx('An toàn nhất: tách cận tại nghiệm, cộng các trị tuyệt đối', 25, GOLD, bold=True)
        VGroup(r1, r2, r3).arrange(DOWN, buff=.4).next_to(lines[-1], DOWN, buff=.7)
        self.wait_until(.25, t0)
        self.play(FadeIn(r1), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.play(FadeIn(r2), run_time=self.rt(.05))
        self.wait_until(.7, t0)
        self.play(FadeIn(r3), run_time=self.rt(.05))

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('HAI BẪY HAY GẶP', CORAL, 20)
        r1 = VGroup(cross(CORAL, .28), tx('Quên trị tuyệt đối: đáp số âm hoặc bằng 0', 26, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25)
        m = self.M('trap', 1.35)
        r2 = VGroup(cross(CORAL, .28), tx('Đưa trị tuyệt đối ra ngoài cả đoạn khi f đổi dấu', 26, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25)
        ok = VGroup(check(GREEN, .28), tx('Diện tích luôn dương', 26, GREEN, bold=True)).arrange(RIGHT, buff=.25)
        self.centre(head, r1, m, r2, ok, top=2.5, gap=.5)
        self.play(FadeIn(head), FadeIn(r1), run_time=self.rt(.06))
        self.play(Write(m), run_time=self.rt(.1))
        self.wait_until(.42, t0)
        self.play(FadeIn(ok), run_time=self.rt(.04))
        self.wait_until(.55, t0)
        self.play(FadeIn(r2), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.hook_axes()
        parts = signed_area(a, hook_f, 0, 3, opacity=.5)
        self.play(FadeIn(parts), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), frac=.04)
        self.wait_until(.25, t0)
        self.write_board(self.M('e1_s1', 1.0), frac=.12)
        self.wait_until(.55, t0)
        self.play(FadeIn(self.flip(a, hook_f, 0, 2)), run_time=self.rt(.1))
        m = self.M('e1_s2', 1.5)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        g = lambda v: v * v - 4 * v + 3  # noqa: E731
        a = self.ax((0, 4.2, 1), (-1.4, 3.4, 1), (1, 2, 3, 4), (-1, 1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, g, 0, 4.1, CYAN, 4.5)), FadeIn(area(a, g, 1, 3, CORAL, .5)), run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('roots', 1.15), frac=.1)
        self.wait_until(.45, t0)
        m = self.M('e2_s1', 1.05)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.flip(a, g, 1, 3)), FadeIn(self.box(m, GREEN)), run_time=self.rt(.08))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        h = lambda v: v ** 3 - v  # noqa: E731
        a = self.ax((-1.5, 1.5, 1), (-1, 1, 1), (-1, 1), (), h=4.6)
        self.show_axes(a)
        self.play(Create(clipped(a, h, -1.45, 1.45, CYAN, 4.5, y_min=-1, y_max=1)),
                  FadeIn(signed_area(a, h, -1, 1, opacity=.5)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), self.M('e3_task', 1.3), frac=.08)
        self.wait_until(.35, t0)
        self.play(FadeIn(tx('1/4', 22, WHITE, bold=True).move_to(a.c2p(-.55, .12))),
                  FadeIn(tx('1/4', 22, WHITE, bold=True).move_to(a.c2p(.55, -.12))), run_time=self.rt(.05))
        m = self.M('e3_s1', .95)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 3.2, 1), (-1.4, 1.4, 1), (1, 2, 3), (-1, 1))
        self.show_axes(a)
        self.play(Create(clipped(a, math.log, .2, 3.1, CYAN, 4.5, y_min=-1.4)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_task', 1.3), frac=.08)
        self.wait_until(.3, t0)
        self.play(Create(dashed(a.c2p(math.e, 0), a.c2p(math.e, 1), color=WHITE)),
                  FadeIn(tx('e', 22, WHITE).move_to(a.c2p(math.e, -.25))), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(FadeIn(area(a, math.log, 1, math.e, GREEN, .5)), run_time=self.rt(.06))
        m = self.M('e4_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        f = lambda v: 1.4 * math.sin(1.25 * (v - .4))  # noqa: E731
        a = self.ax((0, 3.4, 1), (-1.6, 1.6, 1), (), ())
        self.show_axes(a)
        c = .4 + math.pi / 1.25
        self.play(Create(clipped(a, f, .2, 3.3, CYAN, 4.5)), FadeIn(signed_area(a, f, .4, 3.2, opacity=.5)),
                  run_time=self.rt(.08))
        for v, s in ((.4, 'a'), (c, 'c'), (3.2, 'b')):
            self.add(tx(s, 22, WHITE).move_to(a.c2p(v, .25 if v == 3.2 else -.25)))
        self.write_board(badge('VÍ DỤ 5', GOLD, 20), tx('Theo hình vẽ, công thức nào đúng?', 23, WHITE), frac=.1)
        self.wait_until(.45, t0)
        m = self.M('e5_s1', 1.15)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.78, t0)
        self.write_board(tx('nhìn dấu trên hình → dấu trước tích phân', 22, GOLD), frac=.05)

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        f = lambda v: 1.4 * math.sin(1.25 * (v - .4))  # noqa: E731
        a = self.ax((0, 3.4, 1), (-1.6, 1.6, 1), (), ())
        self.show_axes(a)
        c = .4 + math.pi / 1.25
        self.play(Create(clipped(a, f, .2, 3.3, CYAN, 4.5)), FadeIn(signed_area(a, f, .4, 3.2, opacity=.5)),
                  run_time=self.rt(.08))
        self.play(FadeIn(tx('S1 = 3', 22, WHITE, bold=True).move_to(a.c2p(1.65, .6))),
                  FadeIn(tx('S2 = 1', 22, WHITE, bold=True).move_to(a.c2p(c + .45, -.45))), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 6', GOLD, 20), tx('Biết S1 = 3 (trên), S2 = 1 (dưới).', 23, WHITE),
                         tx('Tính tích phân từ a đến b của f.', 23, WHITE), frac=.12)
        self.wait_until(.55, t0)
        m = self.M('e6_s1', 1.25)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.85, t0)
        self.write_board(tx('không phải 3 + 1 = 4!', 23, CORAL, bold=True), frac=.05)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('D giới hạn bởi', 24, WHITE), self.M('tf_given', 1.25)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi S là diện tích của D. Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.3) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.4, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        sol = VGroup(tx('b)', 22, SOFT), self.M('tf_b_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(1, False), run_time=self.rt(.1))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s = lambda v: v * v - 2 * v - 3  # noqa: E731
        a = self.ax((-1.5, 3.5, 1), (-4.4, 1.4, 1), (-1, 1, 2, 3), (-4, -2))
        self.show_axes(a)
        self.play(Create(clipped(a, s, -1.4, 3.4, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), tx('(làm tròn đến hàng phần mười)', 21, SOFT), frac=.14)
        self.wait_until(.65, t0)
        self.write_board(self.M('sa_s1', 1.15), frac=.1)
        self.play(FadeIn(area(a, s, -1, 3, CORAL, .5)), run_time=self.rt(.06))
        self.x4_axes = a

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('sa_s2', 1.0)
        self.write_board(m, frac=.14)
        self.play(FadeIn(area(self.x4_axes, lambda v: v * v - 2 * v - 3, -1, 3, GREEN, .55)), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.write_board(self.answer_sheet('10,7'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Công thức', 'sum1', 'Diện tích không bao giờ âm'),
                                ('Tìm cận', 'sum2', 'Nghiệm của f(x) = 0'),
                                ('Tách cận', 'sum3', 'Mỗi khoảng: đưa trị tuyệt đối ra ngoài')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính S:', 'hw1'), ('Tính S:', 'hw2'), ('Tính S:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Tìm giao điểm · chia khoảng · trên trừ dưới', 26, GOLD, bold=True),
                            self.M('next1', 1.4)])


def dot_pair(a, xs):
    from common.kit import dot
    return VGroup(*[dot(a, v, 0, GOLD, .09) for v in xs])


class INT21_SMOKE(INT21):
    smoke = True
