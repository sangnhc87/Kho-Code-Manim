"""Author Vietnamese docs and illustrative (NOT Manim-rendered) storyboard for STAT05."""
from __future__ import annotations
import sys,math,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat05.lesson import BEATS,CHAPTERS,BASE,EXTREME,COMPARE,SPREAD,EXERCISE,CONSTANT
from stat01.lesson import SCORES

chap_lines=[
 ('Khoảng biến thiên và hai cực trị','R = 10 − 4 = 6','Đổi một cực trị thành 30: R = 26'),
 ('Năm số đặc trưng','Min = 4  •  Q1 = 6  •  Q2 = 7','Q3 = 8  •  Max = 10  •  IQR = 2'),
 ('Từ năm số đến biểu đồ hộp','Hộp từ 6 đến 8','Trung vị tại 7, râu từ 4 đến 10'),
 ('Tukey và điểm ngoại lệ','Ngưỡng: 3 và 11','Râu 4–10; 30 được đánh dấu riêng'),
 ('Hai mẫu cùng trung vị','A: trung vị 5,5 • IQR 4','B: trung vị 5,5 • IQR 8'),
 ('Cùng R = 8, khác IQR','Mẫu A: IQR = 8','Mẫu B: IQR = 2'),
 ('Quy ước và giới hạn','Biểu đồ năm số ≠ Tukey khi có ngoại lệ','IQR = 0: hộp co thành một vạch'),
 ('Bài toán tổng hợp 11 số','Q1 = 4  •  Q2 = 6  •  Q3 = 8','R = 18, IQR = 4; điểm 20 là ngoại lệ'),
]
font='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
bold='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
if not Path(font).exists():font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(bold).exists():bold=font
F=lambda size,b=False:ImageFont.truetype(bold if b else font,size)
C={'bg':'#0A1522','panel':'#10293B','line':'#355A71','muted':'#ADC6D5','white':'#EDF6FF','cyan':'#56CBE9','gold':'#FFD379','green':'#67DDB5','coral':'#FF8E87','purple':'#B7A9FC'}

def base_canvas(ch):
    im=Image.new('RGB',(1280,720),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((33,130,647,639),radius=20,fill=C['panel'],outline=C['line'],width=2)
    d.rounded_rectangle((670,130,1245,639),radius=20,fill=C['panel'],outline=C['line'],width=2)
    d.text((42,36),f'SANGMATH / THỐNG KÊ 05 / CHƯƠNG {ch:02d}',font=F(32,True),fill=C['white'])
    d.line((39,105,1240,105),fill=C['line'],width=2)
    d.text((55,160),chap_lines[ch-1][0].upper(),font=F(24,True),fill=C['cyan'])
    d.text((706,175),f'CHƯƠNG {ch:02d}/08    •    NHỊP 3/4',font=F(23,True),fill=C['cyan'])
    for row,text in enumerate(textwrap.wrap(CHAPTERS[ch-1],width=30,break_long_words=False)):
        d.text((706,235+row*28),text,font=F(21,True),fill=C['white'])
    d.line((704,307,1200,307),fill=C['line'],width=2)
    d.text((706,358),chap_lines[ch-1][1],font=F(23,True),fill=C['gold'])
    d.text((706,414),chap_lines[ch-1][2],font=F(21),fill=C['green'])
    d.text((706,565),'Quan sát → dự đoán → kiểm chứng',font=F(18),fill=C['muted'])
    d.text((45,668),'STORYBOARD MINH HỌA  •  CHƯA PHẢI KHUNG HÌNH RENDER MANIM',font=F(18),fill=C['muted'])
    return im,d

def draw_axis(d,x0,x1,y,mn,mx,ticks):
    d.line((x0,y,x1,y),fill=C['muted'],width=3)
    X=lambda val:int(x0+(val-mn)/(mx-mn)*(x1-x0))
    for t in ticks:
        x=X(t);d.line((x,y-10,x,y+10),fill=C['muted'],width=2)
        d.text((x-15,y+17),str(t),font=F(17),fill=C['muted'])
    return X

def plot_box(d,stat,X,y,col,show_out=True):
    q1,mid,q3=stat['q1'],stat['median'],stat['q3']
    start,end=stat['lower_whisker'],stat['upper_whisker']
    d.line((X(start),y,X(q1),y),fill=col,width=4)
    d.line((X(q3),y,X(end),y),fill=col,width=4)
    for x in [start,end]:d.line((X(x),y-21,X(x),y+21),fill=col,width=4)
    d.rectangle((X(q1),y-41,max(X(q1)+2,X(q3)),y+41),fill='#18394E',outline=col,width=4)
    d.line((X(mid),y-40,X(mid),y+40),fill=C['gold'],width=5)
    if show_out:
        for x in stat['outliers']:
            xx=X(x);d.ellipse((xx-10,y-10,xx+10,y+10),fill=C['coral'])

for ch in range(1,9):
    im,d=base_canvas(ch)
    if ch==1:
        X=draw_axis(d,83,605,494,0,32,[0,4,8,10,20,30]);y=425
        for k,s in enumerate(sorted(SCORES)):
            i=sum(1 for t in list(sorted(SCORES))[:k] if t==s)
            xx=X(s);yy=y-i*11
            d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=C['cyan'])
        d.line((X(4),265,X(10),265),fill=C['gold'],width=6)
        d.text((100,302),'Khoảng biến thiên gốc: 6',font=F(21,True),fill=C['gold'])
    elif ch in (2,3):
        X=draw_axis(d,83,604,498,3,11,[4,5,6,7,8,9,10])
        plot_box(d,BASE,X,376,C['cyan'],False)
        d.text((105,550),'4     6        7        8          10',font=F(22),fill=C['green'])
    elif ch==4:
        X=draw_axis(d,83,604,501,0,32,[0,3,4,6,8,10,11,20,30])
        plot_box(d,EXTREME,X,375,C['cyan'])
        for t in [3,11]:d.line((X(t),263,X(t),491),fill=C['gold'],width=2)
    elif ch==5:
        X=draw_axis(d,83,604,528,0,12,[0,2,4,6,8,10,12])
        plot_box(d,COMPARE[0],X,322,C['cyan']);plot_box(d,COMPARE[1],X,434,C['coral'])
        d.text((90,300),'A',font=F(21,True),fill=C['cyan']);d.text((90,412),'B',font=F(21,True),fill=C['coral'])
    elif ch==6:
        X=draw_axis(d,83,604,528,0,10,[0,1,2,4,5,6,8,9,10])
        plot_box(d,SPREAD[0],X,320,C['purple']);plot_box(d,SPREAD[1],X,432,C['green'])
    elif ch==7:
        X=draw_axis(d,83,604,522,0,10,[0,1,2,4,5,6,8,9,10]);plot_box(d,CONSTANT,X,359,C['green'])
        d.text((110,420),'IQR = 0',font=F(26,True),fill=C['green'])
    else:
        X=draw_axis(d,83,604,525,0,22,[0,2,4,6,8,10,14,20]);plot_box(d,EXERCISE,X,380,C['green'])
    im.save(ROOT/'preview'/'stat05'/f'STAT05_chapter_{ch:02d}.png')

