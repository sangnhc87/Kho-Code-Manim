"""STAT03 - Mean, median and mode (Manim Community >=0.19).
manim -ql -r 854,480 --fps 24 stat03/scene.py STAT03
Requires only Manim for silent fallback; Typst SVG and TTS are optional prebuilt assets.
"""
from __future__ import annotations
import json
import sys
import textwrap
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat03.lesson import (BEATS,CHAPTERS,FREQUENCY,N,SCORES,SORTED,SUM,MEAN,
                            MEDIAN,MODES,BASE,CHANGED,TRANSFORMED)

config.background_color='#091421'
config.frame_width=14.2222222
config.frame_height=8
FONT='Noto Sans'
BG='#091421'; PANEL='#102739'; ALT='#16384A'; LINE='#355A70'
WHITE='#EDF6FF'; MUTED='#A2BECD'; CYAN='#54C8E9'; GOLD='#FFD47A'
GREEN='#63D9B4'; CORAL='#FF8B84'; PURPLE='#BBA7FC'
COLORS={4:'#F08788',5:'#F9AD76',6:'#FFCF79',7:'#52C8E9',
        8:'#62D8B5',9:'#9EABFF',10:'#CBAAF5'}
LEFT=-3.42; RIGHT=3.43


def label(text,x,y,size=18,color=WHITE,bold=False,width=None,height=None):
    obj=Text(str(text),font=FONT,font_size=size,color=color,
             weight='BOLD' if bold else 'NORMAL',line_spacing=.96)
    if width is not None and obj.width>width: obj.scale_to_fit_width(width)
    if height is not None and obj.height>height: obj.scale_to_fit_height(height)
    return obj.move_to((x,y,0))

def visual_heading(text):
    return label(text,LEFT,2.48,19,CYAN,True,width=5.90)

def visual_foot(text):
    return label(text,LEFT,-2.55,14,MUTED,width=6.05)

def badge(text,x,y,w=.6,h=.55,accent=False,color=CYAN,size=17):
    block=RoundedRectangle(width=w,height=h,corner_radius=.09,
            stroke_color=GOLD if accent else LINE,stroke_width=2.1 if accent else .9,
            fill_color=ALT,fill_opacity=1).move_to((x,y,0))
    t=label(text,x,y,size=size,color=GOLD if accent else WHITE,
            bold=accent,width=w-.10,height=h-.07)
    return VGroup(block,t)

def horizontal_axis(xmin,xmax,y,xlo=-6.04,xhi=-.81,ticks=()):
    group=VGroup(Line((xlo,y,0),(xhi,y,0),color=MUTED,stroke_width=2))
    def xx(v):return xlo+(v-xmin)/(xmax-xmin)*(xhi-xlo)
    for v in ticks:
        x=xx(v)
        group.add(Line((x,y-.085,0),(x,y+.085,0),color=MUTED,stroke_width=1.6),
                  label(str(v),x,y-.31,12,MUTED))
    return group,xx

def overview_visual(step):
    g=VGroup(visual_heading('40 ĐIỂM – BA CÂU HỎI'))
    axis,xx=horizontal_axis(3.5,10.5,-1.48,ticks=range(4,11))
    g.add(axis)
    for v,f in sorted(FREQUENCY.items()):
        for j in range(f):
            g.add(Dot((xx(v),-1.23+j*.245,0),radius=.091,
                color=GOLD if step==3 and v==7 else COLORS[v]))
    if step in (2,3,4):
        summary=[('N = 40','TỔNG = 284'),('TB = 7,1','TV = 7 · MỐT = 7'),
                 ('3 SỐ ĐẶC TRƯNG','KHÔNG THAY BIỂU ĐỒ')][step-2]
        g.add(label(summary[0],LEFT-1.35,1.94,18,GOLD,True,width=3),
              label(summary[1],LEFT+1.40,1.94,17,GREEN,True,width=3))
    g.add(visual_foot('40 điểm minh họa · Dữ liệu duy nhất cho STAT01–03'))
    return g,None

