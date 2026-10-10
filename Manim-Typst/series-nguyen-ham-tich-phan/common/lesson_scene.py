"""Base scene of the INT series: fixed chrome + beat-synchronised narration.

Each narration beat ``<id>`` in ``lesson.BEATS`` is rendered by the method
``beat_<id>(T)`` of the subclass. ``T`` is the beat's exact duration (MP3
length + padding). Methods should spend at most ``T`` seconds (use
``self.rt(fraction)``); the base pads the rest, records real start times in
``artifacts/<ep>_timeline.json`` and reports overruns.
"""
from __future__ import annotations

import json

from manim import (DOWN, LEFT, RIGHT, UP, FadeOut, Line, Rectangle,
                   Scene, VGroup, config)

from common import episode
from common.blocks import Blocks
from common.kit import Formula, tx
from common.theme import (AUTHOR, BG, CYAN, DIM, FRAME_H, FRAME_W, GOLD, GREEN, SERIES, SOFT,
                          STROKE)

config.background_color = BG
config.frame_width = FRAME_W
config.frame_height = FRAME_H

# Stage geometry (scene units).
TOP = 3.08           # top of the teaching area
BOTTOM = -3.12       # bottom of the teaching area
LEFT_CX = -3.45      # centre of the left (graph) column
BOARD_X = 0.55       # left edge of the right (board) column
BOARD_W = 6.15


