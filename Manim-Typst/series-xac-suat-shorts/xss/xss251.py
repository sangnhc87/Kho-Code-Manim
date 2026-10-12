"""XSS251 · Tìm xác suất bắn trúng — (1 − p)² = 0,04 ⇒ p = 0,8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402

EPISODE = {'code': 'XSS251', 'answer': 'p = 0,8'}
PROBLEM = ['Bắn $2$ phát độc lập, xác suất trúng',
           'ít nhất $1$ phát là $"0,96"$. Tìm xác suất',
           'trúng $p$ của mỗi phát.']
OPTIONS = ['p = "0,48"', 'p = "0,8"', 'p = "0,98"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('T', GREEN, 'p', []), ('X', CORAL, '1 - p', [('T', GREEN, 'p', []), ('X', CORAL, '1 - p', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ bắn hai phát độc lập, xác suất trúng ít nhất một phát là không phẩy chín sáu. '
                         'Xác suất trúng của mỗi phát là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bốn tám, không phẩy tám, hay không phẩy chín tám? Ba, hai, một!'),
    Beat('s1', 'solve', '"Ít nhất một" thì đi phần bù: trượt cả hai phát có xác suất một trừ p, bình phương. Một trừ cái đó bằng không phẩy chín sáu.'),
    Beat('s2', 'solve', 'Vậy một trừ p bình phương bằng không phẩy không bốn, nên một trừ p bằng không phẩy hai, vì một trừ p không âm.'),
    Beat('s3', 'solve', 'p bằng không phẩy tám. Không phẩy bốn tám là bẫy: chia đôi không phẩy chín sáu như thể hai phát cộng lại.'),
    Beat('answer', 'solve', 'Đáp án: p bằng không phẩy tám. Bài ngược với "ít nhất một": viết phần bù, khai căn!'),
    Beat('outro', 'outro', outro_text(251)),
]

FORMULAS = formulas('p = "0,8"', OPTIONS,
                    eq='1 - (1 - p)^2 = "0,96"',
                    sol='(1 - p)^2 = "0,04" arrow.r.double 1 - p = "0,2" arrow.r.double p = "0,8"')


def validate() -> bool:
    assert [F(k, 100) for k in range(101) if 1 - (1 - F(k, 100)) ** 2 == F(96, 100)] == [F(4, 5)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS251(TreeMixin, ShortScene):
    N = 251

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.6, width=5.6, root_label='phát 1')
        self.wait_until(.7, t0)
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[-1][0].animate.scale(1.35), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        m = self.M('eq', 2.0)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s2(self, T):
        m = self.M('sol', 1.4)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('$"0,96" div 2 = "0,48"$: sai!', 28, CORAL, bold=True), anim='fade')
