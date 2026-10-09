"""STAT09: Grouped-data median. Data-driven Manim + SVG compiled from Typst.
Render: manim -ql -r 854,480 --fps 24 stat09/scene.py STAT09
Smoke: manim -ql -r 426,240 --fps 8 stat09/scene.py STAT09_SMOKE
"""
from __future__ import annotations
import json, sys, textwrap
from pathlib import Path
from manim import *
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stat07.scene import (label, top, foot, badge, ruled_axis, raw_points,
    bar, frequency_table, XL, XR, BG, PANEL, EDGE, WHITE, MUTED, CYAN,
    GOLD, GREEN, CORAL, PURPLE)
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ, CUM, ASYM, ASYM_FREQ, PCLASSES, PFREQ, PRACTICE
from stat09.lesson import (BEATS, MAIN, ALTERNATIVE, EXERCISE, RAW_MEDIAN,
    BOUND, BOUND_CLASSES, BOUND_COUNTS, EXERCISE_RAW)

config.background_color = BG
config.frame_width = 14.222222
config.frame_height = 8
COLORS = (CYAN, GREEN, PURPLE, CORAL)
FORM_KEYS = ('raw_vs_grouped', 'cumulative', 'median_class', 'interpolation',
             'ogive', 'regroup', 'boundary', 'practice')


def headline(txt):
    return label(txt,XL,2.42,18,CYAN,True,6.08)


def marker(X,v,y0,y1,txt,color=GOLD):
    return VGroup(Line((X(v),y0,0),(X(v),y1,0),stroke_width=3,color=color),
                  Dot((X(v),y1,0),radius=.07,color=color),
                  label(txt,X(v),y1+.24,15,color,True,1.65))


def hist(classes, freq, y=-1.57, selected=None, factor=.12):
    line,X=ruled_axis(classes[0].left,classes[-1].right,y,
        tuple(sorted({v for iv in classes for v in (iv.left,iv.right)})))
    g=VGroup(line)
    for i,(iv,f) in enumerate(zip(classes,freq)):
        color=GOLD if i==selected else COLORS[i%4]
        g.add(bar(X,iv.left,iv.right,f*factor,y,color),
              label(str(f),X(iv.midpoint),y+f*factor+.19,15,color,True,1.3))
    return g,X


def cum_table(classes,freq,highlight=None):
    running=0
    g=VGroup(label('KHOẢNG',-5.06,1.55,13,CYAN,True,2.2),
             label('TẦN SỐ',-3.35,1.55,13,CYAN,True,1.25),
             label('TÍCH LŨY',-1.62,1.55,13,CYAN,True,1.5))
    for i,(c,f) in enumerate(zip(classes,freq)):
        running+=f
        y=.93-.69*i
        if i==highlight:
            g.add(RoundedRectangle(width=5.63,height=.51,corner_radius=.06,
                    stroke_color=GOLD,stroke_width=1.4,fill_color=EDGE,
                    fill_opacity=.38).move_to((XL,y,0)))
        ctext=GOLD if i==highlight else WHITE
        g.add(label(c.caption,-5.04,y,17,ctext,True,2.07),
              label(str(f),-3.34,y,18,ctext,True,1.14),
              label(str(running),-1.60,y,18,ctext,True,1.16))
    return g


def chapter1(k):
    g=VGroup(headline('TRUNG VỊ GỐC VÀ TRUNG VỊ GHÉP NHÓM'))
    ax,X=ruled_axis(4,12,-1.46,tuple(range(4,13)))
    if k<=2:
        g.add(ax,raw_points(SCORES,X,-1.23,.039))
        if k>=2:g.add(marker(X,7,-1.40,1.13,'TRUNG VỊ = 7',GOLD))
    else:
        bars,X=hist(CLASSES,FREQ,selected=1)
        g.add(bars)
        if k==4:g.add(marker(X,MAIN.value,-1.55,1.16,'≈ 7,56'))
    if k>=3:g.add(badge('BẢNG CHỈ GIỮ TẦN SỐ, KHÔNG GIỮ TỪNG ĐIỂM',XL,1.84,GREEN,5.89))
    g.add(foot('Trung vị từ điểm gốc chính xác; từ bảng ghép nhóm là nội suy.'))
    return g,None


