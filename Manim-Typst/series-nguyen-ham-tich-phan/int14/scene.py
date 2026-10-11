"""INT14 – Tích phân chứa trị tuyệt đối & hàm từng khúc.

    python scripts/build_typst.py --ep int14
    python scripts/prepare_voice.py --ep int14 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int14/scene.py INT14
    python scripts/finalize.py --ep int14

One method per narration beat (int14/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Transform, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, check, clipped, cross, dashed, dot, signed_area, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def quad(v):
    return v * v - 3 * v + 2


class INT14(LessonScene):
    EP = 'int14'

    def ax(self, xr, yr, xt, yt, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def quad_axes(self):
        a = self.ax((0, 3.3, 1), (-.8, 2.4, 1), (1, 2, 3), (1, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, quad, 0, 3.15, CYAN, 4.5)), run_time=self.rt(.06))
        return a

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m, wrong, right = self.M('hook', 1.55), self.M('hook_wrong', 1.3), self.M('hook_right', 1.3)
        why = tx('Vì sao lệch nhau?', 30, GOLD, bold=True)
        self.centre(m, wrong, right, why, top=2.75, gap=.38)
        self.play(Write(m), run_time=self.rt(.12))
        self.wait_until(.2, t0)
        self.play(Write(wrong), run_time=self.rt(.12))
        self.wait_until(.6, t0)
        self.play(Write(right), run_time=self.rt(.1))
        self.play(FadeIn(why, shift=UP * .1), run_time=self.rt(.06))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Lật phần âm', 'Ý nghĩa hình học của trị tuyệt đối'),
                         ('Ba bước', 'Tìm nghiệm, xét dấu, tách cận'),
                         ('Hàm từng khúc', 'Cắt tại điểm nối, hàm max – min')], t0, fracs=(.12, .4, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.quad_axes()
        parts = signed_area(a, quad, 0, 3, opacity=.5)
        self.play(FadeIn(parts), run_time=self.rt(.06))
        self.write_board(self.heading('DIỆN TÍCH CÓ DẤU'), self.M('f_def', 1.2), self.M('signed', 1.15), frac=.14)
        self.wait_until(.25, t0)
        neg = [p for p in parts if p.get_center()[1] < a.c2p(0, 0)[1]]
        self.play(*[p.animate.set_fill(opacity=.9) for p in neg], run_time=self.rt(.05))
        self.play(*[p.animate.set_fill(opacity=.5) for p in neg], run_time=self.rt(.05))
        self.wait_until(.62, t0)
        up = area(a, lambda v: -quad(v), 1, 2, GREEN, .5)
        flip = clipped(a, lambda v: -quad(v), 1, 2, GOLD, 4.5)
        self.play(*[Transform(p, up) for p in neg[:1]], *[FadeOut(p) for p in neg[1:]], Create(flip),
                  run_time=self.rt(.1))
        self.write_board(self.heading('LẬT PHẦN ÂM LÊN', GREEN), self.M('flipped', 1.15), frac=.12)

    def beat_c2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'TỔNG DIỆN TÍCH HÌNH HỌC', ('ineq',), (.12,), (1.7,), box_last=False)
        self.play(FadeIn(self.box(lines[0], GREEN)), run_time=self.rt(.04))
        self.wait_until(.65, t0)
        self.play(FadeIn(tx('Dấu “=” khi và chỉ khi f không đổi dấu trên [a; b]', 26, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.9)), run_time=self.rt(.07))

    def beat_c3(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'BỎ DẤU TRỊ TUYỆT ĐỐI', ('absdef',), (.1,), (1.6,), box_last=False)
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('→ phải biết DẤU của f trên từng đoạn', 28, CORAL, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.07))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Bước 1: f(x) = 0', 'Giữ nghiệm thuộc đoạn [a; b]'),
                         ('Bước 2: xét dấu', 'Lập bảng dấu của f'),
                         ('Bước 3: tách cận', 'Đoạn âm thì đổi dấu')], t0, fracs=(.05, .33, .5))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        tag = badge('ÁP DỤNG BÀI MỞ ĐẦU', GOLD, 20)
        roots = self.M('roots', 1.45)
        table = self.sign_table(['0', '1', '2', '3'], ['+', '−', '+'], label='f(x)', width=7.4)
        self.centre(tag, roots, table, top=2.6, gap=.6)
        self.play(FadeIn(tag), Write(roots), run_time=self.rt(.14))
        self.wait_until(.55, t0)
        self.play(FadeIn(table[:4]), run_time=self.rt(.06))
        self.play(FadeIn(table[4]), FadeIn(table[5], scale=1.3), run_time=self.rt(.1))

    def beat_c5b(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'KHI NÀO ĐƯỢC ĐƯA TRỊ TUYỆT ĐỐI RA NGOÀI?', ('out_ok', 'out_no'), (.25, .68),
                            (1.35, 1.35), box_last=False, gap=.9)
        self.play(FadeIn(self.box(lines[0], GREEN)), run_time=self.rt(.03))
        self.wait_until(.22, t0)
        self.play(FadeIn(tx('f không đổi dấu trên [a; b]  →  được phép', 25, GREEN, bold=True)
                         .next_to(lines[0], UP, buff=.25)), run_time=self.rt(.05))

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-1.3, 2.4, 1), (0, 2.5, 1), (-1, 1, 2), (1, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, abs, -1.3, 2.3, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(self.heading('HAI TAM GIÁC'), frac=.04)
        self.wait_until(.3, t0)
        left, right = area(a, abs, -1, 0, GREEN, .5), area(a, abs, 0, 2, GOLD, .45)
        self.play(FadeIn(left), FadeIn(tx('1/2', 22, GREEN, bold=True).move_to(a.c2p(-.62, .32))),
                  run_time=self.rt(.07))
        self.wait_until(.52, t0)
        self.play(FadeIn(right), FadeIn(tx('2', 24, GOLD, bold=True).move_to(a.c2p(1.35, .45))),
                  run_time=self.rt(.07))
        self.wait_until(.75, t0)
        m = self.M('absx', 1.4)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 2.3, 1), (0, 4.4, 1), (1, 2), (1, 2, 3, 4))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v, 0, 2.2, CYAN, 3)), Create(clipped(a, lambda v: v * v, 0, 2.1, PURPLE, 3)),
                  run_time=self.rt(.06))
        self.write_board(self.heading('HÀM TỪNG KHÚC'), self.M('piece', 1.0), frac=.12)
        self.wait_until(.55, t0)
        self.play(Create(clipped(a, lambda v: max(v, v * v), 0, 2.05, GOLD, 6)),
                  Create(dashed(a.c2p(1, 0), a.c2p(1, 1), color=WHITE, stroke_width=2)), run_time=self.rt(.08))
        self.write_board(self.heading('HÀM MAX – MIN'), self.M('maxmin', 1.15), frac=.12)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = badge('VÍ DỤ 1', GOLD, 20)
        table = self.sign_table(['0', '1', '2', '3'], ['+', '−', '+'], width=6.4)
        s1, s2 = self.M('e1_s1', 1.25), self.M('e1_s2', 1.5)
        self.centre(tag, table, s1, s2, top=2.7, gap=.45)
        self.play(FadeIn(tag), FadeIn(table), run_time=self.rt(.06))
        self.play(Write(s1), run_time=self.rt(.14))
        self.wait_until(.5, t0)
        self.play(Write(s2), run_time=self.rt(.12))
        self.play(FadeIn(self.box(s2, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 3.5, 1), (-1.3, 1.4, 1), (), (-1, 1))
        self.show_axes(a)
        for v, s in ((math.pi / 2, 'π/2'), (math.pi, 'π')):
            self.add(tx(s, 18, SOFT).move_to(a.c2p(v, 0) + (UP * .3 + RIGHT * .25 if v > 3 else DOWN * .3 + LEFT * .3)))
        self.play(Create(clipped(a, math.cos, 0, 3.4, CYAN, 4.5)), FadeIn(signed_area(a, math.cos, 0, math.pi)),
                  run_time=self.rt(.07))
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_task', 1.4), frac=.08)
        self.wait_until(.3, t0)
        self.play(FadeIn(area(a, lambda v: -math.cos(v), math.pi / 2, math.pi, GREEN, .5)),
                  Create(clipped(a, lambda v: -math.cos(v), math.pi / 2, math.pi, GOLD, 4)), run_time=self.rt(.08))
        m = self.M('e2_s1', 1.0)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.8, t0)
        self.write_board(VGroup(tx('so với', 22, SOFT), self.M('e2_s2', 1.2)).arrange(RIGHT, buff=.25), frac=.08)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 2.3, 1), (0, 4.4, 1), (1, 2), (1, 2, 3, 4))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v, 0, 2.2, CYAN, 3)), Create(clipped(a, lambda v: v * v, 0, 2.1, PURPLE, 3)),
                  run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), self.M('e3_task', 1.4), frac=.08)
        self.wait_until(.22, t0)
        self.play(FadeIn(area(a, lambda v: v, 0, 1, CYAN, .45)),
                  FadeIn(tx('y = x', 20, CYAN, bold=True).move_to(a.c2p(.45, 1.15))), run_time=self.rt(.06))
        self.wait_until(.42, t0)
        self.play(FadeIn(area(a, lambda v: v * v, 1, 2, PURPLE, .45)),
                  FadeIn(tx('y = x²', 20, PURPLE, bold=True).move_to(a.c2p(1.25, 3.6))),
                  Create(dashed(a.c2p(1, 0), a.c2p(1, 1), color=WHITE, stroke_width=2)), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        m = self.M('e3_s1', 1.0)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def piece_axes(self):
        a = self.ax((0, 2.3, 1), (0, 5.6, 1), (1, 2), (1, 2, 3, 4, 5))
        self.show_axes(a)
        return a

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.piece_axes()
        self.write_board(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_f', 1.3), frac=.12)
        self.play(Create(clipped(a, lambda v: 2 * v + 1, 1, 2.2, GOLD, 4.5)), run_time=self.rt(.05))
        self.play(FadeIn(dot(a, 1, 3, GOLD)), FadeIn(tx('(1; 3)', 20, GOLD).move_to(a.c2p(1.45, 2.75))),
                  run_time=self.rt(.04))
        self.wait_until(.45, t0)
        trials = [clipped(a, lambda v, k=k: v * v + k, 0, 1, CORAL, 4) for k in (.5, 1.2)]
        self.play(Create(trials[0]), run_time=self.rt(.05))
        self.play(Transform(trials[0], trials[1]), run_time=self.rt(.05))
        self.wait_until(.68, t0)
        self.play(Transform(trials[0], clipped(a, lambda v: v * v + 2, 0, 1, CYAN, 4.5)), run_time=self.rt(.06))
        m = self.M('e4_s1', 1.35)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.piece_axes()
        self.play(Create(clipped(a, lambda v: v * v + 2, 0, 1, CYAN, 4.5)),
                  Create(clipped(a, lambda v: 2 * v + 1, 1, 2.2, GOLD, 4.5)), run_time=self.rt(.06))
        self.write_board(self.heading('CẮT TẠI ĐIỂM NỐI x = 1'), frac=.04)
        self.wait_until(.18, t0)
        self.play(FadeIn(area(a, lambda v: v * v + 2, 0, 1, CYAN, .45)),
                  Create(dashed(a.c2p(1, 0), a.c2p(1, 3), color=WHITE, stroke_width=2)), run_time=self.rt(.06))
        self.write_board(self.M('e5_s1', 1.0), frac=.12)
        self.wait_until(.5, t0)
        self.play(FadeIn(area(a, lambda v: 2 * v + 1, 1, 2, GOLD, .45)), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        m = self.M('e5_s2', 1.5)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_given', 1.35)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.4), self.M('tf_b', 1.4), self.M('tf_c', 1.4), self.M('tf_d', 1.4))
        self.tf_question(t0, [l1, l2], items, fracs=(.25, .62))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        note = VGroup(cross(CORAL, .26), tx('c) Bẫy: lấy trị tuyệt đối của −3 chỉ được 3', 22, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.2).move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(note), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.35, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', .95)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(note), FadeIn(sol), self.tf_mark(3, True), run_time=self.rt(.1))
        self.wait_until(.88, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task = VGroup(self.M('sa_task', 1.5), tx('(làm tròn đến hàng phần trăm)', 22, SOFT)).arrange(RIGHT, buff=.3)
        s1 = self.M('sa_s1', 1.45)
        table = self.sign_table(['0', 'ln 2', '2'], ['−', '+'], label='eˣ − 2', width=6.0)
        self.centre(tag, task, s1, table, top=2.6, gap=.5)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.14))
        self.wait_until(.5, t0)
        self.play(Write(s1), run_time=self.rt(.1))
        self.wait_until(.72, t0)
        self.play(FadeIn(table), run_time=self.rt(.08))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s2, s3 = self.M('sa_s2', 1.35), self.M('sa_s3', 1.3)
        sheet = self.answer_sheet('3,16')
        tip = VGroup(check(GREEN, .28), tx('Kiểm tra: máy tính bấm được ∫ Abs(eˣ − 2) dx', 22, GREEN)) \
            .arrange(RIGHT, buff=.2)
        self.centre(s2, s3, sheet, tip, top=2.5, gap=.55)
        self.play(Write(s2), run_time=self.rt(.12))
        self.wait_until(.18, t0)
        self.play(Write(s3), run_time=self.rt(.14))
        self.wait_until(.48, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(FadeIn(tip, shift=UP * .1), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Lật phần âm', 'sum3', 'Tích phân trị tuyệt đối = tổng diện tích'),
                                ('Ba bước', 'sum2', 'Tìm nghiệm, xét dấu, tách cận'),
                                ('Từng khúc', 'sum_piece', 'Cắt tại điểm nối hoặc giao điểm')),
                           fracs=(.04, .4, .72))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Tính', 'hw2'), ('Tính', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .33, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [VGroup(tx('Độ dời:', 24, SOFT), self.M('next1', 1.25)).arrange(RIGHT, buff=.3),
                            VGroup(tx('Quãng đường:', 24, GOLD), self.M('next2', 1.25)).arrange(RIGHT, buff=.3)],
                       thanks_at=.62)


class INT14_SMOKE(INT14):
    smoke = True
