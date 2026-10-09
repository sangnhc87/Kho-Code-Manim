"""Clean eight-chapter graphic; intentionally not a video frame."""
from pathlib import Path
import math,sys
from PIL import Image,ImageFont,ImageDraw
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat15.lesson import BAR_VALUES,YEARS,YEAR_VALUES,PICTOGRAM_VALUES,CLASSES,CLASS_COUNTS,CLASS_TOTALS,TREND_VALUES,CHALLENGE_VALUES
W,H=1480,1810
BG='#0A1522';PANEL='#10293B';EDGE='#355A71';WHITE='#EDF6FF'
CYAN='#56CBE9';GOLD='#FFD379';GREEN='#67DDB5';CORAL='#FF8E87';MUTED='#ADC6D5'
font_dir=Path('/usr/share/fonts/truetype/dejavu')
font=str(font_dir/'DejaVuSans.ttf');bold=str(font_dir/'DejaVuSans-Bold.ttf')
F1=ImageFont.truetype(bold,31);F2=ImageFont.truetype(bold,21)
F3=ImageFont.truetype(font,18);F4=ImageFont.truetype(bold,17)
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((55,29),'SANGMATH  |  THỐNG KÊ 10–12',font=F1,fill=CYAN)
d.text((55,79),'STAT15 – BIỂU ĐỒ GÂY HIỂU NHẦM',font=F1,fill=WHITE)
names=[('Cắt trục tung','80 và 100: không phải gấp 5'),('Đổi thang tung','Cùng dãy 40 – 44 – 52 – 56'),
 ('Khoảng cách thời gian','Mốc 2020, 2021, 2024, 2025'),('Biểu tượng phóng đại','Gấp 2 bán kính → gấp 4 diện tích'),
 ('Số lượng và tỉ lệ','18/30 = 60%; 24/80 = 30%'),('Chọn khoảng thời gian','Ngắn hạn −10%; toàn kỳ +28%'),
 ('Histogram lớp không đều','Mật độ 4 – 3 – 6 – 3'),('Thử thách sửa biểu đồ','62% và 68%: chênh 6 điểm %')]
for i,(name,sub) in enumerate(names):
 row,col=divmod(i,2);x=55+col*710;y=151+row*388
 d.rounded_rectangle((x,y,x+675,y+360),radius=19,fill=PANEL,outline=EDGE,width=2)
 d.text((x+23,y+17),f'{i+1:02d}   {name}',fill=WHITE,font=F2)
 d.text((x+22,y+318),sub,fill=GOLD,font=F4)
 x0=x+117;yo=y+273
 if i in (0,1,4,7):
  nums={0:(5,25),1:(40,56),4:(18,24),7:(2,8)}[i]
  for j,n in enumerate(nums):
   h=n/max(nums)*164
   bx=x+170+j*233
   d.rectangle((bx,yo-h,bx+105,yo),fill=CYAN if j==0 else CORAL)
   value=(BAR_VALUES[j] if i==0 else CHALLENGE_VALUES[j] if i==7 else n)
   d.text((bx+20,yo-h-29),str(value),font=F2,fill=GOLD)
  if i in (0,7):d.text((x+22,y+84),f'Gốc trục: {75 if i==0 else 60}',font=F3,fill=MUTED)
  d.line((x+101,yo,x+566,yo),fill=MUTED,width=3)
 elif i==2:
  a,b=2020,2025;vals=YEAR_VALUES
  pts=[(x+105+(yr-a)/(b-a)*480,y+254-(v-38)/20*165) for yr,v in zip(YEARS,vals)]
  d.line(pts,fill=CYAN,width=5)
  for xx,yy in pts:d.ellipse((xx-7,yy-7,xx+7,yy+7),fill=GOLD)
  for year in YEARS:d.text((x+94+(year-a)/(b-a)*480,y+276),str(year),font=F3,fill=MUTED)
 elif i==3:
  d.ellipse((x+143,y+145,x+243,y+245),outline=CYAN,width=4)
  d.ellipse((x+368,y+97,x+568,y+297),outline=CORAL,width=4)
  d.text((x+173,y+266),'20',font=F2,fill=CYAN);d.text((x+451,y+300),'40',font=F2,fill=CORAL)
 elif i==5:
  pts=[(x+107+j*95,y+255-(v-48)*7) for j,v in enumerate(TREND_VALUES)]
  d.line(pts,fill=CYAN,width=5)
  for xx,yy in pts:d.ellipse((xx-6,yy-6,xx+6,yy+6),fill=GOLD)
 elif i==6:
  for j,(a,b,f) in enumerate(CLASSES):
   h=(f/(b-a))*27
   left=x+105+a*45;right=x+105+b*45
   d.rectangle((left,yo-h,right-2,yo),fill=(CYAN,GREEN,GOLD,CORAL)[j])
   d.text((left+10,yo-h-26),f'{f}',font=F3,fill=WHITE)
  d.line((x+100,yo,x+570,yo),fill=MUTED,width=3)
d.text((55,H-95),'STORYBOARD THIẾT KẾ  |  CHƯA PHẢI KHUNG HÌNH RENDER',fill=MUTED,font=F3)
footer='Thầy Nguyễn Văn Sang';wid=d.textbbox((0,0),footer,font=F2)[2]
d.text(((W-wid)//2,H-51),footer,font=F2,fill=WHITE)
out=ROOT/'preview/stat15/STAT15_storyboard_8_chapters.png'
out.parent.mkdir(parents=True,exist_ok=True);im.save(out,optimize=True)
print('STAT15_PREVIEW_OK',out,W,H)
