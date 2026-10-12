"""XSS256 · Tìm tay nghề xạ thủ — 0,2p + 0,8(1 − p) = 0,38 ⇒ p = 0,7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS256', 'answer': 'p = 0,7'}
PROBLEM = ['Hai xạ thủ trúng với xác suất',
           '$p$ và $"0,8"$. Xác suất có đúng $1$ người',
           'trúng là $"0,38"$. Tìm $p$.']
OPTIONS = ['p = "0,6"', 'p = "0,7"', 'p = "0,9"']
CORRECT = 1
ANSWER_VALUE = None
T, X = ('T', GREEN), ('X', CORAL)
BRANCHES = [(*T, 'p', [(*T, '"0,8"', []), (*X, '"0,2"', [])]),
            (*X, '1 - p', [(*T, '"0,8"', []), (*X, '"0,2"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hai xạ thủ: người thứ nhất trúng với xác suất p chưa biết, người thứ hai trúng không phẩy tám. '
                         'Xác suất có đúng một người trúng là không phẩy ba tám. Tìm p.'),
    Beat('guess', 'hook', 'Không phẩy sáu, không phẩy bảy, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đúng một người trúng có hai lá: người một trúng người hai trượt, p nhân không phẩy hai; người một trượt người hai trúng, một trừ p nhân không phẩy tám.'),
    Beat('s2', 'solve', 'Phương trình: không phẩy hai p cộng không phẩy tám trừ không phẩy tám p bằng không phẩy ba tám. '
                        'Không phẩy tám trừ không phẩy sáu p bằng không phẩy ba tám.'),
    Beat('s3', 'solve', 'Không phẩy sáu p bằng không phẩy bốn hai, p bằng không phẩy bảy. Kiểm tra: không phẩy một bốn cộng không phẩy hai bốn bằng không phẩy ba tám.'),
    Beat('answer', 'solve', 'Đáp án: p bằng không phẩy bảy. Mỗi lá chứa ẩn là một hạng tử của phương trình!'),
    Beat('outro', 'outro', outro_text(256)),
]

FORMULAS = formulas('p = "0,7"', OPTIONS,
                    eq='"0,2" p + "0,8" (1 - p) = "0,38"',
                    sol='"0,6" p = "0,42" arrow.r.double p = "0,7"')


def validate() -> bool:
    assert [F(k, 100) for k in range(101) if F(k, 100) * F(2, 10) + (1 - F(k, 100)) * F(8, 10) == F(38, 100)] == [F(7, 10)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS256(TreeMixin, ShortScene):
    N = 256

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='xạ thủ 1')
        self.wait_until(.75, t0)
        self.play(*[FadeIn(lv, lag_ratio=.2) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        self.play(self.leaves[1][0].animate.scale(1.3), self.leaves[2][0].animate.scale(1.3),
                  self.leaves[0][0].animate.set_opacity(.15), self.leaves[3][0].animate.set_opacity(.15), run_time=self.rt(.06))

    def beat_s2(self, T):
        m = self.M('eq', 1.8)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 1.8)
        self.write_board(m)
        self.frame(m)
