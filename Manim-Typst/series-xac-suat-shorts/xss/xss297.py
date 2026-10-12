"""XSS297 · Lên 6 bậc — 13 cách (Fibonacci); dùng đúng hai bước 2: C(4,2) = 6 → 6/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS297', 'answer': '6/13'}
PROBLEM = ['Chọn ngẫu nhiên một cách lên $6$ bậc',
           'thang, mỗi bước $1$ hoặc $2$ bậc (mọi cách',
           'như nhau). Xác suất dùng đúng hai bước $2$',
           'bậc?']
OPTIONS = ['5/13', '6/13', '1/2']
CORRECT = 1
ANSWER_VALUE = 6 / 13
WAYS = [w for n in range(7) for w in product((1, 2), repeat=n) if sum(w) == 6]

BEATS = [
    Beat('hook', 'hook', 'Lên cầu thang sáu bậc, mỗi bước một hoặc hai bậc. Tất cả các cách lên được liệt kê, rồi chọn ngẫu nhiên một cách. '
                         'Xác suất cách đó dùng đúng hai bước dài là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần mười ba, sáu phần mười ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm số cách bằng quy hoạch động: số cách lên n bậc bằng số cách lên n trừ một cộng n trừ hai. Một, hai, ba, năm, tám, mười ba: Fibonacci!'),
    Beat('s2', 'solve', 'Phân loại theo số bước hai bậc: không bước dài, một cách; một bước dài, năm cách; hai bước dài, bốn bước tất cả, sáu cách; ba bước dài, một cách.'),
    Beat('s3', 'solve', 'Một cộng năm cộng sáu cộng một bằng mười ba, khớp với Fibonacci. Xác suất sáu phần mười ba.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười ba. Đếm hai cách, quy hoạch động và tổ hợp, rồi kiểm tra chéo!'),
    Beat('outro', 'outro', outro_text(297)),
]

FORMULAS = formulas('6/13', OPTIONS,
                    fib='a_n = a_(n-1) + a_(n-2): 1, 2, 3, 5, 8, 13',
                    split='C_6^0 + C_5^1 + C_4^2 + C_3^3 = 1 + 5 + 6 + 1 = 13',
                    prob='P = (C_4^2)/13 = 6/13')


def validate() -> bool:
    assert len(WAYS) == 13 and F(sum(w.count(2) == 2 for w in WAYS), 13) == F(6, 13) == F(comb(4, 2), 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS297(ShortScene):
    N = 297

    def hook_visual(self, t0):
        self.board_top = -1.25
        steps = VGroup()
        for k in range(6):
            x, y = -2.7 + .9 * k, -.2 + .5 * k
            steps.add(Line([x, y, 0], [x + .9, y, 0], color=SOFT, stroke_width=6), Line([x + .9, y, 0], [x + .9, y + .5, 0], color=SOFT, stroke_width=6))
        self.steps = steps
        self.wait_until(.55, t0)
        self.play(FadeIn(steps, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('fib', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.3, t0)
        self.write_board(self.M('split', 1.4))

    def beat_s3(self, T):
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)
