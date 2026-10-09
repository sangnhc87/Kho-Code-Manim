"""INT01: 8 chapters / 32 teaching segments / high-fidelity 2D graphs.

Build first: python scripts/build_int01_typst.py
Prepare:     python scripts/prepare_int01.py --voice off|on
Preview:     manim -ql -r 854,480 --fps 24 int01/scene.py INT01
FullHD:      manim -qh -r 1920,1080 --fps 30 int01/scene.py INT01
Smoke:       manim -ql -r 426,240 --fps 8 int01/scene.py INT01_SMOKE

The animation uses true (x,y) coordinate transforms via Axes.c2p, and the SVG
mathematics is compiled from Typst. No technical beat/scene labels appear.
"""
from __future__ import annotations
import json,sys,textwrap
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from int01.lesson import SEGMENTS,CHAPTERS,FORMULAS

BG='#0B1221'; PANEL='#101C30'; STROKE='#293A54'; WHITE='#F1F5F9'
SOFT='#A9B8CA'; CYAN='#38CDE6'; GREEN='#40D7A5'; GOLD='#F6C65B'
PURPLE='#B59AFE'; CORAL='#FB877F'
FONT='Noto Sans'
config.background_color=BG
config.frame_width=14.222222
config.frame_height=8.0
L_CX=-3.51
R_CX=3.52


def tx(s,size=22,color=WHITE,max_width=None,bold=False):
    """Measured Manim Pango text: reduce uniformly instead of clipping."""
    result=Text(str(s),font=FONT,font_size=size,color=color,
                weight="BOLD" if bold else "NORMAL")
    if max_width is not None and result.width>max_width:
        result.scale(max_width/result.width)
    return result


def multiline(text,width=43,size=22,color=SOFT,max_width=6.05):
    lines=textwrap.wrap(str(text),width=width,break_long_words=False,break_on_hyphens=False)
    if not lines:lines=['']
    pieces=VGroup(*[tx(line,size,color,max_width) for line in lines])
    pieces.arrange(DOWN,buff=.17,aligned_edge=LEFT)
    return pieces


def frame():
    background=VGroup(
       RoundedRectangle(width=6.65,height=6.18,corner_radius=.17,
                        fill_color=PANEL,fill_opacity=1,stroke_color=STROKE,stroke_width=1.2).move_to((-3.49,-.15,0)),
       RoundedRectangle(width=6.60,height=6.18,corner_radius=.17,
                        fill_color=PANEL,fill_opacity=1,stroke_color=STROKE,stroke_width=1.2).move_to((3.51,-.15,0)),
       Line((-6.78,3.11,0),(6.75,3.11,0),color=STROKE,stroke_width=1.4),
       Line((-6.78,-3.43,0),(6.75,-3.43,0),color=STROKE,stroke_width=1.4))
    head=tx('NGUYÊN HÀM',26,CYAN,bold=True).move_to((-5.29,3.55,0))
    subtitle=tx('TỪ ĐẠO HÀM ĐI NGƯỢC',23,WHITE,max_width=6.0,bold=True).move_to((3.5,3.55,0))
    left_head=tx('QUAN SÁT ĐỒ THỊ',17,SOFT,bold=True).move_to((L_CX,2.63,0))
    footer=tx('Thầy Nguyễn Văn Sang',17,SOFT,bold=True).move_to((0,-3.77,0))
    return VGroup(background,head,subtitle,left_head,footer)


def ax(kind='standard'):
    if kind=='line':
        a=Axes(x_range=[-2.1,2.1,1],y_range=[-5.0,5.0,2],x_length=5.33,y_length=3.85,
               tips=False,axis_config={'stroke_width':1.65,'color':SOFT})
    elif kind=='motion':
        a=Axes(x_range=[0,3.25,1],y_range=[0,15,3],x_length=5.20,y_length=3.85,
               tips=False,axis_config={'stroke_width':1.65,'color':SOFT})
    elif kind=='practice':
        a=Axes(x_range=[-1.55,1.55,1],y_range=[-3,8.5,2],x_length=5.23,y_length=3.85,
               tips=False,axis_config={'stroke_width':1.65,'color':SOFT})
    else:
        a=Axes(x_range=[-2.05,2.05,1],y_range=[-3.1,7.5,2],x_length=5.23,y_length=3.85,
               tips=False,axis_config={'stroke_width':1.65,'color':SOFT})
    a.move_to((L_CX,-.32,0))
    return a


