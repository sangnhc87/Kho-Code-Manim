"""XSS377 · Dừng trong ba lần — gieo đến khi ra 6; P(T = k) = (5/6)^(k−1)/6: 36, 30, 25 (/216); P(T = 2 | T ≤ 3) = 30/91."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS377', 'answer': '30/91'}
PROBLEM = ['Gieo xúc xắc đến khi ra $6$. Biết số lần',
           'gieo không quá $3$. Xác suất gieo đúng',
           '$2$ lần?']
OPTIONS = ['1/3', '30/91', '5/18']
CORRECT = 1
ANSWER_VALUE = 30 / 91
G = {k: F(5, 6) ** (k - 1) * F(1, 6) for k in range(1, 4)}
BRANCHES = [('6', GOLD, '1/6', []),
            ('≠6', SOFT, '5/6', [('6', GOLD, '1/6', []),
                                ('≠6', SOFT, '5/6', [('6', GOLD, '1/6', []), ('...', SOFT, '5/6', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc liên tục cho đến khi ra mặt sáu thì dừng. Biết số lần gieo không quá ba. '
                         'Xác suất đã gieo đúng hai lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, ba mươi phần chín mươi mốt, hay năm phần mười tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây dừng: mỗi tầng hoặc ra sáu với một phần sáu, hoặc đi tiếp với năm phần sáu. Dừng ở lần k có xác suất năm phần sáu mũ k trừ một nhân một phần sáu.'),
    Beat('s2', 'solve', 'Với k bằng một, hai, ba: ba mươi sáu, ba mươi, hai mươi lăm phần hai trăm mười sáu. Tổng chín mươi mốt phần hai trăm mười sáu.'),
    Beat('s3', 'solve', 'Xác suất dừng ở lần hai, biết không quá ba: ba mươi chia chín mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi phần chín mươi mốt. Điều kiện cắt cây dừng ở tầng ba, rồi so tỉ lệ các lá còn lại.'),
    Beat('outro', 'outro', outro_text(377)),
]

FORMULAS = formulas('30/91', OPTIONS,
                    gk='P(T = k) = (5/6)^(k-1) dot 1/6',
                    vals='36/216, quad 30/216, quad 25/216',
                    prob='P(T = 2 | T <= 3) = 30/(36 + 30 + 25) = 30/91')


def validate() -> bool:
    assert G[2] / sum(G.values()) == F(30, 91)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS377(TreeMixin, ShortScene):
    N = 377

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.15, width=5.4, r=.32, edge_size=24)
        self.wait_until(.65, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2]), FadeIn(self.levels[3]), run_time=self.rt(.12))
        self.wait_until(.55, t0)
        self.write_board(self.M('gk', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.clear_board(.03)
        self.write_board(self.M('vals', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
