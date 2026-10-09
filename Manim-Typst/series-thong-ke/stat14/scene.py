"""STAT14: integrated real-world statistics; no production counters on screen.
Prepare formulas and timeline, then render with manim stat14/scene.py STAT14.
"""
from __future__ import annotations
import json, sys, textwrap
from pathlib import Path
from collections import Counter
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import (label,top,foot,badge,ruled_axis,bar,
    XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE)
from stat07.lesson import CLASSES,FREQ
from stat14.lesson import (BEATS,QUEUE_A,QUEUE_B,QUEUE_OUTLIER,PA,PB,PO,
    EA,EB,EXERCISE_A,EXERCISE_B,COHORTS,RAW,GROUPED,count_at_most)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
COLOR_A=CYAN
COLOR_B=CORAL
FORM_KEYS=('context','dispersion','criteria','outlier','grouped','weighted','responsible','exercise')


def text(s,x,y,sz=17,color=WHITE,w=5.6,bold=False):
    return label(s,x,y,sz,color,bold,w)


def axis(lo=0,hi=16,y=-1.67):
    return ruled_axis(lo,hi,y,tuple(range(lo,hi+1,2)),lo=-5.66,hi=-1.19)


def dots(data,X,y,color):
    g=VGroup();occur=Counter()
    for value in data:
        j=occur[value];occur[value]+=1
        g.add(Dot((X(value),y+j*.15,0),radius=.077,color=color))
    return g


def plot_pair(a=QUEUE_A,b=QUEUE_B,low=0,high=16):
    g=VGroup();axs,X=axis(low,high,-1.70);g.add(axs)
    for vals,y,c,name in ((a,.61,COLOR_A,'QUẦY A'),(b,-.72,COLOR_B,'QUẦY B')):
        g.add(text(name,-5.15,y+.34,14,c,1.2,True),dots(vals,X,y,c))
    return g,X


def boxplot(p,X,y,c):
    """Use sample extrema as whiskers for these datasets, none is a Tukey outlier."""
    gg=VGroup(Line((X(p.minimum),y,0),(X(p.maximum),y,0),stroke_width=3,color=c))
    gg.add(Rectangle(width=X(p.q3)-X(p.q1),height=.49,stroke_width=2.6,
      stroke_color=c,fill_color=c,fill_opacity=.22).move_to(((X(p.q1)+X(p.q3))/2,y,0)))
    for z in (p.minimum,p.maximum):
        gg.add(Line((X(z),y-.15,0),(X(z),y+.15,0),color=c,stroke_width=2.7))
    gg.add(Line((X(p.median),y-.23,0),(X(p.median),y+.23,0),color=GOLD,stroke_width=3.6))
    return gg


def vis1(k):
    g=VGroup(top('HAI QUẦY PHỤC VỤ THƯ VIỆN'))
    p,X=plot_pair();g.add(p)
    if k>=2:g.add(text('MỖI QUẦY: 10 LƯỢT ĐỢI (PHÚT)',XL,1.58,16,GOLD,5.9,True))
    if k>=3:
        g.add(Line((X(8),-1.45,0),(X(8),1.26,0),stroke_width=2.3,color=GOLD))
        g.add(text('TRUNG BÌNH = TRUNG VỊ = 8 PHÚT',XL,2.02,15,GREEN,5.95,True))
    if k==4:g.add(text('MỤC TIÊU NÀO QUAN TRỌNG NHẤT?',XL,-2.30,15,CYAN,5.9,True))
    g.add(foot('Các lượt khảo sát giả lập; mỗi chấm là một lượt.'))
    return g,None


def vis2(k):
    g=VGroup(top('KHOẢNG BIẾN THIÊN • IQR • ĐỘ LỆCH CHUẨN'))
    p,X=axis(0,16,-1.77);g.add(p)
    g.add(text('A',-5.88,.67,19,COLOR_A,.40,True),boxplot(PA,X,.67,COLOR_A))
    if k>=2:g.add(text('B',-5.88,-.63,19,COLOR_B,.40,True),boxplot(PB,X,-.63,COLOR_B))
    if k>=3:g.add(text('IQR: A = 2      B = 5 (PHÚT)',XL,1.72,17,GOLD,5.9,True))
    if k==4:g.add(text('s: A ≈ 1,095     B ≈ 3,873 PHÚT',XL,-2.37,15,GREEN,5.95,True))
    g.add(foot('Hai biểu đồ hộp dùng chung một trục số.'))
    return g,None


