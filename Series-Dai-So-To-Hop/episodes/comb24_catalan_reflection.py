"""COMB24 -- Catalan numbers, Dyck paths, reflection and Narayana.
A rigorous two-column Manim lesson, paced beat-by-beat by its voice manifest.
Run scripts/prepare_comb24_v2.py before rendering this Scene.
"""
from __future__ import annotations
import json,sys,math
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb24_lesson_data import (BEATS,CHAPTER_LABELS,catalan,dyck_words,
    reflect_bad_prefix,peak_count,narayana)
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
LX=-3.56
RX=3.18
FONT='Noto Sans'

def txt(s,x,y,size=17,color=None,bold=False,limit=None):
    t=Text(str(s),font=FONT,font_size=size,color=color or C['text'],
           weight='BOLD' if bold else 'NORMAL')
    if limit and t.width>limit:t.scale_to_fit_width(limit)
    if t.height>.57:t.scale_to_fit_height(.57)
    t.move_to((x,y,0))
    return t

def tag(s,x,y,active=False,width=.78):
    shape=RoundedRectangle(width=width,height=.46,corner_radius=.07,
      stroke_width=1.4,stroke_color=C['gold'] if active else C['line'],
      fill_opacity=1,fill_color=C['panel_alt']).move_to((x,y,0))
    return VGroup(shape,txt(s,x,y,14,C['gold'] if active else C['text'],active,width-.12))

def path_group(word,cx,cy,scale=.34,color=None,mark_peaks=False):
    """Draw a true step-by-step U/D lattice path, with horizontal spacing."""
    h=0;pts=[(0,0)]
    for letter in word:
        h+=1 if letter=='U' else -1
        pts.append((len(pts),h))
    mid=len(word)/2
    g=VGroup()
    baseline=Line((cx-mid*scale,cy,0),(cx+mid*scale,cy,0),
                  stroke_width=1.3,stroke_color=C['line'])
    g.add(baseline)
    for i in range(len(word)):
        x1=cx+(i-mid)*scale;y1=cy+pts[i][1]*scale
        x2=cx+(i+1-mid)*scale;y2=cy+pts[i+1][1]*scale
        bad=min(pts[i][1],pts[i+1][1])<0
        edge=Line((x1,y1,0),(x2,y2,0),
                  stroke_width=3.3,stroke_color=C['red'] if bad else (color or C['cyan']))
        g.add(edge)
        if mark_peaks and i<len(word)-1 and word[i:i+2]=='UD':
            dot=Dot((x2,y2,0),radius=.065,color=C['gold'])
            g.add(dot)
    return g

