"""XSS187 · Tam giác tù trong 12-giác — tù ⇔ 3 đỉnh nằm trong một nửa mở; đếm theo đỉnh góc tù: 12·10 = 120 / 220 = 6/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import Circle, Dot, FadeIn, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT, WHITE  # noqa: E402
from common.visuals import polygon_pts  # noqa: E402

EPISODE = {'code': 'XSS187', 'answer': '6/11'}
PROBLEM = ['Chọn ngẫu nhiên $3$ đỉnh của đa giác đều',
           '$12$ cạnh. Xác suất được một tam giác tù?']
OPTIONS = ['1/2', '6/11', '3/11']
CORRECT = 1
ANSWER_VALUE = 6 / 11


def kind(t, n=12):
    a, b, c = t
    big = max(b - a, c - b, n - c + a)
    return 'vuông' if 2 * big == n else ('tù' if 2 * big > n else 'nhọn')


BEATS = [
    Beat('hook', 'hook', 'Đa giác đều mười hai cạnh nội tiếp đường tròn. Chọn ngẫu nhiên ba đỉnh. '
                         'Xác suất được một tam giác tù là bao nhiêu? Đây là dạng chặn điểm rất hay gặp.'),
    Beat('guess', 'hook', 'Một phần hai, sáu phần mười một, hay ba phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tam giác nội tiếp có góc tù khi và chỉ khi ba đỉnh nằm gọn trên một cung nhỏ hơn nửa đường tròn. '
                        'Đỉnh góc tù là đỉnh nằm giữa cung đó.'),
    Beat('s2', 'solve', 'Đếm theo đỉnh góc tù A. Hai đỉnh còn lại nằm hai bên A, cung giữa chúng chứa A và nhỏ hơn sáu khoảng. '
                        'Với mỗi A có mười cách chọn, mười hai đỉnh cho một trăm hai mươi tam giác tù.'),
    Beat('s3', 'solve', 'Không gian mẫu có tổ hợp chập ba của mười hai, hai trăm hai mươi. Xác suất một trăm hai mươi phần hai trăm hai mươi, '
                        'tức sáu phần mười một. Kiểm tra: tam giác vuông sáu mươi, nhọn bốn mươi.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười một. Hơn một nửa số tam giác nội tiếp là tam giác tù!'),
    Beat('outro', 'outro', outro_text(187)),
]

FORMULAS = formulas('6/11', OPTIONS,
                    cnt='n("tù") = 12 dot 10 = 120',
                    prob='P = 120/(C_12^3) = 120/220 = 6/11',
                    check='120 + 60 + 40 = 220')


def validate() -> bool:
    ks = [kind(t) for t in combinations(range(12), 3)]
    assert (ks.count('tù'), ks.count('vuông'), ks.count('nhọn')) == (120, 60, 40)
    assert F(120, comb(12, 3)) == F(6, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS187(ShortScene):
    N = 187

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.pts = polygon_pts(12, 2.0, (0, 1.3))
        self.shape = VGroup(Circle(radius=2.0, stroke_color=SOFT, stroke_width=2).move_to([0, 1.3, 0]),
                            Polygon(*self.pts, stroke_color=CYAN, stroke_width=3),
                            *[Dot(p, radius=.09, color=WHITE) for p in self.pts])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.shape), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        tri = Polygon(self.pts[11], self.pts[1], self.pts[3], stroke_color=CORAL, stroke_width=5, fill_color=CORAL,
                      fill_opacity=.25)
        self.wait_until(.35, t0)
        self.play(FadeIn(tri), run_time=self.rt(.08))
        self.play(FadeIn(Dot(self.pts[1], radius=.17, color=GOLD), scale=2), run_time=self.rt(.04))
        self.tri = tri

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('cnt', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.M('check', 1.6), anim='fade')


