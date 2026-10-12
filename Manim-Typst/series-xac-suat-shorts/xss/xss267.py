"""XSS267 · Con bạc có lợi thế — p = 2/3, r = q/p = 1/2: P(từ 2 đạt 4) = (1 − r²)/(1 − r⁴) = 4/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402


EPISODE = {'code': 'XSS267', 'answer': '4/5'}
PROBLEM = ['Có $2$ đồng, mỗi ván thắng $2/3$ (thêm $1$',
           'đồng) hoặc thua (mất $1$ đồng). Dừng khi',
           'có $4$ đồng hoặc hết tiền. $P("đạt 4")$?']
OPTIONS = ['2/3', '4/5', '1/2']
CORRECT = 1
ANSWER_VALUE = .8


def solve():
    # x_k = p x_(k+1) + q x_(k-1), x_0 = 0, x_4 = 1 — iterate to the exact fixed point
    p, q = F(2, 3), F(1, 3)
    # closed form for 0..4
    r = q / p
    return [(1 - r ** k) / (1 - r ** 4) for k in range(5)]


BEATS = [
    Beat('hook', 'hook', 'Một con bạc có hai đồng, chơi những ván mà mình thắng với xác suất hai phần ba. Thắng được thêm một đồng, thua mất một đồng. '
                         'Dừng khi đạt bốn đồng hoặc hết tiền. Xác suất đạt bốn đồng là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần ba, bốn phần năm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi x k là xác suất đạt bốn đồng khi đang có k đồng. Xét ván tiếp theo: x k bằng hai phần ba x k cộng một, cộng một phần ba x k trừ một. '
                        'Với x không bằng không, x bốn bằng một.'),
    Beat('s2', 'solve', 'Giải hệ ba ẩn, hoặc dùng công thức con bạc phá sản với tỉ số r bằng q chia p, một phần hai: '
                        'x k bằng một trừ r mũ k, chia một trừ r mũ bốn.'),
    Beat('s3', 'solve', 'x hai bằng một trừ một phần tư, chia một trừ một phần mười sáu, bằng bốn phần năm. Lợi thế nhỏ mỗi ván thành lợi thế lớn chung cuộc.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần năm. Cây có vòng lặp: đặt ẩn cho mỗi trạng thái và lập hệ phương trình!'),
    Beat('outro', 'outro', outro_text(267)),
]

FORMULAS = formulas('4/5', OPTIONS,
                    rec='x_k = 2/3 x_(k+1) + 1/3 x_(k-1), quad x_0 = 0, quad x_4 = 1',
                    sol='x_2 = (1 - (1/2)^2)/(1 - (1/2)^4) = 4/5')


def validate() -> bool:
    x = solve()
    p, q = F(2, 3), F(1, 3)
    assert x[0] == 0 and x[4] == 1 and all(x[k] == p * x[k + 1] + q * x[k - 1] for k in (1, 2, 3))
    assert x[2] == F(4, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS267(ShortScene):
    N = 267

    def hook_visual(self, t0):
        self.board_top = -1.25
        xs = [-2.8 + 1.4 * k for k in range(5)]
        self.axis = Line([xs[0], 1.4, 0], [xs[-1], 1.4, 0], color=SOFT, stroke_width=4)
        self.marks = VGroup(*[VGroup(Dot([x, 1.4, 0], radius=.1, color=SOFT),
                                     self.TM(f'${k}$', 26, CORAL if k == 0 else (GREEN if k == 4 else SOFT)).next_to([x, 1.4, 0], [0, -1, 0], buff=.2))
                              for k, x in enumerate(xs)])
        self.chip = Dot([xs[2], 1.4, 0], radius=.22, color=GOLD)
        self.xs = xs
        self.wait_until(.7, t0)
        self.play(FadeIn(self.axis), FadeIn(self.marks), FadeIn(self.chip, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        for k in (3, 2, 3):
            self.play(self.chip.animate.move_to([self.xs[k], 1.4, 0]), run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.M('rec', 1.5))

    def beat_s2(self, T):
        self.play(self.chip.animate.move_to([self.xs[4], 1.4, 0]).set_color(GREEN), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 1.8)
        self.write_board(m)
        self.frame(m)


