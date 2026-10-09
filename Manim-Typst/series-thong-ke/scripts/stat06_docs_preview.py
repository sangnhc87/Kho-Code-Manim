"""Generate original, data-faithful storyboard images (not Manim render)."""
from __future__ import annotations
import math,sys,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat06.lesson import CHAPTERS,BEATS,FREQ,BASE,A,B,SA,SB,OUTLIER,SEX,EX,EX2
OUT=ROOT/'preview'/'stat06';OUT.mkdir(parents=True,exist_ok=True)
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for p in ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf','/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'):
    if Path(p).exists():
        if 'Bold' in p:bold=p
        else:regular=p
F=lambda size,b=False:ImageFont.truetype(bold if b else regular,size)
C={'bg':'#0A1522','panel':'#10293B','edge':'#355A71','white':'#EDF6FF',
   'cyan':'#56CBE9','gold':'#FFD379','coral':'#FF8E87','green':'#67DDB5',
   'purple':'#B7A9FC','muted':'#ADC6D5'}
DETAILS=[
('Hai mẫu cùng trung bình 7','A: phương sai 2','B: phương sai 18'),
('Bình phương độ lệch','Tổng bình phương = 10','Chia n = 5, phương sai 2'),
('40 điểm của cùng một lớp giả lập','Tổng điểm = 284','Phương sai 2,29, độ lệch chuẩn ≈1,513'),
('Tần số và trọng số','Tổng tần số 40; tổng bình phương 2108','S² = 2108/40 − 7,1² = 2,29'),
('Co giãn quanh trung bình','Mẫu A: s ≈1,414','Mẫu B: s ≈4,243'),
('Biến đổi tuyến tính','Cộng hằng số: s² không đổi','Nhân 2: s² nhân 4'),
('Ngoại lệ và độ nhạy','Đổi một quan sát 10 thành 30','s²: 2,29 → 14,94'),
('Bài tự kiểm tra','Dãy 2,4,6,8,10 có s² = 8','Thay 10 bằng 20: s² = 40'),
]

def addtext(draw,xy,text,sz,col,bold=False):
    draw.text(xy,text,font=F(sz,bold),fill=col)

def axis(d,vmin,vmax,y=490,ticks=()):
    x0,x1=96,605
    X=lambda v:int(x0+(v-vmin)*(x1-x0)/(vmax-vmin))
    d.line((x0,y,x1,y),width=3,fill=C['muted'])
    for t in ticks:
        x=X(t);d.line((x,y-8,x,y+8),width=2,fill=C['muted'])
        addtext(d,(x-11,y+17),str(t),16,C['muted'])
    return X

def scatter(d,vals,X,y,color):
    seen={}
    for val in vals:
        count=seen.get(val,0);seen[val]=count+1
        x=X(val);yy=y-count*8
        d.ellipse((x-7,yy-7,x+7,yy+7),fill=color)

