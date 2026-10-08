"""COMB22 | Dynamic programming for advanced combinatorics.
48 synchronized instructional beats; visual models correspond to exact Python DPs.
Compile formula PNGs and create voice manifest before running Manim.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from itertools import product
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb22_lesson_data import (BEATS,CHAPTER_LABELS,grid_table,tilings_direct,
    no11_states,pattern_rows,bitmask_layers,matrix_power,circular_no11,
    pattern_dp,pattern_bruteforce)
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.56
RX=3.18


def txt(s,x,y,size=16,color=None,bold=False,limit=None):
    obj=Text(str(s),font=FONT,font_size=size,color=color or C['text'],
             weight='BOLD' if bold else 'NORMAL')
    if limit and obj.width>limit:obj.scale_to_fit_width(limit)
    obj.move_to((x,y,0))
    return obj


def token(s,x,y,w=.75,h=.53,hot=False,bad=False,font=17):
    col=C['red'] if bad else (C['gold'] if hot else C['cyan'])
    rect=RoundedRectangle(width=w,height=h,corner_radius=.07,
       fill_color=C['panel_alt'],fill_opacity=1,stroke_color=col,stroke_width=2 if hot else 1.1)
    rect.move_to((x,y,0))
    text=txt(s,x,y,font,C['text'],hot,max(.3,w-.1))
    return VGroup(rect,text)


def title(g,text):
    g.add(txt(text,LX,2.58,14,C['cyan'],True,5.85))


def lattice(g,blocked,state):
    nums=grid_table(4,3,{(2,1)} if blocked else ())
    highlight=[(0,0),(1,0),(2,1),(3,2),(4,3),(4,3)][state]
    focus=None
    for i in range(5):
        for j in range(4):
            x=LX-2.34+i*1.13;y=-1.75+j*.95
            if i<4:g.add(Line((x+.35,y,0),(x+.77,y,0),color=C['line'],stroke_width=1.4))
            if j<3:g.add(Line((x,y+.29,0),(x,y+.66,0),color=C['line'],stroke_width=1.4))
            is_block=blocked and (i,j)==(2,1)
            hot=(i,j)==highlight
            cell=token('X' if is_block else str(nums[i][j]),x,y,.63,.56,hot=hot and not is_block,bad=is_block,font=15)
            if state<3 and (i+j)>state+1 and not is_block:cell.set_opacity(.23)
            g.add(cell)
            if hot:focus=cell
    g.add(txt('ĐÍCH  (4;3)',LX+2.0,2.02,13,C['gold'],True,2.25))
    return focus


def graph(section,state):
    g=VGroup();focus=None
    titles={
       'grid':'LƯỚI 4 × 3 · ĐẾM SỐ ĐƯỜNG ĐI',
       'obstacle':'LƯỚI CÓ MỘT ĐỈNH BỊ CHẶN',
       'tiling':'LÁT GẠCH 1 Ô / 2 Ô · FIBONACCI',
       'binary':'DÃY NHỊ PHÂN · CẤM 11',
       'automaton':'MÁY TRẠNG THÁI · CẤM 101',
       'bitmask':'GÁN VIỆC · DP THEO TẬP CON',
       'matrix':'MA TRẬN CHUYỂN · VÒNG TRÒN',
       'capstone':'BÀI TOÁN OLYMPIC · BA ĐIỀU KIỆN'
    }
    title(g,titles[section])
    if section in ('grid','obstacle'):
        focus=lattice(g,section=='obstacle',state)
        number=17 if section=='obstacle' else 35
        g.add(txt(('BỎ ĐỈNH Q  →  ' if section=='obstacle' else 'KHÔNG CẤM  →  ')+f'{number} ĐƯỜNG',LX,-2.58,16,C['green'],True,5.85))

    elif section=='tiling':
        patterns=tilings_direct(6)
        choices=[0,2,4,6,9,12]
        selected=patterns[choices[state]]
        left=LX-2.50
        for i in range(6):
            g.add(RoundedRectangle(width=.74,height=.62,corner_radius=.05,
                  fill_color=C['panel_alt'],fill_opacity=1,
                  stroke_color=C['line'],stroke_width=1).move_to((left+i*.85,1.04,0)))
        pos=0
        for i,step in enumerate(selected):
            w=.74 if step==1 else 1.58
            cx=left+pos*.85+(step-1)*.425
            tile=RoundedRectangle(width=w,height=.52,corner_radius=.06,
                  fill_color=C['gold'] if (i==state%len(selected)) else C['cyan'],
                  fill_opacity=.5,stroke_color=C['gold'] if step==2 else C['cyan'],stroke_width=2)
            tile.move_to((cx,1.04,0));g.add(tile)
            if i==state%len(selected):focus=tile
            pos+=step
        nums=[1,1,2,3,5,8,13]
        for i,n in enumerate(nums):
            x=LX+(i-3)*.78
            c=token(str(n),x,-.48,.65,.63,hot=i==min(state+1,6),font=16)
            g.add(c)
            if i==min(state+1,6):focus=c
        g.add(txt('f₀  f₁   f₂   f₃   f₄   f₅   f₆',LX,-1.18,14,C['muted']))
        g.add(txt('CÓ 13 CÁCH LÁT DẢI DÀI 6',LX,-2.30,16,C['green'],True,5.90))

    elif section=='binary':
        n=state+1
        a,b=no11_states(n)
        examples=['0','01','010','0101','01010','010100']
        s=examples[state]
        for i,bit in enumerate(s):
            x=LX+(i-(len(s)-1)/2)*.87
            c=token(bit,x,1.12,.68,.73,hot=i==len(s)-1,font=22)
            g.add(c)
            if i==len(s)-1:focus=c
        z=token(f'{a}',LX-1.40,-.19,1.38,.66,hot=state%2==0)
        o=token(f'{b}',LX+1.40,-.19,1.38,.66,hot=state%2==1)
        g.add(z,o,txt('KẾT THÚC 0',LX-1.4,.38,13,C['cyan'],True),
              txt('KẾT THÚC 1',LX+1.4,.38,13,C['gold'],True))
        g.add(txt(f'ĐỘ DÀI {n}:  {a} + {b} = {a+b}',LX,-1.55,18,C['green'],True,5.9))
        g.add(txt('CẤM CẠNH CHUYỂN 1 → 1',LX,-2.38,14,C['red'],True,5.7))
        focus=o if state%2 else z

    elif section=='automaton':
        points=[LX-2.0,LX,LX+2.0]
        counts=pattern_rows(state+1)[-1]
        for i,x in enumerate(points):
            c=Circle(radius=.42,stroke_width=2,
                     stroke_color=C['gold'] if i==state%3 else C['cyan'],
                     fill_color=C['panel_alt'],fill_opacity=1).move_to((x,1.15,0))
            g.add(c,txt('q'+str(i),x,1.15,17,C['text'],True))
            if i==state%3:focus=c
        g.add(Arrow((points[0]+.48,1.15,0),(points[1]-.48,1.15,0),
                    buff=0,stroke_width=2,color=C['cyan'],max_tip_length_to_length_ratio=.16),
              Arrow((points[1]+.48,1.15,0),(points[2]-.48,1.15,0),
                    buff=0,stroke_width=2,color=C['purple'],max_tip_length_to_length_ratio=.16))
        labels=['0→q0, 1→q1','0→q2, 1→q1','0→q0, 1→CẤM']
        for i,(x,s) in enumerate(zip(points,labels)):
            g.add(txt(s,x,.37,11,C['red'] if i==2 else C['muted'],False,2))
            g.add(token(str(counts[i]),x,-.77,1.23,.61,hot=i==state%3,font=17))
        g.add(txt(f'DÀI {state+1}:  {sum(counts)} DÃY HỢP LỆ',LX,-1.66,17,C['green'],True,5.9))
        g.add(txt('CUNG q₂ → (ĐỌC 1) BỊ LOẠI',LX,-2.45,13,C['red'],True,5.9))

    elif section=='bitmask':
        masks=[0,1,3,7,14,15]
        mask=masks[state]
        for i in range(4):
            for j in range(4):
                x=LX-1.85+j*1.2;y=1.48-i*.77
                bad=i==j
                hot=((mask>>j)&1)!=0 and i==min(state,3) and not bad
                c=token('×' if bad else ('✓' if hot else '·'),x,y,.77,.56,
                        hot=hot,bad=bad,font=16)
                g.add(c)
                if hot:focus=c
        layers=bitmask_layers(4)
        label=','.join(map(str,layers))
        g.add(txt('MỖI ĐƯỜNG CHÉO MÀU ĐỎ LÀ VIỆC CẤM',LX,-1.99,12,C['red'],True,5.9),
              txt(f'SỐ CÁCH THEO LỚP:  {label}',LX,-2.53,14,C['green'],True,5.9))
        if focus is None:focus=g[2+min(state,15)]

    elif section=='matrix':
        n=state+3
        m=matrix_power(n)
        g.add(txt('MA TRẬN CHUYỂN',LX-1.28,1.87,14,C['cyan'],True,2.7))
        vals=[[1,1],[1,0]]
        for i in range(2):
            for j in range(2):
                c=token(str(vals[i][j]),LX-1.80+j*.86,1.09-i*.76,.66,.59,
                        hot=(i==j and j==state%2))
                g.add(c)
                if i==j and j==state%2:focus=c
        for i in range(2):
            for j in range(2):
                c=token(str(m[i][j]),LX+.9+j*.86,1.09-i*.76,.66,.59,
                        hot=i==j)
                g.add(c)
                if i==state%2 and j==i:focus=c
        g.add(txt('M',LX-1.35,-.63,17,C['muted'],True),
              txt(f'M^{n}',LX+1.32,-.63,17,C['muted'],True),
              txt(f'tr(M^{n}) = {m[0][0]+m[1][1]}',LX,-1.64,19,C['green'],True,5.8),
              txt('ĐẦU VÀ CUỐI PHẢI KHỚP TRẠNG THÁI',LX,-2.44,13,C['gold'],True,5.8))

    elif section=='capstone':
        n=state+5
        examples=[''.join(map(str,s)) for s in product((0,1),repeat=10) if sum(s)==4 and s[-1]==0 and '101' not in ''.join(map(str,s))]
        sample=examples[(state*7)%len(examples)]
        for i,bit in enumerate(sample):
            x=LX+(i-4.5)*.52
            c=token(bit,x,1.31,.42,.62,hot=i==n-1,font=15)
            if i>=n:c.set_opacity(.21)
            g.add(c)
            if i==n-1:focus=c
        valid=pattern_dp(n,ones=4,last=0)
        g.add(txt(f'ĐÃ XÉT {n}/10 VỊ TRÍ',LX,.13,17,C['cyan'],True),
              txt(f'ĐÚNG 4 SỐ 1 · TRÁNH 101 · CUỐI 0',LX,-.59,14,C['gold'],True,5.95),
              txt(f'SỐ DÃY THỎA TẠM THỜI: {valid}',LX,-1.58,17,C['green'],True,5.87))
        g.add(txt('ĐẾM TỪNG LỚP DP(i,k,q)',LX,-2.44,14,C['muted'],True,5.9))
    return g,focus or g[1]


def formula_png(key):
    image=ROOT/'assets'/'comb22v2'/f'{key}.png'
    if not image.exists():raise FileNotFoundError('Run scripts/prepare_comb22_v2.py first: '+str(image))
    obj=ImageMobject(str(image))
    if obj.width>5.72:obj.scale_to_fit_width(5.72)
    if obj.height>1.12:obj.scale_to_fit_height(1.12)
    obj.move_to((RX,-1.31,0))
    return obj


class COMB22(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb22_voice_manifest.json'
        if not manifest.exists():raise FileNotFoundError('Run scripts/prepare_comb22_v2.py before rendering')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Invalid synchronized beat count')
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.61,16,C['cyan'],True,5.9))
        self.add(txt('COMB22 / QUY HOẠCH ĐỘNG',RX,3.61,15,C['muted'],True,5.8))
        self.add(Line((-6.91,3.32,0),(6.91,3.32,0),stroke_color=C['line'],stroke_width=1))
        for x,w in ((LX,6.24),(RX,6.40)):
            self.add(RoundedRectangle(width=w,height=6.13,corner_radius=.13,
              fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1).move_to((x,0,0)))
        self.previous=None

    def beat(self,index,b):
        clip=self.meta['clips'][f'{index:03}']
        seconds=max(b.min_seconds,float(clip.get('duration',0))+.85)
        if clip.get('file'):self.add_sound(str(ROOT/'voice'/clip['file']))
        model,focus=graph(b.section,b.state)
        heading=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.75,13,C['purple'],True,5.82),
                       txt(b.heading,RX,2.18,19,C['gold'],True,5.81))
        points=VGroup(*[txt('• '+line,RX,1.40-j*.64,15,C['text'],False,5.78)
                        for j,line in enumerate(b.lines)])
        formula=formula_png(b.formula)
        note=VGroup(Line((.27,-2.00,0),(6.34,-2.00,0),color=C['line']),
                    txt(b.takeaway,RX,-2.49,14,C['green'],True,5.76))
        marker=txt(f'{index+1:02d} / 48',0,-3.57,13,C['muted'],True)
        elapsed=0.
        if self.previous:
            a,h,p,f,n,num=self.previous
            self.play(FadeOut(a),FadeOut(h),FadeOut(p),FadeOut(f),FadeOut(n),
                      ReplacementTransform(num,marker),FadeIn(model),FadeIn(heading),run_time=1.30)
        else:self.play(FadeIn(model),FadeIn(heading),FadeIn(marker),run_time=1.30)
        elapsed+=1.30
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.04),run_time=1.55)
        elapsed+=1.55
        for label in points:
            self.play(FadeIn(label,shift=UP*.06),run_time=.92)
            elapsed+=.92
        self.play(FadeIn(formula,shift=UP*.06),run_time=1.26)
        self.play(FadeIn(note),run_time=.62)
        elapsed+=1.88
        if seconds-elapsed>7:
            rest=(seconds-elapsed-1.3)/2
            self.wait(rest)
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.025),run_time=1.3)
            elapsed+=rest+1.3
        if seconds>elapsed:self.wait(seconds-elapsed)
        self.previous=(model,heading,points,formula,note,marker)

    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        if self.previous:self.play(*[FadeOut(x) for x in self.previous],run_time=1.0)
        self.play(FadeIn(txt('QUY HOẠCH ĐỘNG  —  DYNAMIC PROGRAMMING',0,.48,24,C['cyan'],True,12)),run_time=1.2)
        self.play(FadeIn(txt('TRẠNG THÁI  •  TRUY HỒI  •  MÁY TỰ ĐỘNG  •  MA TRẬN',0,-.47,17,C['gold'],True,12)),run_time=.8)
        self.wait(2.2)