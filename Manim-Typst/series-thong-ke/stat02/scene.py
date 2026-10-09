"""STAT02 - Choosing and reading statistical charts.
Render: manim -ql -r 854,480 --fps 24 stat02/scene.py STAT02
Typography: Noto Sans and optional Typst-compiled vector SVG.
All numerical objects come from stat02.lesson, including STAT01's scores.
"""
from __future__ import annotations
import json
import sys
import textwrap
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat02.lesson import (BEATS,CHAPTERS,FREQUENCY,SCORE_VALUES,PERCENT,PIE_ANGLES,
    CLASS_B,CLASS_B_PCT,GROUP_EDGES,GROUP_COUNT,GROUP_DENSITY,MONTHS,MONTHLY_MEAN,
    TIME_CLASSES,TIME_DENSITY,SCORES,N)

config.background_color='#091421'
config.frame_width=14.2222222
config.frame_height=8
FONT='Noto Sans'
BG='#091421'; PANEL='#10273A'; ALT='#16374D'; LINE='#355268'
WHITE='#EDF7FF'; MUTED='#A7C4D6'; CYAN='#52C8EE'; GOLD='#FFD476'
GREEN='#62D8AF'; CORAL='#FF8381'; PURPLE='#C0A6FF'
COLORS={4:'#F78786',5:'#FFA973',6:'#F6CB77',7:'#5AC7ED',
        8:'#58D6A3',9:'#909EFE',10:'#C09EFF'}
LEFT=-3.45; RIGHT=3.43

def txt(s,x=0,y=0,size=19,color=WHITE,bold=False,limit=None,height=None):
    m=Text(str(s),font=FONT,font_size=size,weight='BOLD' if bold else 'NORMAL',
           color=color,line_spacing=.95)
    if limit and m.width>limit:m.scale_to_fit_width(limit)
    if height and m.height>height:m.scale_to_fit_height(height)
    return m.move_to((x,y,0))

def panel_title(s):
    return txt(s,LEFT,2.45,size=19,color=CYAN,bold=True,limit=5.98)

def foot(s):
    return txt(s,LEFT,-2.56,size=15,color=MUTED,limit=5.96)

def pill(s,x,y,w=1.20,chosen=False,color=CYAN):
    p=RoundedRectangle(width=w,height=.53,corner_radius=.10,
        stroke_color=GOLD if chosen else LINE,stroke_width=2 if chosen else 1,
        fill_color=ALT,fill_opacity=1).move_to((x,y,0))
    t=txt(s,x,y,size=15,color=GOLD if chosen else WHITE,bold=chosen,limit=w-.13)
    return VGroup(p,t)

def axis(ybase=-1.55, x0=-6.03,x1=-.82, ymax=2.02, step=2,maxval=10):
    g=VGroup(Line((x0,ybase,0),(x1,ybase,0),color=MUTED,stroke_width=1.8),
             Line((x0,ybase,0),(x0,ymax,0),color=MUTED,stroke_width=1.8))
    for y in range(0,maxval+1,step):
        yy=ybase+(y/maxval)*(ymax-ybase)
        g.add(Line((x0,yy,0),(x1,yy,0),stroke_color=LINE,stroke_width=.65,
                   stroke_opacity=.64),txt(str(y),x0-.29,yy,size=11,color=MUTED))
    return g

