"""COMB15: Complementary counting, eight chapters and 48 timed teaching beats.

Prepare first: python scripts/prepare_comb15_v2.py --voice off
Render: manim -ql -r 854,480 --fps 24 episodes/comb15_number_formation.py COMB15
"""
from __future__ import annotations
import sys,json,math,itertools
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb15_lesson_data import BEATS, CHAPTER_LABELS
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8.0
FONT='Noto Sans'
LX=-3.68
RX=3.15

def txt(s,x,y,size=17,color=None,bold=False,width=None):
    v=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if width and v.width>width:v.scale_to_fit_width(width)
    v.move_to([x,y,0]);return v

def token(label,x,y,stroke=None,w=.57,h=.58):
    r=RoundedRectangle(width=w,height=h,corner_radius=.11,stroke_color=stroke or C['cyan'],stroke_width=2,
                       fill_color=C['panel_alt'],fill_opacity=1).move_to((x,y,0))
    t=txt(label,x,y,18,C['text'],True,w-.065)
    return VGroup(r,t)

def tile_row(group,labels,y=.52,colors=None,spacing=.79):
    xs=[LX+(j-(len(labels)-1)/2)*spacing for j in range(len(labels))]
    tiles=[]
    for j,(ch,x) in enumerate(zip(labels,xs)):
        t=token(ch,x,y,colors[j] if colors else C['cyan'])
        tiles.append(t);group.add(t)
    return tiles

def mark(group,obj,label=None,color=None):
    box=SurroundingRectangle(obj,buff=.105,color=color or C['gold'],stroke_width=2.6,corner_radius=.11)
    group.add(box)
    if label:
        group.add(txt(label,box.get_center()[0],box.get_bottom()[1]-.35,14,color or C['gold'],True,4.45))
    return box

def banner(group,title,detail):
    group.add(txt(title,LX,2.57,16,C['cyan'],True,5.8))
    group.add(txt(detail,LX,-2.82,13,C['muted'],True,5.7))

