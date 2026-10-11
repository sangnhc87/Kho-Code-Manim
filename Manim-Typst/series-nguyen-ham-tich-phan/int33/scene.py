"""INT33 – Mô hình hóa từ dữ liệu thực: bảng số → hàm số → tích phân.

    python scripts/build_typst.py --ep int33
    python scripts/prepare_voice.py --ep int33 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int33/scene.py INT33
    python scripts/finalize.py --ep int33

One method per narration beat (int33/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M`` / ``self.TM``).
Every number is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, Polygon, ValueTracker, VGroup, always_redraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, card, clipped, dashed, dot, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

T_DATA = (0, 2, 4, 6, 8)
V_DATA = (0, 6, 10, 12, 12)


def model(v):
    return -v * v / 4 + 3.5 * v


class INT33(LessonScene):
    EP = 'int33'

    def data_axes(self, xs, ys, xr, yr, xt, yt, xl='t', yl='v', color=GOLD):
        a = axes(xr, yr, 6.0, 4.8, center=[LEFT_CX, -.2, 0], x_ticks=xt, y_ticks=yt, x_label=xl, y_label=yl)
        self.show_axes(a)
        pts = VGroup(*[dot(a, xv, yv, color, .09) for xv, yv in zip(xs, ys)])
        self.play(FadeIn(pts), run_time=self.rt(.05))
        return a, pts

    def trapezoids(self, a, xs, ys, color=PURPLE):
        g = VGroup()
        for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
            g.add(Polygon(a.c2p(x0, 0), a.c2p(x0, y0), a.c2p(x1, y1), a.c2p(x1, 0), stroke_color=WHITE, stroke_width=1.5,
                          fill_color=color, fill_opacity=.45))
        return g

    def table(self, header, rows_t, rows_v, label_t='t', label_v='v'):
        """Small data table, every entry typeset."""
        cells = VGroup()
        for r, (lab, vals) in enumerate(((label_t, rows_t), (label_v, rows_v))):
            row = VGroup(self.TM(f'${lab}$', 22, SOFT), *[self.TM('$' + (f'"{v}"' if ',' in str(v) else str(v)) + '$', 22,
                                                                   WHITE if r else GOLD) for v in vals])
            for k, m in enumerate(row):
                m.move_to([k * .85, -r * .6, 0])
            cells.add(row)
        box = VGroup(Line([-.45, -.3, 0], [len(rows_t) * .85 + .45, -.3, 0], color=SOFT, stroke_width=2),
                     Line([.42, .3, 0], [.42, -.9, 0], color=SOFT, stroke_width=2))
        return VGroup(cells, box)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        tb = self.table('', T_DATA, V_DATA).move_to([0, 1.8, 0])
        self.play(FadeIn(tb), run_time=self.rt(.1))
        self.wait_until(.3, t0)
        self.play(FadeIn(self.TM('Xe đi được bao xa trong $8$ giây?', 28, GOLD, bold=True).move_to([0, .4, 0])), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        cards = VGroup(*[VGroup(card(5.0, 1.6, col), tx(title, 24, col, bold=True)) for title, col in
                         (('tìm hàm số khớp dữ liệu', CYAN), ('cộng các hình thang', PURPLE))]).arrange(RIGHT, buff=.6) \
            .move_to([0, -1.6, 0])
        for c in cards:
            c[1].move_to(c[0])
        self.play(FadeIn(cards, shift=UP * .15), run_time=self.rt(.08))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Mô hình hóa', 'Từ bảng số đến hàm số'),
                         ('Quy tắc hình thang', 'Khi không có công thức'),
                         ('Nhiều bước', 'Câu trả lời ngắn')], t0, fracs=(.1, .35, .6))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH MÔ HÌNH HÓA', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Dữ liệu', CYAN), ('Dạng hàm', GOLD), ('Hệ số', GREEN), ('Tích phân', PURPLE), ('Kiểm tra', CORAL))
        for i, ((title, col), frac) in enumerate(zip(steps, (.05, .2, .45, .62, .75))):
            c = card(2.35, 2.4, col).move_to([-4.9 + 2.45 * i, -.1, 0])
            g = VGroup(c, tx(str(i + 1), 46, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 21, WHITE, bold=True, max_w=2.1).move_to(c.get_center() + DOWN * .3))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))
        self.wait_until(.88, t0)
        self.play(FadeIn(self.M('steps', .9).move_to([0, -2.25, 0])), run_time=self.rt(.04))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.write_board(self.heading('TÌM HỆ SỐ'), self.TM('mỗi điểm dữ liệu: một phương trình', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        self.play(*[pts[k].animate.scale(1.6).set_color(CYAN) for k in (1, 2)], run_time=self.rt(.05))
        m = self.M('fit_sys', 1.0)
        self.write_board(m, frac=.12)
        self.wait_until(.7, t0)
        self.write_board(self.TM('các điểm còn lại: kiểm tra mô hình', 22, SOFT), frac=.05)

    def beat_c2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.write_board(self.heading('CHỌN DẠNG HÀM'), frac=.03)
        steps = VGroup()
        for (x0, y0), (x1, y1) in zip(zip(T_DATA, V_DATA), zip(T_DATA[1:], V_DATA[1:])):
            steps.add(dashed(a.c2p(x0, y0), a.c2p(x1, y0), color=SOFT, stroke_width=2),
                      Line(a.c2p(x1, y0), a.c2p(x1, y1), color=CORAL, stroke_width=4))
        self.play(Create(steps), run_time=self.rt(.08))
        self.write_board(self.M('diffs', 1.0), frac=.06)
        for key, frac, col in (('form_lin', .3, SOFT), ('form_quad', .45, GOLD), ('form_exp', .62, SOFT)):
            self.wait_until(frac, t0)
            m = self.M(key, .85)
            self.write_board(m, frac=.05)
            if col == GOLD:
                self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))
        self.wait_until(.82, t0)
        self.write_board(self.TM('$v(0) = 0 arrow.r.double c = 0$', 24, GREEN), frac=.05)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.write_board(self.heading('QUY TẮC HÌNH THANG'), frac=.04)
        self.wait_until(.15, t0)
        tz = self.trapezoids(a, T_DATA, V_DATA)
        from manim import LaggedStart
        self.play(LaggedStart(*[FadeIn(p) for p in tz], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        m = self.M('trap', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.play(FadeIn(self.trapezoids(a, T_DATA, V_DATA)), run_time=self.rt(.05))
        self.write_board(self.heading('SAI SỐ'), self.TM('hàm bậc nhất: hình thang chính xác', 22, GREEN), frac=.1)
        self.wait_until(.3, t0)
        self.play(Create(clipped(a, model, 0, 8.5, CYAN, 4)), run_time=self.rt(.08))
        self.write_board(self.TM('đồ thị cong xuống: hình thang hơi thiếu', 22, CYAN), frac=.06)
        self.wait_until(.7, t0)
        self.write_board(self.TM('đo dày hơn: sai số nhỏ hơn', 22, GOLD), frac=.05)

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        cards = []
        for i, (title, notes, col) in enumerate((('MÔ HÌNH HÀM SỐ', ('có công thức', 'dự đoán được'), CYAN),
                                                ('QUY TẮC HÌNH THANG', ('không cần dạng hàm', 'chỉ cần bảng số'), PURPLE))):
            c = card(5.9, 3.0, col).move_to([-3.1 + 6.2 * i, .3, 0])
            cards.append(VGroup(c, tx(title, 24, col, bold=True).move_to(c.get_top() + DOWN * .5),
                                VGroup(*[tx(n, 22, WHITE) for n in notes]).arrange(DOWN, buff=.25)
                                .move_to(c.get_center() + DOWN * .25)))
        self.play(FadeIn(cards[0], shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.3, t0)
        self.play(FadeIn(cards[1], shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('câu trả lời ngắn: làm tròn cẩn thận!', 25, GOLD, bold=True).move_to([0, -2.2, 0])),
                  run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.write_board(badge('VÍ DỤ 1: TÌM HÀM KHỚP', GOLD, 20), self.M('fit_sys', .95), frac=.1)
        self.wait_until(.45, t0)
        self.play(Create(clipped(a, model, 0, 8.5, CYAN, 4)), run_time=self.rt(.08))
        m = self.M('e1_s1', .95)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.play(Create(clipped(a, model, 0, 8.5, CYAN, 4)), run_time=self.rt(.05))
        self.wait_until(.15, t0)
        self.play(FadeIn(area(a, model, 0, 8, CYAN, .45)), run_time=self.rt(.06))
        m = self.M('e2_s1', 1.0)
        self.write_board(badge('QUÃNG ĐƯỜNG THEO MÔ HÌNH', GOLD, 20), m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e2b(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 15.5, 1), (0, 14, 1), (2, 4, 6, 8, 10, 12, 14), (6, 12))
        self.play(Create(clipped(a, model, 0, 8, CYAN, 4)), run_time=self.rt(.05))
        self.write_board(badge('DỰ ĐOÁN BẰNG MÔ HÌNH', GOLD, 20), frac=.04)
        self.wait_until(.12, t0)
        self.play(Create(clipped(a, model, 8, 14, CORAL, 4)), run_time=self.rt(.1))
        self.play(FadeIn(dot(a, 10, 10, CORAL, .1)), FadeIn(dot(a, 14, 0, CORAL, .1)), run_time=self.rt(.03))
        self.write_board(self.M('e2b_s1', 1.05), frac=.08)
        self.wait_until(.55, t0)
        self.play(FadeIn(dashed(a.c2p(8, 0), a.c2p(8, 13), color=GOLD, stroke_width=3)), run_time=self.rt(.03))
        self.write_board(self.TM('dữ liệu chỉ đến $t = 8$', 22, GOLD), self.TM('ngoại suy $t > 8$: cần kiểm chứng', 22, CORAL),
                         frac=.08)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a, pts = self.data_axes(T_DATA, V_DATA, (0, 9, 1), (0, 14, 1), (2, 4, 6, 8), (6, 12))
        self.play(FadeIn(self.trapezoids(a, T_DATA, V_DATA)), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 2: HÌNH THANG', GOLD, 20), frac=.04)
        self.wait_until(.2, t0)
        m = self.M('e3_s1', 1.1)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.65, t0)
        self.play(Create(clipped(a, model, 0, 8.5, CYAN, 3)), run_time=self.rt(.06))
        self.write_board(self.TM('$68 < "69,33"$: đồ thị cong xuống', 22, CYAN), frac=.05)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        xs, ys = (0, 1, 2, 3, 4), (0, 4, 10, 6, 2)
        a, pts = self.data_axes(xs, ys, (0, 4.6, 1), (0, 11.5, 1), (1, 2, 3, 4), (4, 8), yl='r', color=CYAN)
        self.write_board(badge('VÍ DỤ 3: LƯỢNG MƯA', GOLD, 20), self.TM('cường độ mưa (mm/h) đo mỗi giờ', 22, WHITE), frac=.1)
        self.wait_until(.35, t0)
        self.play(FadeIn(self.trapezoids(a, xs, ys, CYAN)), run_time=self.rt(.08))
        m = self.M('e4_s1', 1.15)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def channel_axes(self):
        xs, ys = (-2, -1, 0, 1, 2), (0, -1.2, -1.6, -1.2, 0)
        a = axes((-2.6, 2.6, 1), (-2.2, .6, 1), 6.0, 3.6, center=[LEFT_CX, .2, 0], x_ticks=(-2, -1, 1, 2), y_ticks=(-1,),
                 x_label='x', y_label='')
        self.show_axes(a)
        pts = VGroup(*[dot(a, xv, yv, GOLD, .09) for xv, yv in zip(xs, ys)])
        self.play(FadeIn(pts), run_time=self.rt(.05))
        return a

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.channel_axes()
        self.write_board(badge('VÍ DỤ 4: MẶT CẮT CON MƯƠNG', GOLD, 20), self.TM('độ sâu tại $x = -2, -1, 0, 1, 2$', 22, WHITE),
                         frac=.1)
        self.wait_until(.5, t0)
        self.play(Create(clipped(a, lambda v: -(1.6 - .4 * v * v), -2, 2, CYAN, 4)), run_time=self.rt(.08))
        self.write_board(self.M('e5_s1', .9), frac=.12)

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.channel_axes()
        f = lambda v: -(1.6 - .4 * v * v)  # noqa: E731
        self.play(Create(clipped(a, f, -2, 2, CYAN, 4)), FadeIn(area(a, f, -2, 2, CYAN, .45)), run_time=self.rt(.06))
        m = self.M('e6_s1', .95)
        self.write_board(m, frac=.12)
        self.wait_until(.35, t0)
        m2 = self.M('e6_s2', 1.1)
        self.write_board(m2, frac=.1)
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))
        self.wait_until(.75, t0)
        self.write_board(self.M('e6_s3', .95), frac=.08)

    def beat_e7(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((0, 4.6, 1), (0, 11.5, 1), 6.0, 4.8, center=[LEFT_CX, -.2, 0], x_ticks=(1, 2, 3, 4), y_ticks=(4, 8),
                 x_label='t', y_label='r')
        self.show_axes(a)
        at = ValueTracker(3)
        xs = (0, 1, 2, 3, 4)
        ys = lambda: (0, 4, at.get_value(), 6, 2)  # noqa: E731
        tz = always_redraw(lambda: self.trapezoids(a, xs, ys(), CYAN))
        pts = always_redraw(lambda: VGroup(*[dot(a, xv, yv, GOLD if k == 2 else CYAN, .09) for k, (xv, yv) in enumerate(zip(xs, ys()))]))
        self.play(FadeIn(tz), FadeIn(pts), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 5: SỐ LIỆU BỊ THIẾU', GOLD, 20),
                         self.TM('$r$: $0, 4, a, 6, 2$; tổng lượng mưa $19$ mm', 22, WHITE), frac=.1)
        rd = always_redraw(lambda: self.readout([('a', at.get_value(), 1), ('S', 11 + at.get_value(), 1)], 22)
                           .move_to([3.6, -2.4, 0]))
        self.add(rd)
        self.wait_until(.35, t0)
        m = self.M('e7_s1', .95)
        self.write_board(m, frac=.1)
        self.wait_until(.6, t0)
        self.play(at.animate.set_value(8), run_time=self.rt(.15))
        m2 = self.M('e7_s2', 1.1)
        self.write_board(m2, frac=.06)
        self.play(FadeIn(self.box(m2, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Vận tốc đo mỗi giây:', 24, WHITE), self.M('tf_given', 1.2)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (self.M('tf_a', 1.35), self.M('tf_b', 1.35), self.M('tf_c', 1.15), self.M('tf_d', 1.15))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        self.play(self.tf_mark(2, True), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.play(self.tf_mark(3, False), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐĐS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        xs, ys = (0, 5, 10, 15, 20), (10, 14, 20, 18, 12)
        a, pts = self.data_axes(xs, ys, (0, 22, 1), (0, 23, 1), (5, 10, 15, 20), (10, 20), yl='r', color=CYAN)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.0), self.TM('Lượng nước vào bể trong $20$ phút (lít)?', 22, GOLD, bold=True), frac=.14)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.trapezoids(a, xs, ys, CYAN)), run_time=self.rt(.08))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', 1.05), frac=.14)
        self.wait_until(.7, t0)
        self.write_board(self.answer_sheet('315'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Mô hình hóa', 'sum1', 'Tìm hệ số, kiểm tra với điểm còn lại'),
                                ('Hình thang', 'sum2', 'Khi chỉ có bảng số'),
                                ('Sai số', 'sum3', 'Đo dày hơn thì chính xác hơn')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Hình thang:', 'hw1'), ('Mô hình:', 'hw2'), ('Mương:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Phần E · Tổng ôn và luyện đề', 28, GOLD, bold=True), self.M('next1', 1.3)])


class INT33_SMOKE(INT33):
    smoke = True
