"""XSS374 · Một hay hai xúc xắc? — 1đ2x: đỏ → 2 xúc xắc tổng 4 (1/12), xanh → 1 xúc xắc ra 4 (1/6); P(đỏ | 4) = (1/36)/(1/36 + 4/36) = 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS374', 'answer': '1/5'}
PROBLEM = ['Rút $1$ bi ($1$ đỏ $2$ xanh): đỏ thì gieo',
           '$2$ xúc xắc, xanh thì gieo $1$. Số chấm',
           '(tổng) bằng $4$. Xác suất đã rút bi đỏ?']
OPTIONS = ['1/3', '1/5', '1/4']
CORRECT = 1
ANSWER_VALUE = .2
SUM4 = F(sum(a + b == 4 for a in range(1, 7) for b in range(1, 7)), 36)
BRANCHES = [('Đ', CORAL, '1/3', [('4', GOLD, '1/12', [])]), ('X', CYAN, '2/3', [('4', GOLD, '1/6', [])])]

BEATS = [
    Beat('hook', 'hook', 'Rút một bi từ hộp một đỏ hai xanh. Đỏ thì gieo hai xúc xắc và tính tổng; xanh thì gieo một xúc xắc. Kết quả bằng bốn. '
                         'Xác suất đã rút bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần năm, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh đỏ: hai xúc xắc có tổng bốn ở ba cặp, một ba, hai hai, ba một: xác suất ba phần ba mươi sáu, bằng một phần mười hai.'),
    Beat('s2', 'solve', 'Nhánh xanh: một xúc xắc ra bốn với xác suất một phần sáu.'),
    Beat('s3', 'solve', 'Hai lá: một phần ba nhân một phần mười hai bằng một phần ba mươi sáu; hai phần ba nhân một phần sáu bằng bốn phần ba mươi sáu. Bayes: một phần năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Nhánh đỏ vừa hiếm vừa khó ra bốn, nên càng ít khả năng.'),
    Beat('outro', 'outro', outro_text(374)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    sum4='P("tổng" 4) = 3/36 = 1/12',
                    leafs='1/3 dot 1/12 = 1/36, quad 2/3 dot 1/6 = 4/36',
                    prob='P(Đ | 4) = 1/(1 + 4) = 1/5')


def validate() -> bool:
    a, b = F(1, 3) * SUM4, F(2, 3) * F(1, 6)
    assert SUM4 == F(1, 12) and a / (a + b) == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS374(TreeMixin, ShortScene):
    N = 374

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.4)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('sum4', 1.5))

    def beat_s2(self, T):
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('leafs', 1.3))
        self.wait_until(.6, t0)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
