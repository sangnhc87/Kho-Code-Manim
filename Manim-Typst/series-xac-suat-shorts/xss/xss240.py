"""XSS240 · Có cả trai lẫn gái — 4 con, bỏ TTTT và GGGG: 14 dãy, đúng 2 trai: 6 → 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS240', 'answer': '3/7'}
PROBLEM = ['Gia đình có $4$ con, biết có cả',
           'con trai lẫn con gái. Xác suất',
           'có đúng $2$ con trai?']
OPTIONS = ['3/8', '3/7', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 7
SEQS = [''.join(w) for w in product('TG', repeat=4)]

BEATS = [
    Beat('hook', 'hook', 'Một gia đình có bốn con. Bạn biết gia đình có cả con trai lẫn con gái. '
                         'Xác suất có đúng hai con trai là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tám, ba phần bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mười sáu dãy đồng khả năng. "Có cả trai lẫn gái" chỉ loại hai dãy: bốn trai và bốn gái. Còn mười bốn dãy.'),
    Beat('s2', 'solve', 'Đúng hai trai: chọn hai vị trí cho con trai, tổ hợp chập hai của bốn, sáu dãy, và cả sáu đều có con gái.'),
    Beat('s3', 'solve', 'Xác suất sáu phần mười bốn, tức ba phần bảy, lớn hơn ba phần tám lúc chưa biết.'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Điều kiện "có cả hai loại" chỉ loại hai trường hợp đơn sắc!'),
    Beat('outro', 'outro', outro_text(240)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    nb='n(B) = 16 - 2 = 14',
                    prob='P(A | B) = (C_4^2)/14 = 6/14 = 3/7')


def validate() -> bool:
    b = [s for s in SEQS if 0 < s.count('T') < 4]
    assert len(b) == 14 and F(sum(s.count('T') == 2 for s in b), 14) == F(3, 7) == F(comb(4, 2), 14)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS240(ShortScene):
    N = 240

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.rows = VGroup(*[VGroup(*[token(c, CYAN if c == 'T' else CORAL, .2, 16) for c in s]).arrange(buff=.05) for s in SEQS]) \
            .arrange_in_grid(4, 4, buff=(.35, .2))
        self.rows.scale_to_fit_width(min(self.rows.width, 7.2)).move_to([0, 1.3, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.rows, lag_ratio=.04), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[r.animate.set_opacity(.15) for r, s in zip(self.rows, SEQS) if s.count('T') in (0, 4)], run_time=self.rt(.06))
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        two = [r for r, s in zip(self.rows, SEQS) if s.count('T') == 2]
        self.play(*[r.animate.scale(1.15) for r in two], *[c[0].animate.set_stroke(GOLD, 3) for r in two for c in r],
                  run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
