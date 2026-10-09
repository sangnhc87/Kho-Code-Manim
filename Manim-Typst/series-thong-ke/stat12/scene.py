"""STAT12 classroom lecture: grouped variance & standard deviation."""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import (label,top,foot,badge,ruled_axis,raw_points,bar,
    XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE)
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ
from stat12.lesson import (BEATS,MAIN,RAW,OTHER,OTHER_FREQ,OUTLIER_RAW,
    PRACTICE,PRACTICE_CLASSES,PRACTICE_FREQ)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
PALETTE=(CYAN,GREEN,PURPLE,CORAL)
FORM_KEYS=('intro','centers','variance','shortcut','compare','transforms','outlier','practice')

def fmt(v,digits=2):return f'{v:.{digits}f}'.replace('.',',')

def base_axis(lo=4,hi=12,y=-1.53):
    return ruled_axis(lo,hi,y,tuple(range(lo,hi+1,2)))

def histogram(freq=FREQ,classes=CLASSES,lo=4,hi=12,y=-1.62,height_scale=.103,selected=None,headings=True):
    ax,X=base_axis(lo,hi,y);g=VGroup(ax)
    for i,(c,f) in enumerate(zip(classes,freq)):
        col=GOLD if i==selected else PALETTE[i%4]
        h=f*height_scale
        g.add(bar(X,c.left,c.right,h,y,col))
        if headings:
            g.add(label(str(f),X(c.midpoint),y+h+.23,16,col,True,1.0))
    return g,X

def mean_line(X,center=7.6,y0=-1.6,y1=1.36,color=GOLD):
    xx=X(center)
    return VGroup(Line((xx,y0,0),(xx,y1,0),stroke_width=2.7,color=color),
                  label('TRUNG BÌNH',xx,y1+.28,13,color,True,1.85))

def text_list(items,ys,x=-3.45):
    return VGroup(*[label(t,x,y,17,c,True,5.5) for (t,c),y in zip(items,ys)])

def vis1(k):
    g=VGroup(top('DỮ LIỆU VÀ ĐỘ PHÂN TÁN'))
    h,X=histogram();g.add(h)
    if k>=2:g.add(mean_line(X))
    if k==3:
        g.add(badge('40 ĐIỂM, 4 LỚP',XL,1.94,GOLD,3.50))
    if k==4:
        g.add(badge('CHỈ BIẾT TẦN SỐ, CHƯA BIẾT TỪNG ĐIỂM',XL,1.94,GOLD,5.9))
    g.add(foot('Trung bình chỉ nói vị trí trung tâm.'))
    return g,None

def vis2(k):
    g=VGroup(top('TRUNG ĐIỂM LỚP VÀ TRỌNG SỐ'))
    h,X=histogram(selected=(k-1) if k<=4 else None);g.add(h)
    if k>=2:
        for i,c in enumerate(CLASSES):
            g.add(label(str(int(c.midpoint)),X(c.midpoint),-.97,17,WHITE,True,1.0))
    if k>=3:g.add(mean_line(X,y0=-.68,y1=1.38))
    if k==4:g.add(badge('TRUNG BÌNH GỐC: 7,1   |   GHÉP NHÓM: 7,6',XL,2.02,GOLD,6.0))
    g.add(foot('Thay các giá trị trong lớp bằng trung điểm.'))
    return g,None

def vis3(k):
    g=VGroup(top('TỪ ĐỘ LỆCH ĐẾN PHƯƠNG SAI'))
    ax,X=base_axis(y=-1.56);g.add(ax)
    center=7.6
    g.add(mean_line(X,center,y0=-1.50,y1=1.23))
    for i,(c,f) in enumerate(zip(CLASSES,FREQ)):
        xx=X(c.midpoint);cc=PALETTE[i]
        g.add(Dot((xx,-1.12,0),radius=.11,color=cc))
        if k>=2:
            g.add(Line((xx,-.78,0),(X(center),-.78,0),color=cc,stroke_width=3.6))
            g.add(label(fmt(c.midpoint-center,1),xx,-.35,15,cc,True,1.14))
        if k>=3:
            val=f*(c.midpoint-center)**2
            g.add(bar(X,c.left+.25,c.right-.25,val*.027,-1.57,cc))
    if k==4:g.add(badge('TỔNG: 97,6    /    40    =    2,44',XL,2.01,GOLD,5.62))
    g.add(foot('Bình phương độ lệch rồi tính trung bình có trọng số.'))
    return g,None