def miniature_universe(group,state):
    # 9x9 grid contains all 81 four-letter strings over {A,B,C}; exactly 16 omit A.
    codes=list(itertools.product('ABC',repeat=4))
    dots=VGroup()
    for i,code in enumerate(codes):
        invalid=('A' not in code)
        col=C['inactive'] if state==0 else C['red'] if invalid else C['green']
        circle=Dot([LX+(i%9-4)*.31, .28+(4-i//9)*.30,0],radius=.095,color=col)
        dots.add(circle)
    group.add(dots)
    group.add(txt('81 DÃY',LX,-1.76,15,C['gold'],True))
    if state>=2:group.add(txt('16 KHÔNG A',LX,-2.13,14,C['red'],True))
    if state>=3:group.add(txt('65 CÓ A',LX,-2.36,18,C['green'],True))
    return dots

# A digit-slot layout, built from actual selectable digits and real place-value slots.
# Digits are intentionally redrawn at each teaching beat; no decorative motion.
DIGITS={
 'leading':'012345','parity':'01234','divfive':'0123456','divthree':'012345',
 'range':'012345','repeat':'012345','divfour':'012345','capstone':'012345'
}
SAMPLES={
 'leading':['···','1··','10·','102','102','101'],
 'parity':['···','12·','142','120','123','142'],
 'divfive':['····','1230','1235','1230','1235','1230'],
 'divthree':['···','···','123','102','315','123'],
 'range':['···','3··','302','402','502','302'],
 'repeat':['····','1123','1234','1123','0123','1123'],
 'divfour':['····','·104','1204','4312','1024','1234'],
 'capstone':['····','3··0','3120','3015','4125','5130']
}
VALUES={
 'leading':['6 CHỮ SỐ','5 LỰA CHỌN','5 LỰA CHỌN','4 LỰA CHỌN','100 SỐ','180 KHI LẶP'],
 'parity':['3 SỐ CHẴN CUỐI','12 SỐ','18 SỐ','30 SỐ CHẴN','18 SỐ LẺ','PHẢI CHIA NHÁNH'],
 'divfive':['CUỐI 0 HOẶC 5','120 SỐ','100 SỐ','220 SỐ','720 TỔNG SỐ','CHỌN CUỐI TRƯỚC'],
 'divthree':['TỔNG / 3','BA NHÓM DƯ','8 BỘ BA','16 SỐ','24 SỐ','40 SỐ'],
 'range':['ĐẦU 3, 4, 5','12 SỐ','8 SỐ','12 SỐ','32 SỐ','CỘNG 3 NHÁNH'],
 'repeat':['TỒN TẠI CHỮ SỐ LẶP','1080 TỔNG SỐ','300 KHÔNG LẶP','780 CÓ LẶP','MÃ PIN ≠ SỐ','LẤY PHẦN BÙ'],
 'divfour':['XÉT HAI Ô CUỐI','7 CẶP CUỐI','36 SỐ','36 SỐ','72 SỐ','CHẴN CHƯA ĐỦ'],
 'capstone':['CHIA HẾT CHO 15','ĐẦU 3/4/5, CUỐI 0/5','8 SỐ','4 SỐ','12 SỐ','24 SỐ']
}
def slot(group,digit,x,y,w=.93):
    box=RoundedRectangle(width=w,height=.82,corner_radius=.12,stroke_width=2,
        stroke_color=C['inactive'],fill_color=C['panel_alt'],fill_opacity=1).move_to((x,y,0))
    group.add(box)
    group.add(txt(digit,x,y,27,C['text'] if digit!='·' else C['inactive'],True,w-.16))
    return box

def make_group(section,state):
    art=VGroup()
    focus=None
    banner(art,'BỘ CHỮ SỐ  /  CÁC Ô VỊ TRÍ','QUAN SÁT ĐIỀU KIỆN, RỒI ĐẾM TỪNG NHÁNH')
    digits=DIGITS[section]
    k=3 if section in ('leading','parity','divthree','range') else 4
    xbase=LX-(len(digits)-1)*.42
    src=[]
    for j,ch in enumerate(digits):
        center=xbase+j*.84
        src.append(token(ch,center,1.65,C['cyan'],w=.62,h=.67))
        art.add(src[-1])
    art.add(txt('THẺ ĐƯỢC PHÉP SỬ DỤNG',LX,2.31,14,C['cyan'],True,5.7))
    sample=SAMPLES[section][state]
    if len(sample)!=k:sample=sample[:k].ljust(k,'·')
    xs=[LX+(j-(k-1)/2)*1.18 for j in range(k)]
    slots=[]
    names=(['TRĂM','CHỤC','ĐƠN VỊ'] if k==3 else ['NGHÌN','TRĂM','CHỤC','ĐƠN VỊ'])
    for j,x in enumerate(xs):
        slots.append(slot(art,sample[j],x,.18))
        art.add(txt(names[j],x,-.43,12,C['muted'],True,1.10))
    if section in ('leading','repeat','range'):
        inds=[0]
    elif section in ('parity','divfive'):
        inds=[k-1]
    elif section=='divfour':
        inds=[k-2,k-1]
    elif section=='divthree':
        inds=list(range(k))
    else:
        inds=[0,k-1]
    selected=VGroup(*[slots[j] for j in inds])
    focus=SurroundingRectangle(selected,buff=.13,color=C['gold'],stroke_width=3,corner_radius=.12)
    art.add(focus)
    msg=VALUES[section][state]
    art.add(txt(msg,LX,-1.17,22,C['green'] if state in (3,4,5) else C['gold'],True,5.64))
    if section=='leading':
        note=['KHÔNG CẤM 0 Ở TẤT CẢ Ô','KHÔNG CHỌN 0 LÀM ĐẦU','SỐ 0 ĐƯỢC Ở GIỮA','KHÔNG DÙNG LẠI THẺ','5 × 5 × 4','CHO LẶP: 5 × 6 × 6'][state]
    elif section=='parity':
        note=['CHỌN ĐƠN VỊ TRƯỚC','CUỐI 0 → 4 × 3','CUỐI 2,4 → 2 × 3 × 3','12 + 18 = 30','48 − 30 = 18','CÁC NHÁNH KHÔNG ĐỒNG ĐỀU'][state]
    elif section=='divfive':
        note=['ĐƠN VỊ 0 HOẶC 5','6 × 5 × 4','5 × 5 × 4','120 + 100','TẤT CẢ: 6 × 6 × 5 × 4','ĐẾM Ô CHỊU ĐIỀU KIỆN'][state]
    elif section=='divthree':
        note=['XÉT TỔNG 3 CHỮ SỐ','DƯ 0 / DƯ 1 / DƯ 2','2 × 2 × 2 = 8 BỘ','CHỨA 0: 4 × 4','KHÔNG 0: 4 × 6','16 + 24 = 40'][state]
    elif section=='range':
        note=['HÀNG TRĂM 3,4,5','3 × 4','2 × 4','3 × 4','12 + 8 + 12','ĐẦU VÀ CUỐI RÀNG BUỘC NHAU'][state]
    elif section=='repeat':
        note=['LẬP SỐ THEO ĐIỀU KIỆN','5 × 6³','5 × 5 × 4 × 3','1080 − 300','PIN CÓ THỂ BẮT ĐẦU 0','CHÚ Ý SỐ 0 Ở ĐẦU'][state]
    elif section=='divfour':
        note=['2 CHỮ SỐ CUỐI CHIA HẾT 4','04 / 12 / 20 / 24 / 32 / 40 / 52','3 CẶP × 12','4 CẶP × 9','36 + 36 = 72','SỐ CHẴN CHƯA CHẮC /4'][state]
    else:
        note=['ĐỒNG THỜI CHIA HẾT 3 VÀ 5','BỘ CHỮ SỐ ĐÔI MỘT KHÁC','ĐẦU 3, CUỐI 0','ĐẦU 3, CUỐI 5','ĐẦU 4 HOẶC 5','12 + 8 + 4 = 24'][state]
    art.add(txt(note,LX,-1.82,17,C['purple'],True,5.72))
    # Visual count sticks: grouping explains additive branches without tiny unreadable labels.
    if section in ('parity','divfive','range','divfour','capstone') and state>=2:
        if section=='parity':counts=[12,18]
        elif section=='divfive':counts=[120,100]
        elif section=='range':counts=[12,8,12]
        elif section=='divfour':counts=[36,36]
        else:counts=[12,8,4]
        total=sum(counts)
        xp=LX-2.35
        for j,n in enumerate(counts):
            ww=4.7*n/total
            rect=Rectangle(width=ww,height=.27,fill_color=[C['cyan'],C['gold'],C['purple']][j],
                fill_opacity=.90,stroke_width=0).move_to((xp+ww/2,-2.37,0))
            art.add(rect);xp+=ww
    if section=='divthree' and state>=1:
        art.add(txt('0,3       1,4       2,5',LX,-2.38,18,C['cyan'],True,5.7))
    if section=='divfour' and state in (1,2,3):
        art.add(txt('04 · 12 · 20 · 24 · 32 · 40 · 52',LX,-2.39,15,C['cyan'],True,5.72))
    return art,focus

def formula_image(key):
    p=ROOT/'assets'/'comb15v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Prepare Typst formulas first: {p}')
    im=ImageMobject(str(p))
    im.scale_to_fit_width(min(im.width,5.80))
    if im.height>.86:im.scale_to_fit_height(.86)
    im.move_to((RX,-1.11,0))
    return im

class COMB15(Scene):
    def setup(self):
        mf=ROOT/'voice'/'comb15_voice_manifest.json'
        if not mf.is_file():raise FileNotFoundError('Prepare lesson first: python scripts/prepare_comb15_v2.py --voice off')
        self.manifest=json.loads(mf.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('COMB15 manifest beat mismatch')
        self.last=None
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.63,3.62,18,C['cyan'],True,6.0))
        self.add(txt('COMB15  /  LẬP SỐ THEO ĐIỀU KIỆN',3.58,3.62,18,C['muted'],True,5.6))
        self.add(Line((-6.84,3.32,0),(6.84,3.32,0),color=C['line'],stroke_width=1.2))
        for x,w in ((LX,6.16),(RX,6.52)):
            self.add(RoundedRectangle(width=w,height=6.18,corner_radius=.17,stroke_width=1.3,
                         stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1).move_to((x,0,0)))
        self.add(Line((-6.84,-3.32,0),(6.84,-3.32,0),color=C['line'],stroke_width=1.2))

    def right_panel(self,b,i):
        head=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.65,15,C['purple'],True,5.8),
                    txt(b.heading,RX,2.06,20,C['gold'],True,5.84))
        lines=VGroup(*[txt('• '+t,RX,1.28-.63*j,17,C['text'],False,5.78) for j,t in enumerate(b.lines)])
        formula=formula_image(b.formula)
        words=b.takeaway.split(); phrases=[];phrase=[]
        for word in words:
            if phrase and len(' '.join(phrase+[word]))>37:
                phrases.append(' '.join(phrase));phrase=[word]
            else:phrase.append(word)
        if phrase:phrases.append(' '.join(phrase))
        if len(phrases)>2: phrases=[phrases[0],' '.join(phrases[1:])]
        bottom=VGroup(Line((.18,-1.81,0),(6.26,-1.81,0),color=C['line'],stroke_width=1))
        for j,s in enumerate(phrases):bottom.add(txt(s,RX,-2.16-.34*j,14,C['green'],True,5.72))
        count=txt(f'{i+1:02d} / 48',.0,-3.66,15,C['muted'],True)
        return head,lines,formula,bottom,count

    def show_beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            p=ROOT/'voice'/clip['file']
            if not p.is_file():raise FileNotFoundError(p)
            self.add_sound(str(p))
        duration=max(float(b.min_seconds),float(clip.get('duration',0))+.85)
        art,focus=make_group(b.section,b.state)
        head,lines,formula,bottom,counter=self.right_panel(b,i)
        if self.last is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(counter),run_time=1.0)
            spent=1.0
        else:
            oa,oh,ol,of,ob,oc=self.last
            self.play(FadeOut(oa),FadeOut(oh),FadeOut(ol),FadeOut(of),FadeOut(ob),
                      FadeIn(art),FadeIn(head),ReplacementTransform(oc,counter),run_time=1.15)
            spent=1.15
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.012),run_time=1.3)
        spent+=1.3
        for line in lines:
            self.play(FadeIn(line,shift=UP*.07),run_time=1.18)
            spent+=1.18
        self.play(FadeIn(formula,shift=UP*.06),run_time=1.28);spent+=1.28
        self.play(FadeIn(bottom),run_time=1.07);spent+=1.07
        self.play(Circumscribe(bottom[-1],color=C['green'],buff=.08),run_time=1.03);spent+=1.03
        if duration>spent:self.wait(duration-spent)
        self.last=(art,head,lines,formula,bottom,counter)

    def construct(self):
        for i,b in enumerate(BEATS):self.show_beat(i,b)
        self.play(*[FadeOut(o) for o in self.last],run_time=1)
        end=VGroup(txt('COMB15 · PHƯƠNG PHÁP LẬP SỐ THEO ĐIỀU KIỆN',0,.56,29,C['cyan'],True,12),
                   txt('CHỌN ĐÚNG VỊ TRÍ  ·  CHIA NHÁNH  ·  KIỂM CHỨNG',0,-.4,19,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.2)
        self.wait(3.0)
