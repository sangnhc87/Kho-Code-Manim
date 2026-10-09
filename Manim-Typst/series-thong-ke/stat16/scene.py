"""STAT16 – Simpson's paradox (synthetic classroom example).

Full render:
    python scripts/build_stat16_typst.py
    python scripts/prepare_stat16.py --voice off
    manim -ql -r 854,480 --fps 24 stat16/scene.py STAT16
Smoke check:
    manim -ql -r 426,240 --fps 8 stat16/scene.py STAT16_SMOKE
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat07.scene import label,top,foot,XL,XR,BG,PANEL,EDGE,WHITE,MUTED,CYAN,GOLD,GREEN,CORAL,PURPLE
from stat16.lesson import (MAIN,CHALLENGE,METHODS,GROUPS,BEATS,rate,aggregate,
                           weight_easy,mix,pooled_easy_weight,as_pct)
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8
FORM_KEYS=('question','strata','aggregate','weight','standard','meaning','pitfalls','practice')


def tx(s,x,y,size=17,color=WHITE,width=5.70,bold=False):
    return label(str(s),x,y,size,color,bold,width)


def note_line(s,color=GOLD,y=-2.12):
    return tx(s,XL,y,14,color,5.86,True)


def rate_bars(table,group='easy',caption=True,y0=.95):
    """Same origin / same linear 0–100% axis for fair comparison."""
    g=VGroup()
    x0=-5.58; maxw=4.24
    g.add(Line((x0-.08,y0-1.10,0),(x0+maxw+.15,y0-1.10,0),color=MUTED,stroke_width=1.5))
    for j,method in enumerate(METHODS):
        successes,total=table[method][group]
        pct=rate((successes,total))
        yy=y0-j*1.14
        g.add(tx(f'{method}  {successes}/{total}',x0+.72,yy+.25,14,CYAN if j==0 else CORAL,1.65,True))
        rect=Rectangle(width=maxw*pct,height=.31,fill_color=CYAN if j==0 else CORAL,
                      fill_opacity=.73,stroke_width=.7,stroke_color=EDGE)
        rect.move_to((x0+(maxw*pct)/2,yy-.27,0))
        g.add(rect,tx(as_pct(pct),x0+maxw+.40,yy-.26,16,GOLD,.82,True))
    if caption:g.add(tx('CHUNG TRỤC 0–100%',XL,-1.55,14,GREEN,5.8,True))
    return g


def four_cells(table,mode='fraction'):
    g=VGroup(); xs=(-4.69,-2.30);ys=(.77,-.72)
    for i,group in enumerate(GROUPS):
        g.add(tx('BÀI DỄ' if i==0 else 'BÀI KHÓ',XL,ys[i]+.47,14,MUTED,5.8,True))
        for j,method in enumerate(METHODS):
            hits,total=table[method][group]
            value=(f'{hits}/{total}' if mode=='fraction' else as_pct(rate((hits,total))))
            c=CYAN if j==0 else CORAL
            g.add(RoundedRectangle(width=2.10,height=.71,corner_radius=.10,
                                   stroke_width=1.3,stroke_color=c,fill_color=c,fill_opacity=.12)
                  .move_to((xs[j],ys[i],0)),tx(f'{method}: {value}',xs[j],ys[i],16,c,1.9,True))
    return g


def totals_bars(table=MAIN,show_a=True,show_b=True):
    g=VGroup();x0=-5.53;maxw=4.23
    for j,method in enumerate(METHODS):
        if (j==0 and not show_a) or (j==1 and not show_b):continue
        hits,total=aggregate(table,method)
        pct=rate((hits,total)); y=1.06-j*1.33
        c=CYAN if j==0 else CORAL
        g.add(tx(f'{method}: {hits}/{total}',x0+1.0,y+.20,17,c,2.3,True))
        g.add(Rectangle(width=pct*maxw,height=.43,fill_color=c,fill_opacity=.74,
                        stroke_color=EDGE,stroke_width=1).move_to((x0+pct*maxw/2,y-.45,0)))
        g.add(tx(as_pct(pct),x0+maxw+.43,y-.46,18,GOLD,.91,True))
    g.add(tx('CÙNG MỐC 0% VÀ 100%',XL,-1.77,13,MUTED,5.70))
    return g


def composition(table=MAIN):
    g=VGroup();x0=-5.57;ww=4.75
    for j,method in enumerate(METHODS):
        weight=weight_easy(table,method);y=.76-j*1.48
        w1=max(.001,ww*weight);w2=max(.001,ww*(1-weight))
        g.add(tx(f'{method}',x0-.25,y+.22,17,WHITE,.35,True))
        g.add(Rectangle(width=w1,height=.63,fill_color=GREEN,fill_opacity=.72,
                        stroke_color=EDGE,stroke_width=.8).move_to((x0+w1/2,y-.33,0)))
        g.add(Rectangle(width=w2,height=.63,fill_color=PURPLE,fill_opacity=.72,
                        stroke_color=EDGE,stroke_width=.8).move_to((x0+w1+w2/2,y-.33,0)))
        g.add(tx(f'{as_pct(weight,0)} DỄ | {as_pct(1-weight,0)} KHÓ',XL,y-.85,12,MUTED,5.87))
    g.add(tx('XANH: DỄ     TÍM: KHÓ',XL,1.66,12,GOLD,5.85,True))
    return g


def weighted_formula(table=MAIN):
    a=weight_easy(table,'A');b=weight_easy(table,'B')
    g=VGroup(tx('A: 0,2 × 90% + 0,8 × 35%',XL,.82,17,CYAN,5.8,True),
             tx('= 46%',XL,.32,23,GOLD,5.8,True),
             tx('B: 0,9 × 80% + 0,1 × 30%',XL,-.53,17,CORAL,5.8,True),
             tx('= 75%',XL,-1.05,23,GOLD,5.8,True))
    # Guards ensure labels never become stale if data changes.
    if not (abs(a-.2)<1e-12 and abs(b-.9)<1e-12):
        raise ValueError('Weighted-visual scenario differs from lesson data')
    return g


def standardized_bars(weight=.5):
    g=VGroup();x0=-5.52;ww=4.22
    for j,method in enumerate(METHODS):
        r=mix(MAIN,method,weight);y=.78-j*1.37
        c=CYAN if j==0 else CORAL
        g.add(tx(f'{method}',x0+.15,y+.14,17,c,.5,True))
        g.add(Rectangle(width=r*ww,height=.43,fill_color=c,fill_opacity=.76,
                        stroke_color=EDGE,stroke_width=1).move_to((x0+r*ww/2,y-.41,0)))
        g.add(tx(as_pct(r,2),x0+ww+.40,y-.40,18,GOLD,.87,True))
    g.add(tx(f'TRỌNG SỐ DỄ CHUNG: {as_pct(weight,0)}',XL,-1.65,14,GREEN,5.9,True))
    return g


def vis1(k):
    g=VGroup(top('CÙNG MỘT BẢNG, HAI KẾT LUẬN'))
    if k==1:
        g.add(tx('PHƯƠNG ÁN A HAY B?',XL,1.25,21,GOLD,5.9,True),
              tx('Mỗi lượt thuộc nhóm bài dễ hoặc bài khó.',XL,.23,16,WHITE,5.7),
              note_line('SỐ LIỆU GIẢ LẬP DÙNG ĐỂ HỌC',y=-1.28))
    elif k in (2,3):
        g.add(rate_bars(MAIN,'easy' if k==2 else 'hard'))
        g.add(note_line('A DẪN TRƯỚC TRONG NHÓM NÀY'))
    else:
        g.add(four_cells(MAIN,mode='pct'))
        g.add(note_line('KẾT QUẢ GỘP CÓ CÒN GIỐNG?',color=GOLD))
    g.add(foot('So sánh đúng cần giữ cả tử số và mẫu số.'))
    return g,None


def vis2(k):
    g=VGroup(top('SO SÁNH RIÊNG TỪNG ĐỘ KHÓ'))
    g.add(four_cells(MAIN,'fraction' if k==1 else 'pct'))
    if k==2:g.add(note_line('DỄ: A HƠN B 10 ĐIỂM PHẦN TRĂM'))
    if k==3:g.add(note_line('KHÓ: A HƠN B 5 ĐIỂM PHẦN TRĂM'))
    if k==4:g.add(note_line('A > B TRONG CẢ HAI NHÓM',GREEN))
    g.add(foot('Các ô của bảng có cỡ mẫu không bằng nhau.'))
    return g,None


def vis3(k):
    g=VGroup(top('GỘP LẠI VÀ QUAN SÁT ĐẢO CHIỀU'))
    if k==1:
        g.add(totals_bars(MAIN,True,False))
        g.add(note_line('A: 18 + 28 = 46 TRÊN 100 LƯỢT'))
    elif k==2:
        g.add(totals_bars(MAIN,False,True))
        g.add(note_line('B: 72 + 3 = 75 TRÊN 100 LƯỢT'))
    else:
        g.add(totals_bars(MAIN))
        g.add(note_line('A 46% < B 75%: ĐẢO CHIỀU',CORAL))
    g.add(foot('Cộng số lượt trước, rồi mới chia lấy tỉ lệ.'))
    return g,None


def vis4(k):
    g=VGroup(top('TRỌNG SỐ GIẢI THÍCH NGHỊCH LÝ'))
    if k in (1,2):
        g.add(composition(MAIN))
        g.add(note_line('A NHIỀU BÀI KHÓ  •  B NHIỀU BÀI DỄ',GOLD))
    else:
        g.add(weighted_formula(MAIN))
        g.add(note_line('TRỌNG SỐ KHÁC NHAU → KẾT QUẢ KHÁC',GREEN))
    g.add(foot('Tỉ lệ gộp là một trung bình có trọng số.'))
    return g,None


def vis5(k):
    g=VGroup(top('SO SÁNH DƯỚI CÙNG MỘT CƠ CẤU'))
    if k==1:
        g.add(tx('DỄ: 50%     KHÓ: 50%',XL,1.07,19,GOLD,5.8,True),
              note_line('CHỈ ĐỔI TRỌNG SỐ ĐỂ SO SÁNH',y=-1.06))
    else:
        w=pooled_easy_weight(MAIN) if k==4 else .5
        g.add(standardized_bars(w))
        if k==2:g.add(note_line('A CHUẨN HÓA: 62,5%',CYAN))
        elif k==3:g.add(note_line('A 62,5% > B 55%',GREEN))
        else:g.add(note_line('VỚI CƠ CẤU CHUNG: A VẪN HƠN',GREEN))
    g.add(foot('Tỉ lệ chuẩn hóa không phải tỉ lệ đã quan sát.'))
    return g,None


def vis6(k):
    g=VGroup(top('DIỄN GIẢI CÓ CĂN CỨ'))
    if k==1:
        g.add(tx('TỪNG NHÓM: A CAO HƠN',XL,1.03,18,CYAN,5.8,True),
              tx('GỘP THỰC TẾ: B CAO HƠN',XL,.18,18,CORAL,5.8,True))
    elif k==2:
        g.add(composition(MAIN))
    elif k==3:
        g.add(tx('CÙNG NHÓM CHƯA ĐỦ CHỨNG MINH',XL,1.15,17,GOLD,5.9,True),
              tx('HIỆU QUẢ DO PHƯƠNG PHÁP GÂY RA.',XL,.38,17,WHITE,5.8,True),
              note_line('CẦN KIỂM SOÁT CÁCH CHỌN MẪU',CORAL))
    else:
        g.add(tx('TỬ SỐ   |   MẪU SỐ',XL,1.27,19,CYAN,5.8,True),
              tx('CƠ CẤU   |   GIẢ ĐỊNH',XL,.42,19,GOLD,5.8,True),
              note_line('KẾT LUẬN ĐÚNG PHẠM VI DỮ LIỆU',GREEN))
    g.add(foot('Số liệu mô tả không tự chứng minh nhân quả.'))
    return g,None


def vis7(k):
    g=VGroup(top('PHÁT HIỆN BA BẪY KHI GỘP SỐ LIỆU'))
    if k==1:
        g.add(tx('(90% + 35%)/2 = 62,5%',XL,1.03,20,CORAL,5.9,True),
              tx('KHÔNG PHẢI TỈ LỆ GỘP CỦA A',XL,.31,16,GOLD,5.9,True),
              note_line('VÌ 20 LƯỢT KHÁC 80 LƯỢT'))
    elif k==2:
        g.add(four_cells(MAIN,'pct'))
        g.add(note_line('CHỈ BIẾT % THÌ CHƯA ĐỦ GỘP'))
    elif k==3:
        g.add(tx('TƯƠNG QUAN  ≠  NHÂN QUẢ',XL,.92,21,GOLD,5.8,True),
              note_line('PHẢI XEM CÁCH CHỌN MẪU',CORAL,-.68))
    else:
        g.add(tx('PHÂN NHÓM  •  MẪU SỐ',XL,1.13,18,CYAN,5.8,True),
              tx('TRỌNG SỐ  •  KẾT LUẬN',XL,.35,18,GOLD,5.8,True),
              note_line('KIỂM TRA TRƯỚC KHI TIN CON SỐ'))
    g.add(foot('Tránh suy diễn từ tỉ lệ không có mẫu số.'))
    return g,None


def vis8(k):
    g=VGroup(top('BÀI TẬP: PHÁT HIỆN ĐẢO CHIỀU'))
    if k==1:g.add(four_cells(CHALLENGE,'fraction'),note_line('EM HÃY TÍNH VÀ DỰ ĐOÁN',GOLD))
    elif k==2:g.add(four_cells(CHALLENGE,'pct'),note_line('A HƠN B Ở CẢ HAI NHÓM',GREEN))
    else:
        g.add(totals_bars(CHALLENGE))
        g.add(note_line('A 34% < B 62,5%: ĐẢO CHIỀU',CORAL))
    g.add(foot('Kiểm tra cơ cấu mẫu trước khi khẳng định.'))
    return g,None


VISUALS=(vis1,vis2,vis3,vis4,vis5,vis6,vis7,vis8)


class STAT16(Scene):
    def frame(self):
        bg=Rectangle(width=14.222,height=8,fill_color=BG,fill_opacity=1,stroke_width=0)
        g=VGroup(bg)
        for x in (XL,XR):
            g.add(RoundedRectangle(width=6.54,height=5.92,corner_radius=.14,
                stroke_color=EDGE,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to((x,-.01,0)))
        g.add(label('SANGMATH / THỐNG KÊ / NGHỊCH LÝ SIMPSON',0,3.47,20,WHITE,True,13),
            Line((-6.7,3.08,0),(6.7,3.08,0),color=EDGE,stroke_width=1),
            label('Thầy Nguyễn Văn Sang',0,-3.58,15,MUTED,True,12))
        return g

    def notes(self,b):
        title='\n'.join(textwrap.wrap(b.title,27,break_long_words=False))
        thesis='\n'.join(textwrap.wrap(b.thesis,33,break_long_words=False))
        g=VGroup(label(title,XR,2.10,20,WHITE,True,5.75,1.18),
            Line((.70,.78,0),(6.16,.78,0),color=EDGE,stroke_width=1),
            label(thesis,XR,-.07,17,GOLD,True,5.75,1.55))
        if b.step>=3:
            path=ROOT/'assets/stat16_formulas'/f'{FORM_KEYS[b.chapter-1]}.svg'
            if not path.is_file():
                raise FileNotFoundError(f'STAT16 formula SVG missing: {path}; run scripts/build_stat16_typst.py')
            svg=SVGMobject(str(path))
            if svg.width>5.0:svg.scale_to_fit_width(5.0)
            if svg.height>.84:svg.scale_to_fit_height(.84)
            svg.move_to((XR,-1.53,0))
            g.add(label('CÔNG THỨC / KIỂM CHỨNG',XR,-.96,14,CYAN,True),svg)
        else:
            g.add(label('ĐỌC DỮ KIỆN → PHÂN NHÓM → KIỂM CHỨNG',XR,-1.43,13,GREEN,True,5.8))
        g.add(label('DỮ LIỆU MINH HỌA • KHÔNG SUY DIỄN NHÂN QUẢ',XR,-2.45,12,MUTED,maxw=5.8))
        return g

    def construct(self):
        self.add(self.frame())
        path=ROOT/'stat16/runtime_plan.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_stat16.py first')
        plan=json.loads(path.read_text(encoding='utf8'))
        if plan.get('scene')!='STAT16' or len(plan.get('beats',[]))!=32:
            raise ValueError('STAT16 runtime plan incorrect')
        old_visual=old_note=None
        for i,b in enumerate(BEATS):
            row=plan['beats'][i]
            if (row['chapter'],row['step'])!=(b.chapter,b.step):
                raise ValueError(f'STAT16 plan mismatch at {i}')
            if row.get('voice'):
                audio=ROOT/row['voice']
                if not audio.is_file():raise FileNotFoundError(audio)
                self.add_sound(str(audio))
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            if old_visual is None:
                self.play(FadeIn(visual),FadeIn(note),run_time=1.45); used=1.45
            else:
                self.play(FadeOut(old_visual),FadeOut(old_note),run_time=.55)
                self.play(FadeIn(visual),FadeIn(note),run_time=1.05); used=1.60
            self.wait(.35); used+=.35
            pause=float(row['duration'])-used
            if pause<=0:raise ValueError('Invalid beat duration')
            self.wait(pause)
            old_visual,old_note=visual,note


class STAT16_SMOKE(STAT16):
    def construct(self):
        self.add(self.frame())
        for b in BEATS:
            visual,_=VISUALS[b.chapter-1](b.step)
            note=self.notes(b)
            self.add(visual,note)
            self.wait(.12)
            self.remove(visual,note)
