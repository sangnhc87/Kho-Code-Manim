"""Cảnh Manim cho một tập Tinh Hoa Cờ Tàn (định dạng episodes/ep-XXXX.json).

Đọc kịch bản, thời lượng từng câu thoại (voice/timing.json) và thẻ Typst
từ biến môi trường. Đỏ ở phía dưới, toạ độ trùng với chessdb (a0 = góc dưới trái).
Mỗi bước (step) = một câu thoại + tối đa một nước đi, nên nước đi luôn khớp lời.
"""
from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from pathlib import Path

from manim import *  # noqa: F401,F403

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.layout import BOARD_CENTER_X, BOARD_CENTER_Y, BOARD_GRID_STEP, HEADER_LINE_Y, assert_safe_layout  # noqa: E402
from xq.board import Position, parse_sq, side_of  # noqa: E402

BG = '#0B1320'
PANEL = '#15243A'
GOLD = '#F5BF70'
RED = '#C94346'
INK = '#2F2721'
LIGHT = '#F4EFE1'
MUTED = '#9FB3C8'
GREEN = '#54CEA9'
CYAN = '#6ED6EF'
ORANGE = '#F29D52'
LINE = '#8A6540'
config.background_color = BG
FONT = 'Noto Sans'
CJK = 'Noto Sans CJK SC'
GLYPH = {'K': '帥', 'A': '仕', 'B': '相', 'N': '傌', 'R': '俥', 'C': '炮', 'P': '兵',
         'k': '將', 'a': '士', 'b': '象', 'n': '馬', 'r': '車', 'c': '砲', 'p': '卒'}
PANEL_X = 3.21
PANEL_W = 6.02
TEXT_W = 5.55


def label(value, size, color=LIGHT, bold=False, wrap=None, lines=3, max_w=TEXT_W, max_h=None):
    text = str(value)
    if wrap:
        parts = textwrap.wrap(text, width=wrap, break_long_words=False)
        if len(parts) > lines:
            parts = parts[:lines]
            parts[-1] = parts[-1].rstrip(' .,') + '…'
        text = '\n'.join(parts)
    obj = Text(text, font=FONT, font_size=size, color=color, weight=BOLD if bold else NORMAL,
               line_spacing=1.15)
    if obj.width > max_w:
        obj.scale_to_fit_width(max_w)
    if max_h and obj.height > max_h:
        obj.scale_to_fit_height(max_h)
    return obj


def pages(text, limit=135):
    """Chia lời bình thành các trang phụ đề theo câu, mỗi trang tối đa ~3 dòng."""
    sentences = []
    for sen in re.split(r'(?<=[.!?])\s+', text.strip()):
        while len(sen) > limit and ', ' in sen[:limit]:
            cut = sen[:limit].rindex(', ') + 1
            sentences.append(sen[:cut])
            sen = sen[cut:].strip()
        sentences.append(sen)
    out, cur = [], ''
    for sen in sentences:
        if cur and len(cur) + 1 + len(sen) > limit:
            out.append(cur)
            cur = sen
        else:
            cur = (cur + ' ' + sen).strip()
    if cur:
        out.append(cur)
    return out


