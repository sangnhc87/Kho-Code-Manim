"""An accurate storyboard graphic, not a rendered Manim scene."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat14.lesson import (QUEUE_A,QUEUE_B,QUEUE_OUTLIER,PA,PB,EXERCISE_A,
                           EXERCISE_B,EA,EB,CHAPTERS)
W,H=1480,1820
BG='#0A1522';PANEL='#10293B';EDGE='#355A71';WHITE='#EDF6FF';MUTED='#ADC6D5'
CYAN='#56CBE9';GOLD='#FFD379';GREEN='#67DDB5';CORAL='#FF8E87'
font_dir=Path('/usr/share/fonts/truetype/dejavu')
face=str(font_dir/'DejaVuSans.ttf');bold=str(font_dir/'DejaVuSans-Bold.ttf')
F1=ImageFont.truetype(bold,31);F2=ImageFont.truetype(bold,22)
F3=ImageFont.truetype(face,18);F4=ImageFont.truetype(bold,17)
Fsmall=ImageFont.truetype(face,15)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((55,28),'SANGMATH   |   THỐNG KÊ 12',fill=CYAN,font=F1)
d.text((55,77),'STAT14 – VẬN DỤNG THỐNG KÊ',fill=WHITE,font=F1)
labels=[('Hai quầy phục vụ','Cùng trung bình 8 phút'),('Phân tích phân tán','IQR 2 / 5; s² 1,2 / 15'),
    ('Đổi mục tiêu','Đạt ≤10 phút: A 10 / B 8'),('Một quan sát bất thường','Thay 10 thành 30 phút'),
    ('Gốc và ghép nhóm','Trung bình 7,1 và ≈7,6'),('Gộp hai nhóm','Trung bình có trọng số: 6,5'),
    ('Kết luận có giới hạn','Chỉ mô tả mẫu và tiêu chí'),('Bài tập tổng hợp','IQR C=1,5; IQR D=4')]
def coord(x,x0,w,lo,hi):return x0+int((x-lo)/(hi-lo)*w)
def plot_points(vals,y,x0,width,lo,hi,color):
    seen={};d.line((x0,y+50,x0+width,y+50),fill=EDGE,width=3)
    for v in vals:
        rank=seen.get(v,0);seen[v]=rank+1
        x=coord(v,x0,width,lo,hi)
        d.ellipse((x-7,y+30-15*rank,x+7,y+44-15*rank),fill=color)
def draw_box(prof,x0,y,width,lo,hi,color):
    xs=[coord(v,x0,width,lo,hi) for v in (prof.minimum,prof.q1,prof.median,prof.q3,prof.maximum)]
    d.line((xs[0],y,xs[-1],y),fill=color,width=4)
    d.rectangle((xs[1],y-19,xs[3],y+19),outline=color,width=4)
    d.line((xs[2],y-19,xs[2],y+19),fill=GOLD,width=4)
for i,(name,explain) in enumerate(labels):
    row,col=divmod(i,2);x=55+col*710;y=145+row*395
    d.rounded_rectangle((x,y,x+675,y+371),radius=19,fill=PANEL,outline=EDGE,width=2)
    d.text((x+20,y+17),f'{i+1:02d}  {name}',fill=WHITE,font=F2)
    d.text((x+18,y+325),explain,fill=GOLD,font=F4)
    x0=x+94
    if i in (0,):
        plot_points(QUEUE_A,y+94,x0,477,0,16,CYAN)
        plot_points(QUEUE_B,y+192,x0,477,0,16,CORAL)
        d.text((x+25,y+130),'A',font=F2,fill=CYAN);d.text((x+25,y+228),'B',font=F2,fill=CORAL)
    elif i==1:
        draw_box(PA,x0,y+143,475,0,16,CYAN);draw_box(PB,x0,y+235,475,0,16,CORAL)
        d.text((x+27,y+131),'A',font=F2,fill=CYAN);d.text((x+27,y+223),'B',font=F2,fill=CORAL)
    elif i==2:
        for j,(vals,color) in enumerate(((QUEUE_A,CYAN),(QUEUE_B,CORAL))):
            yy=y+129+82*j
            d.text((x+28,yy),'A' if j==0 else 'B',font=F2,fill=color)
            for z,v in enumerate(vals):
                d.rounded_rectangle((x0+z*47,yy,x0+z*47+35,yy+34),radius=5,
                    fill=color if v<=10 else EDGE)
    elif i==3:
        plot_points(QUEUE_A,y+115,x0,480,0,32,CYAN)
        plot_points(QUEUE_OUTLIER,y+208,x0,480,0,32,CORAL)
        d.text((x+20,y+146),'A',font=F2,fill=CYAN);d.text((x+20,y+238),'A’',font=F2,fill=CORAL)
    elif i==4:
        freqs=(6,18,14,2)
        for j,n in enumerate(freqs):
            bx=x+135+j*116;by=y+287;ht=int(n*10)
            d.rectangle((bx,by-ht,bx+67,by),fill=(CYAN,GREEN,GOLD,CORAL)[j])
            d.text((bx+16,by-ht-26),str(n),fill=WHITE,font=F4)
    elif i==5:
        for j,(n,color) in enumerate(((10,CYAN),(30,CORAL))):
            yy=y+131+j*84
            for z in range(n):
                bx=x+115+z*15
                d.rectangle((bx,yy,bx+10,yy+32),fill=color)
            d.text((x+24,yy),str(n),font=F2,fill=color)
    elif i==6:
        for j,title in enumerate(('Dữ liệu', 'Mục tiêu','Kiểm tra giới hạn','Kết luận có điều kiện')):
            yy=y+101+j*54
            d.rounded_rectangle((x+83,yy,x+591,yy+41),radius=9,outline=GREEN,width=2)
            d.text((x+114,yy+9),title,fill=WHITE,font=F4)
    else:
        draw_box(EA,x0,y+137,480,0,16,CYAN)
        draw_box(EB,x0,y+235,480,0,16,CORAL)
        d.text((x+26,y+127),'C',font=F2,fill=CYAN)
        d.text((x+26,y+223),'D',font=F2,fill=CORAL)
d.text((55,H-102),'STORYBOARD THIẾT KẾ – CHƯA PHẢI KHUNG HÌNH RENDER',fill=MUTED,font=F3)
footer='Thầy Nguyễn Văn Sang';width=d.textbbox((0,0),footer,font=F2)[2]
d.text(((W-width)//2,H-56),footer,font=F2,fill=WHITE)
p=ROOT/'preview/stat14/STAT14_storyboard_8_chapters.png'
p.parent.mkdir(parents=True,exist_ok=True)
im.save(p,optimize=True)
print('STAT14_STORYBOARD_OK',p,W,H)
