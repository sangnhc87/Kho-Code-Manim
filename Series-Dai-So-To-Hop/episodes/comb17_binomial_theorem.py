"""COMB17: Deriving the binomial theorem by counting choices.

Render: python scripts/prepare_comb17_v2.py --voice off
        manim -ql -r 854,480 --fps 24 episodes/comb17_binomial_theorem.py COMB17
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb17_lesson_data import BEATS,CHAPTER_LABELS
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.66;RX=3.19


def tx(s,x,y,size=17,color=None,bold=False,width=None):
    obj=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if width and obj.width>width:obj.scale_to_fit_width(width)
    obj.move_to((x,y,0))
    return obj


def tile(text,x,y,color,width=.55,height=.50,fontsize=17,fill=None):
    box=RoundedRectangle(width=width,height=height,corner_radius=.09,
        stroke_color=color,stroke_width=2,fill_color=fill or C['panel_alt'],fill_opacity=.97)
    box.move_to((x,y,0))
    obj=tx(text,x,y,fontsize,C['text'],True,max(width-.13,.28))
    return VGroup(box,obj)


def term_row(group,n,positions,y,title,colors=None):
    width=min(.70,4.70/max(n,1))
    xs=[LX+(i-(n-1)/2)*width*1.22 for i in range(n)]
    for i,x in enumerate(xs):
        chosen=(i in positions)
        color=C['gold'] if chosen else C['cyan']
        if colors:color=colors[i]
        group.add(tile('b' if chosen else 'a',x,y,color,width*.93,.57,18))
    group.add(tx(title,LX,y+.64,15,C['muted'],True,5.80))
    return group


def count_bars(group,counts,current,title,values=None):
    hmax=max(counts)
    group.add(tx(title,LX,2.52,15,C['cyan'],True,5.70))
    for k,val in enumerate(counts):
        x=LX+(k-(len(counts)-1)/2)*(.89 if len(counts)==6 else 1.05)
        height=.25+1.53*(val/hmax)
        r=RoundedRectangle(width=.62,height=height,corner_radius=.09,
            fill_color=C['gold'] if k==current else C['purple'],fill_opacity=.85,
            stroke_color=C['gold'] if k==current else C['line'],stroke_width=1.3)
        r.move_to((x,.45-height/2,0));group.add(r)
        group.add(tx(str(values[k] if values is not None else val),x,.58,16,C['text'],True,.74))
        group.add(tx(f'k={k}',x,-1.39,14,C['muted'],False,.78))
    return group


def two_factor_model(g,state):
    g.add(tx('HAI NHAN TU  /  BON DUONG CHON',LX,2.60,15,C['cyan'],True,5.8))
    for col,x in enumerate([LX-1.17,LX+1.17]):
        g.add(tx(f'NHAN TU {col+1}',x,1.65,14,C['muted'],True,2.2))
        g.add(tile('a',x,1.01,C['cyan'],.76,.63,21))
        g.add(tile('b',x,.12,C['gold'],.76,.63,21))
    paths=['aa','ab','ba','bb']
    for i,path in enumerate(paths):
        x=LX+(i-1.5)*1.31
        color=C['gold'] if (i==state%4 or state>=2 and i in (1,2)) else C['cyan']
        g.add(tile(path.upper(),x,-1.37,color,1.08,.64,18))
        if i==1 or i==2:
            g.add(tx('ab',x,-1.94,13,C['purple'],False,1.1))
    return g[0]


def cube_model(g,state):
    g.add(tx('BA NHAN TU  /  TAM DUONG CHON',LX,2.56,15,C['cyan'],True,5.8))
    paths=[''.join(t) for t in itertools.product('ab',repeat=3)]
    for i,p in enumerate(paths):
        col=i%4;row=i//4
        x=LX+(col-1.5)*1.35;y=1.10-row*.91
        n=p.count('b');sel=(n==max(0,min(3,state-2))) if state in (2,3,4) else i==state%8
        color=C['gold'] if sel else [C['cyan'],C['purple'],C['green'],C['red']][n]
        g.add(tile(p.upper(),x,y,color,1.03,.56,17))
        g.add(tx(f'{n} b',x,y-.42,12,C['muted']))
    g.add(tx('NHOM THEO SO LAN CHON b',LX,-1.65,16,C['gold'],True,5.8))
    return g[-1]


def four_model(g,state):
    g.add(tx('BON NHAN TU  /  16 DUONG CHON',LX,2.52,15,C['cyan'],True,5.80))
    paths=[''.join(t) for t in itertools.product('ab',repeat=4)]
    for i,path in enumerate(paths):
        col=i%4;row=i//4
        x=LX+(col-1.5)*1.28;y=1.55-row*.68
        count=path.count('b')
        color=C['gold'] if count==min(state,4) else C['cyan'] if count%2==0 else C['purple']
        g.add(tile(path.upper(),x,y,color,1.02,.49,14))
    g.add(tx('HE SO 1  -  4  -  6  -  4  -  1',LX,-1.47,16,C['gold'],True,5.75))
    return g[-1]


def theorem_model(g,state):
    n=5;k=min(state,5)
    g.add(tx('MOT VI TRI = MOT LUA CHON',LX,2.58,15,C['cyan'],True,5.8))
    slots={0:(),1:(1,),2:(1,3),3:(0,2,4),4:(0,1,3,4),5:(0,1,2,3,4)}[state]
    focus=term_row(g,n,slots,.94,'VI DU MINH HOA: n = 5')
    g.add(tx(f'CHON {k} NGOAC LAY b',LX,-.10,18,C['gold'],True,5.7))
    count_bars(g,[1,5,10,10,5,1],k,' ')
    return focus[1]


def coefficient_model(g,section,state):
    if section=='choose':
        counts=[1,5,10,10,5,1];k=min(state,5)
        return count_bars(g,counts,k,'HE SO CUA (1+x)^5')[-1]
    if section=='sign':
        vals=[1,-10,40,-80,80,-32]
        n=5
        g.add(tx('THAY b = -2  /  XET DAU',LX,2.55,15,C['cyan'],True,5.8))
        for i in range(n):
            x=LX+(i-2)*1.13
            chosen=i<min(state,5)
            g.add(tile('-2' if chosen else 'x',x,.8,C['red'] if chosen else C['cyan'],.85,.71,19))
        for i,v in enumerate(vals):
            x=LX+(i-2.5)*.91
            color=C['gold'] if i==state else C['red'] if v<0 else C['green']
            g.add(tx(str(v),x,-.54,17,color,True,.85))
            g.add(tx('k='+str(i),x,-1.05,12,C['muted']))
        g.add(tx('DAU CUA HANG DO SO LAN CHON -2',LX,-1.79,14,C['gold'],True,5.9))
        return g[-1]
    if section=='coeff':
        g.add(tx('CHON 2x TU SAU NGOAC',LX,2.53,15,C['cyan'],True,5.8))
        selections=[(0,1,2),(0,2,4),(1,3,5),(0,3,5),(0,2),(1,4)][state]
        for i in range(6):
            x=LX+(i-2.5)*.92
            c=C['gold'] if i in selections else C['purple']
            g.add(tile('2x' if i in selections else '-1',x,.87,c,.73,.67,15))
        g.add(tx('SO LAN CHON 2x = '+str(len(selections)),LX,-.47,17,C['gold'],True,5.65))
        g.add(tx('CACH CHON VI TRI  ×  GIA TRI TICH',LX,-1.46,14,C['cyan'],True,5.8))
        return g[-1]
    # final capstone: four independent cases i=0,1,2,3
    g.add(tx('BANG CHIA TRUONG HOP  /  TICH HAI NHI THUC',LX,2.51,14,C['cyan'],True,5.85))
    vals=[8,48,36,4]
    g.add(tx('(1+x)^4     ×     (1+2x)^3',LX,1.77,17,C['text'],True,5.8))
    for i,v in enumerate(vals):
        y=.98-i*.74
        highlighted=(i==state%4 or state>=4)
        color=C['gold'] if highlighted else C['purple']
        g.add(tile('i = '+str(i),LX-1.6,y,color,1.40,.57,15))
        g.add(tx('x^'+str(i)+'  ×  x^'+str(3-i),LX-.08,y,14,C['muted'],False,2.20))
        g.add(tx(str(v),LX+2.14,y,18,C['gold'] if highlighted else C['cyan'],True,1.0))
    return g[-1]


def model(section,state):
    g=VGroup()
    if section=='binary':focus=two_factor_model(g,state)
    elif section=='cube':focus=cube_model(g,state)
    elif section=='four':focus=four_model(g,state)
    elif section=='theorem':focus=theorem_model(g,state)
    else:focus=coefficient_model(g,section,state)
    return g,focus


def formula_image(key):
    path=ROOT/'assets'/'comb17v2'/f'{key}.png'
    if not path.is_file():
        raise FileNotFoundError(f'Run scripts/prepare_comb17_v2.py first: {path}')
    im=ImageMobject(str(path))
    if im.width>5.77:im.scale_to_fit_width(5.77)
    if im.height>.99:im.scale_to_fit_height(.99)
    im.move_to((RX,-1.07,0))
    return im


def takeaway_lines(s,max_chars=42):
    out=[];line=[]
    for word in s.split():
        if line and len(' '.join(line+[word]))>max_chars:
            out.append(' '.join(line));line=[]
        line.append(word)
    if line:out.append(' '.join(line))
    if len(out)>2:out=[out[0],' '.join(out[1:])]
    return out


class COMB17(Scene):
    def setup(self):
        mf=ROOT/'voice'/'comb17_voice_manifest.json'
        if not mf.is_file():raise FileNotFoundError('First run: python scripts/prepare_comb17_v2.py --voice off')
        self.mf=json.loads(mf.read_text(encoding='utf8'))
        if self.mf['beats']!=len(BEATS):raise ValueError('Wrong narration manifest')
        self.current=None
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.62,3.62,18,C['cyan'],True,6.0))
        self.add(tx('COMB17  /  NHỊ THỨC NEWTON',3.19,3.62,18,C['muted'],True,6.0))
        self.add(Line((-6.86,3.32,0),(6.86,3.32,0),color=C['line'],stroke_width=1.2))
        for x,w in ((LX,6.19),(RX,6.48)):
            self.add(RoundedRectangle(width=w,height=6.17,corner_radius=.14,
                stroke_color=C['line'],stroke_width=1.2,
                fill_color=C['panel'],fill_opacity=1).move_to((x,0,0)))
        self.add(Line((-6.85,-3.32,0),(6.85,-3.32,0),color=C['line'],stroke_width=1.15))

    def right_panel(self,b,index):
        title=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.65,14,C['purple'],True,5.79),
                     tx(b.heading,RX,2.09,19,C['gold'],True,5.79))
        # Each bullet is separate, revealed only after narration has begun.
        bullets=VGroup(*[tx('• '+line,RX,1.31-j*.63,16,C['text'],False,5.72) for j,line in enumerate(b.lines)])
        formula=formula_image(b.formula)
        takeaway=VGroup(Line((.18,-1.77,0),(6.23,-1.77,0),color=C['line'],stroke_width=1.1))
        for j,line in enumerate(takeaway_lines(b.takeaway)):
            takeaway.add(tx(line,RX,-2.14-j*.39,14,C['green'],True,5.66))
        number=tx(f'{index+1:02d} / {len(BEATS)}',0,-3.66,15,C['muted'],True)
        return title,bullets,formula,takeaway,number

    def show(self,i,b):
        clip=self.mf['clips'][f'{i:03}']
        if clip.get('file'):
            sound=ROOT/'voice'/clip['file']
            if not sound.exists():raise FileNotFoundError(sound)
            self.add_sound(str(sound))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.85)
        art,focus=model(b.section,b.state)
        head,bullets,formula,summary,number=self.right_panel(b,i)
        if self.current is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(number),run_time=1.1);elapsed=1.1
        else:
            oa,oh,ob,of,os,on=self.current
            self.play(FadeOut(oa),FadeOut(oh),FadeOut(ob),FadeOut(of),FadeOut(os),
                      FadeIn(art),FadeIn(head),ReplacementTransform(on,number),run_time=1.15)
            elapsed=1.15
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.02),run_time=1.3);elapsed+=1.3
        for line in bullets:
            self.play(FadeIn(line,shift=UP*.08),run_time=1.18);elapsed+=1.18
        self.play(FadeIn(formula,shift=UP*.09),run_time=1.35);elapsed+=1.35
        self.play(FadeIn(summary),run_time=1.08);elapsed+=1.08
        if len(summary)>1:
            self.play(Circumscribe(summary[-1],color=C['green'],buff=.06),run_time=.95);elapsed+=.95
        if elapsed<duration:self.wait(duration-elapsed)
        self.current=(art,head,bullets,formula,summary,number)

    def construct(self):
        for index,b in enumerate(BEATS):self.show(index,b)
        if self.current:self.play(*[FadeOut(o) for o in self.current],run_time=1.0)
        end=VGroup(tx('NHỊ THỨC NEWTON  ·  TỪ PHÉP CHỌN',0,.63,28,C['cyan'],True,12),
                   tx('HIỂU HỆ SỐ  →  BIẾT VẬN DỤNG',0,-.48,22,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.2);self.wait(3.0)