def graph_label(label,color=WHITE):
    return tx(label,19,color,max_width=5.25,bold=True).move_to((L_CX,1.95,0))


def small_xy_labels(a,mode='x'):
    g=VGroup()
    if mode=='t':
        g.add(tx('t',16,SOFT).move_to(a.c2p(3.1,0)+UP*.18),tx('s / v',16,SOFT).next_to(a.y_axis.get_end(),UP,buff=.06))
    else:
        g.add(tx('x',16,SOFT).next_to(a.x_axis.get_end(),RIGHT,buff=.06),
              tx('y',16,SOFT).next_to(a.y_axis.get_end(),UP,buff=.04))
    return g


def curve(a,fun,color,x0=-1.95,x1=1.95):
    return a.plot(fun,x_range=[x0,x1],color=color,stroke_width=4.0)


def mark(a,x,y,color=GOLD,radius=.085):
    return Dot(a.c2p(x,y),radius=radius,color=color)


def tangent(a,x0,c=0,color=GOLD):
    """Correct tangent to y=x²+c at x0, not an independently guessed line."""
    def y_line(v):return x0*x0+c+2*x0*(v-x0)
    return Line(a.c2p(x0-.63,y_line(x0-.63)),a.c2p(x0+.63,y_line(x0+.63)),
                color=color,stroke_width=3.25)


