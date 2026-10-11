"""XSS203 · Ba hộp, đúng hai đỏ — hộp k có k đỏ / 4: 1/4·1/2·3/4·(cách chọn) = 13/32."""
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

EPISODE = {'code': 'XSS203', 'answer': '13/32'}
PROBLEM = ['Hộp thứ $k$ có $k$ bi đỏ và $4 - k$ bi xanh',
           '($k = 1, 2, 3$). Rút mỗi hộp $1$ bi. Xác',
           'suất được đúng $2$ bi đỏ?']
OPTIONS = ['3/8', '13/32', '9/32']
CORRECT = 1
ANSWER_VALUE = 13 / 32
BOXES = ('RBBB', 'RRBB', 'RRRB')
PR = [F(1, 4), F(1, 2), F(3, 4)]


def exactly(k):
    return sum(F(1) * PR[0] ** a * (1 - PR[0]) ** (1 - a) * PR[1] ** b * (1 - PR[1]) ** (1 - b) * PR[2] ** c * (1 - PR[2]) ** (1 - c)
               for a, b, c in product((0, 1), repeat=3) if a + b + c == k)


BEATS = [
    Beat('hook', 'hook', 'Ba hộp: hộp một có một đỏ ba xanh, hộp hai hai đỏ hai xanh, hộp ba ba đỏ một xanh. '
                         'Rút mỗi hộp một bi. Xác suất được đúng hai bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tám, mười ba phần ba mươi hai, hay chín phần ba mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xác suất đỏ ở ba hộp khác nhau: một phần tư, một phần hai, ba phần tư. Không dùng được Bernoulli. '
                        'Ta chọn hộp nào ra xanh.'),
    Beat('s2', 'solve', 'Hộp một xanh: ba phần tư nhân một phần hai nhân ba phần tư, chín phần ba mươi hai. '
                        'Hộp hai xanh: một phần tư nhân một phần hai nhân ba phần tư, ba phần ba mươi hai. '
                        'Hộp ba xanh: một phần tư nhân một phần hai nhân một phần tư, một phần ba mươi hai.'),
    Beat('s3', 'solve', 'Cộng lại: mười ba phần ba mươi hai. Ba phần tám là đáp án sai nếu coi ba hộp như nhau với xác suất một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: mười ba phần ba mươi hai. Xác suất khác nhau ở mỗi lần thử thì liệt kê theo vị trí "ra khác"!'),
    Beat('outro', 'outro', outro_text(203)),
]

FORMULAS = formulas('13/32', OPTIONS,
                    pr='1/4, quad 1/2, quad 3/4',
                    cases='9/32 + 3/32 + 1/32',
                    tot='P = 13/32')


def validate() -> bool:
    direct = F(sum(sum(c == 'R' for c in w) == 2 for w in product(*BOXES)), 64)
    assert direct == exactly(2) == F(13, 32)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS203(ShortScene):
    N = 203

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.urns = urn_row([(b, f'hộp {k}', SOFT) for k, b in enumerate(BOXES, 1)], buff=.45)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('pr', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        rows = VGroup(*[VGroup(*[token('Đ' if i != k else 'X', CORAL if i != k else CYAN, .26) for i in range(3)])
                        .arrange(buff=.12) for k in range(3)]).arrange(buff=.7).move_to([0, .35, 0])
        self.play(FadeIn(rows, lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('cases', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('tot', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)
        self.wait_until(.5, t0)
        self.write_board(self.TM('$3/8$: coi ba hộp như nhau, sai', 24, CORAL), anim='fade')


