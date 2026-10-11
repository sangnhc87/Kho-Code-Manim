"""XSS093 · Đi ngẫu nhiên — 4 bước ±1: về chỗ cũ khi có đúng 2 bước tiến: C(4,2)/2⁴ = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import Create, FadeIn, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS093', 'answer': '3/8'}
PROBLEM = ['Một con kiến đứng ở $0$, mỗi bước tiến',
           'hoặc lùi $1$ với xác suất $1/2$. Sau $4$',
           'bước, $P("về đúng chỗ cũ")$?']
OPTIONS = ['1/2', '3/8', '1/4']
CORRECT = 1
ANSWER_VALUE = 3 / 8
WALKS = list(product((1, -1), repeat=4))

BEATS = [
    Beat('hook', 'hook', 'Một con kiến say rượu đứng ở điểm không. Mỗi bước nó tiến hoặc lùi một đơn vị, khả năng như nhau. '
                         'Sau bốn bước, xác suất nó quay về đúng chỗ cũ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần tám, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn bước, mỗi bước hai lựa chọn: hai mũ bốn bằng mười sáu đường đi đồng khả năng. '
                        'Vẽ mỗi đường đi như một đường gấp khúc theo thời gian.'),
    Beat('s2', 'solve', 'Về lại số không khi số bước tiến bằng số bước lùi: đúng hai bước tiến trong bốn. '
                        'Chọn vị trí hai bước tiến: tổ hợp chập hai của bốn, bằng sáu đường đi.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần mười sáu, tức ba phần tám. Nghĩa là hơn sáu mươi phần trăm số lần, '
                        'kiến không về được chỗ cũ sau bốn bước.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Mô hình đi ngẫu nhiên này được dùng để mô tả cả giá cổ phiếu và chuyển động của phân tử!'),
    Beat('outro', 'outro', outro_text(93)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    n='n(Omega) = 2^4 = 16',
                    a='n(A) = C_4^2 = 6',
                    prob='P = 6/16 = 3/8')


def validate() -> bool:
    assert F(sum(sum(w) == 0 for w in WALKS), 16) == F(comb(4, 2), 16) == F(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS093(ShortScene):
    N = 93

    def lattice(self):
        x0, dx, y0, dy = -3.0, 1.45, 1.3, .52
        P = lambda t, h: [x0 + dx * t, y0 + dy * h, 0]  # noqa: E731
        grid = VGroup(*[Line(P(0, h), P(4, h), color=STROKE, stroke_width=1.5) for h in range(-4, 5)])
        zero = Line(P(0, 0), P(4, 0), color=SOFT, stroke_width=3)
        labs = VGroup(self.TM('$0$', 22, SOFT).next_to(P(0, 0), [-1, 0, 0], buff=.12),
                      tx('bước', 20, SOFT).next_to(P(4, -4), [0, -1, 0], buff=.1))
        paths = VGroup()
        for w in WALKS:
            pts, h = [P(0, 0)], 0
            for t, s in enumerate(w, 1):
                h += s
                pts.append(P(t, h))
            m = VMobject(stroke_color=GOLD if sum(w) == 0 else CYAN, stroke_width=4, stroke_opacity=.8)
            m.set_points_as_corners(pts)
            paths.add(m)
        return VGroup(grid, zero, labs), paths

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.frame_grid, self.paths = self.lattice()
        self.wait_until(.55, t0)
        self.play(FadeIn(self.frame_grid), run_time=self.rt(.08))
        self.play(Create(self.paths[5]), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[Create(p) for p in self.paths], run_time=self.rt(.35))
        self.wait_until(.5, t0)
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[p.animate.set_stroke(opacity=.15) for p, w in zip(self.paths, WALKS) if sum(w)],
                  *[p.animate.set_stroke(width=6) for p, w in zip(self.paths, WALKS) if not sum(w)], run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('a', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