class Board(VGroup):
    def __init__(self, fen, center=(BOARD_CENTER_X, BOARD_CENTER_Y), step=BOARD_GRID_STEP):
        super().__init__()
        assert_safe_layout()
        self.step = step
        self.ox, self.oy = center
        self.frame = None
        self.add(self.art())
        self.pieces = {}
        self.state = Position.from_fen(fen)
        for sq, p in self.state.cells.items():
            self._spawn(sq, p)

    def xy(self, sq):
        if isinstance(sq, str):
            sq = parse_sq(sq)
        x, y = sq
        return np.array([self.ox + (x - 4) * self.step, self.oy + (y - 4.5) * self.step, 0])

    def art(self):
        s = self.step
        g = VGroup()
        k = s / BOARD_GRID_STEP
        self.frame = RoundedRectangle(width=s * 8 + .57 * k, height=s * 9 + .52 * k, corner_radius=.16 * k,
                                      fill_color='#E4C89B', fill_opacity=1, stroke_width=4,
                                      stroke_color='#856344').move_to(self.xy((4, 4.5)))
        g.add(self.frame)
        kw = dict(stroke_color=LINE, stroke_width=1.65)
        for y in range(10):
            g.add(Line(self.xy((0, y)), self.xy((8, y)), **kw))
        for x in range(9):
            if x in (0, 8):
                g.add(Line(self.xy((x, 0)), self.xy((x, 9)), **kw))
            else:
                g.add(Line(self.xy((x, 0)), self.xy((x, 4)), **kw))
                g.add(Line(self.xy((x, 5)), self.xy((x, 9)), **kw))
        for base in (0, 7):
            g.add(Line(self.xy((3, base)), self.xy((5, base + 2)), **kw))
            g.add(Line(self.xy((5, base)), self.xy((3, base + 2)), **kw))
        g.add(Text('楚 河            漢 界', font=CJK, font_size=19 * k, color='#89623E').move_to(self.xy((4, 4.5))))
        # Số cột: Đỏ đếm 9..1 từ trái sang phải (phía dưới), Đen đếm 1..9 (phía trên).
        k = s / BOARD_GRID_STEP
        bottom = self.xy((4, 0))[1] - .26 * k - .225 * k
        top = self.xy((4, 9))[1] + .26 * k + .165 * k
        for x in range(9):
            g.add(Text(str(9 - x), font=FONT, font_size=13 * k, color=LIGHT).move_to(
                [self.xy((x, 0))[0], bottom, 0]))
            g.add(Text(str(x + 1), font=FONT, font_size=13 * k, color=MUTED).move_to(
                [self.xy((x, 9))[0], top, 0]))
        return g

    def make_piece(self, p):
        red = p.isupper()
        col = RED if red else INK
        k = self.step / BOARD_GRID_STEP
        return VGroup(Circle(radius=.235 * k, fill_color='#F5E4C3', fill_opacity=1, stroke_width=2.6, stroke_color=col),
                      Circle(radius=.205 * k, stroke_color=col, stroke_width=.75, stroke_opacity=.55),
                      Text(GLYPH[p], font=CJK, font_size=24 * k, weight=BOLD, color=col))

    def _spawn(self, sq, p):
        mob = self.make_piece(p).move_to(self.xy(sq))
        self.pieces[sq] = mob
        self.add(mob)
        return mob

    def reset(self, scene, fen):
        new = Position.from_fen(fen)
        if new.cells == self.state.cells:
            self.state = new
            return
        old = VGroup(*self.pieces.values())
        scene.play(FadeOut(old), run_time=.3)
        self.remove(*self.pieces.values())
        self.pieces = {}
        self.state = new
        fresh = VGroup(*[self._spawn(sq, p) for sq, p in new.cells.items()])
        scene.play(FadeIn(fresh), run_time=.35)

    def move(self, scene, uci, color=CYAN, tag=None):
        src, dst = parse_sq(uci[:2]), parse_sq(uci[2:])
        mob = self.pieces.pop(src)
        victim = self.pieces.pop(dst, None)
        k = self.step / BOARD_GRID_STEP
        ring = Circle(radius=.28 * k, color=GOLD, stroke_width=5).move_to(self.xy(src))
        arrow = Arrow(self.xy(src), self.xy(dst), buff=.26 * k, stroke_width=5, color=color,
                      max_tip_length_to_length_ratio=.2)
        scene.play(Create(ring), GrowArrow(arrow), run_time=.3)
        anims = [mob.animate.move_to(self.xy(dst))]
        if victim is not None:
            anims.append(FadeOut(victim, scale=.3))
        scene.play(*anims, run_time=.55, rate_func=smooth)
        if victim is not None:
            self.remove(victim)
        self.pieces[dst] = mob
        self.state = self.state.play(uci)
        extras = [FadeOut(arrow), FadeOut(ring)]
        badge = None
        if tag:
            badge = label(tag, 15, color=BG, bold=True)
            box = RoundedRectangle(width=badge.width + .22, height=.32, corner_radius=.08,
                                   fill_color=color, fill_opacity=1, stroke_width=0)
            badge = VGroup(box, badge.move_to(box)).next_to(mob, DOWN if dst[1] >= 8 else UP, buff=.06)
            scene.play(FadeIn(badge, shift=UP * .1), *extras, run_time=.25)
        else:
            scene.play(*extras, run_time=.2)
        if self.state.in_check(self.state.turn):
            k = self.state.king_sq(self.state.turn)
            flash = Circle(radius=.31 * self.step / BOARD_GRID_STEP, color=RED, stroke_width=6).move_to(self.xy(k))
            scene.play(Create(flash), run_time=.2)
            scene.play(FadeOut(flash), run_time=.25)
        return badge


