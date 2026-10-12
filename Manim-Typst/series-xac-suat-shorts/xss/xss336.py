"""XSS336 · Ai rút đỏ trước? — 2 đỏ 3 xanh, A, B luân phiên không hoàn lại; bi đỏ đầu ở vị trí 1, 2, 3, 4 với 2/5, 3/10, 1/5, 1/10; A thắng ở vị trí lẻ → 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from common.kit import tx  # noqa: E402
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS336', 'answer': '3/5'}
PROBLEM = ['Hộp $2$ đỏ, $3$ xanh. A, B lần lượt rút',
           'không hoàn lại (A trước), ai được đỏ',
           'trước thì thắng. Xác suất A thắng?']
OPTIONS = ['1/2', '3/5', '2/3']
CORRECT = 1
ANSWER_VALUE = .6
ORDERS = set(permutations('RRBBB'))

BEATS = [
    Beat('hook', 'hook', 'Hộp có hai bi đỏ và ba bi xanh. A và B lần lượt rút không hoàn lại, A rút trước. Ai rút được bi đỏ trước thì thắng. '
                         'Xác suất A thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'A rút ở lượt một, ba, năm; B ở lượt hai, bốn. Ai thắng phụ thuộc vào vị trí bi đỏ đầu tiên trong thứ tự rút.'),
    Beat('s2', 'solve', 'Bi đỏ đầu ở lượt một: hai phần năm. Ở lượt hai: ba phần năm nhân hai phần tư, ba phần mười. '
                        'Ở lượt ba: ba phần năm nhân hai phần tư nhân hai phần ba, một phần năm. Lượt bốn: một phần mười.'),
    Beat('s3', 'solve', 'A thắng khi bi đỏ đầu ở lượt lẻ: hai phần năm cộng một phần năm, bằng ba phần năm.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Đi trước có lợi, vì A có thêm lượt ba để sửa sai.'),
    Beat('outro', 'outro', outro_text(336)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    pos='2/5, quad 3/10, quad 1/5, quad 1/10',
                    prob='P(A) = 2/5 + 1/5 = 3/5')


def validate() -> bool:
    a = sum(o.index('R') % 2 == 0 for o in ORDERS)
    assert F(a, len(ORDERS)) == F(3, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS336(ShortScene):
    N = 336

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRBBB', cols=5, r=.3).move_to([0, 2.15, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.row = ball_row('BBR', y=.55, r=.34, buff=.45)
        self.who = VGroup(*[tx(w, 28, CYAN if w == 'A' else GOLD, bold=True).next_to(b, [0, -1, 0], buff=.18)
                            for w, b in zip('ABA', self.row)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row, lag_ratio=.4), FadeIn(self.who, lag_ratio=.4), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.play(self.row[2].animate.scale(1.3), self.who[2].animate.scale(1.3), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('pos', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
