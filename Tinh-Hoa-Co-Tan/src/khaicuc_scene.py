"""Cảnh Manim cho một CHƯƠNG của tập khai cục (video dài chia chương, render song song trên Actions).

Dùng lại Board / Panel / MoveList của src/scene.py. Kịch bản: khaicuc/episodes/kc-XXXX.json.
Biến môi trường: KC_EPISODE (json), KC_CHAPTER (chỉ số), KC_OUTPUT (thư mục có voice_<i>/timing.json, cards/).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from manim import *  # noqa: F401,F403

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.layout import HEADER_LINE_Y  # noqa: E402
from src.scene import (BG, CYAN, FONT, GOLD, GREEN, LIGHT, MUTED, ORANGE, PANEL_W, PANEL_X, RED, Board,  # noqa: E402
                       MoveList, Panel, XiangqiLesson, label, pages)
from xq.notation import vn_move  # noqa: E402


class KMoveList(MoveList):
    """Biên bản nước đi bắt đầu từ số hiệp và bên đi bất kỳ (đoạn biến phụ)."""

    def __init__(self, start_no, side):
        super().__init__()
        self.rows = []
        self.start_no = start_no
        self.first = True
        self.side = side

    def push(self, vn, side):
        if self.first:
            self.first = False
            self.rows.append([self.start_no, vn, ''] if side == 'w' else [self.start_no, '…', vn])
            return
        super().push(vn, side)


class KhaiCucChapter(XiangqiLesson):
    def construct(self):
        data = json.loads(Path(os.environ['KC_EPISODE']).read_text(encoding='utf-8'))
        ci = int(os.environ['KC_CHAPTER'])
        out = Path(os.environ['KC_OUTPUT'])
        chapter = data['chapters'][ci]
        timing = json.loads((out / f'voice_{ci}' / 'timing.json').read_text(encoding='utf-8'))
        first_fen = next(b['fen'] for b in chapter['beats'] if b.get('fen'))
        board = Board(first_fen)
        self.chrome(data, ci)
        self.add(board)
        panel = Panel(self)
        if ci == 0:
            self.title_card(out / 'cards' / 'intro.png', 4.0)
        if len(timing) != len(chapter['beats']):
            raise ValueError('Số đoạn âm thanh khác số phân đoạn kịch bản')
        badges = []
        for beat, clips in zip(chapter['beats'], timing):
            for b in badges:
                self.remove(b)
            badges = []
            kind = beat['kind']
            if beat.get('fen'):
                board.reset(self, beat['fen'])
            panel.set_header(beat['label'], beat['headline'], ORANGE if kind == 'line' and 'PHỤ' in beat['label'] else GREEN)
            movelist = None
            if kind in ('hook', 'theory'):
                panel.set_body(Panel.bullets(beat['panel']['bullets']))
            elif kind == 'mnemonic':
                rows = VGroup(*[label(t, 25, GOLD, bold=True, wrap=34, lines=2) for t in beat['panel']['bullets']])
                rows.arrange(DOWN, aligned_edge=LEFT, buff=.32)
                panel.set_body(rows)
            elif kind == 'line':
                movelist = KMoveList(beat['start_no'], beat['start_side'])
                panel.set_body(VGroup())
            for step, clip in zip(beat['steps'], clips):
                start = self.time
                cap_pages = pages(step['say'])
                total_chars = sum(len(x) for x in cap_pages)
                panel.set_caption(cap_pages[0])
                self.add_sound(clip['audio'])
                if step.get('status'):
                    panel.set_status(step['status'], GREEN)
                if step.get('move'):
                    for b in badges:
                        self.remove(b)
                    badges = []
                    vn = vn_move(board.state, step['move'])
                    side = board.state.turn
                    badge = board.move(self, step['move'], color=CYAN)
                    if badge:
                        badges.append(badge)
                    if movelist is not None:
                        movelist.push(vn, side)
                        panel.set_body(movelist.render(7))
                elapsed = len(cap_pages[0])
                for page in cap_pages[1:]:
                    at = clip['seconds'] * elapsed / total_chars
                    if at > self.time - start:
                        self.wait(at - (self.time - start))
                    panel.set_caption(page)
                    elapsed += len(page)
                self.wait(max(.15, clip['seconds'] + .3 - (self.time - start)))
                if step.get('countdown'):
                    self.countdown(step['countdown'])
        if ci == len(data['chapters']) - 1:
            self.title_card(out / 'cards' / 'outro.png', 7.0)

    def chrome(self, data, ci=0):
        brand = Text('TINH HOA CỜ TÀN', font=FONT, font_size=26, color=GOLD, weight=BOLD)
        brand.move_to([-6.34, 3.57, 0], aligned_edge=LEFT)
        series = label(f'KHAI CỤC • {data["title"].split(":")[0].upper()} • CHƯƠNG {ci + 1}/{len(data["chapters"])}',
                       15, MUTED, max_w=8)
        series.move_to([6.27, 3.57, 0], aligned_edge=RIGHT)
        hline = Line([-6.35, HEADER_LINE_Y, 0], [6.34, HEADER_LINE_Y, 0], color='#35465D', stroke_width=1.3)
        foot_bg = Rectangle(width=14.22, height=.40, fill_color='#09101C', fill_opacity=.96, stroke_width=0).to_edge(DOWN, buff=0)
        foot = Text('☕ Ủng hộ kênh ly cà phê — VPBank: 10389821115 (Quét VietQR cuối video)  •  Điểm đánh giá: Pikafish',
                    font=FONT, font_size=12, color=MUTED).move_to(foot_bg)
        if foot.width > 13.6:
            foot.scale_to_fit_width(13.6)
        self.add(brand, series, hline, foot_bg, foot)
