"""XSS429 · Cao nhất cạnh thấp nhất — chỉ xét cặp vị trí của 2 bạn đó: 45 cặp như nhau, 9 cặp kề nhau → 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS429', 'answer': '1/5'}
PROBLEM = ['$10$ bạn xếp hàng ngẫu nhiên. Xác suất bạn',
           'cao nhất đứng cạnh bạn thấp nhất?']
OPTIONS = ['1/5', '1/10', '2/9']
CORRECT = 0
ANSWER_VALUE = .2

BEATS = [
    Beat('hook', 'hook', 'Mười bạn xếp thành một hàng ngẫu nhiên. Xác suất bạn cao nhất đứng ngay cạnh bạn thấp nhất là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, một phần mười, hay hai phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chỉ cần quan tâm hai vị trí của bạn cao nhất và thấp nhất: tổ hợp chập hai của mười, bốn mươi lăm cặp vị trí đồng khả năng.'),
    Beat('s2', 'solve', 'Hai vị trí kề nhau: một hai, hai ba, đến chín mười, có chín cặp.'),
    Beat('s3', 'solve', 'Xác suất chín phần bốn mươi lăm, tức một phần năm. Đếm bằng buộc khối cũng ra: hai nhân chín giai thừa chia mười giai thừa.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Bỏ qua những người không liên quan, bài toán chỉ còn hai vị trí.'),
    Beat('outro', 'outro', outro_text(429)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    pairs='C_10^2 = 45, quad "kề nhau": 9',
                    prob='P = 9/45 = (2 dot 9!)/(10!) = 1/5')


def validate() -> bool:
    assert F(9, comb(10, 2)) == F(2 * factorial(9), factorial(10)) == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS429(ShortScene):
    N = 429

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.seats = seat_row(10, y=1.3, w=.58, gap=.1)
        self.ppl = seat([(' ', SOFT)] * 3 + [('C', CORAL), ('T', CYAN)] + [(' ', SOFT)] * 5, self.seats, r=.24)
        self.wait_until(.45, t0)
        self.play(FadeIn(self.seats), FadeIn(self.ppl, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[p.animate.set_opacity(.2) for i, p in enumerate(self.ppl) if i not in (3, 4)], run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.write_board(self.M('pairs', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.ppl[3].animate.scale(1.25), self.ppl[4].animate.scale(1.25), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
