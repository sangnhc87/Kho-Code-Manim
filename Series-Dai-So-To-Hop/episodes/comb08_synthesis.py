"""COMB08 V2: Hoan vi - Chinh hop - To hop, 48 synchronized teaching beats.

The lesson data and Typst formula assets are prepared by prepare_comb08_v2.py.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import PALETTE as C
from comb08_lesson_data import BEATS,CHAPTER_LABELS
config.background_color=C['bg']
config.frame_width=14.222222
config.frame_height=8
FONT='Noto Sans'
LEFT=-3.79
RIGHT=3.22


def label(text,x,y,size=19,color=None,bold=False,width=None):
    t=Text(str(text),font=FONT,font_size=size,weight='BOLD' if bold else 'NORMAL',color=color or C['text'])
    if width and t.width>width:t.scale_to_fit_width(width)
    t.move_to((x,y,0));return t


def tile(text,x,y,col=None,w=.70,h=.62,size=22):
    bg=RoundedRectangle(width=w,height=h,corner_radius=.11,stroke_color=col or C['line'],
                        stroke_width=2,fill_color=C['panel_alt'],fill_opacity=1).move_to((x,y,0))
    fg=label(text,x,y,size,C['text'],True,w-.10)
    return VGroup(bg,fg)


def framed(text,x,y,w=2.4,h=.92,color=None,small=False):
    rect=RoundedRectangle(width=w,height=h,corner_radius=.12,fill_color=C['panel_alt'],
             fill_opacity=.88,stroke_color=color or C['line'],stroke_width=2).move_to((x,y,0))
    return VGroup(rect,label(text,x,y,15 if small else 18,color or C['text'],True,w-.20))


def people(g,names='ABCDEFGH',chosen='',highlight='',y=1.56):
    m=len(names);step=5.35/max(m-1,1)
    objs=[]
    for j,name in enumerate(names):
        x=-6.46+j*step
        color=C['red'] if name in highlight else C['green'] if name in chosen else C['cyan']
        t=tile(name,x,y,color,w=min(.68,step*.88),h=.62,size=21)
        g.add(t);objs.append(t)
    return objs


def add_slots(g,names,y=-.17,w=1.15,spacing=1.74,colors=None):
    result=[]
    for j,name in enumerate(names):
        x=LEFT+(j-(len(names)-1)/2)*spacing
        col=(colors[j] if colors else C['purple'])
        tag=framed(name,x,y,w,.84,col,True);g.add(tag);result.append(tag)
    return result


def footer(g,s,color=None):
    g.add(label(s,LEFT,-2.61,17,color or C['gold'],True,5.75))


def compare_view(s):
    g=VGroup(label('CÙNG 6 HỌC SINH · KHÁC YÊU CẦU',LEFT,2.53,19,C['cyan'],True,5.79))
    tokens=people(g,'ABCDEF',chosen='AB' if s>=3 else '')
    kinds=['XẾP CẢ 6','2 VAI TRÒ','CHỌN 2 BẠN']
    counts=['720','30','15']
    objs=[]
    for j,(k,count) in enumerate(zip(kinds,counts)):
        x=-5.69+j*1.90
        col=C['green'] if (s>=4 or (s==1 and j==0) or (s==2 and j==1) or (s==3 and j==2)) else C['line']
        ob=framed(k,x,.38,1.78,.75,col,True);g.add(ob);objs.append(ob)
        g.add(label(count if (s>=j+1) else '?',x,-.40,24,col,True,1.5))
    if s>=3:
        g.add(framed('AB ≠ BA (vai trò)',-5.29,-1.41,2.52,.60,C['gold'],True))
        g.add(framed('{A, B} (một đội)',-2.48,-1.41,2.57,.60,C['green'],True))
    else:g.add(label('VỊ TRÍ  •  VAI TRÒ  •  THÀNH VIÊN',LEFT,-1.43,18,C['muted'],True,5.6))
    footer(g,'XÁC ĐỊNH ĐỐI TƯỢNG ĐẾM TRƯỚC')
    return g,objs[min(s//2,2)]


def diagnose_view(s):
    g=VGroup(label('CÂY QUYẾT ĐỊNH PHƯƠNG PHÁP',LEFT,2.53,19,C['cyan'],True,5.7))
    q1=framed('DÙNG TẤT CẢ?',LEFT,1.43,2.45,.72,C['cyan'])
    q2=framed('THỨ TỰ QUAN TRỌNG?',LEFT,.09,3.40,.76,C['purple'],True)
    g.add(q1,q2,Arrow((LEFT,1.03,0),(LEFT,.48,0),color=C['muted'],buff=.05,stroke_width=2))
    nodes=[]
    for j,(t,c) in enumerate([('HOÁN VỊ',C['gold']),('CHỈNH HỢP',C['green']),('TỔ HỢP',C['purple'])]):
        x=-5.65+j*1.86
        nd=framed(t,x,-1.25,1.72,.76,c,True);g.add(nd);nodes.append(nd)
        g.add(Line((LEFT,-.35,0),(x,-.85,0),stroke_width=1.5,color=c))
    g.add(label('CHỌN KHÔNG LẶP · n PHẦN TỬ PHÂN BIỆT',LEFT,-2.08,15,C['muted'],False,5.7))
    footer(g,'HOÁN VỊ / CHỈNH HỢP / TỔ HỢP')
    return g,nodes[min(s//2,2)]


def roles_view(s):
    g=VGroup(label('ĐỔI CHỖ: KHI NÀO TẠO KẾT QUẢ MỚI?',LEFT,2.53,19,C['cyan'],True,5.65))
    people(g,'ABCDEF',chosen='AB',y=1.50)
    top=label('HAI CHỨC VỤ',-5.28,.76,16,C['gold'],True,2.5)
    right=label('MỘT ĐỘI HAI NGƯỜI',-2.43,.76,16,C['green'],True,3.1)
    g.add(top,right)
    ordered=[]
    
    for j,c in enumerate(('A','B')):
        ob=framed(c,-5.73+j*.94,-.08,.84,.91,(C['gold'] if j==0 else C['purple']))
        g.add(ob);ordered.append(ob)
    grouped=framed('{A, B}',-2.15,-.08,2.05,.91,C['green'])
    g.add(grouped)
    if s>=1:
        g.add(label('TRƯỞNG',-5.73,-.79,13,C['muted'],True,.95))
        g.add(label('THƯ KÝ',-4.79,-.79,13,C['muted'],True,.95))
    g.add(framed('30 PHÂN CÔNG' if s>=1 else 'PHÂN CÔNG',-5.22,-1.48,2.49,.72,C['gold'],True))
    g.add(framed('15 NHÓM' if s>=2 else 'CHỌN NHÓM',-2.38,-1.48,2.32,.72,C['green'],True))
    footer(g,'ĐỔI VỊ TRÍ: AB ↔ BA  /  {A,B} KHÔNG ĐỔI')
    return g,(VGroup(*ordered) if s<=2 else grouped)


def captain_view(s):
    g=VGroup(label('CHỌN ĐỘI VÀ MỘT ĐỘI TRƯỞNG',LEFT,2.53,19,C['cyan'],True,5.70))
    people(g,'ABCDEFGH',chosen='ABC',y=1.48)
    cards=add_slots(g,['A','B','C'],y=.02,w=.86,spacing=1.25,
                    colors=[C['green'],C['green'],C['green']])
    index=(s+1)%3
    star=Star(n=5,outer_radius=.15,inner_radius=.06,color=C['gold'],fill_color=C['gold'],fill_opacity=1)
    star.move_to((cards[index].get_center()[0],.65,0));g.add(star)
    g.add(framed('56 ĐỘI' if s>=1 else 'CHỌN 3 NGƯỜI',-5.24,-1.25,2.34,.70,C['green'],True))
    g.add(framed('3 TRƯỞNG / ĐỘI' if s>=2 else 'CHỌN ĐỘI TRƯỞNG',-2.46,-1.25,2.39,.70,C['gold'],True))
    footer(g,'CHỌN ĐỘI → TRƯỞNG  /  TRƯỞNG → 2 BẠN')
    return g,star if s>=2 else cards[0]


def forbidden_view(s):
    g=VGroup(label('CHỨC VỤ CÓ ĐIỀU KIỆN CẤM',LEFT,2.53,19,C['cyan'],True,5.70))
    people(g,'ABCDEFG',chosen='BCD',highlight='A',y=1.40)
    slots=add_slots(g,['TRƯỞNG','PHÓ','THƯ KÝ'],y=.10,w=1.55,spacing=1.93,
                    colors=[C['red'],C['purple'],C['green']])
    g.add(label('A KHÔNG ĐƯỢC LÀM TRƯỞNG',LEFT,-.69,17,C['red'],True,5.66))
    boxes=[]
    for j,(name,val,col) in enumerate([('TẤT CẢ','210',C['cyan']),('VI PHẠM','30',C['red']),('HỢP LỆ','180',C['green'])]):
        x=-5.64+j*1.85
        ob=framed(name+'  '+(val if s>=j+2 else '?'),x,-1.54,1.76,.72,col,True);g.add(ob);boxes.append(ob)
    footer(g,'CHỌN TRỰC TIẾP HOẶC DÙNG PHẦN BÙ')
    return g,slots[0] if s<2 else boxes[min(s-2,2)]


def gender_view(s):
    g=VGroup(label('BỐN NAM · BA NỮ · CHỌN ĐỘI BA',LEFT,2.53,19,C['cyan'],True,5.70))
    males=[];females=[]
    for j in range(4):
        ob=tile('N'+str(j+1),-6.27+j*.78,1.40,C['cyan'],.63,.62,18);g.add(ob);males.append(ob)
    for j in range(3):
        ob=tile('G'+str(j+1),-2.78+j*.78,1.40,C['purple'],.63,.62,18);g.add(ob);females.append(ob)
    models=[]
    for i,(name,num) in enumerate([('3 NAM, 0 NỮ','4'),('2 NAM, 1 NỮ','18'),('1 NAM, 2 NỮ','12'),('0 NAM, 3 NỮ','1')]):
        x=-5.21+(i%2)*2.82; y=.36-(i//2)*1.09
        col=C['red'] if i==0 else C['green'] if i==1 else C['gold']
        ob=framed(name+' : '+(num if s>=([2,4,5,5][i]) else '?'),x,y,2.59,.82,col,True);g.add(ob);models.append(ob)
    footer(g,'ÍT NHẤT 1 NỮ: 18 + 12 + 1 = 31' if s>=5 else 'ĐẾM ĐỦ CÁC TRƯỜNG HỢP KHÔNG TRÙNG')
    return g,models[0] if s in (2,3) else models[1] if s==4 else VGroup(*models[1:])


def digits_view(s):
    g=VGroup(label('LẬP SỐ CÓ BA CHỮ SỐ KHÁC NHAU',LEFT,2.53,19,C['cyan'],True,5.65))
    g.add(label('CHỮ SỐ SỬ DỤNG',LEFT,1.54,16,C['muted'],True))
    nums=[]
    for j in range(5):
        ob=tile(str(j),-5.25+j*.75,1.03,C['red'] if j==0 and s==0 else C['cyan'],.62,.67)
        g.add(ob);nums.append(ob)
    slots=add_slots(g,['TRĂM','CHỤC','ĐƠN VỊ'],y=-.07,w=1.55,spacing=1.91,colors=[C['green'],C['purple'],C['gold']])
    zero=framed('ĐƠN VỊ 0 → 12' if s>=3 else 'ĐƠN VỊ BẰNG 0',-5.13,-1.30,2.66,.73,C['cyan'],True)
    other=framed('ĐƠN VỊ 2 / 4 → 18' if s>=4 else 'ĐƠN VỊ LÀ 2 HOẶC 4',-2.41,-1.30,2.66,.73,C['green'],True)
    g.add(zero,other)
    footer(g,'SỐ CHẴN: 12 + 18 = 30' if s>=5 else 'CHIA CÁC TRƯỜNG HỢP THEO HÀNG ĐƠN VỊ')
    return g,slots[0] if s<2 else slots[2] if s==2 else zero if s==3 else other


def capstone_view(s):
    g=VGroup(label('CAPSTONE · ĐẾM CÓ HAI RÀNG BUỘC',LEFT,2.53,19,C['cyan'],True,5.68))
    people(g,'ABCDEFGH',chosen='ABC',highlight='A' if s>=3 else '',y=1.50)
    g.add(label('ĐỘI CÓ A HOẶC B',LEFT,.76,17,C['gold'],True,5.6))
    g.add(label('A KHÔNG ĐƯỢC LÀM ĐỘI TRƯỞNG',LEFT,.27,17,C['red'],True,5.65))
    allbox=framed('TẤT CẢ: 168' if s>=1 else 'KHÔNG CÓ ĐIỀU KIỆN',LEFT,-.45,2.58,.72,C['cyan'],True)
    a=framed('CÓ A : 42' if s>=5 else 'TRƯỜNG HỢP CÓ A',-5.23,-1.42,2.47,.72,C['green'],True)
    b=framed('KHÔNG A, CÓ B: 45' if s>=5 else 'KHÔNG A, BẮT BUỘC B',-2.32,-1.42,2.70,.72,C['gold'],True)
    g.add(allbox,a,b)
    footer(g,'HAI PHƯƠNG PHÁP ĐỀU CHO 87' if s>=5 else 'CẦN LOẠI TRƯỜNG HỢP VI PHẠM')
    return g,allbox if s<2 else a if s in (2,3) else b if s==4 else VGroup(a,b)

VIEWS={'compare':compare_view,'diagnose':diagnose_view,'roles':roles_view,
       'captain':captain_view,'forbidden':forbidden_view,'gender':gender_view,
       'digits':digits_view,'capstone':capstone_view}


def formula_image(key):
    png=ROOT/'assets'/'comb08v2'/f'{key}.png'
    if not png.exists():raise FileNotFoundError(f'Missing Typst formula PNG: {png}. Run prepare_comb08_v2.py')
    m=ImageMobject(str(png))
    m.scale_to_fit_width(min(m.width,5.80))
    if m.height>.82:m.scale_to_fit_height(.82)
    m.move_to((RIGHT,-1.17,0))
    return m

class COMB08(Scene):
    def setup(self):
        path=ROOT/'voice'/'comb08_voice_manifest.json'
        if not path.is_file():raise FileNotFoundError('Run scripts/prepare_comb08_v2.py first')
        self.meta=json.loads(path.read_text(encoding='utf-8'))
        if self.meta['beats']!=len(BEATS):raise ValueError('Narration manifest count differs from lesson data')
        self.prev=None
        self.add(label('SANG MATH  /  ĐẠI SỐ TỔ HỢP',-3.86,3.63,19,C['cyan'],True,6.20))
        self.add(label('COMB08  /  TỔNG HỢP',4.26,3.63,18,C['muted'],True,4.40))
        self.add(Line((-6.85,3.31,0),(6.85,3.31,0),color=C['line'],stroke_width=1.2))
        for x,w in ((LEFT,6.18),(RIGHT,7.20)):
            p=RoundedRectangle(width=w,height=6.18,corner_radius=.17,
                        stroke_width=1.35,stroke_color=C['line'],fill_color=C['panel'],fill_opacity=1)
            p.move_to((x,0,0));self.add(p)
        self.add(Line((-6.85,-3.34,0),(6.85,-3.34,0),color=C['line'],stroke_width=1.2))

    def righthand(self,b,index):
        head=VGroup(label(CHAPTER_LABELS[b.section],RIGHT,2.73,17,C['purple'],True,6.08),
                 label(b.heading,RIGHT,2.05,21,C['gold'],True,6.03))
        lines=VGroup(*[label('• '+t,RIGHT,1.24-j*.59,18,C['text'],False,5.95)
                       for j,t in enumerate(b.lines)])
        eq=formula_image(b.formula) if b.formula else label('QUAN SÁT  →  SUY LUẬN',RIGHT,-1.13,17,C['cyan'],True,5.89)
        takeaway=VGroup(Line((.46,-1.76,0),(6.30,-1.76,0),stroke_width=1.2,color=C['line']),
                  label(b.takeaway,RIGHT,-2.39,18,C['green'],True,5.93))
        count=label(f'{index+1:02d} / {len(BEATS)}',0,-3.69,15,C['muted'])
        return head,lines,eq,takeaway,count

    def render_beat(self,index,b):
        audio=self.meta['clips'][f'{index:03}']
        if audio.get('file'):
            mp3=ROOT/'voice'/audio['file']
            if not mp3.exists():raise FileNotFoundError(mp3)
            self.add_sound(str(mp3))
        budget=max(b.min_seconds,float(audio.get('duration',0))+.95)
        art,focus=VIEWS[b.section](b.state)
        head,lines,eq,takeaway,count=self.righthand(b,index)
        if self.prev is None:
            self.play(FadeIn(art),FadeIn(head),FadeIn(count),run_time=1.05)
        else:
            old_art,old_h,old_l,old_e,old_t,old_i=self.prev
            self.play(FadeOut(old_art),FadeIn(art),FadeOut(old_h),FadeIn(head),
                      FadeOut(old_l),FadeOut(old_e),FadeOut(old_t),
                      ReplacementTransform(old_i,count),run_time=1.05)
        extra=0
        if b.section=='roles' and b.state==1:
            self.play(Indicate(focus,color=C['gold'],scale_factor=1.12),run_time=1.7)
            extra=1.7
        if b.section=='captain' and b.state==2:
            self.play(Rotate(focus,angle=TAU),run_time=1.5)
            extra=1.5
        self.play(Indicate(focus,color=C['gold'],scale_factor=1.07),run_time=2.05)
        for item in lines:self.play(FadeIn(item,shift=.06*UP),run_time=1.45)
        self.play(FadeIn(eq,shift=.08*UP),run_time=1.20)
        self.play(FadeIn(takeaway),run_time=1.05)
        self.play(Circumscribe(takeaway[-1],color=C['green'],buff=.10),run_time=1.1)
        spent=1.05+2.05+3*1.45+1.20+1.05+1.1+extra
        if budget>spent:self.wait(budget-spent)
        self.prev=(art,head,lines,eq,takeaway,count)

    def construct(self):
        for index,beat in enumerate(BEATS):self.render_beat(index,beat)
        self.play(*[FadeOut(p) for p in self.prev],run_time=1.0)
        end=VGroup(label('MÙA 1 · TƯ DUY ĐẾM VÀ LỰA CHỌN',0,.48,31,C['cyan'],True,12.15),
            label('HOÁN VỊ  •  CHỈNH HỢP  •  TỔ HỢP',0,-.36,23,C['gold'],True,12.0))
        self.play(FadeIn(end),run_time=1.4)
        self.wait(2.8)
