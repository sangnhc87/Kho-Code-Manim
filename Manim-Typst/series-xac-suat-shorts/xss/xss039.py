"""XSS039 · Át hoặc cơ — 4 + 13 − 1 = 16 lá: 16/52 = 4/13 (át cơ chỉ tính một lần)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import RANKS, SUIT_ORDER, mini_deck  # noqa: E402

EPISODE = {'code': 'XSS039', 'answer': '4/13'}
PROBLEM = ['Rút một lá từ bộ bài $52$ lá.', 'Xác suất được lá át hoặc lá cơ?']
OPTIONS = ['17/52', '4/13', '1/52']
CORRECT = 1
ANSWER_VALUE = 4 / 13

BEATS = [
    Beat('hook', 'hook', 'Rút một lá từ bộ bài năm mươi hai lá. Xác suất được lá át hoặc lá cơ là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười bảy phần năm mươi hai, bốn phần mười ba, hay một phần năm mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tô bốn lá át thành một cột, và mười ba lá cơ thành một hàng. Bốn cộng mười ba bằng mười bảy?'),
    Beat('s2', 'solve', 'Không! Át cơ nằm ở cả cột lẫn hàng, bị đếm hai lần. Số lá thuận lợi chỉ là bốn cộng mười ba trừ một, '
                        'bằng mười sáu lá.'),
    Beat('s3', 'solve', 'Xác suất bằng mười sáu phần năm mươi hai, tức bốn phần mười ba. Đây lại là công thức cộng: '
                        'cộng hai xác suất rồi trừ đi phần chung.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần mười ba. Thấy chữ hoặc, nhớ kiểm tra phần chung!'),
    Beat('outro', 'outro', outro_text(39)),
]

FORMULAS = formulas('4/13', OPTIONS,
                    count='4 + 13 - 1 = 16',
                    prob='P = 4/52 + 13/52 - 1/52 = 16/52 = 4/13')


def validate() -> bool:
    deck = list(product(RANKS, SUIT_ORDER))
    assert Fraction(sum(r == 'A' or s == 'H' for r, s in deck), 52) == Fraction(4, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS039(ShortScene):
    N = 39

    def hook_visual(self, t0):
        self.deck = mini_deck(.5).move_to([-.1, 1.35, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.deck, lag_ratio=.01), run_time=self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        aces = VGroup(*[self.deck.cards[('A', s)] for s in SUIT_ORDER])
        hearts = VGroup(*[self.deck.cards[(r, 'H')] for r in RANKS])
        rest = VGroup(*[c for (r, s), c in self.deck.cards.items() if r != 'A' and s != 'H'])
        self.play(rest.animate.set_opacity(.25), *[a[0].animate.set_stroke(GOLD, 4) for a in aces], run_time=self.rt(.1))
        self.wait_until(.35, t0)
        self.play(*[h[0].animate.set_stroke(CYAN, 4) for h in hearts if h not in aces], run_time=self.rt(.1))
        self.wait_until(.7, t0)
        self.write_board(self.TM('$4 + 13 = 17$ ?', 34, GOLD, bold=True))

    def beat_s2(self, T):
        t0 = self.now()
        ah = self.deck.cards[('A', 'H')]
        self.play(ah.animate.scale(1.6), ah[0].animate.set_stroke(CORAL, 6), run_time=self.rt(.08))
        self.write_board(tx('át cơ bị đếm 2 lần!', 30, CORAL, bold=True), anim='fade')
        self.wait_until(.55, t0)
        self.clear_board(.03)
        self.write_board(self.M('count', 2.3))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
