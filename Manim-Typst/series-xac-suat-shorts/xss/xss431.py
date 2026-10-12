"""XSS431 · Tích chia hết cho 4 — bù: 3 số lẻ C(10;3) = 120, hoặc đúng 1 số ≡ 2 (mod 4) và 2 số lẻ: 5·C(10;2) = 225; 345/1140 = 23/76 → 53/76."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401

from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS431', 'answer': '53/76'}
PROBLEM = ['Chọn $3$ số khác nhau từ $1$ đến $20$. Xác',
           'suất tích ba số chia hết cho $4$?']
OPTIONS = ['53/76', '3/4', '1/2']
CORRECT = 0
ANSWER_VALUE = 53 / 76

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba số khác nhau từ một đến hai mươi. Xác suất tích ba số chia hết cho bốn là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm mươi ba phần bảy mươi sáu, ba phần tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chia hai mươi số theo lũy thừa của hai: mười số lẻ, năm số chia bốn dư hai, và năm số chia hết cho bốn.'),
    Beat('s2', 'solve', 'Tích không chia hết cho bốn khi: cả ba số lẻ, một trăm hai mươi cách; hoặc đúng một số chia bốn dư hai cùng hai số lẻ, năm nhân bốn mươi lăm, hai trăm hai mươi lăm cách.'),
    Beat('s3', 'solve', 'Phần bù: ba trăm bốn mươi lăm trên một nghìn một trăm bốn mươi, tức hai mươi ba phần bảy mươi sáu. Vậy xác suất năm mươi ba phần bảy mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: năm mươi ba phần bảy mươi sáu. Phân nhóm theo số mũ của hai là chìa khóa cho bài chia hết.'),
    Beat('outro', 'outro', outro_text(431)),
]

FORMULAS = formulas('53/76', OPTIONS,
                    comp='C_10^3 + 5 dot C_10^2 = 120 + 225 = 345',
                    prob='P = 1 - 345/1140 = 53/76')


def validate() -> bool:
    good = sum(a * b * c % 4 == 0 for a, b, c in combinations(range(1, 21), 3))
    assert comb(10, 3) + 5 * comb(10, 2) == 345 and F(good, comb(20, 3)) == F(53, 76)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS431(ShortScene):
    N = 431

    def hook_visual(self, t0):
        self.board_top = -1.4
        odd = ball_row('B' * 10, r=.22, buff=.06, labels=list(range(1, 21, 2)), size=16)
        two = ball_row('Y' * 5, r=.22, buff=.06, labels=[2, 6, 10, 14, 18], size=16)
        four = ball_row('R' * 5, r=.22, buff=.06, labels=[4, 8, 12, 16, 20], size=16)
        self.groups = VGroup(odd, two, four).arrange(DOWN, buff=.25).move_to([0, 1.1, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.groups, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.groups[2].animate.scale(1.1), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('comp', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)