def diagram(kind,step):
    """Return visible VGroup, optional payload for honest mathematical animations."""
    if kind in ('question',):
        a=ax('line');g=VGroup(a,small_xy_labels(a))
        line=curve(a,lambda v:2*v,CYAN,-2.05,2.05)
        g.add(line,graph_label('ĐỒ THỊ CỦA f(x) = 2x',CYAN))
        for v in (-1.3,0,1.3):
            g.add(mark(a,v,2*v,GOLD,.065),
                  DashedLine(a.c2p(v,0),a.c2p(v,2*v),color=SOFT,stroke_width=1.0))
        return g,{'path':line,'kind':'trace'}
    if kind in ('reverse','tangent_move'):
        a=ax();g=VGroup(a,small_xy_labels(a))
        shape=curve(a,lambda v:v*v,CYAN)
        g.add(shape,graph_label('F(x) = x²',CYAN))
        x0=1.0 if kind=='reverse' else (-1.0 if step==3 else 1.0)
        dot=mark(a,x0,x0*x0,GOLD)
        g.add(dot,tangent(a,x0),
              tx('hệ số góc = '+('-2' if x0<0 else '2'),17,GOLD,max_width=4.7).move_to((L_CX,-2.64,0)))
        return g,{'kind':'point','dot':dot,'path':shape}
    if kind in ('family','family_shift'):
        a=ax();g=VGroup(a,small_xy_labels(a),graph_label('CÙNG ĐẠO HÀM 2x',CYAN))
        for c,col in [(-2.,PURPLE),(0.,CYAN),(2.,GREEN)]:
            g.add(curve(a,lambda v,k=c:v*v+k,col))
        for c,col,x0 in [(-2.,PURPLE,-1.25),(0.,CYAN,0),(2.,GREEN,1.1)]:
            g.add(tx(('C = '+str(int(c))),16,col).move_to(a.c2p(x0,x0*x0+c)+UP*.23))
        if kind=='family_shift':
            highlight=curve(a,lambda v:v*v-2,GOLD)
            target=curve(a,lambda v:v*v+2,GOLD)
            g.add(highlight)
            return g,{'kind':'transform','source':highlight,'target':target}
        return g,{'kind':'none'}
    if kind in ('tangent',):
        a=ax();g=VGroup(a,small_xy_labels(a),graph_label('TIẾP TUYẾN SONG SONG',CYAN))
        for c,color in [(-2.,PURPLE),(0.,CYAN),(2.,GREEN)]:
            g.add(curve(a,lambda v,k=c:v*v+k,color))
            g.add(tangent(a,1.0,c,GOLD))
            g.add(mark(a,1.,1.+c,GOLD,.067))
        g.add(tx('Cùng x = 1, độ dốc = 2',17,GOLD).move_to((L_CX,-2.64,0)))
        return g,{'kind':'none'}
    if kind=='difference':
        a=ax();g=VGroup(a,small_xy_labels(a),graph_label('CHÊNH LỆCH LUÔN LÀ 3',CYAN))
        g.add(curve(a,lambda v:v*v-1,PURPLE),curve(a,lambda v:v*v+2,GREEN))
        for xv in (-1.25,-.55,.35,1.15):
            g.add(DashedLine(a.c2p(xv,xv*xv-1),a.c2p(xv,xv*xv+2),
                             color=GOLD,stroke_width=2.1,dash_length=.08))
        g.add(tx('F₂ − F₁ = 3',20,GOLD).move_to((L_CX,-2.65,0)))
        return g,{'kind':'none'}
    if kind in ('condition','condition_shift'):
        a=ax();g=VGroup(a,small_xy_labels(a),graph_label('ĐI QUA ĐIỂM (1; 3)',CYAN))
        base=curve(a,lambda v:v*v,CYAN)
        g.add(base)
        if kind=='condition' and step<4:
            g.add(curve(a,lambda v:v*v-1,PURPLE).set_opacity(.26))
        if kind=='condition' and step==4:
            base.become(curve(a,lambda v:v*v+2,GREEN))
        g.add(mark(a,1,3,GOLD,.09),
              DashedLine(a.c2p(1,0),a.c2p(1,3),color=GOLD,stroke_width=1.35),
              tx('(1; 3)',18,GOLD).move_to(a.c2p(1,3)+RIGHT*.50+UP*.17))
        if kind=='condition_shift':
            return g,{'kind':'transform','source':base,'target':curve(a,lambda v:v*v+2,GREEN)}
        return g,{'kind':'none'}
    if kind in ('motion_v','motion_s'):
        a=ax('motion');g=VGroup(a,small_xy_labels(a,'t'))
        if kind=='motion_v':
            shape=curve(a,lambda v:2*v+1,CYAN,0.,3.)
            g.add(shape,graph_label('v(t) = 2t + 1 (m/s)',CYAN))
            dot=mark(a,1,3,GOLD)
        else:
            shape=curve(a,lambda v:v*v+v+2,GREEN,0.,3.)
            g.add(shape,graph_label('s(t) = t² + t + 2 (m)',GREEN))
            dot=mark(a,0,2,GOLD)
            g.add(tx('s(0) = 2 m',17,GOLD).move_to((L_CX,-2.64,0)))
        g.add(dot)
        return g,{'kind':'motion','dot':dot,'path':shape}
    if kind in ('practice','practice_shift'):
        a=ax('practice');g=VGroup(a,small_xy_labels(a),graph_label('ĐIỂM ĐIỀU KIỆN (1; 5)',CYAN))
        correct=step==4
        shape=curve(a,(lambda v:v**3+4) if correct else (lambda v:v**3),
                    GREEN if correct else CYAN,-1.53,1.53)
        g.add(shape,mark(a,1,5,GOLD,.09),
              tx('(1; 5)',17,GOLD).move_to(a.c2p(1,5)+LEFT*.65+UP*.3))
        if correct:
            g.add(curve(a,lambda v:v**3,CYAN,-1.53,1.53).set_opacity(.23))
        if kind=='practice_shift':
            return g,{'kind':'transform','source':shape,'target':curve(a,lambda v:v**3+4,GREEN,-1.53,1.53)}
        return g,{'kind':'none'}
    raise ValueError('Unknown graph visual: '+kind)


PROMPTS=(
    'Phân biệt đồ thị của hàm và của đạo hàm.',
    'Tìm một nguyên hàm rồi lấy đạo hàm kiểm tra.',
    'Giữ nguyên x, quan sát độ cao thay đổi.',
    'So sánh hệ số góc tại cùng hoành độ.',
    'Xét hiệu hai hàm trên cùng một khoảng.',
    'Dùng điều kiện để xác định hằng số.',
    'Vận tốc chưa cho biết tọa độ ban đầu.',
    'Tự làm trước khi đối chiếu lời giải.',
)

