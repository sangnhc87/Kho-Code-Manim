"""XSS099 · Tam giác đều trong lục giác — C(6,3) = 20 tam giác, chỉ 2 đều: 1/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import Dot, FadeIn, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT, WHITE  # noqa: E402
from common.visuals import polygon_pts  # noqa: E402

EPISODE = {'code': 'XSS099', 'answer': '1/10'}
PROBLEM = ['Chọn ngẫu nhiên $3$ đỉnh của một lục giác',
           'đều. Xác suất được một tam giác đều?']
OPTIONS = ['1/5', '1/10', '1/20']
CORRECT = 1
ANSWER_VALUE = .1


def equilateral(t):
    a, b, c = sorted(t)
    return (b - a, c - b, a + 6 - c) == (2, 2, 2)


BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của một lục giác đều rồi nối lại thành tam giác. '
                         'Xác suất được một tam giác đều là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, một phần mười, hay một phần hai mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Số cách chọn ba đỉnh trong sáu đỉnh: tổ hợp chập ba của sáu, bằng hai mươi tam giác.'),
    Beat('s2', 'solve', 'Tam giác đều phải lấy các đỉnh cách nhau đúng một đỉnh: đỉnh một, ba, năm, '
                        'hoặc đỉnh hai, bốn, sáu. Chỉ có đúng hai tam giác đều.'),
    Beat('s3', 'solve', 'Xác suất bằng hai phần hai mươi, tức một phần mười. Những bài hình học đếm được '
                        'luôn quy về: đếm tất cả, đếm cái thỏa, rồi chia.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười. Thử tiếp với bát giác: tam giác vuông thì sao?'),
    Beat('outro', 'outro', outro_text(99)),
]

FORMULAS = formulas('1/10', OPTIONS, n='n(Omega) = C_6^3 = 20', prob='P = 2/20 = 1/10')


def validate() -> bool:
    tris = list(combinations(range(6), 3))
    assert len(tris) == comb(6, 3) == 20 and F(sum(equilateral(t) for t in tris), 20) == F(1, 10)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS099(ShortScene):
    N = 99

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.pts = polygon_pts(6, 2.0, (0, 1.4))
        self.hexa = VGroup(Polygon(*self.pts, stroke_color=SOFT, stroke_width=4),
                           *[Dot(p, radius=.12, color=WHITE) for p in self.pts],
                           *[self.TM(f'${k + 1}$', 26, SOFT).move_to([p[0] * 1.15, 1.4 + (p[1] - 1.4) * 1.15, 0])
                             for k, p in enumerate(self.pts)])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.hexa), run_time=self.rt(.15))
        self.tri = Polygon(self.pts[0], self.pts[1], self.pts[3], stroke_color=CYAN, stroke_width=5, fill_color=CYAN,
                           fill_opacity=.2)
        self.play(FadeIn(self.tri), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.tri.animate.set_opacity(0), run_time=self.rt(.03))
        a = Polygon(self.pts[0], self.pts[2], self.pts[4], stroke_color=GOLD, stroke_width=6, fill_color=GOLD, fill_opacity=.3)
        b = Polygon(self.pts[1], self.pts[3], self.pts[5], stroke_color=CORAL, stroke_width=6, fill_color=CORAL, fill_opacity=.3)
        self.wait_until(.3, t0)
        self.play(FadeIn(a), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(FadeIn(b), run_time=self.rt(.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('đếm tất cả, đếm cái thỏa, rồi chia', 26, SOFT), anim='fade')
