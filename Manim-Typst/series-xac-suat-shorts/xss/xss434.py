"""XSS434 · Đúng một lá đúng chỗ — chọn lá đúng: 5 cách; 4 lá còn lại sai hết: D₄ = 9 → 45/120 = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS434', 'answer': '3/8'}
PROBLEM = ['Xếp ngẫu nhiên $5$ lá thư vào $5$ phong bì.',
           'Xác suất có đúng $1$ lá đúng địa chỉ?']
OPTIONS = ['3/8', '1/5', '11/30']
CORRECT = 0
ANSWER_VALUE = 3 / 8


def derange(n):
    return sum(all(p[i] != i for i in range(n)) for p in permutations(range(n)))


BEATS = [
    Beat('hook', 'hook', 'Một thư ký vội vàng bỏ ngẫu nhiên năm lá thư vào năm phong bì đã ghi địa chỉ. Xác suất có đúng một lá vào đúng phong bì?'),
    Beat('guess', 'hook', 'Ba phần tám, một phần năm, hay mười một phần ba mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có năm giai thừa, một trăm hai mươi cách xếp. Chọn lá thư duy nhất đúng chỗ: năm cách.'),
    Beat('s2', 'solve', 'Bốn lá còn lại phải sai hết: số cách xếp sai hoàn toàn bốn phần tử là chín. Ví dụ hai một bốn ba, hay hai ba bốn một.'),
    Beat('s3', 'solve', 'Năm nhân chín bằng bốn mươi lăm, chia một trăm hai mươi được ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Số xếp sai hoàn toàn là viên gạch xây nên mọi bài đúng chỗ.'),
    Beat('outro', 'outro', outro_text(434)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    d4='D_4 = 4! (1 - 1 + 1/2 - 1/6 + 1/24) = 9',
                    prob='P = (5 dot 9)/(5!) = 45/120 = 3/8')


def validate() -> bool:
    assert derange(4) == 9
    good = sum(sum(p[i] == i for i in range(5)) == 1 for p in permutations(range(5)))
    assert good == 45 and F(good, 120) == F(3, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS434(ShortScene):
    N = 434

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.env = VGroup(*[token(str(i + 1), SOFT, .32) for i in range(5)]).arrange(buff=.45).move_to([0, 1.8, 0])
        self.let = VGroup(*[token(str(v), CYAN, .26) for v in (1, 3, 4, 5, 2)]).arrange(buff=.51).move_to([0, .9, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.env), FadeIn(self.let, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.let[0][0].animate.set_fill(GREEN), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.let[i][0].animate.set_fill(CORAL) for i in range(1, 5)], run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.write_board(self.M('d4', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)


