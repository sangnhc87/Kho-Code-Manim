"""XSS299 · Bước dài hay bước ngắn — 1 bậc (1/3), 2 bậc (2/3): p = 1, 1/3, 7/9, 13/27, 55/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS299', 'answer': '55/81'}
PROBLEM = ['Mỗi bước lên $1$ bậc (xác suất $1/3$)',
           'hoặc $2$ bậc ($2/3$). Xác suất chân',
           'chạm đúng bậc thứ $4$?']
OPTIONS = ['11/16', '55/81', '2/3']
CORRECT = 1
ANSWER_VALUE = 55 / 81


def touch(n):
    p = [F(1), F(1, 3)]
    while len(p) <= n:
        p.append(F(1, 3) * p[-1] + F(2, 3) * p[-2])
    return p


BEATS = [
    Beat('hook', 'hook', 'Một người chân dài: mỗi bước lên hai bậc với xác suất hai phần ba, một bậc với xác suất một phần ba. '
                         'Xác suất chân người đó chạm đúng bậc thứ tư là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười một phần mười sáu, năm mươi lăm phần tám mươi mốt, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Như bài cầu thang trước, nhưng hai kiểu bước có trọng số khác nhau: p n bằng một phần ba p n trừ một cộng hai phần ba p n trừ hai.'),
    Beat('s2', 'solve', 'p không bằng một, p một bằng một phần ba, p hai bằng bảy phần chín, p ba bằng mười ba phần hai mươi bảy.'),
    Beat('s3', 'solve', 'p bốn bằng một phần ba nhân mười ba phần hai mươi bảy cộng hai phần ba nhân bảy phần chín, bằng năm mươi lăm phần tám mươi mốt. '
                        'Dãy tiến về ba phần năm, nghịch đảo bước trung bình năm phần ba.'),
    Beat('answer', 'solve', 'Đáp án: năm mươi lăm phần tám mươi mốt. Trọng số của mỗi bước đi thẳng vào công thức truy hồi!'),
    Beat('outro', 'outro', outro_text(299)),
]

FORMULAS = formulas('55/81', OPTIONS,
                    rec='p_n = 1/3 p_(n-1) + 2/3 p_(n-2)',
                    vals='1, quad 1/3, quad 7/9, quad 13/27, quad 55/81 arrow.r 3/5')


def validate() -> bool:
    exact = F(0)
    for n in range(1, 5):
        for w in product((1, 2), repeat=n):
            if sum(w) == 4:
                exact += F(1, 3) ** w.count(1) * F(2, 3) ** w.count(2)
    assert touch(4)[4] == exact == F(55, 81)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS299(ShortScene):
    N = 299

    def hook_visual(self, t0):
        self.board_top = -1.3
        steps = VGroup()
        for k in range(6):
            x, y = -2.7 + .9 * k, -.45 + .42 * k
            steps.add(Line([x, y, 0], [x + .9, y, 0], color=GOLD if k == 4 else SOFT, stroke_width=6),
                      Line([x + .9, y, 0], [x + .9, y + .42, 0], color=SOFT, stroke_width=6))
        self.wait_until(.6, t0)
        self.play(FadeIn(steps, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        m = self.M('rec', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        self.clear_board(.03)
        self.write_board(self.M('vals', 1.6))

    def beat_s3(self, T):
        self.play(self.board_items[0].animate.set_color(GOLD), run_time=self.rt(.05))
