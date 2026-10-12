"""XSS247 · Chọn n rồi chọn m — n đều trên 1..4, m đều trên 1..n: P(m = 1) = 1/4(1 + 1/2 + 1/3 + 1/4) = 25/48."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS247', 'answer': '25/48'}
PROBLEM = ['Chọn ngẫu nhiên $n$ từ $1$ đến $4$, rồi chọn',
           'ngẫu nhiên $m$ từ $1$ đến $n$. Xác suất $m = 1$?']
OPTIONS = ['1/4', '25/48', '1/2']
CORRECT = 1
ANSWER_VALUE = 25 / 48
BRANCHES = [(str(n), CYAN, '1/4', [('1', GOLD, f'1/{n}', [])]) for n in range(1, 5)]

BEATS = [
    Beat('hook', 'hook', 'Hai bước chọn ngẫu nhiên: chọn n từ một đến bốn, rồi chọn m từ một đến n. '
                         'Xác suất m bằng một là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, hai mươi lăm phần bốn mươi tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước hai phụ thuộc bước một: n càng nhỏ, m càng dễ bằng một. n bằng một thì m chắc chắn bằng một; n bằng bốn thì chỉ một phần tư.'),
    Beat('s2', 'solve', 'Công thức toàn phần: một phần tư nhân tổng một, một phần hai, một phần ba, một phần tư.'),
    Beat('s3', 'solve', 'Tổng trong ngoặc là hai mươi lăm phần mười hai, nhân một phần tư được hai mươi lăm phần bốn mươi tám, hơn một nửa!'),
    Beat('answer', 'solve', 'Đáp án: hai mươi lăm phần bốn mươi tám. Thử thách tiếp: biết m bằng một, n đã bằng mấy?'),
    Beat('outro', 'outro', outro_text(247)),
]

FORMULAS = formulas('25/48', OPTIONS,
                    tot='P(m = 1) = 1/4 (1 + 1/2 + 1/3 + 1/4) = 1/4 dot 25/12 = 25/48')


def validate() -> bool:
    assert sum(F(1, 4) * F(1, n) for n in range(1, 5)) == F(25, 48)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS247(TreeMixin, ShortScene):
    N = 247

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='chọn n')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.05))

    def beat_s3(self, T):
        m = self.M('tot', 1.5)
        self.write_board(m)
        self.frame(m)
