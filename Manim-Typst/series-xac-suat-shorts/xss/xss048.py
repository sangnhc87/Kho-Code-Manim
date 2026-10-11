"""XSS048 · Tung đến khi ngửa — cần đúng 3 lần: S, S, N = (1/2)³ = 1/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS048', 'answer': '1/8'}
PROBLEM = ['Tung đồng xu cho đến khi ra mặt ngửa thì dừng.', 'Xác suất phải tung đúng $3$ lần?']
OPTIONS = ['1/3', '1/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 8

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu cho đến khi ra mặt ngửa thì dừng lại. '
                         'Xác suất phải tung đúng ba lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Phải tung đúng ba lần nghĩa là hai lần đầu đều sấp, và lần thứ ba ra ngửa. '
                        'Chỉ có duy nhất một dãy như vậy: sấp, sấp, ngửa.'),
    Beat('s2', 'solve', 'Mỗi lần tung độc lập, xác suất một phần hai. Nhân ba lần: một phần hai mũ ba, bằng một phần tám.'),
    Beat('s3', 'solve', 'Tương tự, dừng ở lần một có xác suất một phần hai, lần hai một phần tư, lần ba một phần tám, '
                        'cứ thế giảm một nửa. Cộng tất cả lại vừa đúng bằng một.'),
    Beat('answer', 'solve', 'Đáp án: một phần tám. Mỗi lần tung thêm, xác suất lại giảm một nửa.'),
    Beat('outro', 'outro', outro_text(48)),
]

FORMULAS = formulas('1/8', OPTIONS,
                    seq='P(S S N) = 1/2 dot 1/2 dot 1/2 = 1/8',
                    sum='1/2 + 1/4 + 1/8 + dots = 1')


def validate() -> bool:
    seqs = list(product('SN', repeat=3))
    assert F(sum(w == ('S', 'S', 'N') for w in seqs), 8) == F(1, 8)
    assert sum(F(1, 2 ** k) for k in range(1, 40)) > F(999999, 1000000)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS048(ShortScene):
    N = 48

    def hook_visual(self, t0):
        self.c = coin('S', 1.2).move_to([0, 1.3, 0])
        self.play(FadeIn(self.c, scale=.6), run_time=self.rt(.05))
        self.wait_until(.35, t0)
        self.c = self.flip(self.c, 'NSSN', self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.c.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.c)
        seq = VGroup(*[VGroup(coin(f, .7), tx(f'lần {i + 1}', 24, SOFT)).arrange([0, -1, 0], buff=.15)
                       for i, f in enumerate('SSN')]).arrange(buff=.5).move_to([0, 1.3, 0])
        for s in seq:
            self.play(FadeIn(s, shift=[.3, 0, 0]), run_time=self.rt(.08))
        self.seq = seq
        self.wait_until(.65, t0)
        self.play(self.seq[2][0].animate.scale(1.2), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        m = self.M('seq', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        bars = VGroup(*[VGroup(self.TM(f'$1/{2 ** k}$', 26, CYAN), tx(f'dừng ở lần {k}', 22, SOFT))
                        .arrange(buff=.25) for k in range(1, 4)]).arrange([0, -1, 0], aligned_edge=[-1, 0, 0], buff=.15)
        self.write_board(bars, anim='fade')
        self.wait_until(.55, t0)
        self.write_board(self.M('sum', 1.9))
        self.play(self.board_items[-1].animate.set_color(GOLD), run_time=self.rt(.03))
