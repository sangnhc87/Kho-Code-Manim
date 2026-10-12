"""XSS368 · Đỏ gieo xúc xắc, xanh tung xu — 2đ2x: đỏ → xúc xắc ra 6 (1/6), xanh → xu ngửa (1/2); P(đỏ | thắng) = (1/12)/(1/12 + 1/4) = 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS368', 'answer': '1/4'}
PROBLEM = ['Rút $1$ bi từ hộp $2$ đỏ $2$ xanh: đỏ thì',
           'gieo xúc xắc, xanh thì tung xu; ra $6$',
           'hoặc ngửa là thắng. Biết đã thắng.',
           'Xác suất đã rút bi đỏ?']
OPTIONS = ['1/4', '1/2', '1/3']
CORRECT = 0
ANSWER_VALUE = .25
BRANCHES = [('Đ', CORAL, '1/2', [('T', GREEN, '1/6', [])]), ('X', CYAN, '1/2', [('T', GREEN, '1/2', [])])]
WIN_R, WIN_B = F(1, 2) * F(1, 6), F(1, 2) * F(1, 2)

BEATS = [
    Beat('hook', 'hook', 'Rút một bi từ hộp hai đỏ hai xanh. Đỏ thì gieo xúc xắc, ra sáu là thắng. Xanh thì tung đồng xu, ngửa là thắng. '
                         'Biết bạn đã thắng. Xác suất bạn đã rút bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần hai, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai nhánh đều một phần hai. Nhánh đỏ thắng với xác suất một phần sáu, nhánh xanh thắng với một phần hai.'),
    Beat('s2', 'solve', 'Lá thắng qua đỏ: một phần mười hai. Lá thắng qua xanh: một phần tư, tức ba phần mười hai.'),
    Beat('s3', 'solve', 'Bayes: một chia một cộng ba, bằng một phần tư. Thắng là dấu hiệu bạn đã chơi trò dễ hơn.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Mỗi nhánh một trò chơi khác nhau, Bayes so sánh độ dễ của chúng.'),
    Beat('outro', 'outro', outro_text(368)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    leafs='1/2 dot 1/6 = 1/12, quad 1/2 dot 1/2 = 3/12',
                    prob='P(Đ | T) = 1/(1 + 3) = 1/4')


def validate() -> bool:
    assert WIN_R / (WIN_R + WIN_B) == F(1, 4)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS368(TreeMixin, ShortScene):
    N = 368

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.4)
        self.wait_until(.65, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('leafs', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