def vis4(k):
    g=VGroup(top('CÁCH TÍNH RÚT GỌN'))
    labels=('TRUNG ĐIỂM','TẦN SỐ','BÌNH PHƯƠNG')
    for tx,x in zip(labels,(-5.03,-3.35,-1.61)):
        g.add(label(tx,x,1.75,13,CYAN,True,2.15))
    for j,(c,f) in enumerate(zip(CLASSES,FREQ)):
        y=1.13-j*.64
        g.add(label(str(int(c.midpoint)),-5.03,y,22,WHITE,True,1.0),
              label(str(f),-3.35,y,22,GOLD,True,1.0))
        if k>=2:g.add(label(str(int(c.midpoint**2)),-1.61,y,22,GREEN,True,1.22))
    if k>=3:g.add(badge('TỔNG f·m² = 2408',XL,-1.78,GOLD,4.05))
    if k==4:g.add(label('60,2 − 7,6² = 2,44',XL,-2.26,18,GREEN,True,5.6))
    g.add(foot('Kiểm tra bằng hai phép tính tương đương.'))
    return g,None

def vis5(k):
    g=VGroup(top('CÙNG TRUNG BÌNH, KHÁC PHƯƠNG SAI'))
    ax,X=base_axis(y=-1.69);g.add(ax)
    yA=-1.62;yB=.30
    for freq,y,tag in ((FREQ,yA,'A'),(OTHER_FREQ,yB,'B')):
        g.add(label(tag,-5.82,y+.50,24,GOLD,True,.55))
        for i,(c,f) in enumerate(zip(CLASSES,freq)):
            g.add(bar(X,c.left,c.right,f*.066,y,PALETTE[i]))
    if k>=2:g.add(mean_line(X,y0=-1.66,y1=1.83))
    if k>=3:g.add(label('A: 2,44     B: 4,44',XL,-2.10,21,GOLD,True,5.72))
    if k==4:g.add(label('sA ≈ 1,562     sB ≈ 2,107',XL,-2.46,17,GREEN,True,5.76))
    g.add(foot('So sánh trên cùng hệ lớp và tổng tần số 40.'))
    return g,None

def vis6(k):
    g=VGroup(top('PHÉP BIẾN ĐỔI VÀ ĐƠN VỊ'))
    ax,X=base_axis(0,24,-1.60);g.add(ax)
    centers=[c.midpoint for c in CLASSES]
    if k==1:
        values=centers;avg=MAIN.mean
    elif k==2:
        values=[v+3 for v in centers];avg=MAIN.mean+3
    else:
        values=[2*v for v in centers];avg=MAIN.mean*2
    for i,(v,f) in enumerate(zip(values,FREQ)):
        g.add(Dot((X(v),-.85+f*.055,0),radius=.12,color=PALETTE[i]))
        g.add(Line((X(v),-1.53,0),(X(v),-.85+f*.055,0),color=PALETTE[i],stroke_width=4))
    if k>=2:g.add(Line((X(avg),-1.48,0),(X(avg),1.35,0),stroke_width=2.6,color=GOLD))
    if k==1:g.add(badge('BAN ĐẦU: s² = 2,44',XL,1.9,GREEN,4.25))
    if k==2:g.add(badge('CỘNG 3: s² = 2,44',XL,1.9,GREEN,4.20))
    if k>=3:g.add(badge('NHÂN 2: s² = 9,76; s ≈ 3,124',XL,1.9,GOLD,5.86))
    if k==4:g.add(label('CÔNG THỨC THPT: CHIA CHO n',XL,-2.24,16,CORAL,True,5.78))
    g.add(foot('Độ lệch chuẩn cùng đơn vị; phương sai bình phương đơn vị.'))
    return g,None

def vis7(k):
    g=VGroup(top('NGOẠI LỆ VÀ THÔNG TIN BỊ MẤT'))
    if k==1:
        ax,X=base_axis();g.add(ax,raw_points(SCORES,X,-1.36,.042))
        g.add(badge('DỮ LIỆU GỐC: s² = 2,29',XL,1.90,GREEN,4.65))
    else:
        ax,X=base_axis(0,32,-1.56);g.add(ax)
        data=list(SCORES);idx=data.index(10);data[idx]=30
        g.add(raw_points(data,X,-1.44,.04))
        g.add(Dot((X(30),.28,0),radius=.14,color=CORAL))
        g.add(label('30 (GIẢ ĐỊNH)',X(30)-.47,.85,13,CORAL,True,1.7))
        if k>=3:g.add(badge('PHƯƠNG SAI GỐC MỚI: 14,94',XL,1.91,GOLD,5.47))
        if k==4:g.add(label('PHẢI LẬP LẠI BẢNG GHÉP NHÓM',XL,-2.22,16,GREEN,True,5.72))
    g.add(foot('Giá trị 30 là mô phỏng toán học, không phải điểm thang 10.'))
    return g,None

