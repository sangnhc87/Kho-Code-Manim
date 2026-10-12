"""XSS392 · Đỏ hay hai vàng liền? — R, B, Y mỗi màu 1/3; trạng thái 0 (vừa không rút vàng) và 1 (vừa rút vàng):
x₀ = 1/3 + x₀/3 + x₁/3, x₁ = 1/3 + x₀/3 → x₀ = 4/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS392', 'answer': '4/5'}
PROBLEM = ['Rút có hoàn lại từ hộp $1$ đỏ $1$ xanh $1$',
           'vàng; dừng khi rút được đỏ hoặc $2$ lần',
           'liên tiếp vàng. Xác suất dừng vì đỏ?']
OPTIONS = ['4/5', '2/3', '3/4']
CORRECT = 0
ANSWER_VALUE = .8


def solve():
    # x1 = 1/3 + x0/3  →  x0 = 1/3 + x0/3 + (1/3 + x0/3)/3  →  x0 (1 - 1/3 - 1/9) = 1/3 + 1/9
    x0 = (F(1, 3) + F(1, 9)) / (1 - F(1, 3) - F(1, 9))
    return x0, F(1, 3) + x0 / 3


BEATS = [
    Beat('hook', 'hook', 'Hộp có một bi đỏ, một xanh, một vàng. Rút có hoàn lại; dừng khi rút được đỏ, hoặc khi có hai lần liên tiếp rút vàng. '
                         'Xác suất trò chơi dừng vì bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Bốn phần năm, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai trạng thái: x không khi lần trước không phải vàng, x một khi lần trước vừa ra vàng. Mỗi lần rút, mỗi màu một phần ba.'),
    Beat('s2', 'solve', 'Từ trạng thái không: đỏ thì thắng, xanh thì ở lại, vàng thì sang trạng thái một. Từ trạng thái một: đỏ thắng, xanh về không, vàng thì dừng vì hai vàng.'),
    Beat('s3', 'solve', 'Giải hệ: x một bằng một phần ba cộng x không chia ba; thế vào được x không bằng bốn phần năm.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần năm. Điều kiện dừng phụ thuộc lần trước: thêm trạng thái để nhớ.'),
    Beat('outro', 'outro', outro_text(392)),
]

FORMULAS = formulas('4/5', OPTIONS,
                    sys='x_0 = 1/3 + 1/3 x_0 + 1/3 x_1, quad x_1 = 1/3 + 1/3 x_0',
                    prob='x_0 = 4/5, quad x_1 = 3/5')


def validate() -> bool:
    x0, x1 = solve()
    assert x0 == F(4, 5) and x1 == F(3, 5)
    assert x0 == F(1, 3) + x0 / 3 + x1 / 3
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS392(ShortScene):
    N = 392

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RBY', cols=3, r=.32).move_to([0, 2.1, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.ex = VGroup(ball_row('BYBR', r=.3, buff=.2), ball_row('YBYY', r=.3, buff=.2)).arrange(buff=1.0).move_to([0, .6, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.ex, lag_ratio=.3), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.play(self.ex.animate.set_opacity(.3), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('sys', 1.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
