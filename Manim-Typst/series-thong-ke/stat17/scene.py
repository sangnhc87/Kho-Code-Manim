"""STAT17: correlation and linear regression. Render after Typst source compilation.
python scripts/build_stat17_typst.py
python scripts/prepare_stat17.py --voice off
manim -ql -r 854,480 --fps 24 stat17/scene.py STAT17
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import label,top,foot,XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE
from stat17.lesson import (BEATS,X,Y,NEGATIVE_Y,CURVED_X,CURVED_Y,OUTLIER_Y,
                            PRACTICE_X,PRACTICE_Y,statistics,fitted,residuals,losses,decimal)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
FORM_KEYS=('data','shapes','pearson','model','least_squares','prediction','caution','practice')


def text(s,x=XL,y=0,size=16,color=WHITE,width=5.85,bold=False):
    return label(str(s),x,y,size,color,bold,width)


def hint(s,y=-2.18,color=GOLD):
    return text(s,XL,y,14,color,5.82,True)


def axes(xmin=0,xmax=9,ymin=0,ymax=10,showgrid=True):
    """Chart drawable lies inside left panel; correct linear coordinate mapping."""
    if not xmax>xmin or not ymax>ymin:raise ValueError('Invalid chart limits')
    l,r=-5.91,-.94
    b,t=-1.73,1.64
    def P(x,y):return (l+(x-xmin)/(xmax-xmin)*(r-l),b+(y-ymin)/(ymax-ymin)*(t-b),0)
    g=VGroup()
    if showgrid:
        for i in range(1,5):
            xx=l+(r-l)*i/5
            yy=b+(t-b)*i/5
            g.add(Line((xx,b,0),(xx,t,0),color=EDGE,stroke_width=.48),
                  Line((l,yy,0),(r,yy,0),color=EDGE,stroke_width=.48))
    g.add(Line((l,b,0),(r+.08,b,0),color=MUTED,stroke_width=1.7),
          Line((l,b,0),(l,t+.10,0),color=MUTED,stroke_width=1.7),
          text('x',r+.13,b-.23,13,GOLD,.36,True),
          text('y',l-.18,t+.13,13,GOLD,.38,True))
    for xx in (xmin,xmax):g.add(text(f'{xx:g}',P(xx,ymin)[0],b-.23,11,MUTED,.40))
    for yy in (ymin,ymax):g.add(text(f'{yy:g}',l-.30,P(xmin,yy)[1],11,MUTED,.45))
    return g,P


def cloud(x=X,y=Y,showfit=False,showcenter=False,select=None,
          bounds=(0,9,0,10),showresiduals=False,color=CYAN):
    stats=statistics(x,y)
    g,P=axes(*bounds)
    for j,(a,b) in enumerate(zip(x,y)):
        c=GOLD if j==select else color
        g.add(Dot(P(a,b),radius=.085 if j==select else .060,color=c))
    if showcenter:
        cx,cy=stats['mx'],stats['my']
        g.add(Line(P(cx,bounds[2]),P(cx,bounds[3]),color=GREEN,stroke_width=1.4),
              Line(P(bounds[0],cy),P(bounds[1],cy),color=GREEN,stroke_width=1.4),
              Dot(P(cx,cy),radius=.085,color=GOLD))
    if showfit:
        a,b=stats['intercept'],stats['slope']
        lo,hi=bounds[0]+.05,bounds[1]-.05
        g.add(Line(P(lo,fitted(lo,stats)),P(hi,fitted(hi,stats)),color=GOLD,stroke_width=3.4))
    if showresiduals:
        for xx,yy in zip(x,y):
            g.add(Line(P(xx,yy),P(xx,fitted(xx,stats)),color=CORAL,stroke_width=2.0))
    return g,P


def two_clouds(k):
    g=VGroup()
    if k==1:
        chart,_=cloud(showfit=False);g.add(chart)
        g.add(hint('MỖI ĐIỂM LÀ MỘT CẶP (x, y)'))
    elif k==2:
        chart,_=cloud(showfit=False,select=0);g.add(chart)
        g.add(hint('QUAN SÁT THỨ NHẤT: (1; 2)'))
    elif k==3:
        chart,_=cloud(showfit=True);g.add(chart)
        g.add(hint('CÁC ĐIỂM GẦN MỘT ĐƯỜNG ĐI LÊN',color=GREEN))
    else:
        chart,_=cloud(showfit=False);g.add(chart)
        g.add(hint('NHÌN XU HƯỚNG, KHÔNG VỘI KẾT LUẬN',color=CORAL))
    return g,None


def direction(k):
    g=VGroup()
    if k==1:
        g.add(text('DƯƠNG  /  ÂM  /  KHÔNG TUYẾN TÍNH',XL,1.95,15,GOLD,5.9,True))
        cc,_=cloud(showfit=False);g.add(cc)
    elif k==2:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('MẪU CHÍNH: r > 0',color=GREEN))
    elif k==3:
        cc,_=cloud(X,NEGATIVE_Y,showfit=True);g.add(cc)
        g.add(hint('PHẢN CHIẾU: r < 0',color=CORAL))
    else:
        cc,_=cloud(X,CURVED_Y,bounds=(0,9,0,13),color=PURPLE);g.add(cc)
        g.add(hint('HÌNH CHỮ U CÓ r = 0',color=GOLD))
    return g,None


def pearson(k):
    g=VGroup()
    if k==1:
        cc,_=cloud(showcenter=True);g.add(cc)
        g.add(hint('TÂM ĐÁM MÂY: (4,5; 5)'))
    elif k==2:
        cc,_=cloud(showcenter=True,select=7);g.add(cc)
        g.add(hint('TÍCH ĐỘ LỆCH CHO BIẾT CHIỀU HƯỚNG'))
    elif k==3:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('Sxx = 42   Syy = 36   Sxy = 36'))
    else:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('r ≈ '+decimal(statistics()['r'],3),color=GREEN))
    return g,None


def regression(k):
    g=VGroup()
    if k==1:
        cc,_=cloud(showfit=False);g.add(cc)
        g.add(hint('TÌM ĐƯỜNG THẲNG DỰ ĐOÁN'))
    elif k==2:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('HỆ SỐ GÓC b = 6/7',color=GREEN))
    elif k==3:
        cc,_=cloud(showfit=True,showcenter=True);g.add(cc)
        g.add(hint('ĐƯỜNG ĐI QUA ĐIỂM (4,5; 5)',color=GREEN))
    else:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('ŷ = 8/7 + (6/7)x',color=GOLD))
    return g,None


def least_squares(k):
    g=VGroup()
    cc,_=cloud(showfit=(k>=2),showresiduals=(k>=2),select=(4 if k==1 else None))
    g.add(cc)
    labels={1:'PHẦN DƯ = y THỰC − ŷ',2:'ĐỘ LỆCH DƯƠNG / ÂM',
            3:'CHỌN ĐƯỜNG LÀM NHỎ NHẤT SSE',4:'MÔ HÌNH DÙNG CẢ TÁM ĐIỂM'}
    g.add(hint(labels[k],color=CORAL if k<3 else GREEN))
    return g,None


def prediction(k):
    g=VGroup()
    if k==1:
        cc,P=cloud(showfit=True);g.add(cc)
        g.add(Dot(P(5,fitted(5)),radius=.108,color=GREEN),
              Line(P(5,0),P(5,fitted(5)),color=GREEN,stroke_width=2),
              hint('x=5  →  ŷ≈'+decimal(fitted(5)),color=GREEN))
    elif k==2:
        cc,P=cloud(showfit=True,bounds=(0,12,0,13));g.add(cc)
        g.add(Line(P(8,fitted(8)),P(11,fitted(11)),color=CORAL,stroke_width=3),
              hint('VƯỢT QUÁ 8 GIỜ: NGOẠI SUY',color=CORAL))
    elif k==3:
        cc,_=cloud(showfit=True,showresiduals=True);g.add(cc)
        g.add(hint('R² = 6/7 ≈ 0,857',color=GREEN))
    else:
        cc,_=cloud(showfit=True);g.add(cc)
        g.add(hint('ĐƯỜNG PHÙ HỢP ≠ QUAN HỆ NHÂN QUẢ',color=CORAL))
    return g,None


def caution(k):
    g=VGroup()
    if k==1:
        # True animation: the final point moves from (8,9) to (8,18).
        chart,P=axes(0,9,0,20);g.add(chart)
        for xx,yy in zip(X[:-1],Y[:-1]):g.add(Dot(P(xx,yy),radius=.057,color=CYAN))
        tracker=ValueTracker(0.0)
        g.add(always_redraw(lambda:Dot(P(8,9+9*tracker.get_value()),radius=.115,color=CORAL)))
        g.add(hint('THỬ KÉO ĐIỂM CUỐI LÊN 18',color=CORAL))
        return g,tracker
    if k==2:
        chart,_=cloud(X,CURVED_Y,bounds=(0,9,0,13),color=PURPLE);g.add(chart)
        g.add(hint('PHI TUYẾN: r = 0, VẪN CÓ QUAN HỆ'))
    elif k==3:
        chart,_=cloud(showfit=False);g.add(chart)
        g.add(hint('BIẾN THỨ BA CÓ THỂ ẢNH HƯỞNG CẢ HAI'))
    else:
        chart,_=cloud(showfit=True);g.add(chart)
        g.add(hint('XEM HÌNH • NGOẠI LỆ • MIỀN x • NHÂN QUẢ'))
    return g,None


def practice(k):
    g=VGroup()
    chart,_=cloud(PRACTICE_X,PRACTICE_Y,showfit=(k>=3),
                  bounds=(0,6,0,12),color=PURPLE)
    g.add(chart)
    if k==1:g.add(hint('HÃY TÍNH r VÀ ĐƯỜNG HỒI QUY'))
    elif k==2:g.add(hint('TRUNG BÌNH: x=3; y=7'))
    elif k==3:g.add(hint('ŷ = 1 + 2x; r = 1',color=GREEN))
    else:g.add(hint('LIÊN HỆ TUYẾN TÍNH ≠ NHÂN QUẢ',color=GREEN))
    return g,None


VISUALS=(two_clouds,direction,pearson,regression,least_squares,prediction,caution,practice)

class STAT17(Scene):
    def frame(self):
        bg=Rectangle(width=14.222,height=8,fill_color=BG,fill_opacity=1,stroke_width=0)
        g=VGroup(bg)
        for x in (XL,XR):
            g.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                    stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        g.add(label('SANGMATH  /  THỐNG KÊ  /  TƯƠNG QUAN VÀ HỒI QUY',0,3.47,18,WHITE,True,13),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,12))
        return g

    def notes(self,b):
        title='\n'.join(textwrap.wrap(b.title,28,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,36,break_long_words=False))
        g=VGroup(label(title,XR,2.08,20,WHITE,True,5.75,1.17),
                 Line((.70,.76,0),(6.16,.76,0),color=EDGE,stroke_width=1),
                 label(thesis,XR,-.06,16,GOLD,True,5.70,1.60))
        if b.step>=3:
            path=ROOT/'assets/stat17_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not path.is_file():raise FileNotFoundError(f'STAT17 SVG missing {path}; run scripts/build_stat17_typst.py')
            svg=SVGMobject(str(path))
            if svg.width>4.85:svg.scale_to_fit_width(4.85)
            if svg.height>.90:svg.scale_to_fit_height(.90)
            svg.move_to((XR,-1.51,0))
            g.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.95,14,CYAN,True,5.8),svg)
        else:
            g.add(label('ĐỌC DỮ KIỆN  →  SUY LUẬN',XR,-1.48,14,GREEN,True,5.8))
        g.add(label('BỘ DỮ LIỆU GIẢ LẬP · KHÔNG KẾT LUẬN NHÂN QUẢ',XR,-2.49,11,MUTED,maxw=5.8))
        return g

    def construct(self):
        self.add(self.frame())
        file=ROOT/'stat17/runtime_plan.json'
        if not file.is_file():raise FileNotFoundError('Run scripts/prepare_stat17.py first')
        plan=json.loads(file.read_text(encoding='utf8'))
        if plan.get('scene')!='STAT17' or len(plan.get('beats',[]))!=32:
            raise ValueError('STAT17 runtime plan invalid')
        old_visual=old_note=None
        for i,b in enumerate(BEATS):
            row=plan['beats'][i]
            if (row['chapter'],row['step'])!=(b.chapter,b.step):raise ValueError(f'Plan mismatch at beat {i+1}')
            if row.get('voice'):
                audio=ROOT/row['voice']
                if not audio.is_file():raise FileNotFoundError(audio)
                self.add_sound(str(audio))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45);used=1.45
            else:
                self.play(FadeOut(old_visual),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05);used=1.60
            if tracker is not None:
                self.play(tracker.animate.set_value(1),run_time=3.0)
                used+=3.0
            self.wait(.35);used+=.35
            pause=float(row['duration'])-used
            if pause<=0:raise ValueError('Beat duration too short')
            self.wait(pause)
            old_visual,old_note=visual,note

class STAT17_SMOKE(STAT17):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(visual,note)
            self.wait(.12)
            self.remove(visual,note)
