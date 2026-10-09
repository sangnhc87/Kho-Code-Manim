"""STAT04: Quartiles. Manim CE >= 0.19; render: manim -ql stat04/scene.py STAT04.
Visuals derive from the same 40 synthetic scores used by STAT01-STAT03.
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat04.lesson import (BEATS, SORTED, SCORES, N, FREQUENCY, CUMULATIVE,
                           Q1,Q2,Q3,EVEN,ODD,EXTREME,SHIFTED,GROUP_A,GROUP_B,UNKNOWN_ANSWER)

config.background_color='#091421'
config.frame_width=14.2222222
config.frame_height=8
FONT='Noto Sans'; BG='#091421'; PANEL='#102739'; ALT='#16384A'; LINE='#355A70'
WHITE='#EDF6FF'; MUTED='#AAC2D1'; CYAN='#54C8E9'; GOLD='#FFD47A'
GREEN='#63D9B4'; CORAL='#FF8B84'; PURPLE='#BBA7FC'
CLR={4:'#F08788',5:'#F9AD76',6:'#FFCF79',7:'#52C8E9',8:'#62D8B5',9:'#9EABFF',10:'#CBAAF5'}
L=-3.42;R=3.43


def txt(s,x,y,size=18,color=WHITE,bold=False,w=None,h=None):
    t=Text(str(s),font=FONT,font_size=size,color=color,weight='BOLD' if bold else 'NORMAL',line_spacing=.97)
    if w is not None and t.width>w:t.scale_to_fit_width(w)
    if h is not None and t.height>h:t.scale_to_fit_height(h)
    return t.move_to((x,y,0))

def card(v,x,y,hi=False,color=None,width=.48,height=.43,size=15):
    t=RoundedRectangle(width=width,height=height,corner_radius=.064,
        stroke_width=2.0 if hi else .7,stroke_color=GOLD if hi else LINE,
        fill_color=ALT,fill_opacity=1).move_to((x,y,0))
    n=txt(str(v),x,y,size,GOLD if hi else (color or CLR.get(v,WHITE)),hi,w=width-.08,h=height-.08)
    return VGroup(t,n)

def head(s):return txt(s,L,2.52,19,CYAN,True,w=6.0)
def foot(s):return txt(s,L,-2.53,13,MUTED,w=6.00)

def strip(data,positions=(),colors=None,start_y=1.58):
    res=VGroup();positions=set(positions)
    for i,v in enumerate(data):
        row=i//10;col=i%10;x=-6.08+col*.592;y=start_y-row*.65
        active=i+1 in positions
        special=color_for_position(i+1,colors) if colors else None
        res.add(card(v,x,y,hi=active,color=special))
    return res

def color_for_position(index,spec):
    if spec=='halves':return CYAN if index<=20 else PURPLE
    if spec=='quarters':return [CORAL,CYAN,GREEN,PURPLE][min((index-1)//10,3)]
    return None

def axis(xmin,xmax,y,ticks):
    xlo=-6.12;xhi=-.87
    def xx(v):return xlo+(float(v)-xmin)*(xhi-xlo)/(xmax-xmin)
    g=VGroup(Line((xlo,y,0),(xhi,y,0),color=MUTED,stroke_width=2))
    for k in ticks:
        x=xx(k);g.add(Line((x,y-.075,0),(x,y+.075,0),color=MUTED,stroke_width=1.5),
             txt(str(k),x,y-.30,12,MUTED))
    return g,xx

def put_summary(g,step,items):
    if step>=2:
        for i,(s,c) in enumerate(items[:max(1,step-1)]):
            g.add(txt(s,L+(i-(len(items)-1)/2)*1.73,-1.71,16,c,True,w=1.66))

def chapter1(step):
    g=VGroup(head('40 ĐIỂM – SẮP XẾP ĐỂ PHÂN VỊ'))
    data=SCORES if step==1 else SORTED
    g.add(strip(data,colors='quarters' if step>=3 else None))
    if step>=2:g.add(txt('DÃY ĐÃ SẮP XẾP KHÔNG GIẢM',L,-1.30,17,GREEN,True,w=5.9))
    if step>=3:
        marks=[(1,10,CORAL),(11,20,CYAN),(21,30,GREEN),(31,40,PURPLE)]
        for i,(lo,hi,c) in enumerate(marks):
            x=-5.70+i*1.46
            g.add(RoundedRectangle(width=1.22,height=.35,corner_radius=.06,fill_color=c,fill_opacity=.14,
                    stroke_color=c,stroke_width=1).move_to((x,-1.86,0)),
                  txt(f'{lo}–{hi}',x,-1.86,13,c,True))
    if step==4:g.add(txt('KHÔNG CHIA ĐỀU KHOẢNG ĐIỂM 4 → 10',L,-2.24,13,CORAL,True,w=5.8))
    g.add(foot('Dữ liệu giả lập, thống nhất với STAT01–STAT03'))
    return g,None

def chapter2(step):
    g=VGroup(head('TRUNG VỊ VÀ HAI NỬA DỮ LIỆU'))
    targets=(20,21) if step==2 else ()
    g.add(strip(SORTED,targets,'halves'))
    if step>=2:
        g.add(txt('NỬA DƯỚI: 1–20',L-1.48,-1.33,16,CYAN,True,w=2.7),
              txt('NỬA TRÊN: 21–40',L+1.55,-1.33,16,PURPLE,True,w=2.8))
    if step>=2:g.add(txt('Q₂ = (x₂₀ + x₂₁)/2 = 7',L,-1.98,19,GOLD,True,w=5.95))
    if step>=3:g.add(txt('Q₁: TRUNG VỊ NỬA DƯỚI     ·     Q₃: TRUNG VỊ NỬA TRÊN',L,-2.28,13,GREEN,True,w=6.0))
    g.add(foot('n = 40 là số chẵn; mỗi nửa có 20 quan sát'))
    return g,None

def chapter3(step):
    targets=(() if step==1 else (10,11) if step==2 else (30,31) if step==3 else (10,11,20,21,30,31))
    g=VGroup(head('TÌM 6 VỊ TRÍ QUYẾT ĐỊNH TỨ PHÂN VỊ'))
    g.add(strip(SORTED,targets,'quarters'))
    specs=[('VỊ TRÍ 10–11  →  Q₁ = 6',GOLD),('VỊ TRÍ 20–21  →  Q₂ = 7',CYAN),('VỊ TRÍ 30–31  →  Q₃ = 8',GREEN)]
    for j,(s,c) in enumerate(specs[:step] if step<4 else specs):
        g.add(txt(s,L,-1.35-j*.39,15,c,True,w=5.85))
    g.add(foot('Các chỉ số vị trí không phải là giá trị điểm'))
    return g,None

def chapter4(step):
    g=VGroup(head('BẢNG TẦN SỐ TÍCH LŨY'))
    xs=[-5.78+i*.80 for i in range(7)]
    rows=[('ĐIỂM',tuple(FREQUENCY)),('TẦN SỐ',tuple(FREQUENCY.values())),('TÍCH LŨY',tuple(v for _,v in CUMULATIVE))]
    for j,(t,values) in enumerate(rows):
        y=1.60-j*.77
        g.add(txt(t,L,y+.29,12,CYAN,True))
        for i,v in enumerate(values):
            active=step>=2 and ((step==2 and v==14 and j==2) or (step==3 and v==24 and j==2) or (step==4 and v==32 and j==2))
            g.add(card(v,xs[i],y-.15,hi=active,width=.66,height=.41,size=16))
    prompts={1:'CỘNG DỒN SỐ QUAN SÁT',2:'VỊ TRÍ 10–11 NẰM TRONG NHÓM 6',
             3:'VỊ TRÍ 20–21 NẰM TRONG NHÓM 7',4:'VỊ TRÍ 30–31 NẰM TRONG NHÓM 8'}
    g.add(txt(prompts[step],L,-1.49,15,GOLD if step>=2 else GREEN,True,w=5.92))
    if step==4:g.add(txt('Q₁ = 6       Q₂ = 7       Q₃ = 8',L,-2.00,19,GREEN,True,w=5.9))
    g.add(foot('Đếm vị trí qua tần số tích lũy, không cần trải đủ 40 thẻ'))
    return g,None

def chapter5(step):
    g=VGroup(head('SO SÁNH CỠ MẪU CHẴN VÀ LẺ'))
    data=EVEN if step==1 else ODD
    targets={1:(2,3,4,5,6,7),2:(5,),3:(2,3,5,7,8),4:(5,)}[step]
    for i,v in enumerate(data):
        x=-5.76+i*.63
        g.add(card(v,x,.80,hi=i+1 in targets,width=.52,height=.58,size=22))
        g.add(txt(str(i+1),x,.28,12,GOLD if i+1 in targets else MUTED))
    if step==1:
        g.add(txt('8 SỐ  →  Q₁=2,5   Q₂=4,5   Q₃=6,5',L,-.72,17,GREEN,True,w=5.9))
    else:
        g.add(txt('9 SỐ  →  BỎ VỊ TRÍ GIỮA KHI CHIA NỬA',L,-.70,16,GOLD,True,w=5.95))
        if step>=3:g.add(txt('Q₁=2,5       Q₂=5       Q₃=7,5',L,-1.42,18,GREEN,True,w=5.95))
        if step==4:g.add(txt('QUY ƯỚC SGK: TRUNG VỊ CỦA HAI NỬA',L,-1.94,14,CORAL,True,w=5.95))
    g.add(foot('Quy ước phần mềm khác có thể cho kết quả khác'))
    return g,None

def chapter6(step):
    g=VGroup(head('NGOẠI LỆ VÀ PHÉP DỊCH DỮ LIỆU'))
    tracker=None
    ay,xx=axis(3,31,-.97,(4,8,12,20,30));g.add(ay)
    vals=SCORES if step==1 else EXTREME if step in (2,3) else SHIFTED
    xs=[v for v in vals if v<=12]
    for i,v in enumerate(xs):
        # deterministic stacking by value, with visual jitter to avoid covering repeats
        rank=sum(1 for x in xs[:i] if x==v)
        g.add(Dot((xx(v),-.71+rank*.103,0),radius=.054,color=CLR.get(v,CYAN)))
    if step in (1,2):
        tracker=ValueTracker(10)
        dot=always_redraw(lambda: Dot((xx(tracker.get_value()),-.24,0),radius=.13,color=CORAL))
        g.add(dot)
    if step>=2:
        g.add(txt('MỘT ĐIỂM: 10 → 30' if step in (2,3) else 'MỖI ĐIỂM + 2',L,1.83,19,CORAL if step<4 else GOLD,True))
    if step>=3:
        g.add(txt('Q₁=6   Q₂=7   Q₃=8' if step==3 else 'Q₁=8   Q₂=9   Q₃=10',L,1.28,18,GREEN,True))
        g.add(txt('TRUNG BÌNH 7,1 → 7,6' if step==3 else 'IQR KHÔNG ĐỔI: 2',L,-1.79,16,GOLD,True))
    if step==1:g.add(txt('HÃY DỰ ĐOÁN BA TỨ PHÂN VỊ KHI CÓ NGOẠI LỆ',L,1.76,15,GOLD,True,w=5.85))
    g.add(foot('Ngoại lệ minh họa: chỉ thay một quan sát của dữ liệu giả lập'))
    return g,tracker if step==2 else None

def chapter7(step):
    g=VGroup(head('KHOẢNG TỨ PHÂN VỊ – VÙNG TRUNG TÂM'))
    ax,xx=axis(0,12,-1.65,(0,2,4,6,8,10,12));g.add(ax)
    if step==1:
        vals=(6,7,8)
        g.add(Rectangle(width=xx(8)-xx(6),height=.76,fill_color=GREEN,fill_opacity=.24,
                         stroke_color=GREEN,stroke_width=2.4).move_to(((xx(6)+xx(8))/2,-.69,0)))
        for s,c in zip(vals,(CORAL,GOLD,CYAN)):
            g.add(Line((xx(s),-1.65,0),(xx(s),-.22,0),color=c,stroke_width=2.4),txt(str(s),xx(s),.06,19,c,True))
        g.add(txt('IQR = 8 − 6 = 2',L,1.78,21,GOLD,True))
    else:
        for k,data in enumerate((GROUP_A,GROUP_B)):
            y=1.12-k*.99;lo,mid,hi=(3.5,5.5,7.5) if k==0 else (2,5.5,10)
            c=CYAN if k==0 else CORAL
            g.add(Line((xx(min(data)),y,0),(xx(max(data)),y,0),color=MUTED),
                  Rectangle(width=xx(hi)-xx(lo),height=.39,fill_color=c,fill_opacity=.29,
                            stroke_color=c,stroke_width=2).move_to(((xx(lo)+xx(hi))/2,y,0)),
                  Line((xx(mid),y-.25,0),(xx(mid),y+.25,0),color=GOLD,stroke_width=2.5),
                  txt('MẪU '+('A' if k==0 else 'B'),-5.90,y+.37,14,c,True))
        if step>=3:g.add(txt('TRUNG VỊ = 5,5 CHO CẢ HAI MẪU',L,-.15,15,GOLD,True))
        if step>=3:g.add(txt('IQR(A) = 4    ·    IQR(B) = 8',L,-.65,17,GREEN,True))
        if step==4:g.add(txt('5 MỐC  →  BIỂU ĐỒ HỘP Ở STAT05',L,-2.18,14,GREEN,True))
    g.add(foot('Khoảng tứ phân vị khác khoảng biến thiên'))
    return g,None

def chapter8(step):
    g=VGroup(head('BÀI TOÁN NGƯỢC – TÌM GIÁ TRỊ CÒN THIẾU'))
    values=(3,4,5,'?' if step<3 else 6,7,8,9,10)
    for i,v in enumerate(values):
        x=-5.83+i*.69
        active=i==3
        g.add(card(v,x,1.03,hi=active,width=.57,height=.67,size=22),
              txt(str(i+1),x,.55,12,GOLD if active else MUTED))
    g.add(txt('BIẾT TRUNG VỊ Q₂ = 6,5',L,2.07,17,CYAN,True))
    if step>=2:g.add(txt('(x + 7) / 2 = 6,5    →    x = 6',L,-.17,19,GOLD,True,w=5.9))
    if step>=3:g.add(txt('Q₁ = 4,5      Q₃ = 8,5      IQR = 4',L,-.93,16,GREEN,True,w=6.0))
    if step==4:g.add(txt('SẮP XẾP  →  Q₂  →  Q₁, Q₃  →  KIỂM TRA',L,-1.65,14,CYAN,True,w=5.96))
    g.add(foot('Bài luyện tập độc lập, không thuộc bộ 40 điểm'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)

class STAT04(Scene):
    def frame(self):
        g=VGroup(Rectangle(width=14.222,height=8,fill_color=BG,fill_opacity=1,stroke_width=0))
        for x,w in ((L,6.53),(R,6.54)):
            g.add(RoundedRectangle(width=w,height=5.92,corner_radius=.13,stroke_color=LINE,
                stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        g.add(txt('SANGMATH  /  THỐNG KÊ 04  /  TỨ PHÂN VỊ Q₁ – Q₂ – Q₃',0,3.49,24,WHITE,True,w=13.35),
              Line((-6.65,3.09,0),(6.65,3.09,0),color=LINE,stroke_width=1.1),
              txt('THỐNG KÊ 10–12   ·   TỨ PHÂN VỊ THEO QUY ƯỚC SGK   ·   MANIM + TYPST',0,-3.53,14,MUTED,w=13.0))
        return g
    def notes(self,b):
        panel=VGroup(txt(f'CHƯƠNG {b.chapter:02d}/08    •    NHỊP {b.step}/4',R,2.52,17,CYAN,True))
        title='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        panel.add(txt(title,R,1.71,28,WHITE,True,w=5.70,h=1.15),
                  Line((.67,.83,0),(6.24,.83,0),color=LINE,stroke_width=1.0),
                  txt(thesis,R,-.05,23,GOLD,True,w=5.77,h=1.52))
        keys=('overview','halves','positions','cumulative','odd','outlier','iqr','exercise')
        source=ROOT/'assets'/'stat04_formulas'/f'{keys[b.chapter-1]}.svg'
        if source.is_file() and b.step>=2:
            try:
                svg=SVGMobject(str(source))
                if svg.width>5.0:svg.scale_to_fit_width(5.0)
                if svg.height>.90:svg.scale_to_fit_height(.90)
                svg.move_to((R,-1.55,0))
                panel.add(txt('CÔNG THỨC / KIỂM CHỨNG',R,-.99,14,CYAN,True),svg)
            except Exception:
                panel.add(txt('Quan sát các vị trí trên hình',R,-1.50,17,GREEN,True,w=5.3))
        else:
            panel.add(txt(['40 số liệu giả lập','Chia hai nửa dữ liệu','Kiểm tra các vị trí',
                           'Dựa vào bảng tích lũy','Đối chiếu chẵn và lẻ','Thay đổi dữ liệu',
                           'So sánh độ trải rộng','Thử làm trước khi xem đáp án'][b.chapter-1],
                           R,-1.51,18,GREEN,True,w=5.5))
        panel.add(txt('GIẢI THÍCH VỊ TRÍ TRƯỚC · CÔNG THỨC SAU',R,-2.54,13,MUTED,w=5.91))
        return panel
    def construct(self):
        self.add(self.frame())
        runtime=ROOT/'stat04'/'runtime_plan.json'
        if runtime.exists():
            plan=json.loads(runtime.read_text(encoding='utf-8'))
            if plan.get('scene')!='STAT04' or len(plan.get('beats',[]))!=len(BEATS):
                raise ValueError('Stale runtime plan; run scripts/prepare_stat04.py')
        else:
            plan={'beats':[{'duration':b.duration,'voice':''} for b in BEATS]}
        old=None;old_notes=None
        for i,b in enumerate(BEATS):
            entry=plan['beats'][i];slot=float(entry['duration']);spent=0
            if entry.get('voice'):
                sound=ROOT/entry['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            if old is None:
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.5);spent+=1.5
            else:
                self.play(FadeOut(old),FadeOut(old_notes),run_time=.67);spent+=.67
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.18);spent+=1.18
            if tracker is not None:
                self.play(tracker.animate.set_value(30),run_time=3.8,rate_func=smooth);spent+=3.8
            elif b.step in (2,3):
                self.play(Indicate(notes[3],color=GOLD,scale_factor=1.015),run_time=.95);spent+=.95
            else:
                self.wait(.7);spent+=.7
            if spent>=slot:raise ValueError(f'Beat {i+1} too short for its animation')
            self.wait(slot-spent)
            old,old_notes=visual,notes
