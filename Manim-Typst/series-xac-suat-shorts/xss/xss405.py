"""XSS405 · Kiến trên tứ diện — p_n = (1 − p_(n−1))/3: 1, 0, 1/3, 2/9, 7/27, 20/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS405', 'answer': '20/81'}
PROBLEM = ['Kiến ở đỉnh A của tứ diện, mỗi bước sang',
           '$1$ trong $3$ đỉnh còn lại (như nhau). Xác',
           'suất sau $5$ bước kiến về A?']
OPTIONS = ['20/81', '1/4', '7/27']
CORRECT = 0
ANSWER_VALUE = 20 / 81


def seq(n):
    p = [F(1)]
    for _ in range(n):
        p.append((1 - p[-1]) / 3)
    return p


BEATS = [
    Beat('hook', 'hook', 'Một con kiến ở đỉnh A của hình tứ diện. Mỗi bước nó bò sang một trong ba đỉnh còn lại với khả năng như nhau. '
                         'Xác suất sau năm bước kiến quay về A?'),
    Beat('guess', 'hook', 'Hai mươi phần tám mươi mốt, một phần tư, hay bảy phần hai mươi bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi p n là xác suất ở A sau n bước. Muốn ở A thì bước trước phải ở đỉnh khác, rồi chọn đúng A với một phần ba.'),
    Beat('s2', 'solve', 'Vậy p n bằng một trừ p n trừ một, chia ba. Bắt đầu p không bằng một: p một bằng không, p hai một phần ba, p ba hai phần chín, p bốn bảy phần hai mươi bảy.'),
    Beat('s3', 'solve', 'p năm bằng một trừ bảy phần hai mươi bảy, chia ba, tức hai mươi phần tám mươi mốt. Dãy dao động quanh một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi phần tám mươi mốt. Gom ba đỉnh khác A thành một trạng thái, cây khổng lồ thu về một công thức truy hồi.'),
    Beat('outro', 'outro', outro_text(405)),
]

FORMULAS = formulas('20/81', OPTIONS,
                    rec='p_n = (1 - p_(n-1))/3, quad p_0 = 1',
                    vals='1, quad 0, quad 1/3, quad 2/9, quad 7/27, quad 20/81')


def validate() -> bool:
    assert seq(5) == [1, 0, F(1, 3), F(2, 9), F(7, 27), F(20, 81)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS405(ShortScene):
    N = 405

    def hook_visual(self, t0):
        self.board_top = -1.3
        pts = [[0, 2.3, 0], [-1.7, .1, 0], [1.7, .1, 0], [.4, .9, 0]]
        edges = VGroup(*[Line(pts[i], pts[j], color=STROKE, stroke_width=3) for i in range(4) for j in range(i + 1, 4)])
        dots = VGroup(*[Dot(p, radius=.14, color=GOLD if i == 0 else CYAN) for i, p in enumerate(pts)])
        lab = self.TM('$A$', 30, SOFT).next_to(pts[0], [1, 0, 0], buff=.2)
        self.tet = VGroup(edges, dots, lab)
        self.wait_until(.4, t0)
        self.play(FadeIn(self.tet), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.tet[1][1:].animate.set_color(SOFT), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('rec', 1.5))
        self.wait_until(.45, t0)
        self.write_board(self.M('vals', 1.3))

    def beat_s3(self, T):
        m = self.M('answer', 1.8)
        self.write_board(m, anim='fade')
        self.frame(m)
