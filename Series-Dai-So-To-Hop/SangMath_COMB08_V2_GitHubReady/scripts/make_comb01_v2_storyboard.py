"""Pillow sketches (NOT Manim renders) to help inspect proposed two-column layout."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb01_lesson_data import BEATS, CHAPTER_LABELS
W,H=1280,720
REG='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
COL={'bg':'#0b1120','panel':'#101f33','line':'#2e4862','text':'#ecf4ff','muted':'#a8b9cc','cyan':'#22d3ee','gold':'#fbbf24','green':'#22c55e','red':'#ef4444'}

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else REG,size)

def tx(d,pt,s,sz=24,c='text',bold=False,anchor=None):
    d.text(pt,s,font=font(sz,bold),fill=COL.get(c,c),anchor=anchor)

def capsule(d,x,y,s,c,w=140,h=58):
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=12,fill='#1a3047',outline=COL[c],width=3)
    tx(d,(x,y),s,23,c,True,'mm')

def draw(section,i):
    im=Image.new('RGB',(W,H),COL['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((31,82,555,642),radius=15,fill=COL['panel'],outline=COL['line'],width=2)
    d.rounded_rectangle((570,82,1246,642),radius=15,fill=COL['panel'],outline=COL['line'],width=2)
    tx(d,(37,23),'SANG MATH / ĐẠI SỐ TỔ HỢP',25,'cyan',True)
    tx(d,(780,23),'COMB01 · QUY TẮC CỘNG',24,'muted')
    d.line((28,70,1252,70),fill=COL['line'],width=2)
    matches=[b for b in BEATS if b.section==section]
    b=matches[min(i,len(matches)-1)]
    tx(d,(650,113),CHAPTER_LABELS[section],23,'cyan',True)
    tx(d,(610,170),b.heading,29,'gold',True)
    for j,l in enumerate(b.lines):tx(d,(616,236+j*52),l,27,'text')
    d.line((610,486,1211,486),fill=COL['line'],width=2)
    # Fit long takeaway by shrinking slightly
    takeaway=b.takeaway
    size=24
    while d.textlength(takeaway,font=font(size,True))>592 and size>16:size-=1
    tx(d,(918,554),takeaway,size,'green',True,'mm')
    tx(d,(42,678),'PHÁC THẢO BỐ CỤC · KHÔNG PHẢI KHUNG HÌNH MANIM',18,'muted')
    if section=='roads':
        ax,ay,bx,by=95,353,485,353
        for j,(dy,col) in enumerate([(180,'cyan'),(106,'cyan'),(44,'gold'),(-110,'gold'),(-171,'gold')]):
            p=[(ax+q*(bx-ax)/40,ay-dy*4*q*(40-q)/(40*40)) for q in range(41)]
            d.line(p,fill=COL[col],width=4)
            tx(d,(200+j%2*112,ay-dy*.68),('Xe '+str(j+1)) if j<2 else 'Tàu '+str(j-1),20,col,True)
        d.ellipse((ax-10,ay-10,ax+10,ay+10),fill='white')
        d.ellipse((bx-10,by-10,bx+10,by+10),fill='white')
        tx(d,(ax-40,ay-30),'A',28,'text',True);tx(d,(bx+12,by-30),'B',28,'text',True)
    elif section in ('count','books'):
        top=['Xe 1','Xe 2'] if section=='count' else ['T1','T2','T3','T4']
        bottom=['Tàu 1','Tàu 2','Tàu 3'] if section=='count' else ['L1','L2','L3']
        tx(d,(85,128),'NHÓM 1',25,'cyan',True)
        for j,s in enumerate(top): capsule(d,128+j*(300/max(1,len(top)-1)),247,s,'cyan',95)
        tx(d,(85,361),'NHÓM 2',25,'gold',True)
        for j,s in enumerate(bottom):capsule(d,128+j*(300/max(1,len(bottom)-1)),473,s,'gold',108)
    elif section=='rule':
        for x,c,t,s in [(162,'cyan','PHƯƠNG ÁN A','m cách'),(420,'gold','PHƯƠNG ÁN B','n cách')]:
            d.rounded_rectangle((x-112,230,x+112,449),radius=18,fill='#1a3047',outline=COL[c],width=3)
            tx(d,(x,278),t,21,c,True,'mm');tx(d,(x,365),s,32,'text',True,'mm')
        tx(d,(292,530),'m + n',36,'green',True,'mm')
    elif section in ('overlap','distinct','quiz'):
        stop=20 if section=='distinct' else 15 if section=='quiz' else 12
        cols=5 if stop>12 else 4
        spacing=93 if cols==5 else 113
        for n in range(1,stop+1):
            x=101+(n-1)%cols*spacing;y=195+(n-1)//cols*97
            if section=='distinct': c='cyan' if n%2 else 'gold' if n%4==0 else 'muted'
            else:c='red' if n%6==0 else 'cyan' if n%2==0 else 'gold' if n%3==0 else 'muted'
            capsule(d,x,y,str(n),c,73,64)
    elif section=='compare':
        tx(d,(148,154),'ÁO',26,'cyan',True);tx(d,(404,154),'MŨ',26,'gold',True)
        for j in range(3): capsule(d,160,262+j*96,'ÁO '+str(j+1),'cyan',140)
        for j in range(2): capsule(d,406,286+j*125,'MŨ '+str(j+1),'gold',138)
        tx(d,(280,593),'HOẶC: 5     VÀ: 6',23,'green',True,'mm')
    return im


def main():
    target=ROOT/'preview'/'comb01_v2';target.mkdir(parents=True,exist_ok=True)
    sections=['roads','count','rule','books','overlap','distinct','compare','quiz']
    for sec in sections: draw(sec,4 if sec not in ('distinct','compare') else 3).save(target/f'{sec}.png')
    sheet=Image.new('RGB',(1280,1440),COL['bg'])
    for i,sec in enumerate(sections):
        frame=Image.open(target/f'{sec}.png').resize((640,360))
        sheet.paste(frame,((i%2)*640,(i//2)*360))
    sheet.save(target/'storyboard_8_chapters.png')
    print('Saved storyboard sketches:',target)

if __name__=='__main__':main()