def vis8(k):
    g=VGroup(top('BÀI TOÁN NGƯỢC – LUYỆN TẬP'))
    ax,X=base_axis(0,8,-1.56);g.add(ax)
    for i,c in enumerate(PRACTICE_CLASSES):
        if k==1:
            g.add(Rectangle(width=X(c.right)-X(c.left),height=.75,
                stroke_color=PALETTE[i],stroke_width=2,fill_opacity=0).move_to((X(c.midpoint),-1.18,0)))
            g.add(label('?',X(c.midpoint),-.95,22,PALETTE[i],True,1.0))
        else:
            f=PRACTICE_FREQ[i]
            g.add(bar(X,c.left,c.right,f*.16,-1.56,PALETTE[i]))
            g.add(label(str(f),X(c.midpoint),-1.34+f*.16,17,PALETTE[i],True,1.2))
    if k==1:g.add(badge('TẦN SỐ: x, 8, 6, 6−x',XL,1.89,GOLD,5.07))
    if k>=2:g.add(badge('BIẾT TRUNG BÌNH ≈ 4,2 ⇒ x = 2',XL,1.89,GOLD,5.74))
    if k==3:g.add(label('s² ≈ 3,36',XL,-2.12,20,GREEN,True,3.75))
    if k==4:g.add(label('s ≈ 1,833',XL,-2.12,20,GREEN,True,3.75))
    g.add(foot('Dùng cùng quy trình cho mọi bảng ghép nhóm.'))
    return g,None

VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)

class STAT12(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 12 / PHƯƠNG SAI VÀ ĐỘ LỆCH CHUẨN GHÉP NHÓM',
                    0,3.47,20,WHITE,True,13.15),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,maxw=12.0))
        return o

    def notes(self,b):
        o=VGroup()
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,33,break_long_words=False))
        o.add(label(ti,XR,2.13,21,WHITE,True,5.75,1.19),
              Line((.70,.81,0),(6.16,.81,0),color=EDGE,stroke_width=1),
              label(th,XR,-.02,19,GOLD,True,5.75,1.52))
        f=ROOT/'assets/stat12_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if b.step>=3:
            if not f.is_file():raise FileNotFoundError(f'STAT12 formula missing: {f}; run scripts/build_stat12_typst.py')
            svg=SVGMobject(str(f))
            if svg.width>5.20:svg.scale_to_fit_width(5.20)
            if svg.height>.87:svg.scale_to_fit_height(.87)
            svg.move_to((XR,-1.51,0))
            o.add(label('CÔNG THỨC / ĐỐI CHIẾU',XR,-.91,14,CYAN,True),svg)
        else:
            o.add(label('QUAN SÁT  →  GIẢI THÍCH  →  KIỂM TRA',XR,-1.48,16,GREEN,True,5.73))
        o.add(label('DỮ LIỆU GHÉP NHÓM: KẾT QUẢ THEO TRUNG ĐIỂM LỚP',
                    XR,-2.47,12,MUTED,maxw=5.7))
        return o

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat12/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat12.py first')
        plan=json.loads(path.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT12' or len(plan.get('beats',[]))!=32:raise ValueError('Invalid STAT12 plan')
        old_v=old_n=None
        for i,b in enumerate(BEATS):
            s=plan['beats'][i]
            if (s['chapter'],s['step'])!=(b.chapter,b.step):raise ValueError(f'Invalid lesson entry {i}')
            if s.get('voice'):
                sound=ROOT/s['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            v,_=VISUALS[b.chapter-1](b.step);n=self.notes(b)
            if old_v is None:
                self.play(FadeIn(v),FadeIn(n),run_time=1.40);used=1.40
            else:
                self.play(FadeOut(old_v),FadeOut(old_n),run_time=.55)
                self.play(FadeIn(v),FadeIn(n),run_time=1.10);used=1.65
            self.wait(.45);used+=.45
            duration=float(s['duration'])
            if duration<=used:raise ValueError(f'Entry {i+1} too short')
            self.wait(duration-used)
            old_v,old_n=v,n

class STAT12_SMOKE(STAT12):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            v,_=VISUALS[b.chapter-1](b.step);n=self.notes(b)
            self.add(v,n);self.wait(.12);self.remove(v,n)
