"""COMB01 | QUY TẮC CỘNG | Sang Math Manim + Typst

Render command (after running scripts/build_formulas.py):
    manim -pql episodes/comb01_rule_of_sum.py COMB01
    manim -qh episodes/comb01_rule_of_sum.py COMB01

Typst raster assets are generated once and loaded as ImageMobject.
If assets are absent, placeholder Text appears for drafting only.
This scene is voiceover-ready; final running time depends on pacing and dubbing.
"""
from __future__ import annotations
from pathlib import Path
import os
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from series_config import PALETTE as P

config.background_color = P['bg']
config.frame_width = 14.222222
config.frame_height = 8.0

FONT = 'Noto Sans'
LEFT = -3.81
RIGHT = 3.18
PANEL_Y = -0.30
LEFT_W = 6.13
RIGHT_W = 7.31
PANEL_H = 6.32


def vtext(s, size=28, color=None, bold=False, max_w=None):
    """Font-safe Vietnamese text with max width protection."""
    t = Text(s, font=FONT, font_size=size, color=color or P['text'],
             weight='BOLD' if bold else 'NORMAL', line_spacing=0.85)
    if max_w and t.width > max_w:
        t.scale_to_fit_width(max_w)
    return t


def tag(s, color, width=None, font_size=19):
    t = vtext(s, font_size, P['text'], max_w=width - 0.25 if width else None)
    w = width if width else t.width + 0.42
    b = RoundedRectangle(width=w, height=0.50, corner_radius=0.13,
                         fill_color=color, fill_opacity=0.18,
                         stroke_color=color, stroke_width=1.4)
    t.move_to(b)
    return VGroup(b, t)


def card_box(w, h, fill=None, stroke=None):
    return RoundedRectangle(width=w, height=h, corner_radius=0.16,
                            fill_color=fill or P['panel_alt'],
                            fill_opacity=1, stroke_color=stroke or P['line'],
                            stroke_width=1.1)


def formula_asset(name, fallback, width=4.1):
    file = ROOT / 'assets' / 'rendered' / f'{name}.png'
    if file.exists():
        img = ImageMobject(str(file))
        img.scale_to_fit_width(width)
        return img
    return vtext(fallback, 37, P['cyan'], bold=True, max_w=width)


