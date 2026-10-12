"""XSS327 · Bát giác: vuông thì có cân? — 4 đường kính × 6 = 24 tam giác vuông; vuông cân: 2 mỗi đường kính = 8 → 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, FadeOut, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin, is_iso, is_right, triangles  # noqa: E402

EPISODE = {'code': 'XSS327', 'answer': '1/3'}
PROBLEM = ['Chọn $3$ đỉnh của bát giác đều. Biết',
           'được tam giác vuông. Xác suất đó là',
           'tam giác vuông cân?']
OPTIONS = ['1/4', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
N_ = 8
RIGHT = triangles(N_, is_right(N_))
ISO = [t for t in RIGHT if is_iso(N_)(t)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của một bát giác đều. Biết ba đỉnh tạo thành tam giác vuông. '
                         'Xác suất nó là tam giác vuông cân bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tam giác nội tiếp vuông khi có cạnh là đường kính. Bát giác có bốn đường kính, mỗi đường ghép với sáu đỉnh còn lại: hai mươi bốn tam giác vuông.'),
    Beat('s2', 'solve', 'Vuông cân thì đỉnh góc vuông nằm chính giữa nửa đường tròn, tức trên đường kính vuông góc. Mỗi đường kính có đúng hai đỉnh như vậy: tám tam giác.'),
    Beat('s3', 'solve', 'Xác suất tám phần hai mươi bốn, tức một phần ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Với đa giác hai n cạnh, câu trả lời luôn là một phần n trừ một.'),
    Beat('outro', 'outro', outro_text(327)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    right='4 dot 6 = 24',
                    iso='4 dot 2 = 8',
                    prob='P = 8/24 = 1/3')


def validate() -> bool:
    assert len(RIGHT) == 24 and len(ISO) == 8
    assert F(len(ISO), len(RIGHT)) == F(1, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS327(PolyMixin, ShortScene):
    N = 327

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.45, t0)
        self.cur = self.flash([(0, 1, 4), (0, 2, 4)], CYAN, .12)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        diam = VGroup(*[Line(self.pts[i], self.pts[i + 4], color=GOLD, stroke_width=4) for i in range(4)])
        self.play(FadeIn(diam), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.play(FadeOut(diam), run_time=self.rt(.03))
        self.cur = self.flash([(0, k, 4) for k in (1, 3, 5, 7)], CYAN, .2)
        self.write_board(self.M('right', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash([(0, 2, 4), (0, 4, 6), (2, 4, 6)], GREEN, .2)
        self.write_board(self.M('iso', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
