"""XSS236 · Ít nhất hai người trúng — P(cả 3) = 0,21; P(≥ 2) = 0,44 + 0,21: 21/65."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS236', 'answer': '21/65'}
PROBLEM = ['Ba xạ thủ trúng với xác suất $"0,5"$; $"0,6"$;',
           '$"0,7"$. Biết có ít nhất $2$ người trúng. Xác',
           'suất cả $3$ người cùng trúng?']
OPTIONS = ['"0,21"', '21/65', '1/2']
CORRECT = 1
ANSWER_VALUE = 21 / 65
PR = (F(1, 2), F(3, 5), F(7, 10))


def prob(w):
    out = F(1)
    for hit, p in zip(w, PR):
        out *= p if hit else 1 - p
    return out


BEATS = [
    Beat('hook', 'hook', 'Vẫn ba xạ thủ với xác suất trúng không phẩy năm, không phẩy sáu, không phẩy bảy. '
                         'Lần này biết có ít nhất hai người trúng. Xác suất cả ba cùng trúng là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy hai mốt, hai mươi mốt phần sáu mươi lăm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ít nhất hai người trúng gồm: đúng hai người, tổng không phẩy bốn bốn như thử thách trước; và cả ba người, không phẩy năm nhân không phẩy sáu nhân không phẩy bảy bằng không phẩy hai mốt.'),
    Beat('s2', 'solve', 'Xác suất điều kiện là không phẩy sáu lăm. Biến cố cả ba trúng nằm trọn trong điều kiện.'),
    Beat('s3', 'solve', 'Chia: không phẩy hai mốt chia không phẩy sáu lăm, bằng hai mươi mốt phần sáu mươi lăm, khoảng ba mươi hai phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi mốt phần sáu mươi lăm. Không phẩy hai mốt là bẫy: quên chia cho xác suất điều kiện!'),
    Beat('outro', 'outro', outro_text(236)),
]

FORMULAS = formulas('21/65', OPTIONS,
                    cond='P(>= 2) = "0,44" + "0,21" = "0,65"',
                    prob='P = ("0,21")/("0,65") = 21/65')


def validate() -> bool:
    ge2 = [w for w in product((0, 1), repeat=3) if sum(w) >= 2]
    assert prob((1, 1, 1)) / sum(prob(w) for w in ge2) == F(21, 65)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS236(ShortScene):
    N = 236

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.rows = VGroup(*[VGroup(*[token('T' if i != k else 'X', GREEN if i != k else CORAL, .24) for i in range(3)])
                             .arrange(buff=.1) for k in range(3)],
                           VGroup(*[token('T', GOLD, .24) for _ in range(3)]).arrange(buff=.1)) \
            .arrange_in_grid(2, 2, buff=(.8, .35)).move_to([0, 1.6, 0])
        self.wait_until(.65, t0)
        self.play(FadeIn(self.rows[:3], lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows[3], scale=1.3), run_time=self.rt(.06))

    def beat_s2(self, T):
        self.write_board(self.M('cond', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)


