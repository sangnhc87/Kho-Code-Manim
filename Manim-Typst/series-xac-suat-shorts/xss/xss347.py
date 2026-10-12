"""XSS347 · Mỗi toa hai người — 6 khách chọn 1 trong 3 toa: 3⁶ = 729; mỗi toa đúng 2: 6!/(2!2!2!) = 90 → 10/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._seatkit import ride, train  # noqa: E402

EPISODE = {'code': 'XSS347', 'answer': '10/81'}
PROBLEM = ['$6$ hành khách, mỗi người chọn ngẫu nhiên',
           '$1$ trong $3$ toa tàu. Xác suất mỗi toa có',
           'đúng $2$ người?']
OPTIONS = ['10/81', '1/27', '2/9']
CORRECT = 0
ANSWER_VALUE = 10 / 81

BEATS = [
    Beat('hook', 'hook', 'Sáu hành khách lên một đoàn tàu ba toa, mỗi người chọn ngẫu nhiên một toa. Xác suất mỗi toa có đúng hai người là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười phần tám mươi mốt, một phần hai mươi bảy, hay hai phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi người có ba lựa chọn độc lập: ba mũ sáu, bảy trăm hai mươi chín cách đồng khả năng.'),
    Beat('s2', 'solve', 'Chia sáu người thành ba nhóm hai cho ba toa đã đánh số: chọn hai người cho toa một, mười lăm cách; hai người cho toa hai, sáu cách; còn lại vào toa ba. Tổng chín mươi.'),
    Beat('s3', 'solve', 'Xác suất chín mươi phần bảy trăm hai mươi chín, rút gọn mười phần tám mươi mốt, khoảng mười hai phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: mười phần tám mươi mốt. Chia đều hoàn hảo hiếm hơn ta tưởng.'),
    Beat('outro', 'outro', outro_text(347)),
]

FORMULAS = formulas('10/81', OPTIONS,
                    all='3^6 = 729',
                    good='C_6^2 dot C_4^2 dot C_2^2 = 90',
                    prob='P = 90/729 = 10/81')


def validate() -> bool:
    good = sum(sorted(t.count(i) for i in range(3)) == [2, 2, 2] for t in product(range(3), repeat=6))
    assert good == 90 and F(good, 729) == F(10, 81)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS347(ShortScene):
    N = 347

    def load(self, counts, frac=.06):
        new = ride(self.cars, counts)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.cars = train(3, y=1.3, scene=self)
        self.play(FadeIn(self.cars, lag_ratio=.2), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.load([3, 1, 2])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.load([1, 0, 5], .05)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.load([2, 2, 2], .06)
        self.wait_until(.5, t0)
        self.clear_board(.03)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
