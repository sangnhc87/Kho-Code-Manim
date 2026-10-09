"""Generate accessible narration, detailed storyboard and chapter concept previews.
The preview PNGs are static pedagogical sketches, NOT real Manim frames.
"""
from __future__ import annotations
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat02.lesson import (BEATS,CHAPTERS,FREQUENCY,PERCENT,PIE_ANGLES,
    GROUP_COUNT,GROUP_EDGES,TIME_CLASSES,TIME_DENSITY,MONTHS,MONTHLY_MEAN,N)
from PIL import Image, ImageDraw, ImageFont
from math import sin,cos,pi

BG='#091421';PANEL='#10273A';ALT='#173650';LINE='#36556B'
CYAN='#52C8EE';GOLD='#FFD476';GREEN='#62D8AF';WHITE='#EEF7FF';MUTED='#ACC5D9'
COLORS={4:'#F78786',5:'#FFA973',6:'#F6CB77',7:'#5AC7ED',
        8:'#58D6A3',9:'#909EFE',10:'#C09EFF'}
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
if not Path(BOLD).is_file():BOLD=FONT

def f(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)
def draw_center(d,xy,s,font,fill):
    bbox=d.textbbox((0,0),s,font=font)
    d.text((xy[0]-(bbox[2]-bbox[0])/2,xy[1]-(bbox[3]-bbox[1])/2),s,font=font,fill=fill)

def rounded(d,box,fill=ALT,outline=LINE,width=2,radius=15):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def dot_chart(d,step):
    xbase=95;ybase=554
    for idx,(score,count) in enumerate(FREQUENCY.items()):
        x=xbase+idx*71
        draw_center(d,(x,587),str(score),f(24,True),WHITE)
        for j in range(count):d.ellipse((x-8,ybase-24*j-8,x+8,ybase-24*j+8),fill=COLORS[score])

def bar_chart(d):
    bottom=565
    d.line((72,bottom,586,bottom),fill=WHITE,width=3)
    d.line((72,235,72,bottom),fill=WHITE,width=3)
    for j,(k,v) in enumerate(FREQUENCY.items()):
        x=104+j*72;h=v*29
        rounded(d,(x-22,bottom-h,x+22,bottom),fill=COLORS[k],outline=BG,width=1,radius=5)
        draw_center(d,(x,bottom-h-25),str(v),f(22,True),GOLD if k==7 else WHITE)
        draw_center(d,(x,bottom+27),str(k),f(23,True),WHITE)

def pie_chart(d):
    s=0.;box=(116,256,465,605)
    for k,count in FREQUENCY.items():
        angle=count/N*360
        d.pieslice(box,start=270+s,end=270+s+angle,fill=COLORS[k],outline=BG,width=3)
        s+=angle
    for i,(k,percent) in enumerate(PERCENT.items()):
        y=260+i*49
        d.rectangle((485,y,506,y+21),fill=COLORS[k])
        d.text((522,y-5),f'{k}: {percent:.0f}%',font=f(19),fill=WHITE)

def percent_chart(d):
    for i,(name,value) in enumerate((('LỚP A',40),('LỚP B',50))):
        y=305+i*125
        d.text((105,y-50),name,font=f(25,True),fill=CYAN)
        rounded(d,(105,y,566,y+54),fill=ALT,outline=LINE,width=1,radius=6)
        d.rounded_rectangle((105,y,105+461*value/100,y+54),fill=GREEN,radius=5)
        d.text((118,y+9),f'{value}%',font=f(22,True),fill=BG)
        d.text((473,y+9),f'{100-value}%',font=f(22),fill=WHITE)

def histogram_chart(d):
    base=570;start=100;w=112
    d.line((start,base,590,base),fill=WHITE,width=2)
    for i,(count,a,b) in enumerate(zip(GROUP_COUNT,GROUP_EDGES,GROUP_EDGES[1:])):
        h=count*14.6;x=start+i*w
        d.rectangle((x,base-h,x+w,base),fill=[CYAN,GREEN,'#B5A0FF',GOLD][i],outline=BG,width=2)
        draw_center(d,(x+w/2,base-h-22),str(count),f(21,True),WHITE)
        draw_center(d,(x+w/2,base+26),f'{a}–{b}',f(21),WHITE)

def line_chart(d):
    left=95;bottom=561;pts=[]
    d.line((left,bottom,586,bottom),fill=WHITE,width=2)
    d.line((left,235,left,bottom),fill=WHITE,width=2)
    for i,y in enumerate(MONTHLY_MEAN):
        x=left+44+i*82; yy=530-(y-5.5)*108
        pts.append((x,yy))
        draw_center(d,(x,585),MONTHS[i],f(21),WHITE)
    d.line(pts,fill=CYAN,width=5)
    for i,(x,y) in enumerate(pts):
        d.ellipse((x-9,y-9,x+9,y+9),fill=GOLD)
        draw_center(d,(x,y-26),str(MONTHLY_MEAN[i]),f(19),WHITE)

def mistakes_chart(d):
    for i,(label,base) in enumerate((('TRỤC 0',0),('TRỤC 7',7))):
        ox=185+262*i;bot=550
        draw_center(d,(ox,277),label,f(24,True),GREEN if i==0 else GOLD)
        d.line((ox-95,bot,ox+95,bot),fill=WHITE,width=2)
        for j,(v,col) in enumerate(((8,CYAN),(10,GOLD))):
            h=232*(v-base)/(10-base)
            x=ox-44+j*88
            d.rectangle((x-25,bot-h,x+25,bot),fill=col)
            draw_center(d,(x,bot-h-20),str(v),f(20,True),WHITE)

