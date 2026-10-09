"""Reusable 16:9 Xiangqi documentary scene for Manim Community 0.19+.
Reads episode JSON, audio timing and Typst title cards from environment.
"""
from __future__ import annotations
import json
import math
import os
import textwrap
from pathlib import Path
from manim import *
from src.core import Board, parse_square

BG = '#0B1320'
PANEL = '#15243A'
GOLD = '#F5BF70'
SAND = '#E4C492'
RED = '#C94346'
INK = '#2F2721'
LIGHT = '#F4EFE1'
MUTED = '#B5C5D6'
GREEN = '#54CEA9'
CYAN = '#6ED6EF'
FONT = 'Noto Sans'
CJK = 'Noto Sans CJK SC'
PIECE_GLYPH = {'K':'帥','A':'仕','B':'相','E':'相','N':'傌','H':'傌','R':'俥','C':'炮','P':'兵',
               'k':'將','a':'士','b':'象','e':'象','n':'馬','h':'馬','r':'車','c':'砲','p':'卒'}


def text_lines(value, width=31, max_lines=3):
    lines = textwrap.wrap(str(value), width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(' .,') + '…'
    return '\n'.join(lines)


class XiangqiDisplay(VGroup):
    """Board coordinates a0 = black top-left, i9 = red bottom-right."""
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.step = 0.57
        self.ox, self.oy = -3.13, 2.28  # board centered on left of frame
        self.pieces = {}
        self.add(self.board_art())
        for pos, piece in state.cells.items():
            mob = self.make_piece(piece).move_to(self.xy(pos))
            self.pieces[pos] = mob
            self.add(mob)

    def xy(self, square):
        if isinstance(square,str): square = parse_square(square)
        x, y = square
        return np.array([self.ox + (x-4)*self.step, self.oy + (4.5-y)*self.step, 0])

    def board_art(self):
        s=self.step
        art=VGroup()
        # Subtle backlight and wood-esque board with no external artwork dependency.
        art.add(RoundedRectangle(width=s*8+0.57,height=s*9+0.52,
                  corner_radius=0.16,fill_color='#E4C89B',fill_opacity=1,
                  stroke_width=4,stroke_color='#856344').move_to(self.xy((4,4.5))))
        lines=VGroup()
        for y in range(10):
            lines.add(Line(self.xy((0,y)),self.xy((8,y)),stroke_color='#8A6540',stroke_width=1.65))
        for x in range(9):
            if x in (0,8):
                lines.add(Line(self.xy((x,0)),self.xy((x,9)),stroke_color='#8A6540',stroke_width=1.65))
            else:
                lines.add(Line(self.xy((x,0)),self.xy((x,4)),stroke_color='#8A6540',stroke_width=1.65))
                lines.add(Line(self.xy((x,5)),self.xy((x,9)),stroke_color='#8A6540',stroke_width=1.65))
        for top in (0,7):
            lines.add(Line(self.xy((3,top)),self.xy((5,top+2)),stroke_color='#8A6540',stroke_width=1.65))
            lines.add(Line(self.xy((5,top)),self.xy((3,top+2)),stroke_color='#8A6540',stroke_width=1.65))
        art.add(lines)
        river = Text('楚 河      漢 界',font=CJK,font_size=19,color='#89623E').move_to(self.xy((4,4.5)))
        art.add(river)
        return art

    def make_piece(self,piece):
        red=piece.isupper()
        body=Circle(radius=0.235,fill_color='#F5E4C3',fill_opacity=1,
                    stroke_width=2.6,stroke_color=RED if red else INK)
        inner=Circle(radius=0.205,stroke_color=RED if red else INK,
                     stroke_width=0.75,stroke_opacity=0.55)
        label=Text(PIECE_GLYPH[piece],font=CJK,font_size=24,
                   weight='BOLD',color=RED if red else INK)
        return VGroup(body,inner,label)

    def move_piece(self,uci,scene,available=1.6):
        src,dst=parse_square(uci[:2]),parse_square(uci[2:])
        mob=self.pieces.pop(src)
        captured=self.pieces.pop(dst,None)
        cue=Circle(radius=0.27,color=GOLD,stroke_width=5).move_to(self.xy(src))
        hint=Arrow(self.xy(src),self.xy(dst),buff=0.26,stroke_width=4,
                   max_tip_length_to_length_ratio=0.18,color=CYAN)
        scene.play(Create(cue),GrowArrow(hint),run_time=0.32)
        if captured is not None:
            scene.play(FadeOut(captured,scale=0.4),run_time=0.28)
        scene.play(mob.animate.move_to(self.xy(dst)),run_time=min(0.85,available*.65),rate_func=smooth)
        self.pieces[dst]=mob
        self.state.play(uci[:2],uci[2:])
        scene.play(FadeOut(hint),FadeOut(cue),run_time=0.23)

    def highlight(self, scene, square, color=GOLD, seconds=0.7):
        cue=Circle(radius=.32,stroke_width=5,color=color).move_to(self.xy(square))
        scene.play(Create(cue),run_time=.2)
        scene.wait(max(0.1,seconds-.35))
        scene.play(FadeOut(cue),run_time=.15)

    def horse_leg(self,scene,start,end):
        x,y=parse_square(start); a,b=parse_square(end)
        if sorted((abs(x-a),abs(y-b))) != [1,2]: return
        leg=(x+(1 if a>x else -1),y) if abs(a-x)==2 else (x,y+(1 if b>y else -1))
        dots=VGroup(Dot(self.xy(leg),radius=.105,color=GOLD),
                    DashedLine(self.xy((x,y)),self.xy(leg),color=GOLD),
                    DashedLine(self.xy(leg),self.xy((a,b)),color=CYAN))
        scene.play(Create(dots),run_time=.45)
        scene.wait(.4)
        scene.play(FadeOut(dots),run_time=.3)


class XiangqiLesson(Scene):
    def construct(self):
        config.background_color=BG
        episode_file=Path(os.environ['XIANGQI_EPISODE'])
        out=Path(os.environ['XIANGQI_OUTPUT'])
        data=json.loads(episode_file.read_text(encoding='utf-8'))
        timing=json.loads((out/'voice'/'timing.json').read_text(encoding='utf-8'))
        board=XiangqiDisplay(Board.fen(data['fen']))
        brand=Text('TINH HOA CỜ TÀN',font=FONT,font_size=21,color=GOLD,weight='BOLD').to_edge(UP,buff=.20).shift(RIGHT*.15)
        series=Text(f"{data['id'].upper()}  •  NGUYỄN VĂN SANG",font=FONT,font_size=13,color=MUTED)
        series.next_to(brand,DOWN,buff=.06)
        footer_bg=Rectangle(width=14.22,height=.38,fill_color='#09101C',fill_opacity=.96,stroke_width=0).to_edge(DOWN,buff=0)
        footer=Text('Nguyễn Văn Sang    •    Mời tôi ly cà phê — MoMo: 0389.821.115',font=FONT,font_size=14,color='#F1D5A0')
        footer.move_to(footer_bg)
        right_bg=RoundedRectangle(width=5.35,height=5.24,corner_radius=.22,
                    stroke_width=1.2,stroke_color='#35465D',fill_color=PANEL,fill_opacity=1)
        right_bg.move_to([3.53,-.10,0])
        divider=Line([1.05,-.6,0],[5.98,-.6,0],color='#46607A',stroke_width=1)
        title=Text('GIẢI MÃ CỜ TÀN',font=FONT,font_size=25,color=LIGHT,weight='BOLD').move_to([3.53,1.82,0])
        headline=Text('Hãy nhìn vào bàn cờ...',font=FONT,font_size=23,color=GOLD,weight='BOLD').move_to([3.5,.93,0])
        insight=Text('Mỗi nước cờ đều có mục đích.',font=FONT,font_size=19,color=LIGHT).move_to([3.5,-1.25,0])
        segment=Text('MỞ ĐẦU',font=FONT,font_size=13,color=GREEN,weight='BOLD').move_to([3.48,2.13,0])
        stamp_label=('MINH HỌA NGUYÊN LÝ • CHƯA CHỨNG MINH BIẾN THẮNG'
                 if data.get('analysis_status')!='engine_verified' else 'BIẾN ĐƯỢC ĐỐI CHIẾU VỚI ENGINE')
        stamp=Text(stamp_label,font=FONT,font_size=11,color=MUTED).move_to([3.52,-2.2,0])
        self.add(board, right_bg, divider, title, headline, insight, segment, stamp, brand, series, footer_bg, footer)
        self.opening_card(out)
        for i,(beat,audio) in enumerate(zip(data['beats'],timing)):
            # audio duration is source of truth; video segment extends to include animations.
            start=self.time
            self.add_sound(audio['audio'])
            next_segment=Text(beat['label'].upper(),font=FONT,font_size=13,color=GREEN,weight='BOLD').move_to(segment)
            next_title=Text(text_lines(beat['headline'],25,2),font=FONT,font_size=25,color=GOLD,
                            weight='BOLD',line_spacing=1.15).move_to(headline)
            next_insight=Text(text_lines(beat['insight'],34,4),font=FONT,font_size=20,color=LIGHT,
                            line_spacing=1.25).move_to(insight)
            self.play(Transform(segment,next_segment),Transform(headline,next_title),
                      Transform(insight,next_insight),run_time=.55)
            moves=beat.get('moves',[])
            if beat.get('horse_leg'):
                pair=beat['horse_leg']
                board.horse_leg(self,pair[0],pair[1])
            if beat.get('spotlight'):
                board.highlight(self,beat['spotlight'])
            for uci in moves:
                board.move_piece(uci,self)
                self.wait(.35)
            # Optional dramatic delay following the spoken segment.
            self.wait(max(.1, audio['seconds']+float(beat.get('pause',.65))-(self.time-start)))
        self.closing_card(out)

    def opening_card(self,out):
        png=out/'cards'/'intro.png'
        if not png.exists(): return
        art=ImageMobject(str(png))
        art.set_width(10.7)
        art.move_to(ORIGIN)
        scrim=Rectangle(width=14.5,height=8.3,fill_color=BG,fill_opacity=.96,stroke_width=0)
        self.play(FadeIn(scrim),FadeIn(art,scale=.94),run_time=.7)
        self.wait(1)
        self.play(FadeOut(art),FadeOut(scrim),run_time=.65)

    def closing_card(self,out):
        png=out/'cards'/'outro.png'
        if not png.exists(): return
        art=ImageMobject(str(png))
        art.set_width(10.8)
        art.move_to(ORIGIN)
        scrim=Rectangle(width=14.5,height=8.3,fill_color=BG,fill_opacity=.95,stroke_width=0)
        self.play(FadeIn(scrim),FadeIn(art,scale=.95),run_time=.8)
        self.wait(3)
        self.play(FadeOut(art),FadeOut(scrim),run_time=.6)
