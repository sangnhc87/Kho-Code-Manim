"""XSS313 · Có cạnh lục giác thì vuông? — 20 − 2 = 18 tam giác có cạnh lục giác; 12 tam giác vuông (chứa đường kính) đều thuộc nhóm đó → 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Create, FadeOut, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin, arcs, is_right, triangles  # noqa: E402

EPISODE = {'code': 'XSS313', 'answer': '2/3'}
PROBLEM = ['Chọn $3$ đỉnh lục giác đều. Biết tam giác',
           'có ít nhất một cạnh là cạnh lục giác.',
           'Xác suất tam giác vuông?']
OPTIONS = ['1/2', '2/3', '3/5']
CORRECT = 1
ANSWER_VALUE = 2 / 3
N_ = 6
COND = triangles(N_, lambda t: 1 in arcs(t, N_))
RIGHT = [t for t in COND if is_right(N_)(t)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của một lục giác đều. Biết tam giác tạo thành có ít nhất một cạnh trùng cạnh lục giác. '
                         'Xác suất nó là tam giác vuông bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có hai mươi cách chọn ba đỉnh. Chỉ hai tam giác không có cạnh nào là cạnh lục giác: hai tam giác đều xen kẽ. '
                        'Vậy điều kiện còn mười tám tam giác.'),
    Beat('s2', 'solve', 'Tam giác nội tiếp vuông khi và chỉ khi có một cạnh là đường kính. Lục giác có ba đường kính, mỗi đường ghép với bốn đỉnh còn lại: mười hai tam giác vuông.'),
    Beat('s3', 'solve', 'Mỗi tam giác vuông đó đều có một cạnh là cạnh lục giác, nên cả mười hai nằm trong mười tám. Xác suất mười hai phần mười tám, tức hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Điều kiện chỉ loại đúng hai tam giác đều, còn tam giác vuông thì giữ nguyên.'),
    Beat('outro', 'outro', outro_text(313)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    cond='C_6^3 - 2 = 18',
                    right='3 dot 4 = 12',
                    prob='P = 12/18 = 2/3')


def validate() -> bool:
    assert len(COND) == 18 and len(RIGHT) == 12
    assert F(len(RIGHT), len(COND)) == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS313(PolyMixin, ShortScene):
    N = 313

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.4, t0)
        self.cur = self.flash([(0, 1, 3), (0, 2, 4), (1, 2, 5)], CYAN, .2)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.wait_until(.25, t0)
        self.cur = self.flash([(0, 2, 4), (1, 3, 5)], CORAL, .12)
        self.wait_until(.6, t0)
        m = self.M('cond', 1.6)
        self.write_board(m)
        self.frame(m)

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.diam = VGroup(*[Line(self.pts[i], self.pts[i + 3], color=GOLD, stroke_width=5) for i in range(3)])
        self.play(Create(self.diam, lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.play(FadeOut(self.diam), run_time=self.rt(.03))
        self.cur = self.flash(RIGHT[:4], GREEN, .2)
        self.clear_board(.03)
        self.write_board(self.M('right', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
