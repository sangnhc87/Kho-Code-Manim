"""COMB20 — Binomial sums: 48 synchronized visual proof beats.

All formulas are precompiled with Typst. Run scripts/prepare_comb20_v2.py first.
"""
from __future__ import annotations
import sys,json,math
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb20_lesson_data import BEATS,CHAPTER_LABELS,row,falling,challenge_terms
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.58
RX=3.21

def tx(s,x,y,size=16,color=None,bold=False,limit=None):
    o=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if limit and o.width>limit:o.scale_to_fit_width(limit)
    o.move_to((x,y,0));return o

def badge(s,x,y,hot=False,width=.64,height=.52):
    c=C['gold'] if hot else C['cyan']
    p=RoundedRectangle(width=width,height=height,corner_radius=.08,stroke_color=c,stroke_width=1.7,
                       fill_color=C['panel_alt'],fill_opacity=1).move_to((x,y,0))
    return VGroup(p,tx(s,x,y,14,C['gold'] if hot else C['text'],True,width-.1))

def graph(section,state):
    """Construct one visual demonstration per mathematical state, not a generic slide."""
    g=VGroup(); focus=None
    if section in ('foundation','evenodd','firstmark','secondmark','higher','partial','challenge'):
        n=5 if section=='foundation' else 6
        ks=list(range(n+1))
        if section=='challenge':
            vals=[v for _,v in challenge_terms()]
        elif section=='firstmark':vals=[k*math.comb(n,k) for k in ks]
        elif section=='secondmark':vals=[k*k*math.comb(n,k) if state>=3 else falling(k,2)*math.comb(n,k) for k in ks]
        elif section=='higher':vals=[(falling(k,3) if state<3 else k**3)*math.comb(n,k) for k in ks]
        elif section=='partial':vals=[(-1)**k*math.comb(n,k) for k in ks]
        else:vals=list(row(n))
        maxv=max(abs(v) for v in vals) or 1
        span=.71 if n==6 else .84
        base=-1.65 if section!='partial' else -.50
        g.add(tx(('CÁC HỆ SỐ NHỊ THỨC' if section in ('foundation','evenodd') else
                 'KẾT QUẢ THEO CHỈ SỐ k'),LX,2.50,16,C['cyan'],True,5.9))
        for i,v in enumerate(vals):
            x=LX+(i-(n/2))*span
            h=0 if v==0 else .12+min(2.30,2.0*abs(v)/maxv)
            positive=v>=0
            hot=((section=='foundation' and i<=min(5,state)) or
                 (section=='evenodd' and i%2==(state%2)) or
                 (section in ('firstmark','secondmark','higher') and i in (min(n,state+1),)) or
                 (section=='partial' and i<=state) or
                 (section=='challenge' and i==min(state,n)))
            color=C['gold'] if hot else (C['purple'] if i%2 else C['cyan'])
            y=(base+h/2) if positive else (base-h/2)
            bar=RoundedRectangle(width=.51,height=max(.04,h),corner_radius=.035,
                 fill_color=color,fill_opacity=.88,stroke_width=0).move_to((x,y,0))
            if v==0:bar.set_opacity(.18)
            g.add(bar)
            g.add(tx(str(v),x,y+(h/2+.2 if positive else -h/2-.22),11,C['gold'] if hot else C['text'],True,.7))
            g.add(tx(str(i),x,base-0.36 if section!='partial' else -2.88,14,C['muted'],True,.45))
            if hot:focus=bar
        if section=='foundation':
            val=['x = 1','TỔNG = 32','n BẤT KỲ','x = −1','CHẴN = LẺ','NHẬN DIỆN TỔNG'][state]
        elif section=='evenodd':val=['E + O','E − O','E = O','ĐỔI MỘT CÔNG TẮC','128 / 128','LỌC MODULO m'][state]
        elif section=='firstmark':val=['k TRỌNG SỐ','ĐẠO HÀM','THẾ x=1','ĐÁNH DẤU THẺ','5·16 = 80','TỔNG QUÁT a,b'][state]
        elif section=='secondmark':val=['CẶP CÓ THỨ TỰ','ĐẠO HÀM HAI LẦN','(k)₂','TÁCH k²','CÔNG THỨC k²','THỬ n=4'][state]
        elif section=='higher':val=['BA DẤU','BẬC r','TÁCH k³','TỔNG k³','STIRLING','TOÁN TỬ D'][state]
        elif section=='partial':val=['ĐOẠN XEN DẤU','PASCAL','TRIỆT TIÊU','n=6, r=3','KIỂM TRA BIÊN','MỞ RỘNG'][state]
        else:val=['TỔNG ĐẶC BIỆT','ĐA THỨC NGUỒN','F′+F″','37.500','75.000','112.500'][state]
        g.add(tx(val,LX,-2.58,16,C['green'],True,5.9))
    elif section=='integral':
        g.add(tx('TỪ HỆ SỐ ĐẾN DIỆN TÍCH',LX,2.5,16,C['cyan'],True,5.8))
        # Quadrature illustration: y=(1+x)^3/8 on [0,1], with filled vertical strips.
        origin=(-5.7,-1.80)
        width=4.50;height=3.25
        g.add(Line((origin[0],origin[1],0),(origin[0]+width+.25,origin[1],0),color=C['muted']))
        g.add(Line((origin[0],origin[1],0),(origin[0],origin[1]+height+.25,0),color=C['muted']))
        pts=[]
        for j in range(61):
            x=j/60;v=((1+x)**3)/8
            pts.append((origin[0]+width*x,origin[1]+height*v,0))
        curve=VMobject(stroke_color=C['cyan'],stroke_width=3)
        curve.set_points_as_corners(pts);g.add(curve)
        for j in range(18):
            x=(j+.5)/18;v=((1+x)**3)/8
            h=v*height
            rec=Rectangle(width=width/18-.014,height=h,fill_opacity=.13 if state==0 else .30,
                fill_color=C['gold'] if j<=state*3+2 else C['purple'],stroke_width=0)
            rec.move_to((origin[0]+x*width,origin[1]+h/2,0));g.add(rec)
            if j==min(state*3,17):focus=rec
        for j,label in enumerate(['0','1']):g.add(tx(label,origin[0]+j*width,origin[1]-.30,13,C['muted']))
        g.add(tx(['MẪU k+1','DIỆN TÍCH x^k','CỘNG TÍCH PHÂN','BIỂU THỨC ĐÓNG','n=3 CHO 15/4','MẪU KÉP'][state],LX,-2.65,15,C['green'],True,5.7))
    if focus is None:focus=g[1]
    return g,focus

