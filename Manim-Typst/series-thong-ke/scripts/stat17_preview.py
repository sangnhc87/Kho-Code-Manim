"""Pillow-only teaching storyboard: not an actual video frame."""
from pathlib import Path
import sys
from PIL import Image,ImageFont,ImageDraw
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat17.lesson import (X,Y,CURVED_Y,PRACTICE_X,PRACTICE_Y,statistics,fitted,
                           OUTLIER_Y,decimal)
W,H=1540,1860
BG='#0A1522'; PANEL='#10293B';EDGE='#355A71';WHITE='#EDF6FF'
CYAN='#56CBE9';GOLD='#FFD379';GREEN='#67DDB5';CORAL='#FF8E87';MUTED='#ADC6D5';PURPLE='#B7A9FC'
fonts=Path('/usr/share/fonts/truetype/dejavu')
normal=str(fonts/'DejaVuSans.ttf');bold=str(fonts/'DejaVuSans-Bold.ttf')
F1=ImageFont.truetype(bold,32);F2=ImageFont.truetype(bold,19)
F3=ImageFont.truetype(normal,17);F4=ImageFont.truetype(bold,14)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((47,30),'SANGMATH  |  THỐNG KÊ 10–12',font=F1,fill=CYAN)
d.text((47,80),'STAT17 – TƯƠNG QUAN & HỒI QUY',font=F1,fill=WHITE)
titles=(
    ('Từ hai đại lượng đến điểm','Tám quan sát giả lập (x, y)'),
    ('Ba kiểu tương quan','Dương / âm / phi tuyến'),
    ('Hệ số Pearson','Sxx=42; Sxy=36; r≈0,926'),
    ('Đường hồi quy tuyến tính','ŷ = 8/7 + (6/7)x'),
    ('Bình phương tối thiểu','Tổng bình phương phần dư'),
    ('Dự đoán và R bình phương','ŷ(5)≈5,43; R²≈0,857'),
    ('Ngoại lệ và tương quan','Thay 9 bằng 18; kiểm tra ảnh hưởng'),
    ('Bài tập có lời giải','ŷ=1+2x; r=1'),
)

def mini_plot(x,y,box,line=False,resid=False,outer=False):
    bx,by,bw,bh=box
    xmin=0;xmax=(6 if outer else 9);ymin=0;ymax=(12 if outer else 20 if max(y)>13 else 13)
    Xp=lambda xx:bx+(xx-xmin)/(xmax-xmin)*bw
    Yp=lambda yy:by+bh-(yy-ymin)/(ymax-ymin)*bh
    d.line((bx,by,bx,by+bh,bx+bw,by+bh),fill=MUTED,width=2)
    for t in range(1,5):
        xx=bx+bw*t/5; yy=by+bh*t/5
        d.line((xx,by,xx,by+bh),fill=EDGE,width=1)
        d.line((bx,yy,bx+bw,yy),fill=EDGE,width=1)
    if line:
        st=statistics(x,y)
        d.line((Xp(min(x)),Yp(fitted(min(x),st)),Xp(max(x)),Yp(fitted(max(x),st))),fill=GOLD,width=4)
        if resid:
            for xx,yy in zip(x,y):d.line((Xp(xx),Yp(yy),Xp(xx),Yp(fitted(xx,st))),fill=CORAL,width=2)
    for xx,yy in zip(x,y):
        px,py=Xp(xx),Yp(yy)
        d.ellipse((px-5,py-5,px+5,py+5),fill=CYAN)

for i,(title,sub) in enumerate(titles):
    row,col=divmod(i,2)
    x0=48+col*744;y0=159+row*391
    d.rounded_rectangle((x0,y0,x0+705,y0+356),radius=18,fill=PANEL,outline=EDGE,width=2)
    d.text((x0+18,y0+18),title,font=F2,fill=WHITE)
    d.text((x0+18,y0+322),sub,font=F4,fill=GOLD)
    if i==1:
        mini_plot(X,tuple(10-y for y in Y),(x0+115,y0+80,455,194),line=True)
    elif i==6:
        mini_plot(X,OUTLIER_Y,(x0+115,y0+80,455,194),line=True)
    elif i==7:
        mini_plot(PRACTICE_X,PRACTICE_Y,(x0+115,y0+80,455,194),line=True,outer=True)
    elif i in (0,2,3,4,5):
        mini_plot(X,Y,(x0+115,y0+80,455,194),line=i!=0,resid=i==4)
    else:
        mini_plot(X,CURVED_Y,(x0+115,y0+80,455,194))
d.text((50,H-99),'STORYBOARD THIẾT KẾ – KHÔNG PHẢI HÌNH RENDER MANIM',font=F3,fill=MUTED)
name='Thầy Nguyễn Văn Sang'
width=d.textbbox((0,0),name,font=F2)[2]
d.text(((W-width)/2,H-52),name,font=F2,fill=WHITE)
out=ROOT/'preview/stat17/STAT17_storyboard_8_chapters.png';out.parent.mkdir(parents=True,exist_ok=True)
im.save(out,optimize=True)
for i in range(8):
    row,col=divmod(i,2);x0=48+col*744;y0=159+row*391
    im.crop((x0,y0,x0+705,y0+356)).save(out.parent/f'STAT17_chapter_{i+1:02d}.png',optimize=True)
print('STAT17_PREVIEW_OK',out)
