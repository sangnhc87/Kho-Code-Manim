"""XSS188 · Hai số từ 1 đến 100 — phần bù: tích không chia hết cho 3 khi cả hai không chia hết: 1 − C(67,2)/C(100,2) = 83/150."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS188', 'answer': '83/150'}
PROBLEM = ['Chọn ngẫu nhiên $2$ số khác nhau',
           'từ $1$ đến $100$. Xác suất tích hai',
           'số chia hết cho $3$?']
OPTIONS = ['1/3', '83/150', '5/9']
CORRECT = 1
ANSWER_VALUE = 83 / 150

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai số khác nhau từ một đến một trăm. Xác suất tích của chúng chia hết cho ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, tám mươi ba phần một trăm năm mươi, hay năm phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tích chia hết cho ba khi có ít nhất một số chia hết cho ba. "Ít nhất một" thì đi đường phần bù: '
                        'cả hai số đều không chia hết cho ba.'),
    Beat('s2', 'solve', 'Từ một đến một trăm có ba mươi ba số chia hết cho ba, còn sáu mươi bảy số không chia hết. '
                        'Chọn hai số đều không chia hết: tổ hợp chập hai của sáu mươi bảy, hai nghìn hai trăm mười một cách.'),
    Beat('s3', 'solve', 'Xác suất bằng một trừ hai nghìn hai trăm mười một phần bốn nghìn chín trăm năm mươi, '
                        'tức tám mươi ba phần một trăm năm mươi, khoảng không phẩy năm năm.'),
    Beat('answer', 'solve', 'Đáp án: tám mươi ba phần một trăm năm mươi. Chia hết cho số nguyên tố: nghĩ ngay tới phần bù!'),
    Beat('outro', 'outro', outro_text(188)),
]

FORMULAS = formulas('83/150', OPTIONS,
                    cnt='33 " số chia hết cho 3", quad 67 " số không"',
                    comp='P = 1 - (C_67^2)/(C_100^2) = 1 - 2211/4950 = 83/150')


def validate() -> bool:
    p = F(sum(a * b % 3 == 0 for a, b in combinations(range(1, 101), 2)), comb(100, 2))
    assert p == F(83, 150) == 1 - F(comb(67, 2), comb(100, 2))
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS188(ShortScene):
    N = 188

    def hook_visual(self, t0):
        self.board_top = -1.3
        s = .38
        self.cells = VGroup(*[VGroup(Square(side_length=s * .92, stroke_width=0, fill_color=PANEL, fill_opacity=1),
                                     self.MNum(k, 0, SOFT, 14)) for k in range(1, 101)])
        for k, c in enumerate(self.cells):
            c.move_to([(k % 10 - 4.5) * s, 2.7 - (k // 10) * s, 0])
            c[1].move_to(c[0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.cells, lag_ratio=.004), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(*[c[0].animate.set_fill(CYAN, .55) for k, c in enumerate(self.cells, 1) if k % 3 == 0], run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('cnt', 1.6))
        self.wait_until(.45, t0)
        self.play(*[c[0].animate.set_fill(GOLD, .35) for k, c in enumerate(self.cells, 1) if k % 3], run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('comp', 1.6)
        self.write_board(m)
        self.frame(m)
