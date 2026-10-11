"""XSS035 · 2 sấp 2 ngửa — 4 đồng xu: C(4,2)/16 = 6/16 = 3/8 (bẫy 1/5)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PANEL, STROKE  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS035', 'answer': '3/8'}
PROBLEM = ['Tung bốn đồng xu.', 'Xác suất được đúng $2$ sấp, $2$ ngửa?']
OPTIONS = ['1/2', '1/5', '3/8']
CORRECT = 2
ANSWER_VALUE = 3 / 8
ALL = [''.join(w) for w in product('SN', repeat=4)]

BEATS = [
    Beat('hook', 'hook', 'Tung bốn đồng xu. Chia đều hai sấp hai ngửa nghe rất tự nhiên. '
                         'Vậy xác suất của nó có lớn không?'),
    Beat('guess', 'hook', 'Một phần hai, một phần năm, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn đồng xu cho hai mũ bốn bằng mười sáu kết quả đồng khả năng. Đây là cả mười sáu kết quả.'),
    Beat('s2', 'solve', 'Chọn hai vị trí trong bốn để đặt mặt ngửa: tổ hợp chập hai của bốn, bằng sáu cách. '
                        'Sáu kết quả được tô sáng trên màn hình.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần mười sáu, tức ba phần tám, chưa tới một nửa! Một phần năm là bẫy: '
                        'số mặt ngửa từ không đến bốn có năm giá trị, nhưng chúng không đồng khả năng.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Chia đều thường gặp nhất, nhưng vẫn ít hơn một nửa số lần!'),
    Beat('outro', 'outro', outro_text(35)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    n='n(Omega) = 2^4 = 16',
                    a='n(A) = C_4^2 = 6',
                    prob='P(A) = 6/16 = 3/8')


def validate() -> bool:
    assert Fraction(sum(w.count('N') == 2 for w in ALL), 16) == Fraction(comb(4, 2), 16) == Fraction(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS035(ShortScene):
    N = 35

    def hook_visual(self, t0):
        self.big = VGroup(*[coin(f, .75) for f in 'SNNS']).arrange(buff=.25).move_to([0, 1.3, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.big, lag_ratio=.25), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.big.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.big)
        self.cells = VGroup()
        for w in ALL:
            row = VGroup(*[coin(f, .15) for f in w]).arrange(buff=.04)
            self.cells.add(VGroup(card(1.55, .55, STROKE, PANEL, radius=.1, stroke_width=2), row))
            self.cells[-1][1].move_to(self.cells[-1][0])
        self.cells.arrange_in_grid(4, 4, buff=(.12, .14)).move_to([0, 1.35, 0])
        self.play(FadeIn(self.cells, lag_ratio=.04), run_time=self.rt(.35))
        self.wait_until(.7, t0)
        self.board_top = -.85
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        hits = [i for i, w in enumerate(ALL) if w.count('N') == 2]
        self.play(*[self.cells[i][0].animate.set_stroke(GOLD, 5).set_fill(GOLD, .25) for i in hits],
                  *[self.cells[i].animate.set_opacity(.3) for i in range(16) if i not in hits], run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.write_board(self.M('a', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('0, 1, 2, 3, 4 ngửa: không đồng khả năng', 24, CORAL), anim='fade')
