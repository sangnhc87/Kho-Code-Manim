"""XSS387 · Đến khi gặp số chẵn — 6 bi số 1..6; T ≥ 2 ⇔ lần 1 lẻ (1/2); T = 3: lẻ, lẻ, chẵn = 3/6·2/5·3/4 = 3/20 → 3/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS387', 'answer': '3/10'}
PROBLEM = ['Rút lần lượt từ $6$ bi số $1$ đến $6$ đến khi',
           'gặp số chẵn. Biết cần ít nhất $2$ lần. Xác',
           'suất cần đúng $3$ lần?']
OPTIONS = ['3/10', '1/3', '3/20']
CORRECT = 0
ANSWER_VALUE = .3


def first_even(o):
    return next(i for i, v in enumerate(o) if v % 2 == 0) + 1


ORD = [o for o in permutations(range(1, 7)) if first_even(o) >= 2]

BEATS = [
    Beat('hook', 'hook', 'Sáu bi đánh số một đến sáu. Rút lần lượt không hoàn lại cho đến khi gặp số chẵn. Biết cần ít nhất hai lần rút. '
                         'Xác suất cần đúng ba lần?'),
    Beat('guess', 'hook', 'Ba phần mười, một phần ba, hay ba phần hai mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cần ít nhất hai lần nghĩa là lần một rút số lẻ: xác suất ba phần sáu, một phần hai.'),
    Beat('s2', 'solve', 'Cần đúng ba lần: lẻ, lẻ, rồi chẵn. Ba phần sáu nhân hai phần năm nhân ba phần bốn, bằng ba phần hai mươi.'),
    Beat('s3', 'solve', 'Chia cho một phần hai: ba phần mười. Hoặc nghĩ trực tiếp: biết lần một lẻ, còn hai lẻ ba chẵn, lần hai lẻ rồi lần ba chẵn: hai phần năm nhân ba phần tư.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười. Điều kiện ở lần đầu chỉ là bắt đầu lại với một hộp nhỏ hơn.'),
    Beat('outro', 'outro', outro_text(387)),
]

FORMULAS = formulas('3/10', OPTIONS,
                    cond='P(T >= 2) = 3/6 = 1/2',
                    t3='P(T = 3) = 3/6 dot 2/5 dot 3/4 = 3/20',
                    prob='P(T = 3 | T >= 2) = (3/20)/(1/2) = 3/10')


def validate() -> bool:
    assert F(sum(first_even(o) == 3 for o in ORD), len(ORD)) == F(3, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS387(ShortScene):
    N = 387

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.pool = ball_row('BRBRBR', y=1.9, r=.34, buff=.15, labels=[1, 2, 3, 4, 5, 6])
        self.play(FadeIn(self.pool, lag_ratio=.1), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.row = ball_row('BBR', y=.5, r=.4, buff=.45, labels=[5, 1, 4], size=28)
        self.wait_until(.3, t0)
        self.play(FadeIn(self.row[0]), run_time=self.rt(.06))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.row[1:], lag_ratio=.4), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('t3', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
