"""XSS357 · Ba lớp, sáu bạn — 3 lớp × 2 bạn vào dãy 6 ghế; bao hàm loại trừ 720 − 3·240 + 3·96 − 48 = 240 → 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS357', 'answer': '1/3'}
PROBLEM = ['$3$ lớp, mỗi lớp $2$ bạn, ngồi ngẫu nhiên',
           'vào dãy $6$ ghế. Xác suất không có $2$ bạn',
           'cùng lớp nào ngồi cạnh nhau?']
OPTIONS = ['1/3', '1/5', '2/5']
CORRECT = 0
ANSWER_VALUE = 1 / 3
CLS = {'A': ('A', CYAN), 'B': ('B', CORAL), 'C': ('C', GOLD)}
TERMS = [(-1) ** k * comb(3, k) * 2 ** k * factorial(6 - k) for k in range(4)]

BEATS = [
    Beat('hook', 'hook', 'Ba lớp, mỗi lớp cử hai bạn, sáu bạn ngồi ngẫu nhiên vào một dãy sáu ghế. '
                         'Xác suất không có hai bạn cùng lớp nào ngồi cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần năm, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tổng sáu giai thừa, bảy trăm hai mươi cách. Đếm phần xấu bằng bao hàm loại trừ: một lớp ngồi cạnh nhau, buộc thành khối: hai nhân năm giai thừa, hai trăm bốn mươi, nhân ba lớp.'),
    Beat('s2', 'solve', 'Hai lớp cùng ngồi cạnh: bốn nhân bốn giai thừa, chín mươi sáu, nhân ba cặp lớp. Cả ba lớp: tám nhân ba giai thừa, bốn mươi tám.'),
    Beat('s3', 'solve', 'Số cách tốt: bảy trăm hai mươi trừ bảy trăm hai mươi cộng hai trăm tám mươi tám trừ bốn mươi tám, bằng hai trăm bốn mươi. Xác suất một phần ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Bao hàm loại trừ biến điều kiện không ai cạnh ai thành các khối dễ đếm.'),
    Beat('outro', 'outro', outro_text(357)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    one='3 dot 2 dot 5! = 720',
                    two='3 dot 2^2 dot 4! = 288, quad 2^3 dot 3! = 48',
                    prob='P = (720 - 720 + 288 - 48)/720 = 1/3')


def validate() -> bool:
    good = sum(all(p[i] // 2 != p[i + 1] // 2 for i in range(5)) for p in permutations(range(6)))
    assert good == sum(TERMS) == 240 and F(good, 720) == F(1, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS357(ShortScene):
    N = 357

    def place(self, pattern, frac=.06):
        new = seat([CLS[c] for c in pattern], self.seats)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.seats = seat_row(6, y=1.3)
        self.play(FadeIn(self.seats), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.place('ABACBC')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.place('AABCBC', .05)
        self.wait_until(.6, t0)
        self.write_board(self.M('one', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.place('AABBCC', .05)
        self.wait_until(.5, t0)
        self.write_board(self.M('two', 1.3))

    def beat_s3(self, T):
        self.place('ABCABC', .05)
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
