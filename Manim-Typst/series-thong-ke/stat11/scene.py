"""STAT11: grouped range and IQR; credit and narrator set for the series."""
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
from stat11.lesson import BEATS,MAIN,RAW_R,RAW_Q,RAW_IQR,COMPARE,UNIFORM,SHIFTED_MAIN,SCALED_MAIN,EDGE_FREQ,EDGE_SPAN
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
COLORS=(CYAN,GREEN,PURPLE,CORAL)
FORM_KEYS=('ranges','quartiles','r_vs_iqr','two_samples','transform','lost_info','mistakes','practice')

def fmt(v):return f'{v:.2f}'.replace('.',',')
def axis(lo=4,hi=12,y=-1.45,ticks=(4,6,8,10,12)):
    return ruled_axis(lo,hi,y,ticks)
def mark(X,x,y,col,text=None):
    g=VGroup(Line((X(x),y-.12,0),(X(x),y+.55,0),color=col,stroke_width=2.6),
             Dot((X(x),y+.55,0),radius=.055,color=col))
    if text:g.add(label(text,X(x),y+.90,13,col,True,1.72))
    return g
def strip(X,a,b,y,col,title=None):
    g=VGroup(Line((X(a),y,0),(X(b),y,0),color=col,stroke_width=10),
        Dot((X(a),y,0),radius=.095,color=col),Dot((X(b),y,0),radius=.095,color=col))
    if title:g.add(label(title,(X(a)+X(b))/2,y+.37,15,col,True,3.2))
    return g

def hist(freq=FREQ,y=-1.48):
    ax,X=axis(y=y)
    g=VGroup(ax)
    for i,(c,f) in enumerate(zip(CLASSES,freq)):
        h=f*.12
        g.add(bar(X,c.left,c.right,h,y,COLORS[i]),
              label(str(f),X(c.midpoint),y+h+.22,16,COLORS[i],True,1.2))
    return g,X

def table(freq=FREQ,highlight=None):
    g=VGroup(label('LỚP',-4.86,1.66,14,CYAN,True,2),
        label('TẦN SỐ',-3.34,1.66,14,CYAN,True,1.65))
    for i,(c,f) in enumerate(zip(CLASSES,freq)):
        y=.97-i*.65
        if i==highlight:
            g.add(RoundedRectangle(width=5.1,height=.49,corner_radius=.06,
                stroke_color=GOLD,stroke_width=1.0,fill_color=EDGE,fill_opacity=.3).move_to((-3.39,y,0)))
        g.add(label(c.caption,-4.85,y,18,GOLD if i==highlight else WHITE,True,2.0),
              label(str(f),-3.33,y,19,GOLD if i==highlight else WHITE,True,1.25))
    return g

def vis1(k):
    g=VGroup(top('KHOẢNG BIẾN THIÊN: GỐC VÀ GHÉP NHÓM'))
    a,X=axis();g.add(a)
    if k<3:
        g.add(raw_points(SCORES,X,-1.16,.049))
        g.add(strip(X,4,10,-.18,GREEN,'R gốc = 6'))
        if k==2:g.add(badge('MAX 10   −   MIN 4   =   6',XL,1.73,GOLD,5.1))
    else:
        h,_=hist();g.add(h)
        g.add(strip(X,4,12,-.41,CORAL,'R ghép = 8'))
        if k==4:g.add(label('RANH GIỚI 12 KHÔNG PHẢI ĐIỂM ĐÃ QUAN SÁT',XL,1.85,15,GOLD,True,5.85))
    g.add(foot('Đọc đúng cực trị gốc hoặc ranh giới lớp.'))
    return g,None

def vis2(k):
    g=VGroup(top('KHOẢNG TỨ PHÂN VỊ: Q3 − Q1'))
    h,X=hist();g.add(h)
    if k>=2:
        g.add(mark(X,MAIN.q1,-.83,GREEN,'Q1'),mark(X,MAIN.q3,-.83,PURPLE,'Q3'))
    if k>=3:g.add(strip(X,MAIN.q1,MAIN.q3,.54,GOLD,'NỬA GIỮA'))
    if k==4:g.add(badge(f'IQR ≈ {fmt(MAIN.iqr)}',XL,2.03,GREEN,3.8))
    g.add(foot('Nội suy từ bảng: dùng dấu xấp xỉ.'))
    return g,None

