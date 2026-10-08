"""SANG MATH COMB13 V2: đếm có điều kiện cấm đứng kề nhau, 48 nhịp.

Render after scripts/prepare_comb13_v2.py:
    manim -ql -r 854,480 --fps 24 episodes/comb13_block_method.py COMB13
"""
from __future__ import annotations
import json, math, sys
import numpy as np
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb13_lesson_data import BEATS,CHAPTER_LABELS
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

def gap_diagram(g,base_names,selected=(),font_size=14):
    """Actual gaps, distinct from people; selected gaps glow cyan."""
    m=len(base_names)
    gap=4.75/max(m,1)
    start=LX-(m-1)*gap/2
    for j,name in enumerate(base_names):
        t=token(name,start+j*gap,.25,C['purple'] if name in ('C','D','E','F') else C['cyan'],w=min(.56,gap*.66),h=.58)
        g.add(t)
    xs=[start-gap/2+j*gap for j in range(m+1)]
    chosen_focus=None
    for i,x in enumerate(xs):
        active=i in selected
        frame=RoundedRectangle(width=min(.46,gap*.58),height=.56,corner_radius=.10,
           stroke_color=C['green'] if active else C['inactive'],stroke_width=2,
           fill_color=C['green'] if active else C['panel_alt'],fill_opacity=.27)
        frame.move_to((x,-.90,0))
        g.add(frame)
        if chosen_focus is None or active:
            chosen_focus=frame
        g.add(text('A' if active else str(i+1),x,-.90,15,C['gold'] if active else C['muted'],True))
    return chosen_focus

def visual_event_venn(g,labels=('AB','CD'),numbers=('144','96','144')):
    l=Circle(radius=1.21,stroke_color=C['cyan'],stroke_width=3,fill_color=C['cyan'],fill_opacity=.10).move_to((LX-.69,0,0))
    r=Circle(radius=1.21,stroke_color=C['purple'],stroke_width=3,fill_color=C['purple'],fill_opacity=.11).move_to((LX+.69,0,0))
    g.add(l,r)
    g.add(text(labels[0],LX-1.30,1.55,15,C['cyan'],True),text(labels[1],LX+1.35,1.55,15,C['purple'],True))
    for xx,n,color in zip([-1.38,0,1.38],numbers,[C['cyan'],C['green'],C['purple']]):
        g.add(text(n,LX+xx,-.08,20,color,True))
    return l

