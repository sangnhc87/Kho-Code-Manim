"""STAT05: range, IQR and Tukey boxplot. Run: manim -ql stat05/scene.py STAT05.
The first rendering is intentionally checked by GitHub smoke render in the workflow.
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat05.lesson import (BEATS,BASE,EXTREME,EXTREME_DATA,COMPARE,SPREAD,
                          CONSTANT,EXERCISE,EXERCISE_DATA,GROUPS,SAME_RANGE,box_summary)
from stat01.lesson import SCORES

config.background_color='#0A1522'
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
BG='#0A1522';PANEL='#10293B';ALT='#18394E';EDGE='#355A71'
WHITE='#EDF6FF';MUTED='#AAC5D6';CYAN='#56CBE9';GOLD='#FFD379'
GREEN='#67DDB5';CORAL='#FF8E87';PURPLE='#B7A9FC';L=-3.43;R=3.43


def label(s,x,y,size=18,color=WHITE,bold=False,maxw=None,maxh=None):
    obj=Text(str(s),font=FONT,font_size=size,color=color,
             weight='BOLD' if bold else 'NORMAL',line_spacing=.93)
    if maxw is not None and obj.width>maxw:obj.scale_to_fit_width(maxw)
    if maxh is not None and obj.height>maxh:obj.scale_to_fit_height(maxh)
    return obj.move_to((x,y,0))


def heading(s):return label(s,L,2.47,20,CYAN,True,6.05)

def footer(s):return label(s,L,-2.58,12,MUTED,False,6.05)

def line_axis(vmin=0,vmax=32,y=-.8,ticks=()):
    xleft,xright=-6.06,-.85
    def X(v):return xleft+(v-vmin)/(vmax-vmin)*(xright-xleft)
    base=VGroup(Line((xleft,y,0),(xright,y,0),color=MUTED,stroke_width=2))
    for tick in ticks:
        x=X(tick)
        base.add(Line((x,y-.10,0),(x,y+.10,0),color=MUTED,stroke_width=1.3),
                 label(str(tick),x,y-.33,12,MUTED))
    return base,X


def point_row(data,X,y=-1.1,small=False):
    group=VGroup()
    seen={}
    for value in sorted(data):
        rank=seen.get(value,0);seen[value]=rank+1
        if rank>11:continue
        x=X(value)
        group.add(Dot((x,y+rank*(.116 if small else .134),0),
                      radius=.050 if small else .068,
                      color=GOLD if value==7 else CYAN))
    return group


def box_shape(summary,X,y=0,color=CYAN,show_box=True,show_med=True,
              show_whiskers=True,show_outliers=True,height=.56):
    g=VGroup()
    q1,q2,q3=summary['q1'],summary['median'],summary['q3']
    if show_whiskers:
        left,right=summary['lower_whisker'],summary['upper_whisker']
        g.add(Line((X(left),y,0),(X(q1),y,0),color=color,stroke_width=3),
              Line((X(q3),y,0),(X(right),y,0),color=color,stroke_width=3))
        for pos in (left,right):
            g.add(Line((X(pos),y-.20,0),(X(pos),y+.20,0),color=color,stroke_width=3))
    if show_box:
        width=max(.015,abs(X(q3)-X(q1)))
        g.add(Rectangle(width=width,height=height,stroke_color=color,stroke_width=2.6,
                        fill_color=color,fill_opacity=.22).move_to(((X(q1)+X(q3))/2,y,0)))
    if show_med:
        g.add(Line((X(q2),y-height/2,0),(X(q2),y+height/2,0),color=GOLD,stroke_width=3.7))
    if show_outliers:
        for v in summary['outliers']:
            g.add(Dot((X(v),y,0),radius=.105,color=CORAL))
    return g


def chips(items,y):
    g=VGroup()
    count=len(items);gap=5.55/count
    for i,(value,color) in enumerate(items):
        x=-6.02+(i+.5)*gap
        w=min(1.09,gap-.12)
        g.add(RoundedRectangle(width=w,height=.45,corner_radius=.06,
             stroke_color=color,stroke_width=1.2,fill_color=ALT,fill_opacity=1).move_to((x,y,0)),
             label(str(value),x,y,16,color,True,w-.08))
    return g


def chapter1(step):
    g=VGroup(heading('HAI CỰC TRỊ VÀ KHOẢNG BIẾN THIÊN'))
    ax,X=line_axis(0,32,-.73,(0,4,8,10,20,30));g.add(ax)
    if step==1:
        g.add(point_row(SCORES,X,y=-.55,small=True))
    else:
        g.add(point_row(SCORES if step<4 else EXTREME_DATA,X,y=-.55,small=True))
        for v,c in ((4,GREEN),(10 if step<4 else 30,CORAL)):
            g.add(Dot((X(v),-.73,0),radius=.12,color=c),label(str(v),X(v),.91,17,c,True))
    if step>=3:
        g.add(Line((X(4),-.15,0),(X(30 if step==4 else 10),-.15,0),color=GOLD,stroke_width=4))
        g.add(label('R = 26' if step==4 else 'R = 10 − 4 = 6',L,1.77,23,GOLD,True,maxw=5.7))
    if step==1:g.add(label('MỖI CHẤM LÀ MỘT ĐIỂM GIẢ LẬP',L,1.72,16,GREEN,True,maxw=6.0))
    g.add(footer('Giá trị 30 là thí nghiệm số học, không phải điểm hợp lệ thang 10'))
    return g,None


def chapter2(step):
    g=VGroup(heading('NĂM MỐC ĐẶC TRƯNG TRÊN CÙNG TRỤC'))
    ax,X=line_axis(3,11,-.59,(4,5,6,7,8,9,10));g.add(ax)
    values=[(4,MUTED),(6,CYAN),(7,GOLD),(8,GREEN),(10,MUTED)]
    for i,(v,c) in enumerate(values[:(3 if step==1 else 5)]):
        g.add(Line((X(v),-.59,0),(X(v),.48,0),color=c,stroke_width=2.7),
              label(str(v),X(v),.76,18,c,True))
    if step>=2:
        g.add(Line((X(6),-.07,0),(X(8),-.07,0),color=GREEN,stroke_width=8))
    if step>=3:g.add(chips([('Min 4',MUTED),('Q1 6',CYAN),('Q2 7',GOLD),('Q3 8',GREEN),('Max 10',MUTED)],-1.39))
    if step==4:g.add(label('R = 6      •      IQR = 2',L,-2.09,22,GOLD,True,maxw=5.9))
    g.add(footer('40 điểm thống nhất với STAT01–STAT04'))
    return g,None


def chapter3(step):
    g=VGroup(heading('DỰNG BIỂU ĐỒ HỘP QUA BỐN BƯỚC'))
    ax,X=line_axis(3,11,-1.2,(4,5,6,7,8,9,10));g.add(ax)
    g.add(box_shape(BASE,X,y=.55,color=CYAN,show_box=True,show_med=step>=2,show_whiskers=step>=3))
    g.add(label('HỘP Q1 ĐẾN Q3',L,1.83,16,GREEN,True))
    if step>=2:g.add(label('VẠCH TRUNG VỊ Q2',L,1.27,15,GOLD,True))
    if step>=3:g.add(label('RÂU: 4 VÀ 10',L,-1.92,16,CYAN,True))
    if step==4:g.add(chips([('4',MUTED),('6',CYAN),('7',GOLD),('8',GREEN),('10',MUTED)],-2.11))
    g.add(footer('Dữ liệu gốc không có ngoại lệ theo ngưỡng 1,5 × IQR'))
    return g,None


def chapter4(step):
    g=VGroup(heading('PHÁT HIỆN NGOẠI LỆ BẰNG QUY TẮC TUKEY'))
    ax,X=line_axis(0,32,-1.25,(0,3,6,10,20,30));g.add(ax)
    tracker=None
    g.add(box_shape(EXTREME,X,y=.49,color=CYAN,
                    show_outliers=False,show_whiskers=True))
    if step==1:
        tracker=ValueTracker(10)
        g.add(always_redraw(lambda: Dot((X(tracker.get_value()),.49,0),
                radius=.14,color=CORAL if tracker.get_value()>11 else GOLD)))
        g.add(always_redraw(lambda: label(f'X = {tracker.get_value():.1f}    R = {tracker.get_value()-4:.1f}',
                                      L,1.78,18,GOLD,True,maxw=6.0)))
    else:
        g.add(Dot((X(30),.49,0),radius=.14,color=CORAL),
              label('30: NGOẠI LỆ',X(24),1.76,17,CORAL,True,maxw=2.6))
    if step>=2:
        for v in (3,11):
            g.add(DashedLine((X(v),-1.00,0),(X(v),1.03,0),color=GOLD,stroke_width=2))
        g.add(label('HÀNG RÀO: 3 VÀ 11',L,1.73,18,GOLD,True,maxw=5.9))
    if step>=3:g.add(label('RÂU TẠI QUAN SÁT 4 VÀ 10, KHÔNG TẠI 3 VÀ 11',L,-2.04,14,GREEN,True,maxw=6.0))
    g.add(footer('Điểm ngoài ngưỡng là dấu hiệu cần xem xét, chưa chắc bị nhập sai'))
    return g,tracker


def chapter5(step):
    g=VGroup(heading('CÙNG TRUNG VỊ, HỘP KHÁC NHAU'))
    ax,X=line_axis(0,12,-1.67,(0,2,4,6,8,10,12));g.add(ax)
    summary1,summary2=COMPARE
    g.add(box_shape(summary1,X,y=.98,color=CYAN))
    g.add(label('MẪU A',-5.52,1.68,15,CYAN,True))
    if step>=2:g.add(label('Q1=3,5       IQR=4       Q3=7,5',L,.33,15,CYAN,True,maxw=5.85))
    if step>=3:
        g.add(box_shape(summary2,X,y=-.49,color=CORAL),
              label('MẪU B',-5.52,-.08,15,CORAL,True))
    if step>=4:g.add(label('TRUNG VỊ CÙNG 5,5 NHƯNG IQR: 4 VÀ 8',L,-2.22,15,GOLD,True,maxw=5.90))
    g.add(footer('Hai mẫu minh họa độc lập, cùng một trục số'))
    return g,None


def chapter6(step):
    g=VGroup(heading('CÙNG KHOẢNG BIẾN THIÊN, KHÁC IQR'))
    ax,X=line_axis(0,10,-1.78,(0,1,2,4,5,6,8,9,10));g.add(ax)
    g.add(box_shape(SPREAD[0],X,.92,color=PURPLE))
    if step>=2:g.add(label('MẪU A: IQR = 8',L,1.72,17,PURPLE,True))
    if step>=3:g.add(box_shape(SPREAD[1],X,-.46,color=GREEN),
                      label('MẪU B: IQR = 2',L,-.01,17,GREEN,True))
    if step==4:g.add(label('CẢ HAI ĐỀU CÓ R = 9 − 1 = 8',L,-2.21,16,GOLD,True,maxw=5.9))
    g.add(footer('Cùng R không có nghĩa cùng dạng phân bố'))
    return g,None


def chapter7(step):
    g=VGroup(heading('HIỂU QUY ƯỚC TRƯỚC KHI ĐỌC HỘP'))
    ax,X=line_axis(0,32,-1.42,(0,4,6,8,10,20,30));g.add(ax)
    if step==1:
        g.add(box_shape(EXTREME,X,.64,color=CORAL,show_outliers=False))
        g.add(Line((X(10),.64,0),(X(30),.64,0),color=CORAL,stroke_width=3),
              Line((X(30),.44,0),(X(30),.84,0),color=CORAL,stroke_width=3),
              label('RÂU TỚI CỰC TRỊ',L,1.69,19,CORAL,True))
    elif step==2:
        g.add(box_shape(CONSTANT,X,.65,color=GREEN),
              label('TẤT CẢ ĐỀU BẰNG 5   →   IQR = 0',L,1.70,18,GREEN,True,maxw=6.0))
    elif step==3:
        g.add(box_shape(CONSTANT,X,.65,color=GREEN),
              label('Q1 = Q3: HÀNG RÀO TRÙNG NHAU',L,1.70,16,GOLD,True,maxw=5.85))
    else:
        g.add(box_shape(EXTREME,X,.65,color=CYAN),
              label('TUKEY: TÁCH NGOẠI LỆ THÀNH ĐIỂM RIÊNG',L,1.70,16,GOLD,True,maxw=6.0))
    g.add(footer('Biểu đồ hộp tóm tắt; không thay thế biểu đồ phân bố'))
    return g,None


def chapter8(step):
    g=VGroup(heading('BÀI TẬP VỚI 11 SỐ – TỰ KIỂM TRA'))
    ax,X=line_axis(0,22,-1.31,(0,2,4,6,8,10,14,20));g.add(ax)
    g.add(point_row(EXERCISE_DATA,X,y=-.99,small=True))
    if step>=2:
        g.add(box_shape(EXERCISE,X,.62,color=GREEN,show_whiskers=step>=3,show_outliers=step>=3),
              label('Q1 = 4     Q2 = 6     Q3 = 8',L,1.78,17,GREEN,True,maxw=6.0))
    if step>=3:g.add(label('NGƯỠNG: −2 ĐẾN 14   •   RÂU 2 ĐẾN 9',L,-2.08,16,GOLD,True,maxw=5.9))
    if step==4:g.add(label('R = 18   IQR = 4   NGOẠI LỆ = 20',L,-2.43,14,CORAL,True,maxw=5.9))
    g.add(footer('Dữ liệu luyện tập riêng, tứ phân vị theo quy ước STAT04'))
    return g,None

VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)

class STAT05(Scene):
    def frame(self):
        g=VGroup(Rectangle(width=14.222,height=8,stroke_width=0,fill_color=BG,fill_opacity=1))
        for x in (L,R):
            g.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                                   stroke_color=EDGE,stroke_width=1,fill_color=PANEL,
                                   fill_opacity=1).move_to((x,-.01,0)))
        g.add(label('SANGMATH   /   THỐNG KÊ 05   /   ĐỘ PHÂN TÁN VÀ BIỂU ĐỒ HỘP',0,3.48,23,WHITE,True,maxw=13.2),
              Line((-6.70,3.09,0),(6.70,3.09,0),color=EDGE,stroke_width=1),
              label('THỐNG KÊ 10–12   •   QUY ƯỚC TỨ PHÂN VỊ SGK   •   MANIM + TYPST',0,-3.53,13,MUTED,maxw=13.0))
        return g

    def notes(self,beat):
        lines=VGroup(label(f'CHƯƠNG {beat.chapter:02d}/08    •    NHỊP {beat.step}/4',R,2.49,17,CYAN,True))
        title='\n'.join(textwrap.wrap(beat.title,26,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(beat.thesis,35,break_long_words=False))
        lines.add(label(title,R,1.73,27,WHITE,True,maxw=5.68,maxh=1.12),
                  Line((.70,.79,0),(6.18,.79,0),color=EDGE,stroke_width=1.1),
                  label(thesis,R,-.03,23,GOLD,True,maxw=5.70,maxh=1.48))
        keys=('range','five','construct','fences','compare','spread','conventions','exercise')
        source=ROOT/'assets'/'stat05_formulas'/f'{keys[beat.chapter-1]}.svg'
        if not source.is_file():
            raise FileNotFoundError(f'Typst asset missing: {source}; run build_stat05_typst.py')
        if beat.step>=3:
            formula=SVGMobject(str(source))
            if formula.width>5.3:formula.scale_to_fit_width(5.3)
            if formula.height>.85:formula.scale_to_fit_height(.85)
            formula.move_to((R,-1.49,0))
            lines.add(label('CÔNG THỨC / KIỂM CHỨNG',R,-.95,14,CYAN,True),formula)
        else:
            lines.add(label('QUAN SÁT HÌNH → DỰ ĐOÁN → KIỂM CHỨNG',R,-1.43,16,GREEN,True,maxw=5.7))
        lines.add(label('ĐỌC ĐÚNG QUY ƯỚC   •   KHÔNG ĐOÁN TỪ HÌNH',R,-2.51,13,MUTED,maxw=5.9))
        return lines

    def construct(self):
        self.add(self.frame())
        planfile=ROOT/'stat05'/'runtime_plan.json'
        if not planfile.is_file():
            raise FileNotFoundError('Missing runtime plan; run scripts/prepare_stat05.py')
        plan=json.loads(planfile.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT05' or len(plan.get('beats',[]))!=len(BEATS):
            raise ValueError('Outdated STAT05 runtime plan')
        old_visual=None;old_notes=None
        for i,beat in enumerate(BEATS):
            entry=plan['beats'][i]
            if (entry['chapter'],entry['step'])!=(beat.chapter,beat.step):
                raise ValueError(f'Wrong beat order at {i+1}')
            slot=float(entry['duration']);spent=0.0
            if entry.get('voice'):
                sound=ROOT/entry['voice']
                if not sound.is_file():raise FileNotFoundError(sound)
                self.add_sound(str(sound))
            visual,tracker=VISUALS[beat.chapter-1](beat.step)
            notes=self.notes(beat)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.5);spent+=1.5
            else:
                self.play(FadeOut(old_visual),FadeOut(old_notes),run_time=.65);spent+=.65
                self.play(FadeIn(visual),FadeIn(notes),run_time=1.15);spent+=1.15
            if tracker is not None:
                self.play(tracker.animate.set_value(30),run_time=4.0,rate_func=smooth);spent+=4.0
            elif beat.step in (2,3):
                self.play(Indicate(notes[3],color=GOLD,scale_factor=1.012),run_time=.85);spent+=.85
            else:
                self.wait(.6);spent+=.6
            if spent>=slot:raise ValueError(f'Beat {i+1} duration too short')
            self.wait(slot-spent)
            old_visual,old_notes=visual,notes

class STAT05_SMOKE(STAT05):
    """Cheap GitHub preflight: render each of 32 complete visual/Typst states.
    Unlike rendering only the first animations, this catches errors in later chapters.
    """
    def construct(self):
        self.add(self.frame())
        for beat in BEATS:
            visual,tracker=VISUALS[beat.chapter-1](beat.step)
            notes=self.notes(beat)
            self.add(visual,notes)
            self.wait(.17)
            self.remove(visual,notes)
