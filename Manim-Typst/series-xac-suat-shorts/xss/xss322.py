"""XSS322 · Vuông cân trong lập phương — 56 bộ ba đỉnh: 8 tam giác đều, 48 tam giác vuông; vuông cân nằm trên mặt: 6·4 = 24 → 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, FadeOut, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import CUBE, cube_mob, cube_view, d2  # noqa: E402

EPISODE = {'code': 'XSS322', 'answer': '1/2'}
PROBLEM = ['Chọn $3$ đỉnh của hình lập phương. Biết',
           'được một tam giác vuông. Xác suất đó là',
           'tam giác vuông cân?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
TRI = list(combinations(CUBE, 3))


def sides(t):
    return sorted((d2(t[0], t[1]), d2(t[1], t[2]), d2(t[0], t[2])))


RIGHT = [t for t in TRI if sides(t)[0] + sides(t)[1] == sides(t)[2]]
ISO = [t for t in RIGHT if sides(t) == [1, 1, 2]]
EQ = [t for t in TRI if sides(t) == [2, 2, 2]]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của hình lập phương. Biết ba đỉnh tạo thành tam giác vuông. '
                         'Xác suất đó là tam giác vuông cân bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có năm mươi sáu bộ ba đỉnh. Tam giác không vuông duy nhất là tam giác đều tạo bởi ba đường chéo mặt, mỗi đỉnh cắt ra một cái: tám tam giác. '
                        'Vậy có bốn mươi tám tam giác vuông.'),
    Beat('s2', 'solve', 'Tam giác vuông cân có hai cạnh góc vuông là cạnh lập phương, nằm gọn trên một mặt. Mỗi mặt có bốn tam giác như vậy, sáu mặt là hai mươi bốn.'),
    Beat('s3', 'solve', 'Hai mươi bốn tam giác vuông còn lại có cạnh một, căn hai, căn ba, không cân. Xác suất hai mươi bốn phần bốn mươi tám, đúng một nửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Phân loại tam giác theo độ dài ba cạnh là cách đếm gọn nhất trong không gian.'),
    Beat('outro', 'outro', outro_text(322)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    cond='C_8^3 - 8 = 48',
                    iso='6 dot 4 = 24',
                    other='(1; sqrt(2); sqrt(3)): 24',
                    prob='P = 24/48 = 1/2')


def validate() -> bool:
    assert len(TRI) == 56 and len(EQ) == 8 and len(RIGHT) == 48 and len(ISO) == 24
    assert F(len(ISO), len(RIGHT)) == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS322(ShortScene):
    N = 322

    def tri(self, t, color):
        return Polygon(*[cube_view(v) for v in t], stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=.35)

    def swap(self, t, color, frac=.05):
        new = self.tri(t, color)
        self.play(*([FadeOut(self.cur)] if self.cur else []), FadeIn(new), run_time=self.rt(frac))
        self.cur = new

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.cur = None
        self.cube = cube_mob()
        self.wait_until(.35, t0)
        self.play(FadeIn(self.cube), run_time=self.rt(.08))
        self.swap(ISO[0], CYAN)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        for t in EQ[:2]:
            self.swap(t, CORAL)
        self.wait_until(.7, t0)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        for t in ISO[:3]:
            self.swap(t, GREEN, .06)
        self.wait_until(.6, t0)
        m = self.M('iso', 1.6)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        other = [t for t in RIGHT if t not in ISO]
        self.swap(other[0], GOLD, .06)
        self.write_board(self.M('other', 1.4))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
