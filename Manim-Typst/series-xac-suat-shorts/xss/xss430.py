"""XSS430 · Tích chia hết cho 6 — bù: không chẵn (1/8) hoặc không chia hết 3 (8/27), trừ phần chung {1; 5} (1/27): 83/216 → 133/216."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS430', 'answer': '133/216'}
PROBLEM = ['Gieo $3$ xúc xắc. Xác suất tích số chấm',
           'chia hết cho $6$?']
OPTIONS = ['133/216', '1/6', '2/3']
CORRECT = 0
ANSWER_VALUE = 133 / 216

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc và nhân số chấm với nhau. Xác suất tích chia hết cho sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một trăm ba mươi ba phần hai trăm mười sáu, một phần sáu, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tích không chia hết cho sáu khi không có số chẵn nào, hoặc không có bội của ba nào. Dùng bao hàm loại trừ trên phần bù.'),
    Beat('s2', 'solve', 'Không có số chẵn: một phần hai mũ ba, một phần tám. Không có bội của ba: hai phần ba mũ ba, tám phần hai mươi bảy. Cả hai, tức toàn số một và năm: một phần hai mươi bảy.'),
    Beat('s3', 'solve', 'Phần bù: một phần tám cộng tám phần hai mươi bảy trừ một phần hai mươi bảy, bằng tám mươi ba phần hai trăm mười sáu. Đáp án: một trăm ba mươi ba phần hai trăm mười sáu.'),
    Beat('answer', 'solve', 'Đáp án: một trăm ba mươi ba phần hai trăm mười sáu. Chia hết cho số hợp: tách thành các thừa số nguyên tố rồi bao hàm loại trừ.'),
    Beat('outro', 'outro', outro_text(430)),
]

FORMULAS = formulas('133/216', OPTIONS,
                    parts='P(overline(2)) = 1/8, quad P(overline(3)) = 8/27, quad P(overline(2) overline(3)) = 1/27',
                    comp='1/8 + 8/27 - 1/27 = 83/216',
                    prob='P = 1 - 83/216 = 133/216')


def validate() -> bool:
    good = sum(a * b * c % 6 == 0 for a, b, c in product(range(1, 7), repeat=3))
    assert F(good, 216) == F(133, 216) == 1 - (F(1, 8) + F(8, 27) - F(1, 27))
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS430(ShortScene):
    N = 430

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.dice = VGroup(*[die(v, .9) for v in (2, 5, 3)]).arrange(buff=.5).move_to([0, 1.4, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.dice, lag_ratio=.2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.dice.animate.set_opacity(.4), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('parts', 1.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('comp', 1.3))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
