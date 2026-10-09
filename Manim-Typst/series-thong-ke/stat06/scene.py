"""STAT06 full lecture: manim -ql stat06/scene.py STAT06.
Preflight all 32 states: manim -ql -r 426,240 --fps 8 stat06/scene.py STAT06_SMOKE.
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat06.lesson import BEATS,CHAPTERS,FREQ,BASE,A,B,SA,SB,OUTLIER,EX,EX2,SEX,SEX2
from stat01.lesson import SCORES

config.background_color='#0A1522'
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
BG='#0A1522';PANEL='#10293B';EDGE='#355A71'
WHITE='#EDF6FF';MUTED='#ADC6D5';CYAN='#56CBE9';GOLD='#FFD379'
GREEN='#67DDB5';CORAL='#FF8E87';PURPLE='#B7A9FC'
L=-3.43;R=3.43


def label(s,x,y,size=18,color=WHITE,bold=False,maxw=None,maxh=None):
    ob=Text(str(s),font=FONT,font_size=size,color=color,
            weight='BOLD' if bold else 'NORMAL',line_spacing=.94)
    if maxw and ob.width>maxw:ob.scale_to_fit_width(maxw)
    if maxh and ob.height>maxh:ob.scale_to_fit_height(maxh)
    return ob.move_to((x,y,0))

def title(s):return label(s,L,2.48,19,CYAN,True,6.0)
def footer(s):return label(s,L,-2.65,12,MUTED,maxw=6.0)
def axis(vmin,vmax,y=-.90,ticks=()):
    x0,x1=-6.06,-.83
    def X(v):return x0+(v-vmin)*(x1-x0)/(vmax-vmin)
    ob=VGroup(Line((x0,y,0),(x1,y,0),color=MUTED,stroke_width=2))
    for t in ticks:
        x=X(t)
        ob.add(Line((x,y-.11,0),(x,y+.11,0),color=MUTED,stroke_width=1.5),
               label(str(t),x,y-.34,12,MUTED))
    return ob,X

def points(vals,X,y=-.76,color=CYAN,radius=.09):
    g=VGroup();count={}
    for v in vals:
        rank=count.get(v,0);count[v]=rank+1
        g.add(Dot((X(v),y+rank*.125,0),radius=radius,color=color))
    return g

def mark(X,value,y0=-.8,y1=1.2,color=GOLD):
    return Line((X(value),y0,0),(X(value),y1,0),color=color,stroke_width=2.8)

def segment(X,v1,v2,y,color=CORAL):
    return Line((X(v1),y,0),(X(v2),y,0),color=color,stroke_width=3.2)

def card(s,x,y,w=2.3,color=GREEN):
    return VGroup(RoundedRectangle(width=w,height=.48,corner_radius=.08,fill_color=PANEL,
                  fill_opacity=1,stroke_color=color,stroke_width=1.3).move_to((x,y,0)),
                  label(s,x,y,15,color,True,w-.13))


def chap1(k):
    g=VGroup(title('CÙNG TRUNG BÌNH – KHÁC ĐỘ PHÂN TÁN'))
    ax,X=axis(0,14,-1.56,(0,1,4,5,7,9,10,13,14));g.add(ax,mark(X,7,-1.53,1.56,GOLD))
    g.add(label('A',-5.90,1.58,20,CYAN,True),points(A,X,1.03,CYAN))
    if k>=2:g.add(label('A = 5, 6, 7, 8, 9',L,1.95,17,CYAN,True,maxw=5.65))
    if k>=3:g.add(label('B',-5.90,.49,20,CORAL,True),points(B,X,-.08,CORAL))
    if k>=4:g.add(card('s²(A) = 2',-4.85,-2.14,2.12,CYAN),card('s²(B) = 18',-2.04,-2.14,2.25,CORAL))
    g.add(footer('Các mẫu minh họa độc lập; cùng đơn vị và cùng tỉ lệ trục'))
    return g,None


def chap2(k):
    g=VGroup(title('TỪ ĐỘ LỆCH ĐẾN PHƯƠNG SAI'))
    ax,X=axis(3.5,10.5,-1.42,(4,5,6,7,8,9,10));g.add(ax,mark(X,7,-1.35,1.36,GOLD))
    for value in A:
        g.add(Dot((X(value),-.66,0),radius=.085,color=CYAN))
        if k>=2 and value!=7:g.add(segment(X,7,value,.21,CORAL if value<7 else GREEN))
    if k==1:g.add(label('−2     −1     0     +1     +2',L,1.74,19,CYAN,True))
    if k>=2:g.add(label('Σ(xᵢ − x̄) = 0',L,1.73,20,GOLD,True,maxw=5.8))
    if k>=3:
        for j,(v,dev) in enumerate(zip(A,(-2,-1,0,1,2))):
            xx=X(v)
            h=.07 + abs(dev)*.23
            g.add(Rectangle(width=.30,height=h,fill_color=PURPLE,fill_opacity=.45,
                            stroke_color=PURPLE,stroke_width=1).move_to((xx,.47+h/2,0)))
        g.add(label('4 + 1 + 0 + 1 + 4 = 10',L,-2.12,18,PURPLE,True,maxw=5.9))
    if k>=4:g.add(label('s² = 10 / 5 = 2',L,2.06,21,GREEN,True,maxw=5.9))
    g.add(footer('Bình phương độ lệch để tránh triệt tiêu âm và dương'))
    return g,None


def chap3(k):
    g=VGroup(title('CÔNG THỨC TỪ 40 ĐIỂM KIỂM TRA'))
    ax,X=axis(3,11,-1.66,(4,5,6,7,8,9,10));g.add(ax)
    if k>=1:g.add(points(SCORES,X,-.95,CYAN,radius=.063))
    if k>=2:g.add(mark(X,7.1,-1.52,1.25,GOLD),label('Độ lệch chuẩn đưa đơn vị về như ban đầu',L,1.92,14,GREEN,True,5.9))
    if k>=3:g.add(card('40 giá trị',-5.17,-2.22,1.65,CYAN),card('Tổng 284',-3.20,-2.22,1.75,GREEN),card('x̄ = 7,1',-1.32,-2.22,1.56,GOLD))
    if k==4:g.add(label('Σxᵢ² = 2108  →  s² = 2,29',L,1.55,19,GOLD,True,maxw=5.8))
    g.add(footer('Đây là 40 điểm giả lập được dùng liên tục từ STAT01'))
    return g,None


def chap4(k):
    g=VGroup(title('PHƯƠNG SAI TỪ BẢNG TẦN SỐ'))
    x0=-5.83
    g.add(label('ĐIỂM',x0,1.65,14,MUTED,True),label('TẦN SỐ',x0,1.20,14,MUTED,True))
    for j,(value,freq) in enumerate(FREQ.items()):
        x=-4.95+j*.66
        g.add(label(str(value),x,1.65,17,CYAN,True),label(str(freq),x,1.20,17,GREEN,True))
    ax,X=axis(3,11,-1.52,(4,5,6,7,8,9,10));g.add(ax)
    for value,freq in FREQ.items():
        h=.10+freq*.15
        g.add(Rectangle(width=.40,height=h,fill_color=GREEN if value==7 else CYAN,
              stroke_width=0,fill_opacity=.65).move_to((X(value),-1.52+h/2,0)))
    if k>=2:g.add(label('Σf = 40      Σfx = 284',L,.29,16,GOLD,True,maxw=5.8))
    if k>=3:g.add(label('Σ f(x − 7,1)² = 91,6',L,-2.13,17,PURPLE,True,maxw=5.9))
    if k>=4:g.add(label('Σ fx² = 2108',L,2.13,20,GOLD,True,maxw=5.8))
    g.add(footer('Không được chia cho 7: n vẫn là 40 quan sát'))
    return g,None

def chap5(k):
    g=VGroup(title('ĐỘ LỆCH CHUẨN: NHÌN THẤY ĐỘ RỘNG'))
    ax,X=axis(-1,15,-1.38,(-1,1,3,5,7,9,11,13,15));g.add(ax,mark(X,7,-1.24,1.55,GOLD))
    tracker=None
    if k==3:
        tracker=ValueTracker(1/3)
        def dpoints():return points([7+(t-7)*tracker.get_value() for t in B],X,.44,CORAL)
        g.add(always_redraw(dpoints),always_redraw(lambda: label(
            f't = {tracker.get_value():.2f}    s² = {18*tracker.get_value()**2:.2f}',
            L,1.88,18,GOLD,True,maxw=5.75)))
    else:
        g.add(points(A,X,.87,CYAN),points(B,X,-.05,CORAL))
        g.add(label('A',-5.90,1.45,18,CYAN,True),label('B',-5.90,.36,18,CORAL,True))
        if k>=2:g.add(card('sA ≈ 1,414',-4.7,-2.06,2.30,CYAN),card('sB ≈ 4,243',-1.96,-2.06,2.34,CORAL))
        if k>=4:g.add(label('CÙNG TÂM KHÔNG CÓ NGHĨA CÙNG ĐỘ PHÂN TÁN',L,2.06,16,GREEN,True,maxw=5.9))
    g.add(footer('Các chấm thuộc hai mẫu khác nhau; không đổi thang đo'))
    return g,tracker


def chap6(k):
    g=VGroup(title('CỘNG VÀ NHÂN: PHƯƠNG SAI BIẾN ĐỔI THẾ NÀO?'))
    ax,X=axis(0,21,-1.38,(0,3,5,7,9,10,12,14,18,21));g.add(ax)
    original=A
    if k==1:new=tuple(v+3 for v in A); txt='y = x + 3   →   s² = 2'
    elif k==2:new=tuple(v*2 for v in A); txt='y = 2x   →   s² = 8'
    elif k==3:new=tuple(-v+15 for v in A);txt='y = −x + 15   →   s² = 2'
    else:new=tuple(v*2+3 for v in A);txt='y = 2x + 3   →   s² = 8'
    g.add(points(original,X,.93,CYAN),points(new,X,-.20,CORAL))
    g.add(label('GỐC',-5.79,1.49,16,CYAN,True),label('MỚI',-5.79,.32,16,CORAL,True))
    g.add(label(txt,L,-2.09,19,GOLD,True,maxw=5.9))
    if k>=3:g.add(label('Var(ax+b) = a² Var(x)',L,2.15,18,GREEN,True,maxw=5.8))
    g.add(footer('Giữ chung đơn vị đo và công thức khi so sánh'))
    return g,None


def chap7(k):
    g=VGroup(title('MỘT GIÁ TRỊ NGOẠI LỆ TÁC ĐỘNG THẾ NÀO?'))
    ax,X=axis(0,32,-1.39,(0,4,8,10,16,24,30,32));g.add(ax)
    g.add(points(SCORES,X,-.85,CYAN,radius=.044))
    tracker=None
    if k==1:
        tracker=ValueTracker(10)
        g.add(always_redraw(lambda: Dot((X(tracker.get_value()),.93,0),radius=.14,color=CORAL)))
        g.add(always_redraw(lambda:label(
            f'x = {tracker.get_value():.1f}   TB = {(274+tracker.get_value())/40:.2f}',
            L,1.91,16,GOLD,True,maxw=5.9)))
    else:
        g.add(Dot((X(30),.9,0),radius=.16,color=CORAL))
        if k>=2:g.add(label('TB: 7,1  →  7,6',L,1.99,19,GOLD,True,maxw=5.85))
        if k>=3:g.add(label('s²: 2,29  →  14,94',L,1.49,18,CORAL,True,maxw=5.85))
        if k>=4:g.add(label('IQR VẪN 2 – HAI THƯỚC ĐO KHÁC NHAU',L,-2.20,15,GREEN,True,maxw=5.9))
    g.add(footer('30 là giá trị thí nghiệm, không hợp lệ trên thang điểm 10'))
    return g,tracker


def chap8(k):
    g=VGroup(title('BÀI TẬP TỔNG HỢP: TỰ KIỂM TRA'))
    ax,X=axis(0,22,-1.4,(0,2,4,6,8,10,14,20,22));g.add(ax)
    vals=EX2 if k==4 else EX
    g.add(points(vals,X,-.70,CORAL if k==4 else CYAN))
    if k==1:g.add(label('2, 4, 6, 8, 10',L,1.77,20,GREEN,True,maxw=5.95))
    if k>=2:g.add(label('x̄ = 8' if k==4 else 'x̄ = 6',L,1.90,20,GOLD,True,maxw=5.8))
    if k>=3:
        g.add(label('s² = 40' if k==4 else 's² = 8',L,1.27,20,GREEN,True,maxw=5.8),
              label('s = 2√10' if k==4 else 's = 2√2',L,-2.12,20,PURPLE,True,maxw=5.8))
    g.add(footer('Đổi giá trị cuối thành 20: phương sai tăng từ 8 lên 40'))
    return g,None

VISUALS=(chap1,chap2,chap3,chap4,chap5,chap6,chap7,chap8)
FORM_KEYS=('compare','square','definition','frequency','spread','transform','outlier','exercise')

class STAT06(Scene):
    def frame(self):
        ob=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,
                           fill_color=BG,fill_opacity=1))
        for x in (L,R):
            ob.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                    stroke_color=EDGE,stroke_width=1,fill_color=PANEL,
                    fill_opacity=1).move_to((x,-.01,0)))
        ob.add(label('SANGMATH  /  THỐNG KÊ 06  /  PHƯƠNG SAI VÀ ĐỘ LỆCH CHUẨN',0,3.48,23,WHITE,True,13.10),
               Line((-6.70,3.09,0),(6.70,3.09,0),color=EDGE,stroke_width=1),
               label('THỐNG KÊ 10–12    •    MẪU SỐ n (MÔ TẢ)    •    MANIM + TYPST',0,-3.56,13,MUTED,maxw=13.0))
        return ob

    def notes(self,b):
        ob=VGroup(label(f'CHƯƠNG {b.chapter:02d}/08    •    NHỊP {b.step}/4',R,2.49,17,CYAN,True))
        ti='\n'.join(textwrap.wrap(b.title,26,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        ob.add(label(ti,R,1.73,27,WHITE,True,5.73,1.13),
               Line((.70,.79,0),(6.18,.79,0),color=EDGE,stroke_width=1.1),
               label(th,R,-.02,23,GOLD,True,5.68,1.50))
        formula=ROOT/'assets'/'stat06_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not formula.is_file():
            raise FileNotFoundError(f'Typst SVG not found: {formula}; run scripts/build_stat06_typst.py')
        if b.step>=3:
            svg=SVGMobject(str(formula))
            if svg.width>5.28:svg.scale_to_fit_width(5.28)
            if svg.height>.83:svg.scale_to_fit_height(.83)
            svg.move_to((R,-1.55,0))
            ob.add(label('CÔNG THỨC / KIỂM CHỨNG',R,-.97,14,CYAN,True),svg)
        else:ob.add(label('QUAN SÁT HÌNH  →  DỰ ĐOÁN  →  CHỨNG MINH',R,-1.46,16,GREEN,True,5.8))
        ob.add(label('KHÔNG NHẦM n VỚI n−1 KHI TÍNH PHƯƠNG SAI MÔ TẢ',R,-2.50,12,MUTED,maxw=5.9))
        return ob

    def construct(self):
        self.add(self.frame())
        src=ROOT/'stat06'/'runtime_plan.json'
        if not src.is_file():raise FileNotFoundError('Need runtime plan: python scripts/prepare_stat06.py --voice off')
        plan=json.loads(src.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT06' or len(plan.get('beats',[]))!=32:
            raise ValueError('Incorrect STAT06 runtime plan')
        old_visual=old_notes=None
        for i,beat in enumerate(BEATS):
            entry=plan['beats'][i]
            if (entry['chapter'],entry['step'])!=(beat.chapter,beat.step):
                raise ValueError(f'Wrong beat plan at index {i}')
            slot=float(entry['duration']);used=0.0
            if entry.get('voice'):
                sound=ROOT/entry['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,tracker=VISUALS[beat.chapter-1](beat.step)
            note=self.notes(beat)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.5);used+=1.5
            else:
                self.play(FadeOut(old_visual),FadeOut(old_notes),run_time=.60);used+=.60
                self.play(FadeIn(visual),FadeIn(note),run_time=1.15);used+=1.15
            if tracker is not None:
                end=3.0 if beat.chapter==5 else 30
                self.play(tracker.animate.set_value(end),run_time=4.5,rate_func=smooth);used+=4.5
            else:
                self.wait(.6);used+=.6
            if slot<=used:raise ValueError(f'Beat {i+1} planned too short')
            self.wait(slot-used)
            old_visual,old_notes=visual,note

class STAT06_SMOKE(STAT06):
    """Actually renders each visual/Typst state, rather than only the opening frame."""
    def construct(self):
        self.add(self.frame())
        for beat in BEATS:
            vis,_=VISUALS[beat.chapter-1](beat.step)
            note=self.notes(beat)
            self.add(vis,note)
            self.wait(.18)
            self.remove(vis,note)
