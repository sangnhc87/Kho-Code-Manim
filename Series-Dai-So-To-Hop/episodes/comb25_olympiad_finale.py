"""COMB25: final Olympiad lesson - Burnside, Polya, roots of unity, cube.
Requires: python scripts/prepare_comb25_v2.py --voice off/on
"""
from __future__ import annotations
import json,sys,math
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb25_lesson_data import (BEATS,CHAPTER_LABELS,ring_permutations,
    cycles,fixed_colorings,orbit_count_formula,cube_rotations,residue_choose)
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
LX=-3.56
RX=3.18
FONT='Noto Sans'
COLORS=[C['cyan'],C['gold'],C['purple'],C['green']]

def txt(s,x,y,size=16,color=None,bold=False,limit=None):
    t=Text(str(s),font=FONT,font_size=size,color=color or C['text'],
           weight='BOLD' if bold else 'NORMAL')
    if limit and t.width>limit:t.scale_to_fit_width(limit)
    if t.height>.64:t.scale_to_fit_height(.64)
    t.move_to((x,y,0))
    return t

def chip(label,x,y,active=False,w=1.15):
    r=RoundedRectangle(width=w,height=.44,corner_radius=.07,
          fill_color=C['panel_alt'],fill_opacity=1,
          stroke_width=1.6,stroke_color=C['gold'] if active else C['line'])
    r.move_to((x,y,0))
    return VGroup(r,txt(label,x,y,13,C['gold'] if active else C['text'],active,w-.10))

def ring(n,state,mirror=False,weight=None):
    """Actual circular arrangement with marked rotational/reflection action."""
    g=VGroup()
    palette=[C['cyan'],C['gold']]
    if weight is None: pattern=[0,1,0,1,1,0,0,1][:n]
    else:pattern=[1]*weight+[0]*(n-weight)
    if state%2:pattern=pattern[1:]+pattern[:1]
    px=[]
    for i in range(n):
        a=PI/2-TAU*i/n
        px.append((LX+1.77*math.cos(a),.30+1.77*math.sin(a),0))
    g.add(Circle(radius=1.77,color=C['line'],stroke_width=2).move_to((LX,.30,0)))
    highlight=VGroup()
    for i,p in enumerate(px):
        circle=Circle(radius=.265,stroke_color=C['bg'],stroke_width=1.6,
                      fill_color=palette[pattern[i]],fill_opacity=1).move_to(p)
        g.add(circle);highlight.add(circle)
        if n<=6:g.add(txt(str(i+1),p[0],p[1],12,C['bg'],True))
    if mirror:
        theta=state*PI/6
        x=.0; y=.30
        l=DashedLine((LX-2.1*math.cos(theta),y-2.1*math.sin(theta),0),
                     (LX+2.1*math.cos(theta),y+2.1*math.sin(theta),0),
                     color=C['red'],dash_length=.13,stroke_width=2.3)
        g.add(l)
    else:
        g.add(Arc(radius=2.23,start_angle=math.radians(18),angle=2.65,
                  color=C['gold'],stroke_width=2.8).move_to((LX,.3,0)))
    return g,highlight

def cube_face(pts,color):
    return Polygon(*[(x,y,0) for x,y in pts],
                   fill_color=color,fill_opacity=.94,
                   stroke_color=C['text'],stroke_width=2.6)

def cube_figure(state):
    """True parallel-edge isometric projection of the three visible cube faces."""
    x=LX;y=.5
    top=[(x-1.4,y+.35),(x,y+1.0),(x+1.4,y+.35),(x,y-.30)]
    left=[(x-1.4,y+.35),(x,y-.30),(x,y-1.85),(x-1.4,y-1.20)]
    right=[(x,y-.30),(x+1.4,y+.35),(x+1.4,y-1.20),(x,y-1.85)]
    triad=[C['gold'],C['cyan'],C['purple']]
    boxes=VGroup(cube_face(top,triad[state%3]),
                 cube_face(left,triad[(state+1)%3]),
                 cube_face(right,triad[(state+2)%3]))
    boxes.add(txt('MẶT TRÊN',x,y+.40,14,C['bg'],True))
    boxes.add(txt('TRÁI',x-.61,y-.85,13,C['bg'],True))
    boxes.add(txt('PHẢI',x+.62,y-.85,13,C['bg'],True))
    return boxes

