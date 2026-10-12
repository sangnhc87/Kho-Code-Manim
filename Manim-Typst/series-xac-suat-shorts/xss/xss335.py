"""XSS335 · Đỏ áp đảo — 6 đỏ 4 xanh rút 5; đỏ > xanh ⇔ ≥ 3 đỏ: 120 + 60 + 6 = 186 / 252 = 31/42."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GREEN  # noqa: E402
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS335', 'answer': '31/42'}
PROBLEM = ['Hộp có $6$ bi đỏ, $4$ bi xanh. Rút $5$ bi.',
           'Xác suất số bi đỏ nhiều hơn số bi xanh?']
OPTIONS = ['31/42', '2/3', '5/6']
CORRECT = 0
ANSWER_VALUE = 31 / 42
WAYS = {k: comb(6, k) * comb(4, 5 - k) for k in range(1, 6)}

BEATS = [
    Beat('hook', 'hook', 'Hộp có sáu bi đỏ và bốn bi xanh. Rút ngẫu nhiên năm bi. Xác suất số bi đỏ nhiều hơn số bi xanh là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba mươi mốt phần bốn mươi hai, hai phần ba, hay năm phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Rút năm bi nên đỏ nhiều hơn xanh nghĩa là có ít nhất ba bi đỏ. Tổng số cách rút: hai trăm năm mươi hai.'),
    Beat('s2', 'solve', 'Ba đỏ hai xanh: hai mươi nhân sáu, một trăm hai mươi. Bốn đỏ một xanh: mười lăm nhân bốn, sáu mươi. Năm đỏ: sáu cách.'),
    Beat('s3', 'solve', 'Cộng lại một trăm tám mươi sáu trên hai trăm năm mươi hai, rút gọn ba mươi mốt phần bốn mươi hai.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi mốt phần bốn mươi hai. Dịch câu chữ nhiều hơn thành số lượng cụ thể rồi chia trường hợp.'),
    Beat('outro', 'outro', outro_text(335)),
]

FORMULAS = formulas('31/42', OPTIONS,
                    tot='C_10^5 = 252',
                    k3='C_6^3 C_4^2 = 120',
                    k4='C_6^4 C_4^1 = 60',
                    k5='C_6^5 = 6',
                    prob='P = (120 + 60 + 6)/252 = 31/42')


def validate() -> bool:
    good = WAYS[3] + WAYS[4] + WAYS[5]
    assert good == 186 and F(good, comb(10, 5)) == F(31, 42)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS335(ShortScene):
    N = 335

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.u = urn('RRRRRRBBBB', cols=5, r=.28).move_to([0, 2.1, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('tot', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        rows = VGroup(VGroup(ball_row('RRRBB', r=.22, buff=.08), self.M('k3', 1.0)).arrange(buff=.4),
                      VGroup(ball_row('RRRRB', r=.22, buff=.08), self.M('k4', 1.0)).arrange(buff=.4),
                      VGroup(ball_row('RRRRR', r=.22, buff=.08), self.M('k5', 1.0)).arrange(buff=.4))
        rows.arrange(DOWN, buff=.25, aligned_edge=[-1, 0, 0]).move_to([0, .1, 0])
        for i, f in enumerate((.05, .4, .75)):
            self.wait_until(f, t0)
            self.play(FadeIn(rows[i]), run_time=self.rt(.05))
        self.rows = rows

    def beat_s3(self, T):
        self.play(*[r[1].animate.set_color(GREEN) for r in self.rows], run_time=self.rt(.05))
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
