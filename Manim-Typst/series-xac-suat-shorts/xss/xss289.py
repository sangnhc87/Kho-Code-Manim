"""XSS289 · Ếch có gió đẩy — r = q/p = 1/3: P(chạm +2 trước −2 từ 0) = (1 − r²)/(1 − r⁴) = 9/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS289', 'answer': '9/10'}
PROBLEM = ['Ếch ở $0$, mỗi bước nhảy $+1$ (xác suất',
           '$3/4$) hoặc $-1$ ($1/4$). Xác suất ếch',
           'chạm $2$ trước khi chạm $-2$?']
OPTIONS = ['3/4', '9/10', '27/28']
CORRECT = 1
ANSWER_VALUE = .9


def solve():
    p, q = F(3, 4), F(1, 4)
    # x_{-1} = p x_0 + q·0, x_0 = p x_1 + q x_{-1}, x_1 = p·1 + q x_0
    # substitute: x_0 = p(p + q x_0) + q(p x_0) ⇒ x_0 (1 − 2pq) = p²
    return p * p / (1 - 2 * p * q)


BEATS = [
    Beat('hook', 'hook', 'Gió thổi về phía trước: ếch nhảy tới với xác suất ba phần tư, lùi với xác suất một phần tư. '
                         'Ếch bắt đầu ở không. Xác suất ếch chạm lá cộng hai trước khi chạm lá trừ hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tư, chín phần mười, hay hai mươi bảy phần hai mươi tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xét từng cặp hai bước. Tới tới: chạm cộng hai, xác suất chín phần mười sáu. Lùi lùi: chạm trừ hai, một phần mười sáu.'),
    Beat('s2', 'solve', 'Tới lùi hoặc lùi tới: về lại không, xác suất sáu phần mười sáu, cây lặp lại. Vậy chỉ cần so sánh hai kết thúc.'),
    Beat('s3', 'solve', 'Xác suất chạm cộng hai bằng chín chia chín cộng một, tức chín phần mười. Lợi thế ba chọi một mỗi bước thành chín chọi một ở đích!'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười. Gộp hai bước thành một vòng, bài con bạc phá sản hóa thành so sánh hai lá!'),
    Beat('outro', 'outro', outro_text(289)),
]

FORMULAS = formulas('9/10', OPTIONS,
                    pair='P(+ +) = 9/16, quad P(- -) = 1/16, quad P("về 0") = 6/16',
                    prob='P = 9/(9 + 1) = 9/10')


def validate() -> bool:
    assert solve() == F(9, 10) == (1 - F(1, 3) ** 2) / (1 - F(1, 3) ** 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS289(ShortScene):
    N = 289

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(-2, 3), y=1.7, bad=())
        self.row[0].set_fill(CORAL, .8)
        self.row[-1].set_fill(GREEN, .8)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, SOFT).next_to(q, [0, -1, 0], buff=.15) for k, q in zip(range(-2, 3), self.row)])
        self.fr = frog().move_to(self.row[2])
        self.wait_until(.7, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        for k in (3, 4):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.04))
        self.wait_until(.45, t0)
        self.play(self.fr.animate.move_to(self.row[2]), run_time=self.rt(.04))
        self.write_board(self.M('pair', 1.4))

    def beat_s2(self, T):
        self.play(self.fr.animate.move_to(self.row[3]), run_time=self.rt(.04))
        self.play(self.fr.animate.move_to(self.row[2]), run_time=self.rt(.04))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)
