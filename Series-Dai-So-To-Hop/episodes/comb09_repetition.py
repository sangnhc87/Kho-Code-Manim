"""COMB09 V2 — Dãy có thứ tự cho phép lặp; 48 đồng bộ nhịp giảng.

Requires: python scripts/prepare_comb09_v2.py --voice on|off
Mathematical counts are independently enumerated in comb09_lesson_data.py.
"""
from __future__ import annotations
import json, sys
from itertools import product
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb09_lesson_data import BEATS, CHAPTER_LABELS
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.70
RX=3.15


def txt(s,x,y,size=20,color=None,bold=False,width=None):
    o=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if width and o.width>width:o.scale_to_fit_width(width)
    o.move_to((x,y,0))
    return o


def panel(t,x,y,width=1.05,height=.67,color=None,size=19):
    color=color or C['cyan']
    shape=RoundedRectangle(width=width,height=height,corner_radius=.12,
                           stroke_color=color,stroke_width=1.8,fill_color=C['panel_alt'],fill_opacity=1)
    shape.move_to((x,y,0))
    return VGroup(shape,txt(t,x,y,size,C['text'],True,width-.14))


def sign(g,s,y=-2.53,color=None):
    g.add(txt(s,LX,y,16,color or C['gold'],True,5.65))


def header(g,s):
    g.add(txt(s,LX,2.51,18,C['cyan'],True,5.70))


def slots(g,items,y=.90,color=None,width=.91,dx=1.30):
    result=[]
    for j,val in enumerate(items):
        x=LX+(j-(len(items)-1)/2)*dx
        obj=panel(val,x,y,width,.76,color or C['purple'],18)
        g.add(obj);result.append(obj)
    return result


