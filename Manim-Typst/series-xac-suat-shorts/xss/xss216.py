"""XSS216 · Thêm bi cùng màu — Pólya 2 bước: P(Đ₁ | Đ₂) = (1/2·2/3)/(1/2) = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS216', 'answer': '2/3'}
PROBLEM = ['Hộp $1$ đỏ $1$ xanh. Rút $1$ bi, trả lại',
           'kèm thêm $1$ bi cùng màu; rút lần hai',
           'được đỏ. Xác suất lần một đỏ?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 1
ANSWER_VALUE = 2 / 3
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '1/2', [(*D, '2/3', []), (*X, '1/3', [])]),
            (*X, '1/2', [(*D, '1/3', []), (*X, '2/3', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có một đỏ một xanh. Rút một bi, trả lại và thêm một bi cùng màu. Rút lần hai được đỏ. '
                         'Xác suất lần một cũng rút được đỏ là bao nhiêu? Câu hỏi đi ngược thời gian!'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lần một đỏ: hộp thành hai đỏ một xanh, lần hai đỏ hai phần ba. Lần một xanh: hộp một đỏ hai xanh, lần hai đỏ một phần ba.'),
    Beat('s2', 'solve', 'Hai lá "lần hai đỏ": một phần ba và một phần sáu, tổng một phần hai. Lần hai đỏ vẫn có xác suất một phần hai.'),
    Beat('s3', 'solve', 'Bayes: một phần ba chia một phần hai, bằng hai phần ba. Lần hai đỏ là bằng chứng cho thấy hộp đã được "bơm" thêm đỏ.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Trong bình Pólya, lần rút sau mang thông tin về lần rút trước!'),
    Beat('outro', 'outro', outro_text(216)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    leaves='1/2 dot 2/3 = 1/3, quad 1/2 dot 1/3 = 1/6',
                    prob='P(Đ_1 | Đ_2) = (1/3)/(1/3 + 1/6) = 2/3')


def validate() -> bool:
    a, b = F(1, 2) * F(2, 3), F(1, 2) * F(1, 3)
    assert a + b == F(1, 2) and a / (a + b) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS216(TreeMixin, ShortScene):
    N = 216

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='lần 1')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        red2 = [self.leaves[0][0], self.leaves[2][0]]
        self.play(*[n.animate.scale(1.3) for n in red2], self.leaves[1][0].animate.set_opacity(.15),
                  self.leaves[3][0].animate.set_opacity(.15), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('leaves', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
        self.play(self.leaves[0][0].animate.set_stroke(GREEN, 6), run_time=self.rt(.04))
