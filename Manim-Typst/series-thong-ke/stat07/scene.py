"""STAT07 Manim lecture.
Run: python scripts/build_stat07_typst.py && python scripts/prepare_stat07.py --voice off
Then: manim -ql -r 854,480 --fps 24 stat07/scene.py STAT07
Smoke test: manim -ql -r 426,240 --fps 8 stat07/scene.py STAT07_SMOKE
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from collections import Counter
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat01.lesson import SCORES
from stat07.lesson import (BEATS,CHAPTERS,CLASSES,FREQ,CUM,REL,DENS,ASYM,ASYM_FREQ,ASYM_DENS,
                           PRACTICE,PCLASSES,PFREQ,PCUM,grouped_mean)
config.background_color='#0A1522'
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
BG='#0A1522';PANEL='#10293B';EDGE='#355A71'
WHITE='#EDF6FF';MUTED='#ADC6D5';CYAN='#56CBE9';GOLD='#FFD379'
GREEN='#67DDB5';CORAL='#FF8E87';PURPLE='#B7A9FC'
XL=-3.43;XR=3.43

def label(t,x,y,size=17,color=WHITE,bold=False,maxw=None,maxh=None):
    o=Text(str(t),font=FONT,font_size=size,color=color,
           weight='BOLD' if bold else 'NORMAL',line_spacing=.92)
    if maxw and o.width>maxw:o.scale_to_fit_width(maxw)
    if maxh and o.height>maxh:o.scale_to_fit_height(maxh)
    return o.move_to((x,y,0))
def top(s):return label(s,XL,2.40,18,CYAN,True,6.02)
def foot(s):return label(s,XL,-2.55,12,MUTED,maxw=6.0)
def paneltext(s,x,y,color=WHITE,w=4.8):return label(s,x,y,16,color,maxw=w)
def badge(s,x,y,color=GREEN,width=2.0):
    return VGroup(RoundedRectangle(width=width,height=.51,corner_radius=.07,
       stroke_color=color,stroke_width=1.2,fill_color=PANEL,fill_opacity=1).move_to((x,y,0)),
       label(s,x,y,15,color,True,width-.15))
def ruled_axis(vmin,vmax,y,ticks,lo=-6.03,hi=-.86):
    def X(v):return lo+(float(v)-vmin)*(hi-lo)/(vmax-vmin)
    g=VGroup(Line((lo,y,0),(hi,y,0),color=MUTED,stroke_width=2))
    for t in ticks:
        xx=X(t)
        g.add(Line((xx,y-.08,0),(xx,y+.08,0),stroke_width=1.4,color=MUTED),
              label(f'{t:g}',xx,y-.30,12,MUTED))
    return g,X

def raw_points(values,X,y=-.6,r=.060,color=CYAN):
    g=VGroup(); used=Counter()
    for v in values:
        j=used[v];used[v]+=1
        g.add(Dot((X(v),y+j*.14,0),radius=r,color=color))
    return g

def class_ranges(classes,X,y,with_titles=True):
    g=VGroup()
    for i,c in enumerate(classes):
        color=(CYAN,GREEN,PURPLE,CORAL)[i]
        xa,xb=X(c.left),X(c.right)
        g.add(Line((xa,y,0),(xb,y,0),stroke_width=8,color=color),
              Dot((xa,y,0),radius=.075,color=color),
              Circle(radius=.069,stroke_color=color,stroke_width=2,fill_opacity=1,
                     fill_color=PANEL).move_to((xb,y,0)))
        if with_titles:g.add(label(c.caption,(xa+xb)/2,y+.37,13,color,True,maxw=1.27))
    return g

def bar(X,a,b,h,ybase,color=CYAN):
    if h<0:raise ValueError('negative bar')
    return Rectangle(width=X(b)-X(a),height=max(.001,h),
        stroke_color=EDGE,stroke_width=1.1,fill_color=color,fill_opacity=.68).move_to(((X(a)+X(b))/2,ybase+h/2,0))

def frequency_table(classes,freq,cumul=None,relative=None,selected=None):
    g=VGroup()
    labels=('LỚP','TẦN SỐ','TÍCH LŨY','TỶ LỆ')
    xpos=(-4.95,-3.52,-2.06,-.94)
    for j in range(4 if relative is not None else 3):
        g.add(label(labels[j],xpos[j],1.55,12,CYAN,True,1.17))
    for i,(interval,count) in enumerate(zip(classes,freq)):
        y=.94-i*.63
        if selected==i:
            g.add(RoundedRectangle(width=5.31,height=.48,corner_radius=.065,
                    stroke_color=GOLD,stroke_width=1.0,fill_color=EDGE,fill_opacity=.3).move_to((-3.37,y,0)))
        parts=(interval.caption,str(count),str(cumul[i] if cumul is not None else sum(freq[:i+1])),
               f'{relative[i]*100:.0f}%' if relative is not None else '')
        for j in range(4 if relative is not None else 3):
            g.add(label(parts[j],xpos[j],y,16,(GOLD if selected==i else WHITE),j==1,1.20))
    g.add(Line((-6.0,-1.82,0),(-.72,-1.82,0),color=EDGE,stroke_width=1.1))
    return g

def chapter1(k):
    g=VGroup(top('DỮ LIỆU THÔ → BẢNG GHÉP NHÓM'))
    ax,X=ruled_axis(4,12,-.95,tuple(range(4,13)));g.add(ax)
    tracker=None
    if k==2:
        tracker=ValueTracker(0.0)
        for i,v in enumerate(SCORES):
            idx=next(j for j,c in enumerate(CLASSES) if c.contains(v))
            rank=sum(1 for earlier in SCORES[:i] if CLASSES[idx].contains(earlier))
            x0=X(v);y0=-.76+rank*.105
            x1=X(CLASSES[idx].midpoint)+((rank%4)-1.5)*.085
            y1=-.77+(rank//4)*.21
            g.add(always_redraw(lambda x0=x0,x1=x1,y0=y0,y1=y1,idx=idx:
                  Dot((x0+(x1-x0)*tracker.get_value(),y0+(y1-y0)*tracker.get_value(),0),
                  radius=.045,color=(CYAN,GREEN,PURPLE,CORAL)[idx])))
    elif k==1:g.add(raw_points(SCORES,X,-.83,.044))
    else:
        for i,c in enumerate(CLASSES):
            count=FREQ[i]; color=(CYAN,GREEN,PURPLE,CORAL)[i]
            g.add(bar(X,c.left,c.right,count*.105,-.95,color))
            g.add(label(str(count),X(c.midpoint),-.75+count*.105,17,color,True))
    if k>=2:g.add(class_ranges(CLASSES,X,-1.66,k<=2))
    if k>=3:g.add(label('6      18      14       2',XL,1.70,23,GOLD,True,5.9))
    if k>=4:g.add(badge('TỔNG = 40',XL,1.28,GREEN,3.3))
    g.add(foot('Mỗi điểm thuộc duy nhất một lớp nửa kín.'))
    return g,tracker

def chapter2(k):
    g=VGroup(top('RANH GIỚI LỚP: TRÁNH ĐẾM TRÙNG'))
    ax,X=ruled_axis(4,12,-1.15,tuple(range(4,13)));g.add(ax)
    g.add(class_ranges(CLASSES,X,-.55,True))
    v=(5,6,8,10)[k-1]
    g.add(Dot((X(v),.33,0),radius=.16,color=GOLD),
          Line((X(v),-.50,0),(X(v),.23,0),stroke_width=3,color=GOLD))
    ix=next(i for i,c in enumerate(CLASSES) if c.contains(v))
    g.add(badge(f'{v} THUỘC {CLASSES[ix].caption}',XL,1.55,GREEN,4.8))
    if k>=3:g.add(label('BÊN TRÁI: NHẬN   •   BÊN PHẢI: LOẠI',XL,-2.10,16,CYAN,True,5.95))
    g.add(foot('Các lớp liền nhau, không chồng lấn và phủ dữ liệu.'))
    return g,None

def chapter3(k):
    g=VGroup(top('TẦN SỐ VÀ TẦN SỐ TÍCH LŨY'))
    g.add(frequency_table(CLASSES,FREQ,CUM,selected=k-1))
    if k>=2:g.add(badge('6 → 24 → 38 → 40',XL,-2.21,GOLD,4.7))
    if k>=3:g.add(label('DƯỚI 8 ĐIỂM: 24 HỌC SINH',XL,2.10,15,GREEN,True,6.0))
    g.add(foot('Tích lũy không giảm và kết thúc ở tổng 40.'))
    return g,None

def chapter4(k):
    g=VGroup(top('TẦN SỐ TƯƠNG ĐỐI: SO SÁNH CÔNG BẰNG'))
    if k<3:
        g.add(frequency_table(CLASSES,FREQ,CUM,REL,selected=(k-1)))
        g.add(badge('15% + 45% + 35% + 5% = 100%',XL,-2.22,GREEN,5.5))
    else:
        vals=(40,50)
        for i,(name,pct) in enumerate((('LỚP A: 16/40',.40),('LỚP B: 25/50',.50))):
            y=.76-i*1.13
            g.add(label(name,-5.23,y+.38,16,(CYAN,CORAL)[i],True,2.5),
                  RoundedRectangle(width=4.7,height=.39,corner_radius=.03,
                       fill_color=EDGE,fill_opacity=.35,stroke_width=0).move_to((-3.55,y-.12,0)),
                  Rectangle(width=4.7*pct,height=.39,fill_color=(CYAN,CORAL)[i],
                     fill_opacity=.85,stroke_width=0).move_to((-5.9+4.7*pct/2,y-.12,0)),
                  label(f'{pct*100:.0f}%',-1.15,y+.38,19,GOLD,True))
        if k>=4:g.add(badge('TÍCH LŨY: 15%  60%  95%  100%',XL,-1.78,GREEN,5.45))
    g.add(foot('Cùng tiêu chí, khác sĩ số → so sánh tỷ lệ.'))
    return g,None

def chapter5(k):
    g=VGroup(top('HISTOGRAM: DIỆN TÍCH CỘT = TẦN SỐ'))
    uneven=k>=2
    classes=ASYM if uneven else CLASSES
    freq=ASYM_FREQ if uneven else FREQ
    dens=ASYM_DENS if uneven else DENS
    ax,X=ruled_axis(4,12,-1.72,(4,5,6,7,8,9,10,11,12));g.add(ax)
    heights=(dens if uneven else freq)
    scale=.153 if uneven else .091
    for i,(iv,value) in enumerate(zip(classes,heights)):
        h=value*scale
        g.add(bar(X,iv.left,iv.right,h,-1.72,(CYAN,GREEN,PURPLE,CORAL)[i]))
        g.add(label(f'{value:g}',X(iv.midpoint),-1.52+h,16,GOLD,True))
        g.add(label(iv.caption,X(iv.midpoint),-2.13,12,MUTED,False,maxw=1.4))
    if k>=3:g.add(badge('MẬT ĐỘ = TẦN SỐ / ĐỘ RỘNG',XL,1.90,GREEN,5.4))
    if k>=4:g.add(label('6 + 8 + 18 + 8 = 40 = TỔNG DIỆN TÍCH',XL,1.32,14,GOLD,True,5.98))
    g.add(foot('Nếu lớp rộng khác nhau, đừng lấy tần số làm chiều cao.'))
    return g,None

def chapter6(k):
    g=VGroup(top('BẢNG GHÉP NHÓM KHÔNG GIỮ HẾT DỮ LIỆU'))
    g.add(frequency_table(CLASSES,FREQ,CUM,selected=1 if k<=2 else None))
    if k<=2:
        g.add(label('TRONG [6;8): 8 ĐIỂM 6 + 10 ĐIỂM 7',XL,-2.24,15,GOLD,True,5.9))
    else:
        g.add(badge('TRUNG ĐIỂM: 5, 7, 9, 11',XL,-2.16,PURPLE,4.7))
        g.add(label('TB GỐC = 7,1' if k==3 else 'ƯỚC LƯỢNG GHÉP NHÓM = 7,6',XL,2.12,17,GOLD,True,5.9))
    g.add(foot('Giữ dữ liệu gốc để tính chính xác khi có thể.'))
    return g,None

def chapter7(k):
    g=VGroup(top('CÙNG 40 ĐIỂM – NHIỀU CÁCH CHIA LỚP'))
    classes=CLASSES if k in (1,3) else ASYM
    freq=FREQ if classes==CLASSES else ASYM_FREQ
    dens=DENS if classes==CLASSES else ASYM_DENS
    ax,X=ruled_axis(4,12,-1.70,(4,5,6,7,8,9,10,11,12));g.add(ax)
    for i,c in enumerate(classes):
        h=(dens[i] if k>=3 else freq[i])* (.15 if k>=3 else .087)
        g.add(bar(X,c.left,c.right,h,-1.7,(CYAN,GREEN,PURPLE,CORAL)[i]),
              label(str(freq[i]),X(c.midpoint),-1.48+h,16,GOLD,True))
    if k==1:g.add(label('CÁCH A: 6 – 18 – 14 – 2',XL,1.95,19,GREEN,True,5.7))
    elif k==2:g.add(label('CÁCH B: 6 – 8 – 18 – 8',XL,1.95,19,GREEN,True,5.7))
    else:g.add(label('DIỆN TÍCH, KHÔNG PHẢI CHỈ CHIỀU CAO',XL,1.95,16,GOLD,True,5.9))
    g.add(foot('Đổi ranh giới có thể đổi hình dạng các cột.'))
    return g,None

def chapter8(k):
    g=VGroup(top('LUYỆN TẬP: 20 THỜI LƯỢNG (PHÚT)'))
    if k==1:
        ax,X=ruled_axis(2,10,-1.62,tuple(range(2,11)));g.add(ax,raw_points(PRACTICE,X,-1.40,.068,CYAN),
                 class_ranges(PCLASSES,X,-2.00,True))
        g.add(label('20 QUAN SÁT GIẢ LẬP',XL,1.91,19,GOLD,True,5.5))
    else:
        g.add(frequency_table(PCLASSES,PFREQ,PCUM,
                              tuple(v/20 for v in PFREQ) if k>=3 else None,
                              selected=(k-2) if k<=3 else None))
        if k>=3:g.add(label('DƯỚI 6 PHÚT: 12  •  TỪ 6 PHÚT: 8',XL,-2.22,15,GREEN,True,5.8))
        if k==4:g.add(label('5 + 7 + 6 + 2 = 20',XL,2.09,17,GOLD,True))
    g.add(foot('Đủ → đúng → nhất quán → trình bày trung thực.'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)
FORM_KEYS=('intervals','boundary','cumulative','relative','density','approximation','grouping','practice')

class STAT07(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH  /  THỐNG KÊ 07  /  MẪU SỐ LIỆU GHÉP NHÓM',0,3.47,22,WHITE,True,13.1),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('THỐNG KÊ LỚP 11   •   BẢNG TẦN SỐ   •   HISTOGRAM   •   MANIM–TYPST',0,-3.58,12,MUTED,maxw=13))
        return o
    def notes(self,b):
        o=VGroup(label(f'CHƯƠNG {b.chapter:02d}/08  •  NHỊP {b.step}/4',XR,2.48,16,CYAN,True))
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,35,break_long_words=False))
        o.add(label(ti,XR,1.74,25,WHITE,True,5.68,1.18),
              Line((.70,.80,0),(6.16,.80,0),color=EDGE,stroke_width=1),
              label(th,XR,-.02,22,GOLD,True,5.68,1.52))
        formula=ROOT/'assets'/'stat07_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not formula.exists():raise FileNotFoundError(f'Missing Typst SVG: {formula}; run scripts/build_stat07_typst.py')
        if b.step>=3:
            o_svg=SVGMobject(str(formula))
            if o_svg.width>5.35:o_svg.scale_to_fit_width(5.35)
            if o_svg.height>.86:o_svg.scale_to_fit_height(.86)
            o_svg.move_to((XR,-1.55,0))
            o.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.97,14,CYAN,True),o_svg)
        else:
            o.add(label('QUAN SÁT → DỰ ĐOÁN → KIỂM CHỨNG',XR,-1.48,16,GREEN,True,5.85))
        o.add(label('GHÉP NHÓM = TÓM TẮT DỮ LIỆU; KHÔNG PHẢI GIỮ NGUYÊN MỌI CHI TIẾT',XR,-2.47,12,MUTED,maxw=5.9))
        return o
    def construct(self):
        self.add(self.frame())
        source=ROOT/'stat07/runtime_plan.json'
        if not source.is_file():raise FileNotFoundError('Run python scripts/prepare_stat07.py --voice off')
        plan=json.loads(source.read_text(encoding='utf8'))
        if plan.get('scene')!='STAT07' or len(plan.get('beats',[]))!=32:raise ValueError('Invalid STAT07 runtime plan')
        prev_visual=prev_notes=None
        for i,b in enumerate(BEATS):
            p=plan['beats'][i]
            if (p['chapter'],p['step'])!=(b.chapter,b.step):raise ValueError(f'Beat mismatch {i}')
            slot=float(p['duration']);used=0
            if p.get('voice'):
                sound=ROOT/p['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if prev_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.4);used=1.4
            else:
                self.play(FadeOut(prev_visual),FadeOut(prev_notes),run_time=.56);used+=.56
                self.play(FadeIn(visual),FadeIn(note),run_time=1.12);used+=1.12
            if tracker is not None:
                self.play(tracker.animate.set_value(1),run_time=4.0,rate_func=smooth);used+=4
            else:
                self.wait(.45);used+=.45
            if slot<=used:raise ValueError(f'Beat too short {i}')
            self.wait(slot-used)
            prev_visual,prev_notes=visual,note

class STAT07_SMOKE(STAT07):
    """Smoke-render all 32 visual states and all 8 compiled Typst SVGs."""
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            vis,_=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            self.add(vis,notes)
            self.wait(.14)
            self.remove(vis,notes)
