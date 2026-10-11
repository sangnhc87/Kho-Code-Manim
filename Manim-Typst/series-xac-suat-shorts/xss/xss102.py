"""XSS102 · Thùng 5 lá — 4·C(13,5)/C(52,5) = 5148/2598960 = 33/16660 ≈ 0,002."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from common.visuals import playing_card  # noqa: E402

EPISODE = {'code': 'XSS102', 'answer': '33/16660 ≈ 0,002'}
PROBLEM = ['Rút ngẫu nhiên $5$ lá từ bộ bài $52$ lá.', 'Xác suất cả $5$ lá cùng một chất?']
OPTIONS = ['1/4^4', '33/16660 approx "0,002"', '1/52']
CORRECT = 1
ANSWER_VALUE = 33 / 16660

BEATS = [
    Beat('hook', 'hook', 'Rút năm lá từ bộ bài năm mươi hai lá. Xác suất cả năm lá cùng một chất, gọi là thùng, '
                         'là bao nhiêu? Bài thùng hiếm đến mức nào?'),
    Beat('guess', 'hook', 'Một phần hai trăm năm mươi sáu, khoảng không phẩy không không hai, hay một phần năm mươi hai? '
                          'Ba, hai, một!'),
    Beat('s1', 'solve', 'Số cách rút năm lá từ năm mươi hai lá: tổ hợp chập năm của năm mươi hai, '
                        'bằng hai triệu năm trăm chín mươi tám nghìn chín trăm sáu mươi cách.'),
    Beat('s2', 'solve', 'Thùng: chọn một trong bốn chất, rồi chọn năm lá trong mười ba lá của chất đó. '
                        'Bốn nhân tổ hợp chập năm của mười ba, bằng năm nghìn một trăm bốn mươi tám cách.'),
    Beat('s3', 'solve', 'Xác suất bằng ba mươi ba phần mười sáu nghìn sáu trăm sáu mươi, khoảng không phẩy không không hai, '
                        'tức chừng một lần trong năm trăm lần chia bài.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy hai phần trăm. Đó là lý do bài thùng được xếp hạng rất cao trong poker!'),
    Beat('outro', 'outro', outro_text(102)),
]

FORMULAS = formulas('33/16660 approx "0,002"', OPTIONS,
                    n='n(Omega) = C_52^5 = 2598960',
                    a='n(A) = 4 dot C_13^5 = 5148',
                    prob='P = 5148/2598960 = 33/16660 approx "0,002"')


def validate() -> bool:
    assert comb(52, 5) == 2598960 and 4 * comb(13, 5) == 5148
    p = F(5148, 2598960)
    assert p == F(33, 16660) and round(float(p), 3) == .002 and round(1 / float(p)) == 505
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS102(ShortScene):
    N = 102

    def hook_visual(self, t0):
        self.hand = VGroup(*[playing_card(r, 'H', 1.05).rotate((i - 2) * .14) for i, r in enumerate(('2', '7', '9', 'J', 'K'))]) \
            .arrange(buff=-.35).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.hand, lag_ratio=.2), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('n', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('a', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('khoảng 1 lần / 500 lần chia bài', 28, CORAL, bold=True), anim='fade')