def vis3(k):
    g=VGroup(top('TIÊU CHÍ CHỜ KHÔNG QUÁ GIỚI HẠN'))
    limit=10 if k in (1,3) else 5
    g.add(text(f'GIỚI HẠN: {limit} PHÚT',XL,1.90,19,GOLD,4.75,True))
    for row,(name,vals,c) in enumerate((('A',QUEUE_A,COLOR_A),('B',QUEUE_B,COLOR_B))):
        y=.69-row*1.20
        g.add(text('QUẦY '+name,-5.24,y,15,c,1.25,True))
        for i,v in enumerate(vals):
            fill=c if v<=limit else MUTED
            g.add(RoundedRectangle(width=.31,height=.38,corner_radius=.06,
             stroke_color=EDGE,stroke_width=.8,fill_color=fill,
             fill_opacity=.85 if v<=limit else .17).move_to((-4.26+i*.34,y,0)))
        if k>=2:g.add(text(f'{count_at_most(vals,limit)}/10',-.73,y,18,c,.76,True))
    if k>=3:g.add(text('ĐỌC THEO MỤC TIÊU, KHÔNG CHỈ THEO TRUNG BÌNH',XL,-1.93,13,GREEN,5.96,True))
    if k==4:g.add(text('TỶ LỆ MẪU KHÔNG PHẢI CAM KẾT TƯƠNG LAI',XL,-2.31,12,GOLD,5.94,True))
    g.add(foot('Các ô biểu diễn mười lượt khách được quan sát.'))
    return g,None


def vis4(k):
    g=VGroup(top('MỘT GIÁ TRỊ RẤT LỚN THAY ĐỔI KẾT QUẢ'))
    ax,X=axis(0,32,-1.70);g.add(ax)
    g.add(text('BAN ĐẦU',-5.05,1.06,14,COLOR_A,1.65,True),dots(QUEUE_A,X,.17,COLOR_A))
    current=QUEUE_A if k==1 else QUEUE_OUTLIER
    if k>=2:g.add(text('THAY ĐỔI',-5.05,-.49,14,COLOR_B,1.65,True),dots(current,X,-1.0,COLOR_B))
    if k>=2:g.add(Line((X(10),-.79,0),(X(30),-.79,0),stroke_width=2,color=GOLD))
    if k>=3:g.add(text('TRUNG BÌNH: 8 → 10   |   TRUNG VỊ: 8',XL,1.72,16,GOLD,5.94,True))
    if k==4:g.add(text('PHƯƠNG SAI: 1,2 → 45,2  |  IQR = 2',XL,-2.36,14,GREEN,5.93,True))
    g.add(foot('Chỉ một điểm 10 phút được thay bằng 30 phút.'))
    return g,None


def vis5(k):
    g=VGroup(top('DỮ LIỆU GỐC VÀ DỮ LIỆU GHÉP NHÓM'))
    ax,X=ruled_axis(4,12,-1.54,tuple(range(4,13)),lo=-5.67,hi=-1.20)
    g.add(ax)
    if k==1:
        # exact original score frequencies for the 40 original observations
        freq=(2,4,8,10,8,6,2)
        for j,(v,n) in enumerate(zip(range(4,11),freq)):
            g.add(bar(X,v-.30,v+.30,n*.117,-1.54,COLOR_A))
            g.add(text(str(n),X(v),-1.32+n*.117,13,GOLD,.35,True))
    else:
        for i,(cls,n) in enumerate(zip(CLASSES,FREQ)):
            g.add(bar(X,cls.left,cls.right,n*.102,-1.54,
                (CYAN,GREEN,PURPLE,CORAL)[i]))
            g.add(text(str(n),X(cls.midpoint),-1.32+n*.102,16,GOLD,.52,True))
    if k>=2:g.add(text('TRUNG ĐIỂM LỚP: 5 • 7 • 9 • 11',XL,1.79,16,GOLD,5.91,True))
    if k>=3:g.add(text('TRUNG BÌNH: GỐC 7,1   |   GHÉP 7,6',XL,1.19,15,GREEN,5.95,True))
    if k==4:g.add(text('PHƯƠNG SAI: GỐC 2,29   |   GHÉP 2,44',XL,-2.29,15,CYAN,5.95,True))
    g.add(foot('Bảng nhóm không lưu từng quan sát trong lớp.'))
    return g,None


def vis6(k):
    g=VGroup(top('GỘP NHÓM PHẢI THEO TRỌNG SỐ'))
    g.add(text('A: 10 HỌC SINH     TRUNG BÌNH 8',XL,1.83,16,COLOR_A,5.85,True),
          text('B: 30 HỌC SINH     TRUNG BÌNH 6',XL,1.31,16,COLOR_B,5.85,True))
    for row,(count,mean) in enumerate(COHORTS):
        y=.55-row*.93;c=COLOR_A if row==0 else COLOR_B
        for j in range(count):
            x=-5.90+j*.160
            g.add(RoundedRectangle(width=.135,height=.43,corner_radius=.025,
                   fill_color=c,fill_opacity=.84,stroke_width=0).move_to((x,y,0)))
        if k>=2:g.add(text(f'{count} × {int(mean)}',-.68,y,15,c,.95,True))
    if k>=3:g.add(text('SAI: (8 + 6)/2 = 7',XL,-1.54,17,CORAL,4.86,True))
    if k==4:g.add(text('ĐÚNG: (10×8 + 30×6)/40 = 6,5',XL,-2.18,16,GREEN,5.92,True))
    g.add(foot('Mỗi ô tượng trưng đúng một học sinh.'))
    return g,None