def core_view(section,state):
    g=VGroup(); focus=None; swap=None
    if section=='complement':
        markers(g,'KHÔNG KỀ NHAU - ĐẾM PHẦN BÙ','TỔNG - VI PHẠM = HỢP LỆ')
        row,t=people_row(list('ABCDE'),y=.79)
        g.add(row)
        focus=highlight(g,t,(0,1),C['red'],'cặp AB bị cấm')
        if state>=2:
            tiles(g,[('[AB]',C['red']),'C','D','E'],y=-.99)
        if state>=3:g.add(text('120 - 48 = 72',LX,-1.97,24,C['green'],True,5.1))
        if state==4:g.add(text('KIỂM: 72 HÀNG HỢP LỆ',LX,-2.35,15,C['gold'],True,5.45))
        if state==1:swap=(t[1],t[2])
    elif section=='gaps':
        markers(g,'TẠO CÁC KHOẢNG AN TOÀN','CHỌN KHOẢNG TRƯỚC, HOÁN VỊ SAU')
        focus=gap_diagram(g,['C','D','E'],selected=() if state<=1 else (0,2) if state<=3 else (1,3))
        if state>=2:tiles(g,[('A',C['green']),('B',C['gold'])],y=-1.89,gap=1.35)
        if state>=3:g.add(text('3! × 6 × 2! = 72',LX,-2.40,19,C['green'],True,5.0))
    elif section=='positions':
        markers(g,'CHỌN VỊ TRÍ KHÔNG LIỀN','CHỮ GIỐNG NHAU: KHÔNG HOÁN VỊ LẠI')
        focus=gap_diagram(g,list('BBBBB'),selected=(0,2,4,5) if state>=2 else ())
        if state>=2:g.add(text('6 KHOẢNG → CHỌN 4 KHOẢNG',LX,-1.92,17,C['gold'],True,5.2))
        if state>=4:g.add(text('CHỌN 4 TRONG 6 = 15',LX,-2.40,18,C['green'],True,5.1))
    elif section=='disjoint':
        markers(g,'CẤM AB VÀ CẤM CD','TRỪ HAI TẬP VI PHẠM, CỘNG LẠI GIAO')
        focus=visual_event_venn(g,('AB kề','CD kề'),('144','96','144'))
        if state>=3:g.add(text('720 - 240 - 240 + 96 = 336',LX,-2.39,18,C['green'],True,5.5))
    elif section=='overlap':
        markers(g,'HAI CẶP CẤM CHUNG NGƯỜI B','GIAO: CHỈ ABC HOẶC CBA')
        row,t=people_row(list('ABCDEF'),y=.69);g.add(row)
        focus=highlight(g,t,(0,1),C['red'],'AB');highlight(g,t,(1,2),C['purple'],'BC')
        tiles(g,[('[ABC]',C['green']),'D','E','F'],y=-.89)
        if state>=2:g.add(text('ABC hoặc CBA  →  2 × 4! = 48',LX,-1.90,16,C['gold'],True,5.5))
        if state>=3:g.add(text('720 - 240 - 240 + 48 = 288',LX,-2.39,17,C['green'],True,5.5))
        if state==5:swap=(t[0],t[2])
    elif section=='boys':
        markers(g,'NĂM NAM - BA NỮ KHÔNG KỀ','CÓ 6 KHOẢNG TRÊN HÀNG NAM')
        focus=gap_diagram(g,list('MMMMM'),selected=(0,2,4) if state>=2 else ())
        if state>=3:g.add(text('5! × 20 × 3! = 14400',LX,-2.25,17,C['green'],True,5.49))
    elif section=='circle':
        markers(g,'KHÔNG KỀ QUANH BÀN TRÒN','VÒNG CÓ m KHOẢNG, KHÁC HÀNG CÓ m+1')
        t=circular_layout(g,list('ABCDEF'))
        focus=SurroundingRectangle(VGroup(t[0],t[1]),buff=.12,stroke_width=2.5,color=C['red']);g.add(focus)
        if state>=2:g.add(text('5! - 2 × 4! = 72',LX,-2.39,19,C['green'],True,5.5))
        if state>=4:g.add(text('4 NAM + 3 NỮ → 144',LX,-2.06,17,C['gold'],True,5.5))
    else:
        markers(g,'BA CẶP ĐỀU CẤM ĐỨNG KỀ','BAO HÀM–LOẠI TRỪ ĐẾN GIAO BA')
        row,t=people_row(list('ABCDEFGH'),y=.85,gap=.68);g.add(row)
        focus=highlight(g,t,(0,1),C['red'],'AB')
        if state>=2:highlight(g,t,(2,3),C['purple'],'CD')
        if state>=3:highlight(g,t,(4,5),C['gold'],'EF')
        if state>=4:g.add(text('40320 - 30240 + 8640 - 960',LX,-1.91,16,C['gold'],True,5.52))
        if state>=4:g.add(text('17760 HÀNG HỢP LỆ',LX,-2.41,19,C['green'],True,5.52))
    return g,focus,swap

def formula_image(key):
    path=ROOT/'assets'/'comb13v2'/f'{key}.png'
    if not path.exists():
        raise FileNotFoundError(f'Build Typst first: python scripts/prepare_comb13_v2.py --voice off: {path}')
    o=ImageMobject(str(path))
    o.scale_to_fit_width(min(o.width,5.62))
    if o.height>.82:o.scale_to_fit_height(.82)
    o.move_to((RX,-1.09,0))
    return o

class COMB13(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb13_voice_manifest.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_comb13_v2.py')
        self.manifest=json.loads(path.read_text(encoding='utf8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Incorrect COMB13 audio manifest')
        self.last=None
        self.add(text('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.65,3.63,19,C['cyan'],True,6.0))
        self.add(text('COMB13  /  PHƯƠNG PHÁP GỘP KHỐI',3.65,3.63,17,C['muted'],True,5.48))
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
        ending=VGroup(text('COMB13 · PHƯƠNG PHÁP GỘP KHỐI',0,.48,28,C['cyan'],True,11.6),
                      text('HIỂU KHỐI · KHÔNG ĐẾM TRÙNG · VẬN DỤNG CAO',0,-.40,20,C['gold'],True,12.0))
        self.play(FadeIn(ending),run_time=1.2)
        self.wait(3.0)
