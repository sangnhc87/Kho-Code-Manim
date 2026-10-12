"""XSS379 · Đủ hai đỏ ở lần bốn — 3đ3x rút đến khi đủ 2 đỏ; dừng ở lần 4: 1 đỏ trong 3 lần đầu, lần 4 đỏ: C(3;1)·C(2;1)/C(6;3) = 6/20 = 3/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS379', 'answer': '3/10'}
PROBLEM = ['Hộp $3$ đỏ $3$ xanh, rút lần lượt đến khi',
           'được $2$ bi đỏ. Xác suất dừng ở lần thứ $4$?']
OPTIONS = ['3/10', '1/4', '1/5']
CORRECT = 0
ANSWER_VALUE = .3
ORDERS = set(permutations('RRRBBB'))


def stop(o):
    return [i for i, c in enumerate(o) if c == 'R'][1] + 1


BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ, ba bi xanh. Rút lần lượt không hoàn lại cho đến khi được hai bi đỏ. '
                         'Xác suất phải dừng ở đúng lần rút thứ tư?'),
    Beat('guess', 'hook', 'Ba phần mười, một phần tư, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tưởng tượng rút hết sáu bi thành một hàng. Mỗi cách đặt ba bi đỏ vào sáu vị trí đồng khả năng: hai mươi cách.'),
    Beat('s2', 'solve', 'Dừng ở lần bốn: vị trí bốn là đỏ, ba vị trí đầu có đúng một đỏ, ba cách, và bi đỏ còn lại ở vị trí năm hoặc sáu, hai cách.'),
    Beat('s3', 'solve', 'Sáu cách trên hai mươi, tức ba phần mười.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười. Quá trình dừng không hoàn lại: rút hết rồi đếm vị trí.'),
    Beat('outro', 'outro', outro_text(379)),
]

FORMULAS = formulas('3/10', OPTIONS,
                    all='C_6^3 = 20',
                    good='C_3^1 dot C_2^1 = 6',
                    prob='P = 6/20 = 3/10')


def validate() -> bool:
    assert F(sum(stop(o) == 4 for o in ORDERS), len(ORDERS)) == F(3, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS379(ShortScene):
    N = 379

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRRBBB', cols=3, r=.3).move_to([0, 2.1, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.row = ball_row('BRBRBR', y=.6, r=.34, buff=.25)
        self.play(FadeIn(self.row, lag_ratio=.2), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.row[3].animate.scale(1.3), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
