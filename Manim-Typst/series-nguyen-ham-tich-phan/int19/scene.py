"""INT19 – Hàm ẩn từ phương trình vi phân đơn giản.

    python scripts/build_typst.py --ep int19
    python scripts/prepare_voice.py --ep int19 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int19/scene.py INT19
    python scripts/finalize.py --ep int19

One method per narration beat (int19/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, check, clipped, cross, dot, slope_field, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT19(LessonScene):
    EP = 'int19'

    def field_axes(self):
        a = axes((-2.2, 2.2, 1), (0, 4.4, 1), 6.0, 5.3, center=[LEFT_CX, -.1, 0], x_ticks=(-2, -1, 1, 2),
                 y_ticks=(1, 2, 3, 4))
        self.show_axes(a)
        xs = [-2 + .4 * i for i in range(11)]
        ys = [.3 + .4 * j for j in range(11)]
        field = slope_field(a, lambda xv, yv: xv * yv, xs, ys, seg=.32)
        self.play(Create(field), run_time=self.rt(.1))
        return a

    def task_screen(self, t0, tag, keys, fracs, scales, box_last=True, gap=.6, top=2.4):
        """Centred example: badge + task on one row, then the steps."""
        self.clear_stage(.05)
        head = VGroup(badge(tag, GOLD, 20), self.M(keys[0], scales[0])).arrange(RIGHT, buff=.4)
        lines = [self.M(k, s) for k, s in zip(keys[1:], scales[1:])]
        self.centre(head, *lines, top=top, gap=gap)
        self.play(FadeIn(head), run_time=self.rt(.08))
        for frac, m in zip(fracs, lines):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.12))
        if box_last:
            self.play(FadeIn(self.box(lines[-1], GREEN)), run_time=self.rt(.03))
        return lines

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m = self.M('hook', 1.5).move_to([0, 1.4, 0])
        self.play(Write(m), run_time=self.rt(.12))
        self.wait_until(.35, t0)
        self.play(FadeIn(tx("không có công thức của f — chỉ có hệ thức giữa f' và f", 25, SOFT).move_to([0, 0, 0])),
                  run_time=self.rt(.06))
        self.wait_until(.72, t0)
        ans = self.M('hook_ans', 1.9).move_to([0, -1.5, 0])
        self.play(Write(ans), run_time=self.rt(.1))
        self.play(FadeIn(self.box(ans, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Trường hướng', 'Điều kiện ban đầu chọn một đường'),
                         ('Tách biến', 'Mọi thứ chứa f về một vế'),
                         ('Bốn dạng', 'ln f, 1/f, f², tích x·f')], t0, fracs=(.12, .4, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.field_axes()
        self.write_board(self.heading('TRƯỜNG HƯỚNG'), self.M('field', 1.4),
                         tx('mỗi đoạn ngắn: độ dốc tại điểm đó', 22, SOFT), frac=.12)
        self.wait_until(.45, t0)
        fam = VGroup(*[clipped(a, lambda v, k=k: k * math.exp(v * v / 2), -2.2, 2.2, PURPLE, 2.5, y_max=4.4)
                       for k in (.35, .6, 1.6)])
        self.play(Create(fam), run_time=self.rt(.1))
        self.write_board(tx('vô số đường cong đi theo trường hướng', 22, PURPLE), frac=.05)
        self.wait_until(.75, t0)
        self.play(FadeIn(dot(a, 0, 1, GOLD, .1)),
                  Create(clipped(a, lambda v: math.exp(v * v / 2), -2.2, 2.2, GOLD, 5, y_max=4.4)), run_time=self.rt(.1))
        self.write_board(tx('đi qua (0; 1): chỉ một đường', 23, GOLD, bold=True), frac=.05)

    def beat_c2(self, T):
        self.worked(self.now(), 'TÁCH BIẾN', ('sep1', 'sep2'), (.05, .35), (1.6, 1.15), gap=.8)

    def beat_c3(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'VẾ TRÁI LÀ MỘT PHÉP ĐỔI BIẾN', ('sub',), (.1,), (1.35,))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('(xem lại tập 16: đổi biến phải đổi cận)', 23, SOFT).next_to(lines[-1], DOWN, buff=.7)),
                  run_time=self.rt(.05))

    def type_card(self, t0, n, key, color, fracs, note):
        self.clear_stage(.05)
        head = badge(f'DẠNG {n}', color, 22)
        m = self.M(key, 1.2)
        nt = tx(note, 24, SOFT)
        self.centre(head, m, nt, top=2.0, gap=.8)
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.wait_until(fracs[0], t0)
        self.play(Write(m), run_time=self.rt(.16))
        self.play(FadeIn(self.box(m, color)), run_time=self.rt(.03))
        self.wait_until(fracs[1], t0)
        self.play(FadeIn(nt, shift=UP * .1), run_time=self.rt(.05))

    def beat_c4(self, T):
        self.type_card(self.now(), 1, 'type1', CYAN, (.12, .7), 'cần f > 0 để lấy ln f')

    def beat_c5(self, T):
        self.type_card(self.now(), 2, 'type2', PURPLE, (.12, .72), 'chú ý thứ tự: 1/f(a) trừ 1/f(b)')

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        cards = []
        for i, (n, key, col) in enumerate(((3, 'type3', GREEN), (4, 'type4', GOLD))):
            c = card(5.9, 3.2, col).move_to([-3.1 + 6.2 * i, .2, 0])
            g = VGroup(c, badge(f'DẠNG {n}', col, 20).move_to(c.get_top() + DOWN * .55),
                       self.M(key, 1.25, max_w=5.4).move_to(c.get_center() + DOWN * .25))
            cards.append(g)
        self.play(FadeIn(cards[0], shift=UP * .2), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(cards[1], shift=UP * .2), run_time=self.rt(.08))
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('Bí quyết: vế trái là đạo hàm của cái gì?', 28, GOLD, bold=True).move_to([0, -2.3, 0])),
                  run_time=self.rt(.06))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        warn = VGroup(cross(CORAL, .32), tx('Chia cho f, lấy ln f khi chưa biết f ≠ 0, f > 0', 27, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.3).move_to([0, .8, 0])
        ok = VGroup(check(GREEN, .32), tx('Đọc kỹ điều kiện đề cho: “f(x) > 0 với mọi x”', 27, GREEN)) \
            .arrange(RIGHT, buff=.3).move_to([0, -.6, 0])
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.07))
        self.wait_until(.5, t0)
        self.play(FadeIn(ok, shift=UP * .1), run_time=self.rt(.07))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.field_axes()
        self.play(Create(clipped(a, lambda v: math.exp(v * v / 2), -2.2, 2.2, GOLD, 5, y_max=4.4)),
                  FadeIn(dot(a, 0, 1, GOLD, .1)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('field', 1.3), frac=.08)
        self.wait_until(.25, t0)
        self.write_board(self.M('e1_s1', 1.15), frac=.12)
        self.wait_until(.6, t0)
        m = self.M('e1_s2', 1.3)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        self.task_screen(self.now(), 'VÍ DỤ 2', ('e2_task', 'e2_s1', 'e2_s2'), (.3, .7), (1.35, 1.35, 1.4))

    def beat_e3(self, T):
        self.task_screen(self.now(), 'VÍ DỤ 3', ('e3_task', 'e3_s1', 'e3_s2'), (.28, .68), (1.3, 1.35, 1.45))

    def beat_e4(self, T):
        self.task_screen(self.now(), 'VÍ DỤ 4', ('e4_task', 'e4_s1', 'e4_s2'), (.3, .7), (1.3, 1.35, 1.45))

    def beat_e5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'HỎI TIẾP: TÍCH PHÂN CỦA f', ('e4_s2', 'e5_s1'), (.05, .3), (1.35, 1.5), gap=.8)
        self.wait_until(.65, t0)
        self.play(FadeIn(tx('câu nhiều bước – hay gặp ở phần trả lời ngắn', 24, SOFT).next_to(lines[-1], DOWN, buff=.7)),
                  run_time=self.rt(.05))

    def beat_e6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'MẸO: THAY NGƯỢC ĐỂ KIỂM TRA', ('check',), (.2,), (1.4,), box_last=False)
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('10 giây kiểm tra – tránh mất điểm', 26, GREEN, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.4, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.25)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.82, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        task = self.M('sa_task', 1.45)
        note = tx('(làm tròn đến hàng phần trăm)', 22, SOFT)
        hint = tx('Dạng 2: đạo hàm của −1/f bằng x', 25, PURPLE, bold=True)
        self.centre(tag, task, note, hint, top=2.4, gap=.5)
        self.play(FadeIn(tag), Write(task), FadeIn(note), run_time=self.rt(.14))
        self.wait_until(.72, t0)
        self.play(FadeIn(hint), run_time=self.rt(.06))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s1, s2 = self.M('sa_s1', 1.4), self.M('sa_s2', 1.45)
        sheet = self.answer_sheet('0,67')
        self.centre(s1, s2, sheet, top=2.2, gap=.75)
        self.play(Write(s1), run_time=self.rt(.14))
        self.wait_until(.35, t0)
        self.play(Write(s2), run_time=self.rt(.14))
        self.wait_until(.75, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Trường hướng', 'sum1', 'Điều kiện ban đầu chọn một hàm'),
                                ('Tách biến', 'sum2', 'Tích phân hai vế'),
                                ('Bốn dạng', 'sum3', 'Vế trái là đạo hàm của gì?')),
                           fracs=(.04, .35, .6))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Cho', 'hw1'), ('Cho', 'hw2'), ('Cho', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .35, .6))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Trắc nghiệm  ·  Đúng/Sai  ·  Trả lời ngắn', 28, GOLD, bold=True),
                            self.M('next1', 1.0)])


class INT19_SMOKE(INT19):
    smoke = True
