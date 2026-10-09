"""Eight chapter concept sketches generated with Pillow. NOT a rendered frame."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat18.lesson import (TRUE_P,trials,sd_sample_proportion,approx_interval,
                           PRACTICE_YES,PRACTICE_N)
W,H=1540,1860
BG='#0A1522';PANEL='#10293B';EDGE='#355A71';WHITE='#EDF6FF'
CYAN='#56CBE9';GOLD='#FFD379';GREEN='#67DDB5';CORAL='#FF8E87';MUTED='#ADC6D5';PURPLE='#B7A9FC'
font_path=Path('/usr/share/fonts/truetype/dejavu')
font=str(font_path/'DejaVuSans.ttf');bold=str(font_path/'DejaVuSans-Bold.ttf')
f_title=ImageFont.truetype(bold,29);f_panel=ImageFont.truetype(bold,20)
f_plain=ImageFont.truetype(font,17);f_small=ImageFont.truetype(bold,13)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((45,28),'SANGMATH  |  THỐNG KÊ 10–12',font=f_title,fill=CYAN)
d.text((45,77),'STAT18 – LẤY MẪU, THIÊN LỆCH VÀ MÔ PHỎNG',font=f_title,fill=WHITE)
chs=[('Quần thể và mẫu','1.000 học sinh: 400 chọn A'),
     ('Lấy mẫu ngẫu nhiên','n=20: 7/20; n=80: 37/80'),
     ('Khảo sát tự nguyện','Quần thể 40% · Tự nguyện 70%'),
     ('Dao động lấy mẫu','Mô phỏng 300 lần rút'),
     ('Cỡ mẫu và sai số chuẩn','n tăng: độ dao động giảm'),
     ('Khoảng ước lượng','44% và khoảng xấp xỉ'),
     ('Kiểm tra độ tin cậy','Ai được chọn? Ai vắng mặt?'),
     ('Bài tập kết thúc','Ngẫu nhiên 44%, thuận tiện 75%')]

def bar_rect(x0,y0,bw,bh,values):
    for j,(v,color) in enumerate(values):
        x=x0+(j+.5)*bw/len(values)
        height=bh*v
        d.rounded_rectangle((x-30,y0+bh-height,x+30,y0+bh),radius=4,fill=color)
        d.text((x-16,y0+bh-height-22),f'{v*100:.0f}%',font=f_small,fill=color)
    d.line((x0,y0+bh,x0+bw,y0+bh),fill=MUTED,width=2)

for i,(title,sub) in enumerate(chs):
    row,col=divmod(i,2)
    x0,y0=48+col*744,156+row*393
    d.rounded_rectangle((x0,y0,x0+705,y0+353),radius=17,fill=PANEL,outline=EDGE,width=2)
    d.text((x0+19,y0+18),title,font=f_panel,fill=WHITE)
    d.text((x0+18,y0+318),sub,font=f_small,fill=GOLD)
    if i in (0,1,6):
        for j in range(100):
            xx=x0+136+j%10*43;yy=y0+77+j//10*20
            if i==1: color=GREEN if j<35 else PURPLE
            elif i==6:color=CYAN if j<60 else CORAL
            else:color=GREEN if j<40 else PURPLE
            d.ellipse((xx-6,yy-6,xx+6,yy+6),fill=color)
    elif i in (2,7):
        bar_rect(x0+150,y0+76,420,195,[(.4,GREEN),(.7,CORAL)] if i==2 else [(.44,CYAN),(.75,CORAL)])
    elif i in (3,4):
        vals=trials(20) if i==3 else trials(80)
        count=[0]*20
        for p in vals:count[min(19,int(p*20+1e-9))]+=1
        maxcnt=max(count)
        for j,cnt in enumerate(count):
            height=190*cnt/maxcnt
            x=x0+112+j*23
            d.rectangle((x,y0+265-height,x+18,y0+265),fill=CYAN if i==3 else GREEN)
        d.line((x0+112+8*23,y0+65,x0+112+8*23,y0+266),fill=GOLD,width=3)
    elif i==5:
        p,l,h=approx_interval(PRACTICE_YES,PRACTICE_N)
        x=lambda v:x0+90+v*520
        d.line((x(0),y0+185,x(1),y0+185),fill=MUTED,width=4)
        d.line((x(l),y0+185,x(h),y0+185),fill=GREEN,width=14)
        d.ellipse((x(p)-9,y0+176,x(p)+9,y0+194),fill=CYAN)
        d.text((x0+200,y0+108),'37,1%  –  50,9%',font=f_panel,fill=GREEN)
name='Thầy Nguyễn Văn Sang'
w=d.textbbox((0,0),name,font=f_panel)[2]
d.text(((W-w)/2,H-52),name,font=f_panel,fill=WHITE)
d.text((50,H-96),'PHÁC THẢO THIẾT KẾ — KHÔNG PHẢI HÌNH RENDER MANIM',font=f_plain,fill=MUTED)
out=ROOT/'preview/stat18/STAT18_storyboard_8_chapters.png'
out.parent.mkdir(parents=True,exist_ok=True)
im.save(out,optimize=True)
for i in range(8):
    row,col=divmod(i,2);x0=48+col*744;y0=156+row*393
    im.crop((x0,y0,x0+705,y0+353)).save(out.parent/f'STAT18_chapter_{i+1:02d}.png',optimize=True)
print('STAT18_PREVIEW_OK',out)
