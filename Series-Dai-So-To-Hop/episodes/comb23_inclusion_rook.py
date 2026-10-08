"""COMB23 V2. Inclusion-exclusion, derangements, rook polynomials.
All mathematical models derive from the independent comb23_lesson_data module.
"""
from __future__ import annotations
import json,sys
from itertools import combinations,permutations
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb23_lesson_data import (BEATS,CHAPTER_LABELS,rook_numbers,
 forbidden_diagonal,forbidden_asymmetric,forbidden_cycle,count_exact_fixed,
 derangements,three_sets,brute_avoiding)
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

def card(s,x,y,w=.7,h=.51,hot=False,bad=False,font=16):
    color=C['red'] if bad else (C['gold'] if hot else C['cyan'])
    outer=RoundedRectangle(width=w,height=h,corner_radius=.07,
              fill_color=C['panel_alt'],fill_opacity=1,stroke_color=color,
              stroke_width=2 if hot or bad else 1.0).move_to((x,y,0))
    label=txt(s,x,y,font,C['text'],hot, max(.22,w-.12))
    return VGroup(outer,label)

def header(g,s):
    g.add(txt(s,LX,2.69,15,C['cyan'],True,5.95))

def board(n,banned,hot=(),muted=(),highlight_allowed=(),left=LX-2.02,top=1.72,step=.73):
    """Visual board; hot squares show selected rook cells."""
    g=VGroup();focus=None
    forbidden=set(banned);hot=set(hot);muted=set(muted)
    for i in range(n):
        for j in range(n):
            x=left+j*step;y=top-i*step
            is_forbidden=(i,j) in forbidden
            tile=RoundedRectangle(width=step*.81,height=step*.78,corner_radius=.055,
                fill_color=C['panel_alt'] if not is_forbidden else '#572639',
                fill_opacity=.98,stroke_color=C['gold'] if (i,j) in hot else
                (C['red'] if is_forbidden else C['line']),
                stroke_width=2.3 if (i,j) in hot else 1.05).move_to((x,y,0))
            if (i,j) in muted:tile.set_opacity(.16)
            g.add(tile)
            if (i,j) in hot:
                mark=txt('●',x,y,24,C['gold'],True)
                g.add(mark);focus=mark
            elif (i,j) in highlight_allowed:
                mark=txt('✓',x,y,17,C['green'],True)
                g.add(mark);focus=mark
            elif is_forbidden:
                g.add(txt('×',x,y,15,C['red'],True))
    for i in range(n):
        g.add(txt(chr(65+i),left-.55,top-i*step,12,C['muted'],True))
        g.add(txt(str(i+1),left+i*step,top+.51,12,C['muted'],True))
    return g,focus

def placement(n,banned,k,index=0):
    b=sorted(banned)
    opts=[]
    for xs in combinations(b,k):
        if len({i for i,j in xs})==len({j for i,j in xs})==k:opts.append(xs)
    return opts[index%len(opts)] if opts else ()

