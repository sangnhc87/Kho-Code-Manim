"""Generate a design-only eight-chapter contact sheet (not an MP4 frame)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat12.lesson import CHAPTERS,MAIN,OTHER,FREQ,OTHER_FREQ
W,H=1440,1680
BG='#0a1522';PANEL='#10293b';LINE='#34566c';FG='#edf6ff';MUTED='#a9c5d4';GOLD='#ffd379';CYAN='#56cbe9';GREEN='#67ddb5';CORAL='#ff8e87'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(font).exists():
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f12=ImageFont.truetype(font,20);f16=ImageFont.truetype(font,25);f22=ImageFont.truetype(bold,29);f28=ImageFont.truetype(bold,38)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((64,34),'SANGMATH  |  THỐNG KÊ 12',font=f28,fill=CYAN)
d.text((64,93),'PHƯƠNG SAI VÀ ĐỘ LỆCH CHUẨN CỦA MẪU SỐ LIỆU GHÉP NHÓM',font=f22,fill=FG)
short=[
('Dữ liệu gốc và ước lượng','40 quan sát | 4 lớp'),
('Trung điểm và trung bình','5, 7, 9, 11  →  7,6'),
('Độ lệch có trọng số','Tổng bình phương = 97,6'),
('Công thức rút gọn','60,2 − 7,6² = 2,44'),
('Cùng tâm, khác phân tán','A = 2,44   |   B = 4,44'),
('Biến đổi và đơn vị','Nhân 2  →  s² nhân 4'),
('Ngoại lệ và thông tin mất','2,29  →  14,94 (gốc)'),
('Bài toán ngược','x = 2   |   s² ≈ 3,36')]
for idx,(name,sub) in enumerate(short):
    row=idx//2;col=idx%2
    x=54+col*704;y=155+row*359
    d.rounded_rectangle((x,y,x+673,y+328),radius=22,fill=PANEL,outline=LINE,width=2)
    d.rounded_rectangle((x+19,y+16,x+654,y+63),radius=12,fill='#173b50')
    d.text((x+33,y+21),f'{idx+1:02d}  {name}',font=f16,fill=FG)
    d.text((x+34,y+273),sub,font=f22,fill=GOLD)
    x0=x+53;ybase=y+234;bw=99
    counts=FREQ if idx not in (4,7) else OTHER_FREQ if idx==4 else (2,8,6,4)
    for j,n in enumerate(counts):
        hh=round(142*n/19)
        fill=(CYAN,GREEN,'#b7a9fc',CORAL)[j]
        d.rounded_rectangle((x0+j*145,ybase-hh,x0+j*145+bw,ybase),radius=5,fill=fill)
        d.text((x0+j*145+31,ybase+8),str(n),font=f12,fill=MUTED)
    if idx in (0,1,3,4):
        t=x0+245
        d.line((t,y+83,t,ybase),fill=GOLD,width=3)
    if idx==2:
        for j,n in enumerate((40.56,6.48,27.44,23.12)):
            yy=ybase-round(n*2.4)
            d.line((x0+j*145,ybase,x0+j*145,yy),fill=GOLD,width=5)
    if idx==6:
        d.ellipse((x+598,y+87,x+620,y+109),fill=CORAL)
footer='Thầy Nguyễn Văn Sang'
bbox=d.textbbox((0,0),footer,font=f16)
d.text(((W-(bbox[2]-bbox[0]))/2,H-37),footer,font=f16,fill=MUTED)
d.text((54,H-76),'STORYBOARD THIẾT KẾ • KHÔNG PHẢI ẢNH RENDER',font=f12,fill=MUTED)
target=ROOT/'preview/stat12/STAT12_storyboard_8_chapters.png';target.parent.mkdir(parents=True,exist_ok=True)
im.save(target,optimize=True)
print('STAT12_STORYBOARD',target,im.size)
