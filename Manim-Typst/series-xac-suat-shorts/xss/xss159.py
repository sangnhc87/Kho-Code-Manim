"""XSS159 · Biết có bi đỏ — hộp 3 đỏ 2 xanh, rút 2: 9 cặp có đỏ, 3 cặp hai đỏ: 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import ball, urn  # noqa: E402

EPISODE = {'code': 'XSS159', 'answer': '1/3'}
PROBLEM = ['Hộp $3$ đỏ $2$ xanh, rút ngẫu nhiên',
           '$2$ bi, biết có ít nhất $1$ bi đỏ.',
           'Xác suất cả hai bi đều đỏ?']
OPTIONS = ['3/10', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
BALLS = 'RRRBB'
PAIRS = list(combinations(range(5), 2))

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ và hai bi xanh. Rút ngẫu nhiên hai bi, bạn được biết có ít nhất một bi đỏ. '
                         'Xác suất cả hai bi đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần mười, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có mười cặp bi đồng khả năng. Điều kiện "có ít nhất một đỏ" chỉ loại cặp hai bi xanh, còn chín cặp.'),
    Beat('s2', 'solve', 'Trong chín cặp đó, cặp hai bi đỏ có tổ hợp chập hai của ba, bằng ba cặp.'),
    Beat('s3', 'solve', 'Xác suất bằng ba phần chín, tức một phần ba. Ba phần mười là xác suất khi chưa có điều kiện.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Điều kiện loại cặp nào thì mẫu số giảm tương ứng!'),
    Beat('outro', 'outro', outro_text(159)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    nb='n(B) = C_5^2 - C_2^2 = 9',
                    nab='n(A sect B) = C_3^2 = 3',
                    prob='P(A | B) = 3/9 = 1/3')


def validate() -> bool:
    b = [p for p in PAIRS if 'R' in (BALLS[p[0]], BALLS[p[1]])]
    assert F(sum(BALLS[p[0]] == BALLS[p[1]] == 'R' for p in b), len(b)) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS159(ShortScene):
    N = 159

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.u = urn(BALLS, cols=5, r=.32).move_to([0, 2.2, 0])
        self.pairs = VGroup(*[VGroup(ball(BALLS[a], .2), ball(BALLS[b], .2)).arrange(buff=.06) for a, b in PAIRS]) \
            .arrange_in_grid(2, 5, buff=(.45, .3)).move_to([0, .45, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.pairs, lag_ratio=.08), run_time=self.rt(.2))
        self.wait_until(.55, t0)
        bb = [p for p, (a, b) in zip(self.pairs, PAIRS) if BALLS[a] == BALLS[b] == 'B']
        self.play(*[p.animate.set_opacity(.15) for p in bb], run_time=self.rt(.05))
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        rr = [p for p, (a, b) in zip(self.pairs, PAIRS) if BALLS[a] == BALLS[b] == 'R']
        self.play(*[p.animate.scale(1.3) for p in rr], run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.write_board(self.M('nab', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)
