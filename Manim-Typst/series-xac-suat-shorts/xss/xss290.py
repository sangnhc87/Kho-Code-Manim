"""XSS290 · Hai ếch gặp nhau — A ở 0, B ở 4; sau 2 giây gặp ⇔ A +2 và B −2: (1/4)(1/4) = 1/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS290', 'answer': '1/16'}
PROBLEM = ['Ếch A ở $0$, ếch B ở $4$; mỗi giây mỗi con',
           'nhảy $+1$ hoặc $-1$ ($1/2$), độc lập. Xác suất',
           'hai ếch gặp nhau sau đúng $2$ giây?']
OPTIONS = ['1/8', '1/16', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 16

BEATS = [
    Beat('hook', 'hook', 'Hai chú ếch trên cùng một hàng lá: A ở lá không, B ở lá bốn. Mỗi giây, mỗi con nhảy sang trái hoặc phải một lá, độc lập. '
                         'Xác suất hai con gặp nhau, đứng cùng một lá, sau đúng hai giây?'),
    Beat('guess', 'hook', 'Một phần tám, một phần mười sáu, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Khoảng cách ban đầu là bốn. Mỗi giây, mỗi con chỉ đi được một lá, nên khoảng cách giảm nhiều nhất hai mỗi giây.'),
    Beat('s2', 'solve', 'Muốn gặp sau hai giây, cả hai phải lao về nhau cả hai lần: A nhảy phải hai lần, B nhảy trái hai lần, cùng gặp ở lá hai.'),
    Beat('s3', 'solve', 'Bốn lần nhảy độc lập, mỗi lần một phần hai: một phần hai mũ bốn, bằng một phần mười sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười sáu. Hai vật đi ngẫu nhiên: xét khoảng cách giữa chúng, và lúc nào bắt buộc phải tiến lại gần!'),
    Beat('outro', 'outro', outro_text(290)),
]

FORMULAS = formulas('1/16', OPTIONS,
                    need='A: +1, +1, quad B: -1, -1',
                    prob='P = (1/2)^4 = 1/16')


def validate() -> bool:
    good = sum(w[0] + w[1] == 2 and w[2] + w[3] == -2 for w in product((1, -1), repeat=4))
    assert F(good, 16) == F(1, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS290(ShortScene):
    N = 290

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.row = pads(range(5), y=1.7)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, GOLD if k == 2 else SOFT).next_to(q, [0, -1, 0], buff=.15) for k, q in enumerate(self.row)])
        self.a = frog().move_to(self.row[0])
        self.b = frog()
        self.b[0].set_fill(CORAL)
        self.b.move_to(self.row[4])
        self.wait_until(.75, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.a, scale=2), FadeIn(self.b, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.TM('khoảng cách $4$, mỗi giây giảm tối đa $2$', 26, SOFT))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.a.animate.move_to(self.row[1]), self.b.animate.move_to(self.row[3]), run_time=self.rt(.06))
        self.play(self.a.animate.move_to(self.row[2]).shift([-.15, 0, 0]), self.b.animate.move_to(self.row[2]).shift([.15, 0, 0]),
                  run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('need', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
