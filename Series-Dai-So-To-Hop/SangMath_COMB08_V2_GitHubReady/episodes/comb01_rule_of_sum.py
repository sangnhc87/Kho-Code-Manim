"""SANG MATH / COMB01 v2: full-length rule of sum video.

Build: python scripts/prepare_comb01_v2.py --voice on
Render: manim -ql episodes/comb01_rule_of_sum.py COMB01

One beat = one synchronized voice clip + a purposeful visual state change.
Timing is controlled by the generated voice metadata, not by arbitrary sleeps.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comb01_lesson_data import BEATS, CHAPTER_LABELS
from series_config import PALETTE as C

config.background_color = C['bg']
config.frame_width = 14.222222
config.frame_height = 8.0

FONT = 'Noto Sans'
LX, RX = -3.84, 3.22


def text(s, size=24, color=None, bold=False, maxw=6.1):
    m = Text(str(s), font=FONT, font_size=size, color=color or C['text'],
             weight='BOLD' if bold else 'NORMAL')
    if maxw is not None and m.width > maxw:
        m.scale_to_fit_width(maxw)
    return m


def box(w,h,fill=None,stroke=None,r=0.14):
    return RoundedRectangle(width=w,height=h,corner_radius=r,
         fill_opacity=1, fill_color=fill or C['panel_alt'],
         stroke_width=1.2,stroke_color=stroke or C['line'])


def locate(m,x,y):
    m.move_to(np.array([x,y,0.0]))
    return m


def capsule(s,col,w=1.22,h=.51,size=21):
    bg=RoundedRectangle(width=w,height=h,corner_radius=.12,
        stroke_color=col,stroke_width=1.5,fill_color=col,fill_opacity=.22)
    return VGroup(bg, locate(text(s,size,maxw=w-.13),0,0))


def label_at(s,x,y,color=None,size=20,bold=False,maxw=5.4):
    return locate(text(s,size,color,bold,maxw),x,y)


def card(num,x,y,col=C['line'],fill=C['panel_alt'],w=.93,h=.72):
    r=box(w,h,fill,col,r=.11)
    t=text(str(num),23,C['text'],True,maxw=w-.12)
    return locate(VGroup(r,t),x,y)


def asset(name, scale_w=4.8):
    if not name:
        return None
    file=ROOT/'assets'/'comb01v2'/f'{name}.png'
    if not file.is_file():
        raise FileNotFoundError('Missing Typst formula: '+str(file)
                               +'\nRun scripts/prepare_comb01_v2.py before rendering.')
    m=ImageMobject(str(file))
    m.scale_to_fit_width(min(scale_w,m.width))
    if m.height>1.04:
        m.scale_to_fit_height(1.04)
    return m


def _roads(step):
    # Edge geometry is intentionally stable; selected group is spotlighted.
    base=VGroup()
    base.add(label_at('A',-6.15,-.12,C['text'],29,True),label_at('B',-1.44,-.12,C['text'],29,True))
    base.add(Dot([-5.83,-.10,0],radius=.11,color=C['text']),
             Dot([-1.76,-.10,0],radius=.11,color=C['text']))
    ys=[1.82,1.18,.54,-.85,-1.47]
    colors=[C['cyan']]*2+[C['gold']]*3
    for i,(y,col) in enumerate(zip(ys,colors)):
        is_focus=(step==1 and i<2) or (step==2 and i>=2) or (step==4)
        alpha=1 if step in (0,3,4) or is_focus else .20
        edge=CubicBezier([-5.80,-.10,0],[-4.55,y,0],[-2.92,y,0],[-1.79,-.10,0],
            stroke_color=col,stroke_width=5 if is_focus else 3,stroke_opacity=alpha)
        base.add(edge)
        middle=-4.50 if i%2==0 else -3.05
        base.add(label_at(('Xe '+str(i+1) if i<2 else 'Tàu '+str(i-1)),middle, y*.60-.04,col,17,maxw=1.28).set_opacity(alpha))
    if step>=3:
        base.add(label_at('Một chuyến đi = một tuyến',LX,-2.53,C['green'],20,True))
    return base


def _count(step):
    g=VGroup(label_at('NHÓM X · XE BUÝT',-4.2,1.86,C['cyan'],21,True),
             label_at('NHÓM Y · TÀU',-4.2,.26,C['gold'],21,True))
    for i in range(2):
        obj=capsule('Xe '+str(i+1),C['cyan'],1.60,.73,22)
        if step==2: obj.set_opacity(.18)
        g.add(locate(obj,-4.80+i*2.05,1.12))
    for i in range(3):
        obj=capsule('Tàu '+str(i+1),C['gold'],1.50,.71,21)
        if step==1: obj.set_opacity(.20)
        g.add(locate(obj,-5.60+i*1.70,-.62))
    if step>=3:
        g.add(label_at('X ∪ Y : 2 + 3 = 5',LX,-2.18,C['green'],25,True))
    else:
        g.add(label_at('Mỗi thẻ là một kết quả',LX,-2.18,C['muted'],20))
    return g


def _rule(step):
    g=VGroup()
    A=box(2.33,2.35,C['panel_alt'],C['cyan'])
    B=box(2.33,2.35,C['panel_alt'],C['gold'])
    g.add(locate(A,-5.20,.35),locate(B,-2.44,.35))
    g.add(label_at('PHƯƠNG ÁN A',-5.20,1.05,C['cyan'],20,True),
          label_at('PHƯƠNG ÁN B',-2.44,1.05,C['gold'],20,True),
          label_at('m cách',-5.20,.25,C['text'],31,True),
          label_at('n cách',-2.44,.25,C['text'],31,True))
    if step>0:
        g.add(label_at('Không có kết quả chung',LX,-1.51,C['green'],20,True))
    if step>1:
        g.add(label_at('m + n',LX,-2.25,C['cyan'],37,True))
    if step==4:
        g.add(label_at('ĐỦ   ·   KHÔNG TRÙNG',LX,2.10,C['gold'],21,True))
    return g


def _books(step):
    g=VGroup(label_at('4 CUỐN TOÁN',-4.2,1.78,C['cyan'],21,True),
             label_at('3 CUỐN VẬT LÍ',-4.2,-.21,C['gold'],21,True))
    for i in range(7):
        upper=i<4
        x=(-6.14+i*.99) if upper else (-5.80+(i-4)*1.44)
        y=.93 if upper else -1.10
        color=C['cyan'] if upper else C['gold']
        op=.19 if (step==1 and not upper) or (step==2 and upper) else 1.0
        cover=box(.74,1.20,color,C['line'])
        title=text(('T'+str(i+1)) if upper else ('L'+str(i-3)),22,C['text'],True,.59)
        g.add(locate(VGroup(cover,title),x,y).set_opacity(op))
    if step>=3:
        g.add(label_at('Chọn 1 cuốn: 4 + 3 = 7',LX,-2.52,C['green'],21,True))
    return g


def _overlap(step):
    g=VGroup()
    for n in range(1,13):
        x=-5.77+((n-1)%4)*1.31
        y=1.57-((n-1)//4)*1.13
        if step==0: co=C['line']; fill=C['panel_alt']
        elif step==1: co=C['cyan'] if n%2==0 else C['line']; fill=C['panel_alt']
        elif step==2: co=C['gold'] if n%3==0 else C['line']; fill=C['panel_alt']
        else:
            co=C['red'] if n%6==0 else C['cyan'] if n%2==0 else C['gold'] if n%3==0 else C['line']
            fill=C['panel_alt']
        g.add(card(n,x,y,co,fill))
    if step>=3:
        g.add(label_at('6 và 12: thuộc cả hai nhóm',LX,-2.25,C['red'],20,True))
    if step>=4:
        g.add(label_at('6 + 4 − 2 = 8',LX,-2.78,C['green'],23,True))
    return g


def _distinct(step):
    g=VGroup()
    for n in range(1,21):
        x=-6.01+((n-1)%5)*1.15
        y=1.83-((n-1)//5)*.97
        high=(n%2==1 and step in (1,3,4)) or (n%4==0 and step in (2,3,4))
        col=(C['cyan'] if n%2==1 else C['gold']) if high else C['line']
        g.add(card(n,x,y,col,w=.81,h=.65))
    if step>=3:
        g.add(label_at('10 số lẻ + 5 bội của 4 = 15',LX,-2.48,C['green'],19,True))
    return g


def _compare(step):
    g=VGroup(label_at('ÁO',-5.31,1.92,C['cyan'],22,True),label_at('MŨ',-2.60,1.92,C['gold'],22,True))
    for i in range(3):
        g.add(locate(capsule('A'+str(i+1),C['cyan'],1.11,.70,21),-5.35,1.12-i*.95))
    for i in range(2):
        g.add(locate(capsule('M'+str(i+1),C['gold'],1.11,.70,21),-2.55,.89-i*1.1))
    if step in (0,1,3,4):
        g.add(label_at('HOẶC  →  5 món riêng lẻ',LX,-2.46,C['cyan'],21,True))
    if step==2:
        g.add(label_at('VÀ  →  6 cặp áo–mũ',LX,-2.46,C['green'],21,True))
    return g


def _quiz(step):
    if step<2:
        g=VGroup(label_at('5 QUÀ A',-4.80,1.79,C['cyan'],20,True),
                 label_at('2 QUÀ B',-4.80,-.15,C['gold'],20,True))
        for i in range(5):
            g.add(locate(capsule('A'+str(i+1),C['cyan'],.87,.65,18),-6.02+i*1.05,.96))
        for i in range(2):
            g.add(locate(capsule('B'+str(i+1),C['gold'],1.01,.67,20),-5.34+i*2.60,-1.05))
        if step==1:
            g.add(label_at('5 + 2 = 7',LX,-2.48,C['green'],30,True))
        return g
    g=VGroup()
    for n in range(1,16):
        x=-5.87+((n-1)%5)*1.19
        y=1.58-((n-1)//5)*1.16
        if step>=3:
            color=C['red'] if n==15 else C['cyan'] if n%3==0 else C['gold'] if n%5==0 else C['line']
        else: color=C['line']
        g.add(card(n,x,y,color,w=.86,h=.70))
    if step>=3:
        g.add(label_at('5 + 3 − 1 = 7',LX,-2.28,C['green'],23,True))
    if step==4:
        g.add(label_at('ĐỦ  ·  KHÔNG TRÙNG',LX,-2.83,C['gold'],19,True))
    return g


VISUALS = {'roads':_roads,'count':_count,'rule':_rule,'books':_books,
           'overlap':_overlap,'distinct':_distinct,'compare':_compare,'quiz':_quiz}


class COMB01(Scene):
    def setup(self):
        self.audio_info={}
        manifest=ROOT/'voice'/'comb01_voice_manifest.json'
        if manifest.exists():
            self.audio_info=json.loads(manifest.read_text(encoding='utf-8')).get('clips',{})
        self.chapter=None
        self.lh=None
        self.rh=None
        self.strip=None
        self.visual=None
        self.announced=0.0
        self.canvas()

    def canvas(self):
        title=label_at('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.85,3.60,C['cyan'],22,True)
        episode=label_at('COMB01  ·  QUY TẮC CỘNG',4.11,3.60,C['muted'],21)
        line=Line([-6.89,3.28,0],[6.89,3.28,0],stroke_color=C['line'])
        lhs=locate(box(6.14,6.26,C['panel']),LX,-.04)
        rhs=locate(box(7.24,6.26,C['panel']),RX,-.04)
        foot=Line([-6.84,-3.34,0],[6.84,-3.34,0],stroke_color=C['line'])
        self.add(title,episode,line,lhs,rhs,foot)
        self.footer=label_at('SANG MATH · HỌC BẰNG HÌNH ĐỘNG',0,-3.71,C['muted'],18)
        self.add(self.footer)

    def panel(self,beat):
        g=Group()
        number=CHAPTER_LABELS[beat.section]
        g.add(label_at(number,RX,2.61,C['purple'],20,True,6.20))
        g.add(label_at(beat.heading,RX,2.07,C['gold'],29,True,6.40))
        for i,s in enumerate(beat.lines):
            g.add(label_at(s,RX,1.32-i*.50,C['text'],25,False,6.32))
        if beat.formula:
            a=asset(beat.formula,5.16)
            locate(a,RX,-.94)
            g.add(a)
        else:
            g.add(label_at('QUAN SÁT  ·  SUY LUẬN  ·  KẾT LUẬN',RX,-.94,C['cyan'],18,False,6.0))
        g.add(Line([.20,-1.87,0],[6.27,-1.87,0],stroke_color=C['line']))
        # Important: at most one takeaway on the right and never in the diagram.
        takeaway=text(beat.takeaway,23,C['green'],True,5.95)
        if takeaway.height>.82:
            takeaway.scale_to_fit_height(.82)
        g.add(locate(takeaway,RX,-2.49))
        return g

    def caption(self,beat,idx):
        # Bottom bar carries the current instructional question, not full narration.
        t=f'{idx+1:02d}/{len(BEATS):02d}   •   {beat.takeaway}'
        return label_at(t,0,-3.72,C['muted'],18,False,12.1)

    def construct(self):
        for i,beat in enumerate(BEATS):
            self.perform(i,beat)
        self.play(FadeOut(self.visual),FadeOut(self.rh),run_time=1.15)
        finish=label_at('ĐẾM ĐỦ · KHÔNG ĐẾM TRÙNG',0,-.18,C['cyan'],37,True,11.8)
        self.play(FadeIn(finish,scale=.9),run_time=2.2)
        self.wait(2.8)

    def focus(self,visual,beat):
        """Only spotlight mathematical objects being counted in this beat."""
        sec,step=beat.section,beat.step
        indices=[]
        if sec=='roads':
            indices=([4,6] if step==1 else [8,10,12] if step==2 else [4,6,8,10,12])
        elif sec=='count':
            indices=[2,3] if step==1 else [4,5,6] if step==2 else list(range(2,7))
        elif sec=='rule':
            indices=[0] if step==1 else [0,1]
        elif sec=='books':
            indices=list(range(2,6)) if step==1 else list(range(6,9)) if step==2 else list(range(2,9))
        elif sec=='overlap':
            indices=([i for i in range(12) if (i+1)%2==0] if step==1
                     else [i for i in range(12) if (i+1)%3==0] if step==2
                     else [5,11] if step==3
                     else [i for i in range(12) if (i+1)%2==0 or (i+1)%3==0])
        elif sec=='distinct':
            indices=([i for i in range(20) if (i+1)%2==1] if step==1
                     else [i for i in range(20) if (i+1)%4==0] if step==2
                     else [i for i in range(20) if (i+1)%2==1 or (i+1)%4==0])
        elif sec=='compare':
            indices=list(range(2,5)) if step==1 else [5,6] if step==2 else list(range(2,7))
        elif sec=='quiz':
            indices=list(range(2,9)) if step<2 else [14] if step==3 else list(range(15))
        indices=[i for i in indices if i < len(visual)]
        return VGroup(*(visual[i] for i in indices)) if indices else visual

    def perform(self,i,beat):
        data=self.audio_info.get(f'{i:03}',{})
        filename=data.get('file')
        if filename:
            full=ROOT/'voice'/filename
            if not full.is_file():
                raise RuntimeError('Narration manifest references missing file: '+str(full))
            self.add_sound(str(full))
        duration=max(float(beat.min_seconds),float(data.get('duration',0))+0.9)
        new_visual=VISUALS[beat.section](beat.step)
        new_panel=self.panel(beat)
        new_caption=self.caption(beat,i)
        # The three problem facts arrive before formula and takeaway, never all at once.
        intro=Group(*list(new_panel)[:5],new_panel[6])
        if self.visual is None:
            self.play(FadeIn(new_visual,shift=.12*UP),FadeIn(intro,shift=.10*RIGHT),
                      ReplacementTransform(self.footer,new_caption),run_time=1.7)
        else:
            self.play(FadeOut(self.visual),FadeIn(new_visual),
                      FadeOut(self.rh),FadeIn(intro),
                      ReplacementTransform(self.footer,new_caption),run_time=1.6)
        self.visual=new_visual
        self.rh=new_panel
        self.footer=new_caption
        target=self.focus(new_visual,beat)
        if beat.section=='roads' and beat.step in (1,2,4):
            # Meaningful motion: watch a traveler actually follow one option.
            path_index=4 if beat.step==1 else 8 if beat.step==2 else 12
            path=new_visual[path_index]
            traveler=Dot(path.get_start(),radius=.098,color=C['green'])
            self.add(traveler)
            self.play(MoveAlongPath(traveler,path),run_time=3.8,rate_func=linear)
            self.remove(traveler)
        else:
            self.play(Indicate(target,scale_factor=1.022,color=C['cyan']),run_time=3.8)
        self.play(FadeIn(new_panel[5],shift=.08*UP),FadeIn(new_panel[7],shift=.08*UP),run_time=2.0)
        self.play(Circumscribe(new_panel[7],color=C['gold'],buff=.11),run_time=2.7)
        used=(1.7 if i==0 else 1.6)+3.8+2.0+2.7
        if duration>used:
            self.wait(duration-used)
        self.announced+=duration
