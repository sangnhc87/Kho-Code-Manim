"""XSS149 · Ba lá cơ liên tiếp — công thức nhân dây chuyền: 13/52 · 12/51 · 11/50 = 11/850."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import card_back, playing_card  # noqa: E402

EPISODE = {'code': 'XSS149', 'answer': '11/850'}
PROBLEM = ['Rút lần lượt $3$ lá không hoàn lại từ bộ',
           'bài $52$ lá. Xác suất cả $3$ lá đều là cơ?']
OPTIONS = ['1/64', '11/850', '1/22']
CORRECT = 1
ANSWER_VALUE = 11 / 850

BEATS = [
    Beat('hook', 'hook', 'Rút lần lượt ba lá bài, không hoàn lại. Xác suất cả ba lá đều là cơ là bao nhiêu? '
                         'Mỗi chất chiếm một phần tư, vậy có phải một phần tư mũ ba không?'),
    Beat('guess', 'hook', 'Một phần sáu mươi tư, mười một phần tám trăm năm mươi, hay một phần hai mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lá đầu là cơ với xác suất mười ba phần năm mươi hai. Biết lá đầu là cơ, bộ bài còn năm mươi mốt lá, mười hai lá cơ.'),
    Beat('s2', 'solve', 'Biết hai lá đầu là cơ, còn năm mươi lá với mười một lá cơ. Công thức nhân xác suất: nhân ba xác suất có điều kiện liên tiếp.'),
    Beat('s3', 'solve', 'Kết quả mười một phần tám trăm năm mươi, khoảng một phẩy ba phần trăm, nhỏ hơn một phần sáu mươi tư '
                        'vì mỗi lá cơ rút ra làm số lá cơ còn lại giảm. Đếm bằng tổ hợp cũng ra đúng như vậy.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần tám trăm năm mươi. Không hoàn lại thì mỗi lần rút là một xác suất có điều kiện mới!'),
    Beat('outro', 'outro', outro_text(149)),
]

FORMULAS = formulas('11/850', OPTIONS,
                    chain='P = 13/52 dot 12/51 dot 11/50 = 11/850',
                    comb='C_13^3 / C_52^3 = 286/22100 = 11/850')


def validate() -> bool:
    deck = list(product(range(13), range(4)))
    assert F(13, 52) * F(12, 51) * F(11, 50) == F(11, 850) == F(comb(13, 3), comb(52, 3))
    assert F(sum(all(c[1] == 1 for c in h) for h in combinations(deck, 3)), comb(52, 3)) == F(11, 850)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS149(ShortScene):
    N = 149

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.slots = VGroup(*[card_back(1.3) for _ in range(3)]).arrange(buff=.5).move_to([0, 1.6, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.slots, lag_ratio=.3), run_time=self.rt(.1))

    def flip(self, i, rank, frac_tex):
        card = playing_card(rank, 'H', 1.3).move_to(self.slots[i])
        lab = self.TM(f'${frac_tex}$', 30, GOLD).next_to(card, [0, -1, 0], buff=.25)
        self.play(FadeIn(card), FadeIn(lab), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.flip(0, 'K', '13/52')
        self.wait_until(.55, t0)
        self.flip(1, '7', '12/51')

    def beat_s2(self, T):
        t0 = self.now()
        self.flip(2, '2', '11/50')
        self.wait_until(.45, t0)
        m = self.M('chain', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.TM('nhỏ hơn $1/64$', 26, CORAL, bold=True), anim='fade')
        self.wait_until(.6, t0)
        self.write_board(self.M('comb', 1.7), anim='fade')
