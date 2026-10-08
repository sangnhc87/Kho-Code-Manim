"""Storyboard PREVIEW only. Final lesson must be rendered by Manim/Typst."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
from matplotlib import font_manager

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'
OUT.mkdir(exist_ok=True)
for p in ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
    if Path(p).exists():
        font_manager.fontManager.addfont(p)
        FAMILY=font_manager.FontProperties(fname=p).get_name()
        break
plt.rcParams['font.family']=FAMILY
BG='#0B1120'; PANEL='#101F33'; TXT='#ECF4FF'; MUT='#A8B9CC'; CYAN='#22D3EE'; GOLD='#FBBF24'; PURPLE='#A78BFA'; GREEN='#22C55E'; RED='#EF4444'
A=np.array([0,3]); B=np.array([-1,2]); C=np.array([2,1]); LO=13/8; HI=7/4

def make_canvas(title):
    fig=plt.figure(figsize=(16,9),facecolor=BG)
    def box(x,y,w,h,color):
        fig.patches.append(FancyBboxPatch((x,y),w,h,transform=fig.transFigure,
            boxstyle='round,pad=0.006,rounding_size=0.009',fc=color,ec='#2E4862',lw=1.3))
    fig.text(.055,.931,'SANG MATH  /  HÌNH HỌC TỌA ĐỘ',color=CYAN,fontsize=17,weight='bold')
    fig.text(.68,.931,'GEO01  ·  MIỀN TRONG TAM GIÁC',color=MUT,fontsize=13)
    fig.lines.append(matplotlib.lines.Line2D([.048,.952],[.905,.905],transform=fig.transFigure,color='#2E4862',lw=1.5))
    box(.045,.11,.43,.78,PANEL)
    box(.488,.11,.467,.78,PANEL)
    fig.text(.72,.836,title,color=GOLD,fontsize=23,ha='center',weight='bold')
    fig.text(.5,.055,'VỊ TRÍ ĐIỂM  ·  NỬA MẶT PHẲNG  ·  TÍCH CÓ HƯỚNG',color=MUT,fontsize=13,ha='center')
    return fig

def axes_box(fig, xlim=(-1.5,2.6),ylim=(.55,3.55)):
    ax=fig.add_axes([.07,.22,.375,.53],facecolor='none')
    ax.set_xlim(*xlim);ax.set_ylim(*ylim)
    ax.set_zorder(10)
    ax.set_aspect('equal',adjustable='box')
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xticks([]);ax.set_yticks([])
    return ax

def tri_full(ax):
    ax.add_patch(Polygon([A,B,C],closed=True,fc=CYAN,ec=CYAN,alpha=.20,lw=3))
    ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]],c=CYAN,lw=2.8)
    for nm,pt,delta in [('A',A,(-.13,.25)),('B',B,(-.18,.12)),('C',C,(.18,-.12))]:
        ax.scatter(*pt,s=80,c=GOLD,zorder=8)
        ax.text(pt[0]+delta[0],pt[1]+delta[1],nm,color=GOLD,fontsize=19,weight='bold')
    xs=np.array([1.15,2.2])
    ax.plot(xs,xs-.5,c=PURPLE,lw=2.8)
    ax.plot([LO,HI],[LO-.5,HI-.5],c=GREEN,lw=7,solid_capstyle='round',zorder=6)
    ax.scatter([LO,HI],[LO-.5,HI-.5],s=100,c=GOLD,zorder=9)


def lines(fig,items,formula=None,color=GREEN):
    ys=np.linspace(.737,.38,len(items))
    for y,s in zip(ys,items):
        fig.text(.517,y,s,color=TXT,fontsize=17)
    if formula:
        fig.text(.72,.227,formula,color=color,fontsize=22,weight='bold',ha='center')

fig=make_canvas('BÀI TOÁN MỞ ĐẦU');ax=axes_box(fig);tri_full(ax)
lines(fig,['A(0; 3), B(-1; 2), C(2; 1).',
           'M(m; (2m - 1)/2) chuyển động.',
           'Tìm m để M ở trong tam giác ABC.',
           'Nếu a < m < b, tính T = 8a + 4b.'],r'$y = x - \frac{1}{2}$',CYAN)
fig.savefig(OUT/'GEO01_01_de_bai.png',dpi=100,facecolor=BG);plt.close(fig)

fig=make_canvas('PHÓNG ĐẠI ĐOẠN NẰM TRONG');ax=axes_box(fig,(1.36,2.08),(.80,1.72))
xx=np.linspace(1.36,2.08,100)
ax.plot(xx,3-xx,c=CYAN,lw=3,label='AC')
ax.plot(xx,(5-xx)/3,c=CYAN,lw=3,label='BC')
ax.plot(xx,xx-.5,c=PURPLE,lw=3,label='M')
ax.fill([1.36,2,1.36],[1.64,1, (5-1.36)/3],color=CYAN,alpha=.15)
ax.plot([LO,HI],[LO-.5,HI-.5],c=GREEN,lw=8,solid_capstyle='round')
ax.scatter([LO,HI],[LO-.5,HI-.5],c=GOLD,s=120,zorder=9)
ax.annotate('13/8',(LO,LO-.5),xytext=(-36,-35),textcoords='offset points',color=GOLD,fontsize=19,weight='bold')
ax.annotate('7/4',(HI,HI-.5),xytext=(12,25),textcoords='offset points',color=GOLD,fontsize=19,weight='bold')
lines(fig,['Quỹ tích: y = x - 1/2.',
           'BC: x + 3y = 5.',
           'AC: x + y = 3.',
           'Hai điểm biên không thuộc miền trong.'],r'$\frac{13}{8}<m<\frac{7}{4}$')
fig.savefig(OUT/'GEO01_02_phong_dai.png',dpi=100,facecolor=BG);plt.close(fig)

fig=make_canvas('ĐIỀU KIỆN TỔNG QUÁT');ax=axes_box(fig);tri_full(ax)
ax.scatter([1.1, .65,1.],[1.62,2.72,2.],c=[GREEN,RED,GOLD],s=110,zorder=12)
ax.annotate('Trong',(1.1,1.62),xytext=(-70,-15),textcoords='offset points',color=GREEN,fontsize=16)
ax.annotate('Ngoài',(.65,2.72),xytext=(12,5),textcoords='offset points',color=RED,fontsize=16)
lines(fig,['Với tam giác ABC không thẳng hàng:',
           'Chọn dấu s của tích có hướng [AB, AC].',
           'M trong tam giác khi 3 tích có hướng',
           'từ ba cạnh tới M cùng dấu với s.',
           'Điều kiện nghiêm: KHÔNG lấy biên.'],r'$T=8\cdot\frac{13}{8}+4\cdot\frac{7}{4}=20$')
fig.savefig(OUT/'GEO01_03_tong_quat.png',dpi=100,facecolor=BG);plt.close(fig)
print('Created 3 storyboard preview PNGs')
