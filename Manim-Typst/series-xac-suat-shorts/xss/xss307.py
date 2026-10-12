"""XSS307 · Tám lần không hai ngửa — Fibonacci: a_8 = 55 → 55/256."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS307', 'answer': '55/256'}
PROBLEM = ['Tung đồng xu $8$ lần. Xác suất không',
           'có $2$ lần ngửa liên tiếp?']
OPTIONS = ['1/4', '55/256', '34/256']
CORRECT = 1
ANSWER_VALUE = 55 / 256


def count(n):
    return sum('NN' not in ''.join(w) for w in product('SN', repeat=n))


BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu tám lần. Xác suất không có hai lần ngửa nào đứng liền nhau là bao nhiêu? '
                         'Với bốn lần tung ta đã biết là một phần hai.'),
    Beat('guess', 'hook', 'Một phần tư, năm mươi lăm phần hai trăm năm mươi sáu, hay ba mươi tư phần hai trăm năm mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dãy tốt kết thúc bằng sấp, hoặc bằng sấp ngửa. Nên a n bằng a n trừ một cộng a n trừ hai: dãy Fibonacci.'),
    Beat('s2', 'solve', 'Hai, ba, năm, tám, mười ba, hai mươi mốt, ba mươi tư, năm mươi lăm. Tám lần tung có năm mươi lăm dãy tốt.'),
    Beat('s3', 'solve', 'Xác suất năm mươi lăm phần hai trăm năm mươi sáu, chỉ khoảng hai mươi mốt phần trăm. Càng tung nhiều, càng khó tránh hai ngửa liền nhau!'),
    Beat('answer', 'solve', 'Đáp án: năm mươi lăm phần hai trăm năm mươi sáu. Fibonacci đếm các dãy không có hai ngửa liền nhau!'),
    Beat('outro', 'outro', outro_text(307)),
]

FORMULAS = formulas('55/256', OPTIONS,
                    fib='2, quad 3, quad 5, quad 8, quad 13, quad 21, quad 34, quad 55',
                    prob='P = 55/2^8 = 55/256 approx "0,21"')


def validate() -> bool:
    assert [count(n) for n in range(1, 9)] == [2, 3, 5, 8, 13, 21, 34, 55]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS307(ShortScene):
    N = 307

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.9
        vals = [F(count(n), 2 ** n) for n in range(1, 9)]
        self.bars = VGroup()
        for k, v in enumerate(vals):
            r = Rectangle(width=.55, height=h * float(v), stroke_width=0, fill_color=GOLD if k == 7 else CYAN, fill_opacity=.85)
            r.move_to([-3.0 + .85 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k + 1}$', 22, SOFT).next_to([-3.0 + .85 * k, base, 0], DOWN, buff=.08) for k in range(8)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.TM('$a_n = a_(n-1) + a_(n-2)$', 32, GOLD))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('fib', 1.6))
        self.wait_until(.4, t0)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m, CORAL)
