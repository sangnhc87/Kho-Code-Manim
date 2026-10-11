"""XSS182 · Ba điểm thẳng hàng — lưới 3 × 3 có 8 đường (3 hàng, 3 cột, 2 chéo): 8/84 = 2/21."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path

from manim import Create, Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, WHITE  # noqa: E402

EPISODE = {'code': 'XSS182', 'answer': '2/21'}
PROBLEM = ['Chọn ngẫu nhiên $3$ trong $9$ điểm',
           'của lưới $3 times 3$. Xác suất',
           'ba điểm đó thẳng hàng?']
OPTIONS = ['1/12', '2/21', '1/7']
CORRECT = 1
ANSWER_VALUE = 2 / 21
PTS = list(product(range(3), repeat=2))
LINES = [((0, j), (2, j)) for j in range(3)] + [((i, 0), (i, 2)) for i in range(3)] + [((0, 0), (2, 2)), ((0, 2), (2, 0))]


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0])


BEATS = [
    Beat('hook', 'hook', 'Lưới ba nhân ba gồm chín điểm. Chọn ngẫu nhiên ba điểm. Xác suất ba điểm đó nằm trên một đường thẳng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười hai, hai phần hai mươi mốt, hay một phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không gian mẫu: tổ hợp chập ba của chín, bằng tám mươi tư bộ ba điểm.'),
    Beat('s2', 'solve', 'Bộ ba thẳng hàng phải nằm trọn trên một đường đi qua ba điểm của lưới: ba hàng ngang, ba cột dọc và hai đường chéo, '
                        'tổng cộng tám đường, mỗi đường đúng một bộ.'),
    Beat('s3', 'solve', 'Xác suất bằng tám phần tám mươi tư, tức hai phần hai mươi mốt. Đừng quên hai đường chéo, lỗi rất hay gặp!'),
    Beat('answer', 'solve', 'Đáp án: hai phần hai mươi mốt. Với lưới điểm, hãy liệt kê hệ thống: hàng, cột, rồi chéo!'),
    Beat('outro', 'outro', outro_text(182)),
]

FORMULAS = formulas('2/21', OPTIONS,
                    omega='n(Omega) = C_9^3 = 84',
                    prob='P = (3 + 3 + 2)/84 = 2/21')


def validate() -> bool:
    good = sum(collinear(*t) for t in combinations(PTS, 3))
    assert good == 8 and F(good, comb(9, 3)) == F(2, 21)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS182(ShortScene):
    N = 182

    def P(self, p):
        return [-1.8 + 1.8 * p[1], 2.8 - 1.8 * p[0], 0]

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.dots = VGroup(*[Dot(self.P(p), radius=.16, color=WHITE) for p in PTS])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.dots, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('omega', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        cols = [CYAN] * 3 + [CORAL] * 3 + [GOLD] * 2
        for i, ((a, b), c) in enumerate(zip(LINES, cols)):
            self.wait_until(.1 + .1 * i, t0)
            self.play(Create(Line(self.P(a), self.P(b), color=c, stroke_width=6)), run_time=self.rt(.03))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
