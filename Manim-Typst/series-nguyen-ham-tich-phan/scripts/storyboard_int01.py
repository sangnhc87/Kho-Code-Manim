"""Create eight standalone 1600x900 chapter design frames (NOT actual Manim renders)."""
from __future__ import annotations
import sys,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from int01.lesson import SEGMENTS,CHAPTERS
OUT=ROOT/'preview/int01';OUT.mkdir(parents=True,exist_ok=True)
BG='#0B1221';PANEL='#101C30';STROKE='#293A54';WHITE='#F1F5F9'
SOFT='#A9B8CA';CYAN='#38CDE6';GREEN='#40D7A5';GOLD='#F6C65B'
PURPLE='#B59AFE';CORAL='#FB877F'
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
if not Path(FONT).is_file():FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(BOLD).is_file():BOLD=FONT

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def center_text(d,xy,s,size=28,color=WHITE,bold=False):
    f=font(size,bold);bounds=d.textbbox((0,0),s,font=f);w=bounds[2]-bounds[0];h=bounds[3]-bounds[1]
    d.text((xy[0]-w/2,xy[1]-h/2),s,font=f,fill=color)
def wrap(d,text,maxw,size=29,bold=False):
    text=str(text).replace('−','-')
    f=font(size,bold);res=[];line=''
    for word in str(text).split():
        n=(line+' '+word).strip()
        if d.textbbox((0,0),n,font=f)[2]<=maxw:line=n
        else:
            if line:res.append(line)
            line=word
    if line:res.append(line)
    return res

def draw_graph(d,chapter,step):
    x0,x1=-2.05,2.05;y0,y1=-3.1,7.5
    if chapter==1:x0,x1=-2.1,2.1;y0,y1=-5,5
    if chapter==7:x0,x1=0,3.25;y0,y1=0,15
    if chapter==8:x0,x1=-1.55,1.55;y0,y1=-3,8.5
    px0,px1=155,713;py0,py1=270,660
    to_x=lambda x:px0+(x-x0)/(x1-x0)*(px1-px0)
    to_y=lambda y:py1-(y-y0)/(y1-y0)*(py1-py0)
    # Grids are thin and unsaturated to avoid overpowering the curves.
    for i in range(math.ceil(x0),math.floor(x1)+1):
        xx=to_x(i);d.line((xx,py0,xx,py1),fill='#24344A',width=2)
        if y0<=0<=y1:d.text((xx-5,to_y(0)+7),str(i),font=font(17),fill=SOFT)
    for j in range(math.ceil(y0),math.floor(y1)+1,2 if chapter!=7 else 3):
        yy=to_y(j);d.line((px0,yy,px1,yy),fill='#24344A',width=2)
    if y0<=0<=y1:d.line((px0,to_y(0),px1,to_y(0)),fill='#7C95B0',width=3)
    if x0<=0<=x1:d.line((to_x(0),py0,to_x(0),py1),fill='#7C95B0',width=3)
    d.text((px1+8,to_y(0)+4 if y0<0<y1 else py1-17),'x' if chapter!=7 else 't',font=font(24),fill=WHITE)
    def plot(fun,color,width=7,low=None,high=None):
        lo=x0+0.04 if low is None else low;hi=x1-0.04 if high is None else high
        pts=[]
        for k in range(500):
            xv=lo+(hi-lo)*k/499;yv=fun(xv)
            if y0<=yv<=y1:pts.append((to_x(xv),to_y(yv)))
            elif len(pts)>=2:
                d.line(pts,fill=color,width=width,joint='curve');pts=[]
        if len(pts)>=2:d.line(pts,fill=color,width=width,joint='curve')
    def point(x,y,label=None,color=GOLD):
        xx,yy=to_x(x),to_y(y);d.ellipse((xx-10,yy-10,xx+10,yy+10),fill=color)
        if label:d.text((xx+14,yy-40),label,font=font(23,True),fill=color)
    def connector(x,low,high):
        xx=to_x(x);a,b=to_y(low),to_y(high)
        for top in range(round(b),round(a),16):d.line((xx,top,xx,min(top+8,round(a))),fill=GOLD,width=3)
    if chapter==1:
        plot(lambda x:2*x,CYAN);point(1,2,'f(1)=2')
        center_text(d,(430,206),'ĐỒ THỊ ĐẠO HÀM f(x)=2x',28,CYAN,True)
    elif chapter==2:
        plot(lambda x:x*x,CYAN);point(1,1,'độ dốc = 2')
        d.line((to_x(.33),to_y(-.34),to_x(1.67),to_y(2.34)),fill=GOLD,width=6)
        center_text(d,(430,206),'ĐẠO HÀM CỦA x² LÀ 2x',28,CYAN,True)
    elif chapter==3:
        for c,col in [(-2,PURPLE),(0,CYAN),(2,GREEN)]:plot(lambda x,k=c:x*x+k,col)
        d.text((180,620),'C = -2',font=font(21,True),fill=PURPLE)
        d.text((365,540),'C = 0',font=font(21,True),fill=CYAN)
        d.text((565,356),'C = 2',font=font(21,True),fill=GREEN)
        center_text(d,(430,206),'MỘT HỌ ĐƯỜNG CONG',28,CYAN,True)
    elif chapter==4:
        for c,col in [(-2,PURPLE),(0,CYAN),(2,GREEN)]:
            plot(lambda x,k=c:x*x+k,col)
            d.line((to_x(.53),to_y(1+c+2*(.53-1)),to_x(1.47),to_y(1+c+2*(1.47-1))),fill=GOLD,width=5)
            point(1,1+c)
        center_text(d,(430,206),'CÙNG x, CÙNG HỆ SỐ GÓC',28,CYAN,True)
    elif chapter==5:
        plot(lambda x:x*x-1,PURPLE);plot(lambda x:x*x+2,GREEN)
        for xv in [-1.25,-.5,.3,1.15]:connector(xv,xv*xv-1,xv*xv+2)
        center_text(d,(430,206),'KHOẢNG CÁCH ĐỀU BẰNG 3',28,CYAN,True)
    elif chapter==6:
        plot(lambda x:x*x+2,GREEN);point(1,3,'(1; 3)')
        connector(1,0,3)
        center_text(d,(430,206),'ĐIỀU KIỆN F(1)=3',28,CYAN,True)
    elif chapter==7:
        plot(lambda t:t*t+t+2,GREEN,low=0,high=3)
        plot(lambda t:2*t+1,CYAN,low=0,high=3)
        point(0,2,'s(0)=2')
        d.text((460,285),'s(t)',font=font(24,True),fill=GREEN)
        d.text((510,506),'v(t)',font=font(24,True),fill=CYAN)
        center_text(d,(430,206),'TỪ VẬN TỐC ĐẾN TỌA ĐỘ',28,CYAN,True)
    elif chapter==8:
        plot(lambda x:x*x*x+4,GREEN);point(1,5,'(1; 5)')
        center_text(d,(430,206),'TÌM HÀM ĐI QUA (1; 5)',28,CYAN,True)

