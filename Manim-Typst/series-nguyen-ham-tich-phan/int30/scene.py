"""INT30 – Tích phân trong thiết kế: cổng parabol, logo, mảnh vườn, chi phí.

    python scripts/build_typst.py --ep int30
    python scripts/prepare_voice.py --ep int30 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int30/scene.py INT30
    python scripts/finalize.py --ep int30

One method per narration beat (int30/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M`` / ``self.TM``).
Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, Dot, FadeIn, FadeOut, Line, Rectangle, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import area, axes, badge, band, card, clipped, dashed, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


def gate(v):
    return 6 - 3 / 8 * v * v


class INT30(LessonScene):
    EP = 'int30'

    def gate_axes(self, with_axes=True):
        a = axes((-5, 5, 1), (0, 7, 1), 6.0, 4.6, center=[LEFT_CX, -.3, 0], x_ticks=(-4, 4) if with_axes else (),
                 y_ticks=(6,) if with_axes else ())
        if with_axes:
            self.show_axes(a)
        ground = Line(a.c2p(-5, 0), a.c2p(5, 0), color=SOFT, stroke_width=4)
        arch = clipped(a, gate, -4, 4, GOLD, 9)
        self.play(FadeIn(ground), Create(arch), run_time=self.rt(.07))
        return a

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        a = self.gate_axes(with_axes=False)
        self.play(FadeIn(area(a, gate, -4, 4, GOLD, .35)), run_time=self.rt(.05))
        self.add(self.TM('$8$ m', 20, WHITE).move_to(a.c2p(0, -.5)),
                 self.TM('$6$ m', 20, WHITE).move_to(a.c2p(.7, 3)),
                 dashed(a.c2p(0, 0), a.c2p(0, 6), color=SOFT))
        self.write_board(self.heading('CỔNG CHÀO PARABOL'), self.TM('rộng $8$ m, cao $6$ m', 23, WHITE),
                         self.TM('sơn: $150 space 000$ đ / $"m"^2$', 23, WHITE), frac=.14)
        self.wait_until(.45, t0)
        self.write_board(tx('Chi phí = ?', 26, GOLD, bold=True), frac=.05)
        self.wait_until(.75, t0)
        m = self.M('hook', 1.15)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Đặt hệ trục', 'Gốc ở giữa, trục tung qua đỉnh'),
                         ('Công thức $2/3$', 'Diện tích miền parabol'),
                         ('Mô hình hóa', 'Từ hình vẽ đến chi phí')], t0, fracs=(.1, .38, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.gate_axes()
        self.write_board(self.heading('ĐẶT HỆ TRỤC'), self.TM('gốc $O$ ở giữa chân cổng', 22, WHITE),
                         self.TM('trục $O y$ đi qua đỉnh', 22, WHITE), frac=.12)
        self.wait_until(.55, t0)
        m = self.M('shape', 1.5)
        self.write_board(m, frac=.08)
        self.play(FadeIn(self.box(m, GOLD)), run_time=self.rt(.03))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.gate_axes()
        self.write_board(self.heading('TÌM HỆ SỐ'), self.TM('chân cổng: $(plus.minus 4; 0)$, đỉnh: $(0; 6)$', 22, WHITE),
                         frac=.1)
        self.wait_until(.3, t0)
        from common.kit import dot
        self.play(FadeIn(dot(a, -4, 0)), FadeIn(dot(a, 4, 0)), FadeIn(dot(a, 0, 6)), run_time=self.rt(.05))
        m = self.M('coef', .95)
        self.write_board(m, frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.gate_axes()
        self.play(FadeIn(area(a, gate, -4, 4, GOLD, .45)), run_time=self.rt(.05))
        self.write_board(self.M('area', 1.0), frac=.12)
        self.wait_until(.45, t0)
        rect = Rectangle(width=abs(a.c2p(4, 0)[0] - a.c2p(-4, 0)[0]), height=abs(a.c2p(0, 6)[1] - a.c2p(0, 0)[1]),
                         color=CYAN, stroke_width=3).move_to(a.c2p(0, 3))
        self.play(Create(rect), run_time=self.rt(.06))
        m = self.M('arch', 1.3)
        self.write_board(self.heading('ARCHIMEDES'), m, self.TM('miền parabol $= 2/3$ hình chữ nhật bao quanh', 21, CYAN),
                         frac=.14)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_c3b(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CHỨNG MINH TỔNG QUÁT', ('gen',), (.2,), (1.35,))
        self.wait_until(.7, t0)
        self.play(FadeIn(self.TM('đúng với mọi cổng parabol rộng $w$, cao $h$', 26, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('QUY TRÌNH MÔ HÌNH HÓA', 26, GOLD, bold=True).move_to([0, 2.55, 0])), run_time=self.rt(.04))
        steps = (('Hệ trục', CYAN), ('Phương trình', GOLD), ('Cận', GREEN), ('Tích phân', PURPLE), ('Đơn giá', CORAL))
        for i, ((title, col), frac) in enumerate(zip(steps, (.08, .2, .32, .45, .6))):
            c = card(2.35, 2.4, col).move_to([-4.9 + 2.45 * i, -.1, 0])
            g = VGroup(c, tx(str(i + 1), 46, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(title, 21, WHITE, bold=True, max_w=2.1).move_to(c.get_center() + DOWN * .3))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = badge('BA LỖI THƯỜNG GẶP', CORAL, 20)
        rows = (self.TM('cận: $-4$ đến $4$ khi gốc ở giữa, không phải $0$ đến $8$', 25, WHITE),
                self.TM('nhầm đơn vị: $1 "dm"^2 = 1/100 "m"^2$', 25, WHITE),
                tx('làm tròn quá sớm làm sai đáp số cuối', 25, WHITE))
        self.centre(head, *rows, top=1.9, gap=.6)
        self.play(FadeIn(head), run_time=self.rt(.04))
        for frac, r in zip((.1, .45, .68), rows):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1: CHI PHÍ SƠN CỔNG', ('area', 'cost'), (.05, .4), (1.2, 1.1), gap=.7)

    def beat_e2(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.gate_axes()
        door = Rectangle(width=abs(a.c2p(2, 0)[0] - a.c2p(-2, 0)[0]), height=abs(a.c2p(0, 4)[1] - a.c2p(0, 0)[1]),
                         color=WHITE, stroke_width=3, fill_color='#0B1221', fill_opacity=1).move_to(a.c2p(0, 2))
        self.play(FadeIn(area(a, gate, -4, 4, GOLD, .45)), run_time=self.rt(.05))
        self.write_board(badge('VÍ DỤ 2: TRỪ PHẦN CỬA', GOLD, 20), self.TM('cửa chữ nhật $4 times 4$ m', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        self.play(FadeIn(door), run_time=self.rt(.05))
        m = self.M('door', 1.3)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.7, t0)
        self.write_board(self.TM('kiểm tra:', 21, SOFT), self.M('door_chk', 1.1), frac=.1)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-5, 5, 1), (-3.8, 3.8, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(-4, 4), y_ticks=(-3, 3))
        self.show_axes(a)
        top = lambda v: 3 * math.sqrt(max(0.0, 1 - v * v / 16))  # noqa: E731
        self.play(FadeIn(band(a, top, lambda v: -top(v), -4, 4, GREEN, .45, samples=120)),
                  Create(clipped(a, top, -4, 4, GREEN, 4)), Create(clipped(a, lambda v: -top(v), -4, 4, GREEN, 4)),
                  run_time=self.rt(.08))
        rnd = random.Random(7)
        flowers = VGroup()
        while len(flowers) < 40:
            px, py = rnd.uniform(-3.8, 3.8), rnd.uniform(-2.8, 2.8)
            if px * px / 16 + py * py / 9 < .85:
                flowers.add(Dot(a.c2p(px, py), radius=.05, color=rnd.choice((GOLD, CORAL, PURPLE))))
        self.play(FadeIn(flowers), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 3: VƯỜN HÌNH ELIP', GOLD, 20), self.M('ell_eq', 1.3), frac=.1)
        self.wait_until(.45, t0)
        self.play(FadeIn(area(a, top, 0, 4, GOLD, .5)), run_time=self.rt(.05))
        m = self.M('ell_s', .95)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e3b(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-5, 5, 1), (-3.8, 3.8, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(-4, 4), y_ticks=(-3, 3))
        self.show_axes(a)
        rect = Rectangle(width=abs(a.c2p(4, 0)[0] - a.c2p(-4, 0)[0]), height=abs(a.c2p(0, 3)[1] - a.c2p(0, -3)[1]),
                         color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=.45).move_to(a.c2p(0, 0))
        top = lambda v: 3 * math.sqrt(max(0.0, 1 - v * v / 16))  # noqa: E731
        hole = band(a, top, lambda v: -top(v), -4, 4, '#0B1221', 1, samples=120)
        self.play(FadeIn(rect), run_time=self.rt(.06))
        self.play(FadeIn(hole), Create(clipped(a, top, -4, 4, GOLD, 3)), Create(clipped(a, lambda v: -top(v), -4, 4, GOLD, 3)),
                  run_time=self.rt(.08))
        self.write_board(badge('PHẦN TRỒNG CỎ', GOLD, 20), self.TM('hình chữ nhật $8 times 6$ trừ elip', 22, WHITE), frac=.1)
        self.wait_until(.45, t0)
        m = self.M('lawn', 1.2)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-1.6, 1.6, 1), (-.3, 2.4, 1), 6.0, 4.6, center=[LEFT_CX, -.2, 0], x_ticks=(-1, 1), y_ticks=(1, 2))
        self.show_axes(a)
        self.play(Create(clipped(a, lambda v: v * v, -1.5, 1.5, CYAN, 4, y_max=2.4)),
                  Create(clipped(a, lambda v: 2 - v * v, -1.5, 1.5, GOLD, 4)), run_time=self.rt(.06))
        self.write_board(badge('VÍ DỤ 4: LOGO', GOLD, 20), self.TM('$y = x^2$ và $y = 2 - x^2$ (đơn vị: dm)', 22, WHITE),
                         frac=.1)
        self.wait_until(.35, t0)
        self.play(FadeIn(band(a, lambda v: 2 - v * v, lambda v: v * v, -1, 1, PURPLE, .6)), run_time=self.rt(.06))
        m = self.M('logo', 1.1)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.8, t0)
        self.write_board(self.TM('$= 8/3 dot 1/100 "m"^2$', 22, SOFT), frac=.05)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        cards = []
        for i, (title, key, col) in enumerate((('cổng parabol', 'quick1', GOLD), ('elip', 'quick2', GREEN))):
            c = card(5.9, 2.8, col).move_to([-3.1 + 6.2 * i, .3, 0])
            cards.append(VGroup(c, tx(title, 24, col, bold=True).move_to(c.get_top() + DOWN * .5),
                                self.M(key, 1.4).move_to(c.get_center() + DOWN * .2)))
        self.play(FadeIn(cards[0], shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.3, t0)
        self.play(FadeIn(cards[1], shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('kiểm tra đáp án trắc nghiệm trong vài giây', 25, GOLD, bold=True).move_to([0, -2.2, 0])),
                  run_time=self.rt(.05))

    def beat_e6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = axes((-.6, 9, 1), (0, 7, 1), 6.0, 4.6, center=[LEFT_CX, -.3, 0], x_ticks=(4, 8), y_ticks=(6,))
        self.show_axes(a)
        f = lambda v: 3 / 8 * v * (8 - v)  # noqa: E731
        self.play(FadeIn(Line(a.c2p(-.5, 0), a.c2p(8.8, 0), color=SOFT, stroke_width=4)),
                  Create(clipped(a, f, 0, 8, GOLD, 9)), FadeIn(area(a, f, 0, 8, GOLD, .35)), run_time=self.rt(.08))
        self.write_board(self.heading('GỐC Ở CHÂN TRÁI'), frac=.04)
        self.wait_until(.25, t0)
        m = self.M('left', 1.0)
        self.write_board(m, frac=.12)
        self.wait_until(.6, t0)
        self.write_board(tx('kết quả không đổi', 23, GREEN, bold=True),
                         tx('nhưng gốc ở giữa thì gọn và nhanh hơn', 22, SOFT), frac=.08)

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = self.TM('Cổng parabol rộng $6$ m, cao $"4,5"$ m; gốc tọa độ ở giữa chân cổng.', 23, WHITE)
        l2 = self.TM('Sơn mặt cổng giá $200 space 000$ đ / $"m"^2$. Xét các mệnh đề:', 23, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.42, .75))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('b, d)', 22, SOFT), self.M('tf_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, False), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSS'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        tag = VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25)
        q1 = self.TM('Vườn hoa hình elip: trục lớn $10$ m, trục nhỏ $6$ m.', 25, WHITE)
        q2 = self.TM('Chi phí trồng hoa $50 space 000$ đ / $"m"^2$.', 25, WHITE)
        q3 = tx('Tổng chi phí (triệu đồng, làm tròn đến hàng phần trăm)?', 25, GOLD, bold=True)
        self.centre(tag, q1, q2, q3, top=2.2, gap=.5)
        self.play(FadeIn(tag), FadeIn(q1), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.play(FadeIn(q2), run_time=self.rt(.05))
        self.wait_until(.7, t0)
        self.play(FadeIn(q3), run_time=self.rt(.05))

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        s1, s2 = self.M('sa_s1', 1.3), self.M('sa_s2', 1.2)
        sheet = self.answer_sheet('2,36')
        self.centre(s1, s2, sheet, top=2.0, gap=.75)
        self.play(Write(s1), run_time=self.rt(.12))
        self.wait_until(.35, t0)
        self.play(Write(s2), run_time=self.rt(.12))
        self.wait_until(.75, t0)
        self.play(FadeIn(sheet), run_time=self.rt(.05))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Đặt hệ trục', 'sum1', 'Gốc ở giữa, trục tung qua đỉnh'),
                                ('Công thức nhanh', 'sum2', 'Parabol và elip'),
                                ('Năm bước', 'sum3', 'Nhân đơn giá, cẩn thận đơn vị')),
                           fracs=(.04, .35, .6))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Cổng:', 'hw1'), ('Logo:', 'hw2'), ('Elip:', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.04, .3, .55))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Lưu lượng thay đổi · lượng nước đã chảy vào', 26, GOLD, bold=True), self.M('next1', 1.4)])


class INT30_SMOKE(INT30):
    smoke = True
