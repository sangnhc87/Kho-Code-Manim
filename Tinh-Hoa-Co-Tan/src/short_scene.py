"""YouTube Short dạng câu đố (khung dọc 1080x1920, dưới 60 giây).

Đọc output/<tập>/short.json (do scripts/make_short.py tạo) và voice/timing.json.
Bố cục: tiêu đề câu đố ở trên, bàn cờ lớn ở giữa, phụ đề ở dưới.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from manim import *  # noqa: F401,F403

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.scene import BG, CYAN, FONT, GOLD, GREEN, LIGHT, MUTED, RED, Board, label, pages  # noqa: E402

config.background_color = BG
config.frame_width = 4.5
config.frame_height = 8.0
W = 4.5  # khung dọc: rộng 4.5, cao 8 đơn vị Manim


class XiangqiShort(Scene):
    def flash(self, text, color, hold=1.0):
        """Chữ lớn giữa màn hình để giữ người xem ở giây đầu và lúc kết liễu."""
        lines = [t.strip() for t in text.split('•') if t.strip()]
        txt = VGroup(*[label(t, 40, LIGHT, bold=True, max_w=W - 1.1) for t in lines]).arrange(DOWN, buff=.18)
        box = RoundedRectangle(width=txt.width + .5, height=txt.height + .4, corner_radius=.15,
                               fill_color=color, fill_opacity=.92, stroke_color=GOLD, stroke_width=3)
        grp = VGroup(box, txt.move_to(box)).move_to([0, -.3, 0])
        self.play(FadeIn(grp, scale=1.6), run_time=.35)
        self.wait(hold)
        self.play(FadeOut(grp, scale=.8), run_time=.3)

    def construct(self):
        out = Path(os.environ['XIANGQI_OUTPUT'])
        data = json.loads((out / 'short.json').read_text(encoding='utf-8'))
        clips = json.loads((out / 'voice_short' / 'timing.json').read_text(encoding='utf-8'))[0]
        board = Board(data['fen'], center=(0, -.33), step=.44)
        brand = label('TINH HOA CỜ TÀN', 22, GOLD, bold=True, max_w=W - .4).move_to([0, 3.66, 0])
        title = label(data['headline'], 26, LIGHT, bold=True, wrap=30, lines=2, max_w=W - .3, max_h=.75).move_to([0, 3.08, 0])
        tag = label(data['tag'], 17, GREEN, bold=True, max_w=W - .4).move_to([0, 2.42, 0])
        cap_bg = RoundedRectangle(width=W - .2, height=.95, corner_radius=.12, stroke_width=0,
                                  fill_color='#0F1B2D', fill_opacity=1).move_to([0, -3.27, 0])
        foot = label(data.get('footer') or f'Lời giải đầy đủ: Tập {data["number"]} trên kênh', 14, MUTED,
                     max_w=W - .4).move_to([0, -3.9, 0])
        self.add(board, brand, title, tag, cap_bg, foot)
        if data.get('flash'):
            self.flash(data['flash'], RED, hold=1.1)
        caption = VGroup()
        badges = []
        for step, clip in zip(data['steps'], clips):
            start = self.time
            parts = pages(step['say'], limit=80)
            total = sum(len(x) for x in parts)
            self.remove(caption)
            caption = label(parts[0], 19, LIGHT, wrap=32, lines=3, max_w=W - .45, max_h=.82).move_to(cap_bg)
            self.add(caption)
            self.add_sound(clip['audio'])
            if step.get('move'):
                for b in badges:
                    self.remove(b)
                badges = []
                mark = step.get('mark')
                color = GOLD if mark in ('only', 'hold') else CYAN
                if step.get('tag'):
                    color = RED if 'THÍ' in step['tag'] else GOLD
                b = board.move(self, step['move'], color=color,
                               tag=step.get('tag') or {'only': 'DUY NHẤT', 'hold': 'GIỮ HÒA', 'answer': 'ĐÁP ÁN'}.get(mark))
                if b:
                    badges.append(b)
            done = len(parts[0])
            for part in parts[1:]:
                at = clip['seconds'] * done / total
                if at > self.time - start:
                    self.wait(at - (self.time - start))
                self.remove(caption)
                caption = label(part, 19, LIGHT, wrap=32, lines=3, max_w=W - .45, max_h=.82).move_to(cap_bg)
                self.add(caption)
                done += len(part)
            self.wait(max(.1, clip['seconds'] + .2 - (self.time - start)))
            if step.get('countdown'):
                for i in range(step['countdown'], 0, -1):
                    num = Text(str(i), font=FONT, font_size=110, color=GOLD, weight=BOLD).move_to([0, -.33, 0])
                    disk = Circle(radius=.75, fill_color=BG, fill_opacity=.85, stroke_color=GOLD).move_to(num)
                    self.play(FadeIn(disk), FadeIn(num, scale=1.3), run_time=.25)
                    self.wait(.5)
                    self.play(FadeOut(disk), FadeOut(num), run_time=.25)
        if board.state.is_mate():
            self.flash('CHIẾU BÍ!', RED, hold=.9)
        verdict = label(data['verdict'], 22, GREEN if data['wdl'] == 'W' else CYAN, bold=True,
                        wrap=26, lines=2, max_w=W - .3, max_h=.5).move_to([0, 2.42, 0])
        self.play(FadeOut(tag), FadeIn(verdict), run_time=.3)
        self.wait(1.2)
