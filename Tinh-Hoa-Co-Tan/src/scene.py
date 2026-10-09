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
from src.engine_coords import board_fen
from src.layout import (BOARD_GRID_STEP, BOARD_CENTER_X, BOARD_CENTER_Y,
                        HEADER_LINE_Y, assert_safe_layout)

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
config.background_color = BG  # Must be set before Manim creates the camera.
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


def fit_label(value, x, y, max_width, max_height, font_size,
              color, bold=False, wrap=None, max_lines=3):
    """Auto-fit real Pango text bounds; never let captions overflow the panel."""
    content = text_lines(value,wrap,max_lines) if wrap else str(value)
    obj = Text(content,font=FONT,font_size=font_size,color=color,
               weight='BOLD' if bold else 'NORMAL',line_spacing=1.18)
    if obj.width > max_width:
        obj.scale(max_width / obj.width)
    if obj.height > max_height:
        obj.scale(max_height / obj.height)
    return obj.move_to([x,y,0])


class XiangqiDisplay(VGroup):
    """Board coordinates a0 = black top-left, i9 = red bottom-right."""
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        # 16:9 Manim frame: x = -7.11..7.11, y = -4..4.
        # Reserve y>3.18 for the header and y<-3.52 for the footer.
        # The entire board including its border must fit within this safe area.
        assert_safe_layout()
        self.step = BOARD_GRID_STEP
        self.ox, self.oy = BOARD_CENTER_X, BOARD_CENTER_Y
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
        # Captions use display coordinates, with rank 0 on Black's side.
        # Cột cờ tướng: Đỏ (9 đến 1 từ trái sang phải), Đen (1 đến 9 từ trái sang phải)
        for x in range(9):
            art.add(Text(str(9-x),font=FONT,font_size=12,color=LIGHT).move_to(
                [self.xy((x,9))[0],-3.30,0]))
            art.add(Text(str(x+1),font=FONT,font_size=12,color=LIGHT).move_to(
                [self.xy((x,0))[0],2.95,0]))
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

    def reset_position(self, fen, scene):
        """Show complete board throughout; only pieces change between branches."""
        new_state=Board.fen(fen)
        if self.state.cells == new_state.cells and self.state.turn == new_state.turn:
            return
        old_mobs=VGroup(*self.pieces.values())
        if len(self.pieces):
            scene.play(FadeOut(old_mobs),run_time=.22)
            self.remove(*list(self.pieces.values()))
        self.state=new_state
        self.pieces={}
        new_mobs=VGroup()
        for pos,piece in new_state.cells.items():
            mob=self.make_piece(piece).move_to(self.xy(pos))
            self.pieces[pos]=mob
            self.add(mob)
            new_mobs.add(mob)
        scene.play(FadeIn(new_mobs),run_time=.25)

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
            self.remove(captured)
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
        episode_file=Path(os.environ['XIANGQI_EPISODE'])
        out=Path(os.environ['XIANGQI_OUTPUT'])
        data=json.loads(episode_file.read_text(encoding='utf-8'))
        timing=json.loads((out/'voice'/'timing.json').read_text(encoding='utf-8'))
        board=XiangqiDisplay(Board.fen(data['fen']))

        # Consistent frame-safe, 16:9 design. No content overlaps the board.
        brand=Text('TINH HOA CỜ TÀN',font=FONT,font_size=26,
                   color=GOLD,weight='BOLD')
        brand.to_edge(LEFT,buff=.64).move_to([-6.34,3.57,0],aligned_edge=LEFT)
        series=Text(f"{data['id'].upper()}  •  NGUYỄN VĂN SANG",font=FONT,
                    font_size=15,color=MUTED)
        series.move_to([6.27,3.57,0],aligned_edge=RIGHT)
        header_line=Line([-6.35,HEADER_LINE_Y,0],[6.34,HEADER_LINE_Y,0],
                         color='#35465D',stroke_width=1.3)

        footer_bg=Rectangle(width=14.22,height=.40,
              fill_color='#09101C',fill_opacity=.96,stroke_width=0)
        footer_bg.to_edge(DOWN,buff=0)
        footer=Text('Nguyễn Văn Sang   •   Mời tôi ly cà phê — MoMo: 0389.821.115',
                    font=FONT,font_size=14,color=MUTED)
        footer.move_to(footer_bg)

        right_bg=RoundedRectangle(width=6.02,height=6.07,
             corner_radius=.20,stroke_width=1.4,stroke_color='#35465D',
             fill_color=PANEL,fill_opacity=1)
        right_bg.move_to([3.21,-.10,0])
        segment=Text('MỞ ĐẦU',font=FONT,font_size=17,
                     color=GREEN,weight='BOLD').move_to([3.20,2.60,0])
        chapter=fit_label(data.get('title','TINH HOA CỜ TÀN'),
                 x=3.20,y=2.03,max_width=5.20,max_height=.55,font_size=24,
                 color=LIGHT,bold=True)
        headline=fit_label('ĐỎ ĐI TRƯỚC',
                 x=3.20,y=1.20,max_width=5.27,max_height=.94,font_size=29,
                 color=GOLD,bold=True,wrap=26,max_lines=2)
        divider=Line([.62,.36,0],[5.80,.36,0],
                     color='#46607A',stroke_width=1.5)
        tip_label=Text('QUY ƯỚC: TIẾN — THOÁI — BÌNH',font=FONT,font_size=14,
                       color=CYAN,weight='BOLD').move_to([3.20,-.08,0])
        insight=fit_label('Chờ phân tích nước đầu.',
                 x=3.20,y=-1.20,max_width=5.10,max_height=1.70,font_size=25,
                 color=LIGHT,wrap=32,max_lines=4)
        goal_text = data.get('goal_text', 'MỤC TIÊU: BẮT SĨ' if 'sĩ' in data.get('title','').lower() else 'MỤC TIÊU: BẮT TƯỢNG')
        stamp_label=(f'{goal_text} • CHƯA XÉT LUẬT LẶP NƯỚC'
               if data.get('analysis_status') in ('four_piece_retrograde_ordinary_moves', 'four_piece_elephant_retrograde')
               else 'BIẾN MINH HỌA • CHƯA CHỨNG MINH THẮNG')
        stamp=fit_label(stamp_label,x=3.20,y=-2.70,
                 max_width=5.22,max_height=.23,font_size=12,color=MUTED)
        # Fail early if later design changes accidentally crop the board again.
        if board.get_top()[1] > header_line.get_y() - .15:
            raise ValueError('Layout: board intersects the header safe area')
        if board.get_bottom()[1] < footer_bg.get_top()[1] + .15:
            raise ValueError('Layout: board intersects the footer safe area')
        if board.get_right()[0] > right_bg.get_left()[0] - .20:
            raise ValueError('Layout: board intersects the teaching panel')
        self.add(board,right_bg,header_line,divider,chapter,headline,
                 insight,segment,tip_label,stamp,brand,series,footer_bg,footer)
        self.opening_card(out)
        if len(timing) != len(data['beats']):
            raise ValueError('Number of audio clips differs from episode segments')
        timeline=[]
        for i,(beat,audio) in enumerate(zip(data['beats'],timing)):
            # audio duration is source of truth; video segment extends to include animations.
            start=self.time
            entry={'beat':i+1,'label':beat['label'],'start':float(start),
                   'initial_fen':board_fen(board.state),'moves':[]}
            if beat.get('fen'):
                board.reset_position(beat['fen'],self)
            # Start voice after changing to the position under discussion.
            start=self.time
            self.add_sound(audio['audio'])
            next_segment=fit_label(beat['label'].upper(),x=3.20,y=2.60,
                 max_width=5.00,max_height=.32,font_size=17,color=GREEN,bold=True)
            next_title=fit_label(beat['headline'],x=3.20,y=1.20,
                 max_width=5.27,max_height=.94,font_size=29,color=GOLD,
                 bold=True,wrap=26,max_lines=2)
            next_insight=fit_label(beat['insight'],x=3.20,y=-1.20,
                 max_width=5.10,max_height=1.70,font_size=25,color=LIGHT,
                 wrap=32,max_lines=4)
            self.play(Transform(segment,next_segment),Transform(headline,next_title),
                      Transform(insight,next_insight),run_time=.55)
            moves=beat.get('moves',[])
            if beat.get('horse_leg'):
                pair=beat['horse_leg']
                board.horse_leg(self,pair[0],pair[1])
            if beat.get('spotlight') and beat.get('spotlight_before'):
                board.highlight(self,beat['spotlight'])
            for uci in moves:
                board.move_piece(uci,self)
                entry['moves'].append({'display_move':uci,'time':float(self.time),
                                      'fen':board_fen(board.state)})
                self.wait(.28)
            if beat.get('spotlight') and not beat.get('spotlight_before'):
                board.highlight(self,beat['spotlight'])
            # Optional dramatic delay following the spoken segment.
            self.wait(max(.1, audio['seconds']+float(beat.get('pause',.65))-(self.time-start)))
            entry['end']=float(self.time)
            timeline.append(entry)
        self.closing_card(out)
        (out/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n',
                                        encoding='utf-8')

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
