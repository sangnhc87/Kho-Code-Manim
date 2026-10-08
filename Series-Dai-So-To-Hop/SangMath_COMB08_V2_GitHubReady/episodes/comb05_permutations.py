"""COMB05 V2 — Permutations, factorial, adjacent block, complement and gap proof.

Render only after: python scripts/prepare_comb05_v2.py --voice off|on
Manim scene: COMB05
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb05_lesson_data import BEATS,CHAPTER_LABELS,FOUR_ORDERS

config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LX=-3.77
RX=3.18


def text(s,x,y,size=20,color=None,bold=False,maxw=5.76):
    t=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if maxw and t.width>maxw:t.scale_to_fit_width(maxw)
    t.move_to([x,y,0]);return t


def card(s,x,y,stroke=None,w=1.03,h=.65,size=23,fill=None):
    box=RoundedRectangle(width=w,height=h,corner_radius=.11,stroke_width=1.65,
       stroke_color=stroke or C['line'],fill_color=fill or C['panel_alt'],fill_opacity=1)
    box.move_to([x,y,0])
    return VGroup(box,text(s,x,y,size,C['text'],True,w-.13))


def title(s):return text(s,LX,2.43,19,C['cyan'],True,5.68)
def foot(s,col=None):return text(s,LX,-2.72,18,col or C['gold'],True,5.80)
def guide(s,y):return text(s,LX,y,17,C['muted'],False,5.65)


def slot(stage):
    g=VGroup(title('XẾP BỐN CUỐN SÁCH VÀO BỐN Ô'))
    for i,ch in enumerate('ABCD'):
        x=-6.00+1.46*i
        g.add(card(ch,x,1.34,C['cyan'] if i>=min(stage,4) else C['inactive'],.87,.64,25))
    for i in range(4):
        x=-6.00+1.46*i
        active=i<stage
        c=C['green'] if active else C['line']
        g.add(card('ABCD'[i] if active else '□',x,-.18,c,.92,.75,27))
        g.add(text(str(i+1),x,-.91,14,C['muted']))
        if stage>=1 and i==stage-1:
            g.add(Arrow([x,.81,0],[x,.35,0],stroke_width=3,tip_length=.13,color=C['gold']))
    g.add(guide(('Chọn phần tử → xếp vào vị trí' if stage==0 else 'Mỗi cuốn chỉ xuất hiện một lần'),-1.53))
    g.add(foot('VỊ TRÍ PHÂN BIỆT • KHÔNG LẶP'))
    return g,g[1]


def slots(s):
    stage=[1,2,3,4,4,4][s]
    g,focus=slot(stage)
    choices=[4,3,2,1]
    if s>=1:
        for k,num in enumerate(choices):
            x=-6.00+k*1.46
            g.add(text(str(num) if k<=min(s,3) else '·',x,.49,23,C['gold'] if k<=min(s,3) else C['muted'],True))
    if s==4:g.add(guide('Mỗi dãy = một đường chọn duy nhất',-1.90))
    elif s==5:g.add(guide('Liệt kê kiểm chứng: 24 kết quả',-1.90))
    else:g.add(guide('Số lựa chọn giảm: 4 → 3 → 2 → 1',-1.90))
    return g,focus


def grid24(s):
    g=VGroup(title('BẢNG TOÀN BỘ 24 HOÁN VỊ'))
    for i,word in enumerate(FOUR_ORDERS):
        row=i%6; col=i//6
        x=-6.09+col*1.54
        y=1.79-row*.64
        high=(col==min(s,3) if s in (0,1) else True)
        obj=card(word,x,y,C['cyan'] if high else C['line'],1.25,.46,17)
        if not high:obj.set_opacity(.43)
        g.add(obj)
    g.add(foot('4 nhóm, mỗi nhóm 3! = 6 dãy'))
    return g,g[1]


def factorial_stage(s):
    g=VGroup(title('GIẢI THÍCH CÔNG THỨC Pₙ = n!'))
    states=[('n','n − 1','n − 2','…','2','1'),('n','n − 1','n − 2','…','2','1'),('5','4','3','2','1',''),('0!','1','','','',''),('n','(n − 1)!','','','',''),('✓','✓','✓','','','')]
    row=states[s]
    for i,v in enumerate(row):
        if v:
            x=-6.19+i*1.01
            g.add(card(v,x,.62,C['cyan'] if i%2==0 else C['gold'],.91,.75,20))
    messages=['Xếp tất cả n phần tử khác nhau','Vị trí đầu tiên có n lựa chọn','Năm phần tử → 5! = 120','Tích rỗng: 0! = 1','Chọn vị trí đầu rồi hoán vị phần còn lại','Dùng đủ – phân biệt – có thứ tự']
    g.add(guide(messages[s],-1.18))
    g.add(foot('Mỗi bước chọn một phần tử CHƯA dùng'))
    return g,g[1]


def block_stage(s):
    g=VGroup(title('NĂM NGƯỜI · A, B PHẢI ĐỨNG CẠNH'))
    if s==4:
        for j,w in enumerate(['ABC','BAC','CAB','CBA']):
            g.add(card(w,-5.45+(j%2)*2.85,.85-(j//2)*1.22,C['green'],2.40,.71,24))
    else:
        block=RoundedRectangle(width=2.17,height=1.23,corner_radius=.14,
            stroke_color=C['purple'],stroke_width=2.7,fill_color=C['panel_alt'],fill_opacity=1)
        block.move_to([-5.91,.53,0]);g.add(block)
        pair='AB' if s==2 else 'BA' if s==3 else 'AB'
        pair_cards=[]
        for k,ch in enumerate(pair):
            token=card(ch,-6.39+k*.90,.53,C['cyan'] if k==0 else C['gold'],.76,.70,23)
            g.add(token);pair_cards.append(token)
        for k,ch in enumerate('CDE'):
            g.add(card(ch,-3.84+1.10*k,.53,C['line'],.91,.73,23))
        g.add(guide('KHỐI AB' if s<2 else 'KHỐI BA : cũng là một cách',-1.08))
        if s>=3:g.add(text('4 đối tượng × 2 cách trong khối',LX,-1.67,19,C['green'],True))
    g.add(foot('ĐỨNG CẠNH = XẾP KHỐI × ĐỔI TRONG KHỐI'))
    return g,(pair_cards[0],pair_cards[1]) if s==2 else g[1]


def gaps_stage(s):
    g=VGroup(title('A VÀ B KHÔNG ĐỨNG CẠNH NHAU'))
    if s in (0,1,5):
        order='ACBDE' if s==5 else 'ABCDE'
        for k,ch in enumerate(order):
            g.add(card(ch,-6.14+k*1.20,.57,C['cyan'] if ch in 'AB' else C['line'],.97,.77,24))
        if s==1:g.add(guide('120 tổng – 48 cạnh nhau = 72',-1.06))
        if s==5:g.add(guide('Hai cách đếm cùng một tập 72 dãy',-1.06))
    else:
        # Four *true* gaps before/between/after the three fixed letters C, D, E.
        gap_x=[-6.42,-4.87,-3.32,-1.77]
        for k,ch in enumerate('CDE'):
            g.add(card(ch,-5.66+k*1.55,.39,C['cyan'],.94,.76,24))
        for k,x in enumerate(gap_x):
            strong=(s>=3 and k in (0,2))
            g.add(card(str(k+1),x,.40,C['gold'] if strong else C['line'],.45,.47,14))
        g.add(guide('4 khoảng: trước / giữa / giữa / sau',-1.16))
        if s>=4:g.add(text('Hai vị trí khác nhau, rồi gán A và B',LX,-1.73,18,C['green'],True))
    g.add(foot('KHÔNG ĐỨNG CẠNH: 72 CÁCH',C['green']))
    return g,g[1]


def advanced_stage(s):
    g=VGroup(title('RÀNG BUỘC VỊ TRÍ TRONG HÀNG'))
    people='ACDEFB' if s==2 else 'ABCDEF' if s==3 else 'ABCDE'
    for i,ch in enumerate(people):
        x=-6.15+i*(1.12 if len(people)==6 else 1.33)
        special=ch in 'AB'
        g.add(card(ch,x,.68,C['gold'] if special else C['line'],.95,.79,25))
    if s==0 or s==1:
        g.add(guide('A đứng trước B, không yêu cầu cạnh nhau',-1.10))
    elif s==2:
        g.add(guide('A và B ở hai đầu • 4 người ở giữa',-1.10))
    elif s==3:
        g.add(guide('Tổng 720 trừ 240 cách kề nhau',-1.10))
    elif s==4:
        g.add(guide('Xếp hết ≠ chọn một phần',-1.10))
    else:g.add(guide('Công thức n! chỉ dùng khi các vật phân biệt',-1.10))
    g.add(foot('LUÔN XÁC ĐỊNH ĐIỀU KIỆN TRƯỚC'))
    return g,g[1]


def practice_stage(s):
    if s==0:return grid24(4)
    if s==1:return block_stage(3)
    if s==2:return gaps_stage(1)
    if s==3:return advanced_stage(2)
    if s==4:return factorial_stage(5)
    return factorial_stage(1)


def visual(b):
    return {'intro':lambda s:slot([0,2,3,1,0,0][s]),'slots':slots,
        'grid':grid24,'factorial':factorial_stage,'block':block_stage,
        'complement':gaps_stage,'advanced':advanced_stage,'practice':practice_stage}[b.section](b.state)


def formula_img(key):
    p=ROOT/'assets'/'comb05v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Prepare COMB05 Typst formulas first: {p}')
    im=ImageMobject(str(p)); im.scale_to_fit_width(min(im.width,5.55))
    if im.height>.65:im.scale_to_fit_height(.65)
    im.move_to([RX,-1.15,0]);return im


class COMB05(Scene):
    def setup(self):
        mf=ROOT/'voice'/'comb05_voice_manifest.json'
        if not mf.exists():raise FileNotFoundError('Run scripts/prepare_comb05_v2.py --voice off/on first')
        self.meta=json.loads(mf.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Voice manifest beat count mismatch')
        self.last=None
        self.add(text('SANG MATH / ĐẠI SỐ TỔ HỢP',-3.93,3.64,19,C['cyan'],True,6.17))
        self.add(text('COMB05 / HOÁN VỊ',4.46,3.64,19,C['muted'],True,4.35))
        self.add(Line([-6.83,3.32,0],[6.83,3.32,0],stroke_width=1.2,color=C['line']))
        for x,w in ((LX,6.18),(RX,7.22)):
            pane=RoundedRectangle(width=w,height=6.20,corner_radius=.16,stroke_width=1.3,
                stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1)
            pane.move_to([x,0,0]);self.add(pane)
        self.add(Line([-6.83,-3.35,0],[6.83,-3.35,0],stroke_width=1.2,color=C['line']))

    def right(self,b,index):
        heads=VGroup(text(CHAPTER_LABELS[b.section],RX,2.72,17,C['purple'],True,6.06),
                     text(b.heading,RX,2.14,24,C['gold'],True,6.06))
        entries=VGroup(*[text(f'• {line}',RX,1.24-i*.53,20,C['text'],False,5.99) for i,line in enumerate(b.lines)])
        formula=formula_img(b.formula) if b.formula else text('QUAN SÁT → SUY LUẬN → KẾT LUẬN',RX,-1.15,17,C['cyan'],True,5.70)
        result=VGroup(Line([.54,-1.73,0],[6.24,-1.73,0],stroke_width=1.3,color=C['line']),
            text(b.takeaway,RX,-2.32,20,C['green'],True,5.96))
        counter=text(f'{index+1:02d} / 48',0,-3.68,14,C['muted'])
        return heads,entries,formula,result,counter

    def show_beat(self,i,b):
        clip=self.meta['clips'][f'{i:03}']
        if clip.get('file'):
            path=ROOT/'voice'/clip['file']
            if not path.is_file():raise FileNotFoundError(path)
            self.add_sound(str(path))
        length=max(b.min_seconds,float(clip.get('duration',0))+.95)
        picture,focus=visual(b)
        heads,entries,formula,result,counter=self.right(b,i)
        if self.last is None:
            self.play(FadeIn(picture),FadeIn(heads),FadeIn(counter),run_time=1.28)
        else:
            oldv,oldh,olde,oldf,oldr,oldc=self.last
            self.play(FadeOut(oldv),FadeIn(picture),FadeOut(oldh),FadeIn(heads),
                FadeOut(olde),FadeOut(oldf),FadeOut(oldr),ReplacementTransform(oldc,counter),run_time=1.28)
        if isinstance(focus,tuple):
            self.play(Swap(focus[0],focus[1]),run_time=2.15)
        else:
            self.play(Indicate(focus,color=C['gold'],scale_factor=1.035),run_time=2.15)
        for line in entries:self.play(FadeIn(line,shift=.08*UP),run_time=.82)
        self.play(FadeIn(formula),run_time=.95)
        self.play(FadeIn(result),run_time=.90)
        self.play(Circumscribe(result[-1],color=C['green'],buff=.10),run_time=1.05)
        spent=1.28+2.15+3*.82+.95+.90+1.05
        if length>spent:self.wait(length-spent)
        self.last=(picture,heads,entries,formula,result,counter)

    def construct(self):
        for i,b in enumerate(BEATS):self.show_beat(i,b)
        self.play(*[FadeOut(obj) for obj in self.last],run_time=1.)
        credit=VGroup(text('HOÁN VỊ • Pₙ = n!',0,.35,36,C['cyan'],True,11.6),
            text('COMB06 / CHỈNH HỢP',0,-.42,27,C['gold'],True,11.7))
        self.play(FadeIn(credit),run_time=1.4)
        self.wait(2.8)
