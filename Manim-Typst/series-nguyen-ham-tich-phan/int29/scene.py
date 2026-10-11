"""INT29 – Bài toán chuyển động thực tế: phanh xe, đuổi kịp, hai xe gặp nhau.

    python scripts/build_typst.py --ep int29
    python scripts/prepare_voice.py --ep int29 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int29/scene.py INT29
    python scripts/finalize.py --ep int29

One method per narration beat (int29/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M``, ``self.TM``,
``self.readout``). Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, ValueTracker, VGroup, Write, always_redraw,
                   linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, car, card, clipped, dot, tx  # noqa: E402
from common.kit import band  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

ROAD_Y = -2.45


class INT29(LessonScene):
    EP = 'int29'

    def vt_axes(self, tmax, vmax, tt, vt, h=3.4, center=None):
        a = axes((0, tmax, 1), (0, vmax, 1), 6.0, h, center=center or [LEFT_CX, .75, 0], x_ticks=tt, y_ticks=vt,
                 x_label='t', y_label='v')
        self.show_axes(a)
        return a

    def road(self, smax, x0=-6.3, x1=-.6):
        to_x = lambda m: x0 + (x1 - x0) * m / smax  # noqa: E731
        g = VGroup(Line([x0 - .1, ROAD_Y, 0], [x1 + .2, ROAD_Y, 0], color=SOFT, stroke_width=3))
        for k in range(0, 5):
            m = smax * k / 4
            g.add(Line([to_x(m), ROAD_Y - .08, 0], [to_x(m), ROAD_Y + .08, 0], color=SOFT, stroke_width=2),
                  self.TM('$' + (f'"{m:g}"'.replace('.', ',') if m % 1 else f'{m:g}') + '$', 15, SOFT)
                  .move_to([to_x(m), ROAD_Y - .3, 0]))
        self.play(Create(g), run_time=self.rt(.04))
        return to_x

    def race(self, sa, sb, tmax, smax, frac, label_b='B', readout_at=(BOARD_X, -2.3)):
        """Two cars driven by position functions sa(t), sb(t) with a live typeset readout."""
        to_x = self.road(smax)
        tt = ValueTracker(0)
        ca, cb = car(GOLD, .55), car(CYAN, .55)
        ca.add_updater(lambda m: m.move_to([to_x(sa(tt.get_value())), ROAD_Y + .55, 0]))
        cb.add_updater(lambda m: m.move_to([to_x(sb(tt.get_value())), ROAD_Y + .2, 0]))
        rd = always_redraw(lambda: self.readout([('t', tt.get_value(), 1), ('s_A', sa(tt.get_value()), 0),
                                                 (f's_{label_b}', sb(tt.get_value()), 0)], 20)
                           .move_to([readout_at[0], readout_at[1], 0], aligned_edge=LEFT))
        self.add(ca, cb, rd)
        self.play(tt.animate.set_value(tmax), run_time=self.rt(frac), rate_func=linear)
        for m in (ca, cb, rd):
            m.clear_updaters()
        return tt

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.vt_axes(22, 44, (10, 20), (20, 40))
        self.play(Create(clipped(a, lambda v: 20, 0, 21.5, GOLD, 4)), Create(clipped(a, lambda v: 2 * v, 0, 21.5, CYAN, 4)),
                  run_time=self.rt(.06))
        self.write_board(self.M('hook_a', 1.3), frac=.06)
        self.wait_until(.12, t0)
        self.race(lambda v: 20 * v, lambda v: v * v, 20, 400, .4)
        self.wait_until(.6, t0)
        self.play(FadeIn(dot(a, 10, 20, CORAL, .1)), run_time=self.rt(.03))
        self.write_board(self.TM('$t = 10$: hai đồ thị cắt nhau', 22, CORAL),
                         self.TM('nhưng lúc đó khoảng cách xa nhất!', 22, CORAL, bold=True), frac=.08)
        self.wait_until(.88, t0)
        self.write_board(self.TM('gặp nhau lúc $t = 20$ s', 24, GREEN, bold=True), frac=.05)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Vị trí', 'Vị trí đầu cộng tích phân vận tốc'),
                         ('Gặp nhau', 'Hai diện tích bằng nhau'),
                         ('Phanh xe', 'Khoảng cách an toàn')], t0, fracs=(.1, .38, .65))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'VỊ TRÍ TỪ VẬN TỐC', ('pos',), (.08,), (1.7,))
        self.wait_until(.5, t0)
        self.play(FadeIn(tx('mỗi xe một phương trình vị trí, chung một trục, chung gốc và chiều dương', 23, SOFT)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.vt_axes(22, 44, (10, 20), (20, 40), h=4.6, center=[LEFT_CX, -.2, 0])
        self.play(Create(clipped(a, lambda v: 20, 0, 21.5, GOLD, 4)), Create(clipped(a, lambda v: 2 * v, 0, 21.5, CYAN, 4)),
                  run_time=self.rt(.05))
        self.write_board(self.heading('GẶP NHAU'), self.M('meet', 1.05), frac=.12)
        self.wait_until(.4, t0)
        self.play(FadeIn(area(a, lambda v: 20, 0, 20, GOLD, .3)), run_time=self.rt(.06))
        self.play(FadeIn(area(a, lambda v: 2 * v, 0, 20, CYAN, .35)), run_time=self.rt(.06))
        self.write_board(self.TM('diện tích vàng $=$ diện tích xanh: $400 = 400$', 22, WHITE), frac=.08)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.vt_axes(22, 44, (10, 20), (20, 40), h=4.6, center=[LEFT_CX, -.2, 0])
        self.play(Create(clipped(a, lambda v: 20, 0, 21.5, GOLD, 4)), Create(clipped(a, lambda v: 2 * v, 0, 21.5, CYAN, 4)),
                  run_time=self.rt(.05))
        self.write_board(self.heading('GIAO ĐIỂM HAI ĐỒ THỊ VẬN TỐC'), frac=.04)
        self.wait_until(.2, t0)
        self.play(FadeIn(band(a, lambda v: 20, lambda v: 2 * v, 0, 10, GREEN, .45)), run_time=self.rt(.06))
        self.write_board(self.TM('trước $t = 10$: A nhanh hơn, khoảng cách tăng', 21, GREEN), frac=.06)
        self.wait_until(.45, t0)
        self.play(FadeIn(band(a, lambda v: 2 * v, lambda v: 20, 10, 20, CORAL, .45)), run_time=self.rt(.06))
        self.write_board(self.TM('sau $t = 10$: B nhanh hơn, khoảng cách giảm', 21, CORAL), frac=.06)
        self.wait_until(.7, t0)
        m = self.M('gap', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_c4(self, T):
        self.worked(self.now(), 'BÀI TOÁN PHANH XE', ('brake1', 'brake2'), (.2, .5), (1.4, 1.4), gap=.7)

    def beat_c5(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'ĐƠN VỊ VÀ THỜI GIAN PHẢN XẠ', ('kmh',), (.05,), (1.6,), box_last=False)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.TM('trong thời gian phản xạ: xe vẫn chạy đều với $v_0$', 25, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH 4 BƯỚC', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Gốc, chiều', 'mốc tọa độ và thời gian', CYAN), ('Vận tốc', 'xe nào xuất phát muộn?', GOLD),
                 ('Vị trí', 'tích phân của vận tốc', GREEN), ('Giải', 'loại nghiệm không phù hợp', CORAL))
        for i, ((title, desc, col), frac) in enumerate(zip(steps, (.05, .25, .5, .7))):
            c = card(3.0, 3.0, col).move_to([-4.65 + 3.1 * i, -.2, 0])
            g = VGroup(c, tx(str(i + 1), 50, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 24, WHITE, bold=True).move_to(c.get_center() + DOWN * .1),
                       tx(desc, 17, SOFT, max_w=2.7).move_to(c.get_bottom() + UP * .55))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.vt_axes(22, 44, (10, 20), (20, 40))
        self.play(Create(clipped(a, lambda v: 20, 0, 21.5, GOLD, 4)), Create(clipped(a, lambda v: 2 * v, 0, 21.5, CYAN, 4)),
                  run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 1', GOLD, 20), self.M('e1_s1', 1.05), frac=.12)
        self.wait_until(.3, t0)
        self.race(lambda v: 20 * v, lambda v: v * v, 20, 400, .35)
        m = self.M('e1_s2', 1.1)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.vt_axes(22, 44, (10, 20), (20, 40), h=4.6, center=[LEFT_CX, -.2, 0])
        self.play(Create(clipped(a, lambda v: 20, 0, 21.5, GOLD, 4)), Create(clipped(a, lambda v: 2 * v, 0, 21.5, CYAN, 4)),
                  run_time=self.rt(.05))
        self.write_board(self.heading('KHOẢNG CÁCH LỚN NHẤT'), frac=.04)
        self.wait_until(.3, t0)
        m = self.M('e2_s1', 1.1)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.6, t0)
        self.play(FadeIn(band(a, lambda v: 20, lambda v: 2 * v, 0, 10, GREEN, .5)), run_time=self.rt(.08))
        self.write_board(self.TM('phần giữa hai đồ thị trên $[0; 10]$: $100$ m', 22, GREEN), frac=.06)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.vt_axes(5, 24, (1, 2, 3, 4), (10, 20))
        self.play(Create(clipped(a, lambda v: 20 - 5 * v, 0, 4, CORAL, 4.5)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 2: PHANH XE', GOLD, 20), self.M('e3_s1', 1.0), frac=.12)
        self.wait_until(.4, t0)
        self.play(FadeIn(area(a, lambda v: 20 - 5 * v, 0, 4, CORAL, .45)), run_time=self.rt(.06))
        to_x = self.road(40)
        tt = ValueTracker(0)
        c = car(CORAL, .55)
        c.add_updater(lambda m: m.move_to([to_x(20 * tt.get_value() - 2.5 * tt.get_value() ** 2), ROAD_Y + .25, 0]))
        self.add(c)
        self.play(tt.animate.set_value(4), run_time=self.rt(.2), rate_func=linear)
        c.clear_updaters()
        m = self.M('e3_s2', 1.2)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        to_x = self.road(60)
        obstacle = VGroup(Line([to_x(50), ROAD_Y, 0], [to_x(50), ROAD_Y + 1.0, 0], color=CORAL, stroke_width=8),
                          self.TM('vật cản $50$ m', 18, CORAL).move_to([to_x(50), ROAD_Y + 1.3, 0]))
        self.play(FadeIn(obstacle), run_time=self.rt(.04))
        self.write_board(badge('VÍ DỤ 3: KHOẢNG CÁCH AN TOÀN', GOLD, 20),
                         self.TM('phản xạ $1$ s rồi phanh như ví dụ 2', 22, WHITE), frac=.1)
        pos = lambda v: 20 * v if v <= 1 else 20 + 20 * (v - 1) - 2.5 * (v - 1) ** 2  # noqa: E731
        tt = ValueTracker(0)
        c = car(GOLD, .55)
        c.add_updater(lambda m: m.move_to([to_x(pos(tt.get_value())), ROAD_Y + .25, 0]))
        self.add(c)
        self.wait_until(.3, t0)
        self.play(tt.animate.set_value(1), run_time=self.rt(.12), rate_func=linear)
        self.write_board(self.TM('phản xạ: $20 dot 1 = 20$ m', 22, SOFT), frac=.05)
        self.play(tt.animate.set_value(5), run_time=self.rt(.2), rate_func=linear)
        c.clear_updaters()
        m = self.M('e4_s1', 1.3)
        self.write_board(m, tx('va chạm!', 26, CORAL, bold=True), frac=.08)

    def beat_e5(self, T):
        self.worked(self.now(), 'MUỐN AN TOÀN: CẦN PHANH MẠNH HƠN', ('e5_s1',), (.25,), (1.35,))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        to_x = self.road(300)
        tt = ValueTracker(0)
        ca, cb = car(GOLD, .55), car(CYAN, .55).flip()
        ca.add_updater(lambda m: m.move_to([to_x(10 * tt.get_value()), ROAD_Y + .25, 0]))
        cb.add_updater(lambda m: m.move_to([to_x(300 - tt.get_value() ** 2), ROAD_Y + .25, 0]))
        self.add(ca, cb)
        self.write_board(badge('VÍ DỤ 4: NGƯỢC CHIỀU', GOLD, 20),
                         self.TM('cách nhau $300$ m, $v_A = 10$, $v_B = 2t$', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        tm = -5 + 5 * math.sqrt(13)
        self.play(tt.animate.set_value(tm), run_time=self.rt(.3), rate_func=linear)
        for m in (ca, cb):
            m.clear_updaters()
        m = self.M('e6_s1', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.vt_axes(10, 34, (2, 4, 6, 8), (10, 20, 30))
        self.play(Create(clipped(a, lambda v: 10, 0, 9.8, GOLD, 4)),
                  Create(clipped(a, lambda v: 4 * (v - 2), 2, 9.8, CYAN, 4, y_max=34)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 5: XUẤT PHÁT LỆCH GIỜ', GOLD, 20),
                         self.TM('$v_A = 10$; B xuất phát sau $2$ s', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        self.write_board(self.M('late1', .95), frac=.12)
        tm = (9 + math.sqrt(65)) / 2
        self.race(lambda v: 10 * v, lambda v: 2 * max(0.0, v - 2) ** 2, tm, 90, .25)
        m = self.M('late2', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Hai xe xuất phát cùng lúc, cùng chỗ:', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.35), VGroup(self.M('tf_b', 1.35), tx('(B đuổi kịp A)', 22, SOFT)).arrange(RIGHT, buff=.2),
                 VGroup(tx('Khoảng cách lớn nhất', 24, WHITE), self.M('tf_c', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.4, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        sol = VGroup(tx('b)', 22, SOFT), self.M('tf_b_calc', 1.1)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.75, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(1, False), run_time=self.rt(.1))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.75, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(3, True), run_time=self.rt(.1))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        q1 = self.TM('Ô tô chạy $54$ km/h thì người lái thấy vật cản.', 25, WHITE)
        q2 = self.TM('Sau $0,5$ s phản xạ, xe phanh với $v = 15 - 5t$ (m/s).'.replace('0,5', '"0,5"'), 25, WHITE)
        q3 = tx('Tổng quãng đường từ lúc thấy vật cản đến khi dừng (m)?', 25, GOLD, bold=True)
        self.centre(tag, q1, q2, q3, top=2.3, gap=.45)
        self.play(FadeIn(tag), FadeIn(q1), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(q2), run_time=self.rt(.06))
        self.wait_until(.75, t0)
        self.play(FadeIn(q3), run_time=self.rt(.05))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s1, s2 = self.M('sa_s1', 1.25), self.M('sa_s2', 1.15)
        sheet = self.answer_sheet('30')
        self.centre(s1, s2, sheet, top=2.0, gap=.75)
        self.play(Write(s1), run_time=self.rt(.12))
        self.wait_until(.35, t0)
        self.play(Write(s2), run_time=self.rt(.14))
        self.wait_until(.75, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.05))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Vị trí', 'sum1', 'Vị trí đầu cộng tích phân vận tốc'),
                                ('Gặp nhau', 'sum2', 'Giao điểm đồ thị: khoảng cách lớn nhất'),
                                ('Phanh xe', 'sum3', 'Cộng thêm quãng đường phản xạ')),
                           fracs=(.04, .3, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Đuổi kịp:', 'hw1'), ('Phanh:', 'hw2'), ('Cách xa nhất:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .4, .62))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Cổng parabol · logo · mảnh vườn · chi phí', 26, GOLD, bold=True), self.M('next1', 1.3)])


class INT29_SMOKE(INT29):
    smoke = True
