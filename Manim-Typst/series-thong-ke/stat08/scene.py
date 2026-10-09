"""STAT08 – Mean and mode of grouped data, Manim + Typst.
Usage: python scripts/build_stat08_typst.py && python scripts/prepare_stat08.py --voice off
       manim -ql -r 854,480 --fps 24 stat08/scene.py STAT08
       manim -ql -r 426,240 --fps 8 stat08/scene.py STAT08_SMOKE
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import (label,top,foot,badge,ruled_axis,raw_points,bar,
                          frequency_table,XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,
                          GREEN,CORAL,PURPLE)
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,ASYM,ASYM_FREQ,ASYM_DENS,PCLASSES,PFREQ
from stat08.lesson import (BEATS,CHAPTERS,EXACT_MEAN,GROUPED_MEAN,GROUPED_MODE,
                           ASYM_MEAN,ASYM_MODE,PRACTICE_MEAN,PRACTICE_MODE)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
FORM_KEYS=('midpoints','weighted_mean','raw_vs_grouped','new_partition',
           'mode_interpolation','density_mode','reverse_count','practice')

COLORS=(CYAN,GREEN,PURPLE,CORAL)

def headline(text):
    return label(text,XL,2.37,19,CYAN,True,6.05)

def hist(classes,counts,*,densities=False,y=-1.53,scale=.09,with_text=True,highlight=None):
    ax,X=ruled_axis(classes[0].left,classes[-1].right,y,
                     tuple(sorted({v for iv in classes for v in (iv.left,iv.right)})))
    g=VGroup(ax)
    for i,(iv,n) in enumerate(zip(classes,counts)):
        value=n/iv.width if densities else n
        h=value*scale
        color=GOLD if highlight==i else COLORS[i]
        g.add(bar(X,iv.left,iv.right,h,y,color))
        if with_text:
            g.add(label(f'{value:g}',X(iv.midpoint),y+h+.17,17,color,True,maxw=1.2),
                  label(iv.caption,X(iv.midpoint),y-.50,12,MUTED,maxw=1.4))
    return g,X

def mean_marker(X,val,low=-1.45,high=1.20,color=GOLD,title=None):
    return VGroup(Line((X(val),low,0),(X(val),high,0),stroke_width=3,color=color),
                  Dot((X(val),high,0),radius=.075,color=color),
                  label(title or f'{val:.2f}'.replace('.',','),X(val),high+.32,15,color,True,maxw=1.7))

def chapter1(k):
    g=VGroup(headline('TỪ 40 ĐIỂM → GIÁ TRỊ ĐẠI DIỆN'))
    axis,X=ruled_axis(4,12,-1.48,tuple(range(4,13)));g.add(axis)
    if k==1:
        g.add(raw_points(SCORES,X,-1.25,.044))
    elif k==2:
        g.add(raw_points(SCORES,X,-1.25,.040))
        g.add(mean_marker(X,5,-1.48,.95,CYAN,'5'),mean_marker(X,7,-1.48,.95,GREEN,'7'),
              mean_marker(X,9,-1.48,.95,PURPLE,'9'),mean_marker(X,11,-1.48,.95,CORAL,'11'))
    else:
        histg,_=hist(CLASSES,FREQ,y=-1.48,scale=.116)
        g.add(histg)
    if k>=3:g.add(badge('TRUNG ĐIỂM  5  •  7  •  9  •  11',XL,1.70,GOLD,5.6))
    if k==4:g.add(badge('TỔNG TẦN SỐ = 40',XL,1.04,GREEN,3.7))
    g.add(foot('Trung điểm đại diện cho lớp; không phải điểm thật của từng em.'))
    return g,None

def chapter2(k):
    g=VGroup(headline('TRUNG BÌNH = TỔNG CÓ TRỌNG SỐ'))
    labels=('5 × 6 = 30','7 × 18 = 126','9 × 14 = 126','11 × 2 = 22')
    for i,(txt,c) in enumerate(zip(labels,COLORS)):
        y=1.55-i*.81
        g.add(RoundedRectangle(width=5.3,height=.59,corner_radius=.075,fill_color=PANEL,
                fill_opacity=1,stroke_color=c,stroke_width=1.5).move_to((XL,y,0)))
        g.add(label(txt,XL,y,19,c,True,5.0))
        if k>i:g.add(Dot((-6.23,y,0),radius=.07,color=GOLD))
    if k>=2:g.add(label('TỔNG CÓ TRỌNG SỐ = 304',XL,-2.17,18,GOLD,True,5.8))
    if k>=3:g.add(label('304 / 40 = 7,6',XL,2.38,17,GREEN,True,5.6))
    g.add(foot('Chia cho tổng tần số n = 40, không chia số lớp.'))
    return g,None

def chapter3(k):
    g=VGroup(headline('TRUNG BÌNH CHÍNH XÁC ≠ ƯỚC LƯỢNG'))
    axis,X=ruled_axis(4,12,-1.3,tuple(range(4,13)));g.add(axis)
    g.add(raw_points(SCORES,X,-1.18,.039))
    if k>=2:g.add(mean_marker(X,EXACT_MEAN,-1.35,1.04,GREEN,'GỐC 7,1'))
    if k>=3:g.add(mean_marker(X,GROUPED_MEAN,-1.35,.44,GOLD,'GHÉP 7,6'))
    if k==4:
        g.add(badge('CÙNG BẢNG ≠ CÙNG DỮ LIỆU CHI TIẾT',XL,1.80,CORAL,5.95))
    g.add(foot('Thay từng quan sát bằng trung điểm làm mất thông tin.'))
    return g,None

def chapter4(k):
    g=VGroup(headline('ĐỔI CÁCH GHÉP → ĐỔI ƯỚC LƯỢNG'))
    if k<=2:
        classes,frequency=CLASSES,FREQ
        mean=GROUPED_MEAN
    else:
        classes,frequency=ASYM,ASYM_FREQ
        mean=ASYM_MEAN
    chart,X=hist(classes,frequency,y=-1.55,scale=.100 if k<=2 else .085)
    g.add(chart)
    g.add(mean_marker(X,mean,-1.48,.95,GOLD,f'{mean:.2f}'.replace('.',',')))
    if k>=2:g.add(label('NHÓM A: 7,60',XL,1.89,16,GREEN,True))
    if k>=3:g.add(label('NHÓM B: 7,65',XL,1.47,16,CYAN,True))
    if k==4:g.add(badge('GỐC VẪN 7,10',XL,.99,CORAL,3.2))
    g.add(foot('Cách chia khoảng thay đổi, 40 quan sát ban đầu không đổi.'))
    return g,None

def chapter5(k):
    g=VGroup(headline('LỚP MỐT VÀ NỘI SUY TẦN SỐ'))
    plot,X=hist(CLASSES,FREQ,y=-1.58,scale=.128,highlight=1)
    g.add(plot)
    if k>=2:
        g.add(label('d₁ = 18 − 6 = 12',XL,1.81,17,GOLD,True,5.7),
              label('d₂ = 18 − 14 = 4',XL,1.42,17,GOLD,True,5.7))
    if k>=3:
        g.add(mean_marker(X,GROUPED_MODE,-1.58,.90,GREEN,'MỐT ≈ 7,5'))
    if k==4:
        g.add(badge('MỐT GỐC = 7  •  TRUNG ĐIỂM = 7',XL,2.24,CORAL,5.95))
    g.add(foot('Lớp có tần số cao nhất: [6;8), không đồng nghĩa mốt bằng 18.'))
    return g,None

def chapter6(k):
    g=VGroup(headline('HISTOGRAM: KHI LỚP KHÁC ĐỘ RỘNG'))
    use_density=k>=2
    chart,X=hist(ASYM,ASYM_FREQ,densities=use_density,y=-1.61,
                 scale=.073 if not use_density else .161,highlight=2)
    g.add(chart)
    if k>=2:g.add(label('MẬT ĐỘ = 3  •  8  •  9  •  4',XL,1.71,17,GOLD,True,5.75))
    if k>=3:g.add(mean_marker(X,ASYM_MODE,-1.54,.92,GREEN,'≈ 7,33'))
    if k==4:g.add(badge('NỘI SUY THEO MẬT ĐỘ: PHẦN MỞ RỘNG',XL,2.21,CORAL,6.00))
    g.add(foot('Với lớp không đều, diện tích cột mới đại diện cho tần số.'))
    return g,None

def chapter7(k):
    g=VGroup(headline('BÀI TOÁN NGƯỢC: TẦN SỐ CHƯA BIẾT'))
    counts=(6,'x',14,2) if k==1 else FREQ
    labels=(iv.caption for iv in CLASSES)
    for i,(lab,f) in enumerate(zip(labels,counts)):
        y=1.64-i*.83
        g.add(label(lab,-4.8,y,17,COLORS[i],True,maxw=2.40),
              label(str(f),-2.30,y,20,GOLD if f=='x' else WHITE,True))
    if k>=2:g.add(label('x = 40 − 6 − 14 − 2 = 18',XL,-2.17,17,GREEN,True,5.88))
    if k>=3:g.add(badge('TRUNG BÌNH ≈ 7,6',XL,2.28,GOLD,4.0))
    if k==4:g.add(badge('MỐT NỘI SUY ≈ 7,5',XL,1.90,GREEN,4.3))
    g.add(foot('Tần số phải nguyên không âm; luôn kiểm tổng n.'))
    return g,None

def chapter8(k):
    g=VGroup(headline('TỰ LUYỆN: 20 THỜI LƯỢNG HỌC TẬP'))
    chart,X=hist(PCLASSES,PFREQ,y=-1.58,scale=.225,highlight=1 if k>=3 else None)
    g.add(chart)
    if k>=2:g.add(label('TRUNG BÌNH ≈ 5,5 PHÚT',XL,1.71,17,GREEN,True,5.95))
    if k>=3:g.add(mean_marker(X,PRACTICE_MODE,-1.55,.96,GOLD,'MỐT ≈ 5,33'))
    if k==4:g.add(badge('HÃY NÓI RÕ ĐÓ LÀ ƯỚC LƯỢNG',XL,2.23,GREEN,5.3))
    g.add(foot('Trung điểm → trọng số; lớp mốt → nội suy; kiểm giới hạn.'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)

class STAT08(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 08 / TRUNG BÌNH VÀ MỐT GHÉP NHÓM',0,3.47,21,WHITE,True,13.1),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('THỐNG KÊ LỚP 11   •   ƯỚC LƯỢNG   •   NỘI SUY   •   MANIM–TYPST',0,-3.58,12,MUTED,maxw=13))
        return o
    def notes(self,b):
        o=VGroup(label(f'CHƯƠNG {b.chapter:02d}/08  •  NHỊP {b.step}/4',XR,2.48,16,CYAN,True))
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        o.add(label(ti,XR,1.74,24,WHITE,True,5.68,1.18),
              Line((.70,.80,0),(6.16,.80,0),color=EDGE,stroke_width=1),
              label(th,XR,-.02,21,GOLD,True,5.68,1.52))
        formula=ROOT/'assets'/'stat08_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not formula.exists():
            raise FileNotFoundError(f'No Typst SVG: {formula}; run scripts/build_stat08_typst.py')
        if b.step>=3:
            o_svg=SVGMobject(str(formula))
            if o_svg.width>5.35:o_svg.scale_to_fit_width(5.35)
            if o_svg.height>.86:o_svg.scale_to_fit_height(.86)
            o_svg.move_to((XR,-1.55,0))
            o.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.97,14,CYAN,True),o_svg)
        else:o.add(label('QUAN SÁT → GIẢI THÍCH → ƯỚC LƯỢNG',XR,-1.48,16,GREEN,True,5.85))
        o.add(label('SỐ GHÉP NHÓM LÀ ƯỚC LƯỢNG, KHÔNG TỰ ĐỘNG LÀ SỐ ĐÚNG CỦA DỮ LIỆU GỐC',XR,-2.47,12,MUTED,maxw=5.88))
        return o
    def construct(self):
        self.add(self.frame())
        source=ROOT/'stat08/runtime_plan.json'
        if not source.is_file():raise FileNotFoundError('Run scripts/prepare_stat08.py first')
        plan=json.loads(source.read_text(encoding='utf8'))
        if plan.get('scene')!='STAT08' or len(plan.get('beats',[]))!=32:
            raise ValueError('Invalid STAT08 runtime plan')
        oldv=oldn=None
        for i,b in enumerate(BEATS):
            p=plan['beats'][i]
            if (p['chapter'],p['step'])!=(b.chapter,b.step):
                raise ValueError(f'Beat mismatch {i}')
            slot=float(p['duration']);used=0.0
            if p.get('voice'):
                sound=ROOT/p['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            v,_=VISUALS[b.chapter-1](b.step)
            n=self.notes(b)
            if oldv is None:
                self.play(FadeIn(v),FadeIn(n),run_time=1.4);used=1.4
            else:
                self.play(FadeOut(oldv),FadeOut(oldn),run_time=.56);used+=.56
                self.play(FadeIn(v),FadeIn(n),run_time=1.12);used+=1.12
            self.wait(.45);used+=.45
            if slot<=used:raise ValueError(f'Beat too short {i}: {slot}')
            self.wait(slot-used)
            oldv,oldn=v,n

class STAT08_SMOKE(STAT08):
    """Real rendering of all visual states and 8 Typst SVGs at low quality."""
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(visual,note)
            self.wait(.14)
            self.remove(visual,note)
