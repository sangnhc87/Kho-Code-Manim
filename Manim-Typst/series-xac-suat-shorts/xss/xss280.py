"""XSS280 · Ba người, ba cơ hội — A ra 1 (1/6), B ra ≤ 2 (1/3), C ra ≤ 3 (1/2): P(A) = (1/6)/(1 − 5/6·4/6·3/6) = 3/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS280', 'answer': '3/13'}
PROBLEM = ['A, B, C lần lượt gieo xúc xắc. A thắng',
           'nếu ra $1$; B thắng nếu ra $1, 2$; C thắng',
           'nếu ra $1, 2, 3$. Lặp lại đến khi có',
           'người thắng. $P(A)$?']
OPTIONS = ['1/6', '3/13', '1/3']
CORRECT = 1
ANSWER_VALUE = 3 / 13
BRANCHES = [('A', CYAN, '1/6', []),
            ('·', SOFT, '5/6', [('B', GOLD, '2/6', []),
                                ('·', SOFT, '4/6', [('C', CORAL, '3/6', []), ('↺', SOFT, '3/6', [])])])]
ROUND = F(5, 6) * F(4, 6) * F(3, 6)


def wins():
    a = F(1, 6) / (1 - ROUND)
    b = F(5, 6) * F(2, 6) / (1 - ROUND)
    c = F(5, 6) * F(4, 6) * F(3, 6) / (1 - ROUND)
    return a, b, c


BEATS = [
    Beat('hook', 'hook', 'Thử thách cuối nhánh ba: A, B, C lần lượt gieo xúc xắc. A đi trước nhưng chỉ thắng khi ra một. B thắng khi ra một hoặc hai, '
                         'C thắng khi ra một, hai hoặc ba. Vòng lặp đến khi có người thắng. Xác suất A thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, ba phần mười ba, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một vòng chơi là một cây ba tầng: A thắng một phần sáu; nếu không, B thắng hai phần sáu; nếu không, C thắng ba phần sáu.'),
    Beat('s2', 'solve', 'Cả ba cùng trượt trong một vòng: năm phần sáu nhân bốn phần sáu nhân ba phần sáu, bằng năm phần mười tám. Khi đó cây lặp lại.'),
    Beat('s3', 'solve', 'A thắng: một phần sáu chia một trừ năm phần mười tám, bằng ba phần mười ba. Tương tự B được năm phần mười ba, C được năm phần mười ba. '
                        'Đi trước không bù được cơ hội nhỏ!'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười ba. Cảm ơn bạn đã đi hết nhánh ba: bốc bi, chuyển bi, đa điều kiện, tham số và cây lạ!'),
    Beat('outro', 'outro', outro_text(280)),
]

FORMULAS = formulas('3/13', OPTIONS,
                    loop='P("cả ba trượt") = 5/6 dot 4/6 dot 3/6 = 5/18',
                    prob='P(A) = (1/6)/(1 - 5/18) = 3/13',
                    all='P(A) : P(B) : P(C) = 3 : 5 : 5')


def validate() -> bool:
    a, b, c = wins()
    assert (a, b, c) == (F(3, 13), F(5, 13), F(5, 13)) and a + b + c == 1
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS280(TreeMixin, ShortScene):
    N = 280

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.85), dy=1.1, width=6.0, root_label='một vòng', r=.36,
                                                  edge_size=26)
        self.wait_until(.85, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        t0 = self.now()
        for i in range(1, 4):
            self.wait_until(.1 + .25 * (i - 1), t0)
            self.play(FadeIn(self.levels[i], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s2(self, T):
        self.play(self.leaves[-1][0].animate.scale(1.3).set_stroke(GOLD, 4), run_time=self.rt(.05))
        self.write_board(self.M('loop', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('all', 1.8), anim='fade')
