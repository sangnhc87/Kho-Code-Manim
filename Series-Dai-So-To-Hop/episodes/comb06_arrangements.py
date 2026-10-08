"""Sang Math COMB06 V2: arrangements (ordered selection without replacement).

Scene COMB06. Prepare Typst and audio first with scripts/prepare_comb06_v2.py.
Left pane visual reasoning; right pane Vietnamese statements and verified Typst maths.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb06_lesson_data import BEATS, CHAPTER_LABELS

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.77
RX=3.18


def label(s,x,y,size=19,color=None,bold=False,maxw=5.62):
    t=Text(str(s),font=FONT,font_size=size,weight='BOLD' if bold else 'NORMAL',color=color or C['text'])
    if maxw and t.width>maxw:t.scale_to_fit_width(maxw)
    t.move_to([x,y,0]);return t


def token(s,x,y,col=None,w=.77,h=.72,size=22,opacity=1):
    box=RoundedRectangle(width=w,height=h,corner_radius=.13,
         stroke_width=2,stroke_color=col or C['line'],
         fill_color=C['panel_alt'],fill_opacity=1)
    box.move_to([x,y,0])
    t=label(s,x,y,size,C['text'],True,w-.10)
    out=VGroup(box,t)
    out.set_opacity(opacity)
    return out


def heading(s):return label(s,LX,2.48,18,C['cyan'],True,5.70)
def info(s,y=-1.72,col=None):return label(s,LX,y,17,col or C['muted'],False,5.74)
def footer(s,col=None):return label(s,LX,-2.67,17,col or C['gold'],True,5.75)


def candidates(g,people='ABCDEF',active=None,y=1.36):
    result=[]
    step=5.05/max(len(people)-1,1)
    for j,ch in enumerate(people):
        t=token(ch,-6.29+j*step,y,C['cyan'] if active is None or ch in active else C['inactive'],.73,.66,22,1.0 if active is None or ch in active else .47)
        g.add(t);result.append(t)
    return result


def role_row(g,roles=('NHẤT','NHÌ','BA'),names=('A','B','C'),high=-1,ban_first=False):
    positions=(-5.73,-3.79,-1.85)
    objects=[]
    for i,(x,name,role) in enumerate(zip(positions,names,roles)):
        color=C['red'] if ban_first and i==0 else C['gold'] if i==high else C['green'] if name!='?' else C['line']
        card=token(name,x,-.38,color,1.22,.92,28)
        g.add(card)
        g.add(label(role,x,-1.15,15,C['muted'],True,1.61))
        objects.append(card)
    return objects


def intro_view(s):
    g=VGroup(heading('SÁU HỌC SINH · BA GIẢI THƯỞNG'))
    candidates(g)
    names=['ABC','BAC','A?C','???','AAC','ABC'][s]
    roles=role_row(g,names=tuple(names),high=s%3)
    if s==4:
        g.add(label('LẶP NGƯỜI!',-3.79,.36,19,C['red'],True))
    elif s==1:
        g.add(label('A ↔ B: GIẢI THƯỞNG ĐỔI!',LX,.39,17,C['gold'],True))
    elif s==3:
        g.add(label('6 lựa chọn cho giải Nhất',LX,.40,18,C['cyan'],True))
    else:g.add(info('Điền ba vị trí có vai trò khác nhau',.42))
    g.add(footer('MỘT NGƯỜI KHÔNG NHẬN HAI GIẢI'))
    return g,roles[min(s%3,2)]


def slots_view(s):
    g=VGroup(heading('MỖI LẦN CHỌN, BỚT MỘT NGƯỜI'))
    used=min(s+1,3)
    candidates(g,active='ABCDEF'[used:])
    names=tuple('ABC'[i] if i<used else '?' for i in range(3))
    roles=role_row(g,names=names,high=min(s,2))
    numbers=('6','5','4')
    for i,num in enumerate(numbers):
        x=(-5.73,-3.79,-1.85)[i]
        g.add(label(num if i<used else '·',x,.43,28,C['gold'] if i<used else C['muted'],True,.8))
    if s==3:g.add(info('Một kết quả ↔ một bộ ba (A, B, C)',-1.72,C['green']))
    elif s==4:g.add(info('(A, B, C) KHÁC (B, A, C)',-1.72,C['gold']))
    elif s==5:g.add(info('Không xếp tiếp ba học sinh còn lại',-1.72))
    else:g.add(info('Mọi nhánh còn cùng số lựa chọn',-1.72))
    g.add(footer('6 × 5 × 4 = 120 KẾT QUẢ',C['green']))
    return g,roles[min(s,2)]


def tree_view(s):
    g=VGroup(heading('NHÁNH CHỌN · KHÔNG HOÀN LẠI'))
    origin=[-6.20,0,0]
    g.add(Dot(origin,color=C['cyan'],radius=.10))
    x1=-5.06
    first=[]
    for i,ch in enumerate('ABCDEF'):
        y=1.83-i*.57
        color=C['gold'] if (s==i or (s>=2 and i==0)) else C['line']
        g.add(Line(origin,[x1-.36,y,0],color=color,stroke_width=2))
        t=token(ch,x1,y,C['cyan'] if i==0 else C['line'],.58,.37,15)
        g.add(t);first.append(t)
    y0=first[0].get_center()[1]
    for i,ch in enumerate('BCDEF'):
        y=1.55-i*.40
        g.add(Line([x1+.35,y0,0],[-3.51,y,0],color=C['line'],stroke_width=1.5))
        g.add(token(ch,-3.27,y,C['gold'] if i==0 else C['line'],.52,.30,14))
    g.add(Line([-2.93,1.55,0],[-1.90,1.55,0],color=C['green'],stroke_width=2.5))
    g.add(label('×4',-1.46,1.55,17,C['green'],True))
    if s==3:g.add(label('A → A',-2.35,-1.35,18,C['red'],True))
    else:g.add(info('Mỗi cặp đầu sinh đúng 4 lựa chọn',-1.83))
    g.add(footer('6 NHÁNH × 5 NHÁNH × 4 LÁ = 120'))
    return g,first[0]


def general_view(s):
    g=VGroup(heading('TỪ n PHẦN TỬ CHỌN k VỊ TRÍ'))
    letters=('1','2','3','···','k','')
    values=('n','n−1','n−2','···','n−k+1','')
    selected=[]
    for i in range(5):
        x=-6.21+i*1.21
        t=token(letters[i],x,.54,C['gold'] if (i==min(s,4)) else C['cyan'],.92,.72,17)
        g.add(t);selected.append(t)
        g.add(label(values[i],x,-.48,18,C['gold'] if i==min(s,4) else C['text'],True,1.15))
    if s==4:g.add(info('k = 0: chỉ có dãy rỗng',-1.58,C['green']))
    elif s==5:g.add(info('k = n: trở thành hoán vị',-1.58,C['green']))
    else:g.add(info('Chỉ lấy đúng k thừa số đầu',-1.58))
    g.add(footer('n ≥ k ≥ 0 • KHÔNG CHỌN LẠI'))
    return g,selected[min(s,4)]


def restriction_view(s):
    g=VGroup(heading('BẢY NGƯỜI · BA CHỨC VỤ'))
    top=candidates(g,people='ABCDEFG')
    roles=role_row(g,roles=('TRƯỞNG','PHÓ','THƯ KÝ'),names=('B','A','C') if s==4 else ('B','C','D'),high=0)
    if s in (0,3):
        g.add(label('A KHÔNG LÀM TRƯỞNG',LX,.37,19,C['red'],True))
        if s==3:g.add(Cross(top[0],stroke_color=C['red'],stroke_width=3).scale(.8))
    else:g.add(label('TRỰC TIẾP ↔ PHẦN BÙ',LX,.37,18,C['gold'],True))
    note={0:'Trưởng: 6 • Phó: 6 • Thư ký: 5',1:'6 × 6 × 5 = 180',2:'210 − 30 = 180',3:'Chỉ cấm A ở vị trí trưởng',4:'A làm phó hoặc thư ký: 60',5:'Loại A khỏi mọi vai trò: 120'}[s]
    g.add(info(note,-1.76,C['green'] if s!=3 else C['red']))
    g.add(footer('KIỂM TRA ĐIỀU KIỆN Ở TỪNG VỊ TRÍ'))
    return g,roles[0]


def digits_view(s):
    g=VGroup(heading('LẬP SỐ TỪ 0, 1, 2, 3, 4'))
    top=[]
    for i,ch in enumerate('01234'):
        obj=token(ch,-6.05+i*1.16,1.35,C['red'] if ch=='0' else C['cyan'],.79,.74,25)
        g.add(obj);top.append(obj)
    names=('1','0','2') if s!=0 else ('?','?','?')
    role=role_row(g,roles=('TRĂM','CHỤC','ĐƠN VỊ'),names=names,high=min(s,2))
    if s in (0,1):g.add(label('0 KHÔNG ĐƯỢC Ở HÀNG TRĂM',LX,.33,17,C['red'],True))
    elif s==5:g.add(info('Tận cùng 0 hoặc 2, 4',.33,C['gold']))
    else:g.add(info('Không lặp chữ số đã dùng',.33,C['cyan']))
    notes=['Chữ số đầu có điều kiện riêng','4 lựa chọn ở hàng trăm','Hàng chục có 4 lựa chọn','4 × 4 × 3 = 48','60 − 12 = 48','12 + 18 = 30 số chẵn']
    g.add(info(notes[s],-1.83,C['green']))
    g.add(footer('RÀNG BUỘC HÀNG TRĂM KHÁC 0'))
    return g,top[0] if s in (0,1) else role[min(s,2)]


def compare_view(s):
    g=VGroup(heading('CÙNG SÁU BẠN · BA CÁCH ĐẾM'))
    candidates(g)
    if s==0:
        for i,ch in enumerate('ABCDEF'):
            g.add(token(ch,-6.22+i*.91,-.22,C['cyan'],.73,.70,23))
    elif s in (2,3):
        team=RoundedRectangle(width=4.35,height=1.25,corner_radius=.22,stroke_width=2,
                              stroke_color=C['purple'],fill_color=C['panel_alt'],fill_opacity=1)
        team.move_to([LX,-.35,0]);g.add(team)
        for j,ch in enumerate('ABC' if s==2 else 'BAC'):
            g.add(token(ch,LX-1.25+j*1.25,-.35,C['cyan'],.76,.75,23))
        g.add(label('ABC ≡ BAC (cùng một đội)',LX,.71,18,C['purple'],True))
    else:
        roles=role_row(g,roles=('1','2','3'),names=('A','B','C'),high=s%3)
        g.add(label('Một nhóm → 3! cách phân vai',LX,.46,18,C['gold'],True))
    notes=['HOÁN VỊ: XẾP HẾT 6','CHỈNH HỢP: 3 VỊ TRÍ PHÂN BIỆT','TỔ HỢP: CHỌN NHÓM KHÔNG VAI TRÒ','120 ÷ 6 = 20 nhóm','A = C × k!','CẦN HIỂU MÔ HÌNH TRƯỚC']
    g.add(info(notes[s],-1.75,C['green']))
    g.add(footer('CHỌN PHƯƠNG PHÁP THEO Ý NGHĨA KẾT QUẢ'))
    return g,g[1]


def practice_view(s):
    if s==0:return slots_view(1)
    if s==1:return slots_view(2)
    if s==2:return restriction_view(1)
    if s==3:return digits_view(5)
    if s==4:return general_view(3)
    return compare_view(4)


def visual(b):
    return {'intro':intro_view,'slots':slots_view,'tree':tree_view,
            'general':general_view,'restrict':restriction_view,'digits':digits_view,
            'compare':compare_view,'practice':practice_view}[b.section](b.state)


def math_png(key):
    p=ROOT/'assets'/'comb06v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Missing Typst formula {p}; run prepare_comb06_v2.py first')
    im=ImageMobject(str(p))
    im.scale_to_fit_width(min(im.width,5.47))
    if im.height>.67:im.scale_to_fit_height(.67)
    im.move_to([RX,-1.16,0])
    return im


class COMB06(Scene):
    def setup(self):
        f=ROOT/'voice'/'comb06_voice_manifest.json'
        if not f.is_file():raise FileNotFoundError('Run scripts/prepare_comb06_v2.py --voice off|on first')
        self.manifest=json.loads(f.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('Narration manifest beat count mismatch')
        self.previous=None
        self.add(label('SANG MATH / ĐẠI SỐ TỔ HỢP',-3.84,3.65,18,C['cyan'],True,6.17))
        self.add(label('COMB06 / CHỈNH HỢP',4.34,3.65,18,C['muted'],True,4.20))
        self.add(Line([-6.83,3.32,0],[6.83,3.32,0],stroke_width=1.2,color=C['line']))
        for x,w in ((LX,6.18),(RX,7.22)):
            pane=RoundedRectangle(width=w,height=6.20,corner_radius=.16,stroke_width=1.3,
                                  stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1)
            pane.move_to([x,0,0]);self.add(pane)
        self.add(Line([-6.83,-3.35,0],[6.83,-3.35,0],stroke_width=1.2,color=C['line']))

    def right(self,b,i):
        heads=VGroup(label(CHAPTER_LABELS[b.section],RX,2.74,18,C['purple'],True,6.06),
                     label(b.heading,RX,2.11,22,C['gold'],True,6.00))
        lines=VGroup(*[label('• '+s,RX,1.25-j*.54,19,C['text'],False,5.98) for j,s in enumerate(b.lines)])
        formula=math_png(b.formula) if b.formula else label('QUAN SÁT  →  SUY LUẬN',RX,-1.15,16,C['cyan'],True)
        result=VGroup(Line([.54,-1.73,0],[6.24,-1.73,0],stroke_width=1.3,color=C['line']),
                      label(b.takeaway,RX,-2.34,19,C['green'],True,5.96))
        counter=label(f'{i+1:02d} / {len(BEATS)}',0,-3.68,14,C['muted'])
        return heads,lines,formula,result,counter

    def beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            sound=ROOT/'voice'/clip['file']
            if not sound.is_file():raise FileNotFoundError(sound)
            self.add_sound(str(sound))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.95)
        art,focus=visual(b)
        heads,lines,formula,result,counter=self.right(b,i)
        if self.previous is None:
            self.play(FadeIn(art),FadeIn(heads),FadeIn(counter),run_time=1.20)
        else:
            old_art,old_heads,old_lines,old_math,old_result,old_counter=self.previous
            self.play(FadeOut(old_art),FadeIn(art),FadeOut(old_heads),FadeIn(heads),
                      FadeOut(old_lines),FadeOut(old_math),FadeOut(old_result),
                      ReplacementTransform(old_counter,counter),run_time=1.20)
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.055),run_time=2.0)
        for entry in lines:self.play(FadeIn(entry,shift=.10*UP),run_time=.85)
        self.play(FadeIn(formula,shift=.06*UP),run_time=.9)
        self.play(FadeIn(result),run_time=.8)
        self.play(Circumscribe(result[-1],color=C['green'],buff=.13),run_time=1.05)
        spent=1.2+2.0+3*.85+.9+.8+1.05
        if duration>spent:self.wait(duration-spent)
        self.previous=(art,heads,lines,formula,result,counter)

    def construct(self):
        for i,b in enumerate(BEATS):self.beat(i,b)
        self.play(*[FadeOut(o) for o in self.previous],run_time=1.0)
        end=VGroup(label('CHỈNH HỢP • CHỌN k RỒI XẾP',0,.33,34,C['cyan'],True,11.8),
                   label('TẬP 07 / TỔ HỢP',0,-.51,26,C['gold'],True,11.8))
        self.play(FadeIn(end),run_time=1.4)
        self.wait(2.8)