def model(section,state):
    """Live geometry that changes across each six-beat conceptual chapter."""
    g=VGroup();focus=None
    headings={
      'parentheses':'DÃY NGOẶC · TIỀN TỐ HỢP LỆ',
      'dyck':'ĐƯỜNG ĐI DYCK · KHÔNG ÂM',
      'reflection':'PHẢN XẠ Ở LẦN VI PHẠM ĐẦU',
      'formula':'CATALAN · TỔNG TRỪ PHẦN SAI',
      'bijections':'SONG ÁNH · CÙNG MỘT CẤU TRÚC',
      'recurrence':'CATALAN · PHÂN RÃ & TRUY HỒI',
      'ballot':'BÀI TOÁN LÁ PHIẾU',
      'narayana':'NARAYANA · ĐẾM ĐỈNH CỦA DYCK'
    }
    g.add(txt(headings[section],LX,2.68,15,C['cyan'],True,6.0))
    if section=='parentheses':
        paths=dyck_words(3)
        # One detailed representative plus five cards labelled by actual paths.
        display=paths[state%5]
        p=path_group(display,LX,.55,.52,mark_peaks=True)
        g.add(p)
        g.add(txt('ĐỘ CAO KHÔNG ÂM',LX,1.87,15,C['green'],True))
        for i,w in enumerate(paths):
            card=tag(w,LX-1.94+(i%3)*1.94,-.94-(i//3)*.70,
                     active=w==display,width=1.76)
            g.add(card)
            if w==display:focus=card
        g.add(txt('5 DÃY ĐÚNG VỚI 3 CẶP NGOẶC',LX,-2.55,14,C['muted'],True,5.8))
    elif section=='dyck':
        paths=dyck_words(3)
        for i,w in enumerate(paths):
            px=LX-1.43+(i%2)*2.86;py=1.40-(i//2)*1.28
            card=path_group(w,px,py,.26,C['gold'] if i==state%5 else C['cyan'])
            g.add(card)
            if i==state%5:focus=card
            g.add(txt(w,px,py-.45,12,C['muted']))
        g.add(txt('U: LÊN  /  D: XUỐNG',LX,-2.64,14,C['green'],True))
    elif section=='reflection':
        original='UDDUUD'
        flipped=reflect_bad_prefix(original)
        g.add(txt('ĐƯỜNG SAI: '+original,LX,1.95,15,C['red'],True))
        top=path_group(original,LX,1.10,.43)
        g.add(top)
        g.add(txt('PHẢN XẠ TIỀN TỐ   ↧',LX,.18,15,C['gold'],True))
        bottom=path_group(flipped,LX,-.91,.43,C['green'])
        g.add(bottom)
        g.add(txt('ĐƯỜNG MỚI: '+flipped,LX,-1.85,15,C['green'],True))
        g.add(txt('U: 4  ·  D: 2  ·  ĐỘ CAO CUỐI: 2',LX,-2.54,13,C['muted'],True))
        focus=top if state<3 else bottom
    elif section=='formula':
        # Show a true partition of all 20 balanced six-step words.
        paths=dyck_words(3);good=set(paths)
        from itertools import combinations
        words=[]
        for loc in combinations(range(6),3):
            words.append(''.join('U' if i in loc else 'D' for i in range(6)))
        for k,w in enumerate(words):
            col=k%5;row=k//5
            x=LX-2.26+col*1.13;y=1.78-row*.91
            valid=w in good
            focus_now=(valid if state%2==0 else not valid) and k in (0,1,2,3,4,5,6,7,8,9)
            chip=tag(w,x,y,active=focus_now,width=1.04)
            chip[0].set_stroke(C['green'] if valid else C['red'],width=1.5)
            g.add(chip)
            if focus_now:focus=chip
        g.add(txt('20 TỔNG  =  5 HỢP LỆ  +  15 SAI',LX,-2.55,14,C['green'],True,6))
    elif section=='bijections':
        # Geometrically faithful convex polygon and non-crossing diagonals.
        n=5 if state<3 else 6
        radius=1.75;center=(LX,.05)
        pts=[]
        for i in range(n):
            ang=math.pi/2+2*math.pi*i/n
            pts.append((center[0]+radius*math.cos(ang),center[1]+radius*math.sin(ang),0))
        lines=VGroup(*[Line(pts[i],pts[(i+1)%n],stroke_color=C['cyan'],stroke_width=2.4) for i in range(n)])
        g.add(lines)
        diagonals_5=[[(0,2),(0,3)],[(0,2),(2,4)],[(0,3),(1,3)],[(1,3),(1,4)],[(1,4),(2,4)]]
        chosen=diagonals_5[state%3] if n==5 else [(0,2),(0,3),(0,4)]
        selected=VGroup(*[Line(pts[i],pts[j],stroke_color=C['gold'],stroke_width=3.0) for i,j in chosen])
        g.add(selected);focus=selected
        for i,pos in enumerate(pts):
            g.add(txt(chr(65+i),pos[0]*.83+LX*.17,pos[1]*1.09,12,C['muted']))
        g.add(txt(f'{n} ĐỈNH   ·   CATALAN {n-2}: {catalan(n-2)}',LX,-2.55,14,C['green'],True))
    elif section=='recurrence':
        for k in range(6):
            col=k%3;row=k//3
            x=LX-1.78+col*1.80;y=1.67-row*.88
            node=tag(f'C{k} = {catalan(k)}',x,y,active=k==state,width=1.63)
            g.add(node)
            if k==state:focus=node
        g.add(txt('C4 = C0·C3 + C1·C2 + C2·C1 + C3·C0',LX,-.42,14,C['gold'],True,5.92))
        g.add(txt('= 5 + 2 + 2 + 5 = 14',LX,-1.13,18,C['green'],True))
        g.add(txt('PHÂN RÃ:  ( A ) B',LX,-2.28,16,C['cyan'],True))
    elif section=='ballot':
        samples=['UUUUDUDD','UUDUUDUD','UDUUDUUD','UUUDUUDD','UUDUDUUD','UDUDUUUD']
        word=samples[state]
        # All examples 5 U 3 D except some samples? enforce rather than misrepresent.
        if word.count('U')!=5 or word.count('D')!=3:
            word='UUUDUDUD'
        g.add(txt('A = U   |   B = D',LX,1.97,17,C['cyan'],True))
        traj=path_group(word,LX,.43,.54,mark_peaks=True)
        g.add(traj);focus=traj
        g.add(txt('5 PHIẾU A   ·   3 PHIẾU B',LX,-1.22,16,C['gold'],True))
        g.add(tag('KHÔNG THUA: 28',LX,-1.85,active=state<3,width=2.70))
        g.add(tag('DẪN TRƯỚC: 14',LX,-2.50,active=state>=3,width=2.70))
    elif section=='narayana':
        samples=[w for w in dyck_words(6) if peak_count(w)==3]
        word=samples[(state*7)%len(samples)]
        traj=path_group(word,LX,.17,.43,C['cyan'],mark_peaks=True)
        g.add(traj);focus=traj
        g.add(txt('ĐƯỜNG DYCK BẬC 6',LX,2.04,17,C['cyan'],True))
        g.add(txt(word,LX,-1.35,16,C['muted'],True,5.9))
        g.add(txt('●  BA ĐỈNH ĐƯỢC ĐÁNH DẤU VÀNG',LX,-1.97,14,C['gold'],True,5.9))
        g.add(txt('N(6, 3) = 50   |   C6 = 132',LX,-2.63,15,C['green'],True))
    if focus is None:focus=g[1] if len(g)>1 else g
    return g,focus

def formula_png(key):
    path=ROOT/'assets'/'comb24v2'/f'{key}.png'
    if not path.exists():raise FileNotFoundError(f'Compile with prepare_comb24_v2.py first: {path}')
    img=ImageMobject(str(path))
    if img.width>5.76:img.scale_to_fit_width(5.76)
    if img.height>1.17:img.scale_to_fit_height(1.17)
    img.move_to((RX,-1.29,0))
    return img

class COMB24(Scene):
    def setup(self):
        manifest=ROOT/'voice'/'comb24_voice_manifest.json'
        if not manifest.exists():raise FileNotFoundError('Prepare manifest before rendering COMB24')
        self.meta=json.loads(manifest.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Voice beat count mismatch')
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',LX,3.61,16,C['cyan'],True,5.9))
        self.add(txt('COMB24 / CATALAN VÀ PHẢN XẠ',RX,3.61,15,C['muted'],True,5.8))
        self.add(Line((-6.91,3.32,0),(6.91,3.32,0),stroke_color=C['line'],stroke_width=1))
        for x,w in ((LX,6.24),(RX,6.40)):
            self.add(RoundedRectangle(width=w,height=6.13,corner_radius=.13,
                fill_color=C['panel'],fill_opacity=1,stroke_color=C['line'],stroke_width=1).move_to((x,0,0)))
        self.previous=None
    def beat(self,index,b):
        clip=self.meta['clips'][f'{index:03}']
        seconds=max(b.min_seconds,float(clip.get('duration',0))+.85)
        if clip.get('file'):self.add_sound(str(ROOT/'voice'/clip['file']))
        diagram,focus=model(b.section,b.state)
        heading=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.75,13,C['purple'],True,5.8),
                       txt(b.heading,RX,2.18,19,C['gold'],True,5.8))
        points=VGroup(*[txt('• '+line,RX,1.41-j*.65,15,C['text'],False,5.8)
                        for j,line in enumerate(b.lines)])
        formula=formula_png(b.formula)
        note=VGroup(Line((.27,-2.00,0),(6.34,-2.00,0),color=C['line']),
                    txt(b.takeaway,RX,-2.49,14,C['green'],True,5.8))
        marker=txt(f'{index+1:02d} / 48',0,-3.57,13,C['muted'],True)
        elapsed=0.0
        if self.previous:
            a,h,p,f,n,num=self.previous
            self.play(FadeOut(a),FadeOut(h),FadeOut(p),FadeOut(f),FadeOut(n),
                      ReplacementTransform(num,marker),FadeIn(diagram),FadeIn(heading),run_time=1.3)
        else:
            self.play(FadeIn(diagram),FadeIn(heading),FadeIn(marker),run_time=1.3)
        elapsed+=1.3
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.025),run_time=1.50)
        elapsed+=1.5
        for p in points:
            self.play(FadeIn(p,shift=UP*.05),run_time=.93)
            elapsed+=.93
        self.play(FadeIn(formula,shift=UP*.05),run_time=1.28)
        self.play(FadeIn(note),run_time=.63)
        elapsed+=1.91
        if seconds-elapsed>7:
            rest=(seconds-elapsed-1.30)/2
            self.wait(rest)
            self.play(Indicate(focus,color=C['cyan'],scale_factor=1.02),run_time=1.3)
            elapsed+=rest+1.3
        if seconds>elapsed:self.wait(seconds-elapsed)
        self.previous=(diagram,heading,points,formula,note,marker)
    def construct(self):
        for index,b in enumerate(BEATS):self.beat(index,b)
        if self.previous:self.play(*[FadeOut(x) for x in self.previous],run_time=1.0)
        self.play(FadeIn(txt('CATALAN  ·  DYCK  ·  NGUYÊN LÝ PHẢN XẠ',0,.48,22,C['cyan'],True,12)),run_time=1.2)
        self.play(FadeIn(txt('SONG ÁNH   →   TRUY HỒI   →   NARAYANA',0,-.47,17,C['gold'],True,12)),run_time=.8)
        self.wait(2.2)