def table_visual(step):
    g=VGroup(panel_title('40 ĐIỂM – MỘT DỮ LIỆU GỐC'))
    highlight=VGroup()
    for i,s in enumerate(SCORES):
        x=LEFT-2.55+(i%8)*.73; y=1.70-(i//8)*.70
        strong=step==3 and s==7
        tile=RoundedRectangle(width=.59,height=.53,corner_radius=.09,
               stroke_color=GOLD if strong else LINE,
               stroke_width=2 if strong else .8,
               fill_color=COLORS[s] if strong else ALT,fill_opacity=1).move_to((x,y,0))
        num=txt(str(s),x,y,size=18,bold=True,color=BG if strong else WHITE)
        g.add(tile,num)
        if strong:highlight.add(tile)
    g.add(foot('Dữ liệu giả lập · n = 40 · Một nguồn cho mọi biểu đồ'))
    return g,highlight,VGroup()

def frequency_visual(step):
    g=VGroup(panel_title('BIỂU ĐỒ CỘT – TẦN SỐ'))
    g.add(axis())
    bars=VGroup();focus=VGroup();reveal=VGroup()
    x0=-5.55
    for j,v in enumerate(SCORE_VALUES):
        x=x0+j*.70
        f=FREQUENCY[v];h=f*3.57/10
        bar=RoundedRectangle(width=.52,height=h,corner_radius=.035,
               fill_color=COLORS[v],fill_opacity=.97,
               stroke_color=GOLD if step==2 and v==7 else BG,
               stroke_width=2.5 if step==2 and v==7 else .7).move_to((x,-1.55+h/2,0))
        bars.add(bar);reveal.add(bar)
        g.add(txt(str(v),x,-1.91,size=17,bold=True),
              txt(str(f),x,-1.55+h+.19,size=15,color=GOLD if v==7 and step==2 else MUTED))
        if (step==2 and v==7) or (step==3 and v in (6,8)):
            focus.add(bar)
    g.add(bars)
    if step==4:
        g.add(txt('MỖI CHẤM = 1 HỌC SINH',LEFT,.88,size=16,color=GOLD,bold=True))
        # The dots preserve the 40 observations; bars are still shown as context.
        dots=VGroup()
        for j,v in enumerate(SCORE_VALUES):
            x=x0+j*.70
            for k in range(FREQUENCY[v]):
                dots.add(Dot((x,-1.34+k*.30,0),radius=.063,color=WHITE))
        g.add(dots);focus=dots;reveal=dots
    g.add(foot('Cột rời nhau · mỗi giá trị điểm là một nhóm'))
    return g,focus,reveal

def pie_visual(step):
    g=VGroup(panel_title('BIỂU ĐỒ TRÒN – CƠ CẤU 40 ĐIỂM'))
    pieces=VGroup(); focus=VGroup();theta=PI/2
    pie_center=(LEFT-1.18,.25,0)
    for v in SCORE_VALUES:
        angle=TAU*FREQUENCY[v]/N
        sector=Sector(radius=1.69,start_angle=theta,angle=angle,
                      fill_color=COLORS[v],fill_opacity=1,
                      stroke_color=BG,stroke_width=2).shift(pie_center)
        pieces.add(sector)
        if (step==2 and v==7) or (step==3 and v==9):focus.add(sector)
        theta+=angle
    g.add(pieces)
    for j,v in enumerate(SCORE_VALUES):
        yy=1.94-j*.50
        swatch=Rectangle(width=.25,height=.25,fill_color=COLORS[v],
                         fill_opacity=1,stroke_width=0).move_to((LEFT+1.05,yy,0))
        g.add(swatch,txt(f'{v}: {int(PERCENT[v])}%  •  {int(PIE_ANGLES[v])}°',
             LEFT+2.18,yy,size=15,limit=2.5))
    g.add(foot('Diện tích và góc của mỗi phần phản ánh cùng tỉ lệ'))
    return g,focus,pieces

def percent_visual(step):
    g=VGroup(panel_title('SO SÁNH HAI LỚP BẰNG PHẦN TRĂM'))
    rows=[('LỚP A',40,40),('LỚP B',50,50)] # each tuple: label, N, percent >=8
    x0=LEFT-2.75;width=5.6;focus=VGroup();reveal=VGroup()
    for j,(name,total,pct) in enumerate(rows):
        yy=.72-j*1.43
        g.add(txt(f'{name}  (n = {total})',LEFT-1.63,yy+.59,size=16,
                  bold=True,color=CYAN))
        bg=Rectangle(width=width,height=.67,fill_color=ALT,fill_opacity=1,
                     stroke_width=.8,stroke_color=LINE).move_to((x0+width/2,yy,0))
        active=Rectangle(width=width*pct/100,height=.67,fill_color=GREEN,
                     fill_opacity=.93,stroke_width=0).move_to((x0+width*pct/200,yy,0))
        g.add(bg,active,txt(f'{pct}%',x0+.56,yy,size=16,bold=True,color=BG),
              txt(f'{100-pct}%',x0+width-.56,yy,size=16,bold=True,color=WHITE))
        reveal.add(active)
        if (step<=2 and j==0) or (step>=3 and j==1):focus.add(active)
    if step>=2:
        g.add(txt('A: 16/40 = 40%',LEFT,-1.38,size=18,color=GOLD,bold=True))
    if step>=3:
        g.add(txt('B: 25/50 = 50%',LEFT,-1.91,size=18,color=GOLD,bold=True))
    g.add(foot('So sánh tỉ trọng khi cỡ lớp khác nhau'))
    return g,focus,reveal

def histogram_visual(step):
    if step<3:
        g=VGroup(panel_title('HISTOGRAM – GHÉP NHÓM ĐIỂM'))
        x0=LEFT-2.70;w=1.33;bottom=-1.50
        g.add(Line((x0-.10,bottom,0),(x0+4*w+.18,bottom,0),stroke_color=MUTED))
        f=VGroup();reveal=VGroup()
        for i,count in enumerate(GROUP_COUNT):
            # equal-width classes: count vs density makes only a fixed scale change
            h=count*.18;xx=x0+(i+.5)*w
            rect=Rectangle(width=w,height=h,fill_color=(CYAN,GREEN,PURPLE,GOLD)[i],
                    fill_opacity=.85,stroke_color=BG,stroke_width=1.5)
            rect.move_to((xx,bottom+h/2,0))
            g.add(rect,txt(f'{GROUP_EDGES[i]}–{GROUP_EDGES[i+1]}',xx,bottom-.34,size=14),
                  txt(str(count),xx,bottom+h+.19,size=14,color=WHITE,bold=True))
            reveal.add(rect)
            if (step==1 and i==0) or (step==2 and i==1):f.add(rect)
        g.add(foot('Bốn khoảng liền nhau, cùng độ rộng 2 điểm'))
        return g,f,reveal
    g=VGroup(panel_title('HISTOGRAM – CÁC KHOẢNG KHÁC RỘNG'))
    x0=LEFT-2.80;bottom=-1.48;scale=.133;f=VGroup();reveal=VGroup()
    g.add(Line((x0-.12,bottom,0),(x0+40*scale+.2,bottom,0),color=MUTED,stroke_width=1.7))
    for i,(a,b,count) in enumerate(TIME_CLASSES):
        density=count/(b-a)
        h=density*2.65
        w=(b-a)*scale
        xx=x0+(a+b)*.5*scale
        r=Rectangle(width=w,height=h,fill_color=(CYAN,GREEN,GOLD)[i],
                    fill_opacity=.91,stroke_color=BG,stroke_width=1.4).move_to((xx,bottom+h/2,0))
        g.add(r,txt(f'{a}–{b}',xx,bottom-.33,size=14),
              txt(f'f = {count}',xx,bottom+h+.20,size=14,color=GOLD if step==4 else WHITE))
        reveal.add(r)
        if i==(0 if step==3 else 2):f.add(r)
    g.add(txt('CHIỀU CAO = TẦN SỐ / ĐỘ RỘNG LỚP',LEFT,2.03,
              size=14,color=GOLD,bold=True,limit=5.75))
    g.add(foot('Dữ liệu thời gian riêng · diện tích mỗi cột = tần số'))
    return g,f,reveal

def trend_visual(step):
    g=VGroup(panel_title('BIỂU ĐỒ ĐƯỜNG – THEO 6 THÁNG'))
    x0=LEFT-2.65;bottom=-1.42;width=5.23
    g.add(Line((x0,bottom,0),(x0+width+.1,bottom,0),color=MUTED),
          Line((x0,bottom,0),(x0,1.85,0),color=MUTED))
    for val in (5.5,6.0,6.5,7.0,7.5,8.0):
        y=bottom+(val-5.5)*1.17
        g.add(Line((x0,y,0),(x0+width,y,0),stroke_color=LINE,stroke_width=.5),
              txt(f'{val:.1f}',x0-.32,y,size=11,color=MUTED))
    pts=[];points=VGroup()
    for i,v in enumerate(MONTHLY_MEAN):
        xx=x0+.38+i*.86;yy=bottom+(v-5.5)*1.17
        pts.append((xx,yy,0))
        g.add(txt(MONTHS[i],xx,bottom-.32,size=16))
        mark=Dot((xx,yy,0),radius=.095,color=GOLD)
        points.add(mark)
        if step>=2:g.add(txt(f'{v:.1f}',xx,yy+.27,size=13,color=WHITE))
    lines=VGroup(*[Line(pts[i],pts[i+1],color=CYAN,stroke_width=3) for i in range(5)])
    g.add(lines,points)
    focus=VGroup(lines[1]) if step==2 else (points if step in (1,4) else lines)
    if step==3:
        g.add(pill('DANH MỤC TÙY Ý ≠ THỜI GIAN',LEFT,-2.10,w=4.72,chosen=True))
    g.add(foot('Bộ dữ liệu sáu tháng độc lập · không lấy từ 40 điểm'))
    return g,focus,lines

def caution_visual(step):
    if step==1:
        g=VGroup(panel_title('CÙNG HAI SỐ – TRỤC KHÁC NHAU'));focus=VGroup()
        for j,(base,maxrange,title) in enumerate(((0,10,'TRỤC TỪ 0'),(7,10,'TRỤC TỪ 7'))):
            cx=LEFT+(-1.56 if j==0 else 1.58)
            g.add(txt(title,cx,1.78,size=15,bold=True,color=GREEN if j==0 else CORAL))
            b=-1.35
            for dx,value,col in ((-.50,8,CYAN),(.50,10,GOLD)):
                h=(value-base)/(maxrange-base)*2.46
                r=Rectangle(width=.65,height=h,fill_color=col,fill_opacity=.90,stroke_width=0)
                r.move_to((cx+dx,b+h/2,0));g.add(r)
                g.add(txt(str(value),cx+dx,b+h+.20,size=15))
                if j==1:focus.add(r)
            g.add(Line((cx-1.12,b,0),(cx+1.12,b,0),color=MUTED))
        g.add(foot('Cắt trục làm khác biệt trông bị phóng đại'))
        return g,focus,VGroup()
    if step==2:return histogram_visual(4)
    g=VGroup(panel_title('CHECKLIST ĐỌC BIỂU ĐỒ'))
    items=['1. NGUỒN SỐ LIỆU','2. ĐƠN VỊ, CỠ MẪU',
           '3. TRỤC VÀ ĐỘ RỘNG LỚP','4. KẾT LUẬN CÓ GIỚI HẠN']
    focus=VGroup()
    for i,st in enumerate(items):
        y=1.37-i*1.01
        c=pill(st,LEFT,y,w=5.5,chosen=(step==3 and i==1) or (step==4 and i==3))
        g.add(c)
        if (step==3 and i==1) or (step==4 and i==3):focus.add(c[0])
    g.add(foot('Đúng biểu đồ còn cần đúng đơn vị và cách diễn giải'))
    return g,focus,VGroup()

def quiz_visual(step):
    g=VGroup(panel_title('CHỌN HÌNH THỨC BIỂU DIỄN'))
    cases=[('SO SÁNH ĐIỂM SỐ','BIỂU ĐỒ CỘT'),
           ('CƠ CẤU PHẦN TRĂM','BIỂU ĐỒ TRÒN / THANH 100%'),
           ('THAY ĐỔI QUA THÁNG','BIỂU ĐỒ ĐƯỜNG'),
           ('TỔNG KẾT','CỘT · TRÒN · HISTOGRAM · ĐƯỜNG')]
    focus=VGroup()
    for i,(a,b) in enumerate(cases):
        y=1.47-i*.98
        active=i==step-1
        r=RoundedRectangle(width=5.85,height=.79,corner_radius=.1,
            fill_color=ALT if active else PANEL,fill_opacity=1,
            stroke_color=GOLD if active else LINE,stroke_width=2 if active else .8).move_to((LEFT,y,0))
        g.add(r,txt(a,LEFT-1.2,y+.15,size=15,bold=True,limit=3.2),
              txt(b,LEFT+.3,y-.18,size=13,color=GREEN if active else MUTED,limit=5.55))
        if active:focus.add(r)
    g.add(foot('Đặt câu hỏi → chọn dữ liệu → chọn biểu đồ → kiểm tra'))
    return g,focus,VGroup()

def model(beat):
    models={1:table_visual,2:frequency_visual,3:pie_visual,4:percent_visual,
            5:histogram_visual,6:trend_visual,7:caution_visual,8:quiz_visual}
    return models[beat.chapter](beat.step)

class STAT02(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(self.frame())
        planpath=ROOT/'stat02'/'runtime_plan.json'
        if planpath.exists():
            plan=json.loads(planpath.read_text(encoding='utf8'))
            assert plan['scene']=='STAT02' and len(plan['beats'])==len(BEATS)
        else:plan={'beats':[{'duration':b.duration,'voice':''} for b in BEATS]}
        old_visual=None;old_right=None
        for i,beat in enumerate(BEATS):
            entry=plan['beats'][i]
            duration=float(entry['duration'])
            track=entry.get('voice','')
            if track:
                f=ROOT/track
                if not f.is_file():raise FileNotFoundError(f)
                self.add_sound(str(f))
            visual,focus,reveal=model(beat)
            right=self.right_content(beat)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(right),run_time=1.55)
            else:
                self.play(FadeOut(old_visual),FadeOut(old_right),
                          FadeIn(visual),FadeIn(right),run_time=1.55)
            # Real semantic animation: emphasis is attached to bars, pie slices,
            # intervals, lines, and specific cells corresponding to each claim.
            if len(focus):
                self.play(Circumscribe(focus,color=GOLD,time_width=.45,
                                      fade_out=True),run_time=1.30)
            else:self.wait(1.30)
            # Chapter-opening animated emphasis on whole datasets rather than
            # meaningless decorative motion. Avoid blinking large datasets.
            if beat.step==1 and beat.chapter in (2,3,4,5,6) and len(reveal):
                if beat.chapter==6:
                    self.play(*[Indicate(ob,color=GOLD,scale_factor=1.025)
                                for ob in reveal],run_time=1.35)
                else:
                    self.play(Indicate(reveal,color=GOLD,scale_factor=1.01),run_time=1.35)
                spent=4.20
            else:spent=2.85
            if duration<spent:raise ValueError(f'Beat {i+1} duration too short')
            self.wait(duration-spent)
            old_visual,old_right=visual,right

    def frame(self):
        g=VGroup(Rectangle(width=14.222,height=8,fill_color=BG,
                           fill_opacity=1,stroke_width=0))
        for x,width in ((LEFT,6.64),(RIGHT,6.45)):
            g.add(RoundedRectangle(width=width,height=5.93,corner_radius=.15,
                fill_color=PANEL,fill_opacity=1,stroke_color=LINE,stroke_width=1.0).move_to((x,-.02,0)))
        g.add(txt('SANGMATH / THỐNG KÊ 02 / BIỂU ĐỒ NÓI GÌ?',0,3.54,
                  size=25,bold=True,limit=13.3),
              Line((-6.7,3.12,0),(6.7,3.12,0),color=LINE,stroke_width=1.3),
              txt('DỮ LIỆU GIẢ LẬP  •  CHỌN ĐÚNG BIỂU ĐỒ  •  MANIM + TYPST',
                  0,-3.54,size=14,color=MUTED,limit=13))
        return g

    def right_content(self,beat):
        g=VGroup(txt(f'CHƯƠNG {beat.chapter:02d}/08   •   NHỊP {beat.step}/4',
                     RIGHT,2.56,size=16,bold=True,color=CYAN))
        title='\n'.join(textwrap.wrap(beat.title,width=28,break_long_words=False))
        g.add(txt(title,RIGHT,1.68,size=29,bold=True,limit=5.55,height=1.2),
              Line((.67,.77,0),(6.22,.77,0),color=LINE,stroke_width=1.3))
        thesis='\n'.join(textwrap.wrap(beat.thesis,width=34,break_long_words=False))
        g.add(txt(thesis,RIGHT,-.06,size=24,color=GOLD,bold=True,
                  limit=5.6,height=1.35))
        formula={2:'bar',3:'pie',4:'percentage',5:'density',6:'line',7:'reading'}
        code=formula.get(beat.chapter) if beat.step in (2,3) else None
        if code:
            svg=ROOT/'assets'/'stat02_formulas'/f'{code}.svg'
            g.add(txt('CÔNG THỨC / QUY TẮC ĐỌC',RIGHT,-1.06,size=15,
                      color=CYAN,bold=True))
            if svg.is_file():
                obj=SVGMobject(str(svg))
                if obj.width>5.1:obj.scale_to_fit_width(5.1)
                if obj.height>.72:obj.scale_to_fit_height(.72)
                obj.move_to((RIGHT,-1.68,0))
                g.add(obj)
            else:
                fallback={
                    'bar':'Tần số (7) = 10',
                    'pie':'10 / 40 × 360° = 90°',
                    'percentage':'16 / 40 = 40%',
                    'density':'Mật độ = tần số / độ rộng lớp',
                    'line':'Tháng 3: 6,4   →   Tháng 4: 7,2',
                    'reading':'Cần kiểm tra gốc trục và đơn vị',
                }
                g.add(txt(fallback[code],RIGHT,-1.72,size=18,bold=True,limit=5.2))
        else:
            fact={
              1:('CỠ DỮ LIỆU','40 quan sát'),
              2:('TẦN SỐ LỚN NHẤT','10 (điểm 7)'),
              3:('TỔNG CÁC GÓC','360 độ'),
              4:('SO SÁNH','40% và 50%'),
              5:('TỔNG NHÓM GHÉP','40 quan sát'),
              6:('DỮ LIỆU RIÊNG','6 tháng'),
              7:('TIÊU CHÍ','Trung thực'),
              8:('NGUYÊN TẮC','Đúng mục đích'),
            }
            left,right=fact[beat.chapter]
            g.add(txt(left,RIGHT-1.15,-1.31,size=16,color=MUTED,limit=3.1),
                  txt(right,RIGHT+1.46,-1.31,size=17,bold=True,color=GREEN,limit=2.5))
        g.add(txt('CÙNG DỮ LIỆU · KHÁC CÂU HỎI · KHÁC BIỂU ĐỒ',
                  RIGHT,-2.50,size=14,color=MUTED,limit=5.6))
        return g
