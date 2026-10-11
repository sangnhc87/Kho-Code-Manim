"""INT32 – Tích phân trong kinh tế và sinh học.

    python scripts/build_typst.py --ep int32
    python scripts/prepare_voice.py --ep int32 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int32/scene.py INT32
    python scripts/finalize.py --ep int32

One method per narration beat (int32/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M``, ``self.TM``,
``self.readout``). Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, ValueTracker, VGroup, always_redraw, linear

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, band, clipped, dot, tx  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT32(LessonScene):
    EP = 'int32'

    def ax(self, xr, yr, xt, yt, xl='x', yl='y', **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.0), center=kw.pop('center', [LEFT_CX, -.2, 0]),
                    x_ticks=xt, y_ticks=yt, x_label=xl, y_label=yl, **kw)

    def sweep_area(self, a, f, x0, x1, frac, label, total, color=CYAN, nd=0):
        """Shade the area under f from x0 to a moving x; live typeset readout of the accumulated amount."""
        xt = ValueTracker(x0 + 1e-3)
        shade = always_redraw(lambda: area(a, f, x0, max(xt.get_value(), x0 + 1e-3), color, .45))
        rd = always_redraw(lambda: self.readout([('x' if label != 't' else 't', xt.get_value(), 0 if label != 't' else 1),
                                                 ('Delta', total(xt.get_value()), nd)], 20)
                           .move_to([BOARD_X, -2.45, 0], aligned_edge=LEFT))
        self.add(shade, rd)
        self.play(xt.animate.set_value(x1), run_time=self.rt(frac), rate_func=linear)
        shade.clear_updaters()
        rd.clear_updaters()
        return VGroup(shade, rd)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.ax((0, 230, 1), (0, 95, 1), (100, 200), (20, 50, 80), yl="C'")
        self.show_axes(a)
        f = lambda v: .3 * v + 20  # noqa: E731
        self.play(Create(clipped(a, f, 0, 225, GOLD, 4)), run_time=self.rt(.06))
        self.write_board(self.M('hook', 1.0), tx('Chi phí tăng bao nhiêu?', 26, GOLD, bold=True), frac=.12)
        self.wait_until(.3, t0)
        self.sweep_area(a, f, 100, 200, .35, 'x', lambda v: .15 * (v * v - 10000) + 20 * (v - 100), GOLD)
        self.wait_until(.85, t0)
        self.write_board(self.TM('$approx "6,5"$ triệu đồng', 24, GREEN, bold=True), frac=.05)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Biên và tổng', 'Đạo hàm và tích phân'),
                         ('Lợi nhuận', 'Tăng thêm và sản lượng tối ưu'),
                         ('Sinh học, y học', 'Tăng trưởng và đào thải')], t0, fracs=(.1, .38, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'ĐẠI LƯỢNG BIÊN LÀ ĐẠO HÀM', ('marg',), (.4,), (1.6,))
        self.wait_until(.15, t0)
        self.play(FadeIn(self.TM("chi phí biên $C'(x)$: chi phí cho thêm một sản phẩm", 25, SOFT)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def marg_axes(self):
        a = self.ax((0, 330, 1), (0, 110, 1), (100, 200, 300), (20, 60, 100), yl='')
        self.show_axes(a)
        R1, C1 = (lambda v: 100 - .2 * v), (lambda v: 20 + .2 * v)
        self.play(Create(clipped(a, R1, 0, 320, CYAN, 4)), Create(clipped(a, C1, 0, 320, CORAL, 4, y_max=110)),
                  FadeIn(self.TM("$R'$", 20, CYAN).move_to(a.c2p(30, 102))),
                  FadeIn(self.TM("$C'$", 20, CORAL).move_to(a.c2p(30, 14))), run_time=self.rt(.06))
        return a, R1, C1

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, R1, C1 = self.marg_axes()
        self.write_board(self.heading('LỢI NHUẬN TĂNG THÊM'), self.M('profit', .95), frac=.12)
        self.wait_until(.6, t0)
        self.play(FadeIn(band(a, R1, C1, 100, 200, GREEN, .5)), run_time=self.rt(.07))
        self.write_board(self.TM("phần giữa hai đường biên $R'$ và $C'$", 22, GREEN), frac=.05)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, R1, C1 = self.marg_axes()
        self.write_board(self.heading('SẢN LƯỢNG TỐI ƯU'), frac=.04)
        self.play(FadeIn(band(a, R1, C1, 0, 200, GREEN, .45)), run_time=self.rt(.06))
        self.write_board(self.TM("$R' > C'$: lợi nhuận tăng", 22, GREEN), frac=.05)
        self.wait_until(.3, t0)
        self.play(FadeIn(band(a, C1, R1, 200, 320, CORAL, .45)), run_time=self.rt(.06))
        self.write_board(self.TM("$R' < C'$: lợi nhuận giảm", 22, CORAL), frac=.05)
        self.wait_until(.55, t0)
        self.play(FadeIn(dot(a, 200, 60, WHITE, .1)), run_time=self.rt(.03))
        m = self.M('opt', 1.3)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_c3b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 235, 1), (0, 110, 1), (80, 200), (60, 100), yl="p")
        self.show_axes(a)
        D = lambda v: 100 - .5 * v  # noqa: E731
        self.play(Create(clipped(a, D, 0, 200, CYAN, 4)), Create(clipped(a, lambda v: 60, 0, 200, GOLD, 3)),
                  run_time=self.rt(.06))
        self.write_board(self.heading('THẶNG DƯ TIÊU DÙNG'), self.M('cs', 1.15), frac=.12)
        self.wait_until(.45, t0)
        self.play(FadeIn(band(a, D, lambda v: 60, 0, 80, GREEN, .5)), FadeIn(dot(a, 80, 60, WHITE)), run_time=self.rt(.06))
        self.write_board(self.TM('$D = 100 - "0,5" x$, $P = 60$, $Q = 80$', 22, WHITE), frac=.06)
        self.wait_until(.75, t0)
        m = self.M('cs_ex', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'TĂNG TRƯỞNG TRONG SINH HỌC', ('growth',), (.25,), (1.6,))
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('tổng lượng = giá trị đầu + tích phân của tốc độ', 26, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 10.5, 1), (0, 22, 1), (2, 4, 6, 8, 10), (10, 20), xl='t', yl='r')
        self.show_axes(a)
        f = lambda v: 20 * math.exp(-.5 * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 10, CORAL, 4)), run_time=self.rt(.06))
        self.write_board(self.heading('ĐÀO THẢI THUỐC'), self.TM('tốc độ giảm dần theo hàm mũ', 22, WHITE), frac=.1)
        self.wait_until(.4, t0)
        self.play(FadeIn(area(a, f, 0, 4, CORAL, .45)), run_time=self.rt(.06))
        self.write_board(self.M('drug', 1.05), frac=.1)

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1: CHI PHÍ TĂNG THÊM', ('e1_s1', 'e1_s2'), (.05, .7), (1.05, 1.3), gap=.7)

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, R1, C1 = self.marg_axes()
        self.write_board(self.heading('VÍ DỤ 2: SẢN LƯỢNG TỐI ƯU'), frac=.04)
        self.wait_until(.45, t0)
        self.play(FadeIn(dot(a, 200, 60, WHITE, .1)), run_time=self.rt(.03))
        m = self.M('e2_s1', .9)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, R1, C1 = self.marg_axes()
        self.write_board(self.heading('LỢI NHUẬN TĂNG THÊM'), frac=.04)
        self.wait_until(.1, t0)
        self.play(FadeIn(band(a, R1, C1, 100, 200, GREEN, .5)), run_time=self.rt(.06))
        m = self.M('e3_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.play(FadeIn(band(a, C1, R1, 200, 250, CORAL, .5)), run_time=self.rt(.05))
        self.write_board(self.TM('vượt $200$: mỗi sản phẩm thêm làm lợi nhuận giảm', 21, CORAL), frac=.05)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 10.5, 1), (0, 9400, 1), (2, 4, 6, 8, 10), (2000, 4000, 6000, 8000), xl='t', yl="N'",
                    label_size=14)
        self.show_axes(a)
        f = lambda v: 1000 * math.exp(.2 * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 10.2, GREEN, 4)), run_time=self.rt(.06))
        self.write_board(self.heading('VÍ DỤ 3: VI KHUẨN'), self.TM("$N(0) = 5000$, $N'(t) = 1000 e^(\"0,2\" t)$", 22, WHITE),
                         frac=.1)
        self.wait_until(.3, t0)
        self.sweep_area(a, f, 0, 10, .3, 't', lambda v: 5000 * (math.exp(.2 * v) - 1), GREEN)
        m = self.M('e4_s1', .9)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 10.5, 1), (0, 22, 1), (2, 4, 6, 8, 10), (10, 20), xl='t', yl='r')
        self.show_axes(a)
        f = lambda v: 20 * math.exp(-.5 * v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 10, CORAL, 4)), run_time=self.rt(.06))
        self.write_board(self.heading('VÍ DỤ 4: ĐÀO THẢI THUỐC'), self.TM('$r(t) = 20 e^(-"0,5" t)$ (mg/h)', 22, WHITE),
                         frac=.1)
        self.wait_until(.3, t0)
        self.sweep_area(a, f, 0, 4, .25, 't', lambda v: 40 * (1 - math.exp(-.5 * v)), CORAL, nd=2)
        m = self.M('e5_s1', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 10.5, 1), (0, 3.4, 1), (5, 10), (1, 2, 3), xl='t', yl='r')
        self.show_axes(a)
        f = lambda v: 2 + .1 * v  # noqa: E731
        self.play(Create(clipped(a, f, 0, 10.3, PURPLE, 4)), run_time=self.rt(.06))
        self.write_board(self.heading('VÍ DỤ 5: DÂN SỐ'), self.TM('$r(t) = 2 + "0,1" t$ (nghìn người/năm)', 22, WHITE),
                         frac=.1)
        self.wait_until(.4, t0)
        self.play(FadeIn(area(a, f, 0, 10, PURPLE, .45)), run_time=self.rt(.06))
        m = self.M('e6_s1', 1.05)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        self.worked(self.now(), 'VÍ DỤ 6: TÌM THAM SỐ', ('inv1', 'inv2'), (.1, .6), (1.35, 1.35), gap=.7)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Chi phí (nghìn đồng):', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.15)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 4.4, 1), (0, 700, 1), (1, 2, 3, 4), (200, 400, 600), xl='t', yl="N'", label_size=14)
        self.show_axes(a)
        f = lambda v: 300 * math.sqrt(v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 4.3, GREEN, 4)), run_time=self.rt(.06))
        from common.kit import badge
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.2), tx('Sau 4 năm có bao nhiêu con cá?', 23, GOLD, bold=True), frac=.14)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', .95), frac=.14)
        self.wait_until(.75, t0)
        self.write_board(self.answer_sheet('3600'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Biên và tổng', 'sum1', 'Giá trị đầu cộng tích phân'),
                                ('Tối ưu', 'sum2', 'Hai đại lượng biên bằng nhau'),
                                ('Hàm mũ', 'sum3', 'Sinh học và y học')),
                           fracs=(.04, .3, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Chi phí:', 'hw1'), ('Tối ưu:', 'hw2'), ('Quần thể:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .35, .58))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Từ bảng số liệu đến hàm số và tích phân', 26, GOLD, bold=True), self.M('next1', 1.2)])


class INT32_SMOKE(INT32):
    smoke = True
