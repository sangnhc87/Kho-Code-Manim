"""XSS401 · Hộp hai bi bí ẩn — số đỏ k ∈ {0; 1; 2} với 1/4, 1/2, 1/4; 3 lần đỏ có hoàn lại: (k/2)³ = 0, 1/8, 1 → P(k = 2) = (1/4)/(1/4 + 1/16) = 4/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS401', 'answer': '4/5'}
PROBLEM = ['Hộp $2$ bi, mỗi bi đỏ hoặc xanh ($1/2$), độc',
           'lập. Rút có hoàn lại $3$ lần đều đỏ. Xác',
           'suất cả $2$ bi trong hộp đều đỏ?']
OPTIONS = ['4/5', '1/4', '8/9']
CORRECT = 0
ANSWER_VALUE = .8
PRI = {0: F(1, 4), 1: F(1, 2), 2: F(1, 4)}
LIK = {k: F(k, 2) ** 3 for k in PRI}
BRANCHES = [('XX', CYAN, '1/4', [('ĐĐĐ', CORAL, '0', [])]),
            ('ĐX', PURPLE, '1/2', [('ĐĐĐ', CORAL, '1/8', [])]),
            ('ĐĐ', CORAL, '1/4', [('ĐĐĐ', CORAL, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một hộp kín có hai bi, mỗi bi đỏ hoặc xanh với xác suất một phần hai, độc lập. Rút có hoàn lại ba lần, cả ba lần đều đỏ. '
                         'Xác suất cả hai bi trong hộp đều đỏ?'),
    Beat('guess', 'hook', 'Bốn phần năm, một phần tư, hay tám phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hộp có không, một hoặc hai bi đỏ với xác suất một phần tư, một phần hai, một phần tư. Nhớ là một đỏ một xanh có hai cách, nên chiếm một nửa.'),
    Beat('s2', 'solve', 'Ba lần đỏ có hoàn lại: hộp không đỏ thì không thể; một đỏ thì một phần hai mũ ba, một phần tám; hai đỏ thì chắc chắn.'),
    Beat('s3', 'solve', 'Hai lá: một phần hai nhân một phần tám bằng một phần mười sáu, và một phần tư nhân một bằng bốn phần mười sáu. Bayes: bốn phần năm.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần năm. Tiên nghiệm sinh ra từ một quá trình ngẫu nhiên khác, cây hai tầng gom tất cả.'),
    Beat('outro', 'outro', outro_text(401)),
]

FORMULAS = formulas('4/5', OPTIONS,
                    lik='P("3 đỏ" | k) = (k/2)^3: quad 0, 1/8, 1',
                    prob='P(k = 2 | "3 đỏ") = (1/4)/(1/2 dot 1/8 + 1/4) = 4/5')


def validate() -> bool:
    tot = sum(PRI[k] * LIK[k] for k in PRI)
    assert PRI[2] * LIK[2] / tot == F(4, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS401(TreeMixin, ShortScene):
    N = 401

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.7, width=6.2, r=.42, edge_size=28)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('lik', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
