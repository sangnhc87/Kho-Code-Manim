"""XSS360 · An ngồi một mình — 5 khách 3 toa, biết toa nào cũng có người (150 cách); An một mình: 3 · (2⁴ − 2) = 42 → 7/25."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from common.visuals import token  # noqa: E402
from xss._seatkit import ride, train  # noqa: E402

EPISODE = {'code': 'XSS360', 'answer': '7/25'}
PROBLEM = ['$5$ hành khách chọn ngẫu nhiên $3$ toa. Biết',
           'toa nào cũng có người. Xác suất An ở một',
           'toa chỉ có mình An?']
OPTIONS = ['7/25', '1/3', '1/5']
CORRECT = 0
ANSWER_VALUE = 7 / 25
COND = [t for t in product(range(3), repeat=5) if len(set(t)) == 3]
ALONE = [t for t in COND if t.count(t[0]) == 1]

BEATS = [
    Beat('hook', 'hook', 'Năm hành khách, trong đó có An, chọn ngẫu nhiên một trong ba toa. Biết toa nào cũng có người. '
                         'Xác suất An ngồi ở một toa chỉ có mình An là bao nhiêu?'),
    Beat('guess', 'hook', 'Bảy phần hai mươi lăm, một phần ba, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện toa nào cũng có người: bao hàm loại trừ cho ba mũ năm trừ ba nhân hai mũ năm cộng ba, bằng một trăm năm mươi cách.'),
    Beat('s2', 'solve', 'An ngồi một mình: An chọn toa, ba cách. Bốn người còn lại phải lấp kín hai toa kia: hai mũ bốn trừ hai, mười bốn cách. Tổng bốn mươi hai.'),
    Beat('s3', 'solve', 'Xác suất bốn mươi hai phần một trăm năm mươi, rút gọn bảy phần hai mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần hai mươi lăm. Hết nhánh bốn vận dụng cao! Nhánh tiếp theo: đa hành động và điều kiện dừng.'),
    Beat('outro', 'outro', outro_text(360)),
]

FORMULAS = formulas('7/25', OPTIONS,
                    cond='3^5 - 3 dot 2^5 + 3 = 150',
                    alone='3 dot (2^4 - 2) = 42',
                    prob='P = 42/150 = 7/25')


def validate() -> bool:
    assert len(COND) == 150 and len(ALONE) == 42
    assert F(len(ALONE), len(COND)) == F(7, 25)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS360(ShortScene):
    N = 360

    def load(self, counts, an, frac=.06):
        dots = ride(self.cars, counts)
        tag = token('An', CORAL, .24).move_to(self.cars[an][0].get_center() + [0, .25 if counts[an] else 0, 0])
        if counts[an]:
            dots[an].shift([0, -.22, 0])
        new = VGroup(dots, tag)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.cars = train(3, y=1.3, scene=self)
        self.play(FadeIn(self.cars, lag_ratio=.2), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.load([1, 2, 1], 0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.load([0, 3, 1], 0, .06)
        self.wait_until(.6, t0)
        self.clear_board(.03)
        self.write_board(self.M('alone', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
