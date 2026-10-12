"""XSS324 · Tâm và hai đỉnh lục giác — 15 cặp đỉnh − 3 cặp đối tâm = 12 tam giác OAB; đều ⇔ A, B kề nhau: 6 → 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import Dot, FadeIn, FadeOut, Line, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin  # noqa: E402

EPISODE = {'code': 'XSS324', 'answer': '1/2'}
PROBLEM = ['Chọn $2$ đỉnh của lục giác đều tâm $O$.',
           'Biết cùng $O$ chúng tạo thành tam giác.',
           'Xác suất đó là tam giác đều?']
OPTIONS = ['1/3', '1/2', '2/5']
CORRECT = 1
ANSWER_VALUE = .5
PAIRS = [p for p in combinations(range(6), 2) if p[1] - p[0] != 3]
ADJ = [p for p in PAIRS if (p[1] - p[0]) % 6 in (1, 5)]
C0 = (0, .9)

BEATS = [
    Beat('hook', 'hook', 'Lục giác đều tâm O. Chọn ngẫu nhiên hai đỉnh, biết hai đỉnh đó cùng với tâm O tạo thành một tam giác thật sự. '
                         'Xác suất tam giác đó đều là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có mười lăm cặp đỉnh. Ba cặp đối xứng qua tâm thì thẳng hàng với O, không tạo tam giác. Điều kiện còn mười hai cặp.'),
    Beat('s2', 'solve', 'Hai đỉnh kề nhau: góc ở tâm sáu mươi độ, hai cạnh bằng bán kính, nên tam giác đều. Lục giác có sáu cặp đỉnh kề.'),
    Beat('s3', 'solve', 'Hai đỉnh cách một đỉnh: góc ở tâm một trăm hai mươi độ, tam giác cân nhưng không đều. Vậy xác suất sáu phần mười hai, bằng một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Lục giác đều chính là sáu tam giác đều ghép quanh tâm.'),
    Beat('outro', 'outro', outro_text(324)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    cond='C_6^2 - 3 = 12',
                    adj='6 "cặp kề" arrow.r 60 degree',
                    prob='P = 6/12 = 1/2')


def validate() -> bool:
    assert len(PAIRS) == 12 and len(ADJ) == 6
    assert F(len(ADJ), len(PAIRS)) == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS324(PolyMixin, ShortScene):
    N = 324

    def tri(self, p, color):
        return Polygon([C0[0], C0[1], 0], self.pts[p[0]], self.pts[p[1]], stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=.35)

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(6, center=C0)
        self.o = Dot([C0[0], C0[1], 0], radius=.11, color=GOLD)
        self.play(FadeIn(self.o), run_time=self.rt(.03))
        self.wait_until(.5, t0)
        self.cur = self.tri((0, 2), CYAN)
        self.play(FadeIn(self.cur), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.diam = VGroup(*[Line(self.pts[i], self.pts[i + 3], color=CORAL, stroke_width=5) for i in range(3)])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.diam), run_time=self.rt(.06))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.diam), run_time=self.rt(.03))
        tris = VGroup(*[self.tri(p, GREEN) for p in ADJ])
        self.wait_until(.35, t0)
        self.play(FadeIn(tris, lag_ratio=.3), run_time=self.rt(.15))
        self.write_board(self.M('adj', 1.5))
        self.tris = tris

    def beat_s3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tris), run_time=self.rt(.03))
        self.cur = self.tri((0, 2), CYAN)
        self.play(FadeIn(self.cur), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
