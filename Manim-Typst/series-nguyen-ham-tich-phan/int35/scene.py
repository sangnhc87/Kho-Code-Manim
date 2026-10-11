"""INT35 – Luyện đề theo cấu trúc thi tốt nghiệp: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.

    python scripts/build_typst.py --ep int35
    python scripts/prepare_voice.py --ep int35 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int35/scene.py INT35
    python scripts/finalize.py --ep int35

One method per narration beat (int35/lesson.py); shared screens come from
common/blocks.py. All math on screen is Typst (``self.M`` / ``self.TM``).
Every answer is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import (DOWN, LEFT, PI, RIGHT, TAU, UP, Arc, Circle, FadeIn, FadeOut, LaggedStart, ValueTracker, VGroup,
                   Write, always_redraw, linear)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, card, tx  # noqa: E402
from common.lesson_scene import LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, STROKE, WHITE  # noqa: E402
from int35.lesson import MC, SHORT, TF_KEYS  # noqa: E402

TIMER_AT = (6.3, 2.72)
TF_GIVEN = ('d1_given', 'd2_given', 'd3_given', 'd4_given')
TF_ITEMS = (('d1a', 'd1b', 'd1c', 'd1d'), ('d2a', 'd2b', 'd2c', 'd2d'), ('d3a', 'd3b', 'd3c', 'd3d'),
            ('d4a', 'd4b', 'd4c', 'd4d'))
MC_KEYS = (
    ('q1', ('q1a', 'q1b', 'q1c', 'q1d'), 'q1_s'),
    ('q2', ('q2a', 'q2b', 'q2c', 'q2d'), 'q2_s'),
    ('q3', ('q3a', 'q3b', 'q3c', 'q3d'), 'q3_s'),
    ('q4', ('q4a', 'q4b', 'q4c', 'q4d'), 'q4_s'),
    ('q5', ('q5a', 'q5b', 'q5c', 'q5d'), 'q5_s'),
    ('q6', ('q6a', 'q6b', 'q6c', 'q6d'), 'q6_s'),
    ('q7', ('q7a', 'q7b', 'q7c', 'q7d'), 'q7_s'),
    ('q8', ('q8a', 'q8b', 'q8c', 'q8d'), 'q8_s'),
    ('q9', ('q9a', 'q9b', 'q9c', 'q9d'), 'q9_s'),
    ('q10', ('q10a', 'q10b', 'q10c', 'q10d'), 'q10_s'),
    ('q11', ('q11a', 'q11b', 'q11c', 'q11d'), 'q11_s'),
    ('q12', ('q12a', 'q12b', 'q12c', 'q12d'), 'q12_s'),
)
SHORT_TASK = ('t1', 't2', 't3', 't4', 't5', 't6')
SHORT_SOL = ('t1_s', 't2_s', 't3_s', 't4_s', 't5_s', 't6_s')


class INT35(LessonScene):
    EP = 'int35'

    # ------------------------------------------------------------ helpers
    def timer(self, label, t0, start, end):
        """Count-down ring in the top-right corner, emptied between two beat fractions."""
        k = ValueTracker(0)
        pos = [TIMER_AT[0], TIMER_AT[1], 0]
        bg = Circle(radius=.27, color=STROKE, stroke_width=6).move_to(pos)
        ring = always_redraw(lambda: Arc(radius=.27, start_angle=PI / 2, angle=-TAU * max(1e-3, 1 - k.get_value()),
                                         arc_center=pos, color=GOLD if k.get_value() < .8 else CORAL, stroke_width=6))
        lab = self.TM(label, 18, SOFT).next_to(bg, LEFT, buff=.18)
        self.wait_until(start, t0)
        self.play(FadeIn(VGroup(bg, lab)), FadeIn(ring), run_time=self.rt(.02))
        self.play(k.animate.set_value(1), run_time=self.rt(max(.05, end - start - .03)), rate_func=linear)
        ring.clear_updaters()
        self.timer_group = VGroup(bg, ring, lab)
        return self.timer_group

    def mc(self, n):
        t0 = self.now()
        q, opts, sol = MC_KEYS[n - 1]
        k = MC[n - 1][2]
        assert MC[n - 1] == (q, opts, k, sol), n
        self.clear_stage(.04)
        self.mc_question(t0, n, [self.M(q, 1.4)], [self.M(o, 1.4) for o in opts], fracs=(.1, .22))
        self.timer('$1$ phút', t0, .26, .5)
        self.play(FadeOut(self.timer_group), *self.mc_mark(k, self.M(sol, 1.3)), run_time=self.rt(.08))

    def tf_ask(self, n):
        t0 = self.now()
        self.clear_stage(.05)
        intro = VGroup(tx(f'Câu {n}:', 24, GOLD, bold=True), self.M(TF_GIVEN[n - 1], 1.25)).arrange(RIGHT, buff=.25)
        items = [self.M(key, 1.2) for key in TF_ITEMS[n - 1]]
        self.tf_question(t0, [intro], items, fracs=(.2, .45))
        self.timer('$3$ phút', t0, .55, .97)

    def tf_answer(self, n, fracs):
        t0 = self.now()
        key = TF_KEYS[n - 1]
        self.play(FadeOut(self.tf_pause), FadeOut(self.timer_group), self.tf_mark(0, key[0] == 'Đ'), run_time=self.rt(.05))
        for i in (1, 2, 3):
            self.wait_until(fracs[i - 1], t0)
            self.play(self.tf_mark(i, key[i] == 'Đ'), run_time=self.rt(.05))
        self.wait_until(.92, t0)
        self.play(FadeIn(self.tf_key(key), shift=LEFT * .1), run_time=self.rt(.04))

    def short(self, n, fracs=(.42, .86)):
        t0 = self.now()
        task, value = SHORT_TASK[n - 1], SHORT[n - 1][1]
        assert SHORT[n - 1][0] == task, n
        self.clear_stage(.05)
        tag = VGroup(badge(f'CÂU {n}', PURPLE, 20), tx('trả lời ngắn – Phần III', 19, SOFT)).arrange(RIGHT, buff=.3)
        m_task, m_sol = self.M(task, 1.45), self.M(SHORT_SOL[n - 1], 1.25)
        sheet = self.answer_sheet(value)
        self.centre(tag, m_task, m_sol, sheet, top=2.7, gap=.6)
        self.play(FadeIn(tag), Write(m_task), run_time=self.rt(.1))
        self.timer('$3$ phút', t0, .13, fracs[0])
        self.play(FadeOut(self.timer_group), Write(m_sol), run_time=self.rt(.12))
        self.wait_until(fracs[1], t0)
        self.play(FadeIn(sheet), run_time=self.rt(.05))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        blocks = VGroup()
        for i, (num, label, col) in enumerate((('12', 'trắc nghiệm', CYAN), ('4', 'đúng / sai', CORAL),
                                               ('6', 'trả lời ngắn', PURPLE))):
            c = card(3.7, 3.0, col).move_to([-4.1 + 4.1 * i, .5, 0])
            blocks.add(VGroup(c, self.TM(f'${num}$', 80, col).move_to(c.get_center() + UP * .35),
                              tx(label, 24, WHITE).move_to(c.get_bottom() + UP * .55)))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .2) for b in blocks], lag_ratio=.5), run_time=self.rt(.35))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.M('next1', 1.3).move_to([0, -1.9, 0])), run_time=self.rt(.07))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('ĐIỂM SỐ VÀ THỜI GIAN', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        for i, (name, key, hint, col, frac) in enumerate((('Phần I', 'score1', '$approx 1$ phút/câu', CYAN, .03),
                                                           ('Phần II', 'score2', '$approx 3$ phút/câu', CORAL, .25),
                                                           ('Phần III', 'score3', '$approx 3$ phút/câu', PURPLE, .7))):
            c = card(4.05, 2.9, col).move_to([-4.3 + 4.3 * i, .45, 0])
            g = VGroup(c, tx(name, 26, col, bold=True).move_to(c.get_top() + DOWN * .5),
                       self.M(key, 1.25).move_to(c.get_center() + DOWN * .05),
                       self.TM(hint, 20, SOFT).move_to(c.get_bottom() + UP * .45))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.05))
            if i == 1:
                self.wait_until(.35, t0)
                self.play(FadeIn(self.M('tf_rule', 1.1).move_to([0, -1.75, 0])), run_time=self.rt(.06))
        self.wait_until(.88, t0)
        self.play(FadeIn(self.TM('Tổng: $3 + 4 + 3 = 10$ điểm', 26, GOLD, bold=True).move_to([0, -2.55, 0])),
                  run_time=self.rt(.04))

    # ================================================================ PHẦN I
    def beat_q1(self, T):
        self.mc(1)

    def beat_q2(self, T):
        self.mc(2)

    def beat_q3(self, T):
        self.mc(3)

    def beat_q4(self, T):
        self.mc(4)

    def beat_q5(self, T):
        self.mc(5)

    def beat_q6(self, T):
        self.mc(6)

    def beat_q7(self, T):
        self.mc(7)

    def beat_q8(self, T):
        self.mc(8)

    def beat_q9(self, T):
        self.mc(9)

    def beat_q10(self, T):
        self.mc(10)

    def beat_q11(self, T):
        self.mc(11)

    def beat_q12(self, T):
        self.mc(12)

    # ================================================================ PHẦN II
    def beat_d1(self, T):
        self.tf_ask(1)

    def beat_d2(self, T):
        self.tf_answer(1, (.2, .38, .7))

    def beat_d3(self, T):
        self.tf_ask(2)

    def beat_d4(self, T):
        self.tf_answer(2, (.2, .55, .78))

    def beat_d5(self, T):
        self.tf_ask(3)

    def beat_d6(self, T):
        self.tf_answer(3, (.25, .5, .75))

    def beat_d7(self, T):
        self.tf_ask(4)

    def beat_d8(self, T):
        self.tf_answer(4, (.18, .42, .65))

    # ================================================================ PHẦN III
    def beat_t1(self, T):
        self.short(1)

    def beat_t2(self, T):
        self.short(2)

    def beat_t3(self, T):
        self.short(3, (.5, .85))

    def beat_t4(self, T):
        self.short(4)

    def beat_t5(self, T):
        self.short(5)

    def beat_t6(self, T):
        self.short(6, (.48, .82))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(badge('BẢNG ĐÁP ÁN', GOLD, 21).move_to([0, 2.7, 0])), run_time=self.rt(.03))
        rows = []
        cells = VGroup()
        for n, (_, _, k, _) in enumerate(MC, 1):
            c = card(.8, .95, CYAN).move_to([-4.45 + .88 * (n - 1), 1.55, 0])
            cells.add(VGroup(c, self.TM(f'${n}$', 15, SOFT).move_to(c.get_top() + DOWN * .2),
                             tx('ABCD'[k], 26, CYAN, bold=True).move_to(c.get_center() + DOWN * .12)))
        rows.append(VGroup(tx('Phần I', 22, CYAN, bold=True).move_to([-6.1, 1.55, 0]), cells))
        tfs = VGroup()
        for n, key in enumerate(TF_KEYS, 1):
            c = card(2.45, .8, CORAL).move_to([-3.9 + 2.65 * (n - 1), .1, 0])
            tfs.add(VGroup(c, VGroup(self.TM(f'${n}$:', 20, SOFT), tx('  '.join(key), 22, CORAL, bold=True))
                           .arrange(RIGHT, buff=.2).move_to(c)))
        rows.append(VGroup(tx('Phần II', 22, CORAL, bold=True).move_to([-6.1, .1, 0]), tfs))
        shorts = VGroup()
        for n, (_, value) in enumerate(SHORT, 1):
            c = card(1.62, .9, PURPLE).move_to([-4.0 + 1.78 * (n - 1), -1.35, 0])
            body = f'"{value}"' if ',' in value else value
            shorts.add(VGroup(c, VGroup(self.TM(f'${n}$:', 17, SOFT), self.TM(f'${body}$', 24, PURPLE))
                              .arrange(RIGHT, buff=.14).move_to(c)))
        rows.append(VGroup(tx('Phần III', 22, PURPLE, bold=True).move_to([-6.1, -1.35, 0]), shorts))
        for row, frac in zip(rows, (.05, .38, .66)):
            self.wait_until(frac, t0)
            self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(c, shift=UP * .1) for c in row[1]], lag_ratio=.12),
                      run_time=self.rt(.12))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('TỰ CHẤM ĐIỂM', 27, GOLD, bold=True).move_to([0, 2.65, 0])), run_time=self.rt(.03))
        lines = VGroup(*[VGroup(tx(name, 24, col, bold=True), self.M(key, 1.3)).arrange(RIGHT, buff=.4)
                         for name, key, col in (('Phần I', 'score1', CYAN), ('Phần II', 'score2', CORAL),
                                                ('Phần III', 'score3', PURPLE))]).arrange(DOWN, aligned_edge=LEFT, buff=.35)
        lines.move_to([0, .9, 0])
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * .2) for m in lines], lag_ratio=.4), run_time=self.rt(.2))
        self.wait_until(.5, t0)
        note = VGroup(badge('SỔ LỖI SAI', CORAL, 20), tx('câu sai thuộc bẫy nào trong tám bẫy của tập 34?', 22, WHITE)) \
            .arrange(RIGHT, buff=.3).move_to([0, -1.6, 0])
        self.play(FadeIn(note, shift=UP * .15), run_time=self.rt(.06))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx('Ghi lại để không lặp lại lần sau!', 24, GREEN, bold=True).move_to([0, -2.45, 0])),
                  run_time=self.rt(.05))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Tập cuối · Chiến lược 8+ / 9+', 28, GOLD, bold=True), self.M('next1', 1.2)])


class INT35_SMOKE(INT35):
    smoke = True
