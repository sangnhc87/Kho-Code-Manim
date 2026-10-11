"""XSS080 · Rút thăm trước hay sau? — 3 người, 1 thăm trúng: người thứ ba 2/3 · 1/2 · 1 = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS080', 'answer': '1/3'}
PROBLEM = ['$3$ người lần lượt rút $3$ lá thăm, chỉ $1$ lá trúng thưởng.', 'Xác suất người rút THỨ BA trúng?']
OPTIONS = ['1/2', '1/3', '2/3']
CORRECT = 1
ANSWER_VALUE = 1 / 3
GRAY = '#5E6E86'
BRANCHES = [('1', GOLD, '1/3', []),
            ('·', GRAY, '2/3', [('2', GOLD, '1/2', []), ('·', GRAY, '1/2', [('3', GOLD, '1', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Ba người bốc thăm lần lượt, chỉ một lá trúng thưởng. Ai cũng muốn bốc trước, '
                         'vì nghĩ bốc sau thì lá trúng đã bị lấy mất. Người bốc thứ ba có thiệt không?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Người thứ ba trúng khi hai người đầu đều trượt. Người một trượt với xác suất hai phần ba.'),
    Beat('s2', 'solve', 'Biết người một trượt, còn hai lá, người hai trượt với xác suất một phần hai. '
                        'Lá cuối cùng chắc chắn là lá trúng: người ba trúng với xác suất bằng một.'),
    Beat('s3', 'solve', 'Nhân dọc nhánh: hai phần ba nhân một phần hai nhân một, bằng một phần ba. '
                        'Đúng bằng cơ hội của người bốc đầu tiên! Bốc trước hay sau đều công bằng.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Bốc thăm là công bằng, miễn là không ai được xem kết quả của người trước.'),
    Beat('outro', 'outro', outro_text(80)),
]

FORMULAS = formulas('1/3', OPTIONS, prob='P = 2/3 dot 1/2 dot 1 = 1/3')


def validate() -> bool:
    perms = list(permutations((1, 0, 0)))
    assert all(F(sum(p[i] for p in perms), len(perms)) == F(1, 3) for i in range(3))
    assert F(2, 3) * F(1, 2) * 1 == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS080(TreeMixin, ShortScene):
    N = 80

    def hook_visual(self, t0):
        self.board_top = -1.05
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.3), dy=1.25, width=5.6, root_label='bốc thăm', r=.33)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('số: người trúng   ·: trượt', 22, SOFT).move_to([0, -.55, 0])), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[3]), run_time=self.rt(.1))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('bằng người bốc đầu tiên!', 30, GOLD, bold=True), anim='fade')
