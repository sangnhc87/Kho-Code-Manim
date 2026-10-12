"""XSS235 · Ai bắn trượt? — 0,5; 0,6; 0,7; đúng 2 trúng: 0,21 (A trượt) / 0,44 = 21/44."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS235', 'answer': '21/44'}
PROBLEM = ['Ba xạ thủ A, B, C trúng với xác suất',
           '$"0,5"$; $"0,6"$; $"0,7"$. Biết có đúng $2$ người',
           'trúng. Xác suất A là người trượt?']
OPTIONS = ['1/3', '21/44', '1/2']
CORRECT = 1
ANSWER_VALUE = 21 / 44
PR = (F(1, 2), F(3, 5), F(7, 10))


def prob(w):
    out = F(1)
    for hit, p in zip(w, PR):
        out *= p if hit else 1 - p
    return out


BEATS = [
    Beat('hook', 'hook', 'Ba xạ thủ A, B, C bắn trúng với xác suất không phẩy năm, không phẩy sáu và không phẩy bảy. '
                         'Biết có đúng hai người trúng. Xác suất A là người bắn trượt là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, hai mươi mốt phần bốn mươi tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đúng hai người trúng có ba khả năng, tùy ai trượt. A trượt: không phẩy năm nhân không phẩy sáu nhân không phẩy bảy, bằng không phẩy hai mốt.'),
    Beat('s2', 'solve', 'B trượt: không phẩy năm nhân không phẩy bốn nhân không phẩy bảy, bằng không phẩy một bốn. '
                        'C trượt: không phẩy năm nhân không phẩy sáu nhân không phẩy ba, bằng không phẩy không chín. Tổng không phẩy bốn bốn.'),
    Beat('s3', 'solve', 'Xác suất A trượt bằng hai mươi mốt phần bốn mươi tư, gần một nửa: người kém nhất là nghi phạm số một.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi mốt phần bốn mươi tư. Liệt kê theo "ai khác biệt", rồi lấy tỉ lệ!'),
    Beat('outro', 'outro', outro_text(235)),
]

FORMULAS = formulas('21/44', OPTIONS,
                    cases='"0,21", quad "0,14", quad "0,09"',
                    prob='P = ("0,21")/("0,21" + "0,14" + "0,09") = 21/44')


def validate() -> bool:
    two = [w for w in product((0, 1), repeat=3) if sum(w) == 2]
    assert sum(prob(w) for w in two if w[0] == 0) / sum(prob(w) for w in two) == F(21, 44)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS235(ShortScene):
    N = 235

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.shooters = VGroup(*[VGroup(token(n, SOFT, .4), self.TM(f'${p}$', 26, SOFT)).arrange([0, -1, 0], buff=.15)
                                 for n, p in zip('ABC', ('"0,5"', '"0,6"', '"0,7"'))]).arrange(buff=1.1).move_to([0, 2.1, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.shooters, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        rows = VGroup(*[VGroup(*[token('T' if i != k else 'X', GREEN if i != k else CORAL, .24) for i in range(3)])
                        .arrange(buff=.1) for k in range(3)]).arrange(buff=.6).move_to([0, .55, 0])
        self.play(FadeIn(rows, lag_ratio=.3), run_time=self.rt(.12))
        self.rows = rows
        self.wait_until(.6, t0)
        self.play(rows[0].animate.scale(1.2), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('cases', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('người kém nhất bị nghi nhất', 26, GOLD), anim='fade')
