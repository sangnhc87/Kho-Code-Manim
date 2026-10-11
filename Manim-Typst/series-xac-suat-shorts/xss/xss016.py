"""XSS016 · Tổng bằng 7 — đường chéo dài nhất của bảng 6 × 6: 6/36 = 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import die, roll_faces  # noqa: E402

EPISODE = {'code': 'XSS016', 'answer': '1/6'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Xác suất tổng số chấm bằng $7$?']
OPTIONS = ['1/12', '7/36', '1/6']
CORRECT = 2
ANSWER_VALUE = 1 / 6

BEATS = [
    Beat('hook', 'hook', 'Trong nhiều trò chơi xúc xắc, tổng bảy được gọi là con số may mắn. '
                         'Gieo hai con xúc xắc, xác suất được tổng bảy là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười hai, bảy phần ba mươi sáu, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mở lại bảng sáu nhân sáu và ghi tổng số chấm vào từng ô. '
                        'Ba mươi sáu ô, ba mươi sáu kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Các ô có tổng bảy: một sáu, hai năm, ba bốn, bốn ba, năm hai, sáu một. '
                        'Sáu ô, nên xác suất bằng sáu phần ba mươi sáu, tức một phần sáu.'),
    Beat('s3', 'solve', 'Để ý: các ô tổng bảy nằm trọn trên đường chéo dài nhất của bảng. '
                        'Không tổng nào có nhiều cách tạo ra hơn, đó là lý do bảy là tổng may mắn.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Gieo sáu lần, trung bình sẽ có một lần ra tổng bảy.'),
    Beat('outro', 'outro', outro_text(16)),
]

FORMULAS = formulas('1/6', OPTIONS, prob='P = 6/36 = 1/6')


def validate() -> bool:
    assert Fraction(sum(a + b == 7 for a, b in product(range(1, 7), repeat=2)), 36) == Fraction(1, 6)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS016(DiceGridMixin, ShortScene):
    N = 16

    def hook_visual(self, t0):
        self.d1 = die(1, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(1, 1.5).move_to([1.2, 1.3, 0])
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.d1 = self.roll(self.d1, roll_faces(3, 4, 16), self.rt(.2))
        self.d2 = self.roll(self.d2, roll_faces(4, 4, 61), self.rt(.2))

    def beat_s1(self, T):
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.3, sums=True)

    def beat_s2(self, T):
        t0 = self.now()
        cells = [self.g.cells[6 - a][a - 1] for a in range(1, 7)]
        self.light(cells, GOLD, .06)
        self.wait_until(.62, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.15, t0)
        self.write_board(VGroup(tx('đường chéo dài nhất', 30, GOLD, bold=True), tx('nhiều cách nhất', 28, SOFT))
                         .arrange(buff=.3), anim='fade')