class LessonScene(Blocks, Scene):
    EP = 'int01'
    smoke = False

    # -------------------------------------------------------------- set-up
    def setup(self):
        self.lesson = episode.load(self.EP)
        self.paths = episode.paths(self.EP)
        self.M = Formula(self.paths['formulas'])
        self.chrome = VGroup()
        self.board_items = []
        self.overruns = []

    def rt(self, frac, minimum=None):
        """Run time as a fraction of the current beat (frame-safe)."""
        lo = 1.5 / config.frame_rate if minimum is None else minimum
        return max(lo, frac * self.T)

    # -------------------------------------------------------------- chrome
    def build_chrome(self, plan):
        ep = self.lesson.EPISODE
        top_line = Line([-FRAME_W / 2 + .3, 3.3, 0], [FRAME_W / 2 - .3, 3.3, 0], color=STROKE, stroke_width=1.4)
        series = tx(SERIES, 17, CYAN, bold=True).move_to([0, 3.62, 0]).to_edge(LEFT, buff=.42)
        code = tx(f"{ep['code']} · {ep['title']}", 17, SOFT).next_to(series, RIGHT, buff=.35)
        # Progress bar: one segment per part, width proportional to its real duration.
        parts = [p for p, _ in self.lesson.PARTS]
        durations = {p: 0.0 for p in parts}
        for b in plan['beats']:
            durations[b['part']] += b['duration']
        total = sum(durations.values())
        x0, x1, y = -FRAME_W / 2 + .42, FRAME_W / 2 - .42, -3.42
        gap = .06
        width = x1 - x0 - gap * (len(parts) - 1)
        self.part_bars, self.part_spans = {}, {}
        x, t = x0, 0.0
        bars = VGroup()
        for p in parts:
            w = width * durations[p] / total
            bg = Rectangle(width=w, height=.07, fill_color=STROKE, fill_opacity=1, stroke_width=0)
            bg.move_to([x + w / 2, y, 0])
            bars.add(bg)
            self.part_bars[p] = (x, w)
            self.part_spans[p] = (t, durations[p])
            x += w + gap
            t += durations[p]
        self.fill = VGroup()
        footer_l = tx(f"{ep['code']} · {ep['subtitle']}", 15, DIM).move_to([0, -3.76, 0]).to_edge(LEFT, buff=.42)
        footer_r = tx(AUTHOR, 16, SOFT, bold=True).move_to([0, -3.76, 0]).to_edge(RIGHT, buff=.42)
        self.part_label = VGroup()
        self.chrome.add(top_line, series, code, bars, footer_l, footer_r)
        self.add(self.chrome)
        self.current_part = None

    def update_chrome(self, part, now):
        names = dict(self.lesson.PARTS)
        if part != self.current_part:
            self.remove(self.part_label)
            idx = [p for p, _ in self.lesson.PARTS].index(part)
            label = tx(f'PHẦN {idx}  ·  {names[part].upper()}' if 0 < idx < len(names) - 1
                       else names[part].upper(), 17, GOLD, bold=True)
            self.part_label = label.move_to([0, 3.62, 0]).to_edge(RIGHT, buff=.42)
            self.add(self.part_label)
            self.current_part = part
        self.remove(self.fill)
        fills = VGroup()
        for p, _ in self.lesson.PARTS:
            x, w = self.part_bars[p]
            t0, d = self.part_spans[p]
            k = min(1.0, max(0.0, (now - t0) / d)) if d else 0
            if k > 0:
                color = GREEN if k >= 1 else CYAN
                fills.add(Rectangle(width=max(w * k, .01), height=.07, fill_color=color, fill_opacity=1,
                                    stroke_width=0).move_to([x + w * k / 2, -3.42, 0]))
        self.fill = fills
        self.add(self.fill)

    # -------------------------------------------------------------- stage helpers
    def stage(self):
        keep = set(self.chrome) | {self.chrome, self.fill, self.part_label}
        return [m for m in self.mobjects if m not in keep]

    def clear_stage(self, frac=0.05):
        items = self.stage()
        self.board_items = []
        if items:
            self.play(*[FadeOut(m) for m in items], run_time=self.rt(frac))

    def board(self, mob, gap=0.32, x=BOARD_X, top=TOP - .2, indent=0.0):
        """Place ``mob`` under the previous board item (left-aligned)."""
        if self.board_items:
            mob.next_to(self.board_items[-1], DOWN, buff=gap)
            mob.align_to([x + indent, 0, 0], LEFT)
        else:
            mob.move_to([0, top, 0], aligned_edge=UP).align_to([x + indent, 0, 0], LEFT)
        if mob.width > BOARD_W - indent:
            mob.scale_to_fit_width(BOARD_W - indent)
            mob.align_to([x + indent, 0, 0], LEFT)
        self.board_items.append(mob)
        return mob

    # -------------------------------------------------------------- main loop
    def construct(self):
        plan_path = self.paths['plan']
        if not plan_path.exists():
            raise FileNotFoundError('Run scripts/prepare_voice.py first')
        plan = json.loads(plan_path.read_text(encoding='utf-8'))
        ids = [b.id for b in self.lesson.BEATS]
        if [b['id'] for b in plan['beats']] != ids:
            raise RuntimeError('runtime_plan.json is stale: re-run scripts/prepare_voice.py')
        if plan['voice'] == 'on' and not self.smoke and not all(b['audio'] for b in plan['beats']):
            raise RuntimeError('voice=on selected but narration missing')
        self.build_chrome(plan)
        starts = []
        root = self.paths['pkg'].parent
        for entry in plan['beats']:
            self.T = 1.2 if self.smoke else float(entry['duration'])
            start = self.renderer.time
            starts.append(round(start, 3))
            self.update_chrome(entry['part'], start if not self.smoke else
                               sum(b['duration'] for b in plan['beats'][:len(starts) - 1]))
            if entry['audio'] and not self.smoke:
                audio = root / entry['audio']
                if not audio.is_file() or audio.stat().st_size < 1000:
                    raise RuntimeError(f'Missing narration: {audio}')
                self.add_sound(str(audio), time_offset=plan.get('lead', 0.0))
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
                'episode': self.lesson.EPISODE['code'], 'voice': plan['voice'],
                'fps': config.frame_rate, 'starts': starts,
                'total': round(self.renderer.time, 3), 'overruns': self.overruns,
            }, ensure_ascii=False, indent=2), encoding='utf-8')
