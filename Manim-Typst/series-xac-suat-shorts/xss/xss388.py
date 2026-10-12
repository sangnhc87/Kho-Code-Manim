"""XSS388 · Vòng quay ba ô — quay đúng 3 lần ⇔ 2 lần đầu không ra C, lần 3 ra C; khi đó mỗi lần đầu là A với 3/5 → 1 − (2/5)² = 21/25."""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import AnnularSector, FadeIn, Rotate, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, INK  # noqa: E402
from common.kit import tx  # noqa: E402

EPISODE = {'code': 'XSS388', 'answer': '21/25'}
PROBLEM = ['Vòng quay A ($1/2$), B ($1/3$), C ($1/6$);',
           'quay đến khi ra C. Biết quay đúng $3$',
           'lần. Xác suất có ít nhất $1$ lần ra A?']
OPTIONS = ['21/25', '3/4', '5/9']
CORRECT = 0
ANSWER_VALUE = 21 / 25
PR = {'A': F(1, 2), 'B': F(1, 3)}


def cond_prob():
    num = den = F(0)
    for s in product('AB', repeat=2):
        w = PR[s[0]] * PR[s[1]] * F(1, 6)
        den += w
        num += w * ('A' in s)
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Một vòng quay có ba ô: A chiếm một nửa, B một phần ba, C một phần sáu. Quay cho đến khi ra C thì dừng. Biết đã quay đúng ba lần. '
                         'Xác suất có ít nhất một lần ra A?'),
    Beat('guess', 'hook', 'Hai mươi mốt phần hai mươi lăm, ba phần tư, hay năm phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Quay đúng ba lần: hai lần đầu không ra C, lần ba ra C. Lần ba không liên quan đến câu hỏi.'),
    Beat('s2', 'solve', 'Biết một lần quay không ra C, nó là A với xác suất một phần hai chia năm phần sáu, tức ba phần năm; là B với hai phần năm.'),
    Beat('s3', 'solve', 'Không có A nào nghĩa là hai lần đều B: hai phần năm bình phương, bốn phần hai mươi lăm. Vậy có ít nhất một A: hai mươi mốt phần hai mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi mốt phần hai mươi lăm. Biết thời điểm dừng, các lần trước trở thành phép thử có điều kiện độc lập.'),
    Beat('outro', 'outro', outro_text(388)),
]

FORMULAS = formulas('21/25', OPTIONS,
                    a='P(A | "không C") = (1/2)/(5/6) = 3/5',
                    prob='P = 1 - (2/5)^2 = 21/25')


def validate() -> bool:
    assert cond_prob() == F(21, 25)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS388(ShortScene):
    N = 388

    def hook_visual(self, t0):
        self.board_top = -1.3
        c = [0, .9, 0]
        parts = [('A', CYAN, .5), ('B', GOLD, 1 / 3), ('C', CORAL, 1 / 6)]
        wheel, start = VGroup(), 0
        for lab, col, frac in parts:
            ang = frac * 6.2832
            sec = AnnularSector(inner_radius=0, outer_radius=1.6, angle=ang, start_angle=start, color=col, fill_opacity=.85).move_arc_center_to(c)
            mid = start + ang / 2
            wheel.add(VGroup(sec, tx(lab, 36, INK, bold=True).move_to([c[0] + math.cos(mid), c[1] + math.sin(mid), 0])))
            start += ang
        self.wheel = wheel
        self.wait_until(.45, t0)
        self.play(FadeIn(wheel), run_time=self.rt(.06))
        self.play(Rotate(wheel, 6.2832 * 1.5, about_point=c), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.wheel[2].animate.set_opacity(.25), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('a', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
