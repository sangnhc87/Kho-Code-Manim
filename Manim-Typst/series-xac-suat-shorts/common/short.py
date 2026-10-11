"""Base scene of every vertical Short (1080 × 1920, ≤ 3 min).

A Short module ``xss/xssNNN.py`` provides EPISODE, PARTS, BEATS, FORMULAS,
PROBLEM (lines, Typst inside ``$…$``), OPTIONS/CORRECT for the guessing game,
ANSWER_VALUE (for the 0 – 1 probability meter) and a scene subclass with one
``beat_<id>(T)`` method per custom beat. ``hook``, ``guess``, ``answer`` and
``outro`` have standard implementations here.

Fixed screen zones (scene units, frame 8 × 14.22):
  top band 6.2 – 7.1 · title + problem 3.9 – 6.0 · stage −1.3 – 3.6 ·
  board −3.5 – −1.5 · captions ≈ −4.1 · nothing important below −4.7
  (YouTube's buttons) or right of x = 3.1 in the lower half.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from manim import (DOWN, LEFT, PI, RIGHT, TAU, UP, Arc, Circle, Create, FadeIn, FadeOut, Line, Rectangle,
                   RoundedRectangle, Scene, SurroundingRectangle, Triangle, VGroup, Write, config)

from common import shortlib
from common.kit import BAR_WIDTH, Formula, badge, card, tx
from common.theme import (AUTHOR, BG, CORAL, CYAN, DIM, FRAME_H, FRAME_W, GOLD, GREEN, INK, LEVEL_COLORS,
                          MATH_SCALE, PANEL, SERIES, SOFT, STROKE, WHITE)

config.background_color = BG
config.frame_width = FRAME_W
config.frame_height = FRAME_H

TITLE_Y = 5.6
PROBLEM_TOP = 5.05
STAGE_Y = 1.15
BOARD_TOP = -0.7
BOARD_BOTTOM = -3.45
BOARD_X = -0.25
BOARD_W = 6.8
CAPTION_Y = -4.22
LEVEL_NAMES = {'L1': 'MỞ ĐẦU', 'L2': 'CƠ BẢN', 'L3': 'THÔNG HIỂU', 'L4': 'VẬN DỤNG', 'L5': 'KHÓ', 'L6': 'RẤT KHÓ'}


@dataclass(frozen=True)
class Beat:
    id: str
    part: str
    text: str
    chapter: str | None = None


PARTS = (('hook', 'Đề bài'), ('solve', 'Lời giải'), ('outro', 'Kết'))


def formulas(answer: str, options=(), **extra) -> dict:
    """FORMULAS dict of a Short: the boxed answer, the guessing options opt0…, plus extras."""
    d = {'answer': answer}
    d.update({f'opt{i}': o for i, o in enumerate(options)})
    d.update(extra)
    return d


def outro_text(n: int) -> str:
    """Standard closing line pointing to the next challenge."""
    plan = json.loads((shortlib.ROOT / 'shorts_plan.json').read_text('utf-8'))['shorts']
    if n < len(plan):
        nxt = plan[n]
        return (f'Bạn trả lời đúng chưa? Bình luận đáp án của bạn nhé! '
                f'Thử thách số {n + 1} tiếp theo: {nxt["title"]}. Theo dõi kênh để không bỏ lỡ!')
    return 'Bạn đã đi hết một trăm hai mươi thử thách. Bình luận câu bạn thích nhất nhé!'


class ShortScene(Scene):
    N = 1
    smoke = False

    # -------------------------------------------------------------- set-up
    def setup(self):
        self.code = f'xss{self.N:03d}'
        self.short = shortlib.load(self.code)
        self.entry = shortlib.plan_entry(self.N)
        self.paths = shortlib.paths(self.code)
        self.M = Formula(self.paths['formulas'])
        self.level = self.entry['level']
        self.lcolor = LEVEL_COLORS[self.level]
        self.board_items = []
        self.overruns = []
        self.fixed = []
        self.clock = 0.0
        self.board_top = BOARD_TOP  # a Short with a tall stage may start its board lower

    def rt(self, frac, minimum=None):
        lo = 1.5 / config.frame_rate if minimum is None else minimum
        return max(lo, frac * self.T)

    def now(self):
        return self.renderer.time

    def wait_until(self, frac, start):
        target = start + frac * self.T
        if target - self.renderer.time > 1 / config.frame_rate:
            self.wait(target - self.renderer.time)

    # -------------------------------------------------------------- typeset math inside text
    def TM(self, s, size=30, color=WHITE, bold=False, max_w=None):
        """``'chữ $toán$'``: text in the series font, every ``$…$`` typeset by Typst."""
        from manim import SVGMobject
        from common.typst_build import compile_inline
        parts = s.split('$')
        for i in range(1, len(parts) - 1, 2):
            if parts[i + 1][:1] in (',', '.', ';', '?') and parts[i + 1][:1]:
                parts[i] += parts[i + 1][0]
                parts[i + 1] = parts[i + 1][1:]
        group, raw = VGroup(), []
        k = size / 24 * 1.12
        for i, part in enumerate(parts):
            if not part.strip():
                continue
            raw.append(part)
            if i % 2 == 0:
                group.add(tx(part.strip(), size, color, bold=bold))
            else:
                svg = compile_inline(part, color, self.paths['typst_src'], self.paths['formulas'])
                m = SVGMobject(str(svg), height=None, width=None).scale(MATH_SCALE * k)
                for sub in m.family_members_with_points():
                    if sub.get_fill_opacity() < .01 and sub.get_stroke_width() > 0:
                        sub.set_stroke(width=BAR_WIDTH * k)
                    else:
                        sub.set_stroke(width=0)
                group.add(m)
        group.arrange(RIGHT, buff=.14)
        for j in range(1, len(group)):
            if raw[j].lstrip()[:1] in '.,:;)?' or raw[j - 1].rstrip()[-1:] == '(':
                group[j:].shift(LEFT * .1)
        if max_w is not None and group.width > max_w:
            group.scale_to_fit_width(max_w)
        return group

    def _glyph(self, ch, color, k):
        cache = self.__dict__.setdefault('_glyphs', {})
        key = (ch, color)
        if key not in cache:
            from manim import SVGMobject
            from common.typst_build import compile_inline
            expr = {'-': '-', '−': '-', ',': '","', '%': '%'}.get(ch, ch)
            svg = compile_inline(expr, color, self.paths['typst_src'], self.paths['formulas'])
            m = SVGMobject(str(svg), height=None, width=None).scale(MATH_SCALE)
            m.set_stroke(width=0)
            cache[key] = m
        return cache[key].copy().scale(k)

    def MNum(self, value, nd=2, color=WHITE, size=30):
        """Number in the math font with the Vietnamese decimal comma (cheap enough for always_redraw)."""
        from common.kit import vn
        k = size / 24 * 1.12
        text = vn(value, nd)
        g = VGroup(*[self._glyph(ch, color, k) for ch in text])
        g.arrange(RIGHT, buff=.02 * k, aligned_edge=DOWN)
        digits = [m for ch, m in zip(text, g) if ch.isdigit()]
        if digits:
            base, hgt = digits[0].get_bottom()[1], digits[0].height
            for ch, m in zip(text, g):
                if ch == ',':
                    m.move_to([m.get_x(), base - .12 * hgt + m.height / 2 - .25 * m.height, 0])
        return g

    # -------------------------------------------------------------- props in motion
    def flip(self, c, faces, run_time):
        """Coin flips through ``faces`` ('NSN…'), ending on the last one; returns the final coin."""
        from common.visuals import coin
        r = c[0].width / 2
        per = run_time / max(1, len(faces))
        for f in faces:
            self.play(c.animate.stretch(.04, 1), run_time=per / 2)
            new = coin(f, r).move_to(c.get_center())
            new.stretch(.04, 1)
            self.remove(c)
            self.add(new)
            self.play(new.animate.stretch(25, 1), run_time=per / 2)
            c = new
        return c

    def roll(self, d, faces, run_time):
        """Die tumbles through ``faces`` and lands on the last one; returns the final die."""
        from common.visuals import die
        s = d[0].width
        per = run_time / max(1, len(faces))
        for i, f in enumerate(faces):
            new = die(f, s).move_to(d.get_center()).rotate((-1) ** i * .35 if i < len(faces) - 1 else 0)
            self.play(FadeOut(d, run_time=per), FadeIn(new, run_time=per))
            d = new
        return d

    def run_sim(self, freqs, label_n, label_f, frac, y=-1.6, color=GREEN):
        """Live counter of a seeded simulation: number of trials and running frequency."""
        from manim import ValueTracker, always_redraw, smooth
        n = ValueTracker(1)
        read = always_redraw(lambda: VGroup(
            VGroup(tx(label_n, 30, SOFT), self.MNum(int(n.get_value()), 0, WHITE, 34)).arrange(RIGHT, buff=.2),
            VGroup(tx(label_f, 30, SOFT), self.MNum(freqs[int(n.get_value()) - 1], 3, color, 34)).arrange(RIGHT, buff=.2))
            .arrange(DOWN, aligned_edge=RIGHT, buff=.22).move_to([BOARD_X, y, 0]))
        self.add(read)
        self.play(n.animate.set_value(len(freqs)), run_time=self.rt(frac), rate_func=smooth)
        read.clear_updaters()
        self.board_items.append(read)
        return read

    def lines(self, rows, size=30, color=WHITE, bold=False, buff=.2, max_w=7.2):
        g = VGroup(*[self.TM(r, size, color, bold) for r in rows]).arrange(DOWN, buff=buff)
        if g.width > max_w:
            g.scale_to_fit_width(max_w)
        return g

    # -------------------------------------------------------------- chrome
    def build_chrome(self, plan):
        top = VGroup(tx(SERIES, 22, CYAN, bold=True), tx(AUTHOR, 17, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=.08)
        top.move_to([0, 6.62, 0]).to_edge(LEFT, buff=.35)
        lvl = VGroup(badge(LEVEL_NAMES[self.level], self.lcolor, 20),
                     tx(f'#{self.N:03d}', 26, WHITE, bold=True)).arrange(RIGHT, buff=.2)
        lvl.move_to([0, 6.62, 0]).to_edge(RIGHT, buff=.35)
        rule = Line([-FRAME_W / 2 + .3, 6.12, 0], [FRAME_W / 2 - .3, 6.12, 0], color=STROKE, stroke_width=2)
        total = plan['total_duration']
        bar = Rectangle(width=.01, height=.07, fill_color=self.lcolor, fill_opacity=1, stroke_width=0)
        bar.move_to([-FRAME_W / 2 + .3, 6.12, 0], aligned_edge=LEFT)
        self.caption = VGroup()
        self.cues = self.caption_cues(plan)
        self.cue_index = -1

        def tick(m, dt):
            self.clock += dt
            w = max(.01, (FRAME_W - .6) * min(1.0, self.clock / max(total, .1)))
            m.stretch_to_fit_width(w).move_to([-FRAME_W / 2 + .3, 6.12, 0], aligned_edge=LEFT)
            self.update_caption()

        bar.add_updater(tick)
        self.add(top, lvl, rule, bar, self.caption)
        self.chrome = [top, lvl, rule, bar, self.caption]

    # -------------------------------------------------------------- burnt-in captions
    def caption_cues(self, plan):
        from common.voice import _chunks
        cues, t0 = [], 0.0
        for b in plan['beats']:
            for s in b['sentences']:
                pieces = _chunks(s['text'], 50)
                total = sum(len(p) for p in pieces) or 1
                a, span = s['start'], max(s['end'] - s['start'], .8)
                for p in pieces:
                    d = span * len(p) / total
                    cues.append((t0 + a, t0 + a + d + .25, p))
                    a += d
            t0 += b['duration']
        return cues

    def update_caption(self):
        idx = -1
        for i, (a, b, _) in enumerate(self.cues):
            if a <= self.clock < b:
                idx = i
                break
        if idx == self.cue_index:
            return
        self.cue_index = idx
        if idx < 0 or self.smoke:
            self.caption.become(VGroup())
            return
        from common.kit import para
        txt = para(self.cues[idx][2], 31, WHITE, width=30, buff=.1, max_w=6.9)
        back = RoundedRectangle(width=txt.width + .4, height=txt.height + .26, corner_radius=.12, fill_color=INK,
                                fill_opacity=.82, stroke_width=0)
        self.caption.become(VGroup(back, txt.move_to(back)).move_to([BOARD_X, CAPTION_Y, 0]))

    # -------------------------------------------------------------- zones
    def stage(self):
        keep = set(self.chrome) | set(self.fixed)
        return [m for m in self.mobjects if m not in keep]

    def clear_stage(self, frac=.04):
        items = self.stage()
        self.board_items = []
        if items:
            self.play(*[FadeOut(m) for m in items], run_time=self.rt(frac))

    def write_board(self, *mobs, frac=.08, gap=.28, anim='write'):
        for m in mobs:
            if m.width > BOARD_W:
                m.scale_to_fit_width(BOARD_W)
            if self.board_items:
                m.next_to(self.board_items[-1], DOWN, buff=gap)
                m.set_x(BOARD_X)
            else:
                m.move_to([BOARD_X, self.board_top, 0], aligned_edge=UP)
            self.board_items.append(m)
        allb = VGroup(*self.board_items)
        if allb.get_bottom()[1] < BOARD_BOTTOM:  # keep clear of the captions
            allb.scale((self.board_top - BOARD_BOTTOM) / allb.height).move_to([BOARD_X, self.board_top, 0], aligned_edge=UP)
        self.play(*[(Write(m) if anim == 'write' else FadeIn(m, shift=UP * .1)) for m in mobs],
                  run_time=self.rt(frac))

    def clear_board(self, frac=.04):
        if self.board_items:
            self.play(*[FadeOut(m) for m in self.board_items], run_time=self.rt(frac))
        self.board_items = []

    def box(self, mob, color=GOLD):
        return SurroundingRectangle(mob, color=color, buff=.16, corner_radius=.1, stroke_width=4)

    def frame(self, mob, color=GOLD, frac=.05):
        """Box a board line; the box is cleared together with the board."""
        b = self.box(mob, color)
        self.play(Create(b), run_time=self.rt(frac))
        self.board_items.append(b)
        return b

    # -------------------------------------------------------------- standard beats
    def header(self):
        title = tx(self.entry['title'], 52, GOLD, bold=True, max_w=7.4).move_to([0, TITLE_Y, 0])
        prob = self.lines(self.short.PROBLEM, 34).next_to(title, DOWN, buff=.3)
        return title, prob

    def beat_hook(self, T):
        t0 = self.now()
        title, prob = self.header()
        self.play(FadeIn(title, shift=DOWN * .2), run_time=self.rt(.08))
        self.play(FadeIn(prob, shift=UP * .1), run_time=self.rt(.1))
        self.fixed += [title, prob]
        self.hook_visual(t0)

    def hook_visual(self, t0):
        """Override: put the props of the problem on the stage."""

    def options(self):
        opts = VGroup()
        for letter, key in zip('ABCD', [f'opt{i}' for i in range(len(self.short.OPTIONS))]):
            c = card(2.1, 1.3, STROKE, PANEL, radius=.18, stroke_width=3)
            m = self.M(key, 1.75, max_w=1.35)
            row = VGroup(tx(letter, 36, GOLD, bold=True), m).arrange(RIGHT, buff=.18)
            opts.add(VGroup(c, row.move_to(c)))
        opts.arrange(RIGHT, buff=.22)
        if opts.width > BOARD_W:
            opts.scale_to_fit_width(BOARD_W)
        return opts.move_to([BOARD_X, -2.0, 0])

    def countdown(self, t0, start, end, pos=(2.75, 3.15)):
        """3 – 2 – 1 ring while the viewer thinks."""
        from manim import ValueTracker, always_redraw, linear
        k = ValueTracker(0)
        p = [pos[0], pos[1], 0]
        bg = Circle(radius=.5, color=STROKE, stroke_width=8).move_to(p)
        ring = always_redraw(lambda: Arc(radius=.5, start_angle=PI / 2, angle=-TAU * max(1e-3, 1 - k.get_value()),
                                         arc_center=p, color=GOLD if k.get_value() < .67 else CORAL, stroke_width=8))
        digits = [self.TM(f'${d}$', 44, WHITE, bold=True).move_to(p) for d in (3, 2, 1)]
        self.wait_until(start, t0)
        self.play(FadeIn(bg), FadeIn(ring), FadeIn(digits[0]), run_time=self.rt(.03))
        seg = (end - start) / 3
        for i in range(3):
            self.play(k.animate.set_value((i + 1) / 3), run_time=self.rt(max(.04, seg - .02)), rate_func=linear)
            if i < 2:
                self.remove(digits[i])
                self.add(digits[i + 1])
        ring.clear_updaters()
        self.play(FadeOut(VGroup(bg, ring, digits[2])), run_time=self.rt(.02))

    def beat_guess(self, T):
        t0 = self.now()
        self.guess_opts = self.options()
        self.play(FadeIn(self.guess_opts, shift=UP * .15, lag_ratio=.25), run_time=self.rt(.12))
        self.countdown(t0, .3, .95)

    def beat_answer(self, T):
        t0 = self.now()
        if getattr(self, 'guess_opts', None) is not None and self.guess_opts in self.mobjects:
            self.remove(self.guess_opts)
        self.clear_board(.03)
        stage = [m for m in self.stage() if m not in self.board_items]
        if any(m.get_bottom()[1] < -.95 for m in stage):  # the stage reaches the answer zone: clear it
            self.play(*[FadeOut(m) for m in stage], run_time=self.rt(.04))
        ans = VGroup(badge('ĐÁP ÁN', GREEN, 28), self.M('answer', 2.0, max_w=4.4)).arrange(RIGHT, buff=.4)
        ans.move_to([BOARD_X, -1.75, 0])
        frame = self.box(ans, GREEN)
        self.play(FadeIn(ans, scale=1.15), Create(frame), run_time=self.rt(.12))
        self.board_items = [ans, frame]
        self.wait_until(.3, t0)
        if getattr(self.short, 'ANSWER_VALUE', None) is not None:
            m = self.meter(self.short.ANSWER_VALUE)
            self.play(FadeIn(m[0]), run_time=self.rt(.06))
            self.play(FadeIn(m[1], shift=DOWN * .2), run_time=self.rt(.08))
            self.board_items.append(m)

    def meter(self, value, y=-3.0, width=6.0):
        """Probability scale 0 (không thể) – 1 (chắc chắn) with a marker at ``value``."""
        x0 = BOARD_X - width / 2
        base = RoundedRectangle(width=width, height=.2, corner_radius=.1, fill_color=STROKE, fill_opacity=1,
                                stroke_width=0).move_to([BOARD_X, y, 0])
        fill = RoundedRectangle(width=max(.2, width * value), height=.2, corner_radius=.1, fill_color=self.lcolor,
                                fill_opacity=1, stroke_width=0).move_to([x0, y, 0], aligned_edge=LEFT)
        ticks = VGroup()
        for v, lab, word in ((0, '0', 'không thể'), (.5, '"0,5"', ''), (1, '1', 'chắc chắn')):
            x = x0 + width * v
            ticks.add(Line([x, y - .16, 0], [x, y + .16, 0], color=SOFT, stroke_width=3))
            t = self.TM(f'${lab}$', 22, SOFT).next_to([x, y - .18, 0], DOWN, buff=.06)
            ticks.add(t)
            if word:
                ticks.add(tx(word, 17, DIM).next_to(t, DOWN, buff=.03))
        mark = Triangle(fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(.13).rotate(PI)
        mark.move_to([x0 + width * value, y + .3, 0])
        return VGroup(VGroup(base, ticks), VGroup(fill, mark))

    def beat_outro(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.remove(*self.fixed)
        self.fixed = []
        q = tx('Bạn trả lời đúng chưa?', 46, GOLD, bold=True).move_to([0, 4.6, 0])
        cmt = tx('Bình luận đáp án của bạn!', 32, WHITE).next_to(q, DOWN, buff=.3)
        self.play(FadeIn(q, scale=1.1), FadeIn(cmt), run_time=self.rt(.1))
        plan = json.loads((shortlib.ROOT / 'shorts_plan.json').read_text('utf-8'))['shorts']
        self.wait_until(.3, t0)
        if self.N < len(plan):
            nxt = plan[self.N]
            box = card(6.8, 2.6, LEVEL_COLORS[nxt['level']], PANEL, radius=.25, stroke_width=4).move_to([0, 1.4, 0])
            tag = badge(f"THỬ THÁCH #{nxt['n']:03d} · {LEVEL_NAMES[nxt['level']]}", LEVEL_COLORS[nxt['level']], 22) \
                .move_to(box.get_top() + DOWN * .45)
            name = tx(nxt['title'], 40, WHITE, bold=True, max_w=6.2).move_to(box.get_center() + DOWN * .25)
            self.play(FadeIn(box), FadeIn(tag, shift=DOWN * .1), Write(name), run_time=self.rt(.14))
        self.wait_until(.6, t0)
        follow = VGroup(badge('THEO DÕI', CORAL, 26), tx('để không bỏ lỡ 120 thử thách', 26, SOFT)) \
            .arrange(DOWN, buff=.2).move_to([0, -1.4, 0])
        self.play(FadeIn(follow, shift=UP * .15), run_time=self.rt(.08))

    # -------------------------------------------------------------- main loop
    def construct(self):
        plan_path = self.paths['plan']
        if not plan_path.exists():
            raise FileNotFoundError('Run scripts/prepare_voice.py first')
        plan = json.loads(plan_path.read_text(encoding='utf-8'))
        ids = [b.id for b in self.short.BEATS]
        if [b['id'] for b in plan['beats']] != ids:
            raise RuntimeError('plan is stale: re-run scripts/prepare_voice.py')
        if plan['voice'] == 'on' and not self.smoke and not all(b['audio'] for b in plan['beats']):
            raise RuntimeError('voice=on selected but narration missing')
        self.build_chrome(plan)
        starts = []
        root = shortlib.ROOT
        for entry in plan['beats']:
            self.T = 1.0 if self.smoke else float(entry['duration'])
            start = self.renderer.time
            starts.append(round(start, 3))
            if entry['audio'] and not self.smoke:
                audio = root / entry['audio']
                if not audio.is_file() or audio.stat().st_size < 1000:
                    raise RuntimeError(f'Missing narration: {audio}')
                self.add_sound(str(audio), time_offset=plan.get('lead', 0.0))
            opts = getattr(self, 'guess_opts', None)
            if entry['id'] not in ('hook', 'guess', 'answer') and opts is not None and opts in self.mobjects:
                self.play(FadeOut(opts), run_time=self.rt(.03))
            getattr(self, f"beat_{entry['id']}")(self.T)
            spent = self.renderer.time - start
            if spent > self.T + 0.04:
                self.overruns.append((entry['id'], round(spent - self.T, 2)))
            elif self.T - spent > 1 / config.frame_rate:
                self.wait(self.T - spent)
        if self.overruns:
            print('BEAT_OVERRUNS', self.overruns)
        if not self.smoke:
            self.paths['timeline'].parent.mkdir(parents=True, exist_ok=True)
            self.paths['timeline'].write_text(json.dumps({
                'short': self.code.upper(), 'voice': plan['voice'], 'fps': config.frame_rate, 'starts': starts,
                'total': round(self.renderer.time, 3), 'overruns': self.overruns,
            }, ensure_ascii=False, indent=2), encoding='utf-8')


class DiceGridMixin:
    """Helpers for Shorts built on the 6 × 6 table of two dice."""

    def show_grid(self, frac=.35, sums=False, center=(.1, 1.0)):
        from common.visuals import dice_grid
        self.board_top = -1.65
        self.g = dice_grid(.66, .5).move_to([center[0], center[1], 0])
        self.play(FadeIn(self.g, lag_ratio=.01), run_time=self.rt(frac))
        if sums:
            self.sum_labels = VGroup(*[self.MNum(i + j + 2, 0, SOFT, 22).move_to(self.g.cells[j][i])
                                       for i in range(6) for j in range(6)])
            self.play(FadeIn(self.sum_labels, lag_ratio=.01), run_time=self.rt(.15))
        return self.g

    def light(self, cells, color=GOLD, frac=.04, opacity=.55):
        for c in cells:
            self.play(c.animate.set_fill(color, opacity), run_time=self.rt(frac))