class COMB01(Scene):
    """The rule of sum, including the overlap counterexample."""

    def setup(self):
        self.frame = Group()
        self.left_objects = Group()
        self.right_objects = Group()
        self.section_no = 0
        self.make_frame()

    def make_frame(self):
        top = vtext('SANG MATH  /  ĐẠI SỐ TỔ HỢP', 22, P['cyan'], bold=True)
        top.move_to([-3.61, 3.60, 0])
        page = vtext('COMB01  ·  QUY TẮC CỘNG', 21, P['muted'])
        page.move_to([4.12, 3.60, 0])
        separator = Line([-6.9, 3.28, 0], [6.9, 3.28, 0],
                         stroke_color=P['line'], stroke_width=1.3)
        left = card_box(LEFT_W, PANEL_H, P['panel'])
        right = card_box(RIGHT_W, PANEL_H, P['panel'])
        left.move_to([LEFT, PANEL_Y, 0])
        right.move_to([RIGHT, PANEL_Y, 0])
        foot = vtext('CHỌN ĐÚNG MỘT PHƯƠNG ÁN  ·  KHÔNG ĐẾM TRÙNG',
                     19, P['muted'], max_w=12.6)
        foot.move_to([0, -3.77, 0])
        self.frame = Group(top, page, separator, left, right, foot)
        self.add(self.frame)

    def L(self, mob):
        self.left_objects.add(mob)
        self.play(FadeIn(mob), run_time=0.75)
        return mob

    def R(self, mob):
        self.right_objects.add(mob)
        self.play(FadeIn(mob), run_time=0.65)
        return mob

    def clear_content(self, run_time=0.60):
        things = Group(*list(self.left_objects), *list(self.right_objects))
        if len(things):
            self.play(FadeOut(things), run_time=run_time)
        self.left_objects = Group()
        self.right_objects = Group()

    def right_note(self, heading, body, highlight=None, last=None):
        """Create self-contained right panel, keeping text away from left panel."""
        objs = Group()
        h = vtext(heading, 31, P['gold'], bold=True, max_w=6.45)
        h.move_to([RIGHT, 2.20, 0])
        objs.add(h)
        y = 1.43
        for line in body:
            t = vtext(line, 26, P['text'], max_w=6.42)
            t.move_to([RIGHT, y, 0])
            objs.add(t)
            y -= 0.53
        if highlight is not None:
            if isinstance(highlight, tuple):
                asset, fallback = highlight
                f = formula_asset(asset, fallback, width=5.4)
            else:
                f = vtext(highlight, 37, P['cyan'], bold=True, max_w=5.6)
            f.move_to([RIGHT, min(y - 0.25, -0.15), 0])
            objs.add(f)
        if last:
            rule = tag(last, P['purple'], width=6.10, font_size=19)
            rule.move_to([RIGHT, -2.75, 0])
            objs.add(rule)
        return objs

    def scene_title(self, title, kicker):
        t = vtext(title, 40, P['text'], bold=True, max_w=5.50)
        t.move_to([LEFT, 1.86, 0])
        k = vtext(kicker, 24, P['muted'], max_w=5.45)
        k.move_to([LEFT, 1.34, 0])
        return Group(t, k)

    def route_graph(self):
        """Five distinct paths: two bus routes, three train routes."""
        origin = np.array([-6.13, -0.56, 0])
        target = np.array([-1.48, -0.56, 0])
        heights = [1.42, 0.68, -0.09, -0.84, -1.60]
        routes = VGroup()
        colors = [P['cyan'], P['cyan'], P['gold'], P['gold'], P['gold']]
        for i, (h, c) in enumerate(zip(heights, colors)):
            curve = CubicBezier(origin, [-5.05, h, 0], [-2.55, h, 0], target,
                                stroke_color=c, stroke_width=5)
            curve.set_opacity(0.8)
            routes.add(curve)
        a = Circle(radius=0.35, fill_color=P['panel_alt'], fill_opacity=1,
                   stroke_width=2.6, stroke_color=P['text']).move_to(origin)
        b = Circle(radius=0.35, fill_color=P['panel_alt'], fill_opacity=1,
                   stroke_width=2.6, stroke_color=P['text']).move_to(target)
        t_a = vtext('A', 30, P['text'], bold=True).move_to(a)
        t_b = vtext('B', 30, P['text'], bold=True).move_to(b)
        labels = Group()
        for i, (h, c) in enumerate(zip(heights, colors)):
            s = f'XE {i+1}' if i < 2 else f'TÀU {i-1}'
            lab = tag(s, c, width=1.15, font_size=17)
            lab.move_to([-3.82, (h - 0.56) * 0.66, 0])
            labels.add(lab)
        g = Group(routes, a, b, t_a, t_b, labels)
        return g, routes, origin

    def lesson_hook(self):
        group = self.scene_title('Một hành trình,', 'Có bao nhiêu con đường?')
        graph, routes, origin = self.route_graph()
        right = self.right_note('BÀI TOÁN MỞ ĐẦU', [
            'Từ A đến B có 2 tuyến xe buýt',
            'và 3 tuyến tàu khác nhau.',
            'Chọn đúng 1 tuyến để đi.',
            'Hỏi có bao nhiêu cách chọn?'
        ], last='Đoán kết quả trước khi đếm!')
        self.L(group)
        self.left_objects.add(graph)
        self.play(Create(routes, lag_ratio=0.13), run_time=3.0)
        self.play(FadeIn(Group(*list(graph)[1:])), run_time=0.8)
        self.R(right)
        self.wait(2.0)
        for i in range(5):
            dot = Dot(routes[i].get_start(), radius=0.105, color=P['text'])
            self.add(dot)
            self.play(MoveAlongPath(dot, routes[i]), run_time=0.95)
            self.remove(dot)
        self.wait(1.0)

    def lesson_count(self):
        self.clear_content()
        title = self.scene_title('Phân thành 2 nhóm', 'Không có lựa chọn nào trùng nhau')
        self.L(title)
        positions = [[-5.65, 0.45, 0], [-3.95, 0.45, 0],
                     [-5.65, -0.65, 0], [-3.95, -0.65, 0], [-2.25, -0.65, 0]]
        chips = Group()
        for i, pos in enumerate(positions):
            s = f'Xe {i+1}' if i < 2 else f'Tàu {i-1}'
            c = P['cyan'] if i < 2 else P['gold']
            chip = tag(s, c, width=1.43, font_size=21)
            chip.move_to(pos)
            chips.add(chip)
        self.left_objects.add(chips)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips],
                              lag_ratio=0.18), run_time=2.5)
        self.R(self.right_note('HAI NHÓM LỰA CHỌN', [
            'Nhóm 1: chọn xe buýt → 2 cách',
            'Nhóm 2: chọn tàu → 3 cách',
            'Chỉ chọn một trong hai nhóm.'
        ], highlight=('sum5', '2 + 3 = 5'), last='Hai nhóm không giao nhau'))
        self.wait(2.0)
        self.play(Indicate(chips[:2], color=P['cyan']), run_time=1.8)
        self.play(Indicate(chips[2:], color=P['gold']), run_time=1.8)
        self.wait(2.0)

    def lesson_rule(self):
        self.clear_content()
        heading = self.scene_title('Từ ví dụ đến quy tắc', 'Chọn phương án A hoặc B')
        a_group = card_box(2.30, 1.45, stroke=P['cyan']).move_to([-5.20, 0.20, 0])
        b_group = card_box(2.30, 1.45, stroke=P['gold']).move_to([-2.43, 0.20, 0])
        group_label = Group(
            vtext('Nhóm A', 27, P['cyan'], bold=True).move_to([-5.20, 0.47, 0]),
            vtext('m cách', 26, P['text']).move_to([-5.20, -0.13, 0]),
            vtext('Nhóm B', 27, P['gold'], bold=True).move_to([-2.43, 0.47, 0]),
            vtext('n cách', 26, P['text']).move_to([-2.43, -0.13, 0]),
        )
        self.L(Group(heading, a_group, b_group, group_label))
        self.R(self.right_note('QUY TẮC CỘNG', [
            'Một công việc được thực hiện',
            'theo phương án A hoặc B.',
            'A có m cách; B có n cách.',
            'Hai nhóm kết quả không trùng.'
        ], highlight=('sum_general', 'm + n'),
            last='Nếu giao nhau, phải trừ phần trùng'))
        self.play(Circumscribe(a_group, color=P['cyan']), run_time=1.7)
        self.play(Circumscribe(b_group, color=P['gold']), run_time=1.7)
        self.wait(4.0)

    def lesson_books(self):
        self.clear_content()
        self.L(self.scene_title('Áp dụng với sách', 'Chọn đúng một cuốn sách'))
        books = Group()
        for i in range(7):
            x = -6.26 + i * 0.81
            col = P['cyan'] if i < 4 else P['gold']
            cover = RoundedRectangle(width=0.65, height=1.45,
                    corner_radius=0.09, stroke_color=col, stroke_width=1.8,
                    fill_color=col, fill_opacity=0.20).move_to([x, -0.10, 0])
            label = vtext(('T' if i < 4 else 'L') + str(i+1 if i < 4 else i-3),
                          24, col, bold=True).move_to(cover)
            books.add(VGroup(cover, label))
        self.left_objects.add(books)
        self.play(LaggedStart(*[FadeIn(m, shift=0.12*UP) for m in books],
                              lag_ratio=0.12), run_time=2.6)
        self.R(self.right_note('VÍ DỤ 2 · CHỌN SÁCH', [
            'Có 4 sách Toán khác nhau.',
            'Có 3 sách Vật lí khác nhau.',
            'Chọn đúng một cuốn.',
            'Hai loại sách không trùng.'
        ], highlight=('sum7', '4 + 3 = 7'), last='Kết quả: 7 cách chọn'))
        self.wait(3.0)
        self.play(Indicate(books[:4], color=P['cyan']), run_time=1.8)
        self.play(Indicate(books[4:], color=P['gold']), run_time=1.8)
        self.wait(1.5)

    def number_grid(self):
        group = Group()
        tiles = {}
        for n in range(1, 13):
            row = (n-1)//4
            col = (n-1)%4
            x = -5.92 + col * 1.36
            y = 0.89 - row * 1.00
            outer = RoundedRectangle(width=1.06, height=0.73,
                           corner_radius=0.13, stroke_color=P['line'],
                           stroke_width=1.4, fill_color=P['panel_alt'],
                           fill_opacity=1).move_to([x,y,0])
            label = vtext(str(n), 28, P['text'], bold=True).move_to(outer)
            tile = VGroup(outer,label)
            tiles[n] = tile
            group.add(tile)
        return group, tiles

    def lesson_overlap(self):
        self.clear_content()
        tiles_grp, tiles = self.number_grid()
        self.L(self.scene_title('Cẩn thận đếm trùng!', 'Các số nguyên từ 1 đến 12'))
        self.left_objects.add(tiles_grp)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles_grp],
                              lag_ratio=0.08), run_time=2.3)
        self.R(self.right_note('THỬ THÁCH', [
            'Đếm số chia hết cho 2 hoặc 3',
            'trong các số từ 1 đến 12.',
            'Chia hết cho 2: 6 số.',
            'Chia hết cho 3: 4 số.'
        ], last='Có phải 6 + 4 = 10?'))
        even = [n for n in range(1,13) if n % 2 == 0]
        mult3 = [n for n in range(1,13) if n % 3 == 0]
        intersect = [n for n in range(1,13) if n % 6 == 0]
        self.play(*[tiles[n][0].animate.set_fill(P['cyan'], opacity=0.48)
                    for n in even], run_time=2.0)
        self.wait(0.8)
        self.play(*[tiles[n][0].animate.set_fill(P['gold'], opacity=0.48)
                    for n in mult3], run_time=2.0)
        self.wait(0.8)
        self.play(*[tiles[n][0].animate.set_fill(P['red'], opacity=0.70)
                    for n in intersect], run_time=2.0)
        self.wait(1.2)
        self.play(FadeOut(self.right_objects), run_time=0.6)
        self.right_objects = Group()
        self.R(self.right_note('CHỈ ĐẾM MỖI SỐ MỘT LẦN', [
            'Số 6 và 12 bị tính hai lần.',
            'Lấy tổng rồi trừ phần trùng.',
            '6 số chẵn, 4 bội của 3,',
            '2 số là bội của cả hai.'
        ], highlight=('union', '6 + 4 - 2 = 8'),
            last='Quy tắc cộng cần kiểm tra giao nhau'))
        self.play(Indicate(Group(tiles[6],tiles[12]), color=P['red']),
                  run_time=2.3)
        self.wait(3.0)

    def lesson_final(self):
        self.clear_content()
        left_group = self.scene_title('Ghi nhớ', 'Chọn một trong nhiều phương án')
        lab1 = tag('CỘNG', P['cyan'], width=2.35, font_size=30)
        lab1.move_to([LEFT, 0.57, 0])
        lab2 = tag('KHÔNG TRÙNG', P['green'], width=4.55, font_size=24)
        lab2.move_to([LEFT, -0.42, 0])
        self.L(Group(left_group,lab1,lab2))
        self.R(self.right_note('TỰ KIỂM TRA', [
            'Có 5 lựa chọn loại A và',
            '2 lựa chọn loại B.',
            'Hai nhóm không trùng nhau.',
            'Có tất cả bao nhiêu cách?'
        ], last='Tạm dừng video và tự trả lời'))
        self.wait(3.5)
        self.play(FadeOut(self.right_objects), run_time=0.65)
        self.right_objects = Group()
        self.R(self.right_note('ĐÁP ÁN', [
            'Dùng quy tắc cộng vì',
            'chọn đúng một trong hai loại,',
            'và các lựa chọn không trùng.'
        ], highlight=('quiz7', '5 + 2 = 7'),
            last='COMB02 · Tiếp theo: QUY TẮC NHÂN'))
        self.wait(4.0)

    def construct(self):
        self.lesson_hook()
        self.lesson_count()
        self.lesson_rule()
        self.lesson_books()
        self.lesson_overlap()
        self.lesson_final()
        self.play(FadeOut(Group(self.left_objects,self.right_objects)),
                  run_time=0.7)
        thanks = vtext('Hiểu cách đếm trước khi dùng công thức.',
                       35, P['cyan'], bold=True, max_w=11.9)
        thanks.move_to([0, -0.15, 0])
        self.play(Write(thanks), run_time=1.5)
        self.wait(2.0)
