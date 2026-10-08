"""COMB03 V2: tree diagrams, sample spaces, and constrained paths.

Run:
    python scripts/prepare_comb03_v2.py --voice off
    manim -ql -r 854,480 episodes/comb03_tree_sample_space.py COMB03
The prepared voice manifest makes scene timing identical to narration/SRT.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb03_lesson_data import (BEATS, CHAPTER_LABELS, OMEGA_3, EXACTLY_TWO_N,
    NO_ADJACENT_N, BAD_ADJACENT_N, OMEGA_4, NO_ADJACENT_4)
from series_config import PALETTE as C

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8.
FONT='Noto Sans'
LEFT=-3.82
RIGHT_PANEL=3.22
L_START=-6.80
L_END=-.80


def txt(s,x=0,y=0,size=22,color=None,bold=False,max_width=6.):
    m=Text(str(s),font=FONT,font_size=size,color=color or C['text'],
           weight='BOLD' if bold else 'NORMAL')
    if max_width and m.width>max_width:m.scale_to_fit_width(max_width)
    m.move_to([x,y,0])
    return m


def panel(w,h,stroke=None,fill=None):
    return RoundedRectangle(width=w,height=h,corner_radius=.13,
            stroke_color=stroke or C['line'],stroke_width=1.35,
            fill_color=fill or C['panel_alt'],fill_opacity=1)


def token(s,x,y,col=None,w=1.25,h=.53,size=21,opacity=1.):
    p=panel(w,h,col or C['line']);p.move_to([x,y,0])
    t=txt(s,x,y,size,C['text'],True,w-.12)
    result=VGroup(p,t)
    result.set_opacity(opacity)
    return result


def segment(x1,y1,x2,y2,col=None,opacity=1.,weight=2.4):
    return Line([x1,y1,0],[x2,y2,0],stroke_color=col or C['line'],
                stroke_opacity=opacity,stroke_width=weight)


def counter(s,col=None):
    return txt(s,LEFT,-2.70,22,col or C['green'],True,5.80)


def outcome_color(s):
    return C['cyan'] if s=='N' else C['gold']


ROOT_POS=(-6.35,0.)
P1={'N':(-4.97,1.23),'S':(-4.97,-1.23)}
P2={'NN':(-3.42,1.84),'NS':(-3.42,.62),
    'SN':(-3.42,-.62),'SS':(-3.42,-1.84)}
P3={v:(-1.61,2.18-i*(4.36/7)) for i,v in enumerate(OMEGA_3)}


def tree_picture(depth=3,selected=(),excluded=(),show_results=True,tag='',prune=False):
    selected=set(selected);excluded=set(excluded)
    leaf_tokens={}
    g=VGroup()
    g.add(txt('N',-5.37,2.67,15,C['cyan']),txt('S',-4.55,2.67,15,C['gold']))
    g.add(Dot([*ROOT_POS,0],radius=.105,color=C['text']))
    for key,(x,y) in P1.items():
        if depth<1:break
        g.add(segment(*ROOT_POS,x-.30,y,outcome_color(key)))
        g.add(token(key,x,y,outcome_color(key),.68,.49,18))
    if depth>=2:
        for key,(x,y) in P2.items():
            px,py=P1[key[0]]
            g.add(segment(px+.33,py,x-.40,y,outcome_color(key[-1])))
            g.add(token(key,x,y,outcome_color(key[-1]),.80,.45,17))
    if depth>=3:
        for key,(x,y) in P3.items():
            px,py=P2[key[:2]]
            forbidden=key in excluded
            chosen=key in selected
            c=C['red'] if forbidden else C['green'] if chosen else C['line']
            opacity=.30 if (selected or excluded) and not (forbidden or chosen) else 1.
            if prune and key.startswith('NN'):
                opacity=.16
            g.add(segment(px+.42,py,x-.65,y,outcome_color(key[-1]),opacity,1.8))
            if show_results:
                leaf=token(key,x,y,c,1.22,.41,18,opacity)
                g.add(leaf)
                leaf_tokens[key]=leaf
            else:
                g.add(Dot([x,y,0],radius=.065,color=c).set_opacity(opacity))
            if forbidden:
                strike=segment(x-.42,y-.17,x+.42,y+.17,C['red'],.90,2.8)
                g.add(strike)
    if tag:g.add(counter(tag))
    g.leaf_tokens=leaf_tokens
    return g


def _coin(x,y,letter,dim=False):
    color=outcome_color(letter)
    circle=Circle(radius=.39,stroke_color=color,stroke_width=2.8,
                  fill_color=color,fill_opacity=.14).move_to([x,y,0])
    content=txt(letter,x,y,27,color,True)
    result=VGroup(circle,content)
    if dim:result.set_opacity(.35)
    return result


def intro(s):
    g=VGroup(txt('THÍ NGHIỆM TUNG ĐỒNG XU',LEFT,2.50,19,C['cyan'],True,5.8))
    for i,x in enumerate([-5.67,-3.82,-1.97]):
        letter='NSN'[i]
        g.add(_coin(x,1.12,letter,dim=(s<3 and i>0)))
        g.add(txt(str(i+1),x,.43,15,C['muted']))
        if i>0:g.add(segment(x-.95,1.12,x-.89,1.12,C['line']))
    if s in (0,3,4):
        g.add(token('N',-4.58,-.51,C['cyan'],1.13,.64,23),
              token('S',-3.07,-.51,C['gold'],1.13,.64,23))
    elif s in (1,2):
        for i,v in enumerate(['NSN','SNN','NN']):
            g.add(token(v,-5.30+i*1.45,-.65,C['cyan'] if i<2 else C['line'],1.20,.65,22))
    else:
        g.add(token('N',-5.30,-.38,C['cyan']),token('S',-3.85,-.38,C['gold']))
        g.add(txt('3 TẦNG LỰA CHỌN',LEFT,-1.50,24,C['gold'],True))
    g.add(counter('Mỗi lần: N hoặc S' if s<4 else 'Ba lần tung liên tiếp',C['gold']))
    return g,g[1]


def omega(s):
    g=VGroup(txt('TẬP HỢP CÁC DÃY KẾT QUẢ',LEFT,2.47,20,C['cyan'],True,5.7))
    selected=set(EXACTLY_TWO_N) if s==5 else set()
    visible=8 if s>=1 else 4
    for i,key in enumerate(OMEGA_3):
        x=-5.22+(i%2)*2.73
        y=1.65-(i//2)*.94
        c=C['green'] if key in selected else C['cyan'] if i%2==0 else C['gold']
        g.add(token(key,x,y,c,2.02,.72,23,1. if i<visible else .17))
    if s==2:g.add(counter('|Omega| = 8'))
    elif s==4:g.add(counter('Cân đối + độc lập: mỗi dãy 1/8',C['gold']))
    elif s==5:g.add(counter('A = {NNS, NSN, SNN}'))
    elif s==3:g.add(counter('Mỗi lá ↔ một dãy duy nhất',C['green']))
    else:g.add(counter('8 kết quả được liệt kê theo cây',C['muted']))
    return g,g[1]


def exactlytwo(s):
    selected=EXACTLY_TWO_N[:min(3,max(0,s))]
    tag='3 kết quả thỏa mãn' if s>=4 else 'Đếm đúng hai lần N'
    pic=tree_picture(3,selected=selected,tag=tag)
    if s>=4:
        # Highlight all three at the end of the derivation.
        pic=tree_picture(3,selected=EXACTLY_TWO_N,tag='A = {NNS, NSN, SNN}')
    if s==5:pic.add(txt('Nếu cân đối: P(A) = 3/8',LEFT,-2.18,19,C['gold'],True,5.5))
    target=EXACTLY_TWO_N[min(max(s-1,0),2)] if s in (1,2,3) else 'NSN'
    return pic,pic.leaf_tokens.get(target,pic[0])


def noadjacent(s):
    excluded=BAD_ADJACENT_N[:min(3,max(0,s+1))] if s in (1,2) else ()
    selected=NO_ADJACENT_N if s>=3 else ()
    if s>=3:excluded=BAD_ADJACENT_N
    pic=tree_picture(3,selected=selected,excluded=excluded,
                     tag=('8 − 3 = 5 kết quả' if s>=4 else 'Không có cặp NN'),prune=s==1)
    target='NNN' if s==1 else 'SNN' if s==2 else 'NSN'
    return pic,pic.leaf_tokens.get(target,pic[0])


def proof(s):
    excluded=BAD_ADJACENT_N if s==3 else ()
    sel=('NSN',) if s in (2,4) else ()
    depth=3
    pic=tree_picture(depth,selected=sel,excluded=excluded,
                     tag='Mỗi đường đi ứng với đúng một dãy')
    if s==2:pic.add(txt('N   ->   S   ->   N',LEFT,-2.17,18,C['cyan'],True))
    if s==3:pic.add(txt('Tiền tố NN: chắc chắn vi phạm',LEFT,-2.17,17,C['red'],True))
    if s==4:pic.add(txt('Tiền tố NS: CHƯA vi phạm',LEFT,-2.17,17,C['green'],True))
    return pic,pic.leaf_tokens.get('NSN',pic[0])


def expansion(s):
    g=VGroup(txt('BỐN LẦN TUNG: 16 DÃY',LEFT,2.50,20,C['cyan'],True))
    good=set(NO_ADJACENT_4)
    ends_s={v for v in good if v.endswith('S')}
    ends_sn={v for v in good if v.endswith('SN')}
    for i,key in enumerate(OMEGA_4):
        x=-5.91+(i%4)*1.38
        y=1.64-(i//4)*.89
        if s==0:col=C['line'];opa=1.
        elif s==1:col=C['green'] if key in good else C['red'];opa=1.
        elif s==2:col=C['green'] if key in ends_s else C['line'];opa=1. if key in ends_s else .20
        elif s==3:col=C['gold'] if key in ends_sn else C['line'];opa=1. if key in ends_sn else .20
        else:col=C['green'] if key in good else C['red'];opa=1. if key in good else .22
        g.add(token(key,x,y,col,1.20,.60,16,opa))
    count=['16 kết quả không điều kiện',
           '8 dãy không có NN','Nhóm kết thúc S: 5 dãy',
           'Nhóm kết thúc SN: 3 dãy',
           '5 + 3 = 8 dãy hợp lệ',
           'f(n) = f(n-1) + f(n-2)'][s]
    g.add(counter(count,C['green']))
    return g,g[1]


def practice(s):
    if s<4:
        g=VGroup(txt('TÌM KẾT QUẢ THỎA ĐIỀU KIỆN',LEFT,2.50,20,C['cyan'],True))
        one_n={'NSS','SNS','SSN'}
        starts_s={v for v in OMEGA_3 if v.startswith('S')}
        picked=one_n if s==1 else starts_s if s==3 else set()
        for i,key in enumerate(OMEGA_3):
            x=-5.20+(i%2)*2.65
            y=1.67-(i//2)*.92
            g.add(token(key,x,y,C['green'] if key in picked else C['line'],2.05,.65,21,
                        1. if key in picked or not picked else .30))
        g.add(counter('3 kết quả' if s==1 else '4 kết quả' if s==3 else 'Hãy thử đếm trên cây',C['gold']))
    else:
        g=VGroup(txt('BA NHÁNH - SỐ LÁ KHÁC NHAU',LEFT,2.51,19,C['cyan'],True))
        start=(-6.20,-.10)
        g.add(Dot([*start,0],radius=.11,color=C['text']))
        for i,y in enumerate((1.60,0,-1.60)):
            g.add(segment(*start,-4.75,y,C['cyan']))
            g.add(token('M'+str(i+1),-4.62,y,C['cyan'],1.03,.58,21))
            count=(2,1,3)[i]
            for j in range(count):
                dy=(j-(count-1)/2)*.45
                yy=y+dy
                g.add(segment(-4.03,y,-2.64,yy,C['gold'],1.,2.0))
                g.add(token('D'+str(j+1),-2.22,yy,C['gold'],.82,.39,16))
        g.add(counter('2 + 1 + 3 = 6' if s==5 else 'Đếm lá của từng nhánh',C['green']))
    return g,g[1]


def visual(beat):
    name=beat.section
    state=beat.state
    if name=='intro':return intro(state)
    if name=='growth':
        level=1 if state==0 else 2 if state==1 else 3
        selected=('NSN',) if state==4 else ()
        pic=tree_picture(level,selected=selected,show_results=state>=3,
                         tag=('2 x 2 x 2 = 8' if state>=3 else 'Mở thêm một tầng của cây'))
        return pic,pic.leaf_tokens.get('NSN',pic[0])
    if name=='omega':return omega(state)
    if name=='exacttwo':return exactlytwo(state)
    if name=='noadjacent':return noadjacent(state)
    if name=='proof':return proof(state)
    if name=='expansion':return expansion(state)
    if name=='practice':return practice(state)
    raise KeyError(name)


def formula_picture(key):
    path=ROOT/'assets'/'comb03v2'/f'{key}.png'
    if not path.exists():raise FileNotFoundError(f'Missing Typst render: {path}')
    image=ImageMobject(str(path))
    if image.width>5.70:image.scale_to_fit_width(5.70)
    if image.height>.88:image.scale_to_fit_height(.88)
    image.move_to([RIGHT_PANEL,-1.08,0])
    return image


class COMB03(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb03_voice_manifest.json'
        if not manifest.exists():
            raise RuntimeError('Run python scripts/prepare_comb03_v2.py --voice off or --voice on first')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta.get('beats')!=len(BEATS):
            raise ValueError('Outdated COMB03 voice manifest')
        self.last_visual=None
        self.last_header=None
        self.last_details=None
        self.last_result=None
        self.last_footer=None
        self.canvas()

    def canvas(self):
        self.add(txt('SANG MATH / ĐẠI SỐ TỔ HỢP',-3.90,3.62,20,C['cyan'],True,6.15))
        self.add(txt('COMB03 / SƠ ĐỒ CÂY',4.26,3.62,19,C['muted'],True,5.25))
        self.add(segment(-6.82,3.31,6.82,3.31,C['line'],1.,1.1))
        self.add(panel(6.16,6.24,C['line'],C['panel']).move_to([LEFT,-.03,0]))
        self.add(panel(7.28,6.24,C['line'],C['panel']).move_to([RIGHT_PANEL,-.03,0]))
        self.add(segment(-6.82,-3.34,6.82,-3.34,C['line'],1.,1.1))

    def pieces(self,beat,i):
        chapter=txt(CHAPTER_LABELS[beat.section],RIGHT_PANEL,2.73,18,C['purple'],True,6.20)
        heading=txt(beat.heading,RIGHT_PANEL,2.17,26,C['gold'],True,6.20)
        head=VGroup(chapter,heading)
        details=VGroup(*[txt(s,RIGHT_PANEL,1.40-j*.52,23,C['text'],False,6.17)
                         for j,s in enumerate(beat.lines)])
        result=Group()
        if beat.formula:result.add(formula_picture(beat.formula))
        else:result.add(txt('QUAN SÁT  /  SUY LUẬN  /  KIỂM CHỨNG',
                            RIGHT_PANEL,-1.06,18,C['cyan'],False,6.1))
        rule=segment(.30,-1.83,6.16,-1.83,C['line'],1.,1.2)
        final=txt(beat.takeaway,RIGHT_PANEL,-2.44,22,C['green'],True,6.02)
        result.add(rule,final)
        foot=txt(f'{i+1:02d} / {len(BEATS)}',0,-3.72,16,C['muted'])
        return head,details,result,foot

    def focus_motion(self,beat,visual,focus):
        # Mathematical action: trace a complete tree path when appropriate.
        if (beat.section,beat.state) in {('growth',4),('proof',2),('exacttwo',2),('noadjacent',3)}:
            path=VMobject().set_points_as_corners([[*ROOT_POS,0],
                    [*P1['N'],0],[*P2['NS'],0],[*P3['NSN'],0]])
            dot=Dot([*ROOT_POS,0],radius=.075,color=C['green'])
            self.add(dot)
            self.play(MoveAlongPath(dot,path),run_time=3.0,rate_func=linear)
            self.remove(dot)
            return 3.0
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.08),run_time=2.8)
        return 2.8

    def perform(self,i,b):
        clip=self.meta['clips'].get(f'{i:03}',{})
        if clip.get('file'):
            path=ROOT/'voice'/clip['file']
            if not path.is_file():raise FileNotFoundError(path)
            self.add_sound(str(path))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.85)
        vis,focus=visual(b)
        head,details,result,foot=self.pieces(b,i)
        if i==0:
            self.play(FadeIn(vis),FadeIn(head),FadeIn(foot),run_time=1.65)
        else:
            self.play(FadeOut(self.last_visual),FadeIn(vis),
                      FadeOut(self.last_header),FadeIn(head),
                      FadeOut(self.last_details),FadeOut(self.last_result),
                      ReplacementTransform(self.last_footer,foot),run_time=1.65)
        visual_time=self.focus_motion(b,vis,focus)
        for j,line in enumerate(details):
            self.play(FadeIn(line,shift=.06*UP),run_time=1.10)
        self.play(FadeIn(result[0],shift=.07*UP),run_time=1.35)
        self.play(FadeIn(result[1]),FadeIn(result[2],shift=.07*UP),run_time=1.30)
        self.play(Circumscribe(result[2],color=C['green'],buff=.06),run_time=1.5)
        self.last_visual,self.last_header=vis,head
        self.last_details,self.last_result,self.last_footer=details,result,foot
        spent=1.65+visual_time+3*1.1+1.35+1.30+1.5
        if duration>spent:self.wait(duration-spent)

    def construct(self):
        for i,b in enumerate(BEATS):self.perform(i,b)
        self.play(FadeOut(self.last_visual),FadeOut(self.last_header),
                  FadeOut(self.last_details),FadeOut(self.last_result),
                  FadeOut(self.last_footer),run_time=.9)
        end=txt('ĐẾM ĐỦ / KHÔNG TRÙNG / ĐÚNG ĐIỀU KIỆN',0,.32,34,C['cyan'],True,12.)
        follow=txt('COMB04: THỨ TỰ CÓ QUAN TRỌNG KHÔNG?',0,-.48,23,C['gold'],True,12.)
        self.play(FadeIn(end),FadeIn(follow),run_time=1.6)
        self.wait(2.7)
