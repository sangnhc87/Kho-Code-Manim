"""COMB19 - Subsets and 2^n: an 8-chapter Manim--Typst lesson."""
from __future__ import annotations
import json, sys
from pathlib import Path
from itertools import combinations
from math import comb
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb19_lesson_data import (BEATS,CHAPTER_LABELS,subset_masks,size_counts,nonadjacent_subsets,
    nonadjacent_count,endpoint_breakdown)
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.68
RX=3.16

def tx(string,x,y,size=17,color=None,bold=False,limit=None):
    o=Text(str(string),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if limit and o.width>limit:o.scale_to_fit_width(limit)
    o.move_to((x,y,0))
    return o

def tile(string,x,y,color=None,w=.65,h=.51,on=True):
    border=color or C['cyan']
    box=RoundedRectangle(width=w,height=h,corner_radius=.09,
        stroke_color=border,stroke_width=2 if on else .9,
        fill_color=C['panel_alt'] if on else C['panel'],fill_opacity=.97).move_to((x,y,0))
    t=tx(string,x,y,15,C['text'] if on else C['muted'],True,w-.07)
    return VGroup(box,t)

def chipline(mask,n=5,y=1.55,dx=.9):
    g=VGroup();hot=None
    for j in range(n):
        x=LX+(j-(n-1)/2)*dx
        on=(j in mask)
        o=tile(chr(65+j) if n<=5 else str(j+1),x,y,
            C['gold'] if on else C['muted'],.68,.66,on)
        g.add(o)
        if on:hot=o
    return g,hot or g[0]

def format_set(s):
    if not s:return '∅'
    return '{'+','.join(chr(65+i) for i in s)+'}'

def explore(st):
    g=VGroup()
    masks=subset_masks(3)
    masks=sorted(masks,key=lambda m:(len(m),m))
    main=[(),(),(0,),(0,1),(0,1,2),(0,1,2)][st]
    row,focus=chipline(main,3,2.23,1.03)
    g.add(row)
    maxsize=max(0,min(st-1,3)) if st<5 else 3
    seen=0
    visible=[s for s in masks if len(s)<=maxsize]
    for i,s in enumerate(visible):
        highlight=(len(s)==st-1 and st in (2,3,4)) or (st==5)
        x=LX+((i%4)-1.5)*1.33; y=.93-(i//4)*.94
        obj=tile(format_set(s),x,y,C['gold'] if highlight else C['cyan'],1.21,.58,highlight)
        g.add(obj)
        if highlight:focus=obj
    g.add(tx('TẤT CẢ 8 TẬP CON (KỂ CẢ ∅)',LX,-2.30,15,C['green'],True,5.7))
    return g,focus

def switches(st):
    g=VGroup();n=4 if st>=3 else 3
    patterns=[(0,0,0),(0,0,0),(1,0,1),(1,0,1,0),(1,1,0,0),(1,1,1,1)]
    chosen=tuple(i for i,s in enumerate(patterns[st]) if s)
    row,focus=chipline(chosen,n,2.35,.98);g.add(row)
    for i in range(n):
        x=LX+(i-(n-1)/2)*.98
        g.add(tx('1' if i in chosen else '0',x,1.55,21,C['gold'] if i in chosen else C['muted'],True,.4))
    for j,s in enumerate(subset_masks(n)):
        x=LX+((j%4)-1.5)*1.33;y=.65-(j//4)*.65
        hi=(s==chosen)
        obj=tile(''.join('1' if k in s else '0' for k in range(n)),x,y,
            C['gold'] if hi else C['cyan'],1.08,.41,hi)
        g.add(obj)
        if hi:focus=obj
    g.add(tx(f'{n} CÔNG TẮC  →  {2**n} MÃ NHỊ PHÂN',LX,-2.66,14,C['green'],True,5.8))
    return g,focus

def sizes(st):
    g=VGroup();counts=size_counts(5)
    selected=st if st<=4 else None
    for k,v in enumerate(counts):
        x=LX+(k-2.5)*.87
        height=.17+v*.20
        rr=RoundedRectangle(width=.62,height=height,corner_radius=.045,
            stroke_width=0,fill_color=C['gold'] if k==selected else C['purple'],fill_opacity=.9)
        rr.move_to((x,-1.38+height/2,0));g.add(rr)
        number=tx(str(v),x,-1.27+height,17,C['gold'] if k==selected else C['text'],True,.7)
        g.add(number)
        g.add(tx(str(k),x,-1.81,15,C['muted'],True,.4))
    g.add(tx('SỐ PHẦN TỬ ĐƯỢC CHỌN: k = 0,1,2,3,4,5',LX,2.42,14,C['cyan'],True,5.8))
    g.add(tx('1 + 5 + 10 + 10 + 5 + 1 = 32',LX,-2.49,17,C['green'],True,5.8))
    return g,g[min(2*min(st,5)+1,len(g)-1)]

def special(st):
    # Four quadrants: A,B states. Each represents 2^3 free choices.
    g=VGroup();
    for i,(a,b) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
        x=LX+(-1.36 if i%2==0 else 1.36)
        y=.78 if i<2 else -.64
        color=C['gold'] if ((st==1 and a) or (st==2 and not a) or
            (st==3 and a and not b) or (st==4 and a!=b) or
            (st==5 and (a or b))) else C['cyan']
        if st==0:color=C['cyan']
        square=RoundedRectangle(width=2.42,height=1.14,corner_radius=.12,
            stroke_color=color,stroke_width=2,fill_color=C['panel_alt'],fill_opacity=.85).move_to((x,y,0))
        g.add(square)
        g.add(tx(f'A={a}   B={b}',x,y+.20,16,color,True,2.1))
        g.add(tx('8 tập con',x,y-.20,15,C['muted'],False,2.0))
    g.add(tx('C, D, E: BA CÔNG TẮC TỰ DO',LX,2.40,15,C['cyan'],True,5.75))
    g.add(tx(['4 nhóm x 8 = 32','CÓ A: 16','KHÔNG A: 16','CÓ A, KHÔNG B: 8','ĐÚNG MỘT: 16','ÍT NHẤT MỘT: 24'][st],LX,-2.39,17,C['gold'],True,5.7))
    return g,g[min(1+4*(st%4),len(g)-1)]

def parity(st):
    g=VGroup()
    ee=[s for s in subset_masks(5) if len(s)%2==0]
    oo=[s for s in subset_masks(5) if len(s)%2==1]
    g.add(tx('CHẴN',LX-1.5,2.37,16,C['cyan'],True,2.0))
    g.add(tx('LẺ',LX+1.5,2.37,16,C['gold'],True,2.0))
    for j in range(16):
        row=j//4;column=j%4
        for sign,arr in [(-1,ee),(1,oo)]:
            x=LX+(column-1.5)*.61+sign*1.37
            y=1.55-row*.69
            highlighted=(st==1 and j==0) or (st==3 and j in (0,1))
            o=tile(str(j+1),x,y,C['gold'] if sign==1 else C['cyan'],.45,.45,highlighted)
            g.add(o)
    g.add(tx(['32 TẬP CON: 16 CHẴN + 16 LẺ', 'ĐỔI TRẠNG THÁI A → ĐỔI CHẴN LẺ',
           'MỖI LOẠI: 2^(n−1)','16 + 16 = 32','TỔNG XEN DẤU BẰNG 0','n=0: CHẴN 1, LẺ 0'][st],LX,-2.40,13,C['green'],True,5.8))
    return g,g[0]

def lattice(st):
    g=VGroup();node={};focal=None
    allsets=subset_masks(4)
    for s in allsets:
        k=len(s)
        peers=[t for t in allsets if len(t)==k]
        j=peers.index(s)
        x=LX+(j-(len(peers)-1)/2)*1.07
        y=-1.83+k*.91
        node[s]=(x,y)
    for s in allsets:
        for i in range(4):
            if i not in s:
                nxt=tuple(sorted(s+(i,)))
                a=node[s];b=node[nxt]
                g.add(Line((a[0],a[1]+.20,0),(b[0],b[1]-.20,0),color=C['line'],stroke_width=1))
    for s in allsets:
        x,y=node[s];hot=st==1 and s in ((),(0,1,2,3)) or st>=2 and s in ((),(0,1,2,3))
        t=tile(format_set(s),x,y,C['gold'] if hot else C['cyan'],1.0,.43,hot)
        g.add(t)
        if hot:focal=t
    g.add(tx(['MẠNG 16 TẬP CON','T ↔ phần bù của T','KHÁC RỖNG: 15','KHÁC RỖNG & THỰC SỰ: 14',
             'CHỌN 2 TRONG 3 ĐẶC BIỆT: 12','CHỌN ĐÚNG k TRONG m ĐẶC BIỆT'][st],LX,-2.73,13,C['green'],True,5.8))
    return g,focal or g[-2]

def separated(st):
    g=VGroup(); n=6 if st==5 else 5
    patterns=[(),(0,2,4),(0,2),(0,2,4),(0,2,4),(0,2,4)]
    active=patterns[st]
    gap=.86
    for i in range(n):
        x=LX+(i-(n-1)/2)*gap
        hot=i in active
        o=tile(str(i+1),x,1.56,C['gold'] if hot else C['muted'],.65,.67,hot)
        g.add(o)
        if hot and i+1<n and i+1 in active:
            g.add(Line((x+.3,1.3,0),(x+.3,1.95,0),color=C['red']))
    if st in (0,1,2,3):
        valid=nonadjacent_subsets(5)
        for j,s in enumerate(valid[:13]):
            x=LX+((j%5)-2)*1.05;y=.46-(j//5)*.73
            g.add(tile(''.join(str(q+1) for q in s) if s else '∅',x,y,C['cyan'],.87,.44,st==2 and len(s)==2))
    else:
        seq=[nonadjacent_count(i) for i in range(7)]
        for i,val in enumerate(seq):
            x=LX+(i-3)*.77;y=.23
            g.add(tile(str(val),x,y,C['gold'] if i>=4 else C['cyan'],.66,.62,i>=4))
    g.add(tx(['KHÔNG CHỌN HAI Ô LIỀN NHAU','CHỌN 1,3,5 LÀ HỢP LỆ',
         '1 + 5 + 6 + 1 = 13','CHỌN k TRONG n−k+1','f(n)=f(n−1)+f(n−2)','f(6)=21'][st],LX,-2.48,15,C['green'],True,5.8))
    return g,g[0]

def challenge(st):
    g=VGroup();groups=[(0,3,5),(0,2,4,7),(0,2,4),(1,3,7),(0,3,5,7),(0,3,5,7)]
    chosen=groups[st];
    for i in range(8):
        x=LX+(i-3.5)*.70;hot=i in chosen
        shade=C['gold'] if hot else C['red'] if st in (2,4) and i in (1,6) else C['muted']
        g.add(tile(str(i+1),x,1.64,shade,.57,.70,hot))
    for i,(label,val) in enumerate([('CHỈ CHỌN 1',13),('CHỈ CHỌN 8',13),('CHỌN CẢ HAI',8),('KHÔNG CHỌN ĐẦU NÀO',21)]):
        x=LX; y=.53-i*.68
        row=RoundedRectangle(width=5.26,height=.55,corner_radius=.08,
            stroke_color=C['gold'] if st>=2 and i==min(st-2,3) else C['line'],
            fill_color=C['panel_alt'],fill_opacity=.85).move_to((x,y,0))
        g.add(row)
        g.add(tx(label,LX-1.2,y,14,C['text'],True,3.2))
        g.add(tx(str(val),LX+2.03,y,18,C['gold'],True,.7))
    g.add(tx(['8 Ô · ÍT NHẤT MỘT ĐẦU','55 − 21 = 34','CHỈ ĐẦU TRÁI: 13',
              'CHỈ ĐẦU PHẢI: 13','CẢ HAI ĐẦU: 8','13 + 13 + 8 = 34'][st],LX,-2.71,16,C['green'],True,5.8))
    return g,g[0]

def model(section,state):
    return {'explore':explore,'switches':switches,'sizes':sizes,'special':special,
            'parity':parity,'lattice':lattice,'separated':separated,'challenge':challenge}[section](state)

def formula_image(name):
    target=ROOT/'assets'/'comb19v2'/f'{name}.png'
    if not target.exists():raise FileNotFoundError(f'Missing Typst formula {target}; run prepare_comb19_v2.py')
    o=ImageMobject(str(target))
    if o.width>5.7:o.scale_to_fit_width(5.7)
    if o.height>1.08:o.scale_to_fit_height(1.08)
    o.move_to((RX,-1.11,0))
    return o

def wrap(s,maxchars=45):
    out=[];current=[]
    for word in s.split():
        if current and len(' '.join(current+[word]))>maxchars:
            out.append(' '.join(current));current=[]
        current.append(word)
    if current:out.append(' '.join(current))
    return out[:2]

class COMB19(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb19_voice_manifest.json'
        if not path.exists():raise FileNotFoundError('Run: python scripts/prepare_comb19_v2.py --voice off')
        self.manifest=json.loads(path.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Voice manifest beats mismatch')
        self.add(tx('SANG MATH / ĐẠI SỐ TỔ HỢP',LX,3.63,17,C['cyan'],True,6))
        self.add(tx('COMB19 / TẬP CON VÀ 2^n',RX,3.63,17,C['muted'],True,6))
        self.add(Line((-6.88,3.30,0),(6.88,3.30,0),color=C['line'],stroke_width=1.2))
        for x,width in ((LX,6.19),(RX,6.48)):
            self.add(RoundedRectangle(width=width,height=6.15,corner_radius=.14,
                fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1.1).move_to((x,0,0)))
        self.add(Line((-6.84,-3.32,0),(6.84,-3.32,0),color=C['line']))
        self.current=None

    def panel(self,b,index):
        title=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.71,14,C['purple'],True,5.8),
            tx(b.heading,RX,2.19,19,C['gold'],True,5.78))
        bullets=VGroup(*[tx('• '+s,RX,1.33-j*.65,16,C['text'],False,5.77) for j,s in enumerate(b.lines)])
        formula=formula_image(b.formula)
        note=VGroup(Line((.2,-1.81,0),(6.14,-1.81,0),color=C['line']))
        for j,s in enumerate(wrap(b.takeaway)):
            note.add(tx(s,RX,-2.22-j*.39,14,C['green'],True,5.7))
        num=tx(f'{index+1:02d} / {len(BEATS)}',0,-3.67,14,C['muted'],True)
        return title,bullets,formula,note,num

    def beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            path=ROOT/'voice'/clip['file']
            if not path.exists():raise FileNotFoundError(path)
            self.add_sound(str(path))
        target=max(b.min_seconds,float(clip.get('duration',0))+.85)
        visual,focus=model(b.section,b.state)
        title,bullets,formula,note,index=self.panel(b,i)
        if self.current is None:
            self.play(FadeIn(visual),FadeIn(title),FadeIn(index),run_time=1.2)
            elapsed=1.2
        else:
            old=self.current
            self.play(*[FadeOut(x) for x in old[:5]],FadeIn(visual),FadeIn(title),
                ReplacementTransform(old[5],index),run_time=1.15)
            elapsed=1.15
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.025),run_time=1.5);elapsed+=1.5
        for line in bullets:
            self.play(FadeIn(line,shift=UP*.07),run_time=1.2);elapsed+=1.2
        self.play(FadeIn(formula,shift=UP*.08),run_time=1.25);elapsed+=1.25
        self.play(FadeIn(note),run_time=.9);elapsed+=.9
        # Additional paced attention directed at the lesson model (not decoration).
        if target-elapsed>5:
            self.wait((target-elapsed-1.6)/2)
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.018),run_time=1.6)
            elapsed+=1.6+(target-elapsed-1.6)/2
        if target>elapsed:self.wait(target-elapsed)
        self.current=(visual,title,bullets,formula,note,index)

    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        if self.current:self.play(*[FadeOut(x) for x in self.current],run_time=1)
        end=VGroup(tx('TẬP CON VÀ CÔNG THỨC 2^n',0,.55,28,C['cyan'],True,12),
            tx('CHỌN / KHÔNG CHỌN  →  CHỨNG MINH  →  VẬN DỤNG',0,-.48,21,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.2);self.wait(3)