class Panel:
    def __init__(self, scene):
        self.scene = scene
        bg = RoundedRectangle(width=PANEL_W, height=6.07, corner_radius=.2, stroke_width=1.4,
                              stroke_color='#35465D', fill_color=PANEL, fill_opacity=1).move_to([PANEL_X, -.10, 0])
        cap_bg = RoundedRectangle(width=PANEL_W - .3, height=1.36, corner_radius=.14, stroke_width=0,
                                  fill_color='#0F1B2D', fill_opacity=1).move_to([PANEL_X, -1.93, 0])
        self.tag = label(' ', 16, GREEN, bold=True).move_to([PANEL_X, 2.62, 0])
        self.head = label(' ', 26, GOLD, bold=True).move_to([PANEL_X, 2.13, 0])
        self.body = VGroup()
        self.caption = label(' ', 19).move_to(cap_bg)
        self.status = label(' ', 15, MUTED).move_to([PANEL_X, -2.86, 0])
        scene.add(bg, cap_bg, self.tag, self.head, self.caption, self.status)
        self.cap_bg = cap_bg

    def swap(self, attr, new, run_time=.35):
        old = getattr(self, attr)
        self.scene.play(FadeOut(old, run_time=run_time * .6), FadeIn(new, run_time=run_time))
        setattr(self, attr, new)

    def set_header(self, tag, head, tag_color=GREEN):
        new_tag = label(tag, 16, tag_color, bold=True, max_w=5.4).move_to([PANEL_X, 2.62, 0])
        new_head = label(head, 26, GOLD, bold=True, wrap=34, lines=2, max_h=.8).move_to([PANEL_X, 2.13, 0])
        self.scene.play(FadeOut(self.tag), FadeOut(self.head), FadeIn(new_tag), FadeIn(new_head), run_time=.4)
        self.tag, self.head = new_tag, new_head

    def set_caption(self, text):
        new = label(text, 19, LIGHT, wrap=48, lines=4, max_w=PANEL_W - .55, max_h=1.2).move_to(self.cap_bg)
        self.scene.remove(self.caption)
        self.scene.add(new)
        self.caption = new

    def set_status(self, text, color=MUTED):
        new = label(text, 15, color, max_w=5.6).move_to([PANEL_X, -2.86, 0])
        self.scene.remove(self.status)
        self.scene.add(new)
        self.status = new

    def set_body(self, group):
        top = 1.72
        if len(group):
            group.move_to([PANEL_X, 0, 0]).align_to([0, top, 0], UP)
            if group.height > 2.85:
                group.scale_to_fit_height(2.85).align_to([0, top, 0], UP)
        self.swap('body', group)

    # ---- các kiểu nội dung ----
    @staticmethod
    def bullets(items):
        rows = VGroup(*[label('•  ' + t, 21, LIGHT, wrap=40, lines=2) for t in items])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=.2)
        return rows

    @staticmethod
    def candidates(rows):
        out = VGroup()
        for r in rows:
            color = GREEN if r.get('good', r['wdl'] == 'W') else (MUTED if r['wdl'] == 'D' else RED)
            left = label(('★ ' if r['best'] else '   ') + r['vn'], 20, GOLD if r['best'] else LIGHT, bold=r['best'],
                         max_w=2.6)
            right = label(r['result'], 18, color, max_w=2.75)
            line = VGroup(left, right)
            left.move_to([1.85, 0, 0], aligned_edge=LEFT).set_x(.45, direction=LEFT)
            right.set_x(6.0, direction=RIGHT)
            out.add(line)
        out.arrange(DOWN, buff=.17)
        for line in out:
            line[0].set_x(.45, direction=LEFT)
            line[1].set_x(6.0, direction=RIGHT)
        return out


