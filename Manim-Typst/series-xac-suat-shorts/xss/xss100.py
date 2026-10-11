"""XSS100 · Tam giác vuông trong bát giác — vuông ⇔ có cạnh là đường kính: 4·6/C(8,3) = 24/56 = 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import Circle, Dot, FadeIn, Line, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT, STROKE, WHITE  # noqa: E402
from common.visuals import polygon_pts  # noqa: E402

EPISODE = {'code': 'XSS100', 'answer': '3/7'}
PROBLEM = ['Chọn ngẫu nhiên $3$ đỉnh của một bát giác',
           'đều. Xác suất được một tam giác vuông?']
OPTIONS = ['1/2', '3/7', '2/7']
CORRECT = 1
ANSWER_VALUE = 3 / 7


def right(t):
    return any((b - a) % 8 == 4 for a, b in combinations(t, 2))


BEATS = [
    Beat('hook', 'hook', 'Thử thách thứ một trăm! Chọn ngẫu nhiên ba đỉnh của một bát giác đều. '
                         'Xác suất ba đỉnh đó tạo thành một tam giác vuông là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần bảy, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mọi đỉnh của bát giác đều nằm trên một đường tròn. Tam giác nội tiếp là tam giác vuông '
                        'khi và chỉ khi một cạnh của nó là đường kính.'),
    Beat('s2', 'solve', 'Bát giác có bốn đường kính nối hai đỉnh đối diện. Mỗi đường kính ghép với một trong sáu đỉnh còn lại '
                        'cho một tam giác vuông: bốn nhân sáu bằng hai mươi tư tam giác.'),
    Beat('s3', 'solve', 'Tổng số tam giác là tổ hợp chập ba của tám, bằng năm mươi sáu. '
                        'Xác suất bằng hai mươi tư phần năm mươi sáu, tức ba phần bảy, gần một nửa!'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Hình học và xác suất gặp nhau thật đẹp. Cảm ơn bạn đã đồng hành đến thử thách thứ một trăm!'),
    Beat('outro', 'outro', outro_text(100)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    rule='"vuông" arrow.l.r.double "có cạnh là đường kính"',
                    cnt='4 dot 6 = 24',
                    prob='P = 24/C_8^3 = 24/56 = 3/7')


def validate() -> bool:
    tris = list(combinations(range(8), 3))
    assert len(tris) == comb(8, 3) == 56 and sum(right(t) for t in tris) == 24
    assert F(24, 56) == F(3, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS100(ShortScene):
    N = 100

    def hook_visual(self, t0):
        self.pts = polygon_pts(8, 2.0, (0, 1.3), start=90)
        self.oct = VGroup(Circle(radius=2.0, stroke_color=STROKE, stroke_width=2).move_to([0, 1.3, 0]),
                          Polygon(*self.pts, stroke_color=SOFT, stroke_width=4),
                          *[Dot(p, radius=.11, color=WHITE) for p in self.pts])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.oct), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.oct[0].animate.set_stroke(CYAN, 4), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        tri = Polygon(self.pts[0], self.pts[4], self.pts[2], stroke_color=GOLD, stroke_width=6, fill_color=GOLD, fill_opacity=.25)
        self.play(FadeIn(tri), run_time=self.rt(.1))
        self.tri = tri
        self.write_board(self.M('rule', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.tri.animate.set_opacity(0), run_time=self.rt(.03))
        diams = VGroup(*[Line(self.pts[k], self.pts[k + 4], color=CYAN, stroke_width=5) for k in range(4)])
        self.play(FadeIn(diams, lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.write_board(self.M('cnt', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('gần một nửa!', 30, GOLD, bold=True), anim='fade')
