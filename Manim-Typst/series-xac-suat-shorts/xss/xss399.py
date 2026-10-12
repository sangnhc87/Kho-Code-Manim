"""XSS399 · Thắng hai ván liên tiếp — trạng thái a (A vừa thắng), b (B vừa thắng): x_a = 0,6 + 0,4x_b, x_b = 0,6x_a → x_a = 15/19, x_b = 9/19; x₀ = 63/95."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS399', 'answer': '63/95'}
PROBLEM = ['Ai thắng $2$ ván liên tiếp trước thì vô',
           'địch; A thắng mỗi ván với xác suất $"0,6"$.',
           'Xác suất A vô địch?']
OPTIONS = ['63/95', '3/5', '9/13']
CORRECT = 0
ANSWER_VALUE = 63 / 95
P = F(3, 5)
BRANCHES = [('A', CYAN, '"0,6"', [('A', CYAN, '"0,6"', []), ('B', CORAL, '"0,4"', [])]),
            ('B', CORAL, '"0,4"', [('A', CYAN, '"0,6"', []), ('B', CORAL, '"0,4"', [])])]


def solve():
    q = 1 - P
    xa = P / (1 - q * P)
    xb = P * xa
    return xa, xb, P * xa + q * xb


BEATS = [
    Beat('hook', 'hook', 'Hai kỳ thủ thi đấu, ai thắng hai ván liên tiếp trước thì vô địch. A thắng mỗi ván với xác suất không phẩy sáu. '
                         'Xác suất A vô địch là bao nhiêu?'),
    Beat('guess', 'hook', 'Sáu mươi ba phần chín mươi lăm, ba phần năm, hay chín phần mười ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây có thể dài vô hạn, nhưng chỉ cần nhớ ai thắng ván gần nhất. Gọi x a là xác suất A vô địch khi A vừa thắng, x b khi B vừa thắng.'),
    Beat('s2', 'solve', 'Khi A vừa thắng: thắng tiếp là vô địch, thua thì sang trạng thái b. Khi B vừa thắng: A phải thắng để sang a, thua là hết.'),
    Beat('s3', 'solve', 'Giải hệ: x a bằng mười lăm phần mười chín, x b bằng chín phần mười chín. Từ đầu: không phẩy sáu x a cộng không phẩy bốn x b, bằng sáu mươi ba phần chín mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: sáu mươi ba phần chín mươi lăm, khoảng sáu mươi sáu phần trăm. Luật hai ván liên tiếp khuếch đại lợi thế của người mạnh hơn.'),
    Beat('outro', 'outro', outro_text(399)),
]

FORMULAS = formulas('63/95', OPTIONS,
                    sys='x_a = "0,6" + "0,4" x_b, quad x_b = "0,6" x_a',
                    sol='x_a = 15/19, quad x_b = 9/19',
                    prob='P = "0,6" dot 15/19 + "0,4" dot 9/19 = 63/95')


def validate() -> bool:
    xa, xb, x0 = solve()
    assert (xa, xb, x0) == (F(15, 19), F(9, 19), F(63, 95))
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS399(TreeMixin, ShortScene):
    N = 399

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.6, width=6.0, r=.4, edge_size=26)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.05))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('sys', 1.3))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('sol', 1.4))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)
