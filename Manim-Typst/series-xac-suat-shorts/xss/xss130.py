"""XSS130 · Xúc xắc chọn hộp — cây 3 nhánh không đều: 1/3·1/2 + 1/2·2/3 + 1/6·1 = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS130', 'answer': '2/3'}
PROBLEM = ['Xúc xắc ra $1, 2$: hộp A ($1$ đỏ $1$ xanh);',
           '$3, 4, 5$: hộp B ($2$ đỏ $1$ xanh); $6$: hộp C',
           '($3$ đỏ). Rút $1$ bi. Xác suất được đỏ?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 1
ANSWER_VALUE = 2 / 3
BRANCHES = [('A', CYAN, '1/3', [('Đ', CORAL, '1/2', []), ('X', CYAN, '1/2', [])]),
            ('B', PURPLE, '1/2', [('Đ', CORAL, '2/3', []), ('X', CYAN, '1/3', [])]),
            ('C', GOLD, '1/6', [('Đ', CORAL, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc để chọn hộp: ra một hoặc hai chọn hộp A, ra ba, bốn, năm chọn hộp B, ra sáu chọn hộp C. '
                         'Rồi rút một bi từ hộp đã chọn. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một có ba nhánh không đều: hộp A một phần ba, hộp B một phần hai, hộp C một phần sáu. '
                        'Tầng hai là xác suất rút được đỏ trong từng hộp.'),
    Beat('s2', 'solve', 'Nhánh A đỏ: một phần ba nhân một phần hai. Nhánh B đỏ: một phần hai nhân hai phần ba. '
                        'Nhánh C đỏ: một phần sáu nhân một.'),
    Beat('s3', 'solve', 'Cộng ba nhánh: một phần sáu cộng một phần ba cộng một phần sáu, bằng hai phần ba. '
                        'Đây là công thức xác suất toàn phần với ba giả thuyết.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Mỗi giả thuyết một nhánh, nhân dọc rồi cộng ngang!'),
    Beat('outro', 'outro', outro_text(130)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    tot='P = 1/3 dot 1/2 + 1/2 dot 2/3 + 1/6 dot 1',
                    val='P = 1/6 + 1/3 + 1/6 = 2/3')


def validate() -> bool:
    assert F(1, 3) * F(1, 2) + F(1, 2) * F(2, 3) + F(1, 6) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS130(TreeMixin, ShortScene):
    N = 130

    def hook_visual(self, t0):
        self.board_top = -1.55
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=7.0, root_label='xúc xắc')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.18))

    def beat_s2(self, T):
        t0 = self.now()
        reds = [n for n, path in self.leaves if path[-1][0] == 'Đ']
        for i, n in enumerate(reds):
            self.wait_until(.15 + .25 * i, t0)
            self.play(n.animate.scale(1.3).set_stroke(GREEN, 5), run_time=self.rt(.05))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('tot', 1.8))
        self.wait_until(.45, t0)
        m = self.M('val', 2.1)
        self.write_board(m)
        self.frame(m)
