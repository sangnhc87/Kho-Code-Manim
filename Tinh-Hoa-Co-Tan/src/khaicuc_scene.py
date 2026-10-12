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


GAP_MOVE, GAP_TALK = 1.6, 2.0   # nghỉ sau mỗi câu cho người xem kịp nhìn (khớp build_khaicuc_episode)


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
        first_fen = next((b['fen'] for b in chapter['beats'] if b.get('fen')), data['fen'])
        board = Board(first_fen)
        self.chrome(data, ci)
        self.add(board)
        panel = Panel(self)
        if ci == 0:
            self.title_card(out / 'cards' / 'intro.png', 4.0)
        if len(timing) != len(chapter['beats']):
            raise ValueError('Số đoạn âm thanh khác số phân đoạn kịch bản')
        badges = []
        movelist = None
        for beat, clips in zip(chapter['beats'], timing):
            for b in badges:
                self.remove(b)
            badges = []
            kind = beat['kind']
            if kind == 'cta':
                self.play_cta(out, beat, clips)
                continue
            if beat.get('fen'):
                board.reset(self, beat['fen'])
            panel.set_header(beat['label'], beat['headline'], ORANGE if kind == 'line' and 'PHỤ' in beat['label'] else GREEN)
            if kind in ('hook', 'theory'):
                panel.set_body(Panel.bullets(beat['panel']['bullets']))
            elif kind == 'mnemonic':
                rows = VGroup(*[label(t, 25, GOLD, bold=True, wrap=34, lines=2) for t in beat['panel']['bullets']])
                rows.arrange(DOWN, aligned_edge=LEFT, buff=.32)
                panel.set_body(rows)
            elif kind == 'line':
                if beat.get('continue') and movelist is not None:
                    panel.set_body(movelist.render(7))
                else:
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
                if step.get('rows'):
                    panel.set_body(Panel.candidates(step['rows']))
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
                self.wait(GAP_MOVE if step.get('move') else GAP_TALK)
                if step.get('rows') and movelist is not None:
                    panel.set_body(movelist.render(7))
                if step.get('countdown'):
                    self.countdown(step['countdown'])
        if ci == len(data['chapters']) - 1 and chapter['beats'][-1]['kind'] != 'cta':
            self.title_card(out / 'cards' / 'outro.png', 7.0)

    def play_cta(self, out, beat, clips):
        """Thẻ cuối có mã QR hiện suốt lúc đọc lời kêu gọi đăng ký / ủng hộ."""
        png = out / 'cards' / 'outro.png'
        art = ImageMobject(str(png)).set_width(11.4).move_to(ORIGIN)
        scrim = Rectangle(width=14.5, height=8.3, fill_color=BG, fill_opacity=1, stroke_width=0)
        scrim.set_z_index(100)   # quân cờ (z=3) không được lộ lên trên thẻ
        art.set_z_index(101)
        self.play(FadeIn(scrim), FadeIn(art, scale=.97), run_time=.8)
        for step, clip in zip(beat['steps'], clips):
            self.add_sound(clip['audio'])
            self.wait(clip['seconds'] + .5)
        self.wait(5.0)
        self.play(FadeOut(art), FadeOut(scrim), run_time=.6)

    def chrome(self, data, ci=0):
        brand = Text('TINH HOA CỜ TÀN', font=FONT, font_size=26, color=GOLD, weight=BOLD)
        brand.move_to([-6.34, 3.57, 0], aligned_edge=LEFT)
        series = label(f'{data["title"].split(":")[0].upper()} • CHƯƠNG {ci + 1}/{len(data["chapters"])}',
                       15, MUTED, max_w=8)
        series.move_to([6.27, 3.57, 0], aligned_edge=RIGHT)
        hline = Line([-6.35, HEADER_LINE_Y, 0], [6.34, HEADER_LINE_Y, 0], color='#35465D', stroke_width=1.3)
        foot_bg = Rectangle(width=14.22, height=.40, fill_color='#09101C', fill_opacity=.96, stroke_width=0).to_edge(DOWN, buff=0)
        foot = Text('☕ Ủng hộ kênh ly cà phê — VPBank: 10389821115 (Quét VietQR cuối video)  •  Điểm đánh giá: Pikafish',
                    font=FONT, font_size=12, color=MUTED).move_to(foot_bg)
        if foot.width > 13.6:
            foot.scale_to_fit_width(13.6)
        self.add(brand, series, hline, foot_bg, foot)
