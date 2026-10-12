"""XSS348 · Toa nào cũng có khách — 5 khách, 3 toa: bao hàm loại trừ 3⁵ − 3·2⁵ + 3·1⁵ = 150 → 150/243 = 50/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._seatkit import ride, train  # noqa: E402

EPISODE = {'code': 'XSS348', 'answer': '50/81'}
PROBLEM = ['$5$ hành khách, mỗi người chọn ngẫu nhiên',
           '$1$ trong $3$ toa. Xác suất toa nào cũng',
           'có người?']
OPTIONS = ['50/81', '2/3', '20/27']
CORRECT = 0
ANSWER_VALUE = 50 / 81

BEATS = [
    Beat('hook', 'hook', 'Năm hành khách, mỗi người chọn ngẫu nhiên một trong ba toa tàu. Xác suất không có toa nào bị bỏ trống là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm mươi phần tám mươi mốt, hai phần ba, hay hai mươi phần hai mươi bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tổng số cách: ba mũ năm, hai trăm bốn mươi ba. Đếm phần bù: có ít nhất một toa trống.'),
    Beat('s2', 'solve', 'Một toa cụ thể trống: mọi người dồn vào hai toa kia, hai mũ năm cách, nhân ba toa. Nhưng trường hợp hai toa trống bị trừ hai lần, phải cộng lại ba cách.'),
    Beat('s3', 'solve', 'Toa nào cũng có người: hai trăm bốn mươi ba trừ chín mươi sáu cộng ba, bằng một trăm năm mươi. Xác suất năm mươi phần tám mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: năm mươi phần tám mươi mốt. Không toa nào trống là bài bao hàm loại trừ kinh điển.'),
    Beat('outro', 'outro', outro_text(348)),
]

FORMULAS = formulas('50/81', OPTIONS,
                    all='3^5 = 243',
                    ie='3^5 - 3 dot 2^5 + 3 dot 1^5 = 150',
                    prob='P = 150/243 = 50/81')


def validate() -> bool:
    good = sum(len(set(t)) == 3 for t in product(range(3), repeat=5))
    assert good == 150 and F(good, 243) == F(50, 81)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS348(ShortScene):
    N = 348

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
        self.load([2, 0, 3])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.load([0, 2, 3], .05)
        self.wait_until(.6, t0)
        self.load([0, 0, 5], .05)

    def beat_s3(self, T):
        self.load([2, 1, 2], .05)
        self.clear_board(.03)
        self.write_board(self.M('ie', 1.4))
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