sheet=Image.new('RGB',(1660,1910),'#091421')
for ch in range(1,9):
    p=Image.open(ROOT/'preview'/'stat05'/f'STAT05_chapter_{ch:02d}.png')
    p.thumbnail((800,450))
    col=(ch-1)%2;row=(ch-1)//2
    sheet.paste(p,(20+col*820,20+row*470))
sheet.save(ROOT/'preview'/'stat05'/'STAT05_storyboard_8_chapters.png')

lines=['# STAT05 – Storyboard chi tiết (8 chương, 32 nhịp)','',
       '## Thiết kế','- Bố cục hai cột: hình động bên trái, phát biểu và công thức Typst bên phải.',
       '- Sử dụng 40 điểm giả lập thống nhất với STAT01–STAT04.',
       '- Tứ phân vị theo phương pháp trung vị hai nửa của STAT04.',
       '- Khi có ngoại lệ, phân biệt hộp năm số và hộp Tukey; các râu Tukey tới quan sát hợp lệ xa nhất.',
       '- Mỗi nhịp 27 giây nền; TTS có thể kéo dài từng nhịp.', '']
for ch in range(1,9):
    lines.extend([f'## Chương {ch:02d} – {CHAPTERS[ch-1]}',''])
    for b in BEATS[(ch-1)*4:ch*4]:
        lines.extend([f'### Nhịp {b.step} – {b.title}',
                      f'**Thông điệp:** {b.thesis}',f'**Hình:** trạng thái {ch}.{b.step} của mô hình chương {ch}.',
                      f'**Lời giảng:** {b.voice}',''])
(ROOT/'STORYBOARD_STAT05.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'LOI_GIANG_STAT05.md').write_text('# Lời giảng STAT05 – Khoảng biến thiên, IQR, biểu đồ hộp\n\n'+
    '\n\n'.join(f'## Chương {b.chapter}, nhịp {b.step}: {b.title}\n\n{b.voice}' for b in BEATS)+'\n',encoding='utf-8')
print('STAT05_DOCS_PREVIEW_OK',len(BEATS),'beats',8,'images')
