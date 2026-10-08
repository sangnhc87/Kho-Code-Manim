"""COMB07 V2 - Tổ hợp. Eight mathematically verified chapters (Manim + Typst).

Source of truth is comb07_lesson_data.py and comb07_beats.json.
Compile equations and (optionally) synthesize narration with prepare_comb07_v2.py.
"""
from __future__ import annotations
import json, sys
from itertools import combinations,permutations
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb07_lesson_data import BEATS,CHAPTER_LABELS

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.77; RX=3.18


def txt(value,x,y,size=18,color=None,bold=False,maxw=None):
    obj=Text(str(value),font=FONT,font_size=size,weight='BOLD' if bold else 'NORMAL',color=color or C['text'])
    if maxw and obj.width>maxw: obj.scale_to_fit_width(maxw)
    obj.move_to((x,y,0))
    return obj


def chip(value,x,y,col=None,w=.76,h=.62,size=21):
    bg=RoundedRectangle(width=w,height=h,corner_radius=.12,
        stroke_color=col or C['line'],stroke_width=2,
        fill_color=C['panel_alt'],fill_opacity=1)
    bg.move_to((x,y,0))
    fg=txt(value,x,y,size,C['text'],True,w-.08)
    return VGroup(bg,fg)


def group_card(name,x,y,col=None,w=1.03,h=.48):
    return chip(name,x,y,col,w,h,17)


def title(name):return txt(name,LX,2.48,19,C['cyan'],True,5.64)
def subline(s,y=-1.75,col=None):return txt(s,LX,y,17,col or C['muted'],False,5.78)
def base(s,col=None):return txt(s,LX,-2.66,16,col or C['gold'],True,5.79)

def pupils(g,names='ABCDE',chosen=(),y=1.35):
    m=len(names); step=5.22/max(m-1,1)
    items=[]
    for j,c in enumerate(names):
        x=-6.42+j*step
        col=C['green'] if c in chosen else C['cyan']
        t=chip(c,x,y,col,w=min(.70,step*.8),h=.66,size=23)
        g.add(t); items.append(t)
    return items


def team(g,name='ABC',y=-.20,color=None):
    outline=RoundedRectangle(width=5.10,height=1.31,corner_radius=.20,
        stroke_width=2,stroke_color=color or C['purple'],fill_color=C['panel_alt'],fill_opacity=.38)
    outline.move_to((LX,y,0));g.add(outline)
    cards=[]
    for j,c in enumerate(name):
        x=LX+(j-(len(name)-1)/2)*1.15
        card=chip(c,x,y,color or C['green'],.87,.86,27)
        g.add(card);cards.append(card)
    return cards


def intro_view(s):
    g=VGroup(title('CHỌN 3 TỪ 5 · KHÔNG CÓ VAI TRÒ'))
    pupils(g,chosen='ABC' if s not in (2,4) else 'ABD')
    names={0:'ABC',1:'BAC',2:'ABD',3:'ABC',4:'BAC',5:'ABC'}
    cards=team(g,names[s],-.20)
    g.add(subline(('ĐỘI: {A, B, C}','BA THẺ ĐỔI CHỖ, NHÓM KHÔNG ĐỔI',
        'THAY C BẰNG D: NHÓM KHÁC', 'DÃY CÓ THỨ TỰ ≠ NHÓM','THỨ TỰ KHÁC, THÀNH VIÊN GIỐNG','MỘT NHÓM CÓ BAO NHIÊU THỨ TỰ?')[s]))
    g.add(base('KHÔNG ĐẾM THỨ TỰ CHỌN'))
    return g,cards[min(s%3,2)]


