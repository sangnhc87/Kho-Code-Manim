"""XSS145 · Biết có ít nhất một ngửa — bỏ lá SSS, còn 7 lá đồng khả năng: 1/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS145', 'answer': '1/7'}
PROBLEM = ['Tung đồng xu $3$ lần, biết có ít nhất một',
           'lần ngửa. Xác suất cả $3$ lần đều ngửa?']
OPTIONS = ['1/8', '1/7', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 7
SEQS = [''.join(w) for w in product('NS', repeat=3)]

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu ba lần. Một người xem kết quả rồi nói: có ít nhất một lần ngửa. '
                         'Xác suất cả ba lần đều ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tám, một phần bảy, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tám kết quả đồng khả năng, từ ngửa ngửa ngửa đến sấp sấp sấp. '
                        'Thông tin "có ít nhất một ngửa" chỉ loại đúng một kết quả: sấp sấp sấp.'),
    Beat('s2', 'solve', 'Còn lại bảy kết quả, vẫn đồng khả năng với nhau. Trong đó chỉ một kết quả là ba ngửa.'),
    Beat('s3', 'solve', 'Xác suất bằng một phần bảy, lớn hơn một chút so với một phần tám ban đầu. '
                        'Cũng có thể tính: một phần tám chia bảy phần tám.'),
    Beat('answer', 'solve', 'Đáp án: một phần bảy. Không phải một phần tư: thông tin chỉ loại một kết quả, không cho biết lần nào ngửa!'),
    Beat('outro', 'outro', outro_text(145)),
]

FORMULAS = formulas('1/7', OPTIONS,
                    nb='n(B) = 8 - 1 = 7',
                    prob='P(A | B) = (1/8)/(7/8) = 1/7')


def validate() -> bool:
    b = [s for s in SEQS if 'N' in s]
    assert F(sum(s == 'NNN' for s in b), len(b)) == F(1, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS145(ShortScene):
    N = 145

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[coin(c, .34) for c in s]).arrange(buff=.08) for s in SEQS]) \
            .arrange_in_grid(4, 2, buff=(.8, .22)).move_to([0, 1.25, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.rows[:2], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[2:], lag_ratio=.12), run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.play(self.rows[-1].animate.set_opacity(.15), run_time=self.rt(.06))
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.rows[0].animate.scale(1.2), *[c[0].animate.set_stroke(GOLD, 5) for c in self.rows[0]],
                  run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)


