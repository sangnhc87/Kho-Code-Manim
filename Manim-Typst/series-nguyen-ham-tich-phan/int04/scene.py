"""INT04 – Nguyên hàm hàm số lượng giác: bảng cơ bản & hạ bậc.

    python scripts/build_typst.py --ep int04
    python scripts/prepare_voice.py --ep int04 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int04/scene.py INT04
    python scripts/finalize.py --ep int04

One method per narration beat (int04/lesson.py); shared screens come from
common/blocks.py. Every number shown is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart,
                   Line, RoundedRectangle, Transform, ValueTracker, VGroup, VMobject, Write,
                   always_redraw, linear, smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, card, check, clipped, cross, dashed, dot, para, tx, vn  # noqa: E402
from common.lesson_scene import BOARD_X, LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL_2, PURPLE, SOFT, STROKE, WHITE  # noqa: E402

PI_LABELS = ((-math.pi, '−π'), (-math.pi / 2, '−π/2'), (math.pi / 2, 'π/2'), (math.pi, 'π'),
             (3 * math.pi / 2, '3π/2'), (2 * math.pi, '2π'))


def spring_pos(t):
    return 2 * math.sin(t) + 1


class INT04(LessonScene):
    EP = 'int04'

    # ================================================================ helpers
    def pi_axes(self, xr, yr, yt, w=6.0, h=5.55, center=None, x_label='x', label_size=17):
        a = axes(xr, yr, w, h, center=center or [LEFT_CX, -.12, 0], x_ticks=(), y_ticks=yt, x_label=x_label,
                 label_size=label_size)
        for v, name in PI_LABELS:
            if xr[0] < v < xr[1] - .15:
                p = a.c2p(v, 0)
                a.labels.add(Line(p + UP * .06, p + DOWN * .06, color=SOFT, stroke_width=2),
                             tx(name, label_size, SOFT).move_to(p + DOWN * .3))
        return a

    def show_axes(self, a, frac=.05):
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(frac))

    def centre(self, *mobs, top=2.55, gap=.42):
        g = VGroup(*mobs).arrange(DOWN, buff=gap)
        g.move_to([0, top, 0], aligned_edge=UP)
        return g

    def spring_system(self, pos_fn, y=1.2, x0=-6.4, origin=-3.2, unit=.8):
        """Wall + zigzag spring + block whose centre sits at origin + unit·pos_fn()."""
        wall = VGroup(Line([x0, y - .6, 0], [x0, y + .6, 0], color=SOFT, stroke_width=5),
                      *[Line([x0, y - .5 + .2 * k, 0], [x0 - .18, y - .65 + .2 * k, 0], color=SOFT, stroke_width=2)
                        for k in range(6)])
        floor = Line([x0, y - .42, 0], [origin + unit * 3.6, y - .42, 0], color=STROKE, stroke_width=2)

        def block_x():
            return origin + unit * pos_fn()

        def spring():
            end = block_x() - .4
            n = 16
            pts = [[x0, y, 0]]
            for k in range(1, n):
                px = x0 + (end - x0) * k / n
                pts.append([px, y + (.18 if k % 2 else -.18), 0])
            pts.append([end, y, 0])
            m = VMobject(stroke_color=SOFT, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        block = always_redraw(lambda: RoundedRectangle(width=.8, height=.7, corner_radius=.08, fill_color=CORAL,
                                                       fill_opacity=1, stroke_width=0).move_to([block_x(), y, 0]))
        ticks = VGroup()
        for p in (-1, 0, 1, 2, 3):
            q = origin + unit * p
            ticks.add(Line([q, y - .5, 0], [q, y - .34, 0], color=SOFT, stroke_width=2),
                      tx(vn(p, 0), 14, SOFT).move_to([q, y - .7, 0]))
        return VGroup(floor, ticks, wall, always_redraw(spring), block)

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        tau = ValueTracker(0)
        system = self.spring_system(lambda: spring_pos(tau.get_value()), y=1.9, origin=-2.4, unit=1.0)
        a = self.pi_axes((0, 6.5, 1), (-1.5, 3.5, 1), (-1, 1, 2, 3), w=8.0, h=2.6, center=[0, -1.3, 0],
                         x_label='t')
        trace = always_redraw(lambda: clipped(a, spring_pos, 0, max(tau.get_value(), .02), GOLD, 4))
        pt = always_redraw(lambda: Dot(a.c2p(tau.get_value(), spring_pos(tau.get_value())), radius=.08, color=GOLD))
        self.play(FadeIn(system), FadeIn(a), FadeIn(a.labels), run_time=self.rt(.08))
        self.add(trace, pt)
        self.play(tau.animate.set_value(2 * math.pi), run_time=self.rt(.55), rate_func=linear)
        for m in (trace, pt, system[3], system[4]):
            m.clear_updaters()
        q = self.M('hook_v', 1.5).move_to([3.6, 2.0, 0])
        self.play(Write(q), run_time=self.rt(.1))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Bốn công thức cơ bản', 'sin, cos, 1/cos², 1/sin² · dấu trừ dễ nhầm'),
                         ('Lệch pha ¼ chu kỳ', 'Nguyên hàm dịch sóng sang phải π/2'),
                         ('Kỹ thuật hạ bậc', 'sin²x, cos²x, tan²x và sin x·cos x')], t0, fracs=(.12, .4, .62))

    # ================================================================ PHẦN 1
    def beat_c1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        h1 = tx('ĐẠO HÀM', 24, CYAN, bold=True).move_to([-3.3, 2.35, 0])
        h2 = tx('NGUYÊN HÀM', 24, GOLD, bold=True).move_to([3.3, 2.35, 0])
        rule = Line([-6, 2.0, 0], [6, 2.0, 0], color=STROKE, stroke_width=2)
        self.play(FadeIn(h1), FadeIn(h2), Create(rule), run_time=self.rt(.06))
        for k, (d, i, y) in enumerate((('d_sin', 'i_cos', 1.0), ('d_cos', 'i_sin', -.7))):
            md = self.M(d, 1.5).move_to([-3.7, y, 0])
            mi = self.M(i, 1.5).move_to([0, y, 0]).to_edge(RIGHT, buff=.6)
            arr = Arrow([md.get_right()[0] + .25, y, 0], [mi.get_left()[0] - .25, y, 0], color=GOLD, buff=0,
                        stroke_width=5)
            lbl = tx('đọc ngược', 17, GOLD).next_to(arr, UP, buff=.08)
            self.wait_until((.08, .45)[k], t0)
            self.play(Write(md), run_time=self.rt(.07))
            self.play(GrowArrow(arr), FadeIn(lbl), Write(mi), run_time=self.rt(.1))
        self.wait_until(.85, t0)
        note = tx('(−cos x)′ = sin x  →  dấu trừ nằm ở nguyên hàm của sin', 22, GOLD, bold=True).move_to([0, -2.3, 0])
        self.play(FadeIn(note), run_time=self.rt(.06))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-.3, 6.6, 1), (-1.6, 1.6, 1), (-1, 1))
        self.show_axes(a)
        bad = VGroup(self.M('trap_sin', 1.4), cross(CORAL, .32)).arrange(RIGHT, buff=.3)
        self.write_board(badge('LỖI SAI PHỔ BIẾN', CORAL, 19), bad, frac=.12)
        self.wait_until(.28, t0)
        self.write_board(self.M('f_sin', 1.4), self.M('F_mcos', 1.4), frac=.1)
        self.verify_plot(a, math.sin, lambda v: -math.cos(v), .3, 6.2, .45, readout_at=(BOARD_X, -2.2))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-1.8, 6.6, 1), (-1.6, 1.6, 1), (-1, 1))
        self.show_axes(a)
        base = clipped(a, math.sin, -1.8, 6.6, CYAN, 4)
        self.play(Create(base), run_time=self.rt(.05))
        self.write_board(self.heading('ĐẠO HÀM: DỊCH TRÁI π/2'), self.M('shift1', 1.5), frac=.1)
        phase = ValueTracker(0)
        live = always_redraw(lambda: clipped(a, lambda v: math.sin(v - phase.get_value()), -1.8, 6.6,
                                             GREEN if phase.get_value() < 0 else GOLD, 4.5))
        self.add(live)
        self.play(phase.animate.set_value(-math.pi / 2), run_time=self.rt(.14), rate_func=smooth)
        cos_curve = live.copy().clear_updaters()
        self.add(cos_curve)
        self.wait_until(.45, t0)
        self.write_board(self.heading('NGUYÊN HÀM: DỊCH PHẢI π/2', GOLD), self.M('shift2', 1.5), frac=.1)
        phase.set_value(0)
        self.play(phase.animate.set_value(math.pi / 2), run_time=self.rt(.16), rate_func=smooth)
        live.clear_updaters()
        lab = VGroup(tx('sin x', 19, CYAN, bold=True), tx('cos x', 19, GREEN, bold=True),
                     tx('−cos x', 19, GOLD, bold=True)).arrange(RIGHT, buff=.5)
        self.board(lab, gap=.5)
        self.play(FadeIn(lab), run_time=self.rt(.04))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-3.3, 3.3, 1), (-4, 4, 1), (-3, -1, 1, 3))
        self.ax = a
        self.show_axes(a)
        self.write_board(self.M('d_tan', 1.15), self.M('i_tan', 1.15), frac=.12, gap=.2)
        branches = VGroup(*[clipped(a, math.tan, lo + .02, hi - .02, GOLD, 4.5)
                            for lo, hi in ((-3.3, -math.pi / 2), (-math.pi / 2, math.pi / 2), (math.pi / 2, 3.3))])
        asym = VGroup(*[dashed(a.c2p(v, -4), a.c2p(v, 4), color=CORAL, stroke_width=2) for v in (-math.pi / 2,
                                                                                                    math.pi / 2)])
        self.play(Create(asym), Create(branches), run_time=self.rt(.1))
        self.write_board(VGroup(tx('với', 20, SOFT), self.M('tan_dom', 1.05)).arrange(RIGHT, buff=.2), frac=.05, gap=.15)
        self.wait_until(.55, t0)
        self.write_board(self.M('d_cot', 1.15), self.M('i_cot', 1.15), frac=.12, gap=.24)
        self.write_board(VGroup(tx('với', 20, SOFT), self.M('cot_dom', 1.05)).arrange(RIGHT, buff=.2), frac=.05, gap=.15)
        self.tan_branches = branches

    def beat_c5(self, T):
        t0 = self.now()
        a = self.ax
        self.clear_board(.03)
        self.write_board(badge('LƯU Ý CHUYÊN SÂU', CORAL, 19),
                         para('tan x chỉ xác định trên từng khoảng giữa hai tiệm cận đứng; mỗi khoảng có thể có '
                              'một hằng số C riêng.', 23, WHITE, width=34), frac=.14)
        mid = self.tan_branches[1]
        ghost = mid.copy().set_stroke(opacity=.25)
        self.add(ghost)
        self.wait_until(.35, t0)
        lifted = clipped(a, lambda v: math.tan(v) + 1.5, -math.pi / 2 + .02, math.pi / 2 - .02, GREEN, 4.5)
        self.play(Transform(mid, lifted), FadeIn(tx('+ C', 22, GREEN, bold=True).move_to(a.c2p(.75, 3.2))),
                  run_time=self.rt(.12))
        self.wait_until(.62, t0)
        self.write_board(tx('Đề thi thường cho sẵn khoảng, ví dụ (−π/2; π/2).', 22, GOLD, bold=True), frac=.08)

    def beat_c6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('NGUYÊN HÀM CỦA sin²x?', 26, GOLD, bold=True)
        wrong = VGroup(self.M('trap_sq', 1.6), cross(CORAL, .4)).arrange(RIGHT, buff=.35)
        hint = tx('→ HẠ BẬC trước khi lấy nguyên hàm', 24, GREEN, bold=True)
        pair = VGroup(self.M('hb_sin', 1.7), self.M('hb_cos', 1.7)).arrange(RIGHT, buff=1.0)
        self.centre(head, wrong, hint, pair, top=2.6, gap=.5)
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.wait_until(.12, t0)
        self.play(Write(wrong[0]), run_time=self.rt(.14))
        self.play(Create(wrong[1]), run_time=self.rt(.04))
        self.wait_until(.62, t0)
        self.play(FadeIn(hint, shift=UP * .1), run_time=self.rt(.05))
        self.play(*[Write(m) for m in pair], run_time=self.rt(.14))
        self.play(FadeIn(self.box(pair, GREEN)), run_time=self.rt(.04))

    def beat_c7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('CẦN THÊM: NGUYÊN HÀM CỦA cos 2x', 26, GOLD, bold=True)
        d = self.M('d_sin2x', 1.5)
        note = tx('đạo hàm hàm hợp – lớp 11', 20, SOFT)
        res = self.M('i_cos2x', 1.6)
        res2 = self.M('i_sin2x', 1.4)
        self.centre(head, d, note, res, res2, top=2.8, gap=.3)
        self.play(FadeIn(head), Write(d), FadeIn(note), run_time=self.rt(.16))
        self.wait_until(.38, t0)
        self.play(Write(res), run_time=self.rt(.12))
        self.play(FadeIn(self.box(res)), run_time=self.rt(.04))
        self.play(Write(res2), run_time=self.rt(.1))
        self.wait_until(.72, t0)
        tag = badge('Quy tắc tổng quát f(ax + b): INT05', PURPLE, 19).next_to(res2, DOWN, buff=.45)
        self.play(FadeIn(tag, shift=UP * .1), run_time=self.rt(.06))

    def beat_c8(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        a = self.pi_axes((-.3, 6.6, 1), (-.6, 3.5, 1), (1, 2, 3))
        self.show_axes(a)
        m = self.M('i_sin2', 1.3)
        self.write_board(self.heading('GHÉP LẠI'), m, self.M('f_sin2', 1.3), frac=.12)
        self.play(FadeIn(self.box(m)), run_time=self.rt(.04))
        self.wait_until(.2, t0)
        self.verify_plot(a, lambda v: math.sin(v) ** 2, lambda v: v / 2 - math.sin(2 * v) / 4, .3, 6.2, .4,
                         readout_at=(BOARD_X, -.5))
        self.wait_until(.8, t0)
        self.write_board(tx('Tương tự:', 21, SOFT), frac=.03, gap=1.35)
        self.write_board(self.M('i_cos2', 1.3), frac=.08, gap=.15)

    def beat_c9(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('NGUYÊN HÀM CỦA tan²x', 26, GOLD, bold=True)
        idt = self.M('tan2_id', 1.9)
        res = self.M('i_tan2', 1.9)
        self.centre(head, idt, res, top=2.2, gap=.7)
        self.play(FadeIn(head), run_time=self.rt(.05))
        self.wait_until(.2, t0)
        self.play(Write(idt), run_time=self.rt(.16))
        self.wait_until(.6, t0)
        self.play(Write(res), run_time=self.rt(.14))
        self.play(FadeIn(self.box(res)), run_time=self.rt(.05))

    def beat_c10(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        head = tx('BẢNG NGUYÊN HÀM LƯỢNG GIÁC', 24, GOLD, bold=True).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.04))
        cells = VGroup()
        for i, key in enumerate(('tb1', 'tb2', 'tb3', 'tb4', 'tb5', 'tb6')):
            r, c = divmod(i, 2)
            box = card(6.1, 1.35, GREEN if r == 2 else STROKE).move_to([-3.15 + 6.3 * c, 1.45 - 1.55 * r, 0])
            g = VGroup(box, self.M(key, 1.25, max_w=5.3).move_to(box))
            if r == 2:
                g.add(badge('HẠ BẬC', GREEN, 14).move_to(box.get_corner(UP + RIGHT) + LEFT * .6 + DOWN * .25))
            cells.add(g)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .15) for c in cells[:4]], lag_ratio=.25), run_time=self.rt(.25))
        self.wait_until(.6, t0)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .15) for c in cells[4:]], lag_ratio=.3), run_time=self.rt(.16))

    # ================================================================ PHẦN 2
    def worked(self, t0, tag, keys, fracs, scales=None, box_last=True, gap=.34):
        """Centred worked example: badge + lines revealed at the given beat fractions."""
        self.clear_stage(.05)
        scales = scales or [1.6] * len(keys)
        tagm = badge(tag, GOLD, 20)
        lines = [self.M(k, s) for k, s in zip(keys, scales)]
        self.centre(tagm, *lines, top=2.75, gap=gap)
        self.play(FadeIn(tagm), run_time=self.rt(.03))
        for frac, m in zip(fracs, lines):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.12))
        if box_last:
            self.play(FadeIn(self.box(lines[-1], GREEN)), run_time=self.rt(.04))

    def beat_e1(self, T):
        self.worked(self.now(), 'VÍ DỤ 1', ('e1_task', 'e1_s1'), (.04, .45), (1.6, 1.7))

    def beat_e2(self, T):
        self.worked(self.now(), 'VÍ DỤ 2', ('e2_task', 'e2_s1', 'e2_s2'), (.04, .3, .72), (1.6, 1.35, 1.6))

    def beat_e5(self, T):
        self.worked(self.now(), 'VÍ DỤ 3', ('e5_task', 'e5_s1', 'e5_s2', 'e5_s3'), (.04, .22, .45, .75),
                    (1.5, 1.5, 1.5, 1.6))

    def beat_e6(self, T):
        self.worked(self.now(), 'VÍ DỤ 4', ('e6_task', 'e6_s1', 'i_sin2x', 'e6_s2'), (.04, .3, .55, .78),
                    (1.3, 1.25, 1.15, 1.35), gap=.26)

    def beat_e3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        self.tau = ValueTracker(0)
        self.spring = self.spring_system(lambda: spring_pos(self.tau.get_value()), y=2.3, x0=-6.6, origin=-4.4,
                                         unit=.8)
        self.play(FadeIn(self.spring), run_time=self.rt(.08))
        self.write_board(badge('VÍ DỤ 5', GOLD, 20), tx('Vật dao động với vận tốc', 24, WHITE),
                         self.M('e3_task', 1.45), tx('v tính bằng cm/s, x tính bằng cm.', 20, SOFT), frac=.28)
        self.wait_until(.75, t0)
        self.write_board(tx('Tìm x(π/2).', 26, GOLD, bold=True), frac=.08)

    def beat_e4(self, T):
        t0 = self.now()
        self.clear_board(.03)
        a = self.pi_axes((0, 6.6, 1), (-1.5, 3.6, 1), (-1, 1, 2, 3), w=6.0, h=3.6, center=[LEFT_CX, -1.05, 0],
                         x_label='t')
        self.show_axes(a, .04)
        self.write_board(self.M('e3_s1', 1.3), frac=.1)
        self.wait_until(.22, t0)
        self.write_board(self.M('e3_s2', 1.2), frac=.1)
        res = self.M('e3_s3', 1.5)
        self.wait_until(.42, t0)
        self.write_board(res, frac=.06)
        self.play(FadeIn(self.box(res)), run_time=self.rt(.03))
        trace = always_redraw(lambda: clipped(a, spring_pos, 0, max(self.tau.get_value(), .02), GOLD, 4))
        pt = always_redraw(lambda: Dot(a.c2p(self.tau.get_value(), spring_pos(self.tau.get_value())), radius=.08,
                                       color=GOLD))
        self.add(trace, pt)
        self.wait_until(.55, t0)
        self.play(self.tau.animate.set_value(math.pi / 2), run_time=self.rt(.12), rate_func=linear)
        self.play(Indicate(pt, color=GOLD, scale_factor=1.8), run_time=self.rt(.05))
        self.play(self.tau.animate.set_value(2 * math.pi), run_time=self.rt(.2), rate_func=linear)
        for m in (trace, pt, self.spring[3], self.spring[4]):
            m.clear_updaters()

    # ================================================================ PHẦN 3
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Cho hàm số', 24, WHITE), self.M('tf_f', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Gọi F là một nguyên hàm của f trên ℝ. Xét các mệnh đề:', 24, WHITE)
        items = (self.M('tf_a', 1.2), self.M('tf_b', 1.2),
                 VGroup(tx('Nếu', 22, WHITE), self.M('tf_c', 1.2)).arrange(RIGHT, buff=.2), self.M('tf_d', 1.2))
        self.tf_question(t0, [l1, l2], items, fracs=(.3, .7))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.07))
        self.wait_until(.35, t0)
        self.play(self.tf_mark(1, False), run_time=self.rt(.07))
        why = VGroup(tx('Thử lại:', 22, SOFT), self.M('trap_sq', 1.2)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.wait_until(.55, t0)
        self.play(FadeIn(why[0]), Write(why[1]), run_time=self.rt(.12))
        self.x2_why = why

    def beat_x3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.x2_why), run_time=self.rt(.03))
        c = VGroup(tx('c)', 22, GOLD, bold=True), self.M('tf_c_calc', 1.05)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(c), run_time=self.rt(.1))
        self.play(self.tf_mark(2, True), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        d = VGroup(tx('d)', 22, GOLD, bold=True), self.M('tf_d_calc', 1.05)).arrange(RIGHT, buff=.2) \
            .move_to([0, -2.72, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeOut(c), FadeIn(d), run_time=self.rt(.1))
        self.play(self.tf_mark(3, False), run_time=self.rt(.06))
        self.wait_until(.86, t0)
        self.play(FadeIn(self.tf_key('ĐSĐS'), shift=LEFT * .1), run_time=self.rt(.06))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.pi_axes((-1.7, 1.7, 1), (-2, 6, 1), (2, 4))
        self.show_axes(a, .04)
        self.write_board(VGroup(badge('TRẢ LỜI NGẮN', PURPLE, 19), tx('Phần III', 18, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('sa_task', 1.05), frac=.12)
        asym = VGroup(*[dashed(a.c2p(v, -2), a.c2p(v, 6), color=CORAL, stroke_width=2)
                        for v in (-math.pi / 2, math.pi / 2)])
        F = clipped(a, lambda v: math.tan(v) + 2, -math.pi / 2 + .02, math.pi / 2 - .02, GOLD, 4.5)
        self.wait_until(.42, t0)
        self.write_board(self.M('sa_s1', 1.1), frac=.1)
        self.play(Create(asym), Create(F), FadeIn(dot(a, math.pi / 4, 3, CYAN, .09)), run_time=self.rt(.08))
        self.wait_until(.75, t0)
        P = dot(a, math.pi / 3, math.sqrt(3) + 2, GREEN, .09)
        self.play(FadeIn(P), Create(dashed(a.c2p(math.pi / 3, 0), a.c2p(math.pi / 3, math.sqrt(3) + 2), color=GREEN,
                                           stroke_width=2)), run_time=self.rt(.04))
        self.write_board(self.M('sa_s2', 1.3), self.answer_sheet('3,73'), frac=.08)

    def beat_x5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        body = RoundedRectangle(width=4.0, height=5.6, corner_radius=.3, fill_color='#1A2840', fill_opacity=1,
                                stroke_color=STROKE, stroke_width=2).move_to([LEFT_CX, -.15, 0])
        screen = RoundedRectangle(width=3.4, height=1.7, corner_radius=.12, fill_color='#C9D8C5', fill_opacity=1,
                                  stroke_width=0).move_to(body.get_top() + DOWN * 1.15)
        mode = tx('R', 20, '#14202B', bold=True).move_to(screen.get_corner(UP + LEFT) + RIGHT * .3 + DOWN * .25)
        keys = VGroup(*[RoundedRectangle(width=.6, height=.38, corner_radius=.07, fill_color=PANEL_2,
                                         fill_opacity=1, stroke_color=STROKE, stroke_width=1)
                        for _ in range(20)]).arrange_in_grid(5, 4, buff=(.18, .16)).next_to(screen, DOWN, buff=.35)
        expr = self.M('casio1', .8).set_color('#14202B').move_to(screen.get_center() + DOWN * .05)
        self.play(FadeIn(body), FadeIn(screen), FadeIn(keys), run_time=self.rt(.06))
        self.write_board(badge('MẸO: CHẾ ĐỘ RADIAN', GOLD, 19),
                         para('Kiểm tra nguyên hàm lượng giác trên máy tính: phải để chế độ Radian (R).', 23, WHITE,
                              width=32), frac=.12)
        self.play(FadeIn(mode, scale=1.6), Indicate(keys[0], color=CYAN), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.play(FadeIn(expr), run_time=self.rt(.06))
        self.write_board(self.M('casio1', 1.15), self.M('casio2', 1.3), frac=.12)
        self.write_board(VGroup(check(), tx('khớp nhau  →  F = −cos x đúng', 22, GREEN, bold=True))
                         .arrange(RIGHT, buff=.2), frac=.05)
        self.wait_until(.78, t0)
        self.write_board(tx('Chế độ Độ (D): kết quả sai hoàn toàn!', 22, CORAL, bold=True), frac=.05)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('sin và cos', 'sum1', 'Nhớ dấu trừ ở nguyên hàm của sin'),
                                ('1/cos² và 1/sin²', 'sum2', 'tan và −cot, xét trên từng khoảng'),
                                ('Hạ bậc', 'sum3', 'Gặp sin², cos²: đưa về cos 2x')),
                           fracs=(.04, .3, .72))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm', 'hw1'), ('Tìm', 'hw2'), ('Biết', 'hw3')), ('hw_ans1', 'hw_ans2', 'hw_ans3'),
                       fracs=(.05, .25, .4))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [self.M('next1', 1.3), self.M('next2', 1.05)])


class INT04_SMOKE(INT04):
    smoke = True
