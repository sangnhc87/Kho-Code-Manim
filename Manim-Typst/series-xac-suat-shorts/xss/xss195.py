"""XSS195 · Bước lên cầu thang — p_n = (p_(n−1) + p_(n−2))/2: 1, 1/2, 3/4, 5/8, 11/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS195', 'answer': '11/16'}
PROBLEM = ['Mỗi bước lên $1$ hoặc $2$ bậc với',
           'xác suất như nhau. Xác suất chân',
           'chạm đúng bậc thứ $4$?']
OPTIONS = ['1/2', '11/16', '5/8']
CORRECT = 1
ANSWER_VALUE = 11 / 16


def touch(n=6):
    p = [F(1), F(1, 2)]
    for _ in range(2, n + 1):
        p.append((p[-1] + p[-2]) / 2)
    return p


BEATS = [
    Beat('hook', 'hook', 'Bạn leo cầu thang, mỗi bước ngẫu nhiên lên một bậc hoặc hai bậc, khả năng như nhau. '
                         'Xác suất chân bạn chạm đúng bậc thứ tư là bao nhiêu? Có thể bước qua nó!'),
    Beat('guess', 'hook', 'Một phần hai, mười một phần mười sáu, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi p n là xác suất chạm bậc n. Muốn chạm bậc n, bước cuối hoặc xuất phát từ bậc n trừ một và bước một bậc, '
                        'hoặc từ bậc n trừ hai và bước hai bậc.'),
    Beat('s2', 'solve', 'Vậy p n bằng một phần hai p n trừ một cộng một phần hai p n trừ hai. Với p không bằng một, p một bằng một phần hai: '
                        'p hai ba phần tư, p ba năm phần tám, p bốn mười một phần mười sáu.'),
    Beat('s3', 'solve', 'Dãy dao động và tiến về hai phần ba: mỗi bước trung bình dài một phẩy năm bậc, nên chạm khoảng hai phần ba số bậc.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần mười sáu. Quy hoạch động biến bài toán vô số đường đi thành một dãy truy hồi gọn gàng!'),
    Beat('outro', 'outro', outro_text(195)),
]

FORMULAS = formulas('11/16', OPTIONS,
                    rec='p_n = 1/2 p_(n-1) + 1/2 p_(n-2)',
                    vals='1, quad 1/2, quad 3/4, quad 5/8, quad 11/16',
                    lim='p_n arrow.r 2/3')


def validate() -> bool:
    exact = F(sum(4 in [sum(w[:k]) for k in range(5)] for w in product((1, 2), repeat=4)), 16)
    assert touch()[4] == exact == F(11, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS195(ShortScene):
    N = 195

    def hook_visual(self, t0):
        self.board_top = -1.2
        steps = VGroup()
        for k in range(7):
            x, y = -3.0 + .9 * k, -.3 + .5 * k
            steps.add(Line([x, y, 0], [x + .9, y, 0], color=GOLD if k == 4 else SOFT, stroke_width=6),
                      Line([x + .9, y, 0], [x + .9, y + .5, 0], color=SOFT, stroke_width=6))
        self.labs = VGroup(*[self.TM(f'${k}$', 22, GOLD if k == 4 else SOFT).move_to([-2.55 + .9 * k, -.05 + .5 * k, 0])
                             for k in range(7)])
        self.steps = steps
        self.wait_until(.5, t0)
        self.play(FadeIn(steps, lag_ratio=.05), FadeIn(self.labs), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        m = self.M('rec', 2.0)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('vals', 1.9))

    def beat_s3(self, T):
        self.write_board(self.M('lim', 2.0), anim='fade')
