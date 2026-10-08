"""SANG MATH COMB04 V2 — Order matters? Render after prepare_comb04_v2.py.

Scene COMB04: 8 sections, 48 carefully staged didactic beats.
Left: exact combinatorial model. Right: 3 arguments and a conclusion.
"""
from __future__ import annotations
from pathlib import Path
import json, sys
import numpy as np
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb04_lesson_data import (BEATS, CHAPTER_LABELS, ORDERED4, UNORDERED4,
                                 ORDERS_ABC, UNORDERED5_3, UNORDERED6_2)

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.78
RX=3.22


def txt(s,x=0,y=0,size=21,color=None,bold=False,maxw=5.92):
    m=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if maxw and m.width>maxw:m.scale_to_fit_width(maxw)
    m.move_to([x,y,0])
    return m


def line(x1,y1,x2,y2,color=None,width=2):
    return Line([x1,y1,0],[x2,y2,0],stroke_color=color or C['line'],stroke_width=width)


def card(text,x,y,color=None,w=1.16,h=.54,size=21,opacity=1):
    p=RoundedRectangle(corner_radius=.115,width=w,height=h,stroke_width=1.6,
                       stroke_color=color or C['line'],fill_color=C['panel_alt'],fill_opacity=1)
    p.move_to([x,y,0])
    t=txt(text,x,y,size,C['text'],True,w-.17)
    return VGroup(p,t).set_opacity(opacity)


def label(s,y=2.45,color=None):return txt(s,LX,y,20,color or C['cyan'],True,5.65)
def bottom(s,color=None):return txt(s,LX,-2.70,19,color or C['green'],True,5.78)


def role_frame(people=('A','B'),team=False):
    g=VGroup()
    positions=(-5.18,-2.43)
    if team:
        box=RoundedRectangle(width=4.75,height=1.27,corner_radius=.16,stroke_color=C['cyan'],fill_color=C['panel_alt'],fill_opacity=.25)
        box.move_to([LX,.05,0]);g.add(box)
        g.add(txt('CÙNG MỘT ĐỘI',LX,1.29,18,C['cyan'],True))
    else:
        g.add(txt('TRƯỞNG',positions[0],1.34,19,C['cyan'],True,2),
              txt('PHÓ',positions[1],1.34,19,C['gold'],True,2))
    a=card(people[0],positions[0],.10,C['cyan'],1.25,.86,29)
    b=card(people[1],positions[1],.10,C['gold'],1.25,.86,29)
    g.add(a,b)
    g.add(bottom('Chỉ chọn thành viên' if team else 'Hai vị trí có vai trò khác nhau',C['cyan']))
    return g,(a,b)


def intro(s):
    g=VGroup(label('CHỌN TỪ BỐN HỌC SINH'))
    for i,name in enumerate('ABCD'):
        g.add(card(name,-6.08+i*1.56,1.28,C['cyan'] if i<2 else C['line'],.95,.69,24))
    if s in (0,4,5):
        g.add(txt('BÀI 1: CHỌN ĐỘI',-5.22,.18,19,C['cyan'],True,2.55),
              txt('BÀI 2: GIAO VIỆC',-2.39,.18,19,C['gold'],True,2.55))
        g.add(card('{A, B}',-5.22,-.72,C['cyan'],2.30,.78,26),
              card('(A, B)',-2.39,-.72,C['gold'],2.30,.78,26))
    elif s==1:
        g.add(card('AB',-5.15,-.65,C['cyan'],2.0,.85,28),
              card('BA',-2.39,-.65,C['cyan'],2.0,.85,28))
        g.add(txt('CÙNG THÀNH VIÊN',LX,-1.48,19,C['green'],True))
    elif s==2:
        g.add(txt('TRƯỞNG / PHÓ',LX,.20,20,C['gold'],True))
        g.add(card('AB',-5.20,-.70,C['cyan'],2,.8,28),
              card('BA',-2.40,-.70,C['gold'],2,.8,28))
        g.add(txt('HAI PHÂN CÔNG',LX,-1.48,19,C['gold'],True))
    else:
        g.add(card('AB = BA?',LX,-.63,C['purple'],3.70,.82,29),
              txt('CÂU HỎI LÀ: KẾT QUẢ NÀO?',LX,-1.52,17,C['cyan'],True))
    g.add(bottom('Quan sát phép đổi vị trí',C['gold']))
    return g,g[1]


