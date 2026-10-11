"""XSS146 · Biết có một lá át — 198 cặp có ít nhất một át, 6 cặp hai át: 1/33."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import SUIT_ORDER, mini_deck  # noqa: E402

EPISODE = {'code': 'XSS146', 'answer': '1/33'}
PROBLEM = ['Rút $2$ lá từ bộ bài $52$ lá, biết',
           'có ít nhất một lá át. Xác suất',
           'cả hai lá đều là át?']
OPTIONS = ['1/221', '1/33', '1/17']
CORRECT = 1
ANSWER_VALUE = 1 / 33
DECK = list(product(range(13), range(4)))

BEATS = [
    Beat('hook', 'hook', 'Rút hai lá từ bộ bài năm mươi hai lá. Bạn được báo: trong hai lá có ít nhất một lá át. '
                         'Xác suất cả hai lá đều là át là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai trăm hai mươi mốt, một phần ba mươi ba, hay một phần mười bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không gian mẫu có tổ hợp chập hai của năm mươi hai, bằng một nghìn ba trăm hai mươi sáu cặp. '
                        'Điều kiện "có ít nhất một át": lấy tất cả trừ đi các cặp không có át, còn một trăm chín mươi tám cặp.'),
    Beat('s2', 'solve', 'Trong đó, cặp hai lá át có tổ hợp chập hai của bốn, bằng sáu cặp.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần một trăm chín mươi tám, tức một phần ba mươi ba. '
                        'Một phần hai trăm hai mươi mốt là xác suất khi chưa biết gì.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba mươi ba. Thử thách tiếp theo sẽ làm bạn bất ngờ: nếu biết có át bích thì sao?'),
    Beat('outro', 'outro', outro_text(146)),
]

FORMULAS = formulas('1/33', OPTIONS,
                    nb='n(B) = C_52^2 - C_48^2 = 1326 - 1128 = 198',
                    nab='n(A sect B) = C_4^2 = 6',
                    prob='P(A | B) = 6/198 = 1/33')


def validate() -> bool:
    pairs = list(combinations(DECK, 2))
    b = [h for h in pairs if 0 in (h[0][0], h[1][0])]
    assert len(b) == 198 == comb(52, 2) - comb(48, 2)
    assert F(sum(h[0][0] == h[1][0] == 0 for h in b), len(b)) == F(1, 33)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS146(ShortScene):
    N = 146

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.deck = mini_deck(.5).move_to([0, 1.35, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.deck, lag_ratio=.01), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(tx('1326 cặp', 28, SOFT), anim='fade')
        self.wait_until(.4, t0)
        aces = [self.deck.cards[('A', s)] for s in SUIT_ORDER]
        self.play(*[c[0].animate.set_stroke(GOLD, 5) for c in aces], run_time=self.rt(.06))
        self.clear_board(.03)
        self.write_board(self.M('nb', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('nab', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
