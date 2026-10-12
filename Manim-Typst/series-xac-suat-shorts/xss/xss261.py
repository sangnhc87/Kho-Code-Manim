"""XSS261 · p nào tốt nhất? — f(p) = 3p²(1 − p), f'(p) = 6p − 9p² = 0 ⇒ p = 2/3, f = 4/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Create, DashedLine, Dot, FadeIn, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS261', 'answer': 'p = 2/3'}
PROBLEM = ['Đồng xu lệch ra ngửa với xác suất',
           '$p$, tung $3$ lần. $p$ bằng bao nhiêu thì',
           '$P("đúng 2 ngửa")$ lớn nhất?']
OPTIONS = ['p = 1/2', 'p = 2/3', 'p = 3/4']
CORRECT = 1
ANSWER_VALUE = None


def f(p):
    return 3 * p * p * (1 - p)


BEATS = [
    Beat('hook', 'hook', 'Bạn được chọn độ lệch của đồng xu, xác suất ra ngửa là p, rồi tung ba lần. '
                         'Chọn p bằng bao nhiêu để xác suất được đúng hai lần ngửa là lớn nhất?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bernoulli: xác suất đúng hai ngửa là tổ hợp chập hai của ba, nhân p bình phương nhân một trừ p, tức ba p bình phương trừ ba p mũ ba.'),
    Beat('s2', 'solve', 'Đây là bài toán cực trị lớp mười hai: đạo hàm sáu p trừ chín p bình phương bằng không, cho p bằng hai phần ba.'),
    Beat('s3', 'solve', 'Giá trị lớn nhất bằng bốn phần chín. Trực giác đẹp: muốn hai trên ba lần ngửa thì chọn p bằng đúng hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: p bằng hai phần ba. Xác suất gặp đạo hàm: tối ưu tham số để sự kiện dễ xảy ra nhất!'),
    Beat('outro', 'outro', outro_text(261)),
]

FORMULAS = formulas('p = 2/3', OPTIONS,
                    fp='f(p) = C_3^2 p^2 (1 - p) = 3 p^2 - 3 p^3',
                    der="f'(p) = 6 p - 9 p^2 = 0 arrow.r.double p = 2/3",
                    mx='f(2/3) = 4/9')


def validate() -> bool:
    best = max((F(k, 300) for k in range(301)), key=f)
    assert best == F(2, 3) and f(best) == F(4, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS261(ShortScene):
    N = 261

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.x0, self.x1, self.y0, self.y1 = -3.0, 3.0, -.2, 2.6
        pts = [self.P(F(k, 100)) for k in range(101)]
        self.curve = VMobject(stroke_color=CYAN, stroke_width=5)
        self.curve.set_points_smoothly(pts)
        self.lab = self.TM('$p$', 24, SOFT).move_to([self.x1 + .2, self.y0, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.lab), run_time=self.rt(.03))

    def P(self, p):
        return [self.x0 + (self.x1 - self.x0) * float(p), self.y0 + (self.y1 - self.y0) * float(f(p)) / .5, 0]

    def beat_s1(self, T):
        t0 = self.now()
        self.play(Create(self.curve), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('fp', 1.8))

    def beat_s2(self, T):
        t0 = self.now()
        top = self.P(F(2, 3))
        self.play(FadeIn(Dot(top, radius=.12, color=GOLD)), FadeIn(DashedLine(top, [top[0], self.y0, 0], color=GOLD)),
                  run_time=self.rt(.06))
        self.wait_until(.3, t0)
        self.clear_board(.03)
        self.write_board(self.M('der', 1.8))

    def beat_s3(self, T):
        m = self.M('mx', 2.2)
        self.write_board(m)
        self.frame(m)