class MoveList:
    """Biên bản nước đi kiểu sổ ghi: số hiệp | nước Đỏ | nước Đen."""

    def __init__(self):
        self.rows = []  # [số hiệp, nước Đỏ, nước Đen]

    def push(self, vn, side):
        if side == 'w' or not self.rows or self.rows[-1][2]:
            n = self.rows[-1][0] + 1 if self.rows else 1
            self.rows.append([n, vn, ''] if side == 'w' else [n, '…', vn])
        else:
            self.rows[-1][2] = vn

    def render(self, last=6):
        group = VGroup()
        shown = self.rows[-last:]
        for i, (n, r, b) in enumerate(shown):
            current = i == len(shown) - 1
            c_red = GOLD if current and not b else LIGHT
            c_blk = GOLD if current and b else LIGHT
            num = label(f'{n}.', 18, MUTED)
            red = label(r, 18, c_red, max_w=2.45)
            blk = label(b, 18, c_blk, max_w=2.45) if b else Dot(radius=.01, fill_opacity=0)
            num.set_x(.55, direction=LEFT)
            red.set_x(1.05, direction=LEFT)
            blk.set_x(3.65, direction=LEFT)
            row = VGroup(num, red, blk)
            group.add(row)
        group.arrange(DOWN, buff=.16, aligned_edge=LEFT)
        for row in group:
            row[0].set_x(.55, direction=LEFT)
            row[1].set_x(1.05, direction=LEFT)
            row[2].set_x(3.65, direction=LEFT)
        return group


