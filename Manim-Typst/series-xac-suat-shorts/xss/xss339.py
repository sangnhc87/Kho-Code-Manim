"""XSS339 · Đúng hai màu — 5 đỏ 4 xanh 3 trắng, rút 3: 220 − 15 (một màu) − 60 (ba màu) = 145 → 29/44."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS339', 'answer': '29/44'}
PROBLEM = ['Hộp $5$ đỏ, $4$ xanh, $3$ trắng. Rút $3$ bi.',
           'Xác suất ba bi có đúng hai màu?']
OPTIONS = ['29/44', '3/4', '15/22']
CORRECT = 0
ANSWER_VALUE = 29 / 44
BALLS = 'RRRRRBBBBWWW'
TWO = [t for t in combinations(range(12), 3) if len({BALLS[i] for i in t}) == 2]

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ, bốn bi xanh, ba bi trắng. Rút ngẫu nhiên ba bi. Xác suất ba bi có đúng hai màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi chín phần bốn mươi bốn, ba phần tư, hay mười lăm phần hai mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm trực tiếp đúng hai màu khá rối, nên dùng phần bù. Tổng số cách: hai trăm hai mươi. Ba bi chỉ có một màu, hoặc có đủ ba màu, hoặc đúng hai màu.'),
    Beat('s2', 'solve', 'Một màu: mười cộng bốn cộng một, mười lăm cách. Ba màu: năm nhân bốn nhân ba, sáu mươi cách.'),
    Beat('s3', 'solve', 'Đúng hai màu: hai trăm hai mươi trừ mười lăm trừ sáu mươi, còn một trăm bốn mươi lăm. Xác suất hai mươi chín phần bốn mươi bốn.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi chín phần bốn mươi bốn. Trường hợp ở giữa thường dễ đếm nhất bằng cách bỏ hai đầu.'),
    Beat('outro', 'outro', outro_text(339)),
]

FORMULAS = formulas('29/44', OPTIONS,
                    one='C_5^3 + C_4^3 + C_3^3 = 15',
                    three='5 dot 4 dot 3 = 60',
                    prob='P = (220 - 15 - 60)/220 = 29/44')


def validate() -> bool:
    assert len(TWO) == 145 and F(len(TWO), comb(12, 3)) == F(29, 44)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS339(ShortScene):
    N = 339

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.pool = ball_row(BALLS, y=2.2, r=.24, buff=.07)
        self.play(FadeIn(self.pool, lag_ratio=.05), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.ex = ball_row('RRW', y=.7, r=.36, buff=.4)
        self.play(FadeIn(self.ex, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.TM('$C_12^3 = 220$', 36))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('one', 1.4))
        self.wait_until(.55, t0)
        self.write_board(self.M('three', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
