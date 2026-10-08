"""COMB14: Complementary counting, eight chapters and 48 timed teaching beats.

Prepare first: python scripts/prepare_comb14_v2.py --voice off
Render: manim -ql -r 854,480 --fps 24 episodes/comb14_complement.py COMB14
"""
from __future__ import annotations
import sys,json,math,itertools
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb14_lesson_data import BEATS, CHAPTER_LABELS
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

def make_group(section,state):
    art=VGroup();focus=None
    if section=='universe':
        banner(art,'TỔNG THỂ 81 DÃY','XANH: CÓ A  ·  ĐỎ: KHÔNG CÓ A')
        focus=miniature_universe(art,state)
    elif section=='groups':
        banner(art,'CHỌN 3 TRONG 9 HỌC SINH','TỔNG NHÓM 84  ·  LOẠI TOÀN NAM 10')
        colors=[C['cyan']]*5+[C['gold']]*4
        tiles=tile_row(art,list('ABCDE')+list('FGHI'),y=.75,colors=colors,spacing=.62)
        focus=mark(art,VGroup(*tiles[:3]),'CHỌN NHÓM',C['green'])
        art.add(txt('5 NAM',LX-1.55,-.45,16,C['cyan'],True),txt('4 NỮ',LX+1.25,-.45,16,C['gold'],True))
        if state>=1: art.add(txt('KHÔNG NỮ: CHỌN 3 TRONG 5 NAM',LX,-1.19,16,C['red'],True,5.5))
        if state>=2: art.add(txt('84 - 10 = 74 NHÓM',LX,-1.86,23,C['green'],True,5.5))
        if state==3: art.add(txt('40 + 30 + 4 = 74',LX,-2.29,16,C['gold'],True,5.4))
    elif section=='seating':
        banner(art,'XẾP HÀNG CÓ ĐIỀU KIỆN','PHẦN VI PHẠM ĐƯỢC ĐÁNH DẤU ĐỎ')
        labels=list('ABCDE') if state<3 else list('ABCDEF')
        tiles=tile_row(art,labels,y=.72,colors=[C['gold'],C['purple']]+[C['cyan']]*(len(labels)-2),spacing=.77)
        focus=mark(art,VGroup(tiles[0],tiles[1]),'AB KỀ',C['red'])
        if state>=1:art.add(txt('[AB]  C  D  E',LX,-.86,22,C['gold'],True))
        if state>=2 and state<3:art.add(txt('120 - 48 = 72',LX,-1.71,24,C['green'],True))
        if state>=3:art.add(txt('720 - 120 = 600',LX,-1.67,21,C['green'],True))
        if state==5:art.add(txt('720 - 120 - 240 + 24 = 384',LX,-2.14,16,C['gold'],True,5.8))
    elif section=='pin':
        banner(art,'MÃ PIN GỒM BỐN CHỮ SỐ','KHÔNG CẤM CHỮ SỐ 0 ĐỨNG ĐẦU')
        tiles=tile_row(art,['0','0','0','7'],y=.72,colors=[C['gold']]*3+[C['cyan']],spacing=1.05)
        focus=mark(art,VGroup(*tiles[:3]),'LẶP CHỮ SỐ 0',C['red'])
        art.add(txt('10   →   9   →   8   →   7',LX,-.80,19,C['cyan'],True,5.5))
        if state>=2:art.add(txt('5.040 MÃ KHÔNG LẶP',LX,-1.44,17,C['gold'],True))
        if state>=3:art.add(txt('10.000 - 5.040 = 4.960',LX,-2.08,20,C['green'],True,5.6))
        if state>=4:art.add(txt('SỐ 4 CHỮ SỐ: 4.464',LX,-2.47,14,C['purple'],True))
    elif section=='fixed':
        banner(art,'BỐN THƯ – BỐN PHONG BÌ','VỊ TRÍ ĐÚNG: ĐIỂM CỐ ĐỊNH')
        letters=tile_row(art,list('ABCD'),y=1.10,colors=[C['cyan']]*4,spacing=1.13)
        slots=tile_row(art,list('ABCD'),y=-.25,colors=[C['gold']]*4,spacing=1.13)
        focus=mark(art,slots[0],'A ĐÚNG VỊ TRÍ',C['red'])
        for j in range(4):
            art.add(Line(letters[j].get_bottom()+DOWN*.06,slots[j].get_top()+UP*.08,
                         stroke_color=C['inactive'],stroke_width=1.4))
        if state>=2:art.add(txt('24 - 24 + 12 - 4 + 1',LX,-1.64,20,C['purple'],True,5.55))
        if state>=3:art.add(txt('9 CÁCH KHÔNG LÁ NÀO ĐÚNG',LX,-2.20,17,C['green'],True,5.7))
    elif section=='binary':
        banner(art,'DÃY 0–1 DÀI SÁU','CẶP 11 LÀ MỘT MẪU LIỀN NHAU')
        vals=list('101101') if state<2 else list('101010')
        cols=[C['gold'] if x=='1' else C['cyan'] for x in vals]
        tiles=tile_row(art,vals,y=.68,colors=cols,spacing=.75)
        pair=(2,3) if state<2 else (0,1)
        focus=mark(art,VGroup(*[tiles[i] for i in pair]),'CẶP 11' if state<2 else 'BẮT ĐẦU 10',C['red'] if state<2 else C['green'])
        if state>=1:art.add(txt('fₙ = fₙ₋₁ + fₙ₋₂',LX,-.82,24,C['purple'],True,5.5))
        if state>=3:art.add(txt('1, 2, 3, 5, 8, 13, 21',LX,-1.65,18,C['gold'],True,5.52))
        if state>=4:art.add(txt('64 - 21 = 43 DÃY',LX,-2.27,22,C['green'],True,5.55))
    elif section=='twopicks':
        banner(art,'CHỌN ĐỘI CÓ A HOẶC B','ĐỌC “HOẶC” THEO NGHĨA BAO GỒM')
        cols=[C['gold'],C['purple']]+[C['cyan']]*6
        tiles=tile_row(art,list('ABCDEFGH'),y=.65,colors=cols,spacing=.68)
        focus=mark(art,VGroup(tiles[0],tiles[1]),'A HOẶC B',C['green'])
        art.add(txt('56 TỔNG NHÓM',LX,-.90,19,C['gold'],True))
        if state>=1:art.add(txt('20 NHÓM KHÔNG A,B',LX,-1.41,17,C['red'],True))
        if state>=2:art.add(txt('56 - 20 = 36',LX,-2.02,22,C['green'],True))
        if state>=3:art.add(txt('ĐÚNG MỘT: 30 · CẢ HAI: 6',LX,-2.48,14,C['purple'],True,5.5))
    else:
        banner(art,'ĐỘI BỐN NGƯỜI CÓ ĐỘI TRƯỞNG','A HOẶC B PHẢI CÓ · TRƯỞNG KHÔNG LÀ A')
        cols=[C['gold'],C['purple']]+[C['cyan']]*6
        tiles=tile_row(art,list('ABCDEFGH'),y=1.00,colors=cols,spacing=.67)
        focus=mark(art,VGroup(tiles[0],tiles[1]),'ĐIỀU KIỆN A/B',C['green'])
        art.add(txt('CHỌN 4 BẠN + 1 ĐỘI TRƯỞNG',LX,-.44,16,C['cyan'],True,5.5))
        if state>=1:art.add(txt('280 TỔNG CÁCH',LX,-1.06,18,C['gold'],True))
        if state>=2:art.add(txt('CẤM THIẾU A,B: 60',LX,-1.55,16,C['red'],True))
        if state>=3:art.add(txt('CẤM TRƯỞNG A: 35',LX,-1.99,16,C['red'],True))
        if state>=4:art.add(txt('280 - 60 - 35 = 185',LX,-2.49,18,C['green'],True,5.5))
    return art,focus

def formula_image(key):
    p=ROOT/'assets'/'comb14v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Prepare Typst formulas first: {p}')
    im=ImageMobject(str(p))
    im.scale_to_fit_width(min(im.width,5.80))
    if im.height>.86:im.scale_to_fit_height(.86)
    im.move_to((RX,-1.11,0))
    return im

class COMB14(Scene):
    def setup(self):
        mf=ROOT/'voice'/'comb14_voice_manifest.json'
        if not mf.is_file():raise FileNotFoundError('Prepare lesson first: python scripts/prepare_comb14_v2.py --voice off')
        self.manifest=json.loads(mf.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('COMB14 manifest beat mismatch')
        self.last=None
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.63,3.62,18,C['cyan'],True,6.0))
        self.add(txt('COMB14  /  ĐẾM PHẦN BÙ',3.58,3.62,18,C['muted'],True,5.6))
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
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.025),run_time=1.3)
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
        end=VGroup(txt('COMB14 · PHƯƠNG PHÁP ĐẾM PHẦN BÙ',0,.56,29,C['cyan'],True,12),
                   txt('ĐẾM TẤT CẢ  -  ĐẾM KHÔNG THỎA  =  ĐẾM THỎA',0,-.4,19,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.2)
        self.wait(3.0)