def vis7(k):
    g=VGroup(top('BỐN QUY TẮC BÁO CÁO THỐNG KÊ'))
    items=(('1. DỮ LIỆU','Đơn vị, thời điểm, cỡ mẫu.'),
      ('2. MỤC TIÊU','Đúng hạn, đồng đều hay mức điển hình?'),
      ('3. GIỚI HẠN','Ngoại lệ, lấy mẫu, dữ liệu ghép.'),
      ('4. KẾT LUẬN','Chỉ kết luận trong số liệu đã xét.'))
    for i,(heading,desc) in enumerate(items):
        y=1.60-i*.93;c=GREEN if i<k else MUTED
        g.add(RoundedRectangle(width=5.83,height=.78,corner_radius=.09,
            stroke_width=1.2,stroke_color=c,fill_color=PANEL,fill_opacity=1).move_to((XL,y,0)))
        g.add(text(heading,XL,y+.16,17,c,5.6,True))
        g.add(text(desc,XL,y-.15,13,WHITE,5.58))
    g.add(foot('Mô tả mẫu chưa chứng minh quan hệ nhân quả.'))
    return g,None


def vis8(k):
    g=VGroup(top('BÀI TẬP: HAI PHƯƠNG ÁN GIAO HÀNG'))
    # Reveal summary only after students have seen raw data.
    for row,(name,vals,c) in enumerate((('C',EXERCISE_A,COLOR_A),('D',EXERCISE_B,COLOR_B))):
        y=1.58-row*.74
        g.add(text(name,-5.75,y,17,c,.60,True))
        for i,v in enumerate(vals):
            g.add(text(str(v),-4.95+i*.54,y,17,c,.45,True))
    if k>=2:g.add(text('C VÀ D: TRUNG BÌNH = TRUNG VỊ = 8',XL,-.55,15,GOLD,5.95,True))
    if k>=3:g.add(text('IQR C = 1,5  |  IQR D = 4',XL,-1.22,17,GREEN,5.94,True))
    if k==4:g.add(text('s² C = 2  |  s² D = 11,5  →  C ỔN ĐỊNH HƠN',XL,-1.95,14,CYAN,5.93,True))
    g.add(foot('Dữ liệu giả lập; nhận xét theo tiêu chí đã chọn.'))
    return g,None

VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)

class STAT14(Scene):
    def frame(self):
        g=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,
                fill_color=BG,fill_opacity=1))
        for x in (XL,XR):
            g.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,
                fill_opacity=1).move_to((x,-.01,0)))
        g.add(label('SANGMATH / THỐNG KÊ 14 / BÀI TOÁN VẬN DỤNG THỰC TẾ',
                    0,3.47,20,WHITE,True,13.0),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,maxw=12.0))
        return g

    def notes(self,b):
        o=VGroup()
        heading='\n'.join(textwrap.wrap(b.title,28,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        o.add(label(heading,XR,2.12,21,WHITE,True,5.70,1.18),
          Line((.70,.82,0),(6.16,.82,0),color=EDGE,stroke_width=1),
          label(thesis,XR,-.04,18,GOLD,True,5.73,1.51))
        if b.step>=3:
            target=ROOT/'assets/stat14_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not target.is_file():
                raise FileNotFoundError(f'STAT14 SVG missing: {target}; run scripts/build_stat14_typst.py')
            svg=SVGMobject(str(target))
            if svg.width>5.2:svg.scale_to_fit_width(5.2)
            if svg.height>.82:svg.scale_to_fit_height(.82)
            svg.move_to((XR,-1.53,0))
            o.add(label('CÔNG THỨC / ĐỐI CHIẾU',XR,-.95,14,CYAN,True),svg)
        else:
            o.add(label('DỮ LIỆU  →  TIÊU CHÍ  →  KẾT LUẬN',XR,-1.47,15,GREEN,True,5.62))
        o.add(label('KẾT LUẬN TRONG MẪU ĐÃ QUAN SÁT',XR,-2.45,12,MUTED,maxw=5.76))
        return o

    def construct(self):
        self.add(self.frame())
        file=ROOT/'stat14/runtime_plan.json'
        if not file.is_file():raise FileNotFoundError('Run scripts/prepare_stat14.py before rendering')
        plan=json.loads(file.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT14' or len(plan.get('beats',[]))!=32:
            raise ValueError('STAT14 runtime plan incorrect')
        old_visual=old_note=None
        for i,b in enumerate(BEATS):
            row=plan['beats'][i]
            if (row['chapter'],row['step'])!=(b.chapter,b.step):
                raise ValueError(f'STAT14 beat plan mismatch at {i+1}')
            if row.get('voice'):
                mp3=ROOT/row['voice']
                if not mp3.is_file():raise FileNotFoundError(mp3)
                self.add_sound(str(mp3))
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45)
                used=1.45
            else:
                self.play(FadeOut(old_visual),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05)
                used=1.60
            self.wait(.35);used+=.35
            pause=float(row['duration'])-used
            if pause<=0:raise ValueError('Duration too short for a scene transition')
            self.wait(pause)
            old_visual,old_note=visual,note

class STAT14_SMOKE(STAT14):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            vis,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(vis,note)
            self.wait(.12)
            self.remove(vis,note)
