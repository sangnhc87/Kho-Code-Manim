"""XSS349 · Bốn người bốn toa — 4 khách chọn 1 trong 4 toa: 4⁴ = 256; mỗi toa đúng 1: 4! = 24 → 3/32."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._seatkit import ride, train  # noqa: E402

EPISODE = {'code': 'XSS349', 'answer': '3/32'}
PROBLEM = ['$4$ hành khách, mỗi người chọn ngẫu nhiên',
           '$1$ trong $4$ toa. Xác suất mỗi toa có đúng',
           '$1$ người?']
OPTIONS = ['3/32', '1/24', '1/4']
CORRECT = 0
ANSWER_VALUE = 3 / 32

BEATS = [
    Beat('hook', 'hook', 'Bốn hành khách lên đoàn tàu bốn toa, mỗi người chọn ngẫu nhiên một toa. Xác suất mỗi toa có đúng một người là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần ba mươi hai, một phần hai mươi tư, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi người bốn lựa chọn: bốn mũ bốn, hai trăm năm mươi sáu cách đồng khả năng.'),
    Beat('s2', 'solve', 'Mỗi toa một người nghĩa là bốn người chọn bốn toa khác nhau: người thứ nhất bốn cách, người thứ hai ba, rồi hai, rồi một. Hai mươi tư cách.'),
    Beat('s3', 'solve', 'Xác suất hai mươi tư phần hai trăm năm mươi sáu, tức ba phần ba mươi hai, chưa tới mười phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: ba phần ba mươi hai. Trùng toa xảy ra dễ hơn nhiều so với cảm giác, giống nghịch lý ngày sinh.'),
    Beat('outro', 'outro', outro_text(349)),
]

FORMULAS = formulas('3/32', OPTIONS,
                    all='4^4 = 256',
                    good='4! = 24',
                    prob='P = 24/256 = 3/32')


def validate() -> bool:
    good = sum(len(set(t)) == 4 for t in product(range(4), repeat=4))
    assert good == 24 and F(good, 256) == F(3, 32)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS349(ShortScene):
    N = 349

    def load(self, counts, frac=.06):
        new = ride(self.cars, counts)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.cars = train(4, y=1.3, w=1.6, scene=self)
        self.play(FadeIn(self.cars, lag_ratio=.2), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.load([2, 0, 1, 1])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.load([1, 1, 1, 1], .06)
        self.wait_until(.5, t0)
        self.clear_board(.03)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
