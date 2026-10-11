"""XSS119 · Bình của Pólya — mọi dãy có k đỏ đều có cùng xác suất k!(10 − k)!/11!, nhân C(10, k) được 1/11 với mọi k."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

from manim import DOWN, DashedLine, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS119', 'answer': '1/11 với mọi k'}
PROBLEM = ['Bình $1$ đỏ $1$ xanh. Rút $1$ bi, trả lại kèm',
           '$1$ bi cùng màu; làm $10$ lần. Xác suất',
           'có đúng $k$ bi đỏ được thêm vào?']
OPTIONS = ['C_10^k / 2^10', '1/11', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 11
N, SEED = 2000, 6


def counts():
    r, c = random.Random(SEED), [0] * 11
    for _ in range(N):
        red, blue = 1, 1
        for _ in range(10):
            if r.random() < red / (red + blue):
                red += 1
            else:
                blue += 1
        c[red - 1] += 1
    return c


def seq_prob(seq):
    red, blue, p = 1, 1, F(1)
    for s in seq:
        if s == 'R':
            p *= F(red, red + blue)
            red += 1
        else:
            p *= F(blue, red + blue)
            blue += 1
    return p


BEATS = [
    Beat('hook', 'hook', 'Bình có một bi đỏ và một bi xanh. Rút một bi, rồi trả lại kèm thêm một bi cùng màu. Làm mười lần. '
                         'Người giàu càng giàu: màu nào ra nhiều sẽ càng dễ ra. Xác suất có đúng k bi đỏ được thêm vào là bao nhiêu?'),
    Beat('guess', 'hook', 'Phân phối nhị thức, một phần mười một, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tính xác suất một dãy cụ thể, ví dụ đỏ đỏ xanh: một phần hai nhân hai phần ba nhân một phần tư, '
                        'bằng một phần mười hai. Đổi thứ tự thành đỏ xanh đỏ: một phần hai nhân một phần ba nhân hai phần tư, '
                        'vẫn một phần mười hai!'),
    Beat('s2', 'solve', 'Tử số luôn là k giai thừa nhân mười trừ k giai thừa, mẫu số luôn là mười một giai thừa, '
                        'không phụ thuộc thứ tự. Có tổ hợp chập k của mười dãy như vậy, nhân lại được đúng một phần mười một.'),
    Beat('s3', 'solve', 'Mô phỏng hai nghìn lần: mười một cột gần như bằng nhau, khác hẳn hình chuông của tung đồng xu.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười một với mọi k. Bình Pólya biến may rủi thành phân phối đều hoàn hảo, '
                            'một thử thách mở rộng rất đẹp!'),
    Beat('outro', 'outro', outro_text(119)),
]

FORMULAS = formulas('1/11', OPTIONS,
                    rrb='P("ĐĐX") = 1/2 dot 2/3 dot 1/4 = 1/12',
                    rbr='P("ĐXĐ") = 1/2 dot 1/3 dot 2/4 = 1/12',
                    gen='C_10^k dot (k! thin (10 - k)!)/(11!) = 1/11')


def validate() -> bool:
    assert seq_prob('RRB') == seq_prob('RBR') == F(1, 12)
    assert all(comb(10, k) * F(factorial(k) * factorial(10 - k), factorial(11)) == F(1, 11) for k in range(11))
    assert all(seq_prob('R' * k + 'B' * (10 - k)) == F(factorial(k) * factorial(10 - k), factorial(11)) for k in range(11))
    assert max(abs(c / N - 1 / 11) for c in counts()) < .01
    assert OPTIONS[CORRECT] == EPISODE['answer'].split()[0]
    return True


class XSS119(ShortScene):
    N = 119

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.u = urn('RB', cols=2, r=.42).move_to([0, 1.4, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        bigger = urn('RRRRBB', cols=3, r=.42).move_to([0, 1.4, 0])
        self.play(self.u.animate.become(bigger), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('rrb', 1.8))
        self.wait_until(.6, t0)
        self.write_board(self.M('rbr', 1.8))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('gen', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.u.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.u)
        c = counts()
        base, h = -.9, 3.3
        bars = VGroup()
        for k, n in enumerate(c):
            b = Rectangle(width=.48, height=h * n / max(c) * .8, stroke_width=0, fill_color=CYAN, fill_opacity=.85)
            b.move_to([-3.0 + k * .6, base + b.height / 2, 0])
            bars.add(b)
        axis = VGroup(*[self.TM(f'${k}$', 20, SOFT).next_to([-3.0 + k * .6, base, 0], DOWN, buff=.08)
                        for k in range(11)])
        level = base + h * (N / 11) / max(c) * .8
        ref = DashedLine([-3.4, level, 0], [3.4, level, 0], color=GOLD, stroke_width=3)
        binom = VGroup(*[Rectangle(width=.48, height=max(.02, h * .8 * 1.25 * comb(10, k) / 252),
                                   stroke_color=CORAL, stroke_width=2, fill_opacity=0) for k in range(11)])
        for k, b in enumerate(binom):
            b.move_to([-3.0 + k * .6, base + b.height / 2, 0])
        self.play(FadeIn(axis), *[GrowFromEdge(b, DOWN) for b in bars], run_time=self.rt(.25))
        self.play(FadeIn(ref), run_time=self.rt(.05))
        self.write_board(VGroup(tx('số bi đỏ thêm vào', 24, SOFT), self.TM('$1/11$', 26, GOLD)).arrange(buff=.4), anim='fade')
        self.wait_until(.7, t0)
        self.play(FadeIn(binom), run_time=self.rt(.06))


