"""Create honest static storyboard previews; not a Manim render."""
from __future__ import annotations
from pathlib import Path
import math,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb11_lesson_data import CHAPTER_LABELS, BEATS
OUT=ROOT/'preview'/'comb11_v2';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(FONT).is_file(): FONT='DejaVuSans.ttf';BOLD='DejaVuSans-Bold.ttf'

cases=[
('ABCD','4! : 4 = 6','PHÉP QUAY','A B C D','B C D A'),
('ABCDEF','5! = 120','CỐ ĐỊNH A','A ở vị trí mốc','5 người còn lại'),
('ABCDEF','120 : 2 = 60*','PHẢN XẠ GƯƠNG','120 nếu giữ hướng','*60 chỉ khi cho phép lật'),
('ABCDEF','2 × 4! = 48','A B LIỀN NHAU','[AB] là một khối','Hai thứ tự trong khối'),
('ACBDEF','120 − 48 = 72','A B KHÔNG KỀ','B tránh hai ghế cạnh A','3 × 4! = 72'),
('MFMFMF','2 × 3! = 12','NAM NỮ XEN KẼ','2 cách xếp nam','6 cách xếp nữ'),
('ABCabc','120 − 144 + 72 − 16','BA CẶP KHÔNG KỀ','Gộp, rồi bù trừ','Kết quả: 32'),
('ABCDEF','4! = 24','A ĐỐI DIỆN B','Giữ A làm mốc','B ngồi ở ghế đối diện')]

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

def center(draw,xy,text,size,color,bold=False):
    draw.text(xy,text,font=font(size,bold),fill=color,anchor='mm')

def rounded(draw,box,fill,outline=None,radius=18,width=2):
    draw.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def thumb(c,j):
    im=Image.new('RGB',(1600,900),'#0b1120');d=ImageDraw.Draw(im)
    rounded(d,(28,30,1572,111),'#14263e',radius=20)
    d.text((66,53),'SANG MATH  /  ĐẠI SỐ TỔ HỢP',font=font(26,True),fill='#67e8f9')
    d.text((1540,53),f'COMB11 · {j+1:02d}/08',font=font(26,True),fill='#a8b9cc',anchor='ra')
    rounded(d,(30,142,733,828),'#101f33','#2e4862',16)
    rounded(d,(753,142,1570,828),'#101f33','#2e4862',16)
    d.text((69,178),c[2],font=font(28,True),fill='#67e8f9')
    cx,cy=381,487
    r=206
    d.ellipse((cx-r-30,cy-r-30,cx+r+30,cy+r+30),outline='#2e4862',width=7,fill='#172a43')
    d.ellipse((cx-r+63,cy-r+63,cx+r-63,cy+r-63),outline='#2e4862',width=4)
    alphabet=c[0]
    for i,s in enumerate(alphabet):
        th=math.pi/2-2*math.pi*i/len(alphabet)
        x=int(cx+r*math.cos(th));y=int(cy-r*math.sin(th))
        tone='#22d3ee'
        if j==5:tone='#a78bfa' if s=='F' else '#22d3ee'
        elif s.upper()=='A':tone='#fbbf24'
        elif s.upper()=='B':tone='#a78bfa'
        rounded(d,(x-42,y-42,x+42,y+42),'#233c57',tone,14,4)
        center(d,(x,y),s,36,'#f8fafc',True)
    center(d,(cx,cy),'BÀN TRÒN',25,'#fbbf24',True)
    d.text((794,190),CHAPTER_LABELS[BEATS[6*j].section],font=font(23,True),fill='#a78bfa')
    d.text((794,282),'MÔ HÌNH',font=font(24,True),fill='#e6f4ff')
    for i,ln in enumerate((c[3],c[4])):d.text((794,347+i*66),'• '+ln,font=font(26),fill='#d8e9fa')
    d.line((794,530,1529,530),fill='#2e4862',width=4)
    d.text((794,560),'KẾT QUẢ',font=font(24,True),fill='#fbbf24')
    d.text((794,632),c[1],font=font(40,True),fill='#22d3ee')
    d.text((45,848),'STORYBOARD TĨNH – CHƯA PHẢI FRAME MANIM',font=font(20),fill='#90a7c0')
    return im

ims=[]
for j,c in enumerate(cases):
    im=thumb(c,j)
    im.save(OUT/f'COMB11_{j+1:02d}.png')
    ims.append(im.resize((800,450)))
sheet=Image.new('RGB',(1600,1800),'#0b1120')
for j,pic in enumerate(ims):sheet.paste(pic,((j%2)*800,(j//2)*450))
sheet.save(OUT/'storyboard_8_chapters.png')
print('STORYBOARD_OK panels=8 total_size=1600x1800')
