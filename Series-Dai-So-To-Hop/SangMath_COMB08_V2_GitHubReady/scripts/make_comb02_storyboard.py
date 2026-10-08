"""Generate visual mockups for COMB02 (Pillow mockup, NOT Manim render)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'; OUT.mkdir(exist_ok=True)
COL={'bg':'#0B1120','panel':'#101F33','panel2':'#172A43','line':'#2E4862',
 'text':'#ECF4FF','muted':'#A8B9CC','cyan':'#22D3EE','gold':'#FBBF24',
 'red':'#EF4444','green':'#22C55E'}
REG='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
W,H=1600,900

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else REG,size)

def base():
 im=Image.new('RGB',(W,H),COL['bg']);d=ImageDraw.Draw(im)
 d.text((70,41),'SANG MATH  /  ĐẠI SỐ TỔ HỢP',font=font(29,True),fill=COL['cyan'])
 d.text((1070,43),'COMB02 · QUY TẮC NHÂN',font=font(26),fill=COL['muted'])
 d.line((70,105,1530,105),fill=COL['line'],width=2)
 d.rounded_rectangle((45,133,733,786),radius=27,fill=COL['panel'],outline=COL['line'],width=2)
 d.rounded_rectangle((758,133,1555,786),radius=27,fill=COL['panel'],outline=COL['line'],width=2)
 d.text((438,830),'BẢN PHÁC THẢO · CHƯA PHẢI RENDER MANIM',font=font(24),fill=COL['muted'])
 return im,d

def title(d,a,b):
 d.text((100,177),a,font=font(42,True),fill=COL['text'])
 d.text((100,238),b,font=font(27),fill=COL['muted'])

def right(d,t,lines,eq=None,concl=None):
 d.text((805,191),t,font=font(36,True),fill=COL['gold'])
 y=285
 for line in lines:
  d.text((813,y),line,font=font(29),fill=COL['text']);y+=66
 if eq:
  d.text((855,570),eq,font=font(57,True),fill=COL['cyan'])
 if concl:
  d.rounded_rectangle((822,700,1495,748),radius=12,fill=COL['panel2'],outline='#65519A',width=2)
  d.text((839,708),concl,font=font(22),fill=COL['text'])

def shirt(d,x,y,name):
 pts=[(-46,-30),(-25,-46),(-12,-36),(12,-36),(25,-46),(46,-30),(72,9),(45,28),(37,13),(37,58),(-37,58),(-37,13),(-45,28),(-72,9)]
 d.polygon([(x+a,y+b) for a,b in pts],fill='#0D4964')
 d.line([(x+a,y+b) for a,b in pts]+[(x+pts[0][0],y+pts[0][1])],fill=COL['cyan'],width=4)
 d.text((x-27,y-15),name,font=font(30,True),fill=COL['text'])

def pants(d,x,y,name):
 pts=[(-44,-43),(44,-43),(37,62),(5,62),(0,4),(-5,62),(-37,62)]
 d.polygon([(x+a,y+b) for a,b in pts],fill='#55421E')
 d.line([(x+a,y+b) for a,b in pts]+[(x+pts[0][0],y+pts[0][1])],fill=COL['gold'],width=4)
 d.text((x-29,y-29),name,font=font(30,True),fill=COL['text'])

def frame_intro():
 im,d=base();title(d,'Mặc gì hôm nay?','3 áo khác nhau · 2 quần khác nhau')
 for i,x in enumerate((210,395,575)):shirt(d,x,413,f'A{i+1}')
 for i,x in enumerate((294,495)):pants(d,x,620,f'Q{i+1}')
 right(d,'BÀI TOÁN MỞ ĐẦU',[
  'Có 3 chiếc áo khác nhau',
  'và 2 chiếc quần khác nhau.',
  'Mỗi bộ gồm 1 áo và 1 quần.',
  'Có bao nhiêu bộ trang phục?'
 ],concl='Đếm đủ số bộ khác nhau')
 return im

def frame_grid():
 im,d=base();title(d,'Ghép tất cả các bộ','Mỗi cặp được tính đúng một lần')
 for i,x in enumerate((190,395,600)):
  for j,y in enumerate((396,590)):
   d.rounded_rectangle((x-90,y-67,x+90,y+76),radius=18,fill=COL['panel2'],outline=COL['line'],width=2)
   shirt(d,x-34,y-12,f'A{i+1}');pants(d,x+49,y-12,f'Q{j+1}')
 right(d,'QUY TẮC NHÂN',[
  'Với mỗi áo có 2 quần.',
  'Có tổng cộng 3 áo.',
  'Mỗi cặp là một bộ khác nhau.'
 ],eq='3 × 2 = 6',concl='3 nhóm · mỗi nhóm có 2 kết quả')
 return im

def frame_forbidden():
 im,d=base();title(d,'Khi có trường hợp cấm','Cặp (A1, Q2) không được phép')
 for i,x in enumerate((190,395,600)):
  for j,y in enumerate((396,590)):
   color=COL['red'] if (i,j)==(0,1) else COL['green']
   d.rounded_rectangle((x-89,y-64,x+90,y+76),radius=18,fill=COL['panel2'],outline=color,width=3)
   shirt(d,x-33,y-12,f'A{i+1}');pants(d,x+49,y-12,f'Q{j+1}')
   if (i,j)==(0,1):
    d.line((x-76,y-52,x+76,y+65),fill=color,width=8)
    d.line((x-76,y+65,x+76,y-52),fill=color,width=8)
 right(d,'LOẠI 1 CẶP BỊ CẤM',[
  'Ban đầu có 6 bộ.',
  'A1 không đi cùng Q2.',
  'Loại đúng 1 trường hợp.',
  'Còn lại 5 bộ hợp lệ.'
 ],eq='6 - 1 = 5',concl='Kiểm tra lại: 1 + 2 + 2 = 5')
 return im

def main():
 pairs=[('COMB02_01_mo_dau',frame_intro),('COMB02_02_sau_bo',frame_grid),('COMB02_03_cap_cam',frame_forbidden)]
 imgs=[]
 for name,fn in pairs:
  img=fn();img.save(OUT/f'{name}.png',optimize=True);imgs.append(img)
 sheet=Image.new('RGB',(1140,1390),COL['bg']);d=ImageDraw.Draw(sheet)
 for idx,im in enumerate(imgs):
  x=40;y=33+idx*394
  sheet.paste(im.resize((1060,596),Image.Resampling.LANCZOS).resize((1060,370),Image.Resampling.LANCZOS),(x,y))
 d.text((54,1240),'COMB02 · BA KHUNG STORYBOARD',font=font(35,True),fill=COL['text'])
 d.text((54,1305),'Dựng bằng Pillow. Chưa phải khung hình Manim.',font=font(24),fill=COL['muted'])
 sheet.save(OUT/'COMB02_storyboard_contact_sheet.png')
 print('Created COMB02 mockups:',len(imgs)+1)

if __name__=='__main__':main()