def vis3(k):
    g=VGroup(top('R TOÀN BỘ, IQR VÙNG GIỮA'))
    a,X=axis();g.add(a)
    g.add(strip(X,4,12,.75,CORAL,'R ≈ 8'))
    if k>=2:g.add(strip(X,MAIN.q1,MAIN.q3,-.14,GREEN,'IQR ≈ 2,41'))
    if k>=3:
        g.add(badge('THÍ NGHIỆM NGOẠI LỆ: 10 → 30',XL,1.87,GOLD,5.54),
              label('R gốc 6 → 26',XL,-2.00,18,CORAL,True,5.75))
    if k==4:g.add(label('MUỐN GHÉP NHÓM LẠI PHẢI CẬP NHẬT LỚP',XL,-2.37,14,GREEN,True,5.96))
    g.add(foot('Ví dụ 30 chỉ là thí nghiệm, không phải điểm thang 10.'))
    return g,None

def vis4(k):
    f=FREQ if k in (1,2) else UNIFORM
    g=VGroup(top('CÙNG R, NHƯNG IQR KHÁC NHAU'))
    h,X=hist(f);g.add(h)
    if k>=2:
        q=MAIN if k==2 else COMPARE
        g.add(strip(X,q.q1,q.q3,.72,GOLD,f'IQR ≈ {fmt(q.iqr)}'))
    if k==4:g.add(badge('A: 2,41   <   B: 4,00',XL,2.04,GREEN,4.85))
    g.add(foot('Bảng A: 6–18–14–2; bảng B: 10–10–10–10.'))
    return g,None

def vis5(k):
    g=VGroup(top('DỊCH CHUYỂN VÀ CO GIÃN DỮ LIỆU'))
    a,X=axis(4,24,-1.15,(4,8,12,16,20,24));g.add(a)
    v=MAIN if k==1 else SHIFTED_MAIN if k==2 else SCALED_MAIN
    g.add(strip(X,v.q1,v.q3,.58,GOLD,f'IQR = {fmt(v.iqr)}'))
    if k==1:g.add(badge('BAN ĐẦU: R = 8',XL,1.8,GREEN,4.2))
    if k==2:g.add(badge('CỘNG 3: R VẪN = 8',XL,1.8,GREEN,4.8))
    if k>=3:g.add(badge('NHÂN 2: R = 16',XL,1.8,GOLD,4.8))
    if k==4:g.add(label('NHÂN SỐ ÂM: NHỚ TRỊ TUYỆT ĐỐI',XL,-2.13,15,CORAL,True,5.7))
    g.add(foot('Khoảng biến thiên và IQR mang đơn vị dữ liệu.'))
    return g,None

def vis6(k):
    g=VGroup(top('THÔNG TIN MẤT ĐI KHI GHÉP NHÓM'))
    if k<=2:
        g.add(table(FREQ,0 if k==2 else 3))
        if k==2:g.add(badge('LỚP CUỐI [10;12): 2 ĐIỂM 10',XL,-2.10,CORAL,5.3))
    else:
        g.add(table(EDGE_FREQ,0 if k==3 else 1))
        g.add(badge('LỚP ĐẦU TRỐNG ⇒ R = 12 − 6 = 6',XL,-2.18,GREEN,5.9))
    g.add(foot('Đọc lớp đầu và lớp cuối có tần số dương.'))
    return g,None