def mean_visual(step):
    g=VGroup(visual_heading('TRUNG BÌNH – ĐIỂM CÂN BẰNG'))
    axis,xx=horizontal_axis(3.5,10.5,-1.80,ticks=range(4,11))
    g.add(axis)
    for v,f in sorted(FREQUENCY.items()):
        x=xx(v); h=.22*f
        bar=RoundedRectangle(width=.49,height=h,corner_radius=.035,
             fill_opacity=.95,fill_color=COLORS[v],stroke_width=0).move_to((x,-1.8+h/2,0))
        g.add(bar)
        if step>=2:
            g.add(label(str(f),x,-1.65+h+.17,13,MUTED))
    if step>=2:
        g.add(label('4×2  +  5×4  +  6×8  +  …  +  10×2',LEFT,.92,19,WHITE,True,width=5.9))
    if step>=3:
        g.add(label('TỔNG = 284',LEFT-1.14,1.77,20,GOLD,True),
              label('284 / 40 = 7,1',LEFT+1.38,1.77,21,GREEN,True))
    if step==4:
        marker=DashedLine((xx(MEAN),-1.57,0),(xx(MEAN),1.56,0),
                 stroke_color=GOLD,stroke_width=3,dash_length=.12)
        g.add(marker,label('7,1',xx(MEAN),1.80,18,GOLD,True))
    g.add(visual_foot('Trung bình dùng tất cả các giá trị và tần số'))
    return g,None

def median_visual(step):
    g=VGroup(visual_heading('TRUNG VỊ – GIỮA DANH SÁCH'))
    for i,v in enumerate(SORTED):
        col=i%10; row=i//10
        x=-6.08+col*.594; y=1.62-row*.69
        chosen=step in (2,3) and i in (19,20)
        g.add(badge(str(v),x,y,w=.49,h=.45,accent=chosen,color=GOLD,size=15))
        if chosen: g.add(label(str(i+1),x,y-.35,11,GOLD,True))
    if step>=2:
        g.add(label('HAI VỊ TRÍ GIỮA: 20 VÀ 21',LEFT,-1.29,17,GOLD,True,width=5.95))
    if step>=3:
        g.add(label('(7 + 7) / 2 = 7',LEFT,-1.81,22,GREEN,True))
    if step==4:
        g.add(label('9 GIÁ TRỊ → VỊ TRÍ THỨ 5',LEFT,-1.81,16,GREEN,True))
    g.add(visual_foot('Phải sắp xếp dữ liệu trước khi xác định trung vị'))
    return g,None

def mode_visual(step):
    g=VGroup(visual_heading('MỐT – GIÁ TRỊ THƯỜNG GẶP'))
    a,xx=horizontal_axis(3.5,10.5,-1.65,ticks=range(4,11));g.add(a)
    for v,f in sorted(FREQUENCY.items()):
        x=xx(v);h=f*.31
        active= v==7 and step in (1,2)
        rect=RoundedRectangle(width=.47,height=h,corner_radius=.035,
            fill_color=GOLD if active else COLORS[v],fill_opacity=1,
            stroke_width=0).move_to((x,-1.65+h/2,0))
        g.add(rect,label(str(f),x,-1.44+h,13,GOLD if active else MUTED,bold=active))
    if step>=2:g.add(label('Mo = 7     TẦN SỐ = 10',LEFT,1.90,20,GOLD,True,width=5.9))
    if step==3:
        g.add(label('VÍ DỤ HAI MỐT: 2, 2, 3, 3, 4',LEFT,-2.12,14,GREEN,True,width=5.9))
    if step==4:
        g.add(label('DỮ LIỆU PHÂN LOẠI CŨNG CÓ MỐT',LEFT,-2.12,14,GREEN,True,width=5.9))
    g.add(visual_foot('Mốt là giá trị có tần số lớn nhất, không phải điểm cao nhất'))
    return g,None

def outlier_visual(step):
    g=VGroup(visual_heading('KÉO MỘT GIÁ TRỊ NGOẠI LỆ'))
    initial=9 if step<=2 else 27
    tracker=ValueTracker(initial)
    axis,xx=horizontal_axis(4,28,-1.25,ticks=(5,7,9,15,21,27))
    g.add(axis)
    for j,v in enumerate(BASE[:-1]):
        # place repeats on separate rows so all eight observations remain visible
        x=xx(v); y=-.70+(.32 if j%2==0 else 0)
        g.add(Dot((x,y,0),radius=.098,color=CYAN))
    movable=always_redraw(lambda: Dot((xx(tracker.get_value()),-.54,0),radius=.142,color=CORAL))
    mean_line=always_redraw(lambda: DashedLine((xx((54+tracker.get_value())/9),-1.10,0),
                    (xx((54+tracker.get_value())/9),1.22,0),stroke_color=GOLD,
                    stroke_width=2.3,dash_length=.1))
    mean_label=always_redraw(lambda: label('TB = '+f'{(54+tracker.get_value())/9:.1f}'.replace('.',','),
                         LEFT+1.00,1.84,20,GOLD,True))
    g.add(mean_line,movable,mean_label)
    g.add(label('TV = 7',LEFT-2.03,1.83,19,GREEN,True),
          label('Mo = 7',LEFT-2.03,1.29,17,CYAN,True))
    g.add(label('9 PHÚT',xx(9),-1.94,12,MUTED,True))
    if step>=2:
        g.add(label('→ 27 PHÚT',LEFT+1.95,-2.05,16,CORAL,True))
    g.add(visual_foot('Dữ liệu THỜI GIAN giả lập · không phải điểm kiểm tra'))
    return g,tracker if step==2 else None

