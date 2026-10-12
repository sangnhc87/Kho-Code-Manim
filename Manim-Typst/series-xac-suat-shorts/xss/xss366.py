"""XSS366 · Xúc xắc pha màu hộp — hộp k đỏ 6 − k xanh; P(đỏ) = Σ k/36 = 7/12; P(k = 6 | đỏ) = (1/6)/(7/12) = 2/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, SurroundingRectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS366', 'answer': '2/7'}
PROBLEM = ['Gieo xúc xắc được $k$; hộp có $k$ bi đỏ và',
           '$6 - k$ bi xanh. Rút $1$ bi được đỏ. Xác',
           'suất $k = 6$?']
OPTIONS = ['1/6', '2/7', '1/3']
CORRECT = 1
ANSWER_VALUE = 2 / 7
BRANCHES = [(str(k), CYAN, '1/6', [('Đ', CORAL, f'{k}/6' if k < 6 else '1', [])]) for k in range(1, 7)]
RED = sum(F(1, 6) * F(k, 6) for k in range(1, 7))

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc được k, rồi pha một hộp gồm k bi đỏ và sáu trừ k bi xanh. Rút một bi, được bi đỏ. '
                         'Xác suất xúc xắc đã ra sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, hai phần bảy, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây sáu nhánh, mỗi nhánh một phần sáu. Nhánh k rút được đỏ với xác suất k phần sáu.'),
    Beat('s2', 'solve', 'Xác suất được đỏ: một phần ba mươi sáu nhân tổng một đến sáu, tức hai mươi mốt phần ba mươi sáu, bằng bảy phần mười hai.'),
    Beat('s3', 'solve', 'Nhánh k bằng sáu chắc chắn ra đỏ: đóng góp một phần sáu. Chia cho bảy phần mười hai được hai phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: hai phần bảy. Hậu nghiệm tỉ lệ với k: mỗi giá trị k có xác suất k phần hai mươi mốt.'),
    Beat('outro', 'outro', outro_text(366)),
]

FORMULAS = formulas('2/7', OPTIONS,
                    red='P(Đ) = 1/36 (1 + 2 + dots + 6) = 7/12',
                    prob='P(k = 6 | Đ) = (1/6)/(7/12) = 2/7')


def validate() -> bool:
    assert RED == F(7, 12) and F(1, 6) / RED == F(2, 7)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS366(TreeMixin, ShortScene):
    N = 366

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.4, r=.3, edge_size=24)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('red', 1.4))

    def beat_s3(self, T):
        self.play(FadeIn(SurroundingRectangle(self.leaves[5][0], color=GOLD, buff=.08)), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
