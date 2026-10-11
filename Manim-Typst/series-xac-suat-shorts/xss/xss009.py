"""XSS009 · Lấy một viên bi — 3 đỏ, 2 xanh: P(đỏ) = 3/5 (bẫy: tỉ số 3/2 không phải xác suất)."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import DOWN, RIGHT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, INK, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS009', 'answer': '3/5'}
PROBLEM = ['Hộp có $3$ bi đỏ, $2$ bi xanh. Lấy ngẫu',
           'nhiên $1$ bi. Xác suất được bi đỏ?']
OPTIONS = ['2/5', '3/5', '3/2']
CORRECT = 1
ANSWER_VALUE = .6

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ và hai bi xanh. Nhắm mắt lấy một viên. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, ba phần năm, hay ba phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đánh số năm viên bi để thấy rõ: viên nào cũng có cùng cơ hội được lấy. '
                        'Không gian mẫu có năm kết quả.'),
    Beat('s2', 'solve', 'Có ba viên đỏ, tức ba kết quả thuận lợi. Xác suất bằng ba phần năm.'),
    Beat('s3', 'solve', 'Ba phần hai là cái bẫy: đó là tỉ số giữa bi đỏ và bi xanh, không phải xác suất. '
                        'Xác suất chia cho tổng số kết quả, nên không bao giờ vượt quá một.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm, tức sáu mươi phần trăm cơ hội lấy được bi đỏ.'),
    Beat('outro', 'outro', outro_text(9)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    n='n(Omega) = 5',
                    prob='P("đỏ") = 3/5',
                    ratio='"đỏ" : "xanh" = 3/2 quad coral(!=) quad P')


def validate() -> bool:
    balls = 'RRRBB'
    assert Fraction(balls.count('R'), len(balls)) == Fraction(3, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS009(ShortScene):
    N = 9

    def hook_visual(self, t0):
        self.u = urn('RRRBB', cols=5, r=.42).move_to([0, 1.3, 0])
        self.wait_until(.25, t0)
        self.play(FadeIn(self.u[0]), FadeIn(self.u.balls, lag_ratio=.2, shift=DOWN * .4), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        nums = VGroup(*[tx(str(i + 1), 26, INK, bold=True).move_to(b) for i, b in enumerate(self.u.balls)])
        self.play(FadeIn(nums, lag_ratio=.2), run_time=self.rt(.15))
        self.nums = nums
        self.wait_until(.55, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        reds, blues = self.u.balls[:3], self.u.balls[3:]
        self.play(reds.animate.shift(UP * .3), self.nums[:3].animate.shift(UP * .3),
                  blues.animate.set_opacity(.3), run_time=self.rt(.1))
        self.play(FadeIn(tx('3 kết quả thuận lợi', 28, GOLD, bold=True).next_to(self.u, UP, buff=.2)),
                  run_time=self.rt(.06))
        self.wait_until(.45, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        r = self.M('ratio', 1.9)
        self.write_board(r, anim='fade')
        self.play(FadeIn(cross(CORAL, .5).next_to(r, RIGHT, buff=.25)), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.write_board(tx('xác suất không bao giờ vượt quá 1', 26, SOFT), anim='fade')