def compare_visual(step):
    g=VGroup(visual_heading('CHỌN CHỈ SỐ THEO MỤC ĐÍCH'))
    cards=[('TRUNG BÌNH','Tổng ÷ số quan sát','7,1',CYAN),
           ('TRUNG VỊ','Vị trí ở giữa','7',GREEN),
           ('MỐT','Xuất hiện nhiều nhất','7',GOLD)]
    for i,(title,sub,result,c) in enumerate(cards):
        y=1.42-i*1.24
        rect=RoundedRectangle(width=5.55,height=1.06,corner_radius=.15,
              fill_color=ALT,fill_opacity=1,stroke_color=c if (i==step-1 and step<=3) else LINE,
              stroke_width=2.3 if (i==step-1 and step<=3) else .9).move_to((LEFT,y,0))
        g.add(rect,label(title,LEFT-.75,y+.22,18,c,True,width=3.4),
              label(sub,LEFT-.75,y-.19,14,MUTED,width=3.4),
              label(result,LEFT+2.00,y,25,GOLD if i==step-1 else WHITE,True))
    if step==4:
        g.add(label('CÙNG TRUNG BÌNH ≠ CÙNG PHÂN BỐ',LEFT,-2.42,15,CORAL,True,width=5.8))
    g.add(visual_foot('Một giá trị đại diện không thay thế cả phân bố'))
    return g,None

def transform_visual(step):
    g=VGroup(visual_heading('PHÉP TỊNH TIẾN DỮ LIỆU'))
    axis,xx=horizontal_axis(3.5,12.5,-1.48,ticks=(4,6,8,10,12))
    g.add(axis)
    values=TRANSFORMED if step>=2 else SCORES
    counts={x:values.count(x) for x in sorted(set(values))}
    for v,f in counts.items():
        for j in range(f):
            g.add(Dot((xx(v),-1.22+j*.235,0),radius=.087,
                    color=GOLD if v==9 else (GREEN if step>=2 else CYAN)))
    if step>=2:
        g.add(label('MỖI GIÁ TRỊ  + 2',LEFT,2.03,21,GOLD,True))
    if step>=3:
        g.add(label('TB: 7,1 → 9,1',LEFT-1.43,1.68,17,GREEN,True),
              label('TV: 7 → 9',LEFT+1.42,1.68,17,GREEN,True))
    if step==4:
        g.add(label('Mo: 7 → 9',LEFT,-2.09,17,GREEN,True))
    g.add(visual_foot('Phép biến đổi toán học · không phải quyết định cộng điểm'))
    return g,None

def exercise_visual(step):
    g=VGroup(visual_heading('BÀI TẬP NGƯỢC – ĐIỀN SỐ'))
    group=(5,6,7,8,'?' if step<3 else 9)
    for i,v in enumerate(group):
        x=LEFT-2.12+i*1.05
        g.add(badge(str(v),x,.68,w=.76,h=.70,accent=i==4,
                    size=27))
    g.add(label('5 SỐ · TRUNG BÌNH = 7',LEFT,1.84,21,CYAN,True))
    if step>=2:
        g.add(label('TỔNG PHẢI CÓ: 5 × 7 = 35',LEFT,-.43,18,GOLD,True))
        g.add(label('4 SỐ ĐÃ BIẾT: 5 + 6 + 7 + 8 = 26',LEFT,-1.14,17,WHITE,True,width=5.96))
    if step>=3:
        g.add(label('SỐ CÒN THIẾU = 35 − 26 = 9',LEFT,-1.89,17,GREEN,True,width=6))
    if step==4:
        g.add(label('TB = 7,1       TV = 7       Mo = 7',LEFT,-2.25,16,GREEN,True,width=6))
    g.add(visual_foot('Tìm tổng trước, rồi mới suy ra giá trị chưa biết'))
    return g,None

VISUALS=(overview_visual,mean_visual,median_visual,mode_visual,
         outlier_visual,compare_visual,transform_visual,exercise_visual)

