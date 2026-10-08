"""COMB02 V2: comprehensive Manim–Typst lesson on the rule of product.

Usage (from repo root):
  python scripts/prepare_comb02_v2.py --voice off
  manim -ql -r 854,480 episodes/comb02_rule_of_product.py COMB02

For voiced teaching, prepare with --voice on. Every beat has a real voice clip
and its on-screen mathematical reveal is scheduled against that clip.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comb02_lesson_data import BEATS, CHAPTER_LABELS
from series_config import PALETTE as C

config.background_color = C['bg']
config.frame_width = 14.222222
config.frame_height = 8.0
FONT = 'Noto Sans'
LEFT_X, RIGHT_X = -3.82, 3.22


def tx(value, x=0., y=0., size=22, color=None, strong=False, max_width=5.8):
    mob = Text(str(value), font=FONT, font_size=size,
               color=color or C['text'], weight='BOLD' if strong else 'NORMAL')
    if max_width and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    mob.move_to(np.array([x,y,0.]))
    return mob


def plate(width, height, color=None, fill=None, radius=.15):
    return RoundedRectangle(width=width, height=height,corner_radius=radius,
                            fill_color=fill or C['panel_alt'],fill_opacity=1,
                            stroke_width=1.4,stroke_color=color or C['line'])


def pill(label,x,y,color=C['cyan'],w=1.20,h=.60,font_size=22):
    p=plate(w,h,color)
    p.move_to([x,y,0])
    t=tx(label,x,y,font_size,C['text'],True,w-.15)
    return VGroup(p,t)


def shirt(label,x,y,scale=.75):
    v=[(-.37,.33),(-.17,.51),(-.08,.42),(.08,.42),(.17,.51),(.37,.33),
       (.59,.03),(.40,-.15),(.30,-.02),(.30,-.50),(-.30,-.50),(-.30,-.02),(-.40,-.15),(-.59,.03)]
    p=Polygon(*[[a,b,0] for a,b in v],stroke_color=C['cyan'],stroke_width=2.0,
              fill_color=C['cyan'],fill_opacity=.18)
    tag=tx(label,0,-.07,19,C['text'],True,.55)
    return VGroup(p,tag).scale(scale).move_to([x,y,0])


def trousers(label,x,y,scale=.75):
    v=[(-.40,.43),(.40,.43),(.36,-.53),(.07,-.53),(0,-.10),(-.07,-.53),(-.36,-.53)]
    p=Polygon(*[[a,b,0] for a,b in v],stroke_color=C['gold'],stroke_width=2,
              fill_color=C['gold'],fill_opacity=.17)
    tag=tx(label,0,.19,18,C['text'],True,.50)
    return VGroup(p,tag).scale(scale).move_to([x,y,0])


def edge(x1,y1,x2,y2,col,width=2.3,alpha=1.):
    return Line([x1,y1,0],[x2,y2,0],stroke_color=col,stroke_width=width,stroke_opacity=alpha)


def count_label(string, y=-2.44,color=None,size=23):
    return tx(string,LEFT_X,y,size,color or C['green'],True,5.75)


def _outfit(s):
    g=VGroup()
    g.add(tx('BA CHIẾC ÁO',-4.94,2.18,20,C['cyan'],True))
    for i,x in enumerate([-5.86,-4.21,-2.56]):
        o=shirt(f'A{i+1}',x,1.30,.90)
        if s in (2,3,4) and i!=s-2:o.set_opacity(.22)
        g.add(o)
    g.add(tx('HAI CHIẾC QUẦN',-4.94,.34,20,C['gold'],True))
    for j,x in enumerate([-5.45,-3.55]):
        g.add(trousers(f'Q{j+1}',x,-.43,.85))
    if s>=1:
        g.add(tx('Một bộ = (áo, quần)',LEFT_X,-1.27,21,C['muted']))
    rows=[('A1','Q1'),('A1','Q2'),('A2','Q1'),('A2','Q2'),('A3','Q1'),('A3','Q2')]
    max_rows=2 if s==2 else 4 if s==3 else 6 if s>=4 else 0
    for k,(a,q) in enumerate(rows[:max_rows]):
        x=-5.48+(k%3)*1.66
        y=-1.78-(k//3)*.55
        c=C['cyan'] if k<2 else C['gold'] if k<4 else C['purple']
        g.add(pill(f'{a},{q}',x,y,c,1.43,.48,16))
    if s==5:g.add(count_label('3 × 2 = 6 bộ',-2.87,C['green'],22))
    return g, g[1 + min(2,max(0,s-2))] if 2<=s<=4 else g[1]


def _grid(s, forbidden=False):
    g=VGroup()
    g.add(tx('BẢNG CÁC BỘ ÁO–QUẦN',LEFT_X,2.36,20,C['cyan'],True))
    g.add(tx('Q1',-3.65,1.66,20,C['gold'],True),tx('Q2',-1.84,1.66,20,C['gold'],True))
    for i in range(3):
        y=.87-i*1.15
        g.add(tx('A'+str(i+1),-5.60,y,21,C['cyan'],True))
        for j in range(2):
            bad=forbidden and i==1 and j==1
            shown=(s >= i+1) if not forbidden else True
            item=pill(f'A{i+1},Q{j+1}',-3.65+j*1.81,y,
                      C['red'] if bad else C['green'] if shown else C['line'],1.46,.70,18)
            if not shown and not forbidden:item.set_opacity(.18)
            g.add(item)
            if bad and s>=1:
                g.add(Line(item.get_left()+.15*RIGHT+(.15*UP),item.get_right()-.15*RIGHT-.15*UP,
                           color=C['red'],stroke_width=3.1))
                g.add(Line(item.get_left()+.15*RIGHT-.15*UP,item.get_right()-.15*RIGHT+.15*UP,
                           color=C['red'],stroke_width=3.1))
    if forbidden:
        if s==0:g.add(count_label('Điều kiện: cấm (A2,Q2)',-2.72,C['gold'],20))
        elif s==1:g.add(count_label('Đã loại đúng 1 ô',-2.72,C['red'],20))
        elif s in (2,5):g.add(count_label('6 - 1 = 5 bộ hợp lệ',-2.72,C['green'],20))
        else:g.add(count_label('A1: 2   ·   A2: 1   ·   A3: 2',-2.72,C['green'],19))
    else:
        if s>=3:g.add(count_label('2 + 2 + 2 = 3 × 2 = 6',-2.72,C['green'],20))
        else:g.add(count_label('Mỗi hàng là một áo',-2.72,C['muted'],19))
    return g, g[5] if len(g)>5 else g[0]


def _tree(s,counts=(2,2,2),generic=False):
    g=VGroup()
    g.add(tx('ĐƯỜNG ĐI = MỘT KẾT QUẢ',LEFT_X,2.34,20,C['cyan'],True))
    root_x=-6.12; root_y=-.11
    root=Dot([root_x,root_y,0],radius=.12,color=C['text'])
    g.add(root)
    g.add(tx('Gốc',root_x,.36,15,C['muted']))
    shirt_x=-4.36;leaf_x=-1.82
    for i in range(3):
        y=1.44-i*1.50
        g.add(edge(root_x,root_y,shirt_x-.27,y,C['cyan'],3.1))
        g.add(pill('A'+str(i+1),shirt_x,y,C['cyan'],.95,.55,19))
        active=s>=i+2 or s>=4 and counts == (2,2,2)
        if counts != (2,2,2):active=s>=i+1
        if not active:continue
        n=counts[i]
        shifts={1:[0],2:[.31,-.31],3:[.48,0,-.48]}[n]
        for j,dy in enumerate(shifts):
            yy=y+dy
            g.add(edge(shirt_x+.50,y,leaf_x-.41,yy,C['gold'],2.0))
            g.add(pill('Q'+str(j+1),leaf_x,yy,C['gold'],.72,.36,13))
    if counts == (2,2,2):
        if s>=4:g.add(count_label('Số lá: 2 + 2 + 2 = 6',-2.70,C['green'],21))
        else:g.add(count_label('Bước 1: áo   ·   Bước 2: quần',-2.70,C['muted'],18))
    else:
        if s>=3:g.add(count_label('Số lá: 2 + 1 + 3 = 6',-2.70,C['green'],21))
        else:g.add(count_label('Nhánh A1: 2; A2: 1; A3: 3',-2.70,C['muted'],18))
    return g, root


def _general(s):
    g=VGroup(tx('CÔNG VIỆC QUA HAI BƯỚC',LEFT_X,2.33,20,C['cyan'],True))
    nodes=[('X1',1.42),('X2',.48),('...',-.47),('Xm',-1.45)]
    g.add(tx('BƯỚC 1',-5.75,1.94,16,C['cyan'],True))
    g.add(tx('BƯỚC 2',-2.15,1.94,16,C['gold'],True))
    for i,(name,y) in enumerate(nodes):
        if name=='...':
            g.add(tx('...',-4.66,y,28,C['muted']))
            g.add(tx('...',-1.98,y,28,C['muted']))
            continue
        g.add(pill(name,-5.10,y,C['cyan'],1.25,.58,19))
        g.add(edge(-4.43,y,-2.85,y,C['gold']))
        g.add(pill('n cách',-2.19,y,C['gold'],1.38,.57,19))
    if s>=1:g.add(count_label('n + n + … + n (m nhánh)',-2.63,C['green'],20))
    else:g.add(count_label('Mỗi nhánh có đúng n kết quả',-2.63,C['muted'],20))
    return g, g[3]


def _hats(s):
    g=VGroup(tx('THÊM HAI CHIẾC MŨ',LEFT_X,2.33,20,C['cyan'],True))
    g.add(pill('M1',-4.64,1.63,C['purple'],1.19,.55,20))
    g.add(pill('M2',-3.03,1.63,C['purple'],1.19,.55,20))
    for i in range(6):
        x=-5.77+(i%3)*1.84;y=.63-(i//3)*1.08
        base=pill(f'A{i//2+1},Q{i%2+1}',x,y,C['cyan'],1.53,.65,17)
        g.add(base)
        if s>=1 and (i==0 or s>=2):
            g.add(tx('× 2 mũ',x,y-.37,14,C['gold']))
    if s>=2:g.add(count_label('6 bộ × 2 mũ = 12',-2.54,C['green'],22))
    else:g.add(count_label('1 bộ cũ sinh 2 bộ mới',-2.54,C['muted'],20))
    return g,g[1]


def _quiz(s):
    g=VGroup()
    if s in (0,1):
        g.add(tx('CHỌN HAI CHỮ SỐ KHÁC NHAU',LEFT_X,2.31,20,C['cyan'],True))
        for i,x in enumerate([-5.95,-4.59,-3.23,-1.87]):
            g.add(pill(str(i+1),x,1.23,C['cyan'],.92,.86,29))
        g.add(tx('Hàng chục',-5.0,.04,18,C['gold'],True))
        g.add(tx('Hàng đơn vị',-2.5,.04,18,C['gold'],True))
        g.add(pill('4 cách',-5.0,-.65,C['cyan'],1.68,.75,24))
        g.add(pill('3 cách',-2.5,-.65,C['gold'],1.68,.75,24))
        if s==1:g.add(count_label('4 × 3 = 12 số',-2.26,C['green'],25))
    elif s in (2,3):
        g.add(tx('CHỌN ĐÚNG MỘT MÓN',LEFT_X,2.31,20,C['cyan'],True))
        for i,x in enumerate([-5.84,-4.25,-2.66]):
            g.add(pill('B'+str(i+1),x,.75,C['cyan'],1.28,.87,25))
        for i,x in enumerate([-5.0,-3.02]):
            g.add(pill('V'+str(i+1),x,-.55,C['gold'],1.35,.87,25))
        if s==3:g.add(count_label('3 + 2 = 5 món',-2.33,C['green'],24))
        else:g.add(count_label('Một bút HOẶC một vở',-2.33,C['gold'],20))
    else:
        g.add(tx('4 ÁO · 3 QUẦN · 2 CẶP CẤM',LEFT_X,2.31,19,C['cyan'],True))
        xs=[-5.47,-4.05,-2.63]
        for j,x in enumerate(xs):g.add(tx('Q'+str(j+1),x,1.60,18,C['gold'],True))
        for i in range(4):
            y=.9-i*.87
            g.add(tx('A'+str(i+1),-6.27,y,17,C['cyan'],True))
            for j,x in enumerate(xs):
                bad=(i==0 and j in (1,2))
                c=C['red'] if bad else C['green'] if s==5 else C['line']
                g.add(pill('×' if bad else 'OK',x,y,c,.90,.59,20))
        if s==5:g.add(count_label('12 - 2 = 10 bộ hợp lệ',-2.72,C['green'],19))
    return g,g[1]

VISUALS = {
    'outfit':lambda i:_outfit(i), 'grid':lambda i:_grid(i),
    'tree':lambda i:_tree(i), 'general':lambda i:_general(i),
    'hat':lambda i:_hats(i), 'forbidden':lambda i:_grid(i,True),
    'uneven':lambda i:_tree(i,(2,1,3)), 'quiz':lambda i:_quiz(i),
}


def formula_png(key):
    path=ROOT/'assets'/'comb02v2'/f'{key}.png'
    if not path.exists():
        raise FileNotFoundError(f'Typst formula missing: {path}. Run scripts/prepare_comb02_v2.py')
    img=ImageMobject(str(path))
    if img.width>5.95:img.scale_to_fit_width(5.95)
    if img.height>.87:img.scale_to_fit_height(.87)
    img.move_to([RIGHT_X,-1.02,0])
    return img


class COMB02(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb02_voice_manifest.json'
        self.meta=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else None
        if self.meta and self.meta.get('beats')!=len(BEATS):
            raise ValueError('Outdated voice manifest: run prepare_comb02_v2.py again')
        self.old_visual=None
        self.old_intro=None
        self.old_result=None
        self.old_caption=None
        self.draw_canvas()

    def draw_canvas(self):
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.85,3.62,20,C['cyan'],True,6.3))
        self.add(tx('COMB02 · QUY TẮC NHÂN',4.18,3.62,20,C['muted'],True,5.2))
        self.add(edge(-6.87,3.31,6.87,3.31,C['line'],1.1))
        self.add(plate(6.18,6.27,C['line'],C['panel']).move_to([LEFT_X,-.02,0]))
        self.add(plate(7.23,6.27,C['line'],C['panel']).move_to([RIGHT_X,-.02,0]))
        self.add(edge(-6.86,-3.34,6.86,-3.34,C['line'],1.1))

    def make_panel(self,beat):
        introductory=Group(
            tx(CHAPTER_LABELS[beat.section],RIGHT_X,2.70,19,C['purple'],True,6.2),
            tx(beat.heading,RIGHT_X,2.16,27,C['gold'],True,6.2),
        )
        for j,line in enumerate(beat.lines):
            introductory.add(tx(line,RIGHT_X,1.51-j*.49,24,C['text'],False,6.15))
        result=Group()
        if beat.formula:
            result.add(formula_png(beat.formula))
        else:
            result.add(tx('QUAN SÁT  ·  SUY LUẬN  ·  KIỂM CHỨNG',RIGHT_X,-1.04,16,C['cyan'],False,6.1))
        result.add(edge(.24,-1.80,6.25,-1.80,C['line'],1.2))
        conclusion=tx(beat.takeaway,RIGHT_X,-2.48,22,C['green'],True,5.92)
        if conclusion.height>.70:conclusion.scale_to_fit_height(.70)
        result.add(conclusion)
        return introductory,result

    def make_caption(self,beat,index):
        return tx(f'{index+1:02d} / {len(BEATS)}     •     {beat.takeaway}',0,-3.73,
                  16,C['muted'],False,12.0)

    def perform(self,index,beat):
        clip=(self.meta or {}).get('clips',{}).get(f'{index:03}',{})
        clipfile=clip.get('file')
        if clipfile:
            source=ROOT/'voice'/clipfile
            if not source.exists():raise FileNotFoundError(f'Missing voice clip: {source}')
            self.add_sound(str(source))
        budget=max(float(beat.min_seconds),float(clip.get('duration',0))+.85)
        visual,focus=VISUALS[beat.section](beat.state)
        intro,result=self.make_panel(beat)
        caption=self.make_caption(beat,index)
        if self.old_visual is None:
            self.play(FadeIn(visual,shift=.09*UP),FadeIn(intro,shift=.06*RIGHT),
                      FadeIn(caption),run_time=1.7)
        else:
            self.play(FadeOut(self.old_visual),FadeIn(visual),
                      FadeOut(self.old_intro),FadeIn(intro),
                      FadeOut(self.old_result),
                      ReplacementTransform(self.old_caption,caption),run_time=1.7)
        self.old_visual,self.old_intro,self.old_caption=visual,intro,caption
        # Motion must convey the actual counting operation, not decoration.
        if beat.section == 'tree' and beat.state in (2,3,4):
            row=min(beat.state-2,2)
            yy=1.44-row*1.50
            trace=VMobject().set_points_as_corners([[-6.12,-.11,0],[-4.36,yy,0],[-1.82,yy+.31,0]])
            marker=Dot([-6.12,-.11,0],radius=.092,color=C['green'])
            self.add(marker)
            self.play(MoveAlongPath(marker,trace),run_time=2.8,rate_func=linear)
            self.remove(marker)
        elif beat.section == 'outfit' and beat.state in (2,3,4):
            shirt_x=[-5.86,-4.21,-2.56][beat.state-2]
            path=VMobject().set_points_as_corners([[shirt_x,1.30,0],[shirt_x,.22,0],[-5.48,-1.78,0]])
            marker=Dot([shirt_x,1.30,0],radius=.09,color=C['green'])
            self.add(marker)
            self.play(MoveAlongPath(marker,path),run_time=2.8,rate_func=linear)
            self.remove(marker)
        elif beat.section == 'forbidden' and beat.state in (1,2,3,4,5):
            marker=Dot([-1.84,-.28,0],radius=.12,color=C['red'])
            self.play(Flash(marker,flash_radius=.38,color=C['red']),run_time=2.8)
        else:
            self.play(Indicate(focus,scale_factor=1.08,color=C['gold']),run_time=2.8)
        self.play(FadeIn(result[0],shift=.06*UP),run_time=1.6)
        self.play(FadeIn(result[1]),FadeIn(result[2],shift=.08*UP),run_time=1.45)
        self.play(Circumscribe(result[2],color=C['green'],buff=.08),run_time=2.0)
        self.old_result=result
        used=1.7+2.8+1.6+1.45+2.0
        if budget>used:self.wait(budget-used)

    def construct(self):
        for idx,beat in enumerate(BEATS):self.perform(idx,beat)
        self.play(FadeOut(self.old_visual),FadeOut(self.old_intro),FadeOut(self.old_result),
                  FadeOut(self.old_caption),run_time=.9)
        headline=tx('HIỂU ĐỐI TƯỢNG · ĐẾM ĐỦ · KHÔNG TRÙNG',0,.25,35,C['cyan'],True,12.8)
        next_video=tx('COMB03 · SƠ ĐỒ CÂY VÀ KHÔNG GIAN MẪU',0,-.48,23,C['gold'],False,12.2)
        self.play(FadeIn(headline,scale=.96),FadeIn(next_video),run_time=1.6)
        self.wait(2.7)
