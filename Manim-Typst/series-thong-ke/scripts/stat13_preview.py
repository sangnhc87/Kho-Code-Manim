"""Independent design storyboard; NOT screenshots of a rendered Manim lecture."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat13.lesson import PA,PB,EA,EB,CHAPTERS,A,B
W,H=1480,1690
BG='#0A1522'; PANEL='#10293B'; EDGE='#355A71'
WHITE='#EDF6FF';MUTED='#ADC6D5'; CYAN='#56CBE9'; GOLD='#FFD379'; GREEN='#67DDB5';CORAL='#FF8E87'
font_dir=Path('/usr/share/fonts/truetype/dejavu')
normal=str(font_dir/'DejaVuSans.ttf');bold=str(font_dir/'DejaVuSans-Bold.ttf')
F1=ImageFont.truetype(bold,32);F2=ImageFont.truetype(bold,25)
F3=ImageFont.truetype(normal,20);F4=ImageFont.truetype(bold,19)
canvas=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(canvas)
d.text((56,28),'SANGMATH   |   THỐNG KÊ 12',font=F1,fill=CYAN)
d.text((56,78),'STAT13 – SO SÁNH HAI MẪU SỐ LIỆU',font=F1,fill=WHITE)
labels=[
    ('Hai nhóm cùng trung bình','Cùng trung bình 7; phân bố khác'),
    ('Ba số đo trung tâm','Trung bình = trung vị = mốt = 7'),
    ('Tứ phân vị và biểu đồ hộp','IQR(A)=2   |   IQR(B)=6'),
    ('Độ lệch chuẩn','s(A)≈1,095   |   s(B)≈2,324'),
    ('Dữ liệu ghép nhóm','Phương sai: 2,44 và 4,44'),
    ('Tiêu chí theo mục tiêu','Đạt từ 6: 90% / 70%'),
    ('Giới hạn khi so sánh','Cùng đơn vị – đúng bối cảnh'),
    ('Bài tập vận dụng','Phương sai: 1,5 và 5,5'),
]

def xval(value, x0, width):return x0+int((value-3)/8*width)

def boxplot(draw,px,y,profile,color):
    x0=px+72;length=510
    vals=(profile.minimum,profile.q1,profile.median,profile.q3,profile.maximum)
    coords=[xval(v,x0,length) for v in vals]
    draw.line((coords[0],y,coords[-1],y),fill=color,width=3)
    draw.rectangle((coords[1],y-20,coords[3],y+20),outline=color,width=4)
    draw.line((coords[2],y-20,coords[2],y+20),fill=GOLD,width=4)
    for val in (coords[0],coords[-1]):draw.line((val,y-11,val,y+11),fill=color,width=3)

for i,(name,desc) in enumerate(labels):
    row,col=divmod(i,2);x=55+col*710;y=153+row*361
    d.rounded_rectangle((x,y,x+676,y+331),radius=20,fill=PANEL,outline=EDGE,width=2)
    d.text((x+19,y+19),f'{i+1:02d}  {name}',font=F2,fill=WHITE)
    d.text((x+18,y+277),desc,font=F4,fill=GOLD)
    if i in (2,3,6,7):
        boxplot(d,x+5,y+141, PA if i!=7 else EA,CYAN)
        boxplot(d,x+5,y+223, PB if i!=7 else EB,CORAL)
        d.text((x+25,y+127),'A',font=F4,fill=CYAN)
        d.text((x+25,y+211),'B',font=F4,fill=CORAL)
    elif i in (0,1,5):
        for row2,(arr,c) in enumerate(((A,CYAN),(B,CORAL))):
            yy=y+112+row2*107
            used={}
            d.line((x+72,yy+58,x+613,yy+58),fill=MUTED,width=2)
            for v in arr:
                j=used.get(v,0);used[v]=j+1
                xx=xval(v,x+72,541)
                d.ellipse((xx-8,yy+39-j*12,xx+8,yy+55-j*12),fill=c)
    else:
        values1=(6,18,14,2);values2=(9,19,3,9)
        for row2,(freq,c) in enumerate(((values1,CYAN),(values2,CORAL))):
            yy=y+145+row2*92
            for j,v in enumerate(freq):
                xx=x+108+j*115
                d.rectangle((xx,yy-v*3,xx+56,yy),fill=c)
footer='Thầy Nguyễn Văn Sang'
w=d.textbbox((0,0),footer,font=F2)[2]
d.text(((W-w)/2,H-44),footer,font=F2,fill=MUTED)
d.text((54,H-75),'STORYBOARD THIẾT KẾ  |  KHÔNG PHẢI ẢNH MANIM ĐÃ RENDER',font=F3,fill=MUTED)
target=ROOT/'preview/stat13/STAT13_storyboard_8_chapters.png'
target.parent.mkdir(parents=True,exist_ok=True)
canvas.save(target,optimize=True)
print('STAT13_PREVIEW_OK',target,canvas.size)
