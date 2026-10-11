"""INT34 – Những bẫy sai kinh điển & kiểm tra bằng máy tính.

    python scripts/build_typst.py --ep int34
    python scripts/prepare_voice.py --ep int34 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int34/scene.py INT34
    python scripts/finalize.py --ep int34

One method per narration beat (int34/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M`` / ``self.TM``).
Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, Polygon, RoundedRectangle, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, band, card, check, clipped, cross, signed_area, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL_2, SOFT, WHITE  # noqa: E402
from int34.lesson import CHECKLIST  # noqa: E402

CK_KEYS = ('ck0', 'ck1', 'ck2', 'ck3', 'ck4', 'ck5', 'ck6', 'ck7')
ROWS = (('Bài làm sai', CORAL), ('Sửa lại', GREEN), ('Kiểm tra', GOLD))


class INT34(LessonScene):
    EP = 'int34'

    # ------------------------------------------------------------ helpers
    def calc(self, key, result, center, scale=1.0):
        """Calculator mock-up: the integral on the screen, the decimal result returned separately."""
        body = RoundedRectangle(width=5.6, height=2.75, corner_radius=.22, fill_color=PANEL_2, fill_opacity=1,
                                stroke_color=SOFT, stroke_width=2)
        screen = RoundedRectangle(width=5.1, height=1.85, corner_radius=.1, fill_color='#0E1E17', fill_opacity=1,
                                  stroke_color=GREEN, stroke_width=1.5).move_to(body.get_center() + UP * .27)
        expr = self.M(key, scale, max_w=4.6)
        expr.next_to(screen.get_top(), DOWN, buff=.14).align_to(screen.get_left() + RIGHT * .22, LEFT)
        tag = tx('MÁY TÍNH CẦM TAY', 15, SOFT, bold=True).move_to(body.get_bottom() + UP * .24)
        res = self.TM(f'$= {result}$', 30, GOLD)
        res.move_to(screen.get_corner(DOWN + RIGHT) + LEFT * .22 + UP * .1, aligned_edge=DOWN + RIGHT)
        shell = VGroup(body, screen, tag, expr).shift([center[0], center[1], 0])
        res.shift([center[0], center[1], 0])
        return shell, res

    def clinic(self, t0, tag, keys, fracs=(.1, .42, .72)):
        """Wrong / fixed / check rows for one classic mistake (full width)."""
        self.clear_stage(.05)
        head = badge(tag, CORAL, 21).move_to([0, 2.7, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        for k, (key, (label, col), frac, y) in enumerate(zip(keys, ROWS, fracs, (1.45, -.05, -1.55))):
            c = card(12.8, 1.3, col).move_to([0, y, 0])
            icon = (cross(CORAL), check(GREEN), check(GOLD))[k]
            lab = VGroup(icon, tx(label, 20, col, bold=True)).arrange(RIGHT, buff=.16) \
                .move_to(c.get_left() + RIGHT * .3, aligned_edge=LEFT)
            m = self.M(key, 1.3, max_w=9.4)
            if m.height > 1.12:
                m.scale_to_fit_height(1.12)
            m.move_to([1.05, y, 0])
            self.wait_until(frac, t0)
            self.play(FadeIn(VGroup(c, lab)), Write(m), run_time=self.rt(.1))
            if k == 0:
                self.play(Create(Line(m.get_left() + LEFT * .1, m.get_right() + RIGHT * .1, color=CORAL, stroke_width=4)),
                          run_time=self.rt(.04))

    def graph_case(self, tag, wrong, right, frac_right, t0, scales=(.95, .95)):
        """Board for a mistake that needs a picture: crossed-out wrong line, then the fix."""
        w = VGroup(cross(CORAL), self.M(wrong, scales[0])).arrange(RIGHT, buff=.2)
        self.write_board(badge(tag, CORAL, 19), w, frac=.1)
        self.play(Create(Line(w[1].get_left(), w[1].get_right(), color=CORAL, stroke_width=3)), run_time=self.rt(.03))
        self.wait_until(frac_right, t0)
        r = VGroup(check(GREEN), self.M(right, scales[1])).arrange(RIGHT, buff=.2)
        self.write_board(r, frac=.1)
        return r

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        lab = tx('Bài làm của một bạn:', 22, SOFT).move_to([-6.3, 2.55, 0], aligned_edge=LEFT)
        m = self.M('h1_wrong', 1.45).move_to([0, 1.5, 0])
        self.play(FadeIn(lab), Write(m), run_time=self.rt(.14))
        self.wait_until(.42, t0)
        shell, res = self.calc('h1_expr', '"3,75"', (-2.9, -1.35))
        self.play(FadeIn(shell, shift=UP * .15), run_time=self.rt(.06))
        self.play(FadeIn(res, scale=1.2), run_time=self.rt(.04))
        self.play(FadeIn(cross(CORAL, .5).next_to(m, RIGHT, buff=.3)), run_time=self.rt(.03))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('Lỗi nằm ở đâu?', 34, GOLD, bold=True).move_to([3.4, -1.35, 0])), run_time=self.rt(.05))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Ba lớp kiểm tra', 'Đạo hàm, máy tính, ước lượng'),
                         ('Tám lỗi sai', 'Hay gặp nhất trong chương'),
                         ('Nhận ra bẫy', 'Đúng/Sai và trả lời ngắn')], t0, fracs=(.1, .38, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('LỚP 1: ĐẠO HÀM', GOLD, 21)
        rule = self.M('c1_rule', 1.35)
        ex = self.M('c1_ex', 1.35)
        note = self.TM('vậy $integral ln x dif x = x ln x - x + C$', 26, GREEN)
        self.centre(head, rule, ex, note, top=2.75, gap=.55)
        self.play(FadeIn(head), run_time=self.rt(.03))
        self.play(Write(rule), run_time=self.rt(.1))
        self.play(FadeIn(self.box(rule, GOLD)), run_time=self.rt(.03))
        self.wait_until(.55, t0)
        self.play(Write(ex), run_time=self.rt(.12))
        self.wait_until(.85, t0)
        self.play(FadeIn(note, shift=UP * .1), run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        shell, res = self.calc('c2_expr', '1', (LEFT_CX, .3), 1.1)
        self.play(FadeIn(shell, shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.22, t0)
        self.play(FadeIn(res, scale=1.2), run_time=self.rt(.04))
        self.write_board(self.heading('LỚP 2: MÁY TÍNH'), self.TM('đổi đáp án sang số thập phân rồi so', 22, WHITE),
                         frac=.06)
        self.wait_until(.55, t0)
        m = self.M('c2_cmp', 1.0)
        self.write_board(m, frac=.12)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 1.3, 1), (0, 3.2, 1), 5.6, 4.8, center=[LEFT_CX, -.2, 0], x_ticks=(1,), y_ticks=(1, 2),
                 x_label='x', y_label='y')
        self.show_axes(a)
        f = lambda v: math.exp(v * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 1.06, CYAN, 4)), FadeIn(area(a, f, 0, 1, CYAN, .4)), run_time=self.rt(.08))
        self.write_board(self.heading('LỚP 3: ƯỚC LƯỢNG'), self.M('c3_bound', .9), frac=.08)
        self.wait_until(.42, t0)
        lo = Polygon(a.c2p(0, 0), a.c2p(0, 1), a.c2p(1, 1), a.c2p(1, 0), stroke_color=GREEN, stroke_width=3, fill_opacity=0)
        hi = Polygon(a.c2p(0, 0), a.c2p(0, math.e), a.c2p(1, math.e), a.c2p(1, 0), stroke_color=GOLD, stroke_width=3,
                     fill_opacity=0)
        self.play(Create(lo), Create(hi), run_time=self.rt(.07))
        self.play(FadeIn(self.TM('$e$', 24, GOLD).next_to(a.c2p(0, math.e), LEFT, buff=.12)), run_time=self.rt(.02))
        self.write_board(self.M('c3_ex', 1.05), frac=.08)
        self.wait_until(.8, t0)
        m = VGroup(self.M('c3_expr', .95), self.TM('$approx "1,46"$ (máy tính)', 24, GOLD)).arrange(RIGHT, buff=.2)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Đạo hàm', 'k1', 'Kiểm tra mọi kết quả nguyên hàm'),
                                ('Máy tính', 'k2', 'So đáp án dạng số thập phân'),
                                ('Ước lượng', 'k3', 'Dấu và độ lớn có hợp lý không?')),
                           fracs=(.04, .2, .42), head_text='BA LỚP KIỂM TRA')

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.clinic(self.now(), 'LỖI 1: QUÊN TRỊ TUYỆT ĐỐI TRONG LN', ('e1_wrong', 'e1_right', 'e1_check'), (.05, .25, .5))

    def beat_e2(self, T):
        self.clinic(self.now(), 'LỖI 2: NGUYÊN HÀM CỦA TÍCH', ('e2_wrong', 'e2_right', 'e2_check'), (.05, .5, .72))

    def beat_e3(self, T):
        self.clinic(self.now(), 'LỖI 3: QUÊN CHIA HỆ SỐ', ('e3_wrong', 'e3_right', 'e3_check'), (.05, .3, .65))

    def beat_e4(self, T):
        self.clinic(self.now(), 'LỖI 4: SAI DẤU LƯỢNG GIÁC', ('e4_wrong', 'e4_right', 'e4_check'), (.05, .3, .65))

    def beat_e5(self, T):
        t0 = self.now()
        self.clinic(t0, 'LỖI 5: ĐỔI BIẾN QUÊN ĐỔI CẬN', ('e5_wrong', 'e5_right', 'e5_check'), (.05, .3, .55))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.TM('$= "3,75"$ đúng như máy tính', 24, GREEN).move_to([0, -2.6, 0])), run_time=self.rt(.04))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 2.3, 1), (-1.4, 3.4, 1), 5.6, 4.9, center=[LEFT_CX, -.2, 0], x_ticks=(1, 2), y_ticks=(-1, 1, 3),
                 x_label='x', y_label='y')
        self.show_axes(a)
        f = lambda v: v * v - 1  # noqa: E731
        self.play(Create(clipped(a, f, 0, 2.08, CYAN, 4)), FadeIn(signed_area(a, f, 0, 2)), run_time=self.rt(.08))
        self.graph_case('LỖI 6: DIỆN TÍCH QUÊN TRỊ TUYỆT ĐỐI', 'e6_wrong', 'e6_right', .45, t0, (1.0, .9))
        self.wait_until(.82, t0)
        m = self.M('e6_check', 1.05)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 1.35, 1), (0, 2.7, 1), 5.6, 4.9, center=[LEFT_CX, -.2, 0], x_ticks=(1,), y_ticks=(1, 2),
                 x_label='x', y_label='y')
        self.show_axes(a)
        top, low = (lambda v: 2), (lambda v: v)
        self.play(Create(clipped(a, top, 0, 1.25, GOLD, 4)), Create(clipped(a, low, 0, 1.25, CYAN, 4)),
                  FadeIn(band(a, top, low, 0, 1, GREEN, .4)), run_time=self.rt(.08))
        R = Line(a.c2p(.6, 0), a.c2p(.6, 2), color=GOLD, stroke_width=6)
        r = Line(a.c2p(.62, 0), a.c2p(.62, .6), color=CYAN, stroke_width=6)
        labels = VGroup(self.TM('$R = 2$', 22, GOLD).next_to(R, RIGHT, buff=.12).shift(UP * .9),
                        self.TM('$r = x$', 22, CYAN).next_to(r, RIGHT, buff=.12))
        self.play(Create(R), Create(r), FadeIn(labels), run_time=self.rt(.05))
        self.graph_case('LỖI 7: BÌNH PHƯƠNG CỦA HIỆU', 'e7_wrong', 'e7_right', .5, t0)
        self.wait_until(.8, t0)
        m = self.M('e7_check', 1.15)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_e8(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 4.4, 1), (-2.5, 2.5, 1), 5.6, 4.9, center=[LEFT_CX, -.2, 0], x_ticks=(1, 2, 3, 4), y_ticks=(-2, 2),
                 x_label='t', y_label='v')
        self.show_axes(a)
        f = lambda v: v - 2  # noqa: E731
        self.play(Create(clipped(a, f, 0, 4.2, CYAN, 4)), FadeIn(signed_area(a, f, 0, 4)), run_time=self.rt(.08))
        self.graph_case('LỖI 8: ĐỘ DỜI VÀ QUÃNG ĐƯỜNG', 'e8_wrong', 'e8_right', .5, t0, (1.05, 1.05))
        self.wait_until(.8, t0)
        m = self.M('e8_check', 1.0)
        self.write_board(m, frac=.06)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_e9(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.play(FadeIn(tx('DANH SÁCH KIỂM TRA TRƯỚC KHI NỘP', 27, GOLD, bold=True).move_to([0, 2.65, 0])),
                  run_time=self.rt(.03))
        for i, (label, _) in enumerate(CHECKLIST):
            col, row = divmod(i, 4)
            x0, y = -6.3 + 6.6 * col, 1.65 - 1.12 * row
            c = card(6.2, .95, GREEN if i % 2 == 0 else CYAN).move_to([x0 + 3.1, y, 0])
            g = VGroup(check(GREEN), tx(f'{i + 1}. {label}', 22, WHITE, bold=True)).arrange(RIGHT, buff=.18) \
                .move_to([x0 + .25, y, 0], aligned_edge=LEFT)
            m = self.M(CK_KEYS[i], .95, max_w=3.2)
            if m.height > .78:
                m.scale_to_fit_height(.78)
            m.move_to([x0 + 4.45, y, 0])
            self.wait_until(.05 + .1 * i, t0)
            self.play(FadeIn(VGroup(c, g, m), shift=RIGHT * .15), run_time=self.rt(.04))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.mc_question(t0, 1, [self.M('mc_q', 1.5)], [self.M(k, 1.5) for k in ('mc_a', 'mc_b', 'mc_c', 'mc_d')],
                         fracs=(.3, .78))

    def beat_x2(self, T):
        self.play(*self.mc_mark(2, self.M('mc_sol', 1.4)), run_time=self.rt(.1))

    def beat_x3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        intro = self.TM('Mỗi mệnh đề có thể chứa một bẫy. Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.2), self.M('tf_b', 1.2), self.M('tf_c', 1.1), self.M('tf_d', 1.1))
        self.tf_question(t0, [intro], items, fracs=(.25, .7))

    def beat_x4(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, False), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x5(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, False), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('SĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def sa_axes(self):
        a = axes((0, 3.5, 1), (-1.5, 3.4, 1), 5.6, 4.9, center=[LEFT_CX, -.2, 0], x_ticks=(1, 2, 3), y_ticks=(-1, 1, 3),
                 x_label='t', y_label='v')
        return a

    def beat_x6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.sa_axes()
        self.show_axes(a)
        self.sa_axes_obj = a
        self.play(Create(clipped(a, lambda v: v * v - 4 * v + 3, 0, 3.3, CYAN, 4)), run_time=self.rt(.08))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', CORAL, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.0),
                         self.TM('Quãng đường trong $3$ giây đầu?', 24, GOLD, bold=True),
                         tx('(làm tròn đến hàng phần trăm)', 19, SOFT), frac=.14)
        self.wait_until(.8, t0)
        self.write_board(self.TM('cẩn thận: $v$ đổi dấu!', 24, CORAL, bold=True), frac=.05)

    def beat_x7(self, T):
        t0 = self.now()
        self.clear_board(.03)
        a = self.sa_axes_obj
        self.play(FadeIn(signed_area(a, lambda v: v * v - 4 * v + 3, 0, 3)), run_time=self.rt(.05))
        self.write_board(self.M('sa_s1', 1.05), frac=.08)
        self.wait_until(.25, t0)
        m = self.M('sa_s2', .95)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.8, t0)
        self.write_board(self.answer_sheet('2,67'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Đạo hàm', 'sum1', 'Nguyên hàm luôn kiểm tra được'),
                                ('Máy tính', 'sum2', 'Đổi đáp án sang thập phân rồi so'),
                                ('Tám bẫy', 'sum3', 'Dấu, hệ số, cận, trị tuyệt đối')),
                           fracs=(.04, .3, .58))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tính:', 'hw1'), ('Diện tích:', 'hw2'), ('Quãng đường:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Phần E · Đề luyện tổng hợp', 28, GOLD, bold=True), self.M('next1', 1.2)])


class INT34_SMOKE(INT34):
    smoke = True
