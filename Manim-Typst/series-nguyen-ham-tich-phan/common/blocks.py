"""Reusable teaching blocks shared by every INT episode.

Mixed into ``LessonScene``: board helpers, timing helpers and the standard
screens of the series (title card, goals, Đúng/Sai question, short-answer
sheet, verification plot, summary, exercises, next episode).
"""
from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, Create, Rectangle, FadeIn, FadeOut, LaggedStart, Line,
                   RoundedRectangle, VGroup, Write, always_redraw, Dot)

from common.kit import badge, card, clipped, dashed, para, tangent, tx, vn
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL, PANEL_2, PURPLE, SOFT, STROKE, WHITE

BOARD_X = 0.55
TF_SOLUTION_Y = -2.72   # worked line under a Đúng/Sai question
GOAL_COLORS = (CYAN, GREEN, GOLD)


class Blocks:
    # ------------------------------------------------------------ timing
    def now(self):
        return self.renderer.time

    def wait_until(self, frac, start):
        """Hold until ``frac`` of the beat has elapsed (keeps visuals on the narration)."""
        target = start + frac * self.T
        if target - self.renderer.time > 1.5 / 30:
            self.wait(target - self.renderer.time)

    # ------------------------------------------------------------ board
    def heading(self, text, color=GOLD):
        return tx(text, 22, color, bold=True)

    def write_board(self, *mobs, frac=0.08, gap=0.32):
        for m in mobs:
            self.board(m, gap=gap)
        self.play(LaggedStart(*[Write(m) if m.__class__.__name__ == 'SVGMobject' else FadeIn(m, shift=.1 * UP)
                                for m in mobs], lag_ratio=.35), run_time=self.rt(frac))

    def stage_board_tail(self):
        """Mobjects on the right column (x > 0.3) that are not chrome."""
        return [m for m in self.stage() if m.get_center()[0] > .3]

    def clear_board(self, frac=.04):
        tail = self.stage_board_tail()
        if tail:
            self.play(*[FadeOut(m) for m in tail], run_time=self.rt(frac))
        self.board_items = []

    # ------------------------------------------------------------ standard screens
    def title_card(self):
        ep = self.lesson.EPISODE
        frame = card(10.6, 4.4, CYAN, PANEL, radius=.3, stroke_width=2.4).move_to([0, .1, 0])
        tag = badge(f"TẬP {ep['number']:02d} / 36", CYAN, 20).move_to(frame.get_top() + DOWN * .55)
        title = tx(ep['title'].upper(), 58, WHITE, bold=True, max_w=9.8).move_to([0, .55, 0])
        sub = tx(ep['subtitle'], 32, GOLD, max_w=9.6).next_to(title, DOWN, buff=.28)
        series = tx('Series Nguyên hàm – Tích phân – Ứng dụng chuyên sâu', 20, SOFT).next_to(sub, DOWN, buff=.42)
        self.play(FadeIn(frame), FadeIn(tag, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(Write(title), run_time=self.rt(.14))
        self.play(FadeIn(sub, shift=UP * .15), FadeIn(series), run_time=self.rt(.1))

    def goal_cards(self, goals, t0, fracs=(.1, .3, .52)):
        head = tx('MỤC TIÊU CỦA BÀI', 26, GOLD, bold=True).move_to([0, 2.55, 0])
        cards = VGroup()
        for i, (title, desc) in enumerate(goals):
            col = GOAL_COLORS[i % 3]
            c = card(4.05, 3.3, col).move_to([-4.3 + 4.3 * i, -.15, 0])
            num = tx(str(i + 1), 54, col, bold=True).move_to(c.get_top() + DOWN * .7)
            t = para(title, 24, WHITE, width=18, bold=True, center=True).move_to(c.get_center() + DOWN * .05)
            d = para(desc, 17, SOFT, width=24, center=True).move_to(c.get_bottom() + UP * .62)
            cards.add(VGroup(c, num, t, d))
        self.play(FadeIn(head), run_time=self.rt(.05))
        for frac, cd in zip(fracs, cards):
            self.wait_until(frac, t0)
            self.play(FadeIn(cd, shift=UP * .25), run_time=self.rt(.07))

    def pause_chip(self, y=-2.6):
        bars = VGroup(*[RoundedRectangle(width=.12, height=.42, corner_radius=.03, fill_color=GOLD,
                                         fill_opacity=1, stroke_width=0) for _ in range(2)]).arrange(RIGHT, buff=.1)
        return VGroup(bars, tx('Tạm dừng video và tự làm!', 22, GOLD, bold=True)).arrange(RIGHT, buff=.2) \
            .move_to([0, y, 0])

    def tf_question(self, t0, intro, items, fracs=(.3, .78)):
        """Phần II question: ``intro`` = list of mobjects (lines), ``items`` = 4 statement mobjects."""
        head = VGroup(badge('ĐÚNG / SAI', CORAL, 20), tx('dạng câu hỏi Phần II – đề thi tốt nghiệp THPT', 19, SOFT)) \
            .arrange(RIGHT, buff=.3).move_to([0, 2.72, 0]).to_edge(LEFT, buff=.6)
        lines = VGroup(*intro).arrange(DOWN, aligned_edge=LEFT, buff=.22).next_to(head, DOWN, buff=.35) \
            .align_to(head, LEFT)
        # Statements are stacked by their real heights (fractions make some rows taller)
        # and shrunk together if they would run into the solution line (TF_SOLUTION_Y).
        bodies = VGroup()
        for k, body in zip('abcd', items):
            r = VGroup(tx(f'{k})', 24, GOLD, bold=True), body).arrange(RIGHT, buff=.3)
            if r.width > 10.4:
                r.scale_to_fit_width(10.4)
            if r.height < .6:  # keep room for the Đúng/Sai slot of short rows
                r.add(Rectangle(width=.01, height=.6, stroke_opacity=0, fill_opacity=0).move_to(r.get_left()))
            bodies.add(r)
        bodies.arrange(DOWN, aligned_edge=LEFT, buff=.14)
        top = lines.get_bottom()[1] - .22
        room = top - (TF_SOLUTION_Y + .5)
        if bodies.height > room:
            bodies.scale(room / bodies.height)
        bodies.move_to([0, top, 0], aligned_edge=UP).align_to(head, LEFT).shift(RIGHT * .3)
        rows = VGroup()
        for r in bodies:
            slot = RoundedRectangle(width=1.25, height=min(.5, .9 * r.height), corner_radius=.08, stroke_color=STROKE,
                                    stroke_width=2, fill_color=PANEL_2, fill_opacity=1).move_to([5.6, r.get_y(), 0])
            rows.add(VGroup(r, slot))
        self.play(FadeIn(head), run_time=self.rt(.04))
        self.play(FadeIn(lines[0], shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(fracs[0], t0)
        if len(lines) > 1:
            self.play(*[FadeIn(m, shift=UP * .1) for m in lines[1:]], run_time=self.rt(.07))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * .2) for r in rows], lag_ratio=.3), run_time=self.rt(.2))
        self.wait_until(fracs[1], t0)
        pause = self.pause_chip(TF_SOLUTION_Y)
        self.play(FadeIn(pause, scale=1.1), run_time=self.rt(.06))
        self.tf_rows, self.tf_pause = rows, pause

    def tf_key(self, answers):
        """Answer key next to the question header, e.g. answers = 'ĐSĐĐ'."""
        text = '   '.join(f'{k}) {a}' for k, a in zip('abcd', answers))
        return tx(f'Đáp án:  {text}', 22, GOLD, bold=True).move_to([0, 2.72, 0]).to_edge(RIGHT, buff=.6)

    def tf_mark(self, i, ok):
        slot = self.tf_rows[i][1]
        b = badge('ĐÚNG' if ok else 'SAI', GREEN if ok else CORAL, 18)
        if b.height > slot.height:
            b.scale_to_fit_height(slot.height)
        b.move_to(slot)
        return FadeIn(b, scale=1.3)

    def answer_sheet(self, value):
        """Phiếu trả lời ngắn: 4 ô, điền ``value`` từ trái sang."""
        cells = VGroup(*[RoundedRectangle(width=.55, height=.68, corner_radius=.06, stroke_color=SOFT,
                                          stroke_width=2) for _ in range(4)]).arrange(RIGHT, buff=.08)
        chars = VGroup(*[tx(ch, 30, GREEN, bold=True).move_to(cells[i]) for i, ch in enumerate(str(value)[:4])])
        return VGroup(tx('Phiếu trả lời:', 20, SOFT), VGroup(cells, chars)).arrange(RIGHT, buff=.25)

    def verify_plot(self, a, f, F, x_from, x_to, frac, x_min=None, x_max=None, f_color=CYAN, F_color=GOLD,
                    readout_at=(BOARD_X, -1.75)):
        """Graphs of f and F; a moving x shows: slope of F's tangent = height of f."""
        lo = a.x_range[0] if x_min is None else x_min
        hi = a.x_range[1] if x_max is None else x_max
        gf = clipped(a, f, lo, hi, f_color, 4)
        gF = clipped(a, F, lo, hi, F_color, 4.5)
        self.play(Create(gf), Create(gF), run_time=self.rt(.08))
        from manim import ValueTracker
        xt = ValueTracker(x_from)
        live = always_redraw(lambda: VGroup(
            tangent(a, xt.get_value(), F(xt.get_value()), f(xt.get_value()), 1.6),
            Dot(a.c2p(xt.get_value(), F(xt.get_value())), radius=.08, color=GOLD),
            Line(a.c2p(xt.get_value(), 0), a.c2p(xt.get_value(), f(xt.get_value())), color=f_color, stroke_width=5),
            Dot(a.c2p(xt.get_value(), f(xt.get_value())), radius=.07, color=f_color),
            dashed(a.c2p(xt.get_value(), F(xt.get_value())), a.c2p(xt.get_value(), f(xt.get_value())),
                   color=SOFT, stroke_width=1.5)))
        reading = always_redraw(lambda: VGroup(
            tx(f'x = {vn(xt.get_value())}', 22, WHITE),
            tx(f'độ dốc của F = {vn(f(xt.get_value()))} = f(x)', 22, GOLD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.14).move_to([readout_at[0], readout_at[1], 0], aligned_edge=LEFT))
        self.play(FadeIn(live), FadeIn(reading), run_time=self.rt(.04))
        self.play(xt.animate.set_value(x_to), run_time=self.rt(frac))
        live.clear_updaters()
        reading.clear_updaters()
        return VGroup(gf, gF, live, reading)

    def summary_cards(self, t0, data, fracs=(.04, .3, .72), head_text='3 Ý CẦN NHỚ'):
        """``data`` = [(title, formula_key, note)] × 3."""
        head = tx(head_text, 28, GOLD, bold=True).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        for i, (title, key, note) in enumerate(data):
            col = GOAL_COLORS[i % 3]
            c = card(4.05, 4.4, col).move_to([-4.3 + 4.3 * i, -.35, 0])
            num = tx(str(i + 1), 46, col, bold=True).move_to(c.get_top() + DOWN * .6)
            t = tx(title, 24, WHITE, bold=True, max_w=3.7).next_to(num, DOWN, buff=.25)
            nt = para(note, 18, SOFT, width=24, center=True).next_to(t, DOWN, buff=.3)
            m = self.M(key, 1.05, max_w=3.6).move_to(c.get_bottom() + UP * .8)
            self.wait_until(fracs[i], t0)
            self.play(FadeIn(VGroup(c, num, t, nt), shift=UP * .2), Write(m), run_time=self.rt(.08))

    def exercises(self, t0, rows, answers, fracs=(.05, .2, .45), show_answers=.8):
        """``rows`` = [(intro text, formula_key)], ``answers`` = formula keys."""
        head = badge('BÀI TẬP TỰ LUYỆN', CYAN, 20).move_to([0, 2.65, 0])
        self.play(FadeIn(head), run_time=self.rt(.03))
        group = VGroup()
        for i, (intro, key) in enumerate(rows):
            r = VGroup(tx(f'{i + 1}.', 26, CYAN, bold=True), tx(intro, 24, WHITE), self.M(key, 1.2)) \
                .arrange(RIGHT, buff=.25)
            if r.width > 8.6:
                r.scale_to_fit_width(8.6)
            r.move_to([0, 1.45 - 1.15 * i, 0]).to_edge(LEFT, buff=.8)
            group.add(r)
        for frac, r in zip(fracs, group):
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.06))
        self.wait_until(show_answers, t0)
        ans = VGroup(*[self.M(k, 1.1, max_w=2.5).set_color(GREEN) for k in answers])
        for m, r in zip(ans, group):
            m.move_to([5.35, r.get_y(), 0])
        lbl = tx('Đáp số', 20, GREEN, bold=True).move_to([5.35, 2.2, 0])
        rule = Line([4.0, 2.0, 0], [4.0, -1.3, 0], color=STROKE, stroke_width=2)
        self.play(FadeIn(lbl), FadeIn(rule), LaggedStart(*[FadeIn(m) for m in ans], lag_ratio=.3),
                  run_time=self.rt(.1))

    def next_card(self, t0, lines, thanks_at=.58):
        ep = self.lesson.EPISODE
        box = card(10.8, 4.7, PURPLE, PANEL, radius=.3, stroke_width=2.4).move_to([0, .6, 0])
        tag = badge(f"TẬP SAU · {ep['next_code']}", PURPLE, 20).move_to(box.get_top() + DOWN * .55)
        title = tx(ep['next_title'], 38, WHITE, bold=True, max_w=10).move_to(box.get_center() + UP * .75)
        body = VGroup(*lines).arrange(DOWN, buff=.3).next_to(title, DOWN, buff=.4)
        if body.width > 10:
            body.scale_to_fit_width(10)
        thanks = tx('Cảm ơn các em đã theo dõi!', 28, GOLD, bold=True).move_to([0, -2.5, 0])
        self.play(FadeIn(box), FadeIn(tag, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(Write(title), run_time=self.rt(.14))
        self.play(FadeIn(body, shift=UP * .1), run_time=self.rt(.08))
        self.wait_until(thanks_at, t0)
        self.play(FadeIn(thanks, shift=UP * .15), run_time=self.rt(.08))
        self.wait_until(.88, t0)
        self.play(*[FadeOut(m) for m in self.stage()], run_time=self.rt(.08))

    def show_axes(self, a, frac=.05):
        self.play(FadeIn(a), FadeIn(a.labels), run_time=self.rt(frac))

    def centre(self, *mobs, top=2.55, gap=.42):
        """Stack mobjects centred on the full width (no graph column)."""
        g = VGroup(*mobs).arrange(DOWN, buff=gap)
        g.move_to([0, top, 0], aligned_edge=UP)
        return g

    def worked(self, t0, tag, keys, fracs, scales=None, box_last=True, gap=.34):
        """Centred worked example: badge + formula lines revealed at the given beat fractions."""
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
        return lines

    def box(self, mob, color=GOLD):
        from manim import SurroundingRectangle
        return SurroundingRectangle(mob, color=color, buff=.16, corner_radius=.1)

