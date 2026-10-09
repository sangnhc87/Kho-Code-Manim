"""Storyboard-only image (not an actual Manim render)."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from stat07.lesson import CHAPTERS,CLASSES,FREQ,CUM,REL,ASYM,ASYM_FREQ,ASYM_DENS,PFREQ
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview/stat07';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
C={'bg':'#07121f','panel':'#0f293d','cyan':'#54cbe9','gold':'#ffd479','green':'#67ddb5','white':'#eef6ff','muted':'#9db9c9','orange':'#ff918a','purp':'#b1a6ef','line':'#31526b'}
TOPICS=[
 ('40 ĐIỂM → 4 LỚP',FREQ,'6 + 18 + 14 + 2 = 40'),
 ('RANH GIỚI NỬA KÍN',FREQ,'6 ∈ [6;8), không thuộc [4;6)'),
 ('TẦN SỐ TÍCH LŨY',CUM,'6 → 24 → 38 → 40'),
 ('TẦN SỐ TƯƠNG ĐỐI',[15,45,35,5],'15% + 45% + 35% + 5% = 100%'),
 ('HISTOGRAM: MẬT ĐỘ',[3,8,9,4],'Chiều cao = tần số / độ rộng'),
 ('THÔNG TIN BỊ MẤT',FREQ,'Trung bình gốc 7,1 ≠ ước lượng 7,6'),
 ('ĐỔI CÁCH CHIA LỚP',ASYM_FREQ,'Cùng dữ liệu → bảng tần số đổi'),
 ('BÀI TẬP 20 QUAN SÁT',PFREQ,'5 + 7 + 6 + 2 = 20'),
]
def centered(d,xy,text,size,color,bold=False,maxwidth=None):
    f=font(size,bold)
    if maxwidth:
        while d.textbbox((0,0),text,font=f)[2]>maxwidth and size>12:
            size-=1;f=font(size,bold)
    box=d.textbbox((0,0),text,font=f);tw=box[2]-box[0]
    d.text((xy[0]-tw/2,xy[1]),text,font=f,fill=color)
def draw_chart(d,vals,x0,y0,w,h):
    base=y0+h;d.line((x0,base,x0+w,base),fill=C['muted'],width=3)
    colors=(C['cyan'],C['green'],C['purp'],C['orange'])
    maxv=max(vals)
    for i,v in enumerate(vals):
        x=x0+i*w/4+4
        bw=w/4-8
        barh=max(6,h*.76*v/maxv)
        d.rectangle((x,base-barh,x+bw,base),fill=colors[i])
        centered(d,(x+bw/2,base-barh-25),str(v),22,C['gold'],True)
    for i,lab in enumerate(('I','II','III','IV')):
        centered(d,(x0+(i+.5)*w/4,base+11),lab,15,C['muted'])
for i,(head,vals,explain) in enumerate(TOPICS):
    im=Image.new('RGB',(1280,720),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((25,30,1255,688),radius=26,fill=C['panel'],outline=C['line'],width=3)
    d.text((58,61),f'SANGMATH  /  STAT07  /  CHƯƠNG {i+1:02d}',font=font(24,True),fill=C['cyan'])
    d.text((58,106),head,font=font(30,True),fill=C['white'])
    d.line((58,168,1222,168),fill=C['line'],width=3)
    d.rounded_rectangle((55,197,693,610),radius=17,outline=C['line'],width=3)
    draw_chart(d,vals,106,265,545,270)
    d.rounded_rectangle((715,197,1225,610),radius=17,outline=C['line'],width=3)
    d.text((749,227),'LUẬN ĐIỂM',font=font(25,True),fill=C['cyan'])
    centered(d,(971,345),explain,27,C['gold'],True,445)
    d.text((752,518),'Dữ liệu và kết quả được',font=font(21),fill=C['muted'])
    d.text((752,553),'tính từ cùng một nguồn.',font=font(21),fill=C['muted'])
    d.text((60,636),'MINH HỌA STORYBOARD — KHÔNG PHẢI KHUNG HÌNH MANIM ĐÃ RENDER',font=font(17),fill=C['muted'])
    im.save(OUT/f'STAT07_chapter_{i+1:02d}.png')
w,h=2*690+55,4*410+90
coll=Image.new('RGB',(w,h),C['bg'])
for i in range(8):
    img=Image.open(OUT/f'STAT07_chapter_{i+1:02d}.png').resize((670,377),Image.Resampling.LANCZOS)
    coll.paste(img,(25+(i%2)*690,35+(i//2)*410))
coll.save(OUT/'STAT07_storyboard_8_chapters.png')
print('STORYBOARD_OK',OUT/'STAT07_storyboard_8_chapters.png')
