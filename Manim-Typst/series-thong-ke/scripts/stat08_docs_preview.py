"""Generate STAT08 Vietnamese narration, 32-step storyboard and 8-chapter visual contact sheet."""
from __future__ import annotations
import textwrap,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
from stat08.lesson import BEATS,CHAPTERS,FREQ,ASYM_FREQ,PFREQ,EXACT_MEAN,GROUPED_MEAN,GROUPED_MODE,ASYM_MODE,PRACTICE_MEAN,PRACTICE_MODE
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview/stat08';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
C=dict(bg='#07121e',panel='#102b3e',cyan='#55cbe7',gold='#ffd57a',green='#66ddb3',white='#eff7ff',muted='#9bbaca',orange='#ff938b',violet='#aea9f2',stroke='#32546a')
COLOR=[C['cyan'],C['green'],C['violet'],C['orange']]

def centered(d,x,y,t,size=22,bold=False,color='white',maxwidth=550):
    t=str(t);f=font(size,bold)
    while size>12 and d.textbbox((0,0),t,font=f)[2]>maxwidth:
        size-=1;f=font(size,bold)
    bbox=d.textbbox((0,0),t,font=f)
    d.text((x-(bbox[2]-bbox[0])/2,y),t,font=f,fill=C.get(color,color))

def chart(d,vals,title,mode='bars',highlight=None):
    centered(d,382,230,title,23,True,'cyan',570)
    x0=105;y0=505;w=555;h=225
    d.line((x0,y0,x0+w,y0),fill=C['muted'],width=3)
    mx=max(vals)*1.18
    for i,v in enumerate(vals):
        bw=w/len(vals)*.65;cx=x0+(i+.5)*w/len(vals)
        barh=(v/mx)*h
        color=C['gold'] if i==highlight else COLOR[i%len(COLOR)]
        d.rectangle((cx-bw/2,y0-barh,cx+bw/2,y0),fill=color)
        centered(d,cx,y0-barh-28,f'{v:g}',21,True,color,130)
        centered(d,cx,y0+14,['I','II','III','IV'][i],18,False,'muted',110)

def special(d,index):
    if index==0:
        chart(d,FREQ,'TRUNG ĐIỂM:  5  •  7  •  9  •  11',highlight=1)
    elif index==1:
        chart(d,(30,126,126,22),'TRỌNG SỐ: 30 + 126 + 126 + 22')
    elif index==2:
        chart(d,(7.1,7.6,7.65),'TRUNG BÌNH GỐC VÀ ƯỚC LƯỢNG')
    elif index==3:
        chart(d,ASYM_FREQ,'ĐỔI CHIA LỚP: 6 – 8 – 18 – 8',highlight=2)
    elif index==4:
        chart(d,FREQ,'LỚP MỐT: [6;8),  f = 18',highlight=1)
    elif index==5:
        chart(d,(3,8,9,4),'MẬT ĐỘ, KHÔNG CHỈ TẦN SỐ',highlight=2)
    elif index==6:
        chart(d,(6,18,14,2),'TÌM TẦN SỐ ẨN x = 18',highlight=1)
    else:chart(d,PFREQ,'20 THỜI LƯỢNG LUYỆN TẬP',highlight=1)

