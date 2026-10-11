"""XSS134 · Đồng xu quyết định — ngửa 1 xúc xắc (P = 1/6), sấp 2 xúc xắc (P tổng 6 = 5/36): 11/72."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS134', 'answer': '11/72'}
PROBLEM = ['Tung xu: ngửa thì gieo $1$ xúc xắc,',
           'sấp thì gieo $2$ xúc xắc. Xác suất',
           'tổng số chấm bằng $6$?']
OPTIONS = ['1/6', '11/72', '5/36']
CORRECT = 1
ANSWER_VALUE = 11 / 72
BRANCHES = [('N', GOLD, '1/2', [('6', GREEN, '1/6', []), ('≠', SOFT, '5/6', [])]),
            ('S', CYAN, '1/2', [('6', GREEN, '5/36', []), ('≠', SOFT, '31/36', [])])]

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu: ngửa thì gieo một con xúc xắc, sấp thì gieo hai con và cộng số chấm. '
                         'Xác suất kết quả cuối cùng bằng sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, mười một phần bảy mươi hai, hay năm phần ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai hành động nối tiếp: đồng xu quyết định cách gieo. Nhánh ngửa: một con xúc xắc ra sáu với xác suất một phần sáu.'),
    Beat('s2', 'solve', 'Nhánh sấp: hai con xúc xắc có tổng sáu ở năm kết quả: một năm, hai bốn, ba ba, bốn hai, năm một, '
                        'nên xác suất là năm phần ba mươi sáu.'),
    Beat('s3', 'solve', 'Toàn phần: một phần hai nhân một phần sáu, cộng một phần hai nhân năm phần ba mươi sáu, '
                        'bằng sáu phần bảy mươi hai cộng năm phần bảy mươi hai, tức mười một phần bảy mươi hai.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần bảy mươi hai. Thử thách tiếp theo: biết kết quả là sáu, đồng xu đã ra mặt nào?'),
    Beat('outro', 'outro', outro_text(134)),
]

FORMULAS = formulas('11/72', OPTIONS,
                    two='(1, 5), (2, 4), (3, 3), (4, 2), (5, 1) arrow.r.double 5/36',
                    hn='1/2 dot 1/6 = 6/72',
                    hs='1/2 dot 5/36 = 5/72',
                    tot='P = 6/72 + 5/72 = 11/72')


def validate() -> bool:
    two = F(sum(a + b == 6 for a, b in product(range(1, 7), repeat=2)), 36)
    assert two == F(5, 36) and F(1, 2) * F(1, 6) + F(1, 2) * two == F(11, 72)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS134(TreeMixin, ShortScene):
    N = 134

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='tung xu')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:6]), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][6:]), run_time=self.rt(.1))
        self.wait_until(.35, t0)
        self.write_board(self.M('two', 1.6))
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('hn', 1.8))
        self.write_board(self.M('hs', 1.8))
        self.wait_until(.6, t0)
        m = self.M('tot', 2.0)
        self.write_board(m)
        self.frame(m)


