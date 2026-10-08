"""GEO01 - Diem nam TRONG tam giac: bai tap va dieu kien tong quat.

Run from repository root:
    python scripts/build_geo_formulas.py
    manim -ql --fps 24 episodes/geo01_point_inside_triangle.py GEO01
    manim -qh -r 1920,1080 --fps 30 episodes/geo01_point_inside_triangle.py GEO01

Math rendered with Typst, shapes and motion rendered with Manim.
No voice is synthesized; see narration_GEO01.md.
"""
from __future__ import annotations

from pathlib import Path
import sys
import numpy as np
from manim import (
    Scene, config, VGroup, Group, Text, RoundedRectangle, Polygon, Line,
    Dot, ImageMobject, Arrow, DashedLine, FadeIn, FadeOut, Create,
    GrowFromCenter, Indicate, Circumscribe, ValueTracker, always_redraw,
    ReplacementTransform, AnimationGroup, ORIGIN
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from series_config import PALETTE as P  # noqa: E402

config.background_color = P['bg']
config.frame_width = 14.222222
config.frame_height = 8.0
FONT = 'Noto Sans'
LEFT_X, RIGHT_X = -3.81, 3.20
LEFT_W, RIGHT_W = 6.12, 7.28
PANEL_Y, PANEL_H = -0.27, 6.34
A = (0.0, 3.0)
B = (-1.0, 2.0)
C = (2.0, 1.0)
M_LO = 13.0 / 8.0
M_HI = 7.0 / 4.0


def label(value, size=25, color=None, max_w=None, bold=False):
    out = Text(str(value), font=FONT, font_size=size,
               color=color or P['text'], weight='BOLD' if bold else 'NORMAL')
    if max_w is not None and out.width > max_w:
        out.scale_to_fit_width(max_w)
    return out


def rectangle(w, h, color=None, stroke=None):
    return RoundedRectangle(width=w, height=h, corner_radius=0.16,
                            fill_color=color or P['panel'], fill_opacity=1,
                            stroke_color=stroke or P['line'], stroke_width=1.2)


def formula(code, max_w=6.30, max_h=.69):
    filename = ROOT / 'assets' / 'rendered' / f'{code}.png'
    if not filename.is_file():
        raise RuntimeError(f'Chua tao Typst asset {filename}. Run python scripts/build_geo_formulas.py')
    pic = ImageMobject(str(filename))
    if pic.width > max_w:
        pic.scale_to_fit_width(max_w)
    if pic.height > max_h:
        pic.scale_to_fit_height(max_h)
    return pic


def fullpos(x, y):
    return np.array([-4.50 + 1.17 * x, -2.29 + 1.17 * y, 0])


def zoompos(x, y):
    return np.array([LEFT_X + 6.2 * (x - 1.71), -.32 + 6.2 * (y - 1.25), 0])


def small_dot(xy, xyz, col=P['gold'], r=.075):
    return Dot(xyz(*xy), radius=r, color=col)


def side_labels(xyz=fullpos):
    items = VGroup()
    for point, name, offset in [
        (A, 'A', np.array([-.22,.25,0])),
        (B, 'B', np.array([-.28,-.06,0])),
        (C, 'C', np.array([.22,-.15,0]))
    ]:
        dot = small_dot(point, xyz, P['gold'])
        txt = label(name, 24, P['gold'], bold=True).move_to(xyz(*point) + offset)
        items.add(dot,txt)
    return items


def base_triangle():
    fill = Polygon(fullpos(*A), fullpos(*B), fullpos(*C),
                   fill_color=P['cyan'], fill_opacity=.12,
                   stroke_color=P['cyan'], stroke_width=3)
    grid = VGroup()
    for x in range(-1, 3):
        grid.add(Line(fullpos(x,.30), fullpos(x,3.38),
                      color=P['line'], stroke_width=.65))
    for y in range(1,4):
        grid.add(Line(fullpos(-1.50,y), fullpos(2.55,y),
                      color=P['line'], stroke_width=.65))
    axes = VGroup(
        Line(fullpos(-1.5,0), fullpos(2.55,0), color=P['muted'], stroke_width=1.2),
        Line(fullpos(0,.25), fullpos(0,3.40), color=P['muted'], stroke_width=1.2)
    )
    return Group(grid, axes, fill, side_labels())


def zoom_geometry():
    # Viewport all coordinates are mapped through a UNIFORM scale, preserving angles.
    p = zoompos
    area = Polygon(p(1.40, 1.60), p(2.0, 1.0), p(1.40, 1.20),
                   fill_color=P['cyan'], fill_opacity=.14, stroke_opacity=0)
    ac = Line(p(1.40, 1.60), p(2.0, 1.0), stroke_color=P['cyan'], stroke_width=3)
    bc = Line(p(1.40, 1.20), p(2.0, 1.0), stroke_color=P['cyan'], stroke_width=3)
    locus = Line(p(1.40, .90), p(2.0, 1.50), color=P['purple'], stroke_width=3)
    inside = Line(p(M_LO, M_LO-.5),p(M_HI, M_HI-.5),
                  color=P['green'], stroke_width=9)
    p_entry = small_dot((M_LO,M_LO-.5),p,P['gold'],r=.09)
    p_exit = small_dot((M_HI,M_HI-.5),p,P['gold'],r=.09)
    n1 = label('13/8', 21, P['gold'], bold=True).move_to(p(M_LO, M_LO-.5)+[-.70,-.27,0])
    n2 = label('7/4', 21, P['gold'], bold=True).move_to(p(M_HI, M_HI-.5)+[.53,.30,0])
    leg1 = label('BC', 18,P['cyan']).move_to(p(1.48,1.16)+[-.18,-.08,0])
    leg2 = label('AC', 18,P['cyan']).move_to(p(1.45,1.55)+[-.14,.17,0])
    return Group(area,ac,bc,locus,inside,p_entry,p_exit,n1,n2,leg1,leg2)


class GEO01(Scene):
    """Standalone lesson; presentation two columns with no text over geometry."""
    def setup(self):
        self.active = Group()
        header1 = label('SANG MATH  /  HÌNH HỌC TỌA ĐỘ', 22, P['cyan'], bold=True)
        header1.move_to([-3.43, 3.60,0])
        header2 = label('GEO01  ·  MIỀN TRONG TAM GIÁC', 20, P['muted'])
        header2.move_to([4.15, 3.60, 0])
        left = rectangle(LEFT_W, PANEL_H).move_to([LEFT_X,PANEL_Y,0])
        right = rectangle(RIGHT_W,PANEL_H).move_to([RIGHT_X,PANEL_Y,0])
        divider = Line([-6.9,3.29,0],[6.9,3.29,0],color=P['line'],stroke_width=1.2)
        footer = label('VỊ TRÍ ĐIỂM  ·  NỬA MẶT PHẲNG  ·  TÍCH CÓ HƯỚNG',18,P['muted'])
        footer.move_to([0,-3.78,0])
        self.add(Group(left,right,header1,header2,divider,footer))

    def clear(self):
        if len(self.active.submobjects):
            self.play(FadeOut(self.active), run_time=.55)
        self.active=Group()

    def show(self, title, lines, illustration=None, *, asset=None, note=None, pause=3.2):
        self.clear()
        pieces = Group()
        title_obj = label(title,30,P['gold'],bold=True,max_w=6.45)
        title_obj.move_to([RIGHT_X,2.44,0])
        pieces.add(title_obj)
        for i,ln in enumerate(lines[:6]):
            txt = label(ln,23,P['text'],max_w=6.45)
            txt.move_to([RIGHT_X,1.78-i*.49,0])
            pieces.add(txt)
        if asset:
            f = formula(asset)
            f.move_to([RIGHT_X,-1.35,0])
            pieces.add(f)
        if note:
            border = rectangle(6.60,.48,P['panel_alt'],P['purple'])
            border.move_to([RIGHT_X,-2.54,0])
            n = label(note,19,P['cyan'],max_w=6.28)
            n.move_to(border)
            pieces.add(border,n)
        self.active.add(pieces)
        if illustration is not None:
            self.active.add(illustration)
            self.play(FadeIn(illustration), FadeIn(pieces),run_time=1.15)
        else:
            self.play(FadeIn(pieces),run_time=.85)
        self.wait(pause)
        return pieces

    def intro(self):
        tri = base_triangle()
        self.show('BÀI TOÁN MỞ ĐẦU', [
            'Cho A(0; 3), B(-1; 2), C(2; 1).',
            'M(m; (2m - 1)/2) chuyển động.',
            'Tìm m để M nằm TRONG tam giác.',
            'Nếu a < m < b, tính T = 8a + 4b.'
        ],tri,note='Chú ý: không lấy các điểm trên cạnh!',pause=3.0)
        self.play(Indicate(tri[2],color=P['cyan'],scale_factor=1.06),run_time=1.3)
        self.wait(1.1)

    def moving_line(self):
        left = base_triangle()
        locus = Line(fullpos(1.02,.52),fullpos(2.28,1.78),
                     color=P['purple'], stroke_width=3)
        dot=Dot(fullpos(1.37,.87),radius=.095,color=P['gold'])
        moving=Group(left,locus,dot)
        self.show('BIỂU DIỄN QUỸ TÍCH M', [
            'Tung độ của M bằng m - 1/2.',
            'Đặt x = m, suy ra y = x - 1/2.',
            'M luôn thuộc một đường thẳng.',
            'Chỉ một đoạn ngắn nằm trong ABC.'
        ], moving,asset='geo_line',note='Cần xác định HAI giao điểm biên.',pause=2.2)
        pts=[fullpos(x,x-.5) for x in [1.37,1.62,1.68,1.75,1.96]]
        for xy in pts[1:]:
            self.play(dot.animate.move_to(xy),run_time=.67)
        self.wait(1.4)

    def zoom(self):
        graph=zoom_geometry()
        self.show('PHÓNG ĐẠI VÙNG GẦN C', [
            'Đoạn màu xanh lá: M ở trong ABC.',
            'Hai chấm vàng: M nằm trên cạnh.',
            'Tại điểm biên phải dùng dấu <.',
            'Hãy tìm hoành độ hai đầu đoạn.'
        ],graph, note='Phóng đại đồng dạng, không bóp méo hình.',pause=3.5)
        self.play(Indicate(graph[4],color=P['green'],scale_factor=1.15),run_time=1.6)
        self.wait(1.8)

    def find_endpoints(self):
        graph=zoom_geometry()
        self.show('HAI ĐƯỜNG THẲNG BIÊN', [
            'Cạnh BC: x + 3y = 5.',
            'Cạnh AC: x + y = 3.',
            'Đường chuyển động: y = x - 1/2.',
            'Giải hai hệ phương trình giao điểm.'
        ],graph,asset='geo_bounds',note='BC gặp trước, AC gặp sau khi m tăng.',pause=4)
        self.play(Indicate(graph[5],color=P['gold']),Indicate(graph[6],color=P['gold']),run_time=1.7)
        self.wait(1.2)

    def inequalities(self):
        tri=base_triangle()
        self.show('BA NỬA MẶT PHẲNG', [
            'Với tam giác ABC ngược chiều kim đồng hồ:',
            'AB: x - y + 3 > 0.',
            'BC: x + 3y - 5 > 0.',
            'CA: 3 - x - y > 0.',
            'Điểm trong phải thỏa CẢ BA.'
        ],tri,asset='geo_three',note='Các dấu đều nghiêm ngặt: miền TRONG.',pause=5.4)

    def substitute(self):
        geo=zoom_geometry()
        self.show('THAY TỌA ĐỘ ĐIỂM M', [
            'x = m; y = m - 1/2.',
            'AB: 7/2 > 0 (luôn đúng).',
            'BC: 4m - 13/2 > 0.',
            'CA: 7/2 - 2m > 0.',
            'Lấy giao các điều kiện của m.'
        ], geo,asset='geo_bounds',note='m thuộc khoảng mở (13/8 ; 7/4).',pause=4.2)

    def result(self):
        tri=zoom_geometry()
        r=self.show('KẾT LUẬN BÀI TOÁN', [
            'a = 13/8,     b = 7/4.',
            'Hai đầu mút nằm trên cạnh tam giác.',
            'Vì yêu cầu miền trong nên không lấy.',
            'Tính giá trị T = 8a + 4b.'
        ],tri,asset='geo_final',note='ĐÁP ÁN CHÍNH XÁC: 20',pause=4.2)
        self.play(Circumscribe(r[-3],color=P['green'],time_width=1),run_time=1.3)
        self.wait(1)

    def general(self):
        tri=base_triangle()
        self.show('ĐỊNH LÝ TỔNG QUÁT', [
            'Đặt D = [AB, AC] khác 0.',
            'Với PQ: D_PQ(M) = [PQ, PM].',
            's = dấu(D) là +1 hoặc -1.',
            'M ở trong khi 3 tích s·D_PQ(M)',
            'ứng với AB, BC, CA đều dương.'
        ],tri,asset='geo_general',note='Đúng cho tam giác ở MỌI hướng.',pause=5.0)

    def general_examples(self):
        tri=base_triangle()
        m_in=Dot(fullpos(1.10,1.62),radius=.09,color=P['green'])
        m_out=Dot(fullpos(.65,2.72),radius=.09,color=P['red'])
        m_edge=Dot(fullpos(1.00,2.00),radius=.09,color=P['gold'])
        li=label('TRONG',19,P['green']).next_to(m_in,[-1,0,0],buff=.2)
        lo=label('NGOÀI',19,P['red']).next_to(m_out,[1,0,0],buff=.15)
        le=label('CẠNH AC',17,P['gold']).next_to(m_edge,[-1,0,0],buff=.13)
        chart=Group(tri,m_in,m_out,m_edge,li,lo,le)
        self.show('PHÂN BIỆT BA VỊ TRÍ', [
            'Ba dấu đúng nghiêm ngặt: M ở trong.',
            'Một tích có hướng bằng 0:',
            'M có thể nằm trên đường chứa cạnh.',
            'Ba dấu không âm: M ở trong',
            'hoặc trên BIÊN tam giác.'
        ],chart,asset='geo_boundary',note='Nằm trên cạnh khác nằm trên đường thẳng.',pause=5.4)

    def barycentric(self):
        tri=base_triangle()
        self.show('MỞ RỘNG: TỌA ĐỘ TỈ CỰ', [
            'Có duy nhất bộ (α, β, γ) sao cho:',
            'M = αA + βB + γC.',
            'α + β + γ = 1.',
            'M ở trong khi cả ba hệ số > 0.',
            'Hữu ích với tham số, đường thẳng, 3D.'
        ],tri,asset='geo_bary',note='Đây là một tiêu chuẩn tương đương.',pause=4.5)

    def finish(self):
        tri=base_triangle()
        self.show('NHỚ BA BƯỚC', [
            '1. Viết phương trình ba cạnh.',
            '2. Chọn đúng nửa mặt phẳng chứa tam giác.',
            '3. Lấy GIAO ba bất phương trình.',
            'Nếu M có tham số, giải hệ điều kiện.',
            'Muốn lấy cả biên: dùng dấu không nghiêm.'
        ],tri,asset='geo_final',note='SANG MATH  ·  TƯ DUY HÌNH HỌC TỌA ĐỘ',pause=5.0)

    def construct(self):
        self.intro()
        self.moving_line()
        self.zoom()
        self.find_endpoints()
        self.inequalities()
        self.substitute()
        self.result()
        self.general()
        self.general_examples()
        self.barycentric()
        self.finish()
