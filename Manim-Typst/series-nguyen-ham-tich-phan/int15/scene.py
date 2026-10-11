"""INT15 – Tích phân, độ dời và quãng đường.

    python scripts/build_typst.py --ep int15
    python scripts/prepare_voice.py --ep int15 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int15/scene.py INT15
    python scripts/finalize.py --ep int15

One method per narration beat (int15/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Line, Transform, ValueTracker, VGroup,
                   Write, always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, car, check, clipped, cross, dashed, signed_area, tx, vn  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def vel(t):
    return t * t - 4 * t + 3


def pos(t):
    return t ** 3 / 3 - 2 * t * t + 3 * t


class INT15(LessonScene):
    EP = 'int15'

    def ax(self, xr, yr, xt, yt, **kw):
        kw.setdefault('x_label', 't')
        kw.setdefault('y_label', 'v')
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=xt, y_ticks=yt, **kw)

    def road(self, y, x0, x1, marks):
        """Number line for positions (metres); returns (group, metre → scene x)."""
        to_x = lambda m: x0 + (x1 - x0) * (m - marks[0][0]) / (marks[-1][0] - marks[0][0])  # noqa: E731
        g = VGroup(Line([x0 - .4, y, 0], [x1 + .4, y, 0], color=SOFT, stroke_width=3))
        for m, label in marks:
            g.add(Line([to_x(m), y - .1, 0], [to_x(m), y + .1, 0], color=SOFT, stroke_width=2),
                  tx(label, 20, SOFT).move_to([to_x(m), y - .38, 0]))
        return g, to_x

    def v_axes(self):
        a = self.ax((0, 4.4, 1), (-1.4, 3.4, 1), (1, 2, 3, 4), (-1, 1, 2, 3))
        self.show_axes(a)
        self.play(Create(clipped(a, vel, 0, 4.2, CYAN, 4.5)), run_time=self.rt(.06))
        return a

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        v = self.M('hook_v', 1.45)
        road, to_x = self.road(-.1, -4.5, 4.5, [(0, '0'), (4 / 3, '4/3 m')])
        d = VGroup(tx('Cách vị trí ban đầu', 26, CYAN, bold=True), self.M('h_d', 1.5)).arrange(RIGHT, buff=.35)
        s = VGroup(tx('Đã đi tổng cộng', 26, GOLD, bold=True), self.M('h_s', 1.5)).arrange(RIGHT, buff=.35)
        self.centre(v, top=2.6)
        VGroup(d, s).arrange(DOWN, buff=.35, aligned_edge=LEFT).move_to([0, -2.0, 0])
        self.play(Write(v), FadeIn(road), run_time=self.rt(.1))
        tau = ValueTracker(0)
        c = car(CORAL, .7).move_to([to_x(0), .25, 0])
        c.add_updater(lambda m: m.move_to([to_x(pos(tau.get_value())), .25, 0]))
        self.add(c)
        self.play(tau.animate.set_value(4), run_time=self.rt(.3), rate_func=linear)
        c.clear_updaters()
        self.wait_until(.38, t0)
        self.play(FadeIn(d, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.play(FadeIn(s, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('gấp 3 lần?', 28, CORAL, bold=True).next_to(s, RIGHT, buff=.5)), run_time=self.rt(.05))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Độ dời', 'Tích phân của vận tốc'),
                         ('Quãng đường', 'Tích phân của trị tuyệt đối vận tốc'),
                         ('Gia tốc', 'Tích phân cho độ thay đổi vận tốc')], t0, fracs=(.15, .4, .68))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 4.4, 1), (-.4, 2.0, 1), (1, 2, 3, 4), (1,), y_label='s')
        self.show_axes(a)
        self.play(Create(clipped(a, pos, 0, 4.2, PURPLE, 4.5)), run_time=self.rt(.08))
        self.write_board(self.heading('TỌA ĐỘ VÀ VẬN TỐC'), self.M('pos', 1.2),
                         tx('vận tốc = đạo hàm của tọa độ', 22, SOFT), frac=.14)
        self.wait_until(.45, t0)
        self.write_board(self.heading('ĐỘ DỜI'), self.M('disp', 1.25), frac=.12)
        self.wait_until(.75, t0)
        self.play(Create(dashed(a.c2p(0, 4 / 3), a.c2p(4, 4 / 3), color=GOLD)),
                  FadeIn(tx('s(4) − s(0) = 4/3', 20, GOLD, bold=True).move_to(a.c2p(2, 1.65))), run_time=self.rt(.08))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        road, to_x = self.road(-.6, -4.8, 4.8, [(0, '0'), (2 / 3, '2/3'), (4 / 3, '4/3')])
        self.play(Create(road), run_time=self.rt(.05))
        tau = ValueTracker(0)
        c = car(CORAL, .75)
        c.add_updater(lambda m: m.move_to([to_x(pos(tau.get_value())), -.2, 0]))
        info = always_redraw(lambda: tx(f't = {vn(tau.get_value(), 1)} s     v = {vn(vel(tau.get_value()), 2)} m/s',
                                        24, WHITE).move_to([0, -2.2, 0]))
        self.add(c, info)
        legs = ((1, .3, GREEN, 1.0, 'tiến 4/3 m'), (3, .66, CORAL, 1.7, 'lùi 4/3 m'), (4, .92, GREEN, 2.4, 'tiến 4/3 m'))
        start = 0
        for t_end, frac, col, y, label in legs:
            self.play(tau.animate.set_value(t_end), run_time=max(t0 + (frac - .04) * T - self.now(), .1),
                      rate_func=linear)
            p, q = to_x(pos(start)), to_x(pos(t_end))
            arr = Arrow([p, y, 0], [q, y, 0], buff=0, color=col, stroke_width=6)
            self.play(FadeIn(arr), FadeIn(tx(label, 20, col, bold=True).next_to(arr, UP, buff=.05)),
                      run_time=self.rt(.03))
            start = t_end
        c.clear_updaters()
        info.clear_updaters()

    def beat_c2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 4.4, 1), (-.4, 2.0, 1), (1, 2, 3, 4), (1,), y_label='s')
        self.show_axes(a)
        self.play(Create(clipped(a, pos, 0, 4.2, PURPLE, 4.5)), run_time=self.rt(.08))
        self.write_board(self.heading('ĐỔI CHIỀU = CỰC TRỊ CỦA s'), frac=.05)
        self.wait_until(.3, t0)
        for tt, col in ((1, GREEN), (3, CORAL)):
            self.play(FadeIn(dot_at(a, tt, pos(tt))), Create(dashed(a.c2p(tt, 0), a.c2p(tt, pos(tt)), color=col)),
                      run_time=self.rt(.05))
        self.write_board(self.M('e1_s1', 1.15), frac=.1)
        self.wait_until(.7, t0)
        self.write_board(tx('v = 0 và đổi dấu  →  chất điểm đổi chiều', 23, GOLD, bold=True), frac=.07)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.v_axes()
        parts = signed_area(a, vel, 0, 4, opacity=.5)
        self.play(FadeIn(parts), run_time=self.rt(.05))
        self.write_board(self.heading('DIỆN TÍCH CÓ DẤU = ĐỘ DỜI'), self.M('e1_d', 1.3), frac=.12)
        self.wait_until(.5, t0)
        neg = [p for p in parts if p.get_center()[1] < a.c2p(0, 0)[1]]
        up = area(a, lambda v: -vel(v), 1, 3, GREEN, .5)
        self.play(Transform(neg[0], up), *[FadeOut(p) for p in neg[1:]],
                  Create(clipped(a, lambda v: -vel(v), 1, 3, GOLD, 4)), run_time=self.rt(.1))
        self.write_board(self.heading('QUÃNG ĐƯỜNG', GREEN), self.M('dist', 1.3), self.M('e1_s', 1.3), frac=.14)

    def beat_c4(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'ĐỘ DỜI VÀ QUÃNG ĐƯỜNG', ('ineq',), (.05,), (1.6,), box_last=False)
        ok = VGroup(check(GREEN, .3), tx('v không đổi dấu: hai đại lượng có độ lớn bằng nhau', 25, GREEN))
        warn = VGroup(cross(CORAL, .28), tx('v đổi dấu (đổi chiều): giải v = 0, xét dấu, tách cận', 25, CORAL, bold=True))
        for m in (ok, warn):
            m.arrange(RIGHT, buff=.25)
        VGroup(ok, warn).arrange(DOWN, buff=.45, aligned_edge=LEFT).next_to(lines[-1], DOWN, buff=.7)
        self.wait_until(.12, t0)
        self.play(FadeIn(ok, shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.06))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 6.5, 1), (-1.5, 6.5, 1), (1, 2, 3, 4, 5, 6), (2, 4, 6), y_label='a')
        self.show_axes(a)
        self.play(Create(clipped(a, lambda u: 6 - 2 * u, 0, 6.5, CYAN, 4.5)), run_time=self.rt(.06))
        self.write_board(self.heading('GIA TỐC → VẬN TỐC'), self.M('vel', 1.15), frac=.12)
        self.wait_until(.35, t0)
        self.play(FadeIn(area(a, lambda u: 6 - 2 * u, 1, 3, GOLD, .45)),
                  FadeIn(self.M('dv', 1.0).move_to(a.c2p(4.6, 2.6))), run_time=self.rt(.07))
        self.wait_until(.6, t0)
        m = self.M('vel2', 1.25)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'KIỂM TRA BẰNG ĐƠN VỊ', ('units',), (.1,), (1.6,), box_last=False)
        rows = VGroup(tx('Diện tích dưới đồ thị v – t  →  quãng đường, độ dời (m)', 25, CYAN),
                      tx('Diện tích dưới đồ thị a – t  →  độ thay đổi vận tốc (m/s)', 25, GOLD)) \
            .arrange(DOWN, buff=.4, aligned_edge=LEFT).next_to(lines[-1], DOWN, buff=.8)
        self.wait_until(.3, t0)
        self.play(FadeIn(rows[0], shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.play(FadeIn(rows[1], shift=UP * .1), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(FadeIn(tx('Đơn vị không khớp  →  chọn sai hàm!', 26, CORAL, bold=True)
                         .next_to(rows, DOWN, buff=.55)), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = badge('VÍ DỤ 1', GOLD, 20)
        s1 = self.M('e1_s1', 1.3)
        table = self.sign_table(['0', '1', '3', '4'], ['+', '−', '+'], label='v(t)', width=6.4, var='t')
        s2 = self.M('e1_s2', 1.1)
        res = VGroup(self.M('e1_d', 1.3), self.M('e1_s', 1.3)).arrange(RIGHT, buff=1.2)
        self.centre(tag, s1, table, s2, res, top=2.75, gap=.33)
        self.play(FadeIn(tag), Write(s1), run_time=self.rt(.1))
        self.wait_until(.25, t0)
        self.play(FadeIn(table), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.play(Write(s2), run_time=self.rt(.12))
        self.wait_until(.68, t0)
        self.play(Write(res[0]), run_time=self.rt(.08))
        self.wait_until(.85, t0)
        self.play(Write(res[1]), FadeIn(self.box(res[1], GREEN)), run_time=self.rt(.08))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 6.6, 1), (-2, 10.5, 2), (1, 2, 3, 4, 5, 6), (2, 4, 6, 8, 10), y_label='')
        self.show_axes(a)
        self.e2_axes = a
        self.write_board(badge('VÍ DỤ 2', GOLD, 20), self.M('e2_a', 1.3), frac=.1)
        self.play(Create(clipped(a, lambda u: 6 - 2 * u, 0, 6.6, CYAN, 3.5)),
                  FadeIn(tx('a(t)', 20, CYAN, bold=True).move_to(a.c2p(.45, 7.4))), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.write_board(self.M('e2_v', 1.15), frac=.12)
        self.play(Create(clipped(a, lambda u: 6 * u - u * u, 0, 6.3, GOLD, 4.5)),
                  FadeIn(tx('v(t)', 20, GOLD, bold=True).move_to(a.c2p(3, 9.8))), run_time=self.rt(.08))
        self.wait_until(.72, t0)
        self.write_board(self.M('e2_stop', 1.3), frac=.08)
        self.play(FadeIn(dot_at(a, 6, 0)), run_time=self.rt(.03))

    def beat_e3(self, T):
        t0 = self.now()
        a = self.e2_axes
        self.clear_board(.03)
        self.play(FadeIn(area(a, lambda u: 6 * u - u * u, 0, 6, GOLD, .4)), run_time=self.rt(.08))
        self.write_board(badge('QUÃNG ĐƯỜNG ĐẾN KHI DỪNG', GREEN, 19), frac=.05)
        self.wait_until(.2, t0)
        m = self.M('e3_s', 1.1)
        self.write_board(m, frac=.16)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.write_board(tx('v ≥ 0 trên [0; 6]: không cần tách cận', 22, SOFT), frac=.06)

    def beat_e3b(self, T):
        t0 = self.now()
        a = self.e2_axes
        self.clear_board(.03)
        self.write_board(badge('HAI CÂU HỎI THƯỜNG GẶP', GOLD, 19), frac=.04)
        self.wait_until(.08, t0)
        self.play(FadeIn(dot_at(a, 3, 9)), Create(dashed(a.c2p(3, 0), a.c2p(3, 9), color=GOLD)), run_time=self.rt(.05))
        self.write_board(self.M('vmax', 1.15), frac=.1)
        self.wait_until(.45, t0)
        self.play(Create(dashed(a.c2p(0, 6), a.c2p(6, 6), color=GREEN)), run_time=self.rt(.05))
        self.write_board(self.M('vavg', 1.25), frac=.1)
        self.wait_until(.75, t0)
        self.write_board(tx('Tốc độ trung bình ≠ trung bình cộng các vận tốc', 21, CORAL, bold=True), frac=.06)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 12.8, 2), (0, 12.5, 2), (2, 4, 6, 8, 10, 12), (5, 10), y_label='v')
        self.show_axes(a)
        g = lambda u: 2.5 * u if u <= 4 else (10 if u <= 10 else 10 - 5 * (u - 10))  # noqa: E731
        self.play(Create(clipped(a, g, 0, 12, CYAN, 4.5)), run_time=self.rt(.1))
        self.write_board(badge('VÍ DỤ 3', GOLD, 20), tx('Tăng tốc 4 s · chạy đều 6 s · phanh 2 s', 22, WHITE), frac=.1)
        self.wait_until(.42, t0)
        for (x0, x1, col, lab, lx) in ((0, 4, GREEN, '20', 2.8), (4, 10, GOLD, '60', 7), (10, 12, PURPLE, '10', 10.7)):
            self.play(FadeIn(area(a, g, x0, x1, col, .45)),
                      FadeIn(tx(lab, 24, col, bold=True).move_to(a.c2p(lx, 4))), run_time=self.rt(.05))
        self.wait_until(.7, t0)
        m = self.M('e4_s', 1.5)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.write_board(tx('Diện tích hình thang – không cần công thức v(t)', 21, SOFT), frac=.05)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Một chất điểm có', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.35),
                 VGroup(tx('Quãng đường đi được', 24, WHITE), self.M('tf_b', 1.35)).arrange(RIGHT, buff=.2),
                 VGroup(tx('Chất điểm đổi chiều tại', 24, WHITE), self.M('tf_c', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_d', 1.35))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        sol = VGroup(tx('b)', 22, SOFT), self.M('tf_b_calc', .95)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(1, False), run_time=self.rt(.1))
        self.x2_sol = sol

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        sol = VGroup(tx('d)', 22, SOFT), self.M('tf_d_calc', 1.15)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(self.x2_sol), FadeIn(sol), self.tf_mark(3, False), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        q1 = tx('Ô tô đang chạy 15 m/s thì phanh, sau đó vận tốc là', 25, WHITE)
        task = self.M('sa_task', 1.5)
        q2 = tx('Từ lúc phanh đến khi dừng hẳn, ô tô đi thêm bao nhiêu mét?', 25, GOLD, bold=True)
        self.centre(tag, q1, task, q2, top=2.65, gap=.35)
        self.play(FadeIn(tag), FadeIn(q1), run_time=self.rt(.08))
        self.play(Write(task), run_time=self.rt(.1))
        road, to_x = self.road(-2.4, -4.8, 4.8, [(0, '0'), (37.5, '?')])
        self.play(Create(road), run_time=self.rt(.04))
        tau = ValueTracker(0)
        c = car(CORAL, .75)
        c.add_updater(lambda m: m.move_to([to_x(15 * tau.get_value() - 1.5 * tau.get_value() ** 2), -1.8, 0]))
        self.add(c)
        self.play(tau.animate.set_value(5), run_time=self.rt(.45), rate_func=linear)
        c.clear_updaters()
        self.wait_until(.72, t0)
        self.play(FadeIn(q2, shift=UP * .1), run_time=self.rt(.06))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s1, s2 = self.M('sa_s1', 1.45), self.M('sa_s2', 1.35)
        sheet = self.answer_sheet('37,5')
        warn = VGroup(cross(CORAL, .26), tx('Bẫy: cận trên phải là thời điểm dừng (v = 0)', 23, CORAL, bold=True)) \
            .arrange(RIGHT, buff=.2)
        self.centre(s1, s2, sheet, warn, top=2.5, gap=.55)
        self.play(Write(s1), run_time=self.rt(.08))
        self.wait_until(.12, t0)
        self.play(Write(s2), run_time=self.rt(.14))
        self.wait_until(.5, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.06))
        self.wait_until(.72, t0)
        self.play(FadeIn(warn, shift=UP * .1), run_time=self.rt(.06))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Độ dời', 'sum1', 'Diện tích có dấu dưới đồ thị v'),
                                ('Quãng đường', 'sum2', 'Xét dấu v, tách cận tại lúc đổi chiều'),
                                ('Gia tốc', 'sum3', 'Vận tốc ban đầu cộng tích phân của a')),
                           fracs=(.04, .33, .68))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Cho', 'hw1'), ('Cho', 'hw2'), ('Cho', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.1)])


def dot_at(a, x0, y0):
    from common.kit import dot
    return dot(a, x0, y0, GOLD, .09)


class INT15_SMOKE(INT15):
    smoke = True
