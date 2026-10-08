#!/usr/bin/env python3
"""Static eight-chapter storyboard; NOT actual Manim render frames."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb06_lesson_data import BEATS,CHAPTER_IDS,CHAPTER_LABELS
OUT=ROOT/'preview'/'comb06_v2';OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
B='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
BG='#0B1120';P='#102039';CY='#22D3EE';YL='#FBBF24';PU='#A78BFA';GR='#22C55E';RD='#EF4444';LN='#37516A';TX='#EEF4FF';MU='#AAB9CF'

def f(n,b=False):return ImageFont.truetype(B if b else F,n)
def txt(d,pos,s,size=20,color=TX,bold=False):d.text(pos,str(s),font=f(size,bold),fill=color)
def centered(d,x,y,s,size=20,color=TX,bold=True):
    box=d.textbbox((0,0),str(s),font=f(size,bold));txt(d,(x-(box[2]-box[0])/2,y-(box[3]-box[1])/2-4),s,size,color,bold)
def pill(d,x,y,s,color=CY,w=75,h=52,sz=22):
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=11,fill='#172A43',outline=color,width=2)
    centered(d,x,y,s,sz,TX)
def wrap(d,x,y,text,width,size=19,leading=9,color=TX):
    acc='';lines=[]
    for w in text.split():
        attempt=(acc+' '+w).strip()
        if acc and d.textbbox((0,0),attempt,font=f(size))[2]>width:lines.append(acc);acc=w
        else:acc=attempt
    if acc:lines.append(acc)
    for i,s in enumerate(lines):txt(d,(x,y+i*(size+leading)),s,size,color)
    return len(lines)

def drawing(d,ch):
    if ch in ('intro','slots','restrict','compare','practice'):
        for i,c in enumerate('ABCDEFG' if ch=='restrict' else 'ABCDEF'):
            pill(d,81+i*(55 if ch=='restrict' else 65),178,c,RD if ch=='restrict' and c=='A' else CY,44,42,17)
        roles=['NHẤT','NHÌ','BA'] if ch!='restrict' else ['TRƯỞNG','PHÓ','THƯ KÝ']
        values=['A','B','C'] if ch!='restrict' else ['B','A','C']
        for j,(role,v) in enumerate(zip(roles,values)):
            x=105+j*133
            pill(d,x,312,v,GR if j<2 else YL,79,64,29)
            centered(d,x,369,role,17,MU)
        centered(d,245,438,{'intro':'6 THÍ SINH · 3 GIẢI THƯỞNG','slots':'6 × 5 × 4 = 120','restrict':'A CẤM LÀM TRƯỞNG: 180','compare':'NHÓM ≠ PHÂN VAI','practice':'VẬN DỤNG NHIỀU ĐIỀU KIỆN'}.get(ch,''),17,YL)
    elif ch=='tree':
        d.ellipse((52,244,67,259),fill=CY)
        for j,c in enumerate('ABCDEF'):
            y=127+j*49
            d.line((62,251,160,y),fill=MU,width=2);pill(d,183,y,c,CY,48,37,17)
        for j,c in enumerate('BCDEF'):
            y=141+j*58;d.line((209,127,303,y),fill=LN,width=2);pill(d,327,y,c,YL,48,34,15)
        d.line((352,141,398,141),fill=GR,width=3)
        txt(d,(366,110),'×4',20,GR,True)
        txt(d,(88,447),'6 nhánh × 5 nhánh × 4 lá',20,YL,True)
    elif ch=='general':
        for i,(top,bottom) in enumerate(zip(['1','2','3','…','k'],['n','n−1','n−2','…','n−k+1'])):
            x=76+i*85;pill(d,x,248,top,CY,62,59,22);centered(d,x,321,bottom,16,YL)
        txt(d,(73,403),'A trên n, dưới k = n! / (n−k)!',19,GR,True)
    elif ch=='digits':
        for i,c in enumerate('01234'):pill(d,94+i*79,179,c,RD if i==0 else CY,58,55,26)
        for j,v in enumerate(('1','0','2')):
            x=127+j*115;pill(d,x,317,v,GR,84,75,32);centered(d,x,383,['TRĂM','CHỤC','ĐƠN VỊ'][j],16,MU)
        txt(d,(114,442),'4 × 4 × 3 = 48 số',20,YL,True)


def one(ch,beat):
    im=Image.new('RGB',(960,540),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((15,61,454,502),radius=16,fill=P,outline=LN,width=2)
    d.rounded_rectangle((468,61,946,502),radius=16,fill=P,outline=LN,width=2)
    txt(d,(23,14),'SANG MATH / MANIM - TYPST',20,CY,True)
    txt(d,(727,14),'COMB06 V2',20,MU,True)
    txt(d,(28,71),'MÔ HÌNH TRỰC QUAN',17,CY,True)
    drawing(d,ch)
    txt(d,(485,81),CHAPTER_LABELS[ch],16,PU,True)
    wrap(d,486,125,beat.heading,432,22,8,YL)
    y=194
    for line in beat.lines:
        n=wrap(d,491,y,'• '+line,427,19,6)
        y+=max(62,n*25+12)
    d.line((490,414,923,414),fill=LN,width=2)
    wrap(d,490,435,beat.takeaway,427,19,7,GR)
    return im

sheet=Image.new('RGB',(1920,2160),BG)
for i,ch in enumerate(CHAPTER_IDS):
    beat=next(b for b in BEATS if b.section==ch and b.state==2)
    im=one(ch,beat);im.save(OUT/f'{i+1:02}_{ch}.png');sheet.paste(im,((i%2)*960,(i//2)*540))
sheet.save(OUT/'storyboard_8_chapters.png',optimize=True)
print('STORYBOARD_OK 8 chapters',OUT/'storyboard_8_chapters.png')