def ordered(s):
    g=VGroup(label('PHÂN CÔNG TRƯỞNG / PHÓ'))
    g.add(txt('TRƯỞNG  →  PHÓ',LX,1.96,17,C['muted'],True))
    n=[4,3,6,12,12,12][s]
    for idx,pair in enumerate(ORDERED4):
        r=idx//3;c=idx%3
        x=-5.98+c*2.19;y=1.25-r*.81
        light=(idx<3 if s==1 else 3<=idx<6 if s==2 else pair in ('AB','BA') if s==5 else True)
        col=C['gold'] if pair in ('AB','BA') and s==5 else C['cyan'] if light else C['line']
        g.add(card(pair,x,y,col,1.57,.60,23,1.0 if (idx<n or s>=3) else .15))
    g.add(bottom('4 × 3 = 12 phân công' if s>=3 else 'Mỗi trưởng có 3 cách chọn phó',C['gold']))
    return g,g[min(len(g)-2,2)]


def unordered(s):
    g=VGroup(label('GOM HAI THỨ TỰ THÀNH MỘT'))
    pairs=[('AB','BA'),('AC','CA'),('AD','DA'),('BC','CB'),('BD','DB'),('CD','DC')]
    for i,(ab,ba) in enumerate(pairs):
        x=-5.52+(i%2)*2.75;y=1.65-(i//2)*1.21
        op=1. if (s>=2 or i==0) else .22
        g.add(card(ab,x-.62,y,C['cyan'],.90,.58,19,op),
              txt('=',x,y,20,C['muted']).set_opacity(op),
              card(ba,x+.62,y,C['gold'],.90,.58,19,op))
    g.add(bottom('12 cặp → 6 nhóm' if s>=3 else 'AB và BA: cùng nhóm {A, B}',C['green']))
    return g,g[1]


def swap(s):
    g,pair=role_frame(('A','B'),team=(s==2))
    if s in (0,3,4,5):
        g.add(txt('AB  ↔  BA',LX,-1.25,30,C['purple'],True))
    elif s==1:
        g.add(txt('NHÃN VAI TRÒ ĐỨNG YÊN',LX,-1.32,18,C['gold'],True))
    else:
        g.add(txt('NHÓM GIỮ NGUYÊN',LX,-1.32,20,C['green'],True))
    return g,pair


def choose3(s):
    g=VGroup(label('NĂM HỌC SINH: CHỌN BA'))
    for i,ch in enumerate('ABCDE'):
        g.add(card(ch,-6.25+i*1.23,1.75,C['cyan'] if i<3 else C['line'],.91,.58,22))
    if s in (2,3):
        g.add(txt('6 THỨ TỰ CỦA CÙNG NHÓM ABC',LX,1.04,17,C['gold'],True,5.7))
        for i,v in enumerate(ORDERS_ABC):
            g.add(card(v,-5.70+(i%3)*1.90,.27-(i//3)*1.03,C['purple'],1.54,.62,23))
    elif s>=4:
        for i,v in enumerate(UNORDERED5_3):
            g.add(card(v,-5.82+(i%3)*2.03,.99-(i//3)*.83,C['green'],1.52,.55,19))
    else:
        g.add(card('5 × 4 × 3',LX,-.24,C['cyan'],4.05,.93,32))
        g.add(txt('THỨ TỰ CÓ / KHÔNG CÓ VAI TRÒ',LX,-1.30,17,C['gold'],True))
    g.add(bottom('60 dãy : 6 = 10 nhóm' if s>=4 else 'Đếm 60 dãy rồi gộp thành nhóm',C['gold']))
    return g,g[1]


def choose6(s):
    g=VGroup(label('SÁU HỌC SINH, CHỌN HAI'))
    for i,ch in enumerate('ABCDEF'):
        g.add(card(ch,-6.30+i*.99,1.92,C['cyan'],.72,.50,19))
    if s in (0,1,3):
        g.add(txt('TRƯỞNG',-5.38,.64,20,C['cyan'],True),txt('PHÓ',-2.47,.64,20,C['gold'],True))
        g.add(card('6',-5.38,-.19,C['cyan'],1.54,.82,31),
              card('5',-2.47,-.19,C['gold'],1.54,.82,31))
        g.add(bottom('6 × 5 = 30 phân công',C['gold']))
    else:
        for i,pair in enumerate(UNORDERED6_2):
            g.add(card(pair,-5.88+(i%3)*2.10,1.19-(i//3)*.72,C['green'],1.54,.51,20))
        g.add(bottom('30 ÷ 2 = 15 nhóm',C['green']))
    return g,g[1]


def captain(s):
    g=VGroup(label('CHỌN ĐỘI BA NGƯỜI CÓ ĐỘI TRƯỞNG'))
    for i,ch in enumerate('ABCDEFGH'):
        g.add(card(ch,-6.32+(i%4)*1.63,1.70-(i//4)*.91,C['cyan'] if i==0 else C['line'],1.18,.53,20))
    if s in (1,2):
        g.add(txt('8 lựa chọn trưởng',LX,-.39,19,C['cyan'],True))
        g.add(card('21 nhóm 2 người',LX,-1.17,C['purple'],4.95,.62,20))
    elif s in (3,4):
        g.add(txt('56 nhóm ba người',LX,-.38,19,C['green'],True))
        g.add(card('3 cách chọn trưởng',LX,-1.17,C['gold'],4.95,.62,20))
    elif s==5:
        g.add(card('336 dãy / 2',LX,-1.10,C['purple'],4.70,.78,25))
    else:
        g.add(card('CHỌN 3 + CHỈ ĐỊNH TRƯỞNG',LX,-1.06,C['cyan'],5.50,.76,19))
    g.add(bottom('168 đội có chỉ định trưởng',C['gold']))
    return g,g[1]


def practice(s):
    if s in (0,2):return choose3(5) if s==2 else unordered(3)
    if s==1:
        g=VGroup(label('HAI GIẢI THƯỞNG KHÁC NHAU'))
        for i,ch in enumerate('ABCDE'):
            g.add(card(ch,-6.12+i*1.22,1.50,C['cyan'],.94,.68,22))
        g.add(card('GIẢI NHẤT',-5.20,.20,C['gold'],2.25,.77,18),
              card('GIẢI NHÌ',-2.38,.20,C['cyan'],2.25,.77,18),bottom('5 × 4 = 20 cách',C['gold']))
        return g,g[1]
    if s==4:
        g=VGroup(label('SƠ ĐỒ QUYẾT ĐỊNH'))
        g.add(card('ĐỔI CHỖ?',LX,1.23,C['purple'],3.50,.68,23))
        g.add(line(LX,.88,-5.18,.12,C['cyan']),line(LX,.88,-2.39,.12,C['gold']))
        g.add(card('CÓ ĐỔI KẾT QUẢ',-5.15,-.31,C['cyan'],2.30,.80,15),
              card('KHÔNG ĐỔI',-2.35,-.31,C['gold'],2.30,.80,16))
        g.add(txt('GIỮ THỨ TỰ',-5.15,-1.28,16,C['cyan'],True),
              txt('GOM THỨ TỰ',-2.35,-1.28,16,C['green'],True))
        g.add(bottom('Phải xét điều kiện chọn lặp',C['gold']))
        return g,g[1]
    if s==5:
        g=VGroup(label('HÀNH TRÌNH KIẾN THỨC'))
        for i,(title,sub) in enumerate([('05','HOÁN VỊ'),('06','CHỈNH HỢP'),('07','TỔ HỢP')]):
            x=-5.69+(i%2)*3.59;y=1.21-(i//2)*1.65
            g.add(card(title,x,y,C['cyan'],1.07,.78,27),txt(sub,x+1.00,y,17,C['gold'],True,1.56))
        g.add(bottom('Định nghĩa kết quả trước công thức',C['green']))
        return g,g[1]
    return swap(0)


def visual(b):
    fn={'intro':intro,'ordered':ordered,'unordered':unordered,'swap':swap,
        'choose3':choose3,'choose6':choose6,'captain':captain,'practice':practice}[b.section]
    return fn(b.state)


def formula_img(key):
    p=ROOT/'assets'/'comb04v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Run prepare_comb04_v2.py before Manim: {p}')
    im=ImageMobject(str(p))
    im.scale_to_fit_width(min(im.width,5.50))
    if im.height>.60:im.scale_to_fit_height(.60)
    im.move_to([RX,-1.18,0]);return im


class COMB04(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb04_voice_manifest.json'
        if not manifest.exists():raise RuntimeError('Run python scripts/prepare_comb04_v2.py --voice off/on first')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta.get('beats')!=len(BEATS):raise ValueError('COMB04 lesson manifest is stale')
        self.last=None
        self.add(txt('SANG MATH / ĐẠI SỐ TỔ HỢP',-3.87,3.63,20,C['cyan'],True,6.16))
        self.add(txt('COMB04 / THỨ TỰ',4.43,3.63,19,C['muted'],True,4.70))
        self.add(line(-6.83,3.31,6.83,3.31,C['line'],1.2))
        for x,w in ((LX,6.18),(RX,7.22)):
            box=RoundedRectangle(width=w,height=6.24,corner_radius=.18,
                    stroke_color=C['line'],stroke_width=1.4,
                    fill_color=C['panel'],fill_opacity=1)
            box.move_to([x,-.02,0]);self.add(box)
        self.add(line(-6.83,-3.34,6.83,-3.34,C['line'],1.2))

    def right_content(self,b,index):
        header=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.73,18,C['purple'],True,6.0),
                      txt(b.heading,RX,2.15,25,C['gold'],True,6.04))
        body=VGroup(*[txt(item,RX,1.30-i*.52,21,C['text'],False,5.96)
                      for i,item in enumerate(b.lines)])
        if b.formula:
            formula=formula_img(b.formula)
        else:
            formula=txt('QUAN SÁT → SO SÁNH → KẾT LUẬN',RX,-1.18,18,C['cyan'],True,5.85)
        answer=VGroup(line(.45,-1.72,6.10,-1.72,C['line'],1.2),
                      txt(b.takeaway,RX,-2.36,22,C['green'],True,5.89))
        footer=txt(f'{index+1:02d} / 48',0,-3.69,15,C['muted'])
        return header,body,formula,answer,footer

    def perform(self,index,b):
        clip=self.meta['clips'].get(f'{index:03}',{})
        if clip.get('file'):
            file=ROOT/'voice'/clip['file']
            if not file.is_file():raise FileNotFoundError(file)
            self.add_sound(str(file))
        target=max(b.min_seconds,float(clip.get('duration',0))+.85)
        picture,focus=visual(b)
        header,body,formula,answer,foot=self.right_content(b,index)
        if self.last is None:
            self.play(FadeIn(picture),FadeIn(header),FadeIn(foot),run_time=1.35)
        else:
            oldpicture,oldheader,oldbody,oldformula,oldanswer,oldfoot=self.last
            self.play(FadeOut(oldpicture),FadeIn(picture),FadeOut(oldheader),FadeIn(header),
                      FadeOut(oldbody),FadeOut(oldformula),FadeOut(oldanswer),
                      ReplacementTransform(oldfoot,foot),run_time=1.35)
        if b.section=='swap' and b.state in (1,2):
            self.play(Swap(focus[0],focus[1]),run_time=2.6)
        else:
            self.play(Indicate(focus[0] if isinstance(focus,tuple) else focus,
                               color=C['gold'],scale_factor=1.06),run_time=2.6)
        for t in body:
            self.play(FadeIn(t,shift=.09*UP),run_time=.90)
        self.play(FadeIn(formula),run_time=.86)
        self.play(FadeIn(answer),run_time=.85)
        self.play(Circumscribe(answer[-1],color=C['green'],buff=.08),run_time=1.10)
        spent=1.35+2.6+3*.90+.86+.85+1.10
        if target>spent:self.wait(target-spent)
        self.last=(picture,header,body,formula,answer,foot)

    def construct(self):
        for index,b in enumerate(BEATS):self.perform(index,b)
        self.play(*[FadeOut(obj) for obj in self.last],run_time=1.00)
        g=VGroup(txt('ĐỔI THỨ TỰ CÓ ĐỔI KẾT QUẢ?',0,.34,34,C['cyan'],True,12.5),
                 txt('COMB05 · HOÁN VỊ',0,-.43,26,C['gold'],True,11.5))
        self.play(FadeIn(g),run_time=1.50)
        self.wait(2.70)
