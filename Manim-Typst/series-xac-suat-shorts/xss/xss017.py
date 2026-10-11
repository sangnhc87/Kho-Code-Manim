"""XSS017 · Tổng bằng 8 — 5 ô: (2;6) (3;5) (4;4) (5;3) (6;2) → 5/36."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS017', 'answer': '5/36'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Xác suất tổng số chấm bằng $8$?']
OPTIONS = ['1/6', '5/36', '1/9']
CORRECT = 1
ANSWER_VALUE = 5 / 36

BEATS = [
    Beat('hook', 'hook', 'Tổng bảy có xác suất một phần sáu. Vậy tổng tám thì sao? Lớn hơn một chút thì xác suất '
                         'có lớn hơn không?'),
    Beat('guess', 'hook', 'Một phần sáu, năm phần ba mươi sáu, hay một phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lại mở bảng sáu nhân sáu có ghi tổng. Ba mươi sáu kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Tổng tám có các cặp: hai sáu, ba năm, bốn bốn, năm ba, sáu hai. Chỉ năm ô thôi, '
                        'vì một cộng bảy không thể xảy ra.'),
    Beat('s3', 'solve', 'Chú ý cặp bốn bốn chỉ có một ô, còn ba năm và năm ba là hai ô khác nhau. '
                        'Xác suất bằng năm phần ba mươi sáu, nhỏ hơn tổng bảy.'),
    Beat('answer', 'solve', 'Đáp án: năm phần ba mươi sáu. Càng xa số bảy, tổng càng khó ra.'),
    Beat('outro', 'outro', outro_text(17)),
]

FORMULAS = formulas('5/36', OPTIONS, prob='P = 5/36', cmp='5/36 < 6/36')


def validate() -> bool:
    assert Fraction(sum(a + b == 8 for a, b in product(range(1, 7), repeat=2)), 36) == Fraction(5, 36)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS017(DiceGridMixin, ShortScene):
    N = 17

    def hook_visual(self, t0):
        self.d1 = die(4, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(4, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.05))
        self.remove(self.d1, self.d2)
        self.show_grid(.35, sums=True)

    def beat_s2(self, T):
        t0 = self.now()
        cells = [self.g.cells[8 - a - 1][a - 1] for a in range(2, 7)]
        self.light(cells, GOLD, .07)
        self.wait_until(.75, t0)
        self.play(self.g.top[0][0].animate.set_stroke(CORAL, 5), run_time=self.rt(.04))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.g.cells[3][3].animate.set_fill(CYAN, .7), run_time=self.rt(.05))
        self.write_board(tx('(4; 4) chỉ có 1 ô', 30, CYAN, bold=True), anim='fade')
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.write_board(self.M('cmp', 1.6), anim='fade')