class STAT03(Scene):
    def frame(self):
        frame=VGroup(Rectangle(width=14.22,height=8,fill_color=BG,fill_opacity=1,stroke_width=0))
        for x,w in ((LEFT,6.50),(RIGHT,6.54)):
            frame.add(RoundedRectangle(width=w,height=5.88,corner_radius=.13,
                 stroke_color=LINE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        frame.add(label('SANGMATH  /  THỐNG KÊ 03  /  TRUNG BÌNH – TRUNG VỊ – MỐT',0,3.52,
                  24,WHITE,True,width=13.25),
              Line((-6.68,3.10,0),(6.68,3.10,0),color=LINE,stroke_width=1.2),
              label('40 ĐIỂM GIẢ LẬP  •  ĐỌC ĐÚNG BẢN CHẤT  •  MANIM + TYPST',0,-3.55,
                  14,MUTED,width=13.1))
        return frame

    def notes(self,b):
        panel=VGroup(label(f'CHƯƠNG {b.chapter:02d}/08   ·   NHỊP {b.step}/4',
                   RIGHT,2.53,17,CYAN,True))
        heading='\n'.join(textwrap.wrap(b.title,width=28,break_long_words=False))
        panel.add(label(heading,RIGHT,1.75,28,WHITE,True,width=5.8,height=1.02),
                  Line((.60,.83,0),(6.20,.83,0),color=LINE,stroke_width=1.2))
        thesis='\n'.join(textwrap.wrap(b.thesis,width=36,break_long_words=False))
        panel.add(label(thesis,RIGHT,-.03,24,GOLD,True,width=5.8,height=1.36))
        formula_map={1:'overview',2:'mean',3:'median',4:'mode',5:'outlier',
                     6:'compare',7:'shift',8:'exercise'}
        key=formula_map[b.chapter]
        source=ROOT/'assets'/'stat03_formulas'/f'{key}.svg'
        if source.is_file() and b.step>=2:
            try:
                svg=SVGMobject(str(source))
                if svg.width>5.0:svg.scale_to_fit_width(5.0)
                if svg.height>.93:svg.scale_to_fit_height(.93)
                svg.move_to((RIGHT,-1.52,0))
                panel.add(label('CÔNG THỨC / KIỂM CHỨNG',RIGHT,-.94,15,CYAN,True),svg)
            except Exception:
                panel.add(label('Xem hình và lập luận theo từng bước',RIGHT,-1.42,18,GREEN,True,width=5.4))
        else:
            chapter_vals=(('40 quan sát','3 số đặc trưng'),('284 điểm','Trung bình 7,1'),
                          ('Vị trí 20–21','Trung vị 7'),('Tần số 10','Mốt 7'),
                          ('9 → 27 phút','TB: 7 → 9'),('Cùng một bộ số','Ba câu hỏi'),
                          ('Cộng 2 đơn vị','TB: 7,1 → 9,1'),('5 số','Tổng cần có 35'))
            one,two=chapter_vals[b.chapter-1]
            panel.add(label(one,RIGHT-1.42,-1.46,17,MUTED,width=2.8),
                      label(two,RIGHT+1.44,-1.46,18,GREEN,True,width=2.8))
        panel.add(label('TRUNG THỰC VỚI DỮ LIỆU · GIẢI THÍCH TRƯỚC KHI TÍNH',
                  RIGHT,-2.50,13,MUTED,width=5.94))
        return panel

    def construct(self):
        self.add(self.frame())
        runtime=ROOT/'stat03'/'runtime_plan.json'
        if runtime.exists():
            plan=json.loads(runtime.read_text(encoding='utf-8'))
            if plan.get('scene')!='STAT03' or len(plan.get('beats',[]))!=len(BEATS):
                raise ValueError('Stale STAT03 runtime_plan; run scripts/prepare_stat03.py')
        else:
            plan={'beats':[{'duration':b.duration,'voice':''} for b in BEATS]}
        previous_g=None;previous_r=None
        for i,b in enumerate(BEATS):
            entry=plan['beats'][i]
            slot=float(entry['duration']);spent=0.
            if entry.get('voice'):
                path=ROOT/entry['voice']
                if not path.is_file():raise FileNotFoundError(path)
                self.add_sound(str(path))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            notes=self.notes(b)
            if previous_g is None:
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.5);spent+=1.5
            else:
                self.play(FadeOut(previous_g),FadeOut(previous_r),run_time=.65);spent+=.65
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.25);spent+=1.25
            if tracker is not None:
                self.play(tracker.animate.set_value(27),run_time=3.2,rate_func=smooth);spent+=3.2
            elif b.chapter in (2,3,4,8) and b.step in (2,3):
                self.play(Indicate(notes[2],color=GOLD,scale_factor=1.025),run_time=1.05);spent+=1.05
            else:
                self.wait(.8);spent+=.8
            if spent>=slot:raise ValueError(f'Beat {i+1} exceeds configured duration')
            self.wait(slot-spent)
            previous_g,previous_r=visual,notes