def vis7(k):
    g=VGroup(top('PHÁT HIỆN NHỮNG CÁCH TÍNH SAI'))
    a,X=axis();g.add(a)
    if k==1:
        g.add(strip(X,5,11,.48,CORAL,'SAI: 11 − 5'))
        g.add(badge('PHẢI DÙNG RANH GIỚI LỚP',XL,-2.12,GREEN,5.35))
    elif k==2:
        g.add(strip(X,6,10,.48,CORAL,'SAI: IQR = 4'))
        g.add(badge('PHẢI NỘI SUY Q1, Q3',XL,-2.12,GREEN,5.15))
    elif k==3:
        g.add(strip(X,4,12,.48,GOLD,'R = 8'))
        g.add(badge('DỮ LIỆU MỚI ⇒ BẢNG MỚI',XL,-2.12,GREEN,5.35))
    else:
        g.add(strip(X,4,12,.48,GOLD,'CÙNG R = 8'))
        g.add(badge('CHƯA KẾT LUẬN ĐƯỢC IQR',XL,-2.12,CORAL,5.35))
    g.add(foot('Chọn chỉ số đo phù hợp trước khi thay số.'))
    return g,None

def vis8(k):
    g=VGroup(top('TỰ KIỂM TRA VÀ TỔNG KẾT'))
    if k<=2:
        g.add(table(FREQ,1 if k==2 else None))
        if k==2:g.add(badge('R = 8; IQR ≈ 2,41',XL,-2.15,GREEN,5.4))
    else:
        g.add(table(UNIFORM,1 if k==3 else None))
        if k==3:g.add(badge('BẢNG B: R = 8; IQR = 4',XL,-2.15,GOLD,5.5))
        if k==4:g.add(badge('STAT12: PHƯƠNG SAI & ĐỘ LỆCH CHUẨN',XL,-2.15,CYAN,5.95))
    g.add(foot('Thước đo nào cũng có giới hạn và ý nghĩa riêng.'))
    return g,None
VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)

class STAT11(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 11 / KHOẢNG BIẾN THIÊN VÀ IQR GHÉP NHÓM',0,3.47,20,WHITE,True,13.1),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,maxw=12.0))
        return o

    def notes(self,b):
        o=VGroup()
        ti='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        o.add(label(ti,XR,2.17,22,WHITE,True,5.75,1.13),
              Line((.70,.81,0),(6.16,.81,0),color=EDGE,stroke_width=1),
              label(th,XR,-.04,20,GOLD,True,5.72,1.55))
        f=ROOT/'assets/stat11_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
        if not f.is_file():
            raise FileNotFoundError(f'STAT11 Typst SVG missing: {f}; run scripts/build_stat11_typst.py')
        if b.step>=3:
            svg=SVGMobject(str(f))
            if svg.width>5.3:svg.scale_to_fit_width(5.3)
            if svg.height>.87:svg.scale_to_fit_height(.87)
            svg.move_to((XR,-1.51,0))
            o.add(label('CÔNG THỨC / ĐỐI CHIẾU',XR,-.93,14,CYAN,True),svg)
        else:
            o.add(label('QUAN SÁT  →  NHẬN XÉT  →  KIỂM TRA',XR,-1.49,17,GREEN,True,5.75))
        o.add(label('BẢNG GHÉP NHÓM CHỈ CHO GIÁ TRỊ ƯỚC LƯỢNG',XR,-2.46,12,MUTED,maxw=5.75))
        return o

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat11/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat11.py first')
        plan=json.loads(path.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT11' or len(plan.get('beats',[]))!=32:
            raise ValueError('Invalid STAT11 plan')
        old_v=old_n=None
        for i,b in enumerate(BEATS):
            s=plan['beats'][i]
            if (s['chapter'],s['step'])!=(b.chapter,b.step):raise ValueError(f'Mismatched beat {i}')
            if s.get('voice'):
                sound=ROOT/s['voice'];
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            v,_=VISUALS[b.chapter-1](b.step);n=self.notes(b)
            used=0.
            if old_v is None:
                self.play(FadeIn(v),FadeIn(n),run_time=1.4);used=1.4
            else:
                self.play(FadeOut(old_v),FadeOut(old_n),run_time=.56);used=.56
                self.play(FadeIn(v),FadeIn(n),run_time=1.12);used+=1.12
            self.wait(.45);used+=.45
            duration=float(s['duration'])
            if duration<=used:raise ValueError(f'Too short beat {i+1}')
            self.wait(duration-used)
            old_v,old_n=v,n

class STAT11_SMOKE(STAT11):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            v,_=VISUALS[b.chapter-1](b.step);n=self.notes(b)
            self.add(v,n);self.wait(.12);self.remove(v,n)
