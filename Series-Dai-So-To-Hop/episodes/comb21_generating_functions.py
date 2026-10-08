"""COMB21 - Hàm sinh / Generating functions.

48 visually distinct instructional beats across eight mathematical models.
Render after scripts/prepare_comb21_v2.py has created Typst PNGs and manifest.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb21_lesson_data import BEATS, CHAPTER_LABELS, tiled_sequences, convolve
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.58
RX=3.21

def tx(s,x,y,size=16,color=None,bold=False,limit=None):
    o=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if limit and o.width>limit:o.scale_to_fit_width(limit)
    o.move_to((x,y,0));return o

def cell(s,x,y,width=.74,height=.54,hot=False,gray=False,font=16):
    color=C['gold'] if hot else (C['inactive'] if gray else C['cyan'])
    bg=C['panel_alt'] if not gray else C['panel']
    body=RoundedRectangle(width=width,height=height,corner_radius=.09,fill_color=bg,
        fill_opacity=1,stroke_color=color,stroke_width=1.9)
    body.move_to((x,y,0))
    label=tx(s,x,y,font,color if hot else C['text'],hot,width-.09)
    return VGroup(body,label)

def graph(section,state):
    """A real model for each chapter with logical highlight progression."""
    g=VGroup(); focus=None
    g.add(tx({
        'intro':'HỆ SỐ LÀ SỐ CÁCH ĐẾM',
        'product':'GHÉP HAI NGUỒN LỰA CHỌN',
        'stars':'SÁU SAO - HAI VẠCH',
        'bounds':'RÀNG BUỘC Ở HAI HỘP ĐẦU',
        'recurrence':'LÁT GẠCH 1 VÀ 2 Ô',
        'exponential':'NHÓM CÓ NHÃN VÀ KHÔNG NHÃN',
        'coins':'ĐỔI XU 1, 2, 3 ĐƠN VỊ',
        'capstone':'BA HẠNG TỬ BAO HÀM - LOẠI TRỪ'
    }[section],LX,2.57,14,C['cyan'],True,5.90))

    if section=='intro':
        vals=[1,3,6,10,15,21]
        for k,v in enumerate(vals):
            x=LX+(k-2.5)*.86
            h=.35+v/21*2.50
            bar=RoundedRectangle(width=.55,height=h,corner_radius=.04,
                fill_color=C['gold'] if k==state else C['cyan'],fill_opacity=.9,
                stroke_width=0).move_to((x,-1.1+h/2,0))
            g.add(bar,tx(str(v),x,-1.1+h+.23,14,C['gold'] if k==state else C['text'],True),
                  tx('x'+('⁰' if k==0 else '¹' if k==1 else f'^{k}'),x,-1.55,13,C['muted']))
            if k==state:focus=bar
        g.add(tx('A(x) = 1 + 3x + 6x² + 10x³ + ...',LX,-2.48,16,C['green'],True,5.9))

    elif section=='product':
        A=[0,1,2];B=[0,2]
        g.add(tx('A: 0, 1, 2',LX-1.20,1.97,14,C['cyan'],True),
              tx('B: 0, 2',LX+1.50,1.97,14,C['purple'],True))
        hits=[]
        for i,a in enumerate(A):
            for j,b in enumerate(B):
                x=LX+(j-.5)*1.65
                y=1.05-i*.82
                hot=(a+b==2) if state>=2 else (i+j==state%4)
                c=cell(f'{a}+{b}={a+b}',x,y,width=1.40,height=.58,hot=hot,font=15)
                g.add(c)
                if hot:hits.append(c)
        g.add(tx('TỔNG = 2  ⇢  2 CON ĐƯỜNG',LX,-2.26,16,C['green'],True,5.7))
        focus=hits[-1] if hits else g[3]

    elif section=='stars':
        assignments=[(2,1,3),(0,0,6),(1,4,1),(3,2,1),(5,0,1),(2,2,2)]
        t=assignments[state]
        symbols=['●']*t[0]+['|']+['●']*t[1]+['|']+['●']*t[2]
        for i,ch in enumerate(symbols):
            x=LX+(i-3.5)*.62
            c=cell(ch,x,.95,width=.48,height=.62,hot=(ch=='|'),font=20)
            g.add(c)
            if ch=='|':focus=c
        g.add(tx(f'x₁ = {t[0]}       x₂ = {t[1]}       x₃ = {t[2]}',LX,-.19,17,C['gold'],True,5.8))
        g.add(tx('6 VẬT  +  2 VẠCH  =  8 VỊ TRÍ',LX,-1.30,15,C['text'],False,5.8))
        g.add(tx('CÓ 28 NGHIỆM NGUYÊN KHÔNG ÂM',LX,-2.37,15,C['green'],True,5.85))

    elif section=='bounds':
        assigns=[(0,0,4,4,4),(1,1,4,3,3),(2,2,3,3,2),(2,0,5,3,2),(0,2,4,4,2),(1,2,2,4,3)]
        arr=assigns[state]
        for i,v in enumerate(arr):
            x=LX+(i-2)*1.10
            c=cell(f'{v}',x,.94,width=.78,height=.72,hot=(i<2),font=20)
            g.add(c,tx(f'x{i+1}',x,.17,14,C['muted']))
            if i==min(state%2,1):focus=c
        g.add(tx('GIỚI HẠN:   x₁ ≤ 2    VÀ    x₂ ≤ 2',LX,-.83,16,C['gold'],True,5.75))
        g.add(tx('TỔNG CÁC HỘP = 12',LX,-1.52,16,C['text'],True))
        g.add(tx('1820  −  1430  +  210  =  600',LX,-2.44,15,C['green'],True,5.9))

    elif section=='recurrence':
        tilings=tiled_sequences(5)
        for j,t in enumerate(tilings):
            x0=LX-2.35
            y=1.89-j*.51
            at=0
            for z in t:
                w=.73*z
                bar=RoundedRectangle(width=w-.045,height=.34,corner_radius=.05,
                    fill_color=C['gold'] if j==state%8 else (C['cyan'] if z==1 else C['purple']),
                    fill_opacity=.82,stroke_width=0).move_to((x0+at*.73+w/2,y,0))
                g.add(bar)
                if j==state:focus=bar
                at+=z
            g.add(tx(f'{j+1:02}',LX+2.22,y,12,C['gold'] if j==state else C['muted']))
        g.add(tx('f(5) = 8     •     f(6) = 13',LX,-2.66,16,C['green'],True,5.75))

    elif section=='exponential':
        names=['NHÓM A','NHÓM B','NHÓM C']
        maps=[(0,0,1,2),(0,1,2,0),(0,1,1,2),(2,2,1,0),(0,1,2,2),(1,0,2,1)]
        assignment=maps[state]
        for i,lab in enumerate(names):
            x=LX+(i-1)*1.80
            c=cell(lab,x,1.55,width=1.59,height=.59,hot=(i==state%3),font=14)
            g.add(c)
            for j,student in enumerate('ABCD'):
                if assignment[j]==i:
                    badge=cell(student,x-.47+.38*(sum(assignment[t]==i for t in range(j))%3),.70,
                        width=.31,height=.4,hot=(j==state%4),font=12)
                    g.add(badge)
                    if j==state%4:focus=badge
        g.add(tx('4 HỌC SINH → 3 NHÓM CÓ NHÃN',LX,-.48,15,C['gold'],True,5.8))
        g.add(tx('PHỦ HẾT 3 NHÓM: 36 CÁCH',LX,-1.30,17,C['green'],True,5.75))
        g.add(tx('2 NHÓM VÔ DANH: 7 CÁCH',LX,-2.40,14,C['muted'],True,5.8))

    elif section=='coins':
        opts=[(12,0,0),(9,0,1),(6,0,2),(3,0,3),(0,0,4),(1,1,3)]
        a,b,c=opts[state]
        for j,(label,quantity,color) in enumerate([('GIÁ 1',a,C['cyan']),('GIÁ 2',b,C['purple']),('GIÁ 3',c,C['gold'])]):
            y=1.53-j*1.10
            g.add(tx(label,LX-2.1,y+.13,15,color,True))
            for k in range(min(quantity,12)):
                chip=Circle(radius=.14,stroke_color=color,stroke_width=1.2,fill_color=color,fill_opacity=.65)
                chip.move_to((LX-.95+(k%7)*.38,y-(k//7)*.32,0))
                g.add(chip)
                if j==state%3 and k==0:focus=chip
            g.add(tx(f'× {quantity}',LX+2.15,y+.12,15,C['text'],True))
        g.add(tx('1·x + 2·y + 3·z = 12',LX,-2.42,16,C['green'],True,5.9))

    elif section=='capstone':
        triples=[('KHÔNG CHẶN',1820,C['cyan']),('LOẠI SAI',-1430,C['red']),('HOÀN LẠI',210,C['gold'])]
        for i,(label,value,color) in enumerate(triples):
            x=LX+(i-1)*1.87
            h=.32+abs(value)/1820*2.35
            rec=RoundedRectangle(width=.92,height=h,corner_radius=.06,stroke_width=0,
                fill_color=color,fill_opacity=.87).move_to((x,-.75+h/2,0))
            if i>state//2:rec.set_opacity(.17)
            g.add(rec,tx(label,x,1.94,12,C['muted'],True,1.72),
                  tx(f'{value:+d}',x,-1.28,16,color,True,1.7))
            if i==min(state//2,2):focus=rec
        g.add(tx('1820  −  1430  +  210  =  600',LX,-2.41,16,C['green'],True,5.95))
    if focus is None:focus=g[1]
    return g,focus

def formula_png(key):
    path=ROOT/'assets'/'comb21v2'/f'{key}.png'
    if not path.exists():raise FileNotFoundError('Compile the Typst formula images first: '+str(path))
    o=ImageMobject(str(path))
    if o.width>5.75:o.scale_to_fit_width(5.75)
    if o.height>1.1:o.scale_to_fit_height(1.1)
    o.move_to((RX,-1.30,0))
    return o

class COMB21(Scene):
    def setup(self):
        m=ROOT/'voice'/'comb21_voice_manifest.json'
        if not m.exists():raise FileNotFoundError('Run scripts/prepare_comb21_v2.py before rendering')
        self.meta=json.loads(m.read_text(encoding='utf8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Wrong number of narration beats')
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.61,16,C['cyan'],True,5.9))
        self.add(tx('COMB21  /  HÀM SINH',RX,3.61,15,C['muted'],True,5.9))
        self.add(Line((-6.91,3.31,0),(6.91,3.31,0),stroke_color=C['line'],stroke_width=1))
        for x,width in ((LX,6.24),(RX,6.40)):
            self.add(RoundedRectangle(width=width,height=6.12,corner_radius=.12,
                fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1).move_to((x,0,0)))
        self.old=None

    def beat(self,i,b):
        clip=self.meta['clips'][f'{i:03}']
        seconds=max(b.min_seconds,float(clip.get('duration',0))+.85)
        if clip.get('file'):self.add_sound(str(ROOT/'voice'/clip['file']))
        model,focus=graph(b.section,b.state)
        header=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.76,13,C['purple'],True,5.85),
            tx(b.heading,RX,2.22,19,C['gold'],True,5.82))
        points=VGroup(*[tx('• '+line,RX,1.44-j*.62,15,C['text'],False,5.79)
                        for j,line in enumerate(b.lines)])
        formula=formula_png(b.formula)
        note=VGroup(Line((.22,-1.99,0),(6.36,-1.99,0),color=C['line']),
            tx(b.takeaway,RX,-2.49,14,C['green'],True,5.80))
        num=tx(f'{i+1:02d} / 48',0,-3.58,13,C['muted'],True)
        elapsed=0.0
        if self.old:
            prev=self.old
            self.play(*[FadeOut(x) for x in prev[:5]],ReplacementTransform(prev[5],num),
                      FadeIn(model),FadeIn(header),run_time=1.35)
        else:
            self.play(FadeIn(model),FadeIn(header),FadeIn(num),run_time=1.35)
        elapsed+=1.35
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.04),run_time=1.50);elapsed+=1.5
        for l in points:
            self.play(FadeIn(l,shift=UP*.055),run_time=.95)
            elapsed+=.95
        self.play(FadeIn(formula,shift=UP*.08),run_time=1.25);elapsed+=1.25
        self.play(FadeIn(note),run_time=.60);elapsed+=.60
        if seconds-elapsed>6:
            hold=(seconds-elapsed-1.35)/2
            self.wait(hold);elapsed+=hold
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.02),run_time=1.35);elapsed+=1.35
        if seconds>elapsed:self.wait(seconds-elapsed)
        self.old=(model,header,points,formula,note,num)

    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        if self.old:self.play(*[FadeOut(o) for o in self.old],run_time=1.0)
        self.play(FadeIn(tx('HÀM SINH  —  GENERATING FUNCTIONS',0,.45,25,C['cyan'],True,12)),run_time=1.2)
        self.play(FadeIn(tx('HỆ SỐ  •  PHÉP NHÂN  •  TRUY HỒI  •  HÀM SINH MŨ',0,-.45,17,C['gold'],True,12)),run_time=.8)
        self.wait(2.2)
