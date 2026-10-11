"""INT17 – Tích phân từng phần.

    python scripts/build_typst.py --ep int17
    python scripts/prepare_voice.py --ep int17 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int17/scene.py INT17
    python scripts/finalize.py --ep int17

One method per narration beat (int17/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Polygon, Transform, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, card, check, clipped, cross, dashed, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, DIM, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

U1, U2 = .6, 1.8


def curve(w):
    return .6 + .8 * w * w


class INT17(LessonScene):
    EP = 'int17'

    def parts_example(self, t0, tag, task, s1, s2, fracs, s2_scale=1.4):
        """Centred example: task, choice of u / dv, the parts formula applied."""
        self.clear_stage(.05)
        head = VGroup(badge(tag, GOLD, 20), self.M(task, 1.5)).arrange(RIGHT, buff=.4)
        m1, m2 = self.M(s1, 1.35), self.M(s2, s2_scale)
        self.centre(head, m1, m2, top=2.5, gap=.7)
        self.play(FadeIn(head[0]), Write(head[1]), run_time=self.rt(.1))
        for frac, m in zip(fracs, (m1, m2)):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.14))
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))
        return m2

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m = self.M('hook', 1.8).move_to([0, 1.5, 0])
        self.play(Write(m), run_time=self.rt(.1))
        self.wait_until(.18, t0)
        tries = VGroup(VGroup(cross(CORAL, .26), tx('bảng nguyên hàm', 24, CORAL)).arrange(RIGHT, buff=.2),
                       VGroup(cross(CORAL, .26), tx('đổi biến số', 24, CORAL)).arrange(RIGHT, buff=.2)) \
            .arrange(RIGHT, buff=1.2).move_to([0, -.1, 0])
        self.play(FadeIn(tries[0]), run_time=self.rt(.05))
        self.wait_until(.36, t0)
        self.play(FadeIn(tries[1]), run_time=self.rt(.05))
        self.wait_until(.58, t0)
        self.play(Transform(m, self.M('hook_ans', 1.8).move_to(m)), run_time=self.rt(.08))
        self.wait_until(.78, t0)
        self.play(FadeIn(tx('→ TÍCH PHÂN TỪNG PHẦN', 30, GOLD, bold=True).move_to([0, -1.7, 0]), shift=UP * .1),
                  run_time=self.rt(.06))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Công thức', 'Và ý nghĩa hình học'),
                         ('Chọn u', 'Nhất log, nhì đa, tam lượng, tứ mũ'),
                         ('Từng phần nhiều lần', 'Đa thức bậc cao, mũ nhân lượng giác')], t0, fracs=(.12, .35, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'TỪ ĐẠO HÀM CỦA TÍCH', ('prod', 'parts'), (.05, .45), (1.6, 1.6), gap=.8)
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('u: lấy đạo hàm   ·   dv: lấy nguyên hàm', 25, SOFT).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 2.2, 1), (0, 3.6, 1), 5.6, 5.3, center=[LEFT_CX, -.1, 0], x_label='u', y_label='v')
        self.show_axes(a)
        self.play(Create(clipped(a, curve, U1, U2, CYAN, 4.5)), run_time=self.rt(.06))
        v1, v2 = curve(U1), curve(U2)
        pts = [a.c2p(U1 + (U2 - U1) * k / 60, curve(U1 + (U2 - U1) * k / 60)) for k in range(61)]
        left = Polygon(a.c2p(0, v1), *pts, a.c2p(0, v2), stroke_width=0, fill_color=GOLD, fill_opacity=.45)
        under = area(a, curve, U1, U2, GREEN, .45)
        small = Polygon(a.c2p(0, 0), a.c2p(U1, 0), a.c2p(U1, v1), a.c2p(0, v1), stroke_width=0, fill_color=DIM,
                        fill_opacity=.6)
        self.write_board(self.heading('HÌNH CHỮ NHẬT uv TÁCH LÀM HAI'), frac=.05)
        self.wait_until(.25, t0)
        self.play(FadeIn(left), FadeIn(tx('∫u dv', 22, GOLD, bold=True).move_to(a.c2p(.65, 2.3))), run_time=self.rt(.07))
        self.wait_until(.45, t0)
        self.play(FadeIn(under), FadeIn(tx('∫v du', 22, GREEN, bold=True).move_to(a.c2p(1.25, .6))),
                  run_time=self.rt(.07))
        self.wait_until(.65, t0)
        frame = VGroup(dashed(a.c2p(0, v2), a.c2p(U2, v2), color=WHITE), dashed(a.c2p(U2, 0), a.c2p(U2, v2), color=WHITE),
                       dashed(a.c2p(U1, 0), a.c2p(U1, v1), color=SOFT), dashed(a.c2p(0, v1), a.c2p(U1, v1), color=SOFT))
        self.play(FadeIn(small), Create(frame), run_time=self.rt(.07))
        self.write_board(self.M('geo', 1.1), tx('hình chữ nhật lớn trừ hình chữ nhật nhỏ', 21, SOFT), frac=.1)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('THỨ TỰ ƯU TIÊN CHỌN u', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        items = (('Nhất', 'log', 'ln x', CYAN), ('Nhì', 'đa', 'đa thức', GREEN), ('Tam', 'lượng', 'sin, cos', PURPLE),
                 ('Tứ', 'mũ', 'eˣ, aˣ', GOLD))
        for i, (rank, key, ex, col) in enumerate(items):
            c = card(3.0, 3.0, col).move_to([-4.65 + 3.1 * i, -.1, 0])
            g = VGroup(c, tx(rank, 22, SOFT).move_to(c.get_top() + DOWN * .5),
                       tx(key, 40, col, bold=True).move_to(c.get_center() + UP * .05),
                       tx(ex, 21, WHITE).move_to(c.get_bottom() + UP * .55))
            self.wait_until((.25, .35, .45, .55)[i], t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))
        self.wait_until(.85, t0)
        self.play(FadeIn(tx('u: hàm đứng trước  ·  dv: phần còn lại', 25, WHITE, bold=True).move_to([0, -2.45, 0])),
                  run_time=self.rt(.05))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        rows = VGroup(
            VGroup(tx('u', 34, CYAN, bold=True, slant=True), tx('lấy đạo hàm  →  phải đơn giản hơn', 27, WHITE)),
            VGroup(tx('', 20), tx('ln x → 1/x    ·    x² → 2x → 2', 25, SOFT)),
            VGroup(tx('dv', 34, GOLD, bold=True, slant=True), tx('lấy nguyên hàm  →  phải dễ tìm v', 27, WHITE)),
            VGroup(tx('', 20), tx('eˣ → eˣ    ·    cos x → sin x', 25, SOFT)))
        for r in rows:
            r.arrange(RIGHT, buff=.4)
        rows.arrange(DOWN, buff=.45, aligned_edge=LEFT).move_to([0, .2, 0])
        for k, frac in zip(range(4), (.03, .2, .5, .68)):
            self.wait_until(frac, t0)
            self.play(FadeIn(rows[k], shift=RIGHT * .2), run_time=self.rt(.06))

    def beat_c5(self, T):
        self.parts_example(self.now(), 'BÀI MỞ ĐẦU', 'hook', 'c5_s1', 'c5_s2', (.04, .45), s2_scale=1.2)

    def beat_c6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CHỌN NGƯỢC: u = eˣ', ('c6_s1', 'c6_s2'), (.05, .38), (1.5, 1.4), box_last=False,
                            gap=.6)
        self.wait_until(.75, t0)
        self.play(FadeIn(VGroup(cross(CORAL, .28), tx('x² còn khó hơn x: sai thứ tự!', 26, CORAL, bold=True))
                         .arrange(RIGHT, buff=.25).next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.06))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('TỪNG PHẦN HAY ĐỔI BIẾN?', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        cols = []
        for i, (title, sign, ex, col) in enumerate((
                ('ĐỔI BIẾN', 'hàm hợp + đạo hàm phần trong', 'x · e^(x²)', CYAN),
                ('TỪNG PHẦN', 'tích hai loại hàm khác nhau', 'x · eˣ   ·   x cos x   ·   x ln x', GOLD))):
            c = card(5.9, 3.6, col).move_to([-3.1 + 6.2 * i, -.2, 0])
            g = VGroup(c, tx(title, 28, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(sign, 23, WHITE).move_to(c.get_center() + UP * .05),
                       tx(ex, 24, SOFT, max_w=5.4).move_to(c.get_bottom() + UP * .75))
            cols.append(g)
        self.wait_until(.12, t0)
        self.play(FadeIn(cols[0], shift=UP * .2), run_time=self.rt(.07))
        self.wait_until(.32, t0)
        self.play(FadeIn(cols[1], shift=UP * .2), run_time=self.rt(.07))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.parts_example(self.now(), 'VÍ DỤ 1', 'e1_task', 'e1_s1', 'e1_s2', (.15, .55))

    def beat_e2(self, T):
        self.parts_example(self.now(), 'VÍ DỤ 2', 'e2_task', 'e2_s1', 'e2_s2', (.12, .45), s2_scale=1.3)

    def beat_e3(self, T):
        self.parts_example(self.now(), 'VÍ DỤ 3', 'e3_task', 'e3_s1', 'e3_s2', (.12, .5), s2_scale=1.3)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('VÍ DỤ 4', GOLD, 20), self.M('e4_task', 1.5)).arrange(RIGHT, buff=.4)
        steps = VGroup(tx('Lần 1: u = x², dv = eˣdx', 24, CYAN), tx('Lần 2: chính là bài mở đầu = 1', 24, PURPLE))
        m = self.M('e4_s1', 1.3)
        self.centre(head, steps[0], m, steps[1], top=2.5, gap=.6)
        self.play(FadeIn(head[0]), Write(head[1]), run_time=self.rt(.08))
        self.wait_until(.1, t0)
        self.play(FadeIn(steps[0]), run_time=self.rt(.05))
        self.play(Write(m), run_time=self.rt(.14))
        self.wait_until(.55, t0)
        self.play(FadeIn(steps[1]), run_time=self.rt(.05))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(badge('SƠ ĐỒ ĐƯỜNG CHÉO', GOLD, 20).move_to([0, 2.72, 0])), run_time=self.rt(.04))
        left = ('x²', '2x', '2', '0')
        right = ('eˣ', 'eˣ', 'eˣ', 'eˣ')
        ys = [1.35 - .68 * k for k in range(4)]
        heads = VGroup(tx('đạo hàm', 22, CYAN, bold=True).move_to([-2.6, 1.95, 0]),
                       tx('nguyên hàm', 22, GOLD, bold=True).move_to([1.0, 1.95, 0]))
        col_l = VGroup(*[tx(v, 30, CYAN).move_to([-2.6, y, 0]) for v, y in zip(left, ys)])
        col_r = VGroup(*[tx(v, 30, GOLD).move_to([1.0, y, 0]) for v, y in zip(right, ys)])
        self.wait_until(.12, t0)
        self.play(FadeIn(heads), FadeIn(col_l), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        self.play(FadeIn(col_r), run_time=self.rt(.06))
        from manim import Arrow
        arrows = VGroup()
        for k, sign in enumerate('+−+'):
            ar = Arrow([-2.2, ys[k], 0], [.6, ys[k + 1], 0], buff=.1, color=(GREEN, CORAL, GREEN)[k], stroke_width=4)
            arrows.add(ar, tx(sign, 30, (GREEN, CORAL, GREEN)[k], bold=True).move_to(ar.get_center() + UP * .3))
        self.wait_until(.42, t0)
        self.play(Create(arrows), run_time=self.rt(.12))
        self.wait_until(.62, t0)
        res = VGroup(self.M('diag', 1.2), self.M('diag_val', 1.2)).arrange(DOWN, buff=.25).move_to([0, -2.15, 0])
        self.play(Write(res[0]), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(Write(res[1]), run_time=self.rt(.08))

    def beat_e5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'DẠNG QUAY VÒNG: eˣ · sin x', ('e5_s1', 'e5_s2'), (.3, .72), (1.45, 1.6), gap=.6)
        self.wait_until(.05, t0)
        self.play(FadeIn(tx('từng phần 2 lần  →  I xuất hiện lại ở vế phải', 24, SOFT)
                         .next_to(lines[0], DOWN, buff=1.6)), run_time=self.rt(.05))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (VGroup(tx('Nên đặt', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.3), self.M('tf_c', 1.35), self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.35, .7))

    def beat_x2(self, T):
        t0 = self.now()
        note = tx('a) Đa thức đứng trước hàm mũ: u = 2x + 1', 22, CORAL, bold=True) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.tf_pause), FadeIn(note), self.tf_mark(0, False), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))
        self.x2_note = note

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c, d)', 22, SOFT), self.M('tf_c_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_note), FadeIn(sol), self.tf_mark(2, True), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(3, False), run_time=self.rt(.08))
        self.wait_until(.82, t0)
        self.play(FadeIn(self.tf_key('SĐĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task = VGroup(self.M('sa_task', 1.5), tx('(làm tròn đến hàng phần trăm)', 22, SOFT)).arrange(RIGHT, buff=.3)
        s1 = self.M('sa_s1', 1.4)
        warn = tx('Chú ý dấu trừ: nguyên hàm của e^(−x) là −e^(−x)', 23, CORAL, bold=True)
        self.centre(tag, task, s1, warn, top=2.5, gap=.6)
        self.play(FadeIn(tag), Write(task), run_time=self.rt(.14))
        self.wait_until(.55, t0)
        self.play(Write(s1), run_time=self.rt(.12))
        self.wait_until(.85, t0)
        self.play(FadeIn(warn), run_time=self.rt(.05))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s2 = self.M('sa_s2', 1.15)
        sheet = self.answer_sheet('0,26')
        self.centre(s2, sheet, top=1.6, gap=.9)
        self.play(Write(s2), run_time=self.rt(.25))
        self.wait_until(.72, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Công thức', 'sum1', 'u lấy đạo hàm, dv lấy nguyên hàm'),
                                ('Chọn u', 'sum2', 'Nhất log, nhì đa, tam lượng, tứ mũ'),
                                ('Nhiều lần', 'sum3', 'Mũ nhân lượng giác: giải theo I')),
                           fracs=(.04, .35, .65))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính', 'hw1'), ('Tính', 'hw2'), ('Tính', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.25), self.M('next2', 1.2)])


class INT17_SMOKE(INT17):
    smoke = True
