"""XSS281 · Ếch nhảy 1, 2, 3 lá — quy hoạch động: p_k = (p_(k−1) + p_(k−2) + p_(k−3))/3: 1, 1/3, 4/9, 16/27, 37/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS281', 'answer': '37/81'}
PROBLEM = ['Ếch ở lá $0$, mỗi lần nhảy tới $1$,',
           '$2$ hoặc $3$ lá (như nhau). Xác suất',
           'ếch đáp đúng lá số $4$?']
OPTIONS = ['1/3', '37/81', '1/2']
CORRECT = 1
ANSWER_VALUE = 37 / 81


def land(n):
    p = [F(1)]
    for k in range(1, n + 1):
        p.append(sum(p[k - s] for s in (1, 2, 3) if k - s >= 0) / 3)
    return p


BEATS = [
    Beat('hook', 'hook', 'Mở đầu nhánh vận dụng cao. Chú ếch ở lá sen số không, mỗi lần nhảy tới một, hai hoặc ba lá, khả năng như nhau. '
                         'Xác suất ếch đáp đúng lá số bốn, không nhảy vượt qua, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, ba mươi bảy phần tám mươi mốt, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Quy hoạch động: gọi p k là xác suất ếch có lúc đáp lá k. Muốn đáp lá k, cú nhảy cuối xuất phát từ lá k trừ một, k trừ hai, hoặc k trừ ba, '
                        'mỗi cách một phần ba.'),
    Beat('s2', 'solve', 'Vậy p k bằng trung bình ba số trước nó. p không bằng một; p một bằng một phần ba; p hai bằng bốn phần chín; p ba bằng mười sáu phần hai mươi bảy.'),
    Beat('s3', 'solve', 'p bốn bằng một phần ba nhân tổng ba số trước, bằng ba mươi bảy phần tám mươi mốt. Dãy tiến dần về một phần hai, nghịch đảo bước nhảy trung bình.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi bảy phần tám mươi mốt. Mỗi ô chỉ cần nhìn vài ô ngay trước nó: đó là sức mạnh của quy hoạch động!'),
    Beat('outro', 'outro', outro_text(281)),
]

FORMULAS = formulas('37/81', OPTIONS,
                    rec='p_k = 1/3 (p_(k-1) + p_(k-2) + p_(k-3))',
                    vals='1, quad 1/3, quad 4/9, quad 16/27, quad 37/81')


def validate() -> bool:
    brute = F(0)
    for n in range(1, 5):
        for w in product((1, 2, 3), repeat=n):
            if sum(w) == 4 and all(sum(w[:i]) < 4 for i in range(n)):
                brute += F(1, 3 ** n)
    assert land(4)[4] == brute == F(37, 81)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS281(ShortScene):
    N = 281

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(5), y=1.7)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, GOLD if k == 4 else SOFT).next_to(p, [0, -1, 0], buff=.15)
                             for k, p in enumerate(self.row)])
        self.fr = frog().move_to(self.row[0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.row, lag_ratio=.1), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.1))
        for k in (1, 3, 4):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.fr.animate.move_to(self.row[0]), run_time=self.rt(.04))
        self.wait_until(.55, t0)
        m = self.M('rec', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        probs = VGroup(*[self.TM(f'${v}$', 22, GOLD).next_to(lab, [0, -1, 0], buff=.12)
                         for v, lab in zip(('1', '1/3', '4/9', '16/27', '?'), self.labs)])
        self.play(FadeIn(probs, lag_ratio=.25), run_time=self.rt(.2))
        self.probs = probs

    def beat_s3(self, T):
        self.clear_board(.03)
        self.play(self.probs[4].animate.become(self.TM('$37/81$', 22, GOLD).move_to(self.probs[4])), run_time=self.rt(.05))
        m = self.M('vals', 1.8)
        self.write_board(m)
        self.frame(m)