def basic(ch):
    im=Image.new('RGB',(1280,720),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((32,135,645,641),radius=18,fill=C['panel'],outline=C['edge'],width=2)
    d.rounded_rectangle((673,135,1248,641),radius=18,fill=C['panel'],outline=C['edge'],width=2)
    addtext(d,(37,35),f'SANGMATH / THỐNG KÊ 06 / CHƯƠNG {ch:02d}',31,C['white'],True)
    d.line((37,109,1244,109),fill=C['edge'],width=2)
    addtext(d,(59,173),DETAILS[ch-1][0].upper(),20,C['cyan'],True)
    addtext(d,(699,181),f'CHƯƠNG {ch:02d}/08   •   NHỊP 3/4',21,C['cyan'],True)
    for j,line in enumerate(textwrap.wrap(CHAPTERS[ch-1],width=30,break_long_words=False)):
        addtext(d,(699,240+33*j),line,19,C['white'],True)
    d.line((700,346,1216,346),fill=C['edge'],width=2)
    addtext(d,(703,393),DETAILS[ch-1][1],21,C['gold'],True)
    addtext(d,(703,449),DETAILS[ch-1][2],18,C['green'])
    addtext(d,(703,572),'Quan sát → dự đoán → chứng minh',17,C['muted'])
    addtext(d,(37,672),'STORYBOARD MINH HỌA • CHƯA PHẢI HÌNH RENDER MANIM',17,C['muted'])
    return im,d

for ch in range(1,9):
    im,d=basic(ch)
    if ch in (1,5):
        X=axis(d,0,14,532,(0,1,4,5,7,9,10,13,14))
        scatter(d,A,X,327,C['cyan']);scatter(d,B,X,433,C['coral'])
        x=X(7);d.line((x,287,x,487),fill=C['gold'],width=3)
        addtext(d,(90,311),'A',22,C['cyan'],True);addtext(d,(90,414),'B',22,C['coral'],True)
    elif ch==2:
        X=axis(d,3,11,527,(4,5,6,7,8,9,10))
        for v in A:
            h=abs(v-7)*37+8
            x=X(v)
            d.rectangle((x-16,424-h,x+16,424),fill=C['purple'])
        addtext(d,(128,571),'4 + 1 + 0 + 1 + 4 = 10',22,C['gold'],True)
    elif ch==3:
        X=axis(d,3,11,527,(4,5,6,7,8,9,10))
        for val,n in FREQ.items():
            x=X(val);h=n*16;d.rectangle((x-20,485-h,x+20,485),fill=C['cyan'])
        d.line((X(7.1),276,X(7.1),505),fill=C['gold'],width=3)
    elif ch==4:
        X=axis(d,3,11,527,(4,5,6,7,8,9,10))
        for v,n in FREQ.items():
            x=X(v);h=n*19
            d.rectangle((x-19,477-h,x+19,477),fill=C['green'] if v==7 else C['cyan'])
            addtext(d,(x-9,480-h-28),str(n),18,C['white'])
    elif ch==6:
        X=axis(d,0,21,527,(0,3,5,7,9,10,12,14,18,21))
        scatter(d,A,X,335,C['cyan']);scatter(d,[2*v for v in A],X,438,C['coral'])
        addtext(d,(80,306),'gốc',20,C['cyan']);addtext(d,(80,412),'x2',20,C['coral'])
    elif ch==7:
        X=axis(d,0,32,527,(0,4,8,10,16,24,30,32))
        for val,n in FREQ.items():
            x=X(val);h=n*15;d.rectangle((x-13,495-h,x+13,495),fill=C['cyan'])
        x=X(30);d.ellipse((x-10,317,x+10,337),fill=C['coral'])
        d.line((X(7.1),310,X(7.1),498),fill=C['gold'],width=2)
    else:
        X=axis(d,0,22,532,(0,2,4,6,8,10,14,20,22))
        scatter(d,EX,X,352,C['cyan']);scatter(d,EX2,X,439,C['coral'])
        addtext(d,(83,318),'A',20,C['cyan']);addtext(d,(83,405),'B',20,C['coral'])
    im.save(OUT/f'STAT06_chapter_{ch:02d}.png')

sheet=Image.new('RGB',(1660,1905),C['bg'])
for ch in range(1,9):
    im=Image.open(OUT/f'STAT06_chapter_{ch:02d}.png')
    im.thumbnail((800,450))
    col=(ch-1)%2;row=(ch-1)//2
    sheet.paste(im,(20+col*820,15+row*472))
sheet.save(OUT/'STAT06_storyboard_8_chapters.png')

lines=['# STAT06 – Storyboard 8 chương, 32 nhịp','',
       '**Chủ đề:** Phương sai, độ lệch chuẩn của mẫu số liệu không ghép nhóm.',
       '**Quy ước:** dùng mẫu số n cho thống kê mô tả SGK; phân biệt ước lượng n−1.',
       '**Dữ liệu:** bộ 40 điểm giả lập từ STAT01–05; các bộ so sánh khác được ghi riêng.',
       '**Bố cục:** hình động phía trái, kết luận từng bước và SVG Typst phía phải.',
       '**Thời lượng:** 32 × 28,5 giây = 912 giây (15 phút 12 giây) chưa căn TTS.','']
for ch in range(1,9):
    lines.extend([f'## Chương {ch:02d}: {CHAPTERS[ch-1]}',''])
    for b in BEATS[(ch-1)*4:ch*4]:
        lines.extend([f'### Nhịp {b.step}: {b.title}',
                      f'- Kết luận: {b.thesis}',
                      f'- Minh họa: mô hình và chuyển động trạng thái {b.chapter}.{b.step}.',
                      f'- Lời giảng: {b.voice}',''])
(ROOT/'STORYBOARD_STAT06.md').write_text('\n'.join(lines),encoding='utf-8')
(ROOT/'LOI_GIANG_STAT06.md').write_text('# Lời giảng STAT06 – Phương sai và độ lệch chuẩn\n\n'+
   '\n\n'.join(f'## Chương {b.chapter}, nhịp {b.step}: {b.title}\n\n{b.voice}' for b in BEATS)+'\n',encoding='utf-8')
print('STAT06_DOCS_AND_STORYBOARD_OK',len(BEATS),'beats',8,'chapters')
