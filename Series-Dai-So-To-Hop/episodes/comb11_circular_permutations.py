"""COMB11 V2 - Hoán vị vòng tròn: 48-beat Manim + Typst lecture."""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb11_lesson_data import BEATS, CHAPTER_LABELS
from series_config import PALETTE as C

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX, RX=-3.68,3.10


def txt(value,x,y,size=18,color=None,bold=False,max_width=None):
    t=Text(str(value),font=FONT,font_size=size,color=color or C['text'],
           weight='BOLD' if bold else 'NORMAL')
    if max_width and t.width>max_width:
        t.scale_to_fit_width(max_width)
    t.move_to((x,y,0))
    return t


def pill(value,x,y,width=.65,height=.64,color=None,size=18):
    col=color or C['cyan']
    b=RoundedRectangle(width=width,height=height,corner_radius=.13,
        stroke_color=col,stroke_width=1.6,fill_color=C['panel_alt'],fill_opacity=1)
    b.move_to((x,y,0))
    value=txt(value,x,y,size,C['text'],True,width-.09)
    return VGroup(b,value)


def left_top(g,title):
    g.add(txt(title,LX,2.62,16,C['cyan'],True,5.62))


def left_foot(g,title):
    g.add(txt(title,LX,-2.64,15,C['gold'],True,5.63))


def ring_layout(people,cy=-.13,r=1.72,cx=LX,mark=None,colors=None,
                center_text=None,seat_numbers=False,draw_links=False):
    """Create an oriented ring; labels remain upright while positions animate."""
    g=VGroup()
    center=(cx,cy,0)
    disc=Circle(radius=r+.22,stroke_width=2,stroke_color=C['line'],
        fill_color=C['panel_alt'],fill_opacity=.30).move_to(center)
    inner=Circle(radius=max(.40,r-.56),stroke_width=1.1,stroke_color=C['line'],
        fill_opacity=0).move_to(center)
    g.add(disc,inner)
    places=[]
    n=len(people)
    for i in range(n):
        phi=math.pi/2-2*math.pi*i/n
        places.append((cx+r*math.cos(phi),cy+r*math.sin(phi),0))
    if draw_links:
        for i in range(n):
            if people[i].lower() in ('a','b','c') and any(x.lower()==people[i].lower() and x!=people[i] for x in people):
                pass
    tokens=[]
    for i,(name,p) in enumerate(zip(people,places)):
        if colors and name in colors: color=colors[name]
        elif name.upper().startswith('A'):color=C['gold']
        elif name.upper().startswith('B'):color=C['purple']
        else:color=C['cyan']
        if mark is not None and name in mark:color=C['green']
        token=pill(name,p[0],p[1],.60 if n<=6 else .53,.60 if n<=6 else .53,color,17 if n<=6 else 15)
        tokens.append(token)
        g.add(token)
        if seat_numbers:
            v=tuple((p[j]-center[j])*(r+.49)/r+center[j] for j in range(3))
            g.add(txt(str(i+1),v[0],v[1],11,C['muted'],False,.31))
    if center_text:g.add(txt(center_text,cx,cy,18,C['gold'],True,2.48))
    return g,tokens,places


def add_small_round(g,people,cx,cy,caption,r=.91):
    tbl,tokens,_=ring_layout(people,cy=cy,r=r,cx=cx)
    g.add(tbl,txt(caption,cx,cy-r-0.38,14,C['muted'],True,2.8))
    return tokens