def quiz_chart(d):
    rows=[('SO SÁNH MỨC ĐIỂM','CỘT'),('CƠ CẤU PHẦN TRĂM','TRÒN / THANH 100%'),
          ('SỐ LIỆU GHÉP KHOẢNG','HISTOGRAM'),('SỰ THAY ĐỔI QUA THÁNG','ĐƯỜNG')]
    for i,(a,b) in enumerate(rows):
        y=262+i*89
        rounded(d,(96,y,578,y+70),fill=ALT,outline=LINE,radius=12)
        d.text((118,y+11),a,font=f(18),fill=WHITE)
        d.text((118,y+36),b,font=f(19,True),fill=GOLD)

DRAW=[dot_chart,bar_chart,pie_chart,percent_chart,histogram_chart,line_chart,mistakes_chart,quiz_chart]

def make_preview(chapter):
    im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
    d.text((58,46),f'SANGMATH  •  THỐNG KÊ 02  •  CHƯƠNG {chapter:02d}/08',
           font=f(30,True),fill=WHITE)
    d.line((55,112,1225,112),fill=LINE,width=3)
    rounded(d,(50,150,624,641),fill=PANEL,outline=LINE,radius=18)
    rounded(d,(649,150,1230,641),fill=PANEL,outline=LINE,radius=18)
    d.text((75,170),'MÔ HÌNH DỮ LIỆU',font=f(23,True),fill=CYAN)
    if chapter==1:dot_chart(d,1)
    else:DRAW[chapter-1](d) # charts from chapter2 onwards
    beat=BEATS[(chapter-1)*4]
    d.text((677,183),f'CHƯƠNG {chapter:02d} – NHỊP 1/4',font=f(21),fill=CYAN)
    from textwrap import wrap
    y=242
    for t in wrap(beat.title,29):
        d.text((679,y),t,font=f(31,True),fill=WHITE);y+=46
    d.line((675,366,1200,366),fill=LINE,width=2)
    for t in wrap(beat.thesis,33):
        d.text((679,y+70),t,font=f(27,True),fill=GOLD);y+=42
    d.text((680,588),'40 điểm giả lập từ STAT01' if chapter<=5 else 'Bộ số liệu ghi rõ nguồn minh họa',
           font=f(17),fill=MUTED)
    d.text((58,666),'BẢN PHÁC THẢO BỐ CỤC – KHÔNG PHẢI KHUNG HÌNH RENDER MANIM',
           font=f(19),fill=MUTED)
    out=ROOT/'preview'/'stat02'/f'STAT02_chapter_{chapter:02d}.png'
    im.save(out)
    return im

def write_docs():
    chapters=['# STORYBOARD STAT02 – CÁC LOẠI BIỂU ĐỒ THỐNG KÊ',
        'Tám chương, 32 nhịp, 736 giây (12 phút 16 giây) trước khi căn theo giọng đọc.',
        'Các ảnh storyboard chỉ phác thảo bố cục, không thay thế QA từ MP4 Manim.','']
    narration=['# LỜI GIẢNG STAT02 – BIỂU ĐỒ THỐNG KÊ',
               'Tất cả dữ liệu đều giả lập; chương 1–5 kế thừa 40 điểm từ STAT01.','']
    for c,name in enumerate(CHAPTERS,1):
        chapters.extend([f'## Chương {c:02d}. {name}',f'Ảnh xem trước: `preview/stat02/STAT02_chapter_{c:02d}.png`',''])
        narration.extend([f'## Chương {c:02d}. {name}',''])
        for b in BEATS[(c-1)*4:c*4]:
            chapters.extend([f'### Nhịp {b.step}: {b.title}',f'- Ý chính: **{b.thesis}**',
                             f'- Thời lượng nền: {b.duration:.0f} giây',
                             f'- Hoạt hình: mô hình của chương {c}, nhấn mạnh đối tượng của nhịp {b.step}.',''])
            narration.extend([f'### Nhịp {b.step}: {b.title}',b.voice,''])
    (ROOT/'STORYBOARD_STAT02.md').write_text('\n'.join(chapters),encoding='utf-8')
    (ROOT/'LOI_GIANG_STAT02.md').write_text('\n'.join(narration),encoding='utf-8')
    ims=[make_preview(c) for c in range(1,9)]
    # 2 columns x 4 rows, previews scaled proportionally.
    thumb_w=900;thumb_h=506;gap=20
    board=Image.new('RGB',(thumb_w*2+gap*3,thumb_h*4+gap*5),BG)
    for i,im in enumerate(ims):
        image=im.resize((thumb_w,thumb_h),Image.Resampling.LANCZOS)
        x=gap+(i%2)*(thumb_w+gap)
        y=gap+(i//2)*(thumb_h+gap)
        board.paste(image,(x,y))
    target=ROOT/'preview'/'stat02'/'STAT02_storyboard_8_chapters.png'
    board.save(target,optimize=True)
    print('Saved',target,'and narration/storyboard MD')

if __name__=='__main__':write_docs()
