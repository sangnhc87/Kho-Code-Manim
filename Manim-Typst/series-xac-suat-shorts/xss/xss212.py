"""XSS212 · Đỏ luôn không ít hơn — dãy 3Đ3X với mọi tiền tố Đ ≥ X: số Catalan 5 / C(6,3) = 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path

from manim import Create, Dot, FadeIn, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS212', 'answer': '1/4'}
PROBLEM = ['Hộp $3$ đỏ $3$ xanh, rút lần lượt đến',
           'hết. Xác suất mọi lúc số bi đỏ đã',
           'rút $>=$ số bi xanh đã rút?']
OPTIONS = ['1/2', '1/4', '1/5']
CORRECT = 1
ANSWER_VALUE = .25
GOOD = sorted(''.join(s) for s in set(permutations('RRRBBB'))
              if all(s[:k].count('R') >= s[:k].count('B') for k in range(7)))

BEATS = [
    Beat('hook', 'hook', 'Hộp ba đỏ ba xanh, rút lần lượt đến hết. Xác suất trong suốt quá trình, số bi đỏ đã rút luôn không ít hơn số bi xanh '
                         'là bao nhiêu? Bài toán này nổi tiếng trong tổ hợp.'),
    Beat('guess', 'hook', 'Một phần hai, một phần tư, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ đường đi: bi đỏ đi lên, bi xanh đi xuống. Điều kiện là đường đi không bao giờ xuống dưới mức không. '
                        'Có hai mươi đường đồng khả năng.'),
    Beat('s2', 'solve', 'Đếm được năm đường không chạm xuống dưới: đỏ đỏ đỏ xanh xanh xanh, đỏ đỏ xanh đỏ xanh xanh, và ba đường khác. '
                        'Năm chính là số Catalan.'),
    Beat('s3', 'solve', 'Xác suất năm phần hai mươi, tức một phần tư. Công thức tổng quát: một phần n cộng một, với n bằng ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Điều kiện "mọi lúc" trên dãy rút bi chính là bài toán đường đi không xuống dưới trục!'),
    Beat('outro', 'outro', outro_text(212)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    omega='n(Omega) = C_6^3 = 20',
                    cat='n(A) = 1/4 C_6^3 = 5',
                    prob='P = 5/20 = 1/(3 + 1) = 1/4')


def validate() -> bool:
    assert len(GOOD) == 5 and F(5, comb(6, 3)) == F(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS212(ShortScene):
    N = 212

    def P(self, t, h):
        return [-3.0 + 1.0 * t, .5 + .55 * h, 0]

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.axis = VGroup(Line(self.P(0, 0), self.P(6, 0), color=SOFT, stroke_width=3),
                           *[Line(self.P(0, h), self.P(6, h), color=STROKE, stroke_width=1) for h in (-3, -2, -1, 1, 2, 3)])
        self.wait_until(.6, t0)
        self.play(Create(self.axis), run_time=self.rt(.08))

    def path(self, s, color):
        pts, h = [self.P(0, 0)], 0
        for t, c in enumerate(s, 1):
            h += 1 if c == 'R' else -1
            pts.append(self.P(t, h))
        m = VMobject(stroke_color=color, stroke_width=5)
        m.set_points_as_corners(pts)
        return m

    def beat_s1(self, T):
        t0 = self.now()
        bad = self.path('RBBRRB', CORAL)
        self.play(Create(bad), run_time=self.rt(.15))
        self.play(FadeIn(Dot(self.P(3, -1), radius=.12, color=CORAL)), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.play(bad.animate.set_opacity(.15), run_time=self.rt(.04))
        self.write_board(self.M('omega', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        for i, s in enumerate(GOOD):
            self.wait_until(.1 + .15 * i, t0)
            self.play(Create(self.path(s, [GREEN, GOLD, '#7AA2FF', '#B78CFF', '#FF6B6B'][i]).shift([0, .02 * i, 0])),
                      run_time=self.rt(.05))
        self.write_board(self.M('cat', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