def core_view(section,state):
    g=VGroup()
    focus=None
    moving=None
    if section=='rotation':
        left_top(g,'QUAY VÒNG · ĐẾM LỚP TƯƠNG ĐƯƠNG')
        people=list('ABCD')
        if state in (1,2):people=people[state%4:]+people[:state%4]
        tbl,tokens,places=ring_layout(people,r=1.67,center_text='4 người')
        g.add(tbl)
        moving=(tokens,places) if state==1 else None
        if state in (2,4):
            g.add(txt('24 dãy → 6 vòng',LX,-.86,17,C['green'],True,5.1))
        left_foot(g,'4! / 4 = 3! = 6 CÁCH NGỒI VÒNG' if state>=2 else 'QUAY BÀN CÓ TẠO CÁCH MỚI KHÔNG?')
        focus=tokens[state%4]
    elif section=='anchor':
        left_top(g,'CỐ ĐỊNH A · SÁU NGƯỜI')
        people=list('ABCDEF')
        if state==5:
            tbl,tokens,places=ring_layout(people,center_text='GHẾ CÓ NHÃN',seat_numbers=True)
        else:
            tbl,tokens,places=ring_layout(people,center_text='A làm mốc')
        g.add(tbl)
        g.add(txt('5! = 120' if state>=2 and state!=5 else '6! = 720' if state==5 else 'ĐẶT A Ở ĐỈNH',
            LX,-.88,19,C['green'] if state>=2 else C['gold'],True,5.35))
        left_foot(g,'VÒNG KHÔNG ĐÁNH SỐ: (n − 1)!' if state>=3 else 'CỐ ĐỊNH A → BỎ PHÉP QUAY TRÙNG')
        focus=tokens[0]
    elif section=='reflection':
        left_top(g,'ĐỔI CHIỀU KHÁC VỚI QUAY')
        a=add_small_round(g,list('ABCDEF'),LX-1.55,.45,'THEO CHIỀU KIM',r=.94)
        b=add_small_round(g,list('AFEDCB'),LX+1.55,.45,'ẢNH GƯƠNG',r=.94)
        g.add(txt('120 vòng có hướng' if state<=1 else '60 lớp nếu được phép lật',
                  LX,-.86,16,C['green'] if state>=2 else C['gold'],True,5.5))
        left_foot(g,'CHỈ CHIA 2 NẾU ĐỀ COI LẬT GIỐNG NHAU' if state>=2 else 'GƯƠNG KHÔNG PHẢI PHÉP QUAY')
        focus=b[1] if state%2 else a[1]
    elif section=='adjacent':
        left_top(g,'A VÀ B PHẢI NGỒI KỀ NHAU')
        people=list('ABCDEF')
        tbl,tokens,_=ring_layout(people,center_text='AB kề')
        g.add(tbl)
        if state>=1:
            highlight=SurroundingRectangle(VGroup(tokens[0],tokens[1]),buff=.14,
                   color=C['green'],stroke_width=2.2,corner_radius=.13)
            g.add(highlight)
        if state>=2:g.add(txt('[AB] và 4 người → 5 vật',LX,-.88,16,C['gold'],True,5.5))
        left_foot(g,'2 × 4! = 48 CÁCH' if state>=3 else 'GỘP A VÀ B THÀNH MỘT KHỐI')
        focus=tokens[1]
    elif section=='apart':
        left_top(g,'A VÀ B KHÔNG ĐƯỢC KỀ')
        people=list('ACBDEF') if state>=2 else list('ABCDEF')
        tbl,tokens,_=ring_layout(people,center_text='72 vòng')
        g.add(tbl)
        if state>=2:g.add(txt('B có 3 vị trí hợp lệ',LX,-.90,17,C['green'],True,5.6))
        else:g.add(txt('120 tổng − 48 bị loại',LX,-.90,17,C['red'],True,5.6))
        left_foot(g,'120 − 48 = 3 × 4! = 72' if state>=1 else 'ĐẾM PHẦN BÙ HOẶC ĐẾM TRỰC TIẾP')
        focus=tokens[people.index('B')]
    elif section=='alternate':
        left_top(g,'NAM – NỮ NGỒI XEN KẼ')
        people=['M1','F1','M2','F2','M3','F3']
        if state<=1:people=['M1','_','M2','_','M3','_']
        cols={x:(C['cyan'] if x.startswith('M') else C['purple']) for x in people if x!='_'}
        cols['_']=C['gold']
        tbl,tokens,_=ring_layout(people,center_text='3 khoảng',colors=cols)
        g.add(tbl)
        g.add(txt('2 cách xếp nam × 6 cách đặt nữ',LX,-.90,16,C['gold'],True,5.45))
        left_foot(g,'(3 − 1)! × 3! = 12' if state>=3 else 'XẾP NAM → CHỌN KHOẢNG CHO NỮ')
        focus=tokens[1 if state<=2 else (state%6)]
    elif section=='couples':
        left_top(g,'BA CẶP · NGUYÊN LÝ BÙ TRỪ')
        people=['A','B','C','a','b','c'] if state==5 else ['A','a','B','b','C','c']
        tbl,tokens,_=ring_layout(people,center_text='3 cặp')
        g.add(tbl)
        # Explicit pair links are a visual aid, not edges of the seating ring.
        for j,one in enumerate((0,2,4)):
            col=C['red'] if j<=max(0,state-2) and state>=2 else C['line']
            p=tokens[one].get_center();q=tokens[one+1].get_center()
            if state in (2,3,4): g.add(Line(p,q,stroke_width=1.8,color=col))
        numerals=['120','120','3 × 48','3 × 24','16','32']
        g.add(txt(numerals[state],LX,-.86,22,C['green'] if state==5 else C['gold'],True,5.0))
        left_foot(g,'120 − 144 + 72 − 16 = 32' if state==5 else 'ĐẾM SỐ VÒNG VI PHẠM ĐIỀU KIỆN')
        focus=tokens[(state*2)%6]
    else:
        left_top(g,'VẬN DỤNG VÒNG TRÒN')
        if state in (0,1):
            people=list('ABCDEF')
            tbl,tokens,_=ring_layout(people,center_text='A đối diện B')
        elif state in (2,3):
            people=list('ABCDEFG')
            tbl,tokens,_=ring_layout(people,r=1.75,center_text='Khối ABC')
        else:
            people=list('ABCDEF')
            tbl,tokens,_=ring_layout(people,center_text='Chọn cách đếm')
        g.add(tbl)
        left_foot(g,'24 CÁCH ĐỐI DIỆN · 144 CÁCH KHỐI BA' if state>=3 else 'CỐ ĐỊNH MỐC, RỒI ĐẾM THEO ĐIỀU KIỆN')
        focus=tokens[0]
    return g,focus,moving


