"""SANG MATH COMB12 V2: gộp khối trong hoán vị, 48 nhịp đồng bộ lời giảng.

Render after scripts/prepare_comb12_v2.py:
    manim -ql -r 854,480 --fps 24 episodes/comb12_block_method.py COMB12
"""
from __future__ import annotations
import json, math, sys
import numpy as np
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb12_lesson_data import BEATS,CHAPTER_LABELS
from series_config import PALETTE as C

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8.0
FONT='Noto Sans'
LX,RX=-3.68,3.12

def text(s,x,y,size=17,color=None,bold=False,maxw=None):
    t=Text(str(s),font=FONT,font_size=size,color=color or C['text'],
           weight='BOLD' if bold else 'NORMAL')
    if maxw is not None and t.width>maxw:t.scale_to_fit_width(maxw)
    t.move_to((x,y,0))
    return t

def token(s,x,y,color=None,w=.69,h=.66):
    frame=RoundedRectangle(width=w,height=h,corner_radius=.11,
        stroke_width=1.8,stroke_color=color or C['cyan'],
        fill_color=C['panel_alt'],fill_opacity=1)
    frame.move_to((x,y,0))
    label=text(s,x,y,18,C['text'],True,w-.06)
    return VGroup(frame,label)

def people_row(names,y=.63,x=LX,gap=.83):
    n=len(names)
    xs=[x+(i-(n-1)/2)*gap for i in range(n)]
    tokens=[];group=VGroup()
    for name,px in zip(names,xs):
        color=C['gold'] if name=='A' else C['purple'] if name=='B' else C['cyan']
        p=token(name,px,y,color)
        tokens.append(p);group.add(p)
    return group,tokens

def highlight(g,tokens,inds,color=None,label=None,below=.0):
    chosen=VGroup(*[tokens[j] for j in inds])
    box=SurroundingRectangle(chosen,color=color or C['green'],stroke_width=2.7,
                             buff=.10,corner_radius=.15)
    g.add(box)
    if label:
        g.add(text(label,box.get_center()[0],box.get_bottom()[1]-.35-below,
                   14,color or C['green'],True,2.15))
    return box

def tiles(g,items,y=-.97,gap=.91):
    n=len(items);width=min(1.25,4.85/n)
    for i,item in enumerate(items):
        if isinstance(item,tuple):name,col=item
        else:name,col=item,C['cyan']
        g.add(token(name,LX+(i-(n-1)/2)*gap,y,col,w=width,h=.65))

def markers(g,title,subtitle):
    g.add(text(title,LX,2.55,16,C['cyan'],True,5.55))
    g.add(text(subtitle,LX,-2.56,15,C['gold'],True,5.54))

def two_events(g,mode='union'):
    g.add(text('HAI BIẾN CỐ ĐỨNG KỀ',LX,2.45,16,C['cyan'],True,5.4))
    c1=Circle(radius=1.26,stroke_color=C['cyan'],stroke_width=3,
              fill_color=C['cyan'],fill_opacity=.12).move_to((LX-.74,-.01,0))
    c2=Circle(radius=1.26,stroke_color=C['purple'],stroke_width=3,
              fill_color=C['purple'],fill_opacity=.12).move_to((LX+.74,-.01,0))
    g.add(c1,c2)
    g.add(text('AB kề',LX-1.4,1.61,14,C['cyan'],True,2.2))
    g.add(text('CD kề',LX+1.4,1.61,14,C['purple'],True,2.2))
    if mode=='union':
        g.add(text('144',LX-1.32,-.06,20,C['cyan'],True),
              text('96',LX,-.06,20,C['green'],True),
              text('144',LX+1.32,-.06,20,C['purple'],True))
        g.add(text('PHẦN HỢP: 384',LX,-2.53,15,C['gold'],True,5.55))
    else:
        g.add(text('AB chỉ',LX-1.38,.06,15,C['cyan'],True,2.05),
              text('96',LX,-.06,20,C['red'],True),
              text('CD chỉ',LX+1.38,.06,15,C['purple'],True,2.05))
        g.add(text('CHỈ MỘT CẶP: 288',LX,-2.53,15,C['gold'],True,5.55))
    return c1

def circular_layout(g,names):
    center=np.array([LX,.05,0]);radius=1.64
    disk=Circle(radius=radius+.31,stroke_color=C['line'],stroke_width=2,
           fill_color=C['panel_alt'],fill_opacity=.40).move_to(center)
    g.add(disk)
    tokens=[]
    for i,name in enumerate(names):
        ang=math.pi/2-i*2*math.pi/len(names)
        xy=center+radius*np.array([math.cos(ang),math.sin(ang),0])
        t=token(name,float(xy[0]),float(xy[1]),C['gold'] if name=='A' else C['purple'] if name=='B' else C['cyan'],.59,.59)
        tokens.append(t);g.add(t)
    return tokens

