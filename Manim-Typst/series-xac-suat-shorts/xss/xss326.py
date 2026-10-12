"""XSS326 · Dây cung dài — 12-giác: 66 dây − 6 đường kính = 60; dài hơn cạnh tam giác đều nội tiếp (cung 4) ⇔ cung 5: 12 dây → 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, FadeOut, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin  # noqa: E402

EPISODE = {'code': 'XSS326', 'answer': '1/5'}
PROBLEM = ['Chọn $2$ đỉnh của đa giác đều $12$ cạnh,',
           'biết dây nối không qua tâm. Xác suất dây',
           'dài hơn cạnh tam giác đều nội tiếp?']
OPTIONS = ['1/5', '1/4', '1/3']
CORRECT = 0
ANSWER_VALUE = .2
N_ = 12


def arc(p):
    return min(p[1] - p[0], N_ - p[1] + p[0])


CHORDS = [p for p in combinations(range(N_), 2) if arc(p) != 6]
LONG = [p for p in CHORDS if arc(p) > 4]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai đỉnh của đa giác đều mười hai cạnh. Biết dây nối hai đỉnh không đi qua tâm. '
                         'Xác suất dây dài hơn cạnh tam giác đều nội tiếp là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, một phần tư, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có sáu mươi sáu dây. Sáu dây là đường kính, đi qua tâm, bị loại. Điều kiện còn sáu mươi dây.'),
    Beat('s2', 'solve', 'Độ dài dây tăng theo số cạnh của cung nhỏ nó chắn, từ một đến sáu. Cạnh tam giác đều nội tiếp chắn cung bốn cạnh.'),
    Beat('s3', 'solve', 'Dài hơn thì cung phải lớn hơn bốn, mà cung sáu là đường kính đã loại, nên chỉ còn cung năm: mười hai dây. Xác suất mười hai phần sáu mươi, tức một phần năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Quy độ dài dây về số cạnh của cung chắn là đếm được ngay.'),
    Beat('outro', 'outro', outro_text(326)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    cond='C_12^2 - 6 = 60',
                    side='"cạnh tam giác đều" <-> "cung" 4',
                    prob='P = 12/60 = 1/5')


def validate() -> bool:
    assert len(CHORDS) == 60 and len(LONG) == 12
    assert F(len(LONG), len(CHORDS)) == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS326(PolyMixin, ShortScene):
    N = 326

    def chords(self, ps, color, w=4):
        return VGroup(*[Line(self.pts[a], self.pts[b], color=color, stroke_width=w) for a, b in ps])

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.45, t0)
        self.cur = self.chords([(0, 5)], CYAN, 6)
        self.play(FadeIn(self.cur), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.chords([(i, i + 6) for i in range(6)], CORAL)
        self.wait_until(.35, t0)
        self.play(FadeIn(self.cur), run_time=self.rt(.06))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.tri = self.shape((0, 4, 8), GOLD, .15)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.tri), run_time=self.rt(.06))
        self.clear_board(.03)
        self.write_board(self.M('side', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.cur = self.chords(LONG, GREEN, 3)
        self.wait_until(.35, t0)
        self.play(FadeIn(self.cur, lag_ratio=.1), run_time=self.rt(.12))
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
