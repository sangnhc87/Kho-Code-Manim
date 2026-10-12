"""XSS372 · Biết m = 3 — n từ xúc xắc, m đều trên 1..n; P(m = 3 | n) = 1/n (n ≥ 3); P(n = 6 | m = 3) = (1/6)/(1/3 + 1/4 + 1/5 + 1/6) = 10/57."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS372', 'answer': '10/57'}
PROBLEM = ['Gieo xúc xắc được $n$, rồi chọn ngẫu nhiên',
           'số $m$ từ $1$ đến $n$. Biết $m = 3$. Xác suất',
           '$n = 6$?']
OPTIONS = ['1/4', '10/57', '1/6']
CORRECT = 1
ANSWER_VALUE = 10 / 57
LEAF = {1: '0', 2: '0', 3: '1/3', 4: '1/4', 5: '1/5', 6: '1/6'}
BRANCHES = [(str(n), CYAN, '1/6', [('3', GOLD, LEAF[n], [])]) for n in range(1, 7)]
LIK = {n: (F(1, n) if n >= 3 else F(0)) for n in range(1, 7)}

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc được n, rồi chọn ngẫu nhiên một số m từ một đến n. Biết m bằng ba. '
                         'Xác suất xúc xắc đã ra sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, mười phần năm mươi bảy, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'n bằng một hoặc hai thì không thể chọn được ba. Với n từ ba đến sáu, xác suất chọn đúng ba là một phần n.'),
    Beat('s2', 'solve', 'Bỏ hệ số một phần sáu chung. Tổng khả năng: một phần ba cộng một phần tư cộng một phần năm cộng một phần sáu, bằng năm mươi bảy phần sáu mươi.'),
    Beat('s3', 'solve', 'Nhánh n bằng sáu đóng góp một phần sáu, tức mười phần sáu mươi. Xác suất mười phần năm mươi bảy.'),
    Beat('answer', 'solve', 'Đáp án: mười phần năm mươi bảy. Biết m bằng ba, n lớn lại kém khả năng hơn, vì có nhiều lựa chọn khác.'),
    Beat('outro', 'outro', outro_text(372)),
]

FORMULAS = formulas('10/57', OPTIONS,
                    lik='P(m = 3 | n) = 1/n quad (n >= 3)',
                    sum='1/3 + 1/4 + 1/5 + 1/6 = 57/60',
                    prob='P(n = 6 | m = 3) = (1/6)/(57/60) = 10/57')


def validate() -> bool:
    total = sum(LIK.values())
    assert total == F(57, 60) and LIK[6] / total == F(10, 57)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS372(TreeMixin, ShortScene):
    N = 372

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.4, r=.3, edge_size=24)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.write_board(self.M('lik', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.clear_board(.03)
        self.write_board(self.M('sum', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
