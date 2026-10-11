"""XSS026 · Hai lá át — C(4,2)/C(52,2) = 6/1326 = 1/221 (bẫy (1/13)² có hoàn lại)."""
from __future__ import annotations

import sys
from fractions import Fraction
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import SUIT_ORDER, mini_deck, playing_card  # noqa: E402

EPISODE = {'code': 'XSS026', 'answer': '1/221'}
PROBLEM = ['Rút ngẫu nhiên $2$ lá từ bộ bài $52$ lá.', 'Xác suất được $2$ lá át?']
OPTIONS = ['1/13', '1/169', '1/221']
CORRECT = 2
ANSWER_VALUE = 1 / 221

BEATS = [
    Beat('hook', 'hook', 'Rút cùng lúc hai lá từ bộ bài năm mươi hai lá. Xác suất được cả hai lá át là bao nhiêu? '
                         'Đây là đôi át, bài mạnh nhất trong nhiều trò chơi.'),
    Beat('guess', 'hook', 'Một phần mười ba, một phần một trăm sáu mươi chín, hay một phần hai trăm hai mươi mốt? '
                          'Ba, hai, một!'),
    Beat('s1', 'solve', 'Số cách rút hai lá từ năm mươi hai lá là tổ hợp chập hai của năm mươi hai, '
                        'bằng một nghìn ba trăm hai mươi sáu cách.'),
    Beat('s2', 'solve', 'Số cách rút được hai lá át: chọn hai trong bốn lá át, tổ hợp chập hai của bốn, bằng sáu cách.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần một nghìn ba trăm hai mươi sáu, tức một phần hai trăm hai mươi mốt. '
                        'Một phần một trăm sáu mươi chín là bẫy: đó là rút có hoàn lại, một lá có thể bị rút hai lần.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai trăm hai mươi mốt. Trung bình hơn hai trăm lần chia bài mới có một lần '
                            'được đôi át!'),
    Beat('outro', 'outro', outro_text(26)),
]

FORMULAS = formulas('1/221', OPTIONS,
                    n='n(Omega) = C_52^2 = 1326',
                    a='n(A) = C_4^2 = 6',
                    prob='P(A) = 6/1326 = 1/221',
                    trap='(1/13)^2 = 1/169 quad coral(times)')


def validate() -> bool:
    assert comb(52, 2) == 1326 and Fraction(comb(4, 2), comb(52, 2)) == Fraction(1, 221)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS026(ShortScene):
    N = 26

    def hook_visual(self, t0):
        self.pair = VGroup(playing_card('A', 'S', 1.5).rotate(.12), playing_card('A', 'H', 1.5).rotate(-.12)) \
            .arrange(buff=-.25).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.pair, lag_ratio=.4), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.pair.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.pair)
        self.deck = mini_deck(.5).move_to([-.1, 1.35, 0])
        self.play(FadeIn(self.deck, lag_ratio=.01), run_time=self.rt(.3))
        self.wait_until(.55, t0)
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        aces = VGroup(*[self.deck.cards[('A', s)] for s in SUIT_ORDER])
        rest = VGroup(*[c for k, c in self.deck.cards.items() if k[0] != 'A'])
        self.play(rest.animate.set_opacity(.25), aces.animate.scale(1.25),
                  *[a[0].animate.set_stroke(GOLD, 5) for a in aces], run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.write_board(self.M('a', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('trap', 1.6), anim='fade')
        self.write_board(tx('chỉ đúng khi rút có hoàn lại', 24, SOFT), anim='fade')
