"""XSS329 · Bi đầu và bi cuối — 4 đỏ 4 xanh rút hết: vị trí đầu và cuối như hai lần rút đầu tiên → 4/8 · 3/7 = 3/14."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, SurroundingRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS329', 'answer': '3/14'}
PROBLEM = ['Hộp có $4$ bi đỏ, $4$ bi xanh. Rút lần lượt',
           'đến hết. Xác suất bi đầu tiên và bi cuối',
           'cùng đều là bi đỏ?']
OPTIONS = ['1/4', '3/14', '2/7']
CORRECT = 1
ANSWER_VALUE = 3 / 14
ORDERS = set(permutations('RRRRBBBB'))

BEATS = [
    Beat('hook', 'hook', 'Hộp có bốn bi đỏ và bốn bi xanh. Rút lần lượt từng bi cho đến hết, xếp thành một hàng. '
                         'Xác suất bi đầu tiên và bi cuối cùng đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, ba phần mười bốn, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo đối xứng: mọi thứ tự rút đều đồng khả năng, nên cặp vị trí đầu và cuối cũng giống hệt cặp hai lần rút đầu tiên.'),
    Beat('s2', 'solve', 'Bi đầu đỏ với xác suất bốn phần tám. Biết bi đầu đỏ, bi cuối là một trong bảy bi còn lại, có ba bi đỏ: xác suất ba phần bảy.'),
    Beat('s3', 'solve', 'Nhân lại: bốn phần tám nhân ba phần bảy bằng ba phần mười bốn.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười bốn. Rút hết rồi nhìn vị trí nào cũng như rút hai bi đầu tiên.'),
    Beat('outro', 'outro', outro_text(329)),
]

FORMULAS = formulas('3/14', OPTIONS,
                    sym='P("đầu", "cuối") = P("lần 1", "lần 2")',
                    prob='P = 4/8 dot 3/7 = 3/14')


def validate() -> bool:
    good = sum(o[0] == 'R' and o[-1] == 'R' for o in ORDERS)
    assert F(good, len(ORDERS)) == F(3, 14)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS329(ShortScene):
    N = 329

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRRRBBBB', cols=4, r=.3).move_to([0, 1.9, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.row = ball_row('RBBRBRBR', y=.05, r=.3)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.row, lag_ratio=.2), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        box = VGroup(SurroundingRectangle(self.row[0], color=GOLD, buff=.08), SurroundingRectangle(self.row[-1], color=GOLD, buff=.08))
        self.play(FadeIn(box), run_time=self.rt(.06))
        self.write_board(self.M('sym', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.row[0].animate.scale(1.3), run_time=self.rt(.05))
        self.wait_until(.65, t0)
        self.play(self.row[-1].animate.scale(1.3), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
