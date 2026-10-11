"""XSS023 · Hai bi đỏ — 4 đỏ 3 xanh, lấy 2: C(4,2)/C(7,2) = 6/21 = 2/7."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

from manim import UP, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS023', 'answer': '2/7'}
PROBLEM = ['Hộp có $4$ bi đỏ, $3$ bi xanh.', 'Lấy ngẫu nhiên $2$ bi. Xác suất cả hai đỏ?']
OPTIONS = ['4/7', '2/7', '16/49']
CORRECT = 1
ANSWER_VALUE = 2 / 7

BEATS = [
    Beat('hook', 'hook', 'Hộp có bốn bi đỏ và ba bi xanh. Lấy cùng lúc hai viên. Xác suất cả hai viên đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Bốn phần bảy, hai phần bảy, hay mười sáu phần bốn mươi chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lấy cùng lúc hai viên từ bảy viên, không quan tâm thứ tự: đó là tổ hợp chập hai của bảy, '
                        'bằng hai mươi mốt cách.'),
    Beat('s2', 'solve', 'Muốn cả hai đều đỏ, ta chọn hai viên trong bốn viên đỏ: tổ hợp chập hai của bốn, bằng sáu cách.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần hai mươi mốt, rút gọn còn hai phần bảy. '
                        'Đáp án mười sáu phần bốn mươi chín chỉ đúng khi lấy có hoàn lại.'),
    Beat('answer', 'solve', 'Đáp án: hai phần bảy. Công thức vàng: số cách chọn thuận lợi chia số cách chọn tất cả.'),
    Beat('outro', 'outro', outro_text(23)),
]

FORMULAS = formulas('2/7', OPTIONS,
                    n='n(Omega) = C_7^2 = 21',
                    a='n(A) = C_4^2 = 6',
                    prob='P(A) = 6/21 = 2/7',
                    back='"có hoàn lại:" quad (4/7)^2 = 16/49')


def validate() -> bool:
    balls = ['R'] * 4 + ['B'] * 3
    pairs = list(combinations(range(7), 2))
    assert comb(7, 2) == 21 and comb(4, 2) == 6
    assert Fraction(sum(balls[i] == balls[j] == 'R' for i, j in pairs), len(pairs)) == Fraction(2, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS023(ShortScene):
    N = 23

    def hook_visual(self, t0):
        self.u = urn('RRRRBBB', cols=4, r=.42).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.u[0]), FadeIn(self.u.balls, lag_ratio=.15), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.u.balls[0].animate.shift(UP * 1.6 + [-.6, 0, 0]),
                  self.u.balls[5].animate.shift(UP * 1.6), run_time=self.rt(.12))
        self.play(self.u.balls[0].animate.shift(UP * -1.6 + [.6, 0, 0]),
                  self.u.balls[5].animate.shift(UP * -1.6), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        reds, blues = self.u.balls[:4], self.u.balls[4:]
        self.play(reds.animate.shift(UP * .25), blues.animate.set_opacity(.3), run_time=self.rt(.1))
        self.play(FadeIn(tx('chọn 2 trong 4 bi đỏ', 28, GOLD, bold=True).next_to(self.u, UP, buff=.2)),
                  run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('a', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(self.M('back', 1.5), anim='fade')
        self.write_board(tx('chỉ khi lấy có hoàn lại', 24, CORAL), anim='fade')


