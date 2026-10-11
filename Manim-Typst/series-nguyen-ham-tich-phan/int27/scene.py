"""INT27 – Khối tròn xoay giữa hai đường: vành khăn.

    python scripts/build_typst.py --ep int27
    python scripts/prepare_voice.py --ep int27 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int27/scene.py INT27
    python scripts/finalize.py --ep int27

One method per narration beat (int27/lesson.py); shared screens come from
common/blocks.py and common/revolve.py. Every number shown is checked in
lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Annulus, Circle, Create, FadeIn, FadeOut, ValueTracker, VGroup, Write, \
    always_redraw, linear

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, cross, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.revolve import region, ring, solid  # noqa: E402
from common.theme import BG, CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def lin(v):
    return v


def sq(v):
    return v * v


class INT27(LessonScene):
    EP = 'int27'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def spin_between(self, a, f, g, x0, x1, frac, color=GOLD, n=10):
        th = ValueTracker(0)
        live = always_redraw(lambda: region(a, f, x0, x1, math.cos(th.get_value()), color, .5,
                                            g=lambda v: g(v)))
        self.add(live)
        self.play(th.animate.set_value(2 * math.pi), run_time=self.rt(frac), rate_func=linear)
        live.clear_updaters()
        self.remove(live)
        outer, inner = solid(a, f, x0, x1, n, color), solid(a, g, x0, x1, n, CYAN)
        rings = VGroup(*[ring(a, f, g, x0 + (x1 - x0) * (k + .5) / n, color, .35, 1) for k in range(n)])
        body = VGroup(outer[1], outer[2], inner[1], inner[2], rings)
        self.add(body)
        return body

    def pair_axes(self, f, g, x0, x1, xr, yr, xt, yt, cf=GOLD, cg=CYAN):
        a = self.ax(xr, yr, xt, yt)
        self.show_axes(a)
        self.play(Create(clipped(a, f, max(xr[0], x0 - .15), min(xr[1], x1 + .15), cf, 4.5, y_min=yr[0], y_max=yr[1])),
                  Create(clipped(a, g, max(xr[0], x0 - .15), min(xr[1], x1 + .15), cg, 4.5, y_min=yr[0], y_max=yr[1])),
                  FadeIn(region(a, f, x0, x1, color=GREEN, opacity=.45, g=g)), run_time=self.rt(.07))
        return a

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.pair_axes(lin, sq, 0, 1, (0, 1.3, 1), (-1.3, 1.3, 1), (1,), (-1, 1))
        self.write_board(self.M('hook', 1.15), frac=.08)
        self.wait_until(.15, t0)
        self.spin_between(a, lin, sq, 0, 1, .2)
        self.wait_until(.42, t0)
        self.write_board(self.M('hook_wrong', 1.05), frac=.1)
        self.wait_until(.7, t0)
        self.write_board(self.M('hook_right', 1.4), tx('lớn gấp 4 lần! Sai ở đâu?', 24, GOLD, bold=True), frac=.1)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Vành khăn', 'Đĩa bị khoét lỗ ở giữa'),
                         ('Công thức vành khăn', 'Khối ngoài trừ khối trong'),
                         ('Bẫy', 'Bình phương của hiệu')], t0, fracs=(.12, .38, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        f = lambda v: 1.6 + .3 * math.sin(1.4 * v)  # noqa: E731
        g = lambda v: .6 + .15 * v  # noqa: E731
        a = self.pair_axes(f, g, .3, 3.8, (0, 4.2, 1), (-2.2, 2.2, 1), (), ())
        self.write_board(self.heading('THIẾT DIỆN LÀ VÀNH KHĂN'), frac=.05)
        self.wait_until(.15, t0)
        self.spin_between(a, f, g, .3, 3.8, .3)
        self.wait_until(.55, t0)
        big = VGroup(Annulus(inner_radius=.55, outer_radius=1.25, color=GOLD, fill_opacity=.6),
                     Circle(radius=.55, color=CYAN, stroke_width=2), Circle(radius=1.25, color=GOLD, stroke_width=2))
        big.move_to([3.4, -.9, 0])
        labels = VGroup(self.TM('$R = f(x)$', 20, GOLD).next_to(big, RIGHT, buff=.2).shift(UP * .3),
                        self.TM('$r = g(x)$', 20, CYAN).next_to(big, RIGHT, buff=.2).shift(DOWN * .3))
        self.play(FadeIn(big), FadeIn(labels), run_time=self.rt(.08))

    def beat_c2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CÔNG THỨC VÀNH KHĂN', ('ring', 'washer'), (.05, .35), (1.4, 1.5), gap=.6)
        self.wait_until(.75, t0)
        r = VGroup(tx('khối ngoài trừ khối trong:', 25, SOFT), self.M('outin', 1.4)).arrange(RIGHT, buff=.3) \
            .next_to(lines[-1], DOWN, buff=.6)
        self.play(FadeIn(r), run_time=self.rt(.05))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(badge('BẪY: BÌNH PHƯƠNG CỦA HIỆU', CORAL, 20).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        self.play(Write(self.M('trap', 1.5).move_to([0, 1.7, 0])), run_time=self.rt(.08))
        self.wait_until(.25, t0)
        ann = VGroup(Annulus(inner_radius=.7, outer_radius=1.3, color=GOLD, fill_opacity=.6),
                     Circle(radius=1.3, color=GOLD, stroke_width=2)).move_to([-3.2, -.15, 0])
        small = Circle(radius=.6, color=CORAL, fill_opacity=.6).move_to([3.0, -.15, 0])
        self.play(FadeIn(ann), FadeIn(self.TM('vành khăn: $pi (R^2 - r^2)$', 22, GOLD, bold=True).next_to(ann, DOWN, buff=.25)),
                  run_time=self.rt(.07))
        self.wait_until(.5, t0)
        self.play(FadeIn(small), FadeIn(self.TM('hình tròn bán kính $R - r$', 22, CORAL, bold=True).next_to(small, DOWN, buff=.85)),
                  run_time=self.rt(.07))
        self.wait_until(.72, t0)
        self.play(Write(self.M('trap_geo', 1.2).move_to([0, -2.72, 0])), run_time=self.rt(.08))

    def beat_c3b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        ann = VGroup(Annulus(inner_radius=.8, outer_radius=1.6, color=GOLD, fill_opacity=.6),
                     Circle(radius=1.6, color=GOLD, stroke_width=2)).move_to([-3.2, .3, 0])
        small = Circle(radius=.8, color=CORAL, fill_opacity=.6).move_to([3.2, .3, 0])
        self.play(FadeIn(ann), FadeIn(self.TM('$R = 2, quad r = 1: quad 3 pi$', 26, GOLD).next_to(ann, DOWN, buff=.3)),
                  run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(FadeIn(small), FadeIn(self.TM('$pi (R - r)^2 = pi$', 26, CORAL).next_to(small, DOWN, buff=1.1)),
                  run_time=self.rt(.08))
        self.wait_until(.65, t0)
        self.play(Write(self.M('num', 1.3).move_to([0, -2.5, 0])), run_time=self.rt(.1))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 4 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Giao điểm', 'tìm cận a, b', CYAN), ('Ngoài / trong', 'đường xa trục hơn là f', GOLD),
                 ('Bình phương', 'từng hàm rồi mới trừ', CORAL), ('Nhân π', 'tích phân rồi nhân π', GREEN))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.05, .2, .45, .65))):
            c = card(3.0, 3.0, col).move_to([-4.65 + 3.1 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 24, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 17, SOFT, max_w=2.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('LƯU Ý', GOLD, 20)
        rows = (self.TM('miền nằm hoàn toàn một phía của trục $O x$', 26, WHITE),
                tx('đề thi chương trình mới hầu như luôn như vậy', 24, SOFT),
                tx('hai hàm âm: lấy trị tuyệt đối, đường ngoài là đường xa trục', 24, GOLD, bold=True))
        self.centre(head, *rows, top=1.8, gap=.55)
        self.play(FadeIn(head), FadeIn(rows[0]), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.play(FadeIn(rows[1]), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.play(FadeIn(rows[2]), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.pair_axes(lin, sq, 0, 1, (0, 1.3, 1), (-1.3, 1.3, 1), (1,), (-1, 1))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.TM('đường ngoài: $y = x$ · đường trong: $y = x^2$', 22, WHITE), frac=.08)
        self.wait_until(.2, t0)
        self.spin_between(a, lin, sq, 0, 1, .25)
        self.wait_until(.55, t0)
        m = self.M('e1_s1', 1.05)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'SO SÁNH VỚI CÁCH SAI', ('e2_s1',), (.1,), (1.4,), box_last=False)
        self.wait_until(.55, t0)
        self.play(FadeIn(VGroup(cross(CORAL, .28), tx('trắc nghiệm hay đặt sẵn phương án sai này', 25, CORAL, bold=True))
                         .arrange(RIGHT, buff=.25).next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def example(self, t0, tag, task, f, g, x0, x1, xr, yr, xt, yt, keys, scales, fracs=(.12, .5, .75)):
        self.clear_stage(.05)
        a = self.pair_axes(f, g, x0, x1, xr, yr, xt, yt)
        self.write_board(badge(tag, GOLD, 20), self.M(task, 1.2), frac=.08)
        self.wait_until(fracs[0], t0)
        self.spin_between(a, f, g, x0, x1, .22)
        lines = []
        for k, s, frac in zip(keys, scales, fracs[1:]):
            self.wait_until(frac, t0)
            m = self.M(k, s)
            self.write_board(m, frac=.1)
            lines.append(m)
        self.play(FadeIn(self.box(lines[-1], GREEN)), run_time=self.rt(.03))
        return a

    def beat_e3(self, T):
        self.example(self.now(), 'VÍ DỤ 2', 'e3_task', math.sqrt, sq, 0, 1, (0, 1.3, 1), (-1.3, 1.3, 1), (1,), (-1, 1),
                     ('e3_s1',), (1.05,), fracs=(.12, .5))

    def beat_e4(self, T):
        self.example(self.now(), 'VÍ DỤ 3', 'e4_task', lambda v: 3 - v * v, lambda v: v * v + 1, -1, 1,
                     (-1.5, 1.5, 1), (-3.4, 3.4, 1), (-1, 1), (-3, -1, 1, 3), ('e4_s1', 'e4_s2'), (1.05, 1.1),
                     fracs=(.12, .5, .75))

    def beat_e5(self, T):
        self.example(self.now(), 'VÍ DỤ 4', 'e5_task', math.exp, lambda v: 1, 0, 1, (0, 1.4, 1), (-3, 3, 1), (1,),
                     (-2, 2), ('e5_s1',), (1.05,), fracs=(.15, .55))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 1.4, 1), (-3, 3, 1), (1,), (-2, 2))
        self.show_axes(a)
        outer = solid(a, math.exp, 0, 1, 10, GOLD)
        inner = solid(a, lambda v: 1, 0, 1, 10, CYAN)
        self.write_board(self.heading('KHỐI NGOÀI TRỪ KHỐI TRONG'), frac=.05)
        self.play(FadeIn(outer), run_time=self.rt(.08))
        self.write_board(self.TM('khối ngoài: quay $y = e^x$', 22, GOLD), frac=.05)
        self.wait_until(.4, t0)
        self.play(FadeIn(inner), run_time=self.rt(.08))
        self.write_board(self.TM('khối trong: hình trụ $r = 1, h = 1$', 22, CYAN), frac=.05)
        self.wait_until(.65, t0)
        m = self.M('e6_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('CHỌN ĐÚNG CÔNG THỨC', 26, GOLD, bold=True).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        rows = (('quay miền dưới một đường', 'pick1', CYAN, .05), ('quay miền giữa hai đường', 'pick2', GOLD, .35),
                ('diện tích miền phẳng', 'pick3', GREEN, .65))
        for i, (txt, key, col, frac) in enumerate(rows):
            c = card(12.4, 1.45, col).move_to([0, 1.4 - 1.65 * i, 0])
            g = VGroup(c, tx(txt, 24, col, bold=True).move_to(c.get_left() + RIGHT * 2.7),
                       self.M(key, 1.15, max_w=6.2).move_to(c.get_center() + RIGHT * 2.6))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.06))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Quay miền giới hạn bởi', 24, WHITE), self.M('tf_given', 1.3),
                    self.TM('quanh $O x$, được thể tích $V$.', 24, WHITE)).arrange(RIGHT, buff=.2)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (VGroup(tx('Giao tại', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.3), self.M('tf_c', 1.3), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .75))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, False), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(3, True), run_time=self.rt(.1))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.pair_axes(math.sqrt, lambda v: v / 2, 0, 4, (0, 4.5, 1), (-2.4, 2.4, 1), (1, 2, 3, 4), (-2, 2))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.3), self.TM('quay quanh $O x$ · làm tròn đến hàng phần trăm', 21, SOFT), frac=.14)
        self.wait_until(.55, t0)
        self.spin_between(a, math.sqrt, lambda v: v / 2, 0, 4, .3)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', .9), frac=.14)
        self.wait_until(.75, t0)
        self.write_board(self.answer_sheet('8,38'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Vành khăn', 'sum1', 'Đĩa bị khoét lỗ'),
                                ('Ngoài trừ trong', 'sum2', 'Thể tích khối ngoài trừ khối trong'),
                                ('Bẫy', 'sum3', 'Không bình phương của hiệu')),
                           fracs=(.04, .3, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Quay:', 'hw1'), ('Quay:', 'hw2'), ('Quay:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Dựng lại công thức bằng tích phân', 26, GOLD, bold=True), self.M('next1', 1.05)])


class INT27_SMOKE(INT27):
    smoke = True
