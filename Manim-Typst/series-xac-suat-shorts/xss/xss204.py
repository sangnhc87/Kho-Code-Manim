"""XSS204 · Bi đỏ duy nhất từ đâu? — đúng 1 đỏ: 1/32, 3/32, 9/32 → hộp 3: 9/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS204', 'answer': '9/13'}
PROBLEM = ['Hộp thứ $k$ có $k$ đỏ, $4 - k$ xanh',
           '($k = 1, 2, 3$). Rút mỗi hộp $1$ bi, được',
           'đúng $1$ đỏ. Xác suất bi đỏ từ hộp $3$?']
OPTIONS = ['1/3', '9/13', '3/4']
CORRECT = 1
ANSWER_VALUE = 9 / 13
BOXES = ('RBBB', 'RRBB', 'RRRB')

BEATS = [
    Beat('hook', 'hook', 'Vẫn ba hộp đó: hộp k có k bi đỏ. Rút mỗi hộp một bi, được đúng một bi đỏ. '
                         'Xác suất bi đỏ đó đến từ hộp ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, chín phần mười ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Liệt kê ba khả năng có đúng một đỏ. Đỏ ở hộp một: một phần tư nhân một phần hai nhân một phần tư, một phần ba mươi hai. '
                        'Đỏ ở hộp hai: ba phần tư nhân một phần hai nhân một phần tư, ba phần ba mươi hai.'),
    Beat('s2', 'solve', 'Đỏ ở hộp ba: ba phần tư nhân một phần hai nhân ba phần tư, chín phần ba mươi hai. '
                        'Tổng mười ba phần ba mươi hai.'),
    Beat('s3', 'solve', 'Bayes: chín phần mười ba. Hộp ba vừa dễ ra đỏ, vừa khiến hai hộp kia dễ ra xanh, nên chiếm ưu thế lớn.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười ba. Đa hộp, điều kiện "đúng một": liệt kê vị trí rồi lấy tỉ lệ!'),
    Beat('outro', 'outro', outro_text(204)),
]

FORMULAS = formulas('9/13', OPTIONS,
                    cases='1/32, quad 3/32, quad 9/32',
                    prob='P = (9/32)/(13/32) = 9/13')


def validate() -> bool:
    ws = [w for w in product(*BOXES) if sum(c == 'R' for c in w) == 1]
    assert F(sum(w[2] == 'R' for w in ws), len(ws)) == F(9, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS204(ShortScene):
    N = 204

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.urns = urn_row([(b, f'hộp {k}', SOFT) for k, b in enumerate(BOXES, 1)], buff=.45)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.rows = VGroup(*[VGroup(*[token('Đ' if i == k else 'X', CORAL if i == k else CYAN, .26) for i in range(3)])
                             .arrange(buff=.12) for k in range(3)]).arrange(buff=.7).move_to([0, .35, 0])
        self.play(FadeIn(self.rows, lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('cases', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.rows[2].animate.scale(1.25), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m, GOLD)
