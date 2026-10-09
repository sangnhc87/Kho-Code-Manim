"""STAT10 Manim lecture: grouped quartiles. All 32 steps are independently smoke-rendered.
Preflight: python scripts/build_stat10_typst.py; python scripts/prepare_stat10.py --voice off
Manim: manim -ql -r 854,480 --fps 24 stat10/scene.py STAT10
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import (label,top,foot,badge,ruled_axis,raw_points,bar,
    XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE)
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,CUM,ASYM,ASYM_FREQ
from stat10.lesson import (BEATS,MAIN,ALT,RAW,IQR,BOUND_FREQ,BOUND,
                           REVERSE_FREQ,REVERSE)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
COLORS=(CYAN,GREEN,PURPLE,CORAL)
FORM_KEYS=('overview','ranks','q1','q2','q3_iqr','ogive','boundaries','reverse')

def num(x):
    return f'{x:.2f}'.replace('.',',')

def hist(classes, freq, selected=None):
    axis,X=ruled_axis(classes[0].left,classes[-1].right,-1.55,
           tuple(sorted(set([c.left for c in classes]+[classes[-1].right]))))
    g=VGroup(axis)
    for i,(interval,f) in enumerate(zip(classes,freq)):
        color=GOLD if selected==i else COLORS[i%4]
        height=f*.115
        g.add(bar(X,interval.left,interval.right,height,-1.55,color),
              label(str(f),X(interval.midpoint),-1.38+height,15,color,True,1.1))
    return g,X

def table(classes,freq,selected=None):
    g=VGroup(label('KHOẢNG',-5.02,1.58,13,CYAN,True,2.03),
             label('TẦN SỐ',-3.39,1.58,13,CYAN,True,1.3),
             label('TÍCH LŨY',-1.57,1.58,13,CYAN,True,1.5))
    accumulated=0
    for i,(c,f) in enumerate(zip(classes,freq)):
        accumulated+=f;y=.96-i*.70
        color=GOLD if selected==i else WHITE
        if selected==i:
            g.add(RoundedRectangle(width=5.52,height=.51,corner_radius=.07,
                 stroke_color=GOLD,stroke_width=1.2,fill_color=EDGE,
                 fill_opacity=.3).move_to((XL,y,0)))
        g.add(label(c.caption,-5.02,y,17,color,True,2.0),
              label(str(f),-3.39,y,18,color,True,1.1),
              label(str(accumulated),-1.57,y,18,color,True,1.12))
    return g

def unknown_table():
    """Keep the unknown frequency concealed until the solution step."""
    g=VGroup(label('KHOẢNG',-5.02,1.58,13,CYAN,True,2.03),
             label('TẦN SỐ',-3.39,1.58,13,CYAN,True,1.3),
             label('TÍCH LŨY',-1.57,1.58,13,CYAN,True,1.5))
    for i,(interval,f,cum) in enumerate(zip(CLASSES,('6','x','32−x','2'),
                                              ('6','6+x','38','40'))):
        y=.96-i*.70
        color=GOLD if i==1 else WHITE
        g.add(label(interval.caption,-5.02,y,17,color,True,2.0),
              label(f,-3.39,y,18,color,True,1.12),
              label(cum,-1.57,y,18,color,True,1.12))
    return g

def axis_marks(values,colors=COLORS):
    axis,X=ruled_axis(4,12,-1.16,(4,6,8,10,12))
    g=VGroup(axis)
    for i,v in enumerate(values):
        col=colors[i%len(colors)]
        g.add(Line((X(v),-1.12,0),(X(v),.91,0),stroke_width=2.5,color=col),
              Dot((X(v),.91,0),radius=.07,color=col),
              label(f'Q{i+1} ≈ {num(v)}',X(v),1.21+(i%2)*.40,13,col,True,1.47))
    return g

def progress_in_class(qs,show=1):
    axis,X=ruled_axis(4,12,-1.44,(4,6,8,10,12))
    g=VGroup(axis)
    g.add(Line((X(6),-.82,0),(X(8),-.82,0),color=EDGE,stroke_width=13),
          Line((X(8),.03,0),(X(10),.03,0),color=EDGE,stroke_width=13))
    for j,q in enumerate(qs[:show]):
        col=(GREEN,GOLD,PURPLE)[j]
        start=6 if j<2 else 8
        y=-.82 if j<2 else .03
        g.add(Line((X(start),y,0),(X(q.value),y,0),color=col,stroke_width=13),
              Line((X(q.value),-1.43,0),(X(q.value),1.19,0),color=col,stroke_width=2),
              label(f'Q{j+1}: {num(q.value)}',X(q.value),1.42,13,col,True,1.63))
    return g

def ogive(k):
    x0,x1=-5.96,-.86;y0=-1.73;dy=.074
    X=lambda x:x0+(x-4)*(x1-x0)/8
    Y=lambda n:y0+n*dy
    g=VGroup(Line((x0,y0,0),(x1,y0,0),color=MUTED,stroke_width=1.3),
             Line((x0,y0,0),(x0,Y(40),0),color=MUTED,stroke_width=1.3))
    nodes=((4,0),(6,6),(8,24),(10,38),(12,40))
    for a,b in zip(nodes,nodes[1:]):
        g.add(Line((X(a[0]),Y(a[1]),0),(X(b[0]),Y(b[1]),0),color=CYAN,stroke_width=2.8))
    for x,y in nodes:
        g.add(Dot((X(x),Y(y),0),radius=.06,color=GOLD),
              label(str(y),X(x),Y(y)+.20,12,GOLD,True,.7),
              label(str(x),X(x),y0-.30,12,MUTED))
    if k>=2:
        for i,q in enumerate(MAIN[:min(3,k-1)]):
            col=(GREEN,GOLD,PURPLE)[i]
            g.add(Line((x0,Y(q.rank),0),(X(q.value),Y(q.rank),0),color=col,stroke_width=2),
                  Line((X(q.value),Y(q.rank),0),(X(q.value),y0,0),color=col,stroke_width=2),
                  Dot((X(q.value),Y(q.rank),0),color=col,radius=.07))
    return g

def chapter1(k):
    g=VGroup(top('TỪ DỮ LIỆU GỐC ĐẾN TỨ PHÂN VỊ GHÉP NHÓM'))
    if k==1:
        ax,X=ruled_axis(4,12,-1.35,(4,6,8,10,12));g.add(ax,raw_points(SCORES,X,-1.16,.042))
    else:
        h,_=hist(CLASSES,FREQ,1);g.add(h)
    if k>=2:g.add(badge('40 QUAN SÁT  •  4 NHÓM',XL,1.73,GREEN,4.5))
    if k>=3:g.add(label('GỐC: Q1=6    Q2=7    Q3=8',XL,1.13,17,GOLD,True,5.84))
    if k>=4:g.add(badge('GHÉP NHÓM ⇒ CÁC GIÁ TRỊ NỘI SUY',XL,-2.24,CORAL,5.8))
    g.add(foot('Không thể khôi phục chính xác từng giá trị bên trong lớp.'))
    return g,None

def chapter2(k):
    g=VGroup(top('BA MỐC TẦN SỐ TÍCH LŨY'))
    selected=(None,None,1,2)[k-1]
    g.add(table(CLASSES,FREQ,selected))
    if k>=2:g.add(badge('n/4 = 10  •  n/2 = 20  •  3n/4 = 30',XL,-2.26,GOLD,5.78))
    if k==4:g.add(label('MỐC 10, 20: LỚP 2   /   MỐC 30: LỚP 3',XL,2.02,14,GREEN,True,6.0))
    g.add(foot('Chọn lớp dựa trên mốc tích lũy, không theo lớp có mốt.'))
    return g,None

def chapter3(k):
    g=VGroup(top('Q1: ĐI 4 TRONG 18 QUAN SÁT'))
    h,X=hist(CLASSES,FREQ,1);g.add(h)
    if k>=2:g.add(badge('MỐC 10 − TRƯỚC LỚP 6 = 4',XL,1.82,GOLD,5.5))
    if k>=3:g.add(Line((X(6),-.31,0),(X(MAIN[0].value),-.31,0),stroke_width=9,color=GREEN),
                  label('4 / 18 CỦA LỚP RỘNG 2',XL,1.27,16,GREEN,True,5.78))
    if k==4:g.add(label('Q1 ≈ 6,44   ≠   Q1 GỐC = 6',XL,-2.16,18,CORAL,True,5.85))
    g.add(foot('Q1 là ước lượng nội suy; giữ dấu xấp xỉ.'))
    return g,None

def chapter4(k):
    g=VGroup(top('Q2: CÙNG LỚP NHƯ Q1, NHƯNG XA HƠN'))
    g.add(progress_in_class(MAIN,1 if k<=2 else 2))
    if k>=2:g.add(label('n/2 = 20   →   20 − 6 = 14',XL,2.06,17,GOLD,True,5.8))
    if k>=3:g.add(badge('Q2 ≈ 6 + (14/18) × 2 = 7,56',XL,-2.09,GREEN,5.9))
    if k==4:g.add(label('Q1 < Q2, DÙ CÙNG LỚP [6;8)',XL,1.65,16,CORAL,True,6.0))
    g.add(foot('Q2 chính là trung vị ghép nhóm của STAT09.'))
    return g,None

def chapter5(k):
    g=VGroup(top('Q3 VÀ KHOẢNG TỨ PHÂN VỊ'))
    h,X=hist(CLASSES,FREQ,2);g.add(h)
    if k>=2:g.add(badge('30 − 24 = 6   •   f = 14   •   h = 2',XL,1.83,GOLD,5.68))
    if k>=3:g.add(Line((X(8),-.25,0),(X(MAIN[2].value),-.25,0),color=GREEN,stroke_width=9),
                  label(f'Q3 ≈ {num(MAIN[2].value)}',XL,1.21,18,GREEN,True,5.5))
    if k==4:g.add(badge(f'IQR = Q3 − Q1 ≈ {num(IQR)}',XL,-2.18,PURPLE,5.14))
    g.add(foot('Tính hiệu trước khi làm tròn để tránh sai số.'))
    return g,None

def chapter6(k):
    g=VGroup(top('OGIVE: BA ĐƯỜNG NGANG 25% – 50% – 75%'),ogive(k))
    if k>=2:g.add(label('25%  →  Q1',XL,1.89,17,GREEN,True,4.6))
    if k>=3:g.add(label('50%  →  Q2',XL,1.54,17,GOLD,True,4.6))
    if k==4:g.add(label('75%  →  Q3',XL,1.19,17,PURPLE,True,4.6))
    g.add(foot('Đồ thị nội suy và công thức đại số cho cùng kết quả.'))
    return g,None

def chapter7(k):
    g=VGroup(top('RANH GIỚI VÀ ẢNH HƯỞNG CÁCH GHÉP'))
    if k<=2:
        g.add(table(CLASSES,BOUND_FREQ,1 if k==2 else None))
        if k==2:g.add(badge('TÍCH LŨY: 10, 20, 30, 40',XL,-2.23,GOLD,5.2))
    else:
        g.add(table(ASYM,ASYM_FREQ,2))
        if k==3:g.add(badge('CÙNG DỮ LIỆU, RANH GIỚI KHÁC',XL,-2.23,CORAL,5.4))
        if k==4:g.add(label('Q1=6,50    Q2≈7,67    Q3≈8,78',XL,1.99,16,GREEN,True,5.94))
    g.add(foot('Bảng chỉ cho xấp xỉ; mốc đúng ranh giới cần xét riêng.'))
    return g,None

def chapter8(k):
    g=VGroup(top('BÀI TOÁN NGƯỢC: TÌM TẦN SỐ x'))
    if k<=2:
        g.add(unknown_table())
        if k==1:g.add(badge('TẦN SỐ: 6, x, 32−x, 2',XL,-2.22,CYAN,5.4))
    else:
        g.add(table(CLASSES,REVERSE_FREQ,1 if k==3 else None))
    if k>=2:g.add(badge('Q1 = 6,5   →   6 + 8/x = 6,5',XL,-2.19,GOLD,5.5))
    if k>=3:g.add(label('x = 16     /     Q2 = 7,75     /     Q3 = 9',XL,2.04,16,GREEN,True,5.99))
    if k==4:g.add(label('IQR = 9 − 6,5 = 2,5',XL,1.65,18,PURPLE,True,5.4))
    g.add(foot('Kiểm tra lại tổng 40 và các mốc tích lũy 10,20,30.'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)

class STAT10(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 10 / TỨ PHÂN VỊ GHÉP NHÓM',0,3.47,20,WHITE,True,13.1),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,12,MUTED,maxw=13))
        return o

    def notes(self,b):
        o=VGroup()
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        o.add(label(ti,XR,2.17,23,WHITE,True,5.72,1.2),
              Line((.70,.81,0),(6.16,.81,0),color=EDGE,stroke_width=1),
              label(th,XR,-.04,21,GOLD,True,5.67,1.54))
        formula=ROOT/'assets/stat10_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not formula.is_file():
            raise FileNotFoundError(f'STAT10 Typst SVG missing: {formula}; run scripts/build_stat10_typst.py')
        if b.step>=3:
            svg=SVGMobject(str(formula))
            if svg.width>5.26:svg.scale_to_fit_width(5.26)
            if svg.height>.86:svg.scale_to_fit_height(.86)
            svg.move_to((XR,-1.55,0))
            o.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.96,14,CYAN,True),svg)
        else:
            o.add(label('TÍCH LŨY  →  LỚP  →  NỘI SUY',XR,-1.52,17,GREEN,True,5.8))
        o.add(label('TỨ PHÂN VỊ TỪ BẢNG GHÉP NHÓM LÀ GIÁ TRỊ ƯỚC LƯỢNG',XR,-2.47,12,MUTED,maxw=5.84))
        return o

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat10/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat10.py first')
        plan=json.loads(path.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT10' or len(plan.get('beats',[]))!=32:
            raise ValueError('Invalid STAT10 plan')
        previous_visual=previous_notes=None
        for i,b in enumerate(BEATS):
            p=plan['beats'][i]
            if (p['chapter'],p['step'])!=(b.chapter,b.step):
                raise ValueError(f'STAT10 beat mismatch at {i+1}')
            seconds=float(p['duration']);used=0
            if p.get('voice'):
                sound=ROOT/p['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,_=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            if previous_visual is None:
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.4);used=1.4
            else:
                self.play(FadeOut(previous_visual),FadeOut(previous_notes),run_time=.56);used+=.56
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.12);used+=1.12
            self.wait(.45);used+=.45
            if seconds<=used:raise ValueError(f'Beat too short: {i+1}')
            self.wait(seconds-used)
            previous_visual,previous_notes=visual,notes

class STAT10_SMOKE(STAT10):
    """A real low-res Manim render of all 32 visual and Typst states."""
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            self.add(visual,notes)
            self.wait(.14)
            self.remove(visual,notes)
