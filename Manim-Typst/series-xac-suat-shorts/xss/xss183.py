"""XSS183 · Ba cạnh tam giác — phần bù: một cạnh ≥ tổng hai cạnh kia, 35 bộ mỗi vị trí, 3·35 = 105: (216 − 105)/216 = 37/72."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS183', 'answer': '37/72'}
PROBLEM = ['Gieo $3$ con xúc xắc. Xác suất ba số chấm',
           'là độ dài ba cạnh của một tam giác?']
OPTIONS = ['1/2', '37/72', '5/8']
CORRECT = 1
ANSWER_VALUE = 37 / 72
THREE = list(product(range(1, 7), repeat=3))

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc được ba số a, b, c. Xác suất ba số đó là độ dài ba cạnh của một tam giác là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba mươi bảy phần bảy mươi hai, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm phần bù: không phải tam giác khi có một cạnh lớn hơn hoặc bằng tổng hai cạnh kia. '
                        'Hai cạnh không thể cùng lúc như vậy, nên ba trường hợp rời nhau.'),
    Beat('s2', 'solve', 'Xét a lớn hơn hoặc bằng b cộng c. Gọi s bằng b cộng c từ hai đến năm: có s trừ một cặp b, c và bảy trừ s giá trị của a. '
                        'Năm cộng tám cộng chín cộng tám cộng năm bằng ba mươi lăm.'),
    Beat('s3', 'solve', 'Nhân ba vị trí của cạnh dài: một trăm lẻ năm bộ không phải tam giác. '
                        'Còn lại một trăm mười một bộ, xác suất ba mươi bảy phần bảy mươi hai.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi bảy phần bảy mươi hai. Khi điều kiện có nhiều bất đẳng thức, đếm phần bù thường nhẹ nhàng hơn!'),
    Beat('outro', 'outro', outro_text(183)),
]

FORMULAS = formulas('37/72', OPTIONS,
                    bad='n(a >= b + c) = 5 + 8 + 9 + 8 + 5 = 35',
                    total='3 dot 35 = 105',
                    prob='P = (216 - 105)/216 = 111/216 = 37/72')


def validate() -> bool:
    assert sum(w[0] >= w[1] + w[2] for w in THREE) == 35
    assert F(sum(2 * max(w) < sum(w) for w in THREE), 216) == F(37, 72)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS183(ShortScene):
    N = 183

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.dice = VGroup(*[die(v, 1.1) for v in (6, 2, 3)]).arrange(buff=.5).move_to([0, 2.0, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.dice, lag_ratio=.3), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.play(self.dice[0][0].animate.set_stroke(CORAL, 6), run_time=self.rt(.05))
        self.play(FadeIn(self.TM('$6 >= 2 + 3$: không phải tam giác', 26, CORAL).move_to([0, .6, 0])), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('bad', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('total', 1.9))
        self.wait_until(.45, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)


