"""XSS288 · Kiến đi qua hai điểm — tới (1;1) sau 2 bước: 2/4; từ (1;1) tới (3;3) sau 4 bước: C(4,2)/16: 1/2·3/8 = 3/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import Dot, FadeIn, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS288', 'answer': '3/16'}
PROBLEM = ['Kiến xuất phát từ $(0; 0)$, mỗi bước sang',
           'phải hoặc lên trên ($1/2$). Xác suất kiến',
           'đi qua cả $(1; 1)$ và $(3; 3)$?']
OPTIONS = ['1/4', '3/16', '3/8']
CORRECT = 1
ANSWER_VALUE = 3 / 16


def at(w, k):
    return w[:k].count('R'), w[:k].count('U')


BEATS = [
    Beat('hook', 'hook', 'Chú kiến bò trên lưới từ gốc tọa độ, mỗi bước sang phải hoặc lên trên, năm mươi năm mươi. '
                         'Xác suất kiến đi qua cả điểm một một và điểm ba ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, ba phần mười sáu, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điểm một một chỉ có thể tới ở bước thứ hai, điểm ba ba ở bước thứ sáu, vì mỗi bước tăng tổng tọa độ thêm một.'),
    Beat('s2', 'solve', 'Tới một một: hai đường trong bốn, một phần hai. Biết đang ở một một, tới ba ba sau bốn bước nữa: cần đúng hai phải hai lên, '
                        'tổ hợp chập hai của bốn trên mười sáu, ba phần tám.'),
    Beat('s3', 'solve', 'Công thức nhân: một phần hai nhân ba phần tám, bằng ba phần mười sáu. Tính không nhớ giúp tách bài thành hai đoạn độc lập.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười sáu. Đi qua nhiều điểm: nhân xác suất từng chặng!'),
    Beat('outro', 'outro', outro_text(288)),
]

FORMULAS = formulas('3/16', OPTIONS,
                    seg='P(arrow.r (1;1)) = 2/4, quad P((1;1) arrow.r (3;3)) = (C_4^2)/2^4 = 3/8',
                    prob='P = 1/2 dot 3/8 = 3/16')


def validate() -> bool:
    ws = list(product('RU', repeat=6))
    assert F(sum(at(w, 2) == (1, 1) and at(w, 6) == (3, 3) for w in ws), 64) == F(3, 16) == F(1, 2) * F(comb(4, 2), 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS288(ShortScene):
    N = 288

    def P(self, x, y):
        return [-1.8 + 1.0 * x, -.1 + .9 * y, 0]

    def hook_visual(self, t0):
        self.board_top = -1.3
        grid = VGroup(*[Line(self.P(0, j), self.P(4, j), color=STROKE, stroke_width=2) for j in range(4)],
                      *[Line(self.P(i, 0), self.P(i, 3), color=STROKE, stroke_width=2) for i in range(5)])
        marks = VGroup(Dot(self.P(1, 1), radius=.13, color=GOLD), Dot(self.P(3, 3), radius=.13, color=GOLD),
                       Dot(self.P(0, 0), radius=.13, color=WHITE))
        self.grid = VGroup(grid, marks)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.grid), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        path = VMobject(stroke_color=CYAN, stroke_width=6)
        path.set_points_as_corners([self.P(0, 0), self.P(1, 0), self.P(1, 1), self.P(1, 2), self.P(2, 2), self.P(3, 2), self.P(3, 3)])
        self.play(FadeIn(path), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('seg', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m, CORAL)
