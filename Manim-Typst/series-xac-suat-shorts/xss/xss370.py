"""XSS370 · Đúng một ngửa — k từ xúc xắc, tung k xu; P(1 ngửa | k) = k/2^k; Σ = 15/8 (bỏ 1/6); P(k ≤ 2 | 1 ngửa) = 1/(15/8) = 8/15."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS370', 'answer': '8/15'}
PROBLEM = ['Gieo xúc xắc được $k$ rồi tung $k$ đồng xu,',
           'được đúng $1$ mặt ngửa. Xác suất $k <= 2$?']
OPTIONS = ['1/3', '8/15', '2/3']
CORRECT = 1
ANSWER_VALUE = 8 / 15
ONE = {k: F(k, 2 ** k) for k in range(1, 7)}
LEAF = {1: '1/2', 2: '1/2', 3: '3/8', 4: '1/4', 5: '5/32', 6: '3/32'}
BRANCHES = [(str(k), CYAN, '1/6', [('1N', GOLD, LEAF[k], [])]) for k in range(1, 7)]

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc được k, rồi tung k đồng xu. Kết quả có đúng một mặt ngửa. '
                         'Xác suất xúc xắc đã ra một hoặc hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, tám phần mười lăm, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tung k đồng xu, đúng một ngửa có k cách trong hai mũ k: xác suất k phần hai mũ k.'),
    Beat('s2', 'solve', 'Sáu giá trị: một phần hai, một phần hai, ba phần tám, một phần tư, năm phần ba mươi hai, ba phần ba mươi hai. Tổng mười lăm phần tám.'),
    Beat('s3', 'solve', 'Hệ số một phần sáu triệt tiêu trong Bayes. Hai nhánh đầu cộng lại bằng một, nên xác suất bằng một chia mười lăm phần tám, tức tám phần mười lăm.'),
    Beat('answer', 'solve', 'Đáp án: tám phần mười lăm. Ít xu thì dễ có đúng một ngửa, nên bằng chứng nghiêng về k nhỏ.'),
    Beat('outro', 'outro', outro_text(370)),
]

FORMULAS = formulas('8/15', OPTIONS,
                    leaf='P("1 ngửa" | k) = k/2^k',
                    sum='sum_(k=1)^6 k/2^k = 15/8',
                    prob='P(k <= 2 | "1 ngửa") = (1/2 + 1/2)/(15/8) = 8/15')


def validate() -> bool:
    assert all(ONE[k] == F(*map(int, LEAF[k].split('/'))) for k in ONE)
    total = sum(ONE.values())
    assert total == F(15, 8) and (ONE[1] + ONE[2]) / total == F(8, 15)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS370(TreeMixin, ShortScene):
    N = 370

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.4, r=.3, edge_size=22)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('leaf', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.clear_board(.03)
        self.write_board(self.M('sum', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)
