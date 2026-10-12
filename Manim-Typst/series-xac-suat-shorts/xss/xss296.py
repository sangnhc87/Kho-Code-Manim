"""XSS296 · Chưa từng sang bờ âm — 6 đường 4 bước về gốc; không âm: Catalan 2 → 2/6 = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import Create, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS296', 'answer': '1/3'}
PROBLEM = ['Ếch nhảy $plus.minus 1$ ($1/2$) trong $4$',
           'bước. Biết cuối cùng ếch về gốc. Xác',
           'suất ếch chưa lần nào ở vị trí âm?']
OPTIONS = ['1/2', '1/3', '1/6']
CORRECT = 1
ANSWER_VALUE = 1 / 3
ZERO = [w for w in product((1, -1), repeat=4) if sum(w) == 0]

BEATS = [
    Beat('hook', 'hook', 'Ếch nhảy ngẫu nhiên bốn bước, mỗi bước cộng hoặc trừ một. Biết cuối cùng ếch về đúng gốc. '
                         'Xác suất trong suốt quá trình, ếch chưa lần nào sang phía âm là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện về gốc: hai bước lên hai bước xuống, tổ hợp chập hai của bốn, sáu đường đồng khả năng. Vẽ cả sáu đường như những ngọn núi.'),
    Beat('s2', 'solve', 'Giữ lại đường không bao giờ xuống dưới trục: lên lên xuống xuống, và lên xuống lên xuống. Chỉ hai đường.'),
    Beat('s3', 'solve', 'Xác suất hai phần sáu, tức một phần ba. Số đường không xuống dưới trục là số Catalan, với n bằng hai là hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Điều kiện kiểu "mọi lúc" trên đường đi: đếm bằng số Catalan!'),
    Beat('outro', 'outro', outro_text(296)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    prob='P = 2/(C_4^2) = 2/6 = 1/3')


def validate() -> bool:
    good = [w for w in ZERO if all(sum(w[:k]) >= 0 for k in range(5))]
    assert len(ZERO) == 6 and F(len(good), 6) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS296(ShortScene):
    N = 296

    def P(self, i, t, h):
        col, row = i % 3, i // 3
        return [-2.4 + 2.4 * col + .4 * t - .8, 2.2 - 1.6 * row + .35 * h, 0]

    def path(self, i, w, color):
        pts, h = [self.P(i, 0, 0)], 0
        for t, s in enumerate(w, 1):
            h += s
            pts.append(self.P(i, t, h))
        m = VMobject(stroke_color=color, stroke_width=5)
        m.set_points_as_corners(pts)
        return m

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.axes = VGroup(*[Line(self.P(i, 0, 0), self.P(i, 4, 0), color=STROKE, stroke_width=2) for i in range(6)])
        self.wait_until(.6, t0)
        self.play(Create(self.axes), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.walks = VGroup(*[self.path(i, w, SOFT) for i, w in enumerate(ZERO)])
        self.play(Create(self.walks, lag_ratio=.15), run_time=self.rt(.25))

    def beat_s2(self, T):
        good = [p for p, w in zip(self.walks, ZERO) if all(sum(w[:k]) >= 0 for k in range(5))]
        bad = [p for p, w in zip(self.walks, ZERO) if not all(sum(w[:k]) >= 0 for k in range(5))]
        self.play(*[p.animate.set_stroke(GREEN, 6) for p in good], *[p.animate.set_stroke(CORAL, 3, opacity=.4) for p in bad],
                  run_time=self.rt(.08))

    def beat_s3(self, T):
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m, GOLD)
