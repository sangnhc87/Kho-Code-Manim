"""XSS012 · Hai mặt giống nhau — đường chéo của bảng 6 × 6: 6/36 = 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import dice_grid, die  # noqa: E402

EPISODE = {'code': 'XSS012', 'answer': '1/6'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Xác suất hai mặt giống nhau?']
OPTIONS = ['1/36', '1/12', '1/6']
CORRECT = 2
ANSWER_VALUE = 1 / 6

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc. Xác suất hai mặt giống nhau, như hai con ba hay hai con sáu, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba mươi sáu, một phần mười hai, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dùng bảng sáu nhân sáu từ thử thách trước: ba mươi sáu ô, mỗi ô là một kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Hai mặt giống nhau nằm trên đường chéo: một một, hai hai, cho đến sáu sáu. Có đúng sáu ô. '
                        'Xác suất bằng sáu phần ba mươi sáu, tức một phần sáu.'),
    Beat('s3', 'solve', 'Cách nghĩ nhanh hơn: con thứ nhất ra mặt nào cũng được, con thứ hai chỉ cần trùng với nó, '
                        'cơ hội là một phần sáu. Đừng nhầm với một phần ba mươi sáu: đó là xác suất ra đúng hai con sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Cứ sáu lần gieo thì trung bình có một lần hai mặt giống nhau.'),
    Beat('outro', 'outro', outro_text(12)),
]

FORMULAS = formulas('1/6', OPTIONS,
                    prob='P = 6/36 = 1/6',
                    quick='P = 1 dot 1/6 = 1/6',
                    pair='P("hai con 6") = 1/36')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=2))
    assert Fraction(sum(a == b for a, b in space), 36) == Fraction(1, 6)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS012(ShortScene):
    N = 12

    def hook_visual(self, t0):
        self.board_top = -1.65
        self.d1 = die(3, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(3, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.12))

    def beat_s1(self, T):
        self.play(FadeOut(self.d1), FadeOut(self.d2), run_time=self.rt(.05))
        self.g = dice_grid(.66, .5).move_to([.1, 1.0, 0])
        self.play(FadeIn(self.g, lag_ratio=.01), run_time=self.rt(.4))

    def beat_s2(self, T):
        t0 = self.now()
        diag = [self.g.cells[i][i] for i in range(6)]
        for c in diag:
            self.play(c.animate.set_fill(GOLD, .55), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(VGroup(tx('con 1: tùy ý', 28, SOFT), tx('con 2: trùng con 1', 28, GOLD))
                         .arrange(buff=.4), anim='fade')
        self.wait_until(.45, t0)
        self.write_board(self.M('quick', 2.0))
        self.wait_until(.72, t0)
        self.write_board(self.M('pair', 1.6), anim='fade')