def graph(section,state):
    g=VGroup();focus=None
    title={
      'three_sets':'BA VÙNG GIAO NHAU · DẤU LUÂN PHIÊN',
      'derange':'THƯ VÀ PHONG BÌ · KHÔNG CỐ ĐỊNH',
      'fixed_ban':'CHỈ CẤM BA VỊ TRÍ ĐẦU',
      'diagonal':'BÀN CỜ ĐƯỜNG CHÉO · ĐA THỨC XE',
      'board':'BẢNG CẤM BẤT ĐỐI XỨNG',
      'rencontres':'CHÍNH XÁC k ĐIỂM CỐ ĐỊNH',
      'rook_recurrence':'HAI NHÁNH CỦA ĐA THỨC XE',
      'menage':'OLYMPIC · HAI Ô CẤM MỖI HÀNG'
    }[section]
    header(g,title)
    if section=='three_sets':
        cols=[C['cyan'],C['gold'],C['purple']]
        centers=[(LX-1.03,.58),(LX+1.0,.58),(LX-.03,-.70)]
        for k,((x,y),c) in enumerate(zip(centers,cols)):
            circ=Circle(radius=1.28,stroke_color=c,stroke_width=3,
                fill_color=c,fill_opacity=.10 if k!=state%3 else .23)
            circ.move_to((x,y,0));g.add(circ)
            if k==state%3:focus=circ
        g.add(txt('A: 15',LX-1.89,1.90,16,C['cyan'],True),
              txt('B: 10',LX+1.90,1.90,16,C['gold'],True),
              txt('C: 6',LX,-2.02,16,C['purple'],True),
              txt('GIAO 3 TẬP: 1',LX,-2.56,13,C['green'],True))
        g.add(txt(['15 + 10 + 6','AB = 5','AC = 3   BC = 2','ABC = 1','TỔNG = 22','KHÔNG ĐẾM TRÙNG'][state],LX,.10,17,C['text'],True,5.85))
    elif section in ('derange','fixed_ban','diagonal','board','menage'):
        n=5 if section=='menage' else (6 if section=='fixed_ban' else 4)
        if section=='derange':n=5
        ban={'derange':forbidden_diagonal(n),'fixed_ban':{(i,i) for i in range(3)},
             'diagonal':forbidden_diagonal(n),'board':forbidden_asymmetric(),
             'menage':forbidden_cycle(n)}[section]
        rs=rook_numbers(n,ban)
        if section=='fixed_ban':
            hot=[(state%3,state%3)] if state<=2 else placement(n,ban,min(3,state-2),0)
        else:
            k=min(n,state)
            hot=placement(n,ban,k,state+1) if k else ()
        grid,f=board(n,ban,hot=hot,left=LX-((n-1)*(.72 if n>=5 else .83))/2,top=1.49,
                     step=.72 if n>=5 else .83)
        g.add(grid);focus=f or grid[0]
        if section=='derange':
            vals=[24,9,9,44,265,44];note=f'HOÁN VỊ KHÔNG CỐ ĐỊNH: {vals[state]}'
        elif section=='fixed_ban':
            terms=['6! = 720','3 × 5! = 360','3 × 4! = 72','3! = 6','N = 426','CHỈ CẤM A,B,C'];note=terms[state]
        elif section=='diagonal':note='HỆ SỐ XE: '+', '.join(str(x) for x in rs)
        elif section=='board':note='HỆ SỐ XE: '+', '.join(str(x) for x in rs)
        else:note='HỆ SỐ XE: '+', '.join(str(x) for x in rs)
        g.add(txt(note,LX,-2.41,14,C['green'],True,5.93))
    elif section=='rencontres':
        letters=['A','B','C','D','E']
        count=state if state<5 else 2
        if state==0:count=2
        values=[44,45,20,10,0,1]
        total=VGroup()
        for i,x in enumerate(letters):
            xpos=LX+(i-2)*1.00
            total.add(card(x,xpos,1.52,.82,.61,hot=i<min(count,5),font=20))
            total.add(txt(str(i+1),xpos,2.06,12,C['muted']))
        g.add(total)
        displays=[('ĐÚNG 2 VỊ TRÍ',20),('CHỌN 2 TRONG 5',10),('D3 = 2',2),('CÔNG THỨC TỔNG QUÁT',20),('CỘNG ĐỦ 120 HOÁN VỊ',120),('KỲ VỌNG = 1',1)]
        g.add(txt(displays[state][0],LX,.15,17,C['cyan'],True,5.93),
              txt(str(displays[state][1]),LX,-.72,34,C['gold'],True))
        for i,val in enumerate(values):
            x=LX+(i-2.5)*.9
            tile=card(str(val),x,-1.72,.76,.62,hot=i==state,font=16)
            g.add(tile)
            if i==state:focus=tile
        g.add(txt('k = 0     1      2      3      4      5',LX,-2.34,12,C['muted']))
    elif section=='rook_recurrence':
        ban=forbidden_asymmetric();cell=(0,0)
        panels=[('B',ban),('B trừ p',ban-{cell}),('B trừ hàng/cột',
                  {(i,j) for i,j in ban if i!=0 and j!=0})]
        for t,(lab,bb) in enumerate(panels):
            xpos=LX-1.95+t*1.95
            g.add(txt(lab,xpos,1.99,13,C['gold'] if t==state%3 else C['muted'],True,1.9))
            sample,focus2=board(4,bb,hot=[cell] if t==0 and state in (0,1,2) else (),
                     left=xpos-.6,top=1.34,step=.38)
            g.add(sample)
            if t==state%3:focus=focus2 or sample[0]
        g.add(txt('KHÔNG CHỌN p    /    CÓ CHỌN p',LX,-1.22,15,C['cyan'],True,5.9))
        g.add(txt('R(B) = R(B bỏ p) + x·R(B bỏ hàng/cột)',LX,-1.99,13,C['green'],True,5.87))
        g.add(txt('1, 5, 8, 5, 1',LX,-2.58,15,C['gold'],True))
    return g,focus if focus is not None else g[1]

def formula_png(key):
    path=ROOT/'assets'/'comb23v2'/f'{key}.png'
    if not path.exists():raise FileNotFoundError('Run scripts/prepare_comb23_v2.py first: '+str(path))
    img=ImageMobject(str(path))
    if img.width>5.74:img.scale_to_fit_width(5.74)
    if img.height>1.11:img.scale_to_fit_height(1.11)
    img.move_to((RX,-1.28,0));return img

class COMB23(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb23_voice_manifest.json'
        if not manifest.exists():raise FileNotFoundError('Run prepare_comb23_v2.py before rendering')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Invalid lesson beat manifest')
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.61,16,C['cyan'],True,5.9))
        self.add(txt('COMB23 / BAO HÀM - LOẠI TRỪ',RX,3.61,15,C['muted'],True,5.8))
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
        self.play(FadeIn(txt('BAO HÀM–LOẠI TRỪ  ·  ĐA THỨC XE',0,.48,24,C['cyan'],True,12)),run_time=1.2)
        self.play(FadeIn(txt('ĐẾM GIAO  →  CỘNG TRỪ  →  HOÁN VỊ HỢP LỆ',0,-.47,17,C['gold'],True,12)),run_time=.8)
        self.wait(2.2)
