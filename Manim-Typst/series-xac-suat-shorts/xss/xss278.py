"""XSS278 · Bốn bạn chuyền bóng — p_(n+1) = (1 − p_n)/3: 1, 0, 1/3, 2/9, 7/27."""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS278', 'answer': '7/27'}
PROBLEM = ['$4$ bạn chuyền bóng, mỗi lần ngẫu nhiên',
           'cho $1$ trong $3$ bạn kia. A cầm bóng đầu.',
           'Xác suất sau $4$ lần bóng về lại A?']
OPTIONS = ['1/4', '7/27', '2/9']
CORRECT = 1
ANSWER_VALUE = 7 / 27


def seq(n=4):
    p = [F(1)]
    for _ in range(n):
        p.append((1 - p[-1]) / 3)
    return p


BEATS = [
    Beat('hook', 'hook', 'Bốn bạn A, B, C, D chuyền bóng. Mỗi lần, người cầm bóng chuyền ngẫu nhiên cho một trong ba bạn còn lại. '
                         'A cầm bóng đầu tiên. Sau bốn lần chuyền, xác suất bóng quay về tay A là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, bảy phần hai mươi bảy, hay hai phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây đầy đủ có tám mươi mốt nhánh. Thay vào đó, gọi p n là xác suất A cầm bóng sau n lần. '
                        'Bóng về A ở lần sau khi và chỉ khi lần này A không cầm, rồi người cầm chọn đúng A, một phần ba.'),
    Beat('s2', 'solve', 'Vậy p n cộng một bằng một trừ p n chia ba. Bắt đầu p không bằng một: p một bằng không, p hai một phần ba, p ba hai phần chín.'),
    Beat('s3', 'solve', 'p bốn bằng một trừ hai phần chín chia ba, bằng bảy phần hai mươi bảy. Dãy tiến dần về một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần hai mươi bảy. Một trạng thái "có bóng hay không" là đủ để viết công thức truy hồi!'),
    Beat('outro', 'outro', outro_text(278)),
]

FORMULAS = formulas('7/27', OPTIONS,
                    rec='p_(n+1) = (1 - p_n)/3',
                    vals='1, quad 0, quad 1/3, quad 2/9, quad 7/27 arrow.r 1/4')


def validate() -> bool:
    brute = F(sum(1 for w in product(range(3), repeat=4) if _ends_at_a(w)), 81)
    assert seq()[4] == brute == F(7, 27)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


def _ends_at_a(choices):
    cur = 0
    for c in choices:
        others = [x for x in range(4) if x != cur]
        cur = others[c]
    return cur == 0


class XSS278(ShortScene):
    N = 278

    def hook_visual(self, t0):
        self.board_top = -1.25
        pos = [[1.6 * math.cos(math.pi / 2 + k * math.pi / 2), 1.05 + 1.4 * math.sin(math.pi / 2 + k * math.pi / 2), 0] for k in range(4)]
        self.kids = VGroup(*[token(n, CORAL if n == "A" else CYAN, .4).move_to(p) for n, p in zip('ABCD', pos)])
        self.links = VGroup(*[Line(pos[i], pos[j], color=STROKE, stroke_width=2) for i in range(4) for j in range(i + 1, 4)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.links), FadeIn(self.kids, lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        m = self.M('rec', 2.2)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        self.clear_board(.03)
        self.write_board(self.M('vals', 1.7))

    def beat_s3(self, T):
        self.play(self.kids[0].animate.scale(1.3), run_time=self.rt(.05))
