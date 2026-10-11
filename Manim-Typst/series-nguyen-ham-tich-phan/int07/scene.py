"""INT07 – Nguyên hàm phân thức hữu tỉ: chia đa thức & tách phân thức (mở rộng).

    python scripts/build_typst.py --ep int07
    python scripts/prepare_voice.py --ep int07 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int07/scene.py INT07
    python scripts/finalize.py --ep int07

One method per narration beat (int07/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, GrowArrow, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, cross, dashed, dot, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT07(LessonScene):
    EP = 'int07'

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        q = self.M('hook', 2.0).move_to([0, 1.7, 0])
        self.play(Write(q), run_time=self.rt(.12))
        self.wait_until(.25, t0)
        miss = VGroup(cross(CORAL, .35), tx('không có trong bảng nguyên hàm', 24, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.25).move_to([0, .3, 0])
        self.play(FadeIn(miss), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        tools = VGroup(badge('① CHIA ĐA THỨC', CYAN, 22), badge('② TÁCH PHÂN THỨC', GREEN, 22)) \
            .arrange(RIGHT, buff=.8).move_to([0, -1.2, 0])
        self.play(FadeIn(tools[0], shift=UP * .15), run_time=self.rt(.06))
        self.play(FadeIn(tools[1], shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.82, t0)
        self.play(FadeIn(tx('→ đưa về các hạng tử quen thuộc trong bảng', 24, GOLD, bold=True).move_to([0, -2.4, 0])),
                  run_time=self.rt(.06))

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        self.title_card()
        self.wait_until(.55, t0)
        tag = badge('NỘI DUNG MỞ RỘNG · HỌC SINH GIỎI / ĐÁNH GIÁ NĂNG LỰC', PURPLE, 19).move_to([0, -2.6, 0])
        self.play(FadeIn(tag, shift=UP * .1), run_time=self.rt(.06))

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Chia đa thức', 'Khi bậc tử ≥ bậc mẫu'),
                         ('Tách phân thức', 'Hệ số bất định · mẹo che nghiệm'),
                         ('Tử là đạo hàm mẫu', 'Ra ngay logarit của mẫu')], t0, fracs=(.12, .32, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('BƯỚC 1: SO SÁNH BẬC CỦA TỬ VÀ MẪU', 24, GOLD, bold=True).move_to([0, 2.6, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        left = VGroup(card(5.6, 2.0, GREEN), tx('bậc tử < bậc mẫu', 26, GREEN, bold=True),
                      tx('phân thức thực sự → tách ngay', 21, SOFT))
        right = VGroup(card(5.6, 2.0, CYAN), tx('bậc tử ≥ bậc mẫu', 26, CYAN, bold=True),
                       tx('chia đa thức trước', 21, SOFT))
        for g, xpos in ((left, -3.2), (right, 3.2)):
            g[0].move_to([xpos, .9, 0])
            g[1].move_to(g[0].get_center() + UP * .35)
            g[2].move_to(g[0].get_center() + DOWN * .35)
        self.wait_until(.12, t0)
        self.play(FadeIn(left, shift=UP * .15), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(right, shift=UP * .15), run_time=self.rt(.08))
        self.wait_until(.65, t0)
        analog = VGroup(tx('Giống đổi phân số sang hỗn số:', 23, SOFT),
                        tx('7/3 = 2 + 1/3', 30, GOLD, bold=True)).arrange(RIGHT, buff=.4).move_to([0, -1.6, 0])
        self.play(FadeIn(analog, shift=UP * .1), run_time=self.rt(.08))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((-2.5, 4.5, 1), (-6, 9, 1), 6.0, 5.55, center=[LEFT_CX, -.12, 0], x_ticks=(-2, 2, 4),
                 y_ticks=(-4, 4, 8))
        self.show_axes(a)
        self.write_board(self.M('div1', 1.35), frac=.12)
        f = lambda v: (v * v + 1) / (v - 1)  # noqa: E731
        branches = VGroup(clipped(a, f, -2.5, .97, CYAN, 4), clipped(a, f, 1.03, 4.5, CYAN, 4))
        va = dashed(a.c2p(1, -6), a.c2p(1, 9), color=CORAL, stroke_width=2)
        self.wait_until(.25, t0)
        self.play(Create(branches), Create(va), run_time=self.rt(.1))
        self.write_board(self.M('div2', 1.35), frac=.1)
        slant = clipped(a, lambda v: v + 1, -2.5, 4.5, GOLD, 3)
        lab = tx('y = x + 1', 19, GOLD, bold=True).move_to(a.c2p(3.3, 2.6))
        self.play(Create(slant), FadeIn(lab), run_time=self.rt(.07))
        self.wait_until(.62, t0)
        res = self.M('div3', 1.0)
        self.write_board(res, frac=.1)
        self.play(FadeIn(self.box(res, GREEN)), run_time=self.rt(.04))

    def beat_c3(self, T):
        self.worked(self.now(), 'TỬ VÀ MẪU CÙNG BẬC MỘT', ('lin1', 'lin2'), (.1, .48), (1.8, 1.25), gap=.7)

    def beat_c4(self, T):
        self.worked(self.now(), 'BƯỚC 2: TÁCH PHÂN THỨC', ('sep1', 'sep_chk', 'sep2'), (.04, .45, .75),
                    (1.4, 1.05, 1.4), gap=.38)

    def beat_c5(self, T):
        self.worked(self.now(), 'HỆ SỐ BẤT ĐỊNH', ('ab1', 'ab2', 'ab3'), (.04, .3, .55), (1.6, 1.6, 1.25),
                    box_last=False, gap=.55)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        res = self.M('ab4', 1.6)
        self.centre(res, top=2.5)
        self.play(Write(res), run_time=self.rt(.12))
        self.play(FadeIn(self.box(res, GREEN)), run_time=self.rt(.04))
        self.wait_until(.38, t0)
        tag = badge('MẸO CHE NGHIỆM', GOLD, 21).move_to([0, .4, 0])
        steps = tx('Che thừa số (x − 1) ở mẫu  →  thay x = 1 vào phần còn lại', 23, WHITE).move_to([0, -.4, 0])
        self.play(FadeIn(tag), FadeIn(steps), run_time=self.rt(.07))
        self.wait_until(.66, t0)
        cov = self.M('cover', 1.7).move_to([0, -1.8, 0])
        self.play(Write(cov), run_time=self.rt(.12))

    def beat_c7(self, T):
        self.worked(self.now(), 'MẪU CÓ NGHIỆM KÉP', ('dbl1', 'dbl2'), (.12, .62), (1.45, 1.6), gap=.8)

    def beat_c8(self, T):
        self.worked(self.now(), 'TỬ SỐ LÀ ĐẠO HÀM CỦA MẪU', ('dlog1', 'dlog2'), (.06, .62), (1.55, 1.7), gap=.8)

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        root = VGroup(card(3.4, .9, GOLD), tx('P(x) / Q(x)', 26, GOLD, bold=True)).move_to([0, 2.3, 0])
        root[1].move_to(root[0])
        self.play(FadeIn(root), run_time=self.rt(.05))
        leaves = (('bậc P ≥ bậc Q', 'chia đa thức', CYAN), ('P = Q′', 'logarit của Q', GREEN),
                  ('Q có nghiệm phân biệt', 'tách A, B', PURPLE), ('Q có nghiệm kép', 'thêm B/(x − a)²', CORAL))
        boxes = VGroup()
        for i, (cond, act, col) in enumerate(leaves):
            c = card(3.0, 1.6, col).move_to([-4.65 + 3.1 * i, -.3, 0])
            boxes.add(VGroup(c, tx(cond, 19, col, bold=True, max_w=2.8).move_to(c.get_center() + UP * .32),
                             tx('→ ' + act, 19, WHITE, max_w=2.8).move_to(c.get_center() + DOWN * .32)))
        for i, (frac, bx) in enumerate(zip((.12, .3, .5, .7), boxes)):
            self.wait_until(frac, t0)
            ar = Arrow(root[0].get_bottom(), bx[0].get_top(), color=SOFT, buff=.08, stroke_width=3)
            self.play(GrowArrow(ar), FadeIn(bx, shift=DOWN * .1), run_time=self.rt(.07))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1_task', 'e1_s1', 'e1_s2'), (.04, .3, .62), (1.7, 1.6, 1.6), gap=.55)

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_task', 'e2_s1', 'e2_s2'), (.04, .3, .75), (1.3, 1.05, 1.6), gap=.55)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('F là một nguyên hàm của f trên (0; +∞). Xét các mệnh đề:', 24, WHITE)
        items = (self.M('tf_a', 1.3), self.M('tf_b', 1.3), self.M('tf_c', 1.3),
                 VGroup(tx('Nếu', 22, WHITE), self.M('tf_d', 1.3)).arrange(RIGHT, buff=.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.36, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, False), run_time=self.rt(.07))
        c = VGroup(tx('c)', 22, GOLD, bold=True), self.M('tf_c_calc', 1.15)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(c), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        d = VGroup(tx('d)', 22, GOLD, bold=True), self.M('tf_d_calc', 1.0)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(c), FadeIn(d), run_time=self.rt(.1))
        self.play(self.tf_mark(3, True), run_time=self.rt(.06))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 4.2, 1), (-1.5, .9, 1), 5.8, 5.4, center=[LEFT_CX, -.12, 0], x_ticks=(1, 2, 3, 4),
                 y_ticks=(-1, .5))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.0), frac=.12)
        self.wait_until(.36, t0)
        self.write_board(self.M('sa_s1', 1.05), frac=.12)
        F = clipped(a, lambda v: math.log(v / (v + 1)) + math.log(2), .12, 4.2, GOLD, 4.5)
        self.play(Create(F), FadeIn(dot(a, 1, 0, CYAN, .09)), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.write_board(self.M('sa_s2', 1.15), frac=.08)
        self.wait_until(.8, t0)
        v2 = math.log(4 / 3)
        self.play(FadeIn(dot(a, 2, v2, GREEN, .09)), Create(dashed(a.c2p(2, 0), a.c2p(2, v2), color=GREEN,
                                                                   stroke_width=2)), run_time=self.rt(.03))
        self.write_board(self.M('sa_s3', 1.2), self.answer_sheet('0,29'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        rule = self.M('cover_rule', 1.4).move_to([0, 1.95, 0])
        self.play(Write(rule), FadeIn(self.box(rule)), run_time=self.rt(.12))
        steps = (('Che', 'Che thừa số (x − a) ở mẫu', CYAN), ('Thay', 'Thay x = a vào phần còn lại', GREEN),
                 ('Lưu ý', 'Chỉ dùng khi các nghiệm phân biệt', CORAL))
        for i, (tag, text, col) in enumerate(steps):
            c = card(11.2, .95, col).move_to([0, .25 - 1.08 * i, 0])
            g = VGroup(c, badge(tag, col, 17).move_to(c.get_left() + RIGHT * .8),
                       tx(text, 23, WHITE).next_to(c.get_left(), RIGHT, buff=1.7))
            self.wait_until((.25, .45, .72)[i], t0)
            self.play(FadeIn(g, shift=UP * .12), run_time=self.rt(.07))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Chia đa thức', 'sum1', 'Khi bậc tử ≥ bậc mẫu'),
                                ('Tách phân thức', 'sum2', 'Hệ số bất định hoặc che nghiệm'),
                                ('Tử là đạo hàm mẫu', 'sum3', 'Ra ngay logarit của mẫu')),
                           fracs=(.04, .3, .64))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Tìm', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.2), self.M('next2', 1.2)])


class INT07_SMOKE(INT07):
    smoke = True
