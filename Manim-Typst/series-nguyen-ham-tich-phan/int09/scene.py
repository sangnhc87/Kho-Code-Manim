"""INT09 – Phương pháp nguyên hàm từng phần (mở rộng).

    python scripts/build_typst.py --ep int09
    python scripts/prepare_voice.py --ep int09 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int09/scene.py INT09
    python scripts/finalize.py --ep int09

One method per narration beat (int09/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, GrowArrow, Indicate, Polygon,
                   VGroup, Write)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, clipped, cross, dashed, dot, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT09(LessonScene):
    EP = 'int09'

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        q = self.M('hook', 2.2).move_to([0, 1.8, 0])
        self.play(Write(q), run_time=self.rt(.1))
        self.wait_until(.2, t0)
        kinds = VGroup(badge('x: đa thức', CYAN, 22), tx('×', 34, WHITE), badge('eˣ: hàm mũ', GOLD, 22)) \
            .arrange(RIGHT, buff=.4).move_to([0, .45, 0])
        self.play(FadeIn(kinds, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.42, t0)
        fails = VGroup(VGroup(cross(CORAL, .3), tx('không tách được như tổng', 22, CORAL)).arrange(RIGHT, buff=.2),
                       VGroup(cross(CORAL, .3), tx('đổi biến bế tắc: không thấy u′', 22, CORAL)).arrange(RIGHT, buff=.2)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=.25).move_to([0, -.9, 0])
        self.play(FadeIn(fails[0]), run_time=self.rt(.06))
        self.play(FadeIn(fails[1]), run_time=self.rt(.06))
        self.wait_until(.78, t0)
        self.play(FadeIn(tx('→ công cụ mới từ đạo hàm của một TÍCH', 25, GOLD, bold=True).move_to([0, -2.4, 0])),
                  run_time=self.rt(.06))

    def beat_h2(self, T):
        t0 = self.now()
        self.clear_stage(.06)
        self.title_card()
        self.wait_until(.55, t0)
        self.play(FadeIn(badge('NỘI DUNG MỞ RỘNG · HỌC SINH GIỎI / ĐÁNH GIÁ NĂNG LỰC', PURPLE, 19)
                         .move_to([0, -2.6, 0]), shift=UP * .1), run_time=self.rt(.06))

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Công thức & hình học', '∫u dv = uv − ∫v du qua diện tích'),
                         ('Chọn u đúng', 'Nhất lô, nhì đa, tam lượng, tứ mũ'),
                         ('Làm nhanh', 'Sơ đồ đường chéo · dạng lặp lại')], t0, fracs=(.12, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('TỪ ĐẠO HÀM CỦA TÍCH', 26, GOLD, bold=True)
        p, r = self.M('prod', 2.0), self.M('parts', 2.2)
        self.centre(head, p, tx('lấy nguyên hàm hai vế, chuyển vế', 22, SOFT), r, top=2.7, gap=.45)
        self.play(FadeIn(head), Write(p), run_time=self.rt(.14))
        self.wait_until(.35, t0)
        self.play(Write(r), run_time=self.rt(.14))
        self.play(FadeIn(self.box(r)), run_time=self.rt(.04))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('đổi nguyên hàm khó  →  nguyên hàm dễ hơn', 24, GREEN, bold=True).move_to([0, -2.75, 0])),
                  run_time=self.rt(.06))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 4.6, 1), (0, 2.5, 1), 6.0, 5.2, center=[LEFT_CX, -.2, 0], x_ticks=(1, 4), y_ticks=(1, 2),
                 x_label='v', y_label='u')
        self.show_axes(a)
        curve = clipped(a, math.sqrt, 1, 4, WHITE, 4)
        self.play(Create(curve), run_time=self.rt(.06))
        vs = np.linspace(1, 4, 40)
        under = Polygon(*[a.c2p(v, 0) for v in (1, 4)], *[a.c2p(v, math.sqrt(v)) for v in vs[::-1]],
                        stroke_width=0, fill_color=CYAN, fill_opacity=.45)
        us = np.linspace(1, 2, 40)
        left = Polygon(a.c2p(0, 1), *[a.c2p(u * u, u) for u in us], a.c2p(0, 2), stroke_width=0, fill_color=GOLD,
                       fill_opacity=.45)
        self.wait_until(.2, t0)
        self.play(FadeIn(under), FadeIn(tx('∫u dv', 22, CYAN, bold=True).move_to(a.c2p(2.6, .55))),
                  run_time=self.rt(.08))
        self.wait_until(.42, t0)
        self.play(FadeIn(left), FadeIn(tx('∫v du', 22, GOLD, bold=True).move_to(a.c2p(1.2, 1.55))),
                  run_time=self.rt(.08))
        self.wait_until(.62, t0)
        big = VGroup(dashed(a.c2p(4, 0), a.c2p(4, 2), color=SOFT), dashed(a.c2p(0, 2), a.c2p(4, 2), color=SOFT))
        small = VGroup(dashed(a.c2p(1, 0), a.c2p(1, 1), color=CORAL), dashed(a.c2p(0, 1), a.c2p(1, 1), color=CORAL))
        self.play(Create(big), Create(small), FadeIn(dot(a, 1, 1, CORAL)), FadeIn(dot(a, 4, 2, GOLD)),
                  run_time=self.rt(.07))
        self.write_board(tx('Diện tích xanh + vàng', 23, WHITE), tx('= hình chữ nhật lớn − hình nhỏ', 23, WHITE),
                         self.M('area', 1.15), frac=.12)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('CHỌN u THEO THỨ TỰ ƯU TIÊN', 26, GOLD, bold=True).move_to([0, 2.5, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        items = (('NHẤT', 'lô', 'ln x', CYAN), ('NHÌ', 'đa', 'xⁿ', GREEN), ('TAM', 'lượng', 'sin, cos', GOLD),
                 ('TỨ', 'mũ', 'eˣ, aˣ', PURPLE))
        for i, (rank, name, ex, col) in enumerate(items):
            c = card(2.8, 2.6, col).move_to([-4.5 + 3.0 * i, .4, 0])
            g = VGroup(c, tx(rank, 22, col, bold=True).move_to(c.get_top() + DOWN * .4),
                       tx(name, 36, WHITE, bold=True).move_to(c.get_center()),
                       tx(ex, 21, SOFT).move_to(c.get_bottom() + UP * .45))
            self.wait_until((.18, .3, .4, .5)[i], t0)
            self.play(FadeIn(g, shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('Hàm đứng trước → u;  phần còn lại → dv', 24, GOLD, bold=True).move_to([0, -1.9, 0])),
                  run_time=self.rt(.06))

    def beat_c4(self, T):
        self.worked(self.now(), 'ÁP DỤNG: x·eˣ', ('pick1', 'pick2'), (.1, .45), (1.4, 1.3), gap=.8)

    def beat_c5(self, T):
        lines = self.worked(self.now(), 'NẾU CHỌN NGƯỢC', ('bad1', 'bad2'), (.05, .3), (1.5, 1.4), box_last=False,
                            gap=.7)
        warn = tx('→ còn khó hơn bài ban đầu!', 26, CORAL, bold=True).next_to(lines[-1], DOWN, buff=.6)
        self.play(FadeIn(warn), run_time=self.rt(.06))

    def beat_c6(self, T):
        self.worked(self.now(), 'NGUYÊN HÀM CỦA ln x', ('ln1', 'ln2'), (.15, .55), (1.4, 1.4), gap=.8)

    def beat_c7(self, T):
        self.worked(self.now(), 'NGUYÊN HÀM CỦA x·cos x', ('cos1', 'cos2'), (.1, .45), (1.5, 1.25), gap=.8)

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('SƠ ĐỒ ĐƯỜNG CHÉO: ∫x²eˣ dx', GOLD, 21).move_to([0, 2.6, 0])
        h1 = tx('ĐẠO HÀM (u)', 21, CYAN, bold=True).move_to([-2.4, 1.85, 0])
        h2 = tx('NGUYÊN HÀM (dv)', 21, GOLD, bold=True).move_to([2.4, 1.85, 0])
        self.play(FadeIn(head), FadeIn(h1), FadeIn(h2), run_time=self.rt(.06))
        left = ['x²', '2x', '2', '0']
        ys = [1.1, .25, -.6, -1.45]
        cells_l = VGroup(*[tx(s, 32, CYAN, bold=True).move_to([-2.4, y, 0]) for s, y in zip(left, ys)])
        cells_r = VGroup(*[tx('eˣ', 32, GOLD, bold=True).move_to([2.4, y, 0]) for y in ys])
        self.wait_until(.2, t0)
        self.play(LaggedIn(cells_l), run_time=self.rt(.12))
        self.play(LaggedIn(cells_r), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        for i, sign in enumerate('+−+'):
            ar = Arrow(cells_l[i].get_right(), cells_r[i + 1].get_left(), color=WHITE, buff=.15, stroke_width=4)
            lab = tx(sign, 30, GREEN if sign == '+' else CORAL, bold=True).next_to(ar.get_center(), UP, buff=.12)
            self.play(GrowArrow(ar), FadeIn(lab), run_time=self.rt(.06))

    def beat_c9(self, T):
        t0 = self.now()
        res = self.M('tab_res', 1.3).move_to([0, -2.6, 0])
        self.play(Write(res), run_time=self.rt(.2))
        self.play(FadeIn(self.box(res, GREEN)), run_time=self.rt(.04))
        self.wait_until(.55, t0)
        note = tx('Bậc n  →  n đường chéo', 22, GOLD, bold=True).move_to([4.9, 1.1, 0])
        self.play(FadeIn(note, shift=LEFT * .1), run_time=self.rt(.06))

    def beat_c10(self, T):
        self.worked(self.now(), 'DẠNG LẶP LẠI: I QUAY VỀ CHÍNH NÓ', ('loop1', 'loop2'), (.15, .7), (1.5, 1.8), gap=.8)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1_s1', 'e1_s2'), (.15, .5), (1.5, 1.6), gap=.8)

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_s1', 'e2_s2'), (.1, .45), (1.5, 1.6), gap=.8)

    def beat_e3(self, T):
        self.worked(self.now(), 'VÍ DỤ 3: SƠ ĐỒ ĐƯỜNG CHÉO', ('e3_tab', 'e3_res'), (.1, .55), (1.3, 1.25), gap=.9)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.4)).arrange(RIGHT, buff=.25)
        l2 = tx('F là một nguyên hàm của f trên ℝ. Xét các mệnh đề:', 24, WHITE)
        items = (VGroup(tx('Đặt', 22, WHITE), self.M('tf_a', 1.25)).arrange(RIGHT, buff=.2), self.M('tf_b', 1.3),
                 self.M('tf_c', 1.3), VGroup(tx('Nếu', 22, WHITE), self.M('tf_d', 1.3)).arrange(RIGHT, buff=.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.08))
        sol = VGroup(tx('b) thử lại:', 22, SOFT), self.M('tf_b_calc', 1.25)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_sol), self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.05)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol[0]), Write(sol[1]), run_time=self.rt(.14))
        self.play(self.tf_mark(3, False), run_time=self.rt(.06))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 3.2, 1), (-.2, 1.6, 1), 5.8, 5.4, center=[LEFT_CX, -.12, 0], x_ticks=(1, 2, 3),
                 y_ticks=(.5, 1, 1.5))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.05), frac=.12)
        self.wait_until(.42, t0)
        self.write_board(self.M('sa_s1', 1.0), frac=.12)
        self.play(Create(clipped(a, lambda v: v * math.log(v) - v + 1, .05, 3.2, GOLD, 4.5)),
                  FadeIn(dot(a, 1, 0, CYAN, .09)), run_time=self.rt(.08))
        self.wait_until(.8, t0)
        v2 = 2 * math.log(2) - 1
        self.play(FadeIn(dot(a, 2, v2, GREEN, .09)),
                  Create(dashed(a.c2p(2, 0), a.c2p(2, v2), color=GREEN, stroke_width=2)), run_time=self.rt(.03))
        self.write_board(self.M('sa_s2', 1.3), self.answer_sheet('0,39'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('MẸO KIỂM TRA', GOLD, 21).move_to([0, 2.5, 0])
        m = self.M('chk', 1.8).move_to([0, 1.1, 0])
        self.play(FadeIn(head), Write(m), run_time=self.rt(.14))
        self.wait_until(.45, t0)
        warn = tx('Lỗi hay gặp nhất: dấu trừ trước ∫v du', 26, CORAL, bold=True).move_to([0, -1.0, 0])
        self.play(FadeIn(warn, shift=UP * .1), Indicate(m, color=GOLD, scale_factor=1.03), run_time=self.rt(.08))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Công thức', 'sum1', 'Đổi nguyên hàm khó thành dễ'),
                                ('Chọn u', 'sum2', 'Nhất lô, nhì đa, tam lượng, tứ mũ'),
                                ('Dạng lặp lại', 'sum3', 'Giải phương trình theo I')),
                           fracs=(.04, .32, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Tìm', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .3, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.3)])


def LaggedIn(group):
    from manim import LaggedStart
    return LaggedStart(*[FadeIn(m, shift=UP * .1) for m in group], lag_ratio=.3)


class INT09_SMOKE(INT09):
    smoke = True
