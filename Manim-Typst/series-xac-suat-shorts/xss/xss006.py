"""XSS006 · Rút được át — 4 lá át trong 52 lá: 1/13."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import RIGHT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import RANKS, SUIT_ORDER, card_back, mini_deck  # noqa: E402

EPISODE = {'code': 'XSS006', 'answer': '1/13'}
PROBLEM = ['Rút ngẫu nhiên một lá từ bộ bài $52$ lá.', 'Xác suất rút được lá át?']
OPTIONS = ['1/52', '1/13', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 13

BEATS = [
    Beat('hook', 'hook', 'Rút ngẫu nhiên một lá từ bộ bài năm mươi hai lá. Cơ hội rút trúng lá át là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm mươi hai, một phần mười ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bộ bài có bốn chất: bích, cơ, rô, nhép. Mỗi chất có mười ba lá, từ át đến già. '
                        'Bốn nhân mười ba bằng năm mươi hai lá, mỗi lá có cùng cơ hội được rút.'),
    Beat('s2', 'solve', 'Lá át có ở cả bốn chất, nên có bốn kết quả thuận lợi. Xác suất bằng bốn phần năm mươi hai.'),
    Beat('s3', 'solve', 'Rút gọn: bốn phần năm mươi hai bằng một phần mười ba. '
                        'Đáp án một phần năm mươi hai là bẫy, vì nó chỉ đúng với một lá át cụ thể, chẳng hạn át cơ.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười ba. Trung bình cứ mười ba lần rút thì có một lần được át.'),
    Beat('outro', 'outro', outro_text(6)),
]

FORMULAS = formulas('1/13', OPTIONS,
                    n='n(Omega) = 4 dot 13 = 52',
                    prob='P = 4/52 = 1/13',
                    one='P("át cơ") = 1/52')


def validate() -> bool:
    deck = list(product(RANKS, SUIT_ORDER))
    assert len(deck) == 52 and Fraction(sum(r == 'A' for r, _ in deck), 52) == Fraction(1, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS006(ShortScene):
    N = 6

    def hook_visual(self, t0):
        backs = VGroup(*[card_back(1.0).rotate((i - 2) * .12) for i in range(5)]).arrange(RIGHT, buff=-.45)
        backs.move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(backs, lag_ratio=.2), run_time=self.rt(.25))
        self.backs = backs

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.backs.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.backs)
        self.deck = mini_deck(.5).move_to([-.1, 1.35, 0])
        self.play(FadeIn(self.deck, lag_ratio=.01), run_time=self.rt(.3))
        self.wait_until(.6, t0)
        self.write_board(self.M('n', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        aces = VGroup(*[self.deck.cards[('A', s)] for s in SUIT_ORDER])
        others = VGroup(*[c for k, c in self.deck.cards.items() if k[0] != 'A'])
        self.play(others.animate.set_opacity(.25), aces.animate.scale(1.25), run_time=self.rt(.1))
        self.play(*[a[0].animate.set_stroke(GOLD, 5) for a in aces], run_time=self.rt(.04))
        self.play(FadeIn(tx('4 lá át', 32, GOLD, bold=True).next_to(aces, UP, buff=.15).shift(UP * .1)),
                  run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('one', 1.6), anim='fade')
        self.write_board(tx('chỉ đúng cho một lá át cụ thể', 26, SOFT), anim='fade')
