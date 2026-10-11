"""INT18 – Tích phân hàm ẩn & tính đối xứng.

    python scripts/build_typst.py --ep int18
    python scripts/prepare_voice.py --ep int18 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int18/scene.py INT18
    python scripts/finalize.py --ep int18

One method per narration beat (int18/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Transform, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, check, clipped, cross, dashed, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def lop(v):
    """A lopsided positive function on [0, 3]."""
    return .5 + .35 * v * v * math.exp(-.45 * v) + .25 * math.sin(2.2 * v)


class INT18(LessonScene):
    EP = 'int18'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m = self.M('hook', 1.7).move_to([0, 1.3, 0])
        self.play(Write(m), run_time=self.rt(.12))
        self.wait_until(.3, t0)
        hard = VGroup(cross(CORAL, .26), tx('tìm nguyên hàm: dài và dễ sai', 25, CORAL)).arrange(RIGHT, buff=.2) \
            .move_to([0, -.5, 0])
        self.play(FadeIn(hard), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        easy = VGroup(check(GREEN, .28), tx('tính đối xứng: 3 dòng', 25, GREEN, bold=True)).arrange(RIGHT, buff=.2) \
            .next_to(hard, DOWN, buff=.45)
        self.play(FadeIn(easy), run_time=self.rt(.06))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Gập đối xứng', 'x → a + b − x'),
                         ('Cộng hai tích phân', 'Triệt tiêu phần khó'),
                         ('Hàm ẩn', 'Biết f(x) + f(−x), tính tích phân')], t0, fracs=(.12, .4, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 3.3, 1), (0, 2.4, 1), (1, 2, 3), (1, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, lop, 0, 3, CYAN, 4.5)), run_time=self.rt(.06))
        reg = area(a, lop, 0, 3, CYAN, .4)
        self.play(FadeIn(reg), run_time=self.rt(.04))
        self.write_board(self.heading('GẬP ĐỐI XỨNG'), self.M('flip', 1.0), frac=.14)
        self.wait_until(.35, t0)
        self.play(Create(dashed(a.c2p(1.5, 0), a.c2p(1.5, 2.3), color=WHITE)),
                  FadeIn(tx('x = (a + b)/2', 18, SOFT).move_to(a.c2p(1.5, 2.45))), run_time=self.rt(.05))
        mirror = lambda v: lop(3 - v)  # noqa: E731
        self.play(Transform(reg, area(a, mirror, 0, 3, GOLD, .4)), Create(clipped(a, mirror, 0, 3, GOLD, 4.5)),
                  run_time=self.rt(.14))
        self.wait_until(.8, t0)
        self.write_board(tx('Lật miền: diện tích không đổi', 23, GOLD, bold=True), frac=.06)

    def beat_c2(self, T):
        self.worked(self.now(), 'CHỨNG MINH: ĐẶT t = a + b − x', ('proof1', 'proof2'), (.08, .45), (1.3, 1.3),
                    gap=.7)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = badge('BÀI MỞ ĐẦU', GOLD, 20)
        m0 = VGroup(tx('I =', 26, WHITE), self.M('hook', 1.3)).arrange(RIGHT, buff=.2)
        m1, m2 = self.M('c3_s1', 1.3), self.M('c3_s2', 1.25)
        self.centre(tag, m0, m1, m2, top=2.7, gap=.5)
        self.play(FadeIn(tag), FadeIn(m0), run_time=self.rt(.08))
        self.wait_until(.2, t0)
        self.play(Write(m1), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(Write(m2), run_time=self.rt(.14))
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))

    def beat_c3b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('DẤU HIỆU DÙNG PHÉP GẬP', GOLD, 20)
        rows = [VGroup(tx(f'{i + 1}.', 26, col, bold=True), self.M(k, 1.3)).arrange(RIGHT, buff=.3)
                for i, (k, col) in enumerate((('signs1', CYAN), ('signs2', GREEN), ('signs3', PURPLE)))]
        self.centre(head, *rows, top=2.5, gap=.6)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, r in zip((.1, .45, .7), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.06))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-2.2, 2.2, 1), (0, 2.4, 1), (-2, -1, 1, 2), (1, 2))
        self.show_axes(a)
        f = lambda v: lop(v + 1.5) * .9  # noqa: E731
        self.play(Create(clipped(a, f, -1.5, 1.5, CYAN, 4.5)), FadeIn(area(a, f, -1.5, 1.5, CYAN, .35)),
                  run_time=self.rt(.08))
        self.write_board(self.heading('ĐOẠN ĐỐI XỨNG [−a; a]'), frac=.05)
        self.wait_until(.3, t0)
        self.play(Create(clipped(a, lambda v: f(-v), -1.5, 1.5, GOLD, 4.5)),
                  FadeIn(area(a, lambda v: f(-v), -1.5, 1.5, GOLD, .25)), run_time=self.rt(.1))
        self.write_board(tx('f lẻ → 0  ·  f chẵn → gấp đôi nửa đoạn', 22, SOFT), frac=.06)
        self.wait_until(.7, t0)
        m = self.M('sym', 1.1)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'HÀM ẨN: LẤY TÍCH PHÂN HAI VẾ', ('hid1',), (.15,), (1.3,))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('Không cần biết f là hàm gì!', 28, GOLD, bold=True).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.06))

    def beat_c6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'TỔNG QUÁT', ('hid2',), (.1,), (1.35,))
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('chìa khóa cho câu vận dụng cao', 26, SOFT).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('VÍ DỤ 1', GOLD, 20), self.M('e1_task', 1.5)).arrange(RIGHT, buff=.4)
        m = self.M('e1_s1', 1.25)
        self.centre(head, m, top=1.9, gap=.9)
        self.play(FadeIn(head), run_time=self.rt(.08))
        self.wait_until(.42, t0)
        self.play(Write(m), run_time=self.rt(.16))
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 3.4, 1), (0, 2.0, 1), (1, 2, 3), (1,))
        self.show_axes(a)
        f = lambda v: v * math.sin(v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, math.pi, CYAN, 4.5)), FadeIn(area(a, f, 0, math.pi, CYAN, .35)),
                  run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.3), frac=.1)
        self.wait_until(.2, t0)
        g = lambda v: (math.pi - v) * math.sin(v)  # noqa: E731
        self.play(Create(clipped(a, g, 0, math.pi, GOLD, 4.5)), FadeIn(area(a, g, 0, math.pi, GOLD, .25)),
                  run_time=self.rt(.08))
        self.write_board(self.M('e2_s1', 1.2), frac=.1)
        self.wait_until(.55, t0)
        m = self.M('e2_s2', 1.15)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2b(self, T):
        self.worked(self.now(), 'TỔNG QUÁT', ('xsin', 'xsin_ex'), (.05, .5), (1.3, 1.3), gap=.8)

    def beat_e3(self, T):
        self.worked(self.now(), 'VÍ DỤ 3', ('e3_task', 'e3_s1'), (.05, .45), (1.3, 1.3), gap=.8)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_task', 1.5)).arrange(RIGHT, buff=.4)
        m1, m2 = self.M('e4_s1', 1.35), self.M('e4_s2', 1.35)
        self.centre(head, m1, m2, top=2.3, gap=.7)
        self.play(FadeIn(head), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(Write(m1), run_time=self.rt(.12))
        self.wait_until(.7, t0)
        self.play(Write(m2), run_time=self.rt(.12))
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('VÍ DỤ 5', GOLD, 20), self.M('e5_task', 1.4)).arrange(RIGHT, buff=.4)
        m1, m2 = self.M('e5_s1', 1.15), self.M('e5_s2', 1.4)
        self.centre(head, m1, m2, top=2.3, gap=.8)
        self.play(FadeIn(head), run_time=self.rt(.08))
        self.wait_until(.25, t0)
        self.play(Write(m1), run_time=self.rt(.16))
        self.wait_until(.68, t0)
        self.play(Write(m2), run_time=self.rt(.1))
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho f liên tục,', 24, WHITE), self.M('tf_given', 1.2)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.3) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .75))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, True), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        sol2 = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.2), tx('không chẵn', 22, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(sol), FadeIn(sol2), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task = self.M('sa_task', 1.4)
        note = tx('(làm tròn đến hàng phần trăm)', 22, SOFT)
        s1 = self.M('sa_s1', 1.35)
        self.centre(tag, task, note, s1, top=2.6, gap=.45)
        self.play(FadeIn(tag), Write(task), FadeIn(note), run_time=self.rt(.14))
        self.wait_until(.7, t0)
        self.play(Write(s1), run_time=self.rt(.12))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s2 = self.M('sa_s2', 1.6)
        sheet = self.answer_sheet('0,79')
        tip = tx('Mọi số mũ n đều cho π/4', 24, GOLD, bold=True)
        self.centre(s2, sheet, tip, top=1.8, gap=.75)
        self.play(Write(s2), run_time=self.rt(.14))
        self.wait_until(.45, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(FadeIn(tip, shift=UP * .1), run_time=self.rt(.05))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Gập đối xứng', 'sum1', 'Thay x bởi a + b − x'),
                                ('Cộng hai tích phân', 'sum2', 'Tử khớp mẫu hoặc khử x'),
                                ('Hàm ẩn', 'sum3', 'Tích phân hai vế, giải theo I')),
                           fracs=(.04, .33, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Cho', 'hw2'), ('Cho', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.2)])


class INT18_SMOKE(INT18):
    smoke = True
