"""XSS034 · Tổng hai thẻ chẵn — 1…5 chọn 2: cùng lẻ C(3,2) + cùng chẵn C(2,2) = 4/10 = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS034', 'answer': '2/5'}
PROBLEM = ['Rút ngẫu nhiên $2$ thẻ từ $5$ thẻ ghi số $1$',
           'đến $5$. Xác suất tổng hai số là số chẵn?']
OPTIONS = ['1/2', '2/5', '3/5']
CORRECT = 1
ANSWER_VALUE = .4
PAIRS = list(combinations(range(1, 6), 2))

BEATS = [
    Beat('hook', 'hook', 'Có năm tấm thẻ ghi số một đến năm. Rút ngẫu nhiên hai thẻ. '
                         'Xác suất tổng hai số là số chẵn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Rút hai thẻ từ năm thẻ: tổ hợp chập hai của năm, bằng mười cách.'),
    Beat('s2', 'solve', 'Tổng chẵn khi hai số cùng tính chẵn lẻ. Cùng lẻ: chọn hai trong ba số lẻ, ba cách. '
                        'Cùng chẵn: chọn cả hai số chẵn, một cách. Tổng cộng bốn cách.'),
    Beat('s3', 'solve', 'Xác suất bằng bốn phần mười, tức hai phần năm. Không phải một phần hai, '
                        'vì số lẻ nhiều hơn số chẵn và thẻ không được rút lặp.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Tổng chẵn: cùng chẵn hoặc cùng lẻ, nhớ chia hai trường hợp!'),
    Beat('outro', 'outro', outro_text(34)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    n='n(Omega) = C_5^2 = 10',
                    a='n(A) = C_3^2 + C_2^2 = 3 + 1 = 4',
                    prob='P(A) = 4/10 = 2/5')


def validate() -> bool:
    assert Fraction(sum((a + b) % 2 == 0 for a, b in PAIRS), len(PAIRS)) == Fraction(2, 5)
    assert comb(3, 2) + comb(2, 2) == 4
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS034(ShortScene):
    N = 34

    def hook_visual(self, t0):
        self.cards = VGroup()
        for k in range(1, 6):
            c = card(1.05, 1.45, GOLD if k % 2 == 0 else CYAN, PANEL, radius=.15, stroke_width=4)
            self.cards.add(VGroup(c, self.MNum(k, 0, GOLD if k % 2 == 0 else CYAN, 54).move_to(c)))
        self.cards.arrange(buff=.25).move_to([0, 1.5, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.cards, lag_ratio=.2), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        legend = VGroup(tx('lẻ: 1, 3, 5', 30, CYAN, bold=True), tx('chẵn: 2, 4', 30, GOLD, bold=True)) \
            .arrange(buff=.6).move_to([0, .2, 0])
        self.play(FadeIn(legend), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('a', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(tx('3 số lẻ, chỉ 2 số chẵn', 26, SOFT), anim='fade')
