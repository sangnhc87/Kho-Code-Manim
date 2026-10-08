"""COMB18 -- Pascal's triangle, combinatorial proofs and rich 2D animation.

Run prepare script before rendering, to compile Typst equation images and sync voice.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb18_lesson_data import BEATS, CHAPTER_LABELS, triangle, vandermonde_splits
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.68
RX=3.16

def tx(text,x,y,size=17,color=None,bold=False,max_width=None):
    m=Text(str(text),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if max_width and m.width>max_width: m.scale_to_fit_width(max_width)
    m.move_to((x,y,0))
    return m

def card(text,x,y,color=None,w=.68,h=.49,font=17,active=True):
    border=color or C['cyan']
    bg=C['panel_alt'] if active else C['panel']
    rect=RoundedRectangle(width=w,height=h,corner_radius=.09,stroke_color=border,
        stroke_width=2 if active else .8,fill_color=bg,fill_opacity=.95).move_to((x,y,0))
    letters=tx(text,x,y,font,C['text'] if active else C['muted'],True,w-.08)
    return VGroup(rect,letters)

def grid_point(n,k,width=.73,top=2.23,dy=.69):
    return (LX+(k-n/2)*width,top-n*dy)

def pascal_grid(maxrow=6,selected=None,parents=None,highlight_row=None):
    g=VGroup(); focal=None
    for n in range(maxrow+1):
        for k,value in enumerate(triangle(n)[n]):
            x,y=grid_point(n,k)
            hot=(selected==(n,k)) or (highlight_row==n)
            par=(n,k) in (parents or ())
            t=card(str(value),x,y,C['gold'] if hot else C['purple'] if par else C['cyan'],
                w=.61,h=.49,font=16,active=hot or par)
            g.add(t)
            if hot: focal=t
    if selected and parents:
        bx,by=grid_point(*selected)
        for p in parents:
            px,py=grid_point(*p)
            ar=Arrow([px,py-.27,0],[bx,by+.25,0],buff=0,
                    stroke_width=2.1,tip_length=.10,color=C['gold'])
            g.add(ar)
    return g, focal or g[0]

def growth(state):
    # A genuinely expanding collection across 6 story beats.
    n=state
    g,f=pascal_grid(n,highlight_row=n)
    g.add(tx('MỖI HÀNG ĐƯỢC TẠO TỪ HÀNG TRƯỚC',LX,-2.65,14,C['muted'],True,5.8))
    return g,f

def parents_model(state):
    coords=[(4,2),(4,2),(5,2),(6,3),(5,0),(6,3)]
    n,k=coords[state]
    pa=((n-1,k-1),(n-1,k)) if 0<k<n else None
    g,f=pascal_grid(6,selected=(n,k),parents=pa)
    if state==4: g.add(tx('Ô BIÊN: LUÔN BẰNG 1',LX,-2.67,14,C['gold'],True,5.6))
    if state==5: g.add(tx('P(n,k) = P(n-1,k-1) + P(n-1,k)',LX,-2.67,13,C['cyan'],True,5.8))
    return g,f

def proof_model(state):
    g=VGroup()
    for i,ch in enumerate('ABCDEF'):
        x=LX+(i-2.5)*.85
        g.add(card(ch,x,1.80,C['gold'] if i==0 else C['cyan'],.64,.60,17))
    g.add(tx('CHỌN 3 TỪ 6 HỌC SINH',LX,2.64,16,C['cyan'],True,5.9))
    rows=[('CÓ A',10,C['gold']),('KHÔNG A',10,C['purple'])]
    for i,(lab,num,c) in enumerate(rows):
        y=.66-i*1.09
        frame=RoundedRectangle(width=4.75,height=.79,corner_radius=.12,
                fill_color=C['panel_alt'],fill_opacity=.9,
                stroke_color=c if (state>=i+1) else C['line'],stroke_width=2).move_to((LX,y,0))
        g.add(frame)
        g.add(tx(lab,LX-1.25,y,17,c,True,1.8))
        val=tx(str(num) if state>=i+1 else '?',LX+1.67,y,23,c,True,.8)
        g.add(val)
    g.add(tx('HAI LOẠI KHÔNG GIAO NHAU',LX,-1.48,14,C['green'],True,5.75))
    total=tx('10 + 10 = 20' if state>=3 else 'CÓ A  +  KHÔNG A',LX,-2.09,18,C['gold'],True,5.6)
    g.add(total)
    return g,total

def mirror_model(state):
    g,f=pascal_grid(6,selected=(6,2) if state<3 else None)
    for k in range(7):
        if k==0 and state==0:continue
        if (state%3==0 or k in ((2,4) if state<4 else (0,6))):
            x,y=grid_point(6,k)
            g.add(Circle(radius=.35,color=C['gold'],stroke_width=2).move_to((x,y,0)))
    if state>=2:
        g.add(tx('CHỌN k  <=>  LOẠI (n-k)',LX,-2.70,16,C['green'],True,5.6))
    return g,f

def sums_model(state):
    g=VGroup()
    g.add(tx('TỔNG HÀNG / HỆ SỐ CỦA (1+x)^n',LX,2.65,15,C['cyan'],True,5.8))
    for n in range(7):
        y=1.9-n*.63
        text=' + '.join(str(x) for x in triangle(n)[n])
        if len(text)>42:text='1 + 6 + 15 + 20 + 15 + 6 + 1'
        highlight=(n==6 if state>1 else n==min(6,state*3))
        g.add(tx(f'n={n}',LX-2.45,y,14,C['gold'] if highlight else C['muted'],True,1))
        g.add(tx(text,LX-.30,y,13,C['text'],False,4.0))
        g.add(tx(str(2**n),LX+2.52,y,15,C['gold'] if highlight else C['green'],True,.6))
    line=tx('TỔNG CHẴN = TỔNG LẺ = 32' if state>=4 else 'TỔNG HÀNG = 2^n',LX,-2.75,14,C['gold'],True,5.7)
    g.add(line)
    return g,line

def hockey_model(state):
    positions=[(2,2),(3,2),(4,2),(5,2)]
    marked=positions[:min(state+1,4)]
    g=VGroup()
    g.add(tx('CÁC Ô CHỌN THEO ĐƯỜNG CHÉO',LX,2.74,15,C['cyan'],True,5.75))
    for n in range(7):
        for k,val in enumerate(triangle(n)[n]):
            x,y=grid_point(n,k,top=2.12,dy=.59)
            focus=(n,k) in marked or ((n,k)==(6,3) and state>=3)
            g.add(card(str(val),x,y,C['gold'] if focus else C['cyan'],.58,.42,14,focus))
    label=tx('1 + 3 + 6 + 10 = 20' if state>=3 else 'CÙNG CHỈ SỐ DƯỚI k = 2',LX,-2.65,17,C['gold'],True,5.6)
    g.add(label)
    return g,label

def parity_bitmap(rows):
    # One image instead of hundreds of Manim rectangles: render-efficient.
    from PIL import Image, ImageDraw
    cell=22
    W=rows*cell+50;H=rows*cell+34
    pic=Image.new('RGB',(W,H),C['panel']);d=ImageDraw.Draw(pic)
    for n,row in enumerate(triangle(rows-1)):
        for k,v in enumerate(row):
            x=(W-rows*cell)//2+round((rows-n-1)*cell/2)+k*cell
            y=12+n*cell
            color=C['gold'] if v%2 else '#233750'
            d.rounded_rectangle((x+2,y+2,x+cell-2,y+cell-2),radius=3,fill=color)
    return np.array(pic)

def parity_model(state):
    rows=[8,12,16,20,26,32][state]
    g=Group()
    g.add(tx('SỐ LẺ SÁNG / SỐ CHẴN TỐI',LX,2.72,15,C['cyan'],True,5.9))
    img=ImageMobject(parity_bitmap(rows));img.scale_to_fit_height(4.6)
    if img.width>5.55:img.scale_to_fit_width(5.55)
    img.move_to((LX,-.18,0))
    g.add(img)
    note=tx(f'{rows} HÀNG · QUY TẮC MODULO 2',LX,-2.77,15,C['gold'],True,5.8)
    g.add(note)
    return g,note

def challenge_model(state):
    g=VGroup()
    g.add(tx('(1+x)^5  ×  (1+x)^3',LX,2.65,17,C['cyan'],True,5.7))
    vals=vandermonde_splits()
    for i,val in enumerate(vals):
        y=1.62-i*.83
        active=i==min(state,3) or state>=4
        g.add(card(f'i={i}',LX-2.04,y,C['gold'] if active else C['purple'],1.10,.58,16,active))
        g.add(tx(f'C(5,{i}) × C(3,{3-i})',LX-.33,y,15,C['text'],False,3.5))
        g.add(tx(str(val),LX+2.25,y,21,C['gold'] if active else C['muted'],True,.6))
    label=tx('1 + 15 + 30 + 10 = 56' if state>=3 else 'CHỌN ĐÚNG 3 CHỮ x',LX,-2.36,16,C['green'],True,5.8)
    g.add(label)
    return g,label

def model(section,state):
    if section=='growth':return growth(state)
    if section=='parents':return parents_model(state)
    if section=='proof':return proof_model(state)
    if section=='mirror':return mirror_model(state)
    if section=='sums':return sums_model(state)
    if section=='hockey':return hockey_model(state)
    if section=='parity':return parity_model(state)
    return challenge_model(state)

def formula_image(name):
    path=ROOT/'assets'/'comb18v2'/f'{name}.png'
    if not path.is_file():raise FileNotFoundError(f'First run prepare_comb18_v2.py; missing {path}')
    obj=ImageMobject(str(path))
    if obj.width>5.72:obj.scale_to_fit_width(5.72)
    if obj.height>.99:obj.scale_to_fit_height(.99)
    obj.move_to((RX,-1.05,0))
    return obj

def wrapped_short(s,maxchars=43):
    ans=[];part=[]
    for word in s.split():
        if part and len(' '.join(part+[word]))>maxchars:
            ans.append(' '.join(part));part=[]
        part.append(word)
    if part:ans.append(' '.join(part))
    return ans[:2]

class COMB18(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb18_voice_manifest.json'
        if not path.is_file():raise FileNotFoundError('First run: python scripts/prepare_comb18_v2.py --voice off')
        self.manifest=json.loads(path.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Manifest mismatch')
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.68,3.62,18,C['cyan'],True,6.0))
        self.add(tx('COMB18  /  TAM GIÁC PASCAL',3.16,3.62,18,C['muted'],True,6.0))
        self.add(Line((-6.88,3.31,0),(6.88,3.31,0),stroke_width=1.2,color=C['line']))
        for x,w in ((LX,6.19),(RX,6.48)):
            panel=RoundedRectangle(width=w,height=6.18,corner_radius=.14,fill_color=C['panel'],
                fill_opacity=1,stroke_color=C['line'],stroke_width=1.2).move_to((x,0,0))
            self.add(panel)
        self.add(Line((-6.85,-3.32,0),(6.85,-3.32,0),color=C['line'],stroke_width=1.2))
        self.current=None

    def text_panel(self,b,index):
        head=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.64,14,C['purple'],True,5.8),
                    tx(b.heading,RX,2.11,19,C['gold'],True,5.8))
        lines=VGroup(*[tx('• '+item,RX,1.31-j*.64,16,C['text'],False,5.76) for j,item in enumerate(b.lines)])
        formula=formula_image(b.formula)
        note=VGroup(Line((.18,-1.75,0),(6.24,-1.75,0),color=C['line']))
        for j,string in enumerate(wrapped_short(b.takeaway)):
            note.add(tx(string,RX,-2.17-j*.40,14,C['green'],True,5.7))
        footer=tx(f'{index+1:02d} / {len(BEATS)}',0,-3.67,14,C['muted'],True)
        return head,lines,formula,note,footer

    def show_beat(self,index,b):
        clip=self.manifest['clips'][f'{index:03}']
        if clip.get('file'):
            path=ROOT/'voice'/clip['file']
            if not path.exists():raise FileNotFoundError(path)
            self.add_sound(str(path))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.85)
        art,focus=model(b.section,b.state)
        head,bullets,formula,note,num=self.text_panel(b,index)
        if self.current is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(num),run_time=1.1)
        else:
            old_art,old_head,old_bullets,old_form,old_note,old_num=self.current
            self.play(FadeOut(old_art),FadeOut(old_head),FadeOut(old_bullets),FadeOut(old_form),
                FadeOut(old_note),FadeIn(art),FadeIn(head),ReplacementTransform(old_num,num),run_time=1.12)
        elapsed=1.12 if self.current else 1.1
        # Highlight the mathematical object, not unrelated decorative motion.
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.02),run_time=1.18);elapsed+=1.18
        for line in bullets:
            self.play(FadeIn(line,shift=UP*.07),run_time=1.0);elapsed+=1.0
        self.play(FadeIn(formula,shift=UP*.08),run_time=1.18);elapsed+=1.18
        self.play(FadeIn(note),run_time=.92);elapsed+=.92
        if elapsed<duration:self.wait(duration-elapsed)
        self.current=(art,head,bullets,formula,note,num)

    def construct(self):
        for i,b in enumerate(BEATS):self.show_beat(i,b)
        if self.current:self.play(*[FadeOut(x) for x in self.current],run_time=1)
        ending=VGroup(tx('TAM GIÁC PASCAL  ·  TỪ PHÉP CỘNG',0,.60,29,C['cyan'],True,12),
                      tx('HIỂU QUY LUẬT  →  CHỨNG MINH  →  VẬN DỤNG',0,-.52,22,C['gold'],True,12))
        self.play(FadeIn(ending),run_time=1.2);self.wait(3.0)
