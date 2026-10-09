"""STAT01: 8 chapters, 32 narrated beats. Render: manim -ql stat01/scene.py STAT01
    Math typography: Typst SVG (precompiled by scripts/build_typst.py).
    Does not import MathTex or require LaTeX.
"""
from __future__ import annotations
import json
import math
import sys
import textwrap
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stat01.lesson import SCORES, SORTED_SCORES, FREQUENCY, RELATIVE, CUMULATIVE, N, BEATS, CHAPTERS

config.background_color = '#091421'
config.frame_width = 14.2222222
config.frame_height = 8
FONT = 'Noto Sans'
BG = '#091421'
PANEL = '#10273A'
ALT = '#16374D'
LINE = '#355268'
WHITE = '#EEF7FF'
MUTED = '#A9C4D5'
CYAN = '#48C6E9'
GOLD = '#F3C76A'
GREEN = '#5ED7A7'
CORAL = '#FA827F'
PURPLE = '#B7A0FF'
COLORS = {4: CORAL, 5:'#F6A874', 6:'#FFD185', 7:CYAN, 8:GREEN, 9:'#88A2FF', 10: PURPLE}
LEFT_X = -3.45
RIGHT_X = 3.42


def label(s: str, size=21, color=WHITE, bold=False, max_width=None, max_height=None):
    t = Text(str(s), font=FONT, font_size=size, color=color,
             weight='BOLD' if bold else 'NORMAL', line_spacing=0.95)
    if max_width and t.width > max_width:
        t.scale_to_fit_width(max_width)
    if max_height and t.height > max_height:
        t.scale_to_fit_height(max_height)
    return t


def located(s, x, y, **kw):
    return label(s, **kw).move_to((x,y,0))


def chip(s, x, y, width=2.0, active=False, color=None):
    edge = color or (GOLD if active else LINE)
    outer = RoundedRectangle(corner_radius=.09, width=width, height=.49,
                             stroke_color=edge, stroke_width=1.7,
                             fill_color=ALT, fill_opacity=1).move_to((x,y,0))
    inner = located(s, x, y, size=16, bold=active, color=GOLD if active else WHITE,
                    max_width=width-.16)
    return VGroup(outer,inner)


def base_caption(s):
    return located(s, LEFT_X, -2.56, size=17, color=MUTED, max_width=5.95)


def score_grid(data, highlight=None, title='40 KẾT QUẢ QUAN SÁT'):
    out = VGroup(located(title,LEFT_X,2.25,size=19,color=CYAN,bold=True,max_width=6.1))
    selected = VGroup()
    for idx, val in enumerate(data):
        col = idx % 8
        row = idx // 8
        x = LEFT_X - 2.56 + col * .73
        y = 1.56 - row * .77
        emphasize = highlight is not None and val in highlight
        bg = RoundedRectangle(corner_radius=.11, width=.59, height=.56,
                              stroke_width=2.1 if emphasize else 1,
                              stroke_color=GOLD if emphasize else LINE,
                              fill_color=COLORS[val] if emphasize else ALT,
                              fill_opacity=.96).move_to((x,y,0))
        foreground = BG if emphasize else WHITE
        tx = located(val,x,y,size=21,color=foreground,bold=True)
        both = VGroup(bg,tx)
        out.add(both)
        if emphasize: selected.add(both)
    return out, selected if len(selected) else out[0]


def frequency_table(step):
    out = VGroup()
    out.add(located('BẢNG TẦN SỐ - 40 ĐIỂM', LEFT_X, 2.27, size=19,color=CYAN,bold=True))
    out.add(located('ĐIỂM', LEFT_X-2.28,1.47,size=17,color=MUTED,bold=True))
    out.add(located('TẦN SỐ', LEFT_X-.32,1.47,size=17,color=MUTED,bold=True))
    out.add(located('CỘNG DỒN', LEFT_X+1.97,1.47,size=17,color=MUTED,bold=True))
    rows=VGroup();focus=VGroup()
    targets=[4,7,None,7]
    for i,(val,n) in enumerate(FREQUENCY.items()):
        yy=.94-i*.48
        emphasize = step==3 or val == targets[step-1]
        r=RoundedRectangle(width=5.86,height=.42,corner_radius=.055,
                           fill_color=ALT if i%2==0 else PANEL,fill_opacity=1,
                           stroke_color=GOLD if emphasize else LINE,
                           stroke_width=1.9 if emphasize else .8).move_to((LEFT_X,yy,0))
        nums=VGroup(located(str(val),LEFT_X-2.28,yy,size=19,color=COLORS[val],bold=True),
                    located(str(n),LEFT_X-.32,yy,size=19,color=WHITE,bold=True),
                    located(str(CUMULATIVE[val]),LEFT_X+1.97,yy,size=19,color=WHITE))
        row=VGroup(r,nums);rows.add(row)
        if emphasize:focus.add(r)
    out.add(rows)
    out.add(base_caption('Tổng tần số: 40   ·   Không bỏ sót quan sát'))
    return out, focus if len(focus) else rows


