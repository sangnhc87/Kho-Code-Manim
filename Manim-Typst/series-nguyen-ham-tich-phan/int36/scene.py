"""INT36 – Bản đồ tư duy toàn chương · chiến lược 8+/9+ · lộ trình tự học.

    python scripts/build_typst.py --ep int36
    python scripts/prepare_voice.py --ep int36 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int36/scene.py INT36
    python scripts/finalize.py --ep int36

One method per narration beat (int36/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M`` / ``self.TM``).
Every number is checked in lesson.validate().
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, ArcBetweenPoints, Arrow, Circle, Create, FadeIn, FadeOut, LaggedStart, Line, ValueTracker,
                   VGroup, Write, always_redraw)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import axes, badge, band, card, check, clipped, tx  # noqa: E402
from common.lesson_scene import LEFT_CX, LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL, PANEL_2, PURPLE, SOFT, STROKE, WHITE  # noqa: E402
from int36.lesson import BRANCHES  # noqa: E402

COLORS = (CYAN, GREEN, GOLD, PURPLE, CORAL)
ANGLES = (90, 18, -54, -126, 162)
LEAVES = (('a1', 'a2', 'a3', 'a4'), ('b1', 'b2', 'b3', 'b4'), ('c1', 'c2', 'c3', 'c4'), ('d1', 'd2', 'd3'),
          ('e1', 'e2', 'e3'))
KEY_OF = ('a1', 'b1', 'c1', 'd2', 'e3')


class INT36(LessonScene):
    EP = 'int36'

    # ------------------------------------------------------------ helpers
    def node(self, i, w=1.95, h=.88, active=True, size=15):
        code, name, _ = BRANCHES[i]
        col = COLORS[i]
        c = card(w, h, col if active else STROKE, PANEL_2, stroke_width=2.4 if active else 1.6)
        return VGroup(c, tx(code, 22, col if active else SOFT, bold=True).move_to(c.get_top() + DOWN * .27),
                      tx(name, size, WHITE if active else SOFT, max_w=w - .2).move_to(c.get_bottom() + UP * .25))

    def mini_map(self, center, r=2.05, active=None):
        """Centre ∫ plus the five branch nodes on a pentagon; ``active`` = indices drawn in colour."""
        cx, cy = center
        hub = VGroup(Circle(radius=.55, color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                     self.M('core', 1.6)).move_to([cx, cy, 0])
        nodes, lines = VGroup(), VGroup()
        for i, ang in enumerate(ANGLES):
            p = [cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)), 0]
            on = active is None or i in active
            nodes.add(self.node(i, active=on).move_to(p))
            lines.add(Line(hub.get_center(), p, color=COLORS[i] if on else STROKE, stroke_width=3 if on else 2))
        lines.set_z_index(-1)  # connectors run behind the cards
        nodes.set_z_index(1)
        hub.set_z_index(2)
        return hub, nodes, lines

    def branch(self, i, t0, fracs):
        """Light up branch ``i`` on the mini-map and list its key formulas on the board."""
        code, name, (lo, hi) = BRANCHES[i]
        new_node = self.node(i, active=True).move_to(self.map_nodes[i])
        new_node.set_z_index(1)
        new_line = Line(self.map_hub.get_center(), self.map_nodes[i].get_center(), color=COLORS[i], stroke_width=3) \
            .set_z_index(-1)
        self.play(FadeOut(self.map_nodes[i]), FadeIn(new_node, scale=1.1), FadeOut(self.map_lines[i]),
                  Create(new_line), run_time=self.rt(.05))
        self.bring_to_front(self.map_hub)
        self.map_nodes[i], self.map_lines[i] = new_node, new_line
        self.write_board(badge(f'NHÁNH {code} · {name.upper()}', COLORS[i], 20),
                         self.TM(f'tập ${lo}$ – ${hi}$', 21, SOFT), frac=.06)
        for key, frac in zip(LEAVES[i], fracs):
            self.wait_until(frac, t0)
            self.write_board(self.M(key, .82), frac=.07, gap=.3)

    def rows(self, t0, head, color, items, fracs, top=1.6, step=1.15):
        self.clear_stage(.04)
        self.play(FadeIn(badge(head, color, 22).move_to([0, 2.7, 0])), run_time=self.rt(.03))
        for k, ((label, key), frac) in enumerate(zip(items, fracs)):
            y = top - step * k
            c = card(12.4, min(.98, step - .12), color).move_to([0, y, 0])
            lab = VGroup(check(color), tx(label, 23, WHITE, bold=True)).arrange(RIGHT, buff=.2) \
                .move_to(c.get_left() + RIGHT * .3, aligned_edge=LEFT)
            m = self.M(key, 1.0, max_w=6.4)
            if m.height > .85:
                m.scale_to_fit_height(.85)
            m.move_to([2.6, y, 0])
            self.wait_until(frac, t0)
            self.play(FadeIn(VGroup(c, lab), shift=RIGHT * .15), Write(m), run_time=self.rt(.06))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        hub, nodes, lines = self.mini_map((0, -.1), r=2.3)
        scattered = ((-5.2, 2.2), (4.9, 2.0), (5.4, -2.0), (-1.2, -2.4), (-5.6, -1.4))
        targets = [n.get_center() for n in nodes]
        for n, (sx, sy) in zip(nodes, scattered):
            n.move_to([sx, sy, 0])
        self.play(LaggedStart(*[FadeIn(n, scale=.8) for n in nodes], lag_ratio=.3), run_time=self.rt(.25))
        self.wait_until(.5, t0)
        self.play(*[n.animate.move_to(p) for n, p in zip(nodes, targets)], run_time=self.rt(.12))
        self.play(FadeIn(hub, scale=1.3), *[Create(ln) for ln in lines], run_time=self.rt(.08))
        self.bring_to_front(hub)

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Bản đồ tư duy', 'Năm nhánh của cả chương'),
                         ('Chiến lược 8+ / 9+', 'Kèm hai câu thử thách'),
                         ('Lộ trình tự học', 'Bốn tuần với series')], t0, fracs=(.1, .35, .65))

    # ================================================================ BẢN ĐỒ TƯ DUY
    def beat_m1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        hub, nodes, lines = self.mini_map((LEFT_CX, -.2), active=())
        self.play(FadeIn(hub, scale=1.2), run_time=self.rt(.04))
        self.play(*[Create(ln) for ln in lines], LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=.15),
                  run_time=self.rt(.08))
        self.bring_to_front(hub)
        self.map_hub, self.map_nodes, self.map_lines = hub, list(nodes), list(lines)
        self.branch(0, t0, (.3, .45, .62, .78))

    def beat_m2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.branch(1, t0, (.12, .5, .66, .8))

    def beat_m3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.branch(2, t0, (.15, .35, .55, .78))

    def beat_m4(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.branch(3, t0, (.15, .4, .75))

    def beat_m5(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.branch(4, t0, (.15, .3, .7))

    def beat_m5b(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.heading('MỐI NỐI GIỮA CÁC NHÁNH'), frac=.04)
        links = ((0, 1, '$A arrow.r B$: đổi biến, từng phần', .08), (1, 2, '$B arrow.r C$: $S = integral abs(f - g)$', .38),
                 (2, 3, '$C, D$: $abs(f - g)$ và $abs(v)$', .55), (3, 4, '$C, D arrow.r E$: tám bẫy sai', .78))
        for i, j, text, frac in links:
            arc = ArcBetweenPoints(self.map_nodes[i].get_center(), self.map_nodes[j].get_center(), angle=.75,
                                   color=GOLD, stroke_width=5).set_z_index(-1)
            self.wait_until(frac, t0)
            self.play(Create(arc), run_time=self.rt(.05))
            self.bring_to_front(self.map_nodes[i], self.map_nodes[j], self.map_hub)
            self.write_board(self.TM(text, 22, WHITE), frac=.05, gap=.4)

    def beat_m6(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        cx, cy, rx, ry = 0, .6, 4.7, 1.75
        hub = VGroup(Circle(radius=.6, color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                     self.M('core', 1.8)).move_to([cx, cy, 0])
        parts = VGroup()
        for i, ang in enumerate(ANGLES):
            p = [cx + rx * math.cos(math.radians(ang)), cy + ry * math.sin(math.radians(ang)), 0]
            c = card(3.25, 1.1, COLORS[i], PANEL_2, stroke_width=2.4).move_to(p)
            title = tx(f'{BRANCHES[i][0]} · {BRANCHES[i][1]}', 17, COLORS[i], bold=True, max_w=3.0) \
                .move_to(c.get_top() + DOWN * .25)
            m = self.M(KEY_OF[i], .62, max_w=3.0)
            if m.height > .6:
                m.scale_to_fit_height(.6)
            m.move_to(c.get_center() + DOWN * .17)
            parts.add(VGroup(Line(hub.get_center(), p, color=COLORS[i], stroke_width=2.5), c, title, m))
        self.play(FadeIn(hub), LaggedStart(*[FadeIn(g) for g in parts], lag_ratio=.2), run_time=self.rt(.15))
        self.bring_to_front(hub)
        self.wait_until(.25, t0)
        idea = self.M('idea', 1.2).move_to([0, -2.35, 0])
        self.play(Write(idea), run_time=self.rt(.08))
        self.wait_until(.72, t0)
        spine = self.M('spine', 1.15).move_to([0, -2.35, 0])
        self.play(FadeOut(idea), FadeIn(spine, shift=UP * .1), run_time=self.rt(.06))
        self.play(FadeIn(self.box(spine, GOLD)), run_time=self.rt(.03))

    # ================================================================ CHIẾN LƯỢC
    def beat_s1(self, T):
        self.rows(self.now(), 'MỤC TIÊU 8+', GREEN, (('Bảng nguyên hàm', 'a2'), ('Tích phân và tính chất', 'b1'),
                                                     ('Diện tích, thể tích', 'c3'), ('Chuyển động Đúng/Sai', 'd1')),
                  (.08, .3, .5, .66))

    def beat_s2(self, T):
        self.rows(self.now(), 'MỤC TIÊU 9+', GOLD, (('Hàm ẩn, đối xứng', 'b4'), ('Bài toán tham số', 'ch1'),
                                                    ('Mô hình hóa', 'd3'), ('Trả lời ngắn nhiều bước', 'd2')),
                  (.15, .3, .42, .55))

    def beat_s2b(self, T):
        self.rows(self.now(), 'TỪ KHÓA NHẬN DẠNG', CYAN, (('Diện tích', 'c1'), ('Quay quanh Ox', 'c3'),
                                                          ('Quãng đường', 'd1'), ('Tổng lượng', 'd2'),
                                                          ('Chỉ có bảng số', 'd3')),
                  (.1, .3, .48, .64, .8), top=1.75, step=1.0)

    def ch_axes(self):
        a = axes((0, 6.9, 1), (0, 42, 1), 6.0, 5.0, center=[LEFT_CX, -.25, 0], x_ticks=(2, 4, 6), y_ticks=(12, 24, 36),
                 x_label='x', y_label='y')
        return a

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        a = self.ch_axes()
        self.show_axes(a)
        at = ValueTracker(1.5)
        self.ch = (a, at)
        par = clipped(a, lambda v: v * v, 0, 6.5, CYAN, 4, y_max=42)
        line = always_redraw(lambda: clipped(a, lambda v: at.get_value() * v, 0, 6.8, GOLD, 4, y_max=42))
        reg = always_redraw(lambda: band(a, lambda v: at.get_value() * v, lambda v: v * v, 0, at.get_value(), GREEN, .45))
        self.play(Create(par), FadeIn(line), FadeIn(reg), run_time=self.rt(.07))
        self.write_board(VGroup(badge('THỬ THÁCH 9+', GOLD, 20), tx('tham số', 19, SOFT)).arrange(RIGHT, buff=.25),
                         self.M('ch1', 1.05), frac=.12)
        rd = always_redraw(lambda: self.readout([('a', at.get_value(), 1), ('S', at.get_value() ** 3 / 6, 1)], 24)
                           .move_to([3.6, -1.6, 0]))
        self.add(rd)
        self.wait_until(.45, t0)
        self.play(at.animate.set_value(4.5), run_time=self.rt(.3))
        self.write_board(tx('Tạm dừng và thử!', 24, GOLD, bold=True), frac=.04)

    def beat_s4(self, T):
        t0 = self.now()
        a, at = self.ch
        self.clear_board(.03)
        self.write_board(self.M('ch1_s1', 1.0), frac=.1)
        self.wait_until(.3, t0)
        m = self.M('ch1_s2', 1.0)
        self.write_board(m, frac=.1)
        self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))
        self.wait_until(.6, t0)
        self.play(at.animate.set_value(6), run_time=self.rt(.15))

    def beat_s5(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = VGroup(badge('THỬ THÁCH 9+', GOLD, 20), tx('hàm ẩn', 19, SOFT)).arrange(RIGHT, buff=.25)
        q = self.M('ch2', 1.4)
        hint = self.TM('Không cần tìm $f$!', 28, GOLD, bold=True)
        self.centre(head, q, hint, top=2.4, gap=.7)
        self.play(FadeIn(head), Write(q), run_time=self.rt(.15))
        self.wait_until(.75, t0)
        self.play(FadeIn(hint, shift=UP * .1), run_time=self.rt(.05))

    def beat_s6(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        lines = [self.M('ch2', 1.05), self.M('ch2_s1', 1.25), self.M('ch2_s2', 1.25), self.M('ch2_s3', 1.15)]
        self.centre(*lines, top=2.75, gap=.45)
        self.play(FadeIn(lines[0]), run_time=self.rt(.03))
        for m, frac in zip(lines[1:], (.05, .38, .7)):
            self.wait_until(frac, t0)
            self.play(Write(m), run_time=self.rt(.1))
            if m is lines[2]:
                self.play(FadeIn(self.box(m, GREEN)), run_time=self.rt(.03))

    def beat_s7(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('TRONG PHÒNG THI', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        data = (('Phần I', 'Làm chắc trước, không sa đà câu khó', '$approx 1$ phút/câu', CYAN, .05),
                ('Phần II', 'Mỗi ý một lời giải ngắn', '$4$ ý đúng $= 1$ điểm', CORAL, .3),
                ('Phần III', 'Kiểm tra trước khi ghi phiếu', '$integral_a^b f approx$ máy tính', PURPLE, .65))
        for i, (title, note, foot, col, frac) in enumerate(data):
            c = card(4.05, 4.2, col).move_to([-4.3 + 4.3 * i, -.3, 0])
            g = VGroup(c, tx(title, 28, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       self.lbl(note, 21, WHITE, width=22, center=True, max_w=3.6).move_to(c.get_center() + UP * .15),
                       self.TM(foot, 22, GOLD, max_w=3.7).move_to(c.get_bottom() + UP * .75))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))

    # ================================================================ LỘ TRÌNH
    def beat_r1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('LỘ TRÌNH 4 TUẦN', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        axis = Line([-6.2, 1.2, 0], [6.2, 1.2, 0], color=STROKE, stroke_width=4)
        self.play(Create(axis), run_time=self.rt(.04))
        weeks = ((0,), (1,), (2, 3), (4,))
        for w, (idx, frac) in enumerate(zip(weeks, (.08, .3, .5, .72))):
            x0 = -4.65 + 3.1 * w
            dotm = Circle(radius=.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to([x0, 1.2, 0])
            label = VGroup(tx('Tuần', 22, WHITE, bold=True), self.TM(f'${w + 1}$', 24, GOLD)).arrange(RIGHT, buff=.12) \
                .move_to([x0, 1.75, 0])
            stack = VGroup(*[self.node(i, w=2.8, h=1.0, size=17) for i in idx]).arrange(DOWN, buff=.18) \
                .next_to(dotm, DOWN, buff=.45)
            eps = VGroup(*[self.TM(f'tập ${BRANCHES[i][2][0]}$ – ${BRANCHES[i][2][1]}$', 18, SOFT) for i in idx])
            for e, n in zip(eps, stack):
                e.next_to(n, DOWN, buff=.08)
            if len(idx) == 2:
                stack[1].shift(DOWN * .3)
                eps[1].next_to(stack[1], DOWN, buff=.08)
            self.wait_until(frac, t0)
            self.play(FadeIn(dotm, scale=1.4), FadeIn(label), FadeIn(stack, shift=DOWN * .15), FadeIn(eps),
                      run_time=self.rt(.06))

    def beat_r2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('HỌC MỖI TẬP THEO 4 BƯỚC', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        steps = (('Xem bản chất', CYAN), ('Tạm dừng, tự giải', GREEN), ('Bài tự luyện', GOLD), ('Sổ lỗi sai', CORAL))
        prev = None
        for i, ((title, col), frac) in enumerate(zip(steps, (.05, .2, .45, .6))):
            c = card(2.65, 2.2, col).move_to([-4.95 + 3.3 * i, .3, 0])
            g = VGroup(c, self.TM(f'${i + 1}$', 44, col, bold=True).move_to(c.get_top() + DOWN * .65),
                       tx(title, 21, WHITE, bold=True, max_w=2.4).move_to(c.get_center() + DOWN * .35))
            anims = [FadeIn(g, shift=UP * .2)]
            if prev is not None:
                anims.append(FadeIn(Arrow(prev.get_right(), c.get_left(), buff=.08, color=SOFT, stroke_width=4,
                                          max_tip_length_to_length_ratio=.35)))
            self.wait_until(frac, t0)
            self.play(*anims, run_time=self.rt(.05))
            prev = c
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('Lời giảng đầy đủ của từng tập: phần mô tả video', 22, SOFT).move_to([0, -1.9, 0])),
                  run_time=self.rt(.05))

    def beat_r2b(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('NGÀY TRƯỚC KỲ THI', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        steps = (('Vẽ lại bản đồ', 'core', CYAN), ('Bảng nguyên hàm', 'a2', GREEN), ('Tám bẫy, sổ lỗi sai', 'e2', CORAL))
        for i, ((title, key, col), frac) in enumerate(zip(steps, (.1, .3, .48))):
            c = card(4.05, 3.0, col).move_to([-4.3 + 4.3 * i, .45, 0])
            m = self.M(key, 1.1 if key != 'core' else 1.8, max_w=3.6)
            g = VGroup(c, tx(title, 23, col, bold=True).move_to(c.get_top() + DOWN * .5), m.move_to(c.get_center() + DOWN * .3))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('và ngủ đủ giấc!', 30, GOLD, bold=True).move_to([0, -1.9, 0])), run_time=self.rt(.05))

    def beat_r3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        hub, nodes, lines = self.mini_map((LEFT_CX, -.2))
        self.play(FadeIn(hub), *[Create(ln) for ln in lines], LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=.15),
                  run_time=self.rt(.15))
        self.bring_to_front(hub)
        self.write_board(self.heading('MẸO CUỐI'), self.TM('mỗi tối: vẽ lại bản đồ trong $5$ phút', 24, WHITE), frac=.1)
        self.wait_until(.55, t0)
        self.write_board(self.TM('nhánh chưa trọn: xem lại ngày mai', 24, GOLD, bold=True), frac=.06)

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.summary_cards(t0, (('Hai chiều', 'sum1', 'Nguyên hàm và đạo hàm'),
                                ('Giới hạn của tổng', 'sum2', 'Cắt nhỏ rồi cộng lại'),
                                ('Ứng dụng', 'sum3', 'Diện tích, thể tích, quãng đường, tổng lượng')),
                           fracs=(.04, .35, .62))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.exercises(t0, (('Tìm a:', 'hw1'), ('Hàm ẩn:', 'hw2'), ('Diện tích:', 'hw3')),
                       ('hw_ans1', 'hw_ans2', 'hw_ans3'), fracs=(.04, .3, .62))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        box = card(10.8, 4.4, GOLD, PANEL, radius=.3, stroke_width=2.6).move_to([0, .45, 0])
        tag = badge('HOÀN THÀNH SERIES', GOLD, 22).move_to(box.get_top() + DOWN * .55)
        stats = VGroup(self.TM('$36$ tập', 34, WHITE, bold=True), tx('·', 34, SOFT),
                       self.TM('$5$ phần', 34, WHITE, bold=True), tx('·', 34, SOFT),
                       self.TM('$1$ ý tưởng', 34, WHITE, bold=True)).arrange(RIGHT, buff=.3).move_to([0, 1.15, 0])
        name = tx('Nguyên hàm – Tích phân – Ứng dụng chuyên sâu', 28, CYAN, bold=True, max_w=10).move_to([0, .3, 0])
        wish = tx('Chúc các em tự tin chinh phục kỳ thi!', 26, GOLD, bold=True).move_to([0, -.55, 0])
        self.play(FadeIn(box), FadeIn(tag, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(FadeIn(stats, shift=UP * .15), run_time=self.rt(.08))
        self.play(Write(name), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.play(FadeIn(wish), run_time=self.rt(.06))
        self.wait_until(.7, t0)
        self.play(FadeIn(tx('Hẹn gặp lại ở series tiếp theo!', 28, WHITE, bold=True).move_to([0, -2.4, 0])),
                  run_time=self.rt(.06))


class INT36_SMOKE(INT36):
    smoke = True
