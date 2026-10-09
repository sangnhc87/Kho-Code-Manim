"""An explanatory sketch, NOT an actual Manim video frame."""
from pathlib import Path
import sys
import subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat01.lesson import SCORES,FREQUENCY,RELATIVE,CHAPTERS

OUT=ROOT/'preview'
OUT.mkdir(exist_ok=True)
BG='#091421'; PANEL='#10273A'; EDGE='#355268'; WHITE='#EEF7FF'; MUTED='#A9C4D5'
CYAN='#48C6E9'; GOLD='#F3C76A'; GREEN='#5ED7A7'; CORAL='#FA827F'
COLORS={4:'#FA827F',5:'#F6A874',6:'#FFD185',7:'#48C6E9',8:'#5ED7A7',9:'#88A2FF',10:'#B7A0FF'}
font_path=subprocess.check_output(['fc-match','-f','%{file}','Noto Sans'],text=True).strip()

def font(sz):return ImageFont.truetype(font_path,sz)
def txt(draw,xy,text,size=19,color=WHITE):draw.text(xy,text,font=font(size),fill=color)
def rect(draw,xy,color=PANEL,outline=None,r=10,width=1):draw.rounded_rectangle(xy,radius=r,fill=color,outline=outline or EDGE,width=width)

def draw_frame(chapter):
    W,H=960,540
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    txt(d,(27,14),f'SANGMATH / THỐNG KÊ 01 / CHƯƠNG {chapter:02d}',19,WHITE)
    d.line((25,53,935,53),fill=EDGE,width=2)
    rect(d,(22,70,514,485));rect(d,(528,70,937,485))
    title=CHAPTERS[chapter-1]
    txt(d,(43,83),title,17,CYAN)
    if chapter in (1,2):
        scores=SCORES if chapter==1 else sorted(SCORES)
        for i,x in enumerate(scores):
            cx=53+(i%8)*56;cy=147+(i//8)*58
            active=x==7 if chapter==2 else False
            rect(d,(cx,cy,cx+45,cy+42),COLORS[x] if active else '#1B3E51',r=7)
            txt(d,(cx+13,cy+6),str(x),22,BG if active else WHITE)
    elif chapter in (3,):
        for i,(s,n) in enumerate(FREQUENCY.items()):
            y=137+i*42
            rect(d,(68,y,470,y+36),'#16374D' if i%2==0 else PANEL,r=4)
            for x,val in [(85,s),(248,n),(372,sum(FREQUENCY[v] for v in FREQUENCY if v<=s))]:
                txt(d,(x,y+5),str(val),17,COLORS[s] if x==85 else WHITE)
    elif chapter in (4,6):
        for i,(s,n) in enumerate(FREQUENCY.items()):
            x=77+i*58;h=n*24
            d.rectangle((x,427-h,x+35,427),fill=COLORS[s])
            txt(d,(x+9,431),str(s),16)
            txt(d,(x+11,400-h),str(n),15,GOLD)
        d.line((58,428,484,428),fill=MUTED,width=2)
    elif chapter==5:
        cursor=67
        for s,n in FREQUENCY.items():
            width=round(408*n/40)
            d.rectangle((cursor,211,cursor+width,268),fill=COLORS[s])
            cursor+=width
        for i,(s,n) in enumerate(FREQUENCY.items()):
            col=i%4;row=i//4
            x=80+col*110;y=322+row*47
            txt(d,(x,y),f'{s}: {round(100*n/40)}%',15,COLORS[s])
    elif chapter==7:
        for j,(base,text) in enumerate(((0,'TRỤC TỪ 0'),(7,'TRỤC TỪ 7'))):
            cx=159+j*235
            txt(d,(cx-60,136),text,16,GREEN if j==0 else CORAL)
            for dx,v in ((-30,8),(30,10)):
                h=(v-base)*(22 if j==0 else 67)
                d.rectangle((cx+dx,403-h,cx+dx+29,403),fill=CYAN if v==8 else GOLD)
            d.line((cx-65,404,cx+93,404),fill=MUTED,width=2)
    else:
        for i,(q,answer) in enumerate((('ĐÚNG ĐIỂM 9','6 em'),('ĐIỂM 7','25%'),('ĐIỂM ≥ 8','40%'),('QUY TRÌNH','4 bước'))):
            y=154+i*68
            rect(d,(69,y,462,y+53),'#16374D',r=7)
            txt(d,(86,y+13),q,16,WHITE)
            txt(d,(356,y+13),answer,17,GREEN)
    txt(d,(547,123),'CÂU HỎI CỦA CHƯƠNG',18,CYAN)
    questions=[
        'Dữ liệu cho biết điều gì?',
        'Sắp xếp có làm mất giá trị?',
        'Số lần xuất hiện là bao nhiêu?',
        'Biểu đồ giúp ta nhìn thấy gì?',
        'Mỗi nhóm chiếm bao nhiêu %?',
        'Từ 8 trở lên có bao nhiêu em?',
        'Thu thập và vẽ sai ảnh hưởng gì?',
        'Em có tự đọc được số liệu?'
    ]
    import textwrap
    for row,line in enumerate(textwrap.wrap(questions[chapter-1],width=29)):
        txt(d,(547,168+31*row),line,26,GOLD)
    d.line((548,274,911,274),fill=EDGE,width=2)
    metrics=[('40 quan sát','7 giá trị'),('4 → 10','40 thẻ nguyên vẹn'),
             ('Tổng tần số','40'),('Đỉnh tại điểm 7','10 em'),
             ('Điểm 7','25%'),('Đạt ≥ 8','16 / 40 = 40%'),
             ('Đơn vị dữ liệu','Mẫu & tổng thể'),('Hiểu trước khi tính','Không phán đoán quá mức')]
    a,b=metrics[chapter-1]
    txt(d,(552,302),a,20,MUTED);txt(d,(552,359),b,24,GREEN)
    txt(d,(36,506),'BẢN PHÁC THẢO — KHÔNG PHẢI ẢNH RENDER TỪ MANIM',14,MUTED)
    im.save(OUT/f'STAT01_chapter_{chapter:02d}.png')
    return im

def main():
    pics=[draw_frame(i) for i in range(1,9)]
    thumb_w,thumb_h=720,405
    collage=Image.new('RGB',(2*thumb_w+60,4*thumb_h+110),BG)
    d=ImageDraw.Draw(collage)
    txt(d,(38,18),'STAT01 · STORYBOARD TÁM CHƯƠNG',29,WHITE)
    for i,img in enumerate(pics):
        x=20+(i%2)*(thumb_w+20)
        y=68+(i//2)*(thumb_h+10)
        collage.paste(img.resize((thumb_w,thumb_h)),(x,y))
    out=OUT/'STAT01_storyboard_8_chapters.png'
    collage.save(out)
    print('Storyboard:',out, 'pixels:',collage.size)
if __name__=='__main__':main()
