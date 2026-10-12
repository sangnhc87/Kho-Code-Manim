"""XSS316 · Phần trái dài hơn 0,3 — x đều trên [0;1], biết x > 0,3; x > 2(1 − x) ⇔ x > 2/3 → (1/3)/(7/10) = 10/21."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, UP, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS316', 'answer': '10/21'}
PROBLEM = ['Chọn ngẫu nhiên điểm $x$ trên $[0; 1]$.',
           'Biết $x > "0,3"$. Xác suất $x > 2(1 - x)$?']
OPTIONS = ['1/3', '10/21', '4/7']
CORRECT = 1
ANSWER_VALUE = 10 / 21
L0, L1, Y = -3.2, 3.2, 1.0


def X(t):
    return [L0 + (L1 - L0) * t, Y, 0]


BEATS = [
    Beat('hook', 'hook', 'Bẻ một que dài một mét tại điểm x ngẫu nhiên. Biết phần bên trái dài hơn không phẩy ba mét. '
                         'Xác suất phần trái dài hơn gấp đôi phần phải là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, mười phần hai mươi mốt, hay bốn phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện x lớn hơn không phẩy ba để lại đoạn từ không phẩy ba đến một, dài không phẩy bảy.'),
    Beat('s2', 'solve', 'Bất phương trình x lớn hơn hai lần một trừ x tương đương ba x lớn hơn hai, tức x lớn hơn hai phần ba. Đoạn đó dài một phần ba.'),
    Beat('s3', 'solve', 'Đoạn từ hai phần ba đến một nằm trọn trong đoạn điều kiện. Xác suất bằng một phần ba chia không phẩy bảy, tức mười phần hai mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: mười phần hai mươi mốt. Trên đoạn thẳng, xác suất có điều kiện là tỉ số độ dài.'),
    Beat('outro', 'outro', outro_text(316)),
]

FORMULAS = formulas('10/21', OPTIONS,
                    cond='x in ("0,3"; 1] arrow.r "dài" 7/10',
                    ineq='x > 2(1 - x) <=> x > 2/3',
                    prob='P = (1/3)/(7/10) = 10/21')


def validate() -> bool:
    assert (1 - F(2, 3)) / (1 - F(3, 10)) == F(10, 21)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS316(ShortScene):
    N = 316

    def hook_visual(self, t0):
        self.board_top = -1.0
        base = Line(X(0), X(1), color=STROKE, stroke_width=10)
        ticks = VGroup(*[self.TM(f'${s}$', 28, SOFT).next_to(X(v), DOWN, buff=.25) for s, v in (('0', 0), ('1', 1))])
        self.play(FadeIn(base), FadeIn(ticks), run_time=self.rt(.06))
        self.base = base
        self.wait_until(.5, t0)
        cut = Line(X(.8) + UP * .4, X(.8) + DOWN * .4, color=GOLD, stroke_width=6)
        self.play(FadeIn(cut), run_time=self.rt(.04))
        self.cut = cut

    def beat_s1(self, T):
        t0 = self.now()
        self.cond = Line(X(.3), X(1), color=CYAN, stroke_width=14)
        lab = self.TM('$"0,3"$', 28, CYAN).next_to(X(.3), DOWN, buff=.25)
        self.play(FadeIn(self.cond), FadeIn(lab), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('ineq', 1.5))
        self.wait_until(.6, t0)
        good = Line(X(2 / 3), X(1), color=GREEN, stroke_width=20)
        lab = self.TM('$2/3$', 30, GREEN).next_to(X(2 / 3), UP, buff=.3)
        bad = Line(X(0), X(.3), color=CORAL, stroke_width=10)
        self.play(FadeIn(good), FadeIn(lab), FadeIn(bad), run_time=self.rt(.08))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
