"""XSS310 · Tiến, tiến hai, lùi — 3 lượt, mỗi lượt +1, +2, −1 như nhau; ở đúng vị trí 3: (+1,+1,+1) và hoán vị (+2,+2,−1) → 4/27."""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import RIGHT, Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS310', 'answer': '4/27'}
PROBLEM = ['Mỗi lượt đi $+1$, $+2$ hoặc $-1$ như nhau.',
           'Xuất phát ở $0$. Xác suất sau $3$ lượt',
           'đứng đúng ở vị trí $3$?']
OPTIONS = ['1/9', '4/27', '2/9']
CORRECT = 1
ANSWER_VALUE = 4 / 27
GOOD = [s for s in itertools.product((1, 2, -1), repeat=3) if sum(s) == 3]

BEATS = [
    Beat('hook', 'hook', 'Một quân cờ trên trục số, mỗi lượt tiến một, tiến hai hoặc lùi một bước, ba khả năng như nhau. '
                         'Sau ba lượt, xác suất nó đứng đúng ở vị trí ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần chín, bốn phần hai mươi bảy, hay hai phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có ba mũ ba bằng hai mươi bảy dãy bước đồng khả năng. Gọi a, b, c là số lần tiến một, tiến hai và lùi một.'),
    Beat('s2', 'solve', 'Ta cần a cộng b cộng c bằng ba và a cộng hai b trừ c bằng ba. Trừ hai phương trình: b bằng hai lần c.'),
    Beat('s3', 'solve', 'Nếu c bằng không thì ba lần tiến một: một dãy. Nếu c bằng một thì hai lần tiến hai và một lần lùi: ba cách xếp thứ tự.'),
    Beat('s4', 'solve', 'Tổng cộng bốn dãy thuận lợi trên hai mươi bảy, tức bốn phần hai mươi bảy.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần hai mươi bảy. Đếm theo số lần mỗi loại bước, rồi nhân số cách xếp thứ tự.'),
    Beat('outro', 'outro', outro_text(310)),
]

FORMULAS = formulas('4/27', OPTIONS,
                    sys1='a + b + c = 3, quad a + 2b - c = 3',
                    bc='b = 2c',
                    cases='(+1, +1, +1): 1, quad (+2, +2, -1): 3',
                    prob='P = (1 + 3)/27 = 4/27')


def validate() -> bool:
    assert len(GOOD) == 4
    assert F(len(GOOD), 27) == F(4, 27)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS310(ShortScene):
    N = 310

    def hook_visual(self, t0):
        self.board_top = -1.0
        X = lambda k: -3.0 + 1.0 * (k + 1)  # noqa: E731
        self.X = X
        line = Line([X(-1) - .3, 1.0, 0], [X(5) + .3, 1.0, 0], color=STROKE, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([X(k), .88, 0], [X(k), 1.12, 0], color=SOFT, stroke_width=3),
                                self.TM(f'${k}$', 28, GOLD if k == 3 else SOFT).move_to([X(k), .6, 0])) for k in range(-1, 6)])
        self.axis = VGroup(line, ticks)
        self.p = Dot([X(0), 1.0, 0], radius=.16, color=CYAN)
        self.play(FadeIn(self.axis), FadeIn(self.p), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        for d in (2, -1, 2):
            self.play(self.p.animate.shift(RIGHT * d), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.p.animate.move_to([self.X(0), 1.0, 0]), run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.TM('$3^3 = 27$ dãy đồng khả năng', 30, SOFT), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('sys1', 1.5))
        self.wait_until(.6, t0)
        m = self.M('bc', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.clear_board(.03)
        rows = VGroup(*[self.TM('$(' + ', '.join(f'{d:+d}' for d in s) + ')$', 28, GREEN) for s in GOOD]) \
            .arrange_in_grid(rows=2, cols=2, buff=(.6, .18)).move_to([0, -.25, 0])
        self.play(FadeIn(rows, lag_ratio=.3), run_time=self.rt(.2))
        self.write_board(self.M('cases', 1.6))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
