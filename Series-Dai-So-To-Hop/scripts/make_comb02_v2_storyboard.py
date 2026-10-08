#!/usr/bin/env python3
"""Static reference artwork only: NOT frames rendered by Manim."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb02_lesson_data import BEATS,CHAPTER_LABELS
OUT=ROOT/'preview'/'comb02_v2';OUT.mkdir(parents=True,exist_ok=True)
COL={'bg':'#0B1120','panel':'#101F33','line':'#2E4862','text':'#ECF4FF','muted':'#A8B9CC',
     'cyan':'#22D3EE','gold':'#FBBF24','purple':'#A78BFA','green':'#22C55E','red':'#EF4444'}
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
def f(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)

def rounded(d,xy,fill,outline=None,r=14,w=2):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline or COL['line'],width=w)

def centered(d,xy,string,fill,size=21,bold=False):
    box=d.textbbox((0,0),string,font=f(size,bold))
    d.text((xy[0]-(box[2]-box[0])/2,xy[1]-(box[3]-box[1])/2-3),string,font=f(size,bold),fill=fill)

def chip(d,label,x,y,color,width=91,height=49):
    rounded(d,(x-width/2,y-height/2,x+width/2,y+height/2),'#172A43',color,10,2)
    centered(d,(x,y),label,COL['text'],21,True)

def diagram(d,key):
    # Illustrated from the mathematical model; not a screenshot of Manim.
    if key=='outfit':
        centered(d,(300,155),'CHỌN MỘT ÁO VÀ MỘT QUẦN',COL['cyan'],23,True)
        for i,x in enumerate([160,300,440]):chip(d,'A'+str(i+1),x,235,COL['cyan'])
        for j,x in enumerate([230,370]):chip(d,'Q'+str(j+1),x,323,COL['gold'])
        for k,(a,q) in enumerate([(a,q) for a in range(1,4) for q in range(1,3)]):
            chip(d,f'A{a}–Q{q}',150+(k%3)*148,417+(k//3)*72,COL['purple'],119)
    if key in ('grid','forbidden'):
        centered(d,(308,157),'MỖI Ô LÀ MỘT KẾT QUẢ',COL['cyan'],23,True)
        for j,x in enumerate([300,445]):centered(d,(x,210),f'Q{j+1}',COL['gold'],23,True)
        for i in range(3):
            y=275+i*94
            centered(d,(143,y),f'A{i+1}',COL['cyan'],23,True)
            for j,x in enumerate([300,445]):
                invalid=key=='forbidden' and i==1 and j==1
                chip(d,f'A{i+1},Q{j+1}',x,y,COL['red'] if invalid else COL['green'],116,60)
                if invalid:d.line((x-38,y-22,x+38,y+22),fill=COL['red'],width=5)
        centered(d,(302,566),'6 bộ' if key=='grid' else '6 - 1 = 5 bộ',COL['green'],24,True)
    if key in ('tree','uneven'):
        centered(d,(300,133),'MỘT ĐƯỜNG ĐI = MỘT KẾT QUẢ',COL['cyan'],21,True)
        d.ellipse((97,337,113,353),fill=COL['text'])
        count=(2,2,2) if key=='tree' else (2,1,3)
        for i,yy in enumerate((241,356,473)):
            d.line((110,345,232,yy),fill=COL['cyan'],width=4)
            chip(d,f'A{i+1}',269,yy,COL['cyan'],72,42)
            cnt=count[i]
            for j in range(cnt):
                x=447;to_y=yy+(j-(cnt-1)/2)*37
                d.line((305,yy,x-51,to_y),fill=COL['gold'],width=3)
                chip(d,f'Q{j+1}',x,to_y,COL['gold'],76,34)
        centered(d,(309,570),'2 + 2 + 2 = 6' if key=='tree' else '2 + 1 + 3 = 6',COL['green'],24,True)
    if key=='general':
        centered(d,(304,159),'CÔNG VIỆC QUA HAI BƯỚC',COL['cyan'],23,True)
        for i,lab in enumerate(['X₁','X₂','...','Xₘ']):
            y=244+i*91
            if lab=='...':centered(d,(250,y),'...',COL['muted'],35,True);continue
            chip(d,lab,214,y,COL['cyan'],113,54)
            d.line((270,y,355,y),fill=COL['gold'],width=3)
            chip(d,'n cách',430,y,COL['gold'],114,54)
        centered(d,(300,577),'N = m × n',COL['green'],25,True)
    if key=='hat':
        centered(d,(302,158),'MỖI BỘ CÓ THÊM 2 MŨ',COL['cyan'],24,True)
        chip(d,'M1',231,226,COL['purple']);chip(d,'M2',374,226,COL['purple'])
        for i in range(6):
            x=145+(i%3)*157;y=330+(i//3)*99
            chip(d,f'A{i//2+1},Q{i%2+1}',x,y,COL['cyan'],123,58)
            centered(d,(x,y+40),'× 2 mũ',COL['gold'],16)
        centered(d,(302,564),'3 × 2 × 2 = 12',COL['green'],26,True)
    if key=='quiz':
        centered(d,(300,149),'4 ÁO · 3 QUẦN · HAI CẶP CẤM',COL['cyan'],20,True)
        for j,x in enumerate([240,347,454]):centered(d,(x,213),f'Q{j+1}',COL['gold'],21,True)
        for i in range(4):
            y=270+i*75
            centered(d,(144,y),f'A{i+1}',COL['cyan'],23,True)
            for j,x in enumerate([240,347,454]):
                bad=i==0 and j>0
                chip(d,'×' if bad else 'OK',x,y,COL['red'] if bad else COL['green'],67,50)
        centered(d,(300,587),'4 × 3 - 2 = 10',COL['green'],24,True)

def make(key,beat):
    img=Image.new('RGB',(1200,675),COL['bg']);d=ImageDraw.Draw(img)
    rounded(d,(35,84,562,618),COL['panel'])
    rounded(d,(575,84,1165,618),COL['panel'])
    d.text((45,23),'SANG MATH  /  ĐẠI SỐ TỔ HỢP',font=f(27,True),fill=COL['cyan'])
    d.text((827,23),'COMB02 · QUY TẮC NHÂN',font=f(24,True),fill=COL['muted'])
    diagram(d,key)
    centered(d,(868,127),CHAPTER_LABELS[key],COL['purple'],22,True)
    centered(d,(868,181),beat.heading,COL['gold'],27,True)
    for j,line in enumerate(beat.lines):centered(d,(868,252+j*58),line,COL['text'],24)
    d.line((630,486,1110,486),fill=COL['line'],width=2)
    takeaway=beat.takeaway
    size=22
    while d.textbbox((0,0),takeaway,font=f(size,True))[2]>490 and size>15:size-=1
    centered(d,(868,548),takeaway,COL['green'],size,True)
    centered(d,(600,649),'STORYBOARD TĨNH · KHÔNG PHẢI FRAME RENDER MANIM',COL['muted'],15)
    img.save(OUT/f'{key}.png')
    return img

def main():
    visuals=[]
    for key in CHAPTER_LABELS:
        beat=next(b for b in BEATS if b.section==key and b.state==(5 if key=='quiz' else 1))
        im=make(key,beat)
        visuals.append(ImageOps.contain(im,(640,360)))
    board=Image.new('RGB',(1280,1440),COL['bg'])
    for i,im in enumerate(visuals):board.paste(im,((i%2)*640,(i//2)*360))
    board.save(OUT/'storyboard_8_chapters.png')
    print('STORYBOARD_OK 8 frames, contact_sheet=',OUT/'storyboard_8_chapters.png')

if __name__=='__main__':main()
