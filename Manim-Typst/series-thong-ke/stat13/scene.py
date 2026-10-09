"""STAT13: compare two samples. Classroom-only labels; no internal counters on screen.

Before real rendering:
 python scripts/build_stat13_typst.py
 python scripts/prepare_stat13.py --voice off
 manim -ql -r 854,480 --fps 24 stat13/scene.py STAT13
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from collections import Counter
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import (label,top,foot,badge,ruled_axis,bar,
    XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE)
from stat07.lesson import CLASSES,FREQ
from stat13.lesson import (A,B,PA,PB,EA,EB,EXERCISE_A,EXERCISE_B,
    GROUPED_A,GROUPED_B,BEATS,count_at_least)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
COLOR_A=CYAN;COLOR_B=CORAL
FORM_KEYS=('problem','central','boxplot','dispersion','grouped','targets','limits','exercise')


def fmt(v,nd=1):return f'{v:.{nd}f}'.replace('.',',')


def x_axis(low=3.0, high=11.0, y=-1.95):
    return ruled_axis(low, high, y, tuple(range(int(low),int(high)+1)),lo=-5.83,hi=-1.02)


def points(values, X, y, color):
    """Stack repeated scores vertically. Preserves count and exact positions."""
    out=VGroup();counts=Counter()
    for v in values:
        j=counts[v];counts[v]+=1
        out.add(Dot((X(v),y+j*.18,0),radius=.085,color=color))
    return out


def two_dotplots(vals_a=A,vals_b=B,mean=False,group_b=True):
    g=VGroup()
    ax,X=x_axis(y=-2.0);g.add(ax)
    g.add(label('NHÓM A',-5.09,.91,17,COLOR_A,True,1.6),points(vals_a,X,.12,COLOR_A))
    if group_b:g.add(label('NHÓM B',-5.09,-.72,17,COLOR_B,True,1.6),points(vals_b,X,-1.55,COLOR_B))
    if mean:
        g.add(Line((X(7),-1.90,0),(X(7),1.62,0),stroke_width=2.7,color=GOLD),
              label('TRUNG BÌNH 7',X(7),1.87,15,GOLD,True,2.25))
    return g,X


def boxplot(p,X,y,color):
    """Tukey-style whiskers to sample extrema; this example has no outliers."""
    g=VGroup()
    g.add(Line((X(p.minimum),y,0),(X(p.maximum),y,0),stroke_width=2.8,color=color))
    g.add(Rectangle(width=X(p.q3)-X(p.q1),height=.53,stroke_color=color,
        stroke_width=2.8,fill_color=color,fill_opacity=.21).move_to(((X(p.q1)+X(p.q3))/2,y,0)))
    for v in (p.minimum,p.maximum):
        g.add(Line((X(v),y-.18,0),(X(v),y+.18,0),color=color,stroke_width=2.7))
    g.add(Line((X(p.median),y-.28,0),(X(p.median),y+.28,0),color=GOLD,stroke_width=3.5))
    return g


def ticks(vals,y,color):
    # Ordered scores are discrete marks on the axis.
    g=VGroup()
    for i,v in enumerate(vals):
        x=-5.22+i*.46
        g.add(label(str(v),x,y,18,color,True,.53))
    return g


def vis1(k):
    g=VGroup(top('HAI NHÓM, CÙNG TRUNG BÌNH'))
    h,X=two_dotplots(mean=k>=3);g.add(h)
    if k>=2:g.add(badge('MỖI NHÓM 10 ĐIỂM KIỂM TRA',XL,2.00,GOLD,4.65))
    if k==4:g.add(label('SO SÁNH CẢ VỊ TRÍ VÀ ĐỘ PHÂN TÁN',XL,-2.50,15,GREEN,True,5.9))
    g.add(foot('Dữ liệu minh họa, cùng thang điểm 0–10.'))
    return g,None


def vis2(k):
    g=VGroup(top('VỊ TRÍ TRUNG TÂM'))
    g.add(label('A:',-5.86,1.45,20,COLOR_A,True,.62),
          label('B:',-5.86,.41,20,COLOR_B,True,.62),
          ticks(A,1.45,COLOR_A),ticks(B,.41,COLOR_B))
    if k>=2:g.add(badge('TỔNG A = TỔNG B = 70',XL,-.56,GOLD,4.34))
    if k>=3:g.add(label('TRUNG VỊ A = TRUNG VỊ B = 7',XL,-1.19,19,GREEN,True,5.95))
    if k==4:g.add(label('MỐT A = MỐT B = 7',XL,-1.81,19,CYAN,True,5.95))
    g.add(foot('Ba số đo trung tâm đều trùng nhau.'))
    return g,None


def vis3(k):
    g=VGroup(top('TỨ PHÂN VỊ VÀ BIỂU ĐỒ HỘP'))
    ax,X=x_axis(y=-1.91);g.add(ax)
    g.add(label('A',-5.95,.88,21,COLOR_A,True,.5),boxplot(PA,X,.89,COLOR_A))
    if k>=2:g.add(label('B',-5.95,-.63,21,COLOR_B,True,.5),boxplot(PB,X,-.64,COLOR_B))
    if k>=3:g.add(badge('HỘP A: [6; 8]    HỘP B: [4; 10]',XL,1.87,GOLD,5.95))
    if k==4:g.add(label('IQR A = 2      IQR B = 6',XL,-2.40,18,GREEN,True,5.95))
    g.add(foot('Cùng trục: chiều dài hộp phản ánh IQR.'))
    return g,None


def vis4(k):
    g=VGroup(top('TỪ ĐỘ LỆCH ĐẾN ĐỘ LỆCH CHUẨN'))
    ax,X=x_axis(y=-1.81);g.add(ax)
    g.add(Line((X(7),-1.79,0),(X(7),1.54,0),stroke_width=2.2,color=GOLD))
    for row,(vals,y,c) in enumerate(((A,.16,COLOR_A),(B,-1.15,COLOR_B))):
        stack=Counter()
        g.add(label('A' if row==0 else 'B',-5.99,y+.14,21,c,True,.50))
        for value in vals:
            ydot=y+stack[value]*.13;stack[value]+=1
            g.add(Dot((X(value),ydot,0),radius=.063,color=c))
            if k>=2:
                g.add(Line((X(value),y-.21,0),(X(7),y-.21,0),color=c,stroke_width=1.6))
    if k>=3:g.add(badge('A: s² = 1,2       B: s² = 5,4',XL,2.00,GOLD,5.58))
    if k==4:g.add(label('A: s ≈ 1,095    |    B: s ≈ 2,324',XL,-2.47,16,GREEN,True,6.0))
    g.add(foot('Cùng trung bình 7; B có độ phân tán lớn hơn.'))
    return g,None


def vis5(k):
    g=VGroup(top('HAI BẢNG GHÉP NHÓM'))
    ax,X=x_axis(4,12,-1.97);g.add(ax)
    for row,(freq,y,c,short) in enumerate(((FREQ,-.50,COLOR_A,'A'),((9,19,3,9),.60,COLOR_B,'B'))):
        g.add(label(short,-5.91,y+.39,20,c,True,.6))
        for cls,f in zip(CLASSES,freq):
            if row==0 or k>=2:
                g.add(bar(X,cls.left,cls.right,f*.047,y,c))
    if k>=2:g.add(badge('TẦN SỐ A: 6, 18, 14, 2',XL,2.02,COLOR_A,4.45))
    if k>=3:g.add(label('TRUNG BÌNH ƯỚC LƯỢNG: 7,6',XL,-2.38,16,GOLD,True,5.92))
    if k==4:g.add(label('PHƯƠNG SAI ƯỚC LƯỢNG: 2,44 / 4,44',XL,1.71,13,GREEN,True,5.9))
    g.add(foot('Bảng ghép nhóm: tính từ trung điểm lớp.'))
    return g,None


def vis6(k):
    g=VGroup(top('MỤC TIÊU THAY ĐỔI, KẾT LUẬN THAY ĐỔI'))
    threshold=6 if k<=2 else 9
    g.add(label('TỪ '+str(threshold)+' ĐIỂM TRỞ LÊN',XL,1.62,18,GOLD,True,5.94))
    for row,(name,data,c) in enumerate((('A',A,COLOR_A),('B',B,COLOR_B))):
        y=.63-row*1.19
        ok=count_at_least(data,threshold)
        g.add(label('NHÓM '+name,-5.25,y,18,c,True,1.9))
        for i in range(len(data)):
            xx=-4.06+i*.37
            passed=data[i]>=threshold
            g.add(RoundedRectangle(width=.28,height=.32,corner_radius=.04,
                stroke_color=EDGE,stroke_width=.8,
                fill_color=(c if passed else MUTED),fill_opacity=(.85 if passed else .20)).move_to((xx,y,0)))
        if k>=2:g.add(label(f'{ok}/10',-.81,y,20,c,True,.9))
    if k==4:g.add(label('A ƯU THẾ MỨC ĐẠT; B ƯU THẾ ĐIỂM CAO',XL,-1.85,15,GREEN,True,5.95))
    g.add(foot('Chọn chỉ số trước khi đưa ra kết luận.'))
    return g,None


def vis7(k):
    g=VGroup(top('ĐỌC SỐ LIỆU CÓ TRÁCH NHIỆM'))
    cards=(('CÙNG THANG ĐO','So sánh số liệu cùng đơn vị.'),
           ('KIỂM TRA NGOẠI LỆ','Giá trị cực đoan có thể đổi trung bình.'),
           ('MẪU CÓ ĐẠI DIỆN?','Mười điểm không đại diện cả trường.'),
           ('KẾT LUẬN TRONG MẪU','Không suy diễn nguyên nhân.'))
    for i,(title,explain) in enumerate(cards):
        yy=1.43-i*.91
        color=GREEN if i<k else MUTED
        g.add(RoundedRectangle(width=5.85,height=.73,corner_radius=.09,
              stroke_color=color,stroke_width=1.1,
              fill_color=PANEL,fill_opacity=.97).move_to((XL,yy,0)))
        g.add(label(title,XL,yy+.14,15,color,True,5.56))
        g.add(label(explain,XL,yy-.17,12,WHITE,maxw=5.52))
    g.add(foot('Không gọi tương quan hay mô tả là nguyên nhân.'))
    return g,None


def vis8(k):
    g=VGroup(top('LUYỆN TẬP: SO SÁNH HAI MẪU 8 ĐIỂM'))
    for i,(name,data,c) in enumerate((('A',EXERCISE_A,COLOR_A),('B',EXERCISE_B,COLOR_B))):
        y=1.35-i*1.22
        g.add(label('NHÓM '+name,-5.28,y,16,c,True,1.35))
        for j,val in enumerate(data):
            g.add(label(str(val),-4.43+j*.45,y,19,c,True,.42))
    if k>=2:g.add(label('CẢ HAI: TRUNG BÌNH = 7, TRUNG VỊ = 7',XL,-1.13,16,GOLD,True,5.96))
    if k>=3:g.add(label('IQR: 2 / 5     |     s²: 1,5 / 5,5',XL,-1.70,17,GREEN,True,5.96))
    if k==4:g.add(label('KẾT LUẬN: A ĐỒNG ĐỀU HƠN TRONG MẪU',XL,-2.21,15,CYAN,True,5.96))
    g.add(foot('Dữ liệu giả lập: nêu rõ tiêu chí so sánh.'))
    return g,None

VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)

class STAT13(Scene):
    def frame(self):
        o=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            o.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,
                fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        o.add(label('SANGMATH / THỐNG KÊ 12 / SO SÁNH HAI MẪU SỐ LIỆU',0,3.47,20,WHITE,True,13.0),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,maxw=12.0))
        return o

    def notes(self,b):
        o=VGroup()
        title='\n'.join(textwrap.wrap(b.title,28,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,33,break_long_words=False))
        o.add(label(title,XR,2.12,22,WHITE,True,5.72,1.18),
              Line((.70,.82,0),(6.16,.82,0),color=EDGE,stroke_width=1),
              label(thesis,XR,-.09,19,GOLD,True,5.75,1.46))
        if b.step>=3:
            target=ROOT/'assets/stat13_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not target.is_file():
                raise FileNotFoundError(f'STAT13 SVG is missing: {target}; run scripts/build_stat13_typst.py')
            svg=SVGMobject(str(target))
            if svg.width>5.22:svg.scale_to_fit_width(5.22)
            if svg.height>.88:svg.scale_to_fit_height(.88)
            svg.move_to((XR,-1.49,0))
            o.add(label('CÔNG THỨC / ĐỐI CHIẾU',XR,-.88,14,CYAN,True),svg)
        else:
            o.add(label('QUAN SÁT  →  LẬP LUẬN  →  KẾT LUẬN',XR,-1.44,16,GREEN,True,5.75))
        o.add(label('CÙNG THANG ĐIỂM, SO SÁNH ĐÚNG TIÊU CHÍ',XR,-2.45,12,MUTED,maxw=5.73))
        return o

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat13/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat13.py before rendering')
        plan=json.loads(path.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT13' or len(plan.get('beats',[]))!=32:
            raise ValueError('Invalid STAT13 runtime plan')
        old_visual=old_note=None
        for i,b in enumerate(BEATS):
            item=plan['beats'][i]
            if (item['chapter'],item['step'])!=(b.chapter,b.step):
                raise ValueError(f'Plan and lesson differ at element {i+1}')
            if item.get('voice'):
                sound=ROOT/item['voice']
                if not sound.is_file():raise FileNotFoundError(f'Voice file not found: {sound}')
                self.add_sound(str(sound))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45);used=1.45
            else:
                self.play(FadeOut(old_visual),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05);used=1.60
            self.wait(.35);used+=.35
            delay=float(item['duration'])-used
            if delay<=0:raise ValueError('Video duration is shorter than the slide transition')
            self.wait(delay)
            old_visual,old_note=visual,note

class STAT13_SMOKE(STAT13):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            v,_=VISUALS[b.chapter-1](b.step)
            n=self.notes(b)
            self.add(v,n);self.wait(.12);self.remove(v,n)