def model(section,state):
    """Eight distinct visual mathematical models, each with a six-step progression."""
    g=VGroup(); focus=None
    names={
      'burnside':'BURNSIDE · LỚP QUỸ ĐẠO VÒNG',
      'bracelet':'DIHEDRAL · THÊM GƯƠNG PHẢN CHIẾU',
      'fixedweight':'RÀNG BUỘC: 3 ĐEN · 3 TRẮNG',
      'polya':'PÓLYA · CHỈ SỐ CHU TRÌNH',
      'roots':'CĂN ĐƠN VỊ · LỌC BẬC ĐỒNG DƯ',
      'weighted':'HÀM SINH CÓ TRỌNG SỐ',
      'synthesis':'CHỌN ĐÚNG NHÓM PHÉP BIẾN ĐỔI',
      'cube':'CUBE · 24 PHÉP QUAY KHÔNG GIAN'}
    g.add(txt(names[section],LX,2.68,15,C['cyan'],True,6.02))
    if section in ('burnside','bracelet','fixedweight','weighted'):
        n=8 if section=='weighted' else 6
        d,focus=ring(n,state,section=='bracelet',4 if section=='weighted' else (3 if section=='fixedweight' else None))
        g.add(d)
        if section=='burnside':
            labels=['0°: 64','60°: 2','120°: 4','180°: 8','240°: 4','300°: 2']
            g.add(txt(labels[state],LX,-2.15,20,C['gold'],True,6))
            g.add(txt('64 + 2 + 4 + 8 + 4 + 2 = 84',LX,-2.72,15,C['green'],True,6))
        elif section=='bracelet':
            g.add(txt('PHÉP QUAY: 84  |  GƯƠNG: 72',LX,-2.22,15,C['gold'],True,6))
            g.add(txt('TỔNG / 12 = 13 MẪU',LX,-2.72,16,C['green'],True,6))
        elif section=='fixedweight':
            g.add(txt('20  +  0  +  2  +  0  +  2  +  0',LX,-2.22,15,C['gold'],True,6))
            g.add(txt('TỔNG / 6 = 4 MẪU',LX,-2.72,16,C['green'],True,6))
        else:
            g.add(txt('70  +  0  +  2  +  0  +  6  +  0  +  2  +  0',LX,-2.22,13,C['gold'],True,6))
            g.add(txt('TỔNG / 8 = 10 MẪU',LX,-2.72,16,C['green'],True,6))
    elif section=='polya':
        # four vertices on an exact square; reflection axes for last states
        positions=[(LX-1.46,1.53,0),(LX+1.46,1.53,0),
                   (LX+1.46,-1.39,0),(LX-1.46,-1.39,0)]
        g.add(Polygon(*positions,stroke_color=C['line'],stroke_width=2.4,fill_opacity=.06))
        color_indices=[(0,1,2,0),(0,0,1,1),(0,1,0,1),(0,0,0,0),(0,1,2,1),(1,0,1,0)][state]
        focus=VGroup()
        for i,p in enumerate(positions):
            circ=Circle(radius=.34,color=C['text'],stroke_width=1.3,
                        fill_color=COLORS[color_indices[i]],fill_opacity=1).move_to(p)
            g.add(circ);focus.add(circ)
        if state>=4:
            g.add(DashedLine((LX,-1.95,0),(LX,2.05,0),
                             stroke_color=C['red'],stroke_width=2,dash_length=.14))
        rows=['QUAY 0°: 4 CHU TRÌNH','QUAY 90°: 1 CHU TRÌNH',
              'QUAY 180°: 2 CHU TRÌNH','QUAY 270°: 1 CHU TRÌNH',
              'D₄: THÊM BỐN GƯƠNG','24 MẪU QUAY  ·  21 MẪU GƯƠNG']
        g.add(txt(rows[state],LX,-2.48,15,C['gold'],True,6))
    elif section=='roots':
        center=(LX,.17,0)
        circle=Circle(radius=1.79,color=C['line'],stroke_width=2).move_to(center)
        g.add(circle)
        marks=VGroup()
        for i in range(3):
            a=TAU*i/3
            x=center[0]+1.79*math.cos(a);y=center[1]+1.79*math.sin(a)
            edge=Arrow((center[0],center[1],0),(x,y,0),buff=0,
                       color=COLORS[i],stroke_width=4,max_tip_length_to_length_ratio=.18)
            g.add(edge);marks.add(edge)
            g.add(txt(['1','ω','ω²'][i],x+(.26 if i==0 else -.2),y+(.2 if i==0 else -.23),17,C['text'],True))
        focus=marks
        g.add(txt('1  +  ω  +  ω²  =  0',LX,-2.08,19,C['gold'],True,6))
        if state>=3:g.add(txt('k ≡ 0 (mod 3)  →  GIỮ',LX,-2.61,15,C['green'],True,6))
        else:g.add(txt('k ≢ 0 (mod 3)  →  KHỬ',LX,-2.61,15,C['red'],True,6))
    elif section=='synthesis':
        themes=[('6 HẠT, 2 MÀU','QUAY: 14','GƯƠNG: 13'),
                ('8 HẠT, 4 ĐEN','QUAY: 10','GƯƠNG: 8'),
                ('4 ĐỈNH, 3 MÀU','QUAY: 24','GƯƠNG: 21')]
        for i,(title,a,b) in enumerate(themes):
            y=1.77-i*1.43
            group=VGroup(chip(title,LX-1.1,y,i==state%3,3.3),
                         chip(a,LX-.64,y-.52,i==state%3,2.14),
                         chip(b,LX+1.58,y-.52,i==state%3,2.14))
            g.add(group)
            if i==state%3:focus=group
        g.add(txt('CHỌN NHÓM PHÉP BIẾN ĐỔI TRƯỚC',LX,-2.72,14,C['green'],True,6))
    elif section=='cube':
        figure=cube_figure(state)
        focus=figure;g.add(figure)
        labels=['ĐỒNG NHẤT  ·  1','QUA MẶT 90°  ·  6','QUA MẶT 180°  ·  3',
                'QUA ĐỈNH 120°  ·  8','QUA CẠNH 180°  ·  6','BURNSIDE  →  57 MẪU']
        g.add(txt(labels[state],LX,-2.24,17,C['gold'],True,6))
        g.add(txt('729 + 162 + 243 + 72 + 162 = 1368',LX,-2.74,13,C['green'],True,6))
    if focus is None:focus=g[1] if len(g)>1 else g
    return g,focus