def load_formula(key):
    src=ROOT/'assets'/'comb20v2'/f'{key}.png'
    if not src.exists():raise FileNotFoundError(f'Compile Typst before Manim: {src}')
    o=ImageMobject(str(src))
    if o.width>5.82:o.scale_to_fit_width(5.82)
    if o.height>1.12:o.scale_to_fit_height(1.12)
    o.move_to((RX,-1.24,0))
    return o

class COMB20(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb20_voice_manifest.json'
        if not path.exists():raise FileNotFoundError('Run scripts/prepare_comb20_v2.py first')
        self.manifest=json.loads(path.read_text(encoding='utf8'))
        assert self.manifest['beats']==len(BEATS)
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.60,16,C['cyan'],True,6))
        self.add(tx('COMB20  /  TỔNG HỆ SỐ NHỊ THỨC',RX,3.60,14,C['muted'],True,6))
        self.add(Line((-6.89,3.31,0),(6.89,3.31,0),stroke_color=C['line'],stroke_width=1))
        for x,width in ((LX,6.23),(RX,6.38)):
            self.add(RoundedRectangle(width=width,height=6.12,corner_radius=.12,
                fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1).move_to((x,0,0)))
        self.current=None

    def beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}'];seconds=max(b.min_seconds,float(clip.get('duration',0))+.85)
        if clip.get('file'):
            audio=ROOT/'voice'/clip['file'];self.add_sound(str(audio))
        model,focus=graph(b.section,b.state)
        heading=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.72,13,C['purple'],True,5.90),
            tx(b.heading,RX,2.21,18,C['gold'],True,5.82))
        bullets=VGroup(*[tx('• '+line,RX,1.41-j*.61,15,C['text'],False,5.82) for j,line in enumerate(b.lines)])
        formula=load_formula(b.formula)
        note=VGroup(Line((.2,-1.95,0),(6.35,-1.95,0),color=C['line']),
            tx(b.takeaway,RX,-2.45,13,C['green'],True,5.8))
        number=tx(f'{i+1:02d} / 48',0,-3.60,13,C['muted'],True)
        elapsed=0
        if self.current:
            old=self.current
            self.play(FadeOut(old[0]),FadeOut(old[1]),FadeOut(old[2]),FadeOut(old[3]),FadeOut(old[4]),
                ReplacementTransform(old[5],number),FadeIn(model),FadeIn(heading),run_time=1.4)
            elapsed+=1.4
        else:
            self.play(FadeIn(model),FadeIn(heading),FadeIn(number),run_time=1.4);elapsed+=1.4
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.03),run_time=1.55);elapsed+=1.55
        for line in bullets:
            self.play(FadeIn(line,shift=UP*.065),run_time=1.15);elapsed+=1.15
        self.play(FadeIn(formula,shift=UP*.09),run_time=1.4);elapsed+=1.4
        self.play(FadeIn(note),run_time=.75);elapsed+=.75
        if seconds-elapsed>6:
            wait=(seconds-elapsed-1.6)/2
            self.wait(wait);elapsed+=wait
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.02),run_time=1.6);elapsed+=1.6
        if seconds>elapsed:self.wait(seconds-elapsed)
        self.current=(model,heading,bullets,formula,note,number)

    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        if self.current:self.play(*[FadeOut(x) for x in self.current],run_time=1)
        end=VGroup(tx('CÁC TỔNG HỆ SỐ NHỊ THỨC',0,.45,26,C['cyan'],True,12),
            tx('PHÉP THẾ  •  ĐẠO HÀM  •  TÍCH PHÂN  •  ĐẾM ĐÔI',0,-.50,19,C['gold'],True,12))
        self.play(FadeIn(end),run_time=1.2);self.wait(3)
