"""XSS350 · Toa 1 trống — 5 khách, 3 toa; biết toa 1 trống thì mỗi người đều chọn toa 2 hoặc 3: 2⁵ = 32 cách như nhau, toa 2 cũng trống: 1 → 1/32."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from xss._seatkit import ride, train  # noqa: E402

EPISODE = {'code': 'XSS350', 'answer': '1/32'}
PROBLEM = ['$5$ hành khách chọn ngẫu nhiên $1$ trong $3$',
           'toa. Biết toa $1$ trống. Xác suất toa $2$',
           'cũng trống?']
OPTIONS = ['1/32', '1/243', '1/16']
CORRECT = 0
ANSWER_VALUE = 1 / 32
ALL = list(product(range(3), repeat=5))
COND = [t for t in ALL if 0 not in t]

BEATS = [
    Beat('hook', 'hook', 'Năm hành khách, mỗi người chọn ngẫu nhiên một trong ba toa. Biết toa một không có ai. '
                         'Xác suất toa hai cũng trống là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba mươi hai, một phần hai trăm bốn mươi ba, hay một phần mười sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết toa một trống, mỗi hành khách đã chọn toa hai hoặc toa ba. Các lựa chọn vẫn đồng khả năng: hai mũ năm, ba mươi hai cách.'),
    Beat('s2', 'solve', 'Toa hai cũng trống nghĩa là cả năm người dồn vào toa ba: chỉ một cách trong ba mươi hai.'),
    Beat('s3', 'solve', 'Xác suất một phần ba mươi hai. Theo công thức: một phần hai trăm bốn mươi ba chia ba mươi hai phần hai trăm bốn mươi ba, cùng kết quả.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba mươi hai. Điều kiện thu nhỏ không gian mẫu, ta đếm lại trong không gian mới.'),
    Beat('outro', 'outro', outro_text(350)),
]

FORMULAS = formulas('1/32', OPTIONS,
                    cond='2^5 = 32',
                    formula='P = (1/243)/(32/243) = 1/32')


def validate() -> bool:
    good = [t for t in COND if 1 not in t]
    assert len(COND) == 32 and len(good) == 1 and F(len(good), len(COND)) == F(1, 32)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS350(ShortScene):
    N = 350

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
        self.load([0, 3, 2])
        self.play(self.cars[0][0].animate.set_stroke(CORAL, 6), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.load([0, 1, 4], .05)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.load([0, 0, 5], .06)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.3, t0)
        m = self.M('formula', 1.6)
        self.write_board(m)
        self.frame(m)
