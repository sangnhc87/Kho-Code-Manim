"""Create storyboard and Vietnamese teacher narration (not rendered Manim frames)."""
from pathlib import Path
import sys,textwrap
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
from stat10.lesson import CHAPTERS,BEATS,MAIN,ALT,BOUND,IQR,REVERSE
OUT=ROOT/'preview/stat10';OUT.mkdir(parents=True,exist_ok=True)
FONT_FILE='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD_FILE='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F=lambda size,b=False:ImageFont.truetype(BOLD_FILE if b else FONT_FILE,size)
C={'bg':'#081522','panel':'#102b3e','line':'#35596e','white':'#f0f8ff','muted':'#aac4d3','cyan':'#5ed0ec','gold':'#ffd57c','green':'#72dfb6','purple':'#b7a6fa','coral':'#ff938d'}

def txt(d,s,x,y,size=22,c='white',width=580,bold=False):
    s=str(s);font=F(size,bold)
    while size>=13 and d.textbbox((0,0),s,font=font)[2]>width:
        size-=1;font=F(size,bold)
    box=d.textbbox((0,0),s,font=font)
    d.text((int(x-(box[2]-box[0])/2),int(y)),s,font=font,fill=C.get(c,c))

def hist(d,nums=(6,18,14,2),selected=1):
    txt(d,'BẢNG TẦN SỐ / HISTOGRAM',390,211,22,'cyan',590,True)
    x0=126;width=120;space=18;floor=572
    d.line((94,floor,699,floor),fill=C['line'],width=3)
    for i,(x,v) in enumerate(zip(range(4),nums)):
        ax=x0+i*(width+space)
        hh=v/max(1,max(nums))*246
        color=C['gold'] if i==selected else C[['cyan','green','purple','coral'][i]]
        d.rectangle((ax,floor-hh,ax+width,floor),fill=color)
        txt(d,str(v),ax+width/2,floor-hh-31,20,'white',100,True)
        txt(d,('[4;6)','[6;8)','[8;10)','[10;12)')[i],ax+width/2,floor+10,14,'muted',width+20)

def cumulative(d,values=(6,24,38,40)):
    txt(d,'TẦN SỐ TÍCH LŨY',390,211,22,'cyan',570,True)
    base=568;top=316;left=126;width=118;gap=22
    d.line((98,base,697,base),fill=C['line'],width=3)
    for i,v in enumerate(values):
        x=left+i*(width+gap);height=245*v/max(values)
        d.rounded_rectangle((x,base-height,x+width,base),radius=6,fill=C['gold'] if i==2 else C['cyan'])
        txt(d,str(v),x+width/2,base-height-31,21,'white',100,True)

def lineplot(d,upto=3):
    txt(d,'OGIVE / ĐƯỜNG TÍCH LŨY',390,200,22,'cyan',570,True)
    left,right=120,683;bottom,top=585,270
    X=lambda x:left+(x-4)*(right-left)/8
    Y=lambda n:bottom-n*(bottom-top)/40
    coords=[(4,0),(6,6),(8,24),(10,38),(12,40)]
    pts=[(X(a),Y(b)) for a,b in coords]
    d.line(pts,fill=C['cyan'],width=5,joint='curve')
    d.line([(left,bottom),(right,bottom)],fill=C['line'],width=3)
    for p in pts:d.ellipse((p[0]-6,p[1]-6,p[0]+6,p[1]+6),fill=C['gold'])
    for i,q in enumerate(MAIN[:upto]):
        y=Y(q.rank);x=X(q.value)
        color=C[['green','gold','purple'][i]]
        d.line((left,y,x,y),fill=color,width=3)
        d.line((x,y,x,bottom),fill=color,width=3)
        txt(d,f'Q{i+1}',x,y-34,15,color,55,True)

