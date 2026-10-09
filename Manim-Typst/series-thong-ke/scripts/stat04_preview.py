"""Eight 1280x720 static storyboard checks; NOT rendered Manim frames."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stat04.lesson import SCORES,SORTED,FREQUENCY,CUMULATIVE,BEATS,EVEN,ODD,GROUP_A,GROUP_B
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'/'stat04';OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FB='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
DARK='#091421';PANEL='#102739';ALT='#16384A';BORDER='#345569';WHITE='#E9F3FA'
CYAN='#54C8E9'; GOLD='#FFD47A';GREEN='#63D9B4';CORAL='#FF8B84';PURPLE='#BBA7FC';MUTED='#A2BECD'
VALUES={4:CORAL,5:'#F9AD76',6:GOLD,7:CYAN,8:GREEN,9:PURPLE,10:'#CBAAF5'}

def font(size=20,bold=False):return ImageFont.truetype(FB if bold else F,size)
def text(d,xy,s,sz=22,fill=WHITE,bold=False,anchor=None):
    d.text(xy,str(s),font=font(sz,bold),fill=fill,anchor=anchor)

def rect(d,coords,fill=ALT,outline=BORDER,width=2,radius=12):
    d.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)

def score_tiles(d,values,highlight=(),initial=(65,175),ncols=10,w=50,h=43,dx=58,dy=79):
    for i,v in enumerate(values):
        x=initial[0]+(i%ncols)*dx;y=initial[1]+(i//ncols)*dy
        sel=i+1 in highlight
        rect(d,(x,y,x+w,y+h),fill=ALT,outline=GOLD if sel else BORDER,width=4 if sel else 1,radius=7)
        text(d,(x+w/2,y+h/2),v,21,GOLD if sel else VALUES.get(v,CYAN),True,'mm')

def frame(chapter,title,subtitle):
    im=Image.new('RGB',(1280,720),DARK);d=ImageDraw.Draw(im)
    rect(d,(26,98,643,650),PANEL,BORDER,2,18)
    rect(d,(663,98,1254,650),PANEL,BORDER,2,18)
    text(d,(40,34),'SANGMATH   /   THỐNG KÊ 04   /   TỨ PHÂN VỊ',29,WHITE,True)
    text(d,(44,117),f'CHƯƠNG {chapter:02d} / 08',20,CYAN,True)
    text(d,(677,127),title,25,WHITE,True)
    d.line((677,180,1235,180),fill=BORDER,width=2)
    text(d,(678,208),subtitle,22,GOLD,True)
    text(d,(45,676),'STORYBOARD TĨNH  •  MÔ HÌNH SƯ PHẠM  •  KHÔNG PHẢI KHUNG HÌNH MANIM',16,MUTED)
    return im,d


def full_line(d,x0,y,x1,labels=range(4,11)):
    d.line((x0,y,x1,y),fill=MUTED,width=3)
    for v in labels:
        xx=x0+(v-min(labels))/(max(labels)-min(labels))*(x1-x0)
        d.line((xx,y-8,xx,y+8),fill=MUTED,width=2)
        text(d,(xx,y+25),v,18,MUTED,anchor='mm')
    return lambda v:x0+(v-min(labels))/(max(labels)-min(labels))*(x1-x0)

scenes=[
 ('40 điểm: từ hỗn độn đến trật tự','Sắp xếp không giảm trước khi chia'),
 ('Trung vị của cả dãy là Q₂','40 giá trị → hai nửa, mỗi nửa 20'),
 ('Tìm Q₁, Q₂, Q₃ qua vị trí','10–11   |   20–21   |   30–31'),
 ('Tần số tích lũy','Đọc giá trị của từng vị trí'),
 ('Khi n chẵn và khi n lẻ','Bỏ trung vị chung khi n lẻ'),
 ('Ngoại lệ và phép dịch','Phân biệt thay một số với thay toàn bộ'),
 ('Khoảng tứ phân vị IQR','Cùng trung vị không có nghĩa cùng phân tán'),
 ('Bài ngược: tìm x và các tứ phân vị','Chỉ công bố kết quả sau khi suy luận'),
]
for ci,(title,sub) in enumerate(scenes,1):
    im,d=frame(ci,title,sub)
    if ci in (1,2,3):
        ids=() if ci==1 else (20,21) if ci==2 else (10,11,20,21,30,31)
        score_tiles(d,SORTED,ids,initial=(64,218),w=46,h=46,dx=56,dy=80)
        if ci==1:
            text(d,(340,590),'40 điểm giả lập  •  xếp từ 4 đến 10',19,GREEN,True,'mm')
            notes=['Dữ liệu có thứ tự là điều kiện', 'Để xác định những mốc vị trí', 'Tứ phân vị không chia đều khoảng 4–10']
        elif ci==2:
            text(d,(340,585),'1–20     ←  Q₂  →     21–40',23,GOLD,True,'mm')
            notes=['Nửa dưới: các vị trí 1 đến 20','Nửa trên: các vị trí 21 đến 40','Q₂ = (7 + 7) / 2 = 7']
        else:
            text(d,(340,586),'Q₁ = 6     Q₂ = 7     Q₃ = 8',25,GREEN,True,'mm')
            notes=['Q₁: trung bình vị trí 10 và 11','Q₂: trung bình vị trí 20 và 21','Q₃: trung bình vị trí 30 và 31']
    elif ci==4:
        for j,(name,vals) in enumerate((('ĐIỂM',tuple(FREQUENCY)),('TẦN SỐ',tuple(FREQUENCY.values())),('TÍCH LŨY',tuple(v for k,v in CUMULATIVE)))):
            text(d,(65,217+j*115),name,18,CYAN,True)
            for i,v in enumerate(vals):
                x=70+i*78;y=256+j*115
                rect(d,(x,y,x+67,y+44),ALT,GOLD if j==2 and v in (14,24,32) else BORDER,3 if j==2 and v in (14,24,32) else 1,7)
                text(d,(x+33,y+22),v,21,GOLD if j==2 and v in (14,24,32) else WHITE,True,'mm')
        notes=['14 quan sát tới điểm 6 → Q₁ = 6','24 quan sát tới điểm 7 → Q₂ = 7','32 quan sát tới điểm 8 → Q₃ = 8']
    elif ci==5:
        score_tiles(d,ODD,highlight=(5,),initial=(69,290),ncols=9,dx=57,w=48,h=57)
        text(d,(320,210),'1  2  3  4  [5]  6  7  8  9',22,MUTED,anchor='mm')
        text(d,(328,454),'Q₁ = 2,5    Q₂ = 5    Q₃ = 7,5',23,GREEN,True,'mm')
        notes=['Với 9 số, trung vị là vị trí thứ 5','Không đưa trung vị chung vào hai nửa','SGK dùng trung vị của nửa dưới/nửa trên']
    elif ci==6:
        f=full_line(d,74,468,590,range(4,11))
        for v,c in sorted(FREQUENCY.items()):
            x=f(v)
            d.ellipse((x-11,424-c*10,x+11,446-c*10),fill=VALUES[v])
        d.line((584,260,590,422),fill=CORAL,width=3)
        text(d,(520,240),'10 → 30',25,CORAL,True,'mm')
        text(d,(310,580),'Q₁=6      Q₂=7      Q₃=8',23,GREEN,True,'mm')
        notes=['Thay một quan sát 10 bằng 30','Trung bình tăng 7,1 → 7,6','Ba tứ phân vị vẫn là 6, 7, 8']
    elif ci==7:
        for i,(lo,mid,hi,name,c) in enumerate(((3.5,5.5,7.5,'A',CYAN),(2,5.5,10,'B',CORAL))):
            y=304+i*157;x0=100;x1=591
            def xx(v):return x0+v/12*(x1-x0)
            d.line((x0,y,x1,y),fill=BORDER,width=3)
            rect(d,(xx(lo),y-26,xx(hi),y+26),fill=PANEL,outline=c,width=5,radius=4)
            d.line((xx(mid),y-28,xx(mid),y+28),fill=GOLD,width=5)
            text(d,(78,y),name,23,c,True,'mm')
        notes=['Hai mẫu đều có trung vị 5,5','Mẫu A: Q₁=3,5 và Q₃=7,5 → IQR=4','Mẫu B: Q₁=2 và Q₃=10 → IQR=8']
    else:
        arr=[3,4,5,'x',7,8,9,10]
        for i,v in enumerate(arr):
            x=72+i*69;rect(d,(x,280,x+54,336),ALT,GOLD if i==3 else BORDER,3 if i==3 else 1,7)
            text(d,(x+27,307),v,23,GOLD if i==3 else WHITE,True,'mm')
        text(d,(330,454),'Q₂ = (x+7)/2 = 6,5',26,GOLD,True,'mm')
        notes=['Trung vị cho phép tìm x = 6','Q₁ = 4,5  ;  Q₃ = 8,5','Khoảng tứ phân vị: IQR = 4']
    for j,line in enumerate(notes):
        text(d,(685,270+j*91),f'{j+1:02d}   {line}',20,GREEN if j==2 else WHITE)
    text(d,(685,574),'HÌNH ĐỘNG  →  SUY LUẬN  →  KIỂM TRA',18,CYAN,True)
    im.save(OUT/f'STAT04_chapter_{ci:02d}.png',optimize=True)

sheet=Image.new('RGB',(2560,720),DARK)
for i in range(8):
    img=Image.open(OUT/f'STAT04_chapter_{i+1:02d}.png').resize((640,360),Image.Resampling.LANCZOS)
    sheet.paste(img,((i%4)*640,(i//4)*360))
sheet.save(OUT/'STAT04_storyboard_8_chapters.png',optimize=True)
print('STAT04 static storyboard: 8 chapters + overview',OUT)
