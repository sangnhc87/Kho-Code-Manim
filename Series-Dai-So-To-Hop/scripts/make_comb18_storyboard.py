"""Eight full-HD design previews (not Manim-rendered frames)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb18_lesson_data import CHAPTERS,BEATS,triangle,odd_cells,vandermonde_splits
OUT=ROOT/'preview'/'comb18_v2';OUT.mkdir(parents=True,exist_ok=True)
W,H=1600,900
B='#0B1120';P='#101F33';Q='#172A43';CY='#22D3EE';GD='#FBBF24';PU='#A78BFA';MT='#A8B9CC';TX='#ECF4FF';GR='#22C55E';LN='#2E4862'
F='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf';FB='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(FB if b else F,n)
def centered(d,pos,words,n,color,bold=False):
    d.text(pos,words,font=font(n,bold),fill=color,anchor='mm')
def split_line(d,s,maxwidth,size):
    pieces=[];a=[]
    for word in s.split():
        if a and d.textbbox((0,0),' '.join(a+[word]),font=font(size))[2]>maxwidth:
            pieces.append(' '.join(a));a=[]
        a.append(word)
    if a:pieces.append(' '.join(a))
    return pieces

def base(ch):
    im=Image.new('RGB',(W,H),B);d=ImageDraw.Draw(im)
    d.rounded_rectangle((55,127,745,785),radius=26,fill=P,outline=LN,width=3)
    d.rounded_rectangle((769,127,1545,785),radius=26,fill=P,outline=LN,width=3)
    d.line((54,103,1545,103),fill=LN,width=3)
    d.text((70,42),'SANG MATH  /  ĐẠI SỐ TỔ HỢP',font=font(29,True),fill=CY)
    d.text((1060,42),'COMB18 · TAM GIÁC PASCAL',font=font(24,True),fill=MT)
    d.text((78,154),f'CHƯƠNG {ch+1:02d}',font=font(27,True),fill=CY)
    label=CHAPTERS[ch][1].split(' · ',1)[-1]
    for j,line in enumerate(split_line(d,label,650,36)[:2]):
        d.text((809,165+j*49),line,font=font(36,True),fill=GD)
    d.text((80,818),'STORYBOARD: MINH HỌA BỐ CỤC, CHƯA PHẢI RENDER MANIM',font=font(20),fill=MT)
    y=302
    for b in BEATS[ch*6:ch*6+1]:
        for sent in b.lines:
            for line in split_line(d,'• '+sent,690,29):
                d.text((804,y),line,font=font(29),fill=TX)
                y+=48
    return im,d

def diagram_pascal(d,rowmax,selected=None,high=None,baseY=270,sepY=69,sepX=79):
    for n in range(rowmax+1):
        for k,val in enumerate(triangle(n)[n]):
            x=int(398+(k-n/2)*sepX)
            y=baseY+n*sepY
            c=GD if selected==(n,k) or high==n else PU if (k+n)%2 else CY
            d.rounded_rectangle((x-30,y-23,x+30,y+23),radius=11,fill=Q,outline=c,width=3)
            centered(d,(x,y),str(val),19,TX,True)

def render(i):
    im,d=base(i)
    if i==0:
        diagram_pascal(d,5,high=5,baseY=300,sepY=78)
    elif i==1:
        diagram_pascal(d,5,selected=(4,2),baseY=265,sepY=79)
        x,y=398,265+4*79
        for k in [1,2]:
            px=398+(k-3/2)*79; py=265+3*79
            d.line((px,py+23,x,y-23),fill=GD,width=5)
    elif i==2:
        for j,ch in enumerate('ABCDEF'):
            x=165+j*99
            d.rounded_rectangle((x-31,267,x+31,331),radius=12,fill=Q,outline=GD if j==0 else CY,width=3)
            centered(d,(x,298),ch,32,TX,True)
        for j,(name,val,color) in enumerate([('CÓ A',10,GD),('KHÔNG CÓ A',10,PU)]):
            y=395+j*142
            d.rounded_rectangle((119,y,683,y+104),radius=17,fill=Q,outline=color,width=4)
            d.text((144,y+28),name,font=font(30,True),fill=color)
            d.text((587,y+22),str(val),font=font(39,True),fill=TX)
        centered(d,(399,724),'10 + 10 = 20',35,GR,True)
    elif i==3:
        diagram_pascal(d,6,baseY=248,sepY=64,sepX=78)
        centered(d,(399,726),'C chọn 2 từ 6 = C chọn 4 từ 6',22,GR,True)
    elif i==4:
        d.text((104,269),'TỔNG TỪNG HÀNG',font=font(32,True),fill=CY)
        for n in range(7):
            y=337+n*54
            d.text((124,y),f'n={n}',font=font(25,True),fill=GD)
            row='  '.join(map(str,triangle(n)[n]))
            d.text((230,y),row,font=font(23),fill=TX)
            d.text((615,y),str(2**n),font=font(26,True),fill=GR)
    elif i==5:
        diagram_pascal(d,6,baseY=253,sepY=62,sepX=78)
        for n,k in [(2,2),(3,2),(4,2),(5,2),(6,3)]:
            x=int(398+(k-n/2)*78);y=253+n*62
            d.ellipse((x-34,y-34,x+34,y+34),outline=GD,width=4)
        centered(d,(399,734),'1 + 3 + 6 + 10 = 20',31,GD,True)
    elif i==6:
        rows=32;cell=16
        for n,row in enumerate(triangle(rows-1)):
            for k,v in enumerate(row):
                x=int(398+(k-n/2)*cell)
                y=int(247+n*15.7)
                color=GD if v%2 else '#25364D'
                d.rectangle((x-5,y-5,x+5,y+5),fill=color)
        centered(d,(399,758),'MODULO 2  ·  32 HÀNG',24,GR,True)
    else:
        values=vandermonde_splits()
        d.text((104,267),'(1+x)^5  ×  (1+x)^3',font=font(35,True),fill=CY)
        for idx,num in enumerate(values):
            y=353+idx*91
            d.rounded_rectangle((117,y,676,y+72),radius=12,fill=Q,outline=GD if idx==2 else PU,width=2)
            d.text((145,y+18),f'i = {idx}',font=font(26,True),fill=CY)
            d.text((310,y+18),f'C(5,{idx})·C(3,{3-idx})',font=font(23),fill=TX)
            d.text((601,y+14),str(num),font=font(32,True),fill=GD)
        centered(d,(402,756),'1 + 15 + 30 + 10 = 56',30,GR,True)
    im.save(OUT/f'COMB18_chuong_{i+1:02d}.png',optimize=True)
    return im

def main():
    thumbs=[]
    for i in range(8):
        image=render(i)
        thumbs.append(image.resize((800,450),Image.Resampling.LANCZOS))
    big=Image.new('RGB',(1600,1800),B)
    for j,t in enumerate(thumbs):big.paste(t,((j%2)*800,(j//2)*450))
    big.save(OUT/'storyboard_8_chapters.png',optimize=True)
    print('COMB18 storyboards generated: 8 frames + contact sheet')

if __name__=='__main__':main()
