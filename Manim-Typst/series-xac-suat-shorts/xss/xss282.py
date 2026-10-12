"""XSS282 · Ếch thích nhảy tới — 4 bước, vị trí 2 ⇔ 3 tới 1 lùi: C(4,1)·(2/3)³·(1/3) = 32/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS282', 'answer': '32/81'}
PROBLEM = ['Ếch trên trục số, mỗi bước nhảy $+1$',
           'với xác suất $2/3$ hoặc $-1$. Xác suất',
           'sau $4$ bước ếch ở vị trí $2$?']
OPTIONS = ['16/81', '32/81', '8/27']
CORRECT = 1
ANSWER_VALUE = 32 / 81

BEATS = [
    Beat('hook', 'hook', 'Chú ếch trên trục số thích nhảy tới: mỗi bước nhảy lên một với xác suất hai phần ba, lùi một với xác suất một phần ba. '
                         'Sau bốn bước, xác suất ếch ở đúng vị trí hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười sáu phần tám mươi mốt, ba mươi hai phần tám mươi mốt, hay tám phần hai mươi bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vị trí cuối bằng số bước tới trừ số bước lùi. Tới cộng lùi bằng bốn, tới trừ lùi bằng hai: ba bước tới, một bước lùi.'),
    Beat('s2', 'solve', 'Bước lùi có thể ở một trong bốn vị trí: tổ hợp chập một của bốn. Mỗi dãy có xác suất hai phần ba mũ ba nhân một phần ba.'),
    Beat('s3', 'solve', 'Xác suất bằng bốn nhân tám phần hai mươi bảy nhân một phần ba, tức ba mươi hai phần tám mươi mốt. Đây là Bernoulli đội lốt bài đi ngẫu nhiên!'),
    Beat('answer', 'solve', 'Đáp án: ba mươi hai phần tám mươi mốt. Đi ngẫu nhiên trên trục: đổi vị trí thành số bước tới và lùi!'),
    Beat('outro', 'outro', outro_text(282)),
]

FORMULAS = formulas('32/81', OPTIONS,
                    sys='a + b = 4, quad a - b = 2 arrow.r.double a = 3, quad b = 1',
                    prob='P = C_4^1 (2/3)^3 (1/3) = 32/81')


def validate() -> bool:
    p = sum(F(2, 3) ** w.count(1) * F(1, 3) ** w.count(-1) for w in product((1, -1), repeat=4) if sum(w) == 2)
    assert p == F(32, 81)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS282(ShortScene):
    N = 282

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.row = pads(range(-2, 5), y=1.8, gap=.95, r=.36)
        self.labs = VGroup(*[self.TM(f'${k}$', 24, GOLD if k == 2 else SOFT).next_to(p, [0, -1, 0], buff=.12)
                             for k, p in zip(range(-2, 5), self.row)])
        self.fr = frog(.18).move_to(self.row[2])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        for k in (3, 4, 3, 4):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.M('sys', 1.7))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('$-1$ ở $1$ trong $4$ vị trí', 30, GOLD))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