def chapter2(k):
    g=VGroup(headline('TẦN SỐ TÍCH LŨY → VỊ TRÍ TRUNG VỊ'))
    g.add(cum_table(CLASSES,FREQ,1 if k>=3 else None))
    if k>=2:g.add(badge('n = 40     →     n/2 = 20',XL,-2.16,GOLD,4.65))
    if k>=3:g.add(label('6 < 20 < 24',XL,-1.66,17,GREEN,True,4.6))
    if k==4:g.add(label('MỐC 20 THUỘC LỚP THỨ HAI',XL,1.92,16,GOLD,True,5.8))
    g.add(foot('Đọc số đã cộng trước và sau lớp, không dựa vào tần số lớn nhất.'))
    return g,None


def chapter3(k):
    g=VGroup(headline('XÁC ĐỊNH BỐN ĐẠI LƯỢNG NỘI SUY'))
    chart,X=hist(CLASSES,FREQ,selected=1,factor=.115)
    g.add(chart)
    if k>=2:g.add(marker(X,6,-1.54,1.14,'L = 6',CYAN))
    if k>=3:g.add(label('TRƯỚC LỚP: 6     •     TRONG LỚP: 18',XL,1.81,16,GOLD,True,5.9))
    if k==4:g.add(badge('ĐỘ RỘNG h = 8 − 6 = 2',XL,1.29,GREEN,4.68))
    g.add(foot('Lớp trung vị [6;8): cận trái 6, tần số 18, tích lũy trước 6.'))
    return g,None


def chapter4(k):
    g=VGroup(headline('NỘI SUY: ĐI 14 TRONG 18 QUAN SÁT'))
    base=-.78
    ax,X=ruled_axis(6,8,base,(6,6.5,7,7.5,8))
    g.add(ax,Line((X(6),base+.35,0),(X(8),base+.35,0),color=EDGE,stroke_width=11))
    if k>=2:
        g.add(Line((X(6),base+.35,0),(X(MAIN.value),base+.35,0),color=GOLD,stroke_width=11),
              label('14 / 18 ĐỘ DÀI LỚP',XL,1.52,19,GOLD,True,5.7))
    if k>=3:g.add(marker(X,MAIN.value,base,1.0,'≈ 7,56',GREEN))
    if k==4:g.add(badge('6 + (20 − 6) / 18 × 2',XL,-1.79,CYAN,5.33))
    g.add(foot('Nội suy giả định tích lũy tăng tuyến tính trong lớp [6;8).'))
    return g,None


def chapter5(k):
    g=VGroup(headline('ĐỒ THỊ TẦN SỐ TÍCH LŨY / OGIVE'))
    x0,x1=-6.04,-.86; y0=-1.60; dy=.077
    X=lambda x:x0+(x-4)*(x1-x0)/8
    Y=lambda n:y0+n*dy
    g.add(Line((x0,y0,0),(x1,y0,0),color=MUTED,stroke_width=1.2),
          Line((x0,y0,0),(x0,Y(40),0),color=MUTED,stroke_width=1.2))
    pts=[(4,0),(6,6),(8,24),(10,38),(12,40)]
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1]
        g.add(Line((X(a[0]),Y(a[1]),0),(X(b[0]),Y(b[1]),0),color=CYAN,stroke_width=3))
    for xx,yy in pts:
        g.add(Dot((X(xx),Y(yy),0),radius=.065,color=GOLD),
              label(str(yy),X(xx),Y(yy)+.18,12,GOLD,True,.8),
              label(str(xx),X(xx),y0-.28,12,MUTED))
    if k>=2:
        g.add(Line((x0,Y(20),0),(X(MAIN.value),Y(20),0),color=GREEN,stroke_width=2),
              label('n/2 = 20',x0+.80,Y(20)+.20,15,GREEN,True,1.7))
    if k>=3:
        g.add(Line((X(MAIN.value),Y(20),0),(X(MAIN.value),y0,0),color=GOLD,stroke_width=2),
              Dot((X(MAIN.value),Y(20),0),radius=.10,color=GOLD))
    if k==4:g.add(badge('HOÀNH ĐỘ ≈ 7,56',XL,1.91,GREEN,3.9))
    g.add(foot('Đường nối thẳng giữa hai biên lớp là mô hình xấp xỉ.'))
    return g,None


def chapter6(k):
    g=VGroup(headline('ĐỔI CÁCH GHÉP: ƯỚC LƯỢNG THAY ĐỔI'))
    if k<=2:
        g.add(cum_table(CLASSES,FREQ,1))
        g.add(badge('BẢNG A  →  M_e ≈ 7,56',XL,-2.13,GOLD,4.4))
    else:
        g.add(cum_table(ASYM,ASYM_FREQ,2))
        g.add(badge('BẢNG B  →  M_e ≈ 7,67',XL,-2.13,GREEN,4.4))
    if k==4:g.add(label('TRUNG VỊ GỐC VẪN BẰNG 7',XL,2.00,16,CORAL,True,5.65))
    g.add(foot('Thay ranh giới lớp không làm thay đổi 40 điểm dữ liệu ban đầu.'))
    return g,None