def formula_png(key):
    file=ROOT/'assets'/'comb25v2'/f'{key}.png'
    if not file.exists():raise FileNotFoundError(f'Run scripts/prepare_comb25_v2.py first: {file}')
    img=ImageMobject(str(file))
    if img.width>5.70:img.scale_to_fit_width(5.70)
    if img.height>1.20:img.scale_to_fit_height(1.20)
    img.move_to((RX,-1.31,0))
    return img

class COMB25(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb25_voice_manifest.json'
        if not path.exists():raise FileNotFoundError('Prepare narration manifest before render')
        self.meta=json.loads(path.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Voice beat count mismatch')
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.60,16,C['cyan'],True,5.9))
        self.add(txt('COMB25 / OLYMPIAD FINALE',RX,3.60,15,C['muted'],True,5.8))
        self.add(Line((-6.91,3.32,0),(6.91,3.32,0),stroke_color=C['line'],stroke_width=1))
        for x,w in ((LX,6.24),(RX,6.40)):
            self.add(RoundedRectangle(width=w,height=6.13,corner_radius=.13,
                     fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1).move_to((x,0,0)))
        self.previous=None
    def beat(self,index,b):
        clip=self.meta['clips'][f'{index:03}']
        seconds=max(b.min_seconds,float(clip.get('duration',0))+.85)
        if clip.get('file'):self.add_sound(str(ROOT/'voice'/clip['file']))
        diagram,focus=model(b.section,b.state)
        heading=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.75,13,C['purple'],True,5.8),
                       txt(b.heading,RX,2.16,19,C['gold'],True,5.8))
        points=VGroup(*[txt('• '+line,RX,1.40-j*.65,15,C['text'],False,5.8)
                        for j,line in enumerate(b.lines)])
        equation=formula_png(b.formula)
        note=VGroup(Line((.27,-2.00,0),(6.34,-2.00,0),color=C['line']),
                    txt(b.takeaway,RX,-2.48,14,C['green'],True,5.8))
        marker=txt(f'{index+1:02d} / 48',0,-3.57,13,C['muted'],True)
        elapsed=0.0
        if self.previous:
            a,h,p,f,n,num=self.previous
            self.play(FadeOut(a),FadeOut(h),FadeOut(p),FadeOut(f),FadeOut(n),
                      ReplacementTransform(num,marker),FadeIn(diagram),FadeIn(heading),run_time=1.30)
        else:self.play(FadeIn(diagram),FadeIn(heading),FadeIn(marker),run_time=1.30)
        elapsed+=1.30
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.025),run_time=1.50)
        elapsed+=1.50
        for text in points:
            self.play(FadeIn(text,shift=UP*.05),run_time=.93);elapsed+=.93
        self.play(FadeIn(equation,shift=UP*.05),run_time=1.28)
        self.play(FadeIn(note),run_time=.63);elapsed+=1.91
        if seconds-elapsed>7:
            rest=(seconds-elapsed-1.30)/2
            self.wait(rest)
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.02),run_time=1.30)
            elapsed+=rest+1.30
        if seconds>elapsed:self.wait(seconds-elapsed)
        self.previous=(diagram,heading,points,equation,note,marker)
    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        if self.previous:self.play(*[FadeOut(x) for x in self.previous],run_time=1.0)
        self.play(FadeIn(txt('25 TẬP  ·  TỪ QUY TẮC CỘNG ĐẾN BURNSIDE',0,.47,22,C['cyan'],True,12)),run_time=1.2)
        self.play(FadeIn(txt('BẢN CHẤT  →  CHỨNG MINH  →  ỨNG DỤNG',0,-.46,18,C['gold'],True,12)),run_time=.8)
        self.wait(2.2)
