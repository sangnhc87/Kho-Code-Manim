"""XSS352 · Bốn cặp quanh bàn tròn — 7! = 5040 cách; bao hàm loại trừ Σ(−1)ᵏ C(4;k) 2ᵏ (7 − k)! = 1488 → 31/105."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
from pathlib import Path

from manim import Circle, FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL_2, STROKE  # noqa: E402
from common.visuals import polygon_pts, token  # noqa: E402

EPISODE = {'code': 'XSS352', 'answer': '31/105'}
PROBLEM = ['$4$ cặp vợ chồng ngồi ngẫu nhiên quanh',
           'bàn tròn $8$ ghế. Xác suất không cặp nào',
           'ngồi cạnh nhau?']
OPTIONS = ['31/105', '1/3', '2/7']
CORRECT = 0
ANSWER_VALUE = 31 / 105
COL = [CYAN, CORAL, GOLD, GREEN]
TERMS = [(-1) ** k * comb(4, k) * 2 ** k * factorial(7 - k) for k in range(5)]


def brute():
    good = 0
    for p in permutations(range(1, 8)):
        seat = (0,) + p
        pos = {v: i for i, v in enumerate(seat)}
        good += all((pos[2 * k] - pos[2 * k + 1]) % 8 not in (1, 7) for k in range(4))
    return good


BEATS = [
    Beat('hook', 'hook', 'Bốn cặp vợ chồng ngồi ngẫu nhiên quanh một bàn tròn tám ghế. Xác suất không có cặp nào ngồi cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba mươi mốt phần một trăm lẻ năm, một phần ba, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cố định một người để khử phép xoay: bảy người còn lại có bảy giai thừa, năm nghìn không trăm bốn mươi cách.'),
    Beat('s2', 'solve', 'Dùng bao hàm loại trừ. Chọn k cặp buộc ngồi cạnh: dán mỗi cặp thành một khối, hoán đổi trong khối hai cách, còn tám trừ k phần tử quanh bàn: bảy trừ k giai thừa cách.'),
    Beat('s3', 'solve', 'Năm nghìn không trăm bốn mươi, trừ năm nghìn bảy trăm sáu mươi, cộng hai nghìn tám trăm tám mươi, trừ bảy trăm sáu mươi tám, cộng chín mươi sáu: còn một nghìn bốn trăm tám mươi tám.'),
    Beat('s4', 'solve', 'Xác suất một nghìn bốn trăm tám mươi tám phần năm nghìn không trăm bốn mươi, rút gọn ba mươi mốt phần một trăm lẻ năm, khoảng ba mươi phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi mốt phần một trăm lẻ năm. Bàn tròn: cố định một người, rồi bao hàm loại trừ.'),
    Beat('outro', 'outro', outro_text(352)),
]

FORMULAS = formulas('31/105', OPTIONS,
                    all='7! = 5040',
                    ie='sum_(k=0)^4 (-1)^k C_4^k dot 2^k dot (7-k)!',
                    num='5040 - 5760 + 2880 - 768 + 96 = 1488',
                    prob='P = 1488/5040 = 31/105')


def validate() -> bool:
    assert sum(TERMS) == 1488 == brute()
    assert F(1488, 5040) == F(31, 105)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS352(ShortScene):
    N = 352

    def place(self, order, frac=.06):
        new = VGroup(*[token(str(v // 2 + 1), COL[v // 2], .3).move_to(p) for v, p in zip(order, self.pts)])
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.ppl = None
        self.pts = polygon_pts(8, 1.85, (0, 1.0))
        self.table = Circle(radius=1.2, stroke_color=STROKE, stroke_width=4, fill_color=PANEL_2, fill_opacity=1).move_to([0, 1.0, 0])
        self.play(FadeIn(self.table), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.place([0, 2, 1, 4, 6, 3, 5, 7])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.place([0, 1, 2, 4, 3, 6, 5, 7], .06)
        self.wait_until(.5, t0)
        self.clear_board(.03)
        self.write_board(self.M('ie', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('num', 1.3))

    def beat_s4(self, T):
        self.place([0, 2, 4, 6, 1, 3, 5, 7], .06)
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
