"""Classroom storyboard, not a frame from rendered Manim footage."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat16.lesson import MAIN,CHALLENGE,rate,aggregate,mix,weight_easy,as_pct
W,H=1480,1810
BG='#0A1522';PANEL='#10293B';EDGE='#355A71';WHITE='#EDF6FF'
CYAN='#56CBE9';GOLD='#FFD379';GREEN='#67DDB5';CORAL='#FF8E87';MUTED='#ADC6D5';PURPLE='#B7A9FC'
fonts=Path('/usr/share/fonts/truetype/dejavu'); font=str(fonts/'DejaVuSans.ttf'); bold=str(fonts/'DejaVuSans-Bold.ttf')
F1=ImageFont.truetype(bold,31);F2=ImageFont.truetype(bold,20)
F3=ImageFont.truetype(font,17);F4=ImageFont.truetype(bold,16)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((55,27),'SANGMATH  |  THỐNG KÊ 10–12',font=F1,fill=CYAN)
d.text((55,78),'STAT16 – NGHỊCH LÝ SIMPSON',font=F1,fill=WHITE)
titles=[
 ('Hai nhóm, hai phương án','Dễ: A 90% > B 80%; khó: A 35% > B 30%'),
 ('Đọc đúng mẫu số','18/20; 72/90; 28/80; 3/10'),
 ('Kết quả gộp đảo chiều','A 46% < B 75%'),
 ('Cơ cấu mẫu khác nhau','A: 20% dễ; B: 90% dễ'),
 ('Chuẩn hóa cùng cơ cấu','Dễ/khó 50/50: A 62,5% > B 55%'),
 ('Không tự suy ra nhân quả','Tỉ lệ quan sát khác kết luận nhân quả'),
 ('Ba bẫy dễ gặp','Thiếu mẫu số và trọng số'),
 ('Bài toán tự giải','A 34% < B 62,5%'),
]
for i,(title,subtitle) in enumerate(titles):
    row,col=divmod(i,2);x=55+col*710;y=150+row*390
    d.rounded_rectangle((x,y,x+675,y+358),radius=19,fill=PANEL,outline=EDGE,width=2)
    d.text((x+22,y+18),f'{i+1:02d}   {title}',font=F2,fill=WHITE)
    d.text((x+21,y+319),subtitle,font=F4,fill=GOLD)
    y0=y+264;x0=x+119;maxw=430
    if i in (0,1,6):
        for j,(a,b) in enumerate(((.9,.8),(.35,.3)) if i==0 else ((18/20,72/90),(28/80,3/10)) if i==1 else ((.46,.75),(.625,.55))):
            yy=y+107+j*89
            for k,val in enumerate((a,b)):
                bx=x0+k*242;h=val*65
                d.rectangle((bx,yy+65-h,bx+85,yy+65),fill=(CYAN,CORAL)[k])
                d.text((bx+7,yy+70),('A' if k==0 else 'B')+' '+as_pct(val),font=F3,fill=MUTED)
    elif i in (2,4,7):
        table=CHALLENGE if i==7 else MAIN
        vals=(rate(aggregate(table,'A')),rate(aggregate(table,'B'))) if i!=4 else (mix(MAIN,'A'),mix(MAIN,'B'))
        for j,r in enumerate(vals):
            yy=y+121+j*80
            d.rectangle((x0,yy,x0+int(maxw*r),yy+34),fill=(CYAN,CORAL)[j])
            d.text((x0+12,yy+40),('A: ' if j==0 else 'B: ')+as_pct(r),font=F3,fill=GOLD)
    elif i==3:
        for j,method in enumerate(('A','B')):
            w=weight_easy(MAIN,method);yy=y+125+j*85
            d.rectangle((x0,yy,x0+maxw*w,yy+45),fill=GREEN)
            d.rectangle((x0+maxw*w,yy,x0+maxw,yy+45),fill=PURPLE)
            d.text((x0+5,yy+52),method+'  '+as_pct(w,0)+' dễ',font=F3,fill=WHITE)
    else:
        for j,line in enumerate(('Có đủ cỡ mẫu không?', 'So sánh trong từng nhóm?', 'Đã xét biến độ khó chưa?')):
            d.text((x+65,y+116+j*58),line,font=F3,fill=(CYAN,GOLD,GREEN)[j])
d.text((55,H-95),'STORYBOARD THIẾT KẾ • CHƯA PHẢI HÌNH TỪ VIDEO',font=F3,fill=MUTED)
name='Thầy Nguyễn Văn Sang';wid=d.textbbox((0,0),name,font=F2)[2]
d.text(((W-wid)//2,H-50),name,font=F2,fill=WHITE)
out=ROOT/'preview/stat16/STAT16_storyboard_8_chapters.png';out.parent.mkdir(parents=True,exist_ok=True)
im.save(out,optimize=True)
for i in range(8):
    row,col=divmod(i,2);x=55+col*710;y=150+row*390
    crop=im.crop((x,y,x+675,y+358))
    crop.save(out.parent/f'STAT16_chapter_{i+1:02d}.png',optimize=True)
print('STAT16_PREVIEW_OK',out,W,H)
