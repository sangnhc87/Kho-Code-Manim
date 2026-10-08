"""COMB16 – Division into labeled/unlabeled groups and roles.

Run `python scripts/prepare_comb16_v2.py --voice off` once before rendering.
Render Manim scene: COMB16 (480p preview or 1080p output).
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb16_lesson_data import BEATS,CHAPTER_LABELS
from series_config import PALETTE as C
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8.0
FONT='Noto Sans'
LX=-3.65;RX=3.16

def tx(s,x,y,size=17,color=None,bold=False,width=None):
    obj=Text(str(s),font=FONT,font_size=size,color=color or C['text'],weight='BOLD' if bold else 'NORMAL')
    if width and obj.width>width:obj.scale_to_fit_width(width)
    obj.move_to((x,y,0))
    return obj

def badge(letter,x,y,color,rad=.28):
    circ=Circle(radius=rad,stroke_width=2.0,stroke_color=color,fill_color=C['panel_alt'],fill_opacity=1).move_to((x,y,0))
    word=tx(letter,x,y,17,C['text'],True,.38)
    return VGroup(circ,word)

def group_row(g,labels,y,color,title,leader=None,dim=False):
    count=len(labels)
    w=max(1.72,count*.66+.36)
    xs=[LX+(j-(count-1)/2)*.67 for j in range(count)]
    outline=RoundedRectangle(width=w,height=.86,corner_radius=.16,stroke_color=color,stroke_width=2.0,
                              fill_color=C['panel_alt'],fill_opacity=.92).move_to((LX,y,0))
    g.add(outline)
    cards=[]
    for j,(ch,x) in enumerate(zip(labels,xs)):
        b=badge(ch,x,y,color)
        g.add(b)
        cards.append(b)
    g.add(tx(title,LX,y+.69,14,color,True,5.8))
    if leader and leader in labels:
        index=labels.index(leader)
        g.add(tx('★',xs[index],y+.44,22,C['gold'],True,.6))
    return outline,cards

def model(section,state):
    g=VGroup()
    g.add(tx('PHÂN NHÓM  /  ĐỔI VỊ TRÍ  /  CHỌN TRƯỞNG',LX,2.64,14,C['cyan'],True,5.9))
    focus=None
    if section=='labeled':
        a=('A','B','C') if state%2==0 else ('A','C','D')
        b=tuple(x for x in 'ABCDEFGH' if x not in a)
        focus,_=group_row(g,a,.85,C['red'],'NHÓM ĐỎ · 3 NGƯỜI',leader='A' if state in (4,5) else None)
        group_row(g,b,-.83,C['cyan'],'NHÓM XANH · 5 NGƯỜI')
        caption=['CHỌN 3 NGƯỜI','5 NGƯỜI TỰ VÀO ĐỘI XANH','56 LỰA CHỌN','ĐỔI TÊN LÀ KHÁC VAI TRÒ','CHỌN THÊM TRƯỞNG','CÓ NHÃN → KHÔNG CHIA 2'][state]
    elif section=='equal':
        a=tuple('ABCD') if state%2==0 else tuple('EFGH')
        b=tuple(x for x in 'ABCDEFGH' if x not in a)
        focus,_=group_row(g,a,.85,C['purple'],'NHÓM KHÔNG TÊN · 4')
        group_row(g,b,-.83,C['cyan'],'NHÓM KHÔNG TÊN · 4')
        caption=['ĐỀU 4–4','70 CÁCH CHỌN NHÓM ĐẦU','MỖI PHÂN HOẠCH GẶP 2 LẦN','ĐỔI CHỖ HAI NHÓM','CÓ TÊN: 70 / KHÔNG TÊN: 35','CÔNG THỨC TỔNG QUÁT'][state]
    elif section=='unequal':
        a=tuple('ABC');b=tuple('DEFGH')
        # Swap their vertical locations, but preserve the size labels.
        y1,y2=(.85,-.85) if state!=2 else (-.85,.85)
        focus,_=group_row(g,a,y1,C['purple'],'NHÓM NHỎ · 3')
        group_row(g,b,y2,C['cyan'],'NHÓM LỚN · 5')
        caption=['HAI KÍCH THƯỚC KHÁC','CHỌN BỘ BA: 56','ĐỔI VỊ TRÍ VẪN BIẾT NHÓM NHỎ','3–5 KHÁC 4–4','NHÓM CỠ 2, 3, 4','CHỈ CÁC NHÓM CÙNG CỠ MỚI ĐỔI'][state]
    elif section=='three':
        packs=[('A','B','C'),('D','E','F'),('G','H','I')]
        if state in (2,4):packs=[packs[1],packs[2],packs[0]]
        for i,chars in enumerate(packs):
            f,_=group_row(g,chars,1.35-i*1.33,[C['purple'],C['cyan'],C['gold']][i],
                ('NHÓM I' if state in (1,4) else 'BỘ BA')+' · '+str(i+1))
            if i==0:focus=f
        caption=['BA BỘ BA','CÓ NHÃN: 1680','KHÔNG NHÃN: CHIA 6','MẪU SỐ (3!)³ · 3!','NẾU CÓ TÊN THÌ KHÔNG CHIA','LUÔN KIỂM TRA SỐ LẦN TRÙNG'][state]
    elif section=='pairs':
        packs=[('A','B'),('C','D'),('E','F')]
        if state==4:packs+=[('G','H')]
        # each pair is a column-shaped bracket in a 2-row grid
        for i,chars in enumerate(packs):
            x=LX+(i-(len(packs)-1)/2)*1.32
            r=RoundedRectangle(width=1.18,height=.93,corner_radius=.16,stroke_width=2,
                stroke_color=[C['cyan'],C['purple'],C['gold'],C['green']][i],
                fill_color=C['panel_alt'],fill_opacity=1).move_to((x,.35,0))
            g.add(r)
            for j,s in enumerate(chars):g.add(badge(s,x+(j-.5)*.53,.35,[C['cyan'],C['purple'],C['gold'],C['green']][i],.23))
            g.add(tx('CẶP '+str(i+1),x,1.19,12,C['muted'],True,1.3))
            if i==0:focus=r
        g.add(tx('ĐỔI AB↔BA HAY ĐỔI CẶP ĐỀU KHÔNG TẠO CÁCH MỚI',LX,-1.3,15,C['purple'],True,5.84))
        caption=['MỖI CẶP 2 PHẦN TỬ','CHIA 2!³ BÊN TRONG','CHIA TIẾP 3! GIỮA CÁC CẶP','CỐ ĐỊNH BẠN GHÉP VỚI A','BỐN CẶP TRONG TÁM NGƯỜI','CHỌN SÁU RỒI GHÉP CẶP'][state]
    elif section=='leaders':
        if state<=1:
            a=('A','B','C');b=('D','E','F','G','H')
            focus,_=group_row(g,a,.86,C['cyan'],'ĐỘI BA NGƯỜI',leader='A' if state else None)
            group_row(g,b,-.86,C['purple'],'KHÔNG THUỘC ĐỘI')
        else:
            for i,chars in enumerate([('A','B','C'),('D','E','F'),('G','H','I')]):
                f,_=group_row(g,chars,1.37-i*1.34,[C['cyan'],C['purple'],C['gold']][i],
                         'NHÓM BA · CÓ TRƯỞNG',leader=chars[(state+i)%3])
                if i==0:focus=f
        caption=['CHỌN NHÓM RỒI CHỌN TRƯỞNG','56 × 3 = 168','280 × 27 = 7560','NHÓM VẪN KHÔNG CÓ TÊN','CHỌN TRƯỞNG TRƯỚC DỄ TRÙNG','TRƯỞNG ≠ NHÃN NHÓM'][state]
    elif section=='condition':
        if state<=3:
            a=('A','B','C','D') if state in (0,1) else ('A','C','D','E')
            b=tuple(x for x in 'ABCDEFGH' if x not in a)
            focus,_=group_row(g,a,.84,C['cyan'],'NHÓM 4 CHỨA A')
            group_row(g,b,-.84,C['red'] if 'B' in b else C['purple'],'NHÓM 4 CÒN LẠI')
        else:
            packs=[('A','B','C'),('D','E','F'),('G','H','I')]
            if state==5:packs=[('A','C','D'),('B','E','F'),('G','H','I')]
            for i,chars in enumerate(packs):
                f,_=group_row(g,chars,1.37-i*1.34,[C['cyan'],C['purple'],C['gold']][i],'BỘ BA '+str(i+1))
                if i==0:focus=f
        caption=['A VÀ B CÙNG NHÓM','15 CÁCH','A, B KHÁC: 20 CÁCH','CỐ ĐỊNH NHÓM CHỨA A','BA NHÓM, CÙNG: 70','BA NHÓM, KHÁC: 210'][state]
    else:
        packs=[('A','C','D'),('B','E','F'),('G','H','I')]
        if state==1:packs=[('A','B','C'),('D','E','F'),('G','H','I')]
        for i,chars in enumerate(packs):
            f,_=group_row(g,chars,1.35-i*1.34,[C['cyan'],C['purple'],C['gold']][i],
                      'BỘ BA · KHÔNG TÊN',leader=chars[(state+i)%3] if state in (2,5) else None)
            if i==0:focus=f
        if state==1:g.add(tx('A VÀ B CÙNG NHÓM: LOẠI',LX,-2.03,17,C['red'],True,5.70))
        caption=['HÃY XÁC ĐỊNH ĐÚNG PHÂN HOẠCH','280 − 70 = 210','MỖI NHÓM CHỌN TRƯỞNG','CHỌN NHÓM CHỨA A','CHỌN NHÓM CHỨA B','5.670 CÁCH · HAI CÁCH GIẢI'][state]
    g.add(tx(caption,LX,-2.43,16,C['green'] if state in (2,5) else C['gold'],True,5.75))
    return g,focus

def formula_image(key):
    p=ROOT/'assets'/'comb16v2'/f'{key}.png'
    if not p.is_file():raise FileNotFoundError(f'Missing Typst image {p}. Run scripts/prepare_comb16_v2.py first.')
    im=ImageMobject(str(p))
    if im.width>5.75:im.scale_to_fit_width(5.75)
    if im.height>.96:im.scale_to_fit_height(.96)
    im.move_to((RX,-1.10,0))
    return im

def split_takeaway(sentence,limit=41):
    words=sentence.split();lines=[];current=[]
    for word in words:
        if current and len(' '.join(current+[word]))>limit:
            lines.append(' '.join(current));current=[word]
        else:current.append(word)
    if current:lines.append(' '.join(current))
    if len(lines)>2:lines=[lines[0],' '.join(lines[1:])]
    return lines

class COMB16(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb16_voice_manifest.json'
        if not path.is_file():raise FileNotFoundError('Run: python scripts/prepare_comb16_v2.py --voice off')
        self.manifest=json.loads(path.read_text(encoding='utf-8'))
        if self.manifest['beats']!=len(BEATS):raise ValueError('COMB16 clip count mismatch')
        self.current=None
        self.add(tx('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.65,3.62,18,C['cyan'],True,6.0))
        self.add(tx('COMB16  /  CHIA NHÓM & VAI TRÒ',3.28,3.62,18,C['muted'],True,6.0))
        self.add(Line((-6.85,3.32,0),(6.85,3.32,0),color=C['line'],stroke_width=1.25))
        for x,w in ((LX,6.17),(RX,6.50)):
            self.add(RoundedRectangle(width=w,height=6.2,corner_radius=.16,
                 stroke_color=C['line'],stroke_width=1.2,
                 fill_color=C['panel'],fill_opacity=1).move_to((x,0,0)))
        self.add(Line((-6.85,-3.33,0),(6.85,-3.33,0),color=C['line'],stroke_width=1.25))

    def panel(self,b,i):
        heading=VGroup(tx(CHAPTER_LABELS[b.section],RX,2.66,15,C['purple'],True,5.72),
                tx(b.heading,RX,2.05,19,C['gold'],True,5.78))
        statements=VGroup(*[tx('• '+line,RX,1.28-j*.64,16,C['text'],False,5.75) for j,line in enumerate(b.lines)])
        formula=formula_image(b.formula)
        takeaway=VGroup(Line((.17,-1.81,0),(6.28,-1.81,0),color=C['line'],stroke_width=1.1))
        for j,line in enumerate(split_takeaway(b.takeaway)):
            takeaway.add(tx(line,RX,-2.16-j*.38,14,C['green'],True,5.68))
        count=tx(f'{i+1:02d} / 48',0,-3.66,15,C['muted'],True)
        return heading,statements,formula,takeaway,count

    def show_beat(self,i,b):
        clip=self.manifest['clips'][f'{i:03}']
        if clip.get('file'):
            voice=ROOT/'voice'/clip['file']
            if not voice.is_file():raise FileNotFoundError(voice)
            self.add_sound(str(voice))
        duration=max(b.min_seconds,float(clip.get('duration',0))+.85)
        art,focus=model(b.section,b.state)
        header,lines,equation,summary,number=self.panel(b,i)
        if self.current is None:
            self.play(FadeIn(art),FadeIn(header),FadeIn(number),run_time=1.05)
            used=1.05
        else:
            oa,oh,ol,oe,os,on=self.current
            self.play(FadeOut(oa),FadeOut(oh),FadeOut(ol),FadeOut(oe),FadeOut(os),
                  FadeIn(art),FadeIn(header),ReplacementTransform(on,number),run_time=1.1)
            used=1.1
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.018),run_time=1.4)
        used+=1.4
        for line in lines:
            self.play(FadeIn(line,shift=UP*.07),run_time=1.2);used+=1.2
        self.play(FadeIn(equation,shift=UP*.07),run_time=1.3);used+=1.3
        self.play(FadeIn(summary),run_time=1.1);used+=1.1
        if len(summary)>1:
            self.play(Circumscribe(summary[-1],color=C['green'],buff=.08),run_time=1.0);used+=1.
        if used<duration:self.wait(duration-used)
        self.current=(art,header,lines,equation,summary,number)

    def construct(self):
        for i,b in enumerate(BEATS):self.show_beat(i,b)
        self.play(*[FadeOut(obj) for obj in self.current],run_time=1.0)
        final=VGroup(tx('COMB16 · CHIA NHÓM & PHÂN CÔNG',0,.60,30,C['cyan'],True,12),
                     tx('CÓ NHÃN · KHÔNG NHÃN · ĐẾM KHÔNG TRÙNG',0,-.42,21,C['gold'],True,12))
        self.play(FadeIn(final),run_time=1.2)
        self.wait(3.0)
