"""STAT18. Static panel, coherent charts, one genuine animated estimator marker.
Run: python scripts/build_stat18_typst.py
     python scripts/prepare_stat18.py --voice off
     manim -ql -r 854,480 --fps 24 stat18/scene.py STAT18
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import label,XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE
from stat18.lesson import (BEATS,POPULATION,N,TRUE_P,VOLUNTARY_YES, VOLUNTARY_NO,
                           sample,trials,estimate,percent,sd_sample_proportion,
                           PRACTICE_YES,PRACTICE_N,PRACTICE_CONVENIENCE_YES,
                           approx_interval)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
FORM_KEYS=('population','random','bias','repeats','standard_error','interval','checklist','practice')


def t(s,x=XL,y=0,size=15,color=WHITE,w=5.9,bold=False,maxh=None):
    return label(str(s),x,y,size,color,bold,w,maxh)


def subtitle(s,color=GOLD):
    return t(s,XL,-2.33,14,color,5.85,True)


def step_header(s):
    return t(s,XL,2.12,16,CYAN,5.75,True)


def dots(values,maxcols=10,diameter=.11):
    values=tuple(values)
    n=len(values)
    cols=min(n,maxcols)
    rows=(n+cols-1)//cols
    gap=min(.48,4.66/max(1,cols-1))
    yg=min(.31,3.1/max(1,rows-1))
    result=VGroup()
    for i,v in enumerate(values):
        cx=XL+(i%cols-(cols-1)/2)*gap
        cy=(rows-1)/2*yg-(i//cols)*yg
        result.add(Dot((cx,cy,0),radius=diameter,color=GREEN if v else PURPLE))
    return result


def population_grid():
    # One marker represents ten pupils, preserving the 400:600 split exactly.
    return dots([1]*40+[0]*60,10,.085)


def bars(items, ymax=100, show_values=True, marker=None, top=''):
    """Vertical percent bars, left-column x range -5.9..-1.0; y range -1.64..1.5."""
    left,right=-5.80,-1.05
    bottom,ceiling=-1.48,1.43
    g=VGroup()
    for tick in (0,25,50,75,100) if ymax==100 else (0,5,10,15,20):
        yy=bottom+(ceiling-bottom)*tick/ymax
        g.add(Line((left,yy,0),(right,yy,0),color=EDGE,stroke_width=.64))
        if tick in ((0,50,100) if ymax==100 else (0,10,20)):
            g.add(t(str(tick),left-.27,yy,11,MUTED,.38))
    width=min(1.23,4.28/(2*len(items)))
    for i,(name,value,color) in enumerate(items):
        cx=left+.80+(i+.5)*(right-left-1.05)/len(items)
        height=(ceiling-bottom)*value/ymax
        g.add(Rectangle(width=width,height=max(.005,height),
                        fill_color=color,fill_opacity=.81,stroke_width=0).move_to((cx,bottom+height/2,0)))
        g.add(t(name,cx,bottom-.30,12,WHITE,1.70,True))
        if show_values:g.add(t(percent(value/100,2 if value%1 else 0),cx,
                              min(1.68,bottom+height+.20),14,color,1.4,True))
    if top:g.add(step_header(top))
    return g


def spectrum(values,color=CYAN,offset=0,opacity=.82):
    """Histogram of sample proportions, bars encode frequency, no fake continuous density."""
    edges=[k/20 for k in range(21)]
    counts=[0]*20
    for value in values:
        k=min(19,int(value*20+1e-9))
        counts[k]+=1
    left,right=-5.72,-1.10
    baseline=-1.48
    maxn=max(counts) or 1
    ceiling=1.45
    g=VGroup()
    for j,c in enumerate(counts):
        if c==0:continue
        w=(right-left)/20*.88
        height=(ceiling-baseline)*c/maxn*.85
        xx=left+(j+.5)*(right-left)/20
        g.add(Rectangle(width=w,height=height,stroke_width=0,
                        fill_color=color,fill_opacity=opacity).move_to((xx,baseline+height/2+offset,0)))
    for value in (0,.2,.4,.6,.8,1):
        x=left+(right-left)*value
        g.add(t(f'{int(value*100)}',x,-1.75,10,MUTED,.38))
    true_x=left+(right-left)*TRUE_P
    g.add(Line((true_x,baseline,0),(true_x,ceiling,0),color=GOLD,stroke_width=2.7))
    g.add(t('40%',true_x,1.66,12,GOLD,.65,True))
    return g


def dial(values,color=GREEN,show_numbers=True):
    """Dot-and-number card representing an actual drawn sample, not a population grid."""
    g=VGroup(dots(values,maxcols=10,diameter=.085 if len(values)>40 else .115))
    if show_numbers:
        g.add(subtitle(f'{sum(values)} / {len(values)} CHỌN A = {percent(estimate(values),2 if len(values)==80 else 0)}',color))
    return g


def lesson_population(k):
    g=VGroup()
    if k==1:
        g.add(population_grid(),step_header('1.000 HỌC SINH TRONG QUẦN THỂ'),
              subtitle('MỖI CHẤM TƯỢNG TRƯNG 10 HỌC SINH'))
    elif k==2:
        g.add(population_grid(),step_header('QUẦN THỂ GIẢ LẬP'),
              subtitle('400 CHỌN A  /  600 KHÔNG CHỌN A',GREEN))
    elif k==3:
        g.add(dial(sample(20)),step_header('MẪU NGẪU NHIÊN 20 HỌC SINH'))
    else:
        g.add(bars([('Toàn trường',40,GREEN),('Tự chọn',70,CORAL)]),
              step_header('PHẢI HỎI: AI ĐƯỢC CHỌN?'),subtitle('SỐ PHIẾU NHIỀU CHƯA ĐỦ ĐẠI DIỆN',CORAL))
    return g,None


def lesson_random(k):
    g=VGroup()
    if k==1:
        g.add(population_grid(),step_header('MỌI NHÓM n NGƯỜI CÙNG CƠ HỘI'),
              subtitle('CHỌN NGẪU NHIÊN ĐƠN, KHÔNG HOÀN LẠI'))
    elif k==2:
        g.add(dial(sample(20)),step_header('MẪU NGẪU NHIÊN n = 20'))
    elif k==3:
        g.add(dial(sample(80)),step_header('MẪU NGẪU NHIÊN n = 80'))
    else:
        g.add(bars([('n=20',35,CYAN),('n=80',46.25,GREEN),('Quần thể',40,GOLD)]),
              step_header('MẪU KHÁC NHAU: KẾT QUẢ KHÁC NHAU'),
              subtitle('RÚT THUẬN TIỆN KHÔNG PHẢI RÚT NGẪU NHIÊN',CORAL))
    return g,None


def lesson_bias(k):
    g=VGroup()
    if k==1:
        g.add(bars([('Tự nguyện',70,CORAL)],top='100 PHIẾU PHẢN HỒI'),
              subtitle('70 CHỌN A, 30 CHỌN PHƯƠNG ÁN KHÁC'))
    elif k==2:
        g.add(bars([('Quần thể',40,GREEN),('Tự nguyện',70,CORAL)],
                   top='THIÊN LỆCH DO TỰ CHỌN MẪU'),
              subtitle('CHÊNH LỆCH 30 ĐIỂM PHẦN TRĂM',CORAL))
    elif k==3:
        g.add(bars([('Trả lời',70,CYAN),('Không trả lời',30,PURPLE)],
                   top='VÍ DỤ 100 NGƯỜI ĐƯỢC MỜI'),
              subtitle('PHẢI GHI NHẬN NGƯỜI KHÔNG PHẢN HỒI',CORAL))
    else:
        g.add(bars([('Ngẫu nhiên',35,CYAN),('Tự nguyện',70,CORAL),('Thật',40,GREEN)]),
              step_header('DAO ĐỘNG ≠ THIÊN LỆCH'),
              subtitle('KHÔNG KHỬ THIÊN LỆCH CHỈ BẰNG TĂNG n'))
    return g,None


def lesson_repeats(k):
    g=VGroup()
    if k==1:
        g.add(dial(sample(20)),step_header('RÚT LẶP LẠI TỪ CÙNG QUẦN THỂ'),
              subtitle('MỖI LẦN RÚT: n = 20'))
    elif k==2:
        g.add(spectrum(trials(20)),step_header('300 MẪU NGẪU NHIÊN, n = 20'),
              subtitle('TỈ LỆ MẪU THAY ĐỔI QUA MỖI LẦN'))
    elif k==3:
        g.add(spectrum(trials(80),GREEN),step_header('300 MẪU NGẪU NHIÊN, n = 80'),
              subtitle('KẾT QUẢ THƯỜNG TẬP TRUNG HƠN',GREEN))
    else:
        g.add(spectrum(trials(20),PURPLE),step_header('MỘT MẪU KHÔNG NÓI HẾT DAO ĐỘNG'),
              subtitle('QUAN SÁT CẢ PHÂN BỐ LẤY MẪU'))
    return g,None


def lesson_size(k):
    g=VGroup()
    if k==1:
        g.add(spectrum(trials(20)),step_header('DAO ĐỘNG CỦA TỈ LỆ MẪU'),
              subtitle('CÁC MẪU KHÁC NHAU VẪN CÓ SAI KHÁC'))
    elif k==2:
        g.add(bars([('n=20',100*sd_sample_proportion(20),CYAN),
                    ('n=80',100*sd_sample_proportion(80),GREEN)],ymax=20),
              step_header('ĐỘ LỆCH CHUẨN TỈ LỆ MẪU'),
              subtitle('CÓ HỆ SỐ HIỆU CHỈNH QUẦN THỂ HỮU HẠN'))
    elif k==3:
        g.add(bars([('n=20',100*sd_sample_proportion(20),CYAN),
                    ('n=80',100*sd_sample_proportion(80),GREEN)],ymax=20),
              step_header('TĂNG n LÀM GIẢM DAO ĐỘNG'),
              subtitle('n=20: 10,85%  /  n=80: 5,26%',GREEN))
    else:
        g.add(bars([('Quần thể',40,GREEN),('Tự nguyện',70,CORAL)]),
              step_header('THIÊN LỆCH KHÔNG TỰ BIẾN MẤT'),
              subtitle('THIẾT KẾ MẪU QUAN TRỌNG HƠN',CORAL))
    return g,None


def interval_visual(k):
    p,lo,hi=approx_interval(PRACTICE_YES,PRACTICE_N)
    g=VGroup()
    X=lambda v:-5.9+4.85*v
    y=-.2
    g.add(Line((X(0),y,0),(X(1),y,0),color=MUTED,stroke_width=2.5))
    for v in (0,.2,.4,.6,.8,1.):
        g.add(Dot((X(v),y,0),radius=.038,color=MUTED),t(f'{int(100*v)}%',X(v),y-.34,10,MUTED,.62))
    if k>=2:
        g.add(Line((X(lo),y,0),(X(hi),y,0),color=GREEN,stroke_width=10))
        for v in (lo,hi):g.add(Dot((X(v),y,0),radius=.09,color=GREEN))
        g.add(t(f'{percent(lo,1)}  ...  {percent(hi,1)}',XL,-1.31,17,GREEN,4.9,True))
    g.add(Line((X(TRUE_P),y-.35,0),(X(TRUE_P),y+.48,0),color=GOLD,stroke_width=2),
          Dot((X(p),y,0),radius=.115,color=CYAN),
          t('44%  mẫu',X(p),y+.49,15,CYAN,1.8,True))
    g.add(step_header('ƯỚC LƯỢNG TỪ 88 / 200 HỌC SINH'))
    labels={1:'44% LÀ ƯỚC LƯỢNG, KHÔNG PHẢI THAM SỐ',
            2:'CẦN BÁO MỨC BẤT ĐỊNH',
            3:'XẤP XỈ CHƯA HIỆU CHỈNH HỮU HẠN',
            4:'MỨC TIN CẬY THUỘC VỀ QUY TRÌNH LẶP'}
    g.add(subtitle(labels[k],GREEN if k>=2 else GOLD))
    return g,None


def lesson_quality(k):
    g=VGroup()
    if k==1:
        g.add(bars([('Quần thể',40,GREEN),('Tự nguyện',70,CORAL)]),
              step_header('BIỂU ĐỒ ĐẸP VẪN CÓ THỂ LỆCH'),
              subtitle('KIỂM TRA CÁCH LẤY MẪU',CORAL))
    elif k==2:
        x=lambda p:-5.7+4.55*p
        y=.02
        g.add(Line((x(0),y,0),(x(1),y,0),color=MUTED,stroke_width=3))
        for p in (.0,.2,.4,.6,.8,1.):
            g.add(t(percent(p),x(p),y-.42,12,MUTED,.55))
        g.add(Line((x(.4),y-.5,0),(x(.4),y+.75,0),color=GREEN,stroke_width=2),
              t('MỐC THẬT 40%',x(.4),1.10,14,GREEN,2,True))
        v=ValueTracker(.70)
        g.add(always_redraw(lambda:Dot((x(v.get_value()),y,0),radius=.15,color=CORAL)))
        g.add(step_header('MINH HỌA KHOẢNG CÁCH DO THIÊN LỆCH'),
              subtitle('KHÔNG PHẢI THUẬT TOÁN HIỆU CHỈNH',CORAL))
        return g,v
    elif k==3:
        for i,s in enumerate(['QUẦN THỂ ĐÍCH?', 'CÁCH CHỌN MẪU?',
                               'AI KHÔNG PHẢN HỒI?', 'CÂU HỎI CÓ DẪN DẮT?']):
            yy=1.49-i*.78
            g.add(RoundedRectangle(width=5.22,height=.60,corner_radius=.08,stroke_color=EDGE,
                    fill_color=PANEL,fill_opacity=.88).move_to((XL,yy,0)),
                  t(s,XL,yy,15,(CYAN,GREEN,GOLD,PURPLE)[i],4.9,True))
        g.add(subtitle('ĐỌC PHƯƠNG PHÁP TRƯỚC KHI TIN KẾT QUẢ'))
    else:
        g.add(population_grid(),step_header('MÔ PHỎNG KHÔNG PHẢI DỮ LIỆU THẬT'),
              subtitle('HỌC PHƯƠNG PHÁP, KHÔNG BỊA KẾT LUẬN',CORAL))
    return g,None


def lesson_practice(k):
    g=VGroup()
    if k<=2:
        g.add(step_header('HAI KHẢO SÁT, MỖI NHÓM 200 HỌC SINH'))
        for i,(name,count,color) in enumerate((('NGẪU NHIÊN',88,CYAN),('THUẬN TIỆN',150,CORAL))):
            y=1.14-i*1.25
            g.add(RoundedRectangle(width=5.05,height=.94,corner_radius=.12,
                  stroke_color=color,stroke_width=1.4,fill_color=PANEL,fill_opacity=1).move_to((XL,y,0)),
                  t(name,XL-1.2,y,15,color,2.43,True),
                  t(f'{count}/200' if k==1 else f'{count} ÷ 200 = ?',XL+1.05,y,17,WHITE,2.0,True))
        g.add(subtitle('TÍNH VÀ SO SÁNH TRƯỚC KHI XEM ĐÁP ÁN'))
    elif k==3:
        g.add(bars([('Ngẫu nhiên',PRACTICE_YES/PRACTICE_N*100,CYAN),
                    ('Thuận tiện',PRACTICE_CONVENIENCE_YES/PRACTICE_N*100,CORAL),
                    ('Quần thể',TRUE_P*100,GREEN)]),
              step_header('CÙNG n, KHÔNG CÙNG CHẤT LƯỢNG'),
              subtitle('44% SO VỚI 75%  —  CẦN XÉT CÁCH CHỌN',GREEN))
    else:
        items=['DỮ LIỆU ĐÚNG','BIỂU DIỄN RÕ','TÍNH TOÁN CHUẨN','SUY LUẬN CÓ ĐIỀU KIỆN']
        for i,s in enumerate(items):
            x=XL
            yy=1.53-i*.83
            g.add(t(s,x,yy,17,(CYAN,GREEN,GOLD,PURPLE)[i],4.85,True))
            if i<3:g.add(Line((x,yy-.26,0),(x,yy-.56,0),color=EDGE,stroke_width=2))
        g.add(subtitle('HỎI: DỮ LIỆU ĐẾN TỪ ĐÂU?',GREEN))
    return g,None

VISUALS=(lesson_population,lesson_random,lesson_bias,lesson_repeats,
         lesson_size,interval_visual,lesson_quality,lesson_practice)


class STAT18(Scene):
    def frame(self):
        bg=Rectangle(width=14.222,height=8,fill_color=BG,fill_opacity=1,stroke_width=0)
        g=VGroup(bg)
        for x in (XL,XR):
            g.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                  stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        g.add(label('SANGMATH  /  THỐNG KÊ  /  LẤY MẪU VÀ MÔ PHỎNG',0,3.47,18,WHITE,True,13),
              Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
              label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,12))
        return g

    def notes(self,b):
        title='\n'.join(textwrap.wrap(b.title,28,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,37,break_long_words=False))
        g=VGroup(label(title,XR,2.07,20,WHITE,True,5.70,1.15),
            Line((.70,.78,0),(6.16,.78,0),color=EDGE,stroke_width=1),
            label(thesis,XR,-.04,16,GOLD,True,5.70,1.70))
        if b.step>=3:
            path=ROOT/'assets/stat18_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not path.is_file():raise FileNotFoundError(f'STAT18 SVG missing {path}; build Typst first')
            svg=SVGMobject(str(path))
            if svg.width>4.8:svg.scale_to_fit_width(4.8)
            if svg.height>.88:svg.scale_to_fit_height(.88)
            svg.move_to((XR,-1.52,0))
            g.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.98,14,CYAN,True,5.8),svg)
        else:
            g.add(label('ĐỌC SỐ LIỆU  →  SUY LUẬN',XR,-1.53,14,GREEN,True,5.8))
        g.add(label('SỐ LIỆU MINH HỌA GIẢ LẬP · KHÔNG SUY RỘNG TÙY TIỆN',
                    XR,-2.54,11,MUTED,maxw=5.81))
        return g

    def construct(self):
        self.add(self.frame())
        plan_path=ROOT/'stat18/runtime_plan.json'
        if not plan_path.is_file():raise FileNotFoundError('Run scripts/prepare_stat18.py first')
        plan=json.loads(plan_path.read_text(encoding='utf8'))
        if plan.get('scene')!='STAT18' or len(plan.get('beats',[]))!=32:
            raise ValueError('STAT18 runtime plan invalid')
        old_vis=old_note=None
        for i,b in enumerate(BEATS):
            entry=plan['beats'][i]
            if (entry['chapter'],entry['step'])!=(b.chapter,b.step):raise ValueError('Plan mismatch')
            if entry.get('voice'):
                voice_file=ROOT/entry['voice']
                if not voice_file.is_file():raise FileNotFoundError(voice_file)
                self.add_sound(str(voice_file))
            visual,tracker=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_vis is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45);used=1.45
            else:
                self.play(FadeOut(old_vis),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05);used=1.60
            if tracker is not None:
                self.play(tracker.animate.set_value(.4),run_time=3.)
                used+=3.
            self.wait(.35);used+=.35
            pause=float(entry['duration'])-used
            if pause<=0:raise ValueError('Duration too short')
            self.wait(pause)
            old_vis,old_note=visual,note

class STAT18_SMOKE(STAT18):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(visual,note)
            self.wait(.12)
            self.remove(visual,note)