def bar_plot(step=1, cut_axis=False, select=None, title='BIỂU ĐỒ CỘT: TẦN SỐ'):
    out=VGroup(located(title,LEFT_X,2.42,size=19,color=CYAN,bold=True,max_width=6.2))
    bottom=-1.60
    top=1.75
    scale=(top-bottom)/10
    y0=bottom+(.0 if not cut_axis else .0)
    x_start=LEFT_X-2.56
    axis = Line((x_start-.44,bottom,0),(x_start-.44,1.85,0),color=MUTED,stroke_width=1.6)
    base = Line((x_start-.46,bottom,0),(x_start+6*.82+.45,bottom,0),color=MUTED,stroke_width=1.6)
    out.add(axis,base)
    marks=[0,2,4,6,8,10] if not cut_axis else [6,8,10]
    for mark in marks:
        y=bottom+mark*scale
        tick=Line((x_start-.48,y,0),(x_start+6*.82+.45,y,0),stroke_color=LINE,stroke_opacity=.7,stroke_width=.7)
        out.add(tick,located(str(mark),x_start-.68,y,size=12,color=MUTED))
    focus=VGroup()
    for i,(score,amount) in enumerate(FREQUENCY.items()):
        x=x_start + i*.82
        highlight=(score in select) if select is not None else (score==7 and step in (2,4))
        bar_height=amount*scale
        r=RoundedRectangle(corner_radius=.04,width=.56,height=max(.03,bar_height),
                          fill_opacity=.92, fill_color=COLORS[score],
                          stroke_color=GOLD if highlight else PANEL,
                          stroke_width=2 if highlight else .8)
        r.move_to((x,bottom+bar_height/2,0))
        out.add(r,located(str(score),x,bottom-.34,size=17,color=WHITE,bold=True),
                located(str(amount),x,bottom+bar_height+.19,size=14,color=GOLD if highlight else MUTED))
        if highlight:focus.add(r)
    out.add(base_caption('Chiều cao mỗi cột bằng số học sinh có điểm đó.'))
    return out,focus if len(focus) else out[0]


def dot_plot(step=3,sel=None):
    out=VGroup(located('BIỂU ĐỒ ĐIỂM: 40 CHẤM',LEFT_X,2.42,size=19,color=CYAN,bold=True))
    focus=VGroup()
    y0=-1.62
    out.add(Line((LEFT_X-3.05,y0,0),(LEFT_X+3.05,y0,0),stroke_width=1.6,color=MUTED))
    for j,(val,amount) in enumerate(FREQUENCY.items()):
        xx=LEFT_X-2.47+j*.82
        out.add(located(str(val),xx,y0-.32,size=17,color=WHITE,bold=True))
        for row in range(amount):
            strong=val == 7 if sel is None else val in sel
            dot=Dot((xx,y0+.19+row*.32,0),radius=.11,
                    color=COLORS[val] if strong else '#5C94B0')
            out.add(dot)
            if strong:focus.add(dot)
    out.add(base_caption('1 chấm = 1 học sinh. Mỗi nhóm có đúng f chấm.'))
    return out,focus


