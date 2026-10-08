"""Pillow storyboard sketches for COMB23 (not a Manim render)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from comb23_lesson_data import CHAPTERS,BEATS,rook_numbers,forbidden_asymmetric,forbidden_cycle
OUT=ROOT/'preview'/'comb23_v2';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
F=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
BG='#0b1120';PANEL='#101f33';CYAN='#22d3ee';GOLD='#fbbf24';RED='#ef4444';TXT='#e9f3ff';MUTED='#a8b9cc';LINE='#2e4862'

def title(d,t,x,y,size=26,color=TXT,bold=False):d.text((x,y),t,font=F(size,bold),fill=color)
def fit_words(d,words,rect,size=23,step=34,maxlines=2):
    x,y,w=rect;cur='';rows=[]
    for wd in words.split():
        attempt=(cur+' '+wd).strip()
        if d.textbbox((0,0),attempt,font=F(size))[2]>w and cur:rows.append(cur);cur=wd
        else:cur=attempt
    if cur:rows.append(cur)
    for i,s in enumerate(rows[:maxlines]):title(d,s,x,y+i*step,size)

def board(d,n,banned,x0,y0,cell=78):
    for i in range(n):
        for j in range(n):
            x=x0+j*cell;y=y0+i*cell
            is_bad=(i,j) in banned
            d.rounded_rectangle((x,y,x+cell-8,y+cell-8),radius=8,fill='#512638' if is_bad else '#172a43',outline=RED if is_bad else LINE,width=2)
            if is_bad:title(d,'×',x+19,y+10,32,RED,True)
    for i in range(n):title(d,str(i+1),x0-29,y0+i*cell+13,18,MUTED)
    for j in range(n):title(d,str(j+1),x0+j*cell+20,y0-26,18,MUTED)

def visual(d,section):
    if section=='three_sets':
        for bbox,color in [((83,187,395,496),CYAN),((258,187,572,496),GOLD),((170,310,482,613),'#a78bfa')]:
            d.ellipse(bbox,outline=color,width=6)
        for x,y,t,c in [(115,210,'A: 15',CYAN),(448,210,'B: 10',GOLD),(275,562,'C: 6','#a78bfa'),(275,355,'ABC = 1',TXT)]:title(d,t,x,y,22,c,True)
    elif section=='derange':board(d,5,{(i,i) for i in range(5)},124,223,68)
    elif section=='fixed_ban':board(d,6,{(i,i) for i in range(3)},100,207,62)
    elif section=='diagonal':board(d,4,{(i,i) for i in range(4)},159,225,83)
    elif section=='board':board(d,4,forbidden_asymmetric(),159,225,83)
    elif section=='rencontres':
        for k,(c,col) in enumerate(zip('ABCDE',[CYAN,CYAN,GOLD,GOLD,GOLD])):
            x=108+k*91;d.rounded_rectangle((x,275,x+78,354),radius=10,outline=col,width=3,fill='#172a43');title(d,c,x+24,293,27,TXT,True)
        title(d,'2 vị trí đúng  ×  D3 = 2',90,426,24,CYAN,True)
        title(d,'10 × 2 = 20',205,497,36,GOLD,True)
    elif section=='rook_recurrence':
        ban=forbidden_asymmetric()
        for q,label in enumerate(['B','B bỏ p','B bỏ hàng/cột']):
            x=80+q*171;title(d,label,x,211,15,GOLD,True)
            for i in range(4):
                for j in range(4):
                    x1=x+j*36;y1=260+i*36
                    forbidden=(i,j) in ban
                    if q==1 and (i,j)==(0,0):forbidden=False
                    if q==2 and (i==0 or j==0):forbidden=False
                    d.rectangle((x1,y1,x1+29,y1+29),fill='#512638' if forbidden else '#172a43',outline=RED if forbidden else LINE)
        title(d,'R(B) = R(B bỏ p) + x R(B bỏ hàng/cột)',74,506,19,CYAN)
    elif section=='menage':board(d,5,forbidden_cycle(5),124,211,68)
    else:pass

for idx,(section,chapter) in enumerate(CHAPTERS,1):
    img=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(img)
    d.rounded_rectangle((22,18,1258,83),radius=15,fill=PANEL,outline=LINE,width=2)
    title(d,'SANG MATH  ·  COMB23 V2',46,31,25,CYAN,True)
    title(d,f'CHƯƠNG {idx:02}',1038,35,19,MUTED,True)
    d.rounded_rectangle((22,99,630,668),radius=15,fill=PANEL,outline=LINE,width=2)
    d.rounded_rectangle((651,99,1258,668),radius=15,fill=PANEL,outline=LINE,width=2)
    chapter_title=chapter.split('· ',1)[-1]
    fit_words(d,chapter_title,(55,122,540),22,29,2)
    visual(d,section)
    b=next(x for x in BEATS if x.section==section)
    title(d,'BÀI TOÁN / LẬP LUẬN',678,132,22,GOLD,True)
    fit_words(d,b.heading,(681,192,525),23,35,2)
    for i,line in enumerate(b.lines):
        title(d,'•',686,291+i*61,24,CYAN,True)
        fit_words(d,line,(715,292+i*61,500),21,29,2)
    d.line((687,507,1224,507),fill=LINE,width=2)
    fit_words(d,b.takeaway,(694,535,528),20,30,3)
    title(d,'STORYBOARD  ·  CHƯA RENDER MANIM',418,678,15,MUTED)
    img.save(OUT/f'COMB23_{idx:02}.png')

contact=Image.new('RGB',(1280,1440),BG)
for i in range(8):
    p=Image.open(OUT/f'COMB23_{i+1:02}.png').resize((640,360),Image.Resampling.LANCZOS)
    contact.paste(p,((i%2)*640,(i//2)*360))
contact.save(OUT/'storyboard_8_chapters.png')
print('STORYBOARD_OK chapters=8')