def ordered_view(s):
    g=VGroup(title('SÁU THỨ TỰ CỦA CÙNG MỘT NHÓM'))
    perm=['ABC','ACB','BAC','BCA','CAB','CBA']
    boxes=[]
    for j,p in enumerate(perm):
        x=-5.58+(j%3)*1.82;y=1.42-(j//3)*.88
        card=group_card(p,x,y,C['gold'] if (s==0 and j==0) or (s>0 and j<=min(s+1,5)) else C['line'],1.48,.64)
        boxes.append(card);g.add(card)
    if s>=1:
        g.add(Arrow((-3.77,-.32,0),(-3.77,-.85,0),buff=0,stroke_width=3,color=C['purple']))
        g.add(group_card('NHÓM ABC',LX,-1.15,C['green'],2.6,.52))
    notes=['6 DÃY CÓ THỨ TỰ','6 DÃY → 1 NHÓM','3 × 2 × 1 = 6','60 DÃY ÷ 6 = 10 NHÓM',
           'CHỈ CHIA KHI KHÔNG XÉT THỨ TỰ','CHỈNH HỢP = TỔ HỢP × k!']
    g.add(subline(notes[s],-1.95,C['green'] if s>0 else C['gold']))
    g.add(base('MỖI NHÓM 3 NGƯỜI ↔ 6 THỨ TỰ'))
    return g,boxes[min(s,5)]


def groups_view(s):
    g=VGroup(title('TOÀN BỘ 10 NHÓM · MỖI NHÓM MỘT LẦN'))
    groups=[''.join(p) for p in combinations('ABCDE',3)]
    boxes=[]
    for j,p in enumerate(groups):
        x=-6.28+(j%5)*1.26; y=1.25-(j//5)*.82
        hl=('A' in p if s==1 else 'A' not in p if s==2 else j<=s+3)
        obj=group_card(p,x,y,C['green'] if hl else C['line'],1.11,.57)
        g.add(obj);boxes.append(obj)
    if s in (4,5):
        g.add(txt('CHỌN 3  ↔  BỎ LẠI 2',LX,-.68,22,C['gold'],True,5.8))
    elif s==1:g.add(txt('CÓ A: 6 NHÓM',LX,-.68,20,C['green'],True))
    elif s==2:g.add(txt('KHÔNG A: 4 NHÓM',LX,-.68,20,C['green'],True))
    else:g.add(txt('6 + 4 = 10 NHÓM',LX,-.68,20,C['gold'],True))
    g.add(subline('ABC · ABD · ABE · ACD · ACE · ADE · BCD · BCE · BDE · CDE',-1.78))
    g.add(base('KHÔNG THIẾU · KHÔNG TRÙNG'))
    return g,boxes[min(s,9)]


def general_view(s):
    g=VGroup(title('TỪ 5 CHỌN 3 → TỪ n CHỌN k'))
    cards=pupils(g,'ABCDE',chosen='ABC' if s!=4 else '')
    for j,(x,sym) in enumerate(zip([-5.92,-4.50,-3.08,-1.66],['n','n−1','···','n−k+1'])):
        g.add(group_card(sym,x,.02,C['cyan'],1.13,.71))
    g.add(txt('CÁC VỊ TRÍ CÓ THỨ TỰ',LX,-.65,18,C['muted'],True))
    texts=['CHỌN NHÓM k PHẦN TỬ','ĐẾM DÃY CÓ THỨ TỰ TRƯỚC',
           'MỖI NHÓM SINH k! DÃY','CHIA CHO k! ĐỂ BỎ THỨ TỰ',
           'CHỌN 0 HOẶC CHỌN TẤT CẢ','VÍ DỤ: n = 5, k = 3']
    g.add(subline(texts[s],-1.70,C['green']))
    g.add(base('0 ≤ k ≤ n · KHÔNG LẶP'))
    return g,cards[min(s,4)]


def symmetry_view(s):
    g=VGroup(title('CHỌN VÀ KHÔNG CHỌN · PASCAL'))
    names='ABCDEFG' if s in (0,1) else 'ABCDEF'
    chosen='AB' if s in (0,1) else 'ABC'
    items=pupils(g,names,chosen=chosen)
    if s<=1:
        g.add(txt('CHỌN 2',-5.12,.22,19,C['green'],True))
        g.add(txt('BỎ LẠI 5',-2.39,.22,19,C['gold'],True))
        g.add(subline('MỖI CẶP ↔ NĂM NGƯỜI CÒN LẠI',-1.53))
    else:
        case_a=VGroup(group_card('CÓ A',-5.18,.11,C['green'],2.05,.80),
                      group_card('10',-5.18,-.87,C['green'],1.20,.70))
        case_no=VGroup(group_card('KHÔNG A',-2.20,.11,C['gold'],2.05,.80),
                       group_card('10',-2.20,-.87,C['gold'],1.20,.70))
        g.add(case_a,case_no)
        g.add(subline('CÓ A HOẶC KHÔNG A: HAI NHÁNH RỜI NHAU',-1.75))
    g.add(base('CỘNG NHỮNG TRƯỜNG HỢP KHÔNG TRÙNG'))
    return g,items[min(s,len(items)-1)]


def constraint_view(s):
    g=VGroup(title('CHỌN 3 TRONG 6 · CẤM A VÀ B CÙNG ĐỘI'))
    allteams=[''.join(p) for p in combinations('ABCDEF',3)]
    objs=[];badcount=0
    for j,name in enumerate(allteams):
        bad=('A' in name and 'B' in name)
        if bad:badcount+=1
        x=-6.24+(j%5)*1.245;y=1.68-(j//5)*.67
        col=C['red'] if bad and s>=2 else C['green'] if s>=3 and not bad else C['line']
        obj=group_card(name,x,y,col,1.02,.52);g.add(obj);objs.append(obj)
    notes=['20 ĐỘI BAN ĐẦU','TÌM ĐỘI CÓ ĐỒNG THỜI A, B',
           '4 ĐỘI ĐỎ BỊ CẤM','20 − 4 = 16 ĐỘI','4 + 12 = 16 ĐỘI','BẮT BUỘC A, CẤM B: 10 ĐỘI']
    g.add(subline(notes[s],-1.64,C['green'] if s>=3 else C['gold']))
    g.add(base('BỘ ĐẾM: 20  →  16'))
    focus=objs[0] if s<2 else next(q for j,q in enumerate(objs) if 'A' in allteams[j] and 'B' in allteams[j])
    return g,focus


def captain_view(s):
    g=VGroup(title('ĐỘI 3 NGƯỜI · CHỌN ĐỘI TRƯỞNG'))
    items=pupils(g,'ABCDEFGH',chosen='ABC')
    cards=team(g,'ABC',-.14,C['green'])
    if s in (2,3,4,5):
        star=Star(n=5,outer_radius=.13,inner_radius=.055,fill_color=C['gold'],fill_opacity=1,stroke_width=0)
        star.move_to((cards[(s-2)%3].get_center()[0],.49,0))
        g.add(star)
        g.add(txt('TRƯỞNG NHÓM',LX,-1.14,18,C['gold'],True))
    notes=['CHỌN 3 NGƯỜI + 1 TRƯỞNG', 'CÓ 56 NHÓM',
           'MỖI NHÓM CÓ 3 CÁCH CHỌN TRƯỞNG',
           'CHỌN TRƯỞNG TRƯỚC: 8 CÁCH',
           'HAI CÁCH ĐẾM → CÙNG 168',
           'KHÔNG SẮP THỨ TỰ HAI THÀNH VIÊN THƯỜNG']
    g.add(subline(notes[s],-1.79,C['green'] if s in (2,4) else C['gold']))
    g.add(base('56 × 3 = 8 × 21 = 168'))
    return g,cards[(s-2)%3] if s>=2 else items[0]


def practice_view(s):
    g=VGroup(title('BÀI TẬP · TỰ NHẬN DIỆN PHÉP ĐẾM'))
    if s in (1,2):
        names='NNNNGGG'
        cards=[]
        for j,ch in enumerate(names):
            x=-6.2+j*.80
            color=C['cyan'] if ch=='N' else C['purple']
            obj=chip(f'{ch}{j+1}',x,1.33,color,.65,.67,18);g.add(obj);cards.append(obj)
    else:cards=pupils(g,'ABCDEF' if s==0 else 'ABCDE',chosen='ABC')
    note=['6 CHỌN 2 → 15 ĐỘI','ÍT NHẤT 1 NỮ: 35 − 4 = 31',
          'ĐÚNG 2 NAM VÀ 1 NỮ: 6 × 3 = 18',
          'THỨ TỰ CÓ TẠO KẾT QUẢ MỚI?',
          '5 NGƯỜI: TỔNG SỐ TẬP CON = 32',
          'TỔ HỢP = CHỌN, KHÔNG SẮP THỨ TỰ']
    g.add(txt(note[s],LX,-.28,19,C['green'],True,5.7))
    g.add(subline('THIẾT LẬP MÔ HÌNH, RỒI MỚI VIẾT CÔNG THỨC',-1.74))
    g.add(base('VIDEO 08: LỰA CHỌN PHƯƠNG PHÁP ĐẾM'))
    return g,cards[min(s,len(cards)-1)]


VIEWS={'intro':intro_view,'ordered':ordered_view,'groups':groups_view,
       'general':general_view,'symmetry':symmetry_view,'constraint':constraint_view,
       'captain':captain_view,'practice':practice_view}


def math_png(key):
    path=ROOT/'assets'/'comb07v2'/f'{key}.png'
    if not path.is_file():raise FileNotFoundError(f'Missing Typst PNG {path}. Run prepare_comb07_v2.py.')
    obj=ImageMobject(str(path));obj.scale_to_fit_width(min(obj.width,5.75))
    if obj.height>.75:obj.scale_to_fit_height(.75)
    obj.move_to((RX,-1.17,0));return obj


class COMB07(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb07_voice_manifest.json'
        if not path.exists():raise FileNotFoundError('Run scripts/prepare_comb07_v2.py first')
        self.meta=json.loads(path.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Narration manifest count mismatch')
        self.previous=None
        self.add(txt('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.88,3.62,19,C['cyan'],True,6.1))
        self.add(txt('COMB07  /  TỔ HỢP',4.30,3.62,18,C['muted'],True,4.2))
        self.add(Line((-6.85,3.31,0),(6.85,3.31,0),color=C['line'],stroke_width=1.2))
        for x,w in ((LX,6.18),(RX,7.18)):
            pane=RoundedRectangle(width=w,height=6.20,corner_radius=.17,
                stroke_width=1.35,stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1)
            pane.move_to((x,0,0));self.add(pane)
        self.add(Line((-6.85,-3.34,0),(6.85,-3.34,0),color=C['line'],stroke_width=1.2))

    def right(self,b,i):
        heads=VGroup(txt(CHAPTER_LABELS[b.section],RX,2.77,17,C['purple'],True,6.0),
                     txt(b.heading,RX,2.12,21,C['gold'],True,6.0))
        bullets=VGroup(*[txt('• '+line,RX,1.25-j*.59,18,C['text'],False,5.89) for j,line in enumerate(b.lines)])
        formula=math_png(b.formula) if b.formula else txt('QUAN SÁT  →  SUY LUẬN',RX,-1.15,17,C['cyan'],True)
        conclusion=VGroup(Line((.45,-1.74,0),(6.29,-1.74,0),stroke_width=1.2,color=C['line']),
                  txt(b.takeaway,RX,-2.35,19,C['green'],True,5.85))
        count=txt(f'{i+1:02d} / {len(BEATS)}',0,-3.69,15,C['muted'])
        return heads,bullets,formula,conclusion,count

    def beat(self,i,b):
        audio=self.meta['clips'][f'{i:03}']
        if audio.get('file'):
            mp3=ROOT/'voice'/audio['file']
            if not mp3.exists():raise FileNotFoundError(mp3)
            self.add_sound(str(mp3))
        budget=max(b.min_seconds,float(audio.get('duration',0))+.90)
        art,focus=VIEWS[b.section](b.state)
        h,lines,math,conclusion,counter=self.right(b,i)
        if self.previous is None:
            self.play(FadeIn(art),FadeIn(h),FadeIn(counter),run_time=1.05)
        else:
            olda,oldh,oldl,oldm,oldc,oldi=self.previous
            self.play(FadeOut(olda),FadeIn(art),FadeOut(oldh),FadeIn(h),
                FadeOut(oldl),FadeOut(oldm),FadeOut(oldc),
                ReplacementTransform(oldi,counter),run_time=1.05)
        extra=0.0
        # The core mathematical insight is genuinely animated, not simply narrated:
        # two students exchange places; then six orderings converge to one group.
        if b.section=='intro' and b.state==1:
            self.play(Swap(art[7],art[8]),run_time=1.4)
            self.play(Swap(art[7],art[8]),run_time=1.4)
            extra=2.8
        if b.section=='ordered' and b.state==1:
            moving=VGroup(*[art[j].copy() for j in range(1,7)])
            self.add(moving)
            self.play(*[q.animate.move_to((LX,-1.15,0)).scale(.3) for q in moving],run_time=2.25)
            self.play(FadeOut(moving),run_time=.45)
            extra=2.7
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.085),run_time=2.35)
        for item in lines:self.play(FadeIn(item,shift=.08*UP),run_time=1.56)
        self.play(FadeIn(math,shift=.08*UP),run_time=1.25)
        self.play(FadeIn(conclusion),run_time=1.05)
        self.play(Circumscribe(conclusion[-1],color=C['green'],buff=.14),run_time=1.20)
        spent=1.05+2.35+3*1.56+1.25+1.05+1.20+extra
        if budget>spent:self.wait(budget-spent)
        self.previous=(art,h,lines,math,conclusion,counter)

    def construct(self):
        for index,b in enumerate(BEATS):self.beat(index,b)
        self.play(*[FadeOut(p) for p in self.previous],run_time=1.0)
        end=VGroup(txt('TỔ HỢP · CHỌN KHÔNG XÉT THỨ TỰ',0,.38,32,C['cyan'],True,12.2),
             txt('VIDEO 08  /  TỔNG HỢP PHƯƠNG PHÁP ĐẾM',0,-.52,24,C['gold'],True,12.2))
        self.play(FadeIn(end),run_time=1.4)
        self.wait(2.8)
