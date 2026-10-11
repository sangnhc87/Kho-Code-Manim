"""XSS140 · Con kiến trên tam giác — p_(n+1) = (1 − p_n)/2: 1, 0, 1/2, 1/4, 3/8, 5/16 (→ 1/3)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS140', 'answer': '5/16'}
PROBLEM = ['Kiến ở một đỉnh tam giác, mỗi bước',
           'sang một trong hai đỉnh còn lại. Xác',
           'suất sau $5$ bước về chỗ cũ?']
OPTIONS = ['1/4', '5/16', '1/3']
CORRECT = 1
ANSWER_VALUE = 5 / 16


def seq(n=5):
    p = [F(1)]
    for _ in range(n):
        p.append((1 - p[-1]) / 2)
    return p


BEATS = [
    Beat('hook', 'hook', 'Một chú kiến đứng ở đỉnh A của tam giác. Mỗi bước, nó bò sang một trong hai đỉnh còn lại, ngẫu nhiên. '
                         'Sau năm bước, xác suất kiến quay về đúng đỉnh A là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, năm phần mười sáu, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây năm tầng có ba mươi hai nhánh, quá nhiều. Quy hoạch động: gọi p n là xác suất ở A sau n bước. '
                        'Muốn ở A ở bước sau thì bước này phải không ở A, rồi chọn đúng A với xác suất một phần hai.'),
    Beat('s2', 'solve', 'Vậy p n cộng một bằng một trừ p n, chia hai. Bắt đầu p không bằng một: '
                        'p một bằng không, p hai một phần hai, p ba một phần tư, p bốn ba phần tám, p năm năm phần mười sáu.'),
    Beat('s3', 'solve', 'Dãy dao động quanh một phần ba và tiến dần về một phần ba: đi lâu thì kiến quên mất nó xuất phát ở đâu.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười sáu. Một công thức truy hồi thay cho cả cây ba mươi hai nhánh!'),
    Beat('outro', 'outro', outro_text(140)),
]

FORMULAS = formulas('5/16', OPTIONS,
                    rec='p_(n+1) = (1 - p_n)/2',
                    vals='1, quad 0, quad 1/2, quad 1/4, quad 3/8, quad 5/16',
                    lim='p_n arrow.r 1/3')


def validate() -> bool:
    from itertools import product
    paths = [w for w in product((1, 2), repeat=5)]
    back = sum(sum(w) % 3 == 0 for w in paths)
    assert seq()[5] == F(5, 16) == F(back, 32)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS140(ShortScene):
    N = 140

    def hook_visual(self, t0):
        self.board_top = -1.2
        pts = [[0, 2.7, 0], [-2.2, -.2, 0], [2.2, -.2, 0]]
        self.tri = Polygon(*pts, stroke_color=SOFT, stroke_width=4)
        self.ant = Dot(pts[0], radius=.2, color=CORAL)
        self.labs = VGroup(*[self.TM(f'${c}$', 30, SOFT).next_to(p, d, buff=.15)
                             for c, p, d in zip('ABC', pts, ([0, 1, 0], [-1, 0, 0], [1, 0, 0]))])
        self.pts = pts
        self.wait_until(.45, t0)
        self.play(FadeIn(self.tri), FadeIn(self.labs), FadeIn(self.ant, scale=2), run_time=self.rt(.1))
        for k in (1, 2, 0):
            self.play(self.ant.animate.move_to(pts[k]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        m = self.M('rec', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('vals', 1.9))

    def beat_s3(self, T):
        self.write_board(self.M('lim', 2.0), anim='fade')