def drawing(i):
    im=Image.new('RGB',(1420,760),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((36,93,746,689),radius=15,fill=C['panel'],outline=C['line'],width=3)
    d.rounded_rectangle((765,93,1384,689),radius=15,fill=C['panel'],outline=C['line'],width=3)
    txt(d,'SANGMATH • THỐNG KÊ 10 • TỨ PHÂN VỊ GHÉP NHÓM',710,22,31,'white',1350,True)
    txt(d,f'CHƯƠNG {i+1:02d} / 08',1073,126,23,'cyan',540,True)
    lines=textwrap.wrap(CHAPTERS[i],32)
    for z,line in enumerate(lines[:3]):txt(d,line,1073,185+z*34,25,'white',548,True)
    facts=[
        ('Q1 gốc = 6  •  Q2 gốc = 7','Q3 gốc = 8'),
        ('Tích lũy: 6, 24, 38, 40','Mốc 10 • 20 • 30'),
        ('Q1 ≈ 6,44','Đi 4/18 lớp [6;8)'),
        ('Q2 ≈ 7,56','Đi 14/18 lớp [6;8)'),
        ('Q3 ≈ 8,86','IQR ≈ 2,41'),
        ('25% → Q1 ≈ 6,44','50% → Q2; 75% → Q3'),
        ('Ranh giới: 6 • 8 • 10','Ghép khác: 6,50 • 7,67 • 8,78'),
        ('Q1 = 6,5 → x = 16','Q2 = 7,75; Q3 = 9; IQR=2,5'),
    ][i]
    for j,f in enumerate(facts):txt(d,f,1073,447+j*46,24,'gold' if j==0 else 'green',555,j==0)
    if i in (0,2,3,4):hist(d,selected=(1,1,1,2)[(0,2,3,4).index(i)])
    elif i==1:cumulative(d)
    elif i==5:lineplot(d,3)
    elif i==6:hist(d,(6,8,18,8),2)
    else:hist(d,(6,16,16,2),1)
    d.text((51,719),'STORYBOARD MINH HỌA • KHÔNG PHẢI KHUNG HÌNH MANIM ĐÃ RENDER',font=F(15),fill=C['muted'])
    im.save(OUT/f'STAT10_chapter_{i+1:02d}.png')

for i in range(8):drawing(i)
board=Image.new('RGB',(1430,1740),C['bg'])
for i in range(8):
    small=Image.open(OUT/f'STAT10_chapter_{i+1:02d}.png').resize((690,369),Image.Resampling.LANCZOS)
    board.paste(small,(19+(i%2)*709,40+(i//2)*422))
board.save(OUT/'STAT10_storyboard_8_chapters.png')
narr=['# THONG-KE-10 – TỨ PHÂN VỊ MẪU SỐ LIỆU GHÉP NHÓM','',
      'Dữ liệu giả lập 40 điểm; 32 nhịp, 8 chương, thời lượng nền 18 phút 08 giây.','']
story=['# STORYBOARD THONG-KE-10','',
       'Bố cục 16:9: dữ liệu và hình động bên trái, lập luận và SVG Typst bên phải.','',
       'Giá trị tứ phân vị ghép nhóm là nội suy xấp xỉ, không thay thế tứ phân vị dữ liệu gốc.','']
for i,ch in enumerate(CHAPTERS):
    narr.extend([f'## Chương {i+1:02d}: {ch}',''])
    story.extend([f'## Chương {i+1:02d}: {ch}',''])
    for b in BEATS[i*4:(i+1)*4]:
        narr.extend([f'### Nhịp {b.step}: {b.title}',b.voice,''])
        story.extend([f'### Nhịp {b.step}: {b.title}',f'- Luận điểm: {b.thesis}',
                      '- Hoạt hình thay đổi theo trạng thái 1–4; công thức Typst xuất ở hai trạng thái cuối.',
                      f'- Thời lượng thiết kế: {b.duration:.0f} giây.',''])
(ROOT/'LOI_GIANG_STAT10.md').write_text('\n'.join(narr)+'\n',encoding='utf-8')
(ROOT/'STORYBOARD_STAT10.md').write_text('\n'.join(story)+'\n',encoding='utf-8')
print('STAT10_STORYBOARD_OK',len(BEATS),'beats','8 chapter images','words',sum(len(b.voice.split()) for b in BEATS))
