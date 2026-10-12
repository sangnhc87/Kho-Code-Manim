"""XSS382 · Phi tiêu tối đa bốn lần — p = 0,4; P(trúng) = 1 − 0,6⁴ = 0,8704; P(trúng lần 1 | trúng) = 0,4/0,8704 = 125/272."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS382', 'answer': '125/272'}
PROBLEM = ['Ném phi tiêu đến khi trúng (mỗi lần',
           'trúng $"0,4"$), tối đa $4$ lần. Biết có',
           'trúng. Xác suất trúng ngay lần $1$?']
OPTIONS = ['125/272', '2/5', '5/8']
CORRECT = 0
ANSWER_VALUE = 125 / 272
P = F(2, 5)
HIT = 1 - (1 - P) ** 4
BRANCHES = [('T', GREEN, '"0,4"', []),
            ('X', SOFT, '"0,6"', [('T', GREEN, '"0,4"', []),
                                  ('X', SOFT, '"0,6"', [('T', GREEN, '"0,4"', []),
                                                        ('X', SOFT, '"0,6"', [('T', GREEN, '"0,4"', []), ('X', SOFT, '"0,6"', [])])])])]

BEATS = [
    Beat('hook', 'hook', 'Ném phi tiêu cho đến khi trúng, mỗi lần trúng với xác suất không phẩy bốn, nhưng chỉ được ném tối đa bốn lần. '
                         'Biết cuối cùng có trúng. Xác suất trúng ngay lần đầu?'),
    Beat('guess', 'hook', 'Một trăm hai mươi lăm phần hai trăm bảy mươi hai, hai phần năm, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây dừng bốn tầng. Không trúng lần nào khi trượt cả bốn lần: không phẩy sáu mũ bốn, bằng không phẩy một hai chín sáu.'),
    Beat('s2', 'solve', 'Vậy xác suất có trúng là một trừ đi, bằng không phẩy tám bảy không bốn.'),
    Beat('s3', 'solve', 'Trúng ngay lần một: không phẩy bốn. Chia cho không phẩy tám bảy không bốn, được một trăm hai mươi lăm phần hai trăm bảy mươi hai, khoảng bốn mươi sáu phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: một trăm hai mươi lăm phần hai trăm bảy mươi hai. Điều kiện có trúng loại nhánh trượt hết, đẩy xác suất lên.'),
    Beat('outro', 'outro', outro_text(382)),
]

FORMULAS = formulas('125/272', OPTIONS,
                    miss='P("trượt cả 4") = "0,6"^4 = "0,1296"',
                    hit='P("trúng") = 1 - "0,1296" = "0,8704"',
                    prob='P = ("0,4")/("0,8704") = 125/272')


def validate() -> bool:
    assert HIT == F(8704, 10000) and P / HIT == F(125, 272)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS382(TreeMixin, ShortScene):
    N = 382

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=.95, width=5.6, r=.3, edge_size=22)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[FadeIn(lv) for lv in self.levels[2:]], run_time=self.rt(.15))
        self.wait_until(.4, t0)
        self.write_board(self.M('miss', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('hit', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
