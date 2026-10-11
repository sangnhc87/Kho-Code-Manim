"""INT28 – Dựng lại công thức thể tích: trụ, nón, cầu, chỏm cầu, nón cụt, elip.

    python scripts/build_typst.py --ep int28
    python scripts/prepare_voice.py --ep int28 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int28/scene.py INT28
    python scripts/finalize.py --ep int28

One method per narration beat (int28/lesson.py); shared screens come from
common/blocks.py and common/revolve.py. All math on screen is Typst
(``self.M`` or ``self.TM('chữ $toán$')``). Every number is checked in
lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, ValueTracker, VGroup, Write, always_redraw, linear

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, clipped, dashed, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.revolve import region, solid  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402

RR = 2.0  # sphere radius used in the drawings


def semi(v):
    return math.sqrt(max(0.0, RR * RR - v * v))


class INT28(LessonScene):
    EP = 'int28'

    def ax(self, xr, yr, **kw):
        return axes(xr, yr, kw.pop('w', 6.0), kw.pop('h', 5.3), center=kw.pop('center', [LEFT_CX, -.1, 0]),
                    x_ticks=(), y_ticks=(), **kw)

    def spin(self, a, f, x0, x1, frac, color=CYAN, n=14):
        th = ValueTracker(0)
        live = always_redraw(lambda: region(a, f, x0, x1, math.cos(th.get_value()), color, .5))
        self.add(live)
        self.play(th.animate.set_value(2 * math.pi), run_time=self.rt(frac), rate_func=linear)
        live.clear_updaters()
        self.remove(live)
        body = solid(a, f, x0, x1, n, color)
        self.add(body)
        return body

    def build(self, t0, a, f, x0, x1, color, gen_key, vol_key, fracs, vol_scale=1.15, heading=None):
        """Generator line → spin → formula: the common pattern of this episode."""
        self.play(Create(clipped(a, f, x0, x1, color, 5)), FadeIn(region(a, f, x0, x1, color=color)),
                  run_time=self.rt(.07))
        if heading:
            self.write_board(self.heading(heading), frac=.04)
        self.write_board(self.TM('đường sinh:', 22, SOFT), self.M(gen_key, 1.15), frac=.1)
        self.wait_until(fracs[0], t0)
        self.spin(a, f, x0, x1, .22, color)
        self.wait_until(fracs[1], t0)
        m = self.M(vol_key, vol_scale)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        return m

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        m = self.M('cap', 2.0).move_to([0, 1.3, 0])
        self.play(Write(m), run_time=self.rt(.12))
        self.wait_until(.25, t0)
        self.play(FadeIn(tx('học thuộc lòng: khó nhớ, dễ nhầm', 26, CORAL).move_to([0, -.3, 0])), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.TM('dựng lại bằng $pi integral_a^b f^2 dif x$: chỉ 3 dòng', 28, GOLD, bold=True)
                         .move_to([0, -1.6, 0])), run_time=self.rt(.08))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Đường sinh', 'Chọn hệ trục khéo léo'),
                         ('Trụ, nón, cầu', 'Ba công thức quen thuộc'),
                         ('Khối khó hơn', 'Chỏm cầu, nón cụt, khối elip')], t0, fracs=(.1, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'CHIẾN LƯỢC CHUNG', ('gen',), (.3,), (1.7,))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.TM('chọn hệ trục để đường sinh $y = f(x)$ thật đơn giản', 26, SOFT)
                         .next_to(lines[-1], DOWN, buff=.8)), run_time=self.rt(.05))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 4.4, 1), (-2.4, 2.4, 1))
        self.show_axes(a)
        self.build(t0, a, lambda v: 1.4, 0, 4, CYAN, 'cyl_f', 'cyl_v', (.25, .55), heading='HÌNH TRỤ')
        self.wait_until(.85, t0)
        self.write_board(self.TM('= diện tích đáy $times$ chiều cao', 22, GOLD), frac=.05)

    def beat_c2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 4.4, 1), (-2.4, 2.4, 1))
        self.show_axes(a)
        from common.revolve import ring
        outer, inner = (lambda v: 1.6), (lambda v: .9)
        self.play(FadeIn(region(a, outer, 0, 4, color=GOLD, opacity=.45, g=inner)), run_time=self.rt(.06))
        self.write_board(self.heading('ỐNG TRỤ RỖNG'), self.TM('giữa $y = R$ và $y = r$: vành khăn (tập 27)', 22, WHITE),
                         frac=.1)
        self.wait_until(.25, t0)
        self.play(FadeIn(VGroup(*[ring(a, outer, inner, .2 + .4 * k, GOLD, .4, 1) for k in range(10)])),
                  run_time=self.rt(.12))
        self.wait_until(.5, t0)
        m = self.M('tube', 1.05)
        self.write_board(m, frac=.12)

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((0, 4.4, 1), (-2.4, 2.4, 1))
        self.show_axes(a)
        self.build(t0, a, lambda v: .45 * v, 0, 4, GOLD, 'cone_f', 'cone_v', (.25, .5), heading='HÌNH NÓN')
        self.wait_until(.8, t0)
        self.write_board(self.TM('$= 1/3$ hình trụ cùng đáy, cùng chiều cao', 22, GOLD), frac=.05)

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-2.6, 2.6, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        self.build(t0, a, semi, -RR, RR, GREEN, 'sph_f', 'sph_v', (.25, .55), heading='HÌNH CẦU')

    def beat_c5(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.ax((-2.6, 2.6, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        cyl = solid(a, lambda v: RR, -RR, RR, 12, CYAN)
        sph = solid(a, semi, -RR, RR, 12, GREEN)
        self.play(FadeIn(cyl), run_time=self.rt(.08))
        self.play(FadeIn(sph), run_time=self.rt(.08))
        self.write_board(self.heading('ARCHIMEDES'), self.TM('cầu nội tiếp trong trụ cao $2R$', 22, WHITE), frac=.1)
        self.wait_until(.35, t0)
        m = self.M('arch', 1.2)
        self.write_board(self.TM('$V_\"cầu\" = 2/3 V_\"trụ\"$:', 24, GOLD), m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    # ================================================================ PHẦN 2
    def beat_e1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.6, 2.6, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        self.play(Create(clipped(a, semi, -RR, RR, SOFT, 2.5)), Create(clipped(a, lambda v: -semi(v), -RR, RR, SOFT, 2.5)),
                  run_time=self.rt(.05))
        hcap = 1.2
        x0 = RR - hcap
        self.play(Create(dashed(a.c2p(x0, -semi(x0)), a.c2p(x0, semi(x0)), color=WHITE)),
                  FadeIn(self.TM('$R - h$', 18, WHITE).move_to(a.c2p(x0, -2.45))), run_time=self.rt(.05))
        self.build(t0, a, semi, x0, RR, GOLD, 'cap_f', 'cap_v', (.3, .55), vol_scale=1.0, heading='CHỎM CẦU')
        self.write_board(self.TM('cùng đường sinh với hình cầu, chỉ đổi cận', 21, SOFT), frac=.05)

    def beat_e2(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'KIỂM TRA HAI ĐẦU', ('cap', 'cap_half', 'cap_full'), (.05, .25, .6), (1.4, 1.3, 1.3),
                            box_last=False, gap=.6)
        self.wait_until(.85, t0)
        self.play(FadeIn(self.TM('nửa cầu và cả hình cầu: đều đúng $checkmark$', 25, GREEN, bold=True)
                         .next_to(lines[-1], DOWN, buff=.55)), run_time=self.rt(.05))

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((0, 4.4, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        self.build(t0, a, lambda v: .7 + .32 * v, 0, 4, PURPLE, 'frus_f', 'frus_v', (.25, .5), vol_scale=1.2,
                   heading='NÓN CỤT')
        self.wait_until(.8, t0)
        self.write_board(self.TM('$r = 0$: trở về hình nón', 22, GOLD), frac=.05)

    def beat_e3b(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'THỬ VỚI SỐ', ('frus_num',), (.05,), (1.5,))
        self.wait_until(.45, t0)
        chk = VGroup(self.TM('kiểm tra bằng hiệu hai hình nón:', 24, SOFT), self.M('frus_chk', 1.2)) \
            .arrange(DOWN, buff=.35).next_to(lines[-1], DOWN, buff=.7)
        self.play(FadeIn(chk[0]), Write(chk[1]), run_time=self.rt(.12))

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-3.2, 3.2, 1), (-2.4, 2.4, 1))
        self.show_axes(a)
        el = lambda v: 1.3 * math.sqrt(max(0.0, 1 - v * v / 9))  # noqa: E731
        self.play(Create(clipped(a, el, -3, 3, CORAL, 5)), FadeIn(region(a, el, -3, 3, color=CORAL)), run_time=self.rt(.07))
        self.write_board(self.heading('KHỐI ELIP TRÒN XOAY'), self.M('ell_f', .95), frac=.12)
        self.wait_until(.3, t0)
        self.spin(a, el, -3, 3, .22, CORAL)
        self.wait_until(.55, t0)
        m = self.M('ell_v', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.85, t0)
        self.write_board(self.TM('$a = b = R$: lại được hình cầu', 22, GOLD), frac=.05)

    def beat_e5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.6, 2.6, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        x0 = RR - .8
        self.play(Create(clipped(a, semi, -RR, RR, SOFT, 2.5)), Create(clipped(a, lambda v: -semi(v), -RR, RR, SOFT, 2.5)),
                  run_time=self.rt(.05))
        self.write_board(badge('BÀI TOÁN THỰC TẾ', GOLD, 20),
                         self.TM('bát bán cầu $R = 10$ cm, nước sâu $h = 4$ cm', 22, WHITE), frac=.1)
        self.wait_until(.3, t0)
        body = solid(a, semi, x0, RR, 8, CYAN)
        self.play(FadeIn(body), FadeIn(region(a, semi, x0, RR, color=CYAN, opacity=.5)), run_time=self.rt(.08))
        self.write_board(self.TM('phần nước là một chỏm cầu', 22, CYAN), frac=.05)
        self.wait_until(.6, t0)
        m = self.M('bowl', 1.0)
        self.write_board(m, frac=.12)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_e6(self, T):
        t0 = self.now()
        lines = self.worked(t0, 'BONUS: THỂ TÍCH VÀ DIỆN TÍCH MẶT', ('shell1', 'shell2'), (.05, .4), (1.5, 1.5), gap=.6,
                            box_last=False)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.TM('thêm lớp vỏ dày $dif R$: $Delta V approx 4 pi R^2 dif R$', 25, GOLD, bold=True)
                         .next_to(lines[-1], DOWN, buff=.7)), run_time=self.rt(.05))

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = self.TM('Khối cầu bán kính $3$ sinh bởi nửa đường tròn quay quanh $O x$.', 24, WHITE)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = (VGroup(tx('Đường sinh', 24, WHITE), self.M('tf_a', 1.35)).arrange(RIGHT, buff=.2),
                 self.M('tf_b', 1.3), self.M('tf_c', 1.35),
                 VGroup(tx('Chỏm cầu cao 1:', 24, WHITE), self.M('tf_d', 1.35)).arrange(RIGHT, buff=.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.35, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c)', 22, SOFT), self.M('tf_c_calc', 1.0)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.78, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ax((-2.6, 2.6, 1), (-2.6, 2.6, 1))
        self.show_axes(a)
        self.play(Create(clipped(a, semi, -RR, RR, SOFT, 2.5)), Create(clipped(a, lambda v: -semi(v), -RR, RR, SOFT, 2.5)),
                  run_time=self.rt(.05))
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.TM('bồn dạng chỏm cầu: $R = 5$ m, $h = 2$ m', 22, WHITE),
                         self.TM('thể tích ($"m"^3$), làm tròn đến hàng đơn vị', 21, SOFT), frac=.14)
        self.wait_until(.5, t0)
        self.spin(a, semi, RR - .8, RR, .3, GOLD, n=8)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sa_s1', .9), frac=.14)
        self.wait_until(.45, t0)
        self.write_board(self.TM('hoặc:', 21, SOFT), self.M('sa_s2', 1.0), frac=.1)
        self.wait_until(.75, t0)
        self.write_board(self.answer_sheet('54'), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Một công thức gốc', 'sum1', 'Mọi khối tròn xoay'),
                                ('Đường sinh', 'sum2', 'Ngang, xiên, nửa đường tròn'),
                                ('Chỏm cầu', 'sum3', 'Cầu với cận khác')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Hình trụ:', 'hw1'), ('Chỏm cầu:', 'hw2'), ('Khối elip:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .25, .45))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Phần D · Ứng dụng thực tế', 28, GOLD, bold=True), self.M('next1', 1.3)])


class INT28_SMOKE(INT28):
    smoke = True
