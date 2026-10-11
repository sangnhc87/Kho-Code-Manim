"""XSS007 · Rút được cơ — 13 lá cơ trong 52 lá: 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import LEFT, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, SOFT  # noqa: E402
from common.visuals import RANKS, SUIT_ORDER, mini_deck, playing_card  # noqa: E402

EPISODE = {'code': 'XSS007', 'answer': '1/4'}
PROBLEM = ['Rút ngẫu nhiên một lá từ bộ bài $52$ lá.', 'Xác suất rút được lá cơ?']
OPTIONS = ['1/13', '1/4', '1/2']
CORRECT = 1
ANSWER_VALUE = .25

BEATS = [
    Beat('hook', 'hook', 'Rút một lá từ bộ bài năm mươi hai lá. Xác suất được một lá cơ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười ba, một phần tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xếp bộ bài thành bốn hàng theo bốn chất. Mỗi hàng có mười ba lá, '
                        'và cả năm mươi hai lá có cùng cơ hội được rút.'),
    Beat('s2', 'solve', 'Lá cơ chiếm trọn một hàng: mười ba kết quả thuận lợi. '
                        'Xác suất bằng mười ba phần năm mươi hai.'),
    Beat('s3', 'solve', 'Rút gọn được một phần tư. Cách nghĩ nhanh hơn: bốn chất có số lá bằng nhau, '
                        'nên mỗi chất chiếm đúng một phần tư bộ bài.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Đổi câu hỏi thành lá màu đỏ, bạn có đoán ra ngay không?'),
    Beat('outro', 'outro', outro_text(7)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    prob='P = 13/52 = 1/4',
                    quick='1/4 " bộ bài"')


def validate() -> bool:
    deck = list(product(RANKS, SUIT_ORDER))
    assert Fraction(sum(s == 'H' for _, s in deck), 52) == Fraction(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS007(ShortScene):
    N = 7

    def hook_visual(self, t0):
        self.card = playing_card('K', 'H', 1.6).move_to([0, 1.3, 0])
        self.wait_until(.25, t0)
        self.play(FadeIn(self.card, scale=.7), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.card.animate.scale(.2).set_opacity(0), run_time=self.rt(.05))
        self.remove(self.card)
        self.deck = mini_deck(.5).move_to([.15, 1.35, 0])
        names = VGroup(*[tx(n, 20, SOFT) for n in ('bích', 'cơ', 'rô', 'nhép')])
        for name, i in zip(names, range(4)):
            name.next_to(self.deck.cards[('A', SUIT_ORDER[i])], LEFT, buff=.12)
        self.play(FadeIn(self.deck, lag_ratio=.01), FadeIn(names), run_time=self.rt(.3))
        self.names = names
        self.wait_until(.7, t0)

    def beat_s2(self, T):
        t0 = self.now()
        hearts = VGroup(*[self.deck.cards[(r, 'H')] for r in RANKS])
        rest = VGroup(*[c for k, c in self.deck.cards.items() if k[1] != 'H'])
        self.play(rest.animate.set_opacity(.25), *[c[0].animate.set_stroke(CORAL, 4) for c in hearts],
                  self.names[1].animate.set_color(CORAL).scale(1.3), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(VGroup(tx('mỗi chất chiếm', 30, SOFT), self.M('quick', 1.6)).arrange(buff=.2), anim='fade')
