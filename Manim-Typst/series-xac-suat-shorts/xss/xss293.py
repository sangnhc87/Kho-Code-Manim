"""XSS293 · Ếch giữa hai bờ — lá 1 và 4 là bờ, ếch ở lá 2, ±1 (1/2): P(lên bờ ở 4) = (2 − 1)/(4 − 1) = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS293', 'answer': '1/3'}
PROBLEM = ['Lá $1$, $2$, $3$, $4$ thẳng hàng; lá $1$ và',
           '$4$ là hai bờ. Ếch ở lá $2$, mỗi bước',
           'nhảy $plus.minus 1$ ($1/2$). Xác suất',
           'ếch lên bờ ở lá $4$?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 3


def solve():
    # x2 = (1/2)·0 + (1/2) x3, x3 = (1/2) x2 + (1/2)·1
    x2 = F(1, 4) / (1 - F(1, 4))
    return x2


BEATS = [
    Beat('hook', 'hook', 'Bốn lá sen thẳng hàng, lá một và lá bốn là hai bờ sông. Ếch đứng ở lá hai, mỗi bước nhảy sang trái hoặc phải một lá. '
                         'Xác suất ếch lên bờ ở phía lá bốn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi x hai, x ba là xác suất lên bờ lá bốn khi đứng ở lá hai, lá ba. Từ lá hai: nửa sang bờ một, thua; nửa sang lá ba.'),
    Beat('s2', 'solve', 'Từ lá ba: nửa lên bờ bốn, thắng; nửa về lá hai. Hệ: x hai bằng nửa x ba, x ba bằng nửa x hai cộng một nửa.'),
    Beat('s3', 'solve', 'Giải ra x hai bằng một phần ba. Quy luật đẹp: xác suất tỉ lệ với khoảng cách tới bờ bên kia, một trên ba khoảng.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Đi ngẫu nhiên đối xứng giữa hai bờ: xác suất tuyến tính theo vị trí!'),
    Beat('outro', 'outro', outro_text(293)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    sys='x_2 = 1/2 x_3, quad x_3 = 1/2 x_2 + 1/2',
                    sol='x_2 = 1/3 = (2 - 1)/(4 - 1)')


def validate() -> bool:
    x2 = solve()
    assert x2 == F(1, 3) and F(1, 2) * x2 + F(1, 2) == 2 * x2
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS293(ShortScene):
    N = 293

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(1, 5), y=1.15, gap=1.4)
        self.row[0].set_fill(CORAL, .8)
        self.row[-1].set_fill(GREEN, .8)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, SOFT).next_to(q, [0, -1, 0], buff=.15) for k, q in zip(range(1, 5), self.row)])
        self.fr = frog().move_to(self.row[1])
        self.wait_until(.75, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.fr.animate.move_to(self.row[2]), run_time=self.rt(.04))
        self.play(self.fr.animate.move_to(self.row[1]), run_time=self.rt(.04))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        self.write_board(self.M('sys', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)
