"""XSS390 · Đỏ lần hai ở lần năm — có hoàn lại, p = 1/3; đỏ thứ hai ở lần 5: C(4;1)·(1/3)²·(2/3)³ = 32/243."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS390', 'answer': '32/243'}
PROBLEM = ['Rút có hoàn lại từ hộp $1$ đỏ $2$ xanh',
           'đến khi được bi đỏ lần thứ hai. Xác suất',
           'dừng ở lần rút thứ $5$?']
OPTIONS = ['32/243', '8/81', '16/243']
CORRECT = 0
ANSWER_VALUE = 32 / 243
R = F(1, 3)


def stop5():
    tot = F(0)
    for s in product('RB', repeat=5):
        if s[4] == 'R' and s[:4].count('R') == 1:
            pr = F(1)
            for c in s:
                pr *= R if c == 'R' else 1 - R
            tot += pr
    return tot


BEATS = [
    Beat('hook', 'hook', 'Hộp có một bi đỏ, hai bi xanh. Rút có hoàn lại cho đến khi được bi đỏ lần thứ hai. '
                         'Xác suất dừng ở đúng lần rút thứ năm?'),
    Beat('guess', 'hook', 'Ba mươi hai phần hai trăm bốn mươi ba, tám phần tám mươi mốt, hay mười sáu phần hai trăm bốn mươi ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở lần năm: lần năm đỏ, và bốn lần trước có đúng một đỏ. Bi đỏ đó có bốn vị trí để chọn.'),
    Beat('s2', 'solve', 'Mỗi dãy như vậy có hai đỏ và ba xanh: một phần ba bình phương nhân hai phần ba mũ ba, bằng tám phần hai trăm bốn mươi ba.'),
    Beat('s3', 'solve', 'Nhân bốn vị trí: ba mươi hai phần hai trăm bốn mươi ba, khoảng mười ba phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi hai phần hai trăm bốn mươi ba. Lần cuối cố định, chỉ chọn vị trí các lần thành công trước đó.'),
    Beat('outro', 'outro', outro_text(390)),
]

FORMULAS = formulas('32/243', OPTIONS,
                    one='(1/3)^2 (2/3)^3 = 8/243',
                    prob='P = C_4^1 dot 8/243 = 32/243')


def validate() -> bool:
    assert stop5() == F(32, 243)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS390(ShortScene):
    N = 390

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.u = urn('RBB', cols=3, r=.3).move_to([0, 2.15, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.rows = VGroup(*[ball_row(''.join('R' if j in (i, 4) else 'B' for j in range(5)), r=.24, buff=.12) for i in range(4)]) \
            .arrange(DOWN, buff=.18).move_to([0, .45, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(self.rows[0]), FadeIn(self.rows[2:]), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('one', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
