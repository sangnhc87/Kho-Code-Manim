"""STAT15: misleading charts, mathematically scaled visual demonstrations.
Full video: python scripts/build_stat15_typst.py; python scripts/prepare_stat15.py --voice off;
            manim -ql -r 854,480 --fps 24 stat15/scene.py STAT15
Smoke:      manim -ql -r 426,240 --fps 8 stat15/scene.py STAT15_SMOKE
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import label,top,foot,XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE
from stat15.lesson import (BEATS,BAR_VALUES,BAR_CROP,YEARS,YEAR_VALUES,
    PICTOGRAM_VALUES,CLASSES,CLASS_COUNTS,CLASS_TOTALS,TREND_YEARS,TREND_VALUES,
    CHALLENGE_VALUES,CHALLENGE_CROP,percentages,histogram_densities,
    exaggerated_height,time_slopes,changes)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
FORM_KEYS=('bar','scale','time','icons','rates','trend','histogram','detective')


def txt(s,x,y,size=16,color=WHITE,width=5.80,bold=False):
    return label(str(s),x,y,size,color,bold,width)


def bar_chart(values,baseline,ybase=-1.68,chart_height=2.35,caption=True):
    """Bar heights use the same linear scale; value labels are truthful."""
    maxdelta=max(values)-baseline
    if maxdelta<=0:raise ValueError('Bars need positive height')
    g=VGroup()
    g.add(Line((-5.73,ybase,0),(-1.0,ybase,0),color=MUTED,stroke_width=2))
    for i,v in enumerate(values):
        h=(v-baseline)/maxdelta*chart_height
        x=-4.63+i*2.47;c=CYAN if i==0 else CORAL
        g.add(Rectangle(width=.98,height=h,stroke_width=1.4,stroke_color=c,
                 fill_color=c,fill_opacity=.65).move_to((x,ybase+h/2,0)))
        g.add(txt(f'{v:g}',x,ybase+h+.20,19,GOLD,.8,True))
        if caption:g.add(txt('A' if i==0 else 'B',x,ybase-.35,16,c,.8,True))
    g.add(txt(f'GỐC TRỤC: {baseline:g}',XL,1.72,15,GREEN,5.75,True))
    return g


def axis_curve(xs,ys,xmin,xmax,ymin,ymax,ybase=-1.65,tick_labels=None):
    width=4.74;left=-5.69;bottom=ybase;height=2.28
    def X(v):return left+(v-xmin)/(xmax-xmin)*width
    def Y(v):return bottom+(v-ymin)/(ymax-ymin)*height
    g=VGroup(Line((left,bottom,0),(left+width,bottom,0),color=MUTED,stroke_width=1.6),
       Line((left,bottom,0),(left,bottom+height,0),color=MUTED,stroke_width=1.6))
    for i,(x,y) in enumerate(zip(xs,ys)):
        if i:g.add(Line((X(xs[i-1]),Y(ys[i-1]),0),(X(x),Y(y),0),color=CYAN,stroke_width=3))
        g.add(Dot((X(x),Y(y),0),radius=.065,color=GOLD))
        g.add(txt(str(tick_labels[i]) if tick_labels else str(x),X(x),bottom-.33,11,MUTED,.77))
    for val in (ymin,ymax):g.add(txt(f'{val:g}',left-.31,Y(val),12,MUTED,.56))
    return g


def diag(s,color=GREEN,y=-2.33):return txt(s,XL,y,14,color,5.94,True)


def vis1(k):
    g=VGroup(top('CÙNG SỐ LIỆU, HAI CÁCH VẼ CỘT'))
    if k==1:
        g.add(txt('CỬA HÀNG A: 80 SẢN PHẨM',XL,1.03,19,CYAN,5.75,True),
              txt('CỬA HÀNG B: 100 SẢN PHẨM',XL,.33,19,CORAL,5.75,True),
              diag('CHÊNH LỆCH: 20 SẢN PHẨM',GOLD,-1.02))
    else:
        g.add(bar_chart(BAR_VALUES,75 if k==2 else 0))
        if k==2:g.add(diag('CỘT CAO GẤP 5 LẦN: ẤN TƯỢNG SAI',CORAL))
        if k>=3:g.add(diag('TỈ SỐ THẬT: 100/80 = 1,25',GREEN))
        if k==4:g.add(txt('SO GỐC TRỤC • NHÃN • ĐƠN VỊ',XL,1.16,14,CYAN,5.9,True))
    g.add(foot('Cột so độ dài nên bắt đầu từ số 0.'))
    return g,None


def vis2(k):
    g=VGroup(top('MỞ RỘNG TRỤC TUNG, ĐỔI CẢM GIÁC'))
    if k==1:
        for j,value in enumerate(YEAR_VALUES):
            g.add(txt(f'{YEARS[j]} : {value}',-5.27,1.53-j*.74,18,CYAN,2.6,True))
    else:
        low,high=(38,58) if k==2 else (0,100)
        g.add(axis_curve(range(4),YEAR_VALUES,0,3,low,high))
        g.add(diag(f'THANG TUNG: {low}–{high}   |   DỮ LIỆU KHÔNG ĐỔI',GOLD))
    if k==4:g.add(txt('ĐƯỜNG KHÔNG BẮT BUỘC GỐC 0',XL,1.47,13,CYAN,5.94,True))
    g.add(foot('Đọc nhãn trục trước khi nhận xét độ dốc.'))
    return g,None


def vis3(k):
    g=VGroup(top('KHOẢNG CÁCH NĂM CŨNG LÀ DỮ LIỆU'))
    if k==1:
        for j,(yr,value) in enumerate(zip(YEARS,YEAR_VALUES)):
            g.add(txt(f'{yr}: {value}',-5.42,1.51-j*.75,17,CYAN,2.1,True))
    else:
        fake=k==2
        xx=tuple(range(4)) if fake else YEARS
        g.add(axis_curve(xx,YEAR_VALUES,xx[0],xx[-1],38,58,tick_labels=YEARS))
        if fake:g.add(diag('SAI LỆCH: KHOẢNG NĂM BỊ VẼ ĐỀU',CORAL))
        else:g.add(diag('1 NĂM  •  3 NĂM  •  1 NĂM',GREEN))
    if k==4:g.add(txt('TỐC ĐỘ: 4 ; 8/3 ; 4 ĐƠN VỊ/NĂM',XL,1.43,13,GOLD,5.9,True))
    g.add(foot('Không có quan sát ≠ giá trị bằng 0.'))
    return g,None


def vis4(k):
    g=VGroup(top('DIỆN TÍCH HÌNH KHÔNG PHẢI BÁN KÍNH'))
    ra=.52;rb=(ra*2 if k==2 else ra*2**.5)
    g.add(Circle(radius=ra,color=CYAN,stroke_width=3,fill_color=CYAN,fill_opacity=.25)
               .move_to((-4.72,-.33,0)))
    if k>=2:g.add(Circle(radius=rb,color=CORAL,stroke_width=3,fill_color=CORAL,fill_opacity=.23)
               .move_to((-2.21,-.33,0)))
    g.add(txt('20 NGƯỜI',-4.72,-1.54,15,CYAN,1.75,True))
    if k>=2:g.add(txt('40 NGƯỜI',-2.21,-1.78,15,CORAL,1.75,True))
    if k==1:g.add(txt('GIÁ TRỊ THẬT: B/A = 2',XL,1.69,17,GOLD,5.8,True))
    if k==2:g.add(diag('BÁN KÍNH ×2  →  DIỆN TÍCH ×4',CORAL))
    if k>=3:g.add(diag('DIỆN TÍCH ×2  →  BÁN KÍNH ×√2',GREEN))
    if k==4:g.add(txt('HÌNH 3D: CẨN THẬN PHỐI CẢNH',XL,1.66,14,CYAN,5.89,True))
    g.add(foot('Biểu tượng phóng đại có thể tạo sai lệch cảm nhận.'))
    return g,None


def vis5(k):
    g=VGroup(top('SỐ ĐẾM KHÁC VỚI TỈ LỆ'))
    pct=percentages()
    if k==1:
        g.add(txt('LỚP A: 18/30 HỌC SINH',XL,1.36,18,CYAN,5.8,True),
              txt('LỚP B: 24/80 HỌC SINH',XL,.49,18,CORAL,5.8,True),
              diag('MẪU SỐ CỦA HAI LỚP KHÁC NHAU',GOLD,-1.36))
    else:
        vals=CLASS_COUNTS if k==2 else pct
        g.add(bar_chart(vals,0))
        if k==2:g.add(diag('24 > 18, NHƯNG B CÓ SĨ SỐ LỚN HƠN',GOLD))
        else:g.add(diag('A = 60%  •  B = 30%',GREEN))
        if k==4:g.add(txt('NÊU CẢ SỐ ĐẾM VÀ CỠ MẪU',XL,1.46,13,CYAN,5.84,True))
    g.add(foot('Tỉ lệ = số đạt / tổng số quan sát.'))
    return g,None


def vis6(k):
    g=VGroup(top('CHỌN MỐC THỜI GIAN CÓ THỂ ĐỔI THÔNG ĐIỆP'))
    if k==1:
        g.add(txt('2022: 60  →  2023: 54',XL,1.04,18,CORAL,5.87,True),
              diag('GIẢM 6 ĐƠN VỊ',GOLD,-.45))
    else:
        g.add(axis_curve(TREND_YEARS,TREND_VALUES,2020,2025,45,70))
        if k==2:g.add(diag('TOÀN BỘ SÁU MỐC NĂM',GOLD))
        if k>=3:g.add(diag('NGẮN HẠN −10%  |  TOÀN KỲ +28%',GREEN))
        if k==4:g.add(txt('KHÔNG SUY CẢ GIAI ĐOẠN TỪ HAI MỐC',XL,1.72,12,CYAN,5.93,True))
    g.add(foot('Hai kết quả đúng có thể thuộc hai thời đoạn khác nhau.'))
    return g,None


def vis7(k):
    g=VGroup(top('HISTOGRAM: LỚP CÓ BỀ RỘNG KHÁC NHAU'))
    dens=histogram_densities()
    lo=-5.61;unit=.47;yb=-1.65
    g.add(Line((lo,yb,0),(-.91,yb,0),color=MUTED,stroke_width=2))
    for i,(left,right,n) in enumerate(CLASSES):
        if k==1:h=n*.105
        elif k==2:h=n*.145
        else:h=dens[i]*.34
        c=(CYAN,GREEN,PURPLE,CORAL)[i]
        x=lo+(left+right)/2*unit
        g.add(Rectangle(width=(right-left)*unit-.012,height=h,
            fill_color=c,fill_opacity=.65,stroke_color=EDGE,stroke_width=1)
            .move_to((x,yb+h/2,0)))
        g.add(txt(str(n if k<3 else round(dens[i],2)),x,yb+h+.16,13,GOLD,.6,True))
        g.add(txt(f'{left}–{right}',x,yb-.30,12,MUTED,.75))
    if k<3:g.add(diag('CỘT THEO TẦN SỐ: SAI KHI ĐỘ RỘNG KHÁC',CORAL))
    else:g.add(diag('MẬT ĐỘ: 4 ; 3 ; 6 ; 3',GREEN))
    if k==4:g.add(txt('DIỆN TÍCH TỔNG: 8+12+6+9 = 35',XL,1.70,14,CYAN,5.90,True))
    g.add(foot('Mật độ × độ rộng lớp = tần số.'))
    return g,None


def vis8(k):
    g=VGroup(top('THỬ THÁCH: PHÁT HIỆN VÀ SỬA BIỂU ĐỒ'))
    if k==1:g.add(bar_chart(CHALLENGE_VALUES,CHALLENGE_CROP),
                  diag('HAI TỈ LỆ KHẢO SÁT: 62% VÀ 68%',GOLD))
    elif k==2:
        g.add(bar_chart(CHALLENGE_VALUES,CHALLENGE_CROP),
              diag('+6 ĐIỂM PHẦN TRĂM  ≠  +6% TƯƠNG ĐỐI',GOLD))
    else:
        g.add(bar_chart(CHALLENGE_VALUES,0))
        g.add(diag('68/62 ≈ 1,097  |  KHÔNG PHẢI 4 LẦN',GREEN))
        if k==4:g.add(txt('TRỤC • ĐƠN VỊ • MẪU SỐ • THỜI GIAN',XL,1.47,13,CYAN,5.83,True))
    g.add(foot('Biểu đồ tốt giúp kiểm tra kết luận từ số liệu.'))
    return g,None

VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)

class STAT15(Scene):
    def frame(self):
        bg=Rectangle(width=14.222,height=8,fill_color=BG,fill_opacity=1,stroke_width=0)
        group=VGroup(bg)
        for x in (XL,XR):
            group.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        group.add(label('SANGMATH / THỐNG KÊ / ĐỌC BIỂU ĐỒ CHÍNH XÁC',0,3.47,20,WHITE,True,13),
            Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
            label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,12))
        return group

    def notes(self,b):
        t='\n'.join(textwrap.wrap(b.title,28,break_long_words=False))
        th='\n'.join(textwrap.wrap(b.thesis,34,break_long_words=False))
        group=VGroup(label(t,XR,2.12,21,WHITE,True,5.72,1.17),
            Line((.70,.82,0),(6.16,.82,0),color=EDGE,stroke_width=1),
            label(th,XR,-.04,18,GOLD,True,5.73,1.52))
        if b.step>=3:
            target=ROOT/'assets/stat15_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not target.is_file():
                raise FileNotFoundError(f'STAT15 SVG missing: {target}; run scripts/build_stat15_typst.py')
            svg=SVGMobject(str(target))
            if svg.width>5.20:svg.scale_to_fit_width(5.20)
            if svg.height>.82:svg.scale_to_fit_height(.82)
            svg.move_to((XR,-1.53,0))
            group.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.95,14,CYAN,True),svg)
        else:group.add(label('ĐỌC SỐ LIỆU  →  KIỂM TRA TRỤC  →  KẾT LUẬN',XR,-1.47,14,GREEN,True,5.71))
        group.add(label('CHỈ KẾT LUẬN TỪ DỮ LIỆU ĐƯỢC CÔNG BỐ',XR,-2.45,12,MUTED,maxw=5.77))
        return group

    def construct(self):
        self.add(self.frame())
        file=ROOT/'stat15/runtime_plan.json'
        if not file.is_file():raise FileNotFoundError('Run scripts/prepare_stat15.py before rendering')
        plan=json.loads(file.read_text(encoding='utf-8'))
        if plan.get('scene')!='STAT15' or len(plan.get('beats',[]))!=32:
            raise ValueError('STAT15 runtime plan incorrect')
        old_visual=old_note=None
        for i,b in enumerate(BEATS):
            row=plan['beats'][i]
            if (row['chapter'],row['step'])!=(b.chapter,b.step):
                raise ValueError(f'STAT15 runtime plan mismatch at {i+1}')
            if row.get('voice'):
                mp3=ROOT/row['voice']
                if not mp3.is_file():raise FileNotFoundError(mp3)
                self.add_sound(str(mp3))
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45);used=1.45
            else:
                self.play(FadeOut(old_visual),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05);used=1.60
            self.wait(.35);used+=.35
            pause=float(row['duration'])-used
            if pause<=0:raise ValueError('Beat duration too short')
            self.wait(pause)
            old_visual,old_note=visual,note

class STAT15_SMOKE(STAT15):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(visual,note);self.wait(.12);self.remove(visual,note)