def chapter7(k):
    g=VGroup(headline('MỐC n/2 TRÙNG RANH GIỚI LỚP'))
    g.add(cum_table(BOUND_CLASSES,BOUND_COUNTS,1 if k<=2 else 2))
    if k>=2:g.add(badge('n = 20  →  n/2 = 10',XL,-2.16,GOLD,4.0))
    if k>=3:g.add(label('LỚP TRÁI KẾT THÚC: 4   /   LỚP PHẢI BẮT ĐẦU: 4',XL,1.93,14,GREEN,True,6.0))
    if k==4:g.add(badge('M_e ≈ 4: CÙNG MỘT RANH GIỚI',XL,-1.73,CYAN,5.25))
    g.add(foot('Khi tích lũy bằng n/2 đúng biên, hai cách xét biên cho cùng giá trị.'))
    return g,None


def chapter8(k):
    g=VGroup(headline('TỰ LUYỆN: 20 THỜI LƯỢNG HỌC TẬP'))
    g.add(cum_table(PCLASSES,PFREQ,1 if k>=2 else None))
    if k>=2:g.add(badge('n/2 = 10  →  LỚP [4;6)',XL,-2.13,GOLD,4.6))
    if k>=3:g.add(label('4 + (10 − 5) / 7 × 2 ≈ 5,43',XL,1.92,18,GREEN,True,5.85))
    if k==4:g.add(badge('TRUNG VỊ GỐC = 5',XL,-1.73,CORAL,4.0))
    g.add(foot('Bài kiểm chứng: đọc đúng tích lũy, lớp, tần số, độ rộng.'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)

class STAT09(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,
                fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 09 / TRUNG VỊ GHÉP NHÓM',0,3.47,20,WHITE,True,13.1),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,12,MUTED,maxw=13))
        return o

    def notes(self,b):
        o=VGroup()
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        o.add(label(ti,XR,2.17,23,WHITE,True,5.72,1.2),
              Line((.70,.80,0),(6.16,.80,0),color=EDGE,stroke_width=1),
              label(th,XR,-.02,21,GOLD,True,5.69,1.54))
        formula=ROOT/'assets'/'stat09_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not formula.is_file():
            raise FileNotFoundError(f'Missing Typst SVG: {formula}; run scripts/build_stat09_typst.py')
        if b.step>=3:
            svg=SVGMobject(str(formula))
            if svg.width>5.35:svg.scale_to_fit_width(5.35)
            if svg.height>.87:svg.scale_to_fit_height(.87)
            svg.move_to((XR,-1.55,0))
            o.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.96,14,CYAN,True),svg)
        else:
            o.add(label('TÍCH LŨY → LỚP → NỘI SUY',XR,-1.50,16,GREEN,True,5.86))
        o.add(label('TRUNG VỊ GHÉP NHÓM LÀ ƯỚC LƯỢNG, KHÔNG PHẢI TRUNG VỊ GỐC',XR,-2.47,12,MUTED,maxw=5.86))
        return o

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat09/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat09.py first')
        plan=json.loads(path.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT09' or len(plan.get('beats',[]))!=32:
            raise ValueError('Invalid STAT09 runtime plan')
        old_visual=old_notes=None
        for i,b in enumerate(BEATS):
            p=plan['beats'][i]
            if (p['chapter'],p['step'])!=(b.chapter,b.step):raise ValueError(f'Beat mismatch {i}')
            duration=float(p['duration']);used=0.0
            if p.get('voice'):
                sound=ROOT/p['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,_=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.4);used=1.4
            else:
                self.play(FadeOut(old_visual),FadeOut(old_notes),run_time=.56);used+=.56
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.12);used+=1.12
            self.wait(.45);used+=.45
            if duration<=used:raise ValueError(f'Beat {i} too short: {duration}')
            self.wait(duration-used)
            old_visual,old_notes=visual,notes

class STAT09_SMOKE(STAT09):
    """Actually render 32 states and Typst SVGs on GitHub (low-res)."""
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            self.add(visual,notes)
            self.wait(.14)
            self.remove(visual,notes)