FORMULA=["f(x) = 2x", "F(x) = x²", "F(x) = x² + C", "F′(x) = 2x", "F₂(x) - F₁(x) = 3", "F(x) = x² + 2", "s(t) = t² + t + 2", "G(x) = x³ + 4"]
SELECT=[2,1,2,2,2,3,3,4]

def make(chapter):
    seg=SEGMENTS[(chapter-1)*4+SELECT[chapter-1]-1]
    im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((33,126,789,791),radius=23,fill=PANEL,outline=STROKE,width=3)
    d.rounded_rectangle((808,126,1567,791),radius=23,fill=PANEL,outline=STROKE,width=3)
    d.line((37,96,1565,96),fill=STROKE,width=3);d.line((37,843,1565,843),fill=STROKE,width=3)
    d.text((48,29),'NGUYÊN HÀM',font=font(38,True),fill=CYAN)
    d.text((899,29),'TỪ ĐẠO HÀM ĐI NGƯỢC',font=font(32,True),fill=WHITE)
    draw_graph(d,chapter,SELECT[chapter-1])
    title_lines=wrap(d,seg.title.upper(),675,36,True)
    for i,line in enumerate(title_lines):d.text((850,184+i*52),line,font=font(36,True),fill=WHITE)
    ypos=284 if len(title_lines)<2 else 345
    for i,line in enumerate(wrap(d,seg.takeaway,665,31)):
        d.text((850,ypos+i*46),line,font=font(31),fill=SOFT)
    d.rounded_rectangle((850,452,1525,568),radius=14,fill='#1B304A',outline='#28576B',width=2)
    center_text(d,(1187,500),FORMULA[chapter-1],41,GOLD,True)
    d.line((856,624,1518,624),fill=STROKE,width=2)
    for i,line in enumerate(wrap(d,CHAPTERS[chapter-1],640,30,True)):
        d.text((851,667+i*37),line,font=font(30,True),fill=CYAN)
    center_text(d,(800,869),'Thầy Nguyễn Văn Sang',23,SOFT,True)
    path=OUT/f'INT01_chapter_{chapter:02d}.png';im.save(path,optimize=True)
    return im

def main():
    ims=[make(i) for i in range(1,9)]
    montage=Image.new('RGB',(2400,2700),BG)
    for k,im in enumerate(ims):
        small=im.resize((1200,675),Image.Resampling.LANCZOS)
        montage.paste(small,((k%2)*1200,(k//2)*675))
    montage.save(OUT/'INT01_storyboard_8_chapters.png',optimize=True)
    print('INT01_STORYBOARD_OK',len(ims),'frames')
if __name__=='__main__':main()
