"""Static design previews only. NOT rendered Manim footage."""
from __future__ import annotations
import math
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat03.lesson import CHAPTERS, FREQUENCY, SORTED
BG='#091421';PANEL='#102739';CYAN='#54C8E9';GOLD='#FFD47A';GREEN='#63D9B4';MUTED='#AAC8D9';WHITE='#EEF8FF';CORAL='#FF8B84'
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
if not Path(FONT).exists():FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(BOLD).exists():BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def write(d,xy,s,size=24,color=WHITE,bold=False):d.text(xy,str(s),font=f(size,bold),fill=color)

def graphics(d,chap):
    if chap in (1,2,4,7):
        total=max(FREQUENCY.values()); lo=160; axis=685
        x0=105
        for idx,(score,freq) in enumerate(FREQUENCY.items()):
            x=x0+idx*100;h=int(freq/total*295)
            d.rounded_rectangle((x,axis-h,x+62,axis),radius=6,fill=GREEN if score==7 else CYAN)
            write(d,(x+13,axis-h-36),freq,24,GOLD if score==7 else WHITE,True)
            write(d,(x+21,axis+14),score,24,MUTED)
        if chap==1:write(d,(146,266),'40 điểm     |     TB = 7,1     |     TV = 7     |     Mo = 7',28,GOLD,True)
        if chap==2:write(d,(125,258),'(4×2 + 5×4 + … + 10×2) / 40 = 7,1',29,GOLD,True)
        if chap==4:write(d,(190,262),'Mốt = 7    •    tần số = 10',32,GOLD,True)
        if chap==7:write(d,(184,258),'Mỗi điểm +2  →  TB +2, TV +2, Mo +2',24,GOLD,True)
    elif chap==3:
        for i,v in enumerate(SORTED):
            col=i%10;row=i//10;x=90+col*66;y=260+row*112
            color=GOLD if i in (19,20) else CYAN
            d.rounded_rectangle((x,y,x+54,y+60),radius=8,outline=color,width=3,fill='#17374A')
            write(d,(x+15,y+10),v,26,color,True)
        write(d,(150,738),'Hai vị trí giữa: 20, 21   →   7, 7',23,GREEN,True)
    elif chap==5:
        d.line((100,620,750,620),fill=MUTED,width=3)
        for xval in (5,7,9,15,21,27):
            x=100+(xval-4)/24*650
            d.line((x,609,x,633),fill=MUTED,width=3)
            write(d,(x-14,644),xval,21,MUTED)
        for val in (5,6,6,7,7,7,8,8):
            x=100+(val-4)/24*650
            d.ellipse((x-10,580,x+10,600),fill=CYAN)
        for val,color in ((9,CORAL),(27,GOLD)):
            x=100+(val-4)/24*650
            d.ellipse((x-14,530,x+14,558),fill=color)
        write(d,(140,287),'Chỉ 9 → 27 phút    TB: 7 → 9',30,GOLD,True)
        write(d,(140,360),'Trung vị = 7      Mốt = 7',27,GREEN,True)
    elif chap==6:
        for i,(t,detail,val) in enumerate((('TRUNG BÌNH','Dùng mọi giá trị','7,1'),('TRUNG VỊ','Vị trí giữa','7'),('MỐT','Tần số cao nhất','7'))):
            y=265+i*142
            d.rounded_rectangle((110,y,725,y+116),radius=14,fill='#16384A',outline=CYAN if i==0 else GREEN,width=2)
            write(d,(138,y+9),t,25,CYAN if i==0 else GREEN,True)
            write(d,(142,y+64),detail,21,MUTED)
            write(d,(635,y+26),val,36,GOLD,True)
    else:
        write(d,(139,285),'5    6    7    8    ?',53,WHITE,True)
        write(d,(135,429),'5 × 7 = 35',30,GOLD,True)
        write(d,(135,497),'5 + 6 + 7 + 8 = 26',26,MUTED)
        write(d,(135,594),'? = 35 − 26 = 9',33,GREEN,True)

def main():
    out=ROOT/'preview/stat03';out.mkdir(parents=True,exist_ok=True)
    imgs=[]
    for ch,title in enumerate(CHAPTERS,1):
        im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im)
        d.rounded_rectangle((45,150,800,822),radius=22,fill=PANEL,outline='#36576D',width=2)
        d.rounded_rectangle((827,150,1555,822),radius=22,fill=PANEL,outline='#36576D',width=2)
        write(d,(65,46),'SANGMATH / THỐNG KÊ 03',42,WHITE,True)
        write(d,(940,64),f'CHƯƠNG {ch:02d} / 08',30,CYAN,True)
        write(d,(90,175),'DỮ LIỆU VÀ HÌNH ĐỘNG',26,CYAN,True)
        graphics(d,ch)
        write(d,(863,226),title[:32],27,WHITE,True)
        messages=(
            ['40 dữ liệu giả lập','TB = 7,1; trung vị = 7','Mốt = 7; không phải một giá trị'],
            ['Lấy tổng chia cỡ mẫu','Tổng 284 cho 40 giá trị','Trung bình bằng 7,1'],
            ['Sắp xếp 40 giá trị','Vị trí 20 và 21 bằng 7','Trung vị bằng 7'],
            ['Cột tần số cao nhất','Điểm 7 có 10 quan sát','Có thể có nhiều mốt'],
            ['Ví dụ độc lập về thời gian','Kéo một điểm 9 lên 27 phút','Trung bình đổi; trung vị giữ'],
            ['Trung bình: đại diện tổng','Trung vị: ít nhạy với ngoại lệ','Mốt: đặc trưng phổ biến'],
            ['Cộng cùng một số','TB, TV và mốt cùng tăng','Giữ nguyên hình dạng phân bố'],
            ['Năm số có trung bình 7','Bốn số đã biết: 5,6,7,8','Tìm số còn thiếu là 9'],
        )[ch-1]
        for j,msg in enumerate(messages):
            yy=355+j*100
            write(d,(866,yy),'• '+msg,24,GOLD if j==2 else WHITE)
        write(d,(850,753),'PREVIEW • Không phải khung hình Manim',17,MUTED)
        path=out/f'STAT03_chapter_{ch:02d}.png';im.save(path,optimize=True)
        imgs.append(im.resize((800,450)))
    canvas=Image.new('RGB',(1640,1840),BG)
    for i,img in enumerate(imgs):canvas.paste(img,(20+(i%2)*820,20+(i//2)*455))
    canvas.save(out/'STAT03_storyboard_8_chapters.png',optimize=True)
    print('Preview exported: 8 chapter frames + montage')
if __name__=='__main__':main()
