"""XSS179 · Bàn tròn xen kẽ — cố định 1 nam: nam vào 3 ghế lẻ 3!, nữ vào 4 ghế 4!, trên 7!: 1/35."""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import Circle, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, PANEL, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS179', 'answer': '1/35'}
PROBLEM = ['$4$ nam, $4$ nữ ngồi ngẫu nhiên quanh',
           'một bàn tròn $8$ ghế. Xác suất',
           'nam nữ ngồi xen kẽ?']
OPTIONS = ['1/70', '1/35', '1/8']
CORRECT = 1
ANSWER_VALUE = 1 / 35

BEATS = [
    Beat('hook', 'hook', 'Bốn bạn nam và bốn bạn nữ ngồi ngẫu nhiên quanh một bàn tròn có tám ghế. '
                         'Xác suất nam và nữ ngồi xen kẽ hoàn toàn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần bảy mươi, một phần ba mươi lăm, hay một phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bàn tròn không có chỗ đầu, nên cố định một bạn nam vào một ghế. Bảy người còn lại xếp vào bảy ghế: bảy giai thừa cách.'),
    Beat('s2', 'solve', 'Muốn xen kẽ, ba ghế cách bạn nam đó một ghế dành cho ba nam còn lại: ba giai thừa cách; '
                        'bốn ghế xen giữa dành cho bốn nữ: bốn giai thừa cách.'),
    Beat('s3', 'solve', 'Xác suất bằng ba giai thừa nhân bốn giai thừa chia bảy giai thừa, bằng một trăm bốn mươi bốn phần năm nghìn không trăm bốn mươi, '
                        'tức một phần ba mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba mươi lăm. Với bàn tròn, cố định một người là bước đầu tiên!'),
    Beat('outro', 'outro', outro_text(179)),
]

FORMULAS = formulas('1/35', OPTIONS,
                    total='n(Omega) = 7! = 5040',
                    good='n(A) = 3! dot 4! = 144',
                    prob='P = 144/5040 = 1/35')


def validate() -> bool:
    good = sum(all((('M' + ''.join(s)) * 2)[i] != (('M' + ''.join(s)) * 2)[i + 1] for i in range(8))
               for s in permutations('MMMFFFF'))
    assert F(good, factorial(7)) == F(1, 35) == F(factorial(3) * factorial(4), factorial(7))
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS179(ShortScene):
    N = 179

    def hook_visual(self, t0):
        self.board_top = -1.3
        c = (0, 1.25)
        self.table = Circle(radius=1.2, stroke_color=SOFT, fill_color=PANEL, fill_opacity=1).move_to([*c, 0])
        self.pos = [[c[0] + 2.0 * math.cos(math.pi / 2 - k * math.pi / 4), c[1] + 2.0 * math.sin(math.pi / 2 - k * math.pi / 4), 0]
                    for k in range(8)]
        self.seats = VGroup(*[token(' ', SOFT, .3).move_to(p) for p in self.pos])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.table), FadeIn(self.seats, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.fixed_boy = token('M', CYAN, .32).move_to(self.pos[0])
        self.play(FadeIn(self.fixed_boy, scale=1.5), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.write_board(self.M('total', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        boys = VGroup(*[token('M', CYAN, .32).move_to(self.pos[k]) for k in (2, 4, 6)])
        girls = VGroup(*[token('F', CORAL, .32).move_to(self.pos[k]) for k in (1, 3, 5, 7)])
        self.play(FadeIn(boys, lag_ratio=.2), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(girls, lag_ratio=.2), run_time=self.rt(.1))
        self.write_board(self.M('good', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
