"""XSS384 · Hai phát trúng liền — bắn tối đa 4 viên, p = 0,6; không có 2 trúng liền: 0,4⁴ + 4·0,6·0,4³ + 3·0,6²·0,4² = 44/125 → 81/125."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS384', 'answer': '81/125'}
PROBLEM = ['Bắn đến khi trúng $2$ phát liên tiếp hoặc',
           'hết $4$ viên, mỗi phát trúng $"0,6"$. Xác suất',
           'dừng vì trúng $2$ phát liên tiếp?']
OPTIONS = ['81/125', '18/25', '27/50']
CORRECT = 0
ANSWER_VALUE = 81 / 125
P = F(3, 5)
NOHH = [s for s in product((1, 0), repeat=4) if not any(s[i] and s[i + 1] for i in range(3))]


def prob(s):
    out = F(1)
    for x in s:
        out *= P if x else 1 - P
    return out


BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ có bốn viên đạn, bắn cho đến khi trúng hai phát liên tiếp hoặc hết đạn. Mỗi phát trúng với xác suất không phẩy sáu. '
                         'Xác suất dừng vì trúng hai phát liên tiếp?'),
    Beat('guess', 'hook', 'Tám mươi mốt phần một trăm hai mươi lăm, mười tám phần hai mươi lăm, hay hai mươi bảy phần năm mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dùng phần bù: bắn hết bốn viên mà không có hai phát trúng liền nhau. Liệt kê theo số phát trúng.'),
    Beat('s2', 'solve', 'Không trúng phát nào: một dãy. Trúng một phát: bốn dãy. Trúng hai phát không kề: ba dãy. Ba phát trở lên chắc chắn có hai phát kề nhau.'),
    Beat('s3', 'solve', 'Xác suất phần bù: không phẩy bốn mũ bốn, cộng bốn nhân không phẩy sáu nhân không phẩy bốn mũ ba, cộng ba nhân không phẩy sáu bình phương nhân không phẩy bốn bình phương, bằng bốn mươi bốn phần một trăm hai mươi lăm.'),
    Beat('s4', 'solve', 'Vậy xác suất dừng vì trúng liền là tám mươi mốt phần một trăm hai mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: tám mươi mốt phần một trăm hai mươi lăm. Với điều kiện dừng phức tạp, đếm các dãy không dừng thường dễ hơn.'),
    Beat('outro', 'outro', outro_text(384)),
]

FORMULAS = formulas('81/125', OPTIONS,
                    comp='"0,4"^4 + 4 dot "0,6" dot "0,4"^3 + 3 dot "0,6"^2 dot "0,4"^2 = 44/125',
                    prob='P = 1 - 44/125 = 81/125')


def validate() -> bool:
    assert len(NOHH) == 8 and sum(prob(s) for s in NOHH) == F(44, 125)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS384(ShortScene):
    N = 384

    def hook_visual(self, t0):
        self.board_top = -1.6
        rows = VGroup()
        for s in NOHH:
            rows.add(VGroup(*[token('T' if x else 'X', GREEN if x else CORAL, .2) for x in s]).arrange(buff=.08))
        self.rows = rows.arrange_in_grid(rows=4, cols=2, buff=(.8, .22)).move_to([0, .8, 0])
        self.wait_until(.6, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows[0]), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[1:5], lag_ratio=.2), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.rows[5:], lag_ratio=.2), run_time=self.rt(.12))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('comp', 1.05))

    def beat_s4(self, T):
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
