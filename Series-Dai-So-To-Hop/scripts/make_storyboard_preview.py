"""Static concept frames for QA when Manim isn't installed; not a Manim render."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'
OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
C={'bg':'#0B1120','panel':'#101F33','panel2':'#172A43','line':'#2E4862','white':'#ECF4FF','muted':'#A8B9CC','cyan':'#22D3EE','gold':'#FBBF24','red':'#EF4444','green':'#22C55E'}
W,H=1600,900

def f(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)
def base():
    im=Image.new('RGB',(W,H),C['bg']); d=ImageDraw.Draw(im)
    d.text((70,42),'SANG MATH  /  ĐẠI SỐ TỔ HỢP',font=f(29,True),fill=C['cyan'])
    d.text((1080,44),'COMB01 · QUY TẮC CỘNG',font=f(25),fill=C['muted'])
    d.line((70,104,1530,104),fill=C['line'],width=2)
    d.rounded_rectangle((45,133,733,786),radius=27,fill=C['panel'],outline=C['line'],width=2)
    d.rounded_rectangle((757,133,1555,786),radius=27,fill=C['panel'],outline=C['line'],width=2)
    d.text((470,831),'STORYBOARD PREVIEW  ·  CHƯA PHẢI VIDEO MANIM',font=f(22),fill=C['muted'])
    return im,d

def title(d,main,sub):
    d.text((100,180),main,font=f(41,True),fill=C['white'])
    d.text((100,246),sub,font=f(29),fill=C['muted'])

def right(d,head,lines,formula=None,footer=None):
    d.text((811,190),head,font=f(39,True),fill=C['gold'])
    y=285
    for x in lines:
        d.text((815,y),x,font=f(30),fill=C['white']);y+=69
    if formula:
        d.text((850,max(550,y+20)),formula,font=f(58,True),fill=C['cyan'])
    if footer:
        d.rounded_rectangle((825,703,1485,750),radius=14,fill=C['panel2'],outline='#594B8B',width=2)
        d.text((844,707),footer,font=f(24),fill=C['white'])

def intro():
    im,d=base();title(d,'Một hành trình,','có bao nhiêu tuyến đường?')
    A=(143,538);B=(631,538)
    from PIL import ImageColor
    shades=[C['cyan'],C['cyan'],C['gold'],C['gold'],C['gold']]
    levels=[-230,-130,-25,95,215]
    for n,(h,col) in enumerate(zip(levels,shades)):
        coords=[]
        for i in range(101):
            t=i/100
            x=A[0]+(B[0]-A[0])*t
            y=A[1]+4*h*t*(1-t)
            coords.append((x,y))
        d.line(coords,fill=col,width=7,joint='curve')
        cx=int((A[0]+B[0])/2)
        cy=int(A[1]+h)
        label=(f'XE {n+1}' if n<2 else f'TÀU {n-1}')
        d.rounded_rectangle((cx-60,cy-24,cx+65,cy+15),radius=9,fill=C['panel'],outline=col,width=2)
        d.text((cx-43,cy-22),label,font=f(21,True),fill=col)
    for center,char in [(A,'A'),(B,'B')]:
        x,y=center; d.ellipse((x-40,y-40,x+40,y+40),fill=C['panel2'],outline=C['white'],width=4)
        d.text((x-17,y-28),char,font=f(39,True),fill=C['white'])
    right(d,'BÀI TOÁN MỞ ĐẦU',[
      'Từ A đến B có 2 tuyến xe buýt',
      'và 3 tuyến tàu khác nhau.',
      'Chọn đúng 1 tuyến để đi.',
      'Hỏi có bao nhiêu cách chọn?'
    ],footer='Dự đoán trước khi xem lời giải')
    return im

def count():
    im,d=base();title(d,'Hai nhóm lựa chọn','không có phương án nào trùng nhau')
    for i,(x,y,s,col) in enumerate([
      (100,340,'XE 1',C['cyan']),(365,340,'XE 2',C['cyan']),
      (100,475,'TÀU 1',C['gold']),(280,475,'TÀU 2',C['gold']),
      (460,475,'TÀU 3',C['gold'])]):
        d.rounded_rectangle((x,y,x+158,y+82),radius=14,fill=C['panel2'],outline=col,width=3)
        d.text((x+31,y+18),s,font=f(27,True),fill=col)
    right(d,'HAI NHÓM LỰA CHỌN',[
      'Nhóm xe buýt: 2 cách',
      'Nhóm tàu: 3 cách',
      'Chỉ chọn một trong hai nhóm.'
    ],'2 + 3 = 5',footer='Không có trường hợp bị đếm trùng')
    return im

def overlap():
    im,d=base();title(d,'Cẩn thận đếm trùng!','Các số tự nhiên từ 1 đến 12')
    for n in range(1,13):
        r=(n-1)//4;c=(n-1)%4
        x=100+145*c;y=335+125*r
        div2=n%2==0;div3=n%3==0
        color=C['red'] if div2 and div3 else C['cyan'] if div2 else C['gold'] if div3 else C['panel2']
        d.rounded_rectangle((x,y,x+114,y+83),radius=12,fill=color,outline=C['line'],width=2)
        d.text((x+41 if n<10 else x+28,y+15),str(n),font=f(42,True),fill=C['bg'] if div2 or div3 else C['white'])
    right(d,'CHỈ ĐẾM MỖI SỐ 1 LẦN',[
      'Chia hết cho 2: 6 số',
      'Chia hết cho 3: 4 số',
      '6 và 12 bị tính 2 lần.',
      'Vì vậy phải trừ 2 số trùng.'
    ],'6 + 4 - 2 = 8',footer='Đừng cộng trực tiếp nếu hai nhóm giao nhau')
    return im

def main():
    ims=[]
    for idx,(name,fn) in enumerate([('01_mo_dau',intro),('02_hai_nhom',count),('03_dem_trung',overlap)]):
        im=fn();im.save(OUT/f'{name}.png',optimize=True);ims.append(im)
    sheet=Image.new('RGB',(1200,1120),'#09111D')
    draw=ImageDraw.Draw(sheet)
    for idx,im in enumerate(ims):
        img=im.resize((1100,619),Image.Resampling.LANCZOS)
        img=img.resize((550,310),Image.Resampling.LANCZOS)
        x=36+(idx%2)*578; y=30+(idx//2)*338
        sheet.paste(img,(x,y))
    draw.text((50,720),'SANG MATH — COMB01 · BA KHUNG HÌNH MINH HỌA',font=f(31,True),fill=C['white'])
    draw.text((50,788),'Bản xem trước dựng bằng Pillow; chưa phải Manim render.',font=f(23),fill=C['muted'])
    sheet.save(OUT/'COMB01_storyboard_contact_sheet.png')
    print('Preview images created:',len(ims)+1)

if __name__=='__main__':main()