def image_formula(key):
    path=ROOT/'assets'/'comb11v2'/f'{key}.png'
    if not path.is_file():raise FileNotFoundError(f'Run python scripts/prepare_comb11_v2.py --voice off: {path}')
    obj=ImageMobject(str(path))
    obj.scale_to_fit_width(min(obj.width,5.58))
    if obj.height>.79:obj.scale_to_fit_height(.79)
    obj.move_to((RX,-1.12,0))
    return obj


class COMB11(Scene):
    def setup(self):
        p=ROOT/'voice'/'comb11_voice_manifest.json'
        if not p.exists():raise FileNotFoundError('Run scripts/prepare_comb11_v2.py')
        self.manifest=json.loads(p.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Wrong voice manifest')
        self.last=None
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.7,3.62,19,C['cyan'],True,6.0))
        self.add(txt('COMB11  /  HOÁN VỊ VÒNG TRÒN',3.68,3.62,17,C['muted'],True,5.1))
        self.add(Line((-6.85,3.32,0),(6.85,3.32,0),color=C['line'],stroke_width=1.1))
        for cx,w in ((LX,6.18),(RX,6.46)):
            p=RoundedRectangle(width=w,height=6.16,corner_radius=.16,
                stroke_color=C['line'],stroke_width=1.3,fill_color=C['panel'],fill_opacity=1)
            p.move_to((cx,0,0));self.add(p)
        self.add(Line((-6.85,-3.32,0),(6.85,-3.32,0),color=C['line'],stroke_width=1.1))

    def right(self,b,i):
        h=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.67,15,C['purple'],True,5.78),
                 txt(b.heading,RX,2.05,20,C['gold'],True,5.73))
        lines=VGroup(*[txt('• '+line,RX,1.24-j*.60,17,C['text'],False,5.75)
                       for j,line in enumerate(b.lines)])
        f=image_formula(b.formula)
        conclusion=VGroup(Line((.25,-1.76,0),(6.17,-1.76,0),color=C['line'],stroke_width=1.1),
              txt(b.takeaway,RX,-2.34,15,C['green'],True,5.72))
        counter=txt(f'{i+1:02d} / {len(BEATS)}',0,-3.70,15,C['muted'],True)
        return h,lines,f,conclusion,counter

    def beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            p=ROOT/'voice'/clip['file']
            if not p.is_file():raise FileNotFoundError(p)
            self.add_sound(str(p))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.85)
        art,focus,moving=core_view(b.section,b.state)
        h,lines,f,con,counter=self.right(b,i)
        if self.last is None:
            self.play(FadeIn(art),FadeIn(h),FadeIn(counter),run_time=.9)
        else:
            prev_art,prev_h,prev_lines,prev_f,prev_con,prev_counter=self.last
            self.play(FadeOut(prev_art),FadeIn(art),FadeOut(prev_h),FadeIn(h),
                FadeOut(prev_lines),FadeOut(prev_f),FadeOut(prev_con),
                ReplacementTransform(prev_counter,counter),run_time=1.0)
        special=0.
        if moving:
            tokens,places=moving
            self.play(*[token.animate.move_to(places[(j+1)%len(places)])
                         for j,token in enumerate(tokens)],run_time=1.65)
            special=1.65
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.07),run_time=1.38)
        for line in lines:
            self.play(FadeIn(line,shift=.08*UP),run_time=1.04)
        self.play(FadeIn(f,shift=.08*UP),run_time=1.12)
        self.play(FadeIn(con),run_time=.9)
        self.play(Circumscribe(con[-1],color=C['green'],buff=.08),run_time=1.05)
        spent=(1.0 if self.last is not None else .9)+special+1.38+3*1.04+1.12+.9+1.05
        if duration>spent:self.wait(duration-spent)
        self.last=(art,h,lines,f,con,counter)

    def construct(self):
        for i,beat in enumerate(BEATS):self.beat(i,beat)
        self.play(*[FadeOut(o) for o in self.last],run_time=1)
        end=VGroup(txt('COMB11 · HOÁN VỊ VÒNG TRÒN',0,.53,28,C['cyan'],True,11.5),
                   txt('HIỂU PHÉP QUAY, GỘP KHỐI VÀ PHẦN BÙ',0,-.40,20,C['gold'],True,12.1))
        self.play(FadeIn(end),run_time=1.2)
        self.wait(2.95)
