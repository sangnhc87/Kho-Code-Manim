"""XSS271 · Bàn Galton — 4 hàng đinh, rơi vào ô giữa khi đúng 2 lần lệch phải: C(4,2)/16 = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import DOWN, Dot, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, WHITE  # noqa: E402

EPISODE = {'code': 'XSS271', 'answer': '3/8'}
PROBLEM = ['Bi rơi qua $4$ hàng đinh, mỗi đinh làm bi',
           'lệch trái hoặc phải với xác suất $1/2$.',
           'Xác suất bi rơi vào ô chính giữa?']
OPTIONS = ['1/5', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8

BEATS = [
    Beat('hook', 'hook', 'Bàn Galton: viên bi rơi qua bốn hàng đinh, mỗi lần chạm đinh thì lệch sang trái hoặc phải, khả năng như nhau. '
                         'Có năm ô hứng ở dưới. Xác suất bi rơi vào ô chính giữa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bàn đinh chính là một sơ đồ cây hình tam giác, các nhánh gặp lại nhau. Mỗi đường đi gồm bốn lần chọn trái phải: mười sáu đường đồng khả năng.'),
    Beat('s2', 'solve', 'Ô thứ k nhận các đường có đúng k lần lệch phải: tổ hợp chập k của bốn. Ô giữa ứng với hai lần phải: sáu đường.'),
    Beat('s3', 'solve', 'Xác suất sáu phần mười sáu, tức ba phần tám. Năm ô có tỉ lệ một, bốn, sáu, bốn, một: tam giác Pascal hiện ra!'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Cây có các nhánh hội tụ thì đếm số đường đến mỗi nút: đó là tam giác Pascal!'),
    Beat('outro', 'outro', outro_text(271)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    paths='1, quad 4, quad 6, quad 4, quad 1',
                    prob='P = (C_4^2)/2^4 = 6/16 = 3/8')


def validate() -> bool:
    assert F(sum(sum(w) == 2 for w in product((0, 1), repeat=4)), 16) == F(3, 8) == F(comb(4, 2), 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS271(ShortScene):
    N = 271

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.pegs = VGroup(*[Dot([(j - r / 2) * .9, 2.8 - .55 * r, 0], radius=.08, color=WHITE) for r in range(4) for j in range(r + 1)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.pegs, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        labs = VGroup(*[self.MNum(comb(r, j), 0, GOLD, 22).move_to([(j - r / 2) * .9, 2.8 - .55 * r + .25, 0])
                        for r in range(4) for j in range(r + 1)])
        self.wait_until(.4, t0)
        self.play(FadeIn(labs, lag_ratio=.05), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        base, h = -.15, 1.2
        bars = VGroup()
        for k in range(5):
            r = Rectangle(width=.7, height=h * comb(4, k) / 6, stroke_width=0, fill_color=GOLD if k == 2 else CYAN, fill_opacity=.85)
            r.move_to([(k - 2) * .9, base + r.height / 2, 0])
            bars.add(r)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.write_board(self.M('paths', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)


