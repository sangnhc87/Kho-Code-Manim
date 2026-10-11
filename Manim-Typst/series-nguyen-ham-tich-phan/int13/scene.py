"""INT13 – Tính chất của tích phân.

    python scripts/build_typst.py --ep int13
    python scripts/prepare_voice.py --ep int13 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int13/scene.py INT13
    python scripts/finalize.py --ep int13

One method per narration beat (int13/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, GrowArrow, Line, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, clipped, cross, dashed, signed_area, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def bump(v):
    return 1 + .6 * math.sin(1.3 * v) + .15 * v


class INT13(LessonScene):
    EP = 'int13'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m = self.M('hook', 1.45).move_to([0, 1.6, 0])
        self.play(Write(m), run_time=self.rt(.14))
        self.wait_until(.42, t0)
        q = VGroup(tx('f = ?', 34, CORAL, bold=True), tx('g = ?', 34, CORAL, bold=True)).arrange(RIGHT, buff=1.4) \
            .move_to([0, 0, 0])
        self.play(FadeIn(q, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('→ dùng TÍNH CHẤT của tích phân', 28, GOLD, bold=True).move_to([0, -1.6, 0])),
                  run_time=self.rt(.07))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Tuyến tính', 'Tách tổng, đưa hằng số ra ngoài'),
                         ('Cộng khoảng & đổi cận', 'Cắt miền tại một điểm'),
                         ('So sánh, chẵn lẻ', 'Ước lượng và đối xứng')], t0, fracs=(.12, .35, .56))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.2, 1), (0, 4.2, 1), (1, 2, 3), (1, 2, 3, 4))
        self.show_axes(a)
        self.play(Create(clipped(a, bump, 0, 3.1, CYAN, 4)), FadeIn(area(a, bump, .2, 2.8, CYAN, .4)),
                  run_time=self.rt(.1))
        self.write_board(self.heading('TÍNH CHẤT TUYẾN TÍNH'), self.M('lin', .95), frac=.16)
        self.wait_until(.6, t0)
        self.play(Create(clipped(a, lambda v: 1.5 * bump(v), 0, 2.75, GOLD, 4)),
                  FadeIn(area(a, lambda v: 1.5 * bump(v), .2, 2.8, GOLD, .2)), run_time=self.rt(.1))
        self.write_board(tx('nhân f với k  →  diện tích nhân k', 23, GOLD, bold=True), frac=.06)

    def beat_c2(self, T):
        self.worked(self.now(), 'ÁP DỤNG BÀI MỞ ĐẦU', ('lin_ex', 'const'), (.05, .7), (1.5, 1.6), box_last=False,
                    gap=.8)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.2, 1), (0, 3.2, 1), (1, 2, 3), (1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, bump, 0, 3.1, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(self.heading('CỘNG KHOẢNG'), self.M('chasles', 1.0), frac=.14)
        self.wait_until(.3, t0)
        left, right = area(a, bump, .3, 1.5, GREEN, .5), area(a, bump, 1.5, 2.8, PURPLE, .5)
        labels = VGroup(tx('a', 20, WHITE).move_to(a.c2p(.3, -.25)), tx('b', 20, GOLD, bold=True).move_to(a.c2p(1.5, -.25)),
                        tx('c', 20, WHITE).move_to(a.c2p(2.8, -.25)))
        self.play(FadeIn(left), FadeIn(right), FadeIn(labels),
                  Create(dashed(a.c2p(1.5, 0), a.c2p(1.5, bump(1.5)), color=GOLD, stroke_width=3)), run_time=self.rt(.1))

    def beat_c4(self, T):
        self.worked(self.now(), 'VÍ DỤ', ('ch_ex1', 'ch_ex2'), (.04, .55), (1.5, 1.6), gap=.8)

    def beat_c4b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        y = .9
        line = VGroup(Line([-5, y, 0], [5, y, 0], color=SOFT, stroke_width=3))
        for v in range(4):
            px = -4.5 + 3 * v
            line.add(Line([px, y - .1, 0], [px, y + .1, 0], color=SOFT, stroke_width=2),
                     tx(str(v), 22, SOFT).move_to([px, y - .4, 0]))
        self.play(Create(line), run_time=self.rt(.06))
        go = Arrow([-4.5, y + .55, 0], [4.5, y + .55, 0], color=GREEN, buff=0, stroke_width=6)
        back = Arrow([4.5, y + 1.15, 0], [-1.5, y + 1.15, 0], color=CORAL, buff=0, stroke_width=6)
        net = Arrow([-4.5, y - 1.0, 0], [-1.5, y - 1.0, 0], color=GOLD, buff=0, stroke_width=7)
        self.wait_until(.25, t0)
        self.play(GrowArrow(go), FadeIn(tx('0 → 3', 20, GREEN).next_to(go, UP, buff=.05)), run_time=self.rt(.08))
        self.play(GrowArrow(back), FadeIn(tx('3 → 1', 20, CORAL).next_to(back, UP, buff=.05)), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(GrowArrow(net), FadeIn(tx('kết quả: 0 → 1', 20, GOLD, bold=True).next_to(net, DOWN, buff=.08)),
                  run_time=self.rt(.08))
        self.play(Write(self.M('ch_out', 1.6).move_to([0, -2.4, 0])), run_time=self.rt(.1))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.2, 1), (0, 3.2, 1), (1, 2, 3), (1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, bump, 0, 3.1, CYAN, 4)), FadeIn(area(a, bump, .3, 2.8, CYAN, .35)),
                  run_time=self.rt(.07))
        self.write_board(self.heading('SO SÁNH'), self.M('cmp1', 1.0), frac=.14)
        self.wait_until(.45, t0)
        lo, hi = min(bump(v / 20) for v in range(6, 57)), max(bump(v / 20) for v in range(6, 57))
        self.play(FadeIn(area(a, lambda v: lo, .3, 2.8, GREEN, .25)), FadeIn(area(a, lambda v: hi, .3, 2.8, GOLD, .12)),
                  Create(dashed(a.c2p(.3, hi), a.c2p(2.8, hi), color=GOLD)), run_time=self.rt(.1))
        self.play(FadeIn(tx('M', 20, GOLD, bold=True).move_to(a.c2p(3.0, hi))),
                  FadeIn(tx('m', 20, GREEN, bold=True).move_to(a.c2p(3.0, lo))), run_time=self.rt(.04))
        self.write_board(self.M('cmp2', 1.05), frac=.1)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        for i, (f, key, sym) in enumerate(((lambda v: v ** 3 / 2, 'odd', True), (lambda v: v * v, 'even', False))):
            a = axes((-1.7, 1.7, 1), (-1.8, 2.6, 1), 4.8, 3.6, center=[-3.3 + 6.6 * i, .5, 0], x_ticks=(-1, 1),
                     x_label='', y_label='')
            g = VGroup(a, clipped(a, f, -1.7, 1.7, CYAN, 4),
                       signed_area(a, f, -1.5, 1.5) if sym else area(a, f, -1.5, 1.5, GREEN, .45))
            m = self.M(key, 1.15, max_w=6.2).next_to(a, DOWN, buff=.35)
            self.wait_until((.05, .45)[i], t0)
            self.play(FadeIn(g), Write(m), run_time=self.rt(.14))

    def beat_c7(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'BẪY TÍCH VÀ THƯƠNG', ('trap',), (.08,), (1.4,), box_last=False)
        self.wait_until(.6, t0)
        self.play(FadeIn(VGroup(cross(CORAL, .3), tx('Không tách tích phân của tích hay thương', 24, CORAL, bold=True))
                         .arrange(RIGHT, buff=.25).next_to(lines[-1], DOWN, buff=.9)), run_time=self.rt(.07))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 2.3, 1), (0, 3.4, 1), (1, 2), (1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, 0, 1, CYAN, 4.5)),
                  Create(clipped(a, lambda v: 2 * v - 1, 1, 2.2, GOLD, 4.5)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('e1_f', 1.3), frac=.14)
        self.wait_until(.42, t0)
        self.play(FadeIn(area(a, lambda v: v * v, 0, 1, CYAN, .45)), FadeIn(area(a, lambda v: 2 * v - 1, 1, 2, GOLD, .45)),
                  Create(dashed(a.c2p(1, 0), a.c2p(1, 1), color=WHITE, stroke_width=2)), run_time=self.rt(.08))
        m = self.M('e1_s1', 1.0)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 1.3, 1), (0, 3.2, 1), (1,), (1, 2, 3))
        self.show_axes(a)
        f = lambda v: math.exp(v * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 1.15, CYAN, 4.5)), FadeIn(area(a, f, 0, 1, CYAN, .4)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), frac=.04)
        self.wait_until(.35, t0)
        self.play(Create(dashed(a.c2p(0, 1), a.c2p(1.3, 1), color=GREEN)),
                  Create(dashed(a.c2p(0, math.e), a.c2p(1.3, math.e), color=GOLD)), run_time=self.rt(.06))
        self.write_board(self.M('e2_s1', 1.0), frac=.12)
        self.wait_until(.78, t0)
        self.write_board(self.M('e2_s2', 1.4), frac=.08)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.2, 2.2, 1), (-4, 21, 5), (-2, -1, 1, 2), (5, 10, 15, 20))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v ** 3, -2.2, 2.2, PURPLE, 3)),
                  Create(clipped(a, lambda v: 3 * v * v, -2.2, 2.2, GREEN, 3)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), tx('x³: hàm lẻ  ·  3x²: hàm chẵn', 22, WHITE), frac=.1)
        self.wait_until(.45, t0)
        m = self.M('e3_s1', 1.05)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        self.worked(self.now(), 'VÍ DỤ 4: TÌM CẬN', ('e4_s1',), (.1,), (1.3,))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Biết', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.4), self.M('tf_b', 1.4), self.M('tf_c', 1.4), self.M('tf_d', 1.4))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.15)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.12))
        self.wait_until(.48, t0)
        note = tx('d) f = x, g = −1 vẫn thỏa đề nhưng ∫f·g = −4: không xác định', 21, CORAL, bold=True) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(sol), FadeIn(note), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐĐSS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task, sol = self.M('sa_task', 1.35), self.M('sa_s1', 1.4)
        sheet = self.answer_sheet('11')
        self.centre(tag, task, sol, sheet, top=2.6, gap=.45)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.14))
        self.wait_until(.5, t0)
        self.play(Write(sol), run_time=self.rt(.14))
        self.play(FadeIn(sheet), run_time=self.rt(.05))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO HÀM THAY THẾ', GOLD, 21)
        idea = tx('Chọn f là hàm hằng thỏa giá trị tích phân đề cho', 25, WHITE)
        m = self.M('tip', 1.7)
        warn = tx('Chỉ dùng khi biểu thức cần tính tuyến tính theo f', 24, CORAL, bold=True)
        self.centre(head, idea, m, warn, top=2.5, gap=.6)
        self.play(FadeIn(head), FadeIn(idea), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(Write(m), run_time=self.rt(.14))
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.04))
        self.wait_until(.8, t0)
        self.play(FadeIn(warn), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Tuyến tính', 'sum1', 'Tích phân của hằng số = k(b − a)'),
                                ('Cộng khoảng', 'sum2', 'Đúng với mọi a, b, c'),
                                ('Chẵn, lẻ', 'sum3', 'Hàm chẵn: gấp đôi nửa đoạn')),
                           fracs=(.04, .45, .66))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Biết', 'hw1'), ('Tính', 'hw2'), ('Tính', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .45, .58))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.0)])


class INT13_SMOKE(INT13):
    smoke = True
