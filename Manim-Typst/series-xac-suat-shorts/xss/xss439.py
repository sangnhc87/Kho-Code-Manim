"""XSS439 · Hai ô trên bàn cờ — ô thứ nhất tùy ý; ô thứ hai cùng màu: 31 ô, bỏ 3 ô cùng hàng và 3 ô cùng cột cùng màu → 25/63."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, PANEL_2, SOFT  # noqa: E402

EPISODE = {'code': 'XSS439', 'answer': '25/63'}
PROBLEM = ['Chọn $2$ ô của bàn cờ $8 times 8$. Xác suất',
           'hai ô cùng màu và không cùng hàng, cùng',
           'cột?']
OPTIONS = ['25/63', '31/63', '1/2']
CORRECT = 0
ANSWER_VALUE = 25 / 63
CELLS = [(r, c) for r in range(8) for c in range(8)]
GOOD = sum((a[0] + a[1]) % 2 == (b[0] + b[1]) % 2 and a[0] != b[0] and a[1] != b[1] for a, b in combinations(CELLS, 2))
S = .42

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai ô của bàn cờ vua tám nhân tám. Xác suất hai ô cùng màu, và không nằm cùng hàng hay cùng cột?'),
    Beat('guess', 'hook', 'Hai mươi lăm phần sáu mươi ba, ba mươi mốt phần sáu mươi ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chọn ô thứ nhất tùy ý. Ô thứ hai là một trong sáu mươi ba ô còn lại, đồng khả năng.'),
    Beat('s2', 'solve', 'Cùng màu với ô thứ nhất có ba mươi mốt ô. Trong hàng của nó có ba ô cùng màu, trong cột của nó cũng ba ô cùng màu. Bỏ đi còn hai mươi lăm.'),
    Beat('s3', 'solve', 'Xác suất hai mươi lăm phần sáu mươi ba. Cố định một đối tượng, đếm đối tượng còn lại: gọn hơn đếm cặp.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi lăm phần sáu mươi ba. Đây cũng là xác suất hai quân tượng cùng màu không bị xe nhìn thấy nhau theo hàng cột.'),
    Beat('outro', 'outro', outro_text(439)),
]

FORMULAS = formulas('25/63', OPTIONS,
                    cnt='31 - 3 - 3 = 25',
                    prob='P = 25/63')


def validate() -> bool:
    assert F(GOOD, comb(64, 2)) == F(25, 63)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS439(ShortScene):
    N = 439

    def P(self, r, c):
        return [-3.5 * S + c * S, .9 + 3.5 * S - r * S, 0]

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.sq = VGroup(*[Square(S, stroke_width=0, fill_color=SOFT if (r + c) % 2 == 0 else PANEL_2, fill_opacity=.9).move_to(self.P(r, c))
                           for r, c in CELLS])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.sq), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.sq[2 * 8 + 3].animate.set_fill(GOLD, 1), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        same = [i for i, (r, c) in enumerate(CELLS) if (r + c) % 2 == 1 and (r, c) != (2, 3)]
        self.play(*[self.sq[i].animate.set_fill(GREEN, .9) for i in same], run_time=self.rt(.08))
        self.wait_until(.5, t0)
        bad = [i for i in same if CELLS[i][0] == 2 or CELLS[i][1] == 3]
        self.play(*[self.sq[i].animate.set_fill(CORAL, .9) for i in bad], run_time=self.rt(.06))
        self.write_board(self.M('cnt', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