def pattern_tiles(g,patterns,limit,cols=3,top=.90,dx=1.72,dy=.48,font=16):
    objs=[]
    for i,p in enumerate(patterns):
        x=LX+(i%cols-(cols-1)/2)*dx
        y=top-(i//cols)*dy
        col=C['green'] if i<limit else C['inactive']
        item=panel(p,x,y,min(dx-.12,1.60),dy-.055,col,font)
        g.add(item);objs.append(item)
    return objs


def repeat_view(s):
    g=VGroup();header(g,'CHỌN LẠI ĐƯỢC · HAI VỊ TRÍ')
    for i,l in enumerate('ABC'):
        g.add(panel(l,LX-1.1+i*1.1,1.62,.8,.74,C['cyan'],24))
    slots(g,['Ô 1','Ô 2'],y=.76,color=C['purple'])
    examples=[a+b for a in 'ABC' for b in 'ABC']
    limit=[0,0,3,9,9,9][s]
    tiles=pattern_tiles(g,examples,limit,cols=3,top=-.05,dy=.54)
    sign(g,'3 CÁCH  ×  3 CÁCH  =  9 DÃY' if s>=3 else 'CHỮ ĐÃ DÙNG VẪN CÓ THỂ DÙNG LẠI')
    return g,tiles[min(max(limit-1,0),8)] if s>=2 else g[1]


def strings_view(s):
    g=VGroup();header(g,'DÃY DÀI BA · MỖI Ô BA LỰA CHỌN')
    slots(g,['1','2','3'],y=1.53,color=C['purple'],width=.85,dx=1.42)
    g.add(txt('3  ×  3  ×  3',LX,.77,26,C['gold'],True,5.3))
    # All 27 results in three 9-element columns; each column corresponds to first letter.
    objects=[]
    for j,a in enumerate('ABC'):
        col=VGroup()
        for i,(b,c) in enumerate(product('ABC',repeat=2)):
            v=txt(a+b+c,LX+(j-1)*1.8,.21-(i//3)*.44-(i%3)*.035,14,
                  C['green'] if s>=3 or j<=max(0,s-2) else C['inactive'],True,1.35)
            v.shift(DOWN*(i%3)*.11) # separate the nine entries within each column
            col.add(v)
        col.arrange(DOWN,buff=.07)
        col.move_to((LX+(j-1)*1.82,-.74,0))
        g.add(col);objects.append(col)
    sign(g,'9 TIỀN TỐ  →  27 DÃY' if s>=3 else 'MỖI VỊ TRÍ CÓ BA CÁCH CHỌN')
    return g,objects[min(s//2,2)]


def pin_view(s):
    g=VGroup();header(g,'MÃ PIN 4 KÝ TỰ · ĐƯỢC LẶP')
    for k in range(10):
        x=LX-2.43+k*.54
        g.add(panel(str(k),x,1.47,.46,.58,C['cyan'],15))
    show=['?','?','?','?']
    if s>=3:show=['0','0','7','3']
    else:
        for i in range(min(s,4)):show[i]='0–9'
    boxes=slots(g,show,y=.35,color=C['gold'],width=1.13,dx=1.40)
    counts=['10','100','1 000','10 000']
    progress=min(max(s,1),4)
    g.add(panel(counts[progress-1],LX,-.85,3.15,.72,C['green'],23))
    g.add(txt('MÃ 0073 VẪN CÓ 4 KÝ TỰ' if s>=4 else 'CHỮ SỐ ĐẦU CÓ THỂ BẰNG 0',LX,-1.75,16,C['muted'],True,5.7))
    sign(g,'CẤU TRÚC MÃ PIN KHÁC SỐ CÓ 4 CHỮ SỐ')
    return g,boxes[min(s%4,3)]


def norepeat_view(s):
    g=VGroup();header(g,'KHÔNG LẶP · SỐ LỰA CHỌN GIẢM DẦN')
    used=[str(j) for j in range(min(s,3))]
    for k in range(10):
        x=LX-2.44+k*.54
        g.add(panel(str(k),x,1.59,.47,.55,C['red'] if str(k) in used else C['cyan'],15))
    arr=['10','9','8','7'] if s<=3 else ['9','9','8','7'] if s==4 else ['10','9','8','7']
    boxes=slots(g,arr,y=.48,color=C['purple'],width=1.07,dx=1.41)
    g.add(txt('CHUỖI: 10 × 9 × 8 × 7 = 5 040',LX,-.60,18,C['green'],True,5.7))
    g.add(txt('SỐ 4 CHỮ SỐ: 9 × 9 × 8 × 7 = 4 536',LX,-1.33,17,C['gold'],True,5.75))
    sign(g,'LẶP / KHÔNG LẶP  ·  MÃ / SỐ LÀ 2 CÂU HỎI')
    return g,boxes[min(s,3)]


def multiset_view(s):
    g=VGroup();header(g,'NHÓM KHÔNG XÉT THỨ TỰ · CÓ LẶP')
    samples=['ABC','BAC','CAB']
    for i,p in enumerate(samples):
        g.add(panel(p,LX+(i-1)*1.73,1.46,1.4,.66,C['purple'],19))
    g.add(txt('CÙNG MỘT NHÓM {A, B, C}',LX,.80,18,C['green'],True,5.65))
    allchoices=['AAA','AAB','AAC','ABB','ABC','ACC','BBB','BBC','BCC','CCC']
    n=[0,0,3,9,10,10][s]
    blocks=pattern_tiles(g,allchoices,n,cols=5,top=-.16,dx=1.12,dy=.85,font=15)
    sign(g,'27 DÃY CÓ THỨ TỰ  ≠  10 NHÓM KHÔNG THỨ TỰ')
    return g,blocks[min(max(n-1,0),9)] if s>=2 else g[1]


def atleast_view(s):
    g=VGroup();header(g,'ÍT NHẤT MỘT A · ĐẾM BẰNG PHẦN BÙ')
    slots(g,['1','2','3','4'],y=1.57,color=C['purple'],width=.78,dx=1.10)
    items=[''.join(p) for p in product('ABC',repeat=4)]
    dots=[]
    for j,w in enumerate(items):
        x=LX-1.75+(j%9)*.44; y=.99-(j//9)*.32
        invalid='A' not in w
        col=C['red'] if invalid and s>=2 else C['green'] if s>=3 and not invalid else C['inactive']
        circ=Dot(point=(x,y,0),radius=.091,color=col)
        g.add(circ);dots.append(circ)
    g.add(txt('81 TẤT CẢ',LX-1.55,-2.07,16,C['cyan'],True,1.9))
    g.add(txt('16 LOẠI' if s>=2 else 'PHẦN BÙ',LX+.05,-2.07,16,C['red'],True,1.9))
    g.add(txt('65 GIỮ' if s>=3 else '?',LX+1.93,-2.07,16,C['green'],True,1.8))
    sign(g,'MỖI CHẤM LÀ MỘT DÃY ĐỘ DÀI 4')
    return g,VGroup(*dots)


def exact_view(s):
    g=VGroup();header(g,'ĐÚNG HAI CHỮ A · CHỌN VỊ TRÍ TRƯỚC')
    forms=['AA··','A·A·','A··A','·AA·','·A·A','··AA']
    tiles=pattern_tiles(g,forms,[0,1,6,6,6,6][s],cols=3,top=1.24,dy=.97,dx=1.71,font=22)
    g.add(panel('6 CHỌN CẶP VỊ TRÍ',LX,-1.16,4.72,.66,C['purple'],18))
    g.add(panel('MỖI MẪU: 4 CÁCH ĐIỀN B/C',LX,-1.91,4.86,.66,C['green'],17))
    sign(g,'6 MẪU VỊ TRÍ  ×  4 CÁCH  =  24 DÃY')
    return g,tiles[min(s,5)]


def adjacency_view(s):
    g=VGroup();header(g,'CẤM HAI A LIỀN NHAU · TRUY HỒI')
    line1=['A','A','B','C'];line2=['A','B','A','C']
    for row,vals in enumerate([line1,line2]):
        for j,ch in enumerate(vals):
            g.add(panel(ch,LX+(j-1.5)*1.03,1.48-row*1.10,.75,.69,
                        C['red'] if row==0 and j<=1 else C['green'],19))
        g.add(txt('SAI' if row==0 else 'ĐÚNG',LX+2.43,1.48-row*1.1,14,
                  C['red'] if row==0 else C['green'],True,.75))
    vals=[('F0','1'),('F1','3'),('F2','8'),('F3','22'),('F4','60')]
    for i,(name,value) in enumerate(vals):
        x=LX+(i-2)*1.14
        box=panel(name+'='+value,x,-.49,1.03,.68,C['green'] if i<=min(s+1,4) else C['inactive'],14)
        g.add(box)
    g.add(txt('CUỐI B/C: 2F(n−1)' if s>=1 else 'XÉT CHỮ CUỐI',LX,-1.37,17,C['cyan'],True,5.5))
    g.add(txt('CUỐI A: 2F(n−2)' if s>=2 else 'CHIA HAI TRƯỜNG HỢP',LX,-1.91,17,C['gold'],True,5.5))
    sign(g,'F4 = 2×22 + 2×8 = 60' if s>=4 else 'CẤM AA KHÔNG CÓ NGHĨA CẤM LẶP B HOẶC C')
    return g,box

VIEWS={
'repeat':repeat_view,'strings':strings_view,'pin':pin_view,'norepeat':norepeat_view,
'multiset':multiset_view,'atleast':atleast_view,'exact':exact_view,'adjacency':adjacency_view
}


def math_image(key):
    png=ROOT/'assets'/'comb09v2'/f'{key}.png'
    if not png.is_file():raise FileNotFoundError(f'Missing Typst PNG {png}. Run scripts/prepare_comb09_v2.py')
    o=ImageMobject(str(png))
    o.scale_to_fit_width(min(o.width,5.70))
    if o.height>.85:o.scale_to_fit_height(.85)
    o.move_to((RX,-1.13,0));return o

class COMB09(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb09_voice_manifest.json'
        if not manifest.is_file():raise FileNotFoundError(f'Missing {manifest}; run prepare_comb09_v2.py')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Lesson / voice manifest mismatch')
        self.prev=None
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.7,3.63,19,C['cyan'],True,6.10))
        self.add(txt('COMB09  /  CHỌN CÓ LẶP',3.72,3.63,17,C['muted'],True,5.2))
        self.add(Line((-6.85,3.32,0),(6.85,3.32,0),stroke_width=1.1,color=C['line']))
        for x,w in [(LX,6.20),(RX,6.45)]:
            p=RoundedRectangle(width=w,height=6.16,corner_radius=.16,
                     stroke_color=C['line'],stroke_width=1.3,fill_color=C['panel'],fill_opacity=1)
            p.move_to((x,0,0));self.add(p)
        self.add(Line((-6.85,-3.32,0),(6.85,-3.32,0),stroke_width=1.1,color=C['line']))

    def right_panel(self,b,index):
        h=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.69,16,C['purple'],True,5.75),
                 txt(b.heading,RX,2.05,21,C['gold'],True,5.77))
        l=VGroup(*[txt('• '+t,RX,1.24-j*.60,18,C['text'],False,5.76)
                   for j,t in enumerate(b.lines)])
        e=math_image(b.formula) if b.formula else txt('QUAN SÁT → SUY LUẬN',RX,-1.13,17,C['cyan'],True,5.7)
        t=VGroup(Line((.27,-1.76,0),(6.13,-1.76,0),stroke_width=1.1,color=C['line']),
                 txt(b.takeaway,RX,-2.34,17,C['green'],True,5.78))
        counter=txt(f'{index+1:02d} / {len(BEATS)}',0,-3.69,15,C['muted'])
        return h,l,e,t,counter

    def one_beat(self,index,b):
        meta=self.meta['clips'][f'{index:03}']
        if meta.get('file'):
            sound=ROOT/'voice'/meta['file']
            if not sound.exists():raise FileNotFoundError(sound)
            self.add_sound(str(sound))
        budget=max(b.min_seconds,float(meta.get('duration',0))+.85)
        art,focus=VIEWS[b.section](b.state)
        head,lines,eq,takeaway,count=self.right_panel(b,index)
        if self.prev is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(count),run_time=1.0)
        else:
            old_art,old_h,old_l,old_eq,old_t,old_count=self.prev
            self.play(FadeOut(old_art),FadeIn(art),FadeOut(old_h),FadeIn(head),
                FadeOut(old_l),FadeOut(old_eq),FadeOut(old_t),
                ReplacementTransform(old_count,count),run_time=1.0)
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.055),run_time=1.8)
        for text in lines:self.play(FadeIn(text,shift=.07*UP),run_time=1.1)
        self.play(FadeIn(eq,shift=.07*UP),run_time=1.15)
        self.play(FadeIn(takeaway),run_time=.95)
        self.play(Circumscribe(takeaway[-1],color=C['green'],buff=.08),run_time=1.15)
        spent=1.0+1.8+3*1.1+1.15+.95+1.15
        if budget>spent:self.wait(budget-spent)
        self.prev=(art,head,lines,eq,takeaway,count)

    def construct(self):
        for i,b in enumerate(BEATS):self.one_beat(i,b)
        self.play(*[FadeOut(o) for o in self.prev],run_time=1.0)
        end=VGroup(txt('COMB09 · CHỌN CÓ LẶP',0,.54,32,C['cyan'],True,12),
                   txt('ĐÚNG MÔ HÌNH → ĐÚNG CÔNG THỨC',0,-.32,22,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.4);self.wait(2.8)
