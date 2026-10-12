"""XSS402 · Kéo dài không đổi cuộc chơi — mỗi lượt thắng 2/6, thua 1/6, gieo lại 3/6; biết kéo dài ≥ 3 lượt (2 lượt đầu gieo lại), không trí nhớ → P(thắng) = (2/6)/(3/6) = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS402', 'answer': '2/3'}
PROBLEM = ['Gieo xúc xắc: $1, 2$ thắng; $3$ thua;',
           '$4, 5, 6$ gieo lại. Biết trò chơi kéo dài',
           'ít nhất $3$ lượt. Xác suất thắng?']
OPTIONS = ['2/3', '1/3', '1/2']
CORRECT = 0
ANSWER_VALUE = 2 / 3
W, L, A = F(2, 6), F(1, 6), F(3, 6)
BRANCHES = [('T', GREEN, '2/6', []), ('Th', CORAL, '1/6', []), ('lại', SOFT, '3/6', [])]

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc: ra một hoặc hai thì thắng, ra ba thì thua, ra bốn, năm, sáu thì gieo lại. Biết trò chơi kéo dài ít nhất ba lượt. '
                         'Xác suất thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần ba, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Kéo dài ít nhất ba lượt nghĩa là hai lượt đầu đều phải gieo lại. Từ lượt ba, trò chơi y hệt như lúc mới bắt đầu.'),
    Beat('s2', 'solve', 'Vậy chỉ cần xác suất thắng của trò chơi gốc. Mỗi lượt, bỏ qua các lần gieo lại, chỉ so thắng và thua: hai phần sáu so với một phần sáu.'),
    Beat('s3', 'solve', 'Xác suất thắng bằng hai phần sáu chia ba phần sáu, tức hai phần ba, không phụ thuộc điều kiện kéo dài.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Cây lặp lại chính nó: điều kiện về quá khứ không đổi tương lai.'),
    Beat('outro', 'outro', outro_text(402)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    prob='P("thắng") = (2/6)/(2/6 + 1/6) = 2/3')


def validate() -> bool:
    approx = sum(A ** k * W for k in range(2, 200)) / A ** 2
    assert W / (W + L) == F(2, 3) and abs(float(approx) - 2 / 3) < 1e-12
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS402(TreeMixin, ShortScene):
    N = 402

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.6), dy=1.8, width=5.6, r=.42, edge_size=28)
        self.wait_until(.7, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.leaves[2][0].animate.scale(1.25), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.leaves[2][0].animate.set_opacity(.3), run_time=self.rt(.05))

    def beat_s3(self, T):
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