def proportions(step):
    out=VGroup(located('TỈ LỆ TRONG 40 QUAN SÁT',LEFT_X,2.25,size=19,color=CYAN,bold=True))
    focus=VGroup()
    total_width=5.95
    start=LEFT_X-total_width/2
    cursor=start
    for score,n in FREQUENCY.items():
        w=total_width*n/N
        rr=Rectangle(width=w,height=.93,fill_color=COLORS[score],fill_opacity=.92,
                     stroke_color=BG,stroke_width=2).move_to((cursor+w/2,.94,0))
        out.add(rr)
        if score==7 or (step==4 and score==8): focus.add(rr)
        if w>.43:
            out.add(located(str(score),cursor+w/2,.94,size=16,color=BG,bold=True,max_width=w-.05))
        cursor+=w
    percent_rows=[(4,5),(5,10),(6,20),(7,25),(8,20),(9,15),(10,5)]
    for j,(score,percent) in enumerate(percent_rows):
        x=LEFT_X-2.5+(j%4)*1.68
        y=-.12-(j//4)*.89
        out.add(chip(f'{score}: {percent}%',x,y,width=1.42,
                     active=(score == 7 and step in (1,2,3)) or (score==8 and step==4),color=COLORS[score]))
    out.add(base_caption('Tổng phần trăm: 5+10+20+25+20+15+5 = 100%.'))
    return out, focus if len(focus) else out[0]


def compare_axis():
    g=VGroup(located('CÙNG HAI GIÁ TRỊ, HAI CÁCH VẼ',LEFT_X,2.36,size=18,color=CYAN,bold=True))
    # Correct bars and misleading cropped-axis bars, same numerical heights 8 and 10.
    for cx,crop,title in [(LEFT_X-1.63,0,'TRỤC TỪ 0'),(LEFT_X+1.62,7,'TRỤC TỪ 7')]:
        g.add(located(title,cx,1.6,size=15,color=GREEN if crop==0 else CORAL,bold=True))
        baseline=-1.58
        if crop==0:ratio=.25
        else:ratio=.76
        for xshift,v in [(-.48,8),(.48,10)]:
            h=max(.08,(v-crop)*ratio)
            r=Rectangle(width=.69,height=h,fill_color=CYAN if v==8 else GOLD,
                        fill_opacity=.94,stroke_width=0).move_to((cx+xshift,baseline+h/2,0))
            g.add(r,located(str(v),cx+xshift,baseline+h+.2,size=14,color=WHITE))
        g.add(Line((cx-1.15,baseline,0),(cx+1.15,baseline,0),color=MUTED,stroke_width=2))
    g.add(base_caption('Chú ý: trục tung của biểu đồ bên phải bị cắt.'))
    return g,g


def data_quality(step):
    if step==1:return compare_axis()
    g=VGroup(located('KIỂM TRA CHẤT LƯỢNG DỮ LIỆU',LEFT_X,2.28,size=19,color=CYAN,bold=True))
    if step==2:
        top=chip('MÃ 12 · ĐIỂM 8',LEFT_X-.86,.99,width=2.6)
        dupe=chip('MÃ 12 · ĐIỂM 8',LEFT_X-.86,-.04,width=2.6,active=True,color=CORAL)
        arrow=Arrow((LEFT_X+.83,.94,0),(LEFT_X+.83,.02,0),buff=.17,color=CORAL)
        g.add(top,dupe,arrow,located('DỮ LIỆU NHẬP TRÙNG',LEFT_X,-1.2,size=21,color=CORAL,bold=True))
        focus=dupe
    elif step==3:
        sample=VGroup()
        for i,val in enumerate((8,9,9,10,8,9,10,8,9,10)):
            x=LEFT_X-2.61+(i%5)*1.26
            y=1.1-(i//5)*.88
            sample.add(chip(str(val),x,y,width=.88,active=True,color=GREEN))
        g.add(sample,located('10 HỌC SINH TỰ NGUYỆN',LEFT_X,-1.05,size=17,color=GOLD,bold=True),
              located('KHÔNG PHẢI MẪU NGẪU NHIÊN',LEFT_X,-1.62,size=16,color=CORAL,bold=True))
        focus=sample
    else:
        left=chip('TỔNG THỂ',LEFT_X-1.5,.73,width=2.2,active=True)
        right=chip('MẪU',LEFT_X+1.5,.73,width=2.2,active=True,color=GREEN)
        arrow=Arrow(left.get_right(),right.get_left(),buff=.22,color=WHITE,stroke_width=2.4)
        g.add(left,right,arrow,
              located('LẤY MẪU THÍCH HỢP  →  KẾT LUẬN PHÙ HỢP',LEFT_X,-.78,size=16,color=GOLD,bold=True,max_width=5.8))
        focus=VGroup(left,right)
    g.add(base_caption('Minh họa giả định, không phải dữ liệu thực của học sinh.'))
    return g,focus


def exercise(step):
    questions=[('ĐÚNG ĐIỂM 9', '6 học sinh'),
               ('ĐÚNG ĐIỂM 7', '25%'),
               ('TỪ ĐIỂM 8 TRỞ LÊN', '16 học sinh = 40%'),
               ('4 BƯỚC CỐT LÕI', 'Hỏi → kiểm tra → mô tả → kết luận')]
    g=VGroup(located('TỰ ĐỌC DỮ LIỆU',LEFT_X,2.28,size=21,color=CYAN,bold=True))
    focus=VGroup()
    for i,(question,answer) in enumerate(questions):
        x=LEFT_X
        y=1.23-i*.86
        active=(i == step-1)
        r=RoundedRectangle(width=5.87,height=.70,corner_radius=.1,
                fill_color=ALT if active else PANEL,fill_opacity=1,
                stroke_color=GOLD if active else LINE,stroke_width=2.3 if active else 1).move_to((x,y,0))
        g.add(r,located(question,LEFT_X-1.29,y,size=15,color=WHITE,bold=active,max_width=3.1),
              located(answer,LEFT_X+1.53,y,size=15,color=GREEN if active else MUTED,bold=active,max_width=2.38))
        if active:focus.add(r)
    g.add(base_caption('Hãy tạm dừng và tự trả lời trước khi xem đáp án.'))
    return g,focus


def model(beat):
    chapter=beat.chapter
    step=beat.step
    if chapter==1:
        return score_grid(SCORES, {7} if step==3 else ({4,10} if step==4 else None))
    if chapter==2:
        return score_grid(SORTED_SCORES, {4,10} if step==2 else ({7} if step==3 else None),
                          title='40 ĐIỂM ĐÃ SẮP XẾP')
    if chapter==3:
        return frequency_table(step)
    if chapter==4:
        if step==3 or step==4: return dot_plot(step)
        return bar_plot(step)
    if chapter==5:
        return proportions(step)
    if chapter==6:
        if step in (1,2):return bar_plot(step,select={8,9,10},title='NHÓM ĐIỂM TỪ 8 TRỞ LÊN')
        return dot_plot(step,sel={7})
    if chapter==7:return data_quality(step)
    return exercise(step)


class STAT01(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.draw_frame()
        plan_path=ROOT/'assets'/'runtime_plan.json'
        if plan_path.exists():
            plan=json.loads(plan_path.read_text(encoding='utf-8'))
        else:
            plan={'beats':[{'duration':b.duration,'voice':''} for b in BEATS]}
        old_vis=None;old_right=None
        for idx,beat in enumerate(BEATS):
            entry=plan['beats'][idx]
            target_duration=float(entry['duration'])
            audio=entry.get('voice','')
            if audio:
                voice_path=ROOT/audio
                if not voice_path.is_file():
                    raise RuntimeError(f'Missing voice audio: {voice_path}')
                self.add_sound(str(voice_path))
            visual,focus=model(beat)
            info=self.right_content(beat,idx)
            if old_vis is None:
                self.play(FadeIn(visual),FadeIn(info),run_time=1.50)
                transition_time=1.50
            elif beat.chapter==2 and beat.step==1:
                # GENUINE SORT ANIMATION: each individual student's card moves
                # to the correct rank. The same physical cards are conserved.
                order=sorted(range(N),key=lambda i:(SCORES[i],i))
                rank_of_old={old_idx:rank for rank,old_idx in enumerate(order)}
                motions=[old_vis[i+1].animate.move_to(
                    visual[rank_of_old[i]+1].get_center()) for i in range(N)]
                self.play(*motions,Transform(old_vis[0],visual[0]),
                          FadeOut(old_right),FadeIn(info),run_time=3.20)
                self.remove(old_vis)
                self.add(visual)
                transition_time=3.20
            else:
                self.play(FadeOut(old_vis),FadeOut(old_right),
                          FadeIn(visual),FadeIn(info),run_time=1.50)
                transition_time=1.50
            # Highlight mathematical objects, never decorative unrelated effects.
            if focus is not None and len(focus)>0:
                self.play(Circumscribe(focus,color=GOLD,fade_out=True,time_width=.4),
                          run_time=1.40)
            else:
                self.wait(1.40)
            remaining=target_duration-transition_time-1.40
            if remaining<0: raise ValueError(f'Invalid beat duration: {idx+1}')
            self.wait(remaining)
            old_vis=visual;old_right=info

    def draw_frame(self):
        background=Rectangle(width=14.22,height=8,
                             fill_color=BG,fill_opacity=1,stroke_width=0)
        self.add(background)
        top=located('SANGMATH  /  THỐNG KÊ 01  /  DỮ LIỆU BIẾT NÓI',
                    0,3.54,size=25,bold=True,color=WHITE,max_width=13.4)
        top_rule=Line((-6.75,3.13,0),(6.75,3.13,0),stroke_color=LINE,stroke_width=1.3)
        leftpanel=RoundedRectangle(width=6.65,height=5.94,corner_radius=.15,
                             fill_color=PANEL,fill_opacity=1,stroke_width=1.1,stroke_color=LINE)
        leftpanel.move_to((LEFT_X,-.02,0))
        rightpanel=RoundedRectangle(width=6.45,height=5.94,corner_radius=.15,
                             fill_color=PANEL,fill_opacity=1,stroke_width=1.1,stroke_color=LINE)
        rightpanel.move_to((RIGHT_X,-.02,0))
        footer=located('DỮ LIỆU GIẢ LẬP  ·  40 QUAN SÁT  ·  CÔNG THỨC TYPST  ·  HÌNH ĐỘNG MANIM',
                       0,-3.54,size=15,color=MUTED,max_width=12.7)
        self.add(leftpanel,rightpanel,top_rule,top,footer)

    def right_content(self,beat,idx):
        g=VGroup()
        g.add(located(f'CHƯƠNG {beat.chapter:02d}/08   •   NHỊP {beat.step}/4',
                      RIGHT_X,2.54,size=16,color=CYAN,bold=True,max_width=5.65))
        wrapped='\n'.join(textwrap.wrap(beat.title, width=31,break_long_words=False))
        g.add(located(wrapped,RIGHT_X,1.71,size=29,color=WHITE,bold=True,
                      max_width=5.65,max_height=1.16))
        line=Line((.6,.77,0),(6.25,.77,0),color=LINE,stroke_width=1.3)
        g.add(line)
        thesis='\n'.join(textwrap.wrap(beat.thought,width=34,break_long_words=False))
        g.add(located(thesis,RIGHT_X,-.15,size=25,color=GOLD,bold=True,max_width=5.7,max_height=1.32))
        # Typst vector mathematics is shown in dedicated space, not over text.
        expr = ('freq_sum' if beat.chapter==3 and beat.step==3 else
                'relative' if beat.chapter==5 and beat.step==1 else None)
        if expr:
            g.add(located('CÔNG THỨC KIỂM TRA',RIGHT_X,-.97,size=15,
                          color=CYAN,bold=True))
            svg=ROOT/'assets'/'formulas'/f'{expr}.svg'
            if svg.exists():
                formula=SVGMobject(str(svg))
                if formula.width>4.85:formula.scale_to_fit_width(4.85)
                if formula.height>.67:formula.scale_to_fit_height(.67)
                formula.move_to((RIGHT_X,-1.61,0))
                g.add(formula)
            else:
                equation=('2 + 4 + 8 + 10 + 8 + 6 + 2 = 40' if expr=='freq_sum'
                          else '10 / 40 × 100% = 25%')
                g.add(located(equation,RIGHT_X,-1.61,size=19,color=WHITE,
                              bold=True,max_width=5.15))
        else:
            notes=[('CỠ MẪU','40'),('SỐ GIÁ TRỊ KHÁC NHAU','7'),('ĐIỂM THƯỜNG GẶP NHẤT','7')]
            if beat.chapter==5:notes=[('TỔNG QUAN SÁT','40'),('NHÓM ĐIỂM 7','25%'),('TỔNG CÁC TỈ LỆ','100%')]
            if beat.chapter==6:notes=[('ĐIỂM ≥ 8','16'),('TẦN SỐ TƯƠNG ĐỐI','40%'),('ĐIỂM KHÁC NHAU','7')]
            if beat.chapter==7:notes=[('THU THẬP','Hợp lệ'),('XỬ LÝ','Không trùng'),('KẾT LUẬN','Đúng phạm vi')]
            if beat.chapter==8:notes=[('ĐÚNG ĐIỂM 9','6'),('ĐÚNG ĐIỂM 7','25%'),('ĐIỂM ≥ 8','40%')]
            for j,(a,b) in enumerate(notes):
                y=-1.2-j*.45
                g.add(located(a,RIGHT_X-1.22,y,size=15,color=MUTED,max_width=3.2),
                      located(b,RIGHT_X+2.0,y,size=16,color=GREEN,bold=True,max_width=1.45))
        g.add(located('BÀI HỌC: quan sát → đặt câu hỏi → rút kết luận',
                      RIGHT_X,-2.53,size=14,color=MUTED,max_width=5.75))
        return g
