"""Narration and educational storyboard; preview is not an actual Manim frame."""
from pathlib import Path
import sys, textwrap
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
from stat09.lesson import CHAPTERS,BEATS,MAIN,ALTERNATIVE,EXERCISE

OUT=ROOT/'preview/stat09';OUT.mkdir(parents=True,exist_ok=True)
NORMAL='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
HEAVY='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT=lambda sz,b=False:ImageFont.truetype(HEAVY if b else NORMAL,sz)
C={'bg':'#081522','panel':'#112b3d','panel2':'#18374b','muted':'#a8c4d5','white':'#f0f8ff','cyan':'#64cee9','gold':'#ffd680','green':'#72d8b0','red':'#ff9d93','line':'#37586d'}


def center(d, s, x, y, size=20, color='white', maxwidth=570, bold=False):
    s=str(s);f=FONT(size,bold)
    while size>11 and d.textbbox((0,0),s,font=f)[2]>maxwidth:
        size-=1;f=FONT(size,bold)
    width=d.textbbox((0,0),s,font=f)[2]
    d.text((x-width/2,y),s,font=f,fill=C.get(color,color))


def bars(d,vals,label,color='cyan',median=None):
    center(d,label,390,240,23,'cyan',590,True)
    x0,x1=95,690;y=567;dx=(x1-x0)/len(vals)
    d.line((x0,y,x1,y),fill=C['line'],width=3)
    for i,n in enumerate(vals):
        x=x0+dx*(i+.5);h=220*n/max(vals)
        d.rectangle((x-dx*.31,y-h,x+dx*.31,y),fill=C['gold'] if median==i else C.get(color,color))
        center(d,str(n),x,y-h-29,20,'white',100,True)
        center(d,str(i+1),x,y+10,16,'muted',80)


def draw_chapter(ch):
    im=Image.new('RGB',(1420,760),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((35,95,745,694),16,fill=C['panel'],outline=C['line'],width=3)
    d.rounded_rectangle((765,95,1385,694),16,fill=C['panel'],outline=C['line'],width=3)
    center(d,'SANGMATH • THỐNG KÊ 09 • TRUNG VỊ GHÉP NHÓM',710,27,32,'white',1350,True)
    center(d,f'CHƯƠNG {ch+1:02d} / 08',1070,130,24,'cyan',510,True)
    section=CHAPTERS[ch]
    for j,line in enumerate(textwrap.wrap(section,32)):
        center(d,line,1070,202+j*38,25,'white',520,True)
    facts=[
        ['Trung vị dữ liệu gốc: 7','Lớp [6;8) chứa mốc giữa'],
        ['6 → 24 → 38 → 40','n/2 = 20'],
        ['Cận trái L = 6','Trước: 6, trong lớp: 18'],
        ['Đi 14/18 của lớp rộng 2',f'M_e ≈ {MAIN.value:.2f}'],
        ['Mức tích lũy = 20','Đọc hoành độ ≈ 7,56'],
        ['Bảng A ≈ 7,56',f'Bảng B ≈ {ALTERNATIVE.value:.2f}'],
        ['Nếu tích lũy = n/2','Trung vị nằm tại ranh giới'],
        ['N = 20, lớp [4;6)',f'M_e ≈ {EXERCISE.value:.2f}'],
    ]
    for i,t in enumerate(facts[ch]):
        center(d,t,1070,425+i*46,24,'gold' if i==0 else 'green',550,i==0)
    if ch in (0,2,3,5,7):
        freq=[[6,18,14,2],[6,18,14,2],[6,18,14,2],[6,8,18,8],[5,7,6,2]][(0,2,3,5,7).index(ch)]
        bars(d,freq,'TẦN SỐ THEO LỚP',median={0:1,2:1,3:1,5:2,7:1}[ch])
    elif ch in (1,6):
        bars(d,[6,24,38,40] if ch==1 else [4,10,17,20],
             'TẦN SỐ TÍCH LŨY',median=1)
    else:
        center(d,'ĐƯỜNG TẦN SỐ TÍCH LŨY',391,238,23,'cyan',575,True)
        pts=[(95,567),(241,520),(389,385),(537,270),(685,246)]
        d.line(pts,fill=C['cyan'],width=5,joint='curve')
        for p in pts:d.ellipse((p[0]-7,p[1]-7,p[0]+7,p[1]+7),fill=C['gold'])
        y=425;d.line((95,y,460,y),fill=C['green'],width=3)
        d.line((460,y,460,567),fill=C['gold'],width=3)
        center(d,'MỨC 20',185,395,20,'green')
    d.text((51,722),'STORYBOARD THIẾT KẾ – KHÔNG PHẢI KHUNG HÌNH MANIM ĐÃ RENDER',font=FONT(15),fill=C['muted'])
    im.save(OUT/f'STAT09_chapter_{ch+1:02d}.png')

for k in range(8):draw_chapter(k)
coll=Image.new('RGB',(1428,1742),C['bg'])
for i in range(8):
    small=Image.open(OUT/f'STAT09_chapter_{i+1:02d}.png').resize((690,369),Image.Resampling.LANCZOS)
    coll.paste(small,(18+(i%2)*708,40+(i//2)*423))
coll.save(OUT/'STAT09_storyboard_8_chapters.png')

narr=['# THONG-KE-09 – TRUNG VỊ CỦA MẪU SỐ LIỆU GHÉP NHÓM','',
      'Kịch bản thuyết minh tiếng Việt khớp từng nhịp Manim. Dữ liệu giả lập 40 điểm.',
      'Thời lượng nền 992 giây (16:32), không tính phần TTS nếu cần thêm thời gian.','']
board=['# STORYBOARD STAT09','',
       '8 chương / 32 nhịp. Bố cục 16:9: hình/bảng bên trái, lập luận bên phải.',
       'Các phương án nội suy được ghi là xấp xỉ. Không đưa đáp số trước lời giải.','']
for j,chapter in enumerate(CHAPTERS,1):
    narr.extend([f'## Chương {j:02d}: {chapter}',''])
    board.extend([f'## Chương {j:02d}: {chapter}',''])
    for b in BEATS[(j-1)*4:j*4]:
        narr.extend([f'### Nhịp {b.step} – {b.title}',b.voice,''])
        board.extend([f'### Nhịp {b.step} – {b.title}',
                      f'- Luận điểm: {b.thesis}',
                      '- Hình bên trái thay đổi theo trạng thái; nhịp 3–4 xuất công thức Typst.',
                      f'- Thời lượng nền: {b.duration:.0f} giây.',''])
(ROOT/'LOI_GIANG_STAT09.md').write_text('\n'.join(narr)+'\n',encoding='utf-8')
(ROOT/'STORYBOARD_STAT09.md').write_text('\n'.join(board)+'\n',encoding='utf-8')
print('STAT09_STORYBOARD_OK',len(BEATS),'beats','8 images','word_count',sum(len(b.voice.split()) for b in BEATS))
