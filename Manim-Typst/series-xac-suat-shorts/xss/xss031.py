"""XSS031 · Số chính phương — 10 số trong 1 … 100: 1/10."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PANEL_2, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS031', 'answer': '1/10'}
PROBLEM = ['Chọn ngẫu nhiên một số từ $1$ đến $100$.', 'Xác suất đó là số chính phương?']
OPTIONS = ['1/9', '1/10', '1/5']
CORRECT = 1
ANSWER_VALUE = .1
SQUARES = [k * k for k in range(1, 11)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một số từ một đến một trăm. Xác suất số đó là số chính phương, '
                         'tức bình phương của một số nguyên, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần chín, một phần mười, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bảng mười nhân mười chứa đúng một trăm số, mỗi số có cùng cơ hội được chọn.'),
    Beat('s2', 'solve', 'Các số chính phương: một, bốn, chín, mười sáu, hai mươi lăm, ba mươi sáu, bốn mươi chín, '
                        'sáu mươi tư, tám mươi mốt, một trăm. Đúng mười số, từ một bình phương đến mười bình phương.'),
    Beat('s3', 'solve', 'Xác suất bằng mười phần một trăm, tức một phần mười. Để ý các số chính phương càng lúc càng '
                        'thưa: khoảng cách giữa chúng tăng dần theo các số lẻ ba, năm, bảy, chín.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười. Nếu chọn từ một đến một vạn, xác suất chỉ còn một phần một trăm!'),
    Beat('outro', 'outro', outro_text(31)),
]

FORMULAS = formulas('1/10', OPTIONS, n='n(Omega) = 100', a='A = {1^2; 2^2; dots; 10^2}', prob='P = 10/100 = 1/10')


def validate() -> bool:
    assert Fraction(sum(int(n ** .5) ** 2 == n for n in range(1, 101)), 100) == Fraction(1, 10)
    assert Fraction(sum(int(n ** .5) ** 2 == n for n in range(1, 10001)), 10000) == Fraction(1, 100)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS031(ShortScene):
    N = 31

    def hook_visual(self, t0):
        self.board_top = -1.4
        cells = VGroup()
        for k in range(1, 101):
            sq = Square(side_length=.6, stroke_color=STROKE, stroke_width=1.5, fill_color=PANEL_2, fill_opacity=1)
            cells.add(VGroup(sq, self.MNum(k, 0, SOFT, 15).move_to(sq)))
        cells.arrange_in_grid(10, 10, buff=.04).move_to([0, 1.05, 0])
        self.cells = cells
        self.wait_until(.45, t0)
        self.play(FadeIn(cells, lag_ratio=.004), run_time=self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        for s in SQUARES:
            self.play(self.cells[s - 1][0].animate.set_fill(GOLD, .8), run_time=self.rt(.055))
        self.wait_until(.75, t0)
        self.write_board(self.M('a', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(tx('càng lớn càng thưa: 3, 5, 7, 9…', 26, SOFT), anim='fade')
