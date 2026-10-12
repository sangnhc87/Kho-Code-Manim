"""XSS381 · Hai mặt giống nhau liền — dừng sau đúng 4 lần ⇔ 3 lần đầu xen kẽ (NSN hoặc SNS) và lần 4 lặp lại lần 3: 2/16 = 1/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS381', 'answer': '1/8'}
PROBLEM = ['Tung đồng xu đến khi có $2$ lần liên tiếp',
           'cùng mặt. Xác suất dừng sau đúng $4$ lần?']
OPTIONS = ['1/8', '1/4', '3/16']
CORRECT = 0
ANSWER_VALUE = 1 / 8


def stop(q):
    for i in range(1, len(q)):
        if q[i] == q[i - 1]:
            return i + 1


GOOD = [q for q in product('NS', repeat=4) if stop(q) == 4]

BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu liên tục cho đến khi có hai lần liên tiếp cùng mặt thì dừng. '
                         'Xác suất phải tung đúng bốn lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tám, một phần tư, hay ba phần mười sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chưa dừng sau ba lần nghĩa là ba lần đầu xen kẽ: ngửa sấp ngửa, hoặc sấp ngửa sấp. Chỉ hai dãy.'),
    Beat('s2', 'solve', 'Lần thứ tư phải lặp lại mặt thứ ba. Vậy có đúng hai dãy bốn lần trong mười sáu dãy đồng khả năng.'),
    Beat('s3', 'solve', 'Xác suất hai phần mười sáu, tức một phần tám. Tổng quát, dừng ở lần k có xác suất một phần hai mũ k trừ một.'),
    Beat('answer', 'solve', 'Đáp án: một phần tám. Điều kiện chưa dừng ép dãy phải xen kẽ, nên đếm rất nhanh.'),
    Beat('outro', 'outro', outro_text(381)),
]

FORMULAS = formulas('1/8', OPTIONS,
                    prob='P = 2/2^4 = 1/8',
                    gen='P(T = k) = 1/2^(k-1)')


def validate() -> bool:
    assert len(GOOD) == 2 and F(len(GOOD), 16) == F(1, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS381(ShortScene):
    N = 381

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[coin(c, .42) for c in q]).arrange(buff=.3) for q in GOOD]).arrange(DOWN, buff=.45).move_to([0, 1.2, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows[0][:2], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[0][2]), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows[1][:3], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[0][3]), FadeIn(self.rows[1][3]), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('gen', 1.4), anim='fade')
