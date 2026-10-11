"""XSS209 · Luân phiên hai hộp — An (2Đ3X), Bình (3Đ1X): P(An) = 2/5 + 3/5·1/4·2/4 = 19/40."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PURPLE, SOFT  # noqa: E402

EPISODE = {'code': 'XSS209', 'answer': '19/40'}
PROBLEM = ['An rút hộp I ($2$ đỏ $3$ xanh), Bình rút hộp',
           'II ($3$ đỏ $1$ xanh), luân phiên, An trước;',
           'ai được đỏ trước thắng. Xác suất An thắng?']
OPTIONS = ['2/5', '19/40', '1/2']
CORRECT = 1
ANSWER_VALUE = 19 / 40
BRANCHES = [('A', GOLD, '2/5', []),
            ('x', SOFT, '3/5', [('B', PURPLE, '3/4', []),
                                ('x', SOFT, '1/4', [('A', GOLD, '2/4', []), ('x', SOFT, '2/4', [('B', PURPLE, '1', [])])])])]


def an_wins():
    win = total = F(0)
    for a in set(permutations('RRBBB')):
        for b in set(permutations('RRRB')):
            pa, pb = F(1, 10), F(1, 4)
            seq = [s for pair in zip(a, b) for s in pair]
            first = next(i for i, c in enumerate(seq) if c == 'R')
            total += pa * pb
            win += pa * pb * (first % 2 == 0)
    return win / total


BEATS = [
    Beat('hook', 'hook', 'An rút từ hộp một có hai đỏ ba xanh, Bình rút từ hộp hai có ba đỏ một xanh. Hai bạn rút luân phiên, không hoàn lại, An trước. '
                         'Ai được bi đỏ trước thì thắng. Xác suất An thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, mười chín phần bốn mươi, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây luân phiên: An đỏ ngay hai phần năm. An xanh ba phần năm, tới Bình: đỏ ba phần tư thì Bình thắng.'),
    Beat('s2', 'solve', 'Bình xanh một phần tư, hộp hai chỉ còn ba đỏ nên lượt sau Bình chắc chắn thắng. Lượt An: hộp một còn hai đỏ hai xanh, đỏ một phần hai.'),
    Beat('s3', 'solve', 'An thắng: hai phần năm cộng ba phần năm nhân một phần tư nhân một phần hai, bằng mười sáu cộng ba phần bốn mươi, tức mười chín phần bốn mươi.'),
    Beat('answer', 'solve', 'Đáp án: mười chín phần bốn mươi. Đi trước chưa chắc có lợi khi hộp của đối thủ tốt hơn!'),
    Beat('outro', 'outro', outro_text(209)),
]

FORMULAS = formulas('19/40', OPTIONS,
                    win='P(A) = 2/5 + 3/5 dot 1/4 dot 2/4 = 19/40')


def validate() -> bool:
    assert an_wins() == F(19, 40) == F(2, 5) + F(3, 5) * F(1, 4) * F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS209(TreeMixin, ShortScene):
    N = 209

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.05, width=6.4, root_label='An rút',
                                                  r=.34, edge_size=26)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[4], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(self.TM('A: An thắng   B: Bình thắng   x: xanh', 20, SOFT).move_to([0, -1.35, 0])), run_time=self.rt(.04))

    def beat_s3(self, T):
        wins = [n for n, path in self.leaves if path[-1][0] == 'A']
        self.play(*[n.animate.scale(1.3) for n in wins], run_time=self.rt(.05))
        m = self.M('win', 1.8)
        self.write_board(m)
        self.frame(m)