class XiangqiLesson(Scene):
    def construct(self):
        data = json.loads(Path(os.environ['XIANGQI_EPISODE']).read_text(encoding='utf-8'))
        out = Path(os.environ['XIANGQI_OUTPUT'])
        timing = json.loads((out / 'voice' / 'timing.json').read_text(encoding='utf-8'))
        board = Board(data['fen'])
        self.chrome(data)
        self.add(board)
        panel = Panel(self)
        self.title_card(out / 'cards' / 'intro.png', 3.2)
        verdict = data['verdict']
        base_status = ('Bảng tra chessdb: Đỏ thắng' if verdict['wdl'] == 'W' else 'Bảng tra chessdb: Hòa')
        panel.set_status(base_status)
        movelist = MoveList()
        badges = []
        if len(timing) != len(data['beats']):
            raise ValueError('Số đoạn âm thanh khác số phân đoạn kịch bản')
        for beat, clips in zip(data['beats'], timing):
            for b in badges:
                self.remove(b)
            badges = []
            kind = beat['kind']
            if beat.get('fen') and kind != 'trap':
                board.reset(self, beat['fen'])
            if kind == 'trap':
                board.reset(self, beat['fen'])
                self.play(board.frame.animate.set_stroke(ORANGE, width=7), run_time=.3)
            panel.set_header(beat['label'], beat['headline'], ORANGE if kind == 'trap' else GREEN)
            p = beat.get('panel', {})
            if kind in ('intro', 'theory', 'summary'):
                panel.set_body(Panel.bullets(p['bullets']))
            elif kind == 'candidates':
                panel.set_body(Panel.candidates(p['rows']))
            elif kind == 'puzzle':
                panel.set_body(VGroup())
            elif kind == 'line':
                panel.set_body(movelist.render())
            elif kind == 'trap':
                panel.set_body(Panel.bullets([p['verdict']]))
                panel.set_status('BIẾN THAM KHẢO – không phải biến chính', ORANGE)
            elif kind == 'mate':
                panel.set_body(VGroup())
                self.mate_marks(board, p['mate'])
            trap_list = MoveList()
            for step, clip in zip(beat['steps'], clips):
                start = self.time
                cap_pages = pages(step['say'])
                total_chars = sum(len(x) for x in cap_pages)
                panel.set_caption(cap_pages[0])
                self.add_sound(clip['audio'])
                if step.get('move'):
                    for b in badges:
                        self.remove(b)
                    badges = []
                    mark = step.get('mark')
                    color = RED if mark == 'bad' else (GOLD if mark in ('only', 'hold') else CYAN)
                    tag = {'only': 'DUY NHẤT', 'wait': 'NƯỚC CHỜ', 'zug': 'BỊ ÉP NƯỚC', 'bad': 'SAI?',
                           'hold': 'GIỮ HÒA'}.get(mark)
                    vn = self.vn_of(board.state, step['move'])
                    side = board.state.turn
                    badge = board.move(self, step['move'], color=color, tag=tag)
                    if badge:
                        badges.append(badge)
                    if kind == 'line':
                        movelist.push(vn, side)
                        panel.set_body(movelist.render())
                        if step.get('remain') is not None:
                            left = (step['remain']) // 2
                            panel.set_status(f'{base_status} • còn {left} nước đến bí' if left else
                                             'Đen hết nước – Đỏ thắng', GREEN if not left else MUTED)
                    elif kind == 'trap':
                        trap_list.push(vn, side)
                        panel.set_body(trap_list.render(4))
                if kind == 'puzzle':
                    self.wait(max(.1, clip['seconds'] - (self.time - start)))
                    self.countdown(p.get('countdown', 5))
                    continue
                elapsed_chars = len(cap_pages[0])
                for page in cap_pages[1:]:
                    at = clip['seconds'] * elapsed_chars / total_chars
                    if at > self.time - start:
                        self.wait(at - (self.time - start))
                    panel.set_caption(page)
                    elapsed_chars += len(page)
                self.wait(max(.15, clip['seconds'] + .3 - (self.time - start)))
            if kind == 'mate':
                self.remove(*self.mate_group)
            if kind == 'trap':
                for b in badges:
                    self.remove(b)
                badges = []
                board.reset(self, beat['return_fen'])
                self.play(board.frame.animate.set_stroke('#856344', width=4), run_time=.3)
                panel.set_status(base_status)
        self.title_card(out / 'cards' / 'outro.png', 7.0)

    @staticmethod
    def vn_of(state, move):
        from xq.notation import vn_move
        return vn_move(state, move)

    def countdown(self, n):
        for i in range(n, 0, -1):
            num = Text(str(i), font=FONT, font_size=96, color=GOLD, weight=BOLD).move_to([PANEL_X, .35, 0])
            self.play(FadeIn(num, scale=1.3), run_time=.25)
            self.wait(.5)
            self.play(FadeOut(num), run_time=.25)

    def mate_marks(self, board, mate):
        group = VGroup()
        for e in mate['escapes']:
            c = board.xy(e['sq'])
            col = MUTED if 'blocked_by_own' in e else RED
            group.add(Cross(scale_factor=.16, stroke_color=col, stroke_width=6).move_to(c))
            for g in e.get('guards', []):
                gsq = g.split(':')[0]
                group.add(DashedLine(board.xy(gsq), c, color=ORANGE, stroke_width=3, dash_length=.08))
        for ch in mate['checkers']:
            group.add(Circle(radius=.3, color=RED, stroke_width=6).move_to(board.xy(ch.split(':')[0])))
        group.add(Circle(radius=.32, color=GOLD, stroke_width=6).move_to(board.xy(mate['king'])))
        self.play(Create(group), run_time=1.0)
        self.mate_group = [group]

    def chrome(self, data):
        brand = Text('TINH HOA CỜ TÀN', font=FONT, font_size=26, color=GOLD, weight=BOLD)
        brand.move_to([-6.34, 3.57, 0], aligned_edge=LEFT)
        series = label(f'TẬP {data["number"]}  •  {data["category"].upper()}', 15, MUTED, max_w=7)
        series.move_to([6.27, 3.57, 0], aligned_edge=RIGHT)
        hline = Line([-6.35, HEADER_LINE_Y, 0], [6.34, HEADER_LINE_Y, 0], color='#35465D', stroke_width=1.3)
        foot_bg = Rectangle(width=14.22, height=.40, fill_color='#09101C', fill_opacity=.96, stroke_width=0).to_edge(DOWN, buff=0)
        foot = Text('☕ Ủng hộ kênh ly cà phê — VPBank: 10389821115 (Quét VietQR cuối video)  •  Dữ liệu: bảng tra cờ tàn chessdb.cn',
                    font=FONT, font_size=12, color=MUTED).move_to(foot_bg)
        if foot.width > 13.6:
            foot.scale_to_fit_width(13.6)
        self.add(brand, series, hline, foot_bg, foot)

    def title_card(self, png, seconds):
        if not png.exists():
            return
        art = ImageMobject(str(png)).set_width(10.8).move_to(ORIGIN)
        scrim = Rectangle(width=14.5, height=8.3, fill_color=BG, fill_opacity=.96, stroke_width=0)
        self.play(FadeIn(scrim), FadeIn(art, scale=.95), run_time=.6)
        self.wait(seconds)
        self.play(FadeOut(art), FadeOut(scrim), run_time=.5)