def core_view(section,state):
    """Return a visual model specific to each counting argument, not a static title slide."""
    g=VGroup();focus=None;swap=None
    if section=='pair':
        markers(g,'MÔ HÌNH: A, B PHẢI ĐỨNG CẠNH','KHỐI AB → 4 VẬT × 2 THỨ TỰ')
        row,t=people_row(list('ABCDE'))
        g.add(row);focus=highlight(g,t,(0,1),label='cặp AB')
        if state>=2:tiles(g,[('[AB]',C['green']),'C','D','E'])
        else:tiles(g,['A','B','C','D','E'])
        if state in (1,3):swap=(t[0],t[1])
        if state>=3:g.add(text('4! × 2! = 48',LX,-1.91,21,C['green'],True,5.48))
        if state==5:g.add(text('TỔNG QUÁT  n NGƯỜI',LX,-2.07,14,C['purple'],True,5.5))
    elif section=='triple':
        markers(g,'MÔ HÌNH: BA NGƯỜI LIỀN NHAU','3! THỨ TỰ TRONG KHỐI × 4! THỨ TỰ NGOÀI')
        row,t=people_row(list('ABCDEF'),y=.65)
        g.add(row);focus=highlight(g,t,(0,1,2),label='khối 3 người')
        tiles(g,[('[ABC]',C['green']),'D','E','F'])
        if state>=2:g.add(text('ABC · ACB · BAC · BCA · CAB · CBA',LX,-1.87,14,C['gold'],True,5.55))
        if state==2:swap=(t[0],t[1])
        if state==4:g.add(text('CỐ ĐỊNH ABC → 24 CÁCH',LX,-2.21,13,C['green'],True,5.4))
    elif section=='double':
        markers(g,'HAI KHỐI KHÁC NHAU KHÔNG GIAO','KHỐI [AB] VÀ [CD] KHÔNG ĐƯỢC TÁCH')
        row,t=people_row(list('ABCDEF'),y=.66)
        g.add(row);focus=highlight(g,t,(0,1),C['green'],'khối 1')
        if state>=1:highlight(g,t,(2,3),C['purple'],'khối 2')
        tiles(g,[('[AB]',C['green']),('[CD]',C['purple']),'E','F'])
        if state>=2:g.add(text('4! × 2 × 2 = 96',LX,-1.93,20,C['gold'],True,5.5))
        if state==4:g.add(text('3 KHỐI → 3! × 2³ = 48',LX,-2.17,14,C['green'],True,5.5))
    elif section=='overlap':
        markers(g,'ĐIỀU KIỆN CHỒNG LẤN','KHÔNG ĐƯỢC DÙNG B HAI LẦN')
        row,t=people_row(list('ABCDEF'),y=.66)
        g.add(row)
        focus=highlight(g,t,(0,1),C['cyan'],'AB')
        if state!=4:highlight(g,t,(1,2),C['purple'],'BC')
        tiles(g,[('A',C['green']),('B',C['gold']),('C',C['purple']),'D','E','F'],y=-.87)
        if state>=1:g.add(text('ABC hoặc CBA' if state<4 else 'BA CẠNH CA CÙNG LÚC? KHÔNG',LX,-1.88,15,C['green'] if state<4 else C['red'],True,5.55))
        if state==2:swap=(t[0],t[2])
        if state==4:g.add(text('AB + BC + AC ĐỀU KỀ → 0',LX,-2.13,14,C['red'],True,5.5))
    elif section in ('union','exact'):
        focus=two_events(g,'union' if section=='union' else 'exact')
        if state>=2:
            extra='HAI KHỐI [AB] [CD] → 96' if section=='union' else 'MỖI BÊN RIÊNG → 144'
            g.add(text(extra,LX,-1.92,15,C['gold'],True,5.55))
        if state==4:g.add(text('KIỂM TRA: 384 + 336 = 720' if section=='union' else 'ĐÚNG MỘT CẶP ≠ ÍT NHẤT MỘT',LX,-2.23,13,C['green'],True,5.54))
    elif section=='circle':
        markers(g,'GỘP KHỐI TRÊN VÒNG TRÒN','SAU GỘP, XẾP VÒNG = (m − 1)!')
        names=list('ABCDEF')
        t=circular_layout(g,names)
        focus=SurroundingRectangle(VGroup(t[0],t[1]),color=C['green'],buff=.08,stroke_width=2.2)
        g.add(focus)
        if state>=3:g.add(text('2 KHỐI: 4 VẬT → 3! × 2²',LX,-2.17,14,C['gold'],True,5.55))
        elif state>=2:g.add(text('1 KHỐI: 5 VẬT → 4! × 2',LX,-2.17,14,C['green'],True,5.55))
    else:
        markers(g,'BÀI TOÁN: BA CẶP ĐỀU CẤM KỀ','7! − 3 × 2 · 6! + 3 × 2² · 5! − 2³ · 4!')
        row,t=people_row(list('ABCDEFG'),y=.82,gap=.77)
        g.add(row)
        focus=highlight(g,t,(0,1),C['red'])
        if state>=2:highlight(g,t,(2,3),C['purple'])
        if state>=3:highlight(g,t,(4,5),C['gold'])
        if state>=1:tiles(g,[('[AB]',C['red']),('[CD]',C['purple']),('[EF]',C['gold']),'G'],y=-.90,gap=1.10)
        if state==4:g.add(text('1968 HÀNG HỢP LỆ',LX,-1.86,22,C['green'],True,5.5))
        if state==5:g.add(text('LIỆT KÊ ĐỦ 5040 HÀNG ĐỂ ĐỐI CHIẾU',LX,-2.08,13,C['green'],True,5.50))
    return g,focus,swap

