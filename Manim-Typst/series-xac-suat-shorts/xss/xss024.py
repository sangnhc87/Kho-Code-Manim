"""XSS024 · Hai bi khác màu — 4 đỏ 3 xanh, lấy 2: 4·3/21 = 4/7."""
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
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS024', 'answer': '4/7'}
PROBLEM = ['Hộp có $4$ bi đỏ, $3$ bi xanh. Lấy $2$ bi.', 'Xác suất hai bi khác màu?']
OPTIONS = ['1/2', '4/7', '2/7']
CORRECT = 1
ANSWER_VALUE = 4 / 7

BEATS = [
    Beat('hook', 'hook', 'Vẫn hộp bốn bi đỏ, ba bi xanh. Lấy cùng lúc hai viên. Xác suất được hai viên khác màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, bốn phần bảy, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Như thử thách trước, có hai mươi mốt cách lấy hai viên từ bảy viên.'),
    Beat('s2', 'solve', 'Hai viên khác màu nghĩa là một đỏ, một xanh. Chọn một viên đỏ có bốn cách, '
                        'một viên xanh có ba cách. Theo quy tắc nhân: bốn nhân ba bằng mười hai cách.'),
    Beat('s3', 'solve', 'Xác suất bằng mười hai phần hai mươi mốt, tức bốn phần bảy. Kiểm tra chéo: cùng màu gồm '
                        'hai đỏ sáu cách và hai xanh ba cách, tổng chín cách. Mười hai cộng chín đúng bằng hai mươi mốt!'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Lấy hai viên thì khác màu dễ xảy ra hơn cùng màu.'),
    Beat('outro', 'outro', outro_text(24)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    n='n(Omega) = C_7^2 = 21',
                    a='n(A) = 4 dot 3 = 12',
                    prob='P(A) = 12/21 = 4/7',
                    check='C_4^2 + C_3^2 + 12 = 6 + 3 + 12 = 21')


def validate() -> bool:
    balls = ['R'] * 4 + ['B'] * 3
    pairs = list(combinations(range(7), 2))
    assert Fraction(sum(balls[i] != balls[j] for i, j in pairs), len(pairs)) == Fraction(4, 7)
    assert comb(4, 2) + comb(3, 2) + 12 == 21
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS024(ShortScene):
    N = 24

    def hook_visual(self, t0):
        self.u = urn('RRRRBBB', cols=4, r=.42).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.u[0]), FadeIn(self.u.balls, lag_ratio=.15), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        r, b = self.u.balls[1], self.u.balls[5]
        self.play(r.animate.shift(UP * .5).scale(1.2), b.animate.shift(UP * .5).scale(1.2), run_time=self.rt(.08))
        self.play(FadeIn(tx('1 đỏ + 1 xanh', 30, GOLD, bold=True).next_to(self.u, UP, buff=.25)), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.write_board(self.M('a', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.write_board(self.M('check', 1.5), anim='fade')
        self.write_board(tx('kiểm tra chéo: đủ 21 cách', 24, SOFT), anim='fade')
