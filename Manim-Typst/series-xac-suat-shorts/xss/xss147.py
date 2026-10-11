"""XSS147 · Biết có át bích — lá còn lại là 1 trong 51 lá, 3 lá át: 3/51 = 1/17, gấp gần đôi 1/33."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402
from common.visuals import SUIT_ORDER, mini_deck  # noqa: E402

EPISODE = {'code': 'XSS147', 'answer': '1/17'}
PROBLEM = ['Rút $2$ lá từ bộ bài $52$ lá, biết',
           'trong đó có lá át bích. Xác suất',
           'cả hai lá đều là át?']
OPTIONS = ['1/33', '1/17', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 17
DECK = list(product(range(13), range(4)))

BEATS = [
    Beat('hook', 'hook', 'Thử thách trước: biết có ít nhất một lá át, xác suất hai át là một phần ba mươi ba. '
                         'Bây giờ thông tin cụ thể hơn: trong hai lá có lá át bích. Xác suất cả hai là át có thay đổi không?'),
    Beat('guess', 'hook', 'Một phần ba mươi ba, một phần mười bảy, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết có át bích thì lá còn lại là một trong năm mươi mốt lá khác, đồng khả năng. '
                        'Không gian mẫu thu hẹp còn năm mươi mốt cặp.'),
    Beat('s2', 'solve', 'Hai lá đều là át khi lá còn lại là một trong ba lá át còn lại: ba cặp.'),
    Beat('s3', 'solve', 'Xác suất bằng ba phần năm mươi mốt, tức một phần mười bảy, gần gấp đôi một phần ba mươi ba! '
                        'Biết tên cụ thể của lá át mang nhiều thông tin hơn chỉ biết có một lá át.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười bảy. Nghịch lý này nhắc ta: điều kiện được phát biểu thế nào thì không gian mẫu thu hẹp đúng như thế!'),
    Beat('outro', 'outro', outro_text(147)),
]

FORMULAS = formulas('1/17', OPTIONS,
                    nb='n(B) = 51',
                    nab='n(A sect B) = 3',
                    prob='P(A | B) = 3/51 = 1/17 > 1/33')


def validate() -> bool:
    b = [h for h in combinations(DECK, 2) if (0, 0) in h]
    assert len(b) == 51 and F(sum(h[0][0] == h[1][0] == 0 for h in b), 51) == F(1, 17)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS147(ShortScene):
    N = 147

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.deck = mini_deck(.5).move_to([0, 1.35, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.deck, lag_ratio=.01), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        spade = self.deck.cards[('A', 'S')]
        self.play(spade.animate.scale(1.5), spade[0].animate.set_stroke(GREEN, 6), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('nb', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        others = [self.deck.cards[('A', s)] for s in SUIT_ORDER if s != 'S']
        self.play(*[c[0].animate.set_stroke(GOLD, 5) for c in others], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('nab', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('thông tin cụ thể hơn → xác suất khác', 26, CORAL, bold=True), anim='fade')