OUTCOMES=[
 'TRUNG ĐIỂM 5, 7, 9, 11',
 '304 ÷ 40 = 7,6',
 'GỐC 7,1  ≠  GHÉP 7,6',
 'A = 7,60   •   B = 7,65',
 'MỐT NỘI SUY ≈ 7,5',
 'MẬT ĐỘ: 3 – 8 – 9 – 4',
 'x = 18   •   MỐT ≈ 7,5',
 'TRUNG BÌNH ≈ 5,5; MỐT ≈ 5,33',
]
for ch in range(8):
    im=Image.new('RGB',(1280,720),C['bg']);d=ImageDraw.Draw(im)
    d.rounded_rectangle((26,27,1253,688),radius=22,fill=C['panel'],outline=C['stroke'],width=3)
    d.text((61,62),f'SANGMATH  /  THỐNG KÊ 08  /  CHƯƠNG {ch+1:02d}',font=font(23,True),fill=C['cyan'])
    d.text((60,107),CHAPTERS[ch],font=font(26,True),fill=C['white'])
    d.line((60,166,1222,166),fill=C['stroke'],width=2)
    d.rounded_rectangle((54,195,693,606),radius=18,outline=C['stroke'],width=3)
    special(d,ch)
    d.rounded_rectangle((717,195,1228,606),radius=18,outline=C['stroke'],width=3)
    centered(d,974,243,'KẾT LUẬN / PHƯƠNG PHÁP',23,True,'cyan',455)
    centered(d,972,334,OUTCOMES[ch],28,True,'gold',461)
    notes={0:'Thay bằng trung điểm để ước lượng.',1:'Mẫu số = 40, không phải 4.',
           2:'Ghép nhóm có thể làm mất thông tin.',3:'Giữ dữ liệu gốc; đổi ranh giới.',
           4:'Công thức nội suy cho giá trị gần đúng.',5:'Chọn cột có mật độ cao nhất.',
           6:'Kiểm tần số nguyên không âm.',7:'Tự giải rồi mới đối chiếu.'}[ch]
    for k,line in enumerate(textwrap.wrap(notes,32)):
        centered(d,972,460+k*38,line,20,False,'muted',466)
    d.text((58,638),'STORYBOARD THIẾT KẾ — KHÔNG PHẢI KHUNG HÌNH MANIM ĐÃ RENDER',font=font(16),fill=C['muted'])
    im.save(OUT/f'STAT08_chapter_{ch+1:02d}.png')
coll=Image.new('RGB',(1435,1740),C['bg'])
for ch in range(8):
    img=Image.open(OUT/f'STAT08_chapter_{ch+1:02d}.png')
    coll.paste(img.resize((690,388),Image.Resampling.LANCZOS),(23+(ch%2)*712,40+(ch//2)*425))
coll.save(OUT/'STAT08_storyboard_8_chapters.png')

narr=['# THONG-KE-08 – Số trung bình và mốt của mẫu số liệu ghép nhóm',
      '', 'Dữ liệu: 40 điểm giả lập từ STAT01–07. Các giá trị ước lượng được đánh dấu rõ.',
      '', 'Thời lượng hình nền: 32 × 30 = 960 giây (16:00).', '']
board=['# STORYBOARD STAT08 – Manim + Typst','', 'Bố cục 16:9, hình bên trái, lập luận bên phải; 32 nhịp / 8 chương.',
       'Giọng đọc liên kết từng nhịp; không lộ kết quả ở đầu nhịp.',
       '', 'Lưu ý: hình trong preview là storyboard, không phải ảnh Manim thật.', '']
for ch,heading in enumerate(CHAPTERS,1):
    narr.extend([f'## Chương {ch:02d}: {heading}',''])
    board.extend([f'## Chương {ch:02d}: {heading}',''])
    for b in BEATS[(ch-1)*4:ch*4]:
        narr.extend([f'### Nhịp {b.step}: {b.title}',b.voice,''])
        board.extend([f'### Nhịp {b.step}: {b.title}',f'- Trọng tâm: {b.thesis}',
            '- Hình bên trái chuyển trạng thái theo bước; Typst xuất hiện từ nhịp 3.',
            f'- Thời gian nền: {b.duration:.0f} giây.',''])
(ROOT/'LOI_GIANG_STAT08.md').write_text('\n'.join(narr),encoding='utf-8')
(ROOT/'STORYBOARD_STAT08.md').write_text('\n'.join(board),encoding='utf-8')
print('STAT08_STORYBOARD_OK',len(BEATS),'beats',OUT/'STAT08_storyboard_8_chapters.png')
