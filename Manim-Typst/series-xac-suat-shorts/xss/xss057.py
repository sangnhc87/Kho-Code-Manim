"""XSS057 · Hợp của hai biến cố độc lập — 0,4 + 0,5 − 0,4·0,5 = 0,7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, LEFT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import unit_square  # noqa: E402

EPISODE = {'code': 'XSS057', 'answer': '0,7'}
PROBLEM = ['$A$, $B$ độc lập, $P(A) = "0,4"$, $P(B) = "0,5"$.', 'Tính $P(A union B)$.']
OPTIONS = ['"0,9"', '"0,7"', '"0,2"']
CORRECT = 1
ANSWER_VALUE = .7

BEATS = [
    Beat('hook', 'hook', 'Hai biến cố A và B độc lập, xác suất của A là không phẩy bốn, của B là không phẩy năm. '
                         'Xác suất để A hoặc B xảy ra là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy chín, không phẩy bảy, hay không phẩy hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Công thức cộng: xác suất A hợp B bằng xác suất A cộng xác suất B trừ xác suất A giao B. '
                        'Cộng thẳng ra không phẩy chín là quên trừ phần chung.'),
    Beat('s2', 'solve', 'A và B độc lập nên phần chung bằng tích: không phẩy bốn nhân không phẩy năm, bằng không phẩy hai. '
                        'Trên hình vuông, đó là hình chữ nhật góc trên bên trái.'),
    Beat('s3', 'solve', 'Vậy xác suất hợp bằng không phẩy bốn cộng không phẩy năm trừ không phẩy hai, bằng không phẩy bảy. '
                        'Kiểm tra bằng biến cố đối: một trừ không phẩy sáu nhân không phẩy năm cũng bằng không phẩy bảy.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bảy. Công thức cộng và công thức nhân làm việc cùng nhau!'),
    Beat('outro', 'outro', outro_text(57)),
]

FORMULAS = formulas('"0,7"', OPTIONS,
                    rule='P(A union B) = P(A) + P(B) - P(A B)',
                    both='P(A B) = "0,4" dot "0,5" = "0,2"',
                    prob='"0,4" + "0,5" - "0,2" = "0,7"',
                    check='1 - "0,6" dot "0,5" = "0,7"')


def validate() -> bool:
    a, b = F(4, 10), F(5, 10)
    assert a + b - a * b == F(7, 10) == 1 - (1 - a) * (1 - b)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS057(ShortScene):
    N = 57

    def hook_visual(self, t0):
        self.board_top = -1.1
        self.sq = unit_square(.4, .5, 3.7, (.2, 1.35))
        labs = VGroup(self.TM('$A$: "0,4"', 24, CYAN).next_to(self.sq[0], DOWN, buff=.12).align_to(self.sq[0], LEFT),
                      self.TM('$B$: "0,5"', 24, CORAL).rotate(1.5708).next_to(self.sq[0], LEFT, buff=.12)
                      .align_to(self.sq[0], UP))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq), FadeIn(labs), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.sq.region('Ab', CYAN, .4)), FadeIn(self.sq.region('aB', CORAL, .4)),
                  FadeIn(self.sq.region('AB', GOLD, .6)), run_time=self.rt(.1))
        self.write_board(self.M('rule', 1.6))
        self.wait_until(.6, t0)
        self.write_board(self.TM('$"0,4" + "0,5" = "0,9"$ ?', 30, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        self.write_board(self.M('both', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('check', 1.6), anim='fade')
        self.write_board(tx('kiểm tra bằng biến cố đối', 24, SOFT), anim='fade')
