"""INT31 – Bồn chứa, bể nước và lưu lượng.

    python scripts/build_typst.py --ep int31
    python scripts/prepare_voice.py --ep int31 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int31/scene.py INT31
    python scripts/finalize.py --ep int31

One method per narration beat (int31/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M``, ``self.TM``,
``self.readout``). Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, Line, RoundedRectangle, ValueTracker, VGroup, Write,
                   always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, clipped, dot, tx  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT31(LessonScene):
    EP = 'int31'

    def water_tank(self, level_fn, capacity, center=(-1.3, -.6), w=1.5, h=3.6, unit='L', color=CYAN):
        """Open tank whose water follows level_fn(); tick labels are typeset."""
        cx, cy = center
        shell = VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0], color=SOFT, stroke_width=3),
                       Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=SOFT, stroke_width=3),
                       Line([cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=SOFT, stroke_width=3))
        ticks = VGroup()
        for k in range(1, 5):
            y = cy - h / 2 + h * k / 4
            ticks.add(Line([cx + w / 2, y, 0], [cx + w / 2 + .1, y, 0], color=SOFT, stroke_width=2),
                      self.TM(f'${capacity * k / 4:g}$', 14, SOFT).move_to([cx + w / 2 + .45, y, 0]))
        water = always_redraw(lambda: RoundedRectangle(
            width=w - .08, height=max(h * min(level_fn(), capacity) / capacity, .01), corner_radius=.02,
            fill_color=color, fill_opacity=.55, stroke_width=0)
            .move_to([cx, cy - h / 2 + h * min(level_fn(), capacity) / capacity / 2, 0]))
        label = self.TM(f'$"{unit}"$', 14, SOFT).move_to([cx + w / 2 + .45, cy - h / 2 - .2, 0])
        return VGroup(water, shell, ticks, label)

    def flow_axes(self, tmax, rmax, tt, rt_, center=(LEFT_CX - 1.1, .9), w=3.6, h=2.9, ylabel='r'):
        a = axes((0, tmax, 1), (0, rmax, 1), w, h, center=[center[0], center[1], 0], x_ticks=tt, y_ticks=rt_,
                 x_label='t', y_label=ylabel, label_size=15)
        self.show_axes(a)
        return a

    def fill_tank(self, a, r, V, tmax, capacity, frac, tank_kw=None, readout_vars=('t', 'V')):
        """Sweep t: shade area under r, fill the tank with V(t), live typeset readout."""
        tt = ValueTracker(0)
        tank = self.water_tank(lambda: V(tt.get_value()), capacity, **(tank_kw or {}))
        shade = always_redraw(lambda: area(a, r, 0, max(tt.get_value(), .01), CYAN, .45))
        rd = always_redraw(lambda: self.readout([(readout_vars[0], tt.get_value(), 1),
                                                 (readout_vars[1], V(tt.get_value()), 0)], 20)
                           .move_to([BOARD_X, -2.4, 0], aligned_edge=LEFT))
        self.add(tank, shade, rd)
        self.play(tt.animate.set_value(tmax), run_time=self.rt(frac), rate_func=linear)
        for m in (tank[0], shade, rd):
            m.clear_updaters()
        return tank

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.flow_axes(20, 104, (5, 10, 15), (20, 60))
        r = lambda v: 20 + 4 * v  # noqa: E731
        self.play(Create(clipped(a, r, 0, 19, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(self.M('hook', 1.0), tx('Bao lâu thì đầy bể?', 26, GOLD, bold=True), frac=.12)
        self.wait_until(.25, t0)
        T1 = -5 + 5 * math.sqrt(21)
        self.fill_tank(a, r, lambda v: 20 * v + 2 * v * v, T1, 1000, .4)
        self.wait_until(.85, t0)
        self.write_board(self.TM('$T approx "17,9"$ phút', 24, GREEN, bold=True), frac=.05)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Lượng nước', 'Tích phân của lưu lượng'),
                         ('Vào và ra', 'Lưu lượng thực, lượng nước lớn nhất'),
                         ('Mực nước', 'Bể trụ: chia diện tích đáy')], t0, fracs=(.1, .38, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'LƯU LƯỢNG LÀ ĐẠO HÀM CỦA THỂ TÍCH', ('flow',), (.12,), (1.4,))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('vẫn là Newton – Leibniz, với một ý nghĩa mới', 25, SOFT).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 10.8, 1), (0, 6, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(5, 10), y_ticks=(2, 4),
                 x_label='t', y_label='r')
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: 3, 0, 9.8, GOLD, 4)), FadeIn(area(a, lambda v: 3, 0, 8, GOLD, .4)),
                  run_time=self.rt(.07))
        self.write_board(self.heading('DIỆN TÍCH = LƯỢNG NƯỚC'), self.TM('lưu lượng không đổi: $r dot T$', 22, GOLD),
                         frac=.1)
        self.wait_until(.45, t0)
        f = lambda v: 1 + .4 * v + .6 * math.sin(v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 9.8, CYAN, 4)), FadeIn(area(a, f, 0, 8, CYAN, .4)), run_time=self.rt(.08))
        self.write_board(self.TM('lưu lượng thay đổi: $integral_0^T r(t) dif t$', 22, CYAN), frac=.08)

    def beat_c2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = axes((0, 10.8, 1), (0, 6, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(5, 10), y_ticks=(2, 4),
                 x_label='t', y_label='r')
        self.show_axes(a)
        f = lambda v: 1 + .4 * v + .6 * math.sin(v)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 9.8, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(self.heading('CHIA NHỎ THỜI GIAN'), self.M('riem', 1.1), frac=.12)
        from manim import Rectangle
        self.wait_until(.3, t0)
        for n, frac in ((5, .3), (20, .55)):
            dt = 8 / n
            bars = VGroup(*[Rectangle(width=abs(a.c2p(dt, 0)[0] - a.c2p(0, 0)[0]),
                                      height=abs(a.c2p(0, f(k * dt + dt / 2))[1] - a.c2p(0, 0)[1]),
                                      fill_color=GOLD, fill_opacity=.45, stroke_color=WHITE, stroke_width=1)
                            .move_to(a.c2p(k * dt + dt / 2, f(k * dt + dt / 2) / 2)) for k in range(n)])
            self.wait_until(frac, t0)
            self.play(FadeIn(bars), run_time=self.rt(.06))
        self.write_board(self.TM('mỗi khoảng nhỏ: lượng nước $approx r(t) Delta t$', 22, GOLD), frac=.06)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        lines = [self.M('net', 1.6), self.M('peak', 1.5)]
        head = badge('VÀO VÀ RA', GOLD, 20)
        self.centre(head, *lines, top=2.3, gap=.8)
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.play(Write(lines[0]), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(Write(lines[1]), run_time=self.rt(.1))
        self.play(FadeIn(self.box(lines[1], GREEN)), run_time=self.rt(.03))

    def beat_c4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'MỰC NƯỚC TRONG BỂ TRỤ', ('level',), (.15,), (1.6,))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.TM('$S$: diện tích đáy bể', 25, SOFT).next_to(lines[-1], DOWN, buff=.8)),
                  run_time=self.rt(.05))

    def beat_c5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CẨN THẬN ĐƠN VỊ', ('units',), (.1,), (1.6,), box_last=False)
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('nhiều lỗi sai đến từ đơn vị, không phải từ tích phân', 25, CORAL, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1: THỜI GIAN ĐẦY BỂ', ('e1_s1', 'e1_s2'), (.05, .55), (1.4, 1.4), gap=.7)

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 37, 1), (-45, 75, 1), 3.6, 2.9, center=[LEFT_CX - 1.1, .9, 0], x_ticks=(15, 30), y_ticks=(30,),
                 x_label='t', y_label='r', label_size=15)
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: 30, 0, 36, GOLD, 3.5)), Create(clipped(a, lambda v: 2 * v, 0, 36, CORAL, 3.5,
                                                                                  y_max=75)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 2: VỪA VÀO VỪA RA', GOLD, 20), self.M('e2_s1', .95), frac=.12)
        self.wait_until(.3, t0)
        tt = ValueTracker(0)
        V = lambda v: 200 + 30 * v - v * v  # noqa: E731
        tank = self.water_tank(lambda: V(tt.get_value()), 500)
        rd = always_redraw(lambda: self.readout([('t', tt.get_value(), 1), ('V', V(tt.get_value()), 0)], 20)
                           .move_to([BOARD_X, -2.4, 0], aligned_edge=LEFT))
        self.add(tank, rd)
        self.play(tt.animate.set_value(15), run_time=self.rt(.3), rate_func=linear)
        tank[0].clear_updaters()
        rd.clear_updaters()
        self.play(FadeIn(dot(a, 15, 30, WHITE)), run_time=self.rt(.03))
        m = self.M('e2_s2', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3(self, T):
        self.clear_stage(.05)
        tt = ValueTracker(15)
        V = lambda v: max(0.0, 200 + 30 * v - v * v)  # noqa: E731
        tank = self.water_tank(lambda: V(tt.get_value()), 500)
        rd = always_redraw(lambda: self.readout([('t', tt.get_value(), 1), ('V', V(tt.get_value()), 0)], 20)
                           .move_to([BOARD_X, -2.4, 0], aligned_edge=LEFT))
        self.add(tank, rd)
        self.write_board(self.heading('SAU ĐÓ: RA NHIỀU HƠN VÀO'), frac=.05)
        self.play(tt.animate.set_value(15 + math.sqrt(425)), run_time=self.rt(.4), rate_func=linear)
        tank[0].clear_updaters()
        rd.clear_updaters()
        m = self.M('e3_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tt = ValueTracker(0)
        tank = self.water_tank(lambda: .1 * tt.get_value() ** 2 / 2 / 2, 4, center=(-2.6, -.6), w=2.6, unit='m',
                               color=CYAN)
        self.add(tank)
        self.write_board(badge('VÍ DỤ 3: MỰC NƯỚC DÂNG', GOLD, 20),
                         self.TM('bể trụ đáy $S = 2 "m"^2$, $r = "0,1" t$ ($"m"^3$/phút)', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        rd = always_redraw(lambda: self.readout([('t', tt.get_value(), 1), ('h', .025 * tt.get_value() ** 2, 2)], 20)
                           .move_to([BOARD_X, -2.4, 0], aligned_edge=LEFT))
        self.add(rd)
        self.play(tt.animate.set_value(10), run_time=self.rt(.3), rate_func=linear)
        tank[0].clear_updaters()
        rd.clear_updaters()
        self.write_board(self.M('e4_s1', 1.1), frac=.1)
        m = self.M('e4_s2', 1.2)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 15, 1), (0, 75, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(2, 12, 14), y_ticks=(60,),
                 x_label='t', y_label='r')
        self.show_axes(a)
        g = lambda v: 30 * v if v <= 2 else (60 if v <= 12 else 60 - 30 * (v - 12))  # noqa: E731
        self.play(Create(clipped(a, g, 0, 14, CYAN, 4.5)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 4: ĐỌC ĐỒ THỊ', GOLD, 20), tx('khởi động 2 phút · bơm đều 10 phút · tắt dần 2 phút',
                                                                   20, WHITE), frac=.1)
        self.wait_until(.5, t0)
        for x0, x1, col, lab, lx in ((0, 2, GREEN, '60', 1.3), (2, 12, GOLD, '600', 7), (12, 14, PURPLE, '60', 12.7)):
            self.play(FadeIn(area(a, g, x0, x1, col, .45)), FadeIn(self.TM(f'${lab}$', 20, WHITE).move_to(a.c2p(lx, 25))),
                      run_time=self.rt(.05))
        m = self.M('e5_s1', 1.4)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 32, 1), (0, 9, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(10, 20, 30), y_ticks=(4, 8),
                 x_label='t', y_label='r')
        self.show_axes(a)
        f = lambda v: 8 * math.exp(-v / 10)  # noqa: E731
        self.play(Create(clipped(a, f, 0, 31, CORAL, 4)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 5: RÒ RỈ', GOLD, 20), self.TM('$r(t) = 8 e^(-t\\/10)$ (L/phút)', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        self.play(FadeIn(area(a, f, 0, 10, CORAL, .5)), run_time=self.rt(.06))
        self.write_board(self.M('leak1', 1.0), frac=.12)
        self.wait_until(.65, t0)
        self.play(FadeIn(area(a, f, 10, 31, CORAL, .2)), run_time=self.rt(.05))
        m = self.M('leak2', 1.1)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        self.worked(self.now(), 'VÍ DỤ 6: TÌM THAM SỐ', ('inv1', 'inv2'), (.05, .45), (1.35, 1.4), gap=.7)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = self.M('tf_given', 1.2)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.15)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.flow_axes(30, 124, (10, 20), (50, 100))
        r = lambda v: 50 + 2 * v  # noqa: E731
        self.play(Create(clipped(a, r, 0, 29, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.TM('bồn rỗng $2000$ L, $r = 50 + 2t$ (L/phút)', 22, WHITE),
                         tx('Thời gian đầy bồn (phút, làm tròn đến hàng phần mười)?', 21, SOFT), frac=.14)
        self.wait_until(.5, t0)
        self.fill_tank(a, r, lambda v: 50 * v + v * v, -25 + math.sqrt(2625), 2000, .35)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', 1.1), frac=.12)
        self.wait_until(.4, t0)
        self.write_board(self.M('sa_s2', 1.2), frac=.1)
        self.wait_until(.75, t0)
        self.write_board(self.answer_sheet('26,2'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Lượng nước', 'sum1', 'Diện tích dưới đồ thị lưu lượng'),
                                ('Vào và ra', 'sum2', 'Lớn nhất khi hai lưu lượng bằng nhau'),
                                ('Mực nước', 'sum3', 'Chia cho diện tích đáy')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Lượng nước:', 'hw1'), ('Lớn nhất:', 'hw2'), ('Mực nước:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .25, .5))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Chi phí biên · lợi nhuận · tăng trưởng', 26, GOLD, bold=True), self.M('next1', 1.3)])


class INT31_SMOKE(INT31):
    smoke = True
