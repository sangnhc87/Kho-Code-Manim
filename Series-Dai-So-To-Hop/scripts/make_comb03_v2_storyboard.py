#!/usr/bin/env python3
"""Produce static storyboard references (not Manim-rendered movie frames)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb03_lesson_data import (BEATS, CHAPTER_IDS, CHAPTER_LABELS,
    OMEGA_3,OMEGA_4,EXACTLY_TWO_N,NO_ADJACENT_N,NO_ADJACENT_4)
OUT=ROOT/'preview'/'comb03_v2'
OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
C={'bg':'#0B1120','panel':'#102039','cyan':'#22D3EE','gold':'#FBBF24',
'purple':'#A78BFA','text':'#EEF5FF','muted':'#9DB3CB','red':'#EF4444',
'green':'#22C55E','line':'#34516E'}

def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)

def label(d,x,y,s,sz=21,color='text',bold=False):
    d.text((x,y),str(s),font=f(sz,bold),fill=C.get(color,color))

def wrap(d,x,y,s,max_width,size=21,leading=7,color='text'):
    buf='';line=0
    for word in s.split():
        attempt=(buf+' '+word).strip()
        if d.textbbox((0,0),attempt,font=f(size))[2]>max_width and buf:
            label(d,x,y+line*(size+leading),buf,size,color)
            line+=1;buf=word
        else:buf=attempt
    if buf:label(d,x,y+line*(size+leading),buf,size,color)
    return line+1

def capsule(d,x,y,t,col='cyan',w=88,h=35,sz=18):
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=9,
                        fill='#172A43',outline=C[col],width=2)
    box=d.textbbox((0,0),t,font=f(sz,True))
    d.text((x-(box[2]-box[0])/2,y-(box[3]-box[1])/2-4),t,
           font=f(sz,True),fill=C['text'])

def tree(d,section):
    root=(84,267)
    a={'N':(160,173),'S':(160,365)}
    b={'NN':(254,125),'NS':(254,221),'SN':(254,317),'SS':(254,413)}
    c={v:(362,103+i*47) for i,v in enumerate(OMEGA_3)}
    d.ellipse((root[0]-5,root[1]-5,root[0]+5,root[1]+5),fill=C['text'])
    for k,(x,y) in a.items():
        d.line((root[0],root[1],x,y),fill=C['cyan' if k=='N' else 'gold'],width=3)
        capsule(d,x,y,k,'cyan' if k=='N' else 'gold',52,34)
    for k,(x,y) in b.items():
        px,py=a[k[0]]
        d.line((px,py,x,y),fill=C['cyan' if k[1]=='N' else 'gold'],width=2)
        capsule(d,x,y,k,'cyan' if k[-1]=='N' else 'gold',57,32,16)
    for k,(x,y) in c.items():
        px,py=b[k[:2]]
        d.line((px,py,x,y),fill=C['line'],width=2)
        col='cyan'
        if section=='exacttwo':col='green' if k in EXACTLY_TWO_N else 'line'
        elif section=='noadjacent':col='green' if k in NO_ADJACENT_N else 'red'
        elif section=='proof':col='green' if k=='NSN' else 'line'
        capsule(d,x,y,k,col,78,33,16)

def grid(d,kind):
    if kind=='expansion':
        items=OMEGA_4;cols=4;w=86;gap=12
    else:
        items=OMEGA_3;cols=2;w=141;gap=26
    for i,v in enumerate(items):
        x=115+(i%cols)*(w+gap)
        y=116+(i//cols)*85
        col='green' if (kind=='expansion' and v in NO_ADJACENT_4) else 'cyan'
        if kind=='omega':col='gold' if i%2 else 'cyan'
        capsule(d,x,y,v,col,w,56,19)

def draw_panel(ch,beat):
    im=Image.new('RGB',(960,540),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((18,57,452,494),radius=17,fill=C['panel'],outline=C['line'],width=2)
    d.rounded_rectangle((466,57,942,494),radius=17,fill=C['panel'],outline=C['line'],width=2)
    label(d,26,12,'SANG MATH / MANIM - TYPST',20,'cyan',True)
    label(d,650,13,'COMB03 V2',19,'muted',True)
    label(d,28,65,'MÔ HÌNH TRỰC QUAN',18,'cyan',True)
    if ch in ('growth','exacttwo','noadjacent','proof'):tree(d,ch)
    elif ch in ('omega','expansion'):grid(d,ch)
    elif ch=='intro':
        for i,k in enumerate('NSN'):
            capsule(d,118+i*119,234,k,'cyan' if k=='N' else 'gold',73,80,38)
            label(d,107+i*119,293,str(i+1),18,'muted')
        label(d,94,380,'N  /  S  /  N',26,'gold',True)
    else:
        for i,(key,num) in enumerate(zip(['M1','M2','M3'],[2,1,3])):
            yy=141+i*126
            capsule(d,145,yy,key,'cyan',86,51,22)
            for j in range(num):
                ly=yy+(j-(num-1)/2)*36
                d.line((190,yy,280,ly),fill=C['line'],width=2)
                capsule(d,316,ly,'D'+str(j+1),'gold',68,27,15)
    label(d,489,83,CHAPTER_LABELS[ch],18,'purple',True)
    label(d,489,126,beat.heading,24,'gold',True)
    y=189
    for line in beat.lines:
        n=wrap(d,489,y,line,425,20)
        y+=max(56,n*27+12)
    d.line((489,405,913,405),fill=C['line'],width=2)
    wrap(d,490,430,beat.takeaway,423,20,color='green')
    return im


def main():
    mapping={'intro':0,'growth':3,'omega':1,'exacttwo':4,
             'noadjacent':3,'proof':2,'expansion':4,'practice':5}
    sheet=Image.new('RGB',(1920,2160),C['bg'])
    for i,ch in enumerate(CHAPTER_IDS):
        beat=next(b for b in BEATS if b.section==ch and b.state==mapping[ch])
        im=draw_panel(ch,beat)
        im.save(OUT/f'{i+1:02}_{ch}.png')
        sheet.paste(im,((i%2)*960,(i//2)*540))
    sheet.save(OUT/'storyboard_8_chapters.png',optimize=True)
    print('STORYBOARD_OK chapters=8 sheet=',OUT/'storyboard_8_chapters.png')

if __name__=='__main__':main()