def formula_image(key):
    path=ROOT/'assets'/'comb12v2'/f'{key}.png'
    if not path.exists():
        raise FileNotFoundError(f'Build Typst first: python scripts/prepare_comb12_v2.py --voice off: {path}')
    o=ImageMobject(str(path))
    o.scale_to_fit_width(min(o.width,5.62))
    if o.height>.82:o.scale_to_fit_height(.82)
    o.move_to((RX,-1.09,0))
    return o

class COMB12(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb12_voice_manifest.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_comb12_v2.py')
        self.manifest=json.loads(path.read_text(encoding='utf8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Incorrect COMB12 audio manifest')
        self.last=None
        self.add(text('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.65,3.63,19,C['cyan'],True,6.0))
        self.add(text('COMB12  /  PHƯƠNG PHÁP GỘP KHỐI',3.65,3.63,17,C['muted'],True,5.48))
        self.add(Line((-6.85,3.32,0),(6.85,3.32,0),color=C['line'],stroke_width=1.1))
        for x,w in ((LX,6.18),(RX,6.46)):
            frame=RoundedRectangle(width=w,height=6.16,corner_radius=.17,
                      stroke_width=1.3,stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1)
            frame.move_to((x,0,0));self.add(frame)
        self.add(Line((-6.85,-3.32,0),(6.85,-3.32,0),color=C['line'],stroke_width=1.1))

    def right(self,b,i):
        headings=VGroup(text(CHAPTER_LABELS[b.section],RX,2.67,15,C['purple'],True,5.78),
            text(b.heading,RX,2.05,20,C['gold'],True,5.76))
        lines=VGroup(*[text('• '+ln,RX,1.24-j*.62,17,C['text'],False,5.79)
                for j,ln in enumerate(b.lines)])
        formula=formula_image(b.formula)
        words=b.takeaway.split()
        subtitle_lines=[]; current=[]
        for word in words:
            if len(' '.join(current+[word]))>34 and current:
                subtitle_lines.append(' '.join(current));current=[word]
            else:
                current.append(word)
        if current:subtitle_lines.append(' '.join(current))
        if len(subtitle_lines)>2:
            subtitle_lines=[subtitle_lines[0], ' '.join(subtitle_lines[1:])]
        ypos=[-2.36] if len(subtitle_lines)==1 else [-2.19,-2.53]
        bottom=VGroup(Line((.22,-1.75,0),(6.2,-1.75,0),color=C['line'],stroke_width=1.05))
        for ln,y in zip(subtitle_lines,ypos):
            bottom.add(text(ln,RX,y,15,C['green'],True,5.69))
        counter=text(f'{i+1:02d} / 48',0,-3.68,15,C['muted'],True)
        return headings,lines,formula,bottom,counter

    def show_beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            path=ROOT/'voice'/clip['file']
            if not path.is_file():raise FileNotFoundError(path)
            self.add_sound(str(path))
        duration=max(float(b.min_seconds),float(clip.get('duration',0))+.85)
        art,focus,swap=core_view(b.section,b.state)
        head,lines,formula,bottom,counter=self.right(b,i)
        if self.last is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(counter),run_time=.93)
            entering=.93
        else:
            old_art,old_head,old_lines,old_formula,old_bottom,old_counter=self.last
            self.play(FadeOut(old_art),FadeIn(art),FadeOut(old_head),FadeIn(head),
                    FadeOut(old_lines),FadeOut(old_formula),FadeOut(old_bottom),
                    ReplacementTransform(old_counter,counter),run_time=1.08)
            entering=1.08
        special=0.0
        if swap:
            self.play(Swap(*swap,path_arc=.6),run_time=1.6)
            special=1.6
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.04),run_time=1.2)
        for ln in lines:self.play(FadeIn(ln,shift=.08*UP),run_time=1.04)
        self.play(FadeIn(formula,shift=.06*UP),run_time=1.20)
        self.play(FadeIn(bottom),run_time=.88)
        self.play(Circumscribe(bottom[-1],color=C['green'],buff=.08),run_time=1.0)
        spent=entering+special+1.2+3*1.04+1.20+.88+1.0
        if duration>spent:self.wait(duration-spent)
        self.last=(art,head,lines,formula,bottom,counter)

    def construct(self):
        for i,beat in enumerate(BEATS):self.show_beat(i,beat)
        self.play(*[FadeOut(o) for o in self.last],run_time=1.)
        ending=VGroup(text('COMB12 · PHƯƠNG PHÁP GỘP KHỐI',0,.48,28,C['cyan'],True,11.6),
                      text('HIỂU KHỐI · KHÔNG ĐẾM TRÙNG · VẬN DỤNG CAO',0,-.40,20,C['gold'],True,12.0))
        self.play(FadeIn(ending),run_time=1.2)
        self.wait(3.0)
