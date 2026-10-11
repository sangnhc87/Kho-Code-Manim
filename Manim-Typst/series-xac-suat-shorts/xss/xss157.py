"""XSS157 · Đôi một độc lập — A, B, C đôi một độc lập nhưng P(A ∩ B ∩ C) = 1/4 ≠ 1/8: không độc lập cả ba."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS157', 'answer': 'Không (chỉ đôi một độc lập)'}
PROBLEM = ['Tung $2$ xu. A: xu $1$ ngửa; B: xu $2$',
           'ngửa; C: hai xu giống nhau. A, B,',
           'C có độc lập (cả ba) không?']
OPTIONS = ['"Có"', '"Không"']
CORRECT = 1
ANSWER_VALUE = None
OUT = list(product('NS', repeat=2))
EV = {'A': lambda w: w[0] == 'N', 'B': lambda w: w[1] == 'N', 'C': lambda w: w[0] == w[1]}


def P(f):
    return F(sum(map(f, OUT)), 4)


BEATS = [
    Beat('hook', 'hook', 'Tung hai đồng xu. A là xu một ra ngửa, B là xu hai ra ngửa, C là hai xu ra giống nhau. '
                         'Mỗi cặp biến cố đều độc lập. Vậy cả ba biến cố có độc lập không?'),
    Beat('guess', 'hook', 'Có, hay không? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn kết quả đồng khả năng. A, B, C đều có xác suất một phần hai. '
                        'A giao B là ngửa ngửa, xác suất một phần tư, đúng bằng một phần hai nhân một phần hai.'),
    Beat('s2', 'solve', 'A giao C cũng là ngửa ngửa, B giao C cũng vậy, đều bằng một phần tư. Vậy ba cặp đều độc lập.'),
    Beat('s3', 'solve', 'Nhưng A giao B giao C vẫn chỉ là ngửa ngửa, xác suất một phần tư, khác một phần hai mũ ba bằng một phần tám. '
                        'Biết A và B xảy ra thì C chắc chắn xảy ra!'),
    Beat('answer', 'solve', 'Đáp án: không. Đôi một độc lập chưa đủ để độc lập cả ba, một điểm rất hay bị nhầm!'),
    Beat('outro', 'outro', outro_text(157)),
]

FORMULAS = formulas('"Không"', OPTIONS,
                    pair='P(A sect B) = P(A sect C) = P(B sect C) = 1/4 = 1/2 dot 1/2',
                    triple='P(A sect B sect C) = 1/4 eq.not 1/8 = P(A) P(B) P(C)')


def validate() -> bool:
    for x, y in combinations('ABC', 2):
        assert P(lambda w: EV[x](w) and EV[y](w)) == P(EV[x]) * P(EV[y])
    assert P(lambda w: all(EV[k](w) for k in 'ABC')) == F(1, 4) != F(1, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS157(ShortScene):
    N = 157

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.rows = VGroup(*[VGroup(coin(a, .4), coin(b, .4)).arrange(buff=.1) for a, b in OUT]) \
            .arrange(buff=.6).move_to([0, 2.0, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.rows, lag_ratio=.2), run_time=self.rt(.12))

    def tags(self, key, color, dy):
        return VGroup(*[tx(key, 26, color, bold=True).next_to(r, [0, -1, 0], buff=.15 + dy) if EV[key](w) else VGroup()
                        for r, w in zip(self.rows, OUT)])

    def beat_s1(self, T):
        t0 = self.now()
        self.ta, self.tb = self.tags('A', CYAN, 0), self.tags('B', GOLD, .42)
        self.play(FadeIn(self.ta), FadeIn(self.tb), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.tc = self.tags('C', GREEN, .84)
        self.play(FadeIn(self.tc), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('pair', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.rows[0].animate.scale(1.2), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        m = self.M('triple', 1.5)
        self.write_board(m)
        self.frame(m, CORAL)


