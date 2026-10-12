"""XSS330 · Ít nhất hai đỏ — 5 đỏ 5 xanh rút 4; ≥ 2 đỏ: 100 + 50 + 5 = 155 bộ, đúng 2 đỏ: 100 → 20/31."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GREEN, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS330', 'answer': '20/31'}
PROBLEM = ['Hộp có $5$ bi đỏ, $5$ bi xanh. Rút $4$ bi,',
           'biết có ít nhất $2$ bi đỏ. Xác suất có',
           'đúng $2$ bi đỏ?']
OPTIONS = ['20/31', '10/21', '2/3']
CORRECT = 0
ANSWER_VALUE = 20 / 31
WAYS = {k: comb(5, k) * comb(5, 4 - k) for k in range(5)}

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ và năm bi xanh. Rút ngẫu nhiên bốn bi, biết trong đó có ít nhất hai bi đỏ. '
                         'Xác suất có đúng hai bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi phần ba mươi mốt, mười phần hai mươi mốt, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm số bộ theo số bi đỏ. Hai đỏ hai xanh: mười nhân mười, một trăm bộ. Ba đỏ một xanh: mười nhân năm, năm mươi bộ. Bốn đỏ: năm bộ.'),
    Beat('s2', 'solve', 'Điều kiện ít nhất hai đỏ gồm cả ba nhóm: một trăm năm mươi lăm bộ.'),
    Beat('s3', 'solve', 'Trong đó đúng hai đỏ có một trăm bộ. Xác suất một trăm phần một trăm năm mươi lăm, rút gọn hai mươi phần ba mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi phần ba mươi mốt. Với điều kiện ít nhất, cứ chia nhóm theo số lượng rồi đếm.'),
    Beat('outro', 'outro', outro_text(330)),
]

FORMULAS = formulas('20/31', OPTIONS,
                    k2='C_5^2 C_5^2 = 100',
                    k3='C_5^3 C_5^1 = 50',
                    k4='C_5^4 = 5',
                    prob='P = 100/(100 + 50 + 5) = 20/31')


def validate() -> bool:
    cond = WAYS[2] + WAYS[3] + WAYS[4]
    assert (WAYS[2], cond) == (100, 155) and F(WAYS[2], cond) == F(20, 31)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS330(ShortScene):
    N = 330

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.u = urn('RRRRRBBBBB', cols=5, r=.28).move_to([0, 2.0, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        rows = VGroup()
        for i, (cols, key) in enumerate((('RRBB', 'k2'), ('RRRB', 'k3'), ('RRRR', 'k4'))):
            r = VGroup(ball_row(cols, r=.24, buff=.1), self.M(key, 1.0)).arrange(buff=.5)
            rows.add(r)
        rows.arrange(DOWN, buff=.3, aligned_edge=[-1, 0, 0]).move_to([0, .1, 0])
        self.rows = rows
        for i, frac in enumerate((.1, .4, .7)):
            self.wait_until(frac, t0)
            self.play(FadeIn(rows[i]), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('$100 + 50 + 5 = 155$', 34, SOFT), anim='fade')

    def beat_s3(self, T):
        self.play(self.rows[0][1].animate.set_color(GREEN), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
