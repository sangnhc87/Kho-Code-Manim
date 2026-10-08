#!/usr/bin/env python3
"""Poster of eight chapter sketches, not screenshots from rendered Manim."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from comb07_lesson_data import BEATS,CHAPTER_IDS,CHAPTER_LABELS
OUT=ROOT/'preview'/'comb07_v2';OUT.mkdir(parents=True,exist_ok=True)
BG='#0B1120'; P='#102038'; P2='#182B45'; TX='#EAF4FF'; CY='#22D3EE';GOLD='#FBBF24'; GR='#22C55E';RED='#EF4444';PU='#A78BFA';MUT='#98B0C7';LN='#37516A'
REG='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf';BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'

def font(s,b=False):return ImageFont.truetype(BOLD if b else REG,s)
def text(d,x,y,s,size=21,color=TX,b=False):d.text((x,y),str(s),font=font(size,b),fill=color)
def center(d,x,y,s,size=21,color=TX,b=True):
    bb=d.textbbox((0,0),s,font=font(size,b));text(d,x-(bb[2]-bb[0])/2,y-(bb[3]-bb[1])/2,s,size,color,b)
def card(d,x,y,s,color=CY,w=62,h=48):
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=9,fill=P2,outline=color,width=2)
    center(d,x,y,s,min(20,int(w/len(s)*1.5)),TX)

def drawing(d,key):
    if key in ('intro','ordered','groups','general'):
        for i,c in enumerate('ABCDE'):card(d,83+i*86,152,c,GR if i<3 else CY,54,50)
        if key=='intro':
            for j,c in enumerate('ABC'):card(d,167+j*86,296,c,GR,65,65)
            text(d,149,357,'ABC = BAC = CAB',19,GOLD,True)
        elif key=='ordered':
            for j,p in enumerate(['ABC','ACB','BAC','BCA','CAB','CBA']):
                card(d,123+(j%3)*135,263+(j//3)*61,p,PU,104,47)
            text(d,178,381,'6 dãy  →  1 nhóm',20,GR,True)
        elif key=='groups':
            from itertools import combinations
            for j,p in enumerate(combinations('ABCDE',3)):
                card(d,88+(j%5)*87,261+(j//5)*63,''.join(p),GR,72,46)
            text(d,156,390,'10 nhóm khác nhau',20,GOLD,True)
        else:
            for j,s in enumerate(('n','n-1','...','n-k+1')):card(d,88+j*116,278,s,PU,91,60)
            text(d,118,374,'Số nhóm = số dãy / k!',18,GR,True)
    elif key=='symmetry':
        for j,c in enumerate('ABCDEFG'):card(d,65+j*63,155,c,GR if j<2 else GOLD,45,47)
        card(d,156,293,'CHỌN 2',GR,154,68);card(d,357,293,'BỎ LẠI 5',GOLD,164,68)
        text(d,128,380,'C(n,k) = C(n,n-k)',22,GR,True)
    elif key=='constraint':
        from itertools import combinations
        for j,p in enumerate(combinations('ABCDEF',3)):
            x=76+(j%5)*92;y=160+(j//5)*62
            card(d,x,y,''.join(p),RED if 'A' in p and 'B' in p else GR,77,43)
        text(d,163,393,'20 - 4 = 16 đội',20,GOLD,True)
    elif key=='captain':
        for i,c in enumerate('ABCDEFGH'):card(d,64+i*59,159,c,GR if i<3 else CY,45,47)
        for j,c in enumerate('ABC'):card(d,155+j*104,291,c,GOLD if j==0 else GR,76,72)
        text(d,125,388,'56 đội × 3 trưởng = 168',19,GOLD,True)
    elif key=='practice':
        for j,c in enumerate('NNNNGGG'):
            card(d,71+j*63,153,c+str(j+1),CY if j<4 else PU,51,52)
        text(d,113,277,'Ít nhất 1 nữ: 31 đội',20,GOLD,True)
        text(d,113,333,'Đúng 2 nam 1 nữ: 18 đội',20,GR,True)

W,H=720,450
board=Image.new('RGB',(W*2,H*4),BG)
for i,ch in enumerate(CHAPTER_IDS):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((8,8,W-8,H-8),radius=16,fill=P,outline=LN,width=2)
    text(d,27,23,f'SANG MATH   ·   COMB07    /    {i+1:02d}',19,CY,True)
    d.line((20,62,W-20,62),fill=LN,width=2)
    text(d,27,72,CHAPTER_LABELS[ch],22,GOLD,True)
    d.rounded_rectangle((22,116,531,439),radius=12,fill=BG,outline=LN,width=2)
    drawing(d,ch)
    d.rounded_rectangle((542,116,699,439),radius=9,fill=BG,outline=LN,width=2)
    text(d,558,137,'NHỊP GIẢNG',16,PU,True)
    for j,b in enumerate([x for x in BEATS if x.section==ch][:5]):
        bname=b.heading
        while d.textbbox((0,0),bname,font=font(13))[2]>115:bname=bname[:-1]
        text(d,554,177+j*48,f'{j+1:02d} {bname}…',13,TX)
    text(d,558,415,'VIDEO 15+ PHÚT',13,GR,True)
    board.paste(im,((i%2)*W,(i//2)*H))
board.save(OUT/'storyboard_8_chapters.png')
print('Storyboard:',OUT/'storyboard_8_chapters.png',board.size)
