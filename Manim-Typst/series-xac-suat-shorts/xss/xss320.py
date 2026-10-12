"""XSS320 · Tam giác trên lưới 3 × 3 — C(9;3) − 8 = 76 tam giác; vuông: 36 góc vuông theo lưới + 8 góc vuông nghiêng 45° = 44 → 11/19."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import Dot, FadeIn, FadeOut, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, WHITE  # noqa: E402

EPISODE = {'code': 'XSS320', 'answer': '11/19'}
PROBLEM = ['Chọn $3$ trong $9$ điểm lưới $3 times 3$.',
           'Biết ba điểm tạo thành tam giác. Xác',
           'suất đó là tam giác vuông?']
OPTIONS = ['1/2', '11/19', '9/19']
CORRECT = 1
ANSWER_VALUE = 11 / 19
PTS = [(x, y) for x in range(3) for y in range(3)]


def area2(t):
    (a, b), (c, d), (e, f) = t
    return (c - a) * (f - b) - (d - b) * (e - a)


def right_at(t):
    for i in range(3):
        p, q, r = t[i], t[(i + 1) % 3], t[(i + 2) % 3]
        if (q[0] - p[0]) * (r[0] - p[0]) + (q[1] - p[1]) * (r[1] - p[1]) == 0:
            return p, q[0] == p[0] or q[1] == p[1]
    return None


TRI = [t for t in combinations(PTS, 3) if area2(t)]
RIGHT = [t for t in TRI if right_at(t)]
TILT = [t for t in RIGHT if not right_at(t)[1]]

BEATS = [
    Beat('hook', 'hook', 'Lưới ba nhân ba có chín điểm. Chọn ngẫu nhiên ba điểm, biết chúng tạo thành một tam giác thật sự. '
                         'Xác suất đó là tam giác vuông bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, mười một phần mười chín, hay chín phần mười chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có tám mươi tư bộ ba điểm. Tám bộ thẳng hàng: ba hàng, ba cột và hai đường chéo. Điều kiện còn bảy mươi sáu tam giác.'),
    Beat('s2', 'solve', 'Góc vuông có cạnh dọc theo lưới: tại mỗi điểm chọn một điểm cùng hàng và một điểm cùng cột, có bốn cách. Chín điểm cho ba mươi sáu tam giác.'),
    Beat('s3', 'solve', 'Còn góc vuông nghiêng bốn mươi lăm độ: bốn tam giác có đỉnh vuông ở tâm theo hai đường chéo, và bốn tam giác đỉnh vuông ở trung điểm cạnh. Thêm tám.'),
    Beat('s4', 'solve', 'Tổng bốn mươi bốn tam giác vuông trên bảy mươi sáu, rút gọn được mười một phần mười chín.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần mười chín. Đừng quên những góc vuông nằm nghiêng!'),
    Beat('outro', 'outro', outro_text(320)),
]

FORMULAS = formulas('11/19', OPTIONS,
                    cond='C_9^3 - 8 = 76',
                    axis='9 dot 4 = 36',
                    tilt='36 + 8 = 44',
                    prob='P = 44/76 = 11/19')


def validate() -> bool:
    assert len(TRI) == 76 and len(RIGHT) == 44 and len(TILT) == 8
    assert F(len(RIGHT), len(TRI)) == F(11, 19)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS320(ShortScene):
    N = 320

    def P(self, p):
        return [-1.8 + 1.8 * p[0], -.6 + 1.6 * p[1], 0]

    def tri(self, t, color):
        return Polygon(*[self.P(p) for p in t], stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=.35)

    def show(self, ts, color, total):
        step = total / len(ts)
        for t in ts:
            new = self.tri(t, color)
            self.play(*([FadeOut(self.cur)] if self.cur else []), FadeIn(new), run_time=self.rt(step))
            self.cur = new

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.cur = None
        self.dots = VGroup(*[Dot(self.P(p), radius=.11, color=WHITE) for p in PTS])
        self.play(FadeIn(self.dots, lag_ratio=.05), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.show([((0, 0), (2, 1), (1, 2)), ((0, 0), (2, 0), (0, 2))], CYAN, .15)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.show([((0, 0), (1, 1), (2, 2)), ((0, 1), (1, 1), (2, 1))], CORAL, .12)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.3, t0)
        self.show([((0, 0), (2, 0), (0, 1)), ((1, 0), (2, 0), (1, 2)), ((1, 1), (0, 1), (1, 2))], GOLD, .3)
        self.write_board(self.M('axis', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.show(TILT[:4], GREEN, .4)
        self.write_board(self.M('tilt', 1.5))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
