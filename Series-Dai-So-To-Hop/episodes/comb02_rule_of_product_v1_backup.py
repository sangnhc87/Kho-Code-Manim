"""COMB02 - QUY TAC NHAN - Sang Math Manim/Typst.

Run from repository root after `python scripts/build_formulas.py`:
    manim -ql episodes/comb02_rule_of_product.py COMB02
    manim -qh -r 1920,1080 --fps 30 episodes/comb02_rule_of_product.py COMB02

The scene has no synthesized voice. See narration_COMB02.md to record/sync.
Every item and line is constructed using Manim primitives; mathematical
expressions are pre-rendered by Typst into transparent PNG assets.
"""
from __future__ import annotations

from pathlib import Path
import sys

from manim import (
    Scene, config, VGroup, Group, Text, RoundedRectangle,
    Polygon, Line, Dot, Cross, ImageMobject,
    FadeIn, FadeOut, Create, Indicate, Circumscribe,
    LaggedStart, GrowFromCenter,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from series_config import PALETTE as P  # noqa: E402

config.background_color = P['bg']
config.frame_width = 14.222222
config.frame_height = 8.0

FONT = 'Noto Sans'
LEFT_X, RIGHT_X = -3.81, 3.18
LEFT_W, RIGHT_W = 6.13, 7.31
PANEL_Y, PANEL_H = -0.30, 6.32


def vtext(value, size=25, color=None, *, bold=False, max_w=None):
    text = Text(str(value), font=FONT, font_size=size,
                color=color or P['text'],
                weight='BOLD' if bold else 'NORMAL', line_spacing=0.85)
    if max_w is not None and text.width > max_w:
        text.scale_to_fit_width(max_w)
    return text


def panel(width, height, fill=None, stroke=None, corner=0.16):
    return RoundedRectangle(width=width, height=height,
                            corner_radius=corner, fill_opacity=1,
                            fill_color=fill or P['panel_alt'],
                            stroke_color=stroke or P['line'], stroke_width=1.2)


def badge(label, color, *, width=None, fontsize=19):
    word = vtext(label, fontsize, P['text'], max_w=(width - 0.25) if width else None)
    bg = RoundedRectangle(width=width or (word.width + 0.32), height=0.43,
                          corner_radius=0.12, stroke_color=color,
                          fill_color=color, fill_opacity=0.12, stroke_width=1.4)
    word.move_to(bg)
    return VGroup(bg, word)


def formula_asset(name, fallback, max_w=5.50):
    """Use Typst asset. Rendering without generated assets is only a rough draft."""
    path = ROOT / 'assets' / 'rendered' / f'{name}.png'
    if path.exists():
        picture = ImageMobject(str(path))
        picture.scale_to_fit_width(min(max_w, picture.width))
        if picture.height > 0.85:
            picture.scale_to_fit_height(0.85)
        return picture
    return vtext(fallback, 35, P['cyan'], bold=True, max_w=max_w)


def tshirt(label, color, center, scale=1.0):
    """A recognisable shirt icon, drawn without external assets."""
    points = [(-.39,.35),(-.17,.49),(-.09,.41),(.09,.41),(.17,.49),
              (.39,.35),(.60,.04),(.38,-.13),(.30,-.03),(.30,-.48),
              (-.30,-.48),(-.30,-.03),(-.38,-.13),(-.60,.04)]
    shape = Polygon(*[[x, y, 0] for x,y in points],
                    stroke_color=color, stroke_width=2.0,
                    fill_color=color, fill_opacity=0.24)
    short = vtext(label, 21, P['text'], bold=True, max_w=.70).move_to([0,-.10,0])
    return VGroup(shape, short).scale(scale).move_to(center)


def trousers(label, color, center, scale=1.0):
    points = [(-.41,.48),(.41,.48),(.36,-.52),(.05,-.52),(0,-.11),
              (-.05,-.52),(-.36,-.52)]
    shape = Polygon(*[[x, y, 0] for x,y in points],
                    stroke_color=color, stroke_width=2.0,
                    fill_color=color, fill_opacity=0.21)
    short = vtext(label, 19, P['text'], bold=True, max_w=.60).move_to([0,.20,0])
    return VGroup(shape, short).scale(scale).move_to(center)


def small_option(kind, name, x, y):
    """Small labelled card for the grid and decision tree."""
    color = P['cyan'] if kind == 'shirt' else P['gold']
    shape = panel(1.24, .54, fill=P['panel_alt'], stroke=color, corner=.13)
    label = vtext(name, 19, P['text'], bold=True, max_w=.98).move_to(shape)
    return VGroup(shape, label).move_to([x, y, 0])


def outfit_cell(shirt_no, pant_no, x, y):
    """A valid clothing pair, identified by its ordered pair (shirt, pants)."""
    card = panel(1.61, 1.24, fill=P['panel_alt'])
    sh = tshirt(f'A{shirt_no}', P['cyan'], [0, .18, 0], scale=.59)
    pa = trousers(f'Q{pant_no}', P['gold'], [.53, .18, 0], scale=.56)
    sh.shift([-.29, 0, 0])
    name = vtext(f'A{shirt_no} – Q{pant_no}', 17, P['text'], max_w=1.35)
    name.move_to([0, -.43, 0])
    return VGroup(card, sh, pa, name).move_to([x, y, 0])


class COMB02(Scene):
    """8 sections: model, enumeration, tree, general rule, hats, restriction,
    branch-based count, contrast and mini exercise.
    """

    def setup(self):
        self.left_content = Group()
        self.right_content = Group()
        self.header_frame()

    def header_frame(self):
        top = vtext('SANG MATH  /  ĐẠI SỐ TỔ HỢP', 22, P['cyan'], bold=True)
        top.move_to([-3.63, 3.60, 0])
        page = vtext('COMB02  ·  QUY TẮC NHÂN', 21, P['muted'])
        page.move_to([4.10, 3.60, 0])
        separator = Line([-6.90,3.28,0],[6.90,3.28,0],
                         stroke_color=P['line'], stroke_width=1.3)
        left = panel(LEFT_W, PANEL_H, fill=P['panel']).move_to([LEFT_X,PANEL_Y,0])
        right = panel(RIGHT_W, PANEL_H, fill=P['panel']).move_to([RIGHT_X,PANEL_Y,0])
        footer = vtext('MỖI BỘ TRANG PHỤC  =  MỘT ÁO VÀ MỘT QUẦN',
                       18, P['muted'], max_w=12)
        footer.move_to([0,-3.77,0])
        self.add(Group(top,page,separator,left,right,footer))

    def add_left(self, obj, *animations, run_time=1):
        self.left_content.add(obj)
        if animations:
            self.play(*animations, run_time=run_time)
        else:
            self.play(FadeIn(obj), run_time=run_time)
        return obj

    def add_right(self, obj, run_time=.85):
        self.right_content.add(obj)
        self.play(FadeIn(obj), run_time=run_time)
        return obj

    def clear_content(self):
        current = Group(*self.left_content.submobjects, *self.right_content.submobjects)
        if len(current):
            self.play(FadeOut(current), run_time=.65)
        self.left_content = Group()
        self.right_content = Group()

    def left_title(self, headline, caption):
        title = vtext(headline, 36, P['text'], bold=True, max_w=5.53)
        title.move_to([LEFT_X,2.29,0])
        sub = vtext(caption, 22, P['muted'], max_w=5.55)
        sub.move_to([LEFT_X,1.76,0])
        return VGroup(title,sub)

    def explanation(self, title, lines, *, formula=None, note=None):
        """Right column: fixed baselines prevent touching formula/summary."""
        block = Group()
        title_m = vtext(title, 30, P['gold'], bold=True, max_w=6.3)
        title_m.move_to([RIGHT_X,2.25,0])
        block.add(title_m)
        for i, text in enumerate(lines[:5]):
            line = vtext(text, 25, P['text'], max_w=6.35)
            line.move_to([RIGHT_X,1.43 - i*.52,0])
            block.add(line)
        if formula:
            key, fallback = formula
            f = formula_asset(key, fallback)
            f.move_to([RIGHT_X,-1.57,0])
            block.add(f)
        if note:
            n = badge(note, P['purple'], width=6.15, fontsize=19)
            n.move_to([RIGHT_X,-2.78,0])
            block.add(n)
        return block

    def section_01_open(self):
        self.add_left(self.left_title('Mặc gì hôm nay?', '3 áo khác nhau · 2 quần khác nhau'))
        shirts = VGroup(*[tshirt(f'A{i+1}', P['cyan'], [-5.74 + i*1.90,.32,0])
                          for i in range(3)])
        pants = VGroup(*[trousers(f'Q{i+1}', P['gold'],[-4.78+i*1.90,-1.64,0])
                         for i in range(2)])
        for item in shirts:
            self.add_left(item, GrowFromCenter(item), run_time=.55)
        for item in pants:
            self.add_left(item, GrowFromCenter(item), run_time=.60)
        question = self.explanation('BÀI TOÁN MỞ ĐẦU', [
            'Có 3 chiếc áo khác nhau',
            'và 2 chiếc quần khác nhau.',
            'Mỗi bộ gồm đúng 1 áo và 1 quần.',
            'Có bao nhiêu bộ trang phục?'
        ], note='Hãy tự đoán kết quả trước!')
        self.add_right(question)
        self.wait(3)
        self.play(Indicate(shirts[0], color=P['cyan']),
                  Indicate(pants[0], color=P['gold']), run_time=1.45)
        self.wait(1.5)

    def section_02_pairs(self):
        self.clear_content()
        self.add_left(self.left_title('Ghép từng áo với quần', 'Liệt kê đủ, không trùng'))
        right = self.explanation('LIỆT KÊ 6 KẾT QUẢ', [
            'Áo A1 đi cùng Q1 hoặc Q2: 2 bộ.',
            'Áo A2 cũng tạo được 2 bộ.',
            'Áo A3 cũng tạo được 2 bộ.',
            'Tổng cộng: 2 + 2 + 2 = 6.'
        ], formula=('comb02_product6', '3 × 2 = 6'),
          note='Mỗi ô = một bộ khác nhau')
        self.add_right(right)
        cells = VGroup(*[outfit_cell(i+1,j+1, -5.87+i*2.05, .50-j*1.74)
                         for i in range(3) for j in range(2)])
        self.left_content.add(cells)
        for col in range(3):
            self.play(LaggedStart(FadeIn(cells[col*2]), FadeIn(cells[col*2+1]),
                                  lag_ratio=.55), run_time=1.65)
            self.wait(.5)
        count = badge('6 BỘ KHÁC NHAU',P['green'],width=4.35, fontsize=25)
        count.move_to([LEFT_X,-2.71,0])
        self.add_left(count, GrowFromCenter(count), run_time=1.0)
        self.wait(2.2)

    def section_03_tree(self):
        self.clear_content()
        self.add_left(self.left_title('Cây lựa chọn hai tầng', 'Từ mỗi áo có 2 nhánh quần'))
        shirt_x = -4.69
        root = Dot([-6.27,-.24,0],radius=.13,color=P['text'])
        root_label = vtext('Bắt đầu',15,P['muted']).move_to([-6.15,-.65,0])
        shirt_y = [.93,-.18,-1.32]
        leaf_ys = [1.19,.59,.12,-.48,-1.01,-1.61]
        mid = [small_option('shirt',f'A{i+1}',shirt_x,y)
               for i,y in enumerate(shirt_y)]
        leaves = [small_option('pants',f'Q{j+1}',-1.86,leaf_ys[2*i+j])
                  for i in range(3) for j in range(2)]
        edges_root = [Line(root.get_center(),mid[i].get_left(),
                           stroke_color=P['cyan'],stroke_width=2.0) for i in range(3)]
        edges_leaf = [Line(mid[i].get_right(),leaves[2*i+j].get_left(),
                           stroke_color=P['gold'],stroke_width=2.0)
                      for i in range(3) for j in range(2)]
        g = Group(root,root_label,*mid,*leaves,*edges_root,*edges_leaf)
        self.left_content.add(g)
        self.play(FadeIn(root), FadeIn(root_label), run_time=.7)
        for i in range(3):
            self.play(Create(edges_root[i]),FadeIn(mid[i]),run_time=.62)
        for i in range(3):
            self.play(Create(edges_leaf[2*i]),Create(edges_leaf[2*i+1]),
                      FadeIn(leaves[2*i]),FadeIn(leaves[2*i+1]),run_time=1.15)
        self.add_right(self.explanation('VÌ SAO LẠI NHÂN?', [
            'Bước 1: chọn áo, có 3 khả năng.',
            'Bước 2: với mỗi áo, có 2 quần.',
            'Vậy có 3 nhóm, mỗi nhóm 2 bộ.',
            'Số lá cây chính là số kết quả.'
        ],formula=('comb02_product6', '3 × 2 = 6'),
           note='3 nhánh áo · mỗi nhánh 2 quần'))
        self.play(LaggedStart(*[Indicate(leaf,color=P['green']) for leaf in leaves],
                              lag_ratio=.18),run_time=3.6)
        self.wait(1.2)

    def section_04_rule(self):
        self.clear_content()
        self.add_left(self.left_title('Phát hiện quy tắc nhân', 'Một công việc gồm các bước'))
        first = panel(2.18,1.53,stroke=P['cyan']).move_to([-5.14,-.24,0])
        second = panel(2.18,1.53,stroke=P['gold']).move_to([-2.36,-.24,0])
        a = vtext('BƯỚC 1',24,P['cyan'],bold=True).move_to([-5.14,.10,0])
        at = vtext('m cách',26,P['text']).move_to([-5.14,-.40,0])
        b = vtext('BƯỚC 2',24,P['gold'],bold=True).move_to([-2.36,.10,0])
        bt = vtext('n cách',26,P['text']).move_to([-2.36,-.40,0])
        arrow = Line([-3.99,-.24,0],[-3.52,-.24,0],stroke_color=P['green'],stroke_width=5)
        diagram = VGroup(first,second,a,at,b,bt,arrow)
        self.add_left(diagram, GrowFromCenter(diagram),run_time=1.3)
        dotnote = badge('THỰC HIỆN CẢ HAI BƯỚC',P['green'],width=4.75,fontsize=22)
        dotnote.move_to([LEFT_X,-1.95,0])
        self.add_left(dotnote)
        self.add_right(self.explanation('QUY TẮC NHÂN', [
            'Bước 1 có m cách thực hiện.',
            'Với MỖI kết quả của bước 1,',
            'bước 2 có đúng n cách.',
            'Số cách thực hiện cả hai bước:'
        ], formula=('comb02_productgeneral','m × n'),
           note='Chỉ nhân trực tiếp khi đủ điều kiện'))
        self.wait(3.2)
        self.play(Indicate(first,color=P['cyan']),run_time=1.2)
        self.play(Indicate(second,color=P['gold']),run_time=1.2)
        self.wait(1)

    def section_05_hats(self):
        self.clear_content()
        self.add_left(self.left_title('Nếu thêm một lựa chọn?', 'Có 2 chiếc mũ khác nhau'))
        rows = VGroup()
        data = [('Áo',3,P['cyan']),('Quần',2,P['gold']),('Mũ',2,P['purple'])]
        for idx,(label,amount,color) in enumerate(data):
            y = .81-idx*1.20
            label_m = badge(label,color,width=1.45,fontsize=22)
            label_m.move_to([-5.91,y,0])
            chips = VGroup(*[Dot(radius=.17,color=color).move_to([-4.48+j*.62,y,0])
                             for j in range(amount)])
            number = vtext(f'{amount} cách',23,P['text']).move_to([-2.01,y,0])
            rows.add(VGroup(label_m,chips,number))
        self.left_content.add(rows)
        for row in rows:
            self.play(FadeIn(row,shift=[0,.22,0]),run_time=.85)
        self.add_right(self.explanation('QUY TẮC NHÂN BA BƯỚC', [
            'Bước 1: chọn áo có 3 cách.',
            'Bước 2: chọn quần có 2 cách.',
            'Bước 3: chọn mũ có 2 cách.',
            'Mỗi bộ gồm đủ ba món.'
        ],formula=('comb02_product12','3 × 2 × 2 = 12'),
           note='Quy tắc nhân mở rộng nhiều bước'))
        self.wait(2)
        for row in rows:
            self.play(Indicate(row,color=P['green']),run_time=.8)
        self.wait(1.8)

    def section_06_forbidden(self):
        self.clear_content()
        self.add_left(self.left_title('Khi xuất hiện điều kiện cấm', 'A1 không được đi cùng Q2'))
        right = self.explanation('ĐẾM CÁCH HỢP LỆ', [
            'Ban đầu có 6 bộ trang phục.',
            'Cấm duy nhất cặp (A1, Q2).',
            'Loại đúng 1 bộ không hợp lệ.',
            'Còn lại 5 bộ được phép.'
        ],formula=('comb02_forbidden5','6 − 1 = 5'),
          note='Trường hợp bị cấm phải loại rõ ràng')
        cells = VGroup(*[outfit_cell(i+1,j+1,-5.87+i*2.05,.5-j*1.74)
                         for i in range(3) for j in range(2)])
        self.left_content.add(cells)
        self.play(LaggedStart(*[FadeIn(m) for m in cells],lag_ratio=.16),run_time=2)
        self.add_right(right)
        banned = cells[1]
        self.play(Circumscribe(banned,color=P['red'],run_time=1.2))
        overlay = Cross(banned,stroke_color=P['red'],stroke_width=6)
        self.add_left(overlay,Create(overlay),run_time=.8)
        self.play(banned.animate.set_opacity(.32),run_time=.9)
        greens = [cells[i] for i in range(6) if i!=1]
        self.play(LaggedStart(*[Indicate(g,color=P['green']) for g in greens],
                              lag_ratio=.12),run_time=2.8)
        self.wait(1.5)

    def section_07_branch_count(self):
        self.clear_content()
        self.add_left(self.left_title('Cẩn thận với điều kiện!', 'Số quần còn lại không như nhau'))
        lines = VGroup()
        for i,(name,cnt) in enumerate([('A1',1),('A2',2),('A3',2)]):
            y = .94-i*1.04
            sh = small_option('shirt',name,-5.80,y)
            chips = VGroup(*[small_option('pants',f'Q{k+1}',-3.73+k*1.4,y)
                             for k in range(cnt)])
            number = vtext(f'{cnt} cách',21,P['green']).move_to([-1.61,y,0])
            lines.add(VGroup(sh,chips,number))
        self.left_content.add(lines)
        for line in lines:
            self.play(FadeIn(line,shift=[0,.16,0]),run_time=.85)
        self.add_right(self.explanation('ĐẾM THEO TỪNG NHÁNH', [
            'Nếu chọn A1: chỉ còn quần Q1.',
            'Nếu chọn A2: có 2 quần.',
            'Nếu chọn A3: có 2 quần.',
            'Cộng các nhánh khác nhau:'
        ],formula=('comb02_branch5','1 + 2 + 2 = 5'),
           note='Không được dùng 3 × 2 sau khi cấm'))
        self.wait(2.2)
        self.play(LaggedStart(*[Indicate(row,color=P['green']) for row in lines],
                              lag_ratio=.3),run_time=3)
        self.wait(1.5)

    def section_08_compare_quiz(self):
        self.clear_content()
        self.add_left(self.left_title('Phân biệt CỘNG và NHÂN', '"Hoặc" khác với "và"'))
        cases = VGroup()
        rows = [
            ('Áo HOẶC quần', '3 + 2 = 5', P['gold']),
            ('Áo VÀ quần', '3 × 2 = 6', P['cyan']),
        ]
        for i,(title,answer,color) in enumerate(rows):
            box = panel(4.80,1.17,stroke=color).move_to([LEFT_X,.55-i*1.55,0])
            t = vtext(title,24,P['text'],bold=True,max_w=4.34)
            t.move_to([LEFT_X,.78-i*1.55,0])
            answer_t = vtext(answer,25,color,bold=True,max_w=4.3)
            answer_t.move_to([LEFT_X,.29-i*1.55,0])
            cases.add(VGroup(box,t,answer_t))
        self.left_content.add(cases)
        self.play(FadeIn(cases[0]),run_time=.9)
        self.play(FadeIn(cases[1]),run_time=.9)
        self.add_right(self.explanation('THỬ SỨC NHANH', [
            'Bữa sáng gồm đúng 1 món ăn,',
            '1 đồ uống và 1 phần trái cây.',
            'Có 2 món, 3 đồ uống, 2 loại quả.',
            'Có bao nhiêu cách chọn bữa sáng?'
        ],note='Tự tính trước khi hiện đáp án!'))
        self.wait(4)
        self.play(Indicate(cases[1],color=P['cyan']),run_time=1.3)
        self.right_content.add(answer := formula_asset('comb02_quiz12','2 × 3 × 2 = 12',max_w=4.8))
        answer.move_to([RIGHT_X,-1.62,0])
        self.play(FadeIn(answer,scale=.82),run_time=1.15)
        self.wait(2.0)
        self.clear_content()
        final_title = vtext('QUY TẮC NHÂN',39,P['cyan'],bold=True).move_to([0,1.35,0])
        final_sub = vtext('Lựa chọn liên tiếp · mỗi nhánh đủ số cách',29,P['text'],max_w=10.8)
        final_sub.move_to([0,.41,0])
        final_formula = formula_asset('comb02_productgeneral','m × n',max_w=5.5)
        final_formula.move_to([0,-.56,0])
        badge_final = badge('COMB02  /  HẾT VIDEO 02',P['purple'],width=6.10,fontsize=22)
        badge_final.move_to([0,-1.64,0])
        self.play(FadeIn(final_title),FadeIn(final_sub),FadeIn(final_formula),
                  GrowFromCenter(badge_final),run_time=1.35)
        self.wait(3)

    def construct(self):
        self.section_01_open()
        self.section_02_pairs()
        self.section_03_tree()
        self.section_04_rule()
        self.section_05_hats()
        self.section_06_forbidden()
        self.section_07_branch_count()
        self.section_08_compare_quiz()
