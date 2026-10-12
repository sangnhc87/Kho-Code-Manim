"""XSS298 · Bước 1, 2, 3 bậc — Tribonacci: 13 cách lên 5 bậc; không dùng bước 3: Fibonacci 8 → 8/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS298', 'answer': '8/13'}
PROBLEM = ['Chọn ngẫu nhiên một cách lên $5$ bậc, mỗi',
           'bước $1$, $2$ hoặc $3$ bậc (mọi cách như',
           'nhau). Xác suất không dùng bước $3$ bậc?']
OPTIONS = ['1/2', '8/13', '5/13']
CORRECT = 1
ANSWER_VALUE = 8 / 13
WAYS = [w for n in range(6) for w in product((1, 2, 3), repeat=n) if sum(w) == 5]

BEATS = [
    Beat('hook', 'hook', 'Cầu thang năm bậc, mỗi bước được lên một, hai hoặc ba bậc. Chọn ngẫu nhiên một trong tất cả các cách lên. '
                         'Xác suất cách đó không có bước ba bậc nào?'),
    Beat('guess', 'hook', 'Một phần hai, tám phần mười ba, hay năm phần mười ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có thêm bước ba bậc thì số cách lên n bậc bằng tổng ba số trước: một, một, hai, bốn, bảy, mười ba. Năm bậc có mười ba cách.'),
    Beat('s2', 'solve', 'Không dùng bước ba bậc thì quay về Fibonacci: một, một, hai, ba, năm, tám. Có tám cách.'),
    Beat('s3', 'solve', 'Xác suất tám phần mười ba. Hai dãy truy hồi, một cho tử số, một cho mẫu số.'),
    Beat('answer', 'solve', 'Đáp án: tám phần mười ba. Thêm một kiểu bước là thêm một số hạng vào công thức truy hồi!'),
    Beat('outro', 'outro', outro_text(298)),
]

FORMULAS = formulas('8/13', OPTIONS,
                    tri='t_n = t_(n-1) + t_(n-2) + t_(n-3): 1, 1, 2, 4, 7, 13',
                    fib='f_n = f_(n-1) + f_(n-2): 1, 1, 2, 3, 5, 8',
                    prob='P = 8/13')


def validate() -> bool:
    assert len(WAYS) == 13 and F(sum(3 not in w for w in WAYS), 13) == F(8, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS298(ShortScene):
    N = 298

    def hook_visual(self, t0):
        self.board_top = -1.25
        steps = VGroup()
        for k in range(5):
            x, y = -2.5 + 1.0 * k, -.1 + .55 * k
            steps.add(Line([x, y, 0], [x + 1.0, y, 0], color=SOFT, stroke_width=6), Line([x + 1.0, y, 0], [x + 1.0, y + .55, 0], color=SOFT, stroke_width=6))
        self.wait_until(.55, t0)
        self.play(FadeIn(steps, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('tri', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('fib', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m, GOLD)