def right_content(item):
    g=VGroup()
    title=multiline(item.title.upper(),width=28,size=27,color=WHITE,max_width=5.9)
    if title.height>1.:title.scale_to_fit_height(.95)
    title.move_to((R_CX,2.22,0))
    subtitle=multiline(item.takeaway,width=38,size=22,color=SOFT,max_width=5.95)
    if subtitle.height>1.27:subtitle.scale_to_fit_height(1.27)
    subtitle.move_to((R_CX,1.24,0))
    formula=ROOT/'assets/int01_formulas'/f'{item.formula}.svg'
    if not formula.exists():
        raise FileNotFoundError(f'Typst asset not compiled: {formula} (run build_int01_typst.py)')
    math=SVGMobject(str(formula))
    if math.width>5.75:math.scale_to_fit_width(5.75)
    if math.height>.92:math.scale_to_fit_height(.92)
    math.move_to((R_CX,-.16,0))
    accent=Line((.75,-1.12,0),(6.32,-1.12,0),color=STROKE,stroke_width=1.4)
    chap=multiline(CHAPTERS[item.chapter-1],width=36,size=17,color=CYAN,max_width=5.8)
    chap.move_to((R_CX,-1.69,0))
    hint=multiline(PROMPTS[item.chapter-1],width=39,size=17,color=SOFT,max_width=5.72)
    hint.move_to((R_CX,-2.65,0))
    g.add(title,subtitle,math,accent,chap,hint)
    return g


class BaseLesson(Scene):
    smoke=False
    def construct(self):
        plan_path=ROOT/'int01/runtime_plan.json'
        if not plan_path.exists():raise FileNotFoundError('Prepare runtime plan first')
        data=json.loads(plan_path.read_text(encoding='utf8'))
        beats=data['segments']
        if len(beats)!=len(SEGMENTS):raise RuntimeError('Invalid plan: expected 32 segments')
        if data['voice']=='on' and not self.smoke and any(not s.get('voice_path') for s in beats):
            raise RuntimeError('voice=on selected but narration missing')
        self.add(frame())
        current_graph=None;current_info=None
        for index,(item,entry) in enumerate(zip(SEGMENTS,beats)):
            if item.chapter!=entry['chapter'] or item.step!=entry['step']:
                raise RuntimeError('Runtime storyboard mismatch')
            if self.smoke:
                span=.24;transition=.06;effect=.04
            else:
                span=float(entry['duration']);transition=.75;effect=2.5
            if entry['voice_path'] and not self.smoke:
                wav=ROOT/entry['voice_path']
                if not wav.is_file() or wav.stat().st_size<1000:raise RuntimeError('Missing narration: '+str(wav))
                self.add_sound(str(wav))
            nxt_graph,payload=diagram(item.visual,item.step)
            nxt_info=right_content(item)
            transitions=[FadeIn(nxt_graph),FadeIn(nxt_info)]
            if current_graph is not None:
                transitions.extend([FadeOut(current_graph),FadeOut(current_info)])
            self.play(*transitions,run_time=transition)
            spent=transition
            if not self.smoke and payload.get('kind')=='motion':
                # A genuine point traveling along the mathematical curve.
                dot=payload['dot'];path=payload['path']
                self.play(MoveAlongPath(dot,path),run_time=3.6,rate_func=linear)
                spent+=3.6
            elif not self.smoke and payload.get('kind')=='trace':
                dot=mark(ax('line'),-1.5,-3,GOLD,.065)
                # The plotted line is the graph itself, not a decorative motion path.
                # Use its own points for an accurate moving marker.
                self.add(dot)
                self.play(MoveAlongPath(dot,payload['path']),run_time=2.0,rate_func=linear)
                self.remove(dot);spent+=2.0
            elif not self.smoke and payload.get('kind')=='transform':
                # Real geometry change; not a static image or decorative transformation.
                self.play(Transform(payload['source'],payload['target']),run_time=3.2)
                spent+=3.2
            else:
                # A subtle but intentional teaching hold; avoid flashing graphics.
                self.wait(effect if not self.smoke else .04)
                spent+=effect if not self.smoke else .04
            self.wait(max(.02,span-spent))
            current_graph,current_info=nxt_graph,nxt_info
        self.play(FadeOut(current_graph),FadeOut(current_info),run_time=.6 if not self.smoke else .05)

class INT01(BaseLesson):
    pass

class INT01_SMOKE(BaseLesson):
    smoke=True
